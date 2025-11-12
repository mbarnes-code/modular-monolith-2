import { Request, Response } from 'express';
import { OnexService } from '../../lib';

export class CategoriesController {
  constructor(private onexService: OnexService) {}

  async getAllCategories(req: Request, res: Response): Promise<void> {
    try {
      const categories = this.onexService.getAllCategories();
      res.json({
        success: true,
        data: categories,
        count: categories.length
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve categories',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  async getToolsByCategory(req: Request, res: Response): Promise<void> {
    try {
      const { key } = req.params;
      const tools = this.onexService.getToolsByCategory(key);
      
      res.json({
        success: true,
        data: tools,
        count: tools.length,
        category: key
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve tools for category',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }
}
