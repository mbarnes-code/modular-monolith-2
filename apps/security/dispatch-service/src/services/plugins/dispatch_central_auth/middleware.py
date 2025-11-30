"""
Dispatch Central Auth Middleware

This middleware integrates the central auth provider plugin
with Dispatch's request processing pipeline.
"""

import logging
from typing import Any, Dict, Optional

from dispatch.auth.models import DispatchUser
from dispatch.auth.service import get_current_user
from dispatch.individual import service as individual_service
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

log = logging.getLogger(__name__)


class CentralAuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware that integrates central authentication with Dispatch.

    This middleware works alongside Dispatch's existing authentication
    system to provide SSO capabilities through the central auth service.
    """

    def __init__(
        self,
        app,
        exempt_paths: Optional[list] = None,
        enable_fallback: bool = True
    ):
        super().__init__(app)
        self.exempt_paths = exempt_paths or [
            "/api/v1/auth/login",
            "/api/v1/auth/logout",
            "/api/v1/auth/callback",
            "/docs",
            "/openapi.json",
            "/health",
            "/static",
        ]
        self.enable_fallback = enable_fallback
        self._auth_plugin = None
        self._initialize_auth_plugin()

    def _initialize_auth_plugin(self):
        """Initialize the central auth provider plugin."""
        try:
            from .plugin import CentralAuthProviderPlugin
            self._auth_plugin = CentralAuthProviderPlugin()
            log.info("Central auth plugin initialized successfully")
        except Exception as e:
            log.error("Failed to initialize central auth plugin: %s", str(e))
            if not self.enable_fallback:
                raise

    async def dispatch(self, request: Request, call_next) -> Response:
        """Process request through central auth middleware."""

        # Skip authentication for exempt paths
        if self._is_exempt_path(request.url.path):
            return await call_next(request)

        # Skip for OPTIONS requests
        if request.method == "OPTIONS":
            return await call_next(request)

        try:
            # Get current user using central auth or fallback
            current_user = await self._authenticate_user(request)

            if current_user:
                # Store user in request state
                request.state.user = current_user
                request.state.current_user = current_user

                # Log successful authentication
                log.debug(
                    "User authenticated: %s via central auth",
                    current_user.email
                )
            else:
                # Authentication failed
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

        except HTTPException:
            raise
        except Exception as e:
            log.error("Authentication middleware error: %s", str(e))
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Authentication service error"
            )

        return await call_next(request)

    def _is_exempt_path(self, path: str) -> bool:
        """Check if path is exempt from authentication."""
        return any(path.startswith(exempt) for exempt in self.exempt_paths)

    async def _authenticate_user(self, request: Request) -> Optional[DispatchUser]:
        """
        Authenticate user using central auth plugin or fallback.

        Returns a DispatchUser object compatible with Dispatch's user system.
        """
        # Try central auth plugin first
        if self._auth_plugin:
            try:
                user_email = self._auth_plugin.get_current_user(request)
                if user_email:
                    return await self._get_or_create_dispatch_user(
                        request, user_email
                    )
            except Exception as e:
                log.warning("Central auth failed, trying fallback: %s", str(e))

        # Fallback to Dispatch's built-in authentication
        if self.enable_fallback:
            try:
                # Use Dispatch's existing auth system
                db_session = request.state.db
                return get_current_user(request=request, db_session=db_session)
            except Exception as e:
                log.debug("Fallback authentication failed: %s", str(e))

        return None

    async def _get_or_create_dispatch_user(
        self,
        request: Request,
        user_email: str
    ) -> DispatchUser:
        """
        Get or create a Dispatch user from the authenticated email.

        This integrates with Dispatch's user management system.
        """
        try:
            # Get database session from request
            db_session = request.state.db

            # Try to find existing user by email
            individual = individual_service.get_by_email(
                db_session=db_session,
                email=user_email
            )

            if individual:
                # Return existing user
                return DispatchUser(
                    id=individual.id,
                    email=individual.email,
                    role=individual.role or "member",
                    projects=getattr(individual, 'projects', []),
                    organizations=getattr(individual, 'organizations', []),
                )
            else:
                # Create new user if not exists
                log.info("Creating new user for %s", user_email)

                individual = individual_service.create(
                    db_session=db_session,
                    email=user_email,
                    name=user_email.split('@')[0],  # Use email prefix as name
                )

                return DispatchUser(
                    id=individual.id,
                    email=individual.email,
                    role="member",  # Default role for new users
                    projects=[],
                    organizations=[],
                )

        except Exception as e:
            log.error("Failed to get/create dispatch user: %s", str(e))
            # Return a minimal user object for compatibility
            return DispatchUser(
                id=None,
                email=user_email,
                role="member",
                projects=[],
                organizations=[],
            )

    def health_check(self) -> Dict[str, Any]:
        """Check health of central auth integration."""
        if not self._auth_plugin:
            return {
                "status": "warning",
                "message": "Central auth plugin not initialized"
            }

        return self._auth_plugin.health_check()


def create_central_auth_middleware(
    exempt_paths: Optional[list] = None,
    enable_fallback: bool = True
) -> type:
    """
    Factory function to create central auth middleware with configuration.

    Args:
        exempt_paths: List of paths to exempt from authentication
        enable_fallback: Whether to enable fallback to built-in auth

    Returns:
        Configured middleware class
    """

    class ConfiguredCentralAuthMiddleware(CentralAuthMiddleware):
        def __init__(self, app):
            super().__init__(
                app,
                exempt_paths=exempt_paths,
                enable_fallback=enable_fallback
            )

    return ConfiguredCentralAuthMiddleware
