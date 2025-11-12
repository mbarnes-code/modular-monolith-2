import KasmVNCService from './main';

describe('KasmVNCService', () => {
  let service: KasmVNCService;

  beforeEach(() => {
    service = new KasmVNCService();
  });

  describe('constructor', () => {
    it('should create an instance', () => {
      expect(service).toBeInstanceOf(KasmVNCService);
    });
  });

  describe('status method', () => {
    it('should exist and be callable', () => {
      expect(typeof service.status).toBe('function');
    });
  });

  describe('clean method', () => {
    it('should exist and be callable', () => {
      expect(typeof service.clean).toBe('function');
    });
  });
});