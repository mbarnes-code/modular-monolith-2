"""
Database Transaction Rollback Manager for Productivity Domain

Manages database transactions and rollback capabilities for all 8
productivity tools (n8n, Mealie, Dispatch, Actual Budget, Firecrawl,
Goose, IT-Tools, Inspector) with business logic preservation.
"""

import asyncio
import logging
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional

# Import the base classes from security service to avoid duplication
from ...security_service.src.data.transaction_manager import (
    DatabaseTransactionManager, RollbackOperation, TransactionContext,
    TransactionSnapshot, TransactionStatus)

logger = logging.getLogger(__name__)


class ProductivityTransactionManager(DatabaseTransactionManager):
    """Transaction manager specialized for productivity domain tools."""

    def __init__(self, connection_config: Dict[str, Any]):
        super().__init__(connection_config)

        # Productivity domain tools (8 tools)
        self.productivity_tools = {
            "n8n": {
                "database": "n8n",
                "primary_tables": ["workflows", "executions", "credentials", "users"],
                "critical_tables": ["workflows", "executions"]
            },
            "mealie": {
                "database": "mealie",
                "primary_tables": ["recipes", "meal_plans", "shopping_lists", "users"],
                "critical_tables": ["recipes", "meal_plans"]
            },
            "dispatch": {
                "database": "dispatch",
                "primary_tables": ["incidents", "tasks", "notifications", "teams"],
                "critical_tables": ["incidents", "tasks"]
            },
            "actual": {
                "database": "actual",
                "primary_tables": ["accounts", "transactions", "budgets", "categories"],
                "critical_tables": ["transactions", "budgets"]
            },
            "firecrawl": {
                "database": "firecrawl",
                "primary_tables": ["crawl_jobs", "pages", "extractions", "schedules"],
                "critical_tables": ["crawl_jobs", "extractions"]
            },
            "goose": {
                "database": "goose",
                "primary_tables": ["conversations", "messages", "models", "users"],
                "critical_tables": ["conversations", "messages"]
            },
            "it-tools": {
                "database": "ittools",
                "primary_tables": ["tools", "usage_logs", "favorites", "users"],
                "critical_tables": ["usage_logs", "favorites"]
            },
            "inspector": {
                "database": "inspector",
                "primary_tables": ["analyses", "reports", "datasets", "projects"],
                "critical_tables": ["analyses", "reports"]
            }
        }

        # Override the security_tools with productivity_tools
        self.security_tools = self.productivity_tools


def create_productivity_transaction_manager(connection_config: Dict[str, Any]) -> ProductivityTransactionManager:
    """Create transaction manager for productivity domain."""
    return ProductivityTransactionManager(connection_config)
