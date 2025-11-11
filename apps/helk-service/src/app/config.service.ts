/**
 * HELK Service - Configuration Management
 * 
 * Manages HELK platform configuration and settings
 */

import * as fs from 'fs';
import * as path from 'path';

export interface HELKConfig {
  elasticsearch: {
    host: string;
    port: number;
    cluster_name: string;
    heap_size: string;
  };
  kibana: {
    host: string;
    port: number;
    elasticsearch_url: string;
  };
  logstash: {
    host: string;
    port: number;
    beats_port: number;
  };
  jupyter: {
    host: string;
    port: number;
    token?: string;
  };
  spark: {
    master_host: string;
    master_port: number;
    worker_cores: number;
    worker_memory: string;
  };
}

export interface NetworkConfig {
  subnet: string;
  gateway: string;
  dns: string[];
}

export class ConfigService {
  private readonly configsDir: string;
  private readonly dockerDir: string;
  private config: HELKConfig | null = null;

  constructor() {
    this.configsDir = path.join(__dirname, '..', '..', 'infrastructure', 'configs');
    this.dockerDir = path.join(__dirname, '..', '..', 'infrastructure', 'docker');
  }

  /**
   * Load HELK configuration
   */
  async loadConfig(): Promise<HELKConfig> {
    if (this.config) {
      return this.config;
    }

    // Load default configuration
    this.config = this.getDefaultConfig();
    
    // Try to load custom configuration if it exists
    const customConfigPath = path.join(this.configsDir, 'helk.config.json');
    if (fs.existsSync(customConfigPath)) {
      const customConfig = JSON.parse(fs.readFileSync(customConfigPath, 'utf-8'));
      this.config = { ...this.config, ...customConfig };
    }

    return this.config!;
  }

  /**
   * Save configuration to file
   */
  async saveConfig(config: Partial<HELKConfig>): Promise<void> {
    const currentConfig = await this.loadConfig();
    const newConfig = { ...currentConfig, ...config };
    
    const configPath = path.join(this.configsDir, 'helk.config.json');
    fs.writeFileSync(configPath, JSON.stringify(newConfig, null, 2));
    
    this.config = newConfig;
  }

  /**
   * Get Docker Compose environment variables
   */
  getDockerEnv(): Record<string, string> {
    if (!this.config) {
      throw new Error('Configuration not loaded. Call loadConfig() first.');
    }

    return {
      HELK_ELASTICSEARCH_HOST: this.config.elasticsearch.host,
      HELK_ELASTICSEARCH_PORT: this.config.elasticsearch.port.toString(),
      HELK_KIBANA_HOST: this.config.kibana.host,
      HELK_KIBANA_PORT: this.config.kibana.port.toString(),
      HELK_LOGSTASH_HOST: this.config.logstash.host,
      HELK_LOGSTASH_PORT: this.config.logstash.port.toString(),
      HELK_JUPYTER_HOST: this.config.jupyter.host,
      HELK_JUPYTER_PORT: this.config.jupyter.port.toString(),
      HELK_SPARK_MASTER_HOST: this.config.spark.master_host,
      HELK_SPARK_MASTER_PORT: this.config.spark.master_port.toString(),
      ES_HEAP_SIZE: this.config.elasticsearch.heap_size,
      SPARK_WORKER_CORES: this.config.spark.worker_cores.toString(),
      SPARK_WORKER_MEMORY: this.config.spark.worker_memory,
    };
  }

  /**
   * Validate configuration
   */
  validateConfig(config: HELKConfig): string[] {
    const errors: string[] = [];

    // Validate Elasticsearch configuration
    if (!config.elasticsearch.host) {
      errors.push('Elasticsearch host is required');
    }
    if (config.elasticsearch.port < 1 || config.elasticsearch.port > 65535) {
      errors.push('Elasticsearch port must be between 1 and 65535');
    }

    // Validate Kibana configuration
    if (!config.kibana.host) {
      errors.push('Kibana host is required');
    }
    if (config.kibana.port < 1 || config.kibana.port > 65535) {
      errors.push('Kibana port must be between 1 and 65535');
    }

    // Validate Logstash configuration
    if (!config.logstash.host) {
      errors.push('Logstash host is required');
    }

    // Validate Spark configuration
    if (config.spark.worker_cores < 1) {
      errors.push('Spark worker cores must be at least 1');
    }

    return errors;
  }

  /**
   * Get network configuration for Docker
   */
  getNetworkConfig(): NetworkConfig {
    return {
      subnet: '10.0.0.0/16',
      gateway: '10.0.0.1',
      dns: ['8.8.8.8', '1.1.1.1']
    };
  }

  /**
   * Check if HELK is properly configured
   */
  async isConfigured(): Promise<boolean> {
    try {
      const config = await this.loadConfig();
      const errors = this.validateConfig(config);
      return errors.length === 0;
    } catch {
      return false;
    }
  }

  private getDefaultConfig(): HELKConfig {
    return {
      elasticsearch: {
        host: 'helk-elasticsearch',
        port: 9200,
        cluster_name: 'helk-cluster',
        heap_size: '2g'
      },
      kibana: {
        host: 'helk-kibana',
        port: 5601,
        elasticsearch_url: 'http://helk-elasticsearch:9200'
      },
      logstash: {
        host: 'helk-logstash',
        port: 5044,
        beats_port: 5044
      },
      jupyter: {
        host: 'helk-jupyter',
        port: 8888
      },
      spark: {
        master_host: 'helk-spark-master',
        master_port: 7077,
        worker_cores: 2,
        worker_memory: '2g'
      }
    };
  }
}