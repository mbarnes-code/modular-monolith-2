"""
MISP Attributes Schema Definitions

Pydantic models for MISP attribute API request/response validation.
Migrated from MISP/app/Model/Attribute.php and related schemas.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class AttributeBase(BaseModel):
    """Base attribute fields"""
    type: str = Field(
        ..., description="Attribute type (e.g., ip-src, domain, hash)"
    )
    value: str = Field(..., description="The actual value of the attribute")
    category: str = Field(..., description="Attribute category")
    comment: Optional[str] = Field(None, description="Optional comment")
    to_ids: bool = Field(default=False, description="IDS flag")
    distribution: int = Field(
        default=5, description="Distribution level (0-5)"
    )
    sharing_group_id: Optional[int] = Field(
        None, description="Sharing group ID if distribution=4"
    )


class AttributeCreate(AttributeBase):
    """Create new attribute"""
    event_id: int = Field(..., description="Event ID to add attribute to")

    @validator('distribution')
    def validate_distribution(cls, v):
        if v not in range(6):  # 0-5
            raise ValueError("Distribution must be between 0 and 5")
        return v


class AttributeUpdate(BaseModel):
    """Update existing attribute"""
    type: Optional[str] = None
    value: Optional[str] = None
    category: Optional[str] = None
    comment: Optional[str] = None
    to_ids: Optional[bool] = None
    distribution: Optional[int] = None
    sharing_group_id: Optional[int] = None

    @validator('distribution')
    def validate_distribution(cls, v):
        if v is not None and v not in range(6):
            raise ValueError("Distribution must be between 0 and 5")
        return v


class AttributeResponse(AttributeBase):
    """Attribute response with metadata"""
    id: int
    event_id: int
    uuid: str
    timestamp: datetime
    deleted: bool = False
    disable_correlation: bool = False
    object_id: Optional[int] = None
    object_relation: Optional[str] = None
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None

    # Related data
    event_uuid: Optional[str] = None
    event_info: Optional[str] = None
    event_date: Optional[str] = None

    class Config:
        from_attributes = True


class AttributeSearch(BaseModel):
    """Advanced attribute search criteria"""
    value: Optional[str] = Field(None, description="Search by value")
    type: Optional[List[str]] = Field(None, description="Filter by types")
    category: Optional[List[str]] = Field(
        None, description="Filter by categories")
    org: Optional[str] = Field(None, description="Filter by organization")
    eventid: Optional[List[int]] = Field(
        None, description="Filter by event IDs")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    timestamp: Optional[str] = Field(None, description="Timestamp filter")
    publish_timestamp: Optional[str] = Field(
        None, description="Publish timestamp filter")
    last: Optional[str] = Field(
        None, description="Time period (e.g., '7d', '1m')")
    enforceWarninglist: Optional[bool] = Field(
        True, description="Apply warning lists")
    to_ids: Optional[bool] = Field(None, description="Filter by IDS flag")
    deleted: Optional[bool] = Field(
        False, description="Include deleted attributes")
    includeEventUuid: Optional[bool] = Field(
        True, description="Include event UUID")
    includeEventTags: Optional[bool] = Field(
        False, description="Include event tags")
    includeProposals: Optional[bool] = Field(
        False, description="Include proposals")
    includeDecayScore: Optional[bool] = Field(
        False, description="Include decay scores")
    decayingModel: Optional[List[int]] = Field(
        None, description="Decaying model IDs")
    excludeDecayed: Optional[bool] = Field(
        False, description="Exclude decayed attributes")
    includeFullModel: Optional[bool] = Field(
        False, description="Include full model data")
    score: Optional[float] = Field(None, description="Minimum decay score")
    limit: Optional[int] = Field(
        60, ge=1, le=9999, description="Results limit")
    page: Optional[int] = Field(1, ge=1, description="Page number")
    returnFormat: Optional[str] = Field("json", description="Return format")


class AttributeListResponse(BaseModel):
    """Paginated attribute list response"""
    attributes: List[AttributeResponse]
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
