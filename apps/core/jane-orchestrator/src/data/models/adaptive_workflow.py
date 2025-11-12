"""
AdaptiveWorkflow model for generated n8n workflows.

This model tracks automatically generated workflows and their performance
metrics for continuous improvement.
"""

from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import (JSON, Boolean, Column, DateTime, Float, ForeignKey,
                        Integer, String, Text)
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class AdaptiveWorkflow(BaseModel):
    """
    Model for tracking automatically generated n8n workflows.

    Stores workflow definitions, execution metrics, and optimization data
    for workflows generated from detected user patterns.
    """

    __tablename__ = "adaptive_workflows"

    # Workflow identification
    workflow_id: str = Column(
        String(255), unique=True, nullable=False, index=True
    )
    n8n_workflow_id: str = Column(String(255), nullable=True, index=True)
    workflow_name: str = Column(String(255), nullable=False)

    # Workflow metadata
    description: str = Column(Text, nullable=True)
    category: str = Column(String(100), nullable=False)
    version: str = Column(String(20), default="1.0.0")

    # Workflow definition
    workflow_definition: Dict[str, Any] = Column(JSON, nullable=False)
    node_configuration: List[Dict[str, Any]] = Column(JSON, nullable=False)
    connection_mapping: Dict[str, Any] = Column(JSON, nullable=False)

    # Generation metadata
    source_pattern_hash: str = Column(String(64), nullable=False, index=True)
    generation_method: str = Column(String(50), default="pattern_based")
    generation_confidence: float = Column(Float, default=0.0)

    # Execution metrics
    total_executions: int = Column(Integer, default=0)
    successful_executions: int = Column(Integer, default=0)
    failed_executions: int = Column(Integer, default=0)
    average_execution_time: float = Column(Float, default=0.0)

    # Performance tracking
    efficiency_score: float = Column(Float, default=0.0)  # 0.0-1.0
    user_satisfaction_score: float = Column(Float, default=0.0)
    time_savings_ratio: float = Column(Float, default=0.0)  # vs manual

    # Workflow status
    is_active: bool = Column(Boolean, default=True)
    is_validated: bool = Column(Boolean, default=False)
    is_optimized: bool = Column(Boolean, default=False)

    # Timestamps
    generated_at: datetime = Column(DateTime, default=datetime.utcnow)
    first_execution: datetime = Column(DateTime, nullable=True)
    last_execution: datetime = Column(DateTime, nullable=True)
    last_optimization: datetime = Column(DateTime, nullable=True)

    # User context
    user_id: str = Column(String(255), nullable=False, index=True)

    # Relationships
    pattern_id: str = Column(
        String(255), ForeignKey("workflow_patterns.id"), nullable=False
    )
    pattern = relationship(
        "WorkflowPattern", back_populates="adaptive_workflows"
    )

    def __repr__(self) -> str:
        return (
            f"<AdaptiveWorkflow(name='{self.workflow_name}', "
            f"id='{self.workflow_id}', active={self.is_active})>"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "workflow_id": self.workflow_id,
            "n8n_workflow_id": self.n8n_workflow_id,
            "workflow_name": self.workflow_name,
            "description": self.description,
            "category": self.category,
            "version": self.version,
            "workflow_definition": self.workflow_definition,
            "node_configuration": self.node_configuration,
            "connection_mapping": self.connection_mapping,
            "source_pattern_hash": self.source_pattern_hash,
            "generation_method": self.generation_method,
            "generation_confidence": self.generation_confidence,
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "failed_executions": self.failed_executions,
            "average_execution_time": self.average_execution_time,
            "efficiency_score": self.efficiency_score,
            "user_satisfaction_score": self.user_satisfaction_score,
            "time_savings_ratio": self.time_savings_ratio,
            "is_active": self.is_active,
            "is_validated": self.is_validated,
            "is_optimized": self.is_optimized,
            "generated_at": (
                self.generated_at.isoformat() if self.generated_at else None
            ),
            "first_execution": (
                self.first_execution.isoformat()
                if self.first_execution else None
            ),
            "last_execution": (
                self.last_execution.isoformat()
                if self.last_execution else None
            ),
            "last_optimization": (
                self.last_optimization.isoformat()
                if self.last_optimization else None
            ),
            "user_id": self.user_id,
            "pattern_id": self.pattern_id,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdaptiveWorkflow":
        """Create instance from dictionary."""
        return cls(
            workflow_id=data["workflow_id"],
            n8n_workflow_id=data.get("n8n_workflow_id"),
            workflow_name=data["workflow_name"],
            description=data.get("description"),
            category=data["category"],
            version=data.get("version", "1.0.0"),
            workflow_definition=data["workflow_definition"],
            node_configuration=data["node_configuration"],
            connection_mapping=data["connection_mapping"],
            source_pattern_hash=data["source_pattern_hash"],
            generation_method=data.get("generation_method", "pattern_based"),
            generation_confidence=data.get("generation_confidence", 0.0),
            total_executions=data.get("total_executions", 0),
            successful_executions=data.get("successful_executions", 0),
            failed_executions=data.get("failed_executions", 0),
            average_execution_time=data.get("average_execution_time", 0.0),
            efficiency_score=data.get("efficiency_score", 0.0),
            user_satisfaction_score=data.get("user_satisfaction_score", 0.0),
            time_savings_ratio=data.get("time_savings_ratio", 0.0),
            is_active=data.get("is_active", True),
            is_validated=data.get("is_validated", False),
            is_optimized=data.get("is_optimized", False),
            user_id=data["user_id"],
            pattern_id=data["pattern_id"]
        )

    def record_execution(
        self,
        success: bool,
        execution_time: float,
        error_message: str = None
    ) -> None:
        """Record a workflow execution result."""
        self.total_executions += 1

        if success:
            self.successful_executions += 1
        else:
            self.failed_executions += 1

        # Update average execution time
        if self.total_executions == 1:
            self.average_execution_time = execution_time
        else:
            current_total = (
                self.average_execution_time * (self.total_executions - 1)
            )
            self.average_execution_time = (
                current_total + execution_time
            ) / self.total_executions

        # Update timestamps
        if not self.first_execution:
            self.first_execution = datetime.utcnow()
        self.last_execution = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def calculate_success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_executions == 0:
            return 0.0
        return (self.successful_executions / self.total_executions) * 100

    def calculate_efficiency_score(self, baseline_time: float = None) -> float:
        """Calculate efficiency score based on execution performance."""
        if not baseline_time or self.average_execution_time == 0:
            return 0.0

        # Efficiency = (baseline_time - avg_time) / baseline_time
        efficiency = (
            (baseline_time - self.average_execution_time) / baseline_time
        )
        self.efficiency_score = max(0.0, min(1.0, efficiency))
        return self.efficiency_score

    def update_user_satisfaction(
        self, satisfaction_scores: List[float]
    ) -> None:
        """Update user satisfaction score from feedback."""
        if satisfaction_scores:
            self.user_satisfaction_score = sum(satisfaction_scores) / len(
                satisfaction_scores
            )
            self.updated_at = datetime.utcnow()

    def calculate_time_savings(self, manual_time: float) -> float:
        """Calculate time savings ratio compared to manual execution."""
        if manual_time == 0 or self.average_execution_time == 0:
            return 0.0

        savings = (manual_time - self.average_execution_time) / manual_time
        self.time_savings_ratio = max(0.0, min(1.0, savings))
        return self.time_savings_ratio

    def is_performing_well(self) -> bool:
        """Check if workflow is performing within acceptable parameters."""
        return (
            self.calculate_success_rate() >= 85.0 and  # 85% success rate
            self.efficiency_score >= 0.3 and  # 30% efficiency improvement
            self.user_satisfaction_score >= 3.5  # 3.5/5 satisfaction
        )

    def needs_optimization(self) -> bool:
        """Check if workflow needs optimization."""
        return (
            self.total_executions >= 10 and
            (
                self.calculate_success_rate() < 85.0 or
                self.efficiency_score < 0.3 or
                self.user_satisfaction_score < 3.5
            ) and
            not self.is_optimized
        )

    def mark_optimized(self) -> None:
        """Mark workflow as optimized."""
        self.is_optimized = True
        self.last_optimization = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def deactivate(self, reason: str = None) -> None:
        """Deactivate workflow (stop automatic execution)."""
        self.is_active = False
        # TODO: Store deactivation reason if needed
        self.updated_at = datetime.utcnow()

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        return {
            "success_rate": self.calculate_success_rate(),
            "total_executions": self.total_executions,
            "average_execution_time": self.average_execution_time,
            "efficiency_score": self.efficiency_score,
            "user_satisfaction_score": self.user_satisfaction_score,
            "time_savings_ratio": self.time_savings_ratio,
            "is_performing_well": self.is_performing_well(),
            "needs_optimization": self.needs_optimization(),
            "days_active": (
                (datetime.utcnow() - self.generated_at).days
                if self.generated_at else 0
            )
        }
