"""
Conflict Resolution Service for concurrent data modifications.

This service handles conflicts that arise when multiple tools or users
modify the same data simultaneously across the 37 integrated tools.
"""

import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from ..data.models.sync_state import \
    ConflictResolutionStrategy as SyncConflictStrategy
from ..data.models.sync_state import SyncState

logger = logging.getLogger(__name__)


class ConflictType(str, Enum):
    """Types of conflicts that can occur during synchronization."""

    DATA_MODIFIED = "data_modified"  # Both source and target modified
    DATA_DELETED = "data_deleted"  # One deleted, other modified
    SCHEMA_MISMATCH = "schema_mismatch"  # Incompatible data structures
    VALIDATION_FAILURE = "validation_failure"  # Data fails validation
    CONCURRENT_UPDATE = "concurrent_update"  # Multiple simultaneous updates
    DEPENDENCY_CONFLICT = "dependency_conflict"  # Dependent data conflicts


class ConflictSeverity(str, Enum):
    """Severity levels for conflicts."""

    LOW = "low"  # Can auto-resolve
    MEDIUM = "medium"  # Requires user notification
    HIGH = "high"  # Requires immediate user intervention
    CRITICAL = "critical"  # Blocks all related operations


class ConflictResolutionStrategy(str, Enum):
    """Strategies for resolving conflicts."""

    LAST_MODIFIED_WINS = "last_modified_wins"
    SOURCE_WINS = "source_wins"
    TARGET_WINS = "target_wins"
    MANUAL_RESOLUTION = "manual_resolution"
    MERGE_STRATEGY = "merge_strategy"
    IGNORE_CONFLICT = "ignore_conflict"
    RETRY_LATER = "retry_later"


class ConflictResolutionAction(str, Enum):
    """Actions taken to resolve conflicts."""

    AUTO_RESOLVED = "auto_resolved"
    USER_RESOLVED = "user_resolved"
    DEFERRED = "deferred"
    ESCALATED = "escalated"
    IGNORED = "ignored"


class DataConflict(BaseModel):
    """Model representing a data conflict."""

    conflict_id: str = Field(default_factory=lambda: str(uuid4()))
    conflict_type: ConflictType = Field(..., description="Type of conflict")
    severity: ConflictSeverity = Field(..., description="Conflict severity")

    # Entity information
    source_tool: str = Field(..., description="Source tool identifier")
    target_tool: str = Field(..., description="Target tool identifier")
    entity_type: str = Field(..., description="Entity type")
    entity_id: str = Field(..., description="Entity identifier")

    # Conflict data
    source_data: Dict[str, Any] = Field(..., description="Source data version")
    target_data: Dict[str, Any] = Field(..., description="Target data version")
    conflicting_fields: List[str] = Field(
        default_factory=list, description="Fields in conflict"
    )

    # Metadata
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    source_modified_at: Optional[datetime] = Field(None)
    target_modified_at: Optional[datetime] = Field(None)

    # Resolution information
    resolution_strategy: Optional[ConflictResolutionStrategy] = Field(None)
    resolution_action: Optional[ConflictResolutionAction] = Field(None)
    resolved_at: Optional[datetime] = Field(None)
    resolved_by: Optional[str] = Field(None, description="User who resolved")
    resolved_data: Optional[Dict[str, Any]] = Field(None)

    # Context
    sync_job_id: Optional[str] = Field(None, description="Associated sync job")
    user_id: Optional[str] = Field(None, description="User context")
    workflow_context: Optional[Dict[str, Any]] = Field(None)


class ConflictResolutionResult(BaseModel):
    """Result of conflict resolution operation."""

    conflict_id: str = Field(..., description="Conflict identifier")
    resolved: bool = Field(..., description="Whether conflict was resolved")
    resolution_action: ConflictResolutionAction = Field(
        ..., description="Action taken"
    )
    resolved_data: Optional[Dict[str, Any]] = Field(None)
    error_message: Optional[str] = Field(None)
    requires_user_action: bool = Field(
        default=False, description="Requires manual intervention"
    )


class ConflictResolutionService:
    """
    Service for detecting and resolving data conflicts.

    Handles conflicts across all 37 integrated tools with domain-specific
    resolution strategies and user intervention capabilities.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the conflict resolution service.

        Args:
            db_session: Async database session
        """
        self.db = db_session
        self.active_conflicts: Dict[str, DataConflict] = {}
        self.resolution_handlers: Dict[ConflictType, callable] = {}
        self._register_resolution_handlers()

    def _register_resolution_handlers(self) -> None:
        """Register conflict resolution handlers."""
        self.resolution_handlers = {
            ConflictType.DATA_MODIFIED: self._resolve_data_modified,
            ConflictType.DATA_DELETED: self._resolve_data_deleted,
            ConflictType.SCHEMA_MISMATCH: self._resolve_schema_mismatch,
            ConflictType.VALIDATION_FAILURE: self._resolve_validation_failure,
            ConflictType.CONCURRENT_UPDATE: self._resolve_concurrent_update,
            ConflictType.DEPENDENCY_CONFLICT: self._resolve_dependency_conflict,
        }

    async def detect_conflicts(
        self,
        source_tool: str,
        target_tool: str,
        entity_type: str,
        entity_id: str,
        source_data: Dict[str, Any],
        target_data: Dict[str, Any],
        sync_job_id: Optional[str] = None,
    ) -> Optional[DataConflict]:
        """
        Detect conflicts between source and target data.

        Args:
            source_tool: Source tool identifier
            target_tool: Target tool identifier
            entity_type: Entity type
            entity_id: Entity identifier
            source_data: Source data
            target_data: Target data
            sync_job_id: Optional sync job ID

        Returns:
            DataConflict if conflict detected, None otherwise
        """
        conflicts = []

        # Check for data modification conflicts
        modification_conflict = self._check_data_modification_conflict(
            source_data, target_data
        )
        if modification_conflict:
            conflicts.append(modification_conflict)

        # Check for schema mismatches
        schema_conflict = self._check_schema_mismatch(source_data, target_data)
        if schema_conflict:
            conflicts.append(schema_conflict)

        # Check for validation failures
        validation_conflict = await self._check_validation_conflicts(
            source_data, target_data, entity_type
        )
        if validation_conflict:
            conflicts.append(validation_conflict)

        # Return the most severe conflict
        if conflicts:
            most_severe = max(
                conflicts, key=lambda c: self._get_severity_priority(c))

            conflict = DataConflict(
                conflict_type=most_severe,
                severity=self._determine_severity(
                    most_severe, source_data, target_data),
                source_tool=source_tool,
                target_tool=target_tool,
                entity_type=entity_type,
                entity_id=entity_id,
                source_data=source_data,
                target_data=target_data,
                conflicting_fields=self._identify_conflicting_fields(
                    source_data, target_data
                ),
                sync_job_id=sync_job_id,
            )

            self.active_conflicts[conflict.conflict_id] = conflict
            logger.warning(
                f"Detected {most_severe} conflict for {entity_type} {entity_id} "
                f"between {source_tool} and {target_tool}"
            )
            return conflict

        return None

    def _check_data_modification_conflict(
        self, source_data: Dict[str, Any], target_data: Dict[str, Any]
    ) -> Optional[ConflictType]:
        """Check for data modification conflicts."""
        # Compare data hashes or modification timestamps
        source_modified = source_data.get("last_modified")
        target_modified = target_data.get("last_modified")

        if source_modified and target_modified:
            # Both have modification timestamps
            try:
                source_dt = datetime.fromisoformat(
                    source_modified.replace("Z", "+00:00"))
                target_dt = datetime.fromisoformat(
                    target_modified.replace("Z", "+00:00"))

                # If both modified within last hour, potential conflict
                time_diff = abs((source_dt - target_dt).total_seconds())
                if time_diff < 3600:  # 1 hour threshold
                    return ConflictType.DATA_MODIFIED
            except (ValueError, AttributeError):
                pass

        # Check for significant data differences
        if self._calculate_data_similarity(source_data, target_data) < 0.8:
            return ConflictType.DATA_MODIFIED

        return None

    def _check_schema_mismatch(
        self, source_data: Dict[str, Any], target_data: Dict[str, Any]
    ) -> Optional[ConflictType]:
        """Check for schema mismatches."""
        source_keys = set(self._get_all_keys(source_data))
        target_keys = set(self._get_all_keys(target_data))

        # Check for significant key differences
        intersection = source_keys.intersection(target_keys)
        union = source_keys.union(target_keys)

        if len(intersection) / len(union) < 0.6:  # Less than 60% overlap
            return ConflictType.SCHEMA_MISMATCH

        return None

    async def _check_validation_conflicts(
        self,
        source_data: Dict[str, Any],
        target_data: Dict[str, Any],
        entity_type: str,
    ) -> Optional[ConflictType]:
        """Check for validation conflicts."""
        # This would implement domain-specific validation
        # For now, basic validation checks

        # Check for required fields
        required_fields = self._get_required_fields_for_entity(entity_type)

        for field in required_fields:
            source_value = self._get_nested_value(source_data, field)
            target_value = self._get_nested_value(target_data, field)

            if source_value is None or target_value is None:
                return ConflictType.VALIDATION_FAILURE

        return None

    def _get_required_fields_for_entity(self, entity_type: str) -> List[str]:
        """Get required fields for entity type."""
        # Domain-specific required fields
        field_mapping = {
            "threat_intelligence": ["id", "timestamp", "info"],
            "security_event": ["@timestamp", "event.action"],
            "task": ["title", "created_at"],
            "recipe": ["name", "instructions"],
            "budget_entry": ["amount", "date"],
            "card": ["name", "mana_cost"],
            "deck": ["name", "commander_id"],
        }
        return field_mapping.get(entity_type, ["id"])

    async def resolve_conflict(
        self,
        conflict_id: str,
        strategy: ConflictResolutionStrategy,
        user_id: Optional[str] = None,
        manual_resolution_data: Optional[Dict[str, Any]] = None,
    ) -> ConflictResolutionResult:
        """
        Resolve a detected conflict.

        Args:
            conflict_id: Conflict identifier
            strategy: Resolution strategy to use
            user_id: Optional user performing resolution
            manual_resolution_data: Data for manual resolution

        Returns:
            ConflictResolutionResult
        """
        if conflict_id not in self.active_conflicts:
            return ConflictResolutionResult(
                conflict_id=conflict_id,
                resolved=False,
                resolution_action=ConflictResolutionAction.IGNORED,
                error_message="Conflict not found",
            )

        conflict = self.active_conflicts[conflict_id]

        try:
            # Get resolution handler
            handler = self.resolution_handlers.get(conflict.conflict_type)
            if not handler:
                return ConflictResolutionResult(
                    conflict_id=conflict_id,
                    resolved=False,
                    resolution_action=ConflictResolutionAction.ESCALATED,
                    error_message=f"No handler for conflict type {conflict.conflict_type}",
                    requires_user_action=True,
                )

            # Execute resolution
            resolved_data = await handler(conflict, strategy, manual_resolution_data)

            # Update conflict
            conflict.resolution_strategy = strategy
            conflict.resolution_action = (
                ConflictResolutionAction.USER_RESOLVED
                if user_id
                else ConflictResolutionAction.AUTO_RESOLVED
            )
            conflict.resolved_at = datetime.utcnow()
            conflict.resolved_by = user_id
            conflict.resolved_data = resolved_data

            # Remove from active conflicts
            del self.active_conflicts[conflict_id]

            logger.info(f"Resolved conflict {conflict_id} using {strategy}")

            return ConflictResolutionResult(
                conflict_id=conflict_id,
                resolved=True,
                resolution_action=conflict.resolution_action,
                resolved_data=resolved_data,
            )

        except Exception as e:
            logger.error(f"Failed to resolve conflict {conflict_id}: {e}")
            return ConflictResolutionResult(
                conflict_id=conflict_id,
                resolved=False,
                resolution_action=ConflictResolutionAction.ESCALATED,
                error_message=str(e),
                requires_user_action=True,
            )

    async def _resolve_data_modified(
        self,
        conflict: DataConflict,
        strategy: ConflictResolutionStrategy,
        manual_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve data modification conflicts."""
        if strategy == ConflictResolutionStrategy.SOURCE_WINS:
            return conflict.source_data
        elif strategy == ConflictResolutionStrategy.TARGET_WINS:
            return conflict.target_data
        elif strategy == ConflictResolutionStrategy.LAST_MODIFIED_WINS:
            return self._resolve_by_timestamp(conflict)
        elif strategy == ConflictResolutionStrategy.MERGE_STRATEGY:
            return self._merge_data(conflict.source_data, conflict.target_data)
        elif strategy == ConflictResolutionStrategy.MANUAL_RESOLUTION:
            if manual_data:
                return manual_data
            else:
                raise ValueError("Manual resolution requires resolution data")
        else:
            raise ValueError(
                f"Unsupported strategy for data modification: {strategy}")

    async def _resolve_data_deleted(
        self,
        conflict: DataConflict,
        strategy: ConflictResolutionStrategy,
        manual_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve data deletion conflicts."""
        # For deletion conflicts, typically preserve the existing data
        if strategy == ConflictResolutionStrategy.SOURCE_WINS:
            return conflict.source_data
        elif strategy == ConflictResolutionStrategy.TARGET_WINS:
            return conflict.target_data
        else:
            # Default to preserving data over deletion
            return conflict.target_data if conflict.target_data else conflict.source_data

    async def _resolve_schema_mismatch(
        self,
        conflict: DataConflict,
        strategy: ConflictResolutionStrategy,
        manual_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve schema mismatch conflicts."""
        if strategy == ConflictResolutionStrategy.MERGE_STRATEGY:
            # Merge compatible fields
            merged = {}
            merged.update(conflict.target_data)

            # Add non-conflicting fields from source
            for key, value in conflict.source_data.items():
                if key not in merged or merged[key] is None:
                    merged[key] = value

            return merged
        elif strategy == ConflictResolutionStrategy.SOURCE_WINS:
            return conflict.source_data
        else:
            return conflict.target_data

    async def _resolve_validation_failure(
        self,
        conflict: DataConflict,
        strategy: ConflictResolutionStrategy,
        manual_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve validation failure conflicts."""
        if strategy == ConflictResolutionStrategy.MANUAL_RESOLUTION and manual_data:
            return manual_data
        else:
            # Try to fix common validation issues
            return self._fix_validation_issues(conflict.source_data, conflict.target_data)

    async def _resolve_concurrent_update(
        self,
        conflict: DataConflict,
        strategy: ConflictResolutionStrategy,
        manual_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve concurrent update conflicts."""
        # Similar to data modification, but with timestamp prioritization
        return await self._resolve_data_modified(conflict, strategy, manual_data)

    async def _resolve_dependency_conflict(
        self,
        conflict: DataConflict,
        strategy: ConflictResolutionStrategy,
        manual_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Resolve dependency conflicts."""
        # This requires checking dependent entities
        # For now, defer to manual resolution
        if manual_data:
            return manual_data
        else:
            raise ValueError("Dependency conflicts require manual resolution")

    def _resolve_by_timestamp(self, conflict: DataConflict) -> Dict[str, Any]:
        """Resolve conflict by choosing most recent modification."""
        source_ts = conflict.source_data.get("last_modified")
        target_ts = conflict.target_data.get("last_modified")

        if not source_ts and not target_ts:
            return conflict.source_data  # Default to source

        if not source_ts:
            return conflict.target_data
        if not target_ts:
            return conflict.source_data

        try:
            source_dt = datetime.fromisoformat(
                source_ts.replace("Z", "+00:00"))
            target_dt = datetime.fromisoformat(
                target_ts.replace("Z", "+00:00"))
            return conflict.source_data if source_dt > target_dt else conflict.target_data
        except (ValueError, AttributeError):
            return conflict.source_data

    def _merge_data(
        self, source_data: Dict[str, Any], target_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge source and target data intelligently."""
        merged = {}

        # Start with target data
        merged.update(target_data)

        # Merge source data, preserving newer values
        for key, source_value in source_data.items():
            if key not in merged:
                merged[key] = source_value
            elif merged[key] is None and source_value is not None:
                merged[key] = source_value
            elif isinstance(merged[key], dict) and isinstance(source_value, dict):
                merged[key] = self._merge_data(source_value, merged[key])
            elif isinstance(merged[key], list) and isinstance(source_value, list):
                # Merge lists, removing duplicates
                merged[key] = list(set(merged[key] + source_value))

        return merged

    def _fix_validation_issues(
        self, source_data: Dict[str, Any], target_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Fix common validation issues by combining valid data."""
        fixed = {}

        # Use target as base
        fixed.update(target_data)

        # Fill missing required fields from source
        for key, value in source_data.items():
            if key not in fixed or fixed[key] is None:
                if value is not None:
                    fixed[key] = value

        return fixed

    def _calculate_data_similarity(
        self, data1: Dict[str, Any], data2: Dict[str, Any]
    ) -> float:
        """Calculate similarity score between two data objects."""
        if not data1 or not data2:
            return 0.0

        keys1 = set(self._get_all_keys(data1))
        keys2 = set(self._get_all_keys(data2))

        if not keys1 and not keys2:
            return 1.0
        if not keys1 or not keys2:
            return 0.0

        intersection = keys1.intersection(keys2)
        union = keys1.union(keys2)

        return len(intersection) / len(union)

    def _get_all_keys(self, data: Dict[str, Any], prefix: str = "") -> List[str]:
        """Get all nested keys from a dictionary."""
        keys = []
        for key, value in data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            keys.append(full_key)

            if isinstance(value, dict):
                keys.extend(self._get_all_keys(value, full_key))

        return keys

    def _get_nested_value(self, data: Dict[str, Any], key_path: str) -> Any:
        """Get nested value using dot notation."""
        keys = key_path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None

        return current

    def _identify_conflicting_fields(
        self, source_data: Dict[str, Any], target_data: Dict[str, Any]
    ) -> List[str]:
        """Identify specific fields that are in conflict."""
        conflicts = []

        all_keys = set(self._get_all_keys(source_data)).union(
            set(self._get_all_keys(target_data))
        )

        for key in all_keys:
            source_value = self._get_nested_value(source_data, key)
            target_value = self._get_nested_value(target_data, key)

            if source_value != target_value:
                conflicts.append(key)

        return conflicts

    def _determine_severity(
        self,
        conflict_type: ConflictType,
        source_data: Dict[str, Any],
        target_data: Dict[str, Any],
    ) -> ConflictSeverity:
        """Determine conflict severity based on type and data."""
        severity_mapping = {
            ConflictType.DATA_MODIFIED: ConflictSeverity.MEDIUM,
            ConflictType.DATA_DELETED: ConflictSeverity.HIGH,
            ConflictType.SCHEMA_MISMATCH: ConflictSeverity.HIGH,
            ConflictType.VALIDATION_FAILURE: ConflictSeverity.MEDIUM,
            ConflictType.CONCURRENT_UPDATE: ConflictSeverity.LOW,
            ConflictType.DEPENDENCY_CONFLICT: ConflictSeverity.CRITICAL,
        }

        return severity_mapping.get(conflict_type, ConflictSeverity.MEDIUM)

    def _get_severity_priority(self, conflict_type: ConflictType) -> int:
        """Get numeric priority for conflict severity."""
        priority_mapping = {
            ConflictType.DEPENDENCY_CONFLICT: 4,
            ConflictType.DATA_DELETED: 3,
            ConflictType.SCHEMA_MISMATCH: 3,
            ConflictType.VALIDATION_FAILURE: 2,
            ConflictType.DATA_MODIFIED: 2,
            ConflictType.CONCURRENT_UPDATE: 1,
        }
        return priority_mapping.get(conflict_type, 1)

    async def get_active_conflicts(
        self, tool_filter: Optional[str] = None, entity_filter: Optional[str] = None
    ) -> List[DataConflict]:
        """
        Get list of active conflicts with optional filtering.

        Args:
            tool_filter: Filter by tool name
            entity_filter: Filter by entity type

        Returns:
            List of active conflicts
        """
        conflicts = list(self.active_conflicts.values())

        if tool_filter:
            conflicts = [
                c
                for c in conflicts
                if c.source_tool == tool_filter or c.target_tool == tool_filter
            ]

        if entity_filter:
            conflicts = [
                c for c in conflicts if c.entity_type == entity_filter]

        return conflicts

    async def escalate_conflict(
        self, conflict_id: str, escalation_reason: str, user_id: Optional[str] = None
    ) -> bool:
        """
        Escalate a conflict for manual resolution.

        Args:
            conflict_id: Conflict identifier
            escalation_reason: Reason for escalation
            user_id: Optional user ID

        Returns:
            True if escalated successfully
        """
        if conflict_id not in self.active_conflicts:
            return False

        conflict = self.active_conflicts[conflict_id]
        conflict.resolution_action = ConflictResolutionAction.ESCALATED
        conflict.severity = ConflictSeverity.HIGH

        logger.warning(
            f"Escalated conflict {conflict_id} for {conflict.entity_type} "
            f"{conflict.entity_id}: {escalation_reason}"
        )

        return True
