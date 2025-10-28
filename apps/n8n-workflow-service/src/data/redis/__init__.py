"""
Redis configuration and management for the Mental Prosthetic Platform.

Provides caching and session management across all 37 integrated tools
with executive function optimizations for ADHD/autism support.
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import redis.asyncio as redis
from pydantic import BaseSettings
from redis.asyncio import ConnectionPool, Redis

logger = logging.getLogger(__name__)


class RedisSettings(BaseSettings):
    """Redis configuration settings."""

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str | None = None
    redis_ssl: bool = False
    redis_max_connections: int = 20

    # Cache TTL settings (executive function optimized)
    default_cache_ttl: int = 3600  # 1 hour
    session_ttl: int = 86400  # 24 hours
    ui_state_ttl: int = 604800  # 1 week (ADHD context preservation)

    class Config:
        env_prefix = "REDIS_"


class RedisManager:
    """
    Redis connection and cache management for cross-domain operations.

    Optimized for executive function support with context preservation
    and rapid state restoration for ADHD/autism accommodations.
    """

    def __init__(self, settings: RedisSettings | None = None):
        self.settings = settings or RedisSettings()
        self.pool: ConnectionPool | None = None
        self.client: Redis | None = None

    async def initialize(self) -> None:
        """Initialize Redis connection pool."""
        try:
            self.pool = redis.ConnectionPool(
                host=self.settings.redis_host,
                port=self.settings.redis_port,
                db=self.settings.redis_db,
                password=self.settings.redis_password,
                ssl=self.settings.redis_ssl,
                max_connections=self.settings.redis_max_connections,
                retry_on_timeout=True,
                decode_responses=True
            )

            self.client = Redis(connection_pool=self.pool)

            # Test connection
            await self.client.ping()
            logger.info(
                f"Redis connected to {self.settings.redis_host}:{self.settings.redis_port}")

        except Exception as e:
            logger.error(f"Failed to initialize Redis: {e}")
            raise

    async def close(self) -> None:
        """Close Redis connections."""
        if self.client:
            await self.client.close()
        if self.pool:
            await self.pool.disconnect()

    async def set_cache(
        self,
        key: str,
        value: str | dict[str, Any],
        ttl: int | None = None
    ) -> bool:
        """Set cache value with optional TTL."""
        try:
            if isinstance(value, dict):
                value = json.dumps(value)

            ttl = ttl or self.settings.default_cache_ttl
            result = await self.client.setex(key, ttl, value)
            return result

        except Exception as e:
            logger.error(f"Failed to set cache key {key}: {e}")
            return False

    async def get_cache(self, key: str) -> str | dict[str, Any] | None:
        """Get cache value, auto-detecting JSON."""
        try:
            value = await self.client.get(key)
            if value is None:
                return None

            # Try to parse as JSON
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value

        except Exception as e:
            logger.error(f"Failed to get cache key {key}: {e}")
            return None

    async def delete_cache(self, key: str) -> bool:
        """Delete cache key."""
        try:
            result = await self.client.delete(key)
            return bool(result)
        except Exception as e:
            logger.error(f"Failed to delete cache key {key}: {e}")
            return False

    async def set_session(self, session_id: str, session_data: dict[str, Any]) -> bool:
        """Set user session data with extended TTL for context preservation."""
        key = f"session:{session_id}"
        return await self.set_cache(key, session_data, self.settings.session_ttl)

    async def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Get user session data."""
        key = f"session:{session_id}"
        return await self.get_cache(key)

    async def delete_session(self, session_id: str) -> bool:
        """Delete user session."""
        key = f"session:{session_id}"
        return await self.delete_cache(key)

    async def set_ui_state(self, user_id: str, domain: str, state_data: dict[str, Any]) -> bool:
        """
        Set UI state for executive function context preservation.
        Extended TTL to maintain context across sessions.
        """
        key = f"ui_state:{user_id}:{domain}"
        return await self.set_cache(key, state_data, self.settings.ui_state_ttl)

    async def get_ui_state(self, user_id: str, domain: str) -> dict[str, Any] | None:
        """Get UI state for context restoration."""
        key = f"ui_state:{user_id}:{domain}"
        return await self.get_cache(key)

    async def set_tool_cache(
        self,
        tool_name: str,
        operation: str,
        params_hash: str,
        result: dict[str, Any]
    ) -> bool:
        """Cache tool operation results for performance optimization."""
        key = f"tool_cache:{tool_name}:{operation}:{params_hash}"
        # Shorter TTL for tool results to ensure freshness
        return await self.set_cache(key, result, 1800)  # 30 minutes

    async def get_tool_cache(
        self,
        tool_name: str,
        operation: str,
        params_hash: str
    ) -> dict[str, Any] | None:
        """Get cached tool operation result."""
        key = f"tool_cache:{tool_name}:{operation}:{params_hash}"
        return await self.get_cache(key)

    async def set_workflow_state(self, workflow_id: str, state: dict[str, Any]) -> bool:
        """Set cross-domain workflow state."""
        key = f"workflow:{workflow_id}"
        return await self.set_cache(key, state, self.settings.default_cache_ttl)

    async def get_workflow_state(self, workflow_id: str) -> dict[str, Any] | None:
        """Get cross-domain workflow state."""
        key = f"workflow:{workflow_id}"
        return await self.get_cache(key)

    async def publish_event(self, channel: str, event_data: dict[str, Any]) -> bool:
        """Publish real-time event for cross-tool synchronization."""
        try:
            message = json.dumps({
                "timestamp": datetime.utcnow().isoformat(),
                "data": event_data
            })
            result = await self.client.publish(channel, message)
            return bool(result)
        except Exception as e:
            logger.error(f"Failed to publish event to {channel}: {e}")
            return False

    async def subscribe_events(self, channels: list[str]):
        """Subscribe to real-time events."""
        try:
            pubsub = self.client.pubsub()
            await pubsub.subscribe(*channels)
            return pubsub
        except Exception as e:
            logger.error(f"Failed to subscribe to channels {channels}: {e}")
            raise

    async def health_check(self) -> dict[str, Any]:
        """Redis health check for monitoring."""
        try:
            # Test basic operations
            test_key = "health_check"
            await self.client.setex(test_key, 10, "ok")
            result = await self.client.get(test_key)
            await self.client.delete(test_key)

            # Get info
            info = await self.client.info()

            return {
                "status": "healthy" if result == "ok" else "unhealthy",
                "connected_clients": info.get("connected_clients", 0),
                "used_memory_human": info.get("used_memory_human", "unknown"),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0)
            }

        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}


# Global Redis manager instance
redis_manager = RedisManager()


async def get_redis() -> RedisManager:
    """Get Redis manager instance."""
    if not redis_manager.client:
        await redis_manager.initialize()
    return redis_manager


# Domain-specific cache keys and patterns
CACHE_PATTERNS = {
    "security": {
        "tools": ["misp", "helk", "securityonion", "maltrail", "yara_x", "cyberchef",
                  "nemesis", "apiscout", "brute_ratel", "meterpreter", "lscript", "rita", "software_forensic_kit"],
        "cache_prefix": "sec:",
        "ttl": 1800  # 30 minutes for security data freshness
    },
    "productivity": {
        "tools": ["n8n", "mealie", "dispatch", "actual", "firecrawl", "goose", "it_tools", "inspector"],
        "cache_prefix": "prod:",
        "ttl": 3600  # 1 hour for productivity data
    },
    "mtg": {
        "tools": ["commander_spellbook", "mtg_commander_map", "mtg_scripting_toolkit", "card_analysis"],
        "cache_prefix": "mtg:",
        "ttl": 7200  # 2 hours for MTG data (less frequently changing)
    },
    "infrastructure": {
        "tools": ["kong", "ghostwriter", "kasmvnc", "chroma_mcp", "filescopemcp", "firecrawl_mcp",
                  "n8n_mcp", "malwarebazaar_mcp", "mcp_virustotal", "onex", "hexstrike_ai", "blackarch"],
        "cache_prefix": "infra:",
        "ttl": 900  # 15 minutes for infrastructure monitoring
    }
}


if __name__ == "__main__":
    # Test Redis connectivity
    async def test_redis():
        manager = RedisManager()
        await manager.initialize()

        # Test basic operations
        await manager.set_cache("test_key", {"message": "Hello Redis!"})
        result = await manager.get_cache("test_key")
        print(f"Cache test result: {result}")

        # Test health check
        health = await manager.health_check()
        print(f"Redis health: {health}")

        await manager.close()

    asyncio.run(test_redis())
