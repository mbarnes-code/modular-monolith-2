import { Request, Response } from 'express';
import { OnexService } from '../../lib';

export class ToolsController {
  constructor(private onexService: OnexService) {}

  async getAllTools(req: Request, res: Response): Promise<void> {
    try {
      const tools = this.onexService.getAllTools();
      res.json({
        success: true,
        data: tools,
        count: tools.length
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve tools',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  async searchTools(req: Request, res: Response): Promise<void> {
    try {
      const query = req.query.q as string;
      
      if (!query) {
        res.status(400).json({
          success: false,
          message: 'Search query is required (use ?q=search_term)'
        });
        return;
      }

      const tools = this.onexService.searchTools(query);
      res.json({
        success: true,
        data: tools,
        count: tools.length,
        query
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to search tools',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  async getToolByName(req: Request, res: Response): Promise<void> {
    try {
      const { name } = req.params;
      const tool = this.onexService.getToolByName(name);
      
      if (!tool) {
        const suggestions = this.onexService.searchTools(name);
        res.status(404).json({
          success: false,
          message: `Tool '${name}' not found`,
          suggestions: suggestions.slice(0, 5).map(t => t.name)
        });
        return;
      }

      res.json({
        success: true,
        data: tool
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve tool',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  async installTool(req: Request, res: Response): Promise<void> {
    try {
      const { name } = req.params;
      const result = await this.onexService.installTool(name);
      
      res.status(result.success ? 200 : 400).json({
        success: result.success,
        message: result.message,
        toolName: result.toolName
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Installation failed',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }
}
