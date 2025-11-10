"""
Core Exception Classes

Custom exception classes for the Jane Orchestrator application,
including MISP external API integration exceptions.
"""


class BaseJaneException(Exception):
    """Base exception class for Jane Orchestrator."""
    pass


class DatabaseError(BaseJaneException):
    """Database operation errors."""
    pass


class AuthenticationError(BaseJaneException):
    """Authentication and authorization errors."""
    pass


class ValidationError(BaseJaneException):
    """Data validation errors."""
    pass


class ConfigurationError(BaseJaneException):
    """Configuration and setup errors."""
    pass


# MISP External API Integration Exceptions

class ExternalAPIError(BaseJaneException):
    """Base class for external API integration errors."""
    pass


class FeedImportError(ExternalAPIError):
    """Feed import operation errors."""
    pass


class SyncError(ExternalAPIError):
    """Server synchronization errors."""
    pass


class WebhookError(ExternalAPIError):
    """Webhook notification errors."""
    pass


class NetworkError(ExternalAPIError):
    """Network connectivity and timeout errors."""
    pass


class ParsingError(ExternalAPIError):
    """Data parsing and format errors."""
    pass


class RetryExhaustedError(ExternalAPIError):
    """Error when maximum retry attempts are exhausted."""
    pass
