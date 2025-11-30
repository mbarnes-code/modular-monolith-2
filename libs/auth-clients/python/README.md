# Python Auth Client

Python client library for the Modular Monolith Authentication Service.

## Installation

```bash
pip install modular-monolith-auth-client
```

For FastAPI integration:
```bash
pip install modular-monolith-auth-client[fastapi]
```

## Quick Start

### Basic Usage

```python
from auth_client import AuthClient

# Initialize client
client = AuthClient('http://auth-service:3001')

# Login
result = client.login('user@example.com', 'password')
if result['success']:
    print(f"Logged in as {result['user']['email']}")

# Get user profile
profile = client.get_profile()
print(f"User: {profile['firstName']} {profile['lastName']}")

# Logout
client.logout()
```

### OAuth2 Flow

```python
from auth_client import OAuth2Client

# Initialize OAuth2 client
oauth_client = OAuth2Client(
    base_url='http://auth-service:3001',
    client_id='your-client-id',
    client_secret='your-client-secret',  # Optional for public clients
    redirect_uri='http://your-app/callback',
    scope=['openid', 'profile', 'email']
)

# Generate authorization URL
auth_data = oauth_client.generate_authorization_url(state='random-state')
print(f"Visit: {auth_data['auth_url']}")

# Exchange code for tokens (after user returns from auth server)
tokens = oauth_client.exchange_code_for_token(
    code='authorization-code',
    code_verifier=auth_data.get('code_verifier')  # For PKCE
)

# Get user info
user_info = oauth_client.get_user_info()
print(f"User: {user_info['name']}")
```

### FastAPI Integration

```python
from fastapi import FastAPI, Depends
from auth_client import AuthClient, FastAPIAuthMiddleware

app = FastAPI()

# Initialize auth
auth_client = AuthClient('http://auth-service:3001')
auth_middleware = FastAPIAuthMiddleware(auth_client)

# Protected endpoint
@app.get("/profile")
async def get_profile(user=Depends(auth_middleware.get_current_user)):
    return {"user": user}

# Role-based protection
@app.get("/admin")
async def admin_only(user=Depends(auth_middleware.require_roles(['admin']))):
    return {"message": "Admin access granted"}
```

## API Reference

### AuthClient

Main client for interacting with the authentication service.

#### Methods

- `login(email, password, organization_id=None, mfa_code=None, remember_me=False)`
- `register(email, password, first_name=None, last_name=None, organization_id=None)`
- `logout()`
- `refresh_access_token()`
- `get_profile()`
- `verify_email(token)`
- `request_password_reset(email)`
- `reset_password(token, new_password)`
- `set_tokens(access_token, refresh_token=None)`
- `clear_tokens()`
- `is_authenticated()`

### OAuth2Client

OAuth2/OIDC specific client extending AuthClient.

#### Methods

- `generate_authorization_url(state=None)`
- `exchange_code_for_token(code, code_verifier=None)`
- `get_user_info(access_token=None)`

### FastAPIAuthMiddleware

Integration with FastAPI for automatic authentication.

#### Methods

- `get_current_user()` - Dependency for getting authenticated user
- `require_roles(required_roles)` - Dependency for role-based access control

## Error Handling

```python
from auth_client import AuthClient, AuthClientError

client = AuthClient('http://auth-service:3001')

try:
    result = client.login('user@example.com', 'wrong-password')
except AuthClientError as e:
    print(f"Auth error: {e.code} - {e.message}")
    if e.details:
        print(f"Details: {e.details}")
```

## Configuration

### Environment Variables

```bash
AUTH_SERVICE_URL=http://auth-service:3001
AUTH_CLIENT_TIMEOUT=10
```

### Using Environment Variables

```python
import os
from auth_client import AuthClient

client = AuthClient(
    base_url=os.getenv('AUTH_SERVICE_URL', 'http://localhost:3001'),
    timeout=int(os.getenv('AUTH_CLIENT_TIMEOUT', '10'))
)
```

## Development

### Setup

```bash
git clone https://github.com/mbarnes-code/modular-monolith-2
cd libs/auth-clients/python
pip install -e .[dev]
```

### Testing

```bash
pytest
```

### Code Quality

```bash
black .
isort .
flake8
mypy auth_client.py
```

## License

MIT