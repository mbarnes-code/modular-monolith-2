"""
Base entity models for the MTG Domain.

Provides data models for all 4 MTG tools with unified schema
and executive function accommodation tracking.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MTGToolStatus(str, Enum):
    """Status enumeration for MTG tools."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    UPDATING = "updating"
    ERROR = "error"


class MTGTool(Base):
    """Base model for MTG tool configuration."""

    __tablename__ = "mtg_tools"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tool_name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(String(20), default=MTGToolStatus.ACTIVE)
    config_data = Column(JSON, default={})
    last_card_update = Column(DateTime, default=datetime.utcnow)
    response_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class MTGDeck(Base):
    """MTG deck storage and analysis."""

    __tablename__ = "mtg_decks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(String(100), nullable=False)
    deck_name = Column(String(255), nullable=False)
    format = Column(String(50), nullable=False)  # commander, standard, etc.
    commander = Column(String(255), nullable=True)
    deck_list = Column(JSON, nullable=False)  # List of cards with quantities
    analysis_data = Column(JSON, default={})
    tags = Column(JSON, default=[])
    is_public = Column(String(10), default="private")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


class MTGCard(Base):
    """MTG card database."""

    __tablename__ = "mtg_cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    card_name = Column(String(255), nullable=False)
    mana_cost = Column(String(100))
    cmc = Column(Integer, default=0)
    type_line = Column(String(255))
    oracle_text = Column(Text)
    power = Column(String(10))
    toughness = Column(String(10))
    colors = Column(JSON, default=[])
    color_identity = Column(JSON, default=[])
    set_code = Column(String(10))
    rarity = Column(String(20))
    card_data = Column(JSON, default={})  # Full card data from APIs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# Pydantic models for API serialization
class MTGToolModel(BaseModel):
    """Pydantic model for MTG tools."""

    id: Optional[str] = None
    tool_name: str
    display_name: str
    description: Optional[str] = None
    status: MTGToolStatus = MTGToolStatus.ACTIVE
    config_data: dict[str, Any] = Field(default_factory=dict)
    last_card_update: Optional[datetime] = None
    response_time_ms: int = 0
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MTGDeckModel(BaseModel):
    """Pydantic model for MTG decks."""

    id: Optional[str] = None
    user_id: str
    deck_name: str
    format: str
    commander: Optional[str] = None
    deck_list: list[dict[str, Any]]
    analysis_data: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)
    is_public: str = "private"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MTGCardModel(BaseModel):
    """Pydantic model for MTG cards."""

    id: Optional[str] = None
    card_name: str
    mana_cost: Optional[str] = None
    cmc: int = 0
    type_line: Optional[str] = None
    oracle_text: Optional[str] = None
    power: Optional[str] = None
    toughness: Optional[str] = None
    colors: list[str] = Field(default_factory=list)
    color_identity: list[str] = Field(default_factory=list)
    set_code: Optional[str] = None
    rarity: Optional[str] = None
    card_data: dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Tool-specific models for the 4 MTG tools
class CommanderSpellbookComboModel(BaseModel):
    """Commander Spellbook infinite combo model."""

    combo_id: str
    cards: list[str] = Field(min_length=2)
    colors: list[str] = Field(default_factory=list)
    prerequisites: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    results: list[str] = Field(default_factory=list)
    popularity: int = 0
    created_at: datetime

    class Config:
        from_attributes = True


class MTGCommanderMapDeckModel(BaseModel):
    """MTG Commander Map deck visualization model."""

    map_id: str
    deck_id: str
    commander: str
    mana_curve: dict[str, int] = Field(default_factory=dict)
    color_distribution: dict[str, int] = Field(default_factory=dict)
    type_distribution: dict[str, int] = Field(default_factory=dict)
    synergy_groups: list[dict[str, Any]] = Field(default_factory=list)
    power_level: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class MTGScriptingToolkitScriptModel(BaseModel):
    """MTG Scripting Toolkit automation script model."""

    script_id: str
    script_name: str
    script_type: str  # deck_builder, card_finder, price_tracker, etc.
    script_content: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    last_run: Optional[datetime] = None
    run_count: int = 0
    status: str = "ready"
    created_at: datetime

    class Config:
        from_attributes = True


class CardAnalysisReportModel(BaseModel):
    """Card Analysis comprehensive report model."""

    analysis_id: str
    target_cards: list[str] = Field(min_length=1)
    analysis_type: str  # synergy, combo, meta, price
    results: dict[str, Any] = Field(default_factory=dict)
    recommendations: list[str] = Field(default_factory=list)
    confidence_score: float = 0.0
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Executive function accommodation models
class MTGUserPreferences(BaseModel):
    """MTG domain user preferences for executive function support."""

    user_id: str
    favorite_formats: list[str] = Field(default_factory=list)
    preferred_colors: list[str] = Field(default_factory=list)
    deck_organization: dict[str, Any] = Field(default_factory=dict)
    analysis_preferences: dict[str, Any] = Field(default_factory=dict)
    notification_settings: dict[str, bool] = Field(default_factory=dict)
    adhd_accommodations: dict[str, Any] = Field(default_factory=dict)
    autism_accommodations: dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


# Domain performance tracking
class MTGPerformanceMetric(BaseModel):
    """Performance metrics for MTG domain constitutional compliance."""

    tool_name: str
    operation: str
    response_time_ms: int
    target_time_ms: int = 3000  # <3s constitutional requirement
    compliant: bool
    timestamp: datetime
    user_id: Optional[str] = None
    deck_size: Optional[int] = None  # Context for performance analysis

    class Config:
        from_attributes = True
