"""
Authentication configuration for Jane Orchestrator.

Integrates with the central authentication service using auth-core
and auth-config libraries for unified SSO across the platform.
"""

import os
from typing import Optional

from pydantic import BaseSettings, Field

try:
    from auth_config import AuthConfigLoader, ConfigUtils, createDefaultLoader
    AUTH_CONFIG_AVAILABLE = True
except ImportError:
    AUTH_CONFIG_AVAILABLE = False


class JaneAuthConfig(BaseSettings):
    """
    Authentication configuration for Jane Orchestrator service.

    This configuration integrates with the central auth system while
    maintaining backward compatibility with existing MISP patterns.
    """

    # Central Auth Service Configuration
    central_auth_service_url: str = Field(
        default=os.getenv("CENTRAL_AUTH_SERVICE_URL", "http://localhost:3001"),
        description="URL of the central authentication service"
    )

    # OAuth2 Client Configuration
    oauth2_client_id: str = Field(
        default=os.getenv("OAUTH2_CLIENT_ID", "jane-orchestrator-dev"),
        description="OAuth2 client ID for Jane Orchestrator"
    )

    oauth2_client_secret: str = Field(
        default=os.getenv("OAUTH2_CLIENT_SECRET", "jane-dev-secret-12345"),
        description="OAuth2 client secret"
    )

    oauth2_redirect_uri: str = Field(
        default=os.getenv(
            "OAUTH2_REDIRECT_URI",
            "http://localhost:8000/auth/callback"
        ),
        description="OAuth2 callback URL"
    )

    # JWT Configuration
    jwt_public_key: Optional[str] = Field(
        default=os.getenv("JWT_PUBLIC_KEY"),
        description="JWT public key for token verification"
    )

    jwt_algorithm: str = Field(
        default=os.getenv("JWT_ALGORITHM", "RS256"),
        description="JWT signing algorithm"
    )

    jwt_issuer: str = Field(
        default=os.getenv("JWT_ISSUER", "https://auth.localhost:3000"),
        description="JWT token issuer"
    )

    jwt_audience: str = Field(
        default=os.getenv("JWT_AUDIENCE", "modular-monolith"),
        description="JWT token audience"
    )

    # Session Configuration
    session_redis_url: str = Field(
        default=os.getenv("SESSION_REDIS_URL", "redis://localhost:6379/0"),
        description="Redis URL for session storage"
    )

    session_secret: str = Field(
        default=os.getenv(
            "SESSION_SECRET",
            "change-this-in-production-jane-session-key"
        ),
        description="Session encryption secret"
    )

    session_timeout: int = Field(
        default=int(os.getenv("SESSION_TIMEOUT", "28800")),  # 8 hours
        description="Session timeout in seconds"
    )

    # API Key Configuration (MISP compatibility)
    api_key_header: str = Field(
        default="X-Authkey",
        description="Header name for API key authentication"
    )

    enable_api_key_auth: bool = Field(
        default=os.getenv("ENABLE_API_KEY_AUTH", "true").lower() == "true",
        description="Enable API key authentication for MISP compatibility"
    )

    # Security Configuration
    require_auth: bool = Field(
        default=os.getenv("REQUIRE_AUTH", "true").lower() == "true",
        description="Require authentication for API endpoints"
    )

    cors_origins: list[str] = Field(
        default_factory=lambda: os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:3001"
        ).split(","),
        description="Allowed CORS origins"
    )

    # Development Configuration
    development_mode: bool = Field(
        default=os.getenv("DEVELOPMENT_MODE", "true").lower() == "true",
        description="Enable development mode features"
    )

    # Auth Config File Path
    auth_config_file: Optional[str] = Field(
        default=os.getenv("AUTH_CONFIG_FILE"),
        description="Path to centralized auth configuration file"
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


class AuthConfigManager:
    """
    Manager for loading and managing authentication configuration.

    Integrates with the central auth-config system when available,
    falls back to local configuration for development.
    """

    def __init__(self, config: Optional[JaneAuthConfig] = None):
        self.local_config = config or JaneAuthConfig()
        self.global_auth_config = None

        # Load global auth configuration if available
        if AUTH_CONFIG_AVAILABLE and self.local_config.auth_config_file:
            try:
                self._load_global_config()
            except Exception as e:
                print(f"Warning: Could not load global auth config: {e}")

    def _load_global_config(self):
        """Load global authentication configuration."""
        if not AUTH_CONFIG_AVAILABLE:
            return

        try:
            environment = os.getenv("ENVIRONMENT", "development")
            loader = createDefaultLoader(environment)
            self.global_auth_config = loader.loadConfig()

            print(f"Loaded global auth config for environment: {environment}")
            print(ConfigUtils.formatConfigSummary(self.global_auth_config))

        except Exception as e:
            print(f"Failed to load global auth config: {e}")

    def get_jwt_config(self) -> dict:
        """Get JWT configuration."""
        if self.global_auth_config:
            jwt_config = self.global_auth_config.jwt
            return {
                "algorithm": jwt_config.algorithm,
                "public_key": jwt_config.publicKey,
                "issuer": jwt_config.issuer,
                "audience": jwt_config.audience,
                "clock_tolerance": jwt_config.clockTolerance
            }

        return {
            "algorithm": self.local_config.jwt_algorithm,
            "public_key": self.local_config.jwt_public_key,
            "issuer": self.local_config.jwt_issuer,
            "audience": self.local_config.jwt_audience,
            "clock_tolerance": 30
        }

    def get_oauth2_config(self) -> dict:
        """Get OAuth2 client configuration."""
        # Check if service is configured in global config
        if self.global_auth_config:
            for service in self.global_auth_config.services:
                if service.clientId == self.local_config.oauth2_client_id:
                    return {
                        "client_id": service.clientId,
                        "client_secret": service.clientSecret,
                        "redirect_uris": service.redirectUris,
                        "scopes": service.allowedScopes
                    }

        return {
            "client_id": self.local_config.oauth2_client_id,
            "client_secret": self.local_config.oauth2_client_secret,
            "redirect_uris": [self.local_config.oauth2_redirect_uri],
            "scopes": ["openid", "profile", "email", "jane:read", "jane:write"]
        }

    def get_redis_config(self) -> dict:
        """Get Redis session configuration."""
        if self.global_auth_config:
            redis_config = self.global_auth_config.redis
            # Use first cluster node for simplicity
            cluster_node = redis_config.cluster[0]
            return {
                "url": f"redis://{cluster_node.host}:{cluster_node.port}/0",
                "password": cluster_node.password,
                "key_prefix": redis_config.keyPrefix,
                "ttl": redis_config.ttl.session
            }

        return {
            "url": self.local_config.session_redis_url,
            "password": None,
            "key_prefix": "mm-auth-jane",
            "ttl": self.local_config.session_timeout
        }

    def get_security_config(self) -> dict:
        """Get security configuration."""
        if self.global_auth_config:
            security_config = self.global_auth_config.security
            return {
                "cors_origins": security_config.cors.allowedOrigins,
                "cors_methods": security_config.cors.allowedMethods,
                "cors_headers": security_config.cors.allowedHeaders,
                "password_policy": security_config.passwordPolicy,
                "rate_limiting": security_config.rateLimiting
            }

        return {
            "cors_origins": self.local_config.cors_origins,
            "cors_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "cors_headers": ["Authorization", "Content-Type", "X-Requested-With"],
            "password_policy": {},
            "rate_limiting": {}
        }

    def is_development_mode(self) -> bool:
        """Check if running in development mode."""
        if self.global_auth_config:
            return self.global_auth_config.environment.debug
        return self.local_config.development_mode

    def get_auth_service_url(self) -> str:
        """Get central auth service URL."""
        return self.local_config.central_auth_service_url


# Global auth config manager instance
auth_config_manager = AuthConfigManager()


def get_auth_config() -> AuthConfigManager:
    """Get the global auth configuration manager."""
    return auth_config_manager
