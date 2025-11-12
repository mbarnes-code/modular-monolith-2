import { Category, InstallResult, SystemInfo, Tool } from '../types/tool.types';
import { DataService } from './data.service';
import { SystemService } from './system.service';

export class OnexService {
  private dataService: DataService;
  private systemService: SystemService;

  constructor() {
    this.dataService = new DataService();
    this.systemService = new SystemService();
  }

  public getSystemInfo(): SystemInfo {
    return this.systemService.getSystemInfo();
  }

  public getAllTools(): Tool[] {
    return this.dataService.getAllTools();
  }

  public getAllCategories(): Category[] {
    return this.dataService.getAllCategories();
  }

  public getToolsByCategory(categoryKey: string): Tool[] {
    return this.dataService.getToolsByCategory(categoryKey);
  }

  public searchTools(query: string): Tool[] {
    return this.dataService.searchTools(query);
  }

  public getToolByName(name: string): Tool | undefined {
    return this.dataService.getToolByName(name);
  }

  public async installTool(toolName: string): Promise<InstallResult> {
    const tool = this.dataService.getToolByName(toolName);
    
    if (!tool) {
      const similarTools = this.dataService.searchTools(toolName);
      const suggestions = similarTools.length > 0 
        ? `\nDid you mean: ${similarTools.slice(0, 5).map(t => t.name).join(', ')}`
        : '';
      
      return {
        success: false,
        message: `Sorry: '${toolName}' tool not found !!${suggestions}`,
        toolName
      };
    }

    return await this.systemService.installTool(tool);
  }

  public getStats(): { toolsCount: number; categoriesCount: number } {
    return {
      toolsCount: this.dataService.getToolsCount(),
      categoriesCount: this.dataService.getCategoriesCount()
    };
  }

  public async isOnline(): Promise<boolean> {
    return await this.systemService.checkOnlineStatus();
  }
}
