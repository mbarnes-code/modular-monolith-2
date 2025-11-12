"""
OAuth2 Authentication for Jane Executive Function Platform - T140
Secure remote access with executive function accommodations
"""

import base64
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlencode

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
from passlib.context import CryptContext
from pydantic import BaseModel, Field, validator

from ...config.security import get_tls_config


class OAuth2Configuration(BaseModel):
    """OAuth2 configuration settings"""

    # JWT Settings
    jwt_secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="JWT signing secret key"
    )
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(
        default=60,  # 1 hour - executive function friendly
        description="Access token expiration in minutes"
    )
    refresh_token_expire_days: int = Field(
        default=30,  # 30 days
        description="Refresh token expiration in days"
    )

    # OAuth2 Client Settings
    client_id: str = Field(
        default="jane-platform-client",
        description="OAuth2 client ID"
    )
    client_secret: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="OAuth2 client secret"
    )

    # Authorization Settings
    auth_code_expire_minutes: int = Field(
        default=10,  # 10 minutes for auth code
        description="Authorization code expiration"
    )

    # Scopes for executive function tools
    available_scopes: Dict[str, str] = Field(
        default={
            "security:read": "Read access to security tools",
            "security:write": "Write access to security tools",
            "productivity:read": "Read access to productivity tools",
            "productivity:write": "Write access to productivity tools",
            "mtg:read": "Read access to MTG tools",
            "mtg:write": "Write access to MTG tools",
            "infrastructure:read": "Read access to infrastructure tools",
            "infrastructure:write": "Write access to infrastructure tools",
            "profile": "Access to user profile information",
            "offline_access": "Offline access via refresh tokens"
        }
    )

    # PKCE Settings (for mobile/SPA security)
    require_pkce: bool = Field(
        default=True,
        description="Require PKCE for authorization code flow"
    )

    class Config:
        env_prefix = "JANE_OAUTH2_"


class OAuth2User(BaseModel):
    """OAuth2 user model"""

    user_id: str
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: bool = True
    scopes: List[str] = []
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="Executive function preferences"
    )

    # Executive function accommodations
    ui_response_timeout: int = Field(
        default=200,  # <200ms requirement
        description="UI response timeout preference (ms)"
    )
    focus_mode_enabled: bool = Field(
        default=False,
        description="Reduced distraction interface"
    )
    notification_preferences: Dict[str, bool] = Field(
        default_factory=lambda: {
            "sound_alerts": True,
            "visual_alerts": True,
            "email_notifications": False
        }
    )


class OAuth2Token(BaseModel):
    """OAuth2 token response"""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class AuthorizationCode(BaseModel):
    """Authorization code storage"""

    code: str
    client_id: str
    user_id: str
    scopes: List[str]
    redirect_uri: str
    code_challenge: Optional[str] = None
    code_challenge_method: Optional[str] = None
    expires_at: datetime
    used: bool = False


class OAuth2Provider:
    """
    OAuth2 Provider for Jane Executive Function Platform
    Implements authorization code flow with PKCE support
    """

    def __init__(self, config: OAuth2Configuration):
        self.config = config
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto"
        )

        # In-memory storage (replace with database in production)
        self.users: Dict[str, OAuth2User] = {}
        self.auth_codes: Dict[str, AuthorizationCode] = {}
        self.refresh_tokens: Dict[str, Dict[str, Any]] = {}

        # Initialize default admin user
        self._create_default_user()

    def _create_default_user(self):
        """Create default admin user for development"""
        admin_user = OAuth2User(
            user_id="admin",
            username="admin",
            email="admin@jane-platform.local",
            full_name="Jane Platform Administrator",
            scopes=list(self.config.available_scopes.keys()),
            preferences={
                "ui_theme": "auto",
                "dashboard_layout": "compact",
                "default_domain": "security"
            }
        )
        self.users["admin"] = admin_user

    def authenticate_user(self, username: str, password: str) -> Optional[OAuth2User]:
        """
        Authenticate user credentials
        In production, integrate with external identity provider
        """
        # Development authentication - replace with real auth
        if username == "admin" and password == "admin":
            return self.users.get("admin")
        return None

    def validate_client(self, client_id: str, client_secret: Optional[str] = None) -> bool:
        """Validate OAuth2 client credentials"""
        if client_id != self.config.client_id:
            return False

        if client_secret is not None:
            return client_secret == self.config.client_secret

        return True

    def validate_scopes(self, requested_scopes: List[str]) -> List[str]:
        """Validate and filter requested scopes"""
        valid_scopes = []
        for scope in requested_scopes:
            if scope in self.config.available_scopes:
                valid_scopes.append(scope)
        return valid_scopes

    def generate_authorization_code(
        self,
        client_id: str,
        user_id: str,
        scopes: List[str],
        redirect_uri: str,
        code_challenge: Optional[str] = None,
        code_challenge_method: Optional[str] = None
    ) -> str:
        """Generate authorization code"""

        # Generate secure random code
        code = secrets.token_urlsafe(32)

        # Store authorization code
        auth_code = AuthorizationCode(
            code=code,
            client_id=client_id,
            user_id=user_id,
            scopes=scopes,
            redirect_uri=redirect_uri,
            code_challenge=code_challenge,
            code_challenge_method=code_challenge_method,
            expires_at=datetime.utcnow() + timedelta(
                minutes=self.config.auth_code_expire_minutes
            )
        )

        self.auth_codes[code] = auth_code
        return code

    def exchange_authorization_code(
        self,
        code: str,
        client_id: str,
        client_secret: Optional[str],
        redirect_uri: str,
        code_verifier: Optional[str] = None
    ) -> OAuth2Token:
        """Exchange authorization code for tokens"""

        # Validate client
        if not self.validate_client(client_id, client_secret):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid client credentials"
            )

        # Get authorization code
        auth_code = self.auth_codes.get(code)
        if not auth_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid authorization code"
            )

        # Check if code is expired or used
        if auth_code.used or datetime.utcnow() > auth_code.expires_at:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authorization code expired or already used"
            )

        # Validate redirect URI
        if auth_code.redirect_uri != redirect_uri:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid redirect URI"
            )

        # Validate PKCE if required
        if self.config.require_pkce and auth_code.code_challenge:
            if not code_verifier:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Code verifier required"
                )

            # Verify code challenge
            if auth_code.code_challenge_method == "S256":
                code_challenge = base64.urlsafe_b64encode(
                    hashlib.sha256(code_verifier.encode()).digest()
                ).decode().rstrip("=")
            else:
                code_challenge = code_verifier

            if code_challenge != auth_code.code_challenge:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid code verifier"
                )

        # Mark code as used
        auth_code.used = True

        # Get user
        user = self.users.get(auth_code.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User not found"
            )

        # Generate tokens
        access_token = self.create_access_token(
            user_id=user.user_id,
            scopes=auth_code.scopes
        )

        refresh_token = self.create_refresh_token(
            user_id=user.user_id,
            scopes=auth_code.scopes
        )

        return OAuth2Token(
            access_token=access_token,
            expires_in=self.config.access_token_expire_minutes * 60,
            refresh_token=refresh_token,
            scope=" ".join(auth_code.scopes)
        )

    def create_access_token(
        self,
        user_id: str,
        scopes: List[str],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.config.access_token_expire_minutes
            )

        # Get user preferences for executive function accommodations
        user = self.users.get(user_id)
        preferences = user.preferences if user else {}

        to_encode = {
            "sub": user_id,
            "scopes": scopes,
            "exp": expire,
            "iat": datetime.utcnow(),
            "iss": "jane-platform",
            "aud": "jane-platform-api",
            "preferences": preferences  # Include user preferences in token
        }

        encoded_jwt = jwt.encode(
            to_encode,
            self.config.jwt_secret_key,
            algorithm=self.config.jwt_algorithm
        )

        return encoded_jwt

    def create_refresh_token(self, user_id: str, scopes: List[str]) -> str:
        """Create refresh token"""
        refresh_token = secrets.token_urlsafe(32)

        self.refresh_tokens[refresh_token] = {
            "user_id": user_id,
            "scopes": scopes,
            "expires_at": datetime.utcnow() + timedelta(
                days=self.config.refresh_token_expire_days
            )
        }

        return refresh_token

    def refresh_access_token(self, refresh_token: str) -> OAuth2Token:
        """Refresh access token using refresh token"""

        token_data = self.refresh_tokens.get(refresh_token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        if datetime.utcnow() > token_data["expires_at"]:
            del self.refresh_tokens[refresh_token]
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token expired"
            )

        # Generate new access token
        access_token = self.create_access_token(
            user_id=token_data["user_id"],
            scopes=token_data["scopes"]
        )

        return OAuth2Token(
            access_token=access_token,
            expires_in=self.config.access_token_expire_minutes * 60,
            scope=" ".join(token_data["scopes"])
        )

    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode access token"""
        try:
            payload = jwt.decode(
                token,
                self.config.jwt_secret_key,
                algorithms=[self.config.jwt_algorithm],
                audience="jane-platform-api",
                issuer="jane-platform"
            )
            return payload
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Global OAuth2 provider instance
oauth_config = OAuth2Configuration()
oauth_provider = OAuth2Provider(oauth_config)

# FastAPI OAuth2 scheme
oauth2_scheme = HTTPBearer()


async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme)
) -> OAuth2User:
    """
    Get current authenticated user from access token
    Executive function accommodation: includes user preferences
    """
    try:
        # Extract token from Bearer header
        token_str = token.credentials

        # Verify token
        payload = oauth_provider.verify_access_token(token_str)

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        # Get user
        user = oauth_provider.users.get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        # Update user with token preferences (executive function support)
        if "preferences" in payload:
            user.preferences.update(payload["preferences"])

        return user

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token validation failed: {str(e)}"
        )


def require_scopes(*required_scopes: str):
    """
    Dependency factory for scope-based authorization
    Executive function accommodation: clear scope requirements
    """
    def scope_checker(current_user: OAuth2User = Depends(get_current_user)):
        user_scopes = set(current_user.scopes)
        required_scopes_set = set(required_scopes)

        if not required_scopes_set.issubset(user_scopes):
            missing_scopes = required_scopes_set - user_scopes
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Missing scopes: {', '.join(missing_scopes)}"
            )

        return current_user

    return scope_checker


def get_oauth_provider() -> OAuth2Provider:
    """Get OAuth2 provider instance"""
    return oauth_provider


def get_oauth_config() -> OAuth2Configuration:
    """Get OAuth2 configuration"""
    return oauth_config
