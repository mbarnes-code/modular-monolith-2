"""
Cache Abstraction - Core Interfaces

Provides unified interface for caching (Redis, In-memory, PostgreSQL).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class CacheEntry:
    """
    Cache entry with metadata.

    Attributes:
        key: Cache key
        value: Cached value
        ttl_seconds: Time-to-live in seconds (None = no expiration)
        tags: Tags for cache invalidation
    """
    key: str
    value: Any
    ttl_seconds: Optional[int] = None
    tags: Optional[List[str]] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class ICache(ABC):
    """
    Abstract interface for cache implementations.

    Supports:
    - Key-value operations (get, set, delete)
    - TTL-based expiration
    - Tag-based invalidation
    - Atomic operations
    - Batch operations
    """

    @abstractmethod
    async def start(self) -> None:
        """Initialize cache connection"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Shutdown cache connection"""
        pass

    @abstractmethod
    async def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Get value from cache.

        Args:
            key: Cache key
            default: Default value if key not found

        Returns:
            Cached value or default
        """
        pass

    @abstractmethod
    async def set(
        self,
        key: str,
        value: Any,
        ttl_seconds: Optional[int] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Expiration time (None = no expiration)
            tags: Tags for invalidation
        """
        pass

    @abstractmethod
    async def delete(
        self,
        key: str,
    ) -> bool:
        """
        Delete value from cache.

        Args:
            key: Cache key

        Returns:
            True if key existed and was deleted
        """
        pass

    @abstractmethod
    async def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check if key exists in cache.

        Args:
            key: Cache key

        Returns:
            True if key exists
        """
        pass

    @abstractmethod
    async def clear(
        self,
        pattern: Optional[str] = None,
    ) -> int:
        """
        Clear cache entries.

        Args:
            pattern: Key pattern to match (None = clear all)

        Returns:
            Number of keys deleted
        """
        pass

    @abstractmethod
    async def invalidate_tags(
        self,
        tags: List[str],
    ) -> int:
        """
        Invalidate all entries with given tags.

        Args:
            tags: List of tags

        Returns:
            Number of keys deleted
        """
        pass

    @abstractmethod
    async def get_many(
        self,
        keys: List[str],
    ) -> Dict[str, Any]:
        """
        Get multiple values at once.

        Args:
            keys: List of cache keys

        Returns:
            Dict of key-value pairs (missing keys omitted)
        """
        pass

    @abstractmethod
    async def set_many(
        self,
        entries: Dict[str, Any],
        ttl_seconds: Optional[int] = None,
    ) -> None:
        """
        Set multiple values at once.

        Args:
            entries: Dict of key-value pairs
            ttl_seconds: Expiration time for all entries
        """
        pass

    @abstractmethod
    async def increment(
        self,
        key: str,
        amount: int = 1,
    ) -> int:
        """
        Atomically increment a counter.

        Args:
            key: Cache key
            amount: Increment amount

        Returns:
            New value after increment
        """
        pass

    @abstractmethod
    async def decrement(
        self,
        key: str,
        amount: int = 1,
    ) -> int:
        """
        Atomically decrement a counter.

        Args:
            key: Cache key
            amount: Decrement amount

        Returns:
            New value after decrement
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check cache health.

        Returns:
            True if healthy, False otherwise
        """
        pass


class ICacheFactory(ABC):
    """Factory interface for creating cache instances"""

    @staticmethod
    @abstractmethod
    def create(
        cache_type: str,
        config: Dict[str, Any],
    ) -> ICache:
        """
        Create a cache adapter instance.

        Args:
            cache_type: Type (redis, memory, postgresql)
            config: Cache-specific configuration

        Returns:
            Configured cache instance
        """
        pass


class CacheError(Exception):
    """Base exception for cache errors"""
    pass
