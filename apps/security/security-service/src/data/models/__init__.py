"""
Base entity models for the Security Domain.

Provides data models for all 13 security tools with unified schema
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


class SecurityToolStatus(str, Enum):
    """Status enumeration for security tools."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class SecurityTool(Base):
    """Base model for security tool configuration and status."""

    __tablename__ = "security_tools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tool_name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default=SecurityToolStatus.ACTIVE)
    config_data = Column(JSON, default={})
    last_health_check = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)


class SecurityWorkflow(Base):
    """Security workflow orchestration model."""

    __tablename__ = "security_workflows"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    tools_involved = Column(JSON, default=[])  # List of tool names
    workflow_steps = Column(JSON, default=[])
    status = Column(String(50), default="active")
    progress = Column(Integer, default=0)  # 0-100
    created_by = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


class SecurityEvent(Base):
    """Security event tracking for SIEM integration."""

    __tablename__ = "security_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_type = Column(String(100), nullable=False)
    source_tool = Column(String(100), nullable=False)
    # low, medium, high, critical
    severity = Column(String(20), default="medium")
    event_data = Column(JSON, nullable=False)
    processed = Column(Boolean, default=False)
    analyst_notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)


class ThreatIntelligence(Base):
    """Threat intelligence data aggregation."""

    __tablename__ = "threat_intelligence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # ip, domain, hash, etc.
    indicator_type = Column(String(50), nullable=False)
    indicator_value = Column(String(500), nullable=False)
    threat_type = Column(String(100))
    confidence = Column(Integer, default=50)  # 0-100
    source_tools = Column(JSON, default=[])
    intelligence_data = Column(JSON, default={})
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow,
                          onupdate=datetime.utcnow)


# Pydantic models for API serialization
class SecurityToolModel(BaseModel):
    """Pydantic model for security tool data."""

    id: Optional[str] = None
    tool_name: str
    display_name: str
    description: Optional[str] = None
    status: SecurityToolStatus = SecurityToolStatus.ACTIVE
    config_data: dict[str, Any] = Field(default_factory=dict)
    last_health_check: Optional[datetime] = None
    response_time_ms: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SecurityWorkflowModel(BaseModel):
    """Pydantic model for security workflows."""

    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    tools_involved: list[str] = Field(default_factory=list)
    workflow_steps: list[dict[str, Any]] = Field(default_factory=list)
    status: str = "active"
    progress: int = 0
    created_by: Optional[str] = None
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SecurityEventModel(BaseModel):
    """Pydantic model for security events."""

    id: Optional[str] = None
    event_type: str
    source_tool: str
    severity: str = "medium"
    event_data: dict[str, Any]
    processed: bool = False
    analyst_notes: Optional[str] = None
    created_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ThreatIntelligenceModel(BaseModel):
    """Pydantic model for threat intelligence."""

    id: Optional[str] = None
    indicator_type: str
    indicator_value: str
    threat_type: Optional[str] = None
    confidence: int = 50
    source_tools: list[str] = Field(default_factory=list)
    intelligence_data: dict[str, Any] = Field(default_factory=dict)
    first_seen: Optional[datetime] = None
    last_updated: Optional[datetime] = None

    class Config:
        from_attributes = True


# Tool-specific models for the 13 security tools
class MispEventModel(BaseModel):
    """MISP threat intelligence platform events."""

    event_id: str
    info: str
    threat_level: int
    analysis: int
    attributes: list[dict[str, Any]] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime

    class Config:
        from_attributes = True


class HelkLogModel(BaseModel):
    """HELK (Hunting ELK) log analysis."""

    log_id: str
    log_level: str
    source: str
    message: str
    fields: dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime

    class Config:
        from_attributes = True


class SecurityOnionAlertModel(BaseModel):
    """Security Onion network security monitoring alerts."""

    alert_id: str
    signature: str
    classification: str
    priority: int
    source_ip: str
    dest_ip: str
    source_port: Optional[int] = None
    dest_port: Optional[int] = None
    protocol: str
    timestamp: datetime

    class Config:
        from_attributes = True


class MaltrailDetectionModel(BaseModel):
    """Maltrail malicious traffic detection."""

    detection_id: str
    trail: str
    info: str
    reference: str
    level: str  # low, medium, high
    tags: list[str] = Field(default_factory=list)
    first_seen: datetime
    last_seen: datetime

    class Config:
        from_attributes = True


class YaraXRuleModel(BaseModel):
    """YARA-X malware detection rules."""

    rule_id: str
    rule_name: str
    rule_content: str
    tags: list[str] = Field(default_factory=list)
    meta: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CyberChefRecipeModel(BaseModel):
    """CyberChef data transformation recipes."""

    recipe_id: str
    recipe_name: str
    operations: list[dict[str, Any]]
    input_data: str
    output_data: str
    created_at: datetime

    class Config:
        from_attributes = True


class NemesisCrackModel(BaseModel):
    """Nemesis password cracking results."""

    crack_id: str
    hash_type: str
    target_hash: str
    cracked_password: Optional[str] = None
    status: str  # pending, cracked, failed
    method: str
    started_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ApiScoutReportModel(BaseModel):
    """ApiScout API monitoring and reconnaissance."""

    report_id: str
    target_url: str
    api_endpoints: list[dict[str, Any]] = Field(default_factory=list)
    vulnerabilities: list[dict[str, Any]] = Field(default_factory=list)
    scan_status: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class BruteRatelSessionModel(BaseModel):
    """Brute Ratel C4 command and control sessions."""

    session_id: str
    target_host: str
    user_context: str
    implant_type: str
    callback_time: datetime
    status: str  # active, inactive, lost
    commands_executed: int = 0

    class Config:
        from_attributes = True


class MeterpreterSessionModel(BaseModel):
    """Metasploit Meterpreter session management."""

    session_id: str
    target_ip: str
    target_os: str
    user_context: str
    session_type: str
    established_at: datetime
    last_checkin: datetime
    status: str  # active, inactive, dead

    class Config:
        from_attributes = True


# Executive function accommodation models
class SecurityUserPreferences(BaseModel):
    """Security domain user preferences for executive function support."""

    user_id: str
    alert_aggregation: bool = True  # Reduce context switching
    priority_filtering: list[str] = Field(
        default_factory=lambda: ["high", "critical"])
    dashboard_layout: dict[str, Any] = Field(default_factory=dict)
    notification_settings: dict[str, bool] = Field(default_factory=dict)
    adhd_accommodations: dict[str, Any] = Field(default_factory=dict)
    autism_accommodations: dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


# Domain performance tracking
class SecurityPerformanceMetric(BaseModel):
    """Performance metrics for security domain constitutional compliance."""

    tool_name: str
    operation: str
    response_time_ms: int
    target_time_ms: int = 1000  # <1s constitutional requirement
    compliant: bool
    timestamp: datetime
    user_id: Optional[str] = None

    class Config:
        from_attributes = True
