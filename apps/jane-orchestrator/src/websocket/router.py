"""
WebSocket Router

FastAPI WebSocket endpoints for real-time communication
with executive function accommodations and AI integration.
"""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from ..auth.jwt_manager import get_current_user_websocket
from .manager import (ConnectionType, MessageType, WebSocketMessage,
                      websocket_manager)

router = APIRouter()
logger = logging.getLogger("websocket_router")


@router.websocket("/ws/ui")
async def websocket_ui_endpoint(
    websocket: WebSocket,
    token: Optional[str] = None
):
    """WebSocket endpoint for user interface connections"""
    user_id = None
    session_id = None

    # Authenticate if token provided
    if token:
        try:
            user_data = await get_current_user_websocket(token)
            user_id = user_data.get("user_id")
            session_id = user_data.get("session_id")
        except Exception as e:
            logger.warning(f"WebSocket UI authentication failed: {e}")
            await websocket.close(code=4001, reason="Authentication failed")
            return

    connection_id = await websocket_manager.connect(
        websocket=websocket,
        connection_type=ConnectionType.USER_INTERFACE,
        user_id=user_id,
        session_id=session_id
    )

    try:
        while True:
            message = await websocket.receive_text()
            await websocket_manager.handle_message(connection_id, message)

    except WebSocketDisconnect:
        await websocket_manager.disconnect(connection_id)
    except Exception as e:
        logger.error(f"WebSocket UI error: {e}")
        await websocket_manager.disconnect(connection_id)


@router.websocket("/ws/ai/{ai_server_id}")
async def websocket_ai_endpoint(
    websocket: WebSocket,
    ai_server_id: str,
    api_key: Optional[str] = None
):
    """WebSocket endpoint for AI server connections"""
    # TODO: Implement AI server authentication
    # For now, accept connections from known AI servers
    known_ai_servers = ["cyber-llm", "mtg-llm", "code-llm", "vllm-main"]

    if ai_server_id not in known_ai_servers:
        await websocket.close(code=4004, reason="Unknown AI server")
        return

    connection_id = await websocket_manager.connect(
        websocket=websocket,
        connection_type=ConnectionType.AI_SERVER,
        tool_id=ai_server_id
    )

    # Subscribe to AI-related topics
    await websocket_manager.subscribe_to_topic(connection_id, f"ai.{ai_server_id}")
    await websocket_manager.subscribe_to_topic(connection_id, "ai.broadcast")

    try:
        while True:
            message = await websocket.receive_text()
            await websocket_manager.handle_message(connection_id, message)

    except WebSocketDisconnect:
        await websocket_manager.disconnect(connection_id)
    except Exception as e:
        logger.error(f"WebSocket AI error for {ai_server_id}: {e}")
        await websocket_manager.disconnect(connection_id)


@router.websocket("/ws/tool/{tool_id}")
async def websocket_tool_endpoint(
    websocket: WebSocket,
    tool_id: str,
    api_key: Optional[str] = None
):
    """WebSocket endpoint for tool adapter connections"""
    # TODO: Implement tool adapter authentication

    connection_id = await websocket_manager.connect(
        websocket=websocket,
        connection_type=ConnectionType.TOOL_ADAPTER,
        tool_id=tool_id
    )

    # Subscribe to tool-specific topics
    await websocket_manager.subscribe_to_topic(connection_id, f"tool.{tool_id}")
    await websocket_manager.subscribe_to_topic(connection_id, "tools.broadcast")

    try:
        while True:
            message = await websocket.receive_text()
            await websocket_manager.handle_message(connection_id, message)

    except WebSocketDisconnect:
        await websocket_manager.disconnect(connection_id)
    except Exception as e:
        logger.error(f"WebSocket tool error for {tool_id}: {e}")
        await websocket_manager.disconnect(connection_id)


@router.websocket("/ws/admin")
async def websocket_admin_endpoint(
    websocket: WebSocket,
    token: Optional[str] = None
):
    """WebSocket endpoint for admin/monitoring connections"""
    user_id = None

    # Require authentication for admin connections
    if not token:
        await websocket.close(code=4001, reason="Authentication required")
        return

    try:
        user_data = await get_current_user_websocket(token)
        user_id = user_data.get("user_id")
        user_role = user_data.get("role", "user")

        if user_role != "admin":
            await websocket.close(code=4003, reason="Admin access required")
            return

    except Exception as e:
        logger.warning(f"WebSocket admin authentication failed: {e}")
        await websocket.close(code=4001, reason="Authentication failed")
        return

    connection_id = await websocket_manager.connect(
        websocket=websocket,
        connection_type=ConnectionType.ADMIN,
        user_id=user_id
    )

    # Subscribe to admin topics
    await websocket_manager.subscribe_to_topic(connection_id, "admin.metrics")
    await websocket_manager.subscribe_to_topic(connection_id, "admin.alerts")
    await websocket_manager.subscribe_to_topic(connection_id, "admin.logs")

    try:
        while True:
            message = await websocket.receive_text()
            await websocket_manager.handle_message(connection_id, message)

    except WebSocketDisconnect:
        await websocket_manager.disconnect(connection_id)
    except Exception as e:
        logger.error(f"WebSocket admin error: {e}")
        await websocket_manager.disconnect(connection_id)


# Message handlers for different message types
async def handle_ai_request(connection_id: str, message: WebSocketMessage):
    """Handle AI request messages"""
    # Route to appropriate AI server
    ai_server = message.data.get("ai_server", "vllm-main")
    topic = f"ai.{ai_server}"

    # Forward to AI server
    await websocket_manager.publish_to_topic(topic, message)


async def handle_tool_sync(connection_id: str, message: WebSocketMessage):
    """Handle tool state synchronization"""
    tool_id = message.data.get("tool_id")
    if tool_id:
        topic = f"tool.{tool_id}"
        await websocket_manager.publish_to_topic(topic, message)


async def handle_preference_update(connection_id: str, message: WebSocketMessage):
    """Handle user preference updates"""
    user_id = message.user_id
    if user_id:
        # Broadcast to all user connections
        await websocket_manager.send_to_user(user_id, message)


# Register message handlers
websocket_manager.register_message_handler(
    MessageType.AI_REQUEST,
    handle_ai_request
)
websocket_manager.register_message_handler(
    MessageType.TOOL_STATE_SYNC,
    handle_tool_sync
)
websocket_manager.register_message_handler(
    MessageType.PREFERENCE_UPDATE,
    handle_preference_update
)
