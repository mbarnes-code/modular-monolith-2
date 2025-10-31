"""
MISP Data Models

SQLAlchemy models for MISP threat intelligence data structures.
Preserves the original MISP data schema while adapting to PostgreSQL
and the unified platform architecture.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import (JSON, UUID, Boolean, Column, DateTime, ForeignKey,
                        Integer, String, Text, UniqueConstraint)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


class AdminSetting(Base):
    """
    MISP admin settings - core configuration storage.

    Preserves MISP's flexible configuration system where settings
    are stored as key-value pairs in the database.
    """
    __tablename__ = "admin_settings"

    id = Column(Integer, primary_key=True)
    setting = Column(String(255), nullable=False, unique=True)
    value = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<AdminSetting(setting='{self.setting}', value='{self.value}')>"


class Role(Base):
    """
    MISP user roles with granular permissions.

    Preserves MISP's detailed permission system for user authorization.
    Permissions stored as JSON for flexibility.
    """
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    permissions = Column(JSON, nullable=False)
    default_role = Column(Boolean, default=False)
    memory_limit = Column(String(50), default="")
    max_execution_time = Column(String(50), default="")
    restricted_to_site_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"<Role(name='{self.name}', default_role={self.default_role})>"


class Organization(Base):
    """
    MISP organizations for multi-tenancy and data sharing.

    Preserves MISP's organization structure for event ownership
    and sharing group management.
    """
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(255), default="")
    nationality = Column(String(100), default="Not specified")
    sector = Column(String(255), default="")
    uuid = Column(UUID(as_uuid=True), nullable=False,
                  unique=True, default=uuid4)
    contacts = Column(Text, default="")
    local = Column(Boolean, default=True)
    restricted_to_domain = Column(JSON, default=list)
    landingpage = Column(String(255), default="")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    users = relationship("User", back_populates="organization")
    events = relationship("Event", back_populates="organization")

    def __repr__(self) -> str:
        return f"<Organization(name='{self.name}', uuid='{self.uuid}')>"


class User(Base):
    """
    MISP users with authentication and authorization.

    Preserves MISP's user management while integrating with
    unified platform authentication.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    password = Column(String(255), nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("servers.id"), default=0)
    email = Column(String(255), nullable=False, unique=True)
    autoalert = Column(Boolean, default=True)
    authkey = Column(String(40), unique=True)
    invited_by = Column(Integer, ForeignKey("users.id"))
    gpgkey = Column(Text)
    certif_public = Column(Text)
    nids_sid = Column(Integer, default=0)
    termsaccepted = Column(Boolean, default=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    change_pw = Column(Boolean, default=True)
    contactalert = Column(Boolean, default=False)
    disabled = Column(Boolean, default=False)
    expiration = Column(DateTime)
    current_login = Column(DateTime)
    last_login = Column(DateTime)
    force_logout = Column(Boolean, default=False)
    date_created = Column(DateTime, default=func.now())
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="users")
    role = relationship("Role", back_populates="users")
    server = relationship("Server", back_populates="users")
    invited_users = relationship("User", remote_side=[id])

    def __repr__(self) -> str:
        return f"<User(email='{self.email}', org_id={self.org_id})>"


class Server(Base):
    """
    MISP servers for synchronization and federation.

    Preserves MISP's server-to-server sync capabilities.
    """
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    authkey = Column(String(40), nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    push = Column(Boolean, default=False)
    pull = Column(Boolean, default=False)
    push_sightings = Column(Boolean, default=False)
    push_galaxy_clusters = Column(Boolean, default=False)
    pull_galaxy_clusters = Column(Boolean, default=False)
    lastpulledid = Column(Integer, default=0)
    lastpushedid = Column(Integer, default=0)
    organization = Column(String(10), default="")
    remote_org_id = Column(Integer, default=1)
    publish_without_email = Column(Boolean, default=False)
    unpublish_event = Column(Boolean, default=False)
    self_signed = Column(Boolean, default=False)
    pull_rules = Column(Text, default="")
    push_rules = Column(Text, default="")
    cert_file = Column(String(255))
    client_cert_file = Column(String(255))
    internal = Column(Boolean, default=False)
    skip_proxy = Column(Boolean, default=False)
    caching_enabled = Column(Boolean, default=False)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    organization_rel = relationship("Organization")
    users = relationship("User", back_populates="server")

    def __repr__(self) -> str:
        return f"<Server(name='{self.name}', url='{self.url}')>"


class Tag(Base):
    """
    MISP tags for event and attribute classification.

    Preserves MISP's flexible tagging system including TLP tags.
    """
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    colour = Column(String(7), nullable=False)
    exportable = Column(Boolean, default=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), default=0)
    user_id = Column(Integer, ForeignKey("users.id"), default=0)
    hide_tag = Column(Boolean, default=False)
    numerical_value = Column(Integer)
    is_galaxy = Column(Boolean, default=False)
    is_custom_galaxy = Column(Boolean, default=False)
    local_only = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization")
    user = relationship("User")

    def __repr__(self) -> str:
        return f"<Tag(name='{self.name}', colour='{self.colour}')>"


class Event(Base):
    """
    MISP events - core threat intelligence containers.

    Preserves MISP's event structure for threat intelligence sharing.
    """
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    info = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uuid = Column(UUID(as_uuid=True), nullable=False,
                  unique=True, default=uuid4)
    published = Column(Boolean, default=False)
    analysis = Column(Integer, default=0)  # 0=initial, 1=ongoing, 2=complete
    attribute_count = Column(Integer, default=0)
    orgc_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    timestamp = Column(Integer, nullable=False)
    distribution = Column(Integer, default=0)
    sharing_group_id = Column(Integer, ForeignKey("sharing_groups.id"))
    proposal_email_lock = Column(Boolean, default=False)
    locked = Column(Boolean, default=False)
    threat_level_id = Column(Integer, default=4)
    publish_timestamp = Column(Integer, default=0)
    sighting_timestamp = Column(Integer, default=0)
    disable_correlation = Column(Boolean, default=False)
    extends_uuid = Column(UUID(as_uuid=True))
    protected = Column(Boolean)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", foreign_keys=[org_id])
    creator_org = relationship("Organization", foreign_keys=[orgc_id])
    user = relationship("User")
    sharing_group = relationship("SharingGroup")
    attributes = relationship("Attribute", back_populates="event")

    def __repr__(self) -> str:
        return f"<Event(id={self.id}, info='{self.info[:50]}...')>"


class Attribute(Base):
    """
    MISP attributes - individual threat indicators.

    Preserves MISP's attribute structure for IoCs and threat data.
    """
    __tablename__ = "attributes"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    object_id = Column(Integer, ForeignKey("objects.id"), default=0)
    object_relation = Column(String(255))
    category = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)
    value1 = Column(Text, nullable=False)
    value2 = Column(Text, default="")
    to_ids = Column(Boolean, default=True)
    uuid = Column(UUID(as_uuid=True), nullable=False,
                  unique=True, default=uuid4)
    timestamp = Column(Integer, nullable=False)
    distribution = Column(Integer, default=5)
    sharing_group_id = Column(Integer, ForeignKey("sharing_groups.id"))
    comment = Column(Text, default="")
    deleted = Column(Boolean, default=False)
    disable_correlation = Column(Boolean, default=False)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    event = relationship("Event", back_populates="attributes")
    sharing_group = relationship("SharingGroup")
    object = relationship("Object")

    def __repr__(self) -> str:
        return f"<Attribute(type='{self.type}', value='{self.value1[:50]}...')>"


class Object(Base):
    """
    MISP objects - complex threat intelligence structures.

    Preserves MISP's object system for structured threat data.
    """
    __tablename__ = "objects"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    meta_category = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    template_uuid = Column(UUID(as_uuid=True), nullable=False)
    template_version = Column(Integer, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    uuid = Column(UUID(as_uuid=True), nullable=False,
                  unique=True, default=uuid4)
    timestamp = Column(Integer, nullable=False)
    distribution = Column(Integer, default=5)
    sharing_group_id = Column(Integer, ForeignKey("sharing_groups.id"))
    comment = Column(Text, default="")
    deleted = Column(Boolean, default=False)
    first_seen = Column(DateTime)
    last_seen = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    event = relationship("Event")
    sharing_group = relationship("SharingGroup")
    attributes = relationship("Attribute", back_populates="object")

    def __repr__(self) -> str:
        return f"<Object(name='{self.name}', template_uuid='{self.template_uuid}')>"


class SharingGroup(Base):
    """
    MISP sharing groups for access control.

    Preserves MISP's sharing group system for granular access control.
    """
    __tablename__ = "sharing_groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    releasability = Column(Text, default="")
    description = Column(Text, default="")
    uuid = Column(UUID(as_uuid=True), nullable=False,
                  unique=True, default=uuid4)
    organisation_uuid = Column(UUID(as_uuid=True), nullable=False)
    org_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created = Column(DateTime, default=func.now())
    modified = Column(DateTime, default=func.now(), onupdate=func.now())
    active = Column(Boolean, default=True)
    local = Column(Boolean, default=True)
    roaming = Column(Boolean, default=False)
    sync_user_id = Column(Integer, ForeignKey("users.id"), default=0)

    # Relationships
    organization = relationship("Organization")
    user = relationship("User", foreign_keys=[user_id])
    sync_user = relationship("User", foreign_keys=[sync_user_id])

    def __repr__(self) -> str:
        return f"<SharingGroup(name='{self.name}', uuid='{self.uuid}')>"


# Export all models for easy importing
__all__ = [
    "Base",
    "AdminSetting",
    "Role",
    "Organization",
    "User",
    "Server",
    "Tag",
    "Event",
    "Attribute",
    "Object",
    "SharingGroup"
]
