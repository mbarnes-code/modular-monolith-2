"""
Shared authentication library for Mental Prosthetic Platform.

Provides unified authentication across all 37 integrated tools with:
- JWT token creation and validation
- Password hashing with secure algorithms
- API key management
- Session management
- Security middleware patterns
- Executive function accommodations
"""

import secrets
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

try:
    from pydantic import BaseSettings
except ImportError:
    from pydantic_settings import BaseSettings

from ..logging import get_logger


class TokenType(str, Enum):
    """JWT token types."""
    ACCESS = "access"
    REFRESH = "refresh"
    API_KEY = "api_key"
    VERIFICATION = "verification"
    PASSWORD_RESET = "password_reset"


class AuthProvider(str, Enum):
    """Authentication providers."""
    LOCAL = "local"
    OAUTH2 = "oauth2"
    LDAP = "ldap"
    API_KEY = "api_key"
    MISP = "misp"  # MISP-compatible auth


class AuthConfig(BaseSettings):
    """Authentication configuration settings."""

    # JWT settings
    secret_key: str = "your-secret-key-change-this"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # Password settings
    password_min_length: int = 8
    password_require_uppercase: bool = True
    password_require_lowercase: bool = True
    password_require_numbers: bool = True
    password_require_special: bool = True

    # Session settings
    session_timeout_minutes: int = 60
    max_concurrent_sessions: int = 5

    # API key settings
    api_key_length: int = 64
    api_key_prefix: str = "mp_"  # Mental Prosthetic prefix

    # Security settings
    bcrypt_rounds: int = 12
    rate_limit_attempts: int = 5
    lockout_duration_minutes: int = 15

    # Executive function accommodations
    clear_error_messages: bool = True
    progressive_security_hints: bool = True

    class Config:
        env_prefix = "AUTH_"


class TokenPayload(BaseModel):
    """JWT token payload structure."""

    sub: str  # Subject (user ID)
    exp: datetime  # Expiration time
    iat: datetime  # Issued at time
    type: TokenType  # Token type

    # User information
    username: Optional[str] = None
    email: Optional[str] = None
    roles: List[str] = []
    permissions: List[str] = []

    # Context for executive function support
    session_id: Optional[str] = None
    adhd_accommodations: Dict[str, Any] = {}

    # MISP compatibility
    authkey_id: Optional[str] = None
    org_id: Optional[str] = None


class AuthUser(BaseModel):
    """Authenticated user model."""

    id: str
    username: str
    email: str
    roles: List[str] = []
    permissions: List[str] = []
    is_active: bool = True
    is_verified: bool = True

    # Executive function support
    adhd_accommodations: Dict[str, Any] = {}
    preferred_auth_method: AuthProvider = AuthProvider.LOCAL

    # MISP compatibility
    authkey_id: Optional[str] = None
    org_id: Optional[str] = None

    # Session information
    session_id: Optional[str] = None
    last_login: Optional[datetime] = None


class AuthError(HTTPException):
    """Authentication error with user-friendly messages."""

    def __init__(
        self,
        status_code: int,
        detail: str,
        user_friendly_message: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        self.user_friendly_message = user_friendly_message or detail
        super().__init__(status_code, detail, headers)


class PasswordValidator:
    """Password validation with executive function accommodations."""

    def __init__(self, config: AuthConfig):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    def validate_password(self, password: str) -> Dict[str, Any]:
        """Validate password strength with clear feedback."""
        errors = []
        suggestions = []
        score = 0

        # Length check
        if len(password) < self.config.password_min_length:
            min_len = self.config.password_min_length
            errors.append(f"Password must be at least {min_len} characters")
            missing = min_len - len(password)
            suggestions.append(f"Add {missing} more characters")
        else:
            score += 1

        # Character type checks
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        if self.config.password_require_uppercase and not has_upper:
            errors.append("Password must contain uppercase letter")
            suggestions.append("Add an uppercase letter (A-Z)")
        elif has_upper:
            score += 1

        if self.config.password_require_lowercase and not has_lower:
            errors.append("Password must contain lowercase letter")
            suggestions.append("Add a lowercase letter (a-z)")
        elif has_lower:
            score += 1

        if self.config.password_require_numbers and not has_digit:
            errors.append("Password must contain at least one number")
            suggestions.append("Add a number (0-9)")
        elif has_digit:
            score += 1

        if self.config.password_require_special and not has_special:
            errors.append("Password must contain special character")
            suggestions.append("Add a special character (!@#$%^&*)")
        elif has_special:
            score += 1

        # Calculate strength
        strength = "weak"
        if score >= 4:
            strength = "strong"
        elif score >= 3:
            strength = "medium"

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "suggestions": (
                suggestions if self.config.progressive_security_hints else []
            ),
            "strength": strength,
            "score": score
        }


class TokenManager:
    """JWT token management with security best practices."""

    def __init__(self, config: AuthConfig):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    def create_access_token(
        self,
        user: AuthUser,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token."""
        if expires_delta is None:
            expires_delta = timedelta(
                minutes=self.config.access_token_expire_minutes
            )

        now = datetime.utcnow()
        payload = TokenPayload(
            sub=user.id,
            exp=now + expires_delta,
            iat=now,
            type=TokenType.ACCESS,
            username=user.username,
            email=user.email,
            roles=user.roles,
            permissions=user.permissions,
            session_id=user.session_id,
            adhd_accommodations=user.adhd_accommodations,
            authkey_id=user.authkey_id,
            org_id=user.org_id
        )

        return jwt.encode(
            payload.dict(),
            self.config.secret_key,
            algorithm=self.config.algorithm
        )

    def create_refresh_token(self, user: AuthUser) -> str:
        """Create JWT refresh token."""
        expires_delta = timedelta(days=self.config.refresh_token_expire_days)
        now = datetime.utcnow()

        payload = TokenPayload(
            sub=user.id,
            exp=now + expires_delta,
            iat=now,
            type=TokenType.REFRESH,
            session_id=user.session_id
        )

        return jwt.encode(
            payload.dict(),
            self.config.secret_key,
            algorithm=self.config.algorithm
        )

    def verify_token(self, token: str) -> TokenPayload:
        """Verify and decode JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm]
            )

            # Convert datetime strings back to datetime objects
            exp_str = payload["exp"].replace("Z", "+00:00")
            payload["exp"] = datetime.fromisoformat(exp_str)
            iat_str = payload["iat"].replace("Z", "+00:00")
            payload["iat"] = datetime.fromisoformat(iat_str)

            return TokenPayload(**payload)

        except jwt.ExpiredSignatureError:
            if self.config.clear_error_messages:
                raise AuthError(
                    401,
                    "Token has expired",
                    "Session expired. Please log in again."
                )
            raise AuthError(401, "Token expired")

        except jwt.InvalidTokenError:
            if self.config.clear_error_messages:
                raise AuthError(
                    401,
                    "Invalid token",
                    "Login issue detected. Please try again."
                )
            raise AuthError(401, "Invalid token")

    def create_api_key(self, user: AuthUser) -> str:
        """Create API key for programmatic access."""
        key = secrets.token_urlsafe(self.config.api_key_length)
        return f"{self.config.api_key_prefix}{key}"

    def verify_api_key_format(self, api_key: str) -> bool:
        """Verify API key format."""
        prefix_len = len(self.config.api_key_prefix)
        expected_length = prefix_len + self.config.api_key_length
        return (
            api_key.startswith(self.config.api_key_prefix) and
            len(api_key) == expected_length
        )


class PasswordManager:
    """Password hashing and verification."""

    def __init__(self, config: AuthConfig):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        salt = bcrypt.gensalt(rounds=self.config.bcrypt_rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                hashed.encode('utf-8')
            )
        except Exception as e:
            self.logger.error(f"Password verification error: {e}")
            return False


class AuthManager:
    """Main authentication manager."""

    def __init__(self, config: Optional[AuthConfig] = None):
        self.config = config or AuthConfig()
        self.logger = get_logger(self.__class__.__name__)

        self.token_manager = TokenManager(self.config)
        self.password_manager = PasswordManager(self.config)
        self.password_validator = PasswordValidator(self.config)

    def authenticate_user(
        self,
        username: str,
        password: str,
        provider: AuthProvider = AuthProvider.LOCAL
    ) -> Optional[AuthUser]:
        """Authenticate user with credentials."""
        # This would typically query a database
        # For now, return None (not implemented)
        self.logger.warning(
            "User authentication not implemented - override this method"
        )
        return None

    def authenticate_api_key(self, api_key: str) -> Optional[AuthUser]:
        """Authenticate user with API key."""
        if not self.token_manager.verify_api_key_format(api_key):
            return None

        # This would typically query a database
        # For now, return None (not implemented)
        self.logger.warning(
            "API key authentication not implemented - override this method"
        )
        return None

    def create_session(self, user: AuthUser) -> Dict[str, str]:
        """Create user session with tokens."""
        # Generate session ID
        user.session_id = secrets.token_urlsafe(32)
        user.last_login = datetime.utcnow()

        # Create tokens
        access_token = self.token_manager.create_access_token(user)
        refresh_token = self.token_manager.create_refresh_token(user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": self.config.access_token_expire_minutes * 60
        }

    def refresh_session(self, refresh_token: str) -> Dict[str, str]:
        """Refresh user session with new access token."""
        try:
            payload = self.token_manager.verify_token(refresh_token)

            if payload.type != TokenType.REFRESH:
                raise AuthError(401, "Invalid token type")

            # Get user (this would typically query a database)
            user = AuthUser(
                id=payload.sub,
                username=payload.username or "",
                email=payload.email or "",
                roles=payload.roles,
                permissions=payload.permissions,
                session_id=payload.session_id,
                adhd_accommodations=payload.adhd_accommodations,
                authkey_id=payload.authkey_id,
                org_id=payload.org_id
            )

            # Create new access token
            access_token = self.token_manager.create_access_token(user)

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": self.config.access_token_expire_minutes * 60
            }

        except Exception as e:
            if self.config.clear_error_messages:
                raise AuthError(
                    401,
                    "Failed to refresh token",
                    "Please log in again to continue using the application."
                )
            raise e

    def validate_password(self, password: str) -> Dict[str, Any]:
        """Validate password strength."""
        return self.password_validator.validate_password(password)

    def hash_password(self, password: str) -> str:
        """Hash password for storage."""
        return self.password_manager.hash_password(password)

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return self.password_manager.verify_password(password, hashed)


# FastAPI dependency functions
security_bearer = HTTPBearer()


def get_current_user_dependency(auth_manager: AuthManager):
    """Create FastAPI dependency for current user."""

    def get_current_user(
        credentials: HTTPAuthorizationCredentials = security_bearer
    ) -> AuthUser:
        """Get current authenticated user from token."""
        try:
            token = credentials.credentials
            payload = auth_manager.token_manager.verify_token(token)

            if payload.type != TokenType.ACCESS:
                raise AuthError(401, "Invalid token type")

            # Create user from payload
            user = AuthUser(
                id=payload.sub,
                username=payload.username or "",
                email=payload.email or "",
                roles=payload.roles,
                permissions=payload.permissions,
                session_id=payload.session_id,
                adhd_accommodations=payload.adhd_accommodations,
                authkey_id=payload.authkey_id,
                org_id=payload.org_id
            )

            return user

        except Exception as e:
            if isinstance(e, AuthError):
                raise e

            if auth_manager.config.clear_error_messages:
                raise AuthError(
                    401,
                    "Authentication failed",
                    "Please log in to access this resource."
                )
            raise AuthError(401, "Authentication failed")

    return get_current_user


# Convenience functions
def create_auth_manager(config: Optional[AuthConfig] = None) -> AuthManager:
    """Create authentication manager with configuration."""
    return AuthManager(config)


def verify_password_strength(password: str) -> Dict[str, Any]:
    """Quick password validation with default config."""
    validator = PasswordValidator(AuthConfig())
    return validator.validate_password(password)
