"""
Secure Remote API Endpoints - T143
Remote access API for Jane Executive Function Platform
Constitutional requirement: <200ms UI response, secure domain access
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import (APIRouter, Depends, HTTPException, Request, WebSocket,
                     WebSocketDisconnect, status)
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ...services.remote_access_service import (ConnectionType,
                                               RemoteAccessService,
                                               get_remote_access_service)
from ...services.vpn_service import VPNService, get_vpn_service
from ..oauth import OAuth2User, get_current_user, require_scopes


class RemoteConnectionRequest(BaseModel):
    """Request to establish remote connection"""

    connection_type: str = Field(..., description="Type of connection")
    user_agent: Optional[str] = Field(None, description="User agent string")
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="Executive function preferences"
    )


class RemoteConnectionResponse(BaseModel):
    """Remote connection response"""

    connection_id: str
    status: str
    message: str
    websocket_url: Optional[str] = None


class DomainAccessRequest(BaseModel):
    """Request for domain-specific access"""

    domain: str = Field(...,
                        description="Domain name (security, productivity, mtg, infrastructure)")
    tools: Optional[List[str]] = Field(
        None, description="Specific tools to access")
    session_preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="Session-specific preferences"
    )


class PerformanceMetrics(BaseModel):
    """Performance metrics for executive function monitoring"""

    response_time_ms: float
    domain: str
    timestamp: datetime
    user_id: str
    constitutional_compliant: bool


class RemoteAPIStatus(BaseModel):
    """Remote API status response"""

    status: str
    active_connections: int
    supported_domains: List[str]
    performance_metrics: Dict[str, Any]
    constitutional_compliance: Dict[str, Any]


# Remote API router
remote_router = APIRouter(prefix="/remote", tags=["remote-access"])


@remote_router.post("/connect", response_model=RemoteConnectionResponse)
async def establish_remote_connection(
    request: Request,
    connection_request: RemoteConnectionRequest,
    current_user: OAuth2User = Depends(get_current_user)
):
    """
    Establish secure remote connection
    Executive function accommodation: streamlined connection setup
    """
    start_time = datetime.utcnow()
    remote_service = get_remote_access_service()

    # Get client information
    client_ip = request.client.host
    user_agent = connection_request.user_agent or request.headers.get(
        "user-agent")

    # Map connection type
    try:
        conn_type = ConnectionType(connection_request.connection_type.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid connection type: {connection_request.connection_type}"
        )

    # Create connection
    connection = await remote_service.create_connection(
        user_id=current_user.user_id,
        connection_type=conn_type,
        remote_ip=client_ip,
        user_agent=user_agent
    )

    if not connection:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Unable to establish connection - rate limited or quota exceeded"
        )

    # Update user preferences with executive function accommodations
    connection.domain_preferences.update(connection_request.preferences)
    connection.accessibility_settings.update(
        connection_request.preferences.get("accessibility", {})
    )

    # Check constitutional response time requirement
    response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    constitutional_compliant = response_time < 200  # <200ms requirement

    # Build WebSocket URL for real-time updates
    websocket_url = None
    if conn_type in [ConnectionType.WEBSOCKET, ConnectionType.PWA, ConnectionType.WEB_BROWSER]:
        websocket_url = f"/remote/ws/{connection.connection_id}"

    return RemoteConnectionResponse(
        connection_id=connection.connection_id,
        status="connected",
        message=f"Remote connection established in {response_time:.1f}ms",
        websocket_url=websocket_url
    )


@remote_router.websocket("/ws/{connection_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    connection_id: str
):
    """
    WebSocket endpoint for real-time communication
    Executive function accommodation: immediate feedback and updates
    """
    remote_service = get_remote_access_service()

    # Accept WebSocket connection
    await websocket.accept()

    try:
        # Register WebSocket with connection
        connection = remote_service.connections.get(connection_id)
        if not connection:
            await websocket.send_json({"error": "Invalid connection ID"})
            await websocket.close()
            return

        connection.websocket = websocket
        remote_service.websockets[connection_id] = websocket

        # Send welcome message
        await websocket.send_json({
            "type": "welcome",
            "connection_id": connection_id,
            "user_id": connection.user_id,
            "preferences": connection.domain_preferences,
            "accessibility": connection.accessibility_settings,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Handle incoming messages
        while True:
            try:
                # Set receive timeout for executive function accommodation
                data = await asyncio.wait_for(websocket.receive_json(), timeout=30.0)

                # Update activity
                await remote_service.update_connection_activity(connection_id)

                # Handle different message types
                message_type = data.get("type")

                if message_type == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.utcnow().isoformat()
                    })

                elif message_type == "domain_access":
                    # Handle domain access request via WebSocket
                    domain = data.get("domain")
                    response = await _handle_domain_access_ws(
                        connection, domain, data.get("preferences", {})
                    )
                    await websocket.send_json(response)

                elif message_type == "preference_update":
                    # Update user preferences
                    preferences = data.get("preferences", {})
                    connection.domain_preferences.update(preferences)

                    await websocket.send_json({
                        "type": "preference_updated",
                        "preferences": connection.domain_preferences,
                        "timestamp": datetime.utcnow().isoformat()
                    })

                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    })

            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.send_json({
                    "type": "keepalive",
                    "timestamp": datetime.utcnow().isoformat()
                })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"WebSocket error: {str(e)}"
            })
        except:
            pass
    finally:
        # Clean up connection
        await remote_service.close_connection(connection_id, "WebSocket disconnected")


async def _handle_domain_access_ws(
    connection,
    domain: str,
    preferences: Dict[str, Any]
) -> Dict[str, Any]:
    """Handle domain access request via WebSocket"""
    start_time = datetime.utcnow()

    # Validate domain
    valid_domains = ["security", "productivity", "mtg", "infrastructure"]
    if domain not in valid_domains:
        return {
            "type": "domain_access_error",
            "error": f"Invalid domain: {domain}",
            "valid_domains": valid_domains
        }

    # Check constitutional response time thresholds
    domain_thresholds = {
        "security": 1000,      # <1s
        "productivity": 2000,  # <2s
        "mtg": 3000,          # <3s
        "infrastructure": 5000  # <5s
    }

    # Simulate domain access (in production, actually access domain services)
    await asyncio.sleep(0.1)  # Simulate processing time

    response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    threshold = domain_thresholds.get(domain, 5000)
    constitutional_compliant = response_time < threshold

    return {
        "type": "domain_access_response",
        "domain": domain,
        "status": "granted",
        "response_time_ms": response_time,
        "constitutional_compliant": constitutional_compliant,
        "threshold_ms": threshold,
        "tools_available": _get_domain_tools(domain),
        "timestamp": datetime.utcnow().isoformat()
    }


def _get_domain_tools(domain: str) -> List[str]:
    """Get available tools for domain"""
    domain_tools = {
        "security": ["MISP", "HELK", "SecurityOnion", "Maltrail", "YARA-X", "CyberChef", "Nemesis"],
        "productivity": ["n8n", "Mealie", "Dispatch", "Actual Budget", "Firecrawl", "Goose", "IT-Tools", "Inspector"],
        "mtg": ["Commander Spellbook", "MTG Commander Map", "MTG Scripting Toolkit", "Card Analysis"],
        "infrastructure": ["Kong", "Ghostwriter", "KasmVNC", "MCP Servers", "Workflow Automation"]
    }
    return domain_tools.get(domain, [])


@remote_router.post("/access/{domain}")
async def request_domain_access(
    domain: str,
    access_request: DomainAccessRequest,
    current_user: OAuth2User = Depends(require_scopes("profile"))
):
    """
    Request access to specific domain tools
    Executive function accommodation: domain-specific thresholds
    """
    start_time = datetime.utcnow()

    # Validate domain
    valid_domains = ["security", "productivity", "mtg", "infrastructure"]
    if domain not in valid_domains:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid domain: {domain}. Valid domains: {valid_domains}"
        )

    # Check required scopes for domain
    required_scope = f"{domain}:read"
    if required_scope not in current_user.scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Insufficient permissions for {domain} domain"
        )

    # Simulate domain access processing
    await asyncio.sleep(0.05)  # Simulate processing

    # Check constitutional response time requirements
    response_time = (datetime.utcnow() - start_time).total_seconds() * 1000
    domain_thresholds = {
        "security": 1000,      # <1s - threat analysis criticality
        "productivity": 2000,  # <2s - task management workflows
        "mtg": 3000,          # <3s - game analysis complexity
        "infrastructure": 5000  # <5s - system operations tolerance
    }

    threshold = domain_thresholds.get(domain, 5000)
    constitutional_compliant = response_time < threshold

    # Log performance for monitoring
    if not constitutional_compliant:
        # In production, log to monitoring system
        pass

    return {
        "domain": domain,
        "access_granted": True,
        "user_id": current_user.user_id,
        "tools_available": _get_domain_tools(domain),
        "specific_tools": access_request.tools or _get_domain_tools(domain),
        "session_preferences": access_request.session_preferences,
        "performance_metrics": {
            "response_time_ms": response_time,
            "constitutional_threshold_ms": threshold,
            "constitutional_compliant": constitutional_compliant
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@remote_router.get("/connections")
async def list_user_connections(
    current_user: OAuth2User = Depends(get_current_user)
):
    """
    List user's active remote connections
    Executive function accommodation: clear connection status
    """
    remote_service = get_remote_access_service()
    user_connections = []

    user_connection_ids = remote_service.user_connections.get(
        current_user.user_id, set())

    for connection_id in user_connection_ids:
        connection_status = remote_service.get_connection_status(connection_id)
        if connection_status:
            user_connections.append(connection_status)

    return {
        "user_id": current_user.user_id,
        "active_connections": len(user_connections),
        "connections": user_connections,
        "timestamp": datetime.utcnow().isoformat()
    }


@remote_router.delete("/connections/{connection_id}")
async def disconnect_remote_connection(
    connection_id: str,
    current_user: OAuth2User = Depends(get_current_user)
):
    """
    Disconnect specific remote connection
    Executive function accommodation: easy connection management
    """
    remote_service = get_remote_access_service()

    # Verify connection belongs to user
    connection = remote_service.connections.get(connection_id)
    if not connection or connection.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connection not found"
        )

    # Close connection
    await remote_service.close_connection(connection_id, "user requested disconnect")

    return {
        "message": "Connection closed successfully",
        "connection_id": connection_id,
        "timestamp": datetime.utcnow().isoformat()
    }


@remote_router.get("/vpn/status")
async def get_vpn_status(
    current_user: OAuth2User = Depends(require_scopes("infrastructure:read"))
):
    """
    Get VPN/tunnel status
    Executive function accommodation: clear infrastructure status
    """
    vpn_service = get_vpn_service()
    return vpn_service.get_service_status()


@remote_router.get("/vpn/tunnels")
async def list_vpn_tunnels(
    current_user: OAuth2User = Depends(require_scopes("infrastructure:read"))
):
    """List available VPN tunnels"""
    vpn_service = get_vpn_service()

    tunnels = []
    for tunnel_id in vpn_service.tunnels.keys():
        tunnel_status = vpn_service.get_tunnel_status(tunnel_id)
        if tunnel_status:
            tunnels.append(tunnel_status)

    return {
        "tunnels": tunnels,
        "total_count": len(tunnels),
        "timestamp": datetime.utcnow().isoformat()
    }


@remote_router.post("/vpn/tunnels/{tunnel_id}/start")
async def start_vpn_tunnel(
    tunnel_id: str,
    current_user: OAuth2User = Depends(require_scopes("infrastructure:write"))
):
    """Start VPN tunnel"""
    vpn_service = get_vpn_service()

    success = await vpn_service.start_tunnel(tunnel_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start tunnel"
        )

    return {
        "message": "Tunnel started successfully",
        "tunnel_id": tunnel_id,
        "timestamp": datetime.utcnow().isoformat()
    }


@remote_router.post("/vpn/tunnels/{tunnel_id}/stop")
async def stop_vpn_tunnel(
    tunnel_id: str,
    current_user: OAuth2User = Depends(require_scopes("infrastructure:write"))
):
    """Stop VPN tunnel"""
    vpn_service = get_vpn_service()

    success = await vpn_service.stop_tunnel(tunnel_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to stop tunnel"
        )

    return {
        "message": "Tunnel stopped successfully",
        "tunnel_id": tunnel_id,
        "timestamp": datetime.utcnow().isoformat()
    }


@remote_router.get("/performance/metrics")
async def get_performance_metrics(
    current_user: OAuth2User = Depends(get_current_user)
):
    """
    Get performance metrics for constitutional compliance
    Executive function accommodation: performance transparency
    """
    remote_service = get_remote_access_service()
    service_status = remote_service.get_service_status()

    return {
        "constitutional_requirements": {
            "ui_response_threshold_ms": 200,
            "domain_thresholds": {
                "security": 1000,      # <1s
                "productivity": 2000,  # <2s
                "mtg": 3000,          # <3s
                "infrastructure": 5000  # <5s
            }
        },
        "current_performance": service_status.get("performance_metrics", {}),
        "compliance_status": "monitoring",
        "user_preferences": current_user.preferences,
        "timestamp": datetime.utcnow().isoformat()
    }


@remote_router.get("/status", response_model=RemoteAPIStatus)
async def get_remote_api_status(
    current_user: OAuth2User = Depends(get_current_user)
):
    """
    Get remote API status
    Executive function accommodation: system transparency
    """
    remote_service = get_remote_access_service()
    service_status = remote_service.get_service_status()

    return RemoteAPIStatus(
        status="operational",
        active_connections=service_status.get("active_connections", 0),
        supported_domains=["security",
                           "productivity", "mtg", "infrastructure"],
        performance_metrics=service_status.get("performance_metrics", {}),
        constitutional_compliance={
            "ui_response_threshold_ms": 200,
            "domain_response_thresholds": {
                "security": 1000,
                "productivity": 2000,
                "mtg": 3000,
                "infrastructure": 5000
            },
            "monitoring_enabled": True
        }
    )


# Development endpoints
@remote_router.get("/dev/connections")
async def list_all_connections():
    """Development endpoint to list all connections"""
    remote_service = get_remote_access_service()

    all_connections = []
    for connection_id in remote_service.connections.keys():
        connection_status = remote_service.get_connection_status(connection_id)
        if connection_status:
            all_connections.append(connection_status)

    return {
        "total_connections": len(all_connections),
        "connections": all_connections,
        "service_status": remote_service.get_service_status()
    }
