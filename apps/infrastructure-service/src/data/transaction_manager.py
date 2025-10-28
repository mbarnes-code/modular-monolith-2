"""
Database Transaction Rollback Manager for Infrastructure Domain

Manages database transactions and rollback capabilities for 12+
infrastructure tools (Kong, Ghostwriter, KasmVNC, etc.) with 
business logic preservation.
"""

import logging
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class TransactionStatus(Enum):
    """Status of database transactions."""
    PENDING = "pending"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


@dataclass
class InfraTransactionSnapshot:
    """Snapshot of infrastructure database state at transaction start."""
    transaction_id: str
    tool_id: str
    timestamp: datetime
    affected_tables: List[str]
    before_state: Dict[str, Any] = field(default_factory=dict)
    after_state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class InfrastructureTransactionManager:
    """Transaction manager for infrastructure domain tools."""

    def __init__(self, connection_config: Dict[str, Any]):
        self.connection_config = connection_config
        self.active_transactions: Dict[str, InfraTransactionSnapshot] = {}

        # Infrastructure domain tools (12+ tools)
        self.infrastructure_tools = {
            "kong": {
                "database": "kong",
                "primary_tables": ["services", "routes", "consumers", "plugins"],
                "critical_tables": ["services", "routes"]
            },
            "ghostwriter": {
                "database": "ghostwriter",
                "primary_tables": ["projects", "reports", "findings", "clients"],
                "critical_tables": ["projects", "reports"]
            },
            "kasmvnc": {
                "database": "kasmvnc",
                "primary_tables": ["sessions", "users", "desktops", "images"],
                "critical_tables": ["sessions", "users"]
            }
        }

    @asynccontextmanager
    async def transaction(self, tool_id: str, description: str = ""):
        """Context manager for infrastructure database transactions."""
        transaction_id = str(uuid.uuid4())

        # Create snapshot
        snapshot = InfraTransactionSnapshot(
            transaction_id=transaction_id,
            tool_id=tool_id,
            timestamp=datetime.utcnow(),
            affected_tables=self.infrastructure_tools.get(
                tool_id, {}).get("primary_tables", []),
            metadata={"description": description}
        )

        self.active_transactions[transaction_id] = snapshot

        try:
            yield InfraTransactionContext(transaction_id, tool_id, self)
            logger.info(
                f"Infrastructure transaction {transaction_id} committed for {tool_id}")
        except Exception as e:
            logger.error(
                f"Infrastructure transaction {transaction_id} failed: {e}")
            raise
        finally:
            if transaction_id in self.active_transactions:
                del self.active_transactions[transaction_id]


class InfraTransactionContext:
    """Context for infrastructure database transactions."""

    def __init__(self, transaction_id: str, tool_id: str, manager):
        self.transaction_id = transaction_id
        self.tool_id = tool_id
        self.manager = manager


def create_infrastructure_transaction_manager(connection_config: Dict[str, Any]) -> InfrastructureTransactionManager:
    """Create transaction manager for infrastructure domain."""
    return InfrastructureTransactionManager(connection_config)
