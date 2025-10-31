"""
UserRequest model for tracking LLM interactions in n8n adaptive workflows.

This model tracks all user requests to identify patterns that can be
automated through workflow generation.
"""

from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.orm import relationship

from .base_model import BaseModel


class UserRequest(BaseModel):
    """
    Model for tracking user requests and LLM interactions.

    Used by PatternDetectionService to analyze user behavior patterns
    and identify opportunities for workflow automation.
    """

    __tablename__ = "user_requests"

    # Request identification
    request_id: str = Column(
        String(255), unique=True, nullable=False, index=True
    )
    session_id: str = Column(String(255), nullable=False, index=True)

    # Request content
    user_input: str = Column(Text, nullable=False)
    intent_category: str = Column(String(100), nullable=True)  # classified
    tool_targets: List[str] = Column(JSON, nullable=True)  # tools mentioned

    # LLM response
    llm_response: str = Column(Text, nullable=True)
    response_type: str = Column(String(50), nullable=False)  # info/action

    # Execution details
    actions_taken: List[Dict[str, Any]] = Column(JSON, nullable=True)
    tools_used: List[str] = Column(JSON, nullable=True)
    execution_success: bool = Column(Boolean, default=True)
    execution_duration: float = Column(JSON, nullable=True)  # seconds

    # Context and metadata
    domain_context: str = Column(String(100), nullable=True)  # security, etc.
    user_context: Dict[str, Any] = Column(JSON, nullable=True)
    previous_request_id: str = Column(String(255), nullable=True)  # chaining

    # Pattern analysis
    pattern_hash: str = Column(String(64), nullable=True, index=True)
    is_part_of_pattern: bool = Column(Boolean, default=False)
    pattern_confidence: float = Column(JSON, default=0.0)

    # User feedback
    user_satisfaction: int = Column(Integer, nullable=True)  # 1-5 rating
    feedback_text: str = Column(Text, nullable=True)
    would_automate: bool = Column(Boolean, nullable=True)

    # Request timing
    request_timestamp: datetime = Column(DateTime, default=datetime.utcnow)
    response_timestamp: datetime = Column(DateTime, nullable=True)

    # User identification
    user_id: str = Column(String(255), nullable=False, index=True)

    # Relationships
    workflow_pattern_id: str = Column(
        String(255), ForeignKey("workflow_patterns.id"), nullable=True
    )
    workflow_pattern = relationship(
        "WorkflowPattern", back_populates="user_requests"
    )

    def __repr__(self) -> str:
        return (
            f"<UserRequest(id='{self.request_id}', "
            f"intent='{self.intent_category}', "
            f"pattern='{self.is_part_of_pattern}')>"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "request_id": self.request_id,
            "session_id": self.session_id,
            "user_input": self.user_input,
            "intent_category": self.intent_category,
            "tool_targets": self.tool_targets,
            "llm_response": self.llm_response,
            "response_type": self.response_type,
            "actions_taken": self.actions_taken,
            "tools_used": self.tools_used,
            "execution_success": self.execution_success,
            "execution_duration": self.execution_duration,
            "domain_context": self.domain_context,
            "user_context": self.user_context,
            "previous_request_id": self.previous_request_id,
            "pattern_hash": self.pattern_hash,
            "is_part_of_pattern": self.is_part_of_pattern,
            "pattern_confidence": self.pattern_confidence,
            "user_satisfaction": self.user_satisfaction,
            "feedback_text": self.feedback_text,
            "would_automate": self.would_automate,
            "request_timestamp": (
                self.request_timestamp.isoformat()
                if self.request_timestamp else None
            ),
            "response_timestamp": (
                self.response_timestamp.isoformat()
                if self.response_timestamp else None
            ),
            "user_id": self.user_id,
            "workflow_pattern_id": self.workflow_pattern_id,
            "created_at": (
                self.created_at.isoformat() if self.created_at else None
            ),
            "updated_at": (
                self.updated_at.isoformat() if self.updated_at else None
            )
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserRequest":
        """Create instance from dictionary."""
        return cls(
            request_id=data["request_id"],
            session_id=data["session_id"],
            user_input=data["user_input"],
            intent_category=data.get("intent_category"),
            tool_targets=data.get("tool_targets"),
            llm_response=data.get("llm_response"),
            response_type=data["response_type"],
            actions_taken=data.get("actions_taken"),
            tools_used=data.get("tools_used"),
            execution_success=data.get("execution_success", True),
            execution_duration=data.get("execution_duration"),
            domain_context=data.get("domain_context"),
            user_context=data.get("user_context"),
            previous_request_id=data.get("previous_request_id"),
            pattern_hash=data.get("pattern_hash"),
            is_part_of_pattern=data.get("is_part_of_pattern", False),
            pattern_confidence=data.get("pattern_confidence", 0.0),
            user_satisfaction=data.get("user_satisfaction"),
            feedback_text=data.get("feedback_text"),
            would_automate=data.get("would_automate"),
            user_id=data["user_id"],
            workflow_pattern_id=data.get("workflow_pattern_id")
        )

    def set_response(self, response: str, response_type: str) -> None:
        """Set LLM response and timestamp."""
        self.llm_response = response
        self.response_type = response_type
        self.response_timestamp = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_execution_details(
        self,
        actions: List[Dict[str, Any]],
        tools: List[str],
        success: bool,
        duration: float
    ) -> None:
        """Add execution details after request completion."""
        self.actions_taken = actions
        self.tools_used = tools
        self.execution_success = success
        self.execution_duration = duration
        self.updated_at = datetime.utcnow()

    def set_pattern_association(
        self,
        pattern_hash: str,
        confidence: float
    ) -> None:
        """Associate request with a detected pattern."""
        self.pattern_hash = pattern_hash
        self.is_part_of_pattern = True
        self.pattern_confidence = confidence
        self.updated_at = datetime.utcnow()

    def add_user_feedback(
        self,
        satisfaction: int,
        feedback: str = None,
        would_automate: bool = None
    ) -> None:
        """Add user feedback for the request."""
        self.user_satisfaction = satisfaction
        self.feedback_text = feedback
        self.would_automate = would_automate
        self.updated_at = datetime.utcnow()

    def is_automatable_intent(self) -> bool:
        """Check if request represents an automatable intent."""
        automatable_intents = [
            "data_transfer", "workflow_execution", "batch_operation",
            "scheduled_task", "conditional_action", "integration_request"
        ]
        return (
            self.intent_category in automatable_intents and
            self.execution_success and
            len(self.tools_used or []) > 1  # Multi-tool operations
        )

    def get_pattern_features(self) -> Dict[str, Any]:
        """Extract features for pattern detection."""
        return {
            "intent_category": self.intent_category,
            "tool_targets": self.tool_targets or [],
            "tools_used": self.tools_used or [],
            "domain_context": self.domain_context,
            "execution_duration": self.execution_duration,
            "action_count": len(self.actions_taken or []),
            "success": self.execution_success,
            "user_satisfaction": self.user_satisfaction or 0
        }

    def calculate_automation_value(self) -> float:
        """Calculate potential value of automating this request type."""
        base_value = 0.0

        # Time savings factor
        if self.execution_duration:
            base_value += min(self.execution_duration /
                              60, 10)  # Max 10 for 1min+

        # Complexity factor (more tools = higher value)
        tool_count = len(self.tools_used or [])
        base_value += min(tool_count * 2, 10)

        # User satisfaction factor
        if self.user_satisfaction:
            base_value += self.user_satisfaction

        # Success factor
        if self.execution_success:
            base_value += 2

        return min(base_value, 25.0)  # Cap at 25 for normalization
