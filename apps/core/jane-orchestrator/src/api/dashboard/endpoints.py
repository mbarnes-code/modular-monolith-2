"""
Dashboard API endpoints for unified access to 37 executive function tools.

Constitutional Requirements:
- Unified interface across all 4 domains
- Performance tier compliance (<200ms UI response)
- Executive function accommodations (ADHD/autism support)
- Domain navigation and tool discovery
"""

import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ...db.session import get_db
from ...services.domain_service import DomainService
from ...services.tool_registry_service import ToolRegistryService
from ..deps import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", summary="Get dashboard overview")
async def get_dashboard_overview(
    include_health: bool = Query(True, description="Include health metrics"),
    include_performance: bool = Query(
        True, description="Include performance data"
    ),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get unified dashboard overview with all domains and tools.

    Executive Function Features:
    - Single unified view reducing context switching
    - Health status for cognitive load assessment
    - Performance data for constitutional compliance
    - Domain organization for structured navigation
    """
    try:
        domain_service = DomainService(db)
        tool_service = ToolRegistryService(db)

        # Get all domains with statistics
        domains = await domain_service.get_all_domains(
            include_stats=include_health
        )

        # Get tool registry health summary
        registry_health = await tool_service.get_registry_health_summary()

        # Get personalized tool recommendations
        user_context = {
            "user_id": current_user.get("id"),
            "needs_executive_function_support": True,
            "prefer_low_cognitive_load": current_user.get(
                "adhd_accommodations", {}
            ).get("reduce_cognitive_load", False),
            "preferred_domains": current_user.get("preferred_domains", [])
        }

        recommendations = await tool_service.get_tool_recommendations(
            user_context=user_context,
            limit=8
        )

        # Calculate overall system health
        overall_health = _calculate_overall_health(domains, registry_health)

        return {
            "user_id": current_user.get("id"),
            "dashboard_timestamp": registry_health["summary_timestamp"],
            "overall_health": overall_health,
            "constitutional_compliance": (
                registry_health["constitutional_compliance"]
            ),
            "domains": domains,
            "tool_summary": {
                "total_tools": registry_health["total_tools"],
                "healthy_tools": (
                    registry_health["health_summary"]["total_healthy"]
                ),
                "integrated_tools": (
                    registry_health["integration_summary"]["total_integrated"]
                ),
                "constitutional_target": (
                    registry_health["constitutional_target"]
                )
            },
            "recommendations": recommendations,
            "quick_actions": _get_quick_actions(domains),
            "executive_function_features": {
                "context_switching_reduction": True,
                "cognitive_load_assessment": True,
                "adhd_accommodations": True,
                "autism_accommodations": True
            }
        }

    except Exception as e:
        logger.error(f"Error getting dashboard overview: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve dashboard overview"
        )


@router.get("/domains", summary="Get all domains")
async def get_domains(
    active_only: bool = Query(True, description="Only active domains"),
    include_stats: bool = Query(True, description="Include statistics"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get all domains with tool counts and performance metrics.

    Constitutional compliance:
    - Security: 13 tools, <1s response
    - Productivity: 8 tools, <2s response
    - MTG: 4 tools, <3s response
    - Infrastructure: 12 tools, <5s response
    """
    try:
        domain_service = DomainService(db)

        domains = await domain_service.get_all_domains(
            active_only=active_only,
            include_stats=include_stats
        )

        return {
            "domains": domains,
            "total_domains": len(domains),
            "constitutional_structure": {
                "security": {"target_tools": 13, "max_response_ms": 1000},
                "productivity": {"target_tools": 8, "max_response_ms": 2000},
                "mtg": {"target_tools": 4, "max_response_ms": 3000},
                "infrastructure": {"target_tools": 12, "max_response_ms": 5000}
            }
        }

    except Exception as e:
        logger.error(f"Error getting domains: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve domains"
        )


@router.get("/domains/{domain_name}", summary="Get domain details")
async def get_domain_details(
    domain_name: str,
    include_tools: bool = Query(True, description="Include domain tools"),
    include_health: bool = Query(True, description="Include health data"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get detailed information about a specific domain.

    Includes:
    - Domain metadata and configuration
    - Tool inventory and health status
    - Performance metrics and compliance
    - Cognitive load assessment
    """
    try:
        domain_service = DomainService(db)
        tool_service = ToolRegistryService(db)

        # Get domain details
        domain = await domain_service.get_domain_by_name(domain_name)
        if not domain:
            raise HTTPException(
                status_code=404,
                detail=f"Domain not found: {domain_name}"
            )

        domain_dict = domain.to_dict()

        if include_tools:
            # Get tools in this domain
            tools = await tool_service.get_tools_by_domain(domain_name)
            domain_dict["tools"] = tools

        if include_health:
            # Get cognitive load assessment
            user_context = {
                "adhd_accommodations": current_user.get(
                    "adhd_accommodations", {}
                ),
                "current_focus_state": "normal"  # Could be from user context
            }

            cognitive_assessment = await domain_service.assess_cognitive_load(
                domain_name, user_context
            )
            domain_dict["cognitive_assessment"] = cognitive_assessment

        return domain_dict

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting domain {domain_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve domain: {domain_name}"
        )


@router.get("/tools", summary="Get all tools")
async def get_tools(
    domain: Optional[str] = Query(None, description="Filter by domain"),
    status: Optional[str] = Query(None, description="Filter by status"),
    active_only: bool = Query(True, description="Only active tools"),
    include_health: bool = Query(True, description="Include health data"),
    limit: int = Query(50, le=100, description="Maximum results"),
    offset: int = Query(0, ge=0, description="Results offset"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get all tools with optional filtering and pagination.

    Supports:
    - Domain-based filtering
    - Status-based filtering
    - Health and performance data
    - Executive function accommodations
    """
    try:
        tool_service = ToolRegistryService(db)

        tools = await tool_service.get_all_tools(
            domain_filter=domain,
            status_filter=status,
            active_only=active_only,
            include_health=include_health
        )

        # Apply pagination
        total_tools = len(tools)
        paginated_tools = tools[offset:offset + limit]

        return {
            "tools": paginated_tools,
            "pagination": {
                "total": total_tools,
                "limit": limit,
                "offset": offset,
                "has_more": offset + limit < total_tools
            },
            "filters": {
                "domain": domain,
                "status": status,
                "active_only": active_only
            }
        }

    except Exception as e:
        logger.error(f"Error getting tools: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve tools"
        )


@router.get("/tools/{tool_name}", summary="Get tool details")
async def get_tool_details(
    tool_name: str,
    include_performance: bool = Query(
        True, description="Include performance metrics"
    ),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get detailed information about a specific tool.

    Includes:
    - Tool metadata and configuration
    - Health and performance status
    - Integration details
    - Executive function accommodations
    """
    try:
        tool_service = ToolRegistryService(db)

        tool = await tool_service.get_tool_by_name(tool_name)
        if not tool:
            raise HTTPException(
                status_code=404,
                detail=f"Tool not found: {tool_name}"
            )

        tool_dict = tool.to_dict()

        if include_performance:
            # Add detailed performance metrics (placeholder)
            performance_metrics = {
                "response_time_ms": 150,
                "health_score": 95,
                "last_check": tool.updated_at
            }
            tool_dict["detailed_performance"] = performance_metrics

            # Add cognitive load assessment (placeholder)
            cognitive_assessment = {
                "cognitive_load_score": 3,
                "complexity_rating": "medium",
                "executive_function_support": True
            }
            tool_dict["cognitive_assessment"] = cognitive_assessment

        return tool_dict

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting tool {tool_name}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve tool: {tool_name}"
        )


@router.get("/search", summary="Search tools and domains")
async def search_dashboard(
    q: str = Query(..., min_length=2, description="Search query"),
    domain: Optional[str] = Query(None, description="Search within domain"),
    limit: int = Query(20, le=50, description="Maximum results"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Search across tools and domains for executive function support.

    Features:
    - Fuzzy search across names, descriptions, and features
    - Domain-scoped search
    - Relevance scoring
    - Executive function context awareness
    """
    try:
        tool_service = ToolRegistryService(db)

        # Search tools
        tools = await tool_service.search_tools(
            query=q,
            domain_filter=domain,
            limit=limit
        )

        # Search domains (simple implementation)
        domain_service = DomainService(db)
        all_domains = await domain_service.get_all_domains(include_stats=False)

        q_lower = q.lower()
        matching_domains = []

        for domain_dict in all_domains:
            relevance = 0
            if q_lower in domain_dict["name"].lower():
                relevance += 10
            if q_lower in domain_dict["display_name"].lower():
                relevance += 8
            desc = domain_dict.get("description")
            if desc and q_lower in desc.lower():
                relevance += 5

            if relevance > 0:
                matching_domains.append({
                    **domain_dict,
                    "relevance_score": relevance
                })

        # Sort domains by relevance
        matching_domains.sort(key=lambda x: x["relevance_score"], reverse=True)

        return {
            "query": q,
            "domain_filter": domain,
            "results": {
                "tools": tools,
                "domains": matching_domains[:5]  # Limit domain results
            },
            "total_results": len(tools) + len(matching_domains)
        }

    except Exception as e:
        logger.error(f"Error searching dashboard: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Search failed"
        )


@router.get("/recommendations", summary="Get personalized recommendations")
async def get_recommendations(
    limit: int = Query(10, le=20, description="Maximum recommendations"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get personalized tool recommendations based on user preferences.

    Considers:
    - Executive function needs (ADHD/autism accommodations)
    - Cognitive load preferences
    - Domain preferences
    - Tool health and integration status
    """
    try:
        tool_service = ToolRegistryService(db)

        # Build user context from profile
        user_context = {
            "user_id": current_user.get("id"),
            "needs_executive_function_support": True,
            "prefer_low_cognitive_load": current_user.get(
                "adhd_accommodations", {}
            ).get("reduce_cognitive_load", False),
            "preferred_domains": current_user.get("preferred_domains", []),
            "autism_accommodations": current_user.get(
                "autism_accommodations", {}
            ),
            "adhd_accommodations": current_user.get("adhd_accommodations", {})
        }

        recommendations = await tool_service.get_tool_recommendations(
            user_context=user_context,
            limit=limit
        )

        return {
            "user_id": current_user.get("id"),
            "recommendations": recommendations,
            "user_context": {
                "executive_function_support": (
                    user_context["needs_executive_function_support"]
                ),
                "low_cognitive_load_preference": (
                    user_context["prefer_low_cognitive_load"]
                ),
                "preferred_domains": user_context["preferred_domains"]
            },
            "recommendation_timestamp": None
        }

    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get recommendations"
        )


@router.get("/health", summary="Get dashboard health status")
async def get_dashboard_health(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get comprehensive health status of the dashboard and all systems.

    Includes:
    - Constitutional compliance status
    - Domain-specific health metrics
    - Performance tier compliance
    - Tool integration status
    """
    try:
        domain_service = DomainService(db)
        tool_service = ToolRegistryService(db)

        # Get domain health summary
        domain_health = await domain_service.get_domain_health_summary()

        # Get tool registry health
        registry_health = await tool_service.get_registry_health_summary()

        # Calculate overall system health score
        overall_health = _calculate_overall_health(
            [domain_health], registry_health
        )

        return {
            "overall_health": overall_health,
            "constitutional_compliance": registry_health["constitutional_compliance"],
            "domain_health": domain_health,
            "registry_health": registry_health,
            "system_status": {
                "dashboard_operational": True,
                "all_domains_active": domain_health["total_domains"] == 4,
                "constitutional_tool_count": registry_health["total_tools"] == 37,
                "health_check_timestamp": registry_health["summary_timestamp"]
            }
        }

    except Exception as e:
        logger.error(f"Error getting dashboard health: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve health status"
        )


def _calculate_overall_health(
    domains: List[Dict], registry_health: Dict
) -> Dict[str, Any]:
    """Calculate overall system health score."""
    try:
        # Health percentage from registry
        health_pct = registry_health["health_summary"]["health_percentage"]

        # Integration percentage
        integration_pct = registry_health[
            "integration_summary"
        ]["integration_percentage"]

        # Constitutional compliance
        compliance_score = (
            100 if registry_health["constitutional_compliance"] else 0
        )

        # Weighted overall score
        overall_score = (
            health_pct * 0.4 +           # 40% health
            integration_pct * 0.4 +     # 40% integration
            compliance_score * 0.2      # 20% compliance
        )

        # Determine status
        if overall_score >= 90:
            status = "excellent"
        elif overall_score >= 75:
            status = "good"
        elif overall_score >= 50:
            status = "fair"
        else:
            status = "poor"

        return {
            "score": round(overall_score, 1),
            "status": status,
            "health_percentage": health_pct,
            "integration_percentage": integration_pct,
            "constitutional_compliance": (
                registry_health["constitutional_compliance"]
            )
        }

    except Exception as e:
        logger.error(f"Error calculating overall health: {str(e)}")
        return {
            "score": 0,
            "status": "unknown",
            "health_percentage": 0,
            "integration_percentage": 0,
            "constitutional_compliance": False
        }


def _get_quick_actions(domains: List[Dict]) -> List[Dict[str, Any]]:
    """Get quick action recommendations based on domain status."""
    actions = []

    for domain in domains:
        domain_name = domain["name"]

        # Add domain navigation action
        actions.append({
            "id": f"navigate_{domain_name}",
            "title": f"Open {domain['display_name']}",
            "description": (
                f"Access {domain['tool_count']} tools in "
                f"{domain_name} domain"
            ),
            "action_type": "navigation",
            "target": f"/domains/{domain_name}",
            "icon": domain.get("icon", "folder"),
            "color": domain.get("color", "#6b7280")
        })

        # Add health-related actions if needed
        perf_stats = domain.get("performance_stats", {})
        if perf_stats.get("health_percentage", 100) < 80:
            actions.append({
                "id": f"health_check_{domain_name}",
                "title": f"Check {domain['display_name']} Health",
                "description": "Some tools in this domain need attention",
                "action_type": "health_check",
                "target": f"/domains/{domain_name}/health",
                "icon": "exclamation-triangle",
                "color": "#f59e0b"
            })

    return actions[:6]  # Limit to 6 quick actions
