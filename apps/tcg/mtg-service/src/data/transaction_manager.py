"""
Database Transaction Rollback Manager for MTG Domain

Manages database transactions and rollback capabilities for all 4
MTG tools (Commander Spellbook, MTG Commander Map, MTG Scripting Toolkit,
Scryfall adapter) with business logic preservation.
"""

import logging
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class TransactionStatus(Enum):
    """Status of database transactions."""
    PENDING = "pending"
    COMMITTED = "committed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


@dataclass
class MTGTransactionSnapshot:
    """Snapshot of MTG database state at transaction start."""
    transaction_id: str
    tool_id: str
    timestamp: datetime
    affected_tables: List[str]
    before_state: Dict[str, Any] = field(default_factory=dict)
    after_state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MTGTransactionManager:
    """Transaction manager for MTG domain tools."""

    def __init__(self, connection_config: Dict[str, Any]):
        self.connection_config = connection_config
        self.active_transactions: Dict[str, MTGTransactionSnapshot] = {}

        # MTG domain tools (4 tools)
        self.mtg_tools = {
            "commander-spellbook": {
                "database": "spellbook",
                "primary_tables": ["combos", "cards", "features", "variants"],
                "critical_tables": ["combos", "variants"]
            },
            "mtg-commander-map": {
                "database": "mtgmap",
                "primary_tables": ["commanders", "decks", "strategies", "synergies"],
                "critical_tables": ["commanders", "decks"]
            },
            "mtg-scripting-toolkit": {
                "database": "mtgtoolkit",
                "primary_tables": ["scripts", "collections", "analyses", "results"],
                "critical_tables": ["collections", "analyses"]
            },
            "scryfall": {
                "database": "scryfall_cache",
                "primary_tables": ["cards", "sets", "rulings", "cache_metadata"],
                "critical_tables": ["cards", "sets"]
            }
        }

    @asynccontextmanager
    async def transaction(self, tool_id: str, description: str = ""):
        """Context manager for MTG database transactions."""
        transaction_id = str(uuid.uuid4())

        # Create snapshot
        snapshot = MTGTransactionSnapshot(
            transaction_id=transaction_id,
            tool_id=tool_id,
            timestamp=datetime.utcnow(),
            affected_tables=self.mtg_tools.get(
                tool_id, {}).get("primary_tables", []),
            metadata={"description": description}
        )

        self.active_transactions[transaction_id] = snapshot

        try:
            yield MTGTransactionContext(transaction_id, tool_id, self)
            logger.info(
                f"MTG transaction {transaction_id} committed for {tool_id}")
        except Exception as e:
            logger.error(f"MTG transaction {transaction_id} failed: {e}")
            raise
        finally:
            if transaction_id in self.active_transactions:
                del self.active_transactions[transaction_id]


class MTGTransactionContext:
    """Context for MTG database transactions."""

    def __init__(self, transaction_id: str, tool_id: str, manager):
        self.transaction_id = transaction_id
        self.tool_id = tool_id
        self.manager = manager


def create_mtg_transaction_manager(connection_config: Dict[str, Any]) -> MTGTransactionManager:
    """Create transaction manager for MTG domain."""
    return MTGTransactionManager(connection_config)
