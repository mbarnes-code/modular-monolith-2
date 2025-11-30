"""
Central Authentication Configuration for Dispatch

This module adds configuration options for integrating Dispatch
with the central authentication service.
"""

from dispatch.config import config

# Central Authentication Service Configuration
CENTRAL_AUTH_ENABLED = config("CENTRAL_AUTH_ENABLED", cast=bool, default=False)
CENTRAL_AUTH_SERVICE_URL = config(
    "CENTRAL_AUTH_SERVICE_URL",
    default="http://localhost:3001"
)
CENTRAL_AUTH_CLIENT_ID = config(
    "CENTRAL_AUTH_CLIENT_ID",
    default="dispatch-service"
)
CENTRAL_AUTH_CLIENT_SECRET = config("CENTRAL_AUTH_CLIENT_SECRET", default=None)

# OAuth2/OIDC Configuration for central auth
CENTRAL_AUTH_SCOPES = config(
    "CENTRAL_AUTH_SCOPES",
    default="openid profile email",
    cast=lambda x: x.split()
)

# Redis Configuration (inherited from Dispatch but exposed for auth providers)
REDIS_HOST = config("REDIS_HOST", default="localhost")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
REDIS_DB = config("REDIS_DB", cast=int, default=0)

# Auth Provider Configuration
CENTRAL_AUTH_PROVIDER_SLUG = "dispatch-auth-provider-central"

# Session Configuration
CENTRAL_AUTH_SESSION_TIMEOUT = config(
    "CENTRAL_AUTH_SESSION_TIMEOUT",
    cast=int,
    default=86400  # 24 hours in seconds
)

# JWT Configuration for central auth
CENTRAL_AUTH_JWT_AUDIENCE = config(
    "CENTRAL_AUTH_JWT_AUDIENCE", default="dispatch-service")

# API Key Configuration for service-to-service auth
CENTRAL_AUTH_SERVICE_API_KEY = config(
    "CENTRAL_AUTH_SERVICE_API_KEY", default=None)

# Health check configuration
CENTRAL_AUTH_HEALTH_CHECK_INTERVAL = config(
    "CENTRAL_AUTH_HEALTH_CHECK_INTERVAL",
    cast=int,
    default=300  # 5 minutes
)

# Fallback configuration
CENTRAL_AUTH_FALLBACK_ENABLED = config(
    "CENTRAL_AUTH_FALLBACK_ENABLED",
    cast=bool,
    default=True
)

# Export configuration values for use in plugins
__all__ = [
    "CENTRAL_AUTH_ENABLED",
    "CENTRAL_AUTH_SERVICE_URL",
    "CENTRAL_AUTH_CLIENT_ID",
    "CENTRAL_AUTH_CLIENT_SECRET",
    "CENTRAL_AUTH_SCOPES",
    "CENTRAL_AUTH_PROVIDER_SLUG",
    "CENTRAL_AUTH_SESSION_TIMEOUT",
    "CENTRAL_AUTH_JWT_AUDIENCE",
    "CENTRAL_AUTH_SERVICE_API_KEY",
    "CENTRAL_AUTH_HEALTH_CHECK_INTERVAL",
    "CENTRAL_AUTH_FALLBACK_ENABLED",
    "REDIS_HOST",
    "REDIS_PORT",
    "REDIS_PASSWORD",
    "REDIS_DB",
]
