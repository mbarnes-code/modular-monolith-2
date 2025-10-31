"""
Performance Metrics Model

Tracks domain-specific performance metrics for constitutional compliance.
Supports Security <1s, Productivity <2s, MTG <3s, Infrastructure <5s requirements.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from libs.shared.data.base import BaseModel
from sqlalchemy import JSON, Boolean, Column, DateTime, Float, String


class DomainType(str, Enum):
    """Domain types for performance tracking"""
    SECURITY = "security"
    PRODUCTIVITY = "productivity"
    MTG = "mtg"
    INFRASTRUCTURE = "infrastructure"


class MetricType(str, Enum):
    """Types of performance metrics"""
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    RESOURCE_USAGE = "resource_usage"
    UI_RESPONSE = "ui_response"
    API_LATENCY = "api_latency"
    DATABASE_QUERY = "database_query"
    WEBSOCKET_LATENCY = "websocket_latency"


class PerformanceMetrics(BaseModel):
    """
    Performance metrics tracking for constitutional compliance

    Attributes:
        domain: Which domain this metric belongs to (Security, Productivity,
                MTG, Infrastructure)
        tool_name: Specific tool being measured (MISP, n8n, etc.)
        metric_type: Type of performance metric being tracked
        value: Measured performance value (milliseconds for response times)
        threshold: Constitutional threshold for this metric
        is_violation: Whether this measurement violates constitutional
                     requirements
        timestamp: When the measurement was taken
        metadata: Additional context (user_id, request_id, etc.)
        test_run_id: Optional ID linking to performance test runs
    """

    __tablename__ = "performance_metrics"

    # Core identification
    domain = Column(String(50), nullable=False, index=True)
    tool_name = Column(String(100), nullable=False, index=True)
    metric_type = Column(String(50), nullable=False, index=True)

    # Performance measurement
    value = Column(Float, nullable=False)  # Measured value (ms)
    threshold = Column(Float, nullable=False)  # Constitutional threshold
    is_violation = Column(Boolean, nullable=False, default=False, index=True)

    # Timing and context
    timestamp = Column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    metadata = Column(JSON, nullable=True)  # Additional context
    test_run_id = Column(String(100), nullable=True, index=True)

    # Performance context
    user_session_id = Column(String(100), nullable=True, index=True)
    request_id = Column(String(100), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Automatically determine if this is a violation
        if self.value and self.threshold:
            self.is_violation = self.value > self.threshold

    @property
    def domain_enum(self) -> DomainType:
        """Get domain as enum"""
        return DomainType(self.domain)

    @property
    def metric_type_enum(self) -> MetricType:
        """Get metric type as enum"""
        return MetricType(self.metric_type)

    @property
    def performance_ratio(self) -> float:
        """Calculate performance ratio (actual/threshold)"""
        if self.threshold == 0:
            return float('inf') if self.value > 0 else 0
        return self.value / self.threshold

    @property
    def performance_grade(self) -> str:
        """Get performance grade based on ratio"""
        ratio = self.performance_ratio
        if ratio <= 0.5:
            return "EXCELLENT"
        elif ratio <= 0.8:
            return "GOOD"
        elif ratio <= 1.0:
            return "ACCEPTABLE"
        elif ratio <= 1.5:
            return "POOR"
        else:
            return "CRITICAL"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "domain": self.domain,
            "tool_name": self.tool_name,
            "metric_type": self.metric_type,
            "value": self.value,
            "threshold": self.threshold,
            "is_violation": self.is_violation,
            "performance_ratio": self.performance_ratio,
            "performance_grade": self.performance_grade,
            "timestamp": (
                self.timestamp.isoformat() if self.timestamp else None
            ),
            "metadata": self.metadata,
            "test_run_id": self.test_run_id,
            "user_session_id": self.user_session_id,
            "request_id": self.request_id,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }

    @classmethod
    def create_response_time_metric(
        cls,
        domain: DomainType,
        tool_name: str,
        response_time_ms: float,
        user_session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "PerformanceMetrics":
        """
        Create a response time metric with constitutional thresholds

        Args:
            domain: Domain type (Security, Productivity, MTG, Infrastructure)
            tool_name: Name of the tool being measured
            response_time_ms: Response time in milliseconds
            user_session_id: Optional user session ID
            request_id: Optional request ID for tracing
            metadata: Optional additional metadata

        Returns:
            PerformanceMetrics instance
        """
        # Constitutional thresholds by domain
        thresholds = {
            DomainType.SECURITY: 1000.0,  # <1s
            DomainType.PRODUCTIVITY: 2000.0,  # <2s
            DomainType.MTG: 3000.0,  # <3s
            DomainType.INFRASTRUCTURE: 5000.0  # <5s
        }

        return cls(
            domain=domain.value,
            tool_name=tool_name,
            metric_type=MetricType.RESPONSE_TIME.value,
            value=response_time_ms,
            threshold=thresholds[domain],
            user_session_id=user_session_id,
            request_id=request_id,
            metadata=metadata or {}
        )

    @classmethod
    def create_ui_response_metric(
        cls,
        tool_name: str,
        ui_response_time_ms: float,
        user_session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "PerformanceMetrics":
        """
        Create a UI response time metric with <200ms constitutional requirement

        Args:
            tool_name: Name of the tool/component
            ui_response_time_ms: UI response time in milliseconds
            user_session_id: Optional user session ID
            metadata: Optional additional metadata

        Returns:
            PerformanceMetrics instance
        """
        return cls(
            domain=DomainType.SECURITY.value,  # UI metrics apply globally
            tool_name=tool_name,
            metric_type=MetricType.UI_RESPONSE.value,
            value=ui_response_time_ms,
            threshold=200.0,  # <200ms constitutional requirement
            user_session_id=user_session_id,
            metadata=metadata or {}
        )

    def __repr__(self) -> str:
        return (
            f"<PerformanceMetrics("
            f"domain={self.domain}, "
            f"tool={self.tool_name}, "
            f"type={self.metric_type}, "
            f"value={self.value}ms, "
            f"threshold={self.threshold}ms, "
            f"violation={self.is_violation}"
            f")>"
        )
