import { ActualService } from './actual.service';

describe('ActualService', () => {
  let service: ActualService;

  beforeEach(() => {
    service = new ActualService();
  });

  it('should create an instance', () => {
    expect(service).toBeDefined();
  });

  it('should return the correct actual budget path', () => {
    const actualPath = service.getActualPath();
    expect(actualPath).toContain('actual-budget');
  });

  it('should check if Actual Budget is installed', async () => {
    const isInstalled = await service.isInstalled();
    expect(typeof isInstalled).toBe('boolean');
  });

  it('should get configuration when installed', async () => {
    const isInstalled = await service.isInstalled();
    
    if (isInstalled) {
      const config = await service.getConfiguration();
      expect(config).toHaveProperty('name');
      expect(config).toHaveProperty('version');
      expect(config).toHaveProperty('description');
      expect(config).toHaveProperty('path');
    } else {
      await expect(service.getConfiguration()).rejects.toThrow('Actual Budget is not installed');
    }
  });

  it('should provide package path helper', () => {
    const packagePath = service.getPackagePath('loot-core');
    expect(packagePath).toContain('packages/loot-core');
  });

  it('should provide build path helper', () => {
    const buildPath = service.getBuildPath();
    expect(buildPath).toContain('build');
  });

  it('should provide data path helper', () => {
    const dataPath = service.getDataPath();
    expect(dataPath).toContain('data');
  });
});