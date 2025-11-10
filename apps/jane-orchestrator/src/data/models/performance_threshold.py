"""
Performance Threshold Model

Defines constitutional performance thresholds for domain validation.
Supports configurable thresholds while enforcing constitutional minimums.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict

from libs.shared.data.base import BaseModel
from sqlalchemy import (JSON, Boolean, Column, DateTime, Float, String,
                        UniqueConstraint)

from .performance_metrics import DomainType, MetricType


class ThresholdStatus(str, Enum):
    """Status of performance thresholds"""
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    TESTING = "testing"


class PerformanceThreshold(BaseModel):
    """
    Performance threshold configuration for constitutional compliance

    Attributes:
        domain: Domain this threshold applies to (Security, Productivity,
                MTG, Infrastructure)
        metric_type: Type of metric this threshold applies to
        threshold_ms: Threshold value in milliseconds
        constitutional_minimum: Constitutional minimum threshold (cannot
                               be exceeded)
        is_default: Whether this is the default constitutional threshold
        description: Human-readable description of the threshold
        status: Whether this threshold is active, deprecated, or testing
        effective_date: When this threshold becomes effective
        created_by: Who created this threshold (system/admin/user)
        metadata: Additional configuration metadata
    """

    __tablename__ = "performance_thresholds"

    # Unique constraint on domain + metric_type for active thresholds
    __table_args__ = (
        UniqueConstraint(
            'domain', 'metric_type', 'status',
            name='uq_active_domain_metric_threshold'
        ),
    )

    # Core identification
    domain = Column(String(50), nullable=False, index=True)
    metric_type = Column(String(50), nullable=False, index=True)

    # Threshold configuration
    threshold_ms = Column(Float, nullable=False)
    constitutional_minimum = Column(Float, nullable=False)
    is_default = Column(Boolean, nullable=False, default=True)

    # Metadata
    description = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default="active", index=True)
    effective_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_by = Column(String(100), nullable=False, default="system")
    metadata = Column(JSON, nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure threshold doesn't violate constitutional minimum
        if (self.threshold_ms and self.constitutional_minimum and
                self.threshold_ms > self.constitutional_minimum):
            self.threshold_ms = self.constitutional_minimum

    @property
    def domain_enum(self) -> DomainType:
        """Get domain as enum"""
        return DomainType(self.domain)

    @property
    def metric_type_enum(self) -> MetricType:
        """Get metric type as enum"""
        return MetricType(self.metric_type)

    @property
    def status_enum(self) -> ThresholdStatus:
        """Get status as enum"""
        return ThresholdStatus(self.status)

    @property
    def is_constitutional_violation(self) -> bool:
        """Check if current threshold violates constitutional minimum"""
        return self.threshold_ms > self.constitutional_minimum

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "domain": self.domain,
            "metric_type": self.metric_type,
            "threshold_ms": self.threshold_ms,
            "constitutional_minimum": self.constitutional_minimum,
            "is_default": self.is_default,
            "description": self.description,
            "status": self.status,
            "effective_date": (
                self.effective_date.isoformat()
                if self.effective_date else None
            ),
            "created_by": self.created_by,
            "metadata": self.metadata,
            "is_constitutional_violation": self.is_constitutional_violation,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }

    @classmethod
    def create_constitutional_defaults(cls) -> list["PerformanceThreshold"]:
        """
        Create default constitutional thresholds for all domains

        Returns:
            List of PerformanceThreshold instances with constitutional defaults
        """
        thresholds = []

        # Domain-specific response time thresholds
        domain_thresholds = {
            DomainType.SECURITY: 1000.0,      # <1s for Security domain
            DomainType.PRODUCTIVITY: 2000.0,  # <2s for Productivity domain
            DomainType.MTG: 3000.0,           # <3s for MTG domain
            DomainType.INFRASTRUCTURE: 5000.0  # <5s for Infrastructure domain
        }

        for domain, threshold_ms in domain_thresholds.items():
            thresholds.append(cls(
                domain=domain.value,
                metric_type=MetricType.RESPONSE_TIME.value,
                threshold_ms=threshold_ms,
                constitutional_minimum=threshold_ms,
                is_default=True,
                description=(
                    f"Constitutional {domain.value} response time "
                    f"threshold: <{threshold_ms/1000}s"
                ),
                status=ThresholdStatus.ACTIVE.value,
                created_by="system",
                metadata={
                    "constitutional": True,
                    "domain_requirement": f"<{threshold_ms/1000}s",
                    "source": "constitutional_requirements"
                }
            ))

        # Universal UI response time threshold (<200ms)
        for domain in DomainType:
            thresholds.append(cls(
                domain=domain.value,
                metric_type=MetricType.UI_RESPONSE.value,
                threshold_ms=200.0,
                constitutional_minimum=200.0,
                is_default=True,
                description="Constitutional UI response threshold: <200ms",
                status=ThresholdStatus.ACTIVE.value,
                created_by="system",
                metadata={
                    "constitutional": True,
                    "global_requirement": "<200ms",
                    "executive_function_support": True,
                    "source": "constitutional_requirements"
                }
            ))

        # API latency thresholds (500ms p95)
        for domain in DomainType:
            thresholds.append(cls(
                domain=domain.value,
                metric_type=MetricType.API_LATENCY.value,
                threshold_ms=500.0,
                constitutional_minimum=500.0,
                is_default=True,
                description="Constitutional API latency threshold: <500ms p95",
                status=ThresholdStatus.ACTIVE.value,
                created_by="system",
                metadata={
                    "constitutional": True,
                    "percentile": "p95",
                    "source": "constitutional_requirements"
                }
            ))

        # WebSocket latency threshold (<250ms for cross-tool sync)
        for domain in DomainType:
            thresholds.append(cls(
                domain=domain.value,
                metric_type=MetricType.WEBSOCKET_LATENCY.value,
                threshold_ms=250.0,
                constitutional_minimum=250.0,
                is_default=True,
                description="Constitutional WebSocket latency: <250ms sync",
                status=ThresholdStatus.ACTIVE.value,
                created_by="system",
                metadata={
                    "constitutional": True,
                    "cross_tool_sync": True,
                    "source": "constitutional_requirements"
                }
            ))

        return thresholds

    @classmethod
    def get_threshold_for_domain_metric(
        cls,
        domain: DomainType,
        metric_type: MetricType
    ) -> float:
        """
        Get the constitutional threshold for a domain and metric type

        Args:
            domain: Domain type
            metric_type: Metric type

        Returns:
            Threshold value in milliseconds
        """
        # Constitutional defaults
        if metric_type == MetricType.RESPONSE_TIME:
            thresholds = {
                DomainType.SECURITY: 1000.0,
                DomainType.PRODUCTIVITY: 2000.0,
                DomainType.MTG: 3000.0,
                DomainType.INFRASTRUCTURE: 5000.0
            }
            return thresholds.get(domain, 5000.0)

        elif metric_type == MetricType.UI_RESPONSE:
            return 200.0  # Universal <200ms requirement

        elif metric_type == MetricType.API_LATENCY:
            return 500.0  # Universal <500ms p95 requirement

        elif metric_type == MetricType.WEBSOCKET_LATENCY:
            return 250.0  # Universal <250ms for real-time sync

        else:
            # Default fallback to infrastructure threshold
            return 5000.0

    def validate_constitutional_compliance(self) -> bool:
        """
        Validate that this threshold meets constitutional requirements

        Returns:
            True if threshold meets constitutional requirements
        """
        constitutional_threshold = self.get_threshold_for_domain_metric(
            self.domain_enum, self.metric_type_enum
        )
        return self.threshold_ms <= constitutional_threshold

    def __repr__(self) -> str:
        return (
            f"<PerformanceThreshold("
            f"domain={self.domain}, "
            f"metric={self.metric_type}, "
            f"threshold={self.threshold_ms}ms, "
            f"constitutional={self.constitutional_minimum}ms, "
            f"status={self.status}"
            f")>"
        )
