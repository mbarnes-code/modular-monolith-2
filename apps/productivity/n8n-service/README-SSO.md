# N8N SSO Integration with Central Auth Service

This directory contains the integration configuration to connect N8N with our central authentication service, enabling unified SSO across the modular monolith.

## Overview

N8N has built-in enterprise SSO features including OIDC support. This integration configures N8N to use our central auth service as the OIDC provider, allowing users to authenticate once and access both N8N workflows and other services in the platform.

## Architecture

```
┌─────────────────┐    OAuth2/OIDC    ┌─────────────────────┐
│                 │◄──────────────────►│                     │
│  N8N Service    │                    │  Central Auth       │
│  (Port 5678)    │                    │  Service            │
│                 │                    │  (Port 3001)        │
└─────────────────┘                    └─────────────────────┘
        │                                        │
        │                              ┌─────────────────┐
        │                              │                 │
        └──────────────────────────────►│  Shared User    │
                                       │  Database       │
                                       │                 │
                                       └─────────────────┘
```

## Files

### Integration Files
- `n8n-auth-integration.ts` - Core integration configuration and types
- `n8n-auth-patch.ts` - Runtime patches to N8N's OIDC service
- `register-n8n-client.js` - OAuth2 client registration script
- `setup-n8n-sso.sh` - Automated setup script

### Configuration Files
- `.env.sso.example` - Template environment configuration
- `docker-compose.sso.yml` - Docker Compose override for SSO (generated)

## Quick Start

### 1. Prerequisites

Ensure the central auth service is running:
```bash
cd ../../../libs/auth-service
npm run dev
```

### 2. Run Setup Script

```bash
# Set environment variables
export AUTH_SERVICE_URL="http://localhost:3001"
export AUTH_SERVICE_ADMIN_API_KEY="your-admin-api-key"
export N8N_BASE_URL="http://localhost:5678"

# Run the setup script
./setup-n8n-sso.sh
```

### 3. Configure Environment

Copy the generated configuration:
```bash
cp .env.sso .env
```

Edit `.env` and add your OAuth2 client credentials from the setup output.

### 4. Start N8N with SSO

```bash
# Using Docker Compose
docker-compose -f docker-compose.yml -f docker-compose.sso.yml up -d

# Or using npm
npm run dev
```

## Manual Setup

### 1. Environment Configuration

Create `.env` file with SSO configuration:

```bash
# Authentication Configuration
N8N_USER_MANAGEMENT_AUTHENTICATION_METHOD=oidc
N8N_SSO_ENABLED=true

# Central Auth Service
AUTH_SERVICE_URL=http://localhost:3001
N8N_OIDC_CLIENT_ID=n8n-service
N8N_OIDC_CLIENT_SECRET=your-client-secret

# Database (required for user management)
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=localhost
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n
DB_POSTGRESDB_USER=n8n_user
DB_POSTGRESDB_PASSWORD=n8n_password

# Redis (for sessions)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=1
```

### 2. Register OAuth2 Client

Register N8N in the central auth service:

```bash
node register-n8n-client.js
```

This creates an OAuth2 client with:
- **Client ID**: `n8n-service`
- **Redirect URI**: `http://localhost:5678/rest/sso/oidc/callback`
- **Scopes**: `openid`, `profile`, `email`

### 3. Start Services

Start required services:

```bash
# PostgreSQL (for N8N user management)
docker run -d --name n8n-postgres \
  -e POSTGRES_DB=n8n \
  -e POSTGRES_USER=n8n_user \
  -e POSTGRES_PASSWORD=n8n_password \
  -p 5432:5432 postgres:15

# Redis (for sessions)
docker run -d --name n8n-redis -p 6379:6379 redis:7-alpine

# Start N8N
npm run dev
```

## Authentication Flow

1. **User visits N8N** → Redirects to central auth service
2. **User authenticates** → Central auth service validates credentials
3. **Authorization code returned** → N8N receives OAuth2 code
4. **Token exchange** → N8N exchanges code for access token
5. **User info retrieved** → N8N gets user profile from auth service
6. **N8N session created** → User logged into N8N with SSO identity

## Configuration Reference

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AUTH_SERVICE_URL` | Central auth service base URL | `http://localhost:3001` |
| `N8N_OIDC_CLIENT_ID` | OAuth2 client ID | `n8n-service` |
| `N8N_OIDC_CLIENT_SECRET` | OAuth2 client secret | *(required)* |
| `N8N_SSO_ENABLED` | Enable SSO integration | `true` |
| `N8N_USER_MANAGEMENT_AUTHENTICATION_METHOD` | Auth method | `oidc` |

### OIDC Endpoints

The integration automatically configures these OIDC endpoints:

- **Discovery**: `{AUTH_SERVICE_URL}/oauth2/.well-known/openid_configuration`
- **Authorization**: `{AUTH_SERVICE_URL}/oauth2/authorize`
- **Token**: `{AUTH_SERVICE_URL}/oauth2/token`
- **UserInfo**: `{AUTH_SERVICE_URL}/oauth2/userinfo`
- **JWKS**: `{AUTH_SERVICE_URL}/oauth2/jwks`

### User Attribute Mapping

| N8N Field | OIDC Claim | Description |
|-----------|------------|-------------|
| `id` | `sub` | Unique user identifier |
| `email` | `email` | User email address |
| `firstName` | `given_name` | User first name |
| `lastName` | `family_name` | User last name |
| `displayName` | `name` | Full display name |

## Troubleshooting

### Common Issues

**OIDC not available**
- Ensure you have N8N Enterprise license or are running the EE version
- Check that `N8N_USER_MANAGEMENT_AUTHENTICATION_METHOD=oidc`

**Client registration failed**
- Verify `AUTH_SERVICE_ADMIN_API_KEY` is valid
- Check that central auth service is running and accessible
- Ensure admin API endpoints are enabled

**Authentication redirects fail**
- Verify `N8N_BASE_URL` matches the actual N8N URL
- Check that redirect URI is registered: `{N8N_BASE_URL}/rest/sso/oidc/callback`
- Ensure both services are accessible from browser

**Database connection errors**
- N8N requires a database for user management and SSO
- Ensure PostgreSQL is running and accessible
- Verify database credentials in environment variables

### Debug Mode

Enable debug logging:

```bash
N8N_LOG_LEVEL=debug npm run dev
```

Check N8N logs for OIDC initialization messages and auth integration status.

### Testing Authentication

1. **Start all services** (auth service, database, redis, N8N)
2. **Navigate to N8N** → `http://localhost:5678`
3. **Click SSO login** → Should redirect to central auth service
4. **Complete authentication** → Should return to N8N with user logged in

## Integration Details

### How It Works

1. **Startup Integration**: The `n8n-auth-patch.ts` hooks into N8N's OIDC initialization
2. **Configuration Override**: Automatically configures OIDC endpoints to use central auth service
3. **Client Registration**: OAuth2 client is registered with proper redirect URIs and scopes
4. **Runtime Integration**: N8N's existing OIDC flow handles the rest seamlessly

### Code Changes

The integration makes minimal changes to N8N:

1. **Server startup hook** in `src/packages/cli/src/server.ts`
2. **Configuration patches** applied at runtime
3. **No core N8N modifications** - uses existing OIDC infrastructure

This ensures easy maintenance and updates while providing full SSO integration.

## Security Considerations

- **Client Secret Protection**: Store client secret securely, not in version control
- **HTTPS in Production**: Use HTTPS for all OAuth2 flows in production
- **Token Validation**: N8N validates tokens with central auth service JWKS endpoint
- **Session Security**: Redis sessions provide secure session management
- **Audit Logging**: All authentication events logged through N8N's audit system

## Production Deployment

### Docker Compose

```yaml
services:
  n8n:
    image: n8nio/n8n:latest
    environment:
      - N8N_USER_MANAGEMENT_AUTHENTICATION_METHOD=oidc
      - N8N_SSO_ENABLED=true
      - AUTH_SERVICE_URL=https://auth.yourdomain.com
      - N8N_OIDC_CLIENT_ID=n8n-service
      - N8N_OIDC_CLIENT_SECRET_FILE=/run/secrets/n8n_oidc_secret
    secrets:
      - n8n_oidc_secret
    depends_on:
      - postgres
      - redis

secrets:
  n8n_oidc_secret:
    external: true
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: n8n
spec:
  template:
    spec:
      containers:
      - name: n8n
        image: n8nio/n8n:latest
        env:
        - name: N8N_USER_MANAGEMENT_AUTHENTICATION_METHOD
          value: "oidc"
        - name: N8N_SSO_ENABLED
          value: "true"
        - name: AUTH_SERVICE_URL
          value: "https://auth.yourdomain.com"
        - name: N8N_OIDC_CLIENT_ID
          value: "n8n-service"
        - name: N8N_OIDC_CLIENT_SECRET
          valueFrom:
            secretKeyRef:
              name: n8n-oidc
              key: client-secret
```

## Support

For issues with N8N SSO integration:

1. Check N8N logs for OIDC errors
2. Verify central auth service is accessible
3. Test OAuth2 flow with curl/Postman
4. Review client registration in auth service admin panel

The integration leverages N8N's existing enterprise SSO capabilities, so most troubleshooting follows standard OIDC debugging practices.