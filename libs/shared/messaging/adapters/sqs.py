"""
AWS SQS Adapter Implementation

Provides AWS Simple Queue Service functionality.
"""

import asyncio
import json
import zlib
from base64 import b64decode, b64encode
from typing import Any, Dict, Optional

import aioboto3

from ..interfaces import (IMessageBus, Message, MessageBusMetrics, Priority,
                          PublishError, SubscriptionConfig, SubscriptionError)


class SQSAdapter(IMessageBus):
    """
    AWS SQS adapter using aioboto3 library.

    Supports:
    - Queue-based messaging
    - Long polling
    - Message attributes
    - Dead letter queues
    - Compression (zlib)
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize SQS adapter.

        Args:
            config: Configuration dict with keys:
                - region_name: AWS region (default: us-east-1)
                - aws_access_key_id: AWS access key
                - aws_secret_access_key: AWS secret key
                - queue_prefix: Queue name prefix (default: jane-)
                - use_compression: Enable zlib compression (default: True)
                - wait_time_seconds: Long polling wait (default: 20)
        """
        self.config = config
        self.region_name = config.get("region_name", "us-east-1")
        self.aws_access_key_id = config.get("aws_access_key_id")
        self.aws_secret_access_key = config.get("aws_secret_access_key")
        self.queue_prefix = config.get("queue_prefix", "jane-")
        self.use_compression = config.get("use_compression", True)
        self.wait_time_seconds = config.get("wait_time_seconds", 20)

        # Internal state
        self._session: Optional[aioboto3.Session] = None
        self._sqs_client = None
        self._queue_urls: Dict[str, str] = {}
        self._consumer_tasks: Dict[str, asyncio.Task] = {}
        self._metrics = MessageBusMetrics()
        self._running = False

    async def start(self) -> None:
        """Initialize SQS session"""
        if self._running:
            return

        try:
            # Create aioboto3 session
            self._session = aioboto3.Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name,
            )

            self._running = True
            self._metrics.active_connections = 1

        except Exception as e:
            raise ConnectionError(
                f"Failed to initialize SQS session: {e}") from e

    async def stop(self) -> None:
        """Shutdown SQS session"""
        if not self._running:
            return

        # Cancel all consumer tasks
        for task in self._consumer_tasks.values():
            task.cancel()

        await asyncio.gather(*self._consumer_tasks.values(), return_exceptions=True)

        self._running = False
        self._metrics.active_connections = 0

    async def publish(self, message: Message) -> str:
        """
        Publish message to SQS queue.

        Queue name is derived from message.topic.
        """
        if not self._running:
            raise PublishError("SQS not started")

        try:
            async with self._session.client("sqs") as sqs:
                # Get or create queue URL
                queue_url = await self._get_queue_url(sqs, message.topic)

                # Prepare message body
                body_data = {
                    "payload": message.payload,
                    "message_id": message.message_id,
                    "timestamp": message.timestamp.isoformat(),
                    "user_id": message.user_id,
                    "session_id": message.session_id,
                    "correlation_id": message.correlation_id,
                    "headers": message.headers,
                }

                body = json.dumps(body_data)

                # Apply compression if enabled
                if self.use_compression:
                    body = b64encode(zlib.compress(body.encode())).decode()

                # Prepare message attributes
                attributes = {
                    "Priority": {
                        "DataType": "String",
                        "StringValue": message.priority.value,
                    },
                    "ContentType": {
                        "DataType": "String",
                        "StringValue": message.content_type.value,
                    },
                    "Compressed": {
                        "DataType": "String",
                        "StringValue": str(self.use_compression),
                    },
                }

                if message.correlation_id:
                    attributes["CorrelationId"] = {
                        "DataType": "String",
                        "StringValue": message.correlation_id,
                    }

                # Send message
                response = await sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=body,
                    MessageAttributes=attributes,
                    DelaySeconds=0,
                )

                self._metrics.messages_published += 1
                return response["MessageId"]

        except Exception as e:
            self._metrics.messages_failed += 1
            raise PublishError(f"Failed to publish to SQS: {e}") from e

    async def subscribe(self, config: SubscriptionConfig) -> str:
        """
        Subscribe to SQS queues.

        Creates consumers for each topic (queue).
        """
        if not self._running:
            raise SubscriptionError("SQS not started")

        try:
            # Start consuming task for each topic
            task = asyncio.create_task(
                self._consume_loop(config)
            )
            self._consumer_tasks[config.handler_id] = task

            self._metrics.active_subscribers += 1
            return config.handler_id

        except Exception as e:
            raise SubscriptionError(f"Failed to subscribe to SQS: {e}") from e

    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from SQS queues"""
        if subscription_id not in self._consumer_tasks:
            return

        try:
            # Cancel consumer task
            self._consumer_tasks[subscription_id].cancel()
            await asyncio.gather(
                self._consumer_tasks[subscription_id],
                return_exceptions=True,
            )
            del self._consumer_tasks[subscription_id]

            self._metrics.active_subscribers -= 1

        except Exception:
            pass  # Best effort cleanup

    async def request(self, message: Message, timeout_seconds: int = 30) -> Message:
        """
        Request/reply pattern using SQS.

        Uses correlation_id and temporary reply queue.
        """
        if not message.reply_to:
            message.reply_to = f"reply-{message.message_id}"

        reply_future = asyncio.Future()

        async def reply_handler(reply_msg: Message):
            if reply_msg.correlation_id == message.message_id:
                reply_future.set_result(reply_msg)

        # Subscribe to reply queue
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

            # Clean up reply queue
            async with self._session.client("sqs") as sqs:
                queue_url = await self._get_queue_url(sqs, message.reply_to)
                await sqs.delete_queue(QueueUrl=queue_url)

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
        """Get SQS metrics"""
        # Calculate total queue depth
        total_messages = 0

        async with self._session.client("sqs") as sqs:
            for queue_url in self._queue_urls.values():
                try:
                    response = await sqs.get_queue_attributes(
                        QueueUrl=queue_url,
                        AttributeNames=["ApproximateNumberOfMessages"],
                    )
                    total_messages += int(
                        response["Attributes"]["ApproximateNumberOfMessages"]
                    )
                except Exception:
                    pass

        self._metrics.queue_depth = total_messages
        return self._metrics

    async def health_check(self) -> bool:
        """Check SQS health"""
        if not self._running or not self._session:
            return False

        try:
            # Try to list queues
            async with self._session.client("sqs") as sqs:
                await sqs.list_queues(QueueNamePrefix=self.queue_prefix)
            return True
        except Exception:
            return False

    # Helper methods

    async def _get_queue_url(self, sqs, topic: str) -> str:
        """Get or create queue URL for topic"""
        queue_name = f"{self.queue_prefix}{topic.replace('.', '-')}"

        if queue_name in self._queue_urls:
            return self._queue_urls[queue_name]

        try:
            # Try to get existing queue
            response = await sqs.get_queue_url(QueueName=queue_name)
            queue_url = response["QueueUrl"]

        except sqs.exceptions.QueueDoesNotExist:
            # Create new queue
            response = await sqs.create_queue(
                QueueName=queue_name,
                Attributes={
                    "VisibilityTimeout": "40",
                    "MessageRetentionPeriod": "86400",  # 24 hours
                },
            )
            queue_url = response["QueueUrl"]

        self._queue_urls[queue_name] = queue_url
        return queue_url

    async def _consume_loop(self, config: SubscriptionConfig) -> None:
        """Background task to consume messages from queues"""
        try:
            async with self._session.client("sqs") as sqs:
                while True:
                    # Poll each topic/queue
                    for topic in config.topics:
                        queue_url = await self._get_queue_url(sqs, topic)

                        # Receive messages
                        response = await sqs.receive_message(
                            QueueUrl=queue_url,
                            MaxNumberOfMessages=config.batch_size,
                            WaitTimeSeconds=self.wait_time_seconds,
                            MessageAttributeNames=["All"],
                        )

                        messages = response.get("Messages", [])

                        for sqs_msg in messages:
                            try:
                                # Convert SQS message to Message
                                message = self._sqs_to_message(sqs_msg, topic)

                                # Apply filters
                                if config.filters and not self._apply_filters(
                                    message, config.filters
                                ):
                                    continue

                                # Call handler
                                await config.callback(message)

                                # Delete message if ack required
                                if config.ack_required:
                                    await sqs.delete_message(
                                        QueueUrl=queue_url,
                                        ReceiptHandle=sqs_msg["ReceiptHandle"],
                                    )

                                self._metrics.messages_delivered += 1

                            except Exception as e:
                                self._metrics.messages_failed += 1
                                # Message will become visible again

        except asyncio.CancelledError:
            pass  # Task cancelled

    def _sqs_to_message(self, sqs_msg: Dict[str, Any], topic: str) -> Message:
        """Convert SQS message to Message"""
        from datetime import datetime

        # Get message attributes
        attrs = sqs_msg.get("MessageAttributes", {})

        compressed = attrs.get("Compressed", {}).get("StringValue") == "True"

        # Decompress body if needed
        body = sqs_msg["Body"]
        if compressed:
            body = zlib.decompress(b64decode(body)).decode()

        # Parse JSON body
        data = json.loads(body)

        # Map priority
        priority_str = attrs.get("Priority", {}).get("StringValue", "medium")
        priority = Priority(priority_str)

        return Message(
            topic=topic,
            payload=data.get("payload"),
            message_id=data.get("message_id", sqs_msg["MessageId"]),
            timestamp=datetime.fromisoformat(data.get("timestamp")) if data.get(
                "timestamp") else datetime.utcnow(),
            priority=priority,
            headers=data.get("headers", {}),
            user_id=data.get("user_id"),
            session_id=data.get("session_id"),
            correlation_id=data.get("correlation_id", attrs.get(
                "CorrelationId", {}).get("StringValue")),
        )

    def _apply_filters(self, message: Message, filters: Dict[str, Any]) -> bool:
        """Apply message filters"""
        for key, value in filters.items():
            if key in message.headers:
                if message.headers[key] != value:
                    return False
        return True
