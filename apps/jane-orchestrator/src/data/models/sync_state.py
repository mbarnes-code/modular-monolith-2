"""
Sync State model for cross-tool synchronization across all 37 integrated tools.

This module provides the data model for tracking synchronization state between
tools across 4 domains (Security, Productivity, MTG, Infrastructure).
"""

import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

from sqlalchemy import (JSON, Boolean, Column, DateTime, Index, Integer,
                        String, Text)
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base


class SyncStatus(str, Enum):
    """Synchronization status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CONFLICT = "conflict"
    CANCELLED = "cancelled"


class SyncDirection(str, Enum):
    """Synchronization direction enumeration."""

    BIDIRECTIONAL = "bidirectional"
    SOURCE_TO_TARGET = "source_to_target"
    TARGET_TO_SOURCE = "target_to_source"


class ConflictResolutionStrategy(str, Enum):
    """Conflict resolution strategy enumeration."""

    LAST_MODIFIED_WINS = "last_modified_wins"
    SOURCE_WINS = "source_wins"
    TARGET_WINS = "target_wins"
    MANUAL_RESOLUTION = "manual_resolution"
    MERGE_STRATEGY = "merge_strategy"


class SyncState(Base):
    """
    Model for tracking synchronization state between tools.

    Supports cross-domain data synchronization across all 37 integrated tools
    with conflict resolution and real-time monitoring capabilities.
    """

    __tablename__ = "sync_states"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sync_job_id = Column(String(255), nullable=False, index=True)

    # Source and target tool information
    source_tool_id = Column(String(100), nullable=False, index=True)
    source_domain = Column(String(50), nullable=False, index=True)
    source_entity_type = Column(String(100), nullable=False)
    source_entity_id = Column(String(255), nullable=False)

    target_tool_id = Column(String(100), nullable=False, index=True)
    target_domain = Column(String(50), nullable=False, index=True)
    target_entity_type = Column(String(100), nullable=False)
    target_entity_id = Column(String(255), nullable=True)

    # Synchronization metadata
    sync_direction = Column(
        String(50), nullable=False, default=SyncDirection.BIDIRECTIONAL
    )
    status = Column(
        String(50), nullable=False, default=SyncStatus.PENDING, index=True
    )
    priority = Column(Integer, nullable=False, default=5)

    # Data payload and mapping
    source_data = Column(JSON, nullable=True)
    target_data = Column(JSON, nullable=True)
    data_mapping_schema = Column(String(100), nullable=True)
    transformed_data = Column(JSON, nullable=True)

    # Conflict resolution
    conflict_resolution_strategy = Column(
        String(50),
        nullable=False,
        default=ConflictResolutionStrategy.LAST_MODIFIED_WINS,
    )
    has_conflicts = Column(Boolean, nullable=False, default=False)
    conflict_details = Column(JSON, nullable=True)    # Timing and performance
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    last_retry_at = Column(DateTime, nullable=True)
    retry_count = Column(Integer, nullable=False, default=0)
    max_retries = Column(Integer, nullable=False, default=3)

    # Error handling
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)

    # Monitoring and validation
    data_hash_source = Column(String(64), nullable=True)
    data_hash_target = Column(String(64), nullable=True)
    validation_status = Column(String(50), nullable=True)
    validation_errors = Column(JSON, nullable=True)

    # Performance metrics
    processing_duration_ms = Column(Integer, nullable=True)
    data_size_bytes = Column(Integer, nullable=True)

    # Dependencies and relationships
    parent_sync_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    dependency_sync_ids = Column(JSON, nullable=True)

    # User context
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    initiated_by = Column(String(100), nullable=False)

    # Metadata for cross-tool workflow context
    workflow_context = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)

    # Indexes for performance
    __table_args__ = (
        Index('idx_sync_tool_domain', 'source_tool_id', 'source_domain'),
        Index('idx_sync_status_priority', 'status', 'priority'),
        Index('idx_sync_created_status', 'created_at', 'status'),
        Index('idx_sync_job_status', 'sync_job_id', 'status'),
        Index('idx_sync_user_status', 'user_id', 'status'),
    )

    def __repr__(self) -> str:
        """String representation of sync state."""
        return (f"<SyncState(id={self.id}, job={self.sync_job_id}, "
                f"source={self.source_tool_id}, target={self.target_tool_id}, "
                f"status={self.status})>")

    @property
    def is_complete(self) -> bool:
        """Check if synchronization is complete."""
        return self.status in [SyncStatus.COMPLETED, SyncStatus.FAILED, SyncStatus.CANCELLED]

    @property
    def is_active(self) -> bool:
        """Check if synchronization is actively running."""
        return self.status == SyncStatus.IN_PROGRESS

    @property
    def needs_retry(self) -> bool:
        """Check if synchronization needs retry."""
        return (self.status == SyncStatus.FAILED and
                self.retry_count < self.max_retries)

    @property
    def processing_duration_seconds(self) -> Optional[float]:
        """Get processing duration in seconds."""
        if self.processing_duration_ms is not None:
            return self.processing_duration_ms / 1000.0
        return None

    def can_retry(self) -> bool:
        """Check if sync can be retried."""
        return (self.status == SyncStatus.FAILED and
                self.retry_count < self.max_retries)

    def get_cross_domain_context(self) -> Dict[str, Any]:
        """Get cross-domain synchronization context."""
        return {
            'source_domain': self.source_domain,
            'target_domain': self.target_domain,
            'is_cross_domain': self.source_domain != self.target_domain,
            'workflow_context': self.workflow_context or {},
            'data_mapping_schema': self.data_mapping_schema
        }

    def update_status(
        self,
        new_status: SyncStatus,
        error_message: Optional[str] = None,
        error_details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update sync status with timing and error information."""
        self.status = new_status

        if new_status == SyncStatus.IN_PROGRESS and not self.started_at:
            self.started_at = datetime.utcnow()
        elif new_status in [SyncStatus.COMPLETED, SyncStatus.FAILED, SyncStatus.CANCELLED]:
            if not self.completed_at:
                self.completed_at = datetime.utcnow()

            # Calculate processing duration
            if self.started_at and self.completed_at:
                duration = self.completed_at - self.started_at
                self.processing_duration_ms = int(
                    duration.total_seconds() * 1000)

        if error_message:
            self.error_message = error_message
            self.error_details = error_details or {}

        if new_status == SyncStatus.FAILED:
            self.retry_count += 1
            self.last_retry_at = datetime.utcnow()


class SyncBatch(Base):
    """
    Model for batch synchronization operations across multiple tools.

    Supports coordinated synchronization of related data across domains
    with rollback capabilities and progress tracking.
    """
    __tablename__ = "sync_batches"

    # Primary identification
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_name = Column(String(255), nullable=False)
    # workflow, domain_migration, user_action
    batch_type = Column(String(100), nullable=False)

    # Batch metadata
    description = Column(Text, nullable=True)
    total_syncs = Column(Integer, nullable=False, default=0)
    completed_syncs = Column(Integer, nullable=False, default=0)
    failed_syncs = Column(Integer, nullable=False, default=0)

    # Status and timing
    status = Column(String(50), nullable=False, default=SyncStatus.PENDING)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # User and context
    user_id = Column(UUID(as_uuid=True), nullable=True, index=True)
    initiated_by = Column(String(100), nullable=False)
    workflow_context = Column(JSON, nullable=True)

    # Configuration
    parallel_execution = Column(Boolean, nullable=False, default=True)
    max_parallel_syncs = Column(Integer, nullable=False, default=5)
    rollback_on_failure = Column(Boolean, nullable=False, default=False)

    # Progress tracking
    progress_percentage = Column(Integer, nullable=False, default=0)
    estimated_completion_at = Column(DateTime, nullable=True)

    def __repr__(self) -> str:
        """String representation of sync batch."""
        return (f"<SyncBatch(id={self.id}, name={self.batch_name}, "
                f"status={self.status}, progress={self.progress_percentage}%)>")

    @property
    def is_complete(self) -> bool:
        """Check if batch is complete."""
        return self.status in [SyncStatus.COMPLETED, SyncStatus.FAILED, SyncStatus.CANCELLED]

    def update_progress(self) -> None:
        """Update batch progress based on sync states."""
        if self.total_syncs > 0:
            self.progress_percentage = int(
                (self.completed_syncs / self.total_syncs) * 100)

        # Update status based on progress
        if self.completed_syncs + self.failed_syncs == self.total_syncs:
            if self.failed_syncs == 0:
                self.status = SyncStatus.COMPLETED
                self.completed_at = datetime.utcnow()
            else:
                self.status = SyncStatus.FAILED
                self.completed_at = datetime.utcnow()
