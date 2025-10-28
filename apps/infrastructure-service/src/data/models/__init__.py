"""
Base entity models for the Infrastructure Domain.

Provides data models for all 12 infrastructure tools with unified schema
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


class InfrastructureToolStatus(str, Enum):
    """Status enumeration for infrastructure tools."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class InfrastructureTool(Base):
    """Base model for infrastructure tool configuration."""

    __tablename__ = "infrastructure_tools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tool_name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default=InfrastructureToolStatus.ACTIVE)
    config_data = Column(JSON, default={})
    health_status = Column(String(50), default="healthy")
    last_health_check = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class ServiceConfiguration(Base):
    """Infrastructure service configuration management."""

    __tablename__ = "service_configurations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    service_name = Column(String(100), nullable=False)
    config_version = Column(String(50), nullable=False)
    config_data = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    environment = Column(String(50), default="production")
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    applied_at = Column(DateTime, nullable=True)


class MCPServer(Base):
    """Model Context Protocol server management."""

    __tablename__ = "mcp_servers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    server_name = Column(String(100), nullable=False, unique=True)
    server_type = Column(String(50), nullable=False)  # chroma, firecrawl, etc.
    endpoint_url = Column(String(500), nullable=False)
    capabilities = Column(JSON, default=[])
    status = Column(String(20), default="running")
    last_ping = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# Pydantic models for API serialization
class InfrastructureToolModel(BaseModel):
    """Pydantic model for infrastructure tools."""

    id: Optional[str] = None
    tool_name: str
    display_name: str
    description: Optional[str] = None
    status: InfrastructureToolStatus = InfrastructureToolStatus.ACTIVE
    config_data: dict[str, Any] = Field(default_factory=dict)
    health_status: str = "healthy"
    last_health_check: Optional[datetime] = None
    response_time_ms: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ServiceConfigurationModel(BaseModel):
    """Pydantic model for service configurations."""

    id: Optional[str] = None
    service_name: str
    config_version: str
    config_data: dict[str, Any]
    is_active: bool = True
    environment: str = "production"
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    applied_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MCPServerModel(BaseModel):
    """Pydantic model for MCP servers."""

    id: Optional[str] = None
    server_name: str
    server_type: str
    endpoint_url: str
    capabilities: list[str] = Field(default_factory=list)
    status: str = "running"
    last_ping: Optional[datetime] = None
    response_time_ms: int = 0
    error_count: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Tool-specific models for the 12 infrastructure tools
class KongServiceModel(BaseModel):
    """Kong API Gateway service model."""

    service_id: str
    name: str
    protocol: str = "http"
    host: str
    port: int = 80
    path: Optional[str] = None
    retries: int = 5
    connect_timeout: int = 60000
    write_timeout: int = 60000
    read_timeout: int = 60000
    tags: list[str] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class GhostwriterProjectModel(BaseModel):
    """Ghostwriter project management model."""

    project_id: str
    name: str
    description: str
    start_date: datetime
    end_date: Optional[datetime] = None
    client: str
    project_type: str
    status: str = "active"
    team_members: list[str] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class KasmVNCSessionModel(BaseModel):
    """KasmVNC remote desktop session model."""

    session_id: str
    user_id: str
    desktop_type: str
    status: str = "active"  # active, stopped, paused
    connection_info: dict[str, Any] = Field(default_factory=dict)
    resource_usage: dict[str, Any] = Field(default_factory=dict)
    started_at: datetime
    last_activity: datetime

    class Config:
        from_attributes = True


class ChromaMCPCollectionModel(BaseModel):
    """Chroma MCP vector database collection model."""

    collection_id: str
    collection_name: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    embedding_function: str
    document_count: int = 0
    created_at: datetime
    last_updated: datetime

    class Config:
        from_attributes = True


class FileScopeMCPAnalysisModel(BaseModel):
    """FileScope MCP file analysis model."""

    analysis_id: str
    file_path: str
    file_type: str
    analysis_results: dict[str, Any] = Field(default_factory=dict)
    threat_indicators: list[dict[str, Any]] = Field(default_factory=list)
    status: str = "completed"
    created_at: datetime

    class Config:
        from_attributes = True


class FirecrawlMCPJobModel(BaseModel):
    """Firecrawl MCP web scraping job model."""

    job_id: str
    url: str
    crawl_options: dict[str, Any] = Field(default_factory=dict)
    status: str = "pending"
    results: list[dict[str, Any]] = Field(default_factory=list)
    pages_crawled: int = 0
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class N8nMCPWorkflowModel(BaseModel):
    """n8n MCP workflow integration model."""

    workflow_id: str
    name: str
    nodes: list[dict[str, Any]] = Field(default_factory=list)
    active: bool = True
    mcp_integrations: list[str] = Field(default_factory=list)
    execution_count: int = 0
    last_execution: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MalwareBazaarMCPSampleModel(BaseModel):
    """MalwareBazaar MCP malware sample model."""

    sample_id: str
    sha256_hash: str
    file_type: str
    file_size: int
    first_seen: datetime
    last_seen: datetime
    signature: Optional[str] = None
    family: Optional[str] = None
    tags: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


class MCPVirusTotalReportModel(BaseModel):
    """MCP VirusTotal integration report model."""

    report_id: str
    resource_hash: str
    scan_results: dict[str, Any] = Field(default_factory=dict)
    positives: int = 0
    total: int = 0
    scan_date: datetime
    permalink: str

    class Config:
        from_attributes = True


class OneXExploitModel(BaseModel):
    """OneX exploit framework model."""

    exploit_id: str
    name: str
    description: str
    target_platform: str
    severity: str = "medium"
    exploit_data: dict[str, Any] = Field(default_factory=dict)
    success_rate: float = 0.0
    created_at: datetime
    last_used: Optional[datetime] = None

    class Config:
        from_attributes = True


class HexStrikeAIAnalysisModel(BaseModel):
    """HexStrike AI analysis model."""

    analysis_id: str
    input_data: dict[str, Any]
    analysis_type: str
    ai_results: dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = 0.0
    processing_time_ms: int = 0
    status: str = "completed"
    created_at: datetime

    class Config:
        from_attributes = True


class BlackArchToolModel(BaseModel):
    """BlackArch penetration testing tool model."""

    tool_id: str
    tool_name: str
    category: str
    description: str
    version: str
    install_status: str = "available"
    usage_count: int = 0
    last_used: Optional[datetime] = None

    class Config:
        from_attributes = True


# Executive function accommodation models
class InfrastructureUserPreferences(BaseModel):
    """Infrastructure domain preferences for executive function support."""

    user_id: str
    monitoring_dashboard: dict[str, Any] = Field(default_factory=dict)
    alert_thresholds: dict[str, Any] = Field(default_factory=dict)
    service_priorities: list[str] = Field(default_factory=list)
    notification_settings: dict[str, bool] = Field(default_factory=dict)
    automation_preferences: dict[str, Any] = Field(default_factory=dict)
    adhd_accommodations: dict[str, Any] = Field(default_factory=dict)
    autism_accommodations: dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


# Domain performance tracking
class InfrastructurePerformanceMetric(BaseModel):
    """Performance metrics for infrastructure constitutional compliance."""

    tool_name: str
    operation: str
    response_time_ms: int
    target_time_ms: int = 5000  # <5s constitutional requirement
    compliant: bool
    timestamp: datetime
    user_id: Optional[str] = None
    resource_usage: dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True
