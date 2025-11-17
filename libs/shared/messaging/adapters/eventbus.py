"""
Event Bus Adapter Implementation

Wraps the existing jane-orchestrator Event Bus Service.
"""

import asyncio
from typing import Any, Dict, List, Optional

from ..interfaces import (IMessageBus, Message, MessageBusMetrics, Priority,
                          PublishError, SubscriptionConfig, SubscriptionError)


class EventBusAdapter(IMessageBus):
    """
    Adapter for the jane-orchestrator Event Bus Service.

    Wraps the existing event_bus_service.py implementation to conform
    to the IMessageBus interface.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Event Bus adapter.

        Args:
            config: Configuration dict with optional keys:
                - host: Event Bus host (default: localhost)
                - port: Event Bus port (default: 8000)
                - websocket_enabled: Enable WebSocket support (default: True)
        """
        self.config = config
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 8000)
        self.websocket_enabled = config.get("websocket_enabled", True)

        # Internal state
        self._event_bus = None  # Will be injected or created
        self._subscriptions: Dict[str, SubscriptionConfig] = {}
        self._metrics = MessageBusMetrics()
        self._running = False

    async def start(self) -> None:
        """Initialize Event Bus connection"""
        if self._running:
            return

        # Import here to avoid circular dependencies
        try:
            from apps.core.jane_orchestrator.src.services.event_bus_service import \
                EventBusService

            self._event_bus = EventBusService()
            await self._event_bus.start()
            self._running = True

        except ImportError as e:
            raise ConnectionError(
                f"Failed to import EventBusService: {e}. "
                "Ensure jane-orchestrator is in PYTHONPATH."
            ) from e

    async def stop(self) -> None:
        """Shutdown Event Bus connection"""
        if not self._running:
            return

        # Unsubscribe all handlers
        for sub_id in list(self._subscriptions.keys()):
            await self.unsubscribe(sub_id)

        if self._event_bus:
            await self._event_bus.stop()

        self._running = False

    async def publish(self, message: Message) -> str:
        """
        Publish message to Event Bus.

        Converts Message to Event Bus Event format.
        """
        if not self._running:
            raise PublishError("Event Bus not started")

        try:
            # Convert Message to Event Bus Event
            from apps.core.jane_orchestrator.src.services.event_bus_service import (
                Event, EventPriority, EventType)

            # Map priority
            priority_map = {
                Priority.CRITICAL: EventPriority.CRITICAL,
                Priority.HIGH: EventPriority.HIGH,
                Priority.MEDIUM: EventPriority.MEDIUM,
                Priority.LOW: EventPriority.LOW,
            }

            # Determine event type from topic
            event_type = self._topic_to_event_type(message.topic)

            event = Event(
                event_id=message.message_id,
                event_type=event_type,
                source_tool=message.headers.get("source_tool", "unknown"),
                source_domain=message.headers.get("source_domain"),
                target_tools=message.headers.get("target_tools"),
                target_domains=message.headers.get("target_domains"),
                payload=message.payload,
                metadata=message.headers,
                priority=priority_map.get(
                    message.priority, EventPriority.MEDIUM),
                ttl_seconds=message.ttl_seconds,
                delivery_required=message.delivery_required,
                user_id=message.user_id,
                session_id=message.session_id,
            )

            await self._event_bus.publish_event(event)

            self._metrics.messages_published += 1
            return message.message_id

        except Exception as e:
            self._metrics.messages_failed += 1
            raise PublishError(f"Failed to publish message: {e}")

    async def subscribe(self, config: SubscriptionConfig) -> str:
        """
        Subscribe to Event Bus topics.

        Registers a handler with the Event Bus service.
        """
        if not self._running:
            raise SubscriptionError("Event Bus not started")

        try:
            from apps.core.jane_orchestrator.src.services.event_bus_service import \
                EventType

            # Convert topic patterns to event types
            event_types = {
                self._topic_to_event_type(topic)
                for topic in config.topics
            }

            # Wrap callback to convert Event back to Message
            async def wrapped_callback(event):
                message = self._event_to_message(event)
                await config.callback(message)

            # Register with Event Bus
            await self._event_bus.subscribe_handler(
                handler_id=config.handler_id,
                callback=wrapped_callback,
                event_types=event_types,
                domain_filter=config.filters.get(
                    "domains") if config.filters else None,
            )

            self._subscriptions[config.handler_id] = config
            self._metrics.active_subscribers += 1

            return config.handler_id

        except Exception as e:
            raise SubscriptionError(f"Failed to subscribe: {e}")

    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from Event Bus"""
        if subscription_id in self._subscriptions:
            await self._event_bus.unsubscribe_handler(subscription_id)
            del self._subscriptions[subscription_id]
            self._metrics.active_subscribers -= 1

    async def request(self, message: Message, timeout_seconds: int = 30) -> Message:
        """
        Request/reply pattern using Event Bus.

        Publishes message and waits for reply on reply_to topic.
        """
        if not message.reply_to:
            raise ValueError(
                "Message must have reply_to set for request/reply")

        # Create reply subscription
        reply_future = asyncio.Future()

        async def reply_handler(reply_msg: Message):
            if reply_msg.correlation_id == message.message_id:
                reply_future.set_result(reply_msg)

        # Subscribe to reply topic
        reply_config = SubscriptionConfig(
            handler_id=f"reply_{message.message_id}",
            topics=[message.reply_to],
            callback=reply_handler,
        )

        sub_id = await self.subscribe(reply_config)

        try:
            # Publish request
            message.correlation_id = message.message_id
            await self.publish(message)

            # Wait for reply with timeout
            reply = await asyncio.wait_for(reply_future, timeout=timeout_seconds)
            return reply

        finally:
            # Clean up reply subscription
            await self.unsubscribe(sub_id)

    async def reply(self, original_message: Message, reply_payload: Any) -> None:
        """Send reply to original message"""
        if not original_message.reply_to:
            raise ValueError("Original message has no reply_to topic")

        reply = Message(
            topic=original_message.reply_to,
            payload=reply_payload,
            correlation_id=original_message.message_id,
            priority=original_message.priority,
        )

        await self.publish(reply)

    async def get_metrics(self) -> MessageBusMetrics:
        """Get Event Bus metrics"""
        if self._event_bus:
            eb_metrics = await self._event_bus.get_metrics()
            self._metrics.messages_published = eb_metrics.get(
                "events_published", 0)
            self._metrics.messages_delivered = eb_metrics.get(
                "events_delivered", 0)
            self._metrics.messages_failed = eb_metrics.get("events_failed", 0)
            self._metrics.average_delivery_time_ms = eb_metrics.get(
                "avg_delivery_time_ms", 0)
            self._metrics.active_subscribers = len(self._subscriptions)
            self._metrics.active_connections = eb_metrics.get(
                "active_connections", 0)

        return self._metrics

    async def health_check(self) -> bool:
        """Check Event Bus health"""
        if not self._running or not self._event_bus:
            return False

        try:
            # Simple health check - try to get metrics
            await self._event_bus.get_metrics()
            return True
        except Exception:
            return False

    # Helper methods for Event Bus integration

    def _topic_to_event_type(self, topic: str) -> str:
        """
        Convert topic string to Event Bus EventType.

        Examples:
            security.threat.detected -> THREAT_DETECTED
            productivity.task.created -> TASK_CREATED
            system.sync.started -> SYNC_STARTED
        """
        from apps.core.jane_orchestrator.src.services.event_bus_service import \
            EventType

        # Extract event name from topic (last segment uppercased)
        parts = topic.split(".")
        event_name = "_".join(parts[1:]).upper() if len(
            parts) > 1 else topic.upper()

        # Try to match to known EventType
        try:
            return EventType[event_name]
        except KeyError:
            # Default to generic event type
            return EventType.DATA_UPDATED

    def _event_to_message(self, event) -> Message:
        """Convert Event Bus Event to Message"""
        from apps.core.jane_orchestrator.src.services.event_bus_service import \
            EventPriority

        # Map priority
        priority_map = {
            EventPriority.CRITICAL: Priority.CRITICAL,
            EventPriority.HIGH: Priority.HIGH,
            EventPriority.MEDIUM: Priority.MEDIUM,
            EventPriority.LOW: Priority.LOW,
        }

        # Convert event type to topic
        topic = self._event_type_to_topic(
            event.event_type, event.source_domain)

        return Message(
            topic=topic,
            payload=event.payload,
            message_id=event.event_id,
            timestamp=event.timestamp,
            priority=priority_map.get(event.priority, Priority.MEDIUM),
            headers={
                "source_tool": event.source_tool,
                "source_domain": event.source_domain,
                "target_tools": event.target_tools,
                "target_domains": event.target_domains,
                **event.metadata,
            },
            ttl_seconds=event.ttl_seconds,
            delivery_required=event.delivery_required,
            user_id=event.user_id,
            session_id=event.session_id,
        )

    def _event_type_to_topic(self, event_type, source_domain) -> str:
        """
        Convert EventType to topic string.

        Examples:
            THREAT_DETECTED + SECURITY -> security.threat.detected
            TASK_CREATED + PRODUCTIVITY -> productivity.task.created
        """
        domain = source_domain.lower() if source_domain else "system"
        event = event_type.name.lower().replace("_", ".")
        return f"{domain}.{event}"
