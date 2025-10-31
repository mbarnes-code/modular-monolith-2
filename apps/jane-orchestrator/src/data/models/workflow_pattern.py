"""
WorkflowPattern model for pattern detection in n8n adaptive workflow system.

This model tracks user interaction patterns to automatically generate
optimized n8n workflows based on detected repetitive behaviors.
"""

from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class WorkflowPattern(BaseModel):
    """
    Model for tracking workflow patterns detected from user behavior.

    Used by PatternDetectionService to identify recurring workflows
    that can be automated through n8n workflow generation.
    """

    __tablename__ = "workflow_patterns"

    # Pattern identification
    pattern_hash: str = Column(
        String(64), unique=True, nullable=False, index=True
    )
    pattern_name: str = Column(String(255), nullable=False)

    # Pattern metadata
    description: str = Column(Text, nullable=True)
    category: str = Column(String(100), nullable=False)  # domain category
    complexity_score: int = Column(Integer, default=1)  # 1-10 complexity

    # Pattern detection criteria
    trigger_sequence: Dict[str, Any] = Column(
        JSON, nullable=False
    )  # sequence of actions
    tool_sequence: List[str] = Column(
        JSON, nullable=False
    )  # ordered list of tools used
    data_flow: Dict[str, Any] = Column(
        JSON, nullable=True
    )  # data transformation pattern
    timing_pattern: Dict[str, Any] = Column(
        JSON, nullable=True
    )  # timing requirements

    # Pattern statistics
    occurrence_count: int = Column(Integer, default=1)
    first_detected: datetime = Column(DateTime, default=datetime.utcnow)
    last_seen: datetime = Column(DateTime, default=datetime.utcnow)
    confidence_score: float = Column(JSON, default=0.0)  # 0.0-1.0 confidence

    # Pattern validation
    success_rate: float = Column(JSON, default=0.0)  # when automated
    user_feedback_score: float = Column(JSON, default=0.0)  # user rating
    is_validated: bool = Column(Boolean, default=False)

    # Workflow generation status
    workflow_generated: bool = Column(Boolean, default=False)
    n8n_workflow_id: str = Column(String(255), nullable=True)
    generation_timestamp: datetime = Column(DateTime, nullable=True)

    # User context
    user_id: str = Column(String(255), nullable=False, index=True)

    # Relationships
    user_requests = relationship(
        "UserRequest", back_populates="workflow_pattern"
    )
    adaptive_workflows = relationship(
        "AdaptiveWorkflow", back_populates="pattern"
    )

    def __repr__(self) -> str:
        return (
            f"<WorkflowPattern(name='{self.pattern_name}', "
            f"hash='{self.pattern_hash}', count={self.occurrence_count})>"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "pattern_hash": self.pattern_hash,
            "pattern_name": self.pattern_name,
            "description": self.description,
            "category": self.category,
            "complexity_score": self.complexity_score,
            "trigger_sequence": self.trigger_sequence,
            "tool_sequence": self.tool_sequence,
            "data_flow": self.data_flow,
            "timing_pattern": self.timing_pattern,
            "occurrence_count": self.occurrence_count,
            "first_detected": (
                self.first_detected.isoformat() if self.first_detected else None
            ),
            "last_seen": (
                self.last_seen.isoformat() if self.last_seen else None
            ),
            "confidence_score": self.confidence_score,
            "success_rate": self.success_rate,
            "user_feedback_score": self.user_feedback_score,
            "is_validated": self.is_validated,
            "workflow_generated": self.workflow_generated,
            "n8n_workflow_id": self.n8n_workflow_id,
            "generation_timestamp": (
                self.generation_timestamp.isoformat()
                if self.generation_timestamp else None
            ),
            "user_id": self.user_id,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkflowPattern":
        """Create instance from dictionary."""
        return cls(
            pattern_hash=data["pattern_hash"],
            pattern_name=data["pattern_name"],
            description=data.get("description"),
            category=data["category"],
            complexity_score=data.get("complexity_score", 1),
            trigger_sequence=data["trigger_sequence"],
            tool_sequence=data["tool_sequence"],
            data_flow=data.get("data_flow"),
            timing_pattern=data.get("timing_pattern"),
            occurrence_count=data.get("occurrence_count", 1),
            confidence_score=data.get("confidence_score", 0.0),
            success_rate=data.get("success_rate", 0.0),
            user_feedback_score=data.get("user_feedback_score", 0.0),
            is_validated=data.get("is_validated", False),
            workflow_generated=data.get("workflow_generated", False),
            n8n_workflow_id=data.get("n8n_workflow_id"),
            user_id=data["user_id"]
        )

    def update_occurrence(self) -> None:
        """Update occurrence count and last seen timestamp."""
        self.occurrence_count += 1
        self.last_seen = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def calculate_confidence(self) -> float:
        """Calculate confidence score based on occurrences and validation."""
        # Max 0.8 from occurrences
        base_confidence = min(self.occurrence_count / 10.0, 0.8)
        validation_bonus = 0.2 if self.is_validated else 0.0
        feedback_bonus = self.user_feedback_score * 0.1

        total_confidence = base_confidence + validation_bonus + feedback_bonus
        self.confidence_score = min(total_confidence, 1.0)
        return self.confidence_score

    def is_ready_for_automation(self) -> bool:
        """Check if pattern is ready for n8n workflow generation."""
        return (
            # Constitutional requirement: 3+ occurrences
            self.occurrence_count >= 3 and
            self.confidence_score >= 0.7 and
            not self.workflow_generated
        )

    def get_automation_priority(self) -> int:
        """Get priority score for workflow generation (1-10, higher)."""
        priority = 0

        # Frequency factor (40% of priority)
        frequency_score = min(self.occurrence_count / 5, 4)
        priority += frequency_score

        # Confidence factor (30% of priority)
        confidence_score = self.confidence_score * 3
        priority += confidence_score

        # User feedback factor (20% of priority)
        feedback_score = self.user_feedback_score * 2
        priority += feedback_score

        # Complexity factor (10% of priority) - simpler = higher priority
        complexity_score = (11 - self.complexity_score) / 10
        priority += complexity_score

        return min(int(priority), 10)
