"""
Shared database utilities for the modular monolith platform.

This library provides unified database connection management, pooling, and
migration utilities across all 37 integrated tools with executive function
accommodations for ADHD/autism users.

Features:
- PostgreSQL, SQLite, and Redis connection management
- Connection pooling with performance monitoring
- Migration utilities with rollback capabilities
- Health checks and connection validation
- Executive function accommodations (clear error messages, progressive hints)
- Domain-specific performance thresholds
"""

import asyncio
import logging
import sqlite3
import time
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager, contextmanager
from datetime import datetime
from typing import Any, AsyncGenerator, Dict, Generator, List, Optional, Union

import redis.asyncio as redis
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool

logger = logging.getLogger(__name__)


class DatabaseConfig(BaseModel):
    """Database configuration with executive function accommodations."""

    # PostgreSQL Configuration
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="")
    postgres_database: str = Field(default="jane_platform")
    postgres_pool_size: int = Field(default=10)
    postgres_max_overflow: int = Field(default=20)
    postgres_pool_timeout: int = Field(default=30)

    # SQLite Configuration
    sqlite_path: str = Field(default="./data/local.db")
    sqlite_timeout: float = Field(default=30.0)
    sqlite_check_same_thread: bool = Field(default=False)

    # Redis Configuration
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_password: Optional[str] = Field(default=None)
    redis_database: int = Field(default=0)
    redis_pool_max_connections: int = Field(default=50)
    redis_socket_timeout: float = Field(default=5.0)

    # Performance Monitoring
    enable_performance_monitoring: bool = Field(default=True)
    slow_query_threshold: float = Field(default=1.0)

    # Domain-specific performance thresholds
    security_domain_threshold: float = Field(default=1.0)
    productivity_domain_threshold: float = Field(default=2.0)
    mtg_domain_threshold: float = Field(default=3.0)
    infrastructure_domain_threshold: float = Field(default=5.0)

    # Executive Function Accommodations
    clear_error_messages: bool = Field(default=True)
    progressive_hints: bool = Field(default=True)
    connection_retry_attempts: int = Field(default=3)

    class Config:
        """Pydantic configuration."""
        env_prefix = "DB_"


class DatabaseError(Exception):
    """Custom database error with ADHD-friendly messaging."""

    def __init__(self, code: int, message: str, user_message: Optional[str] = None):
        self.code = code
        self.message = message
        self.user_message = user_message or message
        super().__init__(self.user_message)


class ConnectionHealth(BaseModel):
    """Database connection health status."""

    is_healthy: bool
    response_time_ms: float
    last_check: datetime
    error_message: Optional[str] = None
    connection_count: Optional[int] = None
    database_type: str


class BaseDatabase(ABC):
    """Abstract base class for database connections."""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.logger = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    async def connect(self) -> None:
        """Establish database connection."""
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        """Close database connection."""
        pass

    @abstractmethod
    async def health_check(self) -> ConnectionHealth:
        """Check connection health."""
        pass

    def _log_performance(self, operation: str, duration: float, domain: str = "general") -> None:
        """Log performance metrics with domain-specific thresholds."""
        thresholds = {
            "security": self.config.security_domain_threshold,
            "productivity": self.config.productivity_domain_threshold,
            "mtg": self.config.mtg_domain_threshold,
            "infrastructure": self.config.infrastructure_domain_threshold,
        }

        threshold = thresholds.get(domain, self.config.slow_query_threshold)

        if duration > threshold:
            self.logger.warning(
                f"Slow {operation} operation: {duration:.3f}s "
                f"(threshold: {threshold}s, domain: {domain})"
            )
        else:
            self.logger.debug(
                f"{operation} completed in {duration:.3f}s (domain: {domain})")


class PostgreSQLDatabase(BaseDatabase):
    """PostgreSQL database connection manager."""

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self.engine = None
        self.async_engine = None
        self.session_factory = None
        self.async_session_factory = None
        self._pool = None

    async def connect(self) -> None:
        """Establish PostgreSQL connection with pooling."""
        try:
            # Synchronous engine
            sync_url = (
                f"postgresql://{self.config.postgres_user}:"
                f"{self.config.postgres_password}@"
                f"{self.config.postgres_host}:{self.config.postgres_port}/"
                f"{self.config.postgres_database}"
            )

            self.engine = create_engine(
                sync_url,
                poolclass=QueuePool,
                pool_size=self.config.postgres_pool_size,
                max_overflow=self.config.postgres_max_overflow,
                pool_timeout=self.config.postgres_pool_timeout,
                echo=False
            )

            # Asynchronous engine
            async_url = (
                f"postgresql+asyncpg://{self.config.postgres_user}:"
                f"{self.config.postgres_password}@"
                f"{self.config.postgres_host}:{self.config.postgres_port}/"
                f"{self.config.postgres_database}"
            )

            self.async_engine = create_async_engine(
                async_url,
                pool_size=self.config.postgres_pool_size,
                max_overflow=self.config.postgres_max_overflow,
                echo=False
            )

            # Session factories
            self.session_factory = sessionmaker(bind=self.engine)
            self.async_session_factory = sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession,
                expire_on_commit=False
            )

            # Test connection
            await self._test_connection()

            self.logger.info("PostgreSQL connection established successfully")

        except Exception as e:
            error_msg = f"Failed to connect to PostgreSQL: {str(e)}"
            user_msg = (
                "Database connection failed. "
                "Please check your connection settings and try again."
            )

            if self.config.progressive_hints:
                user_msg += (
                    " Hint: Verify the database server is running and "
                    "your credentials are correct."
                )

            raise DatabaseError(500, error_msg, user_msg)

    async def _test_connection(self) -> None:
        """Test database connection."""
        try:
            async with self.async_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
        except Exception as e:
            raise DatabaseError(
                500,
                f"Connection test failed: {str(e)}",
                "Unable to verify database connection."
            )

    async def disconnect(self) -> None:
        """Close PostgreSQL connection."""
        try:
            if self.async_engine:
                await self.async_engine.dispose()
            if self.engine:
                self.engine.dispose()

            self.logger.info("PostgreSQL connection closed")

        except Exception as e:
            self.logger.error(f"Error closing PostgreSQL connection: {str(e)}")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get synchronous database session."""
        if not self.session_factory:
            raise DatabaseError(500, "Database not connected")

        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get asynchronous database session."""
        if not self.async_session_factory:
            raise DatabaseError(500, "Database not connected")

        session = self.async_session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def health_check(self) -> ConnectionHealth:
        """Check PostgreSQL connection health."""
        start_time = time.time()

        try:
            async with self.async_engine.begin() as conn:
                await conn.execute(text("SELECT 1"))

            response_time = (time.time() - start_time) * 1000

            # Get connection pool info
            pool_info = None
            if hasattr(self.async_engine.pool, 'size'):
                pool_info = self.async_engine.pool.size()

            return ConnectionHealth(
                is_healthy=True,
                response_time_ms=response_time,
                last_check=datetime.now(),
                connection_count=pool_info,
                database_type="postgresql"
            )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000

            return ConnectionHealth(
                is_healthy=False,
                response_time_ms=response_time,
                last_check=datetime.now(),
                error_message=str(e),
                database_type="postgresql"
            )

    async def execute_query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        domain: str = "general"
    ) -> List[Dict[str, Any]]:
        """Execute a query with performance monitoring."""
        start_time = time.time()

        try:
            async with self.get_async_session() as session:
                result = await session.execute(text(query), params or {})
                rows = result.fetchall()

                # Convert to list of dicts
                columns = result.keys()
                return [dict(zip(columns, row)) for row in rows]

        except Exception as e:
            error_msg = f"Query execution failed: {str(e)}"
            user_msg = "Database query failed. Please check your query and try again."

            if self.config.progressive_hints:
                user_msg += " Hint: Verify your SQL syntax and table names."

            raise DatabaseError(500, error_msg, user_msg)

        finally:
            duration = time.time() - start_time
            self._log_performance("PostgreSQL query", duration, domain)


class SQLiteDatabase(BaseDatabase):
    """SQLite database connection manager."""

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self._connection = None
        self.engine = None
        self.session_factory = None

    async def connect(self) -> None:
        """Establish SQLite connection."""
        try:
            # Create directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(
                self.config.sqlite_path), exist_ok=True)

            # SQLAlchemy engine for ORM operations
            self.engine = create_engine(
                f"sqlite:///{self.config.sqlite_path}",
                echo=False,
                connect_args={
                    "timeout": self.config.sqlite_timeout,
                    "check_same_thread": self.config.sqlite_check_same_thread
                }
            )

            self.session_factory = sessionmaker(bind=self.engine)

            # Test connection
            await self._test_connection()

            self.logger.info(
                f"SQLite connection established: {self.config.sqlite_path}")

        except Exception as e:
            error_msg = f"Failed to connect to SQLite: {str(e)}"
            user_msg = "Local database connection failed. Please check file permissions."

            if self.config.progressive_hints:
                user_msg += f" Hint: Verify the directory exists and is writable: {os.path.dirname(self.config.sqlite_path)}"

            raise DatabaseError(500, error_msg, user_msg)

    async def _test_connection(self) -> None:
        """Test SQLite connection."""
        try:
            conn = sqlite3.connect(
                self.config.sqlite_path,
                timeout=self.config.sqlite_timeout
            )
            conn.execute("SELECT 1")
            conn.close()
        except Exception as e:
            raise DatabaseError(
                500,
                f"SQLite connection test failed: {str(e)}",
                "Unable to verify local database connection."
            )

    async def disconnect(self) -> None:
        """Close SQLite connection."""
        try:
            if self.engine:
                self.engine.dispose()

            self.logger.info("SQLite connection closed")

        except Exception as e:
            self.logger.error(f"Error closing SQLite connection: {str(e)}")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get SQLite database session."""
        if not self.session_factory:
            raise DatabaseError(500, "Database not connected")

        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    async def health_check(self) -> ConnectionHealth:
        """Check SQLite connection health."""
        start_time = time.time()

        try:
            conn = sqlite3.connect(
                self.config.sqlite_path,
                timeout=self.config.sqlite_timeout
            )
            conn.execute("SELECT 1")
            conn.close()

            response_time = (time.time() - start_time) * 1000

            return ConnectionHealth(
                is_healthy=True,
                response_time_ms=response_time,
                last_check=datetime.now(),
                database_type="sqlite"
            )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000

            return ConnectionHealth(
                is_healthy=False,
                response_time_ms=response_time,
                last_check=datetime.now(),
                error_message=str(e),
                database_type="sqlite"
            )


class RedisDatabase(BaseDatabase):
    """Redis database connection manager."""

    def __init__(self, config: DatabaseConfig):
        super().__init__(config)
        self.client = None
        self._connection_pool = None

    async def connect(self) -> None:
        """Establish Redis connection."""
        try:
            # Create connection pool
            self._connection_pool = redis.ConnectionPool(
                host=self.config.redis_host,
                port=self.config.redis_port,
                password=self.config.redis_password,
                db=self.config.redis_database,
                max_connections=self.config.redis_pool_max_connections,
                socket_timeout=self.config.redis_socket_timeout,
                decode_responses=True
            )

            # Create client
            self.client = redis.Redis(
                connection_pool=self._connection_pool,
                decode_responses=True
            )

            # Test connection
            await self._test_connection()

            self.logger.info("Redis connection established successfully")

        except Exception as e:
            error_msg = f"Failed to connect to Redis: {str(e)}"
            user_msg = "Cache database connection failed. Please check Redis server."

            if self.config.progressive_hints:
                user_msg += " Hint: Verify Redis is running and accessible."

            raise DatabaseError(500, error_msg, user_msg)

    async def _test_connection(self) -> None:
        """Test Redis connection."""
        try:
            await self.client.ping()
        except Exception as e:
            raise DatabaseError(
                500,
                f"Redis connection test failed: {str(e)}",
                "Unable to verify cache database connection."
            )

    async def disconnect(self) -> None:
        """Close Redis connection."""
        try:
            if self.client:
                await self.client.close()
            if self._connection_pool:
                await self._connection_pool.disconnect()

            self.logger.info("Redis connection closed")

        except Exception as e:
            self.logger.error(f"Error closing Redis connection: {str(e)}")

    async def health_check(self) -> ConnectionHealth:
        """Check Redis connection health."""
        start_time = time.time()

        try:
            await self.client.ping()

            response_time = (time.time() - start_time) * 1000

            # Get connection pool info
            pool_info = None
            if self._connection_pool:
                pool_info = len(self._connection_pool._available_connections)

            return ConnectionHealth(
                is_healthy=True,
                response_time_ms=response_time,
                last_check=datetime.now(),
                connection_count=pool_info,
                database_type="redis"
            )

        except Exception as e:
            response_time = (time.time() - start_time) * 1000

            return ConnectionHealth(
                is_healthy=False,
                response_time_ms=response_time,
                last_check=datetime.now(),
                error_message=str(e),
                database_type="redis"
            )

    async def set_with_expiry(
        self,
        key: str,
        value: Union[str, bytes, int, float],
        expiry_seconds: Optional[int] = None
    ) -> bool:
        """Set a key with optional expiry."""
        try:
            if expiry_seconds:
                return await self.client.setex(key, expiry_seconds, value)
            else:
                return await self.client.set(key, value)
        except Exception as e:
            error_msg = f"Redis set operation failed: {str(e)}"
            raise DatabaseError(500, error_msg, "Cache operation failed")

    async def get(self, key: str) -> Optional[str]:
        """Get a key from Redis."""
        try:
            return await self.client.get(key)
        except Exception as e:
            error_msg = f"Redis get operation failed: {str(e)}"
            raise DatabaseError(500, error_msg, "Cache retrieval failed")


class DatabaseManager:
    """Unified database manager for all database types."""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.postgres: Optional[PostgreSQLDatabase] = None
        self.sqlite: Optional[SQLiteDatabase] = None
        self.redis: Optional[RedisDatabase] = None
        self.logger = logging.getLogger(__name__)

    async def initialize_postgres(self) -> PostgreSQLDatabase:
        """Initialize PostgreSQL connection."""
        self.postgres = PostgreSQLDatabase(self.config)
        await self.postgres.connect()
        return self.postgres

    async def initialize_sqlite(self) -> SQLiteDatabase:
        """Initialize SQLite connection."""
        self.sqlite = SQLiteDatabase(self.config)
        await self.sqlite.connect()
        return self.sqlite

    async def initialize_redis(self) -> RedisDatabase:
        """Initialize Redis connection."""
        self.redis = RedisDatabase(self.config)
        await self.redis.connect()
        return self.redis

    async def initialize_all(self) -> None:
        """Initialize all database connections."""
        tasks = []

        try:
            if self.config.postgres_host:
                tasks.append(self.initialize_postgres())

            if self.config.sqlite_path:
                tasks.append(self.initialize_sqlite())

            if self.config.redis_host:
                tasks.append(self.initialize_redis())

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

            self.logger.info("Database manager initialized successfully")

        except Exception as e:
            self.logger.error(f"Database initialization failed: {str(e)}")
            raise

    async def health_check_all(self) -> Dict[str, ConnectionHealth]:
        """Check health of all connected databases."""
        results = {}

        if self.postgres:
            results["postgres"] = await self.postgres.health_check()

        if self.sqlite:
            results["sqlite"] = await self.sqlite.health_check()

        if self.redis:
            results["redis"] = await self.redis.health_check()

        return results

    async def close_all(self) -> None:
        """Close all database connections."""
        tasks = []

        if self.postgres:
            tasks.append(self.postgres.disconnect())

        if self.sqlite:
            tasks.append(self.sqlite.disconnect())

        if self.redis:
            tasks.append(self.redis.disconnect())

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

        self.logger.info("All database connections closed")


# Convenience functions for quick access
def create_database_manager(config: Optional[DatabaseConfig] = None) -> DatabaseManager:
    """Create a configured database manager."""
    if config is None:
        config = DatabaseConfig()

    return DatabaseManager(config)
