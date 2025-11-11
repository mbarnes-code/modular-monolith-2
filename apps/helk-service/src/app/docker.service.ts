/**
 * HELK Service - Docker Management Service
 * 
 * Manages Docker containers and services for the HELK platform
 */

import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';

export interface DockerComposeConfig {
  name: string;
  file: string;
  description: string;
  services: string[];
}

export interface ServiceStatus {
  name: string;
  status: 'running' | 'stopped' | 'error';
  ports: string[];
  health: 'healthy' | 'unhealthy' | 'unknown';
}

export class DockerService {
  private readonly dockerDir: string;
  private readonly configs: DockerComposeConfig[] = [
    {
      name: 'basic',
      file: 'helk-kibana-notebook-analysis-basic.yml',
      description: 'Basic HELK stack with Kibana, Jupyter notebooks, and analytics',
      services: ['elasticsearch', 'kibana', 'logstash', 'jupyter', 'spark-master', 'spark-worker']
    },
    {
      name: 'full',
      file: 'helk-kibana-notebook-analysis-alert-basic.yml',
      description: 'Full HELK stack including alerting capabilities',
      services: ['elasticsearch', 'kibana', 'logstash', 'jupyter', 'spark-master', 'spark-worker', 'elastalert']
    }
  ];

  constructor() {
    this.dockerDir = path.join(__dirname, '..', '..', 'infrastructure', 'docker');
  }

  /**
   * Start HELK services with specified configuration
   */
  async start(configName = 'basic', detached = true): Promise<void> {
    const config = this.getConfig(configName);
    await this.runDockerCompose(config.file, 'up', detached);
  }

  /**
   * Stop all HELK services
   */
  async stop(): Promise<void> {
    const scriptPath = path.join(this.dockerDir, 'helk_remove_containers.sh');
    await this.runScript(scriptPath);
  }

  /**
   * Build HELK Docker images
   */
  async build(configName = 'basic'): Promise<void> {
    const config = this.getConfig(configName);
    await this.runDockerCompose(config.file, 'build');
  }

  /**
   * Get status of all HELK services
   */
  async getStatus(configName = 'basic'): Promise<ServiceStatus[]> {
    const config = this.getConfig(configName);
    try {
      const output = execSync(`docker-compose -f ${config.file} ps --format json`, {
        cwd: this.dockerDir,
        encoding: 'utf-8'
      });
      
      return this.parseDockerComposeStatus(output);
    } catch (error) {
      throw new Error(`Failed to get service status: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Get logs from HELK services
   */
  async getLogs(configName = 'basic', serviceName?: string, lines = 100): Promise<string> {
    const config = this.getConfig(configName);
    const args = ['logs', '--tail', lines.toString()];
    if (serviceName) args.push(serviceName);

    try {
      return execSync(`docker-compose -f ${config.file} ${args.join(' ')}`, {
        cwd: this.dockerDir,
        encoding: 'utf-8'
      });
    } catch (error) {
      throw new Error(`Failed to get logs: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Install HELK (first-time setup)
   */
  async install(): Promise<void> {
    const scriptPath = path.join(this.dockerDir, 'helk_docker_install.sh');
    await this.runScript(scriptPath);
  }

  /**
   * Update HELK installation
   */
  async update(): Promise<void> {
    const scriptPath = path.join(this.dockerDir, 'helk_update.sh');
    await this.runScript(scriptPath);
  }

  /**
   * Get available configurations
   */
  getConfigurations(): DockerComposeConfig[] {
    return [...this.configs];
  }

  private getConfig(name: string): DockerComposeConfig {
    const config = this.configs.find(c => c.name === name);
    if (!config) {
      throw new Error(`Configuration '${name}' not found. Available: ${this.configs.map(c => c.name).join(', ')}`);
    }
    return config;
  }

  private async runDockerCompose(configFile: string, command: string, detached = false): Promise<void> {
    const args = ['-f', configFile, command];
    if (detached && command === 'up') args.push('-d');

    try {
      execSync(`docker-compose ${args.join(' ')}`, {
        stdio: 'inherit',
        cwd: this.dockerDir
      });
    } catch (error) {
      throw new Error(`Docker Compose command failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  private async runScript(scriptPath: string): Promise<void> {
    if (!fs.existsSync(scriptPath)) {
      throw new Error(`Script not found: ${scriptPath}`);
    }

    try {
      execSync(`chmod +x ${scriptPath} && ${scriptPath}`, {
        stdio: 'inherit',
        cwd: this.dockerDir
      });
    } catch (error) {
      throw new Error(`Script execution failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  private parseDockerComposeStatus(output: string): ServiceStatus[] {
    // Parse docker-compose ps JSON output
    const services: ServiceStatus[] = [];
    
    try {
      const lines = output.trim().split('\n').filter(line => line.trim());
      for (const line of lines) {
        const service = JSON.parse(line);
        services.push({
          name: service.Service || service.Name,
          status: service.State === 'running' ? 'running' : 'stopped',
          ports: service.Ports ? service.Ports.split(',').map((p: string) => p.trim()) : [],
          health: service.Health || 'unknown'
        });
      }
    } catch (error) {
      // Fallback to text parsing if JSON fails
      console.warn('Failed to parse JSON output, using fallback parser');
    }

    return services;
  }
}