"""MISP Base Model Classes

Base SQLAlchemy models for MISP threat intelligence platform migration.
Provides foundation for all MISP entities with common patterns and relationships.
"""

from .user import User
from .supporting import (AttributeTag, EventTag, Role, SharingGroup,
                         SharingGroupOrg, SharingGroupServer, Tag, ThreatLevel)
from .organisation import Organisation
from .misp_object import MispObject, ObjectReference
from .galaxy import Galaxy, GalaxyCluster, GalaxyClusterRelation, GalaxyElement
from .event import Event
from .attribute import MispAttribute
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import (TIMESTAMP, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class MispBaseModel(Base):
    """Base model class for all MISP entities"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(TIMESTAMP(timezone=True),
                     default=datetime.utcnow, nullable=False)
    modified = Column(TIMESTAMP(timezone=True), default=datetime.utcnow,
                      onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert model instance to dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class UUIDMixin:
    """Mixin for models that require UUID fields"""
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4,
                  unique=True, nullable=False, index=True)


class OrganisationMixin:
    """Mixin for models that belong to organizations"""
    org_id = Column(Integer, ForeignKey('organisations.id'),
                    nullable=False, index=True)
    orgc_id = Column(Integer, ForeignKey('organisations.id'),
                     nullable=False, index=True)


class UserMixin:
    """Mixin for models that track user ownership"""
    user_id = Column(Integer, ForeignKey('users.id'),
                     nullable=False, index=True)


class SharingMixin:
    """Mixin for models with sharing/distribution controls"""
    distribution = Column(Integer, nullable=False, default=0)
    sharing_group_id = Column(Integer, ForeignKey(
        'sharing_groups.id'), nullable=True)


class TimestampMixin:
    """Mixin for models with timestamp tracking"""
    timestamp = Column(Integer, nullable=False,
                       default=lambda: int(datetime.utcnow().timestamp()))


class DeletedMixin:
    """Mixin for soft delete functionality"""
    deleted = Column(Boolean, nullable=False, default=False, index=True)


class LocalMixin:
    """Mixin for models that can be local vs synchronized"""
    local = Column(Boolean, nullable=False, default=False)


# Import all models for easier access

__all__ = [
    # Base classes
    'MispBaseModel', 'UUIDMixin', 'OrganisationMixin', 'UserMixin',
    'SharingMixin', 'TimestampMixin', 'DeletedMixin', 'LocalMixin',

    # Main models
    'Event', 'MispAttribute', 'Organisation', 'User',

    # Object models
    'MispObject', 'ObjectReference',

    # Galaxy models
    'Galaxy', 'GalaxyCluster', 'GalaxyElement', 'GalaxyClusterRelation',

    # Supporting models
    'ThreatLevel', 'Role', 'Tag', 'EventTag', 'AttributeTag',
    'SharingGroup', 'SharingGroupOrg', 'SharingGroupServer',
]
