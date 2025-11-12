"""
Base entity models for the Productivity Domain.

Provides data models for all 8 productivity tools with unified schema
and executive function accommodation tracking.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ProductivityToolStatus(str, Enum):
    """Status enumeration for productivity tools."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SYNCING = "syncing"
    ERROR = "error"


class ProductivityTool(Base):
    """Base model for productivity tool configuration."""

    __tablename__ = "productivity_tools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tool_name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default=ProductivityToolStatus.ACTIVE)
    config_data = Column(JSON, default={})
    sync_status = Column(String(50), default="synced")
    last_sync = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class WorkflowState(Base):
    """Cross-tool workflow state management."""

    __tablename__ = "workflow_states"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    workflow_id = Column(String(255), nullable=False, unique=True)
    user_id = Column(String(100), nullable=False)
    current_step = Column(Integer, default=0)
    tools_involved = Column(JSON, default=[])
    state_data = Column(JSON, nullable=False)
    # Executive function context preservation
    context_data = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class UserTaskData(Base):
    """Unified task and activity data across productivity tools."""

    __tablename__ = "user_task_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String(100), nullable=False)
    source_tool = Column(String(100), nullable=False)
    task_type = Column(String(100), nullable=False)
    task_data = Column(JSON, nullable=False)
    priority = Column(String(20), default="medium")
    status = Column(String(50), default="active")
    due_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# Pydantic models for API serialization
class ProductivityToolModel(BaseModel):
    """Pydantic model for productivity tools."""

    id: Optional[str] = None
    tool_name: str
    display_name: str
    description: Optional[str] = None
    status: ProductivityToolStatus = ProductivityToolStatus.ACTIVE
    config_data: dict[str, Any] = Field(default_factory=dict)
    sync_status: str = "synced"
    last_sync: Optional[datetime] = None
    response_time_ms: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WorkflowStateModel(BaseModel):
    """Pydantic model for workflow states."""

    id: Optional[str] = None
    workflow_id: str
    user_id: str
    current_step: int = 0
    tools_involved: list[str] = Field(default_factory=list)
    state_data: dict[str, Any]
    context_data: dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserTaskDataModel(BaseModel):
    """Pydantic model for user task data."""

    id: Optional[str] = None
    user_id: str
    source_tool: str
    task_type: str
    task_data: dict[str, Any]
    priority: str = "medium"
    status: str = "active"
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Tool-specific models for the 8 productivity tools
class N8nWorkflowModel(BaseModel):
    """n8n workflow automation model."""

    workflow_id: str
    name: str
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    connections: dict[str, Any] = Field(default_factory=dict)
    active: bool = True
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MealieRecipeModel(BaseModel):
    """Mealie recipe management model."""

    recipe_id: str
    name: str
    description: Optional[str] = None
    ingredients: list[dict[str, Any]] = Field(default_factory=list)
    instructions: list[dict[str, Any]] = Field(default_factory=list)
    nutrition: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    rating: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DispatchIncidentModel(BaseModel):
    """Dispatch incident management model."""

    incident_id: str
    title: str
    description: str
    status: str  # active, stable, closed
    priority: str  # low, medium, high, critical
    incident_type: str
    assigned_individuals: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ActualBudgetModel(BaseModel):
    """Actual Budget financial tracking model."""

    budget_id: str
    name: str
    accounts: list[dict[str, Any]] = Field(default_factory=list)
    categories: list[dict[str, Any]] = Field(default_factory=list)
    transactions: list[dict[str, Any]] = Field(default_factory=list)
    current_balance: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FirecrawlJobModel(BaseModel):
    """Firecrawl web scraping job model."""

    job_id: str
    url: str
    crawl_options: dict[str, Any] = Field(default_factory=dict)
    status: str  # pending, running, completed, failed
    results: list[dict[str, Any]] = Field(default_factory=list)
    pages_crawled: int = 0
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GooseSessionModel(BaseModel):
    """Goose AI coding assistant session model."""

    session_id: str
    project_path: str
    conversation: list[dict[str, Any]] = Field(default_factory=list)
    files_modified: list[str] = Field(default_factory=list)
    status: str  # active, paused, completed
    created_at: datetime
    last_activity: datetime

    class Config:
        from_attributes = True


class ITToolsOperationModel(BaseModel):
    """IT-Tools utility operation model."""

    operation_id: str
    tool_name: str
    operation_type: str
    input_data: dict[str, Any]
    output_data: dict[str, Any] = Field(default_factory=dict)
    status: str  # pending, completed, failed
    execution_time_ms: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class InspectorAnalysisModel(BaseModel):
    """Inspector code analysis model."""

    analysis_id: str
    project_path: str
    language: str
    files_analyzed: list[str] = Field(default_factory=list)
    issues_found: list[dict[str, Any]] = Field(default_factory=list)
    metrics: dict[str, Any] = Field(default_factory=dict)
    status: str  # analyzing, completed, failed
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Executive function accommodation models
class ProductivityUserPreferences(BaseModel):
    """Productivity domain user preferences for executive function support."""

    user_id: str
    task_aggregation: bool = True  # Reduce context switching
    priority_system: list[str] = Field(
        default_factory=lambda: ["urgent", "high", "medium", "low"]
    )
    notification_schedule: dict[str, Any] = Field(default_factory=dict)
    dashboard_widgets: list[str] = Field(default_factory=list)
    workflow_templates: dict[str, Any] = Field(default_factory=dict)
    adhd_accommodations: dict[str, Any] = Field(default_factory=dict)
    autism_accommodations: dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


# Domain performance tracking
class ProductivityPerformanceMetric(BaseModel):
    """Performance metrics for productivity domain constitutional compliance."""

    tool_name: str
    operation: str
    response_time_ms: int
    target_time_ms: int = 2000  # <2s constitutional requirement
    compliant: bool
    timestamp: datetime
    user_id: Optional[str] = None
    context_switches: int = 0  # Track context switching reduction

    class Config:
        from_attributes = True
