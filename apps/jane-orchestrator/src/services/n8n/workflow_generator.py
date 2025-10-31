"""Workflow Template Generator for Detected Patterns."""

import uuid
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class WorkflowNodeType(Enum):
    """Types of workflow nodes in n8n."""
    TRIGGER = "trigger"
    WEBHOOK = "webhook"
    HTTP_REQUEST = "http_request"
    CODE = "code"
    CONDITION = "condition"
    SET = "set"
    MERGE = "merge"
    TOOL_ACTION = "tool_action"


@dataclass
class WorkflowNode:
    """Represents a single node in an n8n workflow."""
    id: str
    name: str
    type: WorkflowNodeType
    position: tuple[int, int]
    parameters: Dict[str, Any]
    credentials: Optional[Dict[str, str]] = None


@dataclass
class WorkflowConnection:
    """Represents a connection between workflow nodes."""
    source_node: str
    target_node: str
    source_output: str = "main"
    target_input: str = "main"


@dataclass
class GeneratedWorkflow:
    """Represents a complete generated n8n workflow."""
    id: str
    name: str
    description: str
    nodes: List[WorkflowNode]
    connections: List[WorkflowConnection]
    pattern_id: str
    confidence_score: float
    estimated_time_savings: float
    created_at: datetime


class WorkflowGenerator:
    """Generates n8n workflow templates from detected patterns."""

    def __init__(self):
        self.tool_node_mappings = self._initialize_tool_mappings()
        self.default_node_spacing = (200, 100)
        self.trigger_position = (0, 0)

    def generate_workflow_from_pattern(
        self, pattern: Any
    ) -> GeneratedWorkflow:
        """Generate a complete n8n workflow from a detected pattern."""
        workflow_id = str(uuid.uuid4())
        workflow_name = self._generate_workflow_name(pattern)
        workflow_description = self._generate_workflow_description(pattern)

        # Generate nodes for each tool in the sequence
        nodes = self._generate_nodes_for_pattern(pattern)

        # Generate connections between nodes
        connections = self._generate_connections_for_nodes(nodes)

        # Calculate estimated time savings
        time_savings = self._calculate_time_savings(pattern)

        return GeneratedWorkflow(
            id=workflow_id,
            name=workflow_name,
            description=workflow_description,
            nodes=nodes,
            connections=connections,
            pattern_id=pattern.pattern_id,
            confidence_score=pattern.confidence_score,
            estimated_time_savings=time_savings,
            created_at=datetime.utcnow()
        )

    def _generate_workflow_name(self, pattern: Any) -> str:
        """Generate a descriptive name for the workflow."""
        tool_names = " → ".join(pattern.tool_sequence[:3])
        if len(pattern.tool_sequence) > 3:
            tool_names += f" (+ {len(pattern.tool_sequence) - 3} more)"

        return f"Auto: {tool_names}"

    def _generate_workflow_description(self, pattern: Any) -> str:
        """Generate a description for the workflow."""
        frequency_text = f"Detected {pattern.frequency} times"
        confidence_text = f"{pattern.confidence_score:.1%} confidence"
        tools_text = f"Automates {len(pattern.tool_sequence)} tools"

        return (
            f"Automatically generated workflow based on user patterns. "
            f"{frequency_text}, {confidence_text}. {tools_text}: "
            f"{' → '.join(pattern.tool_sequence)}"
        )

    def _generate_nodes_for_pattern(
        self, pattern: Any
    ) -> List[WorkflowNode]:
        """Generate workflow nodes for each tool in the pattern."""
        nodes = []

        # Add trigger node
        trigger_node = self._create_trigger_node()
        nodes.append(trigger_node)

        # Add nodes for each tool in the sequence
        for i, (tool, action) in enumerate(
            zip(pattern.tool_sequence, pattern.action_sequence)
        ):
            position = (
                (i + 1) * self.default_node_spacing[0],
                self.default_node_spacing[1]
            )

            tool_node = self._create_tool_node(
                tool, action, position, i + 1
            )
            nodes.append(tool_node)

            # Add data transformation node if needed
            if i < len(pattern.tool_sequence) - 1:
                transform_node = self._create_transform_node_if_needed(
                    pattern, i, position
                )
                if transform_node:
                    nodes.append(transform_node)

        return nodes

    def _create_trigger_node(self) -> WorkflowNode:
        """Create a manual trigger node."""
        return WorkflowNode(
            id="trigger",
            name="Manual Trigger",
            type=WorkflowNodeType.TRIGGER,
            position=self.trigger_position,
            parameters={
                "type": "manual"
            }
        )

    def _create_tool_node(
        self, tool: str, action: str, position: tuple[int, int], step: int
    ) -> WorkflowNode:
        """Create a node for a specific tool action."""
        node_id = f"tool_{step}_{tool.lower().replace('-', '_')}"
        node_name = f"{tool}: {action}"

        # Get tool-specific configuration
        tool_config = self.tool_node_mappings.get(
            tool, self._get_default_tool_config()
        )

        # Create parameters based on tool type
        parameters = {
            "tool": tool,
            "action": action,
            "step": step,
            **tool_config.get("default_params", {})
        }

        return WorkflowNode(
            id=node_id,
            name=node_name,
            type=tool_config["node_type"],
            position=position,
            parameters=parameters,
            credentials=tool_config.get("credentials")
        )

    def _create_transform_node_if_needed(
        self, pattern: Any, step_index: int,
        position: tuple[int, int]
    ) -> Optional[WorkflowNode]:
        """Create a data transformation node if needed between steps."""
        transformations = pattern.data_transformation_patterns.get(
            'transformations', []
        )

        # Find transformation for this step
        relevant_transform = None
        for transform in transformations:
            if transform.get('from_step') == step_index:
                relevant_transform = transform
                break

        if not relevant_transform:
            return None

        # Create transformation node
        transform_position = (
            position[0] + self.default_node_spacing[0] // 2,
            position[1] + 50
        )

        return WorkflowNode(
            id=f"transform_{step_index}",
            name=f"Transform Data {step_index + 1}",
            type=WorkflowNodeType.CODE,
            position=transform_position,
            parameters={
                "mode": "runOnceForAllItems",
                "jsCode": self._generate_transform_code(relevant_transform)
            }
        )

    def _generate_transform_code(self, transform: Dict[str, Any]) -> str:
        """Generate JavaScript code for data transformation."""
        transform_type = transform.get('transformation', {}).get('type')

        if transform_type == 'direct_mapping':
            common_keys = transform['transformation']['common_keys']
            mapping_code = []

            for key in common_keys:
                mapping_code.append(f"  '{key}': items[0].json.{key},")

            return f"""
// Auto-generated data transformation
const transformedData = {{
{chr(10).join(mapping_code)}
}};

return [{{ json: transformedData }}];
"""

        # Default transformation
        return """
// Pass-through transformation
return items;
"""

    def _generate_connections_for_nodes(
        self, nodes: List[WorkflowNode]
    ) -> List[WorkflowConnection]:
        """Generate connections between workflow nodes."""
        connections = []

        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]

            connection = WorkflowConnection(
                source_node=current_node.id,
                target_node=next_node.id
            )
            connections.append(connection)

        return connections

    def _calculate_time_savings(self, pattern: Any) -> float:
        """Calculate estimated time savings from automation."""
        # Base time savings calculation
        manual_time = pattern.average_duration
        automated_time = 30  # Estimated 30 seconds for automated execution

        time_saved_per_execution = max(0, manual_time - automated_time)
        estimated_monthly_executions = pattern.frequency * 4  # Weekly to monthly

        return time_saved_per_execution * estimated_monthly_executions

    def _initialize_tool_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Initialize mappings between tools and n8n node types."""
        return {
            # Security Domain Tools
            "MISP": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "GET",
                    "url": "={{$env.MISP_URL}}/attributes",
                    "authentication": "predefinedCredentialType",
                    "nodeCredentialType": "mispApi"
                },
                "credentials": {"mispApi": "misp_credentials"}
            },
            "HELK": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "POST",
                    "url": "={{$env.HELK_URL}}/api/search"
                }
            },
            "SecurityOnion": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "GET",
                    "url": "={{$env.SECURITYONION_URL}}/api/events"
                }
            },
            "YARA-X": {
                "node_type": WorkflowNodeType.CODE,
                "default_params": {
                    "mode": "runOnceForAllItems",
                    "jsCode": "// YARA-X pattern matching logic"
                }
            },
            "CyberChef": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "POST",
                    "url": "={{$env.CYBERCHEF_URL}}/api/recipe"
                }
            },

            # Productivity Domain Tools
            "n8n": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "POST",
                    "url": "={{$env.N8N_URL}}/api/v1/workflows"
                }
            },
            "Actual Budget": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "GET",
                    "url": "={{$env.ACTUAL_URL}}/api/accounts"
                }
            },
            "Mealie": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "GET",
                    "url": "={{$env.MEALIE_URL}}/api/recipes"
                }
            },
            "Dispatch": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "POST",
                    "url": "={{$env.DISPATCH_URL}}/api/incidents"
                }
            },

            # MTG Domain Tools
            "Commander Spellbook": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "GET",
                    "url": "={{$env.SPELLBOOK_URL}}/api/combos"
                }
            },
            "MTG Commander Map": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "GET",
                    "url": "={{$env.COMMANDER_MAP_URL}}/api/commanders"
                }
            },

            # Infrastructure Domain Tools
            "Kong": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "GET",
                    "url": "={{$env.KONG_ADMIN_URL}}/services"
                }
            },
            "Ghostwriter": {
                "node_type": WorkflowNodeType.HTTP_REQUEST,
                "default_params": {
                    "method": "GET",
                    "url": "={{$env.GHOSTWRITER_URL}}/api/projects"
                }
            }
        }

    def _get_default_tool_config(self) -> Dict[str, Any]:
        """Get default configuration for unknown tools."""
        return {
            "node_type": WorkflowNodeType.HTTP_REQUEST,
            "default_params": {
                "method": "GET",
                "url": "={{$env.TOOL_URL}}/api"
            }
        }

    def export_workflow_to_n8n_format(
        self, workflow: GeneratedWorkflow
    ) -> Dict[str, Any]:
        """Export workflow to n8n's JSON format."""
        n8n_nodes = []

        for node in workflow.nodes:
            n8n_node = {
                "id": node.id,
                "name": node.name,
                "type": node.type.value,
                "typeVersion": 1,
                "position": list(node.position),
                "parameters": node.parameters
            }

            if node.credentials:
                n8n_node["credentials"] = node.credentials

            n8n_nodes.append(n8n_node)

        # Convert connections to n8n format
        n8n_connections = {}
        for connection in workflow.connections:
            if connection.source_node not in n8n_connections:
                n8n_connections[connection.source_node] = {}

            if connection.source_output not in n8n_connections[connection.source_node]:
                n8n_connections[connection.source_node][connection.source_output] = [
                ]

            n8n_connections[connection.source_node][connection.source_output].append({
                "node": connection.target_node,
                "type": connection.target_input,
                "index": 0
            })

        return {
            "name": workflow.name,
            "nodes": n8n_nodes,
            "connections": n8n_connections,
            "active": False,
            "settings": {
                "executionOrder": "v1"
            },
            "staticData": None,
            "meta": {
                "pattern_id": workflow.pattern_id,
                "confidence_score": workflow.confidence_score,
                "estimated_time_savings": workflow.estimated_time_savings,
                "generated_at": workflow.created_at.isoformat()
            },
            "pinData": {},
            "versionId": str(uuid.uuid4())
        }

    def generate_multiple_workflow_variants(
        self, pattern: Any, variant_count: int = 3
    ) -> List[GeneratedWorkflow]:
        """Generate multiple workflow variants for user choice."""
        variants = []

        # Generate base workflow
        base_workflow = self.generate_workflow_from_pattern(pattern)
        variants.append(base_workflow)

        # Generate variants with different approaches
        for i in range(variant_count - 1):
            variant = self._create_workflow_variant(base_workflow, i + 1)
            variants.append(variant)

        return variants

    def _create_workflow_variant(
        self, base_workflow: GeneratedWorkflow, variant_number: int
    ) -> GeneratedWorkflow:
        """Create a variant of the base workflow."""
        variant_id = str(uuid.uuid4())
        variant_name = f"{base_workflow.name} (Variant {variant_number})"

        # Create modified nodes (could add error handling, different triggers, etc.)
        modified_nodes = base_workflow.nodes.copy()

        # Add error handling nodes for variants
        if variant_number == 1:
            # Add error handling variant
            error_node = WorkflowNode(
                id="error_handler",
                name="Error Handler",
                type=WorkflowNodeType.CONDITION,
                position=(100, 200),
                parameters={
                    "conditions": {
                        "boolean": [],
                        "dateTime": [],
                        "number": [],
                        "string": [{
                            "value1": "={{$json.error}}",
                            "operation": "exists"
                        }]
                    }
                }
            )
            modified_nodes.append(error_node)

        return GeneratedWorkflow(
            id=variant_id,
            name=variant_name,
            description=f"{base_workflow.description} (Variant {variant_number})",
            nodes=modified_nodes,
            connections=base_workflow.connections,
            pattern_id=base_workflow.pattern_id,
            confidence_score=base_workflow.confidence_score *
            0.9,  # Slightly lower confidence for variants
            estimated_time_savings=base_workflow.estimated_time_savings,
            created_at=datetime.utcnow()
        )
