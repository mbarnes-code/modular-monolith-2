"""
API dependency functions for Jane Orchestrator.

Provides shared dependencies for FastAPI endpoints including:
- Database session management
- Authentication and user context
- Executive function support utilities
"""

import logging
from typing import Any, Dict

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ..data.models import User
from ..db.session import get_db
from .auth.endpoints import decode_token

logger = logging.getLogger(__name__)
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get the current authenticated user from JWT token.

    This is a shared dependency that can be used across all API endpoints
    that require authentication.
    """
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


def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get the current active user (must be active).

    Executive function consideration: Provides clear error messages
    for inactive accounts with helpful guidance.
    """
    if not current_user.get("is_active"):
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Account is inactive",
                "executive_function_hint": (
                    "Contact support to reactivate your account"
                )
            }
        )
    return current_user


def get_optional_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Dict[str, Any] | None:
    """
    Get the current user if authenticated, None if not.

    Useful for endpoints that can work with or without authentication.
    """
    if not credentials:
        return None

    try:
        return get_current_user(credentials, db)
    except HTTPException:
        return None
