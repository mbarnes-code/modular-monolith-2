"""
Security domain data mapping schemas.

Contains specific schemas for mapping data between security tools
like MISP, HELK, SecurityOnion, YARA-X, etc.
"""

from typing import Dict, List

from .base import (DataMappingSchema, DataType, DomainType, FieldMapping,
                   MappingRuleType)

# MISP to HELK event mapping
MISP_TO_HELK_SCHEMA = DataMappingSchema(
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
        FieldMapping(
            source_field="Event.threat_level_id",
            target_field="event.severity",
            mapping_type=MappingRuleType.TRANSFORM,
            transform_function="threat_level_to_severity",
            required=False,
        ),
    ],
)

# YARA-X to MISP IOC mapping
YARAX_TO_MISP_SCHEMA = DataMappingSchema(
    schema_id="yarax_to_misp_ioc",
    schema_name="YARA-X Rules to MISP IOCs",
    description="Map YARA-X detection rules to MISP indicators",
    source_tool="yara_x",
    source_domain=DomainType.SECURITY,
    source_data_type=DataType.YARA_RULE,
    target_tool="misp",
    target_domain=DomainType.SECURITY,
    target_data_type=DataType.IOC,
    bidirectional=False,
    field_mappings=[
        FieldMapping(
            source_field="rule.name",
            target_field="Attribute.value",
            mapping_type=MappingRuleType.DIRECT,
            required=True,
        ),
        FieldMapping(
            source_field="rule.condition",
            target_field="Attribute.comment",
            mapping_type=MappingRuleType.DIRECT,
            required=False,
        ),
    ],
)

# SecurityOnion to HELK log mapping
SECURITYONION_TO_HELK_SCHEMA = DataMappingSchema(
    schema_id="securityonion_to_helk_logs",
    schema_name="SecurityOnion Logs to HELK",
    description="Map SecurityOnion network logs to HELK analytics",
    source_tool="security_onion",
    source_domain=DomainType.SECURITY,
    source_data_type=DataType.SECURITY_EVENT,
    target_tool="helk",
    target_domain=DomainType.SECURITY,
    target_data_type=DataType.LOG_ENTRY,
    bidirectional=False,
    field_mappings=[
        FieldMapping(
            source_field="timestamp",
            target_field="@timestamp",
            mapping_type=MappingRuleType.TRANSFORM,
            transform_function="unix_to_elasticsearch_timestamp",
            required=True,
        ),
        FieldMapping(
            source_field="src_ip",
            target_field="source.ip",
            mapping_type=MappingRuleType.DIRECT,
            required=True,
        ),
        FieldMapping(
            source_field="dest_ip",
            target_field="destination.ip",
            mapping_type=MappingRuleType.DIRECT,
            required=True,
        ),
    ],
)

# All security domain schemas
SECURITY_SCHEMAS: Dict[str, DataMappingSchema] = {
    "misp_to_helk_events": MISP_TO_HELK_SCHEMA,
    "yarax_to_misp_ioc": YARAX_TO_MISP_SCHEMA,
    "securityonion_to_helk_logs": SECURITYONION_TO_HELK_SCHEMA,
}
