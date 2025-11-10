"""
MISP Redis Tool
Migrated from features/MISP/app/Lib/Tools/RedisTool.php

Provides Redis connection management and caching functionality while
maintaining identical behavior to the original PHP implementation.
"""

import json
import pickle
from typing import Any, Optional

import brotli
import redis
import zstd
from redis import Redis


class RedisTool:
    """
    Redis utilities for MISP caching and session management.
    Maintains API compatibility with original PHP RedisTool.
    """

    # Compression constants
    COMPRESS_MIN_LENGTH = 256
    BROTLI_HEADER = b"\xce\xb2\xcf\x81"
    ZSTD_HEADER = b"\x28\xb5\x2f\xfd"

    _connection: Optional[Redis] = None
    _serializer: str = "pickle"

    @classmethod
    def init(cls, config: Optional[dict] = None) -> Redis:
        """
        Initialize Redis connection with configuration.

        Args:
            config: Redis configuration dictionary

        Returns:
            Redis connection instance

        Raises:
            ConnectionError: If Redis connection fails
            ImportError: If Redis library not available
        """
        if cls._connection:
            return cls._connection

        if config is None:
            config = {}

        # Default configuration
        host = config.get('host', '127.0.0.1')
        port = config.get('port', 6379)
        database = config.get('database', 13)
        password = config.get('password')
        socket_path = config.get('socket_path')

        try:
            if socket_path and socket_path.startswith('/'):
                # Unix socket connection
                redis_client = Redis(unix_socket_path=socket_path)
            else:
                # TCP connection
                redis_client = Redis(
                    host=host,
                    port=int(port),
                    password=password,
                    decode_responses=False  # Handle binary data
                )

            # Test connection
            redis_client.ping()

            # Select database
            redis_client.select(database)

            cls._connection = redis_client
            return redis_client

        except redis.ConnectionError as e:
            raise ConnectionError(f"Could not connect to Redis: {e}") from e
        except Exception as e:
            raise ConnectionError(f"Redis initialization failed: {e}") from e

    @classmethod
    def get_connection(cls) -> Redis:
        """
        Get existing Redis connection or create new one.

        Returns:
            Redis connection instance
        """
        if cls._connection is None:
            return cls.init()
        return cls._connection

    @classmethod
    def set(
        cls,
        key: str,
        value: Any,
        expire: Optional[int] = None,
        compress: bool = True
    ) -> bool:
        """
        Set value in Redis with optional compression and expiration.

        Args:
            key: Redis key
            value: Value to store
            expire: Expiration time in seconds
            compress: Whether to compress large values

        Returns:
            True if successful, False otherwise
        """
        try:
            redis_client = cls.get_connection()

            # Serialize value
            if isinstance(value, (str, bytes)):
                serialized_value = (
                    value.encode() if isinstance(value, str) else value
                )
            else:
                if cls._serializer == "json":
                    serialized_value = json.dumps(value).encode()
                else:
                    serialized_value = pickle.dumps(value)

            # Compress if value is large enough
            if compress and len(serialized_value) >= cls.COMPRESS_MIN_LENGTH:
                serialized_value = cls._compress_value(serialized_value)

            # Set value with optional expiration
            if expire:
                return redis_client.setex(key, expire, serialized_value)
            else:
                return redis_client.set(key, serialized_value)

        except Exception:
            return False

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Get value from Redis with automatic decompression.

        Args:
            key: Redis key
            default: Default value if key not found

        Returns:
            Stored value or default
        """
        try:
            redis_client = cls.get_connection()
            value = redis_client.get(key)

            if value is None:
                return default

            # Check for compression and decompress
            decompressed_value = cls._decompress_value(value)

            # Deserialize value
            if cls._serializer == "json":
                try:
                    return json.loads(decompressed_value.decode())
                except (json.JSONDecodeError, UnicodeDecodeError):
                    return decompressed_value
            else:
                try:
                    return pickle.loads(decompressed_value)
                except (pickle.PickleError, TypeError):
                    return decompressed_value

        except Exception:
            return default

    @classmethod
    def delete(cls, key: str) -> bool:
        """
        Delete key from Redis.

        Args:
            key: Redis key to delete

        Returns:
            True if key was deleted, False otherwise
        """
        try:
            redis_client = cls.get_connection()
            return bool(redis_client.delete(key))
        except Exception:
            return False

    @classmethod
    def exists(cls, key: str) -> bool:
        """
        Check if key exists in Redis.

        Args:
            key: Redis key to check

        Returns:
            True if key exists, False otherwise
        """
        try:
            redis_client = cls.get_connection()
            return bool(redis_client.exists(key))
        except Exception:
            return False

    @classmethod
    def expire(cls, key: str, seconds: int) -> bool:
        """
        Set expiration time for key.

        Args:
            key: Redis key
            seconds: Expiration time in seconds

        Returns:
            True if expiration was set, False otherwise
        """
        try:
            redis_client = cls.get_connection()
            return bool(redis_client.expire(key, seconds))
        except Exception:
            return False

    @classmethod
    def increment(cls, key: str, amount: int = 1) -> Optional[int]:
        """
        Increment numeric value in Redis.

        Args:
            key: Redis key
            amount: Amount to increment by

        Returns:
            New value after increment, None on error
        """
        try:
            redis_client = cls.get_connection()
            return redis_client.incrby(key, amount)
        except Exception:
            return None

    @classmethod
    def _compress_value(cls, value: bytes) -> bytes:
        """
        Compress value using brotli (preferred) or zstd.

        Args:
            value: Raw bytes to compress

        Returns:
            Compressed bytes with header
        """
        try:
            # Try brotli compression first
            compressed = brotli.compress(value)
            return cls.BROTLI_HEADER + compressed
        except Exception:
            try:
                # Fallback to zstd compression
                compressed = zstd.compress(value)
                return cls.ZSTD_HEADER + compressed
            except Exception:
                # Return original value if compression fails
                return value

    @classmethod
    def _decompress_value(cls, value: bytes) -> bytes:
        """
        Decompress value based on header.

        Args:
            value: Potentially compressed bytes

        Returns:
            Decompressed bytes
        """
        if value.startswith(cls.BROTLI_HEADER):
            try:
                return brotli.decompress(value[len(cls.BROTLI_HEADER):])
            except Exception:
                return value
        elif value.startswith(cls.ZSTD_HEADER):
            try:
                return zstd.decompress(value[len(cls.ZSTD_HEADER):])
            except Exception:
                return value
        else:
            return value

    @classmethod
    def flush_db(cls) -> bool:
        """
        Flush current Redis database.

        Returns:
            True if successful, False otherwise
        """
        try:
            redis_client = cls.get_connection()
            redis_client.flushdb()
            return True
        except Exception:
            return False

    @classmethod
    def get_info(cls) -> dict:
        """
        Get Redis server information.

        Returns:
            Dictionary with Redis server info
        """
        try:
            redis_client = cls.get_connection()
            return redis_client.info()
        except Exception:
            return {}

    @classmethod
    def set_serializer(cls, serializer: str) -> None:
        """
        Set serialization method.

        Args:
            serializer: 'pickle' or 'json'
        """
        if serializer in ['pickle', 'json']:
            cls._serializer = serializer
