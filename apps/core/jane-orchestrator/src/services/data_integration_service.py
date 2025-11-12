"""
Data Integration Service for cross-domain workflows.

This service orchestrates data synchronization and transformation between
all 37 integrated tools across the 4 domains (Security, Productivity, MTG, Infrastructure).
"""

import asyncio
import hashlib
import json
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import uuid4

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..data.models.sync_state import (ConflictResolutionStrategy, SyncBatch,
                                      SyncDirection, SyncState, SyncStatus)
from ..data.schemas.base import (DataMappingSchema, DataType, DomainType,
                                 FieldMapping, MappingRuleType)
from ..data.schemas.productivity import PRODUCTIVITY_SCHEMAS
from ..data.schemas.security import SECURITY_SCHEMAS

logger = logging.getLogger(__name__)


class DataIntegrationError(Exception):
    """Base exception for data integration errors."""

    pass


class SchemaNotFoundError(DataIntegrationError):
    """Raised when a mapping schema is not found."""

    pass


class TransformationError(DataIntegrationError):
    """Raised when data transformation fails."""

    pass


class ConflictResolutionError(DataIntegrationError):
    """Raised when conflict resolution fails."""

    pass


class DataIntegrationService:
    """
    Service for managing cross-domain data integration and synchronization.

    Handles data transformation, conflict resolution, and synchronization
    across all 37 integrated tools with domain-specific performance requirements.
    """

    def __init__(self, db_session: AsyncSession):
        """
        Initialize the data integration service.

        Args:
            db_session: Async database session for data operations
        """
        self.db = db_session
        self.mapping_schemas: Dict[str, DataMappingSchema] = {}
        self.transformation_functions: Dict[str, callable] = {}
        self._load_schemas()
        self._register_transformation_functions()

    def _load_schemas(self) -> None:
        """Load all available mapping schemas."""
        # Load domain-specific schemas
        self.mapping_schemas.update(SECURITY_SCHEMAS)
        self.mapping_schemas.update(PRODUCTIVITY_SCHEMAS)

        logger.info(f"Loaded {len(self.mapping_schemas)} mapping schemas")

    def _register_transformation_functions(self) -> None:
        """Register transformation functions for data mapping."""
        self.transformation_functions.update(
            {
                "iso_to_datetime": self._iso_to_datetime,
                "iso_to_elasticsearch_timestamp": self._iso_to_elasticsearch_timestamp,
                "unix_to_elasticsearch_timestamp": self._unix_to_elasticsearch_timestamp,
                "date_to_datetime": self._date_to_datetime,
                "threat_level_to_severity": self._threat_level_to_severity,
                "recipe_to_task_title": self._recipe_to_task_title,
            }
        )

    # Transformation functions
    def _iso_to_datetime(self, value: str) -> datetime:
        """Convert ISO string to datetime object."""
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def _iso_to_elasticsearch_timestamp(self, value: str) -> str:
        """Convert ISO timestamp to Elasticsearch format."""
        dt = self._iso_to_datetime(value)
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _unix_to_elasticsearch_timestamp(self, value: Union[int, float]) -> str:
        """Convert Unix timestamp to Elasticsearch format."""
        dt = datetime.fromtimestamp(float(value))
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def _date_to_datetime(self, value: str) -> datetime:
        """Convert date string to datetime object."""
        return datetime.strptime(value, "%Y-%m-%d")

    def _threat_level_to_severity(self, value: int) -> str:
        """Convert MISP threat level to severity string."""
        mapping = {1: "high", 2: "medium", 3: "low", 4: "undefined"}
        return mapping.get(value, "undefined")

    def _recipe_to_task_title(self, value: str) -> str:
        """Convert recipe name to task title."""
        return f"Prepare: {value}"

    async def create_sync_job(
        self,
        source_tool: str,
        source_domain: DomainType,
        source_entity_type: str,
        source_entity_id: str,
        target_tool: str,
        target_domain: DomainType,
        target_entity_type: str,
        source_data: Dict[str, Any],
        mapping_schema_id: Optional[str] = None,
        sync_direction: SyncDirection = SyncDirection.SOURCE_TO_TARGET,
        conflict_strategy: ConflictResolutionStrategy = ConflictResolutionStrategy.LAST_MODIFIED_WINS,
        user_id: Optional[str] = None,
        workflow_context: Optional[Dict[str, Any]] = None,
    ) -> SyncState:
        """
        Create a new synchronization job.

        Args:
            source_tool: Source tool identifier
            source_domain: Source domain
            source_entity_type: Source entity type
            source_entity_id: Source entity ID
            target_tool: Target tool identifier
            target_domain: Target domain
            target_entity_type: Target entity type
            source_data: Source data to synchronize
            mapping_schema_id: Optional mapping schema ID
            sync_direction: Synchronization direction
            conflict_strategy: Conflict resolution strategy
            user_id: Optional user ID
            workflow_context: Optional workflow context

        Returns:
            Created sync state
        """
        # Generate sync job ID
        sync_job_id = f"{source_tool}_{target_tool}_{uuid4().hex[:8]}"

        # Find or infer mapping schema
        if not mapping_schema_id:
            mapping_schema_id = self._infer_mapping_schema(
                source_tool, source_domain, target_tool, target_domain
            )

        # Calculate data hash for change detection
        data_hash = self._calculate_data_hash(source_data)

        # Create sync state
        sync_state = SyncState(
            sync_job_id=sync_job_id,
            source_tool_id=source_tool,
            source_domain=source_domain.value,
            source_entity_type=source_entity_type,
            source_entity_id=source_entity_id,
            target_tool_id=target_tool,
            target_domain=target_domain.value,
            target_entity_type=target_entity_type,
            sync_direction=sync_direction.value,
            source_data=source_data,
            data_mapping_schema=mapping_schema_id,
            conflict_resolution_strategy=conflict_strategy.value,
            data_hash_source=data_hash,
            user_id=user_id,
            initiated_by="user" if user_id else "system",
            workflow_context=workflow_context,
        )

        self.db.add(sync_state)
        await self.db.commit()
        await self.db.refresh(sync_state)

        logger.info(
            f"Created sync job {sync_job_id} from {source_tool} to {target_tool}")
        return sync_state

    async def execute_sync(self, sync_id: str) -> SyncState:
        """
        Execute a synchronization job.

        Args:
            sync_id: Sync state ID

        Returns:
            Updated sync state
        """
        # Get sync state
        result = await self.db.execute(
            select(SyncState).where(SyncState.id == sync_id)
        )
        sync_state = result.scalar_one_or_none()

        if not sync_state:
            raise DataIntegrationError(f"Sync state {sync_id} not found")

        try:
            # Update status to in progress
            sync_state.update_status(SyncStatus.IN_PROGRESS)
            await self.db.commit()

            # Transform data
            transformed_data = await self._transform_data(
                sync_state.source_data,
                sync_state.data_mapping_schema,
                sync_state.source_tool_id,
                sync_state.target_tool_id,
            )

            # Apply data to target
            target_entity_id = await self._apply_data_to_target(
                sync_state.target_tool_id,
                sync_state.target_entity_type,
                transformed_data,
                sync_state.target_entity_id,
            )

            # Update sync state with results
            sync_state.target_data = transformed_data
            sync_state.target_entity_id = target_entity_id
            sync_state.data_hash_target = self._calculate_data_hash(
                transformed_data)
            sync_state.update_status(SyncStatus.COMPLETED)

            await self.db.commit()

            logger.info(
                f"Successfully completed sync job {sync_state.sync_job_id}")
            return sync_state

        except Exception as e:
            # Handle sync failure
            error_message = str(e)
            error_details = {"error_type": type(
                e).__name__, "traceback": str(e)}

            sync_state.update_status(
                SyncStatus.FAILED, error_message=error_message, error_details=error_details
            )
            await self.db.commit()

            logger.error(
                f"Sync job {sync_state.sync_job_id} failed: {error_message}"
            )
            raise DataIntegrationError(
                f"Sync execution failed: {error_message}")

    async def _transform_data(
        self,
        source_data: Dict[str, Any],
        mapping_schema_id: str,
        source_tool: str,
        target_tool: str,
    ) -> Dict[str, Any]:
        """
        Transform data using mapping schema.

        Args:
            source_data: Source data to transform
            mapping_schema_id: Mapping schema identifier
            source_tool: Source tool identifier
            target_tool: Target tool identifier

        Returns:
            Transformed data

        Raises:
            SchemaNotFoundError: If mapping schema is not found
            TransformationError: If transformation fails
        """
        if mapping_schema_id not in self.mapping_schemas:
            raise SchemaNotFoundError(
                f"Mapping schema {mapping_schema_id} not found")

        schema = self.mapping_schemas[mapping_schema_id]
        transformed_data = {}

        try:
            for field_mapping in schema.field_mappings:
                source_value = self._get_nested_value(
                    source_data, field_mapping.source_field
                )

                # Apply transformation if specified
                if (
                    field_mapping.mapping_type == MappingRuleType.TRANSFORM
                    and field_mapping.transform_function
                ):
                    if field_mapping.transform_function in self.transformation_functions:
                        transform_func = self.transformation_functions[
                            field_mapping.transform_function
                        ]
                        source_value = transform_func(source_value)
                    else:
                        logger.warning(
                            f"Transform function {field_mapping.transform_function} not found"
                        )

                # Apply default value if source is empty
                if source_value is None and field_mapping.default_value is not None:
                    source_value = field_mapping.default_value

                # Check required fields
                if field_mapping.required and source_value is None:
                    raise TransformationError(
                        f"Required field {field_mapping.source_field} is missing"
                    )

                # Set transformed value
                if source_value is not None:
                    self._set_nested_value(
                        transformed_data, field_mapping.target_field, source_value
                    )

            return transformed_data

        except Exception as e:
            raise TransformationError(f"Data transformation failed: {str(e)}")

    def _get_nested_value(self, data: Dict[str, Any], field_path: str) -> Any:
        """
        Get nested value from data using dot notation.

        Args:
            data: Source data dictionary
            field_path: Field path in dot notation

        Returns:
            Field value or None if not found
        """
        keys = field_path.split(".")
        current = data

        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None

        return current

    def _set_nested_value(
        self, data: Dict[str, Any], field_path: str, value: Any
    ) -> None:
        """
        Set nested value in data using dot notation.

        Args:
            data: Target data dictionary
            field_path: Field path in dot notation
            value: Value to set
        """
        keys = field_path.split(".")
        current = data

        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]

        current[keys[-1]] = value

    def _calculate_data_hash(self, data: Dict[str, Any]) -> str:
        """
        Calculate SHA-256 hash of data for change detection.

        Args:
            data: Data to hash

        Returns:
            SHA-256 hash string
        """
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.sha256(json_str.encode()).hexdigest()

    def _infer_mapping_schema(
        self,
        source_tool: str,
        source_domain: DomainType,
        target_tool: str,
        target_domain: DomainType,
    ) -> str:
        """
        Infer mapping schema based on tool and domain information.

        Args:
            source_tool: Source tool identifier
            source_domain: Source domain
            target_tool: Target tool identifier
            target_domain: Target domain

        Returns:
            Inferred mapping schema ID
        """
        # Try exact match first
        schema_id = f"{source_tool}_to_{target_tool}"
        if schema_id in self.mapping_schemas:
            return schema_id

        # Try domain-based matching
        for schema in self.mapping_schemas.values():
            if (
                schema.source_domain == source_domain
                and schema.target_domain == target_domain
                and (
                    schema.source_tool == source_tool
                    or schema.target_tool == target_tool
                )
            ):
                return schema.schema_id

        # Default to generic cross-domain mapping
        return f"{source_domain.value}_to_{target_domain.value}_generic"

    async def _apply_data_to_target(
        self,
        target_tool: str,
        target_entity_type: str,
        transformed_data: Dict[str, Any],
        existing_entity_id: Optional[str] = None,
    ) -> str:
        """
        Apply transformed data to target tool.

        Args:
            target_tool: Target tool identifier
            target_entity_type: Target entity type
            transformed_data: Transformed data to apply
            existing_entity_id: Existing entity ID for updates

        Returns:
            Target entity ID

        Note:
            This is a placeholder implementation. In a real system,
            this would integrate with the actual tool APIs.
        """
        # This would integrate with service adapters for each tool
        # For now, we'll simulate the operation
        if existing_entity_id:
            logger.info(
                f"Updating {target_entity_type} {existing_entity_id} in {target_tool}"
            )
            return existing_entity_id
        else:
            new_entity_id = str(uuid4())
            logger.info(
                f"Creating new {target_entity_type} {new_entity_id} in {target_tool}"
            )
            return new_entity_id

    async def get_sync_status(self, sync_id: str) -> Optional[SyncState]:
        """
        Get synchronization status.

        Args:
            sync_id: Sync state ID

        Returns:
            Sync state or None if not found
        """
        result = await self.db.execute(
            select(SyncState).where(SyncState.id == sync_id)
        )
        return result.scalar_one_or_none()

    async def list_active_syncs(
        self, tool_filter: Optional[str] = None, domain_filter: Optional[DomainType] = None
    ) -> List[SyncState]:
        """
        List active synchronization jobs.

        Args:
            tool_filter: Optional tool filter
            domain_filter: Optional domain filter

        Returns:
            List of active sync states
        """
        query = select(SyncState).where(
            SyncState.status.in_([SyncStatus.PENDING, SyncStatus.IN_PROGRESS])
        )

        if tool_filter:
            query = query.where(
                or_(
                    SyncState.source_tool_id == tool_filter,
                    SyncState.target_tool_id == tool_filter,
                )
            )

        if domain_filter:
            query = query.where(
                or_(
                    SyncState.source_domain == domain_filter.value,
                    SyncState.target_domain == domain_filter.value,
                )
            )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def cancel_sync(self, sync_id: str, reason: str = "") -> bool:
        """
        Cancel a synchronization job.

        Args:
            sync_id: Sync state ID
            reason: Cancellation reason

        Returns:
            True if cancelled successfully
        """
        result = await self.db.execute(
            select(SyncState).where(SyncState.id == sync_id)
        )
        sync_state = result.scalar_one_or_none()

        if not sync_state:
            return False

        if sync_state.is_complete:
            return False

        sync_state.update_status(
            SyncStatus.CANCELLED, error_message=f"Cancelled: {reason}"
        )
        await self.db.commit()

        logger.info(f"Cancelled sync job {sync_state.sync_job_id}: {reason}")
        return True

    async def create_batch_sync(
        self,
        batch_name: str,
        batch_type: str,
        sync_configs: List[Dict[str, Any]],
        user_id: Optional[str] = None,
        parallel_execution: bool = True,
        rollback_on_failure: bool = False,
    ) -> SyncBatch:
        """
        Create a batch synchronization operation.

        Args:
            batch_name: Batch name
            batch_type: Batch type
            sync_configs: List of sync configurations
            user_id: Optional user ID
            parallel_execution: Whether to execute syncs in parallel
            rollback_on_failure: Whether to rollback on failure

        Returns:
            Created sync batch
        """
        batch = SyncBatch(
            batch_name=batch_name,
            batch_type=batch_type,
            total_syncs=len(sync_configs),
            user_id=user_id,
            initiated_by="user" if user_id else "system",
            parallel_execution=parallel_execution,
            rollback_on_failure=rollback_on_failure,
        )

        self.db.add(batch)
        await self.db.commit()
        await self.db.refresh(batch)

        # Create individual sync jobs
        for config in sync_configs:
            await self.create_sync_job(**config)

        logger.info(
            f"Created batch sync {batch_name} with {len(sync_configs)} jobs")
        return batch
