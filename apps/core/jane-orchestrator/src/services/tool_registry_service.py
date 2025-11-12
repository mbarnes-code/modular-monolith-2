"""
Tool Registry Service for managing 37 executive function tools.

Constitutional Requirements:
- Complete inventory of 37 tools across 4 domains
- Tool health monitoring and status tracking
- Integration status management
- Performance baseline preservation
- Cognitive load scoring for executive function support

Tool Distribution:
- Security: 13 tools (MISP, HELK, SecurityOnion, YARA-X, etc.)
- Productivity: 8 tools (Actual, Mealie, Dispatch, n8n, etc.)
- MTG: 4 tools (Commander Spellbook, MTG Commander Map, etc.)
- Infrastructure: 12 tools (Kong, KasmVNC, vLLM servers, etc.)
"""

import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ..data.models.integrated_tool import IntegratedTool

logger = logging.getLogger(__name__)


class IntegrationStatus(Enum):
    """Tool integration status levels."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    DEPRECATED = "deprecated"


class HealthStatus(Enum):
    """Tool health status levels."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
    OFFLINE = "offline"


class IntegrationType(Enum):
    """Types of tool integration."""
    ADAPTER = "adapter"           # Service adapter integration
    EMBEDDED = "embedded"         # Embedded in monolith
    MICROSERVICE = "microservice"  # Separate service
    PROXY = "proxy"              # Proxied original tool
    NATIVE = "native"            # Native rewrite


class ToolRegistryService:
    """
    Service for managing the registry of 37 executive function tools.

    Provides:
    - Tool inventory management and constitutional compliance
    - Health monitoring and status tracking
    - Integration status management
    - Performance baseline preservation
    - Cognitive load assessment for executive function support
    - Tool discovery and recommendation
    """

    def __init__(self, db: Session):
        self.db = db
        self._health_cache = {}
        self._performance_cache = {}
        self._cache_expiry = timedelta(minutes=2)
        self._last_cache_update = {}

    async def initialize_constitutional_tools(self) -> List[IntegratedTool]:
        """
        Initialize the constitutional 37-tool inventory.

        Creates or updates all required tools across 4 domains
        to maintain constitutional compliance.

        Returns:
            List of created/updated tool objects
        """
        constitutional_tools = self._get_constitutional_tool_inventory()
        created_tools = []

        for tool_data in constitutional_tools:
            # Check if tool already exists
            existing_tool = self.db.query(IntegratedTool).filter(
                IntegratedTool.name == tool_data["name"]
            ).first()

            if existing_tool:
                # Update existing tool
                for key, value in tool_data.items():
                    if hasattr(existing_tool, key):
                        setattr(existing_tool, key, value)
                existing_tool.updated_at = func.now()
                created_tools.append(existing_tool)
                logger.info(f"Updated constitutional tool: "
                            f"{tool_data['name']}")
            else:
                # Create new tool
                new_tool = IntegratedTool(**tool_data)
                self.db.add(new_tool)
                created_tools.append(new_tool)
                logger.info(f"Created constitutional tool: "
                            f"{tool_data['name']}")

        self.db.commit()
        await self._validate_constitutional_compliance()
        return created_tools

    async def get_all_tools(
        self,
        domain_filter: Optional[str] = None,
        status_filter: Optional[str] = None,
        active_only: bool = True,
        include_health: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get all tools with optional filtering.

        Args:
            domain_filter: Filter by domain name
            status_filter: Filter by integration status
            active_only: Only return active tools
            include_health: Include health and performance data

        Returns:
            List of tool dictionaries with metadata
        """
        query = self.db.query(IntegratedTool)

        # Apply filters
        if domain_filter:
            query = query.filter(IntegratedTool.domain_name == domain_filter)

        if status_filter:
            query = query.filter(
                IntegratedTool.integration_status == status_filter
            )

        if active_only:
            query = query.filter(IntegratedTool.is_active.is_(True))

        # Order by domain, then by sort order, then by name
        query = query.order_by(
            IntegratedTool.domain_name,
            IntegratedTool.sort_order,
            IntegratedTool.display_name
        )

        tools = query.all()
        result = []

        for tool in tools:
            tool_dict = tool.to_dict()

            if include_health:
                # Add real-time health status
                health_status = await self._get_tool_health_status(tool)
                tool_dict["current_health"] = health_status

                # Add performance metrics
                performance_metrics = await self._get_tool_performance(tool)
                tool_dict["performance_metrics"] = performance_metrics

                # Add cognitive load assessment
                cognitive_assessment = await self._assess_tool_cognitive_load(
                    tool
                )
                tool_dict["cognitive_assessment"] = cognitive_assessment

            result.append(tool_dict)

        return result

    async def get_tool_by_name(self, name: str) -> Optional[IntegratedTool]:
        """Get tool by name with validation."""
        return self.db.query(IntegratedTool).filter(
            and_(
                IntegratedTool.name == name,
                IntegratedTool.is_active.is_(True)
            )
        ).first()

    async def update_tool_status(
        self,
        tool_name: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update tool integration status.

        Args:
            tool_name: Name of the tool
            status: New integration status
            details: Additional status details

        Returns:
            True if update was successful
        """
        tool = await self.get_tool_by_name(tool_name)
        if not tool:
            logger.error(f"Tool not found: {tool_name}")
            return False

        old_status = tool.integration_status
        tool.integration_status = status
        tool.updated_at = func.now()

        if details:
            # Update runtime config with status details
            runtime_config = tool.runtime_config or {}
            runtime_config["status_details"] = details
            runtime_config["status_updated_at"] = datetime.utcnow().isoformat()
            tool.runtime_config = runtime_config

        self.db.commit()

        logger.info(f"Updated tool {tool_name} status: "
                    f"{old_status} -> {status}")
        return True

    async def update_tool_health(
        self,
        tool_name: str,
        health_status: str,
        metrics: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Update tool health status and metrics.

        Args:
            tool_name: Name of the tool
            health_status: New health status
            metrics: Performance metrics

        Returns:
            True if update was successful
        """
        tool = await self.get_tool_by_name(tool_name)
        if not tool:
            logger.error(f"Tool not found: {tool_name}")
            return False

        tool.update_health_status(health_status)

        if metrics:
            tool.record_performance(metrics)

        self.db.commit()

        # Clear cache for this tool
        cache_key = f"health_{tool_name}"
        if cache_key in self._health_cache:
            del self._health_cache[cache_key]

        logger.info(f"Updated tool {tool_name} health: {health_status}")
        return True

    async def get_tools_by_domain(
        self, domain_name: str
    ) -> List[Dict[str, Any]]:
        """
        Get all tools in a specific domain.

        Args:
            domain_name: Name of the domain

        Returns:
            List of tools in the domain
        """
        return await self.get_all_tools(
            domain_filter=domain_name,
            include_health=True
        )

    async def get_tool_recommendations(
        self,
        user_context: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get tool recommendations based on user context and preferences.

        Args:
            user_context: User preferences and current context
            limit: Maximum number of recommendations

        Returns:
            List of recommended tools with scores
        """
        tools = await self.get_all_tools(include_health=True)

        recommendations = []
        for tool_dict in tools:
            score = await self._calculate_recommendation_score(
                tool_dict, user_context
            )

            if score > 0:
                recommendations.append({
                    **tool_dict,
                    "recommendation_score": score,
                    "recommendation_reasons": await self._get_recommendation_reasons(
                        tool_dict, user_context
                    )
                })

        # Sort by recommendation score
        recommendations.sort(
            key=lambda x: x["recommendation_score"],
            reverse=True
        )

        return recommendations[:limit]

    async def get_registry_health_summary(self) -> Dict[str, Any]:
        """
        Get overall health summary of the tool registry.

        Returns:
            Health summary with constitutional compliance status
        """
        all_tools = await self.get_all_tools(include_health=True)

        # Constitutional compliance check
        tool_count_by_domain = {}
        healthy_tools_by_domain = {}
        total_healthy = 0
        total_integrated = 0

        for tool in all_tools:
            domain = tool["domain_name"]
            tool_count_by_domain[domain] = tool_count_by_domain.get(
                domain, 0) + 1

            if tool["current_health"]["is_healthy"]:
                healthy_tools_by_domain[domain] = (
                    healthy_tools_by_domain.get(domain, 0) + 1
                )
                total_healthy += 1

            if tool["integration_complete"]:
                total_integrated += 1

        # Check constitutional requirements
        constitutional_counts = IntegratedTool.get_constitutional_tool_count()
        constitutional_compliance = True
        compliance_issues = []

        for domain, expected_count in constitutional_counts.items():
            if domain == "total":
                continue

            actual_count = tool_count_by_domain.get(domain, 0)
            if actual_count != expected_count:
                constitutional_compliance = False
                compliance_issues.append({
                    "domain": domain,
                    "expected": expected_count,
                    "actual": actual_count,
                    "difference": actual_count - expected_count
                })

        summary = {
            "total_tools": len(all_tools),
            "constitutional_target": constitutional_counts["total"],
            "constitutional_compliance": constitutional_compliance,
            "compliance_issues": compliance_issues,
            "health_summary": {
                "total_healthy": total_healthy,
                "health_percentage": (
                    (total_healthy / len(all_tools) * 100) if all_tools else 0
                ),
                "by_domain": {}
            },
            "integration_summary": {
                "total_integrated": total_integrated,
                "integration_percentage": (
                    (total_integrated / len(all_tools) * 100) if all_tools else 0
                )
            },
            "domain_breakdown": tool_count_by_domain,
            "summary_timestamp": datetime.utcnow().isoformat()
        }

        # Add domain-specific health data
        for domain, count in tool_count_by_domain.items():
            healthy_count = healthy_tools_by_domain.get(domain, 0)
            summary["health_summary"]["by_domain"][domain] = {
                "total_tools": count,
                "healthy_tools": healthy_count,
                "health_percentage": (
                    (healthy_count / count * 100) if count > 0 else 0
                )
            }

        return summary

    async def search_tools(
        self,
        query: str,
        domain_filter: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search tools by name, description, or features.

        Args:
            query: Search query string
            domain_filter: Optional domain filter
            limit: Maximum number of results

        Returns:
            List of matching tools with relevance scores
        """
        # Simple text search implementation
        # In production, this could use full-text search
        all_tools = await self.get_all_tools(
            domain_filter=domain_filter,
            include_health=True
        )

        query_lower = query.lower()
        matches = []

        for tool in all_tools:
            relevance_score = 0

            # Check name match (highest weight)
            if query_lower in tool["name"].lower():
                relevance_score += 10

            # Check display name match
            if query_lower in tool["display_name"].lower():
                relevance_score += 8

            # Check description match
            if tool.get("description") and query_lower in tool["description"].lower():
                relevance_score += 5

            # Check technology stack match
            tech_stack = tool.get("technology_stack", {})
            for key, value in tech_stack.items():
                if isinstance(value, str) and query_lower in value.lower():
                    relevance_score += 3

            # Check features match
            features = tool.get("features", {})
            for key, value in features.items():
                if isinstance(value, str) and query_lower in value.lower():
                    relevance_score += 2

            if relevance_score > 0:
                matches.append({
                    **tool,
                    "relevance_score": relevance_score
                })

        # Sort by relevance score
        matches.sort(key=lambda x: x["relevance_score"], reverse=True)

        return matches[:limit]

    def _get_constitutional_tool_inventory(self) -> List[Dict[str, Any]]:
        """Get the constitutional 37-tool inventory definition."""
        # This would be loaded from configuration or database
        # For now, returning a sample of the constitutional tools
        return [
            # Security Domain (13 tools)
            {
                "name": "misp",
                "display_name": "MISP Threat Intelligence",
                "domain_name": "security",
                "description": "Threat intelligence platform for sharing, storing and correlating IoCs",
                "technology_stack": {"primary": "PHP", "database": "MySQL", "frontend": "Bootstrap"},
                "integration_type": "adapter",
                "cognitive_load": "high",
                "adhd_friendly": False,
                "autism_friendly": False,
                "sort_order": 1
            },
            {
                "name": "helk",
                "display_name": "HELK Analytics",
                "domain_name": "security",
                "description": "Hunting ELK stack for threat hunting and security analytics",
                "technology_stack": {"primary": "Python", "database": "Elasticsearch", "frontend": "Kibana"},
                "integration_type": "adapter",
                "cognitive_load": "high",
                "adhd_friendly": False,
                "autism_friendly": True,
                "sort_order": 2
            },
            # Productivity Domain (8 tools)
            {
                "name": "actual_budget",
                "display_name": "Actual Budget",
                "domain_name": "productivity",
                "description": "Personal finance and budgeting tool with bank sync",
                "technology_stack": {"primary": "Node.js", "database": "SQLite", "frontend": "React"},
                "integration_type": "embedded",
                "cognitive_load": "medium",
                "adhd_friendly": True,
                "autism_friendly": True,
                "sort_order": 1
            },
            {
                "name": "mealie",
                "display_name": "Mealie Recipe Manager",
                "domain_name": "productivity",
                "description": "Recipe management and meal planning application",
                "technology_stack": {"primary": "Python", "database": "PostgreSQL", "frontend": "Vue.js"},
                "integration_type": "adapter",
                "cognitive_load": "low",
                "adhd_friendly": True,
                "autism_friendly": True,
                "sort_order": 2
            },
            # MTG Domain (4 tools)
            {
                "name": "commander_spellbook",
                "display_name": "Commander Spellbook",
                "domain_name": "mtg",
                "description": "Magic: The Gathering combo database and analysis",
                "technology_stack": {"primary": "Python", "database": "PostgreSQL", "frontend": "Django"},
                "integration_type": "adapter",
                "cognitive_load": "medium",
                "adhd_friendly": False,
                "autism_friendly": True,
                "sort_order": 1
            },
            # Infrastructure Domain (12 tools)
            {
                "name": "kong",
                "display_name": "Kong Gateway",
                "domain_name": "infrastructure",
                "description": "API gateway and service mesh platform",
                "technology_stack": {"primary": "Lua", "database": "PostgreSQL", "framework": "OpenResty"},
                "integration_type": "proxy",
                "cognitive_load": "high",
                "adhd_friendly": False,
                "autism_friendly": False,
                "sort_order": 1
            },
            {
                "name": "n8n",
                "display_name": "n8n Workflow Automation",
                "domain_name": "infrastructure",
                "description": "Workflow automation platform with 400+ integrations",
                "technology_stack": {"primary": "TypeScript", "database": "PostgreSQL", "frontend": "Vue.js"},
                "integration_type": "embedded",
                "cognitive_load": "medium",
                "adhd_friendly": True,
                "autism_friendly": True,
                "sort_order": 2
            }
        ]

    async def _validate_constitutional_compliance(self) -> bool:
        """Validate that we have the constitutional 37 tools."""
        tool_counts = {}
        all_tools = self.db.query(IntegratedTool).filter(
            IntegratedTool.is_active.is_(True)
        ).all()

        for tool in all_tools:
            domain = tool.domain_name
            tool_counts[domain] = tool_counts.get(domain, 0) + 1

        constitutional_counts = IntegratedTool.get_constitutional_tool_count()

        is_compliant = True
        for domain, expected in constitutional_counts.items():
            if domain == "total":
                continue
            actual = tool_counts.get(domain, 0)
            if actual != expected:
                logger.warning(f"Constitutional compliance issue: "
                               f"Domain {domain} has {actual} tools, "
                               f"expected {expected}")
                is_compliant = False

        return is_compliant

    async def _get_tool_health_status(
        self, tool: IntegratedTool
    ) -> Dict[str, Any]:
        """Get current health status of a tool (cached)."""
        cache_key = f"health_{tool.name}"

        if self._is_cache_valid(cache_key):
            return self._health_cache[cache_key]

        # In production, this would perform actual health checks
        health_status = {
            "status": tool.health_status,
            "is_healthy": tool.is_healthy(),
            "last_check": (
                tool.last_health_check.isoformat()
                if tool.last_health_check else None
            ),
            "check_timestamp": datetime.utcnow().isoformat()
        }

        # Cache the result
        self._health_cache[cache_key] = health_status
        self._last_cache_update[cache_key] = datetime.utcnow()

        return health_status

    async def _get_tool_performance(
        self, tool: IntegratedTool
    ) -> Dict[str, Any]:
        """Get performance metrics for a tool."""
        return {
            "performance_score": tool.get_performance_score(),
            "baseline_preserved": tool.business_logic_preserved,
            "current_metrics": tool.current_performance,
            "baseline_metrics": tool.performance_baseline
        }

    async def _assess_tool_cognitive_load(
        self, tool: IntegratedTool
    ) -> Dict[str, Any]:
        """Assess cognitive load for executive function support."""
        return {
            "cognitive_load": tool.cognitive_load,
            "cognitive_load_score": tool.get_cognitive_load_score(),
            "executive_function_support": tool.supports_executive_function(),
            "adhd_friendly": tool.adhd_friendly,
            "autism_friendly": tool.autism_friendly,
            "accessibility_features": tool.accessibility_features or {}
        }

    async def _calculate_recommendation_score(
        self,
        tool: Dict[str, Any],
        user_context: Optional[Dict[str, Any]]
    ) -> float:
        """Calculate recommendation score for a tool."""
        score = 0.0

        # Base score from tool health and integration status
        if tool.get("current_health", {}).get("is_healthy"):
            score += 2.0

        if tool.get("integration_complete"):
            score += 1.0

        # Executive function accommodations
        if user_context and user_context.get("needs_executive_function_support"):
            if tool.get("cognitive_assessment", {}).get("adhd_friendly"):
                score += 3.0
            if tool.get("cognitive_assessment", {}).get("autism_friendly"):
                score += 3.0

        # Cognitive load considerations
        cognitive_load = tool.get("cognitive_load", "medium")
        if user_context and user_context.get("prefer_low_cognitive_load"):
            if cognitive_load == "low":
                score += 2.0
            elif cognitive_load == "high":
                score -= 1.0

        # Domain preferences
        if user_context and user_context.get("preferred_domains"):
            preferred_domains = user_context["preferred_domains"]
            if tool.get("domain_name") in preferred_domains:
                score += 1.0

        return score

    async def _get_recommendation_reasons(
        self,
        tool: Dict[str, Any],
        user_context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Get reasons why a tool is recommended."""
        reasons = []

        if tool.get("current_health", {}).get("is_healthy"):
            reasons.append("Tool is currently healthy and operational")

        if tool.get("integration_complete"):
            reasons.append(
                "Integration is complete with preserved functionality")

        if tool.get("cognitive_assessment", {}).get("adhd_friendly"):
            reasons.append("ADHD-friendly interface and interactions")

        if tool.get("cognitive_assessment", {}).get("autism_friendly"):
            reasons.append(
                "Autism-friendly interface with predictable patterns")

        cognitive_load = tool.get("cognitive_load", "medium")
        if cognitive_load == "low":
            reasons.append("Low cognitive load for easy use")

        return reasons

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        if cache_key not in self._health_cache:
            return False

        if cache_key not in self._last_cache_update:
            return False

        cache_age = datetime.utcnow() - self._last_cache_update[cache_key]
        return cache_age < self._cache_expiry

    def clear_cache(self) -> None:
        """Clear health and performance cache."""
        self._health_cache.clear()
        self._performance_cache.clear()
        self._last_cache_update.clear()
        logger.info("Tool registry service cache cleared")
