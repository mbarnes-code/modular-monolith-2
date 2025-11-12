"""
Shared middleware components for FastAPI applications.

Provides unified middleware components across all 37 integrated tools with:
- Security, CORS, rate limiting, compression, and access logging
- Executive function accommodations and clear error messages
- Domain-specific performance monitoring
- Standardized error responses and health checks
"""

import asyncio
import gzip
import secrets
import time
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

import redis.asyncio as redis
from fastapi import HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, BaseSettings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN,
                              HTTP_404_NOT_FOUND, HTTP_429_TOO_MANY_REQUESTS,
                              HTTP_500_INTERNAL_SERVER_ERROR)

from ..logging import get_logger


class MiddlewareConfig(BaseSettings):
    """Configuration for HTTP middleware stack."""

    # CORS settings
    cors_allow_origins: List[str] = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    cors_expose_headers: List[str] = []
    cors_max_age: int = 600

    # Security settings
    security_csrf_check: bool = True
    security_force_https: bool = False
    security_disable_browser_cache: bool = True
    security_check_sec_fetch_site: bool = True
    security_csrf_token_limit: int = 100

    # Rate limiting settings
    rate_limit_enabled: bool = True
    rate_limit_requests_per_minute: int = 60
    rate_limit_requests_per_hour: int = 1000
    rate_limit_redis_url: str = "redis://localhost:6379"
    rate_limit_storage_key_prefix: str = "mp_rate_limit"

    # Compression settings
    compression_enabled: bool = True
    compression_minimum_size: int = 1000
    compression_level: int = 6

    # Logging settings
    access_log_enabled: bool = True
    access_log_requests: bool = True
    access_log_responses: bool = True
    access_log_timing: bool = True
    access_log_user_context: bool = True

    # Executive function accommodations
    clear_error_messages: bool = True
    progressive_error_hints: bool = True
    response_time_warnings: bool = True

    class Config:
        env_prefix = "HTTP_"


class ErrorCode(str, Enum):
    """Standard error codes for consistent error handling."""

    # Authentication & Authorization
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INVALID_TOKEN = "INVALID_TOKEN"
    EXPIRED_TOKEN = "EXPIRED_TOKEN"

    # Validation
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_FIELD = "MISSING_FIELD"

    # Resources
    NOT_FOUND = "NOT_FOUND"
    RESOURCE_EXISTS = "RESOURCE_EXISTS"
    RESOURCE_LOCKED = "RESOURCE_LOCKED"

    # Performance
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    REQUEST_TIMEOUT = "REQUEST_TIMEOUT"
    SLOW_RESPONSE = "SLOW_RESPONSE"

    # System
    INTERNAL_ERROR = "INTERNAL_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    DATABASE_ERROR = "DATABASE_ERROR"

    # Executive Function Support
    ATTENTION_REQUIRED = "ATTENTION_REQUIRED"
    CONTEXT_SWITCH_WARNING = "CONTEXT_SWITCH_WARNING"


class ErrorResponse(BaseModel):
    """Standardized error response with executive function support."""

    success: bool = False
    error_code: ErrorCode
    message: str
    user_message: Optional[str] = None

    # Executive function accommodations
    hints: List[str] = []
    suggested_actions: List[str] = []
    context_help: Optional[str] = None

    # Technical details
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.utcnow()
    request_id: Optional[str] = None

    # Domain-specific performance context
    domain: Optional[str] = None
    expected_response_time: Optional[float] = None
    actual_response_time: Optional[float] = None


class HealthResponse(BaseModel):
    """Health check response."""

    healthy: bool
    service: str
    version: str
    timestamp: datetime = datetime.utcnow()
    uptime_seconds: Optional[float] = None
    checks: Dict[str, Any] = {}


class MentalProstheticException(HTTPException):
    """Enhanced HTTP exception with executive function support."""

    def __init__(
        self,
        status_code: int,
        error_code: ErrorCode,
        message: str,
        user_message: Optional[str] = None,
        hints: Optional[List[str]] = None,
        suggested_actions: Optional[List[str]] = None,
        context_help: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        domain: Optional[str] = None
    ):
        self.error_code = error_code
        self.user_message = user_message or message
        self.hints = hints or []
        self.suggested_actions = suggested_actions or []
        self.context_help = context_help
        self.details = details
        self.domain = domain

        super().__init__(status_code, message, headers)


class CorsMiddleware(BaseHTTPMiddleware):
    """CORS middleware with executive function considerations."""

    def __init__(self, app, config: MiddlewareConfig):
        super().__init__(app)
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    async def dispatch(self, request: Request, call_next):
        """Handle CORS with cognitive load reduction."""
        # Handle preflight requests
        if request.method == "OPTIONS":
            response = Response()
            self._add_cors_headers(response, request)
            return response

        # Process request
        response = await call_next(request)
        self._add_cors_headers(response, request)

        return response

    def _add_cors_headers(self, response: Response, request: Request):
        """Add CORS headers to response."""
        origin = request.headers.get("origin")

        if self._is_origin_allowed(origin):
            response.headers["Access-Control-Allow-Origin"] = origin or "*"

        if self.config.cors_allow_credentials:
            response.headers["Access-Control-Allow-Credentials"] = "true"

        response.headers["Access-Control-Allow-Methods"] = ", ".join(
            self.config.cors_allow_methods
        )
        response.headers["Access-Control-Allow-Headers"] = ", ".join(
            self.config.cors_allow_headers
        )

        if self.config.cors_expose_headers:
            response.headers["Access-Control-Expose-Headers"] = ", ".join(
                self.config.cors_expose_headers
            )

        response.headers["Access-Control-Max-Age"] = str(
            self.config.cors_max_age)

    def _is_origin_allowed(self, origin: Optional[str]) -> bool:
        """Check if origin is allowed."""
        if not origin or "*" in self.config.cors_allow_origins:
            return True
        return origin in self.config.cors_allow_origins


class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware with ADHD-friendly error messages."""

    def __init__(self, app, config: MiddlewareConfig):
        super().__init__(app)
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self._csrf_tokens: Set[str] = set()

    async def dispatch(self, request: Request, call_next):
        """Apply security measures with clear feedback."""
        try:
            # Validate request security
            await self._validate_security(request)

            # Process request
            response = await call_next(request)

            # Add security headers
            self._add_security_headers(response)

            return response

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Security middleware error: {e}", exc_info=True)
            raise MentalProstheticException(
                HTTP_403_FORBIDDEN,
                ErrorCode.FORBIDDEN,
                "Security validation failed",
                "Access denied for security reasons.",
                hints=[
                    "Check your request format and try again."] if self.config.clear_error_messages else []
            )

    async def _validate_security(self, request: Request):
        """Validate request security with clear error messages."""
        # CSRF validation for state-changing requests
        if self.config.security_csrf_check and self._needs_csrf_check(request):
            csrf_token = request.headers.get("X-CSRF-Token")
            if not csrf_token or not self._is_valid_csrf_token(csrf_token):
                raise MentalProstheticException(
                    HTTP_403_FORBIDDEN,
                    ErrorCode.FORBIDDEN,
                    "CSRF token validation failed",
                    "Security token missing or invalid.",
                    hints=[
                        "Include X-CSRF-Token header with your request.",
                        "Get a valid token from the /auth/csrf endpoint."
                    ] if self.config.clear_error_messages else []
                )

        # Sec-Fetch-Site validation
        if self.config.security_check_sec_fetch_site:
            sec_fetch_site = request.headers.get("Sec-Fetch-Site")
            if sec_fetch_site and sec_fetch_site not in ["same-origin", "same-site", "none"]:
                raise MentalProstheticException(
                    HTTP_403_FORBIDDEN,
                    ErrorCode.FORBIDDEN,
                    "Cross-origin request not allowed",
                    "Request blocked for security reasons.",
                    context_help="This protects against malicious cross-site requests."
                )

    def _needs_csrf_check(self, request: Request) -> bool:
        """Check if request needs CSRF validation."""
        return request.method in ["POST", "PUT", "PATCH", "DELETE"]

    def _is_valid_csrf_token(self, token: str) -> bool:
        """Validate CSRF token."""
        return token in self._csrf_tokens

    def generate_csrf_token(self) -> str:
        """Generate a new CSRF token."""
        token = secrets.token_urlsafe(32)
        self._csrf_tokens.add(token)

        # Cleanup old tokens
        if len(self._csrf_tokens) > self.config.security_csrf_token_limit:
            # Remove oldest tokens (simplified - in production use proper cleanup)
            excess = len(self._csrf_tokens) - \
                self.config.security_csrf_token_limit
            tokens_to_remove = list(self._csrf_tokens)[:excess]
            for old_token in tokens_to_remove:
                self._csrf_tokens.discard(old_token)

        return token

    def _add_security_headers(self, response: Response):
        """Add security headers to response."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        if self.config.security_force_https:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        if self.config.security_disable_browser_cache:
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with executive function considerations."""

    def __init__(self, app, config: MiddlewareConfig):
        super().__init__(app)
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.redis_client = None

    async def initialize_redis(self):
        """Initialize Redis connection for rate limiting."""
        if not self.config.rate_limit_enabled:
            return

        try:
            self.redis_client = redis.from_url(
                self.config.rate_limit_redis_url)
            await self.redis_client.ping()
        except Exception as e:
            self.logger.warning(
                f"Redis connection failed: {e}. Rate limiting disabled.")
            self.redis_client = None

    async def dispatch(self, request: Request, call_next):
        """Apply rate limiting with user-friendly messages."""
        if not self.config.rate_limit_enabled or not self.redis_client:
            return await call_next(request)

        try:
            # Check rate limit
            user_id = self._get_user_id(request)
            rate_limit_info = await self._check_rate_limit(user_id)

            if rate_limit_info and rate_limit_info["exceeded"]:
                raise MentalProstheticException(
                    HTTP_429_TOO_MANY_REQUESTS,
                    ErrorCode.RATE_LIMIT_EXCEEDED,
                    "Rate limit exceeded",
                    f"Too many requests. Try again in {rate_limit_info['reset_in']} seconds.",
                    hints=[
                        "Take a short break and try again.",
                        "Consider batching your requests to reduce frequency."
                    ] if self.config.clear_error_messages else [],
                    context_help="Rate limiting prevents system overload and ensures fair usage.",
                    headers={
                        "X-RateLimit-Limit": str(rate_limit_info["limit"]),
                        "X-RateLimit-Remaining": str(rate_limit_info["remaining"]),
                        "X-RateLimit-Reset": str(rate_limit_info["reset"]),
                        "Retry-After": str(rate_limit_info["reset_in"])
                    }
                )

            # Process request
            response = await call_next(request)

            # Add rate limit headers
            if rate_limit_info:
                response.headers.update({
                    "X-RateLimit-Limit": str(rate_limit_info["limit"]),
                    "X-RateLimit-Remaining": str(rate_limit_info["remaining"]),
                    "X-RateLimit-Reset": str(rate_limit_info["reset"])
                })

            return response

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(
                f"Rate limit middleware error: {e}", exc_info=True)
            # Don't block on errors - allow request through
            return await call_next(request)

    def _get_user_id(self, request: Request) -> str:
        """Get user identifier for rate limiting."""
        # Try user from auth context
        user = getattr(request.state, "user", None)
        if user and isinstance(user, dict) and "id" in user:
            return f"user:{user['id']}"

        # Fallback to IP address
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"

    async def _check_rate_limit(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Check rate limit for user."""
        try:
            now = time.time()
            minute_key = f"{self.config.rate_limit_storage_key_prefix}:minute:{user_id}"
            hour_key = f"{self.config.rate_limit_storage_key_prefix}:hour:{user_id}"

            # Check minute limit
            minute_count = await self.redis_client.incr(minute_key)
            if minute_count == 1:
                await self.redis_client.expire(minute_key, 60)

            # Check hour limit
            hour_count = await self.redis_client.incr(hour_key)
            if hour_count == 1:
                await self.redis_client.expire(hour_key, 3600)

            # Determine if limit exceeded
            minute_exceeded = minute_count > self.config.rate_limit_requests_per_minute
            hour_exceeded = hour_count > self.config.rate_limit_requests_per_hour

            if minute_exceeded or hour_exceeded:
                # Calculate reset time
                minute_ttl = await self.redis_client.ttl(minute_key)
                hour_ttl = await self.redis_client.ttl(hour_key)
                reset_in = min(minute_ttl, hour_ttl) if minute_ttl > 0 and hour_ttl > 0 else max(
                    minute_ttl, hour_ttl)

                return {
                    "exceeded": True,
                    "limit": self.config.rate_limit_requests_per_minute,
                    "remaining": 0,
                    "reset": int(now + reset_in),
                    "reset_in": reset_in
                }

            # Return current status
            remaining = min(
                self.config.rate_limit_requests_per_minute - minute_count,
                self.config.rate_limit_requests_per_hour - hour_count
            )

            return {
                "exceeded": False,
                "limit": self.config.rate_limit_requests_per_minute,
                "remaining": remaining,
                "reset": int(now + 60),  # Next minute
                "reset_in": 60
            }

        except Exception as e:
            self.logger.error(f"Rate limit check error: {e}")
            return None


class CompressionMiddleware(BaseHTTPMiddleware):
    """Compression middleware for bandwidth optimization."""

    def __init__(self, app, config: MiddlewareConfig):
        super().__init__(app)
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    async def dispatch(self, request: Request, call_next):
        """Apply compression when appropriate."""
        if not self.config.compression_enabled:
            return await call_next(request)

        # Check if client accepts gzip
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" not in accept_encoding:
            return await call_next(request)

        response = await call_next(request)

        # Check if response should be compressed
        if self._should_compress(response):
            # Get response content
            response_content = b""
            async for chunk in response.body_iterator:
                response_content += chunk

            # Compress if large enough
            if len(response_content) >= self.config.compression_minimum_size:
                compressed = gzip.compress(
                    response_content,
                    compresslevel=self.config.compression_level
                )

                # Update response
                response.headers["Content-Encoding"] = "gzip"
                response.headers["Content-Length"] = str(len(compressed))

                # Create new response with compressed content
                return Response(
                    content=compressed,
                    status_code=response.status_code,
                    headers=response.headers,
                    media_type=response.media_type
                )

        return response

    def _should_compress(self, response: Response) -> bool:
        """Check if response should be compressed."""
        # Don't compress already compressed content
        if response.headers.get("Content-Encoding"):
            return False

        # Only compress text-based content types
        content_type = response.headers.get("Content-Type", "")
        compressible_types = [
            "text/", "application/json", "application/javascript",
            "application/xml", "application/rss+xml"
        ]

        return any(content_type.startswith(ct) for ct in compressible_types)


class AccessLogMiddleware(BaseHTTPMiddleware):
    """Access logging middleware with executive function insights."""

    def __init__(self, app, config: MiddlewareConfig):
        super().__init__(app)
        self.config = config
        self.logger = get_logger(self.__class__.__name__)

    async def dispatch(self, request: Request, call_next):
        """Log requests/responses with performance insights."""
        start_time = time.time()
        request_id = secrets.token_urlsafe(8)
        request.state.request_id = request_id

        # Log request
        if self.config.access_log_requests:
            self._log_request(request, request_id)

        try:
            response = await call_next(request)

            # Calculate timing
            processing_time = time.time() - start_time

            # Log response with performance metrics
            if self.config.access_log_responses:
                self._log_response(request, response,
                                   processing_time, request_id)

            # Add performance warnings for executive function support
            if self.config.response_time_warnings:
                self._check_performance_thresholds(request, processing_time)

            # Add request ID to response
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            processing_time = time.time() - start_time
            self._log_error(request, e, processing_time, request_id)
            raise

    def _log_request(self, request: Request, request_id: str):
        """Log incoming request."""
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")

        log_data = {
            "type": "request",
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client_ip": client_ip,
            "user_agent": user_agent
        }

        if self.config.access_log_user_context:
            user = getattr(request.state, "user", None)
            if user:
                log_data["user_id"] = user.get(
                    "id") if isinstance(user, dict) else str(user)

        self.logger.info("Incoming request", extra=log_data)

    def _log_response(
        self,
        request: Request,
        response: Response,
        processing_time: float,
        request_id: str
    ):
        """Log response with performance metrics."""
        client_ip = request.client.host if request.client else "unknown"

        log_data = {
            "type": "response",
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "processing_time_ms": round(processing_time * 1000, 2),
            "client_ip": client_ip
        }

        # Add domain-specific context
        domain = getattr(request.state, "domain", "general")
        log_data["domain"] = domain

        # Performance classification
        if processing_time > 5.0:
            log_level = "warning"
            log_data["performance_issue"] = "very_slow"
        elif processing_time > 2.0:
            log_level = "warning"
            log_data["performance_issue"] = "slow"
        else:
            log_level = "info"

        message = f"Response {response.status_code} in {processing_time:.3f}s"

        if log_level == "warning":
            self.logger.warning(message, extra=log_data)
        else:
            self.logger.info(message, extra=log_data)

    def _log_error(
        self,
        request: Request,
        error: Exception,
        processing_time: float,
        request_id: str
    ):
        """Log error with context."""
        client_ip = request.client.host if request.client else "unknown"

        log_data = {
            "type": "error",
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "processing_time_ms": round(processing_time * 1000, 2),
            "client_ip": client_ip
        }

        self.logger.error(
            f"Request error: {type(error).__name__}: {error}",
            extra=log_data,
            exc_info=True
        )

    def _check_performance_thresholds(self, request: Request, processing_time: float):
        """Check performance against domain-specific thresholds."""
        domain = getattr(request.state, "domain", "general")

        thresholds = {
            "security": 1.0,      # <1s for security tools
            "productivity": 2.0,   # <2s for productivity tools
            "tcg": 3.0,           # <3s for TCG tools
            "infrastructure": 5.0,  # <5s for infrastructure tools
            "general": 2.0         # Default threshold
        }

        threshold = thresholds.get(domain, 2.0)

        if processing_time > threshold:
            self.logger.warning(
                f"Slow response in {domain} domain: {processing_time:.3f}s "
                f"(threshold: {threshold}s)",
                extra={
                    "performance_warning": True,
                    "domain": domain,
                    "actual_time": processing_time,
                    "threshold": threshold,
                    "executive_function_impact": "attention_required"
                }
            )


def create_error_handler(config: MiddlewareConfig):
    """Create standardized error handler with executive function support."""

    def error_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle errors with user-friendly messages."""
        request_id = getattr(request.state, "request_id", None)

        # Handle known exception types
        if isinstance(exc, MentalProstheticException):
            response_data = ErrorResponse(
                error_code=exc.error_code,
                message=exc.detail,
                user_message=exc.user_message,
                hints=exc.hints,
                suggested_actions=exc.suggested_actions,
                context_help=exc.context_help,
                details=exc.details,
                request_id=request_id,
                domain=exc.domain
            )
            return JSONResponse(
                status_code=exc.status_code,
                content=response_data.dict(),
                headers=exc.headers
            )

        elif isinstance(exc, HTTPException):
            # Convert standard HTTP exceptions
            hints = []
            suggested_actions = []

            if config.clear_error_messages:
                if exc.status_code == HTTP_401_UNAUTHORIZED:
                    hints = ["Check your authentication credentials."]
                    suggested_actions = ["Log in again to get a fresh token."]
                elif exc.status_code == HTTP_403_FORBIDDEN:
                    hints = ["You don't have permission for this action."]
                    suggested_actions = [
                        "Contact your administrator if you need access."]
                elif exc.status_code == HTTP_404_NOT_FOUND:
                    hints = ["The requested resource was not found."]
                    suggested_actions = ["Check the URL and try again."]

            response_data = ErrorResponse(
                error_code=ErrorCode.INTERNAL_ERROR,  # Default
                message=exc.detail,
                user_message=exc.detail if config.clear_error_messages else "An error occurred.",
                hints=hints,
                suggested_actions=suggested_actions,
                request_id=request_id
            )
            return JSONResponse(
                status_code=exc.status_code,
                content=response_data.dict(),
                headers=exc.headers
            )

        else:
            # Handle unexpected errors
            logger = get_logger("error_handler")
            logger.error(f"Unhandled exception: {exc}", exc_info=True)

            user_message = (
                "An unexpected error occurred. Please try again."
                if config.clear_error_messages
                else "Internal server error."
            )

            response_data = ErrorResponse(
                error_code=ErrorCode.INTERNAL_ERROR,
                message=str(exc),
                user_message=user_message,
                hints=[
                    "Try refreshing the page or contact support if the problem persists."]
                if config.clear_error_messages else [],
                request_id=request_id
            )
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content=response_data.dict()
            )

    return error_handler


def create_health_endpoint(
    service_name: str,
    version: str,
    health_checks: Optional[Dict[str, Callable]] = None
):
    """Create standardized health check endpoint."""

    async def health_check() -> HealthResponse:
        """Health check endpoint with dependency validation."""
        checks = {}
        overall_healthy = True

        if health_checks:
            for check_name, check_func in health_checks.items():
                try:
                    if asyncio.iscoroutinefunction(check_func):
                        result = await check_func()
                    else:
                        result = check_func()

                    checks[check_name] = {
                        "healthy": True,
                        "details": result if isinstance(result, dict) else {"status": "ok"}
                    }
                except Exception as e:
                    checks[check_name] = {
                        "healthy": False,
                        "error": str(e)
                    }
                    overall_healthy = False

        return HealthResponse(
            healthy=overall_healthy,
            service=service_name,
            version=version,
            checks=checks
        )

    return health_check


# Convenience functions for FastAPI setup
def add_middleware_stack(app, config: Optional[MiddlewareConfig] = None):
    """Add complete middleware stack to FastAPI app."""
    if config is None:
        config = MiddlewareConfig()

    # Order matters - middleware is applied in reverse order

    # 1. Access logging (outermost)
    if config.access_log_enabled:
        app.add_middleware(AccessLogMiddleware, config=config)

    # 2. CORS handling
    app.add_middleware(CorsMiddleware, config=config)

    # 3. Security middleware
    app.add_middleware(SecurityMiddleware, config=config)

    # 4. Compression
    if config.compression_enabled:
        app.add_middleware(CompressionMiddleware, config=config)

    # 5. Rate limiting (innermost)
    if config.rate_limit_enabled:
        rate_limit_middleware = RateLimitMiddleware(app, config)
        app.add_middleware(
            lambda app, call_next: rate_limit_middleware.dispatch)

    return app


def add_standard_exception_handlers(app, config: Optional[MiddlewareConfig] = None):
    """Add standardized exception handlers."""
    if config is None:
        config = MiddlewareConfig()

    error_handler = create_error_handler(config)

    # Add handlers for common exceptions
    app.add_exception_handler(HTTPException, error_handler)
    app.add_exception_handler(MentalProstheticException, error_handler)
    app.add_exception_handler(Exception, error_handler)

    return app


def setup_standard_endpoints(
    app,
    service_name: str,
    version: str,
    health_checks: Optional[Dict[str, Callable]] = None
):
    """Setup standard endpoints (health, ready, etc.)."""

    health_check = create_health_endpoint(service_name, version, health_checks)

    @app.get("/health", response_model=HealthResponse)
    async def health():
        """Health check endpoint."""
        return await health_check()

    @app.get("/ready", response_model=HealthResponse)
    async def ready():
        """Readiness check endpoint."""
        return await health_check()

    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "service": service_name,
            "version": version,
            "status": "running",
            "timestamp": datetime.utcnow().isoformat()
        }

    return app
