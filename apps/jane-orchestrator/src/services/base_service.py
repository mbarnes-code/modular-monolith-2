"""
Base Service Class

Provides common functionality for all services in the Jane orchestrator.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict


class BaseService(ABC):
    """Base class for all Jane orchestrator services."""

    def __init__(self, service_name: str):
        """Initialize base service."""
        self.service_name = service_name
        self.is_healthy = False
        self.created_at = datetime.now()

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the service."""
        pass

    async def get_health_status(self) -> Dict[str, Any]:
        """Get service health status."""
        return {
            'service': self.service_name,
            'healthy': self.is_healthy,
            'created_at': self.created_at.isoformat(),
            'timestamp': datetime.now().isoformat()
        }

    async def cleanup(self) -> None:
        """Cleanup service resources."""
        pass
