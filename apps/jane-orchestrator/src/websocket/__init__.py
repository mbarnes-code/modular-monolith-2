"""
WebSocket Package

Real-time communication infrastructure for the mental prosthetic platform.
Provides WebSocket connections for UI, AI servers, tool adapters, and admin.
"""

from .manager import (ConnectionInfo, ConnectionType, MessageType,
                      WebSocketManager, WebSocketMessage, websocket_manager)
from .router import router as websocket_router

__all__ = [
    'WebSocketManager',
    'websocket_manager',
    'MessageType',
    'ConnectionType',
    'WebSocketMessage',
    'ConnectionInfo',
    'websocket_router'
]
