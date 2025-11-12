"""
User preferences API endpoints for ADHD/autism customizations.

Constitutional Requirements:
- Executive function accommodations for ADHD/autism users
- WCAG 2.1 AA compliance support
- <200ms UI response preferences
- Context switching reduction patterns
- Cross-tool preference synchronization

This module provides REST API endpoints for managing user preferences
across all 37 integrated tools with executive function accommodations.
"""

from typing import Any, Dict, Optional

# Import actual models and services
from ...data.models.user_profile import UserProfile
from ...services.user_service import UserProfileService


# Placeholder API Router for implementation structure
# This will be integrated with FastAPI once dependencies are available
class PreferencesAPI:
    """
    User preferences API for ADHD/autism customizations.

    Provides comprehensive preference management including:
    - ADHD accommodations (focus indicators, reduced animations)
    - Autism accommodations (predictable patterns, sensory considerations)
    - UI preferences (theme, layout, accessibility)
    - Performance preferences (response time targets, caching)
    - Domain-specific preferences (Security, Productivity, MTG, Infrastructure)
    """

    def __init__(self):
        self.prefix = "/preferences"
        self.tags = ["preferences"]

    def get_user_preferences(self, user_profile: UserProfile) -> Dict[str, Any]:
        """
        Get all user preferences with executive function accommodations.

        Returns comprehensive preference settings for ADHD/autism support,
        UI customization, performance optimization, and accessibility features.
        """
        return {
            "user_id": user_profile.username,
            "adhd_accommodations": user_profile.adhd_accommodations or {},
            "autism_accommodations": user_profile.autism_accommodations or {},
            "ui_preferences": user_profile.ui_preferences or {},
            "performance_preferences": user_profile.performance_preferences or {},
            "accessibility_preferences": user_profile.accessibility_preferences or {},
            "domain_preferences": user_profile.domain_preferences or {},
            "last_updated": user_profile.updated_at.isoformat() if user_profile.updated_at else None
        }

    def update_adhd_accommodations(
        self,
        user_profile: UserProfile,
        accommodations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update ADHD-specific accommodation settings.

        Supports executive function patterns including focus indicators,
        context preservation, and cognitive load management.
        """
        # Validate ADHD accommodation settings
        valid_adhd_keys = {
            "ui_animations", "focus_mode", "time_awareness",
            "progress_indicators", "interrupt_protection",
            "consistent_navigation", "context_preservation", "task_breakdown"
        }

        validated_accommodations = {
            key: value for key, value in accommodations.items()
            if key in valid_adhd_keys
        }

        user_profile.update_preferences("adhd", validated_accommodations)

        return {
            "status": "updated",
            "adhd_accommodations": user_profile.adhd_accommodations,
            "message": "ADHD accommodations updated successfully"
        }

    def update_autism_accommodations(
        self,
        user_profile: UserProfile,
        accommodations: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update autism-specific accommodation settings.

        Supports predictable patterns, sensory considerations,
        and routine consistency across all 37 tools.
        """
        # Validate autism accommodation settings
        valid_autism_keys = {
            "predictable_patterns", "sensory_considerations", "clear_structure",
            "routine_support", "change_warnings", "detailed_feedback",
            "preference_stability", "cognitive_load_reduction"
        }

        validated_accommodations = {
            key: value for key, value in accommodations.items()
            if key in valid_autism_keys
        }

        user_profile.update_preferences("autism", validated_accommodations)

        return {
            "status": "updated",
            "autism_accommodations": user_profile.autism_accommodations,
            "message": "Autism accommodations updated successfully"
        }

    def update_ui_preferences(
        self,
        user_profile: UserProfile,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update UI and visual preferences.

        Optimizes interface for executive function support with
        theme, layout, and interaction customizations.
        """
        # Validate UI preference settings
        valid_ui_keys = {
            "theme", "font_size", "animation_speed", "density",
            "color_coding", "shortcuts_enabled", "tooltips_enabled",
            "confirmation_dialogs", "auto_save", "session_restoration"
        }

        validated_preferences = {
            key: value for key, value in preferences.items()
            if key in valid_ui_keys
        }

        user_profile.update_preferences("ui", validated_preferences)

        return {
            "status": "updated",
            "ui_preferences": user_profile.ui_preferences,
            "message": "UI preferences updated successfully"
        }

    def update_performance_preferences(
        self,
        user_profile: UserProfile,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update performance and optimization preferences.

        Configures response time targets, caching strategies,
        and resource management for <200ms constitutional requirement.
        """
        # Validate response time target meets constitutional requirements
        response_time_target = preferences.get("response_time_target", 200)
        if response_time_target > 200:
            return {
                "status": "error",
                "message": "Response time target cannot exceed 200ms constitutional requirement"
            }

        # Validate performance preference settings
        valid_perf_keys = {
            "response_time_target", "preload_frequent_tools", "cache_aggressively",
            "reduce_network_calls", "offline_support", "background_sync"
        }

        validated_preferences = {
            key: value for key, value in preferences.items()
            if key in valid_perf_keys
        }

        user_profile.update_preferences("performance", validated_preferences)

        return {
            "status": "updated",
            "performance_preferences": user_profile.performance_preferences,
            "message": "Performance preferences updated successfully"
        }

    def update_accessibility_preferences(
        self,
        user_profile: UserProfile,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update accessibility preferences.

        Configures WCAG 2.1 AA compliance features including
        screen reader support, contrast modes, and navigation aids.
        """
        # Validate accessibility preference settings
        valid_accessibility_keys = {
            "screen_reader", "high_contrast", "large_text", "keyboard_navigation",
            "focus_indicators", "aria_descriptions", "reduced_motion", "color_blind_support"
        }

        validated_preferences = {
            key: value for key, value in preferences.items()
            if key in valid_accessibility_keys
        }

        user_profile.update_preferences("accessibility", validated_preferences)

        return {
            "status": "updated",
            "accessibility_preferences": user_profile.accessibility_preferences,
            "message": "Accessibility preferences updated successfully"
        }

    def update_domain_preferences(
        self,
        user_profile: UserProfile,
        domain_name: str,
        preferences: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update domain-specific preferences.

        Supports customization for Security, Productivity, MTG,
        and Infrastructure domains with tool-specific settings.
        """
        # Validate domain name
        valid_domains = ["security", "productivity", "mtg", "infrastructure"]
        if domain_name not in valid_domains:
            return {
                "status": "error",
                "message": f"Invalid domain. Must be one of: {', '.join(valid_domains)}"
            }

        # Validate domain preference settings
        valid_domain_keys = {
            "default_view", "favorite_tools", "workflow_templates", "custom_settings"
        }

        validated_preferences = {
            key: value for key, value in preferences.items()
            if key in valid_domain_keys
        }

        user_profile.update_preferences(domain_name, validated_preferences)

        return {
            "status": "updated",
            "domain": domain_name,
            "domain_preferences": user_profile.get_domain_settings(domain_name),
            "message": f"{domain_name.title()} domain preferences updated successfully"
        }

    def get_executive_function_config(
        self,
        user_profile: UserProfile,
        user_service: UserProfileService
    ) -> Dict[str, Any]:
        """
        Get executive function configuration for UI optimization.

        Returns optimized settings for ADHD/autism accommodations including
        response time targets, cognitive load settings, and accessibility features.
        """
        config = user_service.get_executive_function_config(
            user_profile.username)

        return {
            "user_id": user_profile.username,
            "executive_function_config": config,
            "constitutional_compliance": {
                "response_time_target": config["response_time_target"],
                "meets_200ms_requirement": config["response_time_target"] <= 200,
                "wcag_compliance": "2.1 AA",
                "executive_function_support": True
            }
        }

    def get_preference_recommendations(
        self,
        user_profile: UserProfile
    ) -> Dict[str, Any]:
        """
        Get personalized preference recommendations.

        Analyzes user patterns and suggests optimizations for
        executive function support and cognitive load management.
        """
        # Get current settings for analysis
        current_settings = user_profile.get_executive_function_settings()

        recommendations = []

        # Analyze ADHD accommodations
        adhd_settings = current_settings.get("adhd", {})
        if not adhd_settings.get("focus_mode", False):
            recommendations.append({
                "type": "adhd",
                "setting": "focus_mode",
                "recommendation": "Enable focus mode for simplified interface",
                "benefit": "Reduces cognitive load and improves concentration",
                "priority": "high"
            })

        # Analyze performance settings
        perf_settings = current_settings.get("performance", {})
        target_time = perf_settings.get("response_time_target", 200)
        if target_time > 150:
            recommendations.append({
                "type": "performance",
                "setting": "response_time_target",
                "recommendation": "Lower response time target to 150ms",
                "benefit": "Improves executive function support",
                "priority": "medium"
            })

        # Analyze accessibility settings
        accessibility_settings = current_settings.get("accessibility", {})
        if not accessibility_settings.get("focus_indicators", False):
            recommendations.append({
                "type": "accessibility",
                "setting": "focus_indicators",
                "recommendation": "Enable enhanced focus indicators",
                "benefit": "Improves navigation for executive function support",
                "priority": "high"
            })

        return {
            "user_id": user_profile.username,
            "recommendations": recommendations,
            "optimization_score": len([r for r in recommendations if r["priority"] == "high"]),
            "total_recommendations": len(recommendations)
        }

    def reset_preferences_to_defaults(
        self,
        user_profile: UserProfile
    ) -> Dict[str, Any]:
        """
        Reset all preferences to constitutional defaults.

        Restores executive function accommodations, performance settings,
        and accessibility features to optimal default values.
        """
        # Reset to constitutional defaults
        default_adhd = {
            "ui_animations": False,
            "focus_mode": True,
            "time_awareness": True,
            "progress_indicators": True,
            "interrupt_protection": True,
            "consistent_navigation": True,
            "context_preservation": True,
            "task_breakdown": True
        }

        default_autism = {
            "predictable_patterns": True,
            "sensory_considerations": True,
            "clear_structure": True,
            "routine_support": True,
            "change_warnings": True,
            "detailed_feedback": True,
            "preference_stability": True,
            "cognitive_load_reduction": True
        }

        default_ui = {
            "theme": "light",
            "font_size": "medium",
            "animation_speed": "reduced",
            "density": "comfortable",
            "color_coding": True,
            "shortcuts_enabled": True,
            "tooltips_enabled": True,
            "confirmation_dialogs": True,
            "auto_save": True,
            "session_restoration": True
        }

        default_performance = {
            "response_time_target": 200,
            "preload_frequent_tools": True,
            "cache_aggressively": True,
            "reduce_network_calls": True,
            "offline_support": True,
            "background_sync": True
        }

        default_accessibility = {
            "screen_reader": False,
            "high_contrast": False,
            "large_text": False,
            "keyboard_navigation": True,
            "focus_indicators": True,
            "aria_descriptions": True,
            "reduced_motion": False,
            "color_blind_support": False
        }

        user_profile.update_preferences("adhd", default_adhd)
        user_profile.update_preferences("autism", default_autism)
        user_profile.update_preferences("ui", default_ui)
        user_profile.update_preferences("performance", default_performance)
        user_profile.update_preferences("accessibility", default_accessibility)

        return {
            "status": "reset",
            "message": "All preferences reset to constitutional defaults",
            "constitutional_compliance": True,
            "executive_function_support": True
        }


# Export the API class for integration with FastAPI
preferences_api = PreferencesAPI()

# This completes the PreferencesAPI implementation above
# The functionality is now encapsulated in the PreferencesAPI class
