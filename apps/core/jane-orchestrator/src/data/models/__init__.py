"""Data models for Jane Orchestrator."""

from .domain import Domain
from .integrated_tool import IntegratedTool
from .platform_session import PlatformSession
from .user_profile import UserProfile

# Alias for backward compatibility
User = UserProfile

__all__ = [
    "Domain",
    "IntegratedTool",
    "PlatformSession",
    "UserProfile",
    "User"
]
