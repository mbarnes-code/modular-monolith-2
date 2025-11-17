"""
Kafka Adapter Implementation

Provides Apache Kafka message streaming functionality.
"""

import asyncio
import json
from typing import Any, Dict, List, Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError

from ..interfaces import (IMessageBus, Message, MessageBusMetrics, Priority,
                          PublishError, SubscriptionConfig, SubscriptionError)


class KafkaAdapter(IMessageBus):
    """
    Apache Kafka adapter using aiokafka library.

    Supports:
    - Topic-based streaming
    - Consumer groups
    - Offset management
    - Partition assignment
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize Kafka adapter.

        Args:
            config: Configuration dict with keys:
                - bootstrap_servers: Kafka brokers (default: localhost:9092)
                - client_id: Client identifier (default: jane-kafka)
                - group_id: Consumer group ID (default: jane-consumers)
                - compression_type: Message compression (default: gzip)
        """
        self.config = config
        self.bootstrap_servers = config.get(
            "bootstrap_servers", "localhost:9092")
        self.client_id = config.get("client_id", "jane-kafka")
        self.group_id = config.get("group_id", "jane-consumers")
        self.compression_type = config.get("compression_type", "gzip")

        # Internal state
        self._producer: Optional[AIOKafkaProducer] = None
        self._consumers: Dict[str, AIOKafkaConsumer] = {}
        self._consumer_tasks: Dict[str, asyncio.Task] = {}
        self._metrics = MessageBusMetrics()
        self._running = False

    async def start(self) -> None:
        """Initialize Kafka producer"""
        if self._running:
            return

        try:
            # Create producer
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                client_id=self.client_id,
                compression_type=self.compression_type,
                value_serializer=lambda v: json.dumps(v).encode(),
            )

            await self._producer.start()
            self._running = True
            self._metrics.active_connections = 1

        except KafkaError as e:
            raise ConnectionError(f"Failed to connect to Kafka: {e}") from e

    async def stop(self) -> None:
        """Shutdown Kafka connections"""
        if not self._running:
            return

        # Cancel all consumer tasks
        for task in self._consumer_tasks.values():
            task.cancel()

        await asyncio.gather(*self._consumer_tasks.values(), return_exceptions=True)

        # Stop all consumers
        for consumer in self._consumers.values():
            await consumer.stop()

        # Stop producer
        if self._producer:
            await self._producer.stop()

        self._running = False
        self._metrics.active_connections = 0

    async def publish(self, message: Message) -> str:
        """
        Publish message to Kafka topic.

        Topic name comes from message.topic.
        """
        if not self._running:
            raise PublishError("Kafka not started")

        try:
            # Convert Message to Kafka record value
            value = {
                "payload": message.payload,
                "message_id": message.message_id,
                "timestamp": message.timestamp.isoformat(),
                "priority": message.priority.value,
                "user_id": message.user_id,
                "session_id": message.session_id,
                "correlation_id": message.correlation_id,
                "headers": message.headers,
            }

            # Prepare headers
            headers = [
                ("content_type", message.content_type.value.encode()),
                ("priority", message.priority.value.encode()),
            ]
            if message.correlation_id:
                headers.append(
                    ("correlation_id", message.correlation_id.encode()))

            # Send to Kafka
            await self._producer.send(
                topic=message.topic,
                value=value,
                headers=headers,
            )

            self._metrics.messages_published += 1
            return message.message_id

        except KafkaError as e:
            self._metrics.messages_failed += 1
            raise PublishError(f"Failed to publish to Kafka: {e}") from e

    async def subscribe(self, config: SubscriptionConfig) -> str:
        """
        Subscribe to Kafka topics.

        Creates a consumer and starts consuming in background.
        """
        if not self._running:
            raise SubscriptionError("Kafka not started")

        try:
            # Create consumer
            consumer = AIOKafkaConsumer(
                *config.topics,
                bootstrap_servers=self.bootstrap_servers,
                client_id=f"{self.client_id}_{config.handler_id}",
                group_id=self.group_id,
                value_deserializer=lambda m: json.loads(m.decode()),
                enable_auto_commit=config.ack_required,
            )

            await consumer.start()
            self._consumers[config.handler_id] = consumer

            # Start consuming in background
            task = asyncio.create_task(
                self._consume_loop(config.handler_id, config)
            )
            self._consumer_tasks[config.handler_id] = task

            self._metrics.active_subscribers += 1
            return config.handler_id

        except KafkaError as e:
            raise SubscriptionError(
                f"Failed to subscribe to Kafka: {e}") from e

    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from Kafka topics"""
        if subscription_id not in self._consumers:
            return

        try:
            # Cancel consumer task
            if subscription_id in self._consumer_tasks:
                self._consumer_tasks[subscription_id].cancel()
                await asyncio.gather(
                    self._consumer_tasks[subscription_id],
                    return_exceptions=True,
                )
                del self._consumer_tasks[subscription_id]

            # Stop consumer
            consumer = self._consumers[subscription_id]
            await consumer.stop()
            del self._consumers[subscription_id]

            self._metrics.active_subscribers -= 1

        except Exception:
            pass  # Best effort cleanup

    async def request(self, message: Message, timeout_seconds: int = 30) -> Message:
        """
        Request/reply pattern using Kafka.

        Note: Kafka doesn't natively support request/reply.
        This implementation uses correlation_id matching on reply topic.
        """
        if not message.reply_to:
            raise ValueError(
                "Message must have reply_to topic for request/reply")

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

            # Wait for reply
            reply = await asyncio.wait_for(reply_future, timeout=timeout_seconds)
            return reply

        finally:
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
        """Get Kafka metrics"""
        # Kafka metrics would require additional monitoring setup
        return self._metrics

    async def health_check(self) -> bool:
        """Check Kafka health"""
        if not self._running or not self._producer:
            return False

        try:
            # Try to get cluster metadata
            await self._producer.client.fetch_all_metadata()
            return True
        except Exception:
            return False

    # Helper methods

    async def _consume_loop(
        self,
        handler_id: str,
        config: SubscriptionConfig,
    ) -> None:
        """Background task to consume messages"""
        consumer = self._consumers[handler_id]

        try:
            async for kafka_msg in consumer:
                try:
                    # Convert Kafka message to Message
                    message = self._kafka_to_message(kafka_msg)

                    # Apply filters if configured
                    if config.filters and not self._apply_filters(message, config.filters):
                        continue

                    # Call handler
                    await config.callback(message)

                    self._metrics.messages_delivered += 1

                except Exception as e:
                    self._metrics.messages_failed += 1
                    # Log error but continue consuming

        except asyncio.CancelledError:
            # Task cancelled, exit gracefully
            pass

    def _kafka_to_message(self, kafka_msg) -> Message:
        """Convert Kafka message to Message"""
        from datetime import datetime

        value = kafka_msg.value

        # Parse headers
        headers_dict = {}
        if kafka_msg.headers:
            headers_dict = {k: v.decode() for k, v in kafka_msg.headers}

        # Map priority
        priority_str = headers_dict.get("priority", "medium")
        priority = Priority(priority_str)

        return Message(
            topic=kafka_msg.topic,
            payload=value.get("payload"),
            message_id=value.get("message_id", str(kafka_msg.offset)),
            timestamp=datetime.fromisoformat(value.get("timestamp")) if value.get(
                "timestamp") else datetime.utcnow(),
            priority=priority,
            headers=value.get("headers", {}),
            user_id=value.get("user_id"),
            session_id=value.get("session_id"),
            correlation_id=value.get(
                "correlation_id", headers_dict.get("correlation_id")),
        )

    def _apply_filters(self, message: Message, filters: Dict[str, Any]) -> bool:
        """Apply message filters"""
        for key, value in filters.items():
            if key in message.headers:
                if message.headers[key] != value:
                    return False
        return True
