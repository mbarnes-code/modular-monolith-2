# Authentication & Authorization Consolidation Analysis

**Date**: November 15, 2025  
**Status**: Analysis Complete  
**Purpose**: Consolidate diverse auth methods across apps following NX best practices

## Current State: Authentication Methods Inventory

### 1. **Jane Orchestrator (Core)** - `/apps/core/jane-orchestrator/`

**Auth Methods:**
- JWT-based authentication
- API Key authentication (MISP-style with `X-Authkey` header)
- Session-based authentication
- OAuth2 provider support
- Custom authentication plugins

**Key Files:**
- `src/config/auth_settings.py` - Auth configuration
- `src/api/middleware/auth_middleware.py` - Auth middleware
- `src/services/misp/auth_service.py` - MISP auth service
- `src/services/misp/enhanced_auth_service.py` - Enhanced auth
- `src/api/oauth/provider.py` - OAuth2 implementation

**Features:**
- Rate limiting (5 login attempts/minute)
- Multi-session management (max 5 concurrent)
- Password complexity requirements
- Cross-org access controls
- Audit logging

---

### 2. **Mealie Service (Productivity)** - `/apps/productivity/mealie-service/`

**Auth Methods:**
- Credentials-based (username/password)
- LDAP authentication
- OIDC/OpenID Connect
- JWT tokens with "remember me" functionality

**Key Files:**
- `apps/mealie-api/core/security/providers/auth_provider.py` - Base provider
- `apps/mealie-api/core/security/providers/credentials_provider.py` - Credentials
- `apps/mealie-api/core/security/providers/ldap_provider.py` - LDAP
- `apps/mealie-api/core/security/providers/openid_provider.py` - OIDC
- `apps/mealie-api/routes/auth/auth.py` - Auth routes
- `apps/mealie-api/routes/auth/auth_cache.py` - Auth caching

**Features:**
- Abstract `AuthProvider[T]` base class
- 14-day "remember me" tokens
- Token time configurable
- Auth method per user (stored in DB)
- Provider pattern for extensibility

---

### 3. **Dispatch Service (Security)** - `/apps/security/dispatch-service/`

**Auth Methods:**
- Basic authentication
- PKCE (Proof Key for Code Exchange)
- Header-based authentication
- AWS ALB authentication
- Plugin-based authentication system

**Key Files:**
- `src/services/plugins/bases/auth_provider.py` - Base plugin
- `src/services/plugins/bases/auth_mfa.py` - MFA support
- `src/services/plugins/dispatch_core/plugin.py` - Core auth implementations

**Implementations:**
- `BasicAuthProviderPlugin` - Basic auth
- `PKCEAuthProviderPlugin` - PKCE flow
- `HeaderAuthProviderPlugin` - Header-based
- `AwsAlbAuthProviderPlugin` - AWS ALB integration

**Features:**
- Plugin architecture
- MFA support base classes
- Request-based authentication

---

### 4. **n8n Service (Productivity)** - `/apps/productivity/n8n-service/`

**Auth Methods:**
- Cookie-based authentication (`n8n-auth` cookie)
- LDAP support
- Auth identities (external providers)
- Role-based access control (RBAC)

**Key Files:**
- `src/packages/cli/src/auth/auth.service.ts` - Auth service
- `src/packages/cli/src/controllers/auth.controller.ts` - Auth controller
- `src/packages/@n8n/db/src/entities/auth-identity.ts` - Auth identity entity
- `src/packages/@n8n/db/src/services/auth.roles.service.ts` - RBAC service
- `src/packages/@n8n/config/src/configs/auth.config.ts` - Auth config
- `src/packages/frontend/editor-ui/src/utils/rbac/middleware/authenticated.ts` - Frontend middleware

**Features:**
- Provider sync history tracking
- Multiple auth providers per user
- Secure/SameSite cookie configuration
- RBAC with granular permissions
- Browser ID whitelist

---

### 5. **Commander Spellbook (TCG)** - `/apps/tcg/commander-spellbook-backend/`

**Auth Methods:**
- Discord OAuth2

**Key Files:**
- `backend/backend/login/discord.py` - Discord OAuth implementation

**Features:**
- Social login via Discord
- OAuth2 flow

---

### 6. **Ghostwriter Service (Security)** - `/apps/security/ghostwriter-service/`

**Auth Methods:**
- Django authentication system
- Single Sign-On (SSO) providers
- Two-Factor Authentication (TOTP)
- OAuth2/OIDC via django-allauth

**Key Files:**
- Django authentication backend
- SSO adapter for external providers
- TOTP device management

**Features:**
- Role-based access controls
- SSO adapter for Microsoft/Azure, Google, GitHub, etc.
- Required 2FA enforcement per user
- MFA with TOTP devices
- Session management
- Access control routing through main login

**Documentation References:**
- [Ghostwriter SSO Wiki](https://www.ghostwriter.wiki/features/access-authentication-and-session-controls/single-sign-on)
- Uses `django-allauth` module (Microsoft provider, formerly Azure)

---

### 7. **MISP Service (Security)** - `/apps/security/misp-service/`

**Auth Methods:**
- API Key authentication (dual-header support)
- Role-based access control (RBAC)

**Key Files:**
- API authentication middleware
- User management system
- Organization-based access control

**Features:**
- **Dual Authentication Headers**:
  - `Authorization: Bearer <api-key>`
  - `X-MISP-AuthKey: <api-key>`
- Multi-target compatibility layer
- Role-based permissions (Triage, Admin, etc.)
- Organization-level isolation
- GitHub integration for access permissions

**Special Considerations:**
- Critical infrastructure usage (CSIRTs, security teams)
- Security advisory process with CVE assignment
- Encrypted vulnerability reporting (GnuPG key support)

---

## Authentication Patterns Identified

### Pattern 1: **Plugin/Provider Architecture**
Used by: Mealie, Dispatch

**Characteristics:**
- Abstract base class defines interface
- Concrete implementations for each auth method
- Easy to add new providers
- Provider selection at runtime

**Example:**
```python
class AuthProvider[T](metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def authenticate(self) -> tuple[str, timedelta] | None:
        raise NotImplementedError
```

### Pattern 2: **Middleware-Based**
Used by: Jane Orchestrator, n8n

**Characteristics:**
- Centralized auth middleware
- Multiple auth methods tried in sequence
- Request state population
- Framework-integrated (FastAPI/Starlette)

### Pattern 3: **Service-Based**
Used by: n8n, Jane Orchestrator

**Characteristics:**
- Dedicated auth service classes
- Controller delegates to service
- Clear separation of concerns

### Pattern 4: **Multi-Method Support**
Used by: All services

**Characteristics:**
- Fallback chains (API key → Session → Custom)
- User-specific auth method preferences
- External provider linking

---

## NX Best Practices for Consolidation

### Option 1: **Shared Authentication Library** (RECOMMENDED)

Create `libs/shared/auth/` with domain-driven organization:

```
libs/shared/auth/
├── README.md
├── project.json
├── src/
│   ├── index.ts                    # Main exports
│   ├── providers/                  # Auth providers
│   │   ├── base-provider.ts       # Abstract base
│   │   ├── jwt-provider.ts        # JWT implementation
│   │   ├── api-key-provider.ts    # API key
│   │   ├── ldap-provider.ts       # LDAP
│   │   ├── oidc-provider.ts       # OIDC/OAuth2
│   │   ├── session-provider.ts    # Session-based
│   │   ├── oauth2-provider.ts     # OAuth2
│   │   └── index.ts
│   ├── middleware/                 # Framework middleware
│   │   ├── fastapi.py             # FastAPI middleware
│   │   ├── express.ts             # Express middleware
│   │   └── index.ts
│   ├── services/                   # Auth services
│   │   ├── auth-service.ts        # Core service
│   │   ├── token-service.ts       # Token management
│   │   ├── rbac-service.ts        # RBAC
│   │   └── index.ts
│   ├── models/                     # Shared models
│   │   ├── user.ts
│   │   ├── token.ts
│   │   ├── permission.ts
│   │   └── index.ts
│   ├── config/                     # Configuration
│   │   ├── auth-config.ts
│   │   └── index.ts
│   ├── utils/                      # Utilities
│   │   ├── password.ts            # Password hashing
│   │   ├── validators.ts          # Validation
│   │   └── index.ts
│   └── guards/                     # Route guards
│       ├── authenticated.guard.ts
│       ├── role.guard.ts
│       └── index.ts
└── tests/
    └── ...
```

**Benefits:**
- ✅ Single source of truth
- ✅ Shared across all apps
- ✅ Consistent auth behavior
- ✅ Easier to maintain
- ✅ TypeScript + Python support
- ✅ Framework-agnostic core

**Implementation Steps:**
1. Create library structure
2. Extract common interfaces
3. Migrate providers one-by-one
4. Update apps to import from lib
5. Maintain backward compatibility during migration

---

### Option 2: **Domain-Specific Auth Libraries**

Create separate libs for different auth needs:

```
libs/auth/
├── core/                  # Core auth primitives
├── web/                   # Web-specific (cookies, sessions)
├── api/                   # API-specific (keys, tokens)
└── social/                # Social login (OAuth, OIDC)
```

**Benefits:**
- ✅ Smaller, focused libraries
- ✅ Apps only import what they need
- ✅ Easier to tree-shake

**Drawbacks:**
- ❌ More complex dependency graph
- ❌ Potential duplication

---

### Option 3: **Buildable Library with Multiple Entry Points**

Single library with multiple exports:

```typescript
// From apps
import { JWTProvider } from '@myapp/auth/jwt';
import { LDAPProvider } from '@myapp/auth/ldap';
import { AuthMiddleware } from '@myapp/auth/middleware';
```

**Benefits:**
- ✅ One library, organized exports
- ✅ Clear import paths
- ✅ Good IDE support

---

### Option 4: **Plugin Registry Pattern**

Create a central plugin registry:

```
libs/shared/auth-registry/
└── src/
    ├── registry.ts           # Central registry
    ├── plugin-interface.ts   # Plugin contract
    └── built-in-plugins/     # Core plugins
```

Apps register their auth methods:

```typescript
authRegistry.register('jwt', JWTPlugin);
authRegistry.register('ldap', LDAPPlugin);
authRegistry.register('oidc', OIDCPlugin);

// Use at runtime
const auth = authRegistry.get('jwt');
```

**Benefits:**
- ✅ Dynamic provider selection
- ✅ Easy to extend
- ✅ Config-driven

---

## Security & Compliance Features to Preserve

### Multi-Factor Authentication (MFA/2FA)
**Source**: Ghostwriter, Dispatch (MFA base classes)

Required features:
- TOTP device management
- Per-user MFA enforcement
- Backup codes
- Device trust/remember settings

### Rate Limiting & DoS Protection
**Source**: Mealie requirements, Jane Orchestrator

Required features:
- Configurable rate limits per endpoint
- IP-based throttling
- User-based throttling
- Burst allowance

### Credential Security
**Source**: n8n credential management

Required features:
- Automatic password field masking
- Sensitive field detection
- Secure credential storage
- Credential testing before save

### Single Sign-On (SSO)
**Source**: Ghostwriter (django-allauth), Mealie (OIDC), n8n (auth identities)

Required providers:
- Microsoft/Azure
- Google
- GitHub/GitLab
- Generic OIDC
- Generic OAuth2
- SAML support (consideration)

### API Security
**Source**: MISP dual-header auth, Jane Orchestrator

Required features:
- Multiple authentication header support
- API key management (creation, rotation, expiration)
- Key naming and organization
- Last-used tracking
- Automatic expiration

---

## Recommended Architecture

### **Hybrid Approach: Shared Core + Domain Plugins**

```
libs/
├── auth-core/                     # @myapp/auth-core (buildable)
│   ├── src/
│   │   ├── providers/
│   │   │   └── base-provider.ts   # Abstract base for all providers
│   │   ├── models/
│   │   │   ├── user.ts
│   │   │   ├── token.ts
│   │   │   └── permission.ts
│   │   ├── services/
│   │   │   ├── token-service.ts   # JWT, token mgmt
│   │   │   └── rbac-service.ts    # RBAC logic
│   │   ├── utils/
│   │   │   ├── password.ts        # Hashing, validation
│   │   │   └── crypto.ts
│   │   └── config/
│   │       └── auth-config.ts
│   └── project.json
│
├── auth-providers/                # @myapp/auth-providers (buildable)
│   ├── src/
│   │   ├── jwt/
│   │   │   ├── jwt-provider.ts
│   │   │   └── index.ts
│   │   ├── ldap/
│   │   │   ├── ldap-provider.ts
│   │   │   └── index.ts
│   │   ├── oidc/
│   │   │   ├── oidc-provider.ts
│   │   │   └── index.ts
│   │   ├── oauth2/
│   │   │   ├── oauth2-provider.ts
│   │   │   └── index.ts
│   │   ├── api-key/
│   │   │   ├── api-key-provider.ts
│   │   │   └── index.ts
│   │   └── session/
│   │       ├── session-provider.ts
│   │       └── index.ts
│   └── project.json
│
├── auth-middleware/               # @myapp/auth-middleware (buildable)
│   ├── src/
│   │   ├── fastapi/
│   │   │   └── auth-middleware.py
│   │   ├── express/
│   │   │   └── auth-middleware.ts
│   │   └── django/
│   │       └── auth-middleware.py
│   └── project.json
│
├── auth-guards/                   # @myapp/auth-guards (buildable)
│   ├── src/
│   │   ├── authenticated.guard.ts
│   │   ├── roles.guard.ts
│   │   └── permissions.guard.ts
│   └── project.json
│
├── auth-mfa/                      # @myapp/auth-mfa (buildable)
│   ├── src/
│   │   ├── totp/
│   │   │   ├── totp-service.ts    # TOTP generation/validation
│   │   │   ├── device-manager.ts  # Device registration
│   │   │   └── backup-codes.ts    # Backup code management
│   │   ├── sms/                   # SMS-based MFA (future)
│   │   └── webauthn/              # WebAuthn/FIDO2 (future)
│   └── project.json
│
└── auth-security/                 # @myapp/auth-security (buildable)
    ├── src/
    │   ├── rate-limiter.ts        # Rate limiting
    │   ├── credential-scanner.ts  # Sensitive field detection
    │   ├── password-policy.ts     # Password requirements
    │   ├── ip-filter.ts           # IP whitelist/blacklist
    │   └── audit-logger.ts        # Auth audit logging
    └── project.json
```

### Migration Path

#### Phase 1: Extract Core (Week 1-2)
1. Create `libs/auth-core`
2. Define base interfaces
3. Extract token services from Jane Orchestrator
4. Extract password utilities from Mealie
5. Create comprehensive tests

#### Phase 2: Standardize Providers (Week 3-4)
1. Create `libs/auth-providers`
2. Migrate JWT provider (from Jane + Mealie)
3. Migrate LDAP provider (from Mealie + n8n)
4. Migrate OIDC provider (from Mealie)
5. Migrate OAuth2 provider (from Jane + Commander Spellbook)
6. Migrate API Key provider (from Jane + MISP)

#### Phase 3: Framework Integration (Week 5-6)
1. Create `libs/auth-middleware`
2. FastAPI middleware (Jane Orchestrator pattern)
3. Express middleware (n8n pattern)
4. Django middleware (Dispatch pattern)

#### Phase 4: App Migration (Week 7-10)
1. **Jane Orchestrator**: Update to use libs
2. **Mealie**: Replace providers with lib versions
3. **n8n**: Integrate auth-core + middleware
4. **Dispatch**: Migrate to plugin pattern
5. **Commander Spellbook**: Use OAuth2 provider

#### Phase 5: Advanced Features (Week 11-12)
1. MFA support (TOTP from Ghostwriter)
2. SSO integration (django-allauth patterns from Ghostwriter)
3. Provider sync (from n8n)
4. Advanced RBAC
5. Rate limiting (from Mealie requirements)
6. Audit logging consolidation
7. Credential security scanning (from n8n patterns)

---

## Configuration Strategy

### Unified Auth Config

```typescript
// libs/auth-core/src/config/auth-config.ts
export interface AuthConfig {
  // JWT
  jwt: {
    secret: string;
    algorithm: 'HS256' | 'HS512' | 'RS256';
    accessTokenExpiry: number;  // minutes
    refreshTokenExpiry: number; // days
  };
  
  // Cookies
  cookies: {
    secure: boolean;
    sameSite: 'strict' | 'lax' | 'none';
    domain?: string;
  };
  
  // API Keys
  apiKey: {
    headerName: string;
    length: number;
  };
  
  // Rate Limiting
  rateLimit: {
    login: string;  // "5/minute"
    api: string;    // "100/minute"
  };
  
  // Password Policy
  password: {
    minLength: number;
    requireSpecial: boolean;
    requireNumbers: boolean;
    requireUppercase: boolean;
  };
  
  // Session
  session: {
    maxConcurrent: number;
    timeoutMinutes: number;
  };
  
  // Providers
  providers: {
    enabled: Array<'jwt' | 'ldap' | 'oidc' | 'oauth2' | 'apiKey' | 'sso'>;
    ldap?: LDAPConfig;
    oidc?: OIDCConfig;
    oauth2?: OAuth2Config;
    sso?: SSOConfig;
  };
  
  // MFA/2FA
  mfa: {
    enabled: boolean;
    required: boolean;  // Force all users
    perUserEnforcement: boolean;
    methods: Array<'totp' | 'sms' | 'webauthn'>;
    totp?: {
      issuer: string;
      period: number;
      digits: number;
    };
  };
  
  // Security
  security: {
    rateLimit: {
      enabled: boolean;
      endpoints: Record<string, string>;  // endpoint -> limit
      default: string;  // "100/minute"
    };
    auditLog: {
      enabled: boolean;
      events: Array<'login' | 'logout' | 'failed_login' | 'mfa_setup' | 'password_change'>;
    };
    credentialScan: {
      enabled: boolean;
      sensitiveFields: string[];  // ["password", "secret", "token", "key"]
    };
  };
}
```

---

## Database Schema Consolidation

### Unified User & Auth Tables

```sql
-- Users table (shared)
CREATE TABLE users (
  id UUID PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),  -- NULL for external auth
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

-- Auth Identities (external providers)
CREATE TABLE auth_identities (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  provider_type VARCHAR(50),  -- 'ldap', 'oidc', 'oauth2'
  provider_id VARCHAR(255),
  metadata JSONB,
  created_at TIMESTAMP NOT NULL,
  UNIQUE(provider_type, provider_id)
);

-- API Keys
CREATE TABLE api_keys (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  key_hash VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  expires_at TIMESTAMP,
  created_at TIMESTAMP NOT NULL,
  last_used_at TIMESTAMP
);

-- Sessions
CREATE TABLE sessions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  token_hash VARCHAR(255) NOT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP NOT NULL,
  last_activity TIMESTAMP
);

-- MFA/2FA Devices
CREATE TABLE mfa_devices (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  device_type VARCHAR(50) NOT NULL,  -- 'totp', 'sms', 'webauthn'
  device_name VARCHAR(255),
  secret TEXT,  -- Encrypted TOTP secret or device credential
  backup_codes TEXT[],  -- Array of hashed backup codes
  is_primary BOOLEAN DEFAULT false,
  is_trusted BOOLEAN DEFAULT false,
  created_at TIMESTAMP NOT NULL,
  last_used_at TIMESTAMP,
  UNIQUE(user_id, device_name)
);

-- Audit Log
CREATE TABLE auth_audit_log (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  event_type VARCHAR(50) NOT NULL,  -- 'login', 'logout', 'failed_login', 'mfa_setup', etc.
  ip_address VARCHAR(45),
  user_agent TEXT,
  metadata JSONB,
  created_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_audit_user_id ON auth_audit_log(user_id);
CREATE INDEX idx_audit_event_type ON auth_audit_log(event_type);
CREATE INDEX idx_audit_created_at ON auth_audit_log(created_at);

-- Roles & Permissions (RBAC)
CREATE TABLE roles (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT
);

CREATE TABLE permissions (
  id UUID PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  resource VARCHAR(100),
  action VARCHAR(50)
);

CREATE TABLE role_permissions (
  role_id UUID REFERENCES roles(id),
  permission_id UUID REFERENCES permissions(id),
  PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
  user_id UUID REFERENCES users(id),
  role_id UUID REFERENCES roles(id),
  PRIMARY KEY (user_id, role_id)
);
```

---

## Testing Strategy

### Unit Tests
```
libs/auth-core/tests/
├── providers/
│   ├── jwt-provider.spec.ts
│   ├── ldap-provider.spec.ts
│   └── ...
├── services/
│   ├── token-service.spec.ts
│   └── rbac-service.spec.ts
└── utils/
    └── password.spec.ts
```

### Integration Tests
```
libs/auth-middleware/tests/
├── fastapi-integration.spec.py
├── express-integration.spec.ts
└── ...
```

### E2E Tests
Per-app E2E tests using shared auth library

---

## Additional Considerations from Documentation

### Security-Specific Requirements

#### Mealie Security Considerations
- **Denial of Service (DoS) Protection**: API rate limiting required
- **Server-Side Request Forgery (SSRF)**: URL validation and network isolation needed
- **Vulnerable Endpoints**:
  - `/api/recipes/create/url` (external URL scraping)
  - `/api/recipes/{id}/image` (image downloads)
- **Recommended Mitigations**:
  - Reverse proxy rate limiting (Traefik, Nginx, Caddy)
  - Container network isolation
  - Strict rate limits on sensitive endpoints

#### Ghostwriter Advanced Features
- **SSO Providers**: Microsoft/Azure, Google, GitHub, GitLab, etc.
- **django-allauth Integration**: Mature authentication framework
- **2FA/MFA Support**: TOTP-based (Time-based One-Time Password)
- **Per-User 2FA Enforcement**: Configurable requirement
- **Admin Access Protection**: Routes through main login for 2FA

#### MISP Unique Patterns
- **Dual-Header Authentication**: Both `Authorization: Bearer` and `X-MISP-AuthKey` headers
- **Multi-Target Compatibility**:
  - Web mode (CORS-enabled)
  - Node.js mode (server-optimized)
  - Legacy mode (CakePHP compatibility)
  - Modern mode (REST standard)
- **Security-First Design**: CVE assignment for minor bugs, encrypted vulnerability reporting

#### n8n Credential Management
- **Password Field Masking**: `typeOptions.password = true` for sensitive fields
- **Credential Field Security**: ESLint rules enforce proper masking
- **OAuth2 Credential Templates**: Reusable credential parameter translations
- **Sensitive Field Detection**: Automatic detection of "password", "secret", "token", "key" fields

---

## Benefits of Consolidation

### For Developers
- ✅ One auth system to learn
- ✅ Consistent patterns across apps
- ✅ Reusable code
- ✅ Easier onboarding

### For Security
- ✅ Single audit surface
- ✅ Consistent security policies
- ✅ Easier to patch vulnerabilities
- ✅ Centralized logging

### For Maintenance
- ✅ Fix once, fix everywhere
- ✅ Easier to add new providers
- ✅ Simpler testing
- ✅ Better documentation

### For Users
- ✅ Consistent auth experience
- ✅ Single sign-on potential
- ✅ Better security
- ✅ More auth options

---

## Risks & Mitigation

### Risk 1: Breaking Changes
**Mitigation:** 
- Gradual migration
- Maintain backward compatibility
- Feature flags for new implementations

### Risk 2: Performance Impact
**Mitigation:**
- Benchmark before/after
- Optimize hot paths
- Cache authentication results

### Risk 3: Complex Dependencies
**Mitigation:**
- Use NX dependency graph
- Enforce unidirectional dependencies
- Regular dependency audits

### Risk 4: Framework Lock-in
**Mitigation:**
- Keep core framework-agnostic
- Adapter pattern for framework specifics
- Clear separation of concerns

---

## Next Steps

### Immediate Actions
1. ✅ Complete this analysis document
2. ⏳ Review with team
3. ⏳ Prioritize providers to migrate
4. ⏳ Create `libs/auth-core` skeleton
5. ⏳ Define interfaces and contracts

### Short Term (Sprint 1-2)
1. Set up auth libraries structure
2. Extract and test core utilities
3. Migrate JWT provider
4. Update Jane Orchestrator to use lib

### Medium Term (Sprint 3-4)
1. Migrate remaining providers
2. Create middleware for each framework
3. Update 2-3 apps to use consolidated auth

### Long Term (Sprint 5+)
1. Complete app migrations
2. Add advanced features (MFA, SSO)
3. Documentation and training
4. Deprecate old auth code

---

## References

### Existing Implementations
- Jane Orchestrator: `/apps/core/jane-orchestrator/src/config/auth_settings.py`
- Mealie: `/apps/productivity/mealie-service/apps/mealie-api/core/security/providers/`
- Dispatch: `/apps/security/dispatch-service/src/services/plugins/bases/auth_provider.py`
- n8n: `/apps/productivity/n8n-service/src/packages/cli/src/auth/`
- Ghostwriter: Django authentication with SSO adapter
- MISP: Dual-header API key authentication

### Documentation References
- Mealie Security: `/docs/apps/productivity/mealie/docs/docs/documentation/getting-started/installation/security.md`
- Ghostwriter SSO Wiki: https://www.ghostwriter.wiki/features/access-authentication-and-session-controls/single-sign-on
- MISP API Docs: `/docs/apps/security/misp/api-docs/docs/API_Documentation.md`
- n8n Credential Security: `/docs/apps/productivity/n8n/eslint-plugin/docs/rules/credential-password-field.md`

### NX Documentation
- [Buildable Libraries](https://nx.dev/concepts/buildable-and-publishable-libraries)
- [Library Types](https://nx.dev/concepts/more-concepts/library-types)
- [Dependency Management](https://nx.dev/concepts/module-federation/faster-builds)

### Auth Standards
- [OAuth 2.0](https://oauth.net/2/)
- [OpenID Connect](https://openid.net/connect/)
- [LDAP](https://ldap.com/)
- [JWT](https://jwt.io/)
- [PKCE](https://oauth.net/2/pkce/)
