"""
MISP Organizations Schema Definitions

Pydantic models for MISP organization API request/response validation.
Migrated from MISP/app/Model/Organisation.php and related schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class OrganizationBase(BaseModel):
    """Base organization fields"""
    name: str = Field(..., description="Organization name")
    description: Optional[str] = Field(
        None, description="Organization description"
    )
    type: Optional[str] = Field(None, description="Organization type")
    nationality: Optional[str] = Field(None, description="Nationality")
    sector: Optional[str] = Field(None, description="Industry sector")
    created_by: Optional[int] = Field(
        None, description="User ID who created the organization"
    )
    uuid: Optional[str] = Field(None, description="Organization UUID")
    contacts: Optional[str] = Field(None, description="Contact information")
    local: bool = Field(default=True, description="Local organization flag")
    restricted_to_domain: Optional[str] = Field(
        None, description="Domain restriction"
    )


class OrganizationCreate(OrganizationBase):
    """Create new organization"""

    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("Organization name cannot be empty")
        return v.strip()


class OrganizationUpdate(BaseModel):
    """Update existing organization"""
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    nationality: Optional[str] = None
    sector: Optional[str] = None
    contacts: Optional[str] = None
    local: Optional[bool] = None
    restricted_to_domain: Optional[str] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError("Organization name cannot be empty")
        return v.strip() if v else v


class OrganizationResponse(OrganizationBase):
    """Organization response with metadata"""
    id: int
    date_created: datetime
    date_modified: Optional[datetime] = None
    created_by: Optional[int] = None

    # Statistics
    user_count: Optional[int] = Field(
        None, description="Number of users in organization"
    )
    event_count: Optional[int] = Field(
        None, description="Number of events by organization"
    )
    attribute_count: Optional[int] = Field(
        None, description="Number of attributes by organization"
    )

    class Config:
        from_attributes = True


class OrganizationListResponse(BaseModel):
    """Paginated organization list response"""
    organisations: List[OrganizationResponse]
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
