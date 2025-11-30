"""
Dispatch Central Auth Provider Plugin

This plugin integrates Dispatch with the central authentication service
by creating a custom AuthenticationProviderPlugin that uses auth-core providers.
"""

import logging
from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException, Request
from starlette.status import HTTP_401_UNAUTHORIZED

# Import auth-core components
try:
    from auth_clients.python import AuthClient
    from auth_core.providers import JWTProvider, SessionProvider
except ImportError:
    # Fallback for development
    AuthClient = None
    JWTProvider = None
    SessionProvider = None

from dispatch.config import (CENTRAL_AUTH_CLIENT_ID,
                             CENTRAL_AUTH_CLIENT_SECRET, CENTRAL_AUTH_ENABLED,
                             CENTRAL_AUTH_SERVICE_URL)
from dispatch.plugins import dispatch_core as dispatch_plugin
from dispatch.plugins.bases import AuthenticationProviderPlugin

log = logging.getLogger(__name__)


class CentralAuthProviderPlugin(AuthenticationProviderPlugin):
    """
    Dispatch authentication provider using the central auth service.

    This plugin integrates Dispatch's authentication system with the
    central authentication service through auth-core providers.
    """

    title = "Dispatch Plugin - Central Authentication Provider"
    slug = "dispatch-auth-provider-central"
    description = "Central authentication service integration for unified SSO"
    version = dispatch_plugin.__version__

    author = "Modular Monolith Team"
    author_url = "https://github.com/modular-monolith/dispatch-central-auth"
    configuration_schema = None

    def __init__(self):
        super().__init__()
        self.auth_client = None
        self.jwt_provider = None
        self.session_provider = None
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize auth providers if central auth is enabled."""
        if not CENTRAL_AUTH_ENABLED or not AuthClient:
            log.warning("Central auth not enabled or auth-core not available")
            return

        try:
            # Initialize auth client for central service communication
            self.auth_client = AuthClient(
                base_url=CENTRAL_AUTH_SERVICE_URL,
                client_id=CENTRAL_AUTH_CLIENT_ID,
                client_secret=CENTRAL_AUTH_CLIENT_SECRET,
            )

            # Initialize JWT provider for token validation
            self.jwt_provider = JWTProvider(
                issuer=CENTRAL_AUTH_SERVICE_URL,
                jwks_url=f"{CENTRAL_AUTH_SERVICE_URL}/oauth2/jwks",
            )

            # Initialize session provider for session management
            self.session_provider = SessionProvider(
                redis_url=self._get_redis_url(),
                prefix="dispatch_session:",
            )

            log.info("Central auth providers initialized successfully")
        except Exception as e:
            log.error("Failed to initialize central auth providers: %s", str(e))
            self.auth_client = None
            self.jwt_provider = None
            self.session_provider = None

    def _get_redis_url(self) -> str:
        """Get Redis URL from configuration."""
        # Use Dispatch's Redis configuration
        from dispatch.config import (REDIS_DB, REDIS_HOST, REDIS_PASSWORD,
                                     REDIS_PORT)

        if REDIS_PASSWORD:
            return f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
        else:
            return f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

    def get_current_user(self, request: Request, **kwargs) -> str:
        """
        Get current user from request using central auth providers.

        Returns user email for compatibility with Dispatch's user system.
        """
        if not CENTRAL_AUTH_ENABLED or not self.auth_client:
            # Fallback to default authentication if central auth not available
            return self._fallback_authentication(request)

        try:
            # Try JWT authentication first
            user_info = self._authenticate_jwt(request)
            if user_info:
                return user_info.get("email")

            # Try session authentication
            user_info = self._authenticate_session(request)
            if user_info:
                return user_info.get("email")

            # Try API key authentication (for service-to-service)
            user_info = self._authenticate_api_key(request)
            if user_info:
                return user_info.get("email")

            # No valid authentication found
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=[{"msg": "Could not validate credentials"}],
            )

        except HTTPException:
            raise
        except Exception as e:
            log.error("Authentication error: %s", str(e))
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail=[{"msg": "Authentication service error"}],
            )

    def _authenticate_jwt(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate using JWT token from Authorization header."""
        if not self.jwt_provider:
            return None

        authorization = request.headers.get("Authorization", "")
        if not authorization.startswith("Bearer "):
            return None

        token = authorization.split(" ", 1)[1]

        try:
            # Validate JWT token using central auth service
            payload = self.jwt_provider.verify_token(token)

            if payload:
                return {
                    "user_id": payload.get("sub"),
                    "email": payload.get("email"),
                    "username": payload.get("preferred_username"),
                    "name": payload.get("name"),
                    "auth_method": "jwt",
                }
        except Exception as e:
            log.debug("JWT authentication failed: %s", str(e))

        return None

    def _authenticate_session(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate using session from cookies."""
        if not self.session_provider:
            return None

        # Get session ID from cookies
        session_id = request.cookies.get("session_id")
        if not session_id:
            return None

        try:
            # Validate session using central auth service
            session_data = self.session_provider.get_session(session_id)

            if session_data and not session_data.get("expired"):
                return {
                    "user_id": session_data.get("user_id"),
                    "email": session_data.get("email"),
                    "username": session_data.get("username"),
                    "session_id": session_id,
                    "auth_method": "session",
                }
        except Exception as e:
            log.debug("Session authentication failed: %s", str(e))

        return None

    def _authenticate_api_key(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate using API key for service-to-service communication."""
        if not self.auth_client:
            return None

        # Check for API key in X-API-Key header
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            return None

        try:
            # Validate API key with central auth service
            response = self.auth_client.post("/auth/validate-api-key", {
                "api_key": api_key
            })

            if response.get("valid"):
                user_data = response.get("user", {})
                return {
                    "user_id": user_data.get("id"),
                    "email": user_data.get("email"),
                    "username": user_data.get("username"),
                    "api_key": api_key,
                    "auth_method": "api_key",
                }
        except Exception as e:
            log.debug("API key authentication failed: %s", str(e))

        return None

    def _fallback_authentication(self, request: Request) -> str:
        """
        Fallback authentication when central auth is not available.

        Uses Dispatch's default authentication method or returns a default user.
        """
        log.warning(
            "Using fallback authentication - central auth not available")

        # Try to use existing basic auth if JWT secret is configured
        from dispatch.config import (DISPATCH_AUTHENTICATION_DEFAULT_USER,
                                     DISPATCH_JWT_SECRET)

        if DISPATCH_JWT_SECRET:
            # Use basic JWT authentication
            authorization = request.headers.get("Authorization", "")
            if authorization.startswith("Bearer "):
                token = authorization.split(" ", 1)[1]
                try:
                    from jose import jwt
                    data = jwt.decode(token, DISPATCH_JWT_SECRET)
                    return data.get("email", DISPATCH_AUTHENTICATION_DEFAULT_USER)
                except Exception as e:
                    log.debug("Fallback JWT authentication failed: %s", str(e))

        # Return default user for development
        return DISPATCH_AUTHENTICATION_DEFAULT_USER

    def health_check(self) -> Dict[str, Any]:
        """Check health of central auth service integration."""
        if not CENTRAL_AUTH_ENABLED:
            return {"status": "disabled", "message": "Central auth not enabled"}

        if not self.auth_client:
            return {"status": "error", "message": "Auth client not initialized"}

        try:
            # Check if central auth service is accessible
            response = self.auth_client.get("/health")
            if response.get("status") == "healthy":
                return {"status": "healthy", "message": "Central auth service accessible"}
            else:
                return {"status": "warning", "message": "Central auth service reports unhealthy"}
        except Exception as e:
            return {"status": "error", "message": f"Cannot reach central auth service: {str(e)}"}


# Register the plugin
def get_auth_provider_plugin():
    """Factory function to create and return the central auth provider plugin."""
    return CentralAuthProviderPlugin()
