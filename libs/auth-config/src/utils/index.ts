// Utility functions for configuration management

import * as crypto from 'crypto';
import * as os from 'os';
import { AuthProviderConfig, GlobalAuthConfig, OrganizationConfig, ServiceConfig } from '../types';

export class ConfigUtils {
  /**
   * Generates a secure random secret of specified length
   */
  static generateSecret(length = 32): string {
    return crypto.randomBytes(length).toString('hex');
  }

  /**
   * Generates a cryptographically secure client ID
   */
  static generateClientId(prefix = 'mm'): string {
    const timestamp = Date.now().toString(36);
    const random = crypto.randomBytes(8).toString('hex');
    return `${prefix}_${timestamp}_${random}`;
  }

  /**
   * Creates default JWT key pair for RS256 algorithm
   */
  static generateJWTKeyPair(): { publicKey: string; privateKey: string } {
    const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
      modulusLength: 2048,
      publicKeyEncoding: {
        type: 'spki',
        format: 'pem',
      },
      privateKeyEncoding: {
        type: 'pkcs8',
        format: 'pem',
      },
    });

    return { publicKey, privateKey };
  }

  /**
   * Validates JWT algorithm and key pair compatibility
   */
  static validateJWTKeys(algorithm: string, publicKey?: string, privateKey?: string): boolean {
    if (algorithm === 'HS256') {
      return true; // HMAC doesn't require key pair validation
    }

    if (!publicKey || !privateKey) {
      return false;
    }

    try {
      // Test sign/verify cycle
      const testPayload = { test: true, iat: Math.floor(Date.now() / 1000) };
      const token = crypto.sign('sha256', Buffer.from(JSON.stringify(testPayload)), privateKey);
      const verified = crypto.verify('sha256', Buffer.from(JSON.stringify(testPayload)), publicKey, token);
      return verified;
    } catch {
      return false;
    }
  }

  /**
   * Merges organization-specific settings with global defaults
   */
  static mergeOrganizationSettings(
    globalConfig: GlobalAuthConfig,
    organizationId: string
  ): OrganizationConfig | null {
    const org = globalConfig.organizations.find(o => o.id === organizationId);
    if (!org) {
      return null;
    }

    // Deep merge organization settings with global security defaults
    const merged = {
      ...org,
      settings: {
        ...org.settings,
        passwordPolicy: {
          ...globalConfig.security.passwordPolicy,
          ...org.settings.passwordPolicy,
        },
      },
    };

    return merged;
  }

  /**
   * Gets active auth providers for an organization
   */
  static getActiveProviders(
    config: GlobalAuthConfig,
    organizationId?: string
  ): AuthProviderConfig[] {
    return config.providers.filter(provider => {
      if (!provider.enabled) {
        return false;
      }

      // If organization-specific providers are defined
      if (provider.organizationIds && provider.organizationIds.length > 0) {
        return organizationId && provider.organizationIds.includes(organizationId);
      }

      // Global providers are available to all organizations
      return true;
    });
  }

  /**
   * Gets service configuration by client ID
   */
  static getServiceConfig(config: GlobalAuthConfig, clientId: string): ServiceConfig | null {
    return config.services.find(service => service.clientId === clientId) || null;
  }

  /**
   * Validates redirect URI against service configuration
   */
  static validateRedirectUri(serviceConfig: ServiceConfig, redirectUri: string): boolean {
    return serviceConfig.redirectUris.some(allowedUri => {
      // Exact match
      if (allowedUri === redirectUri) {
        return true;
      }

      // Pattern matching for localhost in development
      if (allowedUri.includes('localhost') && redirectUri.includes('localhost')) {
        const allowedUrl = new URL(allowedUri);
        const redirectUrl = new URL(redirectUri);
        
        return (
          allowedUrl.protocol === redirectUrl.protocol &&
          allowedUrl.hostname === redirectUrl.hostname &&
          allowedUrl.pathname === redirectUrl.pathname
        );
      }

      return false;
    });
  }

  /**
   * Generates default configuration template
   */
  static generateDefaultConfig(environment: string = 'development'): Partial<GlobalAuthConfig> {
    const isProduction = environment === 'production';
    const jwtKeys = this.generateJWTKeyPair();

    return {
      environment: {
        name: environment as any,
        debug: !isProduction,
        logLevel: isProduction ? 'warn' : 'debug',
      },
      jwt: {
        issuer: `https://auth.${isProduction ? 'yourdomain.com' : 'localhost:3000'}`,
        audience: 'modular-monolith',
        algorithm: 'RS256',
        publicKey: jwtKeys.publicKey,
        privateKey: jwtKeys.privateKey,
        accessTokenTTL: 3600, // 1 hour
        refreshTokenTTL: 604800, // 1 week
        clockTolerance: 30,
      },
      redis: {
        cluster: [
          {
            host: isProduction ? 'redis-cluster' : 'localhost',
            port: 6379,
            database: 0,
          },
        ],
        keyPrefix: 'mm-auth',
        ttl: {
          session: 28800, // 8 hours
          tokenBlacklist: 86400, // 24 hours
          rateLimitWindow: 900, // 15 minutes
        },
      },
      database: {
        primary: {
          host: isProduction ? 'postgres-primary' : 'localhost',
          port: 5432,
          database: 'modular_monolith_auth',
          username: 'mm_auth_user',
          password: isProduction ? '${MM_AUTH_DB_PASSWORD}' : 'development_password',
          ssl: isProduction,
        },
        pool: {
          min: 2,
          max: isProduction ? 20 : 5,
          idleTimeout: 30000,
        },
      },
      security: {
        passwordPolicy: {
          minLength: 8,
          maxLength: 128,
          requireUppercase: true,
          requireLowercase: true,
          requireNumbers: true,
          requireSpecialChars: !isProduction, // Relaxed for dev
          preventReuse: 5,
          maxAge: isProduction ? 90 : 365, // 3 months in prod, 1 year in dev
          bcryptRounds: 12,
        },
        rateLimiting: {
          login: {
            maxAttempts: isProduction ? 3 : 10,
            windowMs: 900000, // 15 minutes
            blockDuration: 900000,
          },
          api: {
            maxRequests: isProduction ? 100 : 1000,
            windowMs: 60000, // 1 minute
          },
          passwordReset: {
            maxAttempts: 3,
            windowMs: 3600000, // 1 hour
          },
        },
        csrf: {
          enabled: isProduction,
          tokenLength: 32,
          cookieName: '_csrf',
          headerName: 'X-CSRF-Token',
        },
        cors: {
          allowedOrigins: isProduction 
            ? ['https://yourdomain.com'] 
            : ['http://localhost:3000', 'http://localhost:3001', 'http://localhost:8080'],
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
          allowedHeaders: ['Authorization', 'Content-Type', 'X-Requested-With'],
          credentials: true,
          maxAge: 86400,
        },
        encryption: {
          algorithm: 'aes-256-gcm',
          keySize: 32,
          ivSize: 16,
          saltRounds: 12,
        },
      },
      organizations: [
        {
          id: 'default',
          name: 'Default Organization',
          slug: 'default',
          settings: {
            sessionTimeout: 28800, // 8 hours
            maxConcurrentSessions: 5,
            mfaRequired: isProduction,
            ssoEnabled: false,
            allowedEmailDomains: [],
            customFields: {},
          },
        },
      ],
      providers: [
        {
          id: 'local',
          name: 'local',
          type: 'local',
          enabled: true,
          config: {},
          displayName: 'Username/Password',
          order: 0,
        },
      ],
      services: [],
    };
  }

  /**
   * Sanitizes configuration for logging (removes sensitive data)
   */
  static sanitizeConfigForLogging(config: GlobalAuthConfig): any {
    const sanitized = JSON.parse(JSON.stringify(config));

    // Remove sensitive fields
    const sensitiveFields = [
      'privateKey',
      'password',
      'clientSecret',
      'bindPassword',
    ];

    const sanitizeObject = (obj: any): void => {
      if (typeof obj !== 'object' || obj === null) {
        return;
      }

      for (const [key, value] of Object.entries(obj)) {
        if (sensitiveFields.includes(key)) {
          obj[key] = '[REDACTED]';
        } else if (typeof value === 'object') {
          sanitizeObject(value);
        }
      }
    };

    sanitizeObject(sanitized);
    return sanitized;
  }

  /**
   * Validates configuration compatibility across versions
   */
  static validateConfigVersion(config: any, expectedVersion?: string): boolean {
    const configVersion = config.version || '1.0.0';
    const expected = expectedVersion || '1.0.0';

    // Simple semver major version check
    const configMajor = parseInt(configVersion.split('.')[0]);
    const expectedMajor = parseInt(expected.split('.')[0]);

    return configMajor === expectedMajor;
  }

  /**
   * Calculates configuration hash for change detection
   */
  static getConfigHash(config: GlobalAuthConfig): string {
    const normalized = JSON.stringify(config, Object.keys(config).sort());
    return crypto.createHash('sha256').update(normalized).digest('hex');
  }

  /**
   * Creates development-friendly service configuration
   */
  static createDevServiceConfig(serviceName: string): ServiceConfig {
    const clientId = this.generateClientId('dev');
    
    return {
      name: serviceName,
      clientId,
      clientSecret: this.generateSecret(32),
      redirectUris: [
        `http://localhost:3000/auth/callback`,
        `http://localhost:3001/auth/callback`,
        `http://localhost:8080/auth/callback`,
      ],
      allowedScopes: ['openid', 'profile', 'email'],
      tokenEndpointAuthMethod: 'client_secret_post',
      grantTypes: ['authorization_code', 'refresh_token'],
      responseTypes: ['code'],
      isPublic: false,
      pkceRequired: false, // Relaxed for development
    };
  }

  /**
   * Gets system information for configuration context
   */
  static getSystemInfo(): Record<string, any> {
    return {
      hostname: os.hostname(),
      platform: os.platform(),
      arch: os.arch(),
      nodeVersion: process.version,
      memory: {
        total: os.totalmem(),
        free: os.freemem(),
      },
      uptime: os.uptime(),
      timestamp: new Date().toISOString(),
    };
  }

  /**
   * Formats configuration for display
   */
  static formatConfigSummary(config: GlobalAuthConfig): string {
    const summary = [
      `Environment: ${config.environment.name}`,
      `Organizations: ${config.organizations.length}`,
      `Auth Providers: ${config.providers.filter(p => p.enabled).length} enabled`,
      `Services: ${config.services.length}`,
      `JWT Algorithm: ${config.jwt.algorithm}`,
      `Redis Cluster: ${config.redis.cluster.length} nodes`,
      `Database: ${config.database.primary.host}:${config.database.primary.port}`,
    ];

    return summary.join('\n');
  }
}