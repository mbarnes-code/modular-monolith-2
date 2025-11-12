"""
Data mapping schemas for 37-tool integration across 4 domains.

This module provides Pydantic schemas for data transformation and mapping
between different tools across Security, Productivity, MTG, and Infrastructure domains.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

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
    """
    Individual field mapping configuration.
    """

    source_field: str = Field(...,
                              description="Source field path (dot notation)")
    target_field: str = Field(...,
                              description="Target field path (dot notation)")
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

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "source_field": "event.timestamp",
                "target_field": "created_at",
                "mapping_type": "transform",
                "transform_function": "iso_to_datetime",
                "required": True,
            }
        }


class DataMappingSchema(BaseModel):
    """
    Complete data mapping schema between two tools.
    """

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

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "schema_id": "misp_to_helk_events",
                "schema_name": "MISP Events to HELK",
                "source_tool": "misp",
                "source_domain": "security",
                "source_data_type": "security_event",
                "target_tool": "helk",
                "target_domain": "security",
                "target_data_type": "security_event",
                "field_mappings": [
                    {
                        "source_field": "Event.id",
                        "target_field": "event_id",
                        "mapping_type": "direct",
                        "required": True,
                    }
                ],
            }
        }

    @validator("schema_id")
    def validate_schema_id(cls, v: str) -> str:
        """Validate schema ID format."""
        if not v or len(v) < 3:
            raise ValueError("Schema ID must be at least 3 characters")
        return v.lower().replace(" ", "_")


class CrossDomainMapping(BaseModel):
    """
    Cross-domain data mapping configuration.
    """

    mapping_id: str = Field(..., description="Unique mapping identifier")
    name: str = Field(..., description="Mapping name")
    description: Optional[str] = Field(None, description="Mapping description")

    # Domain configuration
    source_domain: DomainType = Field(..., description="Source domain")
    target_domains: List[DomainType] = Field(
        ..., description="Target domains for mapping"
    )

    # Mapping schemas
    schemas: List[DataMappingSchema] = Field(
        ..., description="Individual tool mapping schemas"
    )

    # Cross-domain rules
    domain_rules: Optional[Dict[str, Any]] = Field(
        None, description="Cross-domain business rules"
    )
    conflict_resolution: Optional[Dict[str, str]] = Field(
        None, description="Conflict resolution strategies"
    )

    # Workflow context
    workflow_triggers: Optional[List[str]] = Field(
        None, description="Workflow events that trigger mapping"
    )
    dependencies: Optional[List[str]] = Field(
        None, description="Dependent mapping IDs"
    )

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "mapping_id": "security_to_productivity",
                "name": "Security to Productivity Mapping",
                "source_domain": "security",
                "target_domains": ["productivity"],
                "schemas": [],
            }
        }


class TransformationFunction(BaseModel):
    """
    Custom transformation function definition.
    """

    function_name: str = Field(..., description="Function name")
    description: str = Field(..., description="Function description")
    input_type: str = Field(..., description="Expected input type")
    output_type: str = Field(..., description="Output type")
    implementation: str = Field(...,
                                description="Function implementation code")
    dependencies: Optional[List[str]] = Field(
        None, description="Required libraries/modules"
    )

    # Testing and validation
    test_cases: Optional[List[Dict[str, Any]]] = Field(
        None, description="Test cases for function validation"
    )
    performance_benchmark: Optional[Dict[str, Any]] = Field(
        None, description="Performance benchmarking data"
    )

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "function_name": "iso_to_datetime",
                "description": "Convert ISO string to datetime object",
                "input_type": "str",
                "output_type": "datetime",
                "implementation": "datetime.fromisoformat(value)",
                "test_cases": [
                    {"input": "2023-01-01T00:00:00Z",
                        "expected": "datetime object"}
                ],
            }
        }


class MappingValidationResult(BaseModel):
    """
    Result of mapping validation operation.
    """

    is_valid: bool = Field(..., description="Whether mapping is valid")
    errors: List[str] = Field(default_factory=list,
                              description="Validation errors")
    warnings: List[str] = Field(
        default_factory=list, description="Validation warnings"
    )
    field_coverage: float = Field(
        ..., description="Percentage of fields successfully mapped"
    )
    performance_score: Optional[float] = Field(
        None, description="Performance score (0-100)"
    )

    # Detailed validation results
    field_results: Optional[Dict[str, Dict[str, Any]]] = Field(
        None, description="Per-field validation results"
    )
    schema_compatibility: Optional[Dict[str, bool]] = Field(
        None, description="Schema compatibility check results"
    )

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "is_valid": True,
                "errors": [],
                "warnings": ["Optional field 'description' not mapped"],
                "field_coverage": 95.5,
                "performance_score": 87.2,
            }
        }


class SyncConfiguration(BaseModel):
    """
    Synchronization configuration for tool integration.
    """

    config_id: str = Field(..., description="Configuration identifier")
    name: str = Field(..., description="Configuration name")

    # Tools and domains
    source_tool: str = Field(..., description="Source tool")
    target_tool: str = Field(..., description="Target tool")
    mapping_schema_id: str = Field(...,
                                   description="Associated mapping schema")

    # Sync behavior
    sync_frequency: str = Field(
        default="manual", description="Sync frequency (manual/realtime/scheduled)"
    )
    batch_size: int = Field(default=100, description="Records per batch")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    timeout_seconds: int = Field(default=300, description="Sync timeout")

    # Conflict resolution
    conflict_strategy: str = Field(
        default="last_modified_wins", description="Conflict resolution strategy"
    )
    preserve_source: bool = Field(
        default=True, description="Preserve source data on conflicts"
    )

    # Filtering and conditions
    sync_filters: Optional[Dict[str, Any]] = Field(
        None, description="Data filtering conditions"
    )
    field_exclusions: Optional[List[str]] = Field(
        None, description="Fields to exclude from sync"
    )

    # Monitoring and alerts
    enable_monitoring: bool = Field(
        default=True, description="Enable sync monitoring")
    alert_on_failure: bool = Field(
        default=True, description="Alert on sync failure")
    success_webhook: Optional[str] = Field(
        None, description="Webhook URL for success notifications"
    )
    failure_webhook: Optional[str] = Field(
        None, description="Webhook URL for failure notifications"
    )

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "config_id": "misp_helk_realtime",
                "name": "MISP to HELK Real-time Sync",
                "source_tool": "misp",
                "target_tool": "helk",
                "mapping_schema_id": "misp_to_helk_events",
                "sync_frequency": "realtime",
                "batch_size": 50,
            }
        }


# Pre-defined mapping schemas for common tool integrations
PREDEFINED_SCHEMAS: Dict[str, DataMappingSchema] = {
    "misp_to_helk_events": DataMappingSchema(
        schema_id="misp_to_helk_events",
        schema_name="MISP Events to HELK Security Events",
        description="Map MISP threat intelligence events to HELK security events",
        source_tool="misp",
        source_domain=DomainType.SECURITY,
        source_data_type=DataType.THREAT_INTELLIGENCE,
        target_tool="helk",
        target_domain=DomainType.SECURITY,
        target_data_type=DataType.SECURITY_EVENT,
        bidirectional=False,
        field_mappings=[
            FieldMapping(
                source_field="Event.id",
                target_field="event_id",
                mapping_type=MappingRuleType.DIRECT,
                required=True,
            ),
            FieldMapping(
                source_field="Event.timestamp",
                target_field="@timestamp",
                mapping_type=MappingRuleType.TRANSFORM,
                transform_function="iso_to_elasticsearch_timestamp",
                required=True,
            ),
            FieldMapping(
                source_field="Event.info",
                target_field="event.action",
                mapping_type=MappingRuleType.DIRECT,
                required=False,
            ),
        ],
    ),
    "actual_to_dispatch_budget": DataMappingSchema(
        schema_id="actual_to_dispatch_budget",
        schema_name="Actual Budget to Dispatch Incident Costs",
        description="Map budget entries to incident cost tracking",
        source_tool="actual_budget",
        source_domain=DomainType.PRODUCTIVITY,
        source_data_type=DataType.BUDGET_ENTRY,
        target_tool="dispatch",
        target_domain=DomainType.PRODUCTIVITY,
        target_data_type=DataType.DISPATCH_INCIDENT,
        bidirectional=True,
        field_mappings=[
            FieldMapping(
                source_field="transaction.amount",
                target_field="incident.cost",
                mapping_type=MappingRuleType.DIRECT,
                required=True,
            ),
            FieldMapping(
                source_field="transaction.date",
                target_field="incident.created_at",
                mapping_type=MappingRuleType.TRANSFORM,
                transform_function="date_to_datetime",
                required=True,
            ),
        ],
    ),
}


# Domain-specific data types mapping
DOMAIN_DATA_TYPES: Dict[DomainType, List[DataType]] = {
    DomainType.SECURITY: [
        DataType.THREAT_INTELLIGENCE,
        DataType.SECURITY_EVENT,
        DataType.VULNERABILITY,
        DataType.MALWARE_SAMPLE,
        DataType.IOC,
        DataType.YARA_RULE,
    ],
    DomainType.PRODUCTIVITY: [
        DataType.TASK,
        DataType.RECIPE,
        DataType.BUDGET_ENTRY,
        DataType.DISPATCH_INCIDENT,
        DataType.WORKFLOW,
        DataType.DOCUMENT,
    ],
    DomainType.MTG: [
        DataType.CARD,
        DataType.DECK,
        DataType.COMBO,
        DataType.COMMANDER,
    ],
    DomainType.INFRASTRUCTURE: [
        DataType.SERVICE_CONFIG,
        DataType.API_ROUTE,
        DataType.CONTAINER,
        DataType.WORKFLOW_TEMPLATE,
        DataType.MONITORING_ALERT,
        DataType.LOG_ENTRY,
    ],
}


def get_compatible_data_types(source_type: DataType) -> List[DataType]:
    """
    Get list of data types compatible for cross-domain mapping.

    Args:
        source_type: Source data type

    Returns:
        List of compatible target data types
    """
    compatibility_matrix = {
        # Security domain compatibilities
        DataType.THREAT_INTELLIGENCE: [
            DataType.SECURITY_EVENT,
            DataType.LOG_ENTRY,
            DataType.MONITORING_ALERT,
        ],
        DataType.SECURITY_EVENT: [
            DataType.THREAT_INTELLIGENCE,
            DataType.LOG_ENTRY,
            DataType.DISPATCH_INCIDENT,
        ],
        DataType.VULNERABILITY: [
            DataType.SECURITY_EVENT,
            DataType.TASK,
            DataType.DISPATCH_INCIDENT,
        ],

        # Productivity domain compatibilities
        DataType.TASK: [
            DataType.DISPATCH_INCIDENT,
            DataType.WORKFLOW,
            DataType.VULNERABILITY,
        ],
        DataType.DISPATCH_INCIDENT: [
            DataType.TASK,
            DataType.SECURITY_EVENT,
            DataType.BUDGET_ENTRY,
        ],
        DataType.BUDGET_ENTRY: [
            DataType.DISPATCH_INCIDENT,
            DataType.TASK,
        ],

        # Infrastructure domain compatibilities
        DataType.MONITORING_ALERT: [
            DataType.SECURITY_EVENT,
            DataType.DISPATCH_INCIDENT,
            DataType.LOG_ENTRY,
        ],
        DataType.LOG_ENTRY: [
            DataType.SECURITY_EVENT,
            DataType.MONITORING_ALERT,
            DataType.THREAT_INTELLIGENCE,
        ],
        DataType.WORKFLOW_TEMPLATE: [
            DataType.WORKFLOW,
            DataType.TASK,
        ],
    }

    return compatibility_matrix.get(source_type, [])
