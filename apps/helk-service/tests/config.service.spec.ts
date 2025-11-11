/**
 * HELK Service - Configuration Service Tests
 */

import * as fs from 'fs';
import { ConfigService } from '../src/app/config.service';

// Mock fs module
jest.mock('fs');
const mockFs = fs as jest.Mocked<typeof fs>;

describe('ConfigService', () => {
  let service: ConfigService;

  beforeEach(() => {
    service = new ConfigService();
    jest.clearAllMocks();
  });

  describe('loadConfig', () => {
    it('should load default configuration when no custom config exists', async () => {
      mockFs.existsSync.mockReturnValue(false);

      const config = await service.loadConfig();

      expect(config.elasticsearch.host).toBe('helk-elasticsearch');
      expect(config.elasticsearch.port).toBe(9200);
      expect(config.kibana.host).toBe('helk-kibana');
      expect(config.kibana.port).toBe(5601);
    });

    it('should merge custom configuration when it exists', async () => {
      mockFs.existsSync.mockReturnValue(true);
      mockFs.readFileSync.mockReturnValue(JSON.stringify({
        elasticsearch: {
          port: 9201,
          heap_size: '4g'
        }
      }));

      const config = await service.loadConfig();

      expect(config.elasticsearch.port).toBe(9201);
      expect(config.elasticsearch.heap_size).toBe('4g');
      expect(config.elasticsearch.host).toBe('helk-elasticsearch'); // Should keep default
    });

    it('should return cached config on subsequent calls', async () => {
      mockFs.existsSync.mockReturnValue(false);

      const config1 = await service.loadConfig();
      const config2 = await service.loadConfig();

      expect(config1).toBe(config2);
      expect(mockFs.existsSync).toHaveBeenCalledTimes(1);
    });
  });

  describe('validateConfig', () => {
    it('should return no errors for valid configuration', () => {
      const validConfig = {
        elasticsearch: {
          host: 'localhost',
          port: 9200,
          cluster_name: 'test',
          heap_size: '2g'
        },
        kibana: {
          host: 'localhost',
          port: 5601,
          elasticsearch_url: 'http://localhost:9200'
        },
        logstash: {
          host: 'localhost',
          port: 5044,
          beats_port: 5044
        },
        jupyter: {
          host: 'localhost',
          port: 8888
        },
        spark: {
          master_host: 'localhost',
          master_port: 7077,
          worker_cores: 4,
          worker_memory: '4g'
        }
      };

      const errors = service.validateConfig(validConfig);

      expect(errors).toHaveLength(0);
    });

    it('should return errors for invalid configuration', () => {
      const invalidConfig = {
        elasticsearch: {
          host: '',
          port: 99999,
          cluster_name: 'test',
          heap_size: '2g'
        },
        kibana: {
          host: '',
          port: -1,
          elasticsearch_url: 'http://localhost:9200'
        },
        logstash: {
          host: '',
          port: 5044,
          beats_port: 5044
        },
        jupyter: {
          host: 'localhost',
          port: 8888
        },
        spark: {
          master_host: 'localhost',
          master_port: 7077,
          worker_cores: 0,
          worker_memory: '4g'
        }
      };

      const errors = service.validateConfig(invalidConfig);

      expect(errors.length).toBeGreaterThan(0);
      expect(errors).toContain('Elasticsearch host is required');
      expect(errors).toContain('Elasticsearch port must be between 1 and 65535');
      expect(errors).toContain('Kibana host is required');
      expect(errors).toContain('Spark worker cores must be at least 1');
    });
  });

  describe('getDockerEnv', () => {
    it('should return environment variables for Docker Compose', async () => {
      mockFs.existsSync.mockReturnValue(false);
      
      await service.loadConfig();
      const env = service.getDockerEnv();

      expect(env.HELK_ELASTICSEARCH_HOST).toBe('helk-elasticsearch');
      expect(env.HELK_ELASTICSEARCH_PORT).toBe('9200');
      expect(env.HELK_KIBANA_HOST).toBe('helk-kibana');
      expect(env.HELK_KIBANA_PORT).toBe('5601');
      expect(env.ES_HEAP_SIZE).toBe('2g');
    });

    it('should throw error if config not loaded', () => {
      expect(() => service.getDockerEnv()).toThrow(
        'Configuration not loaded. Call loadConfig() first.'
      );
    });
  });

  describe('getNetworkConfig', () => {
    it('should return network configuration', () => {
      const networkConfig = service.getNetworkConfig();

      expect(networkConfig.subnet).toBe('10.0.0.0/16');
      expect(networkConfig.gateway).toBe('10.0.0.1');
      expect(networkConfig.dns).toEqual(['8.8.8.8', '1.1.1.1']);
    });
  });

  describe('isConfigured', () => {
    it('should return true for valid configuration', async () => {
      mockFs.existsSync.mockReturnValue(false);

      const isConfigured = await service.isConfigured();

      expect(isConfigured).toBe(true);
    });

    it('should return false if configuration loading fails', async () => {
      mockFs.existsSync.mockImplementation(() => {
        throw new Error('File system error');
      });

      const isConfigured = await service.isConfigured();

      expect(isConfigured).toBe(false);
    });
  });
});