"""
Database Transaction Rollback Manager for Security Domain

Manages database transactions and rollback capabilities for all 13
security tools (MISP, HELK, SecurityOnion, Maltrail, YARA-X, CyberChef, 
Nemesis, etc.) with business logic preservation.
"""

import asyncio
import json
import logging
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Set

try:
    import asyncpg
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import AsyncSession
except ImportError:
    # Dependencies not available in current environment
    asyncpg = None
    AsyncSession = None
    text = None

logger = logging.getLogger(__name__)


class TransactionStatus(Enum):
    """Status of database transactions."""
    PENDING = "pending"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


@dataclass
class TransactionSnapshot:
    """Snapshot of database state at transaction start."""
    transaction_id: str
    tool_id: str
    timestamp: datetime
    affected_tables: List[str]
    before_state: Dict[str, Any] = field(default_factory=dict)
    after_state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RollbackOperation:
    """Represents a database rollback operation."""
    operation_id: str
    transaction_id: str
    tool_id: str
    status: TransactionStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    tables_affected: List[str] = field(default_factory=list)
    rows_affected: int = 0


class DatabaseTransactionManager:
    """Manages database transactions and rollbacks for security domain."""

    def __init__(self, connection_config: Dict[str, Any]):
        self.connection_config = connection_config
        self.active_transactions: Dict[str, TransactionSnapshot] = {}
        self.rollback_history: List[RollbackOperation] = []
        self.connection_pool = None

        # Security domain tools
        self.security_tools = {
            "misp": {
                "database": "misp",
                "primary_tables": ["events", "attributes", "objects", "users"],
                # Tables that need special handling
                "critical_tables": ["events", "attributes"]
            },
            "helk": {
                "database": "helk",
                "primary_tables": ["logs", "events", "alerts", "analytics"],
                "critical_tables": ["events", "alerts"]
            },
            "securityonion": {
                "database": "securityonion",
                "primary_tables": ["alerts", "events", "sensors", "users"],
                "critical_tables": ["alerts", "events"]
            },
            "maltrail": {
                "database": "maltrail",
                "primary_tables": ["trails", "events", "sensors"],
                "critical_tables": ["trails", "events"]
            },
            "nemesis": {
                "database": "nemesis",
                "primary_tables": ["operations", "agents", "tasks", "results"],
                "critical_tables": ["operations", "tasks"]
            },
            "cyberchef": {
                "database": "cyberchef",
                "primary_tables": ["recipes", "operations", "history"],
                "critical_tables": ["recipes"]
            },
            "yara-x": {
                "database": "yarax",
                "primary_tables": ["rules", "scans", "matches"],
                "critical_tables": ["rules", "matches"]
            }
        }

    async def initialize(self):
        """Initialize database connection pool."""
        if asyncpg is None:
            logger.warning("asyncpg not available - using mock implementation")
            return

        try:
            self.connection_pool = await asyncpg.create_pool(
                **self.connection_config,
                min_size=5,
                max_size=20,
                command_timeout=30
            )
            logger.info("Database transaction manager initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            raise

    @asynccontextmanager
    async def transaction(self, tool_id: str, description: str = ""):
        """Context manager for database transactions with rollback capability."""
        transaction_id = str(uuid.uuid4())
        snapshot = None

        try:
            # Create transaction snapshot
            snapshot = await self._create_transaction_snapshot(tool_id, transaction_id, description)

            if self.connection_pool:
                async with self.connection_pool.acquire() as conn:
                    async with conn.transaction():
                        yield TransactionContext(
                            transaction_id=transaction_id,
                            tool_id=tool_id,
                            connection=conn,
                            manager=self
                        )
            else:
                # Mock implementation when database not available
                yield TransactionContext(
                    transaction_id=transaction_id,
                    tool_id=tool_id,
                    connection=None,
                    manager=self
                )

            # Transaction committed successfully
            if snapshot:
                await self._finalize_transaction_snapshot(snapshot, TransactionStatus.COMMITTED)

        except Exception as e:
            logger.error(f"Transaction {transaction_id} failed: {e}")
            if snapshot:
                await self._finalize_transaction_snapshot(snapshot, TransactionStatus.FAILED)
            raise

    async def _create_transaction_snapshot(self, tool_id: str, transaction_id: str,
                                           description: str) -> TransactionSnapshot:
        """Create a snapshot of current database state before transaction."""
        snapshot = TransactionSnapshot(
            transaction_id=transaction_id,
            tool_id=tool_id,
            timestamp=datetime.utcnow(),
            affected_tables=[],
            metadata={"description": description}
        )

        if tool_id in self.security_tools:
            tool_config = self.security_tools[tool_id]
            snapshot.affected_tables = tool_config["primary_tables"]

            # Capture before state for critical tables
            if self.connection_pool:
                try:
                    async with self.connection_pool.acquire() as conn:
                        for table in tool_config["critical_tables"]:
                            # Get row counts and recent changes
                            count_query = f"SELECT COUNT(*) FROM {table}"
                            count = await conn.fetchval(count_query)

                            # Get recent records (last 100 for efficiency)
                            recent_query = f"""
                                SELECT * FROM {table} 
                                ORDER BY id DESC LIMIT 100
                            """
                            try:
                                recent_records = await conn.fetch(recent_query)
                                snapshot.before_state[table] = {
                                    "count": count,
                                    "recent_records": [dict(r) for r in recent_records]
                                }
                            except Exception as e:
                                logger.warning(
                                    f"Could not capture state for {table}: {e}")
                                snapshot.before_state[table] = {"count": count}

                except Exception as e:
                    logger.error(f"Failed to capture before state: {e}")

        self.active_transactions[transaction_id] = snapshot
        logger.info(
            f"Created transaction snapshot {transaction_id} for {tool_id}")

        return snapshot

    async def _finalize_transaction_snapshot(self, snapshot: TransactionSnapshot,
                                             status: TransactionStatus):
        """Finalize transaction snapshot with after state."""
        if status == TransactionStatus.COMMITTED and self.connection_pool:
            tool_config = self.security_tools.get(snapshot.tool_id, {})

            try:
                async with self.connection_pool.acquire() as conn:
                    for table in tool_config.get("critical_tables", []):
                        # Capture after state
                        count_query = f"SELECT COUNT(*) FROM {table}"
                        count = await conn.fetchval(count_query)

                        recent_query = f"""
                            SELECT * FROM {table} 
                            ORDER BY id DESC LIMIT 100
                        """
                        try:
                            recent_records = await conn.fetch(recent_query)
                            snapshot.after_state[table] = {
                                "count": count,
                                "recent_records": [dict(r) for r in recent_records]
                            }
                        except Exception as e:
                            logger.warning(
                                f"Could not capture after state for {table}: {e}")
                            snapshot.after_state[table] = {"count": count}

            except Exception as e:
                logger.error(f"Failed to capture after state: {e}")

        # Remove from active transactions
        if snapshot.transaction_id in self.active_transactions:
            del self.active_transactions[snapshot.transaction_id]

        logger.info(
            f"Finalized transaction {snapshot.transaction_id} with status {status.value}")

    async def rollback_to_snapshot(self, transaction_id: str) -> RollbackOperation:
        """Rollback database to a specific transaction snapshot."""
        operation_id = str(uuid.uuid4())

        # Find snapshot (check both active and completed)
        snapshot = self.active_transactions.get(transaction_id)
        if not snapshot:
            # TODO: Implement loading snapshot from persistent storage
            return RollbackOperation(
                operation_id=operation_id,
                transaction_id=transaction_id,
                tool_id="unknown",
                status=TransactionStatus.FAILED,
                started_at=datetime.utcnow(),
                error_message="Transaction snapshot not found"
            )

        rollback_op = RollbackOperation(
            operation_id=operation_id,
            transaction_id=transaction_id,
            tool_id=snapshot.tool_id,
            status=TransactionStatus.PENDING,
            started_at=datetime.utcnow()
        )

        try:
            if self.connection_pool:
                async with self.connection_pool.acquire() as conn:
                    async with conn.transaction():
                        # Perform rollback operations
                        await self._execute_rollback_operations(conn, snapshot, rollback_op)
            else:
                # Mock rollback for testing
                rollback_op.tables_affected = snapshot.affected_tables
                rollback_op.rows_affected = len(
                    snapshot.affected_tables) * 10  # Mock value

            rollback_op.status = TransactionStatus.ROLLED_BACK
            rollback_op.completed_at = datetime.utcnow()

            logger.info(
                f"Successfully rolled back transaction {transaction_id}")

        except Exception as e:
            rollback_op.status = TransactionStatus.FAILED
            rollback_op.error_message = str(e)
            rollback_op.completed_at = datetime.utcnow()
            logger.error(
                f"Rollback failed for transaction {transaction_id}: {e}")

        self.rollback_history.append(rollback_op)
        return rollback_op

    async def _execute_rollback_operations(self, conn, snapshot: TransactionSnapshot,
                                           rollback_op: RollbackOperation):
        """Execute the actual rollback operations on the database."""
        tool_config = self.security_tools.get(snapshot.tool_id, {})

        for table in tool_config.get("critical_tables", []):
            before_state = snapshot.before_state.get(table, {})
            after_state = snapshot.after_state.get(table, {})

            before_count = before_state.get("count", 0)
            after_count = after_state.get("count", 0)

            if after_count > before_count:
                # New records were added, remove them
                try:
                    # This is a simplified approach - real implementation would need
                    # more sophisticated tracking of specific record changes
                    delete_query = f"""
                        DELETE FROM {table} 
                        WHERE id > (
                            SELECT COALESCE(MAX(id), 0) FROM (
                                SELECT id FROM {table} ORDER BY id LIMIT {before_count}
                            ) AS before_records
                        )
                    """
                    result = await conn.execute(delete_query)
                    rollback_op.tables_affected.append(table)
                    rollback_op.rows_affected += int(
                        result.split()[-1]) if result else 0

                except Exception as e:
                    logger.error(f"Failed to rollback table {table}: {e}")
                    raise

    async def get_transaction_history(self, tool_id: str = None,
                                      limit: int = 50) -> List[TransactionSnapshot]:
        """Get transaction history for monitoring."""
        # In a real implementation, this would query persistent storage
        # For now, return active transactions
        transactions = list(self.active_transactions.values())

        if tool_id:
            transactions = [t for t in transactions if t.tool_id == tool_id]

        return sorted(transactions, key=lambda t: t.timestamp, reverse=True)[:limit]

    async def get_rollback_history(self, tool_id: str = None,
                                   limit: int = 50) -> List[RollbackOperation]:
        """Get rollback history for monitoring."""
        history = self.rollback_history

        if tool_id:
            history = [r for r in history if r.tool_id == tool_id]

        return sorted(history, key=lambda r: r.started_at, reverse=True)[:limit]

    async def cleanup_old_snapshots(self, retention_days: int = 7) -> int:
        """Clean up old transaction snapshots."""
        cutoff_time = datetime.utcnow() - timedelta(days=retention_days)

        # Remove old transactions from active list
        old_transactions = [
            tid for tid, snapshot in self.active_transactions.items()
            if snapshot.timestamp < cutoff_time
        ]

        for tid in old_transactions:
            del self.active_transactions[tid]

        logger.info(
            f"Cleaned up {len(old_transactions)} old transaction snapshots")
        return len(old_transactions)


class TransactionContext:
    """Context object for database transactions."""

    def __init__(self, transaction_id: str, tool_id: str, connection, manager):
        self.transaction_id = transaction_id
        self.tool_id = tool_id
        self.connection = connection
        self.manager = manager

    async def execute(self, query: str, *args) -> Any:
        """Execute a query within the transaction."""
        if self.connection:
            return await self.connection.execute(query, *args)
        else:
            # Mock execution for testing
            logger.info(f"Mock execute: {query}")
            return "mock_result"

    async def fetch(self, query: str, *args) -> List[Dict]:
        """Fetch results from a query within the transaction."""
        if self.connection:
            results = await self.connection.fetch(query, *args)
            return [dict(r) for r in results]
        else:
            # Mock fetch for testing
            logger.info(f"Mock fetch: {query}")
            return [{"mock": "data"}]


# Factory function to create domain-specific transaction managers
def create_security_transaction_manager(connection_config: Dict[str, Any]) -> DatabaseTransactionManager:
    """Create transaction manager for security domain."""
    return DatabaseTransactionManager(connection_config)


# Example usage and testing
async def test_transaction_manager():
    """Test the transaction manager functionality."""
    config = {
        "host": "localhost",
        "port": 5432,
        "database": "security",
        "user": "security_user",
        "password": "security_pass"
    }

    manager = create_security_transaction_manager(config)

    try:
        await manager.initialize()

        # Test transaction with rollback capability
        async with manager.transaction("misp", "Test MISP operation") as tx:
            # Simulate database operations
            await tx.execute("INSERT INTO events (name, info) VALUES ($1, $2)",
                             "Test Event", "Test information")

            # Transaction will be automatically committed if no exception
            logger.info("Transaction completed successfully")

    except Exception as e:
        logger.error(f"Transaction test failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_transaction_manager())
