import { Request, Response } from 'express';
import { OnexService } from '../../lib';

export class SystemController {
  constructor(private onexService: OnexService) {}

  async getSystemInfo(req: Request, res: Response): Promise<void> {
    try {
      const systemInfo = this.onexService.getSystemInfo();
      res.json({
        success: true,
        data: systemInfo
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve system information',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  async getStats(req: Request, res: Response): Promise<void> {
    try {
      const stats = this.onexService.getStats();
      res.json({
        success: true,
        data: stats
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        message: 'Failed to retrieve statistics',
        error: error instanceof Error ? error.message : 'Unknown error'
      });
    }
  }

  async healthCheck(req: Request, res: Response): Promise<void> {
    try {
      const isOnline = await this.onexService.isOnline();
      const stats = this.onexService.getStats();
      
      res.json({
        success: true,
        status: 'healthy',
        online: isOnline,
        timestamp: new Date().toISOString(),
        stats
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        status: 'unhealthy',
        message: error instanceof Error ? error.message : 'Unknown error',
        timestamp: new Date().toISOString()
      });
    }
  }
}
