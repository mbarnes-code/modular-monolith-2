"""
UserProfileService for executive function pattern support.

Constitutional Requirements:
- ADHD/autism accommodation patterns
- Executive function support
- Preference management with accessibility features
- UI response time <200ms optimization
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session

from ..data.models.integrated_tool import IntegratedTool
from ..data.models.user_profile import UserProfile


class UserProfileService:
    """
    Executive function pattern service for ADHD/autism accommodations.

    Core Capabilities:
    - User preference management with executive function support
    - ADHD-friendly UI patterns (<200ms response, focus indicators)
    - Autism-friendly interface accommodations
    - Cross-tool consistency for context switching reduction
    - Performance optimization for cognitive load management
    """

    def __init__(self, db_session: Session):
        self.db = db_session

    def create_user_profile(
        self,
        user_id: str,
        email: str,
        display_name: str,
        adhd_accommodations: Optional[Dict[str, Any]] = None,
        autism_accommodations: Optional[Dict[str, Any]] = None
    ) -> UserProfile:
        """
        Create user profile with executive function accommodations.

        Args:
            user_id: Unique user identifier
            email: User email address
            display_name: User display name
            adhd_accommodations: ADHD-specific accommodation settings
            autism_accommodations: Autism-specific accommodation settings

        Returns:
            Created UserProfile instance
        """
        default_adhd = {
            "focus_indicators": True,
            "reduced_animations": True,
            "high_contrast_mode": False,
            "notification_batching": True,
            "task_breakdown_assistance": True,
            "time_blocking_support": True,
            "distraction_filtering": True,
            "quick_access_patterns": True
        }

        default_autism = {
            "predictable_navigation": True,
            "sensory_accommodations": True,
            "routine_consistency": True,
            "clear_communication": True,
            "stimming_support": False,
            "texture_preferences": {},
            "sound_sensitivity": "medium",
            "visual_processing_aids": True
        }

        default_ui_prefs = {
            "theme": "system",
            "font_size": "medium",
            "color_scheme": "blue",
            "layout_density": "comfortable",
            "sidebar_position": "left",
            "tool_grouping": "domain",
            "quick_actions": [],
            "dashboard_widgets": [
                {"type": "tool_status", "position": 0},
                {"type": "recent_activities", "position": 1},
                {"type": "performance_metrics", "position": 2}
            ]
        }

        default_perf_prefs = {
            "max_concurrent_tools": 5,
            "cache_strategy": "aggressive",
            "preload_favorites": True,
            "background_updates": True,
            "response_time_target": 150,  # ms
            "offline_sync_interval": 300,  # seconds
            "data_retention_days": 90
        }

        merged_adhd = {**default_adhd, **(adhd_accommodations or {})}
        merged_autism = {**default_autism, **(autism_accommodations or {})}

        profile = UserProfile(
            user_id=user_id,
            email=email,
            display_name=display_name,
            adhd_accommodations=merged_adhd,
            autism_accommodations=merged_autism,
            ui_preferences=default_ui_prefs,
            performance_preferences=default_perf_prefs
        )

        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)

        return profile

    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by user ID."""
        return self.db.query(UserProfile).filter(
            UserProfile.user_id == user_id
        ).first()

    def update_adhd_accommodations(
        self,
        user_id: str,
        accommodations: Dict[str, Any]
    ) -> Optional[UserProfile]:
        """
        Update ADHD accommodation settings with validation.

        Args:
            user_id: User identifier
            accommodations: ADHD accommodation settings to update

        Returns:
            Updated UserProfile or None if user not found
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return None

        # Validate accommodation settings
        valid_adhd_keys = {
            "focus_indicators", "reduced_animations", "high_contrast_mode",
            "notification_batching", "task_breakdown_assistance",
            "time_blocking_support", "distraction_filtering",
            "quick_access_patterns"
        }

        validated_accommodations = {
            key: value for key, value in accommodations.items()
            if key in valid_adhd_keys
        }

        # Merge with existing accommodations
        current_accommodations = profile.adhd_accommodations or {}
        updated_accommodations = {
            **current_accommodations,
            **validated_accommodations
        }

        profile.adhd_accommodations = updated_accommodations
        profile.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(profile)

        return profile

    def update_autism_accommodations(
        self,
        user_id: str,
        accommodations: Dict[str, Any]
    ) -> Optional[UserProfile]:
        """
        Update autism accommodation settings with validation.

        Args:
            user_id: User identifier
            accommodations: Autism accommodation settings to update

        Returns:
            Updated UserProfile or None if user not found
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return None

        # Validate accommodation settings
        valid_autism_keys = {
            "predictable_navigation", "sensory_accommodations",
            "routine_consistency", "clear_communication", "stimming_support",
            "texture_preferences", "sound_sensitivity", "visual_processing_aids"
        }

        validated_accommodations = {
            key: value for key, value in accommodations.items()
            if key in valid_autism_keys
        }

        # Merge with existing accommodations
        current_accommodations = profile.autism_accommodations or {}
        updated_accommodations = {
            **current_accommodations,
            **validated_accommodations
        }

        profile.autism_accommodations = updated_accommodations
        profile.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(profile)

        return profile

    def update_ui_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> Optional[UserProfile]:
        """
        Update UI preferences with executive function optimization.

        Args:
            user_id: User identifier
            preferences: UI preference settings to update

        Returns:
            Updated UserProfile or None if user not found
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return None

        # Validate UI preference settings
        valid_ui_keys = {
            "theme", "font_size", "color_scheme", "layout_density",
            "sidebar_position", "tool_grouping", "quick_actions",
            "dashboard_widgets"
        }

        validated_preferences = {
            key: value for key, value in preferences.items()
            if key in valid_ui_keys
        }

        # Merge with existing preferences
        current_preferences = profile.ui_preferences or {}
        updated_preferences = {
            **current_preferences,
            **validated_preferences
        }

        profile.ui_preferences = updated_preferences
        profile.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(profile)

        return profile

    def get_executive_function_config(self, user_id: str) -> Dict[str, Any]:
        """
        Get executive function configuration for UI optimization.

        Returns optimized configuration for ADHD/autism accommodations
        including response time targets and cognitive load settings.
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return self._get_default_executive_config()

        adhd_config = profile.adhd_accommodations or {}
        autism_config = profile.autism_accommodations or {}
        ui_config = profile.ui_preferences or {}
        perf_config = profile.performance_preferences or {}

        # Build executive function configuration
        config = {
            "response_time_target": perf_config.get("response_time_target", 150),
            "focus_indicators": adhd_config.get("focus_indicators", True),
            "reduced_animations": adhd_config.get("reduced_animations", True),
            "predictable_navigation": autism_config.get("predictable_navigation", True),
            "sensory_accommodations": autism_config.get("sensory_accommodations", True),
            "cognitive_load_level": self._calculate_cognitive_load(profile),
            "notification_strategy": self._get_notification_strategy(profile),
            "ui_optimization": {
                "preload_favorites": perf_config.get("preload_favorites", True),
                "cache_strategy": perf_config.get("cache_strategy", "aggressive"),
                "max_concurrent_tools": perf_config.get("max_concurrent_tools", 5),
                "layout_density": ui_config.get("layout_density", "comfortable")
            },
            "accessibility_features": {
                "high_contrast": adhd_config.get("high_contrast_mode", False),
                "sound_sensitivity": autism_config.get("sound_sensitivity", "medium"),
                "visual_processing_aids": autism_config.get("visual_processing_aids", True),
                "keyboard_navigation": True
            }
        }

        return config

    def get_tool_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get personalized tool recommendations based on user profile.

        Considers executive function needs, domain preferences,
        and cognitive load management.
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return []

        # Get user's tool usage patterns and preferences
        adhd_friendly = profile.adhd_accommodations.get(
            "task_breakdown_assistance", False)
        autism_friendly = profile.autism_accommodations.get(
            "routine_consistency", False)

        # Query tools that match user needs
        query = self.db.query(IntegratedTool).filter(
            IntegratedTool.is_active.is_(True),
            IntegratedTool.integration_status == "completed"
        )

        if adhd_friendly:
            query = query.filter(IntegratedTool.adhd_friendly.is_(True))

        if autism_friendly:
            query = query.filter(IntegratedTool.autism_friendly.is_(True))

        # Prefer tools with lower cognitive load
        tools = query.order_by(IntegratedTool.cognitive_load).limit(10).all()

        recommendations = []
        for tool in tools:
            recommendations.append({
                "tool_id": tool.id,
                "name": tool.name,
                "display_name": tool.display_name,
                "domain": tool.domain_name,
                "cognitive_load": tool.cognitive_load,
                "executive_function_support": tool.supports_executive_function(),
                "recommendation_score": self._calculate_recommendation_score(tool, profile)
            })

        return recommendations

    def update_performance_preferences(
        self,
        user_id: str,
        preferences: Dict[str, Any]
    ) -> Optional[UserProfile]:
        """Update performance preferences for cognitive load optimization."""
        profile = self.get_user_profile(user_id)
        if not profile:
            return None

        valid_perf_keys = {
            "max_concurrent_tools", "cache_strategy", "preload_favorites",
            "background_updates", "response_time_target",
            "offline_sync_interval", "data_retention_days"
        }

        validated_preferences = {
            key: value for key, value in preferences.items()
            if key in valid_perf_keys
        }

        # Merge with existing preferences
        current_preferences = profile.performance_preferences or {}
        updated_preferences = {
            **current_preferences,
            **validated_preferences
        }

        profile.performance_preferences = updated_preferences
        profile.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(profile)

        return profile

    def record_tool_usage(
        self,
        user_id: str,
        tool_name: str,
        session_duration: int,
        cognitive_load_rating: Optional[int] = None
    ) -> bool:
        """
        Record tool usage for personalization and optimization.

        Args:
            user_id: User identifier
            tool_name: Name of the tool used
            session_duration: Duration in seconds
            cognitive_load_rating: User's cognitive load rating (1-10)

        Returns:
            True if recorded successfully
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return False

        # Update usage analytics
        usage_analytics = profile.usage_analytics or {}
        tool_usage = usage_analytics.get("tool_usage", {})

        if tool_name not in tool_usage:
            tool_usage[tool_name] = {
                "sessions": 0,
                "total_duration": 0,
                "avg_cognitive_load": None,
                "last_used": None
            }

        # Update tool usage statistics
        tool_stats = tool_usage[tool_name]
        tool_stats["sessions"] += 1
        tool_stats["total_duration"] += session_duration
        tool_stats["last_used"] = datetime.utcnow().isoformat()

        # Update cognitive load average if provided
        if cognitive_load_rating is not None:
            current_avg = tool_stats.get("avg_cognitive_load")
            if current_avg is None:
                tool_stats["avg_cognitive_load"] = cognitive_load_rating
            else:
                # Calculate new average
                total_sessions = tool_stats["sessions"]
                prev_total = current_avg * (total_sessions - 1)
                weighted_sum = prev_total + cognitive_load_rating
                new_avg = weighted_sum / total_sessions
                tool_stats["avg_cognitive_load"] = round(new_avg, 2)

        # Update profile
        usage_analytics["tool_usage"] = tool_usage
        profile.usage_analytics = usage_analytics
        profile.updated_at = datetime.utcnow()

        self.db.commit()

        return True

    def _get_default_executive_config(self) -> Dict[str, Any]:
        """Get default executive function configuration."""
        return {
            "response_time_target": 200,
            "focus_indicators": True,
            "reduced_animations": True,
            "predictable_navigation": True,
            "sensory_accommodations": True,
            "cognitive_load_level": "medium",
            "notification_strategy": "batched",
            "ui_optimization": {
                "preload_favorites": False,
                "cache_strategy": "normal",
                "max_concurrent_tools": 3,
                "layout_density": "comfortable"
            },
            "accessibility_features": {
                "high_contrast": False,
                "sound_sensitivity": "medium",
                "visual_processing_aids": True,
                "keyboard_navigation": True
            }
        }

    def _calculate_cognitive_load(self, profile: UserProfile) -> str:
        """Calculate user's cognitive load level based on accommodations."""
        adhd_accommodations = profile.adhd_accommodations or {}
        autism_accommodations = profile.autism_accommodations or {}

        # Count active accommodations
        adhd_active = sum(1 for v in adhd_accommodations.values() if v is True)
        autism_active = sum(
            1 for v in autism_accommodations.values() if v is True
        )

        total_accommodations = adhd_active + autism_active

        if total_accommodations >= 8:
            return "high"
        elif total_accommodations >= 4:
            return "medium"
        else:
            return "low"

    def _get_notification_strategy(self, profile: UserProfile) -> str:
        """Determine optimal notification strategy for user."""
        adhd_config = profile.adhd_accommodations or {}

        if adhd_config.get("notification_batching", False):
            return "batched"
        elif adhd_config.get("distraction_filtering", False):
            return "filtered"
        else:
            return "immediate"

    def _calculate_recommendation_score(
        self,
        tool: IntegratedTool,
        profile: UserProfile
    ) -> float:
        """Calculate recommendation score for a tool based on user profile."""
        score = 0.0

        # Base score for executive function support
        if tool.supports_executive_function():
            score += 30.0

        # ADHD-friendly bonus
        if profile.adhd_accommodations and tool.adhd_friendly:
            score += 25.0

        # Autism-friendly bonus
        if profile.autism_accommodations and tool.autism_friendly:
            score += 25.0

        # Cognitive load penalty
        load_scores = {"low": 20.0, "medium": 10.0, "high": 0.0}
        score += load_scores.get(tool.cognitive_load, 0.0)

        # Usage history bonus
        usage_analytics = profile.usage_analytics or {}
        tool_usage = usage_analytics.get("tool_usage", {})
        if tool.name in tool_usage:
            sessions = tool_usage[tool.name].get("sessions", 0)
            score += min(sessions * 2.0, 20.0)  # Cap at 20 points

        return min(score, 100.0)  # Cap at 100%
