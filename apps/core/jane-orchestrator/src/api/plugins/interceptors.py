"""API interceptors preserving MISP's request/response processing patterns."""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Awaitable, Callable, Dict, List, Optional

from fastapi import Request, Response

logger = logging.getLogger(__name__)


class InterceptorType(Enum):
    """Types of interceptors."""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"


@dataclass
class InterceptorContext:
    """Context passed to interceptors."""
    request: Request
    response: Optional[Response] = None
    error: Optional[Exception] = None
    user: Optional[Dict[str, Any]] = None
    start_time: Optional[float] = None
    data: Optional[Dict[str, Any]] = None


class BaseInterceptor(ABC):
    """Base class for all API interceptors."""

    def __init__(self, priority: int = 100):
        self.priority = priority
        self.logger = logging.getLogger(
            f"interceptor.{self.__class__.__name__}")

    @abstractmethod
    def get_name(self) -> str:
        """Return interceptor name."""
        pass

    @abstractmethod
    def get_type(self) -> InterceptorType:
        """Return interceptor type."""
        pass

    def should_intercept(self, context: InterceptorContext) -> bool:
        """Check if this interceptor should process the request."""
        return True

    @abstractmethod
    async def intercept(self, context: InterceptorContext) -> InterceptorContext:
        """Process the request/response."""
        pass


class RequestInterceptor(BaseInterceptor):
    """Base class for request interceptors."""

    def get_type(self) -> InterceptorType:
        return InterceptorType.REQUEST

    @abstractmethod
    async def process_request(self, context: InterceptorContext) -> InterceptorContext:
        """Process incoming request."""
        pass

    async def intercept(self, context: InterceptorContext) -> InterceptorContext:
        return await self.process_request(context)


class ResponseInterceptor(BaseInterceptor):
    """Base class for response interceptors."""

    def get_type(self) -> InterceptorType:
        return InterceptorType.RESPONSE

    @abstractmethod
    async def process_response(self, context: InterceptorContext) -> InterceptorContext:
        """Process outgoing response."""
        pass

    async def intercept(self, context: InterceptorContext) -> InterceptorContext:
        return await self.process_response(context)


class ErrorInterceptor(BaseInterceptor):
    """Base class for error interceptors."""

    def get_type(self) -> InterceptorType:
        return InterceptorType.ERROR

    @abstractmethod
    async def process_error(self, context: InterceptorContext) -> InterceptorContext:
        """Process error."""
        pass

    async def intercept(self, context: InterceptorContext) -> InterceptorContext:
        return await self.process_error(context)


class RequestValidationInterceptor(RequestInterceptor):
    """Interceptor for request validation."""

    def get_name(self) -> str:
        return "request_validation"

    async def process_request(self, context: InterceptorContext) -> InterceptorContext:
        """Validate incoming request."""
        request = context.request

        # Validate content type for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if not content_type:
                self.logger.warning("Missing content-type header")
            elif not content_type.startswith(("application/json", "application/x-www-form-urlencoded", "multipart/form-data")):
                self.logger.warning(f"Unusual content-type: {content_type}")

        # Validate user agent
        user_agent = request.headers.get("user-agent")
        if not user_agent:
            self.logger.warning("Missing user-agent header")

        return context


class ResponseEnrichmentInterceptor(ResponseInterceptor):
    """Interceptor for response enrichment."""

    def get_name(self) -> str:
        return "response_enrichment"

    async def process_response(self, context: InterceptorContext) -> InterceptorContext:
        """Enrich outgoing response."""
        if context.response:
            # Add custom headers
            context.response.headers["X-Powered-By"] = "MISP-FastAPI"
            context.response.headers["X-Content-Type-Options"] = "nosniff"

            # Add timing information if available
            if context.start_time:
                import time
                processing_time = time.time() - context.start_time
                context.response.headers["X-Processing-Time"] = f"{processing_time:.3f}s"

        return context


class ErrorLoggingInterceptor(ErrorInterceptor):
    """Interceptor for error logging."""

    def get_name(self) -> str:
        return "error_logging"

    async def process_error(self, context: InterceptorContext) -> InterceptorContext:
        """Log error details."""
        if context.error:
            client_ip = context.request.client.host if context.request.client else "unknown"
            user_email = context.user.get(
                "email", "anonymous") if context.user else "anonymous"

            self.logger.error(
                f"API Error: {type(context.error).__name__}: {str(context.error)} "
                f"for {context.request.method} {context.request.url.path} "
                f"by {user_email} from {client_ip}",
                exc_info=True
            )

        return context


class InterceptorChain:
    """
    Interceptor chain preserving MISP's request/response processing patterns:
    - Request preprocessing
    - Response postprocessing
    - Error handling
    - Plugin integration
    """

    def __init__(self):
        self._interceptors: Dict[InterceptorType, List[BaseInterceptor]] = {
            InterceptorType.REQUEST: [],
            InterceptorType.RESPONSE: [],
            InterceptorType.ERROR: []
        }

    def register_interceptor(self, interceptor: BaseInterceptor) -> None:
        """Register an interceptor."""
        interceptor_type = interceptor.get_type()
        if interceptor_type not in self._interceptors:
            self._interceptors[interceptor_type] = []

        self._interceptors[interceptor_type].append(interceptor)

        # Sort by priority (lower number = higher priority)
        self._interceptors[interceptor_type].sort(key=lambda x: x.priority)

        logger.info(
            f"Registered {interceptor_type.value} interceptor: {interceptor.get_name()}")

    def unregister_interceptor(self, interceptor_name: str, interceptor_type: InterceptorType) -> bool:
        """Unregister an interceptor."""
        interceptors = self._interceptors.get(interceptor_type, [])
        for i, interceptor in enumerate(interceptors):
            if interceptor.get_name() == interceptor_name:
                del interceptors[i]
                logger.info(
                    f"Unregistered {interceptor_type.value} interceptor: {interceptor_name}")
                return True
        return False

    async def process_request(self, context: InterceptorContext) -> InterceptorContext:
        """Process request through interceptor chain."""
        for interceptor in self._interceptors[InterceptorType.REQUEST]:
            if interceptor.should_intercept(context):
                try:
                    context = await interceptor.intercept(context)
                except Exception as e:
                    logger.error(
                        f"Error in request interceptor {interceptor.get_name()}: {str(e)}",
                        exc_info=True
                    )
        return context

    async def process_response(self, context: InterceptorContext) -> InterceptorContext:
        """Process response through interceptor chain."""
        for interceptor in self._interceptors[InterceptorType.RESPONSE]:
            if interceptor.should_intercept(context):
                try:
                    context = await interceptor.intercept(context)
                except Exception as e:
                    logger.error(
                        f"Error in response interceptor {interceptor.get_name()}: {str(e)}",
                        exc_info=True
                    )
        return context

    async def process_error(self, context: InterceptorContext) -> InterceptorContext:
        """Process error through interceptor chain."""
        for interceptor in self._interceptors[InterceptorType.ERROR]:
            if interceptor.should_intercept(context):
                try:
                    context = await interceptor.intercept(context)
                except Exception as e:
                    logger.error(
                        f"Error in error interceptor {interceptor.get_name()}: {str(e)}",
                        exc_info=True
                    )
        return context

    def list_interceptors(self, interceptor_type: Optional[InterceptorType] = None) -> Dict[InterceptorType, List[str]]:
        """List all registered interceptors."""
        result = {}

        types_to_list = [interceptor_type] if interceptor_type else list(
            InterceptorType)

        for itype in types_to_list:
            result[itype] = [
                interceptor.get_name()
                for interceptor in self._interceptors.get(itype, [])
            ]

        return result


# Global interceptor chain instance
interceptor_chain = InterceptorChain()

# Register default interceptors
interceptor_chain.register_interceptor(
    RequestValidationInterceptor(priority=10))
interceptor_chain.register_interceptor(
    ResponseEnrichmentInterceptor(priority=90))
interceptor_chain.register_interceptor(ErrorLoggingInterceptor(priority=10))
