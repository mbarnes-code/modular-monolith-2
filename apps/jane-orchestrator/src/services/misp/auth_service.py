"""
MISP Authentication Service

Handles API key authentication for MISP endpoints.
"""

from typing import Optional

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...data.models.misp.core_models import User


async def get_api_key(x_authkey: Optional[str] = Header(None)):
    """Extract API key from X-Authkey header"""
    if not x_authkey:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return x_authkey


async def get_current_user(
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
) -> User:
    """Get current user from API key"""

    user = db.query(User).filter(User.authkey == api_key).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account disabled"
        )

    return user


# Alias for consistency with original MISP naming
require_api_key = get_current_user
