"""
MISP Organizations API Endpoints

FastAPI implementation of MISP Organizations Controller.
Migrated from features/MISP/app/Controller/OrganisationsController.php
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...schemas.misp.organizations import (OrganizationCreate,
                                           OrganizationListResponse,
                                           OrganizationResponse,
                                           OrganizationUpdate)
from ...services.misp.auth_service import require_api_key
from ...services.misp.organizations_service import MispOrganizationsService

router = APIRouter(
    prefix="/organisations", tags=["misp-organizations"]
)


@router.get("/", response_model=OrganizationListResponse)
async def list_organizations(
    name: Optional[str] = None,
    sector: Optional[str] = None,
    nationality: Optional[str] = None,
    limit: int = Query(default=60, le=9999),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    List organizations with filtering

    Migrated from OrganisationsController::index()
    Preserves organization visibility and access control
    """
    orgs_service = MispOrganizationsService(db)

    try:
        results = await orgs_service.list_organizations(
            user=current_user,
            name=name,
            sector=sector,
            nationality=nationality,
            limit=limit,
            page=page
        )

        return OrganizationListResponse(
            organisations=results["organizations"],
            total=results["total"],
            page=page,
            limit=limit
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list organizations: {str(e)}"
        )


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_organization(
    org_data: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    Create new organization

    Migrated from OrganisationsController::add()
    Preserves organization validation and access control
    """
    orgs_service = MispOrganizationsService(db)

    try:
        organization = await orgs_service.create_organization(
            org_data=org_data,
            user=current_user
        )

        return OrganizationResponse(**organization)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create organization: {str(e)}"
        )


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Get single organization by ID"""
    orgs_service = MispOrganizationsService(db)

    try:
        organization = await orgs_service.get_organization(
            org_id=org_id,
            user=current_user
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found or access denied"
            )

        return OrganizationResponse(**organization)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve organization: {str(e)}"
        )


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: int,
    org_data: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Update existing organization"""
    orgs_service = MispOrganizationsService(db)

    try:
        organization = await orgs_service.update_organization(
            org_id=org_id,
            org_data=org_data,
            user=current_user
        )

        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found or access denied"
            )

        return OrganizationResponse(**organization)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update organization: {str(e)}"
        )


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Delete organization (soft delete)"""
    orgs_service = MispOrganizationsService(db)

    try:
        success = await orgs_service.delete_organization(
            org_id=org_id,
            user=current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found or access denied"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete organization: {str(e)}"
        )


@router.get("/{org_id}/events", response_model=dict)
async def get_organization_events(
    org_id: int,
    limit: int = Query(default=50, le=1000),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Get events belonging to organization"""
    orgs_service = MispOrganizationsService(db)

    try:
        events = await orgs_service.get_organization_events(
            org_id=org_id,
            user=current_user,
            limit=limit,
            page=page
        )

        return events

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve organization events: {str(e)}"
        )


@router.get("/{org_id}/users", response_model=dict)
async def get_organization_users(
    org_id: int,
    limit: int = Query(default=50, le=1000),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Get users belonging to organization"""
    orgs_service = MispOrganizationsService(db)

    try:
        users = await orgs_service.get_organization_users(
            org_id=org_id,
            user=current_user,
            limit=limit,
            page=page
        )

        return users

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve organization users: {str(e)}"
        )
