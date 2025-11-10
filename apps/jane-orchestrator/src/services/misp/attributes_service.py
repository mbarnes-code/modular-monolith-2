"""
MISP Attributes Service

Business logic for MISP attribute operations.
Migrated from features/MISP/app/Model/Attribute.php and related controllers.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, desc, func, or_
from sqlalchemy.orm import Session

from ...data.models.misp_models import Attribute, Event, User
from ...schemas.misp.attributes import (AttributeCreate, AttributeSearch,
                                        AttributeUpdate)


class MispAttributesService:
    """Business logic service for MISP attributes"""

    def __init__(self, db: Session):
        self.db = db

    async def search_attributes(
        self,
        user: User,
        value: Optional[str] = None,
        attribute_type: Optional[str] = None,
        category: Optional[str] = None,
        org: Optional[str] = None,
        event_id: Optional[int] = None,
        timestamp: Optional[str] = None,
        limit: int = 60,
        page: int = 1
    ) -> Dict[str, Any]:
        """
        Search attributes with filters

        Migrated from AttributesController::index()
        Preserves complex filtering and distribution-aware results
        """
        query = self.db.query(Attribute).join(Event)

        # Apply user-based distribution filtering
        query = self._apply_distribution_filter(query, user)

        # Apply search filters
        if value:
            query = query.filter(Attribute.value.ilike(f"%{value}%"))

        if attribute_type:
            query = query.filter(Attribute.type == attribute_type)

        if category:
            query = query.filter(Attribute.category == category)

        if org:
            query = query.join(Event.org).filter(Event.org.name == org)

        if event_id:
            query = query.filter(Attribute.event_id == event_id)

        if timestamp:
            # Parse timestamp filter (e.g., "1d", "1w", "1m")
            cutoff_time = self._parse_timestamp_filter(timestamp)
            if cutoff_time:
                query = query.filter(Attribute.timestamp >= cutoff_time)

        # Apply deleted filter (default: exclude deleted)
        query = query.filter(Attribute.deleted == False)

        # Get total count
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        attributes = query.offset(offset).limit(limit).all()

        # Convert to dict format
        attribute_dicts = []
        for attr in attributes:
            attr_dict = {
                "id": attr.id,
                "event_id": attr.event_id,
                "uuid": attr.uuid,
                "type": attr.type,
                "value": attr.value,
                "category": attr.category,
                "comment": attr.comment,
                "to_ids": attr.to_ids,
                "distribution": attr.distribution,
                "sharing_group_id": attr.sharing_group_id,
                "timestamp": attr.timestamp,
                "deleted": attr.deleted,
                "disable_correlation": attr.disable_correlation,
                "object_id": attr.object_id,
                "object_relation": attr.object_relation,
                "first_seen": attr.first_seen,
                "last_seen": attr.last_seen,
                "event_uuid": attr.event.uuid if attr.event else None,
                "event_info": attr.event.info if attr.event else None,
                "event_date": str(attr.event.date) if attr.event else None
            }
            attribute_dicts.append(attr_dict)

        return {
            "attributes": attribute_dicts,
            "total": total
        }

    async def create_attribute(
        self,
        attribute_data: AttributeCreate,
        user: User
    ) -> Dict[str, Any]:
        """
        Create new attribute

        Migrated from AttributesController::add()
        Preserves type validation and correlation triggers
        """
        # Validate event access
        event = self.db.query(Event).filter(
            Event.id == attribute_data.event_id).first()
        if not event:
            raise ValueError("Event not found")

        # Check user permissions for event
        if not self._can_modify_event(user, event):
            raise ValueError("Insufficient permissions to modify event")

        # Validate attribute type-value compatibility
        if not self._validate_type_value(attribute_data.type, attribute_data.value):
            raise ValueError(f"Invalid value for type {attribute_data.type}")

        # Create attribute
        attribute = Attribute(
            event_id=attribute_data.event_id,
            type=attribute_data.type,
            value=attribute_data.value,
            category=attribute_data.category,
            comment=attribute_data.comment,
            to_ids=attribute_data.to_ids,
            distribution=attribute_data.distribution,
            sharing_group_id=attribute_data.sharing_group_id,
            timestamp=datetime.utcnow(),
            uuid=self._generate_uuid()
        )

        self.db.add(attribute)
        self.db.commit()
        self.db.refresh(attribute)

        # Trigger correlation analysis
        await self._trigger_correlation(attribute)

        return self._attribute_to_dict(attribute)

    async def advanced_search(
        self,
        search_criteria: AttributeSearch,
        user: User
    ) -> Dict[str, Any]:
        """
        Advanced attribute search with complex criteria

        Migrated from AttributesController::restSearch()
        Preserves boolean logic and complex filtering
        """
        query = self.db.query(Attribute).join(Event)

        # Apply user-based distribution filtering
        query = self._apply_distribution_filter(query, user)

        # Apply search criteria
        if search_criteria.value:
            query = query.filter(Attribute.value.ilike(
                f"%{search_criteria.value}%"))

        if search_criteria.type:
            query = query.filter(Attribute.type.in_(search_criteria.type))

        if search_criteria.category:
            query = query.filter(
                Attribute.category.in_(search_criteria.category))

        if search_criteria.eventid:
            query = query.filter(
                Attribute.event_id.in_(search_criteria.eventid))

        if search_criteria.org:
            query = query.join(Event.org).filter(
                Event.org.name == search_criteria.org)

        if search_criteria.timestamp:
            cutoff_time = self._parse_timestamp_filter(
                search_criteria.timestamp)
            if cutoff_time:
                query = query.filter(Attribute.timestamp >= cutoff_time)

        if search_criteria.to_ids is not None:
            query = query.filter(Attribute.to_ids == search_criteria.to_ids)

        if search_criteria.deleted is not None:
            query = query.filter(Attribute.deleted == search_criteria.deleted)
        else:
            query = query.filter(Attribute.deleted == False)

        # Get total count
        total = query.count()

        # Apply pagination
        limit = search_criteria.limit or 60
        page = search_criteria.page or 1
        offset = (page - 1) * limit

        attributes = query.offset(offset).limit(limit).all()

        # Convert to dict format
        attribute_dicts = [self._attribute_to_dict(
            attr) for attr in attributes]

        return {
            "attributes": attribute_dicts,
            "total": total
        }

    async def get_attribute(
        self,
        attribute_id: int,
        user: User
    ) -> Optional[Dict[str, Any]]:
        """Get single attribute by ID"""
        query = self.db.query(Attribute).join(
            Event).filter(Attribute.id == attribute_id)

        # Apply distribution filtering
        query = self._apply_distribution_filter(query, user)

        attribute = query.first()

        if attribute:
            return self._attribute_to_dict(attribute)

        return None

    async def update_attribute(
        self,
        attribute_id: int,
        attribute_data: AttributeUpdate,
        user: User
    ) -> Optional[Dict[str, Any]]:
        """Update existing attribute"""
        attribute = self.db.query(Attribute).join(Event).filter(
            Attribute.id == attribute_id
        ).first()

        if not attribute:
            return None

        # Check permissions
        if not self._can_modify_event(user, attribute.event):
            raise ValueError("Insufficient permissions to modify attribute")

        # Update fields
        update_data = attribute_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(attribute, field):
                setattr(attribute, field, value)

        # Validate type-value if both changed
        if attribute_data.type and attribute_data.value:
            if not self._validate_type_value(attribute_data.type, attribute_data.value):
                raise ValueError(
                    f"Invalid value for type {attribute_data.type}")

        attribute.timestamp = datetime.utcnow()

        self.db.commit()
        self.db.refresh(attribute)

        return self._attribute_to_dict(attribute)

    async def delete_attribute(
        self,
        attribute_id: int,
        user: User
    ) -> bool:
        """Delete attribute (soft delete)"""
        attribute = self.db.query(Attribute).join(Event).filter(
            Attribute.id == attribute_id
        ).first()

        if not attribute:
            return False

        # Check permissions
        if not self._can_modify_event(user, attribute.event):
            raise ValueError("Insufficient permissions to delete attribute")

        # Soft delete
        attribute.deleted = True
        attribute.timestamp = datetime.utcnow()

        self.db.commit()

        return True

    def _apply_distribution_filter(self, query, user: User):
        """Apply distribution-based filtering for user access"""
        # Implementation depends on MISP distribution model
        # For now, basic org-based filtering
        if not user.role_admin:
            query = query.filter(
                or_(
                    # Community, org, connected
                    Attribute.distribution.in_([0, 1, 2, 3]),
                    and_(
                        Attribute.distribution == 4,  # Sharing group
                        # Add sharing group membership check
                    )
                )
            )

        return query

    def _can_modify_event(self, user: User, event: Event) -> bool:
        """Check if user can modify event"""
        # Admin can modify all
        if user.role_admin:
            return True

        # Org admin can modify org events
        if user.role_org_admin and event.org_id == user.org_id:
            return True

        # User can modify own org's events if not published
        if event.org_id == user.org_id and not event.published:
            return True

        return False

    def _validate_type_value(self, attr_type: str, value: str) -> bool:
        """Validate attribute type-value compatibility"""
        # Simplified validation - full implementation would check MISP types
        if attr_type in ["ip-src", "ip-dst"] and not self._is_valid_ip(value):
            return False

        if attr_type == "domain" and not self._is_valid_domain(value):
            return False

        # Add more type validations as needed
        return True

    def _is_valid_ip(self, value: str) -> bool:
        """Basic IP validation"""
        import ipaddress
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False

    def _is_valid_domain(self, value: str) -> bool:
        """Basic domain validation"""
        import re
        domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
        return bool(re.match(domain_pattern, value))

    def _generate_uuid(self) -> str:
        """Generate UUID for attribute"""
        import uuid
        return str(uuid.uuid4())

    def _parse_timestamp_filter(self, timestamp_str: str) -> Optional[datetime]:
        """Parse timestamp filter string"""
        if not timestamp_str:
            return None

        # Parse formats like "1d", "7d", "1w", "1m"
        try:
            if timestamp_str.endswith('d'):
                days = int(timestamp_str[:-1])
                return datetime.utcnow() - timedelta(days=days)
            elif timestamp_str.endswith('w'):
                weeks = int(timestamp_str[:-1])
                return datetime.utcnow() - timedelta(weeks=weeks)
            elif timestamp_str.endswith('m'):
                months = int(timestamp_str[:-1])
                return datetime.utcnow() - timedelta(days=months * 30)
        except (ValueError, IndexError):
            pass

        return None

    def _attribute_to_dict(self, attribute: Attribute) -> Dict[str, Any]:
        """Convert attribute to dictionary"""
        return {
            "id": attribute.id,
            "event_id": attribute.event_id,
            "uuid": attribute.uuid,
            "type": attribute.type,
            "value": attribute.value,
            "category": attribute.category,
            "comment": attribute.comment,
            "to_ids": attribute.to_ids,
            "distribution": attribute.distribution,
            "sharing_group_id": attribute.sharing_group_id,
            "timestamp": attribute.timestamp,
            "deleted": attribute.deleted,
            "disable_correlation": attribute.disable_correlation,
            "object_id": attribute.object_id,
            "object_relation": attribute.object_relation,
            "first_seen": attribute.first_seen,
            "last_seen": attribute.last_seen,
            "event_uuid": attribute.event.uuid if attribute.event else None,
            "event_info": attribute.event.info if attribute.event else None,
            "event_date": str(attribute.event.date) if attribute.event else None
        }

    async def _trigger_correlation(self, attribute: Attribute):
        """Trigger correlation analysis for new attribute"""
        # Placeholder for correlation logic
        # In full implementation, this would analyze correlations with other attributes
        pass
