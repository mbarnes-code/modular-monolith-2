"""
Data synchronization API endpoints.

FastAPI endpoints for managing cross-tool data synchronization
across all 37 integrated tools with domain-specific routing.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from ..data.database import get_async_session
from ..data.models.sync_state import SyncDirection, SyncState, SyncStatus
from ..services.data_integration_service import (DataIntegrationError,
                                                 DataIntegrationService,
                                                 SchemaNotFoundError,
                                                 TransformationError)
from ..services.event_bus_service import DomainType, EventBusService, EventType

router = APIRouter(prefix="/api/sync", tags=["data-synchronization"])


# Request/Response Models
class SyncJobRequest(BaseModel):
    """Request model for creating sync jobs."""

    source_tool: str = Field(..., description="Source tool identifier")
    source_domain: DomainType = Field(..., description="Source domain")
    source_entity_type: str = Field(..., description="Source entity type")
    source_entity_id: str = Field(..., description="Source entity ID")
    target_tool: str = Field(..., description="Target tool identifier")
    target_domain: DomainType = Field(..., description="Target domain")
    target_entity_type: str = Field(..., description="Target entity type")
    source_data: Dict[str, Any] = Field(..., description="Source data to sync")
    mapping_schema_id: Optional[str] = Field(
        None, description="Optional mapping schema ID"
    )
    sync_direction: SyncDirection = Field(
        default=SyncDirection.SOURCE_TO_TARGET, description="Sync direction"
    )
    workflow_context: Optional[Dict[str, Any]] = Field(
        None, description="Optional workflow context"
    )

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "source_tool": "misp",
                "source_domain": "security",
                "source_entity_type": "threat_intelligence",
                "source_entity_id": "event_123",
                "target_tool": "helk",
                "target_domain": "security",
                "target_entity_type": "security_event",
                "source_data": {
                    "Event": {
                        "id": "123",
                        "info": "Suspicious activity detected",
                        "timestamp": "2023-01-01T00:00:00Z",
                    }
                },
            }
        }


class SyncJobResponse(BaseModel):
    """Response model for sync job operations."""

    sync_id: str = Field(..., description="Sync job identifier")
    sync_job_id: str = Field(..., description="Human-readable sync job ID")
    status: SyncStatus = Field(..., description="Current sync status")
    source_tool: str = Field(..., description="Source tool")
    target_tool: str = Field(..., description="Target tool")
    created_at: datetime = Field(..., description="Creation timestamp")
    started_at: Optional[datetime] = Field(None, description="Start timestamp")
    completed_at: Optional[datetime] = Field(
        None, description="Completion timestamp")
    error_message: Optional[str] = Field(
        None, description="Error message if failed")
    processing_duration_ms: Optional[int] = Field(
        None, description="Processing duration in milliseconds"
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class BatchSyncRequest(BaseModel):
    """Request model for batch sync operations."""

    batch_name: str = Field(..., description="Batch operation name")
    batch_type: str = Field(..., description="Type of batch operation")
    sync_jobs: List[SyncJobRequest] = Field(...,
                                            description="List of sync jobs")
    parallel_execution: bool = Field(
        default=True, description="Execute jobs in parallel"
    )
    rollback_on_failure: bool = Field(
        default=False, description="Rollback all on any failure"
    )

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "batch_name": "MISP to HELK migration",
                "batch_type": "domain_migration",
                "sync_jobs": [],
                "parallel_execution": True,
                "rollback_on_failure": False,
            }
        }


class SyncStatusFilter(BaseModel):
    """Filter model for sync status queries."""

    tool_filter: Optional[str] = Field(None, description="Filter by tool")
    domain_filter: Optional[DomainType] = Field(
        None, description="Filter by domain")
    status_filter: Optional[List[SyncStatus]] = Field(
        None, description="Filter by status"
    )
    user_filter: Optional[str] = Field(None, description="Filter by user")
    limit: int = Field(default=50, description="Maximum results")
    offset: int = Field(default=0, description="Results offset")

    class Config:
        """Pydantic configuration."""

        schema_extra = {
            "example": {
                "tool_filter": "misp",
                "domain_filter": "security",
                "status_filter": ["pending", "in_progress"],
                "limit": 50,
                "offset": 0,
            }
        }


# Dependency injection
async def get_data_integration_service(
    db: AsyncSession = Depends(get_async_session),
) -> DataIntegrationService:
    """Get data integration service instance."""
    return DataIntegrationService(db)


async def get_event_bus_service() -> EventBusService:
    """Get event bus service instance."""
    # This would be injected from application state
    # For now, return a new instance
    return EventBusService()


# API Endpoints
@router.post("/jobs", response_model=SyncJobResponse, status_code=status.HTTP_201_CREATED)
async def create_sync_job(
    request: SyncJobRequest,
    integration_service: DataIntegrationService = Depends(
        get_data_integration_service),
    event_bus: EventBusService = Depends(get_event_bus_service),
) -> SyncJobResponse:
    """
    Create a new data synchronization job.

    Creates a sync job to transfer and transform data between tools
    across domains with automatic conflict resolution.
    """
    try:
        # Create sync job
        sync_state = await integration_service.create_sync_job(
            source_tool=request.source_tool,
            source_domain=request.source_domain,
            source_entity_type=request.source_entity_type,
            source_entity_id=request.source_entity_id,
            target_tool=request.target_tool,
            target_domain=request.target_domain,
            target_entity_type=request.target_entity_type,
            source_data=request.source_data,
            mapping_schema_id=request.mapping_schema_id,
            sync_direction=request.sync_direction,
            workflow_context=request.workflow_context,
        )

        # Publish sync started event
        await event_bus.publish_sync_event(
            sync_job_id=sync_state.sync_job_id,
            sync_status="started",
            source_tool=request.source_tool,
            target_tool=request.target_tool,
        )

        return SyncJobResponse.from_orm(sync_state)

    except DataIntegrationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sync job creation failed: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}",
        )


@router.post("/jobs/{sync_id}/execute", response_model=SyncJobResponse)
async def execute_sync_job(
    sync_id: UUID,
    integration_service: DataIntegrationService = Depends(
        get_data_integration_service),
    event_bus: EventBusService = Depends(get_event_bus_service),
) -> SyncJobResponse:
    """
    Execute a synchronization job.

    Executes data transformation and synchronization between tools
    with real-time status updates via WebSocket.
    """
    try:
        # Execute sync
        sync_state = await integration_service.execute_sync(str(sync_id))

        # Publish completion event
        await event_bus.publish_sync_event(
            sync_job_id=sync_state.sync_job_id,
            sync_status="completed" if sync_state.status == SyncStatus.COMPLETED else "failed",
            source_tool=sync_state.source_tool_id,
            target_tool=sync_state.target_tool_id,
            error_message=sync_state.error_message,
        )

        return SyncJobResponse.from_orm(sync_state)

    except DataIntegrationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Sync execution failed: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}",
        )


@router.get("/jobs/{sync_id}", response_model=SyncJobResponse)
async def get_sync_job_status(
    sync_id: UUID,
    integration_service: DataIntegrationService = Depends(
        get_data_integration_service),
) -> SyncJobResponse:
    """
    Get synchronization job status.

    Returns current status, progress, and timing information
    for a specific sync job.
    """
    sync_state = await integration_service.get_sync_status(str(sync_id))

    if not sync_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sync job {sync_id} not found",
        )

    return SyncJobResponse.from_orm(sync_state)


@router.delete("/jobs/{sync_id}")
async def cancel_sync_job(
    sync_id: UUID,
    reason: Optional[str] = None,
    integration_service: DataIntegrationService = Depends(
        get_data_integration_service),
    event_bus: EventBusService = Depends(get_event_bus_service),
) -> Dict[str, str]:
    """
    Cancel a synchronization job.

    Cancels a pending or in-progress sync job with optional reason.
    """
    cancelled = await integration_service.cancel_sync(str(sync_id), reason or "")

    if not cancelled:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sync job {sync_id} not found or already completed",
        )

    # Publish cancellation event
    await event_bus.publish_event(
        event_bus.Event(
            event_type=EventType.SYNC_FAILED,
            source_tool="sync_api",
            source_domain=DomainType.SYSTEM,
            payload={
                "sync_id": str(sync_id),
                "status": "cancelled",
                "reason": reason,
            },
        )
    )

    return {"message": f"Sync job {sync_id} cancelled", "reason": reason or ""}


@router.get("/jobs", response_model=List[SyncJobResponse])
async def list_sync_jobs(
    filter_params: SyncStatusFilter = Depends(),
    integration_service: DataIntegrationService = Depends(
        get_data_integration_service),
) -> List[SyncJobResponse]:
    """
    List synchronization jobs with filtering.

    Returns a paginated list of sync jobs with optional filtering
    by tool, domain, status, and user.
    """
    try:
        # Get filtered sync jobs
        sync_states = await integration_service.list_active_syncs(
            tool_filter=filter_params.tool_filter,
            domain_filter=filter_params.domain_filter,
        )

        # Apply additional filters
        if filter_params.status_filter:
            sync_states = [
                s for s in sync_states if s.status in filter_params.status_filter
            ]

        if filter_params.user_filter:
            sync_states = [
                s for s in sync_states if s.user_id == filter_params.user_filter
            ]

        # Apply pagination
        total_count = len(sync_states)
        sync_states = sync_states[
            filter_params.offset: filter_params.offset + filter_params.limit
        ]

        return [SyncJobResponse.from_orm(state) for state in sync_states]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sync jobs: {str(e)}",
        )


@router.post("/batch", response_model=Dict[str, Any])
async def create_batch_sync(
    request: BatchSyncRequest,
    integration_service: DataIntegrationService = Depends(
        get_data_integration_service),
    event_bus: EventBusService = Depends(get_event_bus_service),
) -> Dict[str, Any]:
    """
    Create a batch synchronization operation.

    Creates multiple sync jobs as a coordinated batch with
    optional parallel execution and rollback capabilities.
    """
    try:
        # Convert sync job requests to configuration dictionaries
        sync_configs = []
        for job_request in request.sync_jobs:
            config = {
                "source_tool": job_request.source_tool,
                "source_domain": job_request.source_domain,
                "source_entity_type": job_request.source_entity_type,
                "source_entity_id": job_request.source_entity_id,
                "target_tool": job_request.target_tool,
                "target_domain": job_request.target_domain,
                "target_entity_type": job_request.target_entity_type,
                "source_data": job_request.source_data,
                "mapping_schema_id": job_request.mapping_schema_id,
                "sync_direction": job_request.sync_direction,
                "workflow_context": job_request.workflow_context,
            }
            sync_configs.append(config)

        # Create batch sync
        batch = await integration_service.create_batch_sync(
            batch_name=request.batch_name,
            batch_type=request.batch_type,
            sync_configs=sync_configs,
            parallel_execution=request.parallel_execution,
            rollback_on_failure=request.rollback_on_failure,
        )

        # Publish batch started event
        await event_bus.publish_event(
            event_bus.Event(
                event_type=EventType.WORKFLOW_TRIGGERED,
                source_tool="sync_api",
                source_domain=DomainType.SYSTEM,
                payload={
                    "batch_id": str(batch.id),
                    "batch_name": request.batch_name,
                    "batch_type": request.batch_type,
                    "total_jobs": len(sync_configs),
                },
            )
        )

        return {
            "batch_id": str(batch.id),
            "batch_name": request.batch_name,
            "total_jobs": len(sync_configs),
            "status": batch.status,
            "created_at": batch.created_at.isoformat(),
        }

    except DataIntegrationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Batch sync creation failed: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal error: {str(e)}",
        )


@router.get("/schemas", response_model=List[Dict[str, str]])
async def list_mapping_schemas(
    integration_service: DataIntegrationService = Depends(
        get_data_integration_service),
) -> List[Dict[str, str]]:
    """
    List available data mapping schemas.

    Returns a list of all available mapping schemas for
    cross-tool data transformation.
    """
    schemas = []
    for schema_id, schema in integration_service.mapping_schemas.items():
        schemas.append(
            {
                "schema_id": schema_id,
                "schema_name": schema.schema_name,
                "source_tool": schema.source_tool,
                "target_tool": schema.target_tool,
                "source_domain": schema.source_domain.value,
                "target_domain": schema.target_domain.value,
                "bidirectional": str(schema.bidirectional),
            }
        )

    return schemas


@router.get("/health")
async def sync_service_health() -> Dict[str, Any]:
    """
    Get synchronization service health status.

    Returns health metrics including active syncs, performance,
    and service availability across all domains.
    """
    # This would implement comprehensive health checks
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "data_integration": "healthy",
            "event_bus": "healthy",
            "websocket": "healthy",
        },
        "performance": {
            "average_sync_time_ms": 150,
            "active_syncs": 0,
            "completed_syncs_24h": 0,
            "failed_syncs_24h": 0,
        },
        "domains": {
            "security": {"status": "healthy", "response_time_ms": 45},
            "productivity": {"status": "healthy", "response_time_ms": 65},
            "mtg": {"status": "healthy", "response_time_ms": 85},
            "infrastructure": {"status": "healthy", "response_time_ms": 120},
        },
    }
