# Python Auth Client for Modular Monolith Authentication Service

import base64
import hashlib
import secrets
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlencode, urlparse

import requests


@dataclass
class AuthToken:
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 3600


@dataclass
class User:
    id: str
    email: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    email_verified: bool = False
    mfa_enabled: bool = False
    organization_id: Optional[str] = None
    roles: Optional[List[str]] = None
    permissions: Optional[List[str]] = None


class AuthClientError(Exception):
    def __init__(self, message: str, code: Optional[str] = None, details: Any = None):
        self.message = message
        self.code = code
        self.details = details
        super().__init__(message)


class AuthClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None

        # Set up session with default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

    def _make_request(self, method: str, path: str, **kwargs) -> requests.Response:
        """Make HTTP request with automatic token refresh"""
        url = f"{self.base_url}{path}"

        # Add authorization header if we have a token
        if self.access_token:
            kwargs.setdefault('headers', {})[
                'Authorization'] = f"Bearer {self.access_token}"

        response = self.session.request(
            method, url, timeout=self.timeout, **kwargs)

        # Try to refresh token on 401
        if response.status_code == 401 and self.refresh_token:
            try:
                self.refresh_access_token()
                # Retry the original request
                kwargs.setdefault('headers', {})[
                    'Authorization'] = f"Bearer {self.access_token}"
                response = self.session.request(
                    method, url, timeout=self.timeout, **kwargs)
            except AuthClientError:
                # Refresh failed, clear tokens
                self.clear_tokens()
                raise

        return response

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions"""
        try:
            data = response.json()
        except ValueError:
            data = {'error': {'code': 'INVALID_RESPONSE',
                              'message': 'Invalid JSON response'}}

        if not response.ok:
            error = data.get('error', {})
            raise AuthClientError(
                message=error.get('message', f'HTTP {response.status_code}'),
                code=error.get('code'),
                details=error.get('details')
            )

        return data

    def login(self, email: str, password: str, organization_id: Optional[str] = None,
              mfa_code: Optional[str] = None, remember_me: bool = False) -> Dict[str, Any]:
        """Login with email and password"""
        data = {
            'email': email,
            'password': password,
            'rememberMe': remember_me
        }

        if organization_id:
            data['organizationId'] = organization_id
        if mfa_code:
            data['mfaCode'] = mfa_code

        response = self._make_request('POST', '/auth/login', json=data)
        result = self._handle_response(response)

        # Store tokens if login successful
        if result.get('success') and result.get('tokens'):
            tokens = result['tokens']
            self.access_token = tokens['accessToken']
            self.refresh_token = tokens.get('refreshToken')

        return result

    def register(self, email: str, password: str, first_name: Optional[str] = None,
                 last_name: Optional[str] = None, organization_id: Optional[str] = None) -> Dict[str, Any]:
        """Register new user"""
        data = {
            'email': email,
            'password': password
        }

        if first_name:
            data['firstName'] = first_name
        if last_name:
            data['lastName'] = last_name
        if organization_id:
            data['organizationId'] = organization_id

        response = self._make_request('POST', '/auth/register', json=data)
        return self._handle_response(response)

    def logout(self) -> None:
        """Logout current user"""
        try:
            self._make_request('POST', '/auth/logout')
        except Exception:
            # Continue with logout even if server request fails
            pass
        finally:
            self.clear_tokens()

    def refresh_access_token(self) -> Dict[str, Any]:
        """Refresh access token using refresh token"""
        if not self.refresh_token:
            raise AuthClientError('No refresh token available')

        response = self._make_request('POST', '/auth/refresh', json={
            'refreshToken': self.refresh_token
        })
        result = self._handle_response(response)

        # Update tokens
        if result.get('success') and result.get('tokens'):
            tokens = result['tokens']
            self.access_token = tokens['accessToken']
            if tokens.get('refreshToken'):
                self.refresh_token = tokens['refreshToken']

        return result

    def get_profile(self) -> Dict[str, Any]:
        """Get current user profile"""
        response = self._make_request('GET', '/users/me')
        return self._handle_response(response)

    def verify_email(self, token: str) -> Dict[str, Any]:
        """Verify email address"""
        response = self._make_request(
            'POST', '/auth/verify-email', json={'token': token})
        return self._handle_response(response)

    def request_password_reset(self, email: str) -> Dict[str, Any]:
        """Request password reset"""
        response = self._make_request(
            'POST', '/auth/reset-password/request', json={'email': email})
        return self._handle_response(response)

    def reset_password(self, token: str, new_password: str) -> Dict[str, Any]:
        """Reset password with token"""
        response = self._make_request('POST', '/auth/reset-password', json={
            'token': token,
            'newPassword': new_password
        })
        return self._handle_response(response)

    def set_tokens(self, access_token: str, refresh_token: Optional[str] = None) -> None:
        """Set authentication tokens"""
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token

    def clear_tokens(self) -> None:
        """Clear all authentication tokens"""
        self.access_token = None
        self.refresh_token = None

    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.access_token is not None


class OAuth2Client(AuthClient):
    """OAuth2 specific client implementation"""

    def __init__(self, base_url: str, client_id: str, client_secret: Optional[str] = None,
                 redirect_uri: str = '', scope: Optional[List[str]] = None, use_pkce: bool = True):
        super().__init__(base_url)
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope or ['openid', 'profile', 'email']
        self.use_pkce = use_pkce

    def generate_authorization_url(self, state: Optional[str] = None) -> Dict[str, str]:
        """Generate OAuth2 authorization URL"""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scope),
        }

        if state:
            params['state'] = state

        code_verifier = None
        if self.use_pkce:
            code_verifier = self._generate_code_verifier()
            code_challenge = self._generate_code_challenge(code_verifier)
            params['code_challenge'] = code_challenge
            params['code_challenge_method'] = 'S256'

        auth_url = f"{self.base_url}/oauth2/authorize?{urlencode(params)}"

        result = {'auth_url': auth_url}
        if code_verifier:
            result['code_verifier'] = code_verifier

        return result

    def exchange_code_for_token(self, code: str, code_verifier: Optional[str] = None) -> Dict[str, Any]:
        """Exchange authorization code for tokens"""
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
        }

        if self.client_secret:
            data['client_secret'] = self.client_secret

        if code_verifier:
            data['code_verifier'] = code_verifier

        response = self._make_request('POST', '/oauth2/token', json=data)
        result = self._handle_response(response)

        # Store tokens
        if result.get('access_token'):
            self.access_token = result['access_token']
            self.refresh_token = result.get('refresh_token')

        return result

    def get_user_info(self, access_token: Optional[str] = None) -> Dict[str, Any]:
        """Get OIDC user info"""
        token = access_token or self.access_token
        if not token:
            raise AuthClientError('No access token available')

        headers = {'Authorization': f'Bearer {token}'}
        response = self._make_request(
            'GET', '/oauth2/userinfo', headers=headers)
        return self._handle_response(response)

    def _generate_code_verifier(self) -> str:
        """Generate PKCE code verifier"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')

    def _generate_code_challenge(self, verifier: str) -> str:
        """Generate PKCE code challenge"""
        digest = hashlib.sha256(verifier.encode('utf-8')).digest()
        return base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')


# FastAPI integration
try:
    from fastapi import Depends, HTTPException
    from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

    class FastAPIAuthMiddleware:
        def __init__(self, auth_client: AuthClient):
            self.auth_client = auth_client
            self.security = HTTPBearer(auto_error=False)

        async def get_current_user(self, credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))):
            if not credentials:
                raise HTTPException(
                    status_code=401, detail="Authentication required")

            try:
                # Set token and get profile
                self.auth_client.set_tokens(credentials.credentials)
                profile = self.auth_client.get_profile()
                return profile
            except AuthClientError as e:
                raise HTTPException(status_code=401, detail=str(e))

        def require_roles(self, required_roles: List[str]):
            async def check_roles(user=Depends(self.get_current_user)):
                user_roles = user.get('roles', [])
                if not any(role in user_roles for role in required_roles):
                    raise HTTPException(
                        status_code=403, detail="Insufficient permissions")
                return user
            return check_roles

except ImportError:
    # FastAPI not available
    pass
