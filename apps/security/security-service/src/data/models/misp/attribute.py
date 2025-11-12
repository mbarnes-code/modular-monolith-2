"""MISP Attribute Model

Event attributes and indicators model migrated from CakePHP MispAttribute.php.
Preserves threat intelligence indicators with full categorization and correlation.
"""

from sqlalchemy import (Boolean, CheckConstraint, Column, ForeignKey, Index,
                        Integer, String, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from . import (DeletedMixin, MispBaseModel, OrganisationMixin, SharingMixin,
               TimestampMixin, UserMixin, UUIDMixin)


class MispAttribute(
    MispBaseModel,
    UUIDMixin,
    OrganisationMixin,
    SharingMixin,
    TimestampMixin,
    DeletedMixin
):
    """
    MISP Attribute - Threat intelligence indicators and observables

    Migrated from CakePHP MispAttribute.php maintaining:
    - Full attribute categorization system
    - Type validation and correlation logic
    - IDS signature and detection capabilities
    - Complex validation and normalization rules
    """
    __tablename__ = 'attributes'

    # Core attribute fields
    event_id = Column(
        Integer,
        ForeignKey('events.id'),
        nullable=False,
        index=True
    )
    object_id = Column(
        Integer,
        ForeignKey('objects.id'),
        nullable=False,
        default=0
    )
    object_relation = Column(String(255), nullable=True)

    # Attribute classification
    category = Column(String(255), nullable=False, index=True)
    type = Column(String(100), nullable=False, index=True)
    value = Column(Text, nullable=False)
    value1 = Column(Text, nullable=True)  # For composite attributes
    value2 = Column(Text, nullable=True)  # For composite attributes

    # Attribution and context
    to_ids = Column(Boolean, nullable=False, default=True)
    comment = Column(Text, nullable=True)

    # Data source and provenance
    first_seen = Column(String(19), nullable=True)  # ISO datetime string
    last_seen = Column(String(19), nullable=True)   # ISO datetime string

    # Disable correlation flag
    disable_correlation = Column(Boolean, nullable=False, default=False)

    # Metadata and additional data
    data = Column(Text, nullable=True)  # Base64 encoded binary data

    # JSON fields for flexible metadata
    attribute_meta = Column(JSONB, nullable=True)

    # Relationships
    event = relationship("Event", back_populates="attributes")
    misp_object = relationship("MispObject", back_populates="attributes")
    misp_object = relationship("MispObject", back_populates="attributes")

    # Tags relationship
    attribute_tags = relationship(
        "AttributeTag",
        back_populates="attribute",
        cascade="all, delete-orphan"
    )

    # Sightings relationship
    sightings = relationship(
        "Sighting",
        back_populates="attribute",
        cascade="all, delete-orphan"
    )

    # Table constraints and indexes
    __table_args__ = (
        # Distribution constraints
        CheckConstraint(
            'distribution >= 0 AND distribution <= 4',
            name='check_attribute_distribution_range'
        ),
        # Performance indexes
        Index('idx_attributes_event_id', 'event_id'),
        Index('idx_attributes_object_id', 'object_id'),
        Index('idx_attributes_uuid', 'uuid'),
        Index('idx_attributes_category', 'category'),
        Index('idx_attributes_type', 'type'),
        Index('idx_attributes_to_ids', 'to_ids'),
        Index('idx_attributes_timestamp', 'timestamp'),
        Index('idx_attributes_deleted', 'deleted'),
        Index('idx_attributes_disable_correlation', 'disable_correlation'),

        # Composite indexes for correlation queries
        Index('idx_attributes_correlation', 'category', 'type', 'value'),
        Index('idx_attributes_event_category', 'event_id', 'category'),
        Index('idx_attributes_event_type', 'event_id', 'type'),
        Index('idx_attributes_ids_published', 'to_ids', 'deleted'),

        # Value hash indexes for performance
        Index('idx_attributes_value_hash', 'value', postgresql_using='hash'),
    )

    def __repr__(self):
        return (f"<MispAttribute(id={self.id}, "
                f"category='{self.category}', "
                f"type='{self.type}', "
                f"value='{self.value[:50]}...')>")

    @property
    def is_ids_signature(self) -> bool:
        """Check if attribute is marked for IDS signature"""
        return self.to_ids and not self.deleted

    @property
    def can_correlate(self) -> bool:
        """Check if attribute can be used for correlation"""
        return not self.disable_correlation and not self.deleted

    @property
    def is_composite(self) -> bool:
        """Check if attribute has composite values"""
        return self.value1 is not None or self.value2 is not None

    @property
    def full_value(self) -> str:
        """Get full attribute value including composite parts"""
        if not self.is_composite:
            return self.value

        parts = [self.value]
        if self.value1:
            parts.append(self.value1)
        if self.value2:
            parts.append(self.value2)
        return '|'.join(parts)

    def get_tags(self):
        """Get all tags associated with this attribute"""
        return [tag.tag for tag in self.attribute_tags if not tag.local]

    def get_local_tags(self):
        """Get local tags associated with this attribute"""
        return [tag.tag for tag in self.attribute_tags if tag.local]
