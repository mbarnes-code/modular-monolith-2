"""
Startup initialization for Jane Orchestrator authentication.

Sets up auth providers and middleware for integration with the 
central authentication system.
"""

import asyncio
import logging
from typing import Optional

from fastapi import FastAPI

from ..config.auth_config import AuthConfigManager, get_auth_config

logger = logging.getLogger(__name__)


class AuthProviderManager:
    """
    Manages authentication provider initialization and lifecycle.
    """

    def __init__(self, auth_config: AuthConfigManager):
        self.auth_config = auth_config
        self.jwt_provider = None
        self.session_provider = None
        self.auth_client = None

    async def initialize(self):
        """Initialize all auth providers."""
        try:
            await self._initialize_jwt_provider()
            await self._initialize_session_provider()
            await self._initialize_auth_client()

            logger.info("Auth providers initialized successfully")

        except Exception as e:
            logger.error("Failed to initialize auth providers: %s", str(e))
            # Continue with limited functionality

    async def _initialize_jwt_provider(self):
        """Initialize JWT token provider."""
        try:
            # Try to import auth-core JWT provider
            try:
                from libs.auth_core.src.providers.jwt import JWTProvider

                jwt_config = self.auth_config.get_jwt_config()
                self.jwt_provider = JWTProvider(
                    algorithm=jwt_config["algorithm"],
                    public_key=jwt_config.get("public_key"),
                    issuer=jwt_config["issuer"],
                    audience=jwt_config["audience"]
                )

                logger.info("JWT provider initialized with algorithm: %s",
                            jwt_config["algorithm"])

            except ImportError:
                logger.warning("auth-core not available, using fallback JWT")
                self.jwt_provider = FallbackJWTProvider(
                    self.auth_config.get_jwt_config()
                )

        except Exception as e:
            logger.error("Failed to initialize JWT provider: %s", str(e))

    async def _initialize_session_provider(self):
        """Initialize session provider."""
        try:
            # Try to import auth-core session provider
            try:
                from libs.auth_core.src.providers.session import \
                    SessionProvider

                redis_config = self.auth_config.get_redis_config()
                self.session_provider = SessionProvider(
                    redis_url=redis_config["url"],
                    key_prefix=redis_config["key_prefix"],
                    ttl=redis_config["ttl"]
                )

                logger.info("Session provider initialized with Redis")

            except ImportError:
                logger.warning(
                    "auth-core not available, using fallback session")
                self.session_provider = FallbackSessionProvider()

        except Exception as e:
            logger.error("Failed to initialize session provider: %s", str(e))

    async def _initialize_auth_client(self):
        """Initialize OAuth2 auth client."""
        try:
            # Try to import auth-clients
            try:
                from libs.auth_clients.python.auth_client import AuthClient

                oauth2_config = self.auth_config.get_oauth2_config()
                auth_service_url = self.auth_config.get_auth_service_url()

                self.auth_client = AuthClient(
                    client_id=oauth2_config["client_id"],
                    client_secret=oauth2_config["client_secret"],
                    auth_server_url=auth_service_url
                )

                logger.info("Auth client initialized for service: %s",
                            oauth2_config["client_id"])

            except ImportError:
                logger.warning("auth-clients not available, using fallback")
                self.auth_client = FallbackAuthClient(
                    self.auth_config.get_auth_service_url()
                )

        except Exception as e:
            logger.error("Failed to initialize auth client: %s", str(e))


class FallbackJWTProvider:
    """Fallback JWT provider for development."""

    def __init__(self, jwt_config: dict):
        self.config = jwt_config

    async def verify_token(self, token: str) -> Optional[dict]:
        """Basic JWT verification without signature check."""
        try:
            import jwt

            # Decode without verification for development
            payload = jwt.decode(
                token,
                options={"verify_signature": False}
            )
            return payload
        except Exception as e:
            logger.debug("JWT verification failed: %s", str(e))
            return None


class FallbackSessionProvider:
    """Fallback session provider using in-memory storage."""

    def __init__(self):
        self.sessions = {}

    async def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data."""
        return self.sessions.get(session_id)

    async def set_session(self, session_id: str, data: dict) -> None:
        """Set session data."""
        self.sessions[session_id] = data

    async def delete_session(self, session_id: str) -> None:
        """Delete session."""
        self.sessions.pop(session_id, None)


class FallbackAuthClient:
    """Fallback auth client for development."""

    def __init__(self, auth_service_url: str):
        self.auth_service_url = auth_service_url

    async def get_user_info(self, access_token: str) -> Optional[dict]:
        """Get user info from token."""
        # For development, decode token locally
        try:
            import jwt
            payload = jwt.decode(
                access_token,
                options={"verify_signature": False}
            )
            return {
                "id": payload.get("sub"),
                "username": payload.get("username", payload.get("preferred_username")),
                "email": payload.get("email"),
                "name": payload.get("name"),
                "roles": payload.get("roles", [])
            }
        except Exception:
            return None


# Global auth provider manager
auth_provider_manager = None


async def initialize_auth_system(app: FastAPI):
    """
    Initialize the authentication system for Jane Orchestrator.

    This should be called during FastAPI startup.
    """
    global auth_provider_manager

    try:
        auth_config = get_auth_config()
        auth_provider_manager = AuthProviderManager(auth_config)

        await auth_provider_manager.initialize()

        # Store providers in app state for middleware access
        app.state.jwt_provider = auth_provider_manager.jwt_provider
        app.state.session_provider = auth_provider_manager.session_provider
        app.state.auth_client = auth_provider_manager.auth_client

        logger.info("Jane Orchestrator auth system initialized")

    except Exception as e:
        logger.error("Failed to initialize auth system: %s", str(e))
        raise


async def shutdown_auth_system():
    """
    Cleanup authentication system on shutdown.
    """
    global auth_provider_manager

    try:
        if auth_provider_manager:
            # Cleanup providers if they support it
            logger.info("Shutting down auth system")

    except Exception as e:
        logger.error("Error during auth system shutdown: %s", str(e))


def get_auth_providers():
    """Get the current auth providers."""
    return auth_provider_manager if auth_provider_manager else None
