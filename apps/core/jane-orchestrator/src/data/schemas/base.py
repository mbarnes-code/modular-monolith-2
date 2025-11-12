"""
Base data mapping schemas and types.

Contains core schema definitions used across all domain mappings.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class DomainType(str, Enum):
    """Domain type enumeration."""

    SECURITY = "security"
    PRODUCTIVITY = "productivity"
    MTG = "mtg"
    INFRASTRUCTURE = "infrastructure"


class DataType(str, Enum):
    """Data type enumeration for cross-tool mapping."""

    # Security domain data types
    THREAT_INTELLIGENCE = "threat_intelligence"
    SECURITY_EVENT = "security_event"
    VULNERABILITY = "vulnerability"
    MALWARE_SAMPLE = "malware_sample"
    IOC = "ioc"  # Indicator of Compromise
    YARA_RULE = "yara_rule"

    # Productivity domain data types
    TASK = "task"
    RECIPE = "recipe"
    BUDGET_ENTRY = "budget_entry"
    DISPATCH_INCIDENT = "dispatch_incident"
    WORKFLOW = "workflow"
    DOCUMENT = "document"

    # MTG domain data types
    CARD = "card"
    DECK = "deck"
    COMBO = "combo"
    COMMANDER = "commander"

    # Infrastructure domain data types
    SERVICE_CONFIG = "service_config"
    API_ROUTE = "api_route"
    CONTAINER = "container"
    WORKFLOW_TEMPLATE = "workflow_template"
    MONITORING_ALERT = "monitoring_alert"
    LOG_ENTRY = "log_entry"


class MappingRuleType(str, Enum):
    """Mapping rule type enumeration."""

    DIRECT = "direct"  # Direct field mapping
    TRANSFORM = "transform"  # Transform with function
    AGGREGATE = "aggregate"  # Aggregate multiple fields
    LOOKUP = "lookup"  # Lookup from reference data
    CONDITIONAL = "conditional"  # Conditional mapping
    CUSTOM = "custom"  # Custom transformation logic


class FieldMapping(BaseModel):
    """Individual field mapping configuration."""

    source_field: str = Field(..., description="Source field path")
    target_field: str = Field(..., description="Target field path")
    mapping_type: MappingRuleType = Field(
        default=MappingRuleType.DIRECT, description="Type of mapping rule"
    )
    transform_function: Optional[str] = Field(
        None, description="Transformation function name"
    )
    default_value: Optional[Any] = Field(
        None, description="Default value if source is null/empty"
    )
    required: bool = Field(
        default=False, description="Whether field is required")
    validation_rules: Optional[Dict[str, Any]] = Field(
        None, description="Field validation rules"
    )
    conditions: Optional[Dict[str, Any]] = Field(
        None, description="Conditional mapping rules"
    )


class DataMappingSchema(BaseModel):
    """Complete data mapping schema between two tools."""

    schema_id: str = Field(..., description="Unique schema identifier")
    schema_name: str = Field(..., description="Human-readable schema name")
    description: Optional[str] = Field(None, description="Schema description")

    # Source and target configuration
    source_tool: str = Field(..., description="Source tool identifier")
    source_domain: DomainType = Field(..., description="Source domain")
    source_data_type: DataType = Field(..., description="Source data type")

    target_tool: str = Field(..., description="Target tool identifier")
    target_domain: DomainType = Field(..., description="Target domain")
    target_data_type: DataType = Field(..., description="Target data type")

    # Bidirectional mapping support
    bidirectional: bool = Field(
        default=False, description="Supports reverse mapping")

    # Field mappings
    field_mappings: List[FieldMapping] = Field(
        ..., description="List of field mappings"
    )

    # Schema metadata
    version: str = Field(default="1.0.0", description="Schema version")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = Field(None, description="Schema creator")

    # Validation and constraints
    validation_schema: Optional[Dict[str, Any]] = Field(
        None, description="JSON schema for validation"
    )
    constraints: Optional[Dict[str, Any]] = Field(
        None, description="Business rule constraints"
    )

    # Performance and caching
    cache_ttl_seconds: int = Field(
        default=300, description="Cache TTL for transformed data"
    )
    batch_size: int = Field(default=100, description="Optimal batch size")

    @validator("schema_id")
    def validate_schema_id(cls, v: str) -> str:
        """Validate schema ID format."""
        if not v or len(v) < 3:
            raise ValueError("Schema ID must be at least 3 characters")
        return v.lower().replace(" ", "_")
