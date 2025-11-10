"""
MISP External API Integrations Service

Preserves external API integrations from Section 5.1 maintaining error handling 
and fallback behavior for:
- Feed imports
- Threat intel sharing 
- Webhook notifications

Migrated from features/MISP/app/Model/Feed.php, Server.php, Workflow.php
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import aiohttp
import httpx
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from ...core.exceptions import (ExternalAPIError, FeedImportError, SyncError,
                                WebhookError)
from ...data.models.misp_attributes import Attribute
from ...data.models.misp_events import Event
from ...data.models.misp_external_integrations import (FeedConfig,
                                                       FeedImportLog,
                                                       ServerConfig, SyncLog,
                                                       WebhookConfig,
                                                       WebhookLog)
from .attributes_service import AttributesService
from .events_service import EventsService

logger = logging.getLogger(__name__)


class ExternalAPIsService:
    """
    Service for managing MISP external API integrations with error handling
    and fallback behavior preservation.

    Maintains compatibility with original MISP feed imports, server sync,
    and webhook notification functionality.
    """

    def __init__(self, session: Session):
        self.session = session
        self.events_service = EventsService(session)
        self.attributes_service = AttributesService(session)

        # HTTP client configuration with error handling
        self.http_timeout = aiohttp.ClientTimeout(total=300, connect=30)
        self.max_retries = 3
        self.retry_delay = 5

    # Feed Import Service Methods

    async def import_feed(
        self,
        feed_id: int,
        user_id: int,
        force: bool = False
    ) -> Dict[str, Any]:
        """
        Import threat intelligence from external feed with error handling.

        Preserves original MISP feed import behavior from Feed.php importFeeds()
        """
        try:
            # Get feed configuration
            feed = await self._get_feed_config(feed_id)
            if not feed or not feed.enabled:
                raise FeedImportError(f"Feed {feed_id} not found or disabled")

            logger.info(
                f"Starting feed import for feed {feed_id}: {feed.name}")

            # Check feed availability with fallback
            feed_data = await self._fetch_feed_data(feed)
            if not feed_data:
                return await self._handle_feed_import_failure(
                    feed_id, user_id, "Failed to fetch feed data"
                )

            # Parse and validate feed data
            parsed_data = await self._parse_feed_data(feed, feed_data)
            if not parsed_data:
                return await self._handle_feed_import_failure(
                    feed_id, user_id, "Failed to parse feed data"
                )

            # Import with error tracking
            results = await self._import_feed_events(
                feed, parsed_data, user_id, force
            )

            # Log successful import
            await self._log_feed_import(
                feed_id, user_id, 'success',
                f"Imported {results['successes']} events, {results['failures']} failures"
            )

            return {
                'status': 'success',
                'feed_id': feed_id,
                'successes': results['successes'],
                'failures': results['failures'],
                'processed_at': datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Feed import failed for feed {feed_id}: {str(e)}")
            await self._handle_feed_import_failure(feed_id, user_id, str(e))
            raise FeedImportError(f"Feed import failed: {str(e)}")

    async def _fetch_feed_data(self, feed: FeedConfig) -> Optional[str]:
        """
        Fetch feed data with retry logic and error handling.

        Preserves original MISP feed fetching behavior with fallback.
        """
        headers = self._build_feed_headers(feed)

        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(
                    timeout=self.http_timeout,
                    headers=headers
                ) as session:
                    async with session.get(feed.url) as response:
                        if response.status == 200:
                            return await response.text()
                        elif response.status == 304:
                            # Not modified, use cached data if available
                            return await self._get_cached_feed_data(feed.id)
                        else:
                            logger.warning(
                                f"Feed {feed.id} returned status {response.status}, "
                                f"attempt {attempt + 1}/{self.max_retries}"
                            )

            except Exception as e:
                logger.warning(
                    f"Feed fetch attempt {attempt + 1} failed for {feed.id}: {str(e)}"
                )

                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (attempt + 1))

        # Fallback to cached data on failure
        return await self._get_cached_feed_data(feed.id)

    async def _parse_feed_data(
        self,
        feed: FeedConfig,
        data: str
    ) -> Optional[List[Dict]]:
        """
        Parse feed data based on format with error handling.

        Supports MISP JSON, freetext, and CSV formats.
        """
        try:
            if feed.source_format == 'misp':
                return await self._parse_misp_feed(data)
            elif feed.source_format == 'freetext':
                return await self._parse_freetext_feed(data, feed.rules or {})
            elif feed.source_format == 'csv':
                return await self._parse_csv_feed(data, feed.rules or {})
            else:
                raise FeedImportError(
                    f"Unsupported feed format: {feed.source_format}")

        except Exception as e:
            logger.error(f"Feed parsing failed for {feed.id}: {str(e)}")
            return None

    # Server Synchronization Methods

    async def sync_with_server(
        self,
        server_id: int,
        user_id: int,
        sync_type: str = 'pull'  # 'pull', 'push', 'full'
    ) -> Dict[str, Any]:
        """
        Synchronize with remote MISP server with error handling.

        Preserves original MISP server sync behavior from Server.php
        """
        try:
            server = await self._get_server_config(server_id)
            if not server or not server.enabled:
                raise SyncError(f"Server {server_id} not found or disabled")

            logger.info(
                f"Starting {sync_type} sync with server {server_id}: {server.name}")

            # Test server connectivity with fallback
            if not await self._test_server_connection(server):
                return await self._handle_sync_failure(
                    server_id, user_id, "Server connectivity test failed"
                )

            results = {'successes': 0, 'failures': 0, 'errors': []}

            if sync_type in ['pull', 'full']:
                pull_results = await self._pull_from_server(server, user_id)
                results['successes'] += pull_results['successes']
                results['failures'] += pull_results['failures']
                results['errors'].extend(pull_results['errors'])

            if sync_type in ['push', 'full']:
                push_results = await self._push_to_server(server, user_id)
                results['successes'] += push_results['successes']
                results['failures'] += push_results['failures']
                results['errors'].extend(push_results['errors'])

            # Log successful sync
            await self._log_sync_operation(
                server_id, user_id, sync_type, 'success',
                f"Sync completed: {results['successes']} successes, {results['failures']} failures"
            )

            return {
                'status': 'success',
                'server_id': server_id,
                'sync_type': sync_type,
                'results': results,
                'synced_at': datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(
                f"Server sync failed for server {server_id}: {str(e)}")
            await self._handle_sync_failure(server_id, user_id, str(e))
            raise SyncError(f"Server sync failed: {str(e)}")

    async def _test_server_connection(self, server: ServerConfig) -> bool:
        """
        Test connectivity to remote MISP server with error handling.

        Preserves original MISP server testing functionality.
        """
        try:
            headers = {
                'Authorization': server.authkey,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }

            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers=headers
            ) as session:
                test_url = urljoin(server.url, '/servers/getVersion')
                async with session.get(test_url) as response:
                    return response.status == 200

        except Exception as e:
            logger.warning(
                f"Server connection test failed for {server.id}: {str(e)}")
            return False

    async def _pull_from_server(
        self,
        server: ServerConfig,
        user_id: int
    ) -> Dict[str, Any]:
        """
        Pull events from remote server with error handling and fallback.

        Preserves original MISP pull functionality from Server.php
        """
        results = {'successes': 0, 'failures': 0, 'errors': []}

        try:
            # Get event list from remote server
            event_list = await self._get_remote_event_list(server)

            for event_uuid in event_list:
                try:
                    # Check if event already exists
                    if await self._event_exists_locally(event_uuid):
                        continue

                    # Fetch event from remote server
                    event_data = await self._fetch_remote_event(server, event_uuid)
                    if not event_data:
                        results['failures'] += 1
                        results['errors'].append(
                            f"Failed to fetch event {event_uuid}")
                        continue

                    # Import event with validation
                    if await self._import_remote_event(event_data, user_id):
                        results['successes'] += 1
                    else:
                        results['failures'] += 1
                        results['errors'].append(
                            f"Failed to import event {event_uuid}")

                except Exception as e:
                    logger.error(
                        f"Failed to process event {event_uuid}: {str(e)}")
                    results['failures'] += 1
                    results['errors'].append(f"Event {event_uuid}: {str(e)}")

        except Exception as e:
            logger.error(f"Pull operation failed: {str(e)}")
            results['errors'].append(f"Pull operation error: {str(e)}")

        return results

    # Webhook Notification Methods

    async def send_webhook_notification(
        self,
        webhook_id: int,
        event_data: Dict[str, Any],
        event_type: str = 'event_published'
    ) -> Dict[str, Any]:
        """
        Send webhook notification with error handling and retry logic.

        Preserves original MISP webhook functionality from Workflow.php
        """
        try:
            webhook = await self._get_webhook_config(webhook_id)
            if not webhook or not webhook.enabled:
                raise WebhookError(
                    f"Webhook {webhook_id} not found or disabled")

            logger.info(
                f"Sending webhook notification {webhook_id} for {event_type}")

            # Build webhook payload
            payload = await self._build_webhook_payload(
                webhook, event_data, event_type
            )

            # Send with retry logic
            success = await self._send_webhook_with_retry(webhook, payload)

            if success:
                await self._log_webhook_delivery(
                    webhook_id, event_type, 'success',
                    f"Webhook delivered successfully"
                )
                return {
                    'status': 'success',
                    'webhook_id': webhook_id,
                    'event_type': event_type,
                    'delivered_at': datetime.utcnow().isoformat()
                }
            else:
                return await self._handle_webhook_failure(
                    webhook_id, event_type, "Failed to deliver webhook"
                )

        except Exception as e:
            logger.error(
                f"Webhook notification failed for {webhook_id}: {str(e)}")
            await self._handle_webhook_failure(webhook_id, event_type, str(e))
            raise WebhookError(f"Webhook notification failed: {str(e)}")

    async def _send_webhook_with_retry(
        self,
        webhook: WebhookConfig,
        payload: Dict[str, Any]
    ) -> bool:
        """
        Send webhook with retry logic and error handling.

        Implements exponential backoff for failed deliveries.
        """
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'MISP-Jane-Orchestrator/1.0'
        }

        # Add custom headers if configured
        if webhook.headers:
            headers.update(webhook.headers)

        # Add signature if secret configured
        if webhook.secret:
            signature = self._generate_webhook_signature(
                payload, webhook.secret)
            headers['X-MISP-Signature'] = signature

        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as session:
                    async with session.post(
                        webhook.url,
                        json=payload,
                        headers=headers
                    ) as response:
                        if 200 <= response.status < 300:
                            return True
                        else:
                            logger.warning(
                                f"Webhook {webhook.id} returned status {response.status}, "
                                f"attempt {attempt + 1}/{self.max_retries}"
                            )

            except Exception as e:
                logger.warning(
                    f"Webhook attempt {attempt + 1} failed for {webhook.id}: {str(e)}"
                )

                if attempt < self.max_retries - 1:
                    # Exponential backoff
                    delay = self.retry_delay * (2 ** attempt)
                    await asyncio.sleep(delay)

        return False

    # Helper Methods

    async def _get_feed_config(self, feed_id: int) -> Optional[FeedConfig]:
        """Get feed configuration from database."""
        result = await self.session.execute(
            select(FeedConfig).where(FeedConfig.id == feed_id)
        )
        return result.scalar_one_or_none()

    async def _get_server_config(self, server_id: int) -> Optional[ServerConfig]:
        """Get server configuration from database."""
        result = await self.session.execute(
            select(ServerConfig).where(ServerConfig.id == server_id)
        )
        return result.scalar_one_or_none()

    async def _get_webhook_config(self, webhook_id: int) -> Optional[WebhookConfig]:
        """Get webhook configuration from database."""
        result = await self.session.execute(
            select(WebhookConfig).where(WebhookConfig.id == webhook_id)
        )
        return result.scalar_one_or_none()

    def _build_feed_headers(self, feed: FeedConfig) -> Dict[str, str]:
        """Build HTTP headers for feed requests."""
        headers = {
            'User-Agent': 'MISP-Jane-Orchestrator/1.0',
            'Accept': 'application/json, text/plain, */*'
        }

        if feed.headers:
            headers.update(feed.headers)

        return headers

    def _generate_webhook_signature(
        self,
        payload: Dict[str, Any],
        secret: str
    ) -> str:
        """Generate webhook signature for authentication."""
        payload_str = json.dumps(
            payload, sort_keys=True, separators=(',', ':'))
        signature = hashlib.sha256(
            (secret + payload_str).encode('utf-8')
        ).hexdigest()
        return f"sha256={signature}"

    async def _log_feed_import(
        self,
        feed_id: int,
        user_id: int,
        status: str,
        message: str
    ):
        """Log feed import operation."""
        log_entry = FeedImportLog(
            feed_id=feed_id,
            user_id=user_id,
            status=status,
            message=message,
            created_at=datetime.utcnow()
        )
        self.session.add(log_entry)
        await self.session.commit()

    async def _log_sync_operation(
        self,
        server_id: int,
        user_id: int,
        sync_type: str,
        status: str,
        message: str
    ):
        """Log server synchronization operation."""
        log_entry = SyncLog(
            server_id=server_id,
            user_id=user_id,
            sync_type=sync_type,
            status=status,
            message=message,
            created_at=datetime.utcnow()
        )
        self.session.add(log_entry)
        await self.session.commit()

    async def _log_webhook_delivery(
        self,
        webhook_id: int,
        event_type: str,
        status: str,
        message: str
    ):
        """Log webhook delivery attempt."""
        log_entry = WebhookLog(
            webhook_id=webhook_id,
            event_type=event_type,
            status=status,
            message=message,
            created_at=datetime.utcnow()
        )
        self.session.add(log_entry)
        await self.session.commit()

    async def _handle_feed_import_failure(
        self,
        feed_id: int,
        user_id: int,
        error_message: str
    ) -> Dict[str, Any]:
        """Handle feed import failure with logging."""
        await self._log_feed_import(feed_id, user_id, 'failed', error_message)
        return {
            'status': 'failed',
            'feed_id': feed_id,
            'error': error_message,
            'failed_at': datetime.utcnow().isoformat()
        }

    async def _handle_sync_failure(
        self,
        server_id: int,
        user_id: int,
        error_message: str
    ) -> Dict[str, Any]:
        """Handle sync failure with logging."""
        await self._log_sync_operation(
            server_id, user_id, 'failed', 'failed', error_message
        )
        return {
            'status': 'failed',
            'server_id': server_id,
            'error': error_message,
            'failed_at': datetime.utcnow().isoformat()
        }

    async def _handle_webhook_failure(
        self,
        webhook_id: int,
        event_type: str,
        error_message: str
    ) -> Dict[str, Any]:
        """Handle webhook failure with logging."""
        await self._log_webhook_delivery(
            webhook_id, event_type, 'failed', error_message
        )
        return {
            'status': 'failed',
            'webhook_id': webhook_id,
            'event_type': event_type,
            'error': error_message,
            'failed_at': datetime.utcnow().isoformat()
        }

    # Additional helper methods would be implemented for:
    # - _get_cached_feed_data()
    # - _parse_misp_feed(), _parse_freetext_feed(), _parse_csv_feed()
    # - _import_feed_events()
    # - _get_remote_event_list()
    # - _fetch_remote_event()
    # - _import_remote_event()
    # - _event_exists_locally()
    # - _build_webhook_payload()
    # etc.
