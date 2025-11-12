"""
Platform Session model for unified authentication across all 37 tools.

Constitutional Requirements:
- Single sign-on across all domains
- JWT-based authentication
- Session persistence and restoration
- Cross-tool workflow state preservation
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class PlatformSession(Base):
    """
    Platform session for unified authentication and state management.

    Supports constitutional requirements including:
    - Single sign-on across all 37 tools
    - Cross-domain workflow state preservation
    - Executive function continuity support
    - Session restoration after disconnection
    """

    __tablename__ = "platform_sessions"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # FK to users

    # Authentication details
    jwt_token = Column(Text, nullable=False)  # JWT token for authentication
    refresh_token = Column(String(255), nullable=True)  # Refresh token
    token_expires_at = Column(DateTime(timezone=True), nullable=False)

    # Session metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # Session state
    is_active = Column(Boolean, default=True)
    device_info = Column(JSON, default=lambda: {})  # Device and browser info
    ip_address = Column(String(45), nullable=True)  # IPv4/IPv6 address
    user_agent = Column(String(500), nullable=True)  # Browser user agent

    # Cross-tool workflow state
    current_domain = Column(String(50), nullable=True)  # Current active domain
    current_tool = Column(String(100), nullable=True)  # Current active tool
    workflow_state = Column(JSON, default=lambda: {})  # Cross-tool state

    # Executive function support
    context_data = Column(JSON, default=lambda: {
        "active_workflows": [],  # List of active workflows
        "recent_tools": [],      # Recently used tools for quick access
        "pinned_views": [],      # User-pinned views for quick access
        "focus_mode_active": False,  # Is focus mode currently active
        "last_domain_views": {},     # Last view in each domain
        "interrupted_tasks": [],     # Tasks interrupted for later resumption
        "notification_preferences": {},  # Session-specific notifications
    })

    # Performance tracking
    response_times = Column(JSON, default=lambda: {})  # Track response times
    feature_usage = Column(JSON, default=lambda: {})   # Track feature usage

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.expires_at:
            # Default 24-hour session (constitutional offline capability)
            self.expires_at = datetime.utcnow() + timedelta(hours=24)

    def is_expired(self) -> bool:
        """Check if session has expired."""
        return datetime.utcnow() > self.expires_at

    def is_token_expired(self) -> bool:
        """Check if JWT token has expired."""
        return datetime.utcnow() > self.token_expires_at

    def extend_session(self, hours: int = 24) -> None:
        """Extend session by specified hours."""
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
        self.last_activity = datetime.utcnow()

    def update_activity(self) -> None:
        """Update last activity timestamp."""
        self.last_activity = datetime.utcnow()

    def set_current_context(self, domain: str, tool: str) -> None:
        """Set current domain and tool context."""
        self.current_domain = domain
        self.current_tool = tool
        self.update_activity()

        # Update context data
        if not self.context_data:
            self.context_data = {}

        # Add to recent tools
        recent = self.context_data.get("recent_tools", [])
        tool_entry = {"domain": domain, "tool": tool,
                      "timestamp": datetime.utcnow().isoformat()}

        # Remove if already exists and add to front
        recent = [r for r in recent if not (
            r.get("domain") == domain and r.get("tool") == tool)]
        recent.insert(0, tool_entry)

        # Keep only last 10 recent tools
        self.context_data["recent_tools"] = recent[:10]

        # Update last domain view
        if "last_domain_views" not in self.context_data:
            self.context_data["last_domain_views"] = {}
        self.context_data["last_domain_views"][domain] = tool

    def add_active_workflow(self, workflow_id: str, workflow_data: Dict[str, Any]) -> None:
        """Add an active workflow to track cross-tool state."""
        if not self.workflow_state:
            self.workflow_state = {}

        self.workflow_state[workflow_id] = {
            "data": workflow_data,
            "started_at": datetime.utcnow().isoformat(),
            "last_updated": datetime.utcnow().isoformat(),
            "domain": self.current_domain,
            "tool": self.current_tool,
        }

        # Update context data
        if not self.context_data:
            self.context_data = {}

        active_workflows = self.context_data.get("active_workflows", [])
        if workflow_id not in active_workflows:
            active_workflows.append(workflow_id)
            self.context_data["active_workflows"] = active_workflows

    def update_workflow_state(self, workflow_id: str, workflow_data: Dict[str, Any]) -> None:
        """Update existing workflow state."""
        if self.workflow_state and workflow_id in self.workflow_state:
            self.workflow_state[workflow_id]["data"] = workflow_data
            self.workflow_state[workflow_id]["last_updated"] = datetime.utcnow(
            ).isoformat()

    def complete_workflow(self, workflow_id: str) -> None:
        """Mark workflow as completed and clean up."""
        if self.workflow_state and workflow_id in self.workflow_state:
            self.workflow_state[workflow_id]["completed_at"] = datetime.utcnow(
            ).isoformat()

        # Remove from active workflows
        if self.context_data and "active_workflows" in self.context_data:
            active = self.context_data["active_workflows"]
            self.context_data["active_workflows"] = [
                w for w in active if w != workflow_id]

    def get_recent_tools(self, limit: int = 10) -> list:
        """Get recently used tools for quick access."""
        if not self.context_data:
            return []
        return self.context_data.get("recent_tools", [])[:limit]

    def get_active_workflows(self) -> list:
        """Get list of active workflow IDs."""
        if not self.context_data:
            return []
        return self.context_data.get("active_workflows", [])

    def set_focus_mode(self, active: bool) -> None:
        """Set focus mode state for executive function support."""
        if not self.context_data:
            self.context_data = {}
        self.context_data["focus_mode_active"] = active

    def is_focus_mode_active(self) -> bool:
        """Check if focus mode is currently active."""
        if not self.context_data:
            return False
        return self.context_data.get("focus_mode_active", False)

    def record_response_time(self, endpoint: str, response_time_ms: int) -> None:
        """Record response time for performance monitoring."""
        if not self.response_times:
            self.response_times = {}

        if endpoint not in self.response_times:
            self.response_times[endpoint] = []

        self.response_times[endpoint].append({
            "time": response_time_ms,
            "timestamp": datetime.utcnow().isoformat()
        })

        # Keep only last 100 measurements per endpoint
        self.response_times[endpoint] = self.response_times[endpoint][-100:]

    def get_average_response_time(self, endpoint: str) -> Optional[float]:
        """Get average response time for an endpoint."""
        if not self.response_times or endpoint not in self.response_times:
            return None

        times = [r["time"] for r in self.response_times[endpoint]]
        return sum(times) / len(times) if times else None

    def invalidate(self) -> None:
        """Invalidate the session."""
        self.is_active = False
        self.expires_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "is_active": self.is_active,
            "current_domain": self.current_domain,
            "current_tool": self.current_tool,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "context_data": self.context_data or {},
            "recent_tools": self.get_recent_tools(),
            "active_workflows": self.get_active_workflows(),
            "focus_mode_active": self.is_focus_mode_active(),
        }

    def __repr__(self) -> str:
        return (
            f"<PlatformSession(id={self.id}, session_id='{self.session_id}', "
            f"user_id={self.user_id}, active={self.is_active})>"
        )
