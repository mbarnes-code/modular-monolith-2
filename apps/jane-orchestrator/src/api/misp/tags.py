"""
MISP Tags API Endpoints

FastAPI implementation of MISP Tags Controller.
Migrated from features/MISP/app/Controller/TagsController.php
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...schemas.misp.tags import (TagAttachment, TagCreate, TagListResponse,
                                  TagResponse, TagUpdate)
from ...services.misp.auth_service import require_api_key
from ...services.misp.tags_service import MispTagsService

router = APIRouter(prefix="/tags", tags=["misp-tags"])


@router.get("/", response_model=TagListResponse)
async def list_tags(
    name: Optional[str] = None,
    colour: Optional[str] = None,
    exportable: Optional[bool] = None,
    hide_tag: Optional[bool] = None,
    limit: int = Query(default=100, le=9999),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    List tags with filtering

    Migrated from TagsController::index()
    Preserves tag visibility and taxonomy relationships
    """
    tags_service = MispTagsService(db)

    try:
        results = await tags_service.list_tags(
            user=current_user,
            name=name,
            colour=colour,
            exportable=exportable,
            hide_tag=hide_tag,
            limit=limit,
            page=page
        )

        return TagListResponse(
            tags=results["tags"],
            total=results["total"],
            page=page,
            limit=limit
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list tags: {str(e)}"
        )


@router.post("/", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    Create new tag

    Migrated from TagsController::add()
    Preserves tag validation and taxonomy integration
    """
    tags_service = MispTagsService(db)

    try:
        tag = await tags_service.create_tag(
            tag_data=tag_data,
            user=current_user
        )

        return TagResponse(**tag)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create tag: {str(e)}"
        )


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Get single tag by ID"""
    tags_service = MispTagsService(db)

    try:
        tag = await tags_service.get_tag(
            tag_id=tag_id,
            user=current_user
        )

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found or access denied"
            )

        return TagResponse(**tag)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve tag: {str(e)}"
        )


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_data: TagUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Update existing tag"""
    tags_service = MispTagsService(db)

    try:
        tag = await tags_service.update_tag(
            tag_id=tag_id,
            tag_data=tag_data,
            user=current_user
        )

        if not tag:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found or access denied"
            )

        return TagResponse(**tag)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update tag: {str(e)}"
        )


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Delete tag (soft delete)"""
    tags_service = MispTagsService(db)

    try:
        success = await tags_service.delete_tag(
            tag_id=tag_id,
            user=current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tag not found or access denied"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete tag: {str(e)}"
        )


@router.post("/attachTagToObject", status_code=status.HTTP_200_OK)
async def attach_tag_to_object(
    attachment_data: TagAttachment,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    Attach tag to event or attribute

    Migrated from TagsController::attachTagToObject()
    Preserves tag attachment logic and access control
    """
    tags_service = MispTagsService(db)

    try:
        success = await tags_service.attach_tag_to_object(
            attachment_data=attachment_data,
            user=current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to attach tag to object"
            )

        return {"message": "Tag attached successfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to attach tag: {str(e)}"
        )


@router.post("/removeTagFromObject", status_code=status.HTTP_200_OK)
async def remove_tag_from_object(
    attachment_data: TagAttachment,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    Remove tag from event or attribute

    Migrated from TagsController::removeTagFromObject()
    Preserves tag removal logic and access control
    """
    tags_service = MispTagsService(db)

    try:
        success = await tags_service.remove_tag_from_object(
            attachment_data=attachment_data,
            user=current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to remove tag from object"
            )

        return {"message": "Tag removed successfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to remove tag: {str(e)}"
        )
