"""
MISP Events API Endpoints

FastAPI implementation of MISP Events Controller.
Migrated from features/MISP/app/Controller/EventsController.php
"""

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from ...middleware.misp_rbac import (require_events_create,
                                     require_events_delete,
                                     require_events_publish,
                                     require_events_read,
                                     require_events_update)
from ...schemas.misp.events import (EventCreate, EventListResponse,
                                    EventResponse, EventSearch, EventUpdate)
from ...services.misp.enhanced_auth_service import get_current_user
from ...services.misp.events_service import MispEventsService

router = APIRouter(prefix="/events", tags=["misp-events"])


class EventListParams(BaseModel):
    """Parameters for event listing and filtering"""
    org: Optional[str] = None
    date: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    published: Optional[bool] = None
    limit: int = Field(default=60, le=9999)
    page: int = Field(default=1, ge=1)
    sort: str = Field(default="timestamp")
    direction: str = Field(default="desc")


@router.get("/events")
async def list_events(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(
        50, ge=1, le=100, description="Number of events per page"),
    search: str = Query(None, description="Search term"),
    current_user=Depends(require_events_read)
):
    """
    List events with filtering and pagination

    Migrated from EventsController::index()
    Preserves MISP distribution-aware filtering and ACL enforcement
    """
    events_service = MispEventsService()

    try:
        events = await events_service.list_events(
            user=current_user,
            search=search,
            limit=limit,
            page=page
        )

        return EventListResponse(
            events=events["events"],
            total=events["total"],
            page=page,
            limit=limit
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list events: {str(e)}"
        )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: int,
    include_attributes: bool = Query(default=True, alias="includeAttributes"),
    include_correlations: bool = Query(
        default=False, alias="includeCorrelations"
    ),
    current_user=Depends(require_events_read)
):
    """
    Get single event by ID

    Migrated from EventsController::view()
    Includes distribution-aware attribute filtering and correlation data
    """
    events_service = MispEventsService()

    try:
        event = await events_service.get_event(
            event_id=event_id,
            user=current_user,
            include_attributes=include_attributes,
            include_correlations=include_correlations
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found or access denied"
            )

        return EventResponse(**event)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve event: {str(e)}"
        )


@router.post(
    "/", response_model=EventResponse, status_code=status.HTTP_201_CREATED
)
async def create_event(
    event_data: EventCreate,
    current_user=Depends(require_events_create)
):
    """
    Create new threat intelligence event

    Migrated from EventsController::add()
    Preserves validation, correlation triggers, and notification workflows
    """
    events_service = MispEventsService()

    try:
        event = await events_service.create_event(
            event_data=event_data,
            user=current_user
        )

        return EventResponse(**event)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create event: {str(e)}"
        )


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int,
    event_data: EventUpdate,
    current_user=Depends(require_events_update)
):
    """
    Update existing event

    Migrated from EventsController::edit()
    Preserves published event restrictions and distribution rules
    """
    events_service = MispEventsService(db)

    try:
        event = await events_service.update_event(
            event_id=event_id,
            event_data=event_data,
            user=current_user
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found or access denied"
            )

        return EventResponse(**event)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update event: {str(e)}"
        )


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    current_user=Depends(require_events_delete)
):
    """
    Soft delete event (published events marked deleted)

    Migrated from EventsController::delete()
    Preserves audit trail and cascade behavior
    """
    events_service = MispEventsService(db)

    try:
        success = await events_service.delete_event(
            event_id=event_id,
            user=current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found or access denied"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete event: {str(e)}"
        )


@router.get("/search")
async def search_events(
    query: str = Query(..., description="Search query"),
    limit: int = Query(50, ge=1, le=100, description="Number of results"),
    current_user=Depends(require_events_read)
):
    """
    Complex event search with multiple criteria

    Migrated from EventsController::restSearch()
    Preserves full-text search, taxonomy filtering, and time ranges
    """
    events_service = MispEventsService()

    try:
        results = await events_service.search_events(
            query=query,
            user=current_user,
            limit=limit
        )

        return EventListResponse(
            events=results["events"],
            total=results["total"],
            page=1,
            limit=limit
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search failed: {str(e)}"
        )


@router.get("/{event_id}/publish", response_model=EventResponse)
async def publish_event(
    event_id: int,
    current_user=Depends(require_events_publish)
):
    """
    Publish event for distribution

    Migrated from EventsController::publish()
    Preserves sync triggers and notification workflows
    """
    events_service = MispEventsService()

    try:
        event = await events_service.publish_event(
            event_id=event_id,
            user=current_user
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found or access denied"
            )

        return EventResponse(**event)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish event: {str(e)}"
        )


@router.get("/{event_id}/unpublish", response_model=EventResponse)
async def unpublish_event(
    event_id: int,
    current_user=Depends(require_events_publish)
):
    """
    Unpublish (depublish) event

    Migrated from EventsController::unpublish()
    Preserves revocation notifications and audit logging
    """
    events_service = MispEventsService(db)

    try:
        event = await events_service.unpublish_event(
            event_id=event_id,
            user=current_user
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found or access denied"
            )

        return EventResponse(**event)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to unpublish event: {str(e)}"
        )


@router.get("/nids/{export_format}")
async def export_nids_rules(
    export_format: str,
    org: Optional[str] = None,
    eventid: Optional[int] = None,
    tags: Optional[str] = None,
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
    current_user=Depends(require_events_read)
):
    """
    Generate IDS rules from published events

    Migrated from EventsController::nids()
    Supports suricata, snort, yara formats with business logic preservation
    """
    events_service = MispEventsService(db)

    if format not in ["suricata", "snort", "yara"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported format. Supported: suricata, snort, yara"
        )

    try:
        rules = await events_service.export_nids_rules(
            format=format,
            user=current_user,
            org=org,
            event_id=eventid,
            tags=tags,
            from_date=from_date,
            to_date=to_date
        )

        # Return as plain text for IDS rule formats
        from fastapi.responses import PlainTextResponse
        return PlainTextResponse(
            content=rules,
            media_type="text/plain"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export rules: {str(e)}"
        )


@router.get("/{event_id}/downloadOpenIOCEvent")
async def download_openioc_event(
    event_id: int,
    current_user=Depends(require_events_read)
):
    """
    Export event in OpenIOC XML format

    Migrated from EventsController::downloadOpenIOCEvent()
    Preserves OpenIOC 1.1 specification compliance
    """
    events_service = MispEventsService(db)

    try:
        xml_content = await events_service.export_openioc(
            event_id=event_id,
            user=current_user
        )

        if not xml_content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found or access denied"
            )

        from fastapi.responses import Response
        return Response(
            content=xml_content,
            media_type="application/xml",
            headers={
                "Content-Disposition": f"attachment; filename=event_{event_id}.xml"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export OpenIOC: {str(e)}"
        )
