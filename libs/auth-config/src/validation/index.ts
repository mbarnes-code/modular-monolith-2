// Configuration validation and loading utilities

import { ValidationResult } from 'joi';
import {
    authProviderConfigSchema,
    databaseConfigSchema,
    environmentSchema,
    globalAuthConfigSchema,
    jwtConfigSchema,
    organizationConfigSchema,
    redisConfigSchema,
    securityConfigSchema,
    serviceConfigSchema,
} from '../schemas';
import { Environment, GlobalAuthConfig } from '../types';

export class ConfigValidationError extends Error {
  public readonly details: ValidationResult['error'];

  constructor(message: string, details: ValidationResult['error']) {
    super(message);
    this.name = 'ConfigValidationError';
    this.details = details;
  }
}

export interface ConfigValidationOptions {
  allowUnknown?: boolean;
  stripUnknown?: boolean;
  abortEarly?: boolean;
  context?: Record<string, any>;
}

export class AuthConfigValidator {
  private static readonly defaultOptions: ConfigValidationOptions = {
    allowUnknown: false,
    stripUnknown: true,
    abortEarly: false,
  };

  /**
   * Validates a complete global auth configuration
   */
  static validateGlobalConfig(
    config: unknown,
    options: ConfigValidationOptions = {}
  ): GlobalAuthConfig {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = globalAuthConfigSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Global configuration validation failed: ${error.message}`,
        error
      );
    }

    return value as GlobalAuthConfig;
  }

  /**
   * Validates environment configuration
   */
  static validateEnvironment(
    config: unknown,
    options: ConfigValidationOptions = {}
  ): Environment {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = environmentSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Environment configuration validation failed: ${error.message}`,
        error
      );
    }

    return value as Environment;
  }

  /**
   * Validates JWT configuration
   */
  static validateJWTConfig(
    config: unknown,
    options: ConfigValidationOptions = {}
  ) {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = jwtConfigSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `JWT configuration validation failed: ${error.message}`,
        error
      );
    }

    return value;
  }

  /**
   * Validates Redis configuration
   */
  static validateRedisConfig(
    config: unknown,
    options: ConfigValidationOptions = {}
  ) {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = redisConfigSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Redis configuration validation failed: ${error.message}`,
        error
      );
    }

    return value;
  }

  /**
   * Validates database configuration
   */
  static validateDatabaseConfig(
    config: unknown,
    options: ConfigValidationOptions = {}
  ) {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = databaseConfigSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Database configuration validation failed: ${error.message}`,
        error
      );
    }

    return value;
  }

  /**
   * Validates security configuration
   */
  static validateSecurityConfig(
    config: unknown,
    options: ConfigValidationOptions = {}
  ) {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = securityConfigSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Security configuration validation failed: ${error.message}`,
        error
      );
    }

    return value;
  }

  /**
   * Validates organization configuration
   */
  static validateOrganizationConfig(
    config: unknown,
    options: ConfigValidationOptions = {}
  ) {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = organizationConfigSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Organization configuration validation failed: ${error.message}`,
        error
      );
    }

    return value;
  }

  /**
   * Validates auth provider configuration
   */
  static validateProviderConfig(
    config: unknown,
    options: ConfigValidationOptions = {}
  ) {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = authProviderConfigSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Auth provider configuration validation failed: ${error.message}`,
        error
      );
    }

    return value;
  }

  /**
   * Validates service configuration
   */
  static validateServiceConfig(
    config: unknown,
    options: ConfigValidationOptions = {}
  ) {
    const opts = { ...this.defaultOptions, ...options };
    const { error, value } = serviceConfigSchema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Service configuration validation failed: ${error.message}`,
        error
      );
    }

    return value;
  }

  /**
   * Validates partial configuration updates
   */
  static validatePartialConfig<T>(
    schema: any,
    config: Partial<T>,
    options: ConfigValidationOptions = {}
  ): Partial<T> {
    const opts = { 
      ...this.defaultOptions, 
      ...options,
      // Allow partial validation for updates
      allowUnknown: true,
      presence: 'optional',
    };
    
    const { error, value } = schema.validate(config, opts);

    if (error) {
      throw new ConfigValidationError(
        `Partial configuration validation failed: ${error.message}`,
        error
      );
    }

    return value as Partial<T>;
  }

  /**
   * Performs deep validation with context-aware error reporting
   */
  static validateWithContext(
    schema: any,
    config: unknown,
    context: string,
    options: ConfigValidationOptions = {}
  ) {
    const opts = { ...this.defaultOptions, ...options };
    
    try {
      const { error, value } = schema.validate(config, opts);
      
      if (error) {
        throw new ConfigValidationError(
          `Validation failed in ${context}: ${error.message}`,
          error
        );
      }
      
      return value;
    } catch (err) {
      if (err instanceof ConfigValidationError) {
        throw err;
      }
      
      throw new ConfigValidationError(
        `Unexpected validation error in ${context}: ${err instanceof Error ? err.message : String(err)}`,
        null
      );
    }
  }

  /**
   * Validates array of configurations with indexed error reporting
   */
  static validateArray<T>(
    itemSchema: any,
    configs: unknown[],
    itemName: string,
    options: ConfigValidationOptions = {}
  ): T[] {
    if (!Array.isArray(configs)) {
      throw new ConfigValidationError(
        `Expected array of ${itemName} configurations`,
        null
      );
    }

    return configs.map((config, index) => {
      try {
        return this.validateWithContext(
          itemSchema,
          config,
          `${itemName}[${index}]`,
          options
        );
      } catch (err) {
        if (err instanceof ConfigValidationError) {
          throw new ConfigValidationError(
            `${itemName}[${index}]: ${err.message}`,
            err.details
          );
        }
        throw err;
      }
    });
  }
}