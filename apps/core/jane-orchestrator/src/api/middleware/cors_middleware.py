"""CORS middleware preserving MISP's CORS patterns."""

import logging
from typing import List, Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.status import HTTP_200_OK

logger = logging.getLogger(__name__)


class CorsMiddleware(BaseHTTPMiddleware):
    """
    CORS middleware preserving MISP's CORS handling patterns:
    - Configurable allowed origins
    - Proper preflight handling
    - Security-focused defaults
    """

    def __init__(
        self,
        app,
        allow_origins: Optional[List[str]] = None,
        allow_methods: Optional[List[str]] = None,
        allow_headers: Optional[List[str]] = None,
        allow_credentials: bool = True,
        max_age: int = 600
    ):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or [
            "GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"
        ]
        self.allow_headers = allow_headers or [
            "Accept",
            "Accept-Language",
            "Content-Language",
            "Content-Type",
            "Authorization",
            "X-Requested-With",
            "X-CSRF-Token",
            "X-XSRF-Token"
        ]
        self.allow_credentials = allow_credentials
        self.max_age = max_age

    async def dispatch(self, request: Request, call_next):
        """Process request through CORS middleware."""
        origin = request.headers.get("origin")

        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response(status_code=HTTP_200_OK)
            self._add_cors_headers(response, origin)
            return response

        # Process normal request
        response = await call_next(request)

        # Add CORS headers to response
        self._add_cors_headers(response, origin)

        return response

    def _add_cors_headers(self, response: Response, origin: Optional[str]) -> None:
        """Add CORS headers to response."""
        # Check if origin is allowed
        if origin and self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin
        elif "*" in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = "*"

        # Add other CORS headers
        if self.allow_credentials and origin:
            response.headers["Access-Control-Allow-Credentials"] = "true"

        response.headers["Access-Control-Allow-Methods"] = ", ".join(
            self.allow_methods
        )
        response.headers["Access-Control-Allow-Headers"] = ", ".join(
            self.allow_headers
        )
        response.headers["Access-Control-Max-Age"] = str(self.max_age)

    def _is_origin_allowed(self, origin: str) -> bool:
        """Check if origin is in allowed origins list."""
        return origin in self.allow_origins
