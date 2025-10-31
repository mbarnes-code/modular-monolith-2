"""
MISP Users API Endpoints

FastAPI implementation of MISP Users Controller.
Migrated from features/MISP/app/Controller/UsersController.php
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...schemas.misp.users import (PasswordChange, UserCreate,
                                   UserListResponse, UserResponse, UserUpdate)
from ...services.misp.auth_service import require_api_key
from ...services.misp.users_service import MispUsersService

router = APIRouter(prefix="/users", tags=["misp-users"])


@router.get("/", response_model=UserListResponse)
async def list_users(
    email: Optional[str] = None,
    org_id: Optional[int] = None,
    role_id: Optional[int] = None,
    disabled: Optional[bool] = None,
    limit: int = Query(default=60, le=9999),
    page: int = Query(default=1, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    List users with filtering

    Migrated from UsersController::index()
    Preserves user visibility and access control
    """
    users_service = MispUsersService(db)

    try:
        results = await users_service.list_users(
            requesting_user=current_user,
            email=email,
            org_id=org_id,
            role_id=role_id,
            disabled=disabled,
            limit=limit,
            page=page
        )

        return UserListResponse(
            users=results["users"],
            total=results["total"],
            page=page,
            limit=limit
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list users: {str(e)}"
        )


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """
    Create new user

    Migrated from UsersController::add()
    Preserves user validation and role-based access control
    """
    users_service = MispUsersService(db)

    try:
        user = await users_service.create_user(
            user_data=user_data,
            requesting_user=current_user
        )

        return UserResponse(**user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Get single user by ID"""
    users_service = MispUsersService(db)

    try:
        user = await users_service.get_user(
            user_id=user_id,
            requesting_user=current_user
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or access denied"
            )

        return UserResponse(**user)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Update existing user"""
    users_service = MispUsersService(db)

    try:
        user = await users_service.update_user(
            user_id=user_id,
            user_data=user_data,
            requesting_user=current_user
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or access denied"
            )

        return UserResponse(**user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Delete user (soft delete)"""
    users_service = MispUsersService(db)

    try:
        success = await users_service.delete_user(
            user_id=user_id,
            requesting_user=current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or access denied"
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )


@router.post("/{user_id}/change_password", status_code=status.HTTP_200_OK)
async def change_password(
    user_id: int,
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Change user password"""
    users_service = MispUsersService(db)

    try:
        success = await users_service.change_password(
            user_id=user_id,
            password_data=password_data,
            requesting_user=current_user
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or access denied"
            )

        return {"message": "Password changed successfully"}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )


@router.post("/{user_id}/reset_authkey", response_model=dict)
async def reset_auth_key(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_api_key)
):
    """Reset user API authentication key"""
    users_service = MispUsersService(db)

    try:
        new_key = await users_service.reset_auth_key(
            user_id=user_id,
            requesting_user=current_user
        )

        if not new_key:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or access denied"
            )

        return {"authkey": new_key}

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reset auth key: {str(e)}"
        )
