"""MISP Object Model

Structured threat intelligence objects model migrated from CakePHP MispObject.php.
Handles complex structured data with templates and relationships.
"""

from sqlalchemy import (Boolean, Column, ForeignKey, Index, Integer, String,
                        Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from . import (DeletedMixin, MispBaseModel, OrganisationMixin, SharingMixin,
               TimestampMixin, UUIDMixin)


class MispObject(
    MispBaseModel,
    UUIDMixin,
    OrganisationMixin,
    SharingMixin,
    TimestampMixin,
    DeletedMixin
):
    """
    MISP Object - Structured threat intelligence objects

    Migrated from CakePHP MispObject.php maintaining:
    - Object template system and validation
    - Complex attribute relationships
    - Object-to-object references
    - Template-based structure enforcement
    """
    __tablename__ = 'objects'

    # Core object fields
    name = Column(String(255), nullable=False, index=True)
    meta_category = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    template_uuid = Column(UUID(as_uuid=True), nullable=False, index=True)
    template_version = Column(Integer, nullable=False, index=True)

    # Event relationship
    event_id = Column(Integer, ForeignKey('events.id'),
                      nullable=False, index=True)

    # Object metadata
    comment = Column(Text, nullable=True)

    # First/last seen tracking
    first_seen = Column(String(19), nullable=True)
    last_seen = Column(String(19), nullable=True)

    # JSON fields for flexible metadata
    object_meta = Column(JSONB, nullable=True)

    # Relationships
    event = relationship("Event", back_populates="objects")

    # Object attributes
    attributes = relationship(
        "MispAttribute",
        back_populates="misp_object",
        cascade="all, delete-orphan",
        order_by="MispAttribute.object_relation"
    )

    # Object references (outgoing)
    object_references_source = relationship(
        "ObjectReference",
        foreign_keys="ObjectReference.source_uuid",
        back_populates="source_object",
        cascade="all, delete-orphan"
    )

    # Object references (incoming)
    object_references_target = relationship(
        "ObjectReference",
        foreign_keys="ObjectReference.referenced_uuid",
        back_populates="target_object"
    )

    # Table constraints and indexes
    __table_args__ = (
        # Performance indexes
        Index('idx_objects_name', 'name'),
        Index('idx_objects_meta_category', 'meta_category'),
        Index('idx_objects_template_uuid', 'template_uuid'),
        Index('idx_objects_template_version', 'template_version'),
        Index('idx_objects_event_id', 'event_id'),
        Index('idx_objects_uuid', 'uuid'),
        Index('idx_objects_timestamp', 'timestamp'),
        Index('idx_objects_deleted', 'deleted'),

        # Composite indexes
        Index('idx_objects_event_name', 'event_id', 'name'),
        Index('idx_objects_template_version',
              'template_uuid', 'template_version'),
    )

    def __repr__(self):
        return (f"<MispObject(id={self.id}, "
                f"name='{self.name}', "
                f"meta_category='{self.meta_category}')>")

    @property
    def attribute_count(self) -> int:
        """Get number of attributes in this object"""
        return len(self.attributes) if self.attributes else 0

    @property
    def is_valid_template(self) -> bool:
        """Check if object follows valid template (requires validation)"""
        # This would need template validation logic
        return True  # Placeholder

    def get_attribute_by_relation(self, relation: str):
        """Get attribute by object relation"""
        if not self.attributes:
            return None

        for attr in self.attributes:
            if attr.object_relation == relation:
                return attr
        return None

    def get_all_references(self):
        """Get all object references (both source and target)"""
        references = []
        if self.object_references_source:
            references.extend(self.object_references_source)
        if self.object_references_target:
            references.extend(self.object_references_target)
        return references


class ObjectReference(MispBaseModel, UUIDMixin, TimestampMixin, DeletedMixin):
    """MISP ObjectReference - References between objects"""
    __tablename__ = 'object_references'

    # Reference details
    source_uuid = Column(UUID(as_uuid=True), ForeignKey(
        'objects.uuid'), nullable=False, index=True)
    referenced_uuid = Column(UUID(as_uuid=True), ForeignKey(
        'objects.uuid'), nullable=False, index=True)
    relationship_type = Column(String(255), nullable=False, index=True)
    comment = Column(Text, nullable=True)

    # Event context
    event_id = Column(Integer, ForeignKey('events.id'),
                      nullable=False, index=True)

    # Relationships
    source_object = relationship(
        "MispObject",
        foreign_keys=[source_uuid],
        back_populates="object_references_source"
    )
    target_object = relationship(
        "MispObject",
        foreign_keys=[referenced_uuid],
        back_populates="object_references_target"
    )
    event = relationship("Event")

    __table_args__ = (
        Index('idx_object_references_source_uuid', 'source_uuid'),
        Index('idx_object_references_referenced_uuid', 'referenced_uuid'),
        Index('idx_object_references_relationship_type', 'relationship_type'),
        Index('idx_object_references_event_id', 'event_id'),
    )

    def __repr__(self):
        return (f"<ObjectReference(id={self.id}, "
                f"relationship_type='{self.relationship_type}')>")
