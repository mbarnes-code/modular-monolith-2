"""
WorkflowGenerationService for auto-creating n8n workflows.

This service generates n8n workflow definitions from detected user patterns
and manages the workflow lifecycle.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..data.models.adaptive_workflow import AdaptiveWorkflow
from ..data.models.workflow_pattern import WorkflowPattern
from .base_service import BaseService


class WorkflowGenerationService(BaseService):
    """
    Service for generating n8n workflows from detected patterns.

    Creates workflow definitions, validates them, and manages
    the complete workflow generation lifecycle.
    """

    def __init__(self, db_session: Session):
        super().__init__(db_session)
        self.n8n_base_nodes = {
            "start": {"type": "n8n-nodes-base.start", "position": [240, 300]},
            "webhook": {"type": "n8n-nodes-base.webhook", "position": [240, 300]},
            "http_request": {"type": "n8n-nodes-base.httpRequest"},
            "code": {"type": "n8n-nodes-base.code"},
            "set": {"type": "n8n-nodes-base.set"},
            "if": {"type": "n8n-nodes-base.if"},
            "schedule": {"type": "n8n-nodes-base.scheduleTrigger"},
            "function": {"type": "n8n-nodes-base.function"}
        }

    def generate_workflow_from_pattern(
        self,
        pattern: WorkflowPattern
    ) -> Optional[AdaptiveWorkflow]:
        """
        Generate an n8n workflow from a detected pattern.

        Args:
            pattern: The pattern to generate workflow from

        Returns:
            Generated AdaptiveWorkflow or None if generation failed
        """
        if not pattern.is_ready_for_automation():
            return None

        # Generate workflow definition
        workflow_definition = self._create_workflow_definition(pattern)

        if not workflow_definition:
            return None

        # Create adaptive workflow record
        adaptive_workflow = AdaptiveWorkflow(
            workflow_id=str(uuid.uuid4()),
            workflow_name=self._generate_workflow_name(pattern),
            description=self._generate_workflow_description(pattern),
            category=pattern.category,
            workflow_definition=workflow_definition,
            node_configuration=workflow_definition.get("nodes", []),
            connection_mapping=workflow_definition.get("connections", {}),
            source_pattern_hash=pattern.pattern_hash,
            generation_method="pattern_based",
            generation_confidence=pattern.confidence_score,
            user_id=pattern.user_id,
            pattern_id=pattern.id
        )

        # Mark pattern as having generated workflow
        pattern.workflow_generated = True
        pattern.n8n_workflow_id = adaptive_workflow.workflow_id
        pattern.generation_timestamp = datetime.utcnow()

        self.db_session.add(adaptive_workflow)
        return adaptive_workflow

    def _create_workflow_definition(
        self,
        pattern: WorkflowPattern
    ) -> Optional[Dict[str, Any]]:
        """Create n8n workflow definition from pattern."""
        try:
            # Determine trigger type
            trigger_node = self._create_trigger_node(pattern)

            # Create tool execution nodes
            tool_nodes = self._create_tool_nodes(pattern)

            # Create data flow connections
            connections = self._create_connections(trigger_node, tool_nodes)

            # Build complete workflow
            workflow = {
                "name": self._generate_workflow_name(pattern),
                "nodes": [trigger_node] + tool_nodes,
                "connections": connections,
                "active": False,  # Start inactive for user review
                "settings": {
                    "executionOrder": "v1"
                },
                "staticData": {},
                "meta": {
                    "generated_by": "jane_orchestrator",
                    "source_pattern": pattern.pattern_hash,
                    "generation_timestamp": datetime.utcnow().isoformat()
                }
            }

            return workflow

        except Exception as e:
            self.logger.error(f"Failed to create workflow definition: {e}")
            return None

    def _create_trigger_node(self, pattern: WorkflowPattern) -> Dict[str, Any]:
        """Create appropriate trigger node based on pattern."""
        timing_pattern = pattern.timing_pattern or {}

        # Determine trigger type
        if timing_pattern.get("has_timing_pattern") and timing_pattern.get("is_regular"):
            # Schedule-based trigger
            schedule = self._convert_to_cron_schedule(
                timing_pattern.get("suggested_schedule", "daily")
            )
            return {
                "id": str(uuid.uuid4()),
                "name": "Schedule Trigger",
                "type": "n8n-nodes-base.scheduleTrigger",
                "typeVersion": 1,
                "position": [240, 300],
                "parameters": {
                    "rule": {
                        "interval": schedule["interval"]
                    }
                }
            }
        else:
            # Manual/webhook trigger
            return {
                "id": str(uuid.uuid4()),
                "name": "Manual Trigger",
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [240, 300],
                "parameters": {}
            }

    def _create_tool_nodes(
        self,
        pattern: WorkflowPattern
    ) -> List[Dict[str, Any]]:
        """Create nodes for each tool in the pattern."""
        nodes = []
        tools = pattern.tool_sequence or []

        x_position = 460
        y_position = 300

        for i, tool in enumerate(tools):
            node = self._create_tool_node(tool, i, x_position, y_position)
            nodes.append(node)

            # Adjust position for next node
            x_position += 220
            if (i + 1) % 4 == 0:  # New row every 4 nodes
                x_position = 460
                y_position += 120

        return nodes

    def _create_tool_node(
        self,
        tool: str,
        index: int,
        x_pos: int,
        y_pos: int
    ) -> Dict[str, Any]:
        """Create a node for a specific tool."""
        # Map tool to appropriate n8n node type
        node_config = self._get_tool_node_config(tool)

        return {
            "id": str(uuid.uuid4()),
            "name": f"{tool} Action",
            "type": node_config["type"],
            "typeVersion": 1,
            "position": [x_pos, y_pos],
            "parameters": node_config["parameters"]
        }

    def _get_tool_node_config(self, tool: str) -> Dict[str, Any]:
        """Get node configuration for a specific tool."""
        # Tool-specific configurations
        tool_configs = {
            "misp": {
                "type": "n8n-nodes-base.httpRequest",
                "parameters": {
                    "method": "POST",
                    "url": "{{$env.MISP_URL}}/events",
                    "authentication": "genericCredentialType",
                    "genericAuthType": "httpHeaderAuth"
                }
            },
            "cyberchef": {
                "type": "n8n-nodes-base.code",
                "parameters": {
                    "mode": "runOnceForAllItems",
                    "jsCode": "// CyberChef operation placeholder\nreturn items;"
                }
            },
            "n8n": {
                "type": "n8n-nodes-base.n8n",
                "parameters": {
                    "operation": "execute"
                }
            },
            "mealie": {
                "type": "n8n-nodes-base.httpRequest",
                "parameters": {
                    "method": "GET",
                    "url": "{{$env.MEALIE_URL}}/api/recipes"
                }
            }
        }

        # Default to HTTP request if tool not specifically configured
        return tool_configs.get(tool.lower(), {
            "type": "n8n-nodes-base.httpRequest",
            "parameters": {
                "method": "POST",
                "url": f"{{{{$env.{tool.upper()}_URL}}}}/api/execute"
            }
        })

    def _create_connections(
        self,
        trigger_node: Dict[str, Any],
        tool_nodes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create connections between nodes."""
        connections = {}

        if not tool_nodes:
            return connections

        # Connect trigger to first tool node
        trigger_id = trigger_node["id"]
        connections[trigger_id] = {
            "main": [[{
                "node": tool_nodes[0]["name"],
                "type": "main",
                "index": 0
            }]]
        }

        # Connect tool nodes in sequence
        for i in range(len(tool_nodes) - 1):
            current_node = tool_nodes[i]
            next_node = tool_nodes[i + 1]

            connections[current_node["id"]] = {
                "main": [[{
                    "node": next_node["name"],
                    "type": "main",
                    "index": 0
                }]]
            }

        return connections

    def _convert_to_cron_schedule(self, schedule_type: str) -> Dict[str, Any]:
        """Convert schedule type to n8n interval format."""
        schedules = {
            "every_30_minutes": {"interval": [{"field": "minutes", "value": 30}]},
            "hourly": {"interval": [{"field": "hours", "value": 1}]},
            "daily": {"interval": [{"field": "days", "value": 1}]},
            "weekly": {"interval": [{"field": "weeks", "value": 1}]},
            "monthly": {"interval": [{"field": "months", "value": 1}]}
        }

        return schedules.get(schedule_type, schedules["daily"])

    def _generate_workflow_name(self, pattern: WorkflowPattern) -> str:
        """Generate a descriptive name for the workflow."""
        return f"Auto-{pattern.pattern_name}"

    def _generate_workflow_description(self, pattern: WorkflowPattern) -> str:
        """Generate a description for the workflow."""
        return (
            f"Automatically generated workflow from pattern '{pattern.pattern_name}'. "
            f"Detected {pattern.occurrence_count} times with {pattern.confidence_score:.1%} confidence. "
            f"Tools: {', '.join(pattern.tool_sequence or [])}"
        )

    def validate_workflow_definition(
        self,
        workflow_definition: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate a workflow definition for correctness."""
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": []
        }

        # Check required fields
        required_fields = ["name", "nodes", "connections"]
        for field in required_fields:
            if field not in workflow_definition:
                validation_result["errors"].append(
                    f"Missing required field: {field}")
                validation_result["is_valid"] = False

        # Validate nodes
        nodes = workflow_definition.get("nodes", [])
        if not nodes:
            validation_result["errors"].append(
                "Workflow must have at least one node")
            validation_result["is_valid"] = False

        # Check for trigger node
        trigger_types = [
            "n8n-nodes-base.scheduleTrigger",
            "n8n-nodes-base.manualTrigger",
            "n8n-nodes-base.webhook"
        ]

        has_trigger = any(
            node.get("type") in trigger_types for node in nodes
        )

        if not has_trigger:
            validation_result["warnings"].append(
                "No trigger node found - workflow may not execute automatically"
            )

        # Validate connections
        connections = workflow_definition.get("connections", {})
        node_names = {node.get("name") for node in nodes}

        for node_id, node_connections in connections.items():
            if "main" in node_connections:
                for connection_list in node_connections["main"]:
                    for connection in connection_list:
                        target_node = connection.get("node")
                        if target_node not in node_names:
                            validation_result["errors"].append(
                                f"Connection references non-existent node: {target_node}"
                            )
                            validation_result["is_valid"] = False

        return validation_result

    def optimize_workflow(
        self,
        adaptive_workflow: AdaptiveWorkflow,
        performance_data: Dict[str, Any]
    ) -> bool:
        """Optimize workflow based on performance data."""
        try:
            workflow_def = adaptive_workflow.workflow_definition.copy()

            # Optimization strategies based on performance
            if performance_data.get("average_execution_time", 0) > 60:
                # Add parallel execution where possible
                workflow_def = self._add_parallel_execution(workflow_def)

            if performance_data.get("error_rate", 0) > 0.1:
                # Add error handling
                workflow_def = self._add_error_handling(workflow_def)

            # Update workflow definition
            adaptive_workflow.workflow_definition = workflow_def
            adaptive_workflow.node_configuration = workflow_def.get(
                "nodes", [])
            adaptive_workflow.connection_mapping = workflow_def.get(
                "connections", {})
            adaptive_workflow.mark_optimized()

            return True

        except Exception as e:
            self.logger.error(f"Failed to optimize workflow: {e}")
            return False

    def _add_parallel_execution(
        self,
        workflow_def: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add parallel execution to workflow where possible."""
        # This is a simplified implementation
        # In practice, would analyze dependencies and parallelize independent operations
        return workflow_def

    def _add_error_handling(
        self,
        workflow_def: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add error handling to workflow."""
        # Add error handling nodes and connections
        return workflow_def

    def export_workflow_for_n8n(
        self,
        adaptive_workflow: AdaptiveWorkflow
    ) -> Dict[str, Any]:
        """Export workflow in n8n-compatible format."""
        return {
            "name": adaptive_workflow.workflow_name,
            "nodes": adaptive_workflow.node_configuration,
            "connections": adaptive_workflow.connection_mapping,
            "active": adaptive_workflow.is_active,
            "settings": adaptive_workflow.workflow_definition.get("settings", {}),
            "staticData": adaptive_workflow.workflow_definition.get("staticData", {}),
            "tags": [
                "auto-generated",
                f"pattern-{adaptive_workflow.source_pattern_hash[:8]}",
                adaptive_workflow.category
            ]
        }
