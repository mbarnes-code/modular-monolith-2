"""
Role-Based Access Control Middleware

Enhanced RBAC middleware integrating MISP role system with unified JWT.
Migrated from features/MISP/app/Controller/Component/ACL/ patterns.
"""

from functools import wraps
from typing import Any, Callable, Dict, List

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...data.database import get_db
from ...services.misp.enhanced_auth_service import (MispAuthService,
                                                    get_current_user_api_key,
                                                    get_current_user_jwt)


class MispRolePermissions:
    """MISP role-based permission definitions"""

    # Site Admin permissions (full access)
    SITE_ADMIN = ["admin"]

    # Organization Admin permissions
    ORG_ADMIN = [
        "org_admin",
        "events:create", "events:update:org", "events:publish:org",
        "attributes:create", "attributes:update:org",
        "users:create:org", "users:update:org",
        "tags:create", "tags:attach",
        "sharinggroups:read", "sharinggroups:create"
    ]

    # Sync User permissions
    SYNC_USER = [
        "sync:read", "sync:write",
        "events:read", "events:create", "events:update",
        "attributes:read", "attributes:create", "attributes:update"
    ]

    # Publisher permissions
    PUBLISHER = [
        "events:create", "events:update", "events:publish",
        "attributes:create", "attributes:update",
        "tags:attach"
    ]

    # Standard User permissions
    USER = [
        "events:read", "events:create", "events:update:own",
        "attributes:read", "attributes:create", "attributes:update:own",
        "tags:read"
    ]

    # Read Only permissions
    READ_ONLY = [
        "events:read",
        "attributes:read",
        "tags:read"
    ]


def require_misp_permission(permission: str, allow_api_key: bool = True):
    """
    Decorator for MISP permission-based access control

    Args:
        permission: Required permission string (e.g., "events:create")
        allow_api_key: Whether to allow API key authentication
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get user from JWT or API key
            if allow_api_key:
                # Try API key first (for backward compatibility)
                try:
                    current_user = await get_current_user_api_key(
                        kwargs.get('request'),
                        kwargs.get('db')
                    )
                except HTTPException:
                    # Fall back to JWT
                    current_user = await get_current_user_jwt(
                        kwargs.get('credentials'),
                        kwargs.get('db')
                    )
            else:
                current_user = await get_current_user_jwt(
                    kwargs.get('credentials'),
                    kwargs.get('db')
                )

            # Check permission
            db = kwargs.get('db')
            auth_service = MispAuthService(db)

            user_permissions = current_user.get("permissions", [])

            if not auth_service.check_permission(user_permissions, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions: {permission} required"
                )

            # Add current user to kwargs for the endpoint
            kwargs['current_user'] = current_user
            return await func(*args, **kwargs)

        return wrapper
    return decorator


def require_misp_role(role: str, allow_api_key: bool = True):
    """
    Decorator for MISP role-based access control

    Args:
        role: Required role name (e.g., "admin", "org_admin")
        allow_api_key: Whether to allow API key authentication
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get user (similar to permission check)
            if allow_api_key:
                try:
                    current_user = await get_current_user_api_key(
                        kwargs.get('request'),
                        kwargs.get('db')
                    )
                except HTTPException:
                    current_user = await get_current_user_jwt(
                        kwargs.get('credentials'),
                        kwargs.get('db')
                    )
            else:
                current_user = await get_current_user_jwt(
                    kwargs.get('credentials'),
                    kwargs.get('db')
                )

            # Check role
            user_permissions = current_user.get("permissions", [])

            if role == "admin" and "admin" not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Administrator role required"
                )
            elif role == "org_admin" and not any(
                perm in user_permissions for perm in ["admin", "org_admin"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Organization administrator role required"
                )

            kwargs['current_user'] = current_user
            return await func(*args, **kwargs)

        return wrapper
    return decorator


def require_org_access(target_org_field: str = None):
    """
    Decorator for organization-based access control

    Args:
        target_org_field: Field name in request data containing target org ID
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                # Try to get user
                try:
                    current_user = await get_current_user_api_key(
                        kwargs.get('request'),
                        kwargs.get('db')
                    )
                except HTTPException:
                    current_user = await get_current_user_jwt(
                        kwargs.get('credentials'),
                        kwargs.get('db')
                    )

            # Get target organization ID
            target_org_id = None
            if target_org_field:
                # From request data
                request_data = kwargs.get(target_org_field)
                if hasattr(request_data, 'org_id'):
                    target_org_id = request_data.org_id
            else:
                # From path parameter
                target_org_id = kwargs.get('org_id')

            if target_org_id:
                db = kwargs.get('db')
                auth_service = MispAuthService(db)

                if not auth_service.check_organization_access(
                    current_user.get("org_id"),
                    target_org_id,
                    current_user.get("permissions", [])
                ):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Access denied to target organization"
                    )

            kwargs['current_user'] = current_user
            return await func(*args, **kwargs)

        return wrapper
    return decorator


def create_permission_dependency(permission: str):
    """
    Create FastAPI dependency for permission checking

    Args:
        permission: Required permission string
    """
    async def permission_dependency(
        current_user: Dict[str, Any] = Depends(get_current_user_jwt),
        db: Session = Depends(get_db)
    ) -> Dict[str, Any]:
        auth_service = MispAuthService(db)

        if not auth_service.check_permission(
            current_user.get("permissions", []),
            permission
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Insufficient permissions: {permission} required"
            )

        return current_user

    return permission_dependency


def create_role_dependency(role: str):
    """
    Create FastAPI dependency for role checking

    Args:
        role: Required role name
    """
    async def role_dependency(
        current_user: Dict[str, Any] = Depends(get_current_user_jwt),
        db: Session = Depends(get_db)
    ) -> Dict[str, Any]:
        user_permissions = current_user.get("permissions", [])

        if role == "admin" and "admin" not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Administrator role required"
            )
        elif role == "org_admin" and not any(
            perm in user_permissions for perm in ["admin", "org_admin"]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Organization administrator role required"
            )

        return current_user

    return role_dependency


# Common permission dependencies
require_admin = create_role_dependency("admin")
require_org_admin = create_role_dependency("org_admin")

require_events_read = create_permission_dependency("events:read")
require_events_create = create_permission_dependency("events:create")
require_events_update = create_permission_dependency("events:update")
require_events_delete = create_permission_dependency("events:delete")
require_events_publish = create_permission_dependency("events:publish")

require_attributes_create = create_permission_dependency("attributes:create")
require_attributes_update = create_permission_dependency("attributes:update")

require_tags_create = create_permission_dependency("tags:create")
require_tags_attach = create_permission_dependency("tags:attach")

require_sync_read = create_permission_dependency("sync:read")
require_sync_write = create_permission_dependency("sync:write")
