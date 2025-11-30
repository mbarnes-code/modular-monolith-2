# Auth Service

Central authentication service providing OAuth2/OIDC, user management, and SSO for the modular monolith.

## Features

- **OAuth2/OIDC Provider**: Complete OAuth2 authorization server with PKCE support
- **User Management**: Registration, email verification, password reset
- **Multi-Factor Authentication**: TOTP-based MFA support
- **Session Management**: Redis-based centralized sessions
- **JWT Tokens**: Secure access and refresh token handling
- **Rate Limiting**: Protection against brute force attacks
- **Audit Logging**: Comprehensive authentication event tracking
- **Multi-Tenancy**: Organization-based user segregation
- **API Documentation**: Swagger/OpenAPI documentation

## Quick Start

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```

4. **Access API documentation**:
   Open http://localhost:3001/docs

## Environment Variables

See `.env.example` for all required environment variables.

### Critical Security Variables

```bash
JWT_SECRET=your-jwt-secret-change-in-production
JWT_REFRESH_SECRET=your-refresh-secret-change-in-production
API_KEY_SALT=your-api-key-salt-change-in-production
```

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/refresh` - Refresh access token
- `POST /auth/logout` - User logout
- `POST /auth/verify-email` - Verify email address
- `POST /auth/reset-password/request` - Request password reset
- `POST /auth/reset-password` - Reset password

### OAuth2/OIDC
- `GET /oauth2/authorize` - OAuth2 authorization endpoint
- `POST /oauth2/token` - OAuth2 token endpoint
- `GET /oauth2/userinfo` - OIDC UserInfo endpoint
- `GET /oauth2/.well-known/openid-configuration` - OIDC Discovery
- `GET /oauth2/.well-known/jwks.json` - JSON Web Key Set

### User Management
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update user profile
- `POST /users/me/change-password` - Change password
- `POST /users/me/enable-mfa` - Enable MFA
- `POST /users/me/disable-mfa` - Disable MFA

### Organizations
- `GET /organizations` - List organizations
- `GET /organizations/:id` - Get organization details
- `PUT /organizations/:id` - Update organization

### Admin
- `GET /admin/users` - List all users (admin only)
- `GET /admin/audit-logs` - View audit logs (admin only)

## Authentication Flow

### Standard Login Flow
1. Client sends credentials to `POST /auth/login`
2. Service validates credentials and generates tokens
3. Service returns access token, refresh token, and sets session cookie
4. Client uses access token for API requests

### OAuth2 Authorization Code Flow
1. Client redirects to `GET /oauth2/authorize`
2. User authenticates via login form
3. Service redirects back with authorization code
4. Client exchanges code for tokens at `POST /oauth2/token`
5. Client uses access token for API requests

### PKCE Flow (for public clients)
1. Client generates code verifier and challenge
2. Client includes challenge in authorization request
3. Client includes verifier in token exchange
4. Service validates PKCE parameters for security

## Integration with Services

### Express.js Applications
```typescript
import { ExpressAuthMiddleware } from '@modular-monolith/auth-core';

const authMiddleware = new ExpressAuthMiddleware(config);
app.use('/api', authMiddleware.authenticate());
```

### FastAPI Applications
```python
# Python integration coming soon
```

### Frontend Applications
```javascript
// Redirect to auth service for login
window.location.href = 'http://auth-service:3001/oauth2/authorize?client_id=your-app&redirect_uri=...';

// Or use direct API calls
const response = await fetch('http://auth-service:3001/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
```

## Development

### Build
```bash
npm run build
```

### Test
```bash
npm test
```

### Linting
```bash
npm run lint
```

### Production
```bash
npm start
```

## Database Schema

The service uses Prisma for database access. Database models are defined in the auth-core library.

Required tables:
- `users` - User accounts
- `roles` - User roles
- `permissions` - System permissions
- `organizations` - Multi-tenant organizations
- `api_keys` - API key management
- `audit_logs` - Authentication events

## Redis Usage

Redis is used for:
- Session storage
- Token blacklisting
- Rate limiting
- MFA challenges
- Password reset tokens

## Security Features

- **Password Hashing**: bcrypt with configurable rounds
- **JWT Security**: Secure token generation and validation
- **Rate Limiting**: Configurable request throttling
- **Account Lockout**: Automatic lockout after failed attempts
- **CSRF Protection**: Built-in CSRF token validation
- **Audit Logging**: All authentication events logged
- **Multi-Factor Auth**: TOTP-based MFA support

## Monitoring

The service provides health check endpoints and structured logging for monitoring:

- `GET /health` - Service health check
- All requests logged with correlation IDs
- Authentication events logged for security monitoring

## License

MIT