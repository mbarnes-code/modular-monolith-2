"""Authentication middleware preserving MISP's auth patterns."""

import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware preserving MISP's authentication patterns:
    - API key authentication
    - Session-based authentication
    - Custom authentication plugins
    - User context management
    """

    def __init__(
        self,
        app,
        auth_service=None,
        exempt_paths: Optional[list[str]] = None
    ):
        super().__init__(app)
        self.auth_service = auth_service
        self.exempt_paths = exempt_paths or [
            "/api/health",
            "/api/heartbeat",
            "/docs",
            "/openapi.json",
            "/favicon.ico"
        ]

    async def dispatch(self, request: Request, call_next):
        """Process request through authentication middleware."""
        try:
            # Skip authentication for exempt paths
            if self._is_exempt_path(request.url.path):
                return await call_next(request)

            # Skip authentication for OPTIONS requests
            if request.method == "OPTIONS":
                return await call_next(request)

            # Authenticate user
            user = await self._authenticate_request(request)

            if user:
                # Store authenticated user in request state
                request.state.user = user
                request.state.is_authenticated = True

                # Log access if configured
                await self._log_access(request, user)

            else:
                # Check if authentication is required for this endpoint
                if self._requires_authentication(request):
                    raise HTTPException(
                        status_code=HTTP_401_UNAUTHORIZED,
                        detail="Authentication required"
                    )

            # Process request
            response = await call_next(request)

            # Add user info to response headers if configured
            if user and hasattr(self.auth_service, 'add_user_headers'):
                self.auth_service.add_user_headers(response, user)

            return response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Auth middleware error: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Authentication error"
            )

    async def _authenticate_request(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate request using various methods."""
        if not self.auth_service:
            return None

        # Try API key authentication first (for REST API)
        if self._is_rest_request(request):
            user = await self._authenticate_api_key(request)
            if user:
                user["logged_by_authkey"] = True
                return user

        # Try session-based authentication
        user = await self._authenticate_session(request)
        if user:
            user["logged_by_authkey"] = False
            return user

        # Try custom authentication plugins
        user = await self._authenticate_custom(request)
        if user:
            return user

        return None

    async def _authenticate_api_key(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate using API key from Authorization header."""
        auth_header = request.headers.get("authorization")
        if not auth_header:
            return None

        # Extract API key from header
        api_key = None
        if auth_header.startswith("Bearer "):
            api_key = auth_header[7:]
        elif auth_header.startswith("ApiKey "):
            api_key = auth_header[7:]
        else:
            # Direct API key in header
            api_key = auth_header

        if not api_key:
            return None

        # Validate API key using auth service
        try:
            user = await self.auth_service.authenticate_api_key(api_key)
            if user:
                # Add authkey ID for logging
                user["authkey_id"] = api_key[:8] + "..."
            return user
        except Exception as e:
            logger.error(f"API key authentication error: {str(e)}")
            return None

    async def _authenticate_session(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate using session data."""
        try:
            session_data = request.session if hasattr(
                request, 'session') else {}
            if not session_data:
                return None

            user_id = session_data.get("user_id")
            if not user_id:
                return None

            # Get user from auth service
            user = await self.auth_service.get_user_by_id(user_id)
            return user

        except Exception as e:
            logger.error(f"Session authentication error: {str(e)}")
            return None

    async def _authenticate_custom(self, request: Request) -> Optional[Dict[str, Any]]:
        """Authenticate using custom authentication plugins."""
        try:
            if hasattr(self.auth_service, 'custom_authenticate'):
                return await self.auth_service.custom_authenticate(request)
            return None
        except Exception as e:
            logger.error(f"Custom authentication error: {str(e)}")
            return None

    def _is_exempt_path(self, path: str) -> bool:
        """Check if path is exempt from authentication."""
        return any(path.startswith(exempt) for exempt in self.exempt_paths)

    def _is_rest_request(self, request: Request) -> bool:
        """Check if request is a REST API request."""
        return (
            request.url.path.startswith("/api/") or
            request.headers.get("accept", "").startswith("application/json") or
            request.headers.get(
                "content-type", "").startswith("application/json")
        )

    def _requires_authentication(self, request: Request) -> bool:
        """Check if endpoint requires authentication."""
        # By default, all non-exempt paths require authentication
        # This can be overridden by specific endpoint configurations
        return not self._is_exempt_path(request.url.path)

    async def _log_access(self, request: Request, user: Dict[str, Any]) -> None:
        """Log user access for audit purposes."""
        try:
            client_ip = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("user-agent", "unknown")

            logger.info(
                f"User access: {user.get('email', 'unknown')} "
                f"from {client_ip} to {request.url.path} "
                f"({request.method}) - {user_agent}"
            )

            # If auth service has logging method, use it
            if hasattr(self.auth_service, 'log_access'):
                await self.auth_service.log_access(request, user)

        except Exception as e:
            logger.error(f"Access logging error: {str(e)}")
