"""
OpenAPI Specification Generator

Generates comprehensive OpenAPI documentation for the mental prosthetic platform
with executive function accommodations and all 37 tool integrations.
"""

import json
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel, Field


class ExecutiveFunctionTag(BaseModel):
    """Tag for executive function endpoints"""
    name: str = Field(..., description="Tag name")
    description: str = Field(..., description="Tag description")
    executive_function_level: str = Field(
        default="moderate",
        description="Level of executive function support"
    )


class ToolIntegrationInfo(BaseModel):
    """Information about integrated tool"""
    tool_id: str = Field(..., description="Unique tool identifier")
    tool_name: str = Field(..., description="Display name")
    domain: str = Field(...,
                        description="Domain (security, productivity, mtg, infrastructure)")
    version: str = Field(..., description="Tool version")
    endpoints: List[str] = Field(..., description="Available API endpoints")
    executive_function_features: List[str] = Field(
        default_factory=list,
        description="Executive function accommodations available"
    )


def generate_mental_prosthetic_openapi_schema(app: FastAPI) -> Dict[str, Any]:
    """
    Generate enhanced OpenAPI schema for mental prosthetic platform
    with executive function documentation and tool integration details
    """

    # Base OpenAPI schema
    openapi_schema = get_openapi(
        title="Mental Prosthetic Platform API",
        version="1.0.0",
        description="""
        # Mental Prosthetic Platform API

        Unified API for 37 executive function tools with ADHD/autism accommodations.

        ## Executive Function Support

        This API provides comprehensive executive function accommodations:

        - **ADHD Support**: Reduced cognitive load, progress tracking, hyperfocus management
        - **Autism Support**: Predictable navigation, sensory preferences, routine preservation  
        - **Context Preservation**: Maintains user state across tool switches
        - **Performance Optimization**: Domain-specific response time targets

        ## Domain Organization

        Tools are organized into 4 domains with specific performance targets:

        - **Security Domain** (13 tools): <1s response time for threat analysis
        - **Productivity Domain** (8 tools): <2s response time for task management
        - **MTG Domain** (4 tools): <3s response time for game analysis
        - **Infrastructure Domain** (12 tools): <5s response time for system operations

        ## Authentication

        Uses JWT-based authentication with executive function scopes:

        ```json
        {
          "user_id": "user123",
          "scopes": ["security:read", "productivity:write", "executive_function:enhanced"],
          "accommodations": {
            "adhd_mode": true,
            "focus_assist": true,
            "context_preservation": true
          }
        }
        ```

        ## Real-time Communication

        WebSocket endpoints provide real-time updates for:

        - Context state synchronization
        - AI server communication
        - Cross-tool data flow
        - Executive function metrics

        ## Error Handling

        All errors include executive function accommodations:

        - User-friendly error messages
        - Suggested next actions
        - Context preservation recommendations
        - Cognitive load considerations
        """,
        routes=app.routes,
        tags=[
            {
                "name": "Authentication",
                "description": "JWT authentication with executive function scopes"
            },
            {
                "name": "Executive Function",
                "description": "ADHD/autism accommodations and context management"
            },
            {
                "name": "Security Tools",
                "description": "13 security tools (MISP, HELK, SecurityOnion, etc.) - <1s target"
            },
            {
                "name": "Productivity Tools",
                "description": "8 productivity tools (n8n, Mealie, Dispatch, etc.) - <2s target"
            },
            {
                "name": "MTG Tools",
                "description": "4 MTG tools (Commander Spellbook, deck analysis, etc.) - <3s target"
            },
            {
                "name": "Infrastructure Tools",
                "description": "12 infrastructure tools (Kong, Ghostwriter, etc.) - <5s target"
            },
            {
                "name": "AI Integration",
                "description": "vLLM and MCP server communication endpoints"
            },
            {
                "name": "WebSocket",
                "description": "Real-time communication endpoints"
            },
            {
                "name": "Health & Metrics",
                "description": "System health checks and performance metrics"
            }
        ]
    )

    # Add executive function extensions
    openapi_schema["info"]["x-executive-function-support"] = {
        "adhd_accommodations": [
            "Reduced cognitive load",
            "Progress indicators",
            "Break reminders",
            "Hyperfocus warnings",
            "Task chunking"
        ],
        "autism_accommodations": [
            "Predictable navigation",
            "Sensory preferences",
            "Change notifications",
            "Routine preservation",
            "Minimal sensory distractions"
        ],
        "performance_targets": {
            "security": "1000ms",
            "productivity": "2000ms",
            "mtg": "3000ms",
            "infrastructure": "5000ms",
            "ui_responsiveness": "200ms"
        }
    }

    # Add tool integration information
    openapi_schema["info"]["x-integrated-tools"] = {
        "total_count": 37,
        "domains": {
            "security": {
                "count": 13,
                "tools": [
                    "MISP", "HELK", "SecurityOnion", "Maltrail", "YARA-X",
                    "CyberChef", "Nemesis", "MalwareBazaar", "VirusTotal",
                    "Brute-Ratel", "APISCout", "Rita", "Software Forensic Kit"
                ]
            },
            "productivity": {
                "count": 8,
                "tools": [
                    "n8n", "Mealie", "Dispatch", "Actual Budget", "Firecrawl",
                    "Goose", "IT-Tools", "Inspector"
                ]
            },
            "mtg": {
                "count": 4,
                "tools": [
                    "Commander Spellbook", "MTG Commander Map",
                    "MTG Scripting Toolkit", "Card Analysis Engine"
                ]
            },
            "infrastructure": {
                "count": 12,
                "tools": [
                    "Kong", "Ghostwriter", "KasmVNC", "BlackArch", "OnEx",
                    "LSCript", "Meterpreter", "Chroma-MCP", "FileScopeMP",
                    "n8n-MCP", "Firecrawl-MCP", "HexStrike-AI"
                ]
            }
        }
    }

    # Add executive function schema components
    if "components" not in openapi_schema:
        openapi_schema["components"] = {}

    if "schemas" not in openapi_schema["components"]:
        openapi_schema["components"]["schemas"] = {}

    # Executive function schemas
    openapi_schema["components"]["schemas"]["ExecutiveFunctionContext"] = {
        "type": "object",
        "properties": {
            "user_id": {"type": "string", "description": "User identifier"},
            "adhd_mode_enabled": {"type": "boolean", "default": False},
            "focus_assist_enabled": {"type": "boolean", "default": True},
            "context_switching_warning": {"type": "boolean", "default": True},
            "ui_response_threshold_ms": {"type": "integer", "default": 200},
            "cognitive_load_score": {"type": "integer", "minimum": 0, "maximum": 100, "default": 30},
            "current_tool": {"type": "string", "nullable": True},
            "active_workflows": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["user_id"]
    }

    openapi_schema["components"]["schemas"]["ExecutiveFunctionResponse"] = {
        "type": "object",
        "properties": {
            "success": {"type": "boolean"},
            "data": {"type": "object"},
            "execution_time_ms": {"type": "integer"},
            "accommodations_applied": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of executive function accommodations applied"
            },
            "cognitive_load_impact": {
                "type": "integer",
                "minimum": -10,
                "maximum": 10,
                "description": "Impact on cognitive load (-10 reduces, +10 increases)"
            },
            "warnings": {
                "type": "array",
                "items": {"type": "string"},
                "description": "User-friendly warnings and suggestions"
            }
        },
        "required": ["success"]
    }

    # Tool adapter response schema
    openapi_schema["components"]["schemas"]["ToolAdapterResponse"] = {
        "type": "object",
        "properties": {
            "tool_id": {"type": "string", "description": "Tool identifier"},
            "tool_name": {"type": "string", "description": "Tool display name"},
            "domain": {"type": "string", "enum": ["security", "productivity", "mtg", "infrastructure"]},
            "response_data": {"type": "object", "description": "Tool-specific response data"},
            "executive_function_enhanced": {"type": "boolean", "default": True},
            "performance_metrics": {
                "type": "object",
                "properties": {
                    "execution_time_ms": {"type": "integer"},
                    "domain_target_ms": {"type": "integer"},
                    "target_met": {"type": "boolean"}
                }
            }
        },
        "required": ["tool_id", "tool_name", "domain", "response_data"]
    }

    # WebSocket message schema
    openapi_schema["components"]["schemas"]["WebSocketMessage"] = {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": [
                    "context_update", "focus_change", "task_progress", "cognitive_load_update",
                    "ai_request", "ai_response", "ai_stream_start", "ai_stream_chunk", "ai_stream_end",
                    "tool_state_sync", "cross_tool_data", "workflow_update",
                    "preference_update", "setting_change",
                    "connection_ack", "heartbeat", "error"
                ]
            },
            "data": {"type": "object"},
            "timestamp": {"type": "string", "format": "date-time"},
            "message_id": {"type": "string", "format": "uuid"},
            "source": {"type": "string"},
            "target": {"type": "string", "nullable": True},
            "user_id": {"type": "string", "nullable": True},
            "session_id": {"type": "string", "nullable": True}
        },
        "required": ["type", "data", "timestamp", "message_id"]
    }

    # Add security schemes
    if "securitySchemes" not in openapi_schema["components"]:
        openapi_schema["components"]["securitySchemes"] = {}

    openapi_schema["components"]["securitySchemes"]["JWTBearer"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "JWT token with executive function scopes"
    }

    openapi_schema["components"]["securitySchemes"]["WebSocketToken"] = {
        "type": "apiKey",
        "in": "query",
        "name": "token",
        "description": "JWT token for WebSocket authentication"
    }

    # Add response examples for executive function accommodations
    openapi_schema["components"]["examples"] = {
        "ADHDResponse": {
            "summary": "Response with ADHD accommodations",
            "value": {
                "success": True,
                "data": {"items": [{"id": 1, "name": "Task 1"}]},
                "execution_time_ms": 150,
                "accommodations_applied": [
                    "reduced_result_set",
                    "progress_indicators",
                    "essential_fields_only"
                ],
                "cognitive_load_impact": -2,
                "warnings": []
            }
        },
        "ContextSwitchWarning": {
            "summary": "Context switch warning",
            "value": {
                "success": True,
                "data": {"tool_data": "..."},
                "execution_time_ms": 300,
                "accommodations_applied": ["context_switch_detected"],
                "cognitive_load_impact": 3,
                "warnings": [
                    "Switching from Security Tool to Productivity Tool detected",
                    "Consider completing current task before switching",
                    "Context has been preserved for easy return"
                ]
            }
        }
    }

    return openapi_schema


def save_openapi_spec(app: FastAPI, output_path: str = "openapi.json") -> None:
    """Save OpenAPI specification to file"""
    schema = generate_mental_prosthetic_openapi_schema(app)

    with open(output_path, 'w') as f:
        json.dump(schema, f, indent=2, default=str)

    print(f"OpenAPI specification saved to {output_path}")


def setup_openapi_docs(app: FastAPI) -> None:
    """Setup enhanced OpenAPI documentation for the app"""
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        app.openapi_schema = generate_mental_prosthetic_openapi_schema(app)
        return app.openapi_schema

    app.openapi = custom_openapi
