"""
MISP External API Integration Models

Data models for external API integrations preserving original MISP functionality:
- Feed configurations and import logs
- Server configurations and sync logs
- Webhook configurations and delivery logs
"""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Index,
                        Integer, String, Text, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class FeedConfig(Base):
    """
    Feed configuration model preserving MISP Feed.php functionality.

    Stores external threat intelligence feed configurations with
    error handling and fallback behavior settings.
    """
    __tablename__ = 'misp_feed_configs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    # Feed configuration
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    source_format: Mapped[str] = mapped_column(
        String(50), default='misp')  # misp, freetext, csv
    caching_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    # Import settings
    publish: Mapped[bool] = mapped_column(Boolean, default=False)
    override_ids: Mapped[bool] = mapped_column(Boolean, default=False)
    delta_merge: Mapped[bool] = mapped_column(Boolean, default=False)
    lookup_visible: Mapped[bool] = mapped_column(Boolean, default=True)

    # Filtering and rules
    rules: Mapped[Optional[Dict[str, Any]]
                  ] = mapped_column(JSON, nullable=True)
    headers: Mapped[Optional[Dict[str, str]]
                    ] = mapped_column(JSON, nullable=True)

    # Tagging
    tag_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Sharing group
    sharing_group_id: Mapped[Optional[int]
                             ] = mapped_column(Integer, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_import_at: Mapped[Optional[datetime]
                           ] = mapped_column(DateTime, nullable=True)

    # Relationships
    import_logs: Mapped[list["FeedImportLog"]] = relationship(
        "FeedImportLog", back_populates="feed", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_feed_enabled', 'enabled'),
        Index('idx_feed_source_format', 'source_format'),
        Index('idx_feed_last_import', 'last_import_at'),
    )


class ServerConfig(Base):
    """
    Server configuration model preserving MISP Server.php functionality.

    Stores MISP server configurations for threat intelligence sharing
    with sync settings and error handling.
    """
    __tablename__ = 'misp_server_configs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    authkey: Mapped[str] = mapped_column(String(255), nullable=False)

    # Server configuration
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    push: Mapped[bool] = mapped_column(Boolean, default=False)
    pull: Mapped[bool] = mapped_column(Boolean, default=False)
    caching_enabled: Mapped[bool] = mapped_column(Boolean, default=False)

    # Organization association
    org_id: Mapped[int] = mapped_column(Integer, nullable=False)
    remote_org_id: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True)

    # Sync settings
    pull_rules: Mapped[Optional[Dict[str, Any]]
                       ] = mapped_column(JSON, nullable=True)
    push_rules: Mapped[Optional[Dict[str, Any]]
                       ] = mapped_column(JSON, nullable=True)
    unpublish_event: Mapped[bool] = mapped_column(Boolean, default=False)
    publish_without_email: Mapped[bool] = mapped_column(Boolean, default=False)

    # Connection settings
    self_signed: Mapped[bool] = mapped_column(Boolean, default=False)
    skip_proxy: Mapped[bool] = mapped_column(Boolean, default=False)

    # Priority and internal flags
    priority: Mapped[int] = mapped_column(Integer, default=0)
    internal: Mapped[bool] = mapped_column(Boolean, default=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_sync_at: Mapped[Optional[datetime]
                         ] = mapped_column(DateTime, nullable=True)

    # Relationships
    sync_logs: Mapped[list["SyncLog"]] = relationship(
        "SyncLog", back_populates="server", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_server_enabled', 'enabled'),
        Index('idx_server_push', 'push'),
        Index('idx_server_pull', 'pull'),
        Index('idx_server_org', 'org_id'),
        Index('idx_server_last_sync', 'last_sync_at'),
        UniqueConstraint('url', name='uq_server_url'),
    )


class WebhookConfig(Base):
    """
    Webhook configuration model preserving MISP Workflow.php webhook functionality.

    Stores webhook configurations for external notifications with
    retry logic and error handling settings.
    """
    __tablename__ = 'misp_webhook_configs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)

    # Webhook configuration
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    secret: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    headers: Mapped[Optional[Dict[str, str]]
                    ] = mapped_column(JSON, nullable=True)

    # Event filters
    # event_published, attribute_added, etc.
    event_types: Mapped[Optional[list[str]]
                        ] = mapped_column(JSON, nullable=True)
    filters: Mapped[Optional[Dict[str, Any]]
                    ] = mapped_column(JSON, nullable=True)

    # Retry settings
    max_retries: Mapped[int] = mapped_column(Integer, default=3)
    retry_delay: Mapped[int] = mapped_column(Integer, default=5)  # seconds

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_triggered_at: Mapped[Optional[datetime]
                              ] = mapped_column(DateTime, nullable=True)

    # Relationships
    delivery_logs: Mapped[list["WebhookLog"]] = relationship(
        "WebhookLog", back_populates="webhook", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index('idx_webhook_enabled', 'enabled'),
        Index('idx_webhook_event_types', 'event_types'),
        Index('idx_webhook_last_triggered', 'last_triggered_at'),
    )


class FeedImportLog(Base):
    """
    Feed import operation log preserving MISP feed import tracking.

    Tracks feed import operations with status and error details
    for monitoring and debugging.
    """
    __tablename__ = 'misp_feed_import_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feed_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('misp_feed_configs.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Import details
    status: Mapped[str] = mapped_column(
        String(50), nullable=False)  # success, failed, partial
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Statistics
    events_processed: Mapped[Optional[int]
                             ] = mapped_column(Integer, nullable=True)
    events_imported: Mapped[Optional[int]
                            ] = mapped_column(Integer, nullable=True)
    events_failed: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True)

    # Execution details
    execution_time: Mapped[Optional[float]] = mapped_column(
        Integer, nullable=True)  # seconds
    memory_usage: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True)  # bytes

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]
                         ] = mapped_column(DateTime, nullable=True)

    # Relationships
    feed: Mapped["FeedConfig"] = relationship(
        "FeedConfig", back_populates="import_logs")

    __table_args__ = (
        Index('idx_feed_import_feed_id', 'feed_id'),
        Index('idx_feed_import_status', 'status'),
        Index('idx_feed_import_created', 'created_at'),
        Index('idx_feed_import_user', 'user_id'),
    )


class SyncLog(Base):
    """
    Server synchronization operation log preserving MISP sync tracking.

    Tracks server sync operations with detailed status and error information
    for monitoring distributed MISP deployments.
    """
    __tablename__ = 'misp_sync_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    server_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('misp_server_configs.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Sync details
    sync_type: Mapped[str] = mapped_column(
        String(50), nullable=False)  # pull, push, full
    status: Mapped[str] = mapped_column(
        String(50), nullable=False)  # success, failed, partial
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Statistics
    events_processed: Mapped[Optional[int]
                             ] = mapped_column(Integer, nullable=True)
    events_synced: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True)
    events_failed: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True)

    # Execution details
    execution_time: Mapped[Optional[float]] = mapped_column(
        Integer, nullable=True)  # seconds

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]
                         ] = mapped_column(DateTime, nullable=True)

    # Relationships
    server: Mapped["ServerConfig"] = relationship(
        "ServerConfig", back_populates="sync_logs")

    __table_args__ = (
        Index('idx_sync_log_server_id', 'server_id'),
        Index('idx_sync_log_sync_type', 'sync_type'),
        Index('idx_sync_log_status', 'status'),
        Index('idx_sync_log_created', 'created_at'),
        Index('idx_sync_log_user', 'user_id'),
    )


class WebhookLog(Base):
    """
    Webhook delivery log preserving MISP webhook notification tracking.

    Tracks webhook delivery attempts with retry information and
    response details for debugging notification issues.
    """
    __tablename__ = 'misp_webhook_logs'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    webhook_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('misp_webhook_configs.id'), nullable=False)

    # Delivery details
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50), nullable=False)  # success, failed, retry
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # HTTP details
    http_status: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    response_time: Mapped[Optional[float]] = mapped_column(
        Integer, nullable=True)  # milliseconds

    # Retry tracking
    attempt_number: Mapped[int] = mapped_column(Integer, default=1)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)
    next_retry_at: Mapped[Optional[datetime]
                          ] = mapped_column(DateTime, nullable=True)

    # Payload information
    payload_size: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True)  # bytes
    payload_hash: Mapped[Optional[str]] = mapped_column(
        String(64), nullable=True)  # SHA256

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    delivered_at: Mapped[Optional[datetime]
                         ] = mapped_column(DateTime, nullable=True)

    # Relationships
    webhook: Mapped["WebhookConfig"] = relationship(
        "WebhookConfig", back_populates="delivery_logs")

    __table_args__ = (
        Index('idx_webhook_log_webhook_id', 'webhook_id'),
        Index('idx_webhook_log_event_type', 'event_type'),
        Index('idx_webhook_log_status', 'status'),
        Index('idx_webhook_log_created', 'created_at'),
        Index('idx_webhook_log_next_retry', 'next_retry_at'),
    )


# Additional indexes for performance optimization
Index('idx_feed_config_provider', FeedConfig.provider)
Index('idx_server_config_priority', ServerConfig.priority)
Index('idx_webhook_config_name', WebhookConfig.name)
