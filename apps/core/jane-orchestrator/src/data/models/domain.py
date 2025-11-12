"""
Domain Classification model for organizing 37 executive function tools.

Constitutional Requirements:
- 4 domains: Security (13 tools), Productivity (8 tools),
  MTG (4 tools), Infrastructure (12 tools)
- Domain-specific performance requirements
- Cross-domain workflow support
"""

from typing import Any, Dict, List

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Domain(Base):
    """
    Domain classification for organizing executive function tools.

    Constitutional organization:
    - Security: 13 tools (<1s response time)
    - Productivity: 8 tools (<2s response time)
    - MTG: 4 tools (<3s response time)
    - Infrastructure: 12 tools (<5s response time)
    """

    __tablename__ = "domains"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)

    # Domain metadata
    description = Column(Text, nullable=True)
    icon = Column(String(50), nullable=True)  # Icon identifier
    color = Column(String(20), nullable=True)  # Theme color

    # Performance requirements (constitutional)
    max_response_time_ms = Column(Integer, nullable=False)

    # Tool organization
    tool_count = Column(Integer, default=0)
    tools_config = Column(JSON, default=lambda: {})  # Tool configuration

    # Domain-specific settings
    default_view = Column(String(100), nullable=True)
    navigation_config = Column(JSON, default=lambda: {})
    feature_flags = Column(JSON, default=lambda: {})

    # Executive function accommodations
    cognitive_load_level = Column(String(20), default="medium")  # low/med/high
    context_switching_cost = Column(Integer, default=5)  # 1-10 scale
    interruption_sensitivity = Column(String(20), default="medium")

    # Status and metadata
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    @classmethod
    def get_constitutional_domains(cls) -> List[Dict[str, Any]]:
        """Get the constitutional 4-domain structure."""
        return [
            {
                "name": "security",
                "display_name": "Security Operations",
                "description": "13 security tools for threat analysis and response",
                "icon": "shield-check",
                "color": "#dc2626",  # Red
                "max_response_time_ms": 1000,  # <1s requirement
                "tool_count": 13,
                "cognitive_load_level": "high",
                "context_switching_cost": 8,
                "interruption_sensitivity": "high",
                "tools_config": {
                    "categories": [
                        "threat_intelligence", "network_monitoring",
                        "malware_analysis", "incident_response"
                    ],
                    "critical_tools": [
                        "MISP", "HELK", "SecurityOnion", "YARA-X", "Maltrail"
                    ],
                    "airgapped_capable": True,
                    "requires_isolation": True
                },
                "default_view": "dashboard",
                "sort_order": 1
            },
            {
                "name": "productivity",
                "display_name": "Productivity & Workflow",
                "description": "8 productivity tools for task and workflow management",
                "icon": "clipboard-check",
                "color": "#059669",  # Green
                "max_response_time_ms": 2000,  # <2s requirement
                "tool_count": 8,
                "cognitive_load_level": "medium",
                "context_switching_cost": 4,
                "interruption_sensitivity": "low",
                "tools_config": {
                    "categories": [
                        "task_management", "budgeting", "meal_planning",
                        "incident_management", "automation"
                    ],
                    "critical_tools": [
                        "Actual Budget", "Mealie", "Dispatch", "n8n", "IT-Tools"
                    ],
                    "executive_function_support": True,
                    "adhd_optimized": True
                },
                "default_view": "dashboard",
                "sort_order": 2
            },
            {
                "name": "mtg",
                "display_name": "Magic: The Gathering",
                "description": "4 MTG tools for deck building and combo analysis",
                "icon": "sparkles",
                "color": "#7c3aed",  # Purple
                "max_response_time_ms": 3000,  # <3s requirement
                "tool_count": 4,
                "cognitive_load_level": "medium",
                "context_switching_cost": 3,
                "interruption_sensitivity": "low",
                "tools_config": {
                    "categories": [
                        "deck_building", "combo_analysis", "rules_reference"
                    ],
                    "critical_tools": [
                        "Commander Spellbook", "MTG Commander Map",
                        "MTG Scripting Toolkit"
                    ],
                    "game_formats": ["commander", "legacy", "vintage"],
                    "analysis_heavy": True
                },
                "default_view": "commander_spellbook",
                "sort_order": 3
            },
            {
                "name": "infrastructure",
                "display_name": "Infrastructure & Automation",
                "description": "12 infrastructure tools for system management",
                "icon": "server",
                "color": "#0891b2",  # Cyan
                "max_response_time_ms": 5000,  # <5s requirement
                "tool_count": 12,
                "cognitive_load_level": "high",
                "context_switching_cost": 7,
                "interruption_sensitivity": "medium",
                "tools_config": {
                    "categories": [
                        "monitoring", "deployment", "networking",
                        "virtualization", "ai_servers"
                    ],
                    "critical_tools": [
                        "Kong", "KasmVNC", "vLLM servers", "MCP servers"
                    ],
                    "requires_privileges": True,
                    "system_integration": True
                },
                "default_view": "monitoring",
                "sort_order": 4
            }
        ]

    def get_performance_tier(self) -> str:
        """Get performance tier based on response time requirement."""
        if self.max_response_time_ms <= 1000:
            return "critical"
        elif self.max_response_time_ms <= 2000:
            return "high"
        elif self.max_response_time_ms <= 3000:
            return "medium"
        else:
            return "standard"

    def is_high_cognitive_load(self) -> bool:
        """Check if domain requires high cognitive resources."""
        return self.cognitive_load_level in ["high"]

    def get_context_switching_penalty(self) -> int:
        """Get context switching penalty in milliseconds."""
        return self.context_switching_cost * 50  # Base 50ms per penalty point

    def should_minimize_interruptions(self) -> bool:
        """Check if domain is sensitive to interruptions."""
        return self.interruption_sensitivity in ["high", "critical"]

    def get_tool_categories(self) -> List[str]:
        """Get list of tool categories in this domain."""
        if not self.tools_config:
            return []
        return self.tools_config.get("categories", [])

    def get_critical_tools(self) -> List[str]:
        """Get list of critical tools in this domain."""
        if not self.tools_config:
            return []
        return self.tools_config.get("critical_tools", [])

    def supports_airgapped_operation(self) -> bool:
        """Check if domain supports airgapped operation."""
        if not self.tools_config:
            return False
        return self.tools_config.get("airgapped_capable", False)

    def requires_system_privileges(self) -> bool:
        """Check if domain requires elevated system privileges."""
        if not self.tools_config:
            return False
        return self.tools_config.get("requires_privileges", False)

    def is_executive_function_optimized(self) -> bool:
        """Check if domain is optimized for executive function support."""
        if not self.tools_config:
            return False
        return self.tools_config.get("executive_function_support", False)

    def get_navigation_config(self) -> Dict[str, Any]:
        """Get navigation configuration for this domain."""
        return self.navigation_config or {}

    def get_feature_flags(self) -> Dict[str, Any]:
        """Get feature flags for this domain."""
        return self.feature_flags or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert domain to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "display_name": self.display_name,
            "description": self.description,
            "icon": self.icon,
            "color": self.color,
            "max_response_time_ms": self.max_response_time_ms,
            "performance_tier": self.get_performance_tier(),
            "tool_count": self.tool_count,
            "cognitive_load_level": self.cognitive_load_level,
            "context_switching_cost": self.context_switching_cost,
            "context_switching_penalty_ms": self.get_context_switching_penalty(),
            "interruption_sensitivity": self.interruption_sensitivity,
            "default_view": self.default_view,
            "tool_categories": self.get_tool_categories(),
            "critical_tools": self.get_critical_tools(),
            "features": {
                "airgapped_capable": self.supports_airgapped_operation(),
                "requires_privileges": self.requires_system_privileges(),
                "executive_function_optimized": self.is_executive_function_optimized(),
                "high_cognitive_load": self.is_high_cognitive_load(),
                "minimize_interruptions": self.should_minimize_interruptions()
            },
            "is_active": self.is_active,
            "sort_order": self.sort_order
        }

    def __repr__(self) -> str:
        return (
            f"<Domain(id={self.id}, name='{self.name}', "
            f"tools={self.tool_count}, "
            f"max_response_ms={self.max_response_time_ms})>"
        )
