"""
MISP Organizations Service

Business logic for MISP organization operations.
Migrated from features/MISP/app/Model/Organisation.php and related controllers.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from ...data.models.misp_models import Event, Organization, User
from ...schemas.misp.organizations import (OrganizationCreate,
                                           OrganizationUpdate)


class MispOrganizationsService:
    """Business logic service for MISP organizations"""

    def __init__(self, db: Session):
        self.db = db

    async def list_organizations(
        self,
        user: User,
        name: Optional[str] = None,
        sector: Optional[str] = None,
        nationality: Optional[str] = None,
        limit: int = 60,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        List organizations with filters

        Migrated from OrganisationsController::index()
        Preserves organization visibility and access control
        """
        query = self.db.query(Organization)

        # Apply visibility filtering
        if not user.role_admin:
            # Non-admin users can only see their own org and public orgs
            query = query.filter(
                or_(
                    Organization.id == user.org_id,
                    Organization.local == True  # Public organizations
                )
            )

        # Apply search filters
        if name:
            query = query.filter(
                Organization.name.ilike(f"%{name}%")
            )

        if sector:
            query = query.filter(Organization.sector == sector)

        if nationality:
            query = query.filter(Organization.nationality == nationality)

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        organizations = query.offset(offset).limit(limit).all()

        # Convert to dict format with statistics
        org_dicts = []
        for org in organizations:
            org_dict = self._organization_to_dict(org)

            # Add statistics
            org_dict.update(await self._get_organization_stats(org.id))

            org_dicts.append(org_dict)

        return {
            "organizations": org_dicts,
            "total": total
        }

    async def create_organization(
        self,
        org_data: OrganizationCreate,
        user: User
    ) -> Dict[str, Any]:
        """
        Create new organization

        Migrated from OrganisationsController::add()
        Preserves organization validation and access control
        """
        # Check permissions - only admins can create organizations
        if not user.role_admin:
            raise ValueError("Insufficient permissions to create organization")

        # Check for duplicate name
        existing = self.db.query(Organization).filter(
            Organization.name == org_data.name
        ).first()

        if existing:
            raise ValueError(
                f"Organization with name '{org_data.name}' already exists")

        # Create organization
        organization = Organization(
            name=org_data.name,
            description=org_data.description,
            type=org_data.type,
            nationality=org_data.nationality,
            sector=org_data.sector,
            contacts=org_data.contacts,
            local=org_data.local,
            restricted_to_domain=org_data.restricted_to_domain,
            created_by=user.id,
            date_created=datetime.utcnow(),
            uuid=self._generate_uuid()
        )

        self.db.add(organization)
        self.db.commit()
        self.db.refresh(organization)

        return self._organization_to_dict(organization)

    async def get_organization(
        self,
        org_id: int,
        user: User
    ) -> Optional[Dict[str, Any]]:
        """Get single organization by ID"""
        query = self.db.query(Organization).filter(Organization.id == org_id)

        # Apply visibility filtering
        if not user.role_admin:
            query = query.filter(
                or_(
                    Organization.id == user.org_id,
                    Organization.local == True
                )
            )

        organization = query.first()

        if organization:
            org_dict = self._organization_to_dict(organization)
            org_dict.update(await self._get_organization_stats(org_id))
            return org_dict

        return None

    async def update_organization(
        self,
        org_id: int,
        org_data: OrganizationUpdate,
        user: User
    ) -> Optional[Dict[str, Any]]:
        """Update existing organization"""
        organization = self.db.query(Organization).filter(
            Organization.id == org_id
        ).first()

        if not organization:
            return None

        # Check permissions
        if not self._can_modify_organization(user, organization):
            raise ValueError("Insufficient permissions to modify organization")

        # Check for duplicate name if changing
        if org_data.name and org_data.name != organization.name:
            existing = self.db.query(Organization).filter(
                and_(
                    Organization.name == org_data.name,
                    Organization.id != org_id
                )
            ).first()

            if existing:
                raise ValueError(
                    f"Organization with name '{org_data.name}' already exists"
                )

        # Update fields
        update_data = org_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(organization, field):
                setattr(organization, field, value)

        organization.date_modified = datetime.utcnow()

        self.db.commit()
        self.db.refresh(organization)

        return self._organization_to_dict(organization)

    async def delete_organization(
        self,
        org_id: int,
        user: User
    ) -> bool:
        """Delete organization (soft delete)"""
        organization = self.db.query(Organization).filter(
            Organization.id == org_id
        ).first()

        if not organization:
            return False

        # Check permissions - only admins can delete organizations
        if not user.role_admin:
            raise ValueError("Insufficient permissions to delete organization")

        # Check if organization has users or events
        user_count = self.db.query(User).filter(
            User.org_id == org_id
        ).count()

        event_count = self.db.query(Event).filter(
            Event.org_id == org_id
        ).count()

        if user_count > 0 or event_count > 0:
            raise ValueError(
                "Cannot delete organization with existing users or events"
            )

        # Soft delete (in practice, MISP might use hard delete for orgs)
        self.db.delete(organization)
        self.db.commit()

        return True

    async def get_organization_events(
        self,
        org_id: int,
        user: User,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get events belonging to organization"""
        # Check organization access
        org = await self.get_organization(org_id, user)
        if not org:
            raise ValueError("Organization not found or access denied")

        query = self.db.query(Event).filter(Event.org_id == org_id)

        # Apply user-based filtering
        if not user.role_admin and user.org_id != org_id:
            query = query.filter(Event.published == True)

        total = query.count()

        offset = (page - 1) * limit
        events = query.offset(offset).limit(limit).all()

        return {
            "events": [self._event_to_dict(event) for event in events],
            "total": total,
            "page": page,
            "limit": limit
        }

    async def get_organization_users(
        self,
        org_id: int,
        user: User,
        limit: int = 50,
        page: int = 1
    ) -> Dict[str, Any]:
        """Get users belonging to organization"""
        # Check permissions
        if not user.role_admin and user.org_id != org_id:
            raise ValueError(
                "Insufficient permissions to view organization users")

        query = self.db.query(User).filter(User.org_id == org_id)

        total = query.count()

        offset = (page - 1) * limit
        users = query.offset(offset).limit(limit).all()

        return {
            "users": [self._user_to_dict(user_obj) for user_obj in users],
            "total": total,
            "page": page,
            "limit": limit
        }

    def _can_modify_organization(self, user: User, organization: Organization) -> bool:
        """Check if user can modify organization"""
        # Admin can modify all
        if user.role_admin:
            return True

        # Org admin can modify own organization
        if user.role_org_admin and user.org_id == organization.id:
            return True

        return False

    async def _get_organization_stats(self, org_id: int) -> Dict[str, int]:
        """Get statistics for organization"""
        user_count = self.db.query(User).filter(User.org_id == org_id).count()
        event_count = self.db.query(Event).filter(
            Event.org_id == org_id).count()

        # Attribute count (through events)
        attribute_count = self.db.query(func.count()).select_from(
            self.db.query(Event).filter(Event.org_id == org_id).subquery()
        ).scalar() or 0

        return {
            "user_count": user_count,
            "event_count": event_count,
            "attribute_count": attribute_count
        }

    def _generate_uuid(self) -> str:
        """Generate UUID for organization"""
        import uuid
        return str(uuid.uuid4())

    def _organization_to_dict(self, organization: Organization) -> Dict[str, Any]:
        """Convert organization to dictionary"""
        return {
            "id": organization.id,
            "name": organization.name,
            "description": organization.description,
            "type": organization.type,
            "nationality": organization.nationality,
            "sector": organization.sector,
            "contacts": organization.contacts,
            "local": organization.local,
            "restricted_to_domain": organization.restricted_to_domain,
            "created_by": organization.created_by,
            "date_created": organization.date_created,
            "date_modified": organization.date_modified,
            "uuid": organization.uuid
        }

    def _event_to_dict(self, event: Event) -> Dict[str, Any]:
        """Convert event to dictionary (basic info)"""
        return {
            "id": event.id,
            "uuid": event.uuid,
            "info": event.info,
            "date": str(event.date),
            "published": event.published,
            "analysis": event.analysis,
            "threat_level_id": event.threat_level_id
        }

    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        """Convert user to dictionary (basic info)"""
        return {
            "id": user.id,
            "email": user.email,
            "role_id": user.role_id,
            "disabled": user.disabled,
            "created": user.created,
            "last_login": user.last_login
        }
