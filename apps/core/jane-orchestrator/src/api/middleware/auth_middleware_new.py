"""Authentication middleware using unified auth-core system."""

import logging
from typing import Any, Dict, Optional

from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

# Import auth-core middleware
try:
    from auth_core.middleware.fastapi import AuthCoreMiddleware
    from auth_core.providers import JWTProvider, SessionProvider
    from auth_clients.python import AuthClient
except ImportError:
    # Fallback for development/testing
    AuthCoreMiddleware = None
    JWTProvider = None
    SessionProvider = None
    AuthClient = None

logger = logging.getLogger(__name__)


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication middleware using unified auth-core system.

    Provides backward compatibility with MISP patterns while using
    the centralized authentication infrastructure.
    """

    def __init__(
        self,
        app,
        auth_client: Optional[AuthClient] = None,
        jwt_provider: Optional[JWTProvider] = None,
        session_provider: Optional[SessionProvider] = None,
        exempt_paths: Optional[list[str]] = None
    ):
        super().__init__(app)
        self.auth_client = auth_client
        self.jwt_provider = jwt_provider
        self.session_provider = session_provider
        self.exempt_paths = exempt_paths or [
            "/api/health",
            "/api/heartbeat",
            "/docs",
            "/openapi.json",
            "/favicon.ico",
            "/auth/callback"
        ]

        # Initialize auth-core middleware if available
        self.auth_core_middleware = None
        if AuthCoreMiddleware and self.jwt_provider:
            self.auth_core_middleware = AuthCoreMiddleware(
                jwt_provider=self.jwt_provider,
                session_provider=self.session_provider,
                exempt_paths=self.exempt_paths
            )

    async def dispatch(self, request: Request, call_next):
        """Process request through authentication middleware."""
        try:
            # Use auth-core middleware if available
            if self.auth_core_middleware:
                return await self.auth_core_middleware.dispatch(
                    request, call_next
                )

            # Fallback to legacy authentication
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

            return response

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Auth middleware error: %s", str(e), exc_info=True)
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Authentication error"
            ) from e

    async def _authenticate_request(
        self, request: Request
    ) -> Optional[Dict[str, Any]]:
        """Authenticate request using various methods."""
        # Try JWT token authentication first
        if self.jwt_provider:
            user = await self._authenticate_jwt(request)
            if user:
                user["auth_method"] = "jwt"
                return user

        # Try session-based authentication
        if self.session_provider:
            user = await self._authenticate_session(request)
            if user:
                user["auth_method"] = "session"
                return user

        # Try API key authentication (legacy MISP compatibility)
        user = await self._authenticate_api_key(request)
        if user:
            user["auth_method"] = "api_key"
            return user

        # Try OAuth2 client authentication
        if self.auth_client:
            user = await self._authenticate_oauth2(request)
            if user:
                user["auth_method"] = "oauth2"
                return user

        return None

    async def _authenticate_jwt(
        self, request: Request
    ) -> Optional[Dict[str, Any]]:
        """Authenticate using JWT token from Authorization header."""
        if not self.jwt_provider:
            return None

        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header[7:]  # Remove "Bearer " prefix

        try:
            payload = await self.jwt_provider.verify_token(token)
            if payload:
                return {
                    "user_id": payload.get("sub"),
                    "username": payload.get(
                        "username", payload.get("preferred_username")
                    ),
                    "email": payload.get("email"),
                    "scopes": payload.get("scopes", []),
                    "token_payload": payload
                }
        except Exception as e:
            logger.debug("JWT authentication failed: %s", str(e))

        return None

    async def _authenticate_oauth2(
        self, request: Request
    ) -> Optional[Dict[str, Any]]:
        """Authenticate using OAuth2 client."""
        if not self.auth_client:
            return None

        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header[7:]  # Remove "Bearer " prefix

        try:
            user_info = await self.auth_client.get_user_info(token)
            if user_info:
                return {
                    "user_id": user_info.get("id"),
                    "username": user_info.get("username"),
                    "email": user_info.get("email"),
                    "name": user_info.get("name"),
                    "roles": user_info.get("roles", []),
                    "user_info": user_info
                }
        except Exception as e:
            logger.debug("OAuth2 authentication failed: %s", str(e))

        return None

    async def _authenticate_api_key(
        self, request: Request
    ) -> Optional[Dict[str, Any]]:
        """Authenticate using API key (MISP compatibility)."""
        # Check X-Authkey header (MISP standard)
        api_key = request.headers.get("x-authkey")

        # Fallback to Authorization header for backward compatibility
        if not api_key:
            auth_header = request.headers.get("authorization")
            if auth_header:
                if auth_header.startswith("ApiKey "):
                    api_key = auth_header[7:]
                elif not auth_header.startswith("Bearer "):
                    # Direct API key in header
                    api_key = auth_header

        if not api_key:
            return None

        # TODO: Validate API key using central auth service
        # For now, provide basic validation for development
        try:
            # This would be replaced with actual API key validation
            # against the central auth service
            if len(api_key) >= 40:  # Basic length check
                return {
                    "user_id": f"api-user-{api_key[:8]}",
                    "username": f"api-user-{api_key[:8]}",
                    "email": f"api-user-{api_key[:8]}@misp.local",
                    "authkey_id": api_key[:8] + "...",
                    "api_key": True
                }
        except Exception as e:
            logger.error("API key authentication error: %s", str(e))

        return None

    async def _authenticate_session(
        self, request: Request
    ) -> Optional[Dict[str, Any]]:
        """Authenticate using session data."""
        if not self.session_provider:
            return None

        # Get session ID from cookie or header
        session_id = request.cookies.get("session_id")
        if not session_id:
            session_id = request.headers.get("x-session-id")

        if not session_id:
            return None

        # Validate session using session provider
        try:
            session_data = await self.session_provider.get_session(session_id)
            if session_data and not session_data.get("expired"):
                return {
                    "user_id": session_data.get("user_id"),
                    "username": session_data.get("username"),
                    "email": session_data.get("email"),
                    "session_id": session_id,
                    "session_data": session_data
                }
        except Exception as e:
            logger.error("Session authentication error: %s", str(e))

        return None

    def _is_exempt_path(self, path: str) -> bool:
        """Check if path is exempt from authentication."""
        return any(path.startswith(exempt) for exempt in self.exempt_paths)

    def _requires_authentication(self, request: Request) -> bool:
        """Check if endpoint requires authentication."""
        # Most endpoints require authentication by default
        return not self._is_exempt_path(request.url.path)

    def _is_rest_request(self, request: Request) -> bool:
        """Check if request is a REST API request."""
        return (
            request.url.path.startswith("/api/") or
            request.headers.get("x-authkey") is not None
        )

    async def _log_access(
        self, request: Request, user: Dict[str, Any]
    ) -> None:
        """Log user access for audit purposes."""
        try:
            # Extract relevant information
            client_ip = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("user-agent", "unknown")
            auth_method = user.get("auth_method", "unknown")

            # Log basic access information
            logger.info(
                "User access: %s from %s to %s (%s) via %s - %s",
                user.get('email', user.get('username', 'unknown')),
                client_ip,
                request.url.path,
                request.method,
                auth_method,
                user_agent
            )

            # TODO: Send audit logs to central auth service
        except Exception as e:
            logger.error("Access logging error: %s", str(e))
