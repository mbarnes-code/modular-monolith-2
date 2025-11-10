"""
MISP Attributes API Endpoints

FastAPI implementation of MISP Attributes Controller.
Migrated from features/MISP/app/Controller/AttributesController.php
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...schemas.misp.attributes import (AttributeCreate, AttributeListResponse,
                                        AttributeResponse, AttributeSearch,
                                        AttributeUpdate)
from ...services.misp.attributes_service import MispAttributesService
from ...services.misp.auth_service import require_api_key

router = APIRouter(prefix="/attributes", tags=["misp-attributes"])


@router.get("/", response_model=AttributeListResponse)
async def list_attributes(
    value: Optional[str] = None,
    type: Optional[str] = None,
    category: Optional[str] = None,
    org: Optional[str] = None,
    eventid: Optional[int] = None,
    timestamp: Optional[str] = None,
    limit: int = Query(default=60, le=9999),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    Search across all attributes with complex filtering

    Migrated from AttributesController::index()
    Preserves cross-event correlation and distribution filtering
    """
    attributes_service = MispAttributesService(db)

    try:
        results = await attributes_service.search_attributes(
            user=current_user,
            value=value,
            attribute_type=type,
            category=category,
            org=org,
            event_id=eventid,
            timestamp=timestamp,
            limit=limit,
            page=page
        )

        return AttributeListResponse(
            attributes=results["attributes"],
            total=results["total"],
            page=page,
            limit=limit
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search attributes: {str(e)}"
        )


@router.post("/", response_model=AttributeResponse, status_code=status.HTTP_201_CREATED)
async def create_attribute(
    attribute_data: AttributeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    Add new attribute to existing event

    Migrated from AttributesController::add()
    Preserves type-value compatibility and correlation triggers
    """
    attributes_service = MispAttributesService(db)

    try:
        attribute = await attributes_service.create_attribute(
            attribute_data=attribute_data,
            user=current_user
        )

        return AttributeResponse(**attribute)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create attribute: {str(e)}"
        )


@router.post("/restSearch", response_model=AttributeListResponse)
async def search_attributes_advanced(
    search_data: AttributeSearch,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    Advanced attribute search with complex criteria

    Migrated from AttributesController::restSearch()
    Preserves boolean logic, date ranges, and organization filtering
    """
    attributes_service = MispAttributesService(db)

    try:
        results = await attributes_service.advanced_search(
            search_criteria=search_data,
            user=current_user
        )

        return AttributeListResponse(
            attributes=results["attributes"],
            total=results["total"],
            page=search_data.page or 1,
            limit=search_data.limit or 60
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Advanced search failed: {str(e)}"
        )


@router.get("/{attribute_id}", response_model=AttributeResponse)
async def get_attribute(
    attribute_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Get single attribute by ID"""
    attributes_service = MispAttributesService(db)

    try:
        attribute = await attributes_service.get_attribute(
            attribute_id=attribute_id,
            user=current_user
        )

        if not attribute:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attribute not found or access denied"
            )

        return AttributeResponse(**attribute)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attribute: {str(e)}"
        )


@router.put("/{attribute_id}", response_model=AttributeResponse)
async def update_attribute(
    attribute_id: int,
    attribute_data: AttributeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Update existing attribute"""
    attributes_service = MispAttributesService(db)

    try:
        attribute = await attributes_service.update_attribute(
            attribute_id=attribute_id,
            attribute_data=attribute_data,
            user=current_user
        )

        if not attribute:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attribute not found or access denied"
            )

        return AttributeResponse(**attribute)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update attribute: {str(e)}"
        )


@router.delete("/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute(
    attribute_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Delete attribute (soft delete)"""
    attributes_service = MispAttributesService(db)

    try:
        success = await attributes_service.delete_attribute(
            attribute_id=attribute_id,
            user=current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Attribute not found or access denied"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete attribute: {str(e)}"
        )
