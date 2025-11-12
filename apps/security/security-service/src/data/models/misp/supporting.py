"""MISP Supporting Models

Additional critical models for MISP threat intelligence platform.
Includes ThreatLevel, Role, Tag, and other supporting entities.
"""

from sqlalchemy import (Boolean, Column, ForeignKey, Index, Integer, String,
                        Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from . import MispBaseModel, TimestampMixin, UUIDMixin


class ThreatLevel(MispBaseModel):
    """MISP Threat Level - Risk classification system"""
    __tablename__ = 'threat_levels'

    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    form_description = Column(Text, nullable=True)

    # Relationships
    events = relationship("Event", back_populates="threat_level")

    def __repr__(self):
        return f"<ThreatLevel(id={self.id}, name='{self.name}')>"


class Role(MispBaseModel):
    """MISP Role - User role and permission management"""
    __tablename__ = 'roles'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Permission flags
    perm_add = Column(Boolean, nullable=False, default=False)
    perm_modify = Column(Boolean, nullable=False, default=False)
    perm_modify_org = Column(Boolean, nullable=False, default=False)
    perm_publish = Column(Boolean, nullable=False, default=False)
    perm_delegate = Column(Boolean, nullable=False, default=False)
    perm_sync = Column(Boolean, nullable=False, default=False)
    perm_admin = Column(Boolean, nullable=False, default=False)
    perm_audit = Column(Boolean, nullable=False, default=False)
    perm_full = Column(Boolean, nullable=False, default=False)
    perm_auth = Column(Boolean, nullable=False, default=False)
    perm_regexp_access = Column(Boolean, nullable=False, default=False)
    perm_tagger = Column(Boolean, nullable=False, default=False)
    perm_site_admin = Column(Boolean, nullable=False, default=False)
    perm_template = Column(Boolean, nullable=False, default=False)
    perm_sharing_group = Column(Boolean, nullable=False, default=False)
    perm_tag_editor = Column(Boolean, nullable=False, default=False)
    perm_sighting = Column(Boolean, nullable=False, default=False)
    perm_object_template = Column(Boolean, nullable=False, default=False)

    # Additional permission controls
    default_role = Column(Boolean, nullable=False, default=False)
    memory_limit = Column(String(255), nullable=True)
    max_execution_time = Column(String(255), nullable=True)
    restricted_to_site_admin = Column(Boolean, nullable=False, default=False)
    enforce_rate_limit = Column(Boolean, nullable=False, default=False)
    rate_limit_count = Column(Integer, nullable=False, default=0)

    # Relationships
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"


class Tag(MispBaseModel, UUIDMixin, TimestampMixin):
    """MISP Tag - Classification and labeling system"""
    __tablename__ = 'tags'

    name = Column(String(255), nullable=False, unique=True, index=True)
    colour = Column(String(7), nullable=False, default='#ffffff')
    exportable = Column(Boolean, nullable=False, default=True)
    org_id = Column(Integer, ForeignKey('organisations.id'), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    hide_tag = Column(Boolean, nullable=False, default=False)
    numerical_value = Column(Integer, nullable=True)
    is_galaxy = Column(Boolean, nullable=False, default=False)
    is_custom_galaxy = Column(Boolean, nullable=False, default=False)
    local_only = Column(Boolean, nullable=False, default=False)

    # Relationships
    organisation = relationship("Organisation")
    user = relationship("User")

    # Tag associations
    event_tags = relationship("EventTag", back_populates="tag")
    attribute_tags = relationship("AttributeTag", back_populates="tag")

    __table_args__ = (
        Index('idx_tags_name', 'name'),
        Index('idx_tags_org_id', 'org_id'),
        Index('idx_tags_exportable', 'exportable'),
        Index('idx_tags_numerical_value', 'numerical_value'),
    )

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}', colour='{self.colour}')>"


class EventTag(MispBaseModel, TimestampMixin):
    """MISP EventTag - Junction table for Event-Tag relationships"""
    __tablename__ = 'event_tags'

    event_id = Column(Integer, ForeignKey('events.id'),
                      nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False, index=True)
    local = Column(Boolean, nullable=False, default=False)
    relationship_type = Column(String(191), nullable=True, default='')

    # Relationships
    event = relationship("Event", back_populates="event_tags")
    tag = relationship("Tag", back_populates="event_tags")

    __table_args__ = (
        Index('idx_event_tags_event_id', 'event_id'),
        Index('idx_event_tags_tag_id', 'tag_id'),
        Index('idx_event_tags_local', 'local'),
    )


class AttributeTag(MispBaseModel, TimestampMixin):
    """MISP AttributeTag - Junction table for Attribute-Tag relationships"""
    __tablename__ = 'attribute_tags'

    attribute_id = Column(Integer, ForeignKey(
        'attributes.id'), nullable=False, index=True)
    event_id = Column(Integer, ForeignKey('events.id'),
                      nullable=False, index=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=False, index=True)
    local = Column(Boolean, nullable=False, default=False)
    relationship_type = Column(String(191), nullable=True, default='')

    # Relationships
    attribute = relationship("MispAttribute", back_populates="attribute_tags")
    event = relationship("Event")
    tag = relationship("Tag", back_populates="attribute_tags")

    __table_args__ = (
        Index('idx_attribute_tags_attribute_id', 'attribute_id'),
        Index('idx_attribute_tags_event_id', 'event_id'),
        Index('idx_attribute_tags_tag_id', 'tag_id'),
        Index('idx_attribute_tags_local', 'local'),
    )


class SharingGroup(MispBaseModel, UUIDMixin, TimestampMixin):
    """MISP SharingGroup - Data sharing controls and permissions"""
    __tablename__ = 'sharing_groups'

    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    releasability = Column(Text, nullable=True)
    org_id = Column(Integer, ForeignKey('organisations.id'),
                    nullable=False, index=True)
    sync_user_id = Column(Integer, ForeignKey(
        'users.id'), nullable=False, index=True)
    active = Column(Boolean, nullable=False, default=True)
    local = Column(Boolean, nullable=False, default=True)
    roaming = Column(Boolean, nullable=False, default=False)

    # Relationships
    organisation = relationship("Organisation")
    sync_user = relationship("User")

    # Events using this sharing group
    events = relationship("Event", back_populates="sharing_group")

    __table_args__ = (
        Index('idx_sharing_groups_name', 'name'),
        Index('idx_sharing_groups_org_id', 'org_id'),
        Index('idx_sharing_groups_active', 'active'),
        Index('idx_sharing_groups_local', 'local'),
    )

    def __repr__(self):
        return f"<SharingGroup(id={self.id}, name='{self.name}', active={self.active})>"
