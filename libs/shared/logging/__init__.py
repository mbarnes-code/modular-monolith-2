"""
Shared logging library for Mental Prosthetic Platform.

Provides unified logging across all 37 integrated tools with executive function
accommodations and constitutional compliance tracking.
"""

import json
import logging
import logging.config
import os
import sys
from datetime import datetime
from enum import Enum
from pathlib import Path

from pydantic import BaseSettings


class LogLevel(str, Enum):
    """Supported log levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class LogFormat(str, Enum):
    """Supported log formats."""
    JSON = "json"
    CONSOLE = "console"
    DETAILED = "detailed"


class LoggingConfig(BaseSettings):
    """Logging configuration settings."""

    # Core settings
    log_level: LogLevel = LogLevel.INFO
    log_format: LogFormat = LogFormat.CONSOLE

    # Output settings
    log_to_console: bool = True
    log_to_file: bool = True
    log_file_path: str = "logs/app.log"
    log_file_max_size: int = 10 * 1024 * 1024  # 10MB
    log_file_backup_count: int = 5

    # Service identification
    service_name: str = "unknown"
    service_version: str = "unknown"
    environment: str = "development"

    # Performance monitoring
    log_slow_queries: bool = True
    slow_query_threshold: float = 1.0  # seconds

    # Executive function accommodations
    enable_adhd_friendly_format: bool = True
    use_color_coding: bool = True
    include_context_breadcrumbs: bool = True

    class Config:
        env_prefix = "LOG_"


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging."""

    def __init__(
        self, service_name: str, service_version: str, environment: str
    ):
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment
        super().__init__()

    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": {
                "name": self.service_name,
                "version": self.service_version,
                "environment": self.environment
            },
            "source": {
                "file": record.pathname,
                "line": record.lineno,
                "function": record.funcName
            }
        }

        # Add exception info if present
        if record.exc_info:
            exc_type = (
                record.exc_info[0].__name__ if record.exc_info[0] else None
            )
            exc_msg = str(record.exc_info[1]) if record.exc_info[1] else None
            log_entry["exception"] = {
                "type": exc_type,
                "message": exc_msg,
                "traceback": self.formatException(record.exc_info)
            }

        # Add extra fields from log record
        excluded_keys = [
            "name", "msg", "args", "levelname", "levelno", "pathname",
            "filename", "module", "lineno", "funcName", "created",
            "msecs", "relativeCreated", "thread", "threadName",
            "processName", "process", "exc_info", "exc_text", "stack_info"
        ]
        for key, value in record.__dict__.items():
            if key not in excluded_keys:
                log_entry["extra"] = log_entry.get("extra", {})
                log_entry["extra"][key] = value

        return json.dumps(log_entry, ensure_ascii=False)


class ConsoleFormatter(logging.Formatter):
    """Human-readable console formatter with color coding."""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def __init__(self, use_colors: bool = True, adhd_friendly: bool = True):
        has_tty = hasattr(sys.stderr, 'isatty') and sys.stderr.isatty()
        self.use_colors = use_colors and has_tty
        self.adhd_friendly = adhd_friendly

        if self.adhd_friendly:
            # More structured format for executive function support
            fmt = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
        else:
            fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

        super().__init__(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with optional colors."""
        if self.use_colors and record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            reset = self.COLORS['RESET']
            record.levelname = f"{color}{record.levelname}{reset}"

        formatted = super().format(record)

        # Add context breadcrumbs for executive function support
        if self.adhd_friendly and hasattr(record, 'context'):
            formatted += f" [Context: {record.context}]"

        return formatted


class DetailedFormatter(logging.Formatter):
    """Detailed formatter for debugging with all available information."""

    def __init__(self):
        fmt = (
            "%(asctime)s | %(levelname)s | %(name)s | "
            "%(pathname)s:%(funcName)s:%(lineno)d | "
            "%(message)s"
        )
        super().__init__(fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S.%f")


class LoggerSetup:
    """Centralized logger setup for all services."""

    def __init__(self, config: LoggingConfig):
        self.config = config

    def setup_logging(self) -> logging.Logger:
        """Setup and configure logging based on configuration."""
        # Create logs directory if it doesn't exist
        log_dir = Path(self.config.log_file_path).parent
        log_dir.mkdir(parents=True, exist_ok=True)

        # Get root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.config.log_level))

        # Clear existing handlers
        root_logger.handlers.clear()

        # Setup console handler
        if self.config.log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, self.config.log_level))

            if self.config.log_format == LogFormat.JSON:
                console_formatter = StructuredFormatter(
                    self.config.service_name,
                    self.config.service_version,
                    self.config.environment
                )
            elif self.config.log_format == LogFormat.DETAILED:
                console_formatter = DetailedFormatter()
            else:
                console_formatter = ConsoleFormatter(
                    use_colors=self.config.use_color_coding,
                    adhd_friendly=self.config.enable_adhd_friendly_format
                )

            console_handler.setFormatter(console_formatter)
            root_logger.addHandler(console_handler)

        # Setup file handler
        if self.config.log_to_file:
            from logging.handlers import RotatingFileHandler

            file_handler = RotatingFileHandler(
                self.config.log_file_path,
                maxBytes=self.config.log_file_max_size,
                backupCount=self.config.log_file_backup_count
            )
            file_handler.setLevel(getattr(logging, self.config.log_level))

            # Always use JSON format for file logs
            file_formatter = StructuredFormatter(
                self.config.service_name,
                self.config.service_version,
                self.config.environment
            )
            file_handler.setFormatter(file_formatter)
            root_logger.addHandler(file_handler)

        return root_logger

    def get_logger(self, name: str) -> logging.Logger:
        """Get a logger with the specified name."""
        return logging.getLogger(name)


class PerformanceLogger:
    """Logger for performance monitoring and slow query detection."""

    def __init__(self, logger: logging.Logger, threshold: float = 1.0):
        self.logger = logger
        self.threshold = threshold

    def log_performance(self, operation: str, duration: float, **kwargs):
        """Log performance metrics."""
        extra = {
            "operation": operation,
            "duration_seconds": duration,
            "performance_metric": True,
            **kwargs
        }

        if duration > self.threshold:
            self.logger.warning(
                f"Slow operation detected: {operation} took {duration:.2f}s",
                extra=extra
            )
        else:
            self.logger.debug(
                f"Operation completed: {operation} took {duration:.2f}s",
                extra=extra
            )


# Convenience functions
def setup_logging(
    service_name: str,
    service_version: str = "unknown",
    environment: str = None,
    log_level: str = None,
    log_format: str = None,
    **kwargs
) -> logging.Logger:
    """Convenience function to setup logging quickly."""
    config = LoggingConfig(
        service_name=service_name,
        service_version=service_version,
        environment=environment or os.getenv("ENVIRONMENT", "development"),
        log_level=LogLevel(log_level or os.getenv("LOG_LEVEL", "INFO")),
        log_format=LogFormat(log_format or os.getenv("LOG_FORMAT", "console")),
        **kwargs
    )

    logger_setup = LoggerSetup(config)
    return logger_setup.setup_logging()


def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)


def get_performance_logger(
    name: str, threshold: float = 1.0
) -> PerformanceLogger:
    """Get a performance logger for monitoring slow operations."""
    logger = get_logger(name)
    return PerformanceLogger(logger, threshold)
