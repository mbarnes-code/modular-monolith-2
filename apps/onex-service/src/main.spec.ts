import { DataService, OnexService, SystemService } from './lib';

describe('OnexService', () => {
  let onexService: OnexService;

  beforeEach(() => {
    onexService = new OnexService();
  });

  describe('getAllTools', () => {
    it('should return an array of tools', () => {
      const tools = onexService.getAllTools();
      expect(Array.isArray(tools)).toBe(true);
      expect(tools.length).toBeGreaterThan(0);
    });

    it('should return tools with required properties', () => {
      const tools = onexService.getAllTools();
      const firstTool = tools[0];
      
      expect(firstTool).toHaveProperty('name');
      expect(firstTool).toHaveProperty('packageName');
      expect(firstTool).toHaveProperty('category');
      expect(firstTool).toHaveProperty('url');
      expect(firstTool).toHaveProperty('installer');
      expect(firstTool).toHaveProperty('dependencies');
    });
  });

  describe('getAllCategories', () => {
    it('should return an array of categories', () => {
      const categories = onexService.getAllCategories();
      expect(Array.isArray(categories)).toBe(true);
      expect(categories.length).toBeGreaterThan(0);
    });

    it('should return categories with required properties', () => {
      const categories = onexService.getAllCategories();
      const firstCategory = categories[0];
      
      expect(firstCategory).toHaveProperty('displayName');
      expect(firstCategory).toHaveProperty('key');
      expect(typeof firstCategory.displayName).toBe('string');
      expect(typeof firstCategory.key).toBe('string');
    });
  });

  describe('searchTools', () => {
    it('should return tools matching search query', () => {
      const results = onexService.searchTools('nmap');
      expect(Array.isArray(results)).toBe(true);
    });

    it('should return empty array for non-existent tools', () => {
      const results = onexService.searchTools('nonexistenttool123456');
      expect(results).toEqual([]);
    });

    it('should be case insensitive', () => {
      const lowerCase = onexService.searchTools('nmap');
      const upperCase = onexService.searchTools('NMAP');
      const mixedCase = onexService.searchTools('NmAp');
      
      expect(lowerCase).toEqual(upperCase);
      expect(upperCase).toEqual(mixedCase);
    });
  });

  describe('getToolByName', () => {
    it('should return a tool when found', () => {
      const tools = onexService.getAllTools();
      const firstTool = tools[0];
      const foundTool = onexService.getToolByName(firstTool.name);
      
      expect(foundTool).toBeDefined();
      expect(foundTool?.name).toBe(firstTool.name);
    });

    it('should return undefined when tool not found', () => {
      const tool = onexService.getToolByName('nonexistenttool123456');
      expect(tool).toBeUndefined();
    });

    it('should be case insensitive', () => {
      const tools = onexService.getAllTools();
      const firstTool = tools[0];
      const lowerCase = onexService.getToolByName(firstTool.name.toLowerCase());
      const upperCase = onexService.getToolByName(firstTool.name.toUpperCase());
      
      expect(lowerCase).toBeDefined();
      expect(upperCase).toBeDefined();
      expect(lowerCase?.name).toBe(upperCase?.name);
    });
  });

  describe('getToolsByCategory', () => {
    it('should return tools for a valid category', () => {
      const categories = onexService.getAllCategories();
      const firstCategory = categories[0];
      const tools = onexService.getToolsByCategory(firstCategory.key);
      
      expect(Array.isArray(tools)).toBe(true);
      tools.forEach(tool => {
        expect(tool.category).toBe(firstCategory.key);
      });
    });

    it('should return empty array for invalid category', () => {
      const tools = onexService.getToolsByCategory('invalid_category');
      expect(tools).toEqual([]);
    });
  });

  describe('getStats', () => {
    it('should return statistics object', () => {
      const stats = onexService.getStats();
      
      expect(stats).toHaveProperty('toolsCount');
      expect(stats).toHaveProperty('categoriesCount');
      expect(typeof stats.toolsCount).toBe('number');
      expect(typeof stats.categoriesCount).toBe('number');
      expect(stats.toolsCount).toBeGreaterThan(0);
      expect(stats.categoriesCount).toBeGreaterThan(0);
    });
  });

  describe('getSystemInfo', () => {
    it('should return system information', () => {
      const systemInfo = onexService.getSystemInfo();
      
      expect(systemInfo).toHaveProperty('packageManager');
      expect(systemInfo).toHaveProperty('system');
      expect(systemInfo).toHaveProperty('hasRoot');
      expect(systemInfo).toHaveProperty('binPath');
      expect(systemInfo).toHaveProperty('homePath');
      
      expect(typeof systemInfo.packageManager).toBe('string');
      expect(typeof systemInfo.system).toBe('string');
      expect(typeof systemInfo.hasRoot).toBe('boolean');
      expect(typeof systemInfo.binPath).toBe('string');
      expect(typeof systemInfo.homePath).toBe('string');
    });
  });
});

describe('DataService', () => {
  let dataService: DataService;

  beforeEach(() => {
    dataService = new DataService();
  });

  it('should load tools data successfully', () => {
    const tools = dataService.getAllTools();
    expect(tools.length).toBeGreaterThan(0);
  });

  it('should load categories data successfully', () => {
    const categories = dataService.getAllCategories();
    expect(categories.length).toBeGreaterThan(0);
  });
});

describe('SystemService', () => {
  let systemService: SystemService;

  beforeEach(() => {
    systemService = new SystemService();
  });

  it('should detect system information', () => {
    const systemInfo = systemService.getSystemInfo();
    expect(systemInfo).toBeDefined();
    expect(systemInfo.packageManager).toBeDefined();
    expect(systemInfo.system).toBeDefined();
  });

  it('should check online status', async () => {
    const isOnline = await systemService.checkOnlineStatus();
    expect(typeof isOnline).toBe('boolean');
  });
});