# Authentication Consolidation Plan - Modular Monolith

## Executive Summary

Complete consolidation of 15+ authentication technologies across 37+ services in the modular monolith architecture. Current status: 3 services migrated (Jane Orchestrator, N8N, Dispatch), 34+ services remaining.

## Migration Architecture

### Central Authentication Infrastructure

- **Central Auth Service**: FastAPI OAuth2/OIDC provider with user management API
- **Auth-Core Library**: Unified authentication providers (JWT, OAuth2/OIDC, SAML, LDAP)
- **Auth-Clients**: Auto-generated client libraries (TypeScript, Python, Rust, PHP)
- **Auth-Config**: Centralized configuration with environment validation

### Completed Migrations (3/37)

1. **Jane Orchestrator** - FastAPI + auth-core integration ✅
2. **N8N Service** - OIDC integration via environment configuration ✅
3. **Dispatch Service** - Custom plugin implementation with CentralAuthProviderPlugin ✅

## Service Inventory & Migration Strategy

### Phase 1: Critical Security Fixes (Week 1-2) - IMMEDIATE PRIORITY

#### Maltrail Service (apps/security/maltrail-service)

- **Risk**: DEFAULT CREDENTIALS - Critical security vulnerability
- **Current**: Admin/admin default login
- **Strategy**: Emergency credential update + auth proxy integration
- **Implementation**:
  - Immediate: Change default credentials via environment override
  - Migration: Auth proxy pattern for legacy Python integration

#### MISP Service (apps/security/misp-service)

- **Risk**: Legacy PHP authentication system
- **Current**: PHP-based user management with potential vulnerabilities
- **Strategy**: Auth proxy pattern with reverse proxy authentication
- **Implementation**: Nginx/Apache auth proxy forwarding to central auth

### Phase 2: Core Services Migration (Week 3-4)

#### Mealie Service (apps/productivity/mealie-service)

- **Current**: Multi-backend auth (LDAP, OIDC, Local)
- **Strategy**: Replace with auth-core OIDC provider
- **Complexity**: Medium - Python FastAPI, existing OIDC support

#### Actual Budget (apps/productivity/actual-budget-service)

- **Current**: Express.js session-based authentication
- **Strategy**: JWT middleware replacement with auth-clients
- **Complexity**: Medium - Node.js/Express migration pattern

#### Jane UI (apps/ai/jane-ui)

- **Current**: React frontend with session management
- **Strategy**: OIDC implicit flow with auth-clients TypeScript
- **Complexity**: Low - Frontend-only authentication

#### Firecrawl Service (apps/productivity/firecrawl-service)

- **Current**: API key authentication
- **Strategy**: Bearer token with auth-core JWT validation
- **Complexity**: Low - API-focused service

### Phase 3: Bulk Migration (Week 5-7) - Template-Based Approach

#### High-Volume Services (30+ services)

- **Node.js Services** (12 services): Express middleware template
- **Python Services** (8 services): FastAPI auth-core integration
- **API-Only Services** (10 services): JWT bearer token validation

### Migration Patterns by Technology

#### Pattern A: Python/FastAPI Services

```python
# Standard auth-core integration
from auth_core import AuthProvider, JWTProvider
from auth_clients import CentralAuthClient

# Middleware integration
app.add_middleware(AuthCoreMiddleware, provider=auth_provider)
```

#### Pattern B: Node.js/Express Services

```javascript
// JWT middleware with auth-clients
const { authMiddleware } = require('@auth-clients/typescript');
app.use(authMiddleware({ validateTokens: true }));
```

#### Pattern C: Legacy Services via Auth Proxy

```nginx
# Reverse proxy with auth validation
location / {
    auth_request /auth;
    proxy_pass http://legacy-service;
}
```

## Implementation Timeline

### Week 1-2: Security Critical

- [ ] Fix Maltrail default credentials
- [ ] Implement MISP auth proxy
- [ ] Security audit of exposed services

### Week 3-4: Core Services

- [ ] Migrate Mealie OIDC integration
- [ ] Update Actual Budget to JWT
- [ ] Convert Jane UI to OIDC flow
- [ ] Implement Firecrawl bearer tokens

### Week 5-7: Bulk Migration

- [ ] Create migration templates per technology
- [ ] Batch migrate Node.js services (12)
- [ ] Batch migrate Python services (8)
- [ ] Convert API-only services (10)
- [ ] Implement auth proxy for remaining legacy (5)

### Week 8: Validation & Cleanup

- [ ] End-to-end SSO testing
- [ ] Remove deprecated auth systems
- [ ] Update documentation
- [ ] Security compliance audit

## Technical Requirements

### Dependencies to Add

```json
{
  "auth-core": "^1.0.0",
  "@auth-clients/typescript": "^1.0.0",
  "auth-clients-python": "^1.0.0"
}
```

### Configuration Updates

- Central auth service environment variables
- Redis session store configuration
- OAuth2 client registrations
- CORS policies for cross-service communication

### Testing Strategy

- Unit tests for auth middleware integration
- Integration tests for SSO flow
- Security penetration testing
- Performance impact assessment

## Risk Assessment

### High Risk

- **Maltrail**: Immediate security vulnerability
- **MISP**: Complex PHP legacy system
- **Production Downtime**: Service interruption during migration

### Medium Risk

- **Session Continuity**: User logout during migration
- **API Compatibility**: Breaking changes to existing integrations
- **Performance Impact**: Additional auth validation latency

### Low Risk

- **Development Services**: Non-production impact
- **API-Only Services**: Stateless migration pattern
- **Frontend Services**: Client-side auth flow changes

## Success Metrics

### Security Improvements

- Elimination of 15+ different auth systems
- Single point of credential management
- Centralized audit logging
- Consistent security policies

### Operational Benefits

- Reduced maintenance overhead
- Simplified user onboarding
- Single sign-on experience
- Centralized user management

### Technical Achievements

- Standardized authentication patterns
- Reusable auth-core components
- Auto-generated client libraries
- Comprehensive test coverage

## Next Actions

### Immediate (Today)

1. Fix Maltrail critical security vulnerability
2. Begin MISP auth proxy implementation
3. Create migration templates for bulk services

### Short-term (Week 1)

1. Security audit of all exposed services
2. Begin core service migrations (Mealie, Actual)
3. Prepare bulk migration automation

### Long-term (Week 2-8)

1. Execute phased migration plan
2. Comprehensive testing and validation
3. Documentation and training materials
4. Post-migration security compliance audit

## Resource Requirements

### Development Team

- 2-3 developers for 6-8 weeks
- 1 security specialist for audit/validation
- 1 DevOps engineer for infrastructure changes

### Infrastructure

- Central auth service deployment
- Redis cluster for session management
- Load balancing for auth proxy services
- Monitoring and logging infrastructure

### Testing Resources

- Staging environment replication
- Security testing tools
- Performance benchmarking setup
- User acceptance testing coordination
