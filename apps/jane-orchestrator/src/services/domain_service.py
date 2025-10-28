"""
Domain Service for managing 4-domain organization and performance tiers.

Constitutional Requirements:
- Security Domain: 13 tools, <1s response time, high cognitive load
- Productivity Domain: 8 tools, <2s response time, executive function support
- MTG Domain: 4 tools, <3s response time, analysis-heavy workflows
- Infrastructure Domain: 12 tools, <5s response time, system-level operations

Executive Function Support:
- Context switching cost tracking and minimization
- Cognitive load assessment and accommodation
- Interruption sensitivity management
- Performance tier enforcement
"""

import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from ..data.models.domain import Domain
from ..data.models.integrated_tool import IntegratedTool

logger = logging.getLogger(__name__)


class PerformanceTier(Enum):
    """Constitutional performance tiers for domains."""
    CRITICAL = "critical"      # <1s (Security)
    HIGH = "high"             # <2s (Productivity)
    MEDIUM = "medium"         # <3s (MTG)
    STANDARD = "standard"     # <5s (Infrastructure)


class CognitiveLoadLevel(Enum):
    """Cognitive load levels for executive function support."""
    LOW = "low"              # Simple, routine tasks
    MEDIUM = "medium"        # Moderate complexity
    HIGH = "high"            # Complex, demanding tasks


class DomainService:
    """
    Service for managing domain organization and constitutional requirements.

    Provides:
    - 4-domain structure management
    - Performance tier enforcement
    - Executive function accommodations
    - Context switching optimization
    - Tool organization within domains
    """

    def __init__(self, db: Session):
        self.db = db
        self._performance_cache = {}
        self._cache_expiry = timedelta(minutes=5)
        self._last_cache_update = {}

    async def initialize_constitutional_domains(self) -> List[Domain]:
        """
        Initialize the constitutional 4-domain structure.

        Returns:
            List of created/updated domain objects
        """
        constitutional_domains = Domain.get_constitutional_domains()
        created_domains = []

        for domain_data in constitutional_domains:
            # Check if domain already exists
            existing_domain = self.db.query(Domain).filter(
                Domain.name == domain_data["name"]
            ).first()

            if existing_domain:
                # Update existing domain with constitutional requirements
                for key, value in domain_data.items():
                    if hasattr(existing_domain, key):
                        setattr(existing_domain, key, value)
                existing_domain.updated_at = func.now()
                created_domains.append(existing_domain)
                logger.info(f"Updated constitutional domain: "
                            f"{domain_data['name']}")
            else:
                # Create new domain
                new_domain = Domain(**domain_data)
                self.db.add(new_domain)
                created_domains.append(new_domain)
                logger.info(f"Created constitutional domain: "
                            f"{domain_data['name']}")

        self.db.commit()
        return created_domains

    async def get_all_domains(
        self,
        active_only: bool = True,
        include_stats: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get all domains with optional statistics and tool counts.

        Args:
            active_only: Only return active domains
            include_stats: Include tool counts and performance stats

        Returns:
            List of domain dictionaries with metadata
        """
        query = self.db.query(Domain)

        if active_only:
            query = query.filter(Domain.is_active.is_(True))

        query = query.order_by(Domain.sort_order, Domain.name)
        domains = query.all()

        result = []
        for domain in domains:
            domain_dict = domain.to_dict()

            if include_stats:
                # Add real-time tool count
                tool_count = self.db.query(IntegratedTool).filter(
                    and_(
                        IntegratedTool.domain_name == domain.name,
                        IntegratedTool.is_active.is_(True)
                    )
                ).count()
                domain_dict["actual_tool_count"] = tool_count

                # Add performance statistics
                performance_stats = await self._get_domain_performance_stats(
                    domain.name
                )
                domain_dict["performance_stats"] = performance_stats

                # Add context switching metrics
                context_metrics = await self._get_context_switching_metrics(
                    domain.name
                )
                domain_dict["context_metrics"] = context_metrics

            result.append(domain_dict)

        return result

    async def get_domain_by_name(self, name: str) -> Optional[Domain]:
        """Get domain by name with validation."""
        return self.db.query(Domain).filter(
            and_(Domain.name == name, Domain.is_active.is_(True))
        ).first()

    async def get_domain_tools(
        self,
        domain_name: str,
        active_only: bool = True,
        include_health: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Get all tools in a specific domain.

        Args:
            domain_name: Name of the domain
            active_only: Only return active tools
            include_health: Include health status and performance metrics

        Returns:
            List of tools in the domain
        """
        query = self.db.query(IntegratedTool).filter(
            IntegratedTool.domain_name == domain_name
        )

        if active_only:
            query = query.filter(IntegratedTool.is_active.is_(True))

        query = query.order_by(
            IntegratedTool.sort_order,
            IntegratedTool.display_name
        )

        tools = query.all()
        result = []

        for tool in tools:
            tool_dict = tool.to_dict()

            if include_health:
                # Add real-time health check
                health_status = await self._check_tool_health(tool)
                tool_dict["current_health"] = health_status

                # Add performance metrics
                performance_metrics = await self._get_tool_performance_metrics(
                    tool
                )
                tool_dict["performance_metrics"] = performance_metrics

            result.append(tool_dict)

        return result

    async def assess_cognitive_load(
        self,
        domain_name: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Assess cognitive load for a domain transition.

        Args:
            domain_name: Target domain name
            user_context: Current user context and preferences

        Returns:
            Cognitive load assessment with recommendations
        """
        domain = await self.get_domain_by_name(domain_name)
        if not domain:
            raise ValueError(f"Domain not found: {domain_name}")

        # Base cognitive load from domain
        base_load = domain.get_cognitive_load_score()

        # Context switching penalty
        context_penalty = domain.get_context_switching_penalty()

        # User-specific adjustments
        user_adjustments = 0
        if user_context:
            # ADHD/autism accommodations
            if user_context.get("adhd_accommodations", {}).get("reduce_cognitive_load"):
                user_adjustments -= 2

            # Current focus state
            if user_context.get("current_focus_state") == "deep_work":
                context_penalty *= 2  # Higher penalty for interrupting deep work

        total_load = max(1, base_load + user_adjustments)

        # Generate recommendations
        recommendations = []
        if total_load >= 7:
            recommendations.append("Consider break before domain switch")
            recommendations.append(
                "Enable focus mode to minimize interruptions")

        if context_penalty > 250:  # >250ms penalty
            recommendations.append(
                "High context switching cost - batch similar tasks")

        if domain.should_minimize_interruptions():
            recommendations.append(
                "Domain sensitive to interruptions - enable quiet mode")

        return {
            "domain_name": domain_name,
            "cognitive_load_score": total_load,
            "cognitive_load_level": domain.cognitive_load_level,
            "context_switching_penalty_ms": context_penalty,
            "performance_tier": domain.get_performance_tier(),
            "max_response_time_ms": domain.max_response_time_ms,
            "interruption_sensitivity": domain.interruption_sensitivity,
            "recommendations": recommendations,
            "executive_function_optimized": domain.is_executive_function_optimized(),
            "assessment_timestamp": datetime.utcnow().isoformat()
        }

    async def validate_performance_requirements(
        self,
        domain_name: str,
        response_time_ms: int
    ) -> Dict[str, Any]:
        """
        Validate if response time meets constitutional requirements.

        Args:
            domain_name: Domain to validate
            response_time_ms: Actual response time in milliseconds

        Returns:
            Validation result with compliance status
        """
        domain = await self.get_domain_by_name(domain_name)
        if not domain:
            raise ValueError(f"Domain not found: {domain_name}")

        max_allowed = domain.max_response_time_ms
        is_compliant = response_time_ms <= max_allowed

        performance_tier = domain.get_performance_tier()

        # Calculate performance score (1.0 = exactly at limit)
        performance_score = response_time_ms / max_allowed

        # Determine severity if non-compliant
        severity = "compliant"
        if not is_compliant:
            if performance_score <= 1.5:
                severity = "warning"  # 50% over limit
            elif performance_score <= 2.0:
                severity = "critical"  # 100% over limit
            else:
                severity = "failure"  # >100% over limit

        return {
            "domain_name": domain_name,
            "performance_tier": performance_tier,
            "max_allowed_ms": max_allowed,
            "actual_response_ms": response_time_ms,
            "is_compliant": is_compliant,
            "performance_score": performance_score,
            "severity": severity,
            "validation_timestamp": datetime.utcnow().isoformat()
        }

    async def get_domain_health_summary(self) -> Dict[str, Any]:
        """
        Get overall health summary across all domains.

        Returns:
            Health summary with metrics and alerts
        """
        domains = await self.get_all_domains(include_stats=True)

        summary = {
            "total_domains": len(domains),
            "total_tools": sum(d.get("actual_tool_count", 0) for d in domains),
            "constitutional_compliance": True,
            "performance_issues": [],
            "cognitive_load_warnings": [],
            "domain_health": {},
            "summary_timestamp": datetime.utcnow().isoformat()
        }

        for domain in domains:
            domain_name = domain["name"]

            # Check constitutional tool count
            expected_count = domain.get("tool_count", 0)
            actual_count = domain.get("actual_tool_count", 0)

            if actual_count != expected_count:
                summary["constitutional_compliance"] = False
                summary["performance_issues"].append({
                    "domain": domain_name,
                    "issue": "tool_count_mismatch",
                    "expected": expected_count,
                    "actual": actual_count
                })

            # Check cognitive load levels
            if domain.get("cognitive_load_level") == "high":
                summary["cognitive_load_warnings"].append({
                    "domain": domain_name,
                    "warning": "high_cognitive_load",
                    "context_switching_cost": domain.get("context_switching_cost", 0)
                })

            # Domain-specific health metrics
            performance_stats = domain.get("performance_stats", {})
            summary["domain_health"][domain_name] = {
                "tool_count": actual_count,
                "performance_tier": domain.get("performance_tier"),
                "avg_response_time_ms": performance_stats.get("avg_response_time_ms"),
                "is_compliant": performance_stats.get("is_compliant", True),
                "cognitive_load_level": domain.get("cognitive_load_level")
            }

        return summary

    async def _get_domain_performance_stats(
        self, domain_name: str
    ) -> Dict[str, Any]:
        """Get performance statistics for a domain (cached)."""
        cache_key = f"perf_{domain_name}"

        # Check cache
        if self._is_cache_valid(cache_key):
            return self._performance_cache[cache_key]

        # Query performance data
        tools = self.db.query(IntegratedTool).filter(
            and_(
                IntegratedTool.domain_name == domain_name,
                IntegratedTool.is_active.is_(True)
            )
        ).all()

        response_times = []
        healthy_tools = 0

        for tool in tools:
            if tool.current_performance:
                response_time = tool.current_performance.get(
                    "avg_response_time_ms")
                if response_time:
                    response_times.append(response_time)

            if tool.is_healthy():
                healthy_tools += 1

        stats = {
            "total_tools": len(tools),
            "healthy_tools": healthy_tools,
            "health_percentage": (healthy_tools / len(tools) * 100) if tools else 0
        }

        if response_times:
            avg_response = sum(response_times) / len(response_times)
            stats.update({
                "avg_response_time_ms": avg_response,
                "min_response_time_ms": min(response_times),
                "max_response_time_ms": max(response_times),
                "response_time_count": len(response_times)
            })

            # Check compliance
            domain = await self.get_domain_by_name(domain_name)
            if domain:
                stats["is_compliant"] = avg_response <= domain.max_response_time_ms

        # Cache results
        self._performance_cache[cache_key] = stats
        self._last_cache_update[cache_key] = datetime.utcnow()

        return stats

    async def _get_context_switching_metrics(
        self, domain_name: str
    ) -> Dict[str, Any]:
        """Get context switching metrics for a domain."""
        domain = await self.get_domain_by_name(domain_name)
        if not domain:
            return {}

        return {
            "context_switching_cost": domain.context_switching_cost,
            "context_switching_penalty_ms": domain.get_context_switching_penalty(),
            "interruption_sensitivity": domain.interruption_sensitivity,
            "minimize_interruptions": domain.should_minimize_interruptions()
        }

    async def _check_tool_health(self, tool: IntegratedTool) -> Dict[str, Any]:
        """Check current health status of a tool."""
        # This would integrate with actual health check systems
        # For now, return cached health status
        return {
            "status": tool.health_status,
            "last_check": tool.last_health_check.isoformat() if tool.last_health_check else None,
            "is_healthy": tool.is_healthy()
        }

    async def _get_tool_performance_metrics(
        self, tool: IntegratedTool
    ) -> Dict[str, Any]:
        """Get performance metrics for a specific tool."""
        metrics = {
            "performance_score": tool.get_performance_score(),
            "cognitive_load": tool.cognitive_load,
            "cognitive_load_score": tool.get_cognitive_load_score()
        }

        if tool.current_performance:
            metrics["current"] = tool.current_performance

        if tool.performance_baseline:
            metrics["baseline"] = tool.performance_baseline

        return metrics

    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid."""
        if cache_key not in self._performance_cache:
            return False

        if cache_key not in self._last_cache_update:
            return False

        cache_age = datetime.utcnow() - self._last_cache_update[cache_key]
        return cache_age < self._cache_expiry

    def clear_cache(self) -> None:
        """Clear performance cache (for testing or manual refresh)."""
        self._performance_cache.clear()
        self._last_cache_update.clear()
        logger.info("Domain service cache cleared")
