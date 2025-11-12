import { BlackArchPackage, BlackArchStats } from 'blackarch';
import * as fs from 'fs';
import { BlackArchService } from './blackarch.service';

// Mock fs module
jest.mock('fs');
const mockFs = fs as jest.Mocked<typeof fs>;

describe('BlackArchService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    
    // Mock successful directory structure
    mockFs.existsSync.mockImplementation((path: string) => {
      return path.includes('blackarch');
    });
    
    mockFs.readdirSync.mockImplementation((dir: string) => {
      if (dir.includes('blackarch')) {
        return [
          { name: 'test-package', isDirectory: () => true } as any,
          { name: 'PKGBUILD', isDirectory: () => false } as any,
        ];
      }
      if (dir.includes('test-package')) {
        return [
          { name: 'PKGBUILD', isDirectory: () => false } as any,
        ];
      }
      return [];
    });
    
    mockFs.readFileSync.mockImplementation((path: string) => {
      if (path.includes('PKGBUILD')) {
        return `
pkgname=test-package
pkgver=1.0.0
pkgrel=1
pkgdesc="Test package description"
url="https://example.com"
license=('MIT')
arch=('x86_64')
depends=('base')
groups=('blackarch-test')
        `.trim();
      }
      return '';
    });
  });

  describe('initialization', () => {
    it('should initialize and load packages', () => {
      const service = new BlackArchService();
      expect(service).toBeInstanceOf(BlackArchService);
    });

    it('should find repository path', () => {
      expect(() => new BlackArchService()).not.toThrow();
    });
  });

  describe('getStats', () => {
    it('should return repository statistics', () => {
      const service = new BlackArchService();
      const stats: BlackArchStats = service.getStats();
      
      expect(stats).toHaveProperty('total');
      expect(stats).toHaveProperty('official');
      expect(stats).toHaveProperty('broken');
      expect(stats).toHaveProperty('working');
      expect(typeof stats.total).toBe('number');
      expect(typeof stats.official).toBe('number');
      expect(typeof stats.broken).toBe('number');
      expect(typeof stats.working).toBe('number');
    });
  });

  describe('getAllPackages', () => {
    it('should return all packages', () => {
      const service = new BlackArchService();
      const packages: BlackArchPackage[] = service.getAllPackages();
      
      expect(Array.isArray(packages)).toBe(true);
    });
  });

  describe('getPackage', () => {
    it('should return a specific package', () => {
      const service = new BlackArchService();
      const pkg = service.getPackage('test-package');
      
      expect(pkg).toBeDefined();
      if (pkg) {
        expect(pkg.name).toBe('test-package');
        expect(pkg.version).toBe('1.0.0');
        expect(pkg.description).toBe('Test package description');
      }
    });

    it('should return undefined for non-existent package', () => {
      const service = new BlackArchService();
      const pkg = service.getPackage('non-existent-package');
      
      expect(pkg).toBeUndefined();
    });
  });

  describe('searchPackages', () => {
    it('should search packages by name', () => {
      const service = new BlackArchService();
      const results = service.searchPackages('test');
      
      expect(Array.isArray(results)).toBe(true);
    });

    it('should search packages by description', () => {
      const service = new BlackArchService();
      const results = service.searchPackages('description');
      
      expect(Array.isArray(results)).toBe(true);
    });

    it('should return empty array for no matches', () => {
      const service = new BlackArchService();
      const results = service.searchPackages('xyz123nonexistent');
      
      expect(results).toEqual([]);
    });
  });

  describe('getPackagesByGroup', () => {
    it('should return packages by group', () => {
      const service = new BlackArchService();
      const packages = service.getPackagesByGroup('blackarch-test');
      
      expect(Array.isArray(packages)).toBe(true);
    });

    it('should return all packages when no group specified', () => {
      const service = new BlackArchService();
      const allPackages = service.getAllPackages();
      const packagesNoGroup = service.getPackagesByGroup();
      
      expect(packagesNoGroup).toEqual(allPackages);
    });
  });

  describe('getGroups', () => {
    it('should return list of groups', () => {
      const service = new BlackArchService();
      const groups = service.getGroups();
      
      expect(Array.isArray(groups)).toBe(true);
      expect(groups.every(group => typeof group === 'string')).toBe(true);
    });

    it('should return sorted groups', () => {
      const service = new BlackArchService();
      const groups = service.getGroups();
      
      const sortedGroups = [...groups].sort();
      expect(groups).toEqual(sortedGroups);
    });
  });
});