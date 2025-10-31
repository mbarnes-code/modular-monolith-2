"""Rate limiting middleware preserving MISP's rate limiting patterns."""

import logging
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

import redis
from fastapi import HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.status import (HTTP_405_METHOD_NOT_ALLOWED,
                              HTTP_429_TOO_MANY_REQUESTS)

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware preserving MISP's rate limiting patterns:
    - Per-user rate limiting
    - Redis-based counters
    - Role-based limits
    - REST API protection
    """

    # Limited functions that require rate limiting (from MISP)
    LIMITED_FUNCTIONS = {
        "attributes": {"restSearch": 1},
        "events": {"restSearch": 1}
    }

    def __init__(
        self,
        app,
        redis_client: Optional[redis.Redis] = None,
        default_window_seconds: int = 900,  # 15 minutes like MISP
        misp_uuid: Optional[str] = None
    ):
        super().__init__(app)
        self.redis_client = redis_client
        self.default_window_seconds = default_window_seconds
        self.misp_uuid = misp_uuid or "default-misp-instance"

    async def dispatch(self, request: Request, call_next):
        """Process request through rate limiting middleware."""
        try:
            # Check if rate limiting applies to this request
            user = getattr(request.state, "user", None)
            if user and self._should_check_rate_limit(request, user):
                rate_limit_result = await self._check_rate_limit(
                    request, user
                )

                if rate_limit_result and rate_limit_result.get("exceeded"):
                    # Add rate limit headers
                    headers = {
                        "X-RateLimit-Limit": str(rate_limit_result["limit"]),
                        "X-RateLimit-Remaining": str(rate_limit_result["remaining"]),
                        "X-RateLimit-Reset": str(rate_limit_result["reset"]),
                        "Retry-After": str(rate_limit_result["reset"])
                    }

                    raise HTTPException(
                        status_code=HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded",
                        headers=headers
                    )

                # Add rate limit info to response headers
                if rate_limit_result:
                    request.state.rate_limit_headers = {
                        "X-RateLimit-Limit": str(rate_limit_result["limit"]),
                        "X-RateLimit-Remaining": str(rate_limit_result["remaining"]),
                        "X-RateLimit-Reset": str(rate_limit_result["reset"])
                    }

            # Process request
            response = await call_next(request)

            # Add rate limit headers to response
            if hasattr(request.state, "rate_limit_headers"):
                for key, value in request.state.rate_limit_headers.items():
                    response.headers[key] = value

            return response

        except HTTPException:
            raise
        except Exception as e:
            logger.error(
                f"Rate limit middleware error: {str(e)}", exc_info=True)
            # Don't block on rate limiting errors - allow request through
            return await call_next(request)

    def _should_check_rate_limit(self, request: Request, user: Dict) -> bool:
        """Check if rate limiting should be applied to this request."""
        # Get controller and action from path
        path_parts = request.url.path.strip("/").split("/")

        if len(path_parts) < 3 or path_parts[0] != "api":
            return False

        controller = path_parts[1]
        action = path_parts[2] if len(path_parts) > 2 else ""

        # Check if this controller/action combination is rate limited
        if controller not in self.LIMITED_FUNCTIONS:
            return False

        if action not in self.LIMITED_FUNCTIONS[controller]:
            return False

        # Check if user role enforces rate limiting
        user_role = user.get("Role", {})
        if not user_role.get("enforce_rate_limit", False):
            return False

        return True

    async def _check_rate_limit(
        self,
        request: Request,
        user: Dict
    ) -> Optional[Dict]:
        """Check rate limit for user and return limit info."""
        if not self.redis_client:
            return None  # Redis not available, allow access

        user_role = user.get("Role", {})
        rate_limit = int(user_role.get("rate_limit_count", 0))

        if rate_limit == 0:
            raise HTTPException(
                status_code=HTTP_405_METHOD_NOT_ALLOWED,
                detail="API searches are not allowed for this user role."
            )

        try:
            # Create Redis key
            key_name = f"misp:{self.misp_uuid}:rate_limit:{user['id']}"

            # Get current count
            current_count = self.redis_client.get(key_name)
            current_count = int(current_count) if current_count else 0

            # Check if limit exceeded
            if current_count >= rate_limit:
                reset_time = self.redis_client.ttl(key_name)
                return {
                    "exceeded": True,
                    "limit": rate_limit,
                    "reset": reset_time,
                    "remaining": 0
                }

            # Increment counter
            new_count = self.redis_client.incr(key_name)

            # Set expiry if this is the first request
            if new_count == 1:
                self.redis_client.expire(key_name, self.default_window_seconds)
                reset_time = self.default_window_seconds
            else:
                reset_time = self.redis_client.ttl(key_name)

            return {
                "exceeded": False,
                "limit": rate_limit,
                "reset": reset_time,
                "remaining": rate_limit - new_count
            }

        except Exception as e:
            logger.error(f"Redis rate limiting error: {str(e)}")
            return None  # Allow request on Redis errors
