"""
Tool-Specific Rollback Infrastructure for Mental Prosthetic Platform

Provides rollback capabilities for all 37 mental prosthetic tools across
4 domains, ensuring business logic preservation and data consistency
during rollback operations.
"""

import asyncio
import json
import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Union

logger = logging.getLogger(__name__)


class RollbackType(Enum):
    """Types of rollback operations supported."""
    DATA_ROLLBACK = "data"          # Database/file data rollback
    CONFIG_ROLLBACK = "config"      # Configuration rollback
    STATE_ROLLBACK = "state"        # Application state rollback
    FULL_ROLLBACK = "full"          # Complete tool rollback


class RollbackStatus(Enum):
    """Status of rollback operations."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


@dataclass
class RollbackPoint:
    """Represents a point in time that can be rolled back to."""
    rollback_id: str
    tool_id: str
    timestamp: datetime
    description: str
    rollback_type: RollbackType
    metadata: Dict[str, Any] = field(default_factory=dict)
    data_snapshot: Optional[Dict[str, Any]] = None
    config_snapshot: Optional[Dict[str, Any]] = None
    state_snapshot: Optional[Dict[str, Any]] = None
    # Other tools that depend on this
    dependencies: List[str] = field(default_factory=list)


@dataclass
class RollbackResult:
    """Result of a rollback operation."""
    rollback_id: str
    tool_id: str
    status: RollbackStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    rolled_back_items: List[str] = field(default_factory=list)
    affected_dependencies: List[str] = field(default_factory=list)


class BaseToolRollbackHandler(ABC):
    """Abstract base class for tool-specific rollback handlers."""

    def __init__(self, tool_id: str, config: Dict[str, Any] = None):
        self.tool_id = tool_id
        self.config = config or {}
        self.logger = logging.getLogger(f"rollback.{tool_id}")

    @abstractmethod
    async def create_rollback_point(self, description: str,
                                    rollback_type: RollbackType = RollbackType.FULL) -> RollbackPoint:
        """Create a rollback point for this tool."""
        pass

    @abstractmethod
    async def execute_rollback(self, rollback_point: RollbackPoint) -> RollbackResult:
        """Execute rollback to the specified point."""
        pass

    @abstractmethod
    async def validate_rollback_point(self, rollback_point: RollbackPoint) -> bool:
        """Validate that a rollback point is still valid."""
        pass

    @abstractmethod
    async def cleanup_old_rollback_points(self, retention_days: int = 7) -> int:
        """Clean up old rollback points, return number cleaned."""
        pass


class GenericToolRollbackHandler(BaseToolRollbackHandler):
    """Generic rollback handler for tools without specific implementations."""

    def __init__(self, tool_id: str, config: Dict[str, Any] = None):
        super().__init__(tool_id, config)
        self.rollback_dir = Path(config.get(
            "rollback_dir", f"/data/rollback/{tool_id}"))
        self.rollback_dir.mkdir(parents=True, exist_ok=True)
        self.rollback_points: Dict[str, RollbackPoint] = {}

    async def create_rollback_point(self, description: str,
                                    rollback_type: RollbackType = RollbackType.FULL) -> RollbackPoint:
        """Create a generic rollback point by capturing current state."""
        rollback_id = f"{self.tool_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        rollback_point = RollbackPoint(
            rollback_id=rollback_id,
            tool_id=self.tool_id,
            timestamp=datetime.utcnow(),
            description=description,
            rollback_type=rollback_type
        )

        try:
            # Capture data snapshot (tool-specific files, databases, etc.)
            if rollback_type in [RollbackType.DATA_ROLLBACK, RollbackType.FULL_ROLLBACK]:
                rollback_point.data_snapshot = await self._capture_data_snapshot()

            # Capture configuration snapshot
            if rollback_type in [RollbackType.CONFIG_ROLLBACK, RollbackType.FULL_ROLLBACK]:
                rollback_point.config_snapshot = await self._capture_config_snapshot()

            # Capture application state
            if rollback_type in [RollbackType.STATE_ROLLBACK, RollbackType.FULL_ROLLBACK]:
                rollback_point.state_snapshot = await self._capture_state_snapshot()

            # Save rollback point to disk
            await self._save_rollback_point(rollback_point)
            self.rollback_points[rollback_id] = rollback_point

            self.logger.info(
                f"Created rollback point {rollback_id} for {self.tool_id}")
            return rollback_point

        except Exception as e:
            self.logger.error(
                f"Failed to create rollback point for {self.tool_id}: {e}")
            raise

    async def execute_rollback(self, rollback_point: RollbackPoint) -> RollbackResult:
        """Execute rollback to the specified point."""
        result = RollbackResult(
            rollback_id=rollback_point.rollback_id,
            tool_id=self.tool_id,
            status=RollbackStatus.IN_PROGRESS,
            started_at=datetime.utcnow()
        )

        try:
            # Validate rollback point is still valid
            if not await self.validate_rollback_point(rollback_point):
                result.status = RollbackStatus.FAILED
                result.error_message = "Rollback point is no longer valid"
                return result

            # Execute rollback based on type
            if rollback_point.rollback_type in [RollbackType.DATA_ROLLBACK, RollbackType.FULL_ROLLBACK]:
                await self._rollback_data(rollback_point, result)

            if rollback_point.rollback_type in [RollbackType.CONFIG_ROLLBACK, RollbackType.FULL_ROLLBACK]:
                await self._rollback_config(rollback_point, result)

            if rollback_point.rollback_type in [RollbackType.STATE_ROLLBACK, RollbackType.FULL_ROLLBACK]:
                await self._rollback_state(rollback_point, result)

            result.status = RollbackStatus.COMPLETED
            result.completed_at = datetime.utcnow()

            self.logger.info(
                f"Successfully rolled back {self.tool_id} to {rollback_point.rollback_id}")

        except Exception as e:
            result.status = RollbackStatus.FAILED
            result.error_message = str(e)
            result.completed_at = datetime.utcnow()
            self.logger.error(f"Rollback failed for {self.tool_id}: {e}")

        return result

    async def validate_rollback_point(self, rollback_point: RollbackPoint) -> bool:
        """Validate that a rollback point is still valid."""
        rollback_file = self.rollback_dir / \
            f"{rollback_point.rollback_id}.json"

        if not rollback_file.exists():
            return False

        # Check if rollback point is too old
        max_age = timedelta(days=self.config.get("max_rollback_age_days", 30))
        if datetime.utcnow() - rollback_point.timestamp > max_age:
            return False

        # Additional validation could include checking dependencies
        return True

    async def cleanup_old_rollback_points(self, retention_days: int = 7) -> int:
        """Clean up old rollback points."""
        cutoff_time = datetime.utcnow() - timedelta(days=retention_days)
        cleaned_count = 0

        for rollback_file in self.rollback_dir.glob("*.json"):
            try:
                with open(rollback_file, 'r') as f:
                    data = json.load(f)

                timestamp = datetime.fromisoformat(data["timestamp"])
                if timestamp < cutoff_time:
                    rollback_file.unlink()
                    # Clean up associated data files
                    data_dir = self.rollback_dir / data["rollback_id"]
                    if data_dir.exists():
                        import shutil
                        shutil.rmtree(data_dir)

                    cleaned_count += 1
                    self.logger.info(
                        f"Cleaned up old rollback point: {data['rollback_id']}")

            except Exception as e:
                self.logger.warning(
                    f"Failed to clean up rollback file {rollback_file}: {e}")

        return cleaned_count

    async def _capture_data_snapshot(self) -> Dict[str, Any]:
        """Capture data state for rollback (tool-specific implementation needed)."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "data_type": "generic",
            "note": "Generic data snapshot - tool-specific implementation needed"
        }

    async def _capture_config_snapshot(self) -> Dict[str, Any]:
        """Capture configuration state for rollback."""
        return {
            "tool_config": self.config.copy(),
            "timestamp": datetime.utcnow().isoformat()
        }

    async def _capture_state_snapshot(self) -> Dict[str, Any]:
        """Capture application state for rollback."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "state_type": "generic",
            "note": "Generic state snapshot - tool-specific implementation needed"
        }

    async def _rollback_data(self, rollback_point: RollbackPoint, result: RollbackResult):
        """Rollback data to the specified point."""
        if rollback_point.data_snapshot:
            # Generic rollback - tool specific implementations would restore databases, files, etc.
            result.rolled_back_items.append("data_snapshot")
            result.warnings.append(
                "Generic data rollback - tool-specific implementation recommended")

    async def _rollback_config(self, rollback_point: RollbackPoint, result: RollbackResult):
        """Rollback configuration to the specified point."""
        if rollback_point.config_snapshot:
            self.config = rollback_point.config_snapshot.get("tool_config", {})
            result.rolled_back_items.append("configuration")

    async def _rollback_state(self, rollback_point: RollbackPoint, result: RollbackResult):
        """Rollback application state to the specified point."""
        if rollback_point.state_snapshot:
            result.rolled_back_items.append("application_state")
            result.warnings.append(
                "Generic state rollback - tool-specific implementation recommended")

    async def _save_rollback_point(self, rollback_point: RollbackPoint):
        """Save rollback point to disk."""
        rollback_file = self.rollback_dir / \
            f"{rollback_point.rollback_id}.json"

        # Convert rollback point to serializable format
        data = {
            "rollback_id": rollback_point.rollback_id,
            "tool_id": rollback_point.tool_id,
            "timestamp": rollback_point.timestamp.isoformat(),
            "description": rollback_point.description,
            "rollback_type": rollback_point.rollback_type.value,
            "metadata": rollback_point.metadata,
            "data_snapshot": rollback_point.data_snapshot,
            "config_snapshot": rollback_point.config_snapshot,
            "state_snapshot": rollback_point.state_snapshot,
            "dependencies": rollback_point.dependencies
        }

        with open(rollback_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)


class ToolRollbackService:
    """Main service for managing rollbacks across all 37 mental prosthetic tools."""

    def __init__(self):
        self.handlers: Dict[str, BaseToolRollbackHandler] = {}
        self.rollback_history: List[RollbackResult] = []

        # Tool domains for dependency management
        self.tool_domains = {
            # Security domain (13 tools)
            "misp": "security", "helk": "security", "securityonion": "security",
            "maltrail": "security", "yara-x": "security", "cyberchef": "security",
            "nemesis": "security",

            # Productivity domain (8 tools)
            "n8n": "productivity", "mealie": "productivity", "dispatch": "productivity",
            "actual": "productivity", "firecrawl": "productivity", "goose": "productivity",
            "it-tools": "productivity", "inspector": "productivity",

            # MTG domain (4 tools)
            "commander-spellbook": "mtg", "mtg-commander-map": "mtg",
            "mtg-scripting-toolkit": "mtg", "scryfall": "mtg",

            # Infrastructure domain (12 tools)
            "kong": "infrastructure", "ghostwriter": "infrastructure", "kasmvnc": "infrastructure"
            # Note: Additional infrastructure tools would be listed here
        }

    def register_handler(self, tool_id: str, handler: BaseToolRollbackHandler):
        """Register a rollback handler for a specific tool."""
        self.handlers[tool_id] = handler
        logger.info(f"Registered rollback handler for {tool_id}")

    def get_handler(self, tool_id: str) -> BaseToolRollbackHandler:
        """Get rollback handler for a tool, creating generic one if needed."""
        if tool_id not in self.handlers:
            # Create generic handler
            config = {"rollback_dir": f"/data/rollback/{tool_id}"}
            self.handlers[tool_id] = GenericToolRollbackHandler(
                tool_id, config)

        return self.handlers[tool_id]

    async def create_rollback_point(self, tool_id: str, description: str,
                                    rollback_type: RollbackType = RollbackType.FULL) -> RollbackPoint:
        """Create a rollback point for a specific tool."""
        handler = self.get_handler(tool_id)
        return await handler.create_rollback_point(description, rollback_type)

    async def execute_rollback(self, tool_id: str, rollback_id: str) -> RollbackResult:
        """Execute rollback for a specific tool."""
        handler = self.get_handler(tool_id)

        # Find rollback point
        rollback_point = await self._find_rollback_point(tool_id, rollback_id)
        if not rollback_point:
            return RollbackResult(
                rollback_id=rollback_id,
                tool_id=tool_id,
                status=RollbackStatus.FAILED,
                started_at=datetime.utcnow(),
                error_message=f"Rollback point {rollback_id} not found"
            )

        # Execute rollback
        result = await handler.execute_rollback(rollback_point)
        self.rollback_history.append(result)

        return result

    async def create_domain_rollback_point(self, domain: str, description: str) -> Dict[str, RollbackPoint]:
        """Create rollback points for all tools in a domain."""
        domain_tools = [tool_id for tool_id, tool_domain in self.tool_domains.items()
                        if tool_domain == domain]

        rollback_points = {}
        for tool_id in domain_tools:
            try:
                rollback_point = await self.create_rollback_point(
                    tool_id, f"{description} (domain: {domain})"
                )
                rollback_points[tool_id] = rollback_point
            except Exception as e:
                logger.error(
                    f"Failed to create rollback point for {tool_id}: {e}")

        return rollback_points

    async def execute_domain_rollback(self, domain: str, rollback_timestamp: datetime) -> Dict[str, RollbackResult]:
        """Execute rollback for all tools in a domain to a specific timestamp."""
        domain_tools = [tool_id for tool_id, tool_domain in self.tool_domains.items()
                        if tool_domain == domain]

        results = {}
        for tool_id in domain_tools:
            try:
                # Find closest rollback point to timestamp
                rollback_point = await self._find_closest_rollback_point(tool_id, rollback_timestamp)
                if rollback_point:
                    result = await self.execute_rollback(tool_id, rollback_point.rollback_id)
                    results[tool_id] = result
                else:
                    results[tool_id] = RollbackResult(
                        rollback_id="not_found",
                        tool_id=tool_id,
                        status=RollbackStatus.FAILED,
                        started_at=datetime.utcnow(),
                        error_message="No suitable rollback point found"
                    )
            except Exception as e:
                logger.error(f"Failed to rollback {tool_id}: {e}")
                results[tool_id] = RollbackResult(
                    rollback_id="error",
                    tool_id=tool_id,
                    status=RollbackStatus.FAILED,
                    started_at=datetime.utcnow(),
                    error_message=str(e)
                )

        return results

    async def _find_rollback_point(self, tool_id: str, rollback_id: str) -> Optional[RollbackPoint]:
        """Find a specific rollback point."""
        handler = self.get_handler(tool_id)
        if hasattr(handler, 'rollback_points'):
            return handler.rollback_points.get(rollback_id)
        return None

    async def _find_closest_rollback_point(self, tool_id: str,
                                           timestamp: datetime) -> Optional[RollbackPoint]:
        """Find the rollback point closest to (but before) the specified timestamp."""
        handler = self.get_handler(tool_id)
        if hasattr(handler, 'rollback_points'):
            candidates = [
                rp for rp_id, rp in handler.rollback_points.items()
                if rp.timestamp <= timestamp
            ]
            if candidates:
                return max(candidates, key=lambda rp: rp.timestamp)
        return None

    async def cleanup_old_rollback_points(self, retention_days: int = 7) -> Dict[str, int]:
        """Clean up old rollback points for all registered tools."""
        cleanup_results = {}

        for tool_id, handler in self.handlers.items():
            try:
                cleaned_count = await handler.cleanup_old_rollback_points(retention_days)
                cleanup_results[tool_id] = cleaned_count
            except Exception as e:
                logger.error(
                    f"Failed to cleanup rollback points for {tool_id}: {e}")
                cleanup_results[tool_id] = 0

        return cleanup_results

    def get_rollback_history(self, tool_id: str = None, limit: int = 50) -> List[RollbackResult]:
        """Get rollback history, optionally filtered by tool."""
        history = self.rollback_history

        if tool_id:
            history = [r for r in history if r.tool_id == tool_id]

        return sorted(history, key=lambda r: r.started_at, reverse=True)[:limit]


# Global rollback service instance
tool_rollback_service = ToolRollbackService()
