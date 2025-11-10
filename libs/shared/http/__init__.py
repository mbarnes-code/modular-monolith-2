"""
Shared HTTP client library for Mental Prosthetic Platform.

Provides unified HTTP clients for all 37 integrated tools with:
- Automatic retry logic with exponential backoff
- Performance monitoring and domain-specific thresholds
- Executive function accommodations (clear error messages)
- Request/response interceptors
- Error handling with user-friendly messages
"""

import asyncio
import time
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import httpx
import requests
from pydantic import BaseModel, BaseSettings

from ..logging import get_logger, get_performance_logger


class HTTPMethod(str, Enum):
    """Supported HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"


class RetryStrategy(str, Enum):
    """Retry strategies for failed requests."""
    EXPONENTIAL = "exponential"
    LINEAR = "linear"
    FIXED = "fixed"


class HTTPClientConfig(BaseSettings):
    """HTTP client configuration settings."""

    # Basic settings
    timeout: float = 30.0
    connect_timeout: float = 5.0
    read_timeout: float = 25.0

    # Retry settings
    max_retries: int = 3
    retry_strategy: RetryStrategy = RetryStrategy.EXPONENTIAL
    backoff_factor: float = 0.5
    retry_status_codes: List[int] = [408, 429, 500, 502, 503, 504]

    # Performance monitoring
    performance_threshold_security: float = 1.0  # Security tools: <1s
    performance_threshold_productivity: float = 2.0  # Productivity: <2s
    performance_threshold_mtg: float = 3.0  # MTG tools: <3s
    performance_threshold_infrastructure: float = 5.0  # Infrastructure: <5s

    # Executive function accommodations
    enable_progress_callbacks: bool = True
    include_request_context: bool = True
    user_friendly_errors: bool = True

    # Security settings
    verify_ssl: bool = True
    follow_redirects: bool = True
    max_redirects: int = 10

    class Config:
        env_prefix = "HTTP_CLIENT_"


class HTTPResponse(BaseModel):
    """Standardized HTTP response model."""

    status_code: int
    headers: Dict[str, str]
    content: Union[str, bytes, Dict[str, Any]]
    success: bool
    error_message: Optional[str] = None

    # Performance metrics
    response_time_ms: float
    domain: Optional[str] = None
    tool_name: Optional[str] = None

    # Request context for debugging
    request_url: Optional[str] = None
    request_method: Optional[str] = None

    @property
    def json(self) -> Optional[Dict[str, Any]]:
        """Get response content as JSON if applicable."""
        if isinstance(self.content, dict):
            return self.content
        return None

    @property
    def text(self) -> str:
        """Get response content as text."""
        if isinstance(self.content, str):
            return self.content
        elif isinstance(self.content, bytes):
            return self.content.decode('utf-8')
        else:
            return str(self.content)


class HTTPError(Exception):
    """HTTP client error with executive function accommodations."""

    def __init__(
        self,
        message: str,
        response: Optional[HTTPResponse] = None,
        user_friendly_message: Optional[str] = None
    ):
        self.response = response
        self.user_friendly_message = user_friendly_message or message
        super().__init__(message)


class BaseHTTPClient(ABC):
    """Abstract base class for HTTP clients."""

    def __init__(self, config: HTTPClientConfig):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.perf_logger = get_performance_logger(
            f"{self.__class__.__name__}.performance"
        )
        self._session = None

    @abstractmethod
    def request(
        self,
        method: HTTPMethod,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        **kwargs
    ) -> HTTPResponse:
        """Make an HTTP request."""
        pass

    @abstractmethod
    async def async_request(
        self,
        method: HTTPMethod,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        **kwargs
    ) -> HTTPResponse:
        """Make an async HTTP request."""
        pass

    def _calculate_delay(self, attempt: int) -> float:
        """Calculate retry delay based on strategy."""
        if self.config.retry_strategy == RetryStrategy.EXPONENTIAL:
            return self.config.backoff_factor * (2 ** attempt)
        elif self.config.retry_strategy == RetryStrategy.LINEAR:
            return self.config.backoff_factor * attempt
        else:  # FIXED
            return self.config.backoff_factor

    def _should_retry(self, status_code: int, attempt: int) -> bool:
        """Determine if request should be retried."""
        return (
            attempt < self.config.max_retries and
            status_code in self.config.retry_status_codes
        )

    def _check_performance_threshold(self, domain: str, response_time: float):
        """Check if response time exceeds domain-specific threshold."""
        thresholds = {
            "security": self.config.performance_threshold_security,
            "productivity": self.config.performance_threshold_productivity,
            "mtg": self.config.performance_threshold_mtg,
            "infrastructure": self.config.performance_threshold_infrastructure
        }

        threshold = thresholds.get(domain, 5.0)
        if response_time > threshold:
            self.logger.warning(
                f"Slow response detected for {domain} domain: "
                f"{response_time:.2f}s > {threshold}s"
            )

    def _create_user_friendly_error(
        self, error: Exception, url: str
    ) -> str:
        """Create user-friendly error message."""
        if not self.config.user_friendly_errors:
            return str(error)

        if "timeout" in str(error).lower():
            return (
                "The request took too long to complete. This might be "
                "temporary - please wait a moment and try again."
            )
        elif "connection" in str(error).lower():
            return (
                "Unable to connect to the service. Please check your "
                "internet connection and try again."
            )
        elif "ssl" in str(error).lower():
            return (
                "There was a security certificate issue. Please try "
                "again or contact support if the problem continues."
            )
        else:
            return (
                f"There was a problem with the request to {url}. "
                "Please try again or contact support if this continues."
            )

    def get(self, url: str, **kwargs) -> HTTPResponse:
        """Make a GET request."""
        return self.request(HTTPMethod.GET, url, **kwargs)

    def post(self, url: str, **kwargs) -> HTTPResponse:
        """Make a POST request."""
        return self.request(HTTPMethod.POST, url, **kwargs)

    def put(self, url: str, **kwargs) -> HTTPResponse:
        """Make a PUT request."""
        return self.request(HTTPMethod.PUT, url, **kwargs)

    def patch(self, url: str, **kwargs) -> HTTPResponse:
        """Make a PATCH request."""
        return self.request(HTTPMethod.PATCH, url, **kwargs)

    def delete(self, url: str, **kwargs) -> HTTPResponse:
        """Make a DELETE request."""
        return self.request(HTTPMethod.DELETE, url, **kwargs)

    async def async_get(self, url: str, **kwargs) -> HTTPResponse:
        """Make an async GET request."""
        return await self.async_request(HTTPMethod.GET, url, **kwargs)

    async def async_post(self, url: str, **kwargs) -> HTTPResponse:
        """Make an async POST request."""
        return await self.async_request(HTTPMethod.POST, url, **kwargs)

    async def async_put(self, url: str, **kwargs) -> HTTPResponse:
        """Make an async PUT request."""
        return await self.async_request(HTTPMethod.PUT, url, **kwargs)

    async def async_patch(self, url: str, **kwargs) -> HTTPResponse:
        """Make an async PATCH request."""
        return await self.async_request(HTTPMethod.PATCH, url, **kwargs)

    async def async_delete(self, url: str, **kwargs) -> HTTPResponse:
        """Make an async DELETE request."""
        return await self.async_request(HTTPMethod.DELETE, url, **kwargs)


class RequestsHTTPClient(BaseHTTPClient):
    """HTTP client implementation using requests library."""

    def __init__(self, config: HTTPClientConfig):
        super().__init__(config)
        self._session = requests.Session()

        # Configure session
        self._session.verify = config.verify_ssl
        if config.follow_redirects:
            self._session.max_redirects = config.max_redirects

    def request(
        self,
        method: HTTPMethod,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        **kwargs
    ) -> HTTPResponse:
        """Make an HTTP request using requests."""
        start_time = time.time()
        last_error = None

        # Extract context for performance monitoring
        domain = kwargs.pop("domain", None)
        tool_name = kwargs.pop("tool_name", None)

        for attempt in range(self.config.max_retries + 1):
            try:
                # Make request
                response = self._session.request(
                    method=method.value,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    timeout=(
                        self.config.connect_timeout,
                        self.config.read_timeout
                    ),
                    **kwargs
                )

                # Calculate response time
                response_time = (time.time() - start_time) * 1000

                # Check performance threshold
                if domain:
                    self._check_performance_threshold(domain, response_time)

                # Log performance
                self.perf_logger.log_performance(
                    f"{method.value} {url}",
                    response_time / 1000,
                    domain=domain,
                    tool_name=tool_name,
                    status_code=response.status_code
                )

                # Parse response content
                try:
                    content = response.json()
                except ValueError:
                    content = response.text

                # Create response object
                http_response = HTTPResponse(
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    content=content,
                    success=200 <= response.status_code < 400,
                    response_time_ms=response_time,
                    domain=domain,
                    tool_name=tool_name,
                    request_url=url,
                    request_method=method.value
                )

                # Handle HTTP errors
                if not http_response.success:
                    if self._should_retry(response.status_code, attempt):
                        delay = self._calculate_delay(attempt)
                        self.logger.warning(
                            f"Request failed with status {response.status_code}. "
                            f"Retrying in {delay:.2f}s (attempt {attempt + 1}/"
                            f"{self.config.max_retries + 1})"
                        )
                        time.sleep(delay)
                        continue

                    http_response.error_message = (
                        f"HTTP {response.status_code}: {response.reason}"
                    )

                return http_response

            except Exception as e:
                last_error = e

                if attempt < self.config.max_retries:
                    delay = self._calculate_delay(attempt)
                    self.logger.warning(
                        f"Request failed with error: {str(e)}. "
                        f"Retrying in {delay:.2f}s (attempt {attempt + 1}/"
                        f"{self.config.max_retries + 1})"
                    )
                    time.sleep(delay)
                    continue

                # Final attempt failed
                response_time = (time.time() - start_time) * 1000
                user_friendly_msg = self._create_user_friendly_error(e, url)

                raise HTTPError(
                    f"Request failed after {self.config.max_retries + 1} "
                    f"attempts: {str(e)}",
                    user_friendly_message=user_friendly_msg
                )

        # Should not reach here
        raise HTTPError(
            "Unexpected error in request retry loop",
            user_friendly_message="An unexpected error occurred. Please try again."
        )

    async def async_request(
        self,
        method: HTTPMethod,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        **kwargs
    ) -> HTTPResponse:
        """Make an async HTTP request (runs in executor)."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            lambda: self.request(
                method, url, headers, params, json, data, **kwargs
            )
        )


class HTTPXClient(BaseHTTPClient):
    """HTTP client implementation using httpx library."""

    def __init__(self, config: HTTPClientConfig):
        super().__init__(config)

        # Configure httpx client
        self._client = httpx.Client(
            verify=config.verify_ssl,
            follow_redirects=config.follow_redirects,
            max_redirects=config.max_redirects,
            timeout=httpx.Timeout(
                connect=config.connect_timeout,
                read=config.read_timeout,
                write=config.timeout,
                pool=config.timeout
            )
        )

        self._async_client = httpx.AsyncClient(
            verify=config.verify_ssl,
            follow_redirects=config.follow_redirects,
            max_redirects=config.max_redirects,
            timeout=httpx.Timeout(
                connect=config.connect_timeout,
                read=config.read_timeout,
                write=config.timeout,
                pool=config.timeout
            )
        )

    def request(
        self,
        method: HTTPMethod,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        **kwargs
    ) -> HTTPResponse:
        """Make an HTTP request using httpx."""
        return asyncio.run(
            self.async_request(
                method, url, headers, params, json, data, **kwargs
            )
        )

    async def async_request(
        self,
        method: HTTPMethod,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[str, bytes, Dict[str, Any]]] = None,
        **kwargs
    ) -> HTTPResponse:
        """Make an async HTTP request using httpx."""
        start_time = time.time()
        last_error = None

        # Extract context for performance monitoring
        domain = kwargs.pop("domain", None)
        tool_name = kwargs.pop("tool_name", None)

        for attempt in range(self.config.max_retries + 1):
            try:
                # Make request
                response = await self._async_client.request(
                    method=method.value,
                    url=url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    **kwargs
                )

                # Calculate response time
                response_time = (time.time() - start_time) * 1000

                # Check performance threshold
                if domain:
                    self._check_performance_threshold(domain, response_time)

                # Log performance
                self.perf_logger.log_performance(
                    f"{method.value} {url}",
                    response_time / 1000,
                    domain=domain,
                    tool_name=tool_name,
                    status_code=response.status_code
                )

                # Parse response content
                try:
                    content = response.json()
                except ValueError:
                    content = response.text

                # Create response object
                http_response = HTTPResponse(
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    content=content,
                    success=200 <= response.status_code < 400,
                    response_time_ms=response_time,
                    domain=domain,
                    tool_name=tool_name,
                    request_url=url,
                    request_method=method.value
                )

                # Handle HTTP errors
                if not http_response.success:
                    if self._should_retry(response.status_code, attempt):
                        delay = self._calculate_delay(attempt)
                        self.logger.warning(
                            f"Request failed with status {response.status_code}. "
                            f"Retrying in {delay:.2f}s (attempt {attempt + 1}/"
                            f"{self.config.max_retries + 1})"
                        )
                        await asyncio.sleep(delay)
                        continue

                    http_response.error_message = (
                        f"HTTP {response.status_code}: {response.reason_phrase}"
                    )

                return http_response

            except Exception as e:
                last_error = e

                if attempt < self.config.max_retries:
                    delay = self._calculate_delay(attempt)
                    self.logger.warning(
                        f"Request failed with error: {str(e)}. "
                        f"Retrying in {delay:.2f}s (attempt {attempt + 1}/"
                        f"{self.config.max_retries + 1})"
                    )
                    await asyncio.sleep(delay)
                    continue

                # Final attempt failed
                response_time = (time.time() - start_time) * 1000
                user_friendly_msg = self._create_user_friendly_error(e, url)

                raise HTTPError(
                    f"Request failed after {self.config.max_retries + 1} "
                    f"attempts: {str(e)}",
                    user_friendly_message=user_friendly_msg
                )

        # Should not reach here
        raise HTTPError(
            "Unexpected error in request retry loop",
            user_friendly_message="An unexpected error occurred. Please try again."
        )

    def close(self):
        """Close HTTP clients."""
        self._client.close()
        asyncio.create_task(self._async_client.aclose())


# Factory functions
def create_http_client(
    config: Optional[HTTPClientConfig] = None,
    client_type: str = "requests"
) -> BaseHTTPClient:
    """Create an HTTP client instance."""
    if config is None:
        config = HTTPClientConfig()

    if client_type.lower() == "httpx":
        return HTTPXClient(config)
    else:
        return RequestsHTTPClient(config)


# Convenience functions for quick usage
def get(url: str, **kwargs) -> HTTPResponse:
    """Make a GET request with default configuration."""
    client = create_http_client()
    return client.get(url, **kwargs)


def post(url: str, **kwargs) -> HTTPResponse:
    """Make a POST request with default configuration."""
    client = create_http_client()
    return client.post(url, **kwargs)


async def async_get(url: str, **kwargs) -> HTTPResponse:
    """Make an async GET request with default configuration."""
    client = create_http_client(client_type="httpx")
    return await client.async_get(url, **kwargs)


async def async_post(url: str, **kwargs) -> HTTPResponse:
    """Make an async POST request with default configuration."""
    client = create_http_client(client_type="httpx")
    return await client.async_post(url, **kwargs)
