"""
User Profile model with ADHD/autism executive function accommodations.

Constitutional Requirements:
- Executive function accommodations for ADHD/autism users
- WCAG 2.1 AA compliance support
- <200ms UI response preferences
- Context switching reduction patterns
"""

from typing import Any, Dict

from sqlalchemy import JSON, Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class UserProfile(Base):
    """
    User profile with executive function accommodations.

    Supports constitutional requirements for ADHD/autism users including:
    - UI preferences for focus maintenance
    - Context switching reduction patterns
    - Accessibility accommodations
    - Performance preferences
    """

    __tablename__ = "user_profiles"

    # Primary identification
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)

    # Executive function accommodations
    adhd_accommodations = Column(JSON, default=lambda: {
        "ui_animations": False,  # Reduce distracting animations
        "focus_mode": True,      # Simplified interface when focused
        "time_awareness": True,  # Show time indicators
        "progress_indicators": True,  # Visual progress feedback
        "interrupt_protection": True,  # Minimize unexpected UI changes
        "consistent_navigation": True,  # Same navigation patterns across tools
        "context_preservation": True,  # Remember where user was working
        "task_breakdown": True,  # Break complex tasks into steps
    })

    autism_accommodations = Column(JSON, default=lambda: {
        "predictable_patterns": True,    # Consistent UI patterns
        "sensory_considerations": True,  # Reduced sensory overload
        "clear_structure": True,         # Clear visual hierarchy
        "routine_support": True,         # Support for routine workflows
        "change_warnings": True,         # Warn before interface changes
        "detailed_feedback": True,       # Comprehensive status messages
        "preference_stability": True,    # Don't change settings automatically
        "cognitive_load_reduction": True,  # Minimize simultaneous choices
    })

    # UI and performance preferences
    ui_preferences = Column(JSON, default=lambda: {
        "theme": "light",  # light, dark, high-contrast
        "font_size": "medium",  # small, medium, large, extra-large
        "animation_speed": "reduced",  # none, reduced, normal
        "density": "comfortable",  # compact, comfortable, spacious
        "color_coding": True,  # Use colors to organize domains
        "shortcuts_enabled": True,  # Keyboard shortcuts active
        "tooltips_enabled": True,  # Show helpful tooltips
        "confirmation_dialogs": True,  # Confirm destructive actions
        "auto_save": True,  # Auto-save work frequently
        "session_restoration": True,  # Restore previous session
    })

    # Performance and accessibility settings
    performance_preferences = Column(JSON, default=lambda: {
        "response_time_target": 200,  # Target response time in ms
        "preload_frequent_tools": True,  # Preload commonly used tools
        "cache_aggressively": True,  # Use aggressive caching
        "reduce_network_calls": True,  # Minimize API calls
        "offline_support": True,  # Enable offline capabilities
        "background_sync": True,  # Sync in background when possible
    })

    accessibility_preferences = Column(JSON, default=lambda: {
        "screen_reader": False,  # Screen reader compatibility mode
        "high_contrast": False,  # High contrast mode
        "large_text": False,     # Larger text mode
        "keyboard_navigation": True,  # Full keyboard navigation
        "focus_indicators": True,     # Enhanced focus indicators
        "aria_descriptions": True,    # Detailed ARIA descriptions
        "reduced_motion": False,      # Reduce motion and animations
        "color_blind_support": False,  # Color blindness accommodations
    })

    # Domain-specific preferences
    domain_preferences = Column(JSON, default=lambda: {
        "security": {
            "default_view": "dashboard",
            "favorite_tools": [],
            "workflow_templates": [],
            "alert_preferences": "medium",
        },
        "productivity": {
            "default_view": "dashboard",
            "favorite_tools": [],
            "workflow_templates": [],
            "reminder_preferences": "enabled",
        },
        "mtg": {
            "default_view": "commander_spellbook",
            "favorite_tools": [],
            "deck_preferences": {},
            "format_preferences": ["commander"],
        },
        "infrastructure": {
            "default_view": "monitoring",
            "favorite_tools": [],
            "deployment_preferences": {},
            "monitoring_preferences": "detailed",
        }
    })

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    last_login = Column(DateTime(timezone=True), nullable=True)

    def get_executive_function_settings(self) -> Dict[str, Any]:
        """Get combined executive function accommodations."""
        return {
            "adhd": self.adhd_accommodations or {},
            "autism": self.autism_accommodations or {},
            "ui": self.ui_preferences or {},
            "performance": self.performance_preferences or {},
            "accessibility": self.accessibility_preferences or {},
        }

    def get_domain_settings(self, domain: str) -> Dict[str, Any]:
        """Get preferences for a specific domain."""
        return (
            self.domain_preferences.get(domain, {})
            if self.domain_preferences else {}
        )

    def update_preferences(
        self, category: str, preferences: Dict[str, Any]
    ) -> None:
        """Update preferences for a specific category."""
        if category == "adhd":
            self.adhd_accommodations = {
                **(self.adhd_accommodations or {}), **preferences
            }
        elif category == "autism":
            self.autism_accommodations = {
                **(self.autism_accommodations or {}), **preferences
            }
        elif category == "ui":
            self.ui_preferences = {
                **(self.ui_preferences or {}), **preferences
            }
        elif category == "performance":
            self.performance_preferences = {
                **(self.performance_preferences or {}), **preferences
            }
        elif category == "accessibility":
            self.accessibility_preferences = {
                **(self.accessibility_preferences or {}), **preferences
            }
        elif category in ["security", "productivity", "mtg", "infrastructure"]:
            if not self.domain_preferences:
                self.domain_preferences = {}
            self.domain_preferences[category] = {
                **(self.domain_preferences.get(category, {})),
                **preferences
            }

    def should_use_reduced_ui(self) -> bool:
        """Check if user prefers reduced UI complexity."""
        return (
            (self.adhd_accommodations or {}).get("focus_mode", False) or
            (self.autism_accommodations or {}).get(
                "cognitive_load_reduction", False
            )
        )

    def get_response_time_target(self) -> int:
        """Get target response time in milliseconds."""
        return (self.performance_preferences or {}).get(
            "response_time_target", 200
        )

    def __repr__(self) -> str:
        return (
            f"<UserProfile(id={self.id}, username='{self.username}', "
            f"active={self.is_active})>"
        )
