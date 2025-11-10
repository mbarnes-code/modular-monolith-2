"""Access logging middleware preserving MISP's logging patterns."""

import logging
import time
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class AccessLogMiddleware(BaseHTTPMiddleware):
    """
    Access logging middleware preserving MISP's access logging patterns:
    - Request/response logging
    - Performance timing
    - User context logging
    - Error tracking
    """

    def __init__(
        self,
        app,
        log_requests: bool = True,
        log_responses: bool = True,
        log_timing: bool = True,
        log_user_context: bool = True
    ):
        super().__init__(app)
        self.log_requests = log_requests
        self.log_responses = log_responses
        self.log_timing = log_timing
        self.log_user_context = log_user_context

    async def dispatch(self, request: Request, call_next):
        """Process request through access logging middleware."""
        start_time = time.time()

        # Log incoming request
        if self.log_requests:
            self._log_request(request)

        try:
            # Process request
            response = await call_next(request)

            # Calculate processing time
            processing_time = time.time() - start_time

            # Log response
            if self.log_responses:
                self._log_response(request, response, processing_time)

            return response

        except Exception as e:
            # Log error
            processing_time = time.time() - start_time
            self._log_error(request, e, processing_time)
            raise

    def _log_request(self, request: Request) -> None:
        """Log incoming request details."""
        try:
            client_ip = request.client.host if request.client else "unknown"
            user_agent = request.headers.get("user-agent", "unknown")

            # Get user context if available
            user_info = ""
            if (self.log_user_context and
                hasattr(request.state, "user") and
                    request.state.user):
                user = request.state.user
                user_email = user.get("email", "unknown")
                auth_method = "API" if user.get(
                    "logged_by_authkey") else "session"
                user_info = f" [User: {user_email} via {auth_method}]"

            logger.info(
                f"Request: {request.method} {request.url.path} "
                f"from {client_ip}{user_info} - {user_agent[:100]}"
            )

        except Exception as e:
            logger.error(f"Request logging error: {str(e)}")

    def _log_response(
        self,
        request: Request,
        response,
        processing_time: float
    ) -> None:
        """Log response details."""
        try:
            client_ip = request.client.host if request.client else "unknown"

            # Format processing time
            time_info = ""
            if self.log_timing:
                time_info = f" [{processing_time:.3f}s]"

            logger.info(
                f"Response: {response.status_code} "
                f"for {request.method} {request.url.path} "
                f"from {client_ip}{time_info}"
            )

        except Exception as e:
            logger.error(f"Response logging error: {str(e)}")

    def _log_error(
        self,
        request: Request,
        error: Exception,
        processing_time: float
    ) -> None:
        """Log error details."""
        try:
            client_ip = request.client.host if request.client else "unknown"

            # Format processing time
            time_info = ""
            if self.log_timing:
                time_info = f" [{processing_time:.3f}s]"

            logger.error(
                f"Error: {type(error).__name__}: {str(error)} "
                f"for {request.method} {request.url.path} "
                f"from {client_ip}{time_info}",
                exc_info=True
            )

        except Exception as e:
            logger.error(f"Error logging error: {str(e)}")
