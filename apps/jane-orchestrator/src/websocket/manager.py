"""
WebSocket Manager

Provides real-time communication infrastructure for:
- AI server communication (vLLM, MCP servers)
- Cross-tool synchronization
- Executive function accommodations (context preservation, focus tracking)
- User preference sync across all 37 tools
"""

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel


class MessageType(Enum):
    """WebSocket message types"""
    # Executive function messages
    CONTEXT_UPDATE = "context_update"
    FOCUS_CHANGE = "focus_change"
    TASK_PROGRESS = "task_progress"
    COGNITIVE_LOAD_UPDATE = "cognitive_load_update"

    # AI communication
    AI_REQUEST = "ai_request"
    AI_RESPONSE = "ai_response"
    AI_STREAM_START = "ai_stream_start"
    AI_STREAM_CHUNK = "ai_stream_chunk"
    AI_STREAM_END = "ai_stream_end"

    # Tool synchronization
    TOOL_STATE_SYNC = "tool_state_sync"
    CROSS_TOOL_DATA = "cross_tool_data"
    WORKFLOW_UPDATE = "workflow_update"

    # User preferences
    PREFERENCE_UPDATE = "preference_update"
    SETTING_CHANGE = "setting_change"

    # System messages
    CONNECTION_ACK = "connection_ack"
    HEARTBEAT = "heartbeat"
    ERROR = "error"


class ConnectionType(Enum):
    """Types of WebSocket connections"""
    USER_INTERFACE = "ui"  # Frontend connections
    AI_SERVER = "ai"       # LLM server connections
    TOOL_ADAPTER = "tool"  # Service adapter connections
    ADMIN = "admin"        # Admin/monitoring connections


@dataclass
class WebSocketMessage:
    """Standardized WebSocket message format"""
    type: MessageType
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.utcnow)
    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""
    target: Optional[str] = None
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class ConnectionInfo(BaseModel):
    """Information about a WebSocket connection"""
    connection_id: str
    connection_type: ConnectionType
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    tool_id: Optional[str] = None
    connected_at: datetime = field(default_factory=datetime.utcnow)
    last_activity: datetime = field(default_factory=datetime.utcnow)
    subscribed_topics: Set[str] = field(default_factory=set)


class WebSocketManager:
    """
    Manages all WebSocket connections for the mental prosthetic platform

    Provides real-time communication between:
    - User interfaces and backend services
    - AI servers and orchestration layer  
    - Cross-tool data synchronization
    - Executive function context updates
    """

    def __init__(self):
        # Active connections by connection ID
        self._connections: Dict[str, WebSocket] = {}

        # Connection metadata
        self._connection_info: Dict[str, ConnectionInfo] = {}

        # Connections by type for efficient routing
        self._connections_by_type: Dict[ConnectionType, Set[str]] = {
            conn_type: set() for conn_type in ConnectionType
        }

        # Connections by user for user-specific messaging
        self._connections_by_user: Dict[str, Set[str]] = {}

        # Topic subscriptions for pub/sub messaging
        self._topic_subscribers: Dict[str, Set[str]] = {}

        # Message handlers
        self._message_handlers: Dict[MessageType, List[Callable]] = {}

        # Performance tracking
        self._message_count = 0
        self._error_count = 0
        self._connection_count = 0

        self.logger = logging.getLogger("websocket_manager")

        # Executive function context tracking
        self._user_contexts: Dict[str, Dict[str, Any]] = {}
        self._focus_tracking: Dict[str, Dict[str, Any]] = {}

    async def connect(
        self,
        websocket: WebSocket,
        connection_type: ConnectionType,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        tool_id: Optional[str] = None
    ) -> str:
        """Accept a new WebSocket connection"""
        connection_id = str(uuid.uuid4())

        await websocket.accept()

        # Store connection
        self._connections[connection_id] = websocket

        # Create connection info
        connection_info = ConnectionInfo(
            connection_id=connection_id,
            connection_type=connection_type,
            user_id=user_id,
            session_id=session_id,
            tool_id=tool_id
        )
        self._connection_info[connection_id] = connection_info

        # Index by type
        self._connections_by_type[connection_type].add(connection_id)

        # Index by user if provided
        if user_id:
            if user_id not in self._connections_by_user:
                self._connections_by_user[user_id] = set()
            self._connections_by_user[user_id].add(connection_id)

        self._connection_count += 1

        self.logger.info(
            f"New {connection_type.value} connection established: "
            f"{connection_id} (user: {user_id}, tool: {tool_id})"
        )

        # Send connection acknowledgment
        await self.send_to_connection(
            connection_id,
            WebSocketMessage(
                type=MessageType.CONNECTION_ACK,
                data={
                    "connection_id": connection_id,
                    "connection_type": connection_type.value,
                    "server_time": datetime.utcnow().isoformat()
                }
            )
        )

        return connection_id

    async def disconnect(self, connection_id: str) -> None:
        """Disconnect and clean up a WebSocket connection"""
        if connection_id not in self._connections:
            return

        connection_info = self._connection_info.get(connection_id)
        if connection_info:
            # Remove from type index
            self._connections_by_type[connection_info.connection_type].discard(
                connection_id
            )

            # Remove from user index
            if connection_info.user_id:
                user_connections = self._connections_by_user.get(
                    connection_info.user_id, set()
                )
                user_connections.discard(connection_id)
                if not user_connections:
                    del self._connections_by_user[connection_info.user_id]

            # Remove from topic subscriptions
            for topic_subscribers in self._topic_subscribers.values():
                topic_subscribers.discard(connection_id)

            # Clean up connection info
            del self._connection_info[connection_id]

        # Remove connection
        del self._connections[connection_id]

        self.logger.info(f"Connection {connection_id} disconnected")

    async def send_to_connection(
        self,
        connection_id: str,
        message: WebSocketMessage
    ) -> bool:
        """Send message to specific connection"""
        if connection_id not in self._connections:
            self.logger.warning(f"Connection {connection_id} not found")
            return False

        websocket = self._connections[connection_id]

        try:
            # Add executive function accommodations
            enhanced_message = await self._apply_executive_function_enhancements(
                message, connection_id
            )

            message_data = {
                "type": enhanced_message.type.value,
                "data": enhanced_message.data,
                "timestamp": enhanced_message.timestamp.isoformat(),
                "message_id": enhanced_message.message_id,
                "source": enhanced_message.source,
                "target": enhanced_message.target
            }

            await websocket.send_text(json.dumps(message_data))
            self._message_count += 1

            # Update connection activity
            if connection_id in self._connection_info:
                self._connection_info[connection_id].last_activity = (
                    datetime.utcnow()
                )

            return True

        except Exception as e:
            self._error_count += 1
            self.logger.error(
                f"Failed to send message to {connection_id}: {e}"
            )
            await self.disconnect(connection_id)
            return False

    async def send_to_user(
        self,
        user_id: str,
        message: WebSocketMessage
    ) -> int:
        """Send message to all connections for a user"""
        if user_id not in self._connections_by_user:
            return 0

        connection_ids = list(self._connections_by_user[user_id])
        successful_sends = 0

        for connection_id in connection_ids:
            if await self.send_to_connection(connection_id, message):
                successful_sends += 1

        return successful_sends

    async def send_to_type(
        self,
        connection_type: ConnectionType,
        message: WebSocketMessage
    ) -> int:
        """Send message to all connections of a specific type"""
        connection_ids = list(self._connections_by_type[connection_type])
        successful_sends = 0

        for connection_id in connection_ids:
            if await self.send_to_connection(connection_id, message):
                successful_sends += 1

        return successful_sends

    async def broadcast(self, message: WebSocketMessage) -> int:
        """Broadcast message to all connections"""
        connection_ids = list(self._connections.keys())
        successful_sends = 0

        for connection_id in connection_ids:
            if await self.send_to_connection(connection_id, message):
                successful_sends += 1

        return successful_sends

    async def subscribe_to_topic(
        self,
        connection_id: str,
        topic: str
    ) -> bool:
        """Subscribe connection to a topic"""
        if connection_id not in self._connections:
            return False

        if topic not in self._topic_subscribers:
            self._topic_subscribers[topic] = set()

        self._topic_subscribers[topic].add(connection_id)

        # Update connection info
        if connection_id in self._connection_info:
            self._connection_info[connection_id].subscribed_topics.add(topic)

        self.logger.debug(f"Connection {connection_id} subscribed to {topic}")
        return True

    async def unsubscribe_from_topic(
        self,
        connection_id: str,
        topic: str
    ) -> bool:
        """Unsubscribe connection from a topic"""
        if topic in self._topic_subscribers:
            self._topic_subscribers[topic].discard(connection_id)

            # Clean up empty topic
            if not self._topic_subscribers[topic]:
                del self._topic_subscribers[topic]

        # Update connection info
        if connection_id in self._connection_info:
            self._connection_info[connection_id].subscribed_topics.discard(
                topic)

        self.logger.debug(
            f"Connection {connection_id} unsubscribed from {topic}")
        return True

    async def publish_to_topic(
        self,
        topic: str,
        message: WebSocketMessage
    ) -> int:
        """Publish message to all subscribers of a topic"""
        if topic not in self._topic_subscribers:
            return 0

        subscriber_ids = list(self._topic_subscribers[topic])
        successful_sends = 0

        for connection_id in subscriber_ids:
            if await self.send_to_connection(connection_id, message):
                successful_sends += 1

        return successful_sends

    def register_message_handler(
        self,
        message_type: MessageType,
        handler: Callable
    ) -> None:
        """Register a handler for a specific message type"""
        if message_type not in self._message_handlers:
            self._message_handlers[message_type] = []

        self._message_handlers[message_type].append(handler)
        self.logger.debug(f"Registered handler for {message_type.value}")

    async def handle_message(
        self,
        connection_id: str,
        raw_message: str
    ) -> None:
        """Process incoming message from connection"""
        try:
            message_data = json.loads(raw_message)

            message = WebSocketMessage(
                type=MessageType(message_data.get("type")),
                data=message_data.get("data", {}),
                message_id=message_data.get("message_id", str(uuid.uuid4())),
                source=connection_id,
                target=message_data.get("target"),
                user_id=message_data.get("user_id"),
                session_id=message_data.get("session_id")
            )

            # Execute registered handlers
            handlers = self._message_handlers.get(message.type, [])
            for handler in handlers:
                try:
                    await handler(connection_id, message)
                except Exception as e:
                    self.logger.error(
                        f"Handler error for {message.type.value}: {e}"
                    )

            # Handle executive function specific messages
            await self._handle_executive_function_message(connection_id, message)

        except Exception as e:
            self._error_count += 1
            self.logger.error(f"Message handling error: {e}")

            # Send error response
            error_message = WebSocketMessage(
                type=MessageType.ERROR,
                data={
                    "error": "Invalid message format",
                    "details": str(e)
                }
            )
            await self.send_to_connection(connection_id, error_message)

    async def _apply_executive_function_enhancements(
        self,
        message: WebSocketMessage,
        connection_id: str
    ) -> WebSocketMessage:
        """Apply executive function accommodations to outgoing messages"""
        connection_info = self._connection_info.get(connection_id)
        if not connection_info or not connection_info.user_id:
            return message

        user_id = connection_info.user_id

        # Get user's executive function context
        user_context = self._user_contexts.get(user_id, {})

        enhanced_data = message.data.copy()

        # ADHD accommodations
        if user_context.get("adhd_mode_enabled", False):
            # Add progress indicators for long operations
            if message.type in [MessageType.AI_REQUEST, MessageType.TOOL_STATE_SYNC]:
                enhanced_data["progress_enabled"] = True

            # Reduce information density
            if "items" in enhanced_data and isinstance(enhanced_data["items"], list):
                enhanced_data["items"] = enhanced_data["items"][:20]
                enhanced_data["truncated"] = True

        # Focus assist accommodations
        if user_context.get("focus_assist_enabled", True):
            # Add focus context
            enhanced_data["focus_context"] = {
                "current_tool": user_context.get("current_tool"),
                "context_switches": user_context.get("context_switches", 0)
            }

        # Context switching warnings
        if (user_context.get("context_switching_warning", True) and
                message.type == MessageType.TOOL_STATE_SYNC):
            current_tool = user_context.get("current_tool")
            message_tool = enhanced_data.get("tool_id")

            if current_tool and message_tool and current_tool != message_tool:
                enhanced_data["context_switch_warning"] = {
                    "from_tool": current_tool,
                    "to_tool": message_tool,
                    "switch_count": user_context.get("context_switches", 0) + 1
                }

        return WebSocketMessage(
            type=message.type,
            data=enhanced_data,
            timestamp=message.timestamp,
            message_id=message.message_id,
            source=message.source,
            target=message.target,
            user_id=message.user_id,
            session_id=message.session_id
        )

    async def _handle_executive_function_message(
        self,
        connection_id: str,
        message: WebSocketMessage
    ) -> None:
        """Handle executive function specific messages"""
        connection_info = self._connection_info.get(connection_id)
        if not connection_info or not connection_info.user_id:
            return

        user_id = connection_info.user_id

        if message.type == MessageType.CONTEXT_UPDATE:
            # Update user context
            if user_id not in self._user_contexts:
                self._user_contexts[user_id] = {}

            self._user_contexts[user_id].update(message.data)

            # Broadcast context update to user's other connections
            context_message = WebSocketMessage(
                type=MessageType.CONTEXT_UPDATE,
                data=self._user_contexts[user_id],
                source="server"
            )
            await self.send_to_user(user_id, context_message)

        elif message.type == MessageType.FOCUS_CHANGE:
            # Track focus changes for cognitive load calculation
            if user_id not in self._focus_tracking:
                self._focus_tracking[user_id] = {}

            self._focus_tracking[user_id].update({
                "current_focus": message.data.get("focus_target"),
                "timestamp": datetime.utcnow(),
                "tool_id": message.data.get("tool_id")
            })

            # Update context switches count
            if user_id in self._user_contexts:
                current_switches = self._user_contexts[user_id].get(
                    "context_switches", 0)
                self._user_contexts[user_id]["context_switches"] = current_switches + 1
                self._user_contexts[user_id]["current_tool"] = message.data.get(
                    "tool_id")

        elif message.type == MessageType.COGNITIVE_LOAD_UPDATE:
            # Update cognitive load metrics
            if user_id not in self._user_contexts:
                self._user_contexts[user_id] = {}

            self._user_contexts[user_id]["cognitive_load"] = message.data.get(
                "load_score", 30)

            # Send load warning if high
            load_score = message.data.get("load_score", 30)
            if load_score > 80:
                warning_message = WebSocketMessage(
                    type=MessageType.ERROR,
                    data={
                        "type": "cognitive_overload_warning",
                        "message": "High cognitive load detected. Consider taking a break.",
                        "load_score": load_score,
                        "suggestions": [
                            "Take a 5-minute break",
                            "Close unnecessary tools",
                            "Focus on one task at a time"
                        ]
                    },
                    source="server"
                )
                await self.send_to_user(user_id, warning_message)

    async def start_heartbeat(self, interval: int = 30) -> None:
        """Start heartbeat to keep connections alive"""
        while True:
            await asyncio.sleep(interval)

            heartbeat_message = WebSocketMessage(
                type=MessageType.HEARTBEAT,
                data={"timestamp": datetime.utcnow().isoformat()},
                source="server"
            )

            await self.broadcast(heartbeat_message)

    def get_connection_stats(self) -> Dict[str, Any]:
        """Get WebSocket connection statistics"""
        active_connections = len(self._connections)
        connections_by_type = {
            conn_type.value: len(connection_ids)
            for conn_type, connection_ids in self._connections_by_type.items()
        }

        return {
            "active_connections": active_connections,
            "connections_by_type": connections_by_type,
            "total_messages": self._message_count,
            "error_count": self._error_count,
            "error_rate": self._error_count / max(self._message_count, 1),
            "unique_users": len(self._connections_by_user),
            "active_topics": len(self._topic_subscribers)
        }


# Global WebSocket manager instance
websocket_manager = WebSocketManager()
