"""
Event Bus Service for real-time data propagation.

This service manages real-time event distribution and data propagation
across all 37 integrated tools with WebSocket support and domain-specific routing.
"""

import asyncio
import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    """Event type enumeration for cross-tool communication."""

    # Data synchronization events
    SYNC_STARTED = "sync_started"
    SYNC_COMPLETED = "sync_completed"
    SYNC_FAILED = "sync_failed"
    DATA_UPDATED = "data_updated"
    DATA_CREATED = "data_created"
    DATA_DELETED = "data_deleted"

    # Domain-specific events
    SECURITY_ALERT = "security_alert"
    THREAT_DETECTED = "threat_detected"
    TASK_CREATED = "task_created"
    TASK_COMPLETED = "task_completed"
    WORKFLOW_TRIGGERED = "workflow_triggered"
    BUDGET_UPDATED = "budget_updated"

    # System events
    TOOL_CONNECTED = "tool_connected"
    TOOL_DISCONNECTED = "tool_disconnected"
    DOMAIN_STATUS_CHANGED = "domain_status_changed"
    PERFORMANCE_ALERT = "performance_alert"

    # User events
    USER_ACTION = "user_action"
    PREFERENCE_UPDATED = "preference_updated"
    SESSION_STARTED = "session_started"
    SESSION_ENDED = "session_ended"


class EventPriority(str, Enum):
    """Event priority levels."""

    CRITICAL = "critical"  # <200ms delivery requirement
    HIGH = "high"  # <1s delivery requirement
    MEDIUM = "medium"  # <5s delivery requirement
    LOW = "low"  # Best effort delivery


class DomainType(str, Enum):
    """Domain type enumeration."""

    SECURITY = "security"
    PRODUCTIVITY = "productivity"
    MTG = "mtg"
    INFRASTRUCTURE = "infrastructure"
    SYSTEM = "system"


class Event(BaseModel):
    """Event model for cross-tool communication."""

    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType = Field(..., description="Type of event")
    source_tool: str = Field(..., description="Source tool identifier")
    source_domain: DomainType = Field(..., description="Source domain")
    target_tools: Optional[List[str]] = Field(
        None, description="Specific target tools (None = broadcast)"
    )
    target_domains: Optional[List[DomainType]] = Field(
        None, description="Target domains (None = all domains)"
    )

    # Event data
    payload: Dict[str, Any] = Field(
        default_factory=dict, description="Event payload")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Event metadata"
    )

    # Timing and routing
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    priority: EventPriority = Field(default=EventPriority.MEDIUM)
    ttl_seconds: int = Field(
        default=300, description="Time to live in seconds")

    # Delivery tracking
    delivery_required: bool = Field(
        default=False, description="Requires delivery confirmation"
    )
    retry_count: int = Field(default=0, description="Number of retry attempts")
    max_retries: int = Field(default=3, description="Maximum retry attempts")

    # User context
    user_id: Optional[str] = Field(None, description="Associated user ID")
    session_id: Optional[str] = Field(None, description="Session identifier")

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "event_type": "data_updated",
                "source_tool": "misp",
                "source_domain": "security",
                "target_tools": ["helk", "security_onion"],
                "payload": {"entity_id": "123", "entity_type": "threat_intelligence"},
                "priority": "high",
            }
        }


class EventHandler:
    """Event handler wrapper for callbacks."""

    def __init__(
        self,
        handler_id: str,
        callback: Callable[[Event], Any],
        event_types: Set[EventType],
        tool_filter: Optional[Set[str]] = None,
        domain_filter: Optional[Set[DomainType]] = None,
    ):
        self.handler_id = handler_id
        self.callback = callback
        self.event_types = event_types
        self.tool_filter = tool_filter or set()
        self.domain_filter = domain_filter or set()
        self.created_at = datetime.utcnow()

    def should_handle(self, event: Event) -> bool:
        """Check if this handler should process the event."""
        # Check event type
        if event.event_type not in self.event_types:
            return False

        # Check tool filter
        if self.tool_filter and event.source_tool not in self.tool_filter:
            return False

        # Check domain filter
        if self.domain_filter and event.source_domain not in self.domain_filter:
            return False

        return True


class WebSocketConnection:
    """WebSocket connection wrapper."""

    def __init__(
        self,
        websocket: WebSocket,
        connection_id: str,
        user_id: Optional[str] = None,
        tool_subscriptions: Optional[Set[str]] = None,
        domain_subscriptions: Optional[Set[DomainType]] = None,
    ):
        self.websocket = websocket
        self.connection_id = connection_id
        self.user_id = user_id
        self.tool_subscriptions = tool_subscriptions or set()
        self.domain_subscriptions = domain_subscriptions or set()
        self.connected_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()

    def should_receive(self, event: Event) -> bool:
        """Check if this connection should receive the event."""
        # Check tool subscriptions
        if self.tool_subscriptions:
            if event.target_tools:
                if not any(tool in self.tool_subscriptions for tool in event.target_tools):
                    return False
            elif event.source_tool not in self.tool_subscriptions:
                return False

        # Check domain subscriptions
        if self.domain_subscriptions:
            if event.target_domains:
                if not any(
                    domain in self.domain_subscriptions for domain in event.target_domains
                ):
                    return False
            elif event.source_domain not in self.domain_subscriptions:
                return False

        # Check user context
        if event.user_id and event.user_id != self.user_id:
            return False

        return True


class EventBusService:
    """
    Service for managing real-time event distribution and data propagation.

    Handles cross-domain event routing, WebSocket connections, and
    performance-aware event delivery across all 37 integrated tools.
    """

    def __init__(self):
        """Initialize the event bus service."""
        self.handlers: Dict[str, EventHandler] = {}
        self.websocket_connections: Dict[str, WebSocketConnection] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.delivery_confirmations: Dict[str, Set[str]] = {}
        self.event_metrics: Dict[str, Any] = {
            "events_published": 0,
            "events_delivered": 0,
            "events_failed": 0,
            "average_delivery_time_ms": 0,
        }
        self._running = False
        self._processing_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the event bus service."""
        if not self._running:
            self._running = True
            self._processing_task = asyncio.create_task(self._process_events())
            logger.info("Event bus service started")

    async def stop(self) -> None:
        """Stop the event bus service."""
        if self._running:
            self._running = False
            if self._processing_task:
                self._processing_task.cancel()
                try:
                    await self._processing_task
                except asyncio.CancelledError:
                    pass
            logger.info("Event bus service stopped")

    async def publish_event(self, event: Event) -> None:
        """
        Publish an event to the event bus.

        Args:
            event: Event to publish
        """
        # Validate event
        if not event.event_id:
            event.event_id = str(uuid4())

        # Add to queue for processing
        await self.event_queue.put(event)
        self.event_metrics["events_published"] += 1

        logger.debug(
            f"Published event {event.event_type} from {event.source_tool} "
            f"(ID: {event.event_id})"
        )

    async def subscribe_handler(
        self,
        handler_id: str,
        callback: Callable[[Event], Any],
        event_types: Set[EventType],
        tool_filter: Optional[Set[str]] = None,
        domain_filter: Optional[Set[DomainType]] = None,
    ) -> None:
        """
        Subscribe an event handler.

        Args:
            handler_id: Unique handler identifier
            callback: Handler callback function
            event_types: Set of event types to handle
            tool_filter: Optional tool filter
            domain_filter: Optional domain filter
        """
        handler = EventHandler(
            handler_id=handler_id,
            callback=callback,
            event_types=event_types,
            tool_filter=tool_filter,
            domain_filter=domain_filter,
        )
        self.handlers[handler_id] = handler

        logger.info(
            f"Subscribed handler {handler_id} for events: {event_types}"
        )

    async def unsubscribe_handler(self, handler_id: str) -> bool:
        """
        Unsubscribe an event handler.

        Args:
            handler_id: Handler identifier

        Returns:
            True if handler was removed
        """
        if handler_id in self.handlers:
            del self.handlers[handler_id]
            logger.info(f"Unsubscribed handler {handler_id}")
            return True
        return False

    async def connect_websocket(
        self,
        websocket: WebSocket,
        connection_id: str,
        user_id: Optional[str] = None,
        tool_subscriptions: Optional[List[str]] = None,
        domain_subscriptions: Optional[List[str]] = None,
    ) -> None:
        """
        Connect a WebSocket for real-time events.

        Args:
            websocket: WebSocket connection
            connection_id: Unique connection identifier
            user_id: Optional user identifier
            tool_subscriptions: Tools to subscribe to
            domain_subscriptions: Domains to subscribe to
        """
        await websocket.accept()

        # Convert subscriptions to sets and enums
        tool_set = set(tool_subscriptions) if tool_subscriptions else set()
        domain_set = (
            {DomainType(d) for d in domain_subscriptions}
            if domain_subscriptions
            else set()
        )

        connection = WebSocketConnection(
            websocket=websocket,
            connection_id=connection_id,
            user_id=user_id,
            tool_subscriptions=tool_set,
            domain_subscriptions=domain_set,
        )

        self.websocket_connections[connection_id] = connection

        # Send connection confirmation
        await self._send_websocket_event(
            connection,
            Event(
                event_type=EventType.TOOL_CONNECTED,
                source_tool="event_bus",
                source_domain=DomainType.SYSTEM,
                payload={"connection_id": connection_id,
                         "status": "connected"},
            ),
        )

        logger.info(f"WebSocket connected: {connection_id} (user: {user_id})")

    async def disconnect_websocket(self, connection_id: str) -> None:
        """
        Disconnect a WebSocket connection.

        Args:
            connection_id: Connection identifier
        """
        if connection_id in self.websocket_connections:
            connection = self.websocket_connections[connection_id]

            # Send disconnection event
            try:
                await self._send_websocket_event(
                    connection,
                    Event(
                        event_type=EventType.TOOL_DISCONNECTED,
                        source_tool="event_bus",
                        source_domain=DomainType.SYSTEM,
                        payload={"connection_id": connection_id,
                                 "status": "disconnected"},
                    ),
                )
            except Exception:
                pass  # Connection may already be closed

            del self.websocket_connections[connection_id]
            logger.info(f"WebSocket disconnected: {connection_id}")

    async def _process_events(self) -> None:
        """Process events from the queue."""
        while self._running:
            try:
                # Get event from queue with timeout
                event = await asyncio.wait_for(self.event_queue.get(), timeout=1.0)

                # Process event
                start_time = datetime.utcnow()
                await self._handle_event(event)
                processing_time = (datetime.utcnow() -
                                   start_time).total_seconds() * 1000

                # Update metrics
                self.event_metrics["events_delivered"] += 1
                self._update_average_delivery_time(processing_time)

                # Check delivery requirements
                if event.delivery_required:
                    await self._handle_delivery_confirmation(event)

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                self.event_metrics["events_failed"] += 1
                logger.error(f"Event processing error: {e}")

    async def _handle_event(self, event: Event) -> None:
        """
        Handle event distribution to handlers and WebSocket connections.

        Args:
            event: Event to handle
        """
        # Distribute to registered handlers
        for handler in self.handlers.values():
            if handler.should_handle(event):
                try:
                    if asyncio.iscoroutinefunction(handler.callback):
                        await handler.callback(event)
                    else:
                        handler.callback(event)
                except Exception as e:
                    logger.error(
                        f"Handler {handler.handler_id} failed to process event "
                        f"{event.event_id}: {e}"
                    )

        # Distribute to WebSocket connections
        for connection in self.websocket_connections.values():
            if connection.should_receive(event):
                await self._send_websocket_event(connection, event)

    async def _send_websocket_event(
        self, connection: WebSocketConnection, event: Event
    ) -> None:
        """
        Send event to WebSocket connection.

        Args:
            connection: WebSocket connection
            event: Event to send
        """
        try:
            event_data = {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "source_tool": event.source_tool,
                "source_domain": event.source_domain.value,
                "payload": event.payload,
                "metadata": event.metadata,
                "timestamp": event.timestamp.isoformat(),
                "priority": event.priority.value,
            }

            await connection.websocket.send_text(json.dumps(event_data))
            connection.last_activity = datetime.utcnow()

        except WebSocketDisconnect:
            # Handle disconnection
            await self.disconnect_websocket(connection.connection_id)
        except Exception as e:
            logger.error(
                f"Failed to send event to WebSocket {connection.connection_id}: {e}"
            )

    async def _handle_delivery_confirmation(self, event: Event) -> None:
        """
        Handle delivery confirmation for critical events.

        Args:
            event: Event requiring confirmation
        """
        # This would implement delivery confirmation tracking
        # For now, we'll log the requirement
        logger.debug(f"Event {event.event_id} requires delivery confirmation")

    def _update_average_delivery_time(self, processing_time: float) -> None:
        """
        Update average delivery time metric.

        Args:
            processing_time: Processing time in milliseconds
        """
        current_avg = self.event_metrics["average_delivery_time_ms"]
        delivered_count = self.event_metrics["events_delivered"]

        if delivered_count == 1:
            self.event_metrics["average_delivery_time_ms"] = processing_time
        else:
            # Running average calculation
            new_avg = ((current_avg * (delivered_count - 1)) +
                       processing_time) / delivered_count
            self.event_metrics["average_delivery_time_ms"] = new_avg

    async def publish_data_update_event(
        self,
        source_tool: str,
        source_domain: DomainType,
        entity_type: str,
        entity_id: str,
        update_data: Dict[str, Any],
        target_tools: Optional[List[str]] = None,
        user_id: Optional[str] = None,
    ) -> None:
        """
        Publish a data update event for cross-tool synchronization.

        Args:
            source_tool: Source tool identifier
            source_domain: Source domain
            entity_type: Type of entity that was updated
            entity_id: Entity identifier
            update_data: Updated data
            target_tools: Optional specific target tools
            user_id: Optional user context
        """
        event = Event(
            event_type=EventType.DATA_UPDATED,
            source_tool=source_tool,
            source_domain=source_domain,
            target_tools=target_tools,
            payload={
                "entity_type": entity_type,
                "entity_id": entity_id,
                "data": update_data,
            },
            priority=EventPriority.HIGH,
            delivery_required=True,
            user_id=user_id,
        )

        await self.publish_event(event)

    async def publish_sync_event(
        self,
        sync_job_id: str,
        sync_status: str,
        source_tool: str,
        target_tool: str,
        error_message: Optional[str] = None,
    ) -> None:
        """
        Publish a synchronization status event.

        Args:
            sync_job_id: Sync job identifier
            sync_status: Sync status (started/completed/failed)
            source_tool: Source tool
            target_tool: Target tool
            error_message: Optional error message
        """
        event_type_map = {
            "started": EventType.SYNC_STARTED,
            "completed": EventType.SYNC_COMPLETED,
            "failed": EventType.SYNC_FAILED,
        }

        event = Event(
            event_type=event_type_map.get(sync_status, EventType.SYNC_STARTED),
            source_tool="data_integration_service",
            source_domain=DomainType.SYSTEM,
            payload={
                "sync_job_id": sync_job_id,
                "source_tool": source_tool,
                "target_tool": target_tool,
                "status": sync_status,
                "error_message": error_message,
            },
            priority=EventPriority.HIGH if sync_status == "failed" else EventPriority.MEDIUM,
        )

        await self.publish_event(event)

    def get_metrics(self) -> Dict[str, Any]:
        """
        Get event bus metrics.

        Returns:
            Metrics dictionary
        """
        return {
            **self.event_metrics,
            "active_handlers": len(self.handlers),
            "active_websocket_connections": len(self.websocket_connections),
            "queue_size": self.event_queue.qsize(),
        }
