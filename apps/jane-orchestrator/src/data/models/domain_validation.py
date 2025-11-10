"""
Domain Validation Model

Tracks validation results for constitutional performance compliance.
Records validation runs, results, and recommendations for each domain.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from libs.shared.data.base import BaseModel
from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text

from .performance_metrics import DomainType


class ValidationStatus(str, Enum):
    """Status of domain validation runs"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"


class ValidationSeverity(str, Enum):
    """Severity levels for validation issues"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DomainValidation(BaseModel):
    """
    Domain validation results for constitutional compliance

    Attributes:
        domain: Domain being validated (Security, Productivity, MTG,
                Infrastructure)
        validation_run_id: Unique identifier for this validation run
        status: Overall validation status (passed/failed/warning/error)
        started_at: When validation started
        completed_at: When validation completed (if finished)
        duration_ms: Total validation duration in milliseconds
        tools_tested: Number of tools tested in this domain
        metrics_collected: Number of performance metrics collected
        violations_found: Number of constitutional violations found
        warnings_found: Number of warnings found
        pass_rate: Percentage of tests that passed (0.0-1.0)
        summary: Human-readable summary of validation results
        recommendations: List of recommendations for improvement
        detailed_results: Detailed validation results and metrics
        metadata: Additional validation context and configuration
        triggered_by: What triggered this validation (manual/scheduled/ci)
    """

    __tablename__ = "domain_validations"

    # Core identification
    domain = Column(String(50), nullable=False, index=True)
    validation_run_id = Column(
        String(100), nullable=False, unique=True, index=True
    )

    # Validation status
    status = Column(String(20), nullable=False, default="pending", index=True)
    started_at = Column(
        DateTime, nullable=False, default=datetime.utcnow, index=True
    )
    completed_at = Column(DateTime, nullable=True, index=True)
    duration_ms = Column(Float, nullable=True)  # Total validation time

    # Validation metrics
    tools_tested = Column(Integer, nullable=False, default=0)
    metrics_collected = Column(Integer, nullable=False, default=0)
    violations_found = Column(Integer, nullable=False, default=0)
    warnings_found = Column(Integer, nullable=False, default=0)
    pass_rate = Column(Float, nullable=True)  # 0.0-1.0

    # Results and recommendations
    summary = Column(Text, nullable=True)
    recommendations = Column(JSON, nullable=True)  # List of recommendations
    detailed_results = Column(JSON, nullable=True)  # Detailed metrics/results
    metadata = Column(JSON, nullable=True)  # Additional context

    # Execution context
    triggered_by = Column(String(50), nullable=False, default="manual")
    triggered_by_user = Column(String(100), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.validation_run_id:
            # Generate unique run ID
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            self.validation_run_id = f"{self.domain}_{timestamp}"

    @property
    def domain_enum(self) -> DomainType:
        """Get domain as enum"""
        return DomainType(self.domain)

    @property
    def status_enum(self) -> ValidationStatus:
        """Get status as enum"""
        return ValidationStatus(self.status)

    @property
    def is_completed(self) -> bool:
        """Check if validation is completed"""
        return self.completed_at is not None

    @property
    def is_passed(self) -> bool:
        """Check if validation passed"""
        return self.status == ValidationStatus.PASSED.value

    @property
    def is_failed(self) -> bool:
        """Check if validation failed"""
        return self.status == ValidationStatus.FAILED.value

    @property
    def has_violations(self) -> bool:
        """Check if constitutional violations were found"""
        return self.violations_found > 0

    @property
    def severity_level(self) -> ValidationSeverity:
        """Get overall severity level based on results"""
        if self.violations_found > 0:
            return ValidationSeverity.CRITICAL
        elif self.warnings_found > 5:
            return ValidationSeverity.ERROR
        elif self.warnings_found > 0:
            return ValidationSeverity.WARNING
        else:
            return ValidationSeverity.INFO

    def mark_completed(self, status: ValidationStatus) -> None:
        """Mark validation as completed with given status"""
        self.status = status.value
        self.completed_at = datetime.utcnow()
        if self.started_at:
            delta = self.completed_at - self.started_at
            self.duration_ms = delta.total_seconds() * 1000

    def add_recommendation(
        self,
        recommendation: str,
        severity: str = "info",
        category: str = "performance"
    ) -> None:
        """Add a recommendation to the validation results"""
        if not self.recommendations:
            self.recommendations = []

        self.recommendations.append({
            "recommendation": recommendation,
            "severity": severity,
            "category": category,
            "timestamp": datetime.utcnow().isoformat()
        })

    def calculate_pass_rate(self, total_tests: int, passed_tests: int) -> None:
        """Calculate and set the pass rate"""
        if total_tests > 0:
            self.pass_rate = passed_tests / total_tests
        else:
            self.pass_rate = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "domain": self.domain,
            "validation_run_id": self.validation_run_id,
            "status": self.status,
            "started_at": (
                self.started_at.isoformat() if self.started_at else None
            ),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "duration_ms": self.duration_ms,
            "tools_tested": self.tools_tested,
            "metrics_collected": self.metrics_collected,
            "violations_found": self.violations_found,
            "warnings_found": self.warnings_found,
            "pass_rate": self.pass_rate,
            "summary": self.summary,
            "recommendations": self.recommendations,
            "detailed_results": self.detailed_results,
            "metadata": self.metadata,
            "triggered_by": self.triggered_by,
            "triggered_by_user": self.triggered_by_user,
            "is_completed": self.is_completed,
            "is_passed": self.is_passed,
            "is_failed": self.is_failed,
            "has_violations": self.has_violations,
            "severity_level": self.severity_level.value,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }

    @classmethod
    def create_validation_run(
        cls,
        domain: DomainType,
        triggered_by: str = "manual",
        triggered_by_user: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "DomainValidation":
        """
        Create a new domain validation run

        Args:
            domain: Domain to validate
            triggered_by: What triggered this validation
            triggered_by_user: User who triggered validation
            metadata: Additional context

        Returns:
            DomainValidation instance
        """
        return cls(
            domain=domain.value,
            status=ValidationStatus.PENDING.value,
            triggered_by=triggered_by,
            triggered_by_user=triggered_by_user,
            metadata=metadata or {}
        )

    def generate_summary(self) -> None:
        """Generate human-readable summary of validation results"""
        if not self.is_completed:
            self.summary = f"Validation for {self.domain} domain is pending"
            return

        domain_name = self.domain.title()
        duration_str = (
            f"{self.duration_ms/1000:.2f}s" if self.duration_ms else "unknown"
        )

        if self.is_passed:
            self.summary = (
                f"{domain_name} domain validation PASSED in {duration_str}. "
                f"Tested {self.tools_tested} tools, "
                f"collected {self.metrics_collected} metrics, "
                f"found {self.violations_found} violations, "
                f"{self.warnings_found} warnings. "
                f"Pass rate: {self.pass_rate*100:.1f}%"
            )
        else:
            self.summary = (
                f"{domain_name} domain validation FAILED in {duration_str}. "
                f"Tested {self.tools_tested} tools, "
                f"collected {self.metrics_collected} metrics, "
                f"found {self.violations_found} constitutional violations, "
                f"{self.warnings_found} warnings. "
                f"Pass rate: {self.pass_rate*100:.1f}%"
            )

        # Add severity context
        severity = self.severity_level
        if severity == ValidationSeverity.CRITICAL:
            self.summary += " CRITICAL issues - immediate action required."
        elif severity == ValidationSeverity.ERROR:
            self.summary += " Multiple issues require attention."
        elif severity == ValidationSeverity.WARNING:
            self.summary += " Minor issues detected."

    def __repr__(self) -> str:
        return (
            f"<DomainValidation("
            f"domain={self.domain}, "
            f"run_id={self.validation_run_id}, "
            f"status={self.status}, "
            f"violations={self.violations_found}, "
            f"pass_rate={self.pass_rate}"
            f")>"
        )
