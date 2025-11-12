import { ApiResponse, BlackArchPackage, PaginatedResponse } from 'blackarch';
import { Request, Response } from 'express';
import { configService } from '../config/config.service';
import { blackArchService } from '../services/blackarch.service';

export class BlackArchController {
  
  public async getStats(req: Request, res: Response<ApiResponse<any>>): Promise<void> {
    try {
      const stats = blackArchService.getStats();
      res.json({
        success: true,
        data: stats
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Internal server error'
      });
    }
  }
  
  public async getAllPackages(req: Request, res: Response<PaginatedResponse<BlackArchPackage>>): Promise<void> {
    try {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || configService.blackarchConfig.defaultPageSize;
      const group = req.query.group as string;
      
      const allPackages = blackArchService.getPackagesByGroup(group);
      const total = allPackages.length;
      const totalPages = Math.ceil(total / limit);
      const offset = (page - 1) * limit;
      const packages = allPackages.slice(offset, offset + limit);
      
      res.json({
        success: true,
        data: packages,
        pagination: {
          page,
          limit,
          total,
          totalPages,
          hasNext: page < totalPages,
          hasPrev: page > 1
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Internal server error',
        data: [],
        pagination: {
          page: 1,
          limit: configService.blackarchConfig.defaultPageSize,
          total: 0,
          totalPages: 0,
          hasNext: false,
          hasPrev: false
        }
      });
    }
  }
  
  public async getPackage(req: Request, res: Response<ApiResponse<BlackArchPackage>>): Promise<void> {
    try {
      const { name } = req.params;
      const pkg = blackArchService.getPackage(name);
      
      if (!pkg) {
        res.status(404).json({
          success: false,
          error: `Package '${name}' not found`
        });
        return;
      }
      
      res.json({
        success: true,
        data: pkg
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Internal server error'
      });
    }
  }
  
  public async searchPackages(req: Request, res: Response<PaginatedResponse<BlackArchPackage>>): Promise<void> {
    try {
      const query = req.query.q as string;
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || configService.blackarchConfig.defaultPageSize;
      
      if (!query) {
        res.status(400).json({
          success: false,
          error: 'Query parameter "q" is required',
          data: [],
          pagination: {
            page: 1,
            limit,
            total: 0,
            totalPages: 0,
            hasNext: false,
            hasPrev: false
          }
        });
        return;
      }
      
      const allResults = blackArchService.searchPackages(query);
      const total = allResults.length;
      const totalPages = Math.ceil(total / limit);
      const offset = (page - 1) * limit;
      const packages = allResults.slice(offset, offset + limit);
      
      res.json({
        success: true,
        data: packages,
        pagination: {
          page,
          limit,
          total,
          totalPages,
          hasNext: page < totalPages,
          hasPrev: page > 1
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Internal server error',
        data: [],
        pagination: {
          page: 1,
          limit: configService.blackarchConfig.defaultPageSize,
          total: 0,
          totalPages: 0,
          hasNext: false,
          hasPrev: false
        }
      });
    }
  }
  
  public async getGroups(req: Request, res: Response<ApiResponse<string[]>>): Promise<void> {
    try {
      const groups = blackArchService.getGroups();
      res.json({
        success: true,
        data: groups
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: error instanceof Error ? error.message : 'Internal server error'
      });
    }
  }
}

export const blackArchController = new BlackArchController();