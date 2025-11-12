import { BlackArchPackage, BlackArchStats } from 'blackarch';
import { Request, Response } from 'express';
import { blackArchService } from '../services/blackarch.service';
import { BlackArchController } from './blackarch.controller';

// Mock the blackArchService
jest.mock('../services/blackarch.service');
const mockBlackArchService = blackArchService as jest.Mocked<typeof blackArchService>;

describe('BlackArchController', () => {
  let controller: BlackArchController;
  let mockRequest: Partial<Request>;
  let mockResponse: Partial<Response>;
  let mockJson: jest.Mock;
  let mockStatus: jest.Mock;

  beforeEach(() => {
    controller = new BlackArchController();
    
    mockJson = jest.fn();
    mockStatus = jest.fn().mockReturnValue({ json: mockJson });
    
    mockRequest = {};
    mockResponse = {
      json: mockJson,
      status: mockStatus,
    };
    
    jest.clearAllMocks();
  });

  describe('getStats', () => {
    it('should return statistics successfully', async () => {
      const mockStats: BlackArchStats = {
        total: 100,
        official: 80,
        broken: 5,
        working: 95
      };
      
      mockBlackArchService.getStats.mockReturnValue(mockStats);
      
      await controller.getStats(mockRequest as Request, mockResponse as Response);
      
      expect(mockBlackArchService.getStats).toHaveBeenCalled();
      expect(mockJson).toHaveBeenCalledWith({
        success: true,
        data: mockStats
      });
    });

    it('should handle errors', async () => {
      const error = new Error('Test error');
      mockBlackArchService.getStats.mockImplementation(() => {
        throw error;
      });
      
      await controller.getStats(mockRequest as Request, mockResponse as Response);
      
      expect(mockStatus).toHaveBeenCalledWith(500);
      expect(mockJson).toHaveBeenCalledWith({
        success: false,
        error: 'Test error'
      });
    });
  });

  describe('getPackage', () => {
    it('should return package successfully', async () => {
      const mockPackage: BlackArchPackage = {
        name: 'test-package',
        version: '1.0.0',
        release: '1',
        description: 'Test package',
        url: 'https://example.com',
        license: ['MIT'],
        arch: ['x86_64'],
        depends: [],
        groups: ['test'],
        path: '/test/path'
      };
      
      mockRequest.params = { name: 'test-package' };
      mockBlackArchService.getPackage.mockReturnValue(mockPackage);
      
      await controller.getPackage(mockRequest as Request, mockResponse as Response);
      
      expect(mockBlackArchService.getPackage).toHaveBeenCalledWith('test-package');
      expect(mockJson).toHaveBeenCalledWith({
        success: true,
        data: mockPackage
      });
    });

    it('should return 404 for non-existent package', async () => {
      mockRequest.params = { name: 'non-existent' };
      mockBlackArchService.getPackage.mockReturnValue(undefined);
      
      await controller.getPackage(mockRequest as Request, mockResponse as Response);
      
      expect(mockStatus).toHaveBeenCalledWith(404);
      expect(mockJson).toHaveBeenCalledWith({
        success: false,
        error: "Package 'non-existent' not found"
      });
    });
  });

  describe('searchPackages', () => {
    it('should search packages successfully', async () => {
      const mockPackages: BlackArchPackage[] = [{
        name: 'test-package',
        version: '1.0.0',
        release: '1',
        description: 'Test package',
        url: 'https://example.com',
        license: ['MIT'],
        arch: ['x86_64'],
        depends: [],
        groups: ['test'],
        path: '/test/path'
      }];
      
      mockRequest.query = { q: 'test', page: '1', limit: '10' };
      mockBlackArchService.searchPackages.mockReturnValue(mockPackages);
      
      await controller.searchPackages(mockRequest as Request, mockResponse as Response);
      
      expect(mockBlackArchService.searchPackages).toHaveBeenCalledWith('test');
      expect(mockJson).toHaveBeenCalledWith({
        success: true,
        data: mockPackages,
        pagination: {
          page: 1,
          limit: 10,
          total: 1,
          totalPages: 1,
          hasNext: false,
          hasPrev: false
        }
      });
    });

    it('should return 400 for missing query', async () => {
      mockRequest.query = {};
      
      await controller.searchPackages(mockRequest as Request, mockResponse as Response);
      
      expect(mockStatus).toHaveBeenCalledWith(400);
      expect(mockJson).toHaveBeenCalledWith({
        success: false,
        error: 'Query parameter "q" is required',
        data: [],
        pagination: expect.any(Object)
      });
    });
  });

  describe('getGroups', () => {
    it('should return groups successfully', async () => {
      const mockGroups = ['group1', 'group2', 'group3'];
      mockBlackArchService.getGroups.mockReturnValue(mockGroups);
      
      await controller.getGroups(mockRequest as Request, mockResponse as Response);
      
      expect(mockBlackArchService.getGroups).toHaveBeenCalled();
      expect(mockJson).toHaveBeenCalledWith({
        success: true,
        data: mockGroups
      });
    });

    it('should handle errors', async () => {
      const error = new Error('Test error');
      mockBlackArchService.getGroups.mockImplementation(() => {
        throw error;
      });
      
      await controller.getGroups(mockRequest as Request, mockResponse as Response);
      
      expect(mockStatus).toHaveBeenCalledWith(500);
      expect(mockJson).toHaveBeenCalledWith({
        success: false,
        error: 'Test error'
      });
    });
  });
});