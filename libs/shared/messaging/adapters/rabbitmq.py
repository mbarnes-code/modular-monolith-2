"""
RabbitMQ Adapter Implementation

Provides RabbitMQ message bus functionality with AMQP protocol.
"""

import asyncio
import json
from typing import Any, Dict, Optional

import aio_pika
from aio_pika import ExchangeType
from aio_pika import Message as AMQPMessage

from ..interfaces import (IMessageBus, Message, MessageBusMetrics, Priority,
                          PublishError, SubscriptionConfig, SubscriptionError)


class RabbitMQAdapter(IMessageBus):
    """
    RabbitMQ adapter using aio-pika library.

    Supports:
    - Topic-based routing via topic exchanges
    - Priority queues
    - Dead letter exchanges
    - Request/reply pattern with correlation IDs
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize RabbitMQ adapter.

        Args:
            config: Configuration dict with keys:
                - host: RabbitMQ host (default: localhost)
                - port: RabbitMQ port (default: 5672)
                - username: Authentication username (default: guest)
                - password: Authentication password (default: guest)
                - vhost: Virtual host (default: /)
                - exchange_name: Exchange to use (default: jane.events)
        """
        self.config = config
        self.host = config.get("host", "localhost")
        self.port = config.get("port", 5672)
        self.username = config.get("username", "guest")
        self.password = config.get("password", "guest")
        self.vhost = config.get("vhost", "/")
        self.exchange_name = config.get("exchange_name", "jane.events")

        # Internal state
        self._connection: Optional[aio_pika.Connection] = None
        self._channel: Optional[aio_pika.Channel] = None
        self._exchange: Optional[aio_pika.Exchange] = None
        self._subscriptions: Dict[str, Dict[str, Any]] = {}
        self._metrics = MessageBusMetrics()
        self._running = False

    async def start(self) -> None:
        """Initialize RabbitMQ connection"""
        if self._running:
            return

        try:
            # Connect to RabbitMQ
            self._connection = await aio_pika.connect_robust(
                host=self.host,
                port=self.port,
                login=self.username,
                password=self.password,
                virtualhost=self.vhost,
            )

            # Create channel
            self._channel = await self._connection.channel()
            await self._channel.set_qos(prefetch_count=10)

            # Declare topic exchange
            self._exchange = await self._channel.declare_exchange(
                name=self.exchange_name,
                type=ExchangeType.TOPIC,
                durable=True,
            )

            # Declare dead letter exchange
            await self._channel.declare_exchange(
                name=f"{self.exchange_name}.dlx",
                type=ExchangeType.TOPIC,
                durable=True,
            )

            self._running = True
            self._metrics.active_connections = 1

        except Exception as e:
            raise ConnectionError(f"Failed to connect to RabbitMQ: {e}") from e

    async def stop(self) -> None:
        """Shutdown RabbitMQ connection"""
        if not self._running:
            return

        # Cancel all subscriptions
        for sub_id in list(self._subscriptions.keys()):
            await self.unsubscribe(sub_id)

        # Close channel and connection
        if self._channel:
            await self._channel.close()

        if self._connection:
            await self._connection.close()

        self._running = False
        self._metrics.active_connections = 0

    async def publish(self, message: Message) -> str:
        """
        Publish message to RabbitMQ.

        Uses topic routing with routing key = message.topic
        """
        if not self._running:
            raise PublishError("RabbitMQ not started")

        try:
            # Convert Message to AMQP message
            body = json.dumps({
                "payload": message.payload,
                "message_id": message.message_id,
                "timestamp": message.timestamp.isoformat(),
                "user_id": message.user_id,
                "session_id": message.session_id,
                "correlation_id": message.correlation_id,
                "headers": message.headers,
            }).encode()

            # Map priority to AMQP priority (0-9)
            priority_map = {
                Priority.CRITICAL: 9,
                Priority.HIGH: 7,
                Priority.MEDIUM: 5,
                Priority.LOW: 1,
            }

            amqp_message = AMQPMessage(
                body=body,
                content_type=message.content_type.value,
                message_id=message.message_id,
                correlation_id=message.correlation_id,
                reply_to=message.reply_to,
                priority=priority_map.get(message.priority, 5),
                expiration=str(message.ttl_seconds *
                               1000) if message.ttl_seconds else None,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT if message.delivery_required else aio_pika.DeliveryMode.NOT_PERSISTENT,
            )

            # Publish to exchange with routing key = topic
            await self._exchange.publish(
                message=amqp_message,
                routing_key=message.topic,
                mandatory=message.delivery_required,
            )

            self._metrics.messages_published += 1
            return message.message_id

        except Exception as e:
            self._metrics.messages_failed += 1
            raise PublishError(f"Failed to publish to RabbitMQ: {e}") from e

    async def subscribe(self, config: SubscriptionConfig) -> str:
        """
        Subscribe to RabbitMQ topics.

        Creates a queue bound to topic patterns.
        """
        if not self._running:
            raise SubscriptionError("RabbitMQ not started")

        try:
            # Create queue with dead letter exchange
            queue_args = {
                "x-dead-letter-exchange": f"{self.exchange_name}.dlx",
                "x-message-ttl": 86400000,  # 24 hours
            }

            queue = await self._channel.declare_queue(
                name=f"queue.{config.handler_id}",
                durable=True,
                arguments=queue_args,
            )

            # Bind queue to topic patterns
            for topic in config.topics:
                await queue.bind(
                    exchange=self._exchange,
                    routing_key=topic,
                )

            # Start consuming
            async def on_message(amqp_message: aio_pika.IncomingMessage):
                async with amqp_message.process(
                    requeue=False,
                    reject_on_redelivered=True,
                ):
                    try:
                        # Convert AMQP message to Message
                        message = self._amqp_to_message(amqp_message)

                        # Apply filters if configured
                        if config.filters and not self._apply_filters(message, config.filters):
                            return

                        # Call handler
                        await config.callback(message)

                        self._metrics.messages_delivered += 1

                    except Exception as e:
                        self._metrics.messages_failed += 1
                        # Message will go to DLX due to reject_on_redelivered
                        raise

            consumer_tag = await queue.consume(on_message)

            # Store subscription
            self._subscriptions[config.handler_id] = {
                "queue": queue,
                "consumer_tag": consumer_tag,
                "config": config,
            }

            self._metrics.active_subscribers += 1
            return config.handler_id

        except Exception as e:
            raise SubscriptionError(
                f"Failed to subscribe to RabbitMQ: {e}") from e

    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from RabbitMQ"""
        if subscription_id not in self._subscriptions:
            return

        try:
            sub = self._subscriptions[subscription_id]
            queue = sub["queue"]

            # Cancel consumer
            await queue.cancel(sub["consumer_tag"])

            # Delete queue
            await queue.delete()

            del self._subscriptions[subscription_id]
            self._metrics.active_subscribers -= 1

        except Exception:
            pass  # Best effort cleanup

    async def request(self, message: Message, timeout_seconds: int = 30) -> Message:
        """
        Request/reply pattern using RabbitMQ.

        Uses correlation_id and reply_to for matching.
        """
        if not message.reply_to:
            # Create temporary reply queue
            message.reply_to = f"reply.{message.message_id}"

        # Create reply queue
        reply_queue = await self._channel.declare_queue(
            name=message.reply_to,
            exclusive=True,
            auto_delete=True,
        )

        reply_future = asyncio.Future()

        async def on_reply(amqp_message: aio_pika.IncomingMessage):
            async with amqp_message.process():
                if amqp_message.correlation_id == message.message_id:
                    reply = self._amqp_to_message(amqp_message)
                    reply_future.set_result(reply)

        # Start consuming replies
        consumer_tag = await reply_queue.consume(on_reply)

        try:
            # Set correlation ID and publish request
            message.correlation_id = message.message_id
            await self.publish(message)

            # Wait for reply with timeout
            reply = await asyncio.wait_for(reply_future, timeout=timeout_seconds)
            return reply

        finally:
            # Clean up reply queue
            await reply_queue.cancel(consumer_tag)
            await reply_queue.delete()

    async def reply(self, original_message: Message, reply_payload: Any) -> None:
        """Send reply to original message"""
        if not original_message.reply_to:
            raise ValueError("Original message has no reply_to queue")

        reply = Message(
            topic=original_message.reply_to,
            payload=reply_payload,
            correlation_id=original_message.message_id,
            priority=original_message.priority,
        )

        await self.publish(reply)

    async def get_metrics(self) -> MessageBusMetrics:
        """Get RabbitMQ metrics"""
        # Update queue depth
        total_messages = 0
        for sub in self._subscriptions.values():
            queue = sub["queue"]
            declaration = await queue.declare(passive=True)
            total_messages += declaration.message_count

        self._metrics.queue_depth = total_messages
        return self._metrics

    async def health_check(self) -> bool:
        """Check RabbitMQ health"""
        if not self._running or not self._connection:
            return False

        return not self._connection.is_closed

    # Helper methods

    def _amqp_to_message(self, amqp_message: aio_pika.IncomingMessage) -> Message:
        """Convert AMQP message to Message"""
        # Parse JSON body
        data = json.loads(amqp_message.body.decode())

        # Map AMQP priority to Priority enum
        priority_map = {
            9: Priority.CRITICAL,
            7: Priority.HIGH,
            5: Priority.MEDIUM,
            1: Priority.LOW,
        }
        priority = priority_map.get(
            amqp_message.priority or 5, Priority.MEDIUM)

        from datetime import datetime
        return Message(
            topic=amqp_message.routing_key or "",
            payload=data.get("payload"),
            message_id=data.get("message_id", amqp_message.message_id),
            timestamp=datetime.fromisoformat(data.get("timestamp")) if data.get(
                "timestamp") else datetime.utcnow(),
            priority=priority,
            headers=data.get("headers", {}),
            user_id=data.get("user_id"),
            session_id=data.get("session_id"),
            correlation_id=data.get(
                "correlation_id", amqp_message.correlation_id),
            reply_to=amqp_message.reply_to,
        )

    def _apply_filters(self, message: Message, filters: Dict[str, Any]) -> bool:
        """Apply message filters"""
        for key, value in filters.items():
            # Simple equality filter
            if key in message.headers:
                if message.headers[key] != value:
                    return False
        return True
