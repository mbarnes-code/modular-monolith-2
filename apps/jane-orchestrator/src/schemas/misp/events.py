"""
MISP Event Schemas

Pydantic schemas for MISP event API endpoints.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class EventBase(BaseModel):
    """Base event model with common fields"""
    info: str = Field(description="Event description")
    analysis: int = Field(
        default=0, description="Analysis status"
    )
    threat_level_id: int = Field(
        default=4, description="Threat level"
    )
    published: bool = Field(default=False, description="Publication status")
    distribution: int = Field(default=0, description="Distribution level")


class EventCreate(EventBase):
    """Schema for creating new events"""


class EventUpdate(BaseModel):
    """Schema for updating events"""
    info: Optional[str] = None
    analysis: Optional[int] = None
    threat_level_id: Optional[int] = None
    published: Optional[bool] = None
    distribution: Optional[int] = None


class EventResponse(EventBase):
    """Schema for event responses"""
    id: int
    uuid: str
    org_id: int
    user_id: int
    orgc_id: int
    timestamp: int
    date: datetime
    publish_timestamp: int = 0
    sharing_group_id: Optional[int] = None
    attribute_count: int = 0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EventSearch(BaseModel):
    """Schema for event search requests"""
    value: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    org: Optional[str] = None
    tags: Optional[List[str]] = None
    from_date: Optional[str] = Field(None, alias="from")
    to_date: Optional[str] = Field(None, alias="to")
    published: Optional[bool] = None
    limit: Optional[int] = Field(60, le=9999)
    page: Optional[int] = Field(1, ge=1)


class EventListResponse(BaseModel):
    """Schema for event list responses"""
    events: List[EventResponse]
    total: int
    page: int
    limit: int
