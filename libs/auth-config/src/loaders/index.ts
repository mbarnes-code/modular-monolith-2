// Configuration loaders for different environments and sources

import * as fs from 'fs/promises';
import * as yaml from 'js-yaml';
import * as path from 'path';
import { GlobalAuthConfig } from '../types';
import { AuthConfigValidator, ConfigValidationError } from '../validation';

export interface ConfigSource {
  type: 'file' | 'env' | 'vault' | 'consul' | 'custom';
  path?: string;
  format?: 'json' | 'yaml' | 'toml';
  loader?: (path: string) => Promise<any>;
}

export interface LoaderOptions {
  sources: ConfigSource[];
  environment?: string;
  baseDir?: string;
  mergeStrategy?: 'deep' | 'shallow' | 'replace';
  validateOnLoad?: boolean;
  secretsManager?: SecretsManager;
}

export interface SecretsManager {
  getSecret(key: string): Promise<string>;
  getSecrets(keys: string[]): Promise<Record<string, string>>;
}

export class ConfigLoadError extends Error {
  constructor(message: string, public readonly source: ConfigSource, public readonly cause?: Error) {
    super(message);
    this.name = 'ConfigLoadError';
  }
}

export class AuthConfigLoader {
  private readonly options: LoaderOptions;

  constructor(options: LoaderOptions) {
    this.options = {
      baseDir: process.cwd(),
      mergeStrategy: 'deep',
      validateOnLoad: true,
      ...options,
    };
  }

  /**
   * Loads configuration from multiple sources with hierarchy
   */
  async loadConfig(): Promise<GlobalAuthConfig> {
    let config: any = {};

    for (const source of this.options.sources) {
      try {
        const sourceConfig = await this.loadFromSource(source);
        config = this.mergeConfigs(config, sourceConfig);
      } catch (error) {
        throw new ConfigLoadError(
          `Failed to load configuration from ${source.type} source`,
          source,
          error instanceof Error ? error : new Error(String(error))
        );
      }
    }

    // Process environment variables and secrets
    config = await this.processSecrets(config);
    config = this.processEnvironmentVariables(config);

    // Validate if requested
    if (this.options.validateOnLoad) {
      try {
        return AuthConfigValidator.validateGlobalConfig(config);
      } catch (error) {
        if (error instanceof ConfigValidationError) {
          throw new ConfigLoadError(
            `Configuration validation failed: ${error.message}`,
            { type: 'custom' },
            error
          );
        }
        throw error;
      }
    }

    return config as GlobalAuthConfig;
  }

  /**
   * Loads configuration from a specific source
   */
  private async loadFromSource(source: ConfigSource): Promise<any> {
    switch (source.type) {
      case 'file':
        return this.loadFromFile(source);
      case 'env':
        return this.loadFromEnvironment(source);
      case 'custom':
        if (!source.loader) {
          throw new Error('Custom source requires a loader function');
        }
        return source.loader(source.path || '');
      default:
        throw new Error(`Unsupported source type: ${source.type}`);
    }
  }

  /**
   * Loads configuration from file system
   */
  private async loadFromFile(source: ConfigSource): Promise<any> {
    if (!source.path) {
      throw new Error('File source requires a path');
    }

    const filePath = path.isAbsolute(source.path) 
      ? source.path 
      : path.resolve(this.options.baseDir!, source.path);

    try {
      const content = await fs.readFile(filePath, 'utf8');
      return this.parseContent(content, source.format || this.getFormatFromExtension(filePath));
    } catch (error) {
      throw new Error(`Failed to read file ${filePath}: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  /**
   * Loads configuration from environment variables
   */
  private loadFromEnvironment(source: ConfigSource): any {
    const prefix = source.path || 'MM_AUTH_';
    const config: any = {};

    Object.entries(process.env).forEach(([key, value]) => {
      if (key.startsWith(prefix) && value !== undefined) {
        const configKey = key.substring(prefix.length).toLowerCase();
        const nestedKey = configKey.split('_');
        
        let current = config;
        for (let i = 0; i < nestedKey.length - 1; i++) {
          if (!current[nestedKey[i]]) {
            current[nestedKey[i]] = {};
          }
          current = current[nestedKey[i]];
        }
        
        current[nestedKey[nestedKey.length - 1]] = this.parseEnvironmentValue(value);
      }
    });

    return config;
  }

  /**
   * Processes secrets in configuration
   */
  private async processSecrets(config: any): Promise<any> {
    if (!this.options.secretsManager) {
      return config;
    }

    const secretKeys: string[] = [];
    
    // Recursively find secret references
    const findSecrets = (obj: any, path = ''): void => {
      if (typeof obj === 'object' && obj !== null) {
        for (const [key, value] of Object.entries(obj)) {
          const currentPath = path ? `${path}.${key}` : key;
          
          if (typeof value === 'string' && value.startsWith('secret:')) {
            secretKeys.push(value.substring(7));
          } else if (typeof value === 'object') {
            findSecrets(value, currentPath);
          }
        }
      }
    };

    findSecrets(config);

    if (secretKeys.length === 0) {
      return config;
    }

    // Fetch secrets
    const secrets = await this.options.secretsManager.getSecrets(secretKeys);

    // Replace secret references
    const replaceSecrets = (obj: any): any => {
      if (typeof obj === 'object' && obj !== null) {
        const result: any = Array.isArray(obj) ? [] : {};
        
        for (const [key, value] of Object.entries(obj)) {
          if (typeof value === 'string' && value.startsWith('secret:')) {
            const secretKey = value.substring(7);
            result[key] = secrets[secretKey];
          } else if (typeof value === 'object') {
            result[key] = replaceSecrets(value);
          } else {
            result[key] = value;
          }
        }
        
        return result;
      }
      
      return obj;
    };

    return replaceSecrets(config);
  }

  /**
   * Processes environment variable substitutions in config
   */
  private processEnvironmentVariables(config: any): any {
    const envVarRegex = /\$\{([^}]+)\}/g;

    const processValue = (value: any): any => {
      if (typeof value === 'string') {
        return value.replace(envVarRegex, (match, envVar) => {
          const [varName, defaultValue] = envVar.split(':');
          return process.env[varName] || defaultValue || match;
        });
      }
      
      if (typeof value === 'object' && value !== null) {
        const result: any = Array.isArray(value) ? [] : {};
        
        for (const [key, val] of Object.entries(value)) {
          result[key] = processValue(val);
        }
        
        return result;
      }
      
      return value;
    };

    return processValue(config);
  }

  /**
   * Merges configurations based on strategy
   */
  private mergeConfigs(target: any, source: any): any {
    if (this.options.mergeStrategy === 'replace') {
      return source;
    }

    if (this.options.mergeStrategy === 'shallow') {
      return { ...target, ...source };
    }

    // Deep merge
    return this.deepMerge(target, source);
  }

  /**
   * Performs deep merge of objects
   */
  private deepMerge(target: any, source: any): any {
    if (typeof target !== 'object' || target === null) {
      return source;
    }

    if (typeof source !== 'object' || source === null) {
      return target;
    }

    if (Array.isArray(source)) {
      return source;
    }

    const result = { ...target };

    for (const [key, value] of Object.entries(source)) {
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        result[key] = this.deepMerge(result[key], value);
      } else {
        result[key] = value;
      }
    }

    return result;
  }

  /**
   * Parses content based on format
   */
  private parseContent(content: string, format: string): any {
    switch (format) {
      case 'json':
        return JSON.parse(content);
      case 'yaml':
        return yaml.load(content);
      case 'toml':
        // Note: You'll need to add a TOML parser dependency
        throw new Error('TOML parsing not implemented');
      default:
        throw new Error(`Unsupported format: ${format}`);
    }
  }

  /**
   * Determines format from file extension
   */
  private getFormatFromExtension(filePath: string): string {
    const ext = path.extname(filePath).toLowerCase();
    
    switch (ext) {
      case '.json':
        return 'json';
      case '.yaml':
      case '.yml':
        return 'yaml';
      case '.toml':
        return 'toml';
      default:
        return 'json';
    }
  }

  /**
   * Parses environment variable value to appropriate type
   */
  private parseEnvironmentValue(value: string): any {
    // Boolean
    if (value.toLowerCase() === 'true') return true;
    if (value.toLowerCase() === 'false') return false;

    // Number
    if (/^\d+$/.test(value)) return parseInt(value, 10);
    if (/^\d+\.\d+$/.test(value)) return parseFloat(value);

    // JSON
    if (value.startsWith('{') || value.startsWith('[')) {
      try {
        return JSON.parse(value);
      } catch {
        // Fall through to string
      }
    }

    // Array (comma-separated)
    if (value.includes(',')) {
      return value.split(',').map(item => item.trim());
    }

    // String
    return value;
  }
}

/**
 * Convenience function to create a loader for common scenarios
 */
export function createDefaultLoader(environment: string, baseDir?: string): AuthConfigLoader {
  const sources: ConfigSource[] = [
    // Base configuration
    {
      type: 'file',
      path: 'config/auth.json',
      format: 'json',
    },
    // Environment-specific overrides
    {
      type: 'file',
      path: `config/auth.${environment}.json`,
      format: 'json',
    },
    // Environment variables
    {
      type: 'env',
      path: 'MM_AUTH_',
    },
  ];

  return new AuthConfigLoader({
    sources,
    environment,
    baseDir,
    mergeStrategy: 'deep',
    validateOnLoad: true,
  });
}

/**
 * Convenience function for Docker/Kubernetes deployments
 */
export function createContainerLoader(): AuthConfigLoader {
  const sources: ConfigSource[] = [
    // Config map volume
    {
      type: 'file',
      path: '/etc/auth-config/config.yaml',
      format: 'yaml',
    },
    // Environment variables for secrets
    {
      type: 'env',
      path: 'MM_AUTH_',
    },
  ];

  return new AuthConfigLoader({
    sources,
    mergeStrategy: 'deep',
    validateOnLoad: true,
  });
}