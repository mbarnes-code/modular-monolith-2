"""
Enhanced Authentication Configuration

Settings for JWT-based authentication integrated with MISP patterns.
"""

import os
from typing import Optional

from pydantic import BaseSettings


class AuthSettings(BaseSettings):
    """Authentication configuration settings"""

    # JWT Settings
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "your-secret-key-change-in-production"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    REMEMBER_ME_EXPIRE_DAYS: int = 30

    # Cookie Settings
    SECURE_COOKIES: bool = os.getenv(
        "SECURE_COOKIES", "false").lower() == "true"

    # API Key Settings
    API_KEY_HEADER: str = "X-Authkey"
    API_KEY_LENGTH: int = 40

    # Rate Limiting
    LOGIN_RATE_LIMIT: str = "5/minute"
    API_RATE_LIMIT: str = "100/minute"

    # Security
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_SPECIAL: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_UPPERCASE: bool = True

    # Session Management
    MAX_CONCURRENT_SESSIONS: int = 5
    SESSION_TIMEOUT_MINUTES: int = 480  # 8 hours

    # Organization Access
    ALLOW_CROSS_ORG_ACCESS: bool = False
    SHARING_GROUP_AUTO_ACCEPT: bool = False

    # Audit Settings
    LOG_AUTH_ATTEMPTS: bool = True
    LOG_API_ACCESS: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


def get_auth_settings() -> AuthSettings:
    """Get authentication settings instance"""
    return AuthSettings()
