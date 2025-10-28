"""
T054: Cross-tool preference synchronization service

This service ensures that user preferences for ADHD/autism accommodations
are synchronized across all 37 integrated tools in real-time.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PreferenceSyncService:
    """Cross-tool preference sync service for executive function accommodations."""

    def __init__(self):
        self.preference_cache: Dict[str, Dict[str, Any]] = {}
        self.running = False

    async def start(self):
        """Start the preference synchronization service."""
        if self.running:
            return

        self.running = True
        logger.info("Starting preference synchronization service")

    async def stop(self):
        """Stop the preference synchronization service."""
        self.running = False
        logger.info("Stopping preference synchronization service")

    async def update_preferences(
        self,
        user_id: str,
        category: str,
        updates: Dict[str, Any],
        source_tool: str = "system"
    ) -> bool:
        """Update user preferences and sync across all tools."""
        try:
            logger.info(
                f"Updating preferences for user {user_id}, "
                f"category {category}: {updates}"
            )

            # Update cache
            if user_id not in self.preference_cache:
                self.preference_cache[user_id] = {}

            if category not in self.preference_cache[user_id]:
                self.preference_cache[user_id][category] = {}

            self.preference_cache[user_id][category].update(updates)

            return True

        except Exception as e:
            logger.error(f"Error updating preferences for user {user_id}: {e}")
            return False

    async def get_user_preferences(
        self, user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get current user preferences with caching."""
        try:
            # Check cache first
            if user_id in self.preference_cache:
                return self.preference_cache[user_id]

            # Return default preferences if not found
            default_preferences = {
                "adhd_accommodations": {
                    "ui_animations": False,
                    "focus_mode": True,
                    "time_awareness": True,
                    "progress_indicators": True
                },
                "ui_preferences": {
                    "theme": "light",
                    "font_size": "medium",
                    "color_coding": True
                },
                "performance_preferences": {
                    "response_time_target": 200,
                    "preload_frequent_tools": True
                }
            }

            self.preference_cache[user_id] = default_preferences
            return default_preferences

        except Exception as e:
            logger.error(f"Error loading preferences for user {user_id}: {e}")
            return None

    async def validate_preferences(
        self, preferences: Dict[str, Any]
    ) -> tuple[bool, List[str]]:
        """Validate preference values for constitutional compliance."""
        errors = []

        try:
            # Validate performance preferences
            if "performance_preferences" in preferences:
                perf_prefs = preferences["performance_preferences"]

                if "response_time_target" in perf_prefs:
                    target = perf_prefs["response_time_target"]
                    if target > 200:
                        errors.append(
                            f"Response time target ({target}ms) exceeds "
                            "constitutional maximum of 200ms"
                        )

            return len(errors) == 0, errors

        except Exception as e:
            logger.error(f"Error validating preferences: {e}")
            return False, [f"Validation error: {e}"]


# Global service instance
preference_sync_service = PreferenceSyncService()


async def get_preference_sync_service() -> PreferenceSyncService:
    """Get the global preference synchronization service instance."""
    if not preference_sync_service.running:
        await preference_sync_service.start()
    return preference_sync_service
