"""
WebSocket infrastructure for real-time synchronization across domains.
Supports executive function accommodations with <250ms latency.

This module provides the foundation for real-time communication between
the Mental Prosthetic Platform's 37 integrated tools.
"""

import json
import logging
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class MessageType(str, Enum):
    """WebSocket message types for domain communication."""
    # Executive function support
    CONTEXT_SWITCH = "context_switch"
    FOCUS_MAINTENANCE = "focus_maintenance"
    TASK_STATUS = "task_status"

    # Domain-specific events
    SECURITY_ALERT = "security_alert"
    PRODUCTIVITY_UPDATE = "productivity_update"
    MTG_ANALYSIS = "mtg_analysis"
    INFRASTRUCTURE_STATUS = "infrastructure_status"

    # Cross-domain sync
    DATA_SYNC = "data_sync"
    PREFERENCE_UPDATE = "preference_update"
    ROLLBACK_EVENT = "rollback_event"

    # System events
    PERFORMANCE_METRIC = "performance_metric"
    ERROR_EVENT = "error_event"
    HEARTBEAT = "heartbeat"


class WebSocketMessage:
    """Standard WebSocket message format."""

    def __init__(self, message_type: MessageType, data: Dict[str, Any],
                 user_id: Optional[str] = None,
                 timestamp: Optional[datetime] = None):
        self.type = message_type
        self.data = data
        self.user_id = user_id
        self.timestamp = timestamp or datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for JSON serialization."""
        return {
            "type": self.type,
            "data": self.data,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat()
        }

    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, json_str: str) -> 'WebSocketMessage':
        """Create message from JSON string."""
        data = json.loads(json_str)
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(
            timestamp_str) if timestamp_str else None
        return cls(
            message_type=MessageType(data["type"]),
            data=data.get("data", {}),
            user_id=data.get("user_id"),
            timestamp=timestamp
        )


class ConnectionMetadata:
    """Metadata for WebSocket connections to support executive function."""

    def __init__(self, user_id: str, domain: Optional[str] = None,
                 focus_mode: bool = False, performance_tier: str = "default"):
        self.user_id = user_id
        self.connected_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()
        self.active_domain = domain
        self.focus_mode = focus_mode
        self.performance_tier = performance_tier
        self.message_count = 0
        self.latency_violations = 0

    def update_activity(self):
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()
        self.message_count += 1

    def record_latency_violation(self):
        """Record a latency violation for monitoring."""
        self.latency_violations += 1
        logger.warning(
            f"Latency violation recorded for user {self.user_id}. Total: {self.latency_violations}")


class PerformanceMonitor:
    """Monitor WebSocket performance for executive function requirements."""

    # Domain-specific performance thresholds (milliseconds)
    DOMAIN_THRESHOLDS = {
        "security": 1000,      # 1s for security domain
        "productivity": 2000,  # 2s for productivity domain
        "mtg": 3000,          # 3s for MTG domain
        "infrastructure": 5000  # 5s for infrastructure domain
    }

    WEBSOCKET_THRESHOLD = 250  # 250ms for WebSocket latency

    @classmethod
    def check_latency(cls, duration_ms: float, domain: str = "default") -> bool:
        """Check if latency meets performance requirements."""
        threshold = cls.DOMAIN_THRESHOLDS.get(domain, 2000)  # Default 2s
        return duration_ms <= threshold

    @classmethod
    def check_websocket_latency(cls, duration_ms: float) -> bool:
        """Check if WebSocket latency meets executive function requirements."""
        return duration_ms <= cls.WEBSOCKET_THRESHOLD

    @classmethod
    def create_performance_alert(cls, domain: str, actual_latency: float,
                                 threshold: float) -> WebSocketMessage:
        """Create performance alert message."""
        severity = "warning" if actual_latency < threshold * 1.5 else "critical"

        return WebSocketMessage(
            message_type=MessageType.PERFORMANCE_METRIC,
            data={
                "alert": "performance_violation",
                "domain": domain,
                "actual_latency": actual_latency,
                "threshold": threshold,
                "severity": severity
            }
        )


class DataSyncManager:
    """Manage cross-domain data synchronization."""

    def __init__(self):
        self.sync_cache: Dict[str, Dict[str, Any]] = {}
        self.sync_versions: Dict[str, int] = {}

    def create_sync_key(self, user_id: str, domain: str, tool_id: str) -> str:
        """Create standardized sync key."""
        return f"sync:{user_id}:{domain}:{tool_id}"

    def store_sync_data(self, user_id: str, domain: str, tool_id: str,
                        data: Dict[str, Any]) -> WebSocketMessage:
        """Store sync data and create sync message."""
        sync_key = self.create_sync_key(user_id, domain, tool_id)

        # Update version
        self.sync_versions[sync_key] = self.sync_versions.get(sync_key, 0) + 1

        # Store data
        self.sync_cache[sync_key] = {
            "data": data,
            "timestamp": datetime.utcnow(),
            "version": self.sync_versions[sync_key]
        }

        # Create sync message
        return WebSocketMessage(
            message_type=MessageType.DATA_SYNC,
            data={
                "domain": domain,
                "tool_id": tool_id,
                "sync_data": data,
                "version": self.sync_versions[sync_key],
                "source_user": user_id
            },
            user_id=user_id
        )

    def get_sync_data(self, user_id: str, domain: str, tool_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve sync data for specific tool."""
        sync_key = self.create_sync_key(user_id, domain, tool_id)
        return self.sync_cache.get(sync_key)


class PreferenceManager:
    """Manage user preferences with executive function support."""

    def __init__(self):
        self.preferences_cache: Dict[str, Dict[str, Any]] = {}

    def update_preferences(self, user_id: str, preferences: Dict[str, Any]) -> WebSocketMessage:
        """Update user preferences and create update message."""
        self.preferences_cache[user_id] = {
            "preferences": preferences,
            "updated_at": datetime.utcnow()
        }

        return WebSocketMessage(
            message_type=MessageType.PREFERENCE_UPDATE,
            data={
                "preferences": preferences,
                "executive_function_support": {
                    "focus_mode": preferences.get("focus_mode", False),
                    "high_contrast": preferences.get("high_contrast", False),
                    "reduced_motion": preferences.get("reduced_motion", False),
                    "task_reminders": preferences.get("task_reminders", True)
                }
            },
            user_id=user_id
        )

    def get_preferences(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user preferences."""
        return self.preferences_cache.get(user_id)


# Global instances for use by WebSocket handlers
performance_monitor = PerformanceMonitor()
data_sync_manager = DataSyncManager()
preference_manager = PreferenceManager()


def create_context_switch_message(domain: str, focus_mode: bool = False) -> WebSocketMessage:
    """Create context switch message for executive function support."""
    return WebSocketMessage(
        message_type=MessageType.CONTEXT_SWITCH,
        data={
            "new_domain": domain,
            "focus_mode": focus_mode,
            "performance_tier": performance_monitor.DOMAIN_THRESHOLDS.get(domain, 2000),
            "transition_guidance": {
                "expected_response_time": f"<{performance_monitor.DOMAIN_THRESHOLDS.get(domain, 2000)}ms",
                "focus_recommendations": _get_focus_recommendations(domain)
            }
        }
    )


def create_heartbeat_message(status: str = "alive") -> WebSocketMessage:
    """Create heartbeat message for connection health."""
    return WebSocketMessage(
        message_type=MessageType.HEARTBEAT,
        data={
            "status": status,
            "websocket_threshold": performance_monitor.WEBSOCKET_THRESHOLD,
            "system_healthy": True
        }
    )


def _get_focus_recommendations(domain: str) -> Dict[str, str]:
    """Get domain-specific focus recommendations for executive function support."""
    recommendations = {
        "security": {
            "priority": "high",
            "cognitive_load": "intense",
            "break_frequency": "every_30_minutes",
            "distraction_level": "minimal"
        },
        "productivity": {
            "priority": "medium",
            "cognitive_load": "moderate",
            "break_frequency": "every_45_minutes",
            "distraction_level": "low"
        },
        "mtg": {
            "priority": "medium",
            "cognitive_load": "analytical",
            "break_frequency": "every_60_minutes",
            "distraction_level": "moderate"
        },
        "infrastructure": {
            "priority": "low",
            "cognitive_load": "light",
            "break_frequency": "every_90_minutes",
            "distraction_level": "high"
        }
    }

    return recommendations.get(domain, recommendations["productivity"])


# WebSocket endpoint handler stubs (to be implemented with FastAPI)
async def handle_websocket_connection(websocket, user_id: str, context: Optional[Dict[str, Any]] = None):
    """
    Handle WebSocket connection with executive function support.

    This function should be implemented in main.py when FastAPI is available.
    It will use the classes and functions defined above.
    """
    pass


async def handle_websocket_message(message_data: str, user_id: str):
    """
    Handle incoming WebSocket message.

    This function should be implemented in main.py when FastAPI is available.
    It will parse messages using WebSocketMessage.from_json() and route them appropriately.
    """
    pass


# Health check functions
def get_websocket_health() -> Dict[str, Any]:
    """Get WebSocket system health status."""
    return {
        "websocket_infrastructure": "ready",
        "performance_monitor": "active",
        "data_sync_manager": "active",
        "preference_manager": "active",
        "executive_function_support": "enabled",
        "domain_thresholds": performance_monitor.DOMAIN_THRESHOLDS,
        "websocket_threshold": performance_monitor.WEBSOCKET_THRESHOLD,
        "timestamp": datetime.utcnow().isoformat()
    }


def validate_websocket_config() -> bool:
    """Validate WebSocket configuration for production readiness."""
    checks = [
        # Check if all required managers are initialized
        performance_monitor is not None,
        data_sync_manager is not None,
        preference_manager is not None,

        # Check if domain thresholds are configured
        len(performance_monitor.DOMAIN_THRESHOLDS) >= 4,
        performance_monitor.WEBSOCKET_THRESHOLD == 250,

        # Check if message types are complete
        len(MessageType) >= 10
    ]

    return all(checks)


if __name__ == "__main__":
    # Test the WebSocket infrastructure
    print("WebSocket Infrastructure Test")
    print("=" * 30)

    # Test message creation
    test_message = create_heartbeat_message()
    print(f"Heartbeat message: {test_message.to_json()}")

    # Test performance monitoring
    print(
        f"Security domain check (500ms): {performance_monitor.check_latency(500, 'security')}")
    print(
        f"WebSocket latency check (100ms): {performance_monitor.check_websocket_latency(100)}")

    # Test data sync
    sync_msg = data_sync_manager.store_sync_data(
        "user1", "security", "misp", {"alert": "test"})
    print(f"Sync message: {sync_msg.to_json()}")

    # Test configuration
    print(f"Configuration valid: {validate_websocket_config()}")
    print(f"Health status: {get_websocket_health()}")
