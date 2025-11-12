import * as fs from 'fs';
import * as path from 'path';
import { Category, Tool } from '../types/tool.types';

export class DataService {
  private toolsData: Tool[] = [];
  private categoriesData: Category[] = [];
  private readonly assetsPath: string;

  constructor() {
    // Try multiple possible asset locations
    const possiblePaths = [
      path.join(__dirname, '../assets'),
      path.join(__dirname, '../../assets'), 
      path.join(__dirname, '../../../assets'),
      path.join(process.cwd(), 'libs/onex-core/src/lib/assets'),
      path.join(process.cwd(), 'dist/libs/onex-core/assets')
    ];

    this.assetsPath = possiblePaths.find(assetPath => {
      const toolsFile = path.join(assetPath, 'tools.dat');
      return fs.existsSync(toolsFile);
    }) || possiblePaths[0];

    this.loadData();
  }

  private loadData(): void {
    this.loadTools();
    this.loadCategories();
  }

  private loadTools(): void {
    const toolsFile = path.join(this.assetsPath, 'tools.dat');
    
    if (!fs.existsSync(toolsFile)) {
      throw new Error(`Tools data file not found: ${toolsFile}`);
    }

    const content = fs.readFileSync(toolsFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());

    this.toolsData = lines.map(line => {
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
  }

  private loadCategories(): void {
    const categoriesFile = path.join(this.assetsPath, 'category.dat');
    
    if (!fs.existsSync(categoriesFile)) {
      throw new Error(`Categories data file not found: ${categoriesFile}`);
    }

    const content = fs.readFileSync(categoriesFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());

    this.categoriesData = lines.map(line => {
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