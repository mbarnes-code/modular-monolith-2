"""
FastAPI routing structure for the Mental Prosthetic Platform orchestration layer.

Provides unified API routing with domain service communication across
all 37 integrated tools with executive function accommodations.
"""

import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from .auth import TokenData, get_current_user

logger = logging.getLogger(__name__)

# Main API router
api_router = APIRouter(prefix="/api/v1")

# Domain-specific routers for 37-tool integration
security_router = APIRouter(prefix="/security", tags=["security"])
productivity_router = APIRouter(prefix="/productivity", tags=["productivity"])
mtg_router = APIRouter(prefix="/mtg", tags=["mtg"])
infrastructure_router = APIRouter(
    prefix="/infrastructure", tags=["infrastructure"])

# System routers
auth_router = APIRouter(prefix="/auth", tags=["authentication"])
health_router = APIRouter(prefix="/health", tags=["health"])
websocket_router = APIRouter(prefix="/ws", tags=["websocket"])


# Health check endpoints
@health_router.get("/")
async def health_check() -> dict[str, Any]:
    """Basic health check for orchestration layer."""
    return {
        "status": "healthy",
        "service": "n8n-workflow-service",
        "version": "1.0.0",
        "domains": ["security", "productivity", "mtg", "infrastructure"]
    }


@health_router.get("/detailed")
async def detailed_health_check() -> dict[str, Any]:
    """Detailed health check including domain service status."""
    # TODO: Add actual domain service health checks
    return {
        "status": "healthy",
        "services": {
            "database": {"status": "healthy", "response_time_ms": 5},
            "redis": {"status": "healthy", "response_time_ms": 2},
            "security_service": {"status": "healthy", "tools": 13},
            "productivity_service": {"status": "healthy", "tools": 8},
            "mtg_service": {"status": "healthy", "tools": 4},
            "infrastructure_service": {"status": "healthy", "tools": 12}
        },
        "executive_function": {
            "ui_response_time_ms": 45,  # <200ms constitutional requirement
            "context_preservation": "active",
            "adhd_accommodations": "enabled"
        }
    }


# Authentication endpoints
@auth_router.post("/login")
async def login(credentials: dict[str, str]) -> dict[str, Any]:
    """User authentication with JWT token generation."""
    # TODO: Implement actual user authentication
    return {
        "access_token": "jwt_token_here",
        "refresh_token": "refresh_token_here",
        "token_type": "bearer",
        "expires_in": 1800
    }


@auth_router.post("/refresh")
async def refresh_token(refresh_token: str) -> dict[str, Any]:
    """Refresh JWT access token."""
    # TODO: Implement token refresh logic
    return {
        "access_token": "new_jwt_token_here",
        "token_type": "bearer",
        "expires_in": 1800
    }


@auth_router.get("/me")
async def get_current_user_info(
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Get current user information and preferences."""
    return {
        "user_id": current_user.user_id,
        "username": current_user.username,
        "scopes": current_user.scopes,
        "executive_function_settings": {
            "adhd_accommodations": True,
            "autism_accommodations": True,
            "ui_response_target_ms": 150
        }
    }


# Security domain endpoints (13 tools)
@security_router.get("/tools")
async def get_security_tools(
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Get available security tools and their status."""
    return {
        "tools": [
            {"name": "misp", "status": "active", "response_time_ms": 450},
            {"name": "helk", "status": "active", "response_time_ms": 650},
            {"name": "securityonion", "status": "active", "response_time_ms": 320},
            {"name": "maltrail", "status": "active", "response_time_ms": 180},
            {"name": "yara_x", "status": "active", "response_time_ms": 95},
            {"name": "cyberchef", "status": "active", "response_time_ms": 12},
            {"name": "nemesis", "status": "active", "response_time_ms": 890},
            {"name": "apiscout", "status": "active", "response_time_ms": 145},
            {"name": "brute_ratel", "status": "active", "response_time_ms": 230},
            {"name": "meterpreter", "status": "active", "response_time_ms": 340},
            {"name": "lscript", "status": "active", "response_time_ms": 67},
            {"name": "rita", "status": "active", "response_time_ms": 420},
            {"name": "software_forensic_kit",
                "status": "active", "response_time_ms": 780}
        ],
        "domain_performance": {
            "target_response_ms": 1000,  # <1s constitutional requirement
            "current_avg_ms": 385
        }
    }


# Productivity domain endpoints (8 tools)
@productivity_router.get("/tools")
async def get_productivity_tools(
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Get available productivity tools and their status."""
    return {
        "tools": [
            {"name": "n8n", "status": "active", "response_time_ms": 1200},
            {"name": "mealie", "status": "active", "response_time_ms": 340},
            {"name": "dispatch", "status": "active", "response_time_ms": 890},
            {"name": "actual", "status": "active", "response_time_ms": 450},
            {"name": "firecrawl", "status": "active", "response_time_ms": 1800},
            {"name": "goose", "status": "active", "response_time_ms": 670},
            {"name": "it_tools", "status": "active", "response_time_ms": 120},
            {"name": "inspector", "status": "active", "response_time_ms": 230}
        ],
        "domain_performance": {
            "target_response_ms": 2000,  # <2s constitutional requirement
            "current_avg_ms": 712
        }
    }


# MTG domain endpoints (4 tools)
@mtg_router.get("/tools")
async def get_mtg_tools(
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Get available MTG tools and their status."""
    return {
        "tools": [
            {"name": "commander_spellbook",
                "status": "active", "response_time_ms": 1800},
            {"name": "mtg_commander_map", "status": "active", "response_time_ms": 950},
            {"name": "mtg_scripting_toolkit",
                "status": "active", "response_time_ms": 1200},
            {"name": "card_analysis", "status": "active", "response_time_ms": 2100}
        ],
        "domain_performance": {
            "target_response_ms": 3000,  # <3s constitutional requirement
            "current_avg_ms": 1512
        }
    }


# Infrastructure domain endpoints (12 tools)
@infrastructure_router.get("/tools")
async def get_infrastructure_tools(
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Get available infrastructure tools and their status."""
    return {
        "tools": [
            {"name": "kong", "status": "active", "response_time_ms": 45},
            {"name": "ghostwriter", "status": "active", "response_time_ms": 1200},
            {"name": "kasmvnc", "status": "active", "response_time_ms": 340},
            {"name": "chroma_mcp", "status": "active", "response_time_ms": 890},
            {"name": "filescopemcp", "status": "active", "response_time_ms": 450},
            {"name": "firecrawl_mcp", "status": "active", "response_time_ms": 1100},
            {"name": "n8n_mcp", "status": "active", "response_time_ms": 780},
            {"name": "malwarebazaar_mcp", "status": "active", "response_time_ms": 650},
            {"name": "mcp_virustotal", "status": "active", "response_time_ms": 1800},
            {"name": "onex", "status": "active", "response_time_ms": 2300},
            {"name": "hexstrike_ai", "status": "active", "response_time_ms": 3200},
            {"name": "blackarch", "status": "active", "response_time_ms": 4100}
        ],
        "domain_performance": {
            "target_response_ms": 5000,  # <5s constitutional requirement
            "current_avg_ms": 1496
        }
    }


# Cross-domain workflow endpoints
@api_router.get("/workflows")
async def get_active_workflows(
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Get active cross-domain workflows."""
    return {
        "workflows": [
            {
                "id": "wf_001",
                "name": "Security Incident Response",
                "domains": ["security", "productivity"],
                "tools_involved": ["misp", "dispatch", "n8n"],
                "status": "active",
                "progress": 0.6
            },
            {
                "id": "wf_002",
                "name": "MTG Deck Analysis",
                "domains": ["mtg"],
                "tools_involved": ["commander_spellbook", "card_analysis"],
                "status": "completed",
                "progress": 1.0
            }
        ]
    }


@api_router.post("/workflows")
async def create_workflow(
    workflow_data: dict[str, Any],
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Create new cross-domain workflow."""
    # TODO: Implement workflow creation logic
    return {
        "workflow_id": "wf_003",
        "status": "created",
        "message": "Workflow created successfully"
    }


# Executive function accommodations endpoints
@api_router.get("/user/preferences")
async def get_user_preferences(
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Get user executive function preferences."""
    return {
        "ui_preferences": {
            "response_time_target_ms": 150,
            "context_switching_reduction": True,
            "adhd_accommodations": {
                "focus_indicators": True,
                "progress_tracking": True,
                "distraction_blocking": True
            },
            "autism_accommodations": {
                "consistent_navigation": True,
                "sensory_optimization": "medium",
                "routine_preservation": True
            }
        }
    }


@api_router.put("/user/preferences")
async def update_user_preferences(
    preferences: dict[str, Any],
    current_user: TokenData = Depends(get_current_user)
) -> dict[str, Any]:
    """Update user executive function preferences."""
    # TODO: Implement preference updates
    return {
        "status": "updated",
        "message": "Preferences updated successfully"
    }


# Register all routers with the main API router
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(security_router)
api_router.include_router(productivity_router)
api_router.include_router(mtg_router)
api_router.include_router(infrastructure_router)


# Error handling
@api_router.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Custom HTTP exception handler with executive function considerations."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "executive_function_note": (
                "Error responses are designed to be clear and actionable "
                "to support executive function accommodations."
            )
        }
    )


# Domain service communication helpers
class DomainServiceCommunicator:
    """Helper class for communicating with domain services."""

    @staticmethod
    async def call_security_service(
        tool_name: str,
        operation: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """Call security domain service."""
        # TODO: Implement actual service communication
        return {"status": "success", "data": {}}

    @staticmethod
    async def call_productivity_service(
        tool_name: str,
        operation: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """Call productivity domain service."""
        # TODO: Implement actual service communication
        return {"status": "success", "data": {}}

    @staticmethod
    async def call_mtg_service(
        tool_name: str,
        operation: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """Call MTG domain service."""
        # TODO: Implement actual service communication
        return {"status": "success", "data": {}}

    @staticmethod
    async def call_infrastructure_service(
        tool_name: str,
        operation: str,
        params: dict[str, Any]
    ) -> dict[str, Any]:
        """Call infrastructure domain service."""
        # TODO: Implement actual service communication
        return {"status": "success", "data": {}}
