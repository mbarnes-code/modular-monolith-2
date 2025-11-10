"""
Enhanced MISP Authentication API Endpoints

JWT-based authentication endpoints integrating with MISP patterns.
Migrated from features/MISP/app/Controller/UsersController.php login methods.
"""

from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ...config.settings import get_settings
from ...data.database import get_db
from ...services.misp.enhanced_auth_service import (MispAuthService,
                                                    get_current_user_api_key,
                                                    get_current_user_jwt)

router = APIRouter(prefix="/auth", tags=["misp-auth"])
settings = get_settings()


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str
    remember_me: bool = False


class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: dict


class RefreshRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class ApiKeyResponse(BaseModel):
    """API key response"""
    authkey: str
    message: str


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with email/password and return JWT tokens

    Migrated from MISP UsersController::login()
    Enhanced with JWT token generation
    """
    auth_service = MispAuthService(db)

    user_data = await auth_service.authenticate_user(
        login_data.email,
        login_data.password
    )

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Create tokens
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    if login_data.remember_me:
        access_token_expires = timedelta(
            days=settings.REMEMBER_ME_EXPIRE_DAYS
        )

    access_token = await auth_service.create_access_token(
        user_data,
        expires_delta=access_token_expires
    )

    refresh_token = await auth_service.create_refresh_token(user_data["id"])

    # Set secure HTTP-only cookies for web clients
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=int(access_token_expires.total_seconds()),
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=int(timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ).total_seconds()),
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax"
    )

    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=int(access_token_expires.total_seconds()),
        user={
            "id": user_data["id"],
            "email": user_data["email"],
            "org_id": user_data["org_id"],
            "org_name": user_data["org_name"],
            "role_name": user_data["role_name"],
            "permissions": user_data["permissions"]
        }
    )


@router.post("/refresh", response_model=dict)
async def refresh_token(
    refresh_data: RefreshRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token

    Enhanced security with token rotation
    """
    auth_service = MispAuthService(db)

    new_access_token = await auth_service.refresh_access_token(
        refresh_data.refresh_token
    )

    if not new_access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/logout")
async def logout(
    response: Response,
    current_user: dict = Depends(get_current_user_jwt)
):
    """
    Logout user and clear authentication cookies

    Enhanced with secure cookie clearing
    """
    # Clear authentication cookies
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {"message": "Successfully logged out"}


@router.get("/me", response_model=dict)
async def get_current_user(
    current_user: dict = Depends(get_current_user_jwt)
):
    """
    Get current user information from JWT token

    Enhanced with full user profile data
    """
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "org_id": current_user["org_id"],
        "org_name": current_user.get("org_name"),
        "role_id": current_user["role_id"],
        "role_name": current_user.get("role_name"),
        "permissions": current_user.get("permissions", [])
    }


@router.get("/me/api-key", response_model=dict)
async def get_current_user_api_key_info(
    current_user: dict = Depends(get_current_user_api_key)
):
    """
    Get current user information from API key

    Preserves MISP API key authentication compatibility
    """
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "org_id": current_user["org_id"],
        "org_name": current_user.get("org_name"),
        "role_name": current_user.get("role_name"),
        "authkey": current_user.get("authkey", "")[:8] + "..." if current_user.get("authkey") else None,
        "last_api_access": current_user.get("last_api_access")
    }


@router.post("/generate-api-key", response_model=ApiKeyResponse)
async def generate_new_api_key(
    current_user: dict = Depends(get_current_user_jwt),
    db: Session = Depends(get_db)
):
    """
    Generate new API key for current user

    Migrated from MISP UsersController::resetauthkey()
    Enhanced with JWT-based authorization
    """
    auth_service = MispAuthService(db)

    # Generate new API key
    new_api_key = auth_service.generate_api_key()

    # Update user's API key in database
    from ...data.models.misp_models import User
    user = db.query(User).filter(User.id == current_user["id"]).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.authkey = new_api_key
    db.commit()

    return ApiKeyResponse(
        authkey=new_api_key,
        message="New API key generated successfully"
    )


@router.get("/permissions", response_model=dict)
async def get_user_permissions(
    current_user: dict = Depends(get_current_user_jwt)
):
    """
    Get detailed user permissions

    Enhanced with granular permission breakdown
    """
    permissions = current_user.get("permissions", [])

    # Categorize permissions for better understanding
    categorized_permissions = {
        "admin": "admin" in permissions,
        "org_admin": "org_admin" in permissions,
        "events": {
            "create": "events:create" in permissions,
            "update": "events:update" in permissions,
            "publish": "events:publish" in permissions,
        },
        "attributes": {
            "create": "attributes:create" in permissions,
            "update": "attributes:update" in permissions,
        },
        "tags": {
            "create": "tags:create" in permissions,
            "update": "tags:update" in permissions,
            "attach": "tags:attach" in permissions,
        },
        "sync": {
            "read": "sync:read" in permissions,
            "write": "sync:write" in permissions,
        },
        "audit": {
            "read": "audit:read" in permissions,
        },
        "sharing_groups": {
            "read": "sharinggroups:read" in permissions,
            "create": "sharinggroups:create" in permissions,
            "update": "sharinggroups:update" in permissions,
        }
    }

    return {
        "raw_permissions": permissions,
        "categorized": categorized_permissions
    }


@router.post("/verify-token", response_model=dict)
async def verify_token(
    current_user: dict = Depends(get_current_user_jwt)
):
    """
    Verify JWT token validity

    Useful for client-side token validation
    """
    return {
        "valid": True,
        "user_id": current_user["id"],
        "expires": current_user.get("exp"),
        "issued": current_user.get("iat")
    }
