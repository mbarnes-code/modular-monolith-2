# Dispatch Central Auth Integration

This directory contains the integration components to connect Dispatch with our central authentication service, enabling unified SSO across the modular monolith.

## Overview

Dispatch is a Netflix-developed incident management platform with a pluggable authentication system. This integration creates a custom authentication provider plugin that connects to our central auth service, allowing users to authenticate once and access both Dispatch and other services in the platform.

## Architecture

```
┌─────────────────┐    OAuth2/OIDC    ┌─────────────────────┐
│                 │◄──────────────────►│                     │
│  Dispatch       │                    │  Central Auth       │
│  Service        │                    │  Service            │
│  (Port 8080)    │                    │  (Port 3001)        │
└─────────────────┘                    └─────────────────────┘
        │                                        │
        │                              ┌─────────────────┐
        │                              │                 │
        └──────────────────────────────►│  Shared User    │
                                       │  Database       │
                                       │                 │
                                       └─────────────────┘
```

## Files Structure

### Core Integration Files
```
src/services/plugins/dispatch_central_auth/
├── __init__.py                 # Package initialization
├── plugin.py                   # Central auth provider plugin
├── middleware.py              # Authentication middleware  
├── config.py                  # Configuration settings
├── integration.py             # Dispatch integration logic
└── patch_main.py             # Application startup patches
```

### Setup Files
```
register-dispatch-client.py    # OAuth2 client registration script
.env.central-auth.example      # Environment configuration template
README-CENTRAL-AUTH.md         # This documentation
```

## Quick Start

### 1. Prerequisites

Ensure the central auth service is running:
```bash
cd ../../../apps/core/auth-service
npm run dev
```

### 2. Install Dependencies

Add central auth dependencies to Dispatch:
```bash
cd /path/to/dispatch-service
pip install auth-core auth-clients auth-config httpx
```

### 3. Register OAuth2 Client

```bash
# Set environment variables
export CENTRAL_AUTH_SERVICE_URL="http://localhost:3001"
export CENTRAL_AUTH_ADMIN_API_KEY="your-admin-api-key"
export DISPATCH_BASE_URL="http://localhost:8080"

# Run registration script
python register-dispatch-client.py
```

### 4. Configure Environment

Copy the generated configuration:
```bash
cp .env.dispatch-sso .env
```

Edit `.env` and add any additional Dispatch configuration needed.

### 5. Update Dispatch Startup

Modify Dispatch's main application file to integrate central auth:

```python
# In dispatch/main.py or your main startup file
from dispatch.plugins.dispatch_central_auth.patch_main import integrate_central_auth_with_dispatch

# After creating the FastAPI app
integrate_central_auth_with_dispatch(app)
```

### 6. Start Dispatch

```bash
dispatch server develop
```

## Integration Components

### 1. CentralAuthProviderPlugin

The main authentication provider plugin that implements Dispatch's `AuthenticationProviderPlugin` interface:

- **JWT Authentication**: Validates JWT tokens from central auth service
- **Session Authentication**: Manages sessions through Redis
- **API Key Authentication**: Supports service-to-service authentication
- **Fallback Support**: Falls back to Dispatch's built-in auth when central auth unavailable

### 2. CentralAuthMiddleware

Middleware that integrates the auth plugin with Dispatch's request processing:

- **User Management**: Gets or creates Dispatch users from authenticated identities
- **Request State**: Stores authenticated user in request state
- **Path Exemption**: Configurable paths that skip authentication
- **Error Handling**: Graceful degradation when auth service unavailable

### 3. Configuration System

Comprehensive configuration for central auth integration:

- **Service URLs**: Central auth service endpoints
- **OAuth2 Settings**: Client ID, secret, scopes
- **Session Management**: Redis configuration for sessions
- **Fallback Behavior**: Controls fallback to built-in authentication

### 4. Integration Patches

Startup patches that integrate central auth with Dispatch:

- **Plugin Registration**: Registers central auth plugin with Dispatch
- **Route Addition**: Adds OAuth2 callback and auth management routes
- **Middleware Setup**: Configures authentication middleware
- **Health Checks**: Monitors central auth service health

## Manual Setup

### 1. Environment Configuration

Create `.env` file with central auth settings:

```bash
# Central Auth Configuration
CENTRAL_AUTH_ENABLED=true
CENTRAL_AUTH_SERVICE_URL=http://localhost:3001
CENTRAL_AUTH_CLIENT_ID=dispatch-service
CENTRAL_AUTH_CLIENT_SECRET=your-client-secret

# Dispatch Configuration  
DISPATCH_AUTHENTICATION_PROVIDER_SLUG=dispatch-auth-provider-central
DISPATCH_BASE_URL=http://localhost:8080

# Database Configuration
DATABASE_URL=postgresql://dispatch:dispatch@localhost:5432/dispatch

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

### 2. Register OAuth2 Client

Register Dispatch manually in central auth service:

```bash
curl -X POST http://localhost:3001/admin/oauth2/clients \
  -H "X-API-Key: your-admin-key" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "dispatch-service",
    "client_name": "Dispatch Incident Management", 
    "client_type": "confidential",
    "grant_types": ["authorization_code", "refresh_token"],
    "response_types": ["code"],
    "redirect_uris": ["http://localhost:8080/auth/callback"],
    "scopes": ["openid", "profile", "email"]
  }'
```

### 3. Database Setup

Ensure PostgreSQL and Redis are running:

```bash
# PostgreSQL
docker run -d --name dispatch-postgres \
  -e POSTGRES_DB=dispatch \
  -e POSTGRES_USER=dispatch \
  -e POSTGRES_PASSWORD=dispatch \
  -p 5432:5432 postgres:15

# Redis  
docker run -d --name dispatch-redis -p 6379:6379 redis:7-alpine
```

### 4. Start Services

Start Dispatch with central auth integration:

```bash
# Apply database migrations
dispatch database upgrade

# Start development server
dispatch server develop --host 0.0.0.0 --port 8080
```

## Authentication Flow

1. **User accesses Dispatch** → Redirects to central auth service login
2. **User authenticates** → Central auth service validates credentials  
3. **Authorization code returned** → Dispatch receives OAuth2 authorization code
4. **Token exchange** → Dispatch exchanges code for access token
5. **User info retrieved** → Dispatch gets user profile from central auth service
6. **Dispatch user created/updated** → User logged into Dispatch with SSO identity

## Configuration Reference

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CENTRAL_AUTH_ENABLED` | Enable central auth integration | `false` |
| `CENTRAL_AUTH_SERVICE_URL` | Central auth service base URL | `http://localhost:3001` |
| `CENTRAL_AUTH_CLIENT_ID` | OAuth2 client ID | `dispatch-service` |
| `CENTRAL_AUTH_CLIENT_SECRET` | OAuth2 client secret | *(required)* |
| `CENTRAL_AUTH_SCOPES` | OAuth2 scopes | `openid profile email` |
| `CENTRAL_AUTH_FALLBACK_ENABLED` | Enable fallback auth | `true` |

### Plugin Configuration

The central auth provider plugin supports these configuration options:

- **Authentication Methods**: JWT, Session, API Key
- **Token Validation**: JWKS endpoint validation
- **Session Management**: Redis-based session storage
- **User Mapping**: Automatic Dispatch user creation
- **Health Monitoring**: Service availability checks

## Advanced Configuration

### Custom User Mapping

Customize how central auth users map to Dispatch users:

```python
# In your Dispatch configuration
CENTRAL_AUTH_USER_MAPPING = {
    'email': 'email',
    'name': 'preferred_username', 
    'role': 'dispatch_role',
}
```

### Service-to-Service Authentication

Configure API key authentication for automated systems:

```bash
# Environment variables
CENTRAL_AUTH_SERVICE_API_KEY=your-service-api-key

# Use in API requests
curl -H "X-API-Key: your-api-key" http://localhost:8080/api/v1/incidents
```

### Session Configuration

Configure Redis session management:

```bash
# Session timeout (seconds)  
CENTRAL_AUTH_SESSION_TIMEOUT=86400

# Redis configuration
REDIS_HOST=redis.example.com
REDIS_PORT=6379
REDIS_PASSWORD=redis-password
REDIS_DB=1
```

## Troubleshooting

### Common Issues

**Plugin not loading**
- Verify `CENTRAL_AUTH_ENABLED=true` in environment
- Check that auth-core dependencies are installed
- Ensure plugin is in Python path

**OAuth2 flow fails**  
- Verify client ID and secret are correct
- Check that redirect URI matches registered value
- Ensure both services are accessible from browser

**Authentication errors**
- Check central auth service is running and accessible
- Verify JWT validation is working (JWKS endpoint)
- Check Redis connectivity for session management

**User creation fails**
- Ensure Dispatch database is accessible
- Check user email format and validation
- Verify individual service permissions

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# Environment variables
DISPATCH_LOG_LEVEL=DEBUG
CENTRAL_AUTH_DEBUG=true

# Check logs
dispatch server develop --log-level debug
```

### Health Checks

Monitor integration health:

```bash
# Check central auth plugin status
curl http://localhost:8080/auth/health

# Check central auth service
curl http://localhost:3001/health

# Check Dispatch status  
curl http://localhost:8080/api/v1/
```

## Integration with Existing Dispatch

### Migrating from Built-in Auth

1. **Export existing users** from Dispatch database
2. **Import users** into central auth service
3. **Update configuration** to use central auth provider
4. **Test authentication flow** with existing users
5. **Update user workflows** to use SSO login

### Gradual Migration

Enable both authentication methods during transition:

```bash
# Enable fallback to built-in auth
CENTRAL_AUTH_FALLBACK_ENABLED=true

# Gradual user migration
DISPATCH_AUTH_MIGRATION_MODE=true
```

## Production Deployment

### Docker Configuration

```yaml
# docker-compose.yml
services:
  dispatch:
    image: dispatch:latest
    environment:
      - CENTRAL_AUTH_ENABLED=true
      - CENTRAL_AUTH_SERVICE_URL=https://auth.yourdomain.com
      - CENTRAL_AUTH_CLIENT_ID=dispatch-service
      - CENTRAL_AUTH_CLIENT_SECRET_FILE=/run/secrets/dispatch_client_secret
    secrets:
      - dispatch_client_secret
    depends_on:
      - postgres
      - redis

secrets:
  dispatch_client_secret:
    external: true
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dispatch
spec:
  template:
    spec:
      containers:
      - name: dispatch
        image: dispatch:latest
        env:
        - name: CENTRAL_AUTH_ENABLED
          value: "true"
        - name: CENTRAL_AUTH_SERVICE_URL
          value: "https://auth.yourdomain.com"
        - name: CENTRAL_AUTH_CLIENT_ID
          value: "dispatch-service"
        - name: CENTRAL_AUTH_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: dispatch-auth
              key: client-secret
```

## Security Considerations

- **Client Secret Protection**: Store client secrets securely, not in version control
- **HTTPS in Production**: Use HTTPS for all OAuth2 flows in production  
- **Token Validation**: Dispatch validates tokens using central auth JWKS endpoint
- **Session Security**: Redis sessions provide secure session management
- **API Key Security**: Rotate API keys regularly and use least privilege access
- **Audit Logging**: All authentication events logged through Dispatch's audit system

## Support

For issues with Dispatch central auth integration:

1. Check Dispatch logs for authentication errors
2. Verify central auth service is accessible and healthy
3. Test OAuth2 flow manually with curl/Postman  
4. Review client registration in central auth admin panel
5. Check Redis connectivity and session management

The integration leverages Dispatch's existing plugin architecture, so most troubleshooting follows standard Dispatch plugin debugging practices.