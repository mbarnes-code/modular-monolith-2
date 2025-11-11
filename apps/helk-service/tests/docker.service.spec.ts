/**
 * HELK Service - Docker Service Tests
 */

import { execSync } from 'child_process';
import { DockerService } from '../src/app/docker.service';

// Mock execSync
jest.mock('child_process');
const mockExecSync = execSync as jest.MockedFunction<typeof execSync>;

describe('DockerService', () => {
  let service: DockerService;

  beforeEach(() => {
    service = new DockerService();
    jest.clearAllMocks();
  });

  describe('getConfigurations', () => {
    it('should return available configurations', () => {
      const configs = service.getConfigurations();
      
      expect(configs).toHaveLength(2);
      expect(configs[0].name).toBe('basic');
      expect(configs[1].name).toBe('full');
    });

    it('should include service descriptions', () => {
      const configs = service.getConfigurations();
      
      configs.forEach(config => {
        expect(config.description).toBeDefined();
        expect(config.file).toBeDefined();
        expect(config.services).toBeDefined();
        expect(Array.isArray(config.services)).toBe(true);
      });
    });
  });

  describe('start', () => {
    it('should start basic configuration by default', async () => {
      mockExecSync.mockReturnValue(Buffer.from(''));

      await service.start();

      expect(mockExecSync).toHaveBeenCalledWith(
        'docker-compose -f helk-kibana-notebook-analysis-basic.yml up -d',
        expect.objectContaining({
          stdio: 'inherit'
        })
      );
    });

    it('should start specified configuration', async () => {
      mockExecSync.mockReturnValue(Buffer.from(''));

      await service.start('full');

      expect(mockExecSync).toHaveBeenCalledWith(
        'docker-compose -f helk-kibana-notebook-analysis-alert-basic.yml up -d',
        expect.objectContaining({
          stdio: 'inherit'
        })
      );
    });

    it('should throw error for invalid configuration', async () => {
      await expect(service.start('invalid')).rejects.toThrow(
        "Configuration 'invalid' not found"
      );
    });
  });

  describe('build', () => {
    it('should build basic configuration by default', async () => {
      mockExecSync.mockReturnValue(Buffer.from(''));

      await service.build();

      expect(mockExecSync).toHaveBeenCalledWith(
        'docker-compose -f helk-kibana-notebook-analysis-basic.yml build',
        expect.objectContaining({
          stdio: 'inherit'
        })
      );
    });
  });

  describe('getStatus', () => {
    it('should return service status', async () => {
      const mockOutput = JSON.stringify({
        Service: 'elasticsearch',
        State: 'running',
        Ports: '9200/tcp, 9300/tcp',
        Health: 'healthy'
      });
      
      mockExecSync.mockReturnValue(mockOutput);

      const status = await service.getStatus();

      expect(status).toHaveLength(1);
      expect(status[0].name).toBe('elasticsearch');
      expect(status[0].status).toBe('running');
      expect(status[0].health).toBe('healthy');
    });

    it('should handle docker-compose errors', async () => {
      mockExecSync.mockImplementation(() => {
        throw new Error('Docker not running');
      });

      await expect(service.getStatus()).rejects.toThrow(
        'Failed to get service status'
      );
    });
  });

  describe('getLogs', () => {
    it('should get logs for all services by default', async () => {
      mockExecSync.mockReturnValue('Service logs...');

      const logs = await service.getLogs();

      expect(logs).toBe('Service logs...');
      expect(mockExecSync).toHaveBeenCalledWith(
        'docker-compose -f helk-kibana-notebook-analysis-basic.yml logs --tail 100',
        expect.objectContaining({
          encoding: 'utf-8'
        })
      );
    });

    it('should get logs for specific service', async () => {
      mockExecSync.mockReturnValue('Elasticsearch logs...');

      const logs = await service.getLogs('basic', 'elasticsearch', 50);

      expect(logs).toBe('Elasticsearch logs...');
      expect(mockExecSync).toHaveBeenCalledWith(
        'docker-compose -f helk-kibana-notebook-analysis-basic.yml logs --tail 50 elasticsearch',
        expect.objectContaining({
          encoding: 'utf-8'
        })
      );
    });
  });
});