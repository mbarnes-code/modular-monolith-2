"""
MISP Users Schema Definitions

Pydantic models for MISP user API request/response validation.
Migrated from MISP/app/Model/User.php and related schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base user fields"""
    email: EmailStr = Field(..., description="User email address")
    org_id: int = Field(..., description="Organization ID")
    role_id: int = Field(..., description="Role ID")
    disabled: bool = Field(default=False, description="User disabled flag")
    autoalert: bool = Field(
        default=False, description="Auto-alert subscription"
    )
    contactalert: bool = Field(
        default=False, description="Contact alert subscription"
    )
    gpgkey: Optional[str] = Field(None, description="GPG public key")
    nids_sid: Optional[int] = Field(None, description="NIDS SID")
    server_id: int = Field(default=0, description="Server ID")
    newsread: Optional[datetime] = Field(
        None, description="Last news read timestamp"
    )


class UserCreate(UserBase):
    """Create new user"""
    password: str = Field(..., min_length=6, description="User password")

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserUpdate(BaseModel):
    """Update existing user"""
    email: Optional[EmailStr] = None
    org_id: Optional[int] = None
    role_id: Optional[int] = None
    disabled: Optional[bool] = None
    autoalert: Optional[bool] = None
    contactalert: Optional[bool] = None
    gpgkey: Optional[str] = None
    nids_sid: Optional[int] = None
    server_id: Optional[int] = None


class PasswordChange(BaseModel):
    """Password change request"""
    current_password: Optional[str] = Field(
        None, description="Current password (required for self-change)"
    )
    new_password: str = Field(
        ..., min_length=6, description="New password"
    )
    confirm_password: str = Field(
        ..., description="Confirm new password"
    )

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Passwords do not match')
        return v

    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return v


class UserResponse(UserBase):
    """User response with metadata"""
    id: int
    authkey: Optional[str] = Field(
        None, description="API authentication key"
    )
    invited_by: Optional[int] = Field(
        None, description="User ID who invited this user"
    )
    invited_on: Optional[datetime] = Field(
        None, description="Invitation timestamp"
    )
    created: datetime
    modified: Optional[datetime] = None
    last_login: Optional[datetime] = Field(
        None, description="Last login timestamp"
    )
    current_login: Optional[datetime] = Field(
        None, description="Current login timestamp"
    )
    last_api_access: Optional[datetime] = Field(
        None, description="Last API access timestamp"
    )

    # Related data
    organisation: Optional[dict] = Field(
        None, description="Organization details"
    )
    role: Optional[dict] = Field(None, description="Role details")

    # Statistics
    event_count: Optional[int] = Field(
        None, description="Number of events created by user"
    )
    attribute_count: Optional[int] = Field(
        None, description="Number of attributes created by user"
    )

    class Config:
        from_attributes = True

    @validator('authkey', pre=True)
    def mask_authkey(cls, v):
        """Mask auth key for security (show only first/last 4 chars)"""
        if v and len(v) > 8:
            return f"{v[:4]}...{v[-4:]}"
        return v


class UserListResponse(BaseModel):
    """Paginated user list response"""
    users: List[UserResponse]
    total: int
    page: int
    limit: int
    has_next: bool = False
    has_prev: bool = False

    @validator('has_next', pre=True, always=True)
    def set_has_next(cls, v, values):
        total = values.get('total', 0)
        page = values.get('page', 1)
        limit = values.get('limit', 60)
        return (page * limit) < total

    @validator('has_prev', pre=True, always=True)
    def set_has_prev(cls, v, values):
        page = values.get('page', 1)
        return page > 1


class UserSelfResponse(BaseModel):
    """Extended user response for self-queries (includes sensitive data)"""
    id: int
    email: EmailStr
    org_id: int
    role_id: int
    disabled: bool
    authkey: str = Field(..., description="Full API authentication key")
    created: datetime
    modified: Optional[datetime] = None
    last_login: Optional[datetime] = None

    # Related data
    organisation: Optional[dict] = None
    role: Optional[dict] = None

    class Config:
        from_attributes = True
