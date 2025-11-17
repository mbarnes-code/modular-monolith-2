"""
Message Bus Abstraction Layer - Core Interfaces

Provides a unified interface for message bus implementations,
enabling config-driven adapter swapping without domain code changes.

Supports: Event Bus, RabbitMQ, Kafka, AWS SQS
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import uuid4


class Priority(Enum):
    """Message priority levels"""
    CRITICAL = "critical"  # <200ms delivery requirement
    HIGH = "high"          # <1s delivery requirement
    MEDIUM = "medium"      # <5s delivery requirement
    LOW = "low"            # Best effort delivery


class MessageFormat(Enum):
    """Standard message formats"""
    JSON = "application/json"
    CLOUDEVENTS = "application/cloudevents+json"
    AVRO = "application/avro"
    PROTOBUF = "application/protobuf"


@dataclass
class Message:
    """
    Universal message format for all message bus implementations.

    Attributes:
        topic: Message routing topic/channel
        payload: Message data (dict for JSON, bytes for binary)
        message_id: Unique message identifier
        timestamp: Message creation time
        priority: Delivery priority level
        headers: Additional metadata
        content_type: Message format
        ttl_seconds: Time-to-live (None = no expiration)
        delivery_required: Whether delivery confirmation is needed
        user_id: Optional user context
        session_id: Optional session context
        correlation_id: Optional correlation for request/reply
        reply_to: Optional reply-to topic for request/reply pattern
    """
    topic: str
    payload: Any
    message_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    priority: Priority = Priority.MEDIUM
    headers: Dict[str, Any] = field(default_factory=dict)
    content_type: MessageFormat = MessageFormat.JSON
    ttl_seconds: Optional[int] = 300
    delivery_required: bool = False
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary representation"""
        return {
            "topic": self.topic,
            "payload": self.payload,
            "message_id": self.message_id,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "headers": self.headers,
            "content_type": self.content_type.value,
            "ttl_seconds": self.ttl_seconds,
            "delivery_required": self.delivery_required,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "correlation_id": self.correlation_id,
            "reply_to": self.reply_to,
        }


@dataclass
class SubscriptionConfig:
    """
    Configuration for message subscriptions.

    Attributes:
        handler_id: Unique identifier for this subscription
        topics: List of topic patterns to subscribe to
        callback: Async function to handle messages
        filters: Optional message filtering predicates
        max_retries: Maximum retry attempts on failure
        dead_letter_topic: Topic for failed messages
        batch_size: Number of messages to batch (if supported)
        ack_required: Whether acknowledgment is required
    """
    handler_id: str
    topics: List[str]
    callback: Callable
    filters: Optional[Dict[str, Any]] = None
    max_retries: int = 3
    dead_letter_topic: Optional[str] = None
    batch_size: int = 1
    ack_required: bool = True


@dataclass
class MessageBusMetrics:
    """Message bus performance metrics"""
    messages_published: int = 0
    messages_delivered: int = 0
    messages_failed: int = 0
    average_delivery_time_ms: float = 0.0
    active_subscribers: int = 0
    active_connections: int = 0
    queue_depth: int = 0


class IMessageBus(ABC):
    """
    Abstract interface for message bus implementations.

    Provides pub/sub, request/reply, and fan-out messaging patterns.
    All implementations must support:
    - Topic-based routing
    - Priority-based delivery
    - Retry logic with dead letter queues
    - Metrics collection
    """

    @abstractmethod
    async def start(self) -> None:
        """
        Initialize the message bus connection.

        Raises:
            ConnectionError: If connection cannot be established
        """
        pass

    @abstractmethod
    async def stop(self) -> None:
        """
        Gracefully shutdown the message bus connection.
        Ensures all pending messages are flushed.
        """
        pass

    @abstractmethod
    async def publish(
        self,
        message: Message,
    ) -> str:
        """
        Publish a message to the bus.

        Args:
            message: Message to publish

        Returns:
            Message ID for tracking

        Raises:
            PublishError: If message cannot be published
        """
        pass

    @abstractmethod
    async def subscribe(
        self,
        config: SubscriptionConfig,
    ) -> str:
        """
        Subscribe to message topics.

        Args:
            config: Subscription configuration

        Returns:
            Subscription ID for management

        Raises:
            SubscriptionError: If subscription fails
        """
        pass

    @abstractmethod
    async def unsubscribe(
        self,
        subscription_id: str,
    ) -> None:
        """
        Unsubscribe from topics.

        Args:
            subscription_id: ID returned from subscribe()
        """
        pass

    @abstractmethod
    async def request(
        self,
        message: Message,
        timeout_seconds: int = 30,
    ) -> Message:
        """
        Send a request and wait for a reply (request/reply pattern).

        Args:
            message: Request message (must have reply_to set)
            timeout_seconds: Maximum wait time for reply

        Returns:
            Reply message

        Raises:
            TimeoutError: If no reply received within timeout
        """
        pass

    @abstractmethod
    async def reply(
        self,
        original_message: Message,
        reply_payload: Any,
    ) -> None:
        """
        Reply to a request message.

        Args:
            original_message: Original request message
            reply_payload: Reply data
        """
        pass

    @abstractmethod
    async def get_metrics(self) -> MessageBusMetrics:
        """
        Get current message bus metrics.

        Returns:
            Current performance metrics
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check message bus health.

        Returns:
            True if healthy, False otherwise
        """
        pass


class IMessageBusFactory(ABC):
    """
    Factory interface for creating message bus instances.

    Enables config-driven adapter selection.
    """

    @staticmethod
    @abstractmethod
    def create(
        adapter_type: str,
        config: Dict[str, Any],
    ) -> IMessageBus:
        """
        Create a message bus adapter instance.

        Args:
            adapter_type: Type of adapter (eventbus, rabbitmq, kafka, sqs)
            config: Adapter-specific configuration

        Returns:
            Configured message bus instance

        Raises:
            ValueError: If adapter_type is unknown
            ConfigurationError: If config is invalid
        """
        pass


class MessageBusError(Exception):
    """Base exception for message bus errors"""
    pass


class PublishError(MessageBusError):
    """Error publishing message"""
    pass


class SubscriptionError(MessageBusError):
    """Error subscribing to topics"""
    pass


class ConfigurationError(MessageBusError):
    """Invalid configuration"""
    pass
