# Auth Core Library

Unified authentication and authorization library for the modular monolith, providing SSO consolidation across all 37 applications.

## Features

- **JWT Token Management**: Secure token generation, verification, and rotation
- **OAuth2/OIDC Support**: Complete OAuth2 provider with PKCE support
- **Session Management**: Redis-based centralized session storage
- **SAML SSO**: Enterprise SAML authentication
- **LDAP Integration**: Directory service authentication
- **API Key Management**: Secure API key generation and validation
- **Multi-Framework Support**: Middleware for Express, FastAPI, Django, and Axum
- **Role-Based Access Control**: Flexible permission system
- **Audit Logging**: Comprehensive authentication event tracking
- **Security Utilities**: Password policies, rate limiting, MFA support

## Installation

```bash
npm install @modular-monolith/auth-core
```

## Quick Start

```typescript
import { 
  AuthConfig, 
  createDefaultConfig, 
  JWTProvider, 
  SessionProvider,
  ExpressAuthMiddleware 
} from '@modular-monolith/auth-core';

// Initialize configuration
const config = createDefaultConfig();

// Create providers
const jwtProvider = new JWTProvider(config);
const sessionProvider = new SessionProvider(config);

// Set up Express middleware
const authMiddleware = new ExpressAuthMiddleware(config);

app.use('/api', authMiddleware.authenticate());
app.use('/api/admin', authMiddleware.requireRoles('admin'));
```

## Configuration

Set the following environment variables:

```bash
# JWT Configuration
JWT_SECRET=your-jwt-secret
JWT_REFRESH_SECRET=your-refresh-secret
JWT_ISSUER=modular-monolith-auth
JWT_AUDIENCE=modular-monolith

# Redis Configuration  
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=your-redis-password

# API Key Configuration
API_KEY_PREFIX=mm
API_KEY_SALT=your-api-key-salt

# Security Configuration
BCRYPT_ROUNDS=12
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=900
```

## Providers

### JWT Provider

```typescript
import { JWTProvider } from '@modular-monolith/auth-core';

const jwtProvider = new JWTProvider(config);

// Generate tokens
const tokens = await jwtProvider.generateTokens(user);

// Verify token
const payload = await jwtProvider.verifyToken(accessToken);

// Refresh token
const newTokens = await jwtProvider.refreshAccessToken(refreshToken);
```

### Session Provider

```typescript
import { SessionProvider } from '@modular-monolith/auth-core';

const sessionProvider = new SessionProvider(config);

// Create session
const session = await sessionProvider.createSession(
  user, 
  ipAddress, 
  userAgent
);

// Get session
const sessionData = await sessionProvider.getSession(sessionId);

// Destroy session
await sessionProvider.destroySession(sessionId);
```

### OAuth2 Provider

```typescript
import { OAuth2Provider } from '@modular-monolith/auth-core';

const oauth2Provider = new OAuth2Provider(config, oauth2Config);

// Get authorization URL
const authUrl = oauth2Provider.getAuthorizationUrl(state);

// Exchange code for token
const tokens = await oauth2Provider.exchangeCodeForToken(code);

// Get user info
const userInfo = await oauth2Provider.getUserInfo(accessToken);
```

## Middleware

### Express.js

```typescript
import { ExpressAuthMiddleware } from '@modular-monolith/auth-core';

const authMiddleware = new ExpressAuthMiddleware(config);

// Basic authentication
app.use(authMiddleware.authenticate());

// Require specific roles
app.use('/admin', authMiddleware.requireRoles('admin'));

// Require specific permissions
app.use('/api/users', authMiddleware.requirePermissions('user:read'));

// Optional authentication
app.use('/public', authMiddleware.optional());
```

### FastAPI

```typescript
import { FastAPIAuthMiddleware } from '@modular-monolith/auth-core';

const authMiddleware = new FastAPIAuthMiddleware(config);

// Apply middleware
app.use(authMiddleware.createMiddleware({
  excludePaths: ['/health', '/docs'],
  requireAuth: true,
  requiredRoles: ['user']
}));
```

## Security Features

### Password Security

```typescript
import { SecurityUtils } from '@modular-monolith/auth-core';

const security = new SecurityUtils(12); // bcrypt rounds

// Hash password
const hash = await security.hashPassword(password);

// Verify password
const isValid = await security.verifyPassword(password, hash);

// Validate against policy
const validation = security.validatePassword(password, passwordPolicy);
```

### API Key Management

```typescript
import { ApiKeyProvider } from '@modular-monolith/auth-core';

const apiKeyProvider = new ApiKeyProvider(config);

// Generate API key
const { apiKey, rawKey } = await apiKeyProvider.generateApiKey(
  user,
  'My API Key',
  permissions,
  expiresAt
);

// Verify API key
const result = await apiKeyProvider.verifyApiKey(rawKey);
```

## Database Models

The library provides TypeScript interfaces for all database models:

```typescript
import { 
  UserModel, 
  RoleModel, 
  PermissionModel,
  OrganizationModel 
} from '@modular-monolith/auth-core';
```

## Event System

Subscribe to authentication events:

```typescript
// Authentication events are emitted for audit logging
// Implement based on your event system integration
```

## Migration from Existing Auth

1. **Install the library**: `npm install @modular-monolith/auth-core`
2. **Configure environment variables**: Set up JWT secrets, Redis connection
3. **Replace existing auth middleware**: Swap out current auth with unified middleware
4. **Migrate user data**: Transform existing user models to unified schema
5. **Update client code**: Use new authentication endpoints

## API Reference

### Classes

- `JWTProvider`: JWT token management
- `OAuth2Provider`: OAuth2/OIDC authentication  
- `SessionProvider`: Session management with Redis
- `SAMLProvider`: SAML SSO authentication
- `LDAPProvider`: LDAP directory authentication
- `ApiKeyProvider`: API key management
- `SecurityUtils`: Password and security utilities
- `ExpressAuthMiddleware`: Express.js middleware
- `FastAPIAuthMiddleware`: FastAPI middleware

### Interfaces

- `User`: User model interface
- `Role`: Role model interface  
- `Permission`: Permission model interface
- `AuthConfig`: Configuration interface
- `AuthToken`: Token response interface
- `SessionData`: Session data interface

## Development

```bash
# Install dependencies
npm install

# Build library
npm run build

# Run tests
npm test

# Watch mode
npm run dev
```

## License

MIT