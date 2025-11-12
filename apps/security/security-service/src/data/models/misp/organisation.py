"""MISP Organisation Model

Organisation management model migrated from CakePHP Organisation.php.
Handles organizational structure, user management, and inter-MISP federation.
"""

from sqlalchemy import (Boolean, CheckConstraint, Column, Index, Integer,
                        String, Text)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from . import MispBaseModel, TimestampMixin, UUIDMixin


class Organisation(MispBaseModel, UUIDMixin, TimestampMixin):
    """
    MISP Organisation - Organizational entities and federation management

    Migrated from CakePHP Organisation.php maintaining:
    - Inter-MISP federation capabilities
    - Organizational hierarchy and permissions
    - Contact information and metadata
    - Local vs remote organization tracking
    """
    __tablename__ = 'organisations'

    # Core organization fields
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    type = Column(String(255), nullable=True)
    nationality = Column(String(255), nullable=True)
    sector = Column(String(255), nullable=True)

    # Contact information
    contact_person = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(255), nullable=True)

    # Federation and sync
    local = Column(Boolean, nullable=False, default=True, index=True)

    # Organizational metadata
    url = Column(String(255), nullable=True)
    logo_url = Column(String(255), nullable=True)
    landingpage = Column(Text, nullable=True)

    # Restrictions and limits
    restricted_to_domain = Column(String(255), nullable=True)

    # JSON fields for flexible metadata
    org_meta = Column(JSONB, nullable=True)

    # Relationships
    # Users belonging to this organization
    users = relationship(
        "User",
        back_populates="organisation",
        foreign_keys="User.org_id"
    )

    # Events owned by this organization (org_id)
    events_owned = relationship(
        "Event",
        back_populates="org",
        foreign_keys="Event.org_id"
    )

    # Events created by this organization (orgc_id)
    events_created = relationship(
        "Event",
        back_populates="orgc",
        foreign_keys="Event.orgc_id"
    )

    # Table constraints and indexes
    __table_args__ = (
        # Performance indexes
        Index('idx_organisations_name', 'name'),
        Index('idx_organisations_uuid', 'uuid'),
        Index('idx_organisations_local', 'local'),
        Index('idx_organisations_type', 'type'),
        Index('idx_organisations_sector', 'sector'),
        Index('idx_organisations_nationality', 'nationality'),

        # Composite indexes
        Index('idx_organisations_local_name', 'local', 'name'),
    )

    def __repr__(self):
        return f"<Organisation(id={self.id}, name='{self.name}', local={self.local})>"

    @property
    def is_local(self) -> bool:
        """Check if organization is local to this MISP instance"""
        return self.local

    @property
    def is_remote(self) -> bool:
        """Check if organization is from a remote MISP instance"""
        return not self.local

    @property
    def has_contact_info(self) -> bool:
        """Check if organization has contact information"""
        return bool(self.contact_email or self.contact_person or self.contact_phone)

    def get_user_count(self):
        """Get number of users in this organization"""
        return len(self.users) if self.users else 0

    def get_event_count(self):
        """Get number of events owned by this organization"""
        return len(self.events_owned) if self.events_owned else 0
