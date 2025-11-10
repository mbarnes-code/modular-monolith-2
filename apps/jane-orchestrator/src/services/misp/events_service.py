"""
MISP Events Service

Business logic for MISP event operations.
Migrated from features/MISP/app/Controller/EventsController.php
"""

from typing import Any, Dict, List, Optional

from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import Session

from ...data.models.misp.core_models import (Attribute, Event, Organization,
                                             User)
from ...schemas.misp.events import EventCreate, EventSearch, EventUpdate


class MispEventsService:
    """Service for MISP event operations"""

    def __init__(self, db: Session):
        self.db = db

    async def list_events(
        self,
        user: User,
        org: Optional[str] = None,
        date_filter: Optional[str] = None,
        event_type: Optional[str] = None,
        category: Optional[str] = None,
        published: Optional[bool] = None,
        limit: int = 60,
        page: int = 1,
        sort: str = "timestamp",
        direction: str = "desc"
    ) -> Dict[str, Any]:
        """List events with filtering and pagination"""

        query = self.db.query(Event)

        # Apply filters based on user permissions and distribution
        if org:
            query = query.join(Organization).filter(Organization.name == org)

        if published is not None:
            query = query.filter(Event.published == published)

        # Apply sorting
        sort_column = getattr(Event, sort, Event.timestamp)
        if direction.lower() == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))

        # Count total before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * limit
        events = query.offset(offset).limit(limit).all()

        return {
            "events": [self._event_to_dict(event) for event in events],
            "total": total
        }

    async def get_event(
        self,
        event_id: int,
        user: User,
        include_attributes: bool = True,
        include_correlations: bool = False,
        extended: bool = False
    ) -> Optional[Dict[str, Any]]:
        """Get single event with optional related data"""

        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        # Check user permissions for this event
        # TODO: Implement distribution-based access control

        event_dict = self._event_to_dict(event)

        if include_attributes:
            attributes = self.db.query(Attribute).filter(
                and_(Attribute.event_id == event_id, Attribute.deleted == False)
            ).all()
            event_dict["attributes"] = [
                self._attribute_to_dict(attr) for attr in attributes]

        return event_dict

    async def create_event(
        self,
        event_data: EventCreate,
        user: User
    ) -> Dict[str, Any]:
        """Create new event"""

        import time
        from uuid import uuid4

        event = Event(
            info=event_data.info,
            analysis=event_data.analysis,
            threat_level_id=event_data.threat_level_id,
            published=event_data.published,
            distribution=event_data.distribution,
            org_id=user.org_id,
            orgc_id=user.org_id,
            user_id=user.id,
            uuid=uuid4(),
            timestamp=int(time.time()),
            date=event_data.date if hasattr(event_data, 'date') else None
        )

        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)

        return self._event_to_dict(event)

    async def update_event(
        self,
        event_id: int,
        event_data: EventUpdate,
        user: User
    ) -> Optional[Dict[str, Any]]:
        """Update existing event"""

        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        # Check permissions - only org owner or admin can modify
        if event.org_id != user.org_id and not user.role.name == "admin":
            return None

        # Update fields
        for field, value in event_data.dict(exclude_unset=True).items():
            setattr(event, field, value)

        self.db.commit()
        self.db.refresh(event)

        return self._event_to_dict(event)

    async def delete_event(
        self,
        event_id: int,
        user: User
    ) -> bool:
        """Delete (soft delete) event"""

        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return False

        # Check permissions
        if event.org_id != user.org_id and not user.role.name == "admin":
            return False

        # Soft delete
        event.deleted = True
        self.db.commit()

        return True

    async def search_events(
        self,
        search_criteria: EventSearch,
        user: User
    ) -> Dict[str, Any]:
        """Complex event search"""

        query = self.db.query(Event)

        # Apply search filters
        if search_criteria.value:
            # Join with attributes for value search
            query = query.join(Attribute).filter(
                or_(
                    Attribute.value1.contains(search_criteria.value),
                    Attribute.value2.contains(search_criteria.value)
                )
            )

        if search_criteria.published is not None:
            query = query.filter(Event.published == search_criteria.published)

        # Apply pagination
        limit = search_criteria.limit or 60
        page = search_criteria.page or 1
        offset = (page - 1) * limit

        total = query.count()
        events = query.offset(offset).limit(limit).all()

        return {
            "events": [self._event_to_dict(event) for event in events],
            "total": total
        }

    async def publish_event(
        self,
        event_id: int,
        user: User
    ) -> Optional[Dict[str, Any]]:
        """Publish event"""

        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        # Check permissions and business rules
        if event.org_id != user.org_id and not user.role.name == "admin":
            return None

        # Business rule: event must have at least one attribute
        attr_count = self.db.query(Attribute).filter(
            and_(Attribute.event_id == event_id, Attribute.deleted == False)
        ).count()

        if attr_count == 0:
            raise ValueError(
                "Event must have at least one attribute before publication")

        import time
        event.published = True
        event.publish_timestamp = int(time.time())

        # TODO: Trigger sync to connected instances

        self.db.commit()
        self.db.refresh(event)

        return self._event_to_dict(event)

    async def unpublish_event(
        self,
        event_id: int,
        user: User
    ) -> Optional[Dict[str, Any]]:
        """Unpublish event"""

        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        # Only admin can unpublish
        if not user.role.name == "admin":
            return None

        event.published = False
        event.publish_timestamp = 0

        # TODO: Trigger revocation notifications

        self.db.commit()
        self.db.refresh(event)

        return self._event_to_dict(event)

    async def export_nids_rules(
        self,
        format: str,
        user: User,
        org: Optional[str] = None,
        event_id: Optional[int] = None,
        tags: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None
    ) -> str:
        """Export NIDS rules in specified format"""

        # This is a placeholder - would need format-specific generators
        return f"# NIDS rules in {format} format\n# Generated from MISP events\n"

    async def export_openioc(
        self,
        event_id: int,
        user: User
    ) -> Optional[str]:
        """Export event in OpenIOC XML format"""

        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        # This is a placeholder - would need OpenIOC XML generation
        return f'<?xml version="1.0"?>\n<ioc>\n  <event id="{event_id}"/>\n</ioc>'

    def _event_to_dict(self, event: Event) -> Dict[str, Any]:
        """Convert event model to dictionary"""
        return {
            "id": event.id,
            "uuid": str(event.uuid),
            "info": event.info,
            "org_id": event.org_id,
            "orgc_id": event.orgc_id,
            "user_id": event.user_id,
            "date": event.date,
            "timestamp": event.timestamp,
            "published": event.published,
            "analysis": event.analysis,
            "threat_level_id": event.threat_level_id,
            "distribution": event.distribution,
            "sharing_group_id": event.sharing_group_id,
            "attribute_count": event.attribute_count,
            "publish_timestamp": event.publish_timestamp,
            "created_at": event.created_at,
            "updated_at": event.updated_at
        }

    def _attribute_to_dict(self, attribute: Attribute) -> Dict[str, Any]:
        """Convert attribute model to dictionary"""
        return {
            "id": attribute.id,
            "event_id": attribute.event_id,
            "category": attribute.category,
            "type": attribute.type,
            "value1": attribute.value1,
            "value2": attribute.value2,
            "to_ids": attribute.to_ids,
            "uuid": str(attribute.uuid),
            "timestamp": attribute.timestamp,
            "distribution": attribute.distribution,
            "comment": attribute.comment
        }
