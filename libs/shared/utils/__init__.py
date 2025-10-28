"""
Cross-domain error handling and logging infrastructure.

Provides unified error handling and logging for all 37 integrated tools
with executive function accommodations and constitutional compliance tracking.
"""

import json
import logging
import sys
import traceback
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union
from uuid import uuid4

from pydantic import BaseModel


class ErrorSeverity(str, Enum):
    """Error severity levels for executive function accommodations."""
    CRITICAL = "critical"  # System-breaking, requires immediate attention
    HIGH = "high"        # User-blocking, affects primary functionality
    MEDIUM = "medium"    # Degraded performance, workarounds available
    LOW = "low"         # Minor issues, minimal user impact
    INFO = "info"       # Informational, no user impact


class ErrorCategory(str, Enum):
    """Error categories for domain-specific handling."""
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    VALIDATION = "validation"
    DATABASE = "database"
    NETWORK = "network"
    EXTERNAL_API = "external_api"
    PERFORMANCE = "performance"
    CONFIGURATION = "configuration"
    BUSINESS_LOGIC = "business_logic"
    EXECUTIVE_FUNCTION = "executive_function"  # ADHD/autism accommodations


class ErrorModel(BaseModel):
    """Structured error model for consistent error handling."""

    error_id: str
    timestamp: datetime
    severity: ErrorSeverity
    category: ErrorCategory
    domain: str  # security, productivity, mtg, infrastructure
    tool_name: Optional[str] = None
    error_code: str
    message: str
    details: Dict[str, Any] = {}
    user_message: Optional[str] = None  # Executive function friendly message
    suggestion: Optional[str] = None    # Actionable suggestion
    stack_trace: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class LogLevel(str, Enum):
    """Log levels aligned with Python logging."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogEntry(BaseModel):
    """Structured log entry model."""

    timestamp: datetime
    level: LogLevel
    logger_name: str
    message: str
    domain: str
    tool_name: Optional[str] = None
    user_id: Optional[str] = None
    request_id: Optional[str] = None
    response_time_ms: Optional[int] = None
    additional_data: Dict[str, Any] = {}

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ExecutiveFunctionErrorHandler:
    """
    Error handler optimized for executive function accommodations.

    Provides clear, actionable error messages and suggestions to support
    ADHD/autism users in understanding and resolving issues.
    """

    def __init__(self):
        self.error_suggestions = {
            ErrorCategory.AUTHENTICATION: {
                "default": "Please check your login credentials and try again.",
                "token_expired": "Your session has expired. Please log in again to continue.",
                "invalid_credentials": "The username or password is incorrect. Please try again."
            },
            ErrorCategory.VALIDATION: {
                "default": "Some information is missing or incorrect. Please review and try again.",
                "required_field": "This field is required. Please fill it in.",
                "invalid_format": "Please check the format of your input and try again."
            },
            ErrorCategory.PERFORMANCE: {
                "default": "The system is responding slowly. Please wait a moment and try again.",
                "timeout": "The request took too long. This might be temporary - please try again.",
                "overload": "The system is busy. Please wait a few minutes and try again."
            },
            ErrorCategory.EXECUTIVE_FUNCTION: {
                "context_lost": "Your work has been saved. You can continue where you left off.",
                "overwhelm": "Too many things happening at once. Let's focus on one task at a time.",
                "distraction": "Notification temporarily disabled to help you focus."
            }
        }

    def create_user_friendly_message(self, error: ErrorModel) -> str:
        """Create executive function friendly error message."""
        category_suggestions = self.error_suggestions.get(error.category, {})

        # Try specific error code first
        if error.error_code in category_suggestions:
            return category_suggestions[error.error_code]

        # Fall back to default for category
        if "default" in category_suggestions:
            return category_suggestions["default"]

        # Generic fallback
        return f"Something went wrong with {error.tool_name or 'the system'}. Please try again or contact support if the problem continues."

    def create_actionable_suggestion(self, error: ErrorModel) -> str:
        """Create actionable suggestion for error resolution."""
        suggestions = {
            ErrorCategory.AUTHENTICATION: "Try logging out and back in, or reset your password if needed.",
            ErrorCategory.VALIDATION: "Double-check all required fields are filled correctly.",
            ErrorCategory.DATABASE: "This is a temporary issue. Please try again in a few minutes.",
            ErrorCategory.NETWORK: "Check your internet connection and try again.",
            ErrorCategory.PERFORMANCE: "The system may be busy. Wait 30 seconds and try again.",
            ErrorCategory.EXECUTIVE_FUNCTION: "Take a break if needed. Your progress is saved automatically."
        }

        return suggestions.get(error.category, "Please try again or contact support if the issue persists.")


class MentalProstheticLogger:
    """
    Unified logging system for the Mental Prosthetic Platform.

    Provides structured logging across all 37 tools with performance
    tracking and executive function accommodation support.
    """

    def __init__(self, name: str, domain: str, log_level: str = "INFO"):
        self.name = name
        self.domain = domain
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))

        # Create formatters
        self.json_formatter = JsonFormatter()
        self.console_formatter = ConsoleFormatter()

        # Setup handlers
        self._setup_handlers()

        # Performance tracking
        self.performance_targets = {
            "security": 1000,      # <1s
            "productivity": 2000,  # <2s
            "mtg": 3000,          # <3s
            "infrastructure": 5000  # <5s
        }

    def _setup_handlers(self):
        """Setup logging handlers for console and file output."""
        # Console handler for development
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.console_formatter)
        self.logger.addHandler(console_handler)

        # File handler for structured logs
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        file_handler = logging.FileHandler(
            log_dir / f"{self.domain}-{self.name}.jsonl"
        )
        file_handler.setFormatter(self.json_formatter)
        self.logger.addHandler(file_handler)

    def log_structured(
        self,
        level: LogLevel,
        message: str,
        tool_name: Optional[str] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        response_time_ms: Optional[int] = None,
        **kwargs
    ):
        """Log structured entry with executive function context."""
        entry = LogEntry(
            timestamp=datetime.utcnow(),
            level=level,
            logger_name=self.name,
            message=message,
            domain=self.domain,
            tool_name=tool_name,
            user_id=user_id,
            request_id=request_id,
            response_time_ms=response_time_ms,
            additional_data=kwargs
        )

        # Check performance compliance
        if response_time_ms and self.domain in self.performance_targets:
            target = self.performance_targets[self.domain]
            if response_time_ms > target:
                self.logger.warning(
                    f"Performance target exceeded: {response_time_ms}ms > {target}ms target for {self.domain} domain"
                )

        # Log the entry
        getattr(self.logger, level.lower())(entry.json())

    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self.log_structured(LogLevel.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs):
        """Log info message."""
        self.log_structured(LogLevel.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self.log_structured(LogLevel.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs):
        """Log error message."""
        self.log_structured(LogLevel.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self.log_structured(LogLevel.CRITICAL, message, **kwargs)


class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def format(self, record):
        """Format log record as JSON."""
        try:
            # Try to parse as structured LogEntry
            log_data = json.loads(record.getMessage())
            return json.dumps(log_data, ensure_ascii=False)
        except (json.JSONDecodeError, ValueError):
            # Fallback to simple JSON structure
            return json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "line": record.lineno
            }, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    """Human-readable console formatter."""

    def __init__(self):
        super().__init__(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


class ErrorManager:
    """
    Centralized error management for the Mental Prosthetic Platform.

    Handles error tracking, user notification, and recovery suggestions
    with executive function accommodations.
    """

    def __init__(self):
        self.error_handler = ExecutiveFunctionErrorHandler()
        self.logger = MentalProstheticLogger("error_manager", "system")
        self.error_store = []  # In production, use proper storage

    def handle_error(
        self,
        exception: Exception,
        domain: str,
        tool_name: Optional[str] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> ErrorModel:
        """Handle and process error with executive function support."""

        # Determine error category and severity
        category = self._categorize_error(exception)
        severity = self._determine_severity(exception, category)

        # Create structured error
        error = ErrorModel(
            error_id=str(uuid4()),
            timestamp=datetime.utcnow(),
            severity=severity,
            category=category,
            domain=domain,
            tool_name=tool_name,
            error_code=type(exception).__name__,
            message=str(exception),
            details=additional_context or {},
            stack_trace=traceback.format_exc(),
            user_id=user_id,
            request_id=request_id
        )

        # Add executive function accommodations
        error.user_message = self.error_handler.create_user_friendly_message(
            error)
        error.suggestion = self.error_handler.create_actionable_suggestion(
            error)

        # Log the error
        self.logger.error(
            f"Error in {domain}/{tool_name}: {error.message}",
            error_id=error.error_id,
            category=category.value,
            severity=severity.value,
            user_id=user_id,
            request_id=request_id
        )

        # Store for analysis
        self.error_store.append(error)

        return error

    def _categorize_error(self, exception: Exception) -> ErrorCategory:
        """Categorize error based on exception type."""
        error_type = type(exception).__name__

        category_mapping = {
            "AuthenticationError": ErrorCategory.AUTHENTICATION,
            "PermissionError": ErrorCategory.AUTHORIZATION,
            "ValidationError": ErrorCategory.VALIDATION,
            "DatabaseError": ErrorCategory.DATABASE,
            "ConnectionError": ErrorCategory.NETWORK,
            "TimeoutError": ErrorCategory.PERFORMANCE,
            "ConfigurationError": ErrorCategory.CONFIGURATION,
            "HTTPException": ErrorCategory.EXTERNAL_API
        }

        return category_mapping.get(error_type, ErrorCategory.BUSINESS_LOGIC)

    def _determine_severity(self, exception: Exception, category: ErrorCategory) -> ErrorSeverity:
        """Determine error severity based on exception and category."""

        # Critical errors that break core functionality
        critical_errors = ["SystemExit",
                           "KeyboardInterrupt", "DatabaseConnectionError"]
        if type(exception).__name__ in critical_errors:
            return ErrorSeverity.CRITICAL

        # High severity for user-blocking issues
        high_severity_categories = [
            ErrorCategory.AUTHENTICATION, ErrorCategory.DATABASE]
        if category in high_severity_categories:
            return ErrorSeverity.HIGH

        # Performance issues are medium severity
        if category == ErrorCategory.PERFORMANCE:
            return ErrorSeverity.MEDIUM

        # Default to low severity
        return ErrorSeverity.LOW


# Global instances for use across the platform
error_manager = ErrorManager()


def get_logger(name: str, domain: str) -> MentalProstheticLogger:
    """Get or create logger for specific domain and component."""
    return MentalProstheticLogger(name, domain)


def handle_exception(
    exception: Exception,
    domain: str,
    tool_name: Optional[str] = None,
    user_id: Optional[str] = None,
    request_id: Optional[str] = None,
    **context
) -> ErrorModel:
    """Global exception handler wrapper."""
    return error_manager.handle_error(
        exception, domain, tool_name, user_id, request_id, context
    )


# Domain-specific loggers for the 37 tools
def get_security_logger(tool_name: str) -> MentalProstheticLogger:
    """Get security domain logger."""
    return get_logger(f"security-{tool_name}", "security")


def get_productivity_logger(tool_name: str) -> MentalProstheticLogger:
    """Get productivity domain logger."""
    return get_logger(f"productivity-{tool_name}", "productivity")


def get_mtg_logger(tool_name: str) -> MentalProstheticLogger:
    """Get MTG domain logger."""
    return get_logger(f"mtg-{tool_name}", "mtg")


def get_infrastructure_logger(tool_name: str) -> MentalProstheticLogger:
    """Get infrastructure domain logger."""
    return get_logger(f"infrastructure-{tool_name}", "infrastructure")


if __name__ == "__main__":
    # Test the logging and error handling system
    logger = get_logger("test", "security")

    logger.info("Testing structured logging",
                tool_name="test-tool", user_id="user123")
    logger.warning("Performance warning",
                   response_time_ms=1500, tool_name="test-tool")

    try:
        raise ValueError("Test error for error handling")
    except Exception as e:
        error = handle_exception(e, "security", "test-tool", "user123")
        print(f"Error handled: {error.user_message}")
        print(f"Suggestion: {error.suggestion}")
