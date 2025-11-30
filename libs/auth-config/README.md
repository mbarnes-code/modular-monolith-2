# @modular-monolith/auth-config

Comprehensive configuration management library for the Modular Monolith authentication system. Provides type-safe configuration loading, validation, and management across all authentication components.

## Features

- 🔧 **Type-Safe Configuration** - Comprehensive TypeScript definitions for all auth components
- ✅ **Schema Validation** - Joi-based validation with detailed error reporting
- 📁 **Multiple Sources** - Load from files, environment variables, secrets managers
- 🔄 **Flexible Merging** - Deep, shallow, or replace merge strategies
- 🔒 **Security First** - Secure secret handling and sensitive data redaction
- 🚀 **Production Ready** - Container-friendly loaders and environment-specific configs

## Installation

```bash
pnpm add @modular-monolith/auth-config
```

## Quick Start

### Basic Configuration Loading

```typescript
import { createDefaultLoader, ConfigUtils } from '@modular-monolith/auth-config';

// Load configuration for development
const loader = createDefaultLoader('development');
const config = await loader.loadConfig();

console.log(ConfigUtils.formatConfigSummary(config));
```

### Container/Kubernetes Deployment

```typescript
import { createContainerLoader } from '@modular-monolith/auth-config';

// Load from config maps and environment
const loader = createContainerLoader();
const config = await loader.loadConfig();
```

### Custom Configuration Sources

```typescript
import { AuthConfigLoader } from '@modular-monolith/auth-config';

const loader = new AuthConfigLoader({
  sources: [
    { type: 'file', path: 'config/base.json', format: 'json' },
    { type: 'file', path: 'config/production.yaml', format: 'yaml' },
    { type: 'env', path: 'MM_AUTH_' },
  ],
  mergeStrategy: 'deep',
  validateOnLoad: true,
});

const config = await loader.loadConfig();
```

## Configuration Structure

### Global Configuration

```typescript
interface GlobalAuthConfig {
  environment: Environment;
  jwt: JWTConfig;
  redis: RedisConfig;
  database: DatabaseConfig;
  security: SecurityConfig;
  organizations: OrganizationConfig[];
  providers: AuthProviderConfig[];
  services: ServiceConfig[];
}
```

### Key Components

- **Environment**: Runtime environment settings and debug levels
- **JWT**: Token configuration, algorithms, keys, and TTL settings
- **Redis**: Session storage, clustering, and caching configuration
- **Database**: Primary/replica connections with connection pooling
- **Security**: Password policies, rate limiting, CORS, and encryption
- **Organizations**: Multi-tenant organization settings
- **Providers**: Authentication provider configurations (OAuth2, SAML, LDAP)
- **Services**: OAuth2 client configurations for integrated services

## Configuration Files

### Development Configuration (`config/auth.development.json`)

```json
{
  "environment": {
    "name": "development",
    "debug": true,
    "logLevel": "debug"
  },
  "jwt": {
    "issuer": "https://auth.localhost:3000",
    "audience": "modular-monolith",
    "algorithm": "HS256",
    "accessTokenTTL": 3600,
    "refreshTokenTTL": 604800
  },
  "redis": {
    "cluster": [{ "host": "localhost", "port": 6379 }],
    "keyPrefix": "mm-auth-dev"
  },
  "database": {
    "primary": {
      "host": "localhost",
      "port": 5432,
      "database": "mm_auth_dev",
      "username": "dev_user",
      "password": "dev_password"
    }
  }
}
```

### Production Configuration (`config/auth.production.yaml`)

```yaml
environment:
  name: production
  debug: false
  logLevel: warn

jwt:
  issuer: https://auth.yourdomain.com
  audience: modular-monolith
  algorithm: RS256
  publicKey: secret:jwt-public-key
  privateKey: secret:jwt-private-key
  accessTokenTTL: 900  # 15 minutes
  refreshTokenTTL: 86400  # 24 hours

redis:
  cluster:
    - host: redis-1.cluster.local
      port: 6379
    - host: redis-2.cluster.local
      port: 6379
  keyPrefix: mm-auth

database:
  primary:
    host: postgres-primary.db.local
    port: 5432
    database: modular_monolith_auth
    username: ${DB_USERNAME}
    password: secret:database-password
    ssl: true
  replicas:
    - host: postgres-replica-1.db.local
      port: 5432
      database: modular_monolith_auth
      username: ${DB_READONLY_USERNAME}
      password: secret:database-readonly-password
      ssl: true
```

## Environment Variables

Configuration supports environment variable substitution:

```bash
# Database
MM_AUTH_DATABASE_PRIMARY_HOST=postgres.example.com
MM_AUTH_DATABASE_PRIMARY_USERNAME=auth_user
MM_AUTH_DATABASE_PRIMARY_PASSWORD=secure_password

# Redis
MM_AUTH_REDIS_CLUSTER_0_HOST=redis-primary.example.com
MM_AUTH_REDIS_CLUSTER_0_PASSWORD=redis_password

# JWT
MM_AUTH_JWT_ISSUER=https://auth.example.com
MM_AUTH_JWT_ALGORITHM=RS256

# Security
MM_AUTH_SECURITY_CORS_ALLOWEDORIGINS=https://app.example.com,https://admin.example.com
```

## Validation

All configurations are validated using Joi schemas:

```typescript
import { AuthConfigValidator } from '@modular-monolith/auth-config';

try {
  const config = AuthConfigValidator.validateGlobalConfig(rawConfig);
  console.log('Configuration is valid');
} catch (error) {
  if (error instanceof ConfigValidationError) {
    console.error('Validation failed:', error.details);
  }
}
```

## Utilities

### Generate Default Configuration

```typescript
import { ConfigUtils } from '@modular-monolith/auth-config';

// Generate complete default config
const defaultConfig = ConfigUtils.generateDefaultConfig('production');

// Generate JWT key pair
const { publicKey, privateKey } = ConfigUtils.generateJWTKeyPair();

// Generate secure secrets
const clientSecret = ConfigUtils.generateSecret(32);
const clientId = ConfigUtils.generateClientId('myservice');
```

### Configuration Management

```typescript
// Get organization-specific config
const orgConfig = ConfigUtils.mergeOrganizationSettings(config, 'org-123');

// Get active providers for organization
const providers = ConfigUtils.getActiveProviders(config, 'org-123');

// Validate service redirect URI
const isValid = ConfigUtils.validateRedirectUri(serviceConfig, redirectUri);

// Sanitize for logging
const sanitized = ConfigUtils.sanitizeConfigForLogging(config);
```

## Advanced Usage

### Custom Secrets Manager

```typescript
import { AuthConfigLoader, SecretsManager } from '@modular-monolith/auth-config';

class VaultSecretsManager implements SecretsManager {
  async getSecret(key: string): Promise<string> {
    // Fetch from HashiCorp Vault
    return await vault.read(`secret/${key}`);
  }

  async getSecrets(keys: string[]): Promise<Record<string, string>> {
    const secrets: Record<string, string> = {};
    for (const key of keys) {
      secrets[key] = await this.getSecret(key);
    }
    return secrets;
  }
}

const loader = new AuthConfigLoader({
  sources: [
    { type: 'file', path: 'config/base.yaml' },
    { type: 'env', path: 'MM_AUTH_' },
  ],
  secretsManager: new VaultSecretsManager(),
});
```

### Custom Configuration Source

```typescript
const loader = new AuthConfigLoader({
  sources: [
    {
      type: 'custom',
      path: 'consul://config/auth',
      loader: async (path: string) => {
        const consulClient = new Consul();
        const result = await consulClient.kv.get(path.replace('consul://', ''));
        return JSON.parse(result.Value);
      },
    },
  ],
});
```

## Configuration Examples

### Multi-Organization Setup

```typescript
const config: GlobalAuthConfig = {
  // ... other config
  organizations: [
    {
      id: 'acme-corp',
      name: 'ACME Corporation',
      slug: 'acme',
      domain: 'acme.com',
      settings: {
        mfaRequired: true,
        ssoEnabled: true,
        allowedEmailDomains: ['acme.com'],
        sessionTimeout: 14400, // 4 hours
      },
    },
    {
      id: 'beta-inc',
      name: 'Beta Inc',
      slug: 'beta',
      domain: 'beta.com',
      settings: {
        mfaRequired: false,
        ssoEnabled: false,
        sessionTimeout: 28800, // 8 hours
      },
    },
  ],
};
```

### OAuth2/OIDC Providers

```typescript
const providers: AuthProviderConfig[] = [
  {
    id: 'google-sso',
    name: 'google',
    type: 'oidc',
    enabled: true,
    organizationIds: ['acme-corp'],
    displayName: 'Google Workspace',
    config: {
      issuer: 'https://accounts.google.com',
      clientId: 'your-google-client-id',
      clientSecret: 'secret:google-client-secret',
      redirectUri: 'https://auth.yourdomain.com/callback/google',
    },
  },
  {
    id: 'azure-ad',
    name: 'azure',
    type: 'oidc',
    enabled: true,
    organizationIds: ['beta-inc'],
    displayName: 'Microsoft Azure AD',
    config: {
      issuer: 'https://login.microsoftonline.com/tenant-id/v2.0',
      clientId: 'your-azure-client-id',
      clientSecret: 'secret:azure-client-secret',
      redirectUri: 'https://auth.yourdomain.com/callback/azure',
    },
  },
];
```

## Best Practices

### Security

1. **Never commit secrets** - Use environment variables or secrets managers
2. **Use strong algorithms** - Prefer RS256 over HS256 for JWT in production
3. **Validate all inputs** - Always use the provided validation schemas
4. **Sanitize logs** - Use `ConfigUtils.sanitizeConfigForLogging()` for logging

### Configuration Management

1. **Environment hierarchy** - base → environment-specific → environment variables
2. **Validate on startup** - Fail fast with invalid configurations
3. **Monitor changes** - Use `ConfigUtils.getConfigHash()` for change detection
4. **Document settings** - Maintain clear documentation for all configuration options

### Performance

1. **Cache configurations** - Load once at startup, reload on changes only
2. **Use connection pooling** - Configure appropriate database pool sizes
3. **Optimize Redis** - Use appropriate TTL values and key prefixes

## API Reference

### Classes

- `AuthConfigValidator` - Configuration validation utilities
- `AuthConfigLoader` - Multi-source configuration loading
- `ConfigUtils` - Configuration management utilities
- `ConfigValidationError` - Validation error with detailed information
- `ConfigLoadError` - Configuration loading error

### Functions

- `createDefaultLoader(environment, baseDir?)` - Create standard file-based loader
- `createContainerLoader()` - Create container/Kubernetes optimized loader

### Types

See the [types documentation](./src/types/index.ts) for complete TypeScript definitions.

## Contributing

See the main project [CONTRIBUTING.md](../../CONTRIBUTING.md) for contribution guidelines.

## License

Part of the Modular Monolith project. See the main project LICENSE file.