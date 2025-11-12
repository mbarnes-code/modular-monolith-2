"""
Productivity domain data mapping schemas.

Contains specific schemas for mapping data between productivity tools
like Actual Budget, Mealie, Dispatch, etc.
"""

from typing import Dict

from .base import (DataMappingSchema, DataType, DomainType, FieldMapping,
                   MappingRuleType)

# Actual Budget to Dispatch incident mapping
ACTUAL_TO_DISPATCH_SCHEMA = DataMappingSchema(
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
        FieldMapping(
            source_field="transaction.description",
            target_field="incident.title",
            mapping_type=MappingRuleType.DIRECT,
            required=False,
        ),
    ],
)

# Mealie recipe to task mapping
MEALIE_TO_TASK_SCHEMA = DataMappingSchema(
    schema_id="mealie_recipe_to_task",
    schema_name="Mealie Recipe to Task Management",
    description="Convert recipes to meal preparation tasks",
    source_tool="mealie",
    source_domain=DomainType.PRODUCTIVITY,
    source_data_type=DataType.RECIPE,
    target_tool="task_manager",
    target_domain=DomainType.PRODUCTIVITY,
    target_data_type=DataType.TASK,
    bidirectional=False,
    field_mappings=[
        FieldMapping(
            source_field="recipe.name",
            target_field="task.title",
            mapping_type=MappingRuleType.TRANSFORM,
            transform_function="recipe_to_task_title",
            required=True,
        ),
        FieldMapping(
            source_field="recipe.prep_time",
            target_field="task.estimated_duration",
            mapping_type=MappingRuleType.DIRECT,
            required=False,
        ),
        FieldMapping(
            source_field="recipe.instructions",
            target_field="task.description",
            mapping_type=MappingRuleType.DIRECT,
            required=False,
        ),
    ],
)

# All productivity domain schemas
PRODUCTIVITY_SCHEMAS: Dict[str, DataMappingSchema] = {
    "actual_to_dispatch_budget": ACTUAL_TO_DISPATCH_SCHEMA,
    "mealie_recipe_to_task": MEALIE_TO_TASK_SCHEMA,
}
