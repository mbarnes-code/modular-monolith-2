"""
MISP Service - Main Integration Service
Aggregates all MISP-related services for unified access

This service provides the main interface for MISP functionality
within the modular monolith architecture.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from .base_service import BaseService
from .misp.attributes_service import AttributesService
from .misp.auth_service import AuthService
from .misp.events_service import EventsService
from .misp.external_apis_service import ExternalApisService
from .misp.feed_parser import FeedParser
from .misp.organizations_service import OrganizationsService

logger = logging.getLogger(__name__)


class MISPService(BaseService):
    """
    Main MISP integration service that coordinates all MISP functionality
    """

    def __init__(self):
        super().__init__()
        self.events_service = EventsService()
        self.attributes_service = AttributesService()
        self.organizations_service = OrganizationsService()
        self.auth_service = AuthService()
        self.external_apis_service = ExternalApisService()
        self.feed_parser = FeedParser()

        self.initialized = False

    async def initialize(self) -> bool:
        """Initialize all MISP services"""
        try:
            # Initialize component services
            await self.events_service.initialize()
            await self.attributes_service.initialize()
            await self.organizations_service.initialize()
            await self.auth_service.initialize()
            await self.external_apis_service.initialize()
            await self.feed_parser.initialize()

            self.initialized = True
            logger.info("MISP service initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize MISP service: {e}")
            return False

    # Event Management
    async def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new MISP event"""
        return await self.events_service.create_event(event_data)

    async def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get MISP event by ID"""
        return await self.events_service.get_event(event_id)

    async def update_event(self, event_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update MISP event"""
        return await self.events_service.update_event(event_id, event_data)

    async def delete_event(self, event_id: str) -> bool:
        """Delete MISP event"""
        return await self.events_service.delete_event(event_id)

    async def list_events(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """List MISP events with optional filters"""
        return await self.events_service.list_events(filters)

    # Attribute Management
    async def create_attribute(self, attribute_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new MISP attribute"""
        return await self.attributes_service.create_attribute(attribute_data)

    async def get_attribute(self, attribute_id: str) -> Optional[Dict[str, Any]]:
        """Get MISP attribute by ID"""
        return await self.attributes_service.get_attribute(attribute_id)

    async def correlate_attributes(self, attribute_id: str) -> List[Dict[str, Any]]:
        """Get correlations for attribute"""
        return await self.attributes_service.correlate_attributes(attribute_id)

    async def search_attributes(self, search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Search MISP attributes"""
        return await self.attributes_service.search_attributes(search_params)

    # Organization Management
    async def get_organizations(self) -> List[Dict[str, Any]]:
        """Get all organizations"""
        return await self.organizations_service.get_organizations()

    async def get_organization(self, org_id: str) -> Optional[Dict[str, Any]]:
        """Get organization by ID"""
        return await self.organizations_service.get_organization(org_id)

    # Search and Analysis
    async def search(self, query: str, search_type: str = "all") -> Dict[str, Any]:
        """Universal search across MISP data"""
        results = {
            "events": [],
            "attributes": [],
            "query": query,
            "search_type": search_type,
            "timestamp": datetime.utcnow().isoformat()
        }

        if search_type in ["all", "events"]:
            event_results = await self.events_service.search_events(query)
            results["events"] = event_results

        if search_type in ["all", "attributes"]:
            attribute_results = await self.attributes_service.search_attributes({"value": query})
            results["attributes"] = attribute_results

        return results

    # Import/Export
    async def import_data(self, data: Dict[str, Any], data_format: str = "misp_json") -> Dict[str, Any]:
        """Import data into MISP"""
        if data_format == "misp_json":
            return await self._import_misp_json(data)
        elif data_format == "stix":
            return await self._import_stix(data)
        else:
            raise ValueError(f"Unsupported import format: {data_format}")

    async def export_data(self, export_params: Dict[str, Any]) -> Dict[str, Any]:
        """Export MISP data"""
        export_format = export_params.get("format", "misp_json")

        if export_format == "misp_json":
            return await self._export_misp_json(export_params)
        elif export_format == "stix":
            return await self._export_stix(export_params)
        else:
            raise ValueError(f"Unsupported export format: {export_format}")

    # Feed Management
    async def process_feed(self, feed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process external threat intelligence feed"""
        return await self.feed_parser.process_feed(feed_data)

    # Health and Status
    async def get_status(self) -> Dict[str, Any]:
        """Get MISP service status"""
        return {
            "service": "MISP",
            "status": "healthy" if self.initialized else "initializing",
            "initialized": self.initialized,
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "events_service": await self.events_service.get_status(),
                "attributes_service": await self.attributes_service.get_status(),
                "organizations_service": await self.organizations_service.get_status(),
                "auth_service": await self.auth_service.get_status(),
                "external_apis_service": await self.external_apis_service.get_status(),
                "feed_parser": await self.feed_parser.get_status()
            }
        }

    # Private helper methods
    async def _import_misp_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Import MISP JSON format data"""
        # Implementation for MISP JSON import
        return {"status": "success", "imported": 0}

    async def _import_stix(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Import STIX format data"""
        # Implementation for STIX import
        return {"status": "success", "imported": 0}

    async def _export_misp_json(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Export data in MISP JSON format"""
        # Implementation for MISP JSON export
        return {"status": "success", "exported": 0}

    async def _export_stix(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Export data in STIX format"""
        # Implementation for STIX export
        return {"status": "success", "exported": 0}


# Singleton instance
misp_service = MISPService()


async def get_misp_service() -> MISPService:
    """Get the MISP service instance"""
    if not misp_service.initialized:
        await misp_service.initialize()
    return misp_service
