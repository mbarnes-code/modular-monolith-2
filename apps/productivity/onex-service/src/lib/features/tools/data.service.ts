import * as fs from 'fs';
import * as path from 'path';
import { Category, Tool } from '../../shared/types/tool.types';

export class DataService {
  private toolsData: Tool[] = [];
  private categoriesData: Category[] = [];
  private readonly assetsPath: string;

  constructor() {
    this.assetsPath = path.join(__dirname, '../../shared/assets');
    this.loadData();
  }

  private loadData(): void {
    this.toolsData = this.loadTools();
    this.categoriesData = this.loadCategories();
  }

  private loadTools(): Tool[] {
    // Try multiple paths to handle different build configurations
    const possiblePaths = [
      path.join(__dirname, '../../shared/assets/tools.dat'),  // Development
      path.join(__dirname, '../../../../../apps/onex-service/src/lib/shared/assets/tools.dat'),  // Built CLI
      path.join(process.cwd(), 'apps/onex-service/src/lib/shared/assets/tools.dat'),  // From workspace root
      path.join(process.cwd(), 'src/lib/shared/assets/tools.dat')  // Alternative
    ];
    
    let toolsFile = '';
    for (const filePath of possiblePaths) {
      if (fs.existsSync(filePath)) {
        toolsFile = filePath;
        break;
      }
    }
    
    if (!fs.existsSync(toolsFile)) {
      throw new Error(`Tools data file not found: ${toolsFile}`);
    }

    const content = fs.readFileSync(toolsFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());

    const toolsData = lines.map(line => {
      const parts = line.split('|');
      
      if (parts.length < 6) {
        console.warn(`Invalid tool data line: ${line}`);
        return null;
      }

      const [name, packageName, category, url, installer, dependencies] = parts;
      
      return {
        name: name.trim(),
        packageName: packageName.trim(),
        category: category.trim() === 'null' ? null : category.trim(),
        url: url.trim(),
        installer: installer.trim() as any,
        dependencies: dependencies.trim() === 'null' ? [] : dependencies.trim().split(',').map(dep => dep.trim())
      };
    }).filter((tool): tool is Tool => tool !== null);
    
    return toolsData;
  }

  private loadCategories(): Category[] {
    // Try multiple paths to handle different build configurations
    const possiblePaths = [
      path.join(__dirname, '../../shared/assets/category.dat'),  // Development
      path.join(__dirname, '../../../../../apps/onex-service/src/lib/shared/assets/category.dat'),  // Built CLI
      path.join(process.cwd(), 'apps/onex-service/src/lib/shared/assets/category.dat'),  // From workspace root
      path.join(process.cwd(), 'src/lib/shared/assets/category.dat')  // Alternative
    ];
    
    let categoriesFile = '';
    for (const filePath of possiblePaths) {
      if (fs.existsSync(filePath)) {
        categoriesFile = filePath;
        break;
      }
    }
    
    if (!fs.existsSync(categoriesFile)) {
      throw new Error(`Categories data file not found: ${categoriesFile}`);
    }

    const content = fs.readFileSync(categoriesFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());

    const categoriesData = lines.map(line => {
      const parts = line.split('|');
      
      if (parts.length < 2) {
        console.warn(`Invalid category data line: ${line}`);
        return null;
      }

      const [displayName, key] = parts;
      
      return {
        displayName: displayName.trim(),
        key: key.trim()
      };
    }).filter((category): category is Category => category !== null);
    
    return categoriesData;
  }

  public getAllTools(): Tool[] {
    return [...this.toolsData];
  }

  public getAllCategories(): Category[] {
    return [...this.categoriesData];
  }

  public getToolsByCategory(categoryKey: string): Tool[] {
    return this.toolsData.filter(tool => tool.category === categoryKey);
  }

  public searchTools(query: string): Tool[] {
    const searchTerm = query.toLowerCase();
    return this.toolsData.filter(tool => 
      tool.name.toLowerCase().includes(searchTerm) ||
      tool.packageName.toLowerCase().includes(searchTerm)
    );
  }

  public getToolByName(name: string): Tool | undefined {
    return this.toolsData.find(tool => 
      tool.name.toLowerCase() === name.toLowerCase()
    );
  }

  public getToolsCount(): number {
    return this.toolsData.length;
  }

  public getCategoriesCount(): number {
    return this.categoriesData.length;
  }
}