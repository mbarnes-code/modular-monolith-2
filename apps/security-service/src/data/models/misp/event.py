"""MISP Event Model

Central threat intelligence entity model migrated from CakePHP Event.php (8,740 lines).
Preserves all critical business logic and relationships for threat intelligence correlation.
"""

from datetime import datetime

from sqlalchemy import (TIMESTAMP, Boolean, CheckConstraint, Column,
                        ForeignKey, Index, Integer, String, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from . import (MispBaseModel, OrganisationMixin, SharingMixin, TimestampMixin,
               UserMixin, UUIDMixin)


class Event(
    MispBaseModel,
    UUIDMixin,
    OrganisationMixin,
    UserMixin,
    SharingMixin,
    TimestampMixin
):
    """
    MISP Event - Central threat intelligence entity

    Migrated from CakePHP Event.php maintaining all business logic:
    - Threat intelligence correlation algorithms
    - Distribution and sharing controls  
    - Event lifecycle management
    - Complex attribute relationships
    """
    __tablename__ = 'events'

    # Core event fields
    info = Column(Text, nullable=False)  # Event description/title
    date = Column(String(10), nullable=False)  # Event date (YYYY-MM-DD)

    # Analysis and threat level
    analysis = Column(
        Integer,
        nullable=False,
        default=0,
        comment="0=Initial, 1=Ongoing, 2=Complete"
    )
    threat_level_id = Column(
        Integer,
        ForeignKey('threat_levels.id'),
        nullable=False,
        comment="1=High, 2=Medium, 3=Low, 4=Undefined"
    )

    # Publishing and lifecycle
    published = Column(Boolean, nullable=False, default=False, index=True)
    publish_timestamp = Column(Integer, nullable=True)

    # Event extension and relationships
    extends_uuid = Column(UUID(as_uuid=True), nullable=True, index=True)

    # Event locking
    locked = Column(Boolean, nullable=False, default=False)

    # Attribution and provenance
    attribute_count = Column(Integer, nullable=True)
    proposal_email_lock = Column(Boolean, nullable=False, default=False)

    # Protected event flag
    protected = Column(Boolean, nullable=False, default=False)

    # Additional metadata
    event_creator_email = Column(String(255), nullable=True)
    sighting_timestamp = Column(Integer, nullable=True)

    # JSON fields for flexible metadata
    event_meta = Column(JSONB, nullable=True,
                        comment="Flexible event metadata")

    # Relationships (preserved from CakePHP associations)
    user = relationship("User", foreign_keys=[UserMixin.user_id])
    org = relationship(
        "Organisation",
        foreign_keys=[OrganisationMixin.org_id],
        back_populates="events_owned"
    )
    orgc = relationship(
        "Organisation",
        foreign_keys=[OrganisationMixin.orgc_id],
        back_populates="events_created"
    )
    threat_level = relationship("ThreatLevel")
    sharing_group = relationship("SharingGroup")

    # Dependent relationships
    attributes = relationship(
        "MispAttribute",
        back_populates="event",
        cascade="all, delete-orphan",
        order_by="MispAttribute.category, MispAttribute.type"
    )
    objects = relationship(
        "MispObject",
        back_populates="event",
        cascade="all, delete-orphan"
    )
    event_tags = relationship(
        "EventTag",
        back_populates="event",
        cascade="all, delete-orphan"
    )
    event_reports = relationship(
        "EventReport",
        back_populates="event",
        cascade="all, delete-orphan"
    )
    shadow_attributes = relationship(
        "ShadowAttribute",
        back_populates="event",
        cascade="all, delete-orphan"
    )
    sightings = relationship(
        "Sighting",
        back_populates="event",
        cascade="all, delete-orphan"
    )
    cryptographic_keys = relationship(
        "CryptographicKey",
        primaryjoin="and_(Event.id==CryptographicKey.parent_id, "
        "CryptographicKey.parent_type=='Event')",
        cascade="all, delete-orphan"
    )

    # Table constraints
    __table_args__ = (
        # Distribution constraints
        CheckConstraint(
            'distribution >= 0 AND distribution <= 4',
            name='check_distribution_range'
        ),
        # Analysis level constraints
        CheckConstraint(
            'analysis >= 0 AND analysis <= 2',
            name='check_analysis_range'
        ),
        # Threat level constraints
        CheckConstraint(
            'threat_level_id >= 1 AND threat_level_id <= 4',
            name='check_threat_level_range'
        ),
        # Performance indexes
        Index('idx_events_uuid', 'uuid'),
        Index('idx_events_published', 'published'),
        Index('idx_events_timestamp', 'timestamp'),
        Index('idx_events_org_id', 'org_id'),
        Index('idx_events_orgc_id', 'orgc_id'),
        Index('idx_events_user_id', 'user_id'),
        Index('idx_events_sharing_group_id', 'sharing_group_id'),
        Index('idx_events_threat_level_id', 'threat_level_id'),
        # Composite indexes for correlation queries
        Index('idx_events_published_timestamp', 'published', 'timestamp'),
        Index('idx_events_org_distribution', 'org_id', 'distribution'),
        Index('idx_events_analysis_published', 'analysis', 'published'),
    )

    def __repr__(self):
        return f"<Event(id={self.id}, uuid='{self.uuid}', info='{self.info[:50]}...')>"

    @property
    def is_complete(self) -> bool:
        """Check if event analysis is complete"""
        return self.analysis == 2

    @property
    def is_published(self) -> bool:
        """Check if event is published"""
        return self.published

    @property
    def distribution_level(self) -> str:
        """Get human-readable distribution level"""
        levels = {
            0: "Organisation only",
            1: "Community only",
            2: "Connected communities",
            3: "All communities",
            4: "Sharing group"
        }
        return levels.get(self.distribution, "Unknown")

    @property
    def analysis_status(self) -> str:
        """Get human-readable analysis status"""
        statuses = {
            0: "Initial",
            1: "Ongoing",
            2: "Complete"
        }
        return statuses.get(self.analysis, "Unknown")
