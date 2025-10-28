"""
JWT-based authentication framework for the Mental Prosthetic Platform.

Provides unified authentication across all 37 integrated tools
with executive function accommodations and session management.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Any, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from pydantic import BaseModel, BaseSettings

logger = logging.getLogger(__name__)


class AuthSettings(BaseSettings):
    """Authentication configuration settings."""

    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # Password hashing
    pwd_hash_schemes: list[str] = ["bcrypt"]
    pwd_deprecated: str = "auto"

    class Config:
        env_prefix = "AUTH_"


class TokenData(BaseModel):
    """JWT token data structure."""
    user_id: str
    username: str
    scopes: list[str] = []
    expires_at: datetime


class UserCredentials(BaseModel):
    """User authentication credentials."""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class AuthManager:
    """
    Authentication manager for cross-domain security.

    Handles JWT token creation, validation, and user session management
    across all 37 integrated tools with executive function accommodations.
    """

    def __init__(self, settings: AuthSettings | None = None):
        self.settings = settings or AuthSettings()
        self.pwd_context = CryptContext(
            schemes=self.settings.pwd_hash_schemes,
            deprecated=self.settings.pwd_deprecated
        )
        self.security = HTTPBearer()

    def hash_password(self, password: str) -> str:
        """Generate password hash."""
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(
        self,
        user_id: str,
        username: str,
        scopes: list[str] | None = None
    ) -> str:
        """Create JWT access token."""
        expires_delta = timedelta(
            minutes=self.settings.jwt_access_token_expire_minutes
        )
        expires_at = datetime.utcnow() + expires_delta

        payload = {
            "sub": user_id,
            "username": username,
            "scopes": scopes or [],
            "exp": expires_at,
            "iat": datetime.utcnow(),
            "type": "access"
        }

        return jwt.encode(
            payload,
            self.settings.jwt_secret_key,
            algorithm=self.settings.jwt_algorithm
        )

    def create_refresh_token(
        self,
        user_id: str,
        username: str
    ) -> str:
        """Create JWT refresh token."""
        expires_delta = timedelta(
            days=self.settings.jwt_refresh_token_expire_days)
        expires_at = datetime.utcnow() + expires_delta

        payload = {
            "sub": user_id,
            "username": username,
            "exp": expires_at,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }

        return jwt.encode(
            payload,
            self.settings.jwt_secret_key,
            algorithm=self.settings.jwt_algorithm
        )

    def verify_token(self, token: str) -> TokenData:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.settings.jwt_secret_key,
                algorithms=[self.settings.jwt_algorithm]
            )

            user_id = payload.get("sub")
            username = payload.get("username")
            scopes = payload.get("scopes", [])
            expires_at = datetime.fromtimestamp(payload.get("exp"))

            if not user_id or not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )

            return TokenData(
                user_id=user_id,
                username=username,
                scopes=scopes,
                expires_at=expires_at
            )

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> TokenData:
        """Extract current user from JWT token."""
        token = credentials.credentials
        return self.verify_token(token)

    def create_token_pair(
        self,
        user_id: str,
        username: str,
        scopes: list[str] | None = None
    ) -> TokenResponse:
        """Create access and refresh token pair."""
        access_token = self.create_access_token(user_id, username, scopes)
        refresh_token = self.create_refresh_token(user_id, username)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.settings.jwt_access_token_expire_minutes * 60
        )

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token."""
        try:
            payload = jwt.decode(
                refresh_token,
                self.settings.jwt_secret_key,
                algorithms=[self.settings.jwt_algorithm]
            )

            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )

            user_id = payload.get("sub")
            username = payload.get("username")

            if not user_id or not username:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token payload"
                )

            # Create new token pair
            return self.create_token_pair(user_id, username)

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )


# Global authentication manager
auth_manager = AuthManager()


# Dependency functions for FastAPI
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> TokenData:
    """FastAPI dependency to get current authenticated user."""
    return auth_manager.verify_token(credentials.credentials)


async def get_current_active_user(
    current_user: TokenData = Depends(get_current_user)
) -> TokenData:
    """FastAPI dependency to get current active user."""
    # Add additional checks here if needed (user active status, etc.)
    return current_user


# Scope-based authorization decorators
def require_scopes(required_scopes: list[str]):
    """Decorator to require specific scopes for endpoint access."""
    async def scope_checker(current_user: TokenData = Depends(get_current_user)):
        if not all(scope in current_user.scopes for scope in required_scopes):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions. Required: {required_scopes}"
            )
        return current_user
    return scope_checker


# Domain-specific scope definitions for 37-tool access control
DOMAIN_SCOPES = {
    "security": [
        "security:read", "security:write", "security:admin",
        "misp:access", "helk:access", "securityonion:access", "maltrail:access",
        "yara_x:access", "cyberchef:access", "nemesis:access", "apiscout:access",
        "brute_ratel:access", "meterpreter:access", "lscript:access",
        "rita:access", "software_forensic_kit:access"
    ],
    "productivity": [
        "productivity:read", "productivity:write", "productivity:admin",
        "n8n:access", "mealie:access", "dispatch:access", "actual:access",
        "firecrawl:access", "goose:access", "it_tools:access", "inspector:access"
    ],
    "mtg": [
        "mtg:read", "mtg:write", "mtg:admin",
        "commander_spellbook:access", "mtg_commander_map:access",
        "mtg_scripting_toolkit:access", "card_analysis:access"
    ],
    "infrastructure": [
        "infrastructure:read", "infrastructure:write", "infrastructure:admin",
        "kong:access", "ghostwriter:access", "kasmvnc:access",
        "chroma_mcp:access", "filescopemcp:access", "firecrawl_mcp:access",
        "n8n_mcp:access", "malwarebazaar_mcp:access", "mcp_virustotal:access",
        "onex:access", "hexstrike_ai:access", "blackarch:access"
    ]
}


# Executive function accommodation settings
EXECUTIVE_FUNCTION_SCOPES = [
    "adhd:accommodations",
    "autism:accommodations",
    "ui:preferences",
    "context:preservation",
    "rapid:access"
]


if __name__ == "__main__":
    # Test authentication functionality
    async def test_auth():
        auth = AuthManager()

        # Test password hashing
        password = "test_password"
        hashed = auth.hash_password(password)
        print(f"Password hash: {hashed}")
        print(f"Verification: {auth.verify_password(password, hashed)}")

        # Test token creation
        token_response = auth.create_token_pair(
            "user123",
            "testuser",
            ["security:read", "productivity:write"]
        )
        print(f"Token response: {token_response}")

        # Test token verification
        token_data = auth.verify_token(token_response.access_token)
        print(f"Token data: {token_data}")

    asyncio.run(test_auth())
