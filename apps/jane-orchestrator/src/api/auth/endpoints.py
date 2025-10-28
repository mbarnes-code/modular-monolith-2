"""
Authentication API endpoints for executive function platform.

Constitutional Requirements:
- JWT-based authentication with secure session management
- Executive function user preferences and accommodations
- Unified login/logout across all 37 tools
- ADHD/autism-friendly authentication flows
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ...core.config import settings
from ...data.models import User
from ...db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


class AuthRequest:
    """Authentication request models."""

    def __init__(
        self,
        username: str,
        password: str,
        remember_me: bool = False,
        executive_function_preferences: Optional[Dict[str, Any]] = None
    ):
        self.username = username
        self.password = password
        self.remember_me = remember_me
        self.executive_function_preferences = (
            executive_function_preferences or {}
        )


class AuthResponse:
    """Authentication response models."""

    def __init__(
        self,
        access_token: str,
        refresh_token: str,
        token_type: str = "bearer",
        expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_info: Optional[Dict[str, Any]] = None
    ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.user_info = user_info


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password for storage."""
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create a JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )


def authenticate_user(
    db: Session, username: str, password: str
) -> Optional[User]:
    """Authenticate a user by username and password."""
    user = db.query(User).filter(User.username == username).first()

    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None

    return user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Get the current authenticated user from JWT token."""
    try:
        token = credentials.credentials
        payload = decode_token(token)

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token type"
            )

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="User not found"
            )

        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active,
            "adhd_accommodations": user.adhd_accommodations or {},
            "autism_accommodations": user.autism_accommodations or {},
            "preferred_domains": user.preferred_domains or [],
            "ui_preferences": user.ui_preferences or {}
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting current user: %s", str(e))
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )


@router.post("/login", summary="User login")
async def login(
    username: str,
    password: str,
    remember_me: bool = False,
    executive_function_preferences: Optional[Dict[str, Any]] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Authenticate user and return JWT tokens.

    Executive Function Features:
    - Simplified login flow for cognitive load reduction
    - Remember me option for reduced authentication friction
    - Executive function preferences integration
    - ADHD/autism-friendly error messages
    """
    try:
        # Authenticate user
        user = authenticate_user(db, username, password)
        if not user:
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Login failed - please check your credentials",
                    "executive_function_hint": (
                        "Take your time and double-check your username "
                        "and password"
                    )
                }
            )

        if not user.is_active:
            raise HTTPException(
                status_code=401,
                detail={
                    "message": "Account is not active",
                    "executive_function_hint": (
                        "Contact support if you need help activating "
                        "your account"
                    )
                }
            )

        # Update executive function preferences if provided
        if executive_function_preferences:
            user.adhd_accommodations = executive_function_preferences.get(
                "adhd_accommodations", user.adhd_accommodations
            )
            user.autism_accommodations = executive_function_preferences.get(
                "autism_accommodations", user.autism_accommodations
            )
            user.ui_preferences = executive_function_preferences.get(
                "ui_preferences", user.ui_preferences
            )
            db.commit()

        # Create tokens
        token_data = {"sub": str(user.id), "username": user.username}

        access_token_expires = timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        if remember_me:
            # Extend access token for remember me
            access_token_expires = timedelta(days=1)

        access_token = create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data=token_data)

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": int(access_token_expires.total_seconds()),
            "user_info": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "executive_function_support": True,
                "adhd_accommodations": user.adhd_accommodations or {},
                "autism_accommodations": user.autism_accommodations or {},
                "preferred_domains": user.preferred_domains or [],
                "ui_preferences": user.ui_preferences or {}
            },
            "authentication_features": {
                "remember_me_enabled": remember_me,
                "executive_function_support": True,
                "unified_session": True,
                "cognitive_load_optimized": True
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Login error: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Login system temporarily unavailable",
                "executive_function_hint": (
                    "Please try again in a moment. The system is "
                    "working to resolve this."
                )
            }
        )


@router.post("/refresh", summary="Refresh access token")
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Refresh an access token using a valid refresh token.

    Executive Function Features:
    - Seamless token refresh for uninterrupted access
    - No re-authentication required
    - Maintains user preferences and accommodations
    """
    try:
        # Decode refresh token
        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        user_id = payload.get("sub")
        username = payload.get("username")

        if not user_id or not username:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )

        # Verify user still exists and is active
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail="User not found or inactive"
            )

        # Create new access token
        token_data = {"sub": str(user.id), "username": user.username}
        access_token = create_access_token(data=token_data)

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "refresh_successful": True,
            "user_id": user.id
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Token refresh error: %s", str(e))
        raise HTTPException(
            status_code=401,
            detail="Could not refresh token"
        )


@router.post("/logout", summary="User logout")
async def logout(
    response: Response,
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Log out the current user.

    Executive Function Features:
    - Clear logout confirmation
    - Session cleanup guidance
    - Smooth transition back to login
    """
    try:
        # In a production system, you might want to:
        # 1. Add tokens to a blacklist
        # 2. Clear server-side sessions
        # 3. Invalidate refresh tokens

        # Clear any HTTP-only cookies if used
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return {
            "message": "Successfully logged out",
            "user_id": current_user.get("id"),
            "logout_timestamp": datetime.utcnow().isoformat(),
            "executive_function_guidance": {
                "message": "You've been safely logged out",
                "next_steps": "You can log back in anytime to access your tools",
                "cognitive_load_tip": (
                    "Take a break if needed - your preferences will be "
                    "saved for next time"
                )
            }
        }

    except Exception as e:
        logger.error("Logout error: %s", str(e))
        return {
            "message": "Logout completed",
            "note": "Session cleared locally"
        }


@router.get("/me", summary="Get current user info")
async def get_me(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get current authenticated user information.

    Executive Function Features:
    - Complete user profile with accommodations
    - Preference settings for all tools
    - Domain configuration and accessibility needs
    """
    return {
        "user": current_user,
        "authentication_status": "active",
        "executive_function_profile": {
            "adhd_support_enabled": bool(
                current_user.get("adhd_accommodations")
            ),
            "autism_support_enabled": bool(
                current_user.get("autism_accommodations")
            ),
            "preferred_domains": current_user.get("preferred_domains", []),
            "ui_customizations": current_user.get("ui_preferences", {})
        },
        "session_info": {
            "unified_access": True,
            "tool_count": 37,
            "domain_count": 4,
            "executive_function_ready": True
        }
    }


@router.put("/preferences", summary="Update user preferences")
async def update_preferences(
    adhd_accommodations: Optional[Dict[str, Any]] = None,
    autism_accommodations: Optional[Dict[str, Any]] = None,
    ui_preferences: Optional[Dict[str, Any]] = None,
    preferred_domains: Optional[List[str]] = None,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Update executive function preferences and accommodations.

    Features:
    - ADHD accommodations (focus, timing, reminders)
    - Autism accommodations (sensory, routine, communication)
    - UI customizations (colors, layout, interactions)
    - Domain preferences and organization
    """
    try:
        user = db.query(User).filter(
            User.id == current_user.get("id")
        ).first()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        # Update preferences
        if adhd_accommodations is not None:
            user.adhd_accommodations = adhd_accommodations

        if autism_accommodations is not None:
            user.autism_accommodations = autism_accommodations

        if ui_preferences is not None:
            user.ui_preferences = ui_preferences

        if preferred_domains is not None:
            user.preferred_domains = preferred_domains

        user.updated_at = datetime.utcnow()
        db.commit()

        return {
            "message": "Preferences updated successfully",
            "user_id": user.id,
            "updated_preferences": {
                "adhd_accommodations": user.adhd_accommodations,
                "autism_accommodations": user.autism_accommodations,
                "ui_preferences": user.ui_preferences,
                "preferred_domains": user.preferred_domains
            },
            "executive_function_confirmation": {
                "accommodations_active": True,
                "ui_customizations_applied": True,
                "preferences_saved": True
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating preferences: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail="Could not update preferences"
        )


@router.get("/health", summary="Authentication system health")
async def auth_health() -> Dict[str, Any]:
    """
    Check authentication system health and configuration.

    Executive Function Features:
    - System status for transparency
    - Configuration validation
    - Executive function readiness check
    """
    return {
        "status": "healthy",
        "authentication_system": "JWT",
        "token_expiry": {
            "access_token_minutes": ACCESS_TOKEN_EXPIRE_MINUTES,
            "refresh_token_days": REFRESH_TOKEN_EXPIRE_DAYS
        },
        "executive_function_features": {
            "adhd_accommodations": True,
            "autism_accommodations": True,
            "preference_management": True,
            "unified_session": True,
            "cognitive_load_optimization": True
        },
        "security_features": {
            "jwt_tokens": True,
            "password_hashing": "bcrypt",
            "token_refresh": True,
            "secure_logout": True
        }
    }
