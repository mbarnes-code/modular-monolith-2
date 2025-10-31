"""MISP User Model

User management and authentication model migrated from CakePHP User.php.
Handles user accounts, permissions, and authentication for MISP platform.
"""

from sqlalchemy import (Boolean, CheckConstraint, Column, ForeignKey, Index,
                        Integer, String, Text)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from . import MispBaseModel, TimestampMixin


class User(MispBaseModel, TimestampMixin):
    """
    MISP User - User accounts and authentication management

    Migrated from CakePHP User.php maintaining:
    - User authentication and session management
    - Role-based access control integration
    - Organization membership and permissions
    - User preferences and settings
    """
    __tablename__ = 'users'

    # Core user fields
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)

    # Organization membership
    org_id = Column(Integer, ForeignKey('organisations.id'),
                    nullable=False, index=True)

    # Role and permissions
    role_id = Column(Integer, ForeignKey('roles.id'),
                     nullable=False, index=True)

    # User status and controls
    autoalert = Column(Boolean, nullable=False, default=False)
    contactalert = Column(Boolean, nullable=False, default=False)
    disabled = Column(Boolean, nullable=False, default=False, index=True)

    # Authentication tokens
    authkey = Column(String(40), nullable=True, unique=True, index=True)

    # User preferences
    nids_sid = Column(Integer, nullable=False, default=0)
    termsaccepted = Column(Boolean, nullable=False, default=False)
    newsread = Column(Integer, nullable=False, default=0)

    # Contact and identification
    gpgkey = Column(Text, nullable=True)
    certif_public = Column(Text, nullable=True)

    # Activity tracking
    last_login = Column(Integer, nullable=True)
    current_login = Column(Integer, nullable=True)

    # User metadata
    invitation_token = Column(String(40), nullable=True, index=True)

    # JSON fields for user preferences and settings
    user_settings = Column(JSONB, nullable=True)

    # Relationships
    organisation = relationship("Organisation", back_populates="users")
    role = relationship("Role", back_populates="users")

    # Events created by this user
    events = relationship("Event", back_populates="user")

    # User login profiles for tracking
    user_login_profiles = relationship(
        "UserLoginProfile",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Auth keys for API access
    auth_keys = relationship(
        "AuthKey",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Table constraints and indexes
    __table_args__ = (
        # Performance indexes
        Index('idx_users_email', 'email'),
        Index('idx_users_org_id', 'org_id'),
        Index('idx_users_role_id', 'role_id'),
        Index('idx_users_authkey', 'authkey'),
        Index('idx_users_disabled', 'disabled'),
        Index('idx_users_invitation_token', 'invitation_token'),
        Index('idx_users_last_login', 'last_login'),

        # Composite indexes
        Index('idx_users_org_role', 'org_id', 'role_id'),
        Index('idx_users_active', 'disabled', 'org_id'),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', org_id={self.org_id})>"

    @property
    def is_active(self) -> bool:
        """Check if user account is active"""
        return not self.disabled

    @property
    def is_admin(self) -> bool:
        """Check if user has admin role (requires role relationship)"""
        return self.role.perm_admin if self.role else False

    @property
    def has_gpg_key(self) -> bool:
        """Check if user has GPG key configured"""
        return bool(self.gpgkey)

    @property
    def has_certificate(self) -> bool:
        """Check if user has certificate configured"""
        return bool(self.certif_public)

    def can_publish(self) -> bool:
        """Check if user can publish events"""
        return self.role.perm_publish if self.role else False

    def can_sync(self) -> bool:
        """Check if user can synchronize with other instances"""
        return self.role.perm_sync if self.role else False

    def can_create_events(self) -> bool:
        """Check if user can create events"""
        return self.role.perm_add if self.role else False
