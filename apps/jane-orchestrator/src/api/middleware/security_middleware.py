"""Security middleware preserving MISP's security patterns."""

import hashlib
import logging
import re
import secrets
import time
from typing import Dict, Optional, Set

from fastapi import HTTPException, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED

logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Security middleware preserving MISP's security patterns:
    - CSRF protection
    - Security token generation
    - Blackhole protection
    - Sec-Fetch-Site header validation
    - Browser cache control
    - XSS protection headers
    """

    def __init__(
        self,
        app,
        csrf_check: bool = True,
        force_https: bool = False,
        disable_browser_cache: bool = True,
        check_sec_fetch_site: bool = True,
        csrf_token_limit: int = 100,
        unlocked_actions: Optional[Set[str]] = None
    ):
        super().__init__(app)
        self.csrf_check = csrf_check
        self.force_https = force_https
        self.disable_browser_cache = disable_browser_cache
        self.check_sec_fetch_site = check_sec_fetch_site
        self.csrf_token_limit = csrf_token_limit
        self.unlocked_actions = unlocked_actions or set()

    async def dispatch(self, request: Request, call_next):
        """Process request through security middleware."""
        try:
            # Force HTTPS if configured
            if self.force_https:
                request.scope["scheme"] = "https"

            # Validate Sec-Fetch-Site header for state-changing requests
            if self.check_sec_fetch_site:
                await self._validate_sec_fetch_site(request)

            # CSRF protection for non-REST endpoints
            if self.csrf_check and not self._is_rest_request(request):
                await self._validate_csrf_token(request)

            # Process request
            response = await call_next(request)

            # Add security headers
            self._add_security_headers(response)

            return response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Security middleware error: {str(e)}", exc_info=True)
            # Blackhole - log and reject suspicious requests
            await self._blackhole(request, "security_error", e)
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Security validation failed"
            )

    async def _validate_sec_fetch_site(self, request: Request) -> None:
        """Validate Sec-Fetch-Site header for cross-origin requests."""
        sec_fetch_site = request.headers.get("sec-fetch-site")

        if (sec_fetch_site is not None and
            sec_fetch_site != "same-origin" and
                request.method in ["POST", "PUT", "PATCH", "DELETE"]):

            # Check if this is an AJAX request
            is_ajax = (
                request.headers.get("x-requested-with") == "XMLHttpRequest" or
                request.headers.get(
                    "content-type", "").startswith("application/json")
            )

            if is_ajax or request.method in ["POST", "PUT", "PATCH"]:
                raise HTTPException(
                    status_code=HTTP_405_METHOD_NOT_ALLOWED,
                    detail="POST, PUT and AJAX requests are allowed just from same origin."
                )

    async def _validate_csrf_token(self, request: Request) -> None:
        """Validate CSRF token for state-changing requests."""
        if request.method not in ["POST", "PUT", "PATCH", "DELETE"]:
            return

        # Skip CSRF check for unlocked actions
        action = self._get_action_from_request(request)
        if action in self.unlocked_actions:
            return

        # Get token from header or form data
        csrf_token = (
            request.headers.get("x-csrf-token") or
            request.headers.get("x-xsrf-token")
        )

        if not csrf_token:
            # Try to get from form data for non-JSON requests
            if request.headers.get("content-type", "").startswith("application/x-www-form-urlencoded"):
                form_data = await request.form()
                csrf_token = form_data.get("_token")

        if not csrf_token:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="CSRF token missing"
            )

        # Validate token (simplified - in production use proper session-based validation)
        if not self._is_valid_csrf_token(csrf_token):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Invalid CSRF token"
            )

    def _add_security_headers(self, response: Response) -> None:
        """Add security headers to response."""
        # XSS Protection
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy (basic - should be configured per environment)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self' data:; "
            "connect-src 'self';"
        )

        # Disable browser cache if configured
        if self.disable_browser_cache:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"

        # Frame options
        response.headers["X-Frame-Options"] = "SAMEORIGIN"

        # Content type options
        response.headers["X-Content-Type-Options"] = "nosniff"

    def _is_rest_request(self, request: Request) -> bool:
        """Check if request is a REST API request."""
        return (
            request.url.path.startswith("/api/") or
            request.headers.get("accept", "").startswith("application/json") or
            request.headers.get(
                "content-type", "").startswith("application/json")
        )

    def _get_action_from_request(self, request: Request) -> str:
        """Extract action name from request path."""
        path_parts = request.url.path.strip("/").split("/")
        return path_parts[-1] if path_parts else ""

    def _is_valid_csrf_token(self, token: str) -> bool:
        """Validate CSRF token format and structure."""
        # Simplified validation - in production, validate against session
        if not token or len(token) < 32:
            return False

        # Check if token contains only valid characters
        if not re.match(r'^[a-zA-Z0-9]+$', token):
            return False

        return True

    async def _blackhole(self, request: Request, error_type: str, exception: Exception) -> None:
        """Log security violations (blackhole pattern from MISP)."""
        user_agent = request.headers.get("user-agent", "unknown")
        client_ip = request.client.host if request.client else "unknown"

        logger.warning(
            f"Security blackhole triggered: {error_type} "
            f"at {request.url.path} "
            f"from {client_ip} ({user_agent}): {str(exception)}"
        )

        # In production, could implement rate limiting or IP blocking here

    def generate_csrf_token(self) -> str:
        """Generate a new CSRF token."""
        return secrets.token_hex(32)
