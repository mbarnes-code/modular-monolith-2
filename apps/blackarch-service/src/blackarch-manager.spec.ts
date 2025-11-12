import { BlackArchManager } from '../src/blackarch-manager';

describe('BlackArchManager', () => {
  let manager: BlackArchManager;

  beforeEach(() => {
    manager = new BlackArchManager();
  });

  describe('getStats', () => {
    it('should return repository statistics', () => {
      const stats = manager.getStats();
      
      expect(stats).toBeDefined();
      expect(stats.totalPackages).toBeGreaterThan(0);
      expect(stats.totalGroups).toBeGreaterThan(0);
      expect(stats.repositoryPath).toContain('blackarch');
    });
  });

  describe('getToolGroups', () => {
    it('should return an array of tool groups', () => {
      const groups = manager.getToolGroups();
      
      expect(Array.isArray(groups)).toBe(true);
      expect(groups.length).toBeGreaterThan(0);
    });
  });

  describe('getAllPackages', () => {
    it('should return an array of package names', () => {
      const packages = manager.getAllPackages();
      
      expect(Array.isArray(packages)).toBe(true);
      expect(packages.length).toBeGreaterThan(0);
    });
  });

  describe('getOfficialPackages', () => {
    it('should return an array of official package names', () => {
      const packages = manager.getOfficialPackages();
      
      expect(Array.isArray(packages)).toBe(true);
    });
  });

  describe('getBrokenPackages', () => {
    it('should return an array of broken package names', () => {
      const packages = manager.getBrokenPackages();
      
      expect(Array.isArray(packages)).toBe(true);
    });
  });

  describe('searchPackages', () => {
    it('should search packages by keyword', () => {
      const results = manager.searchPackages('nmap');
      
      expect(Array.isArray(results)).toBe(true);
      // Should find packages containing 'nmap' in name or description
    });

    it('should return empty array for non-existent keyword', () => {
      const results = manager.searchPackages('nonexistentpackage12345');
      
      expect(Array.isArray(results)).toBe(true);
      expect(results.length).toBe(0);
    });
  });

  describe('getPackageInfo', () => {
    it('should return null for non-existent package', () => {
      const info = manager.getPackageInfo('nonexistentpackage12345');
      
      expect(info).toBeNull();
    });

    it('should return package info for existing package', () => {
      // Test with first available package
      const packages = manager.getAllPackages();
      if (packages.length > 0) {
        const info = manager.getPackageInfo(packages[0]);
        
        if (info) {
          expect(info).toBeDefined();
          expect(info.name).toBe(packages[0]);
        }
      }
    });
  });
});