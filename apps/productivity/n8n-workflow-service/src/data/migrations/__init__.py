"""
Database migrations framework for the orchestration layer.

This module provides the foundation for PostgreSQL schema migrations
across all domain services in the Mental Prosthetic Platform.
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import asyncpg
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class MigrationManager:
    """
    Manages PostgreSQL database migrations for the orchestration layer.

    Handles schema versioning, migration execution, and rollback capabilities
    for all 37 integrated tools across 4 domains.
    """

    def __init__(self, database_url: str):
        self.database_url = database_url
        self.migrations_dir = Path(__file__).parent
        self.engine = create_async_engine(database_url)
        self.SessionLocal = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )

    async def initialize_migration_table(self) -> None:
        """Initialize the migrations tracking table."""
        async with self.engine.begin() as conn:
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS migration_history (
                    id SERIAL PRIMARY KEY,
                    migration_name VARCHAR(255) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    rollback_sql TEXT,
                    checksum VARCHAR(64)
                )
            """))

    async def get_applied_migrations(self) -> List[str]:
        """Get list of applied migration names."""
        async with self.engine.begin() as conn:
            result = await conn.execute(text("""
                SELECT migration_name FROM migration_history 
                ORDER BY applied_at
            """))
            return [row[0] for row in result.fetchall()]

    async def apply_migration(self, migration_name: str, sql: str, rollback_sql: str = "") -> None:
        """Apply a single migration with rollback capability."""
        async with self.engine.begin() as conn:
            try:
                # Execute migration
                await conn.execute(text(sql))

                # Record in migration history
                await conn.execute(text("""
                    INSERT INTO migration_history (migration_name, rollback_sql)
                    VALUES (:name, :rollback)
                """), {"name": migration_name, "rollback": rollback_sql})

                logger.info(f"Applied migration: {migration_name}")

            except Exception as e:
                logger.error(
                    f"Failed to apply migration {migration_name}: {e}")
                raise

    async def rollback_migration(self, migration_name: str) -> None:
        """Rollback a specific migration."""
        async with self.engine.begin() as conn:
            # Get rollback SQL
            result = await conn.execute(text("""
                SELECT rollback_sql FROM migration_history 
                WHERE migration_name = :name
            """), {"name": migration_name})

            row = result.fetchone()
            if not row or not row[0]:
                raise ValueError(
                    f"No rollback available for migration: {migration_name}")

            # Execute rollback
            await conn.execute(text(row[0]))

            # Remove from history
            await conn.execute(text("""
                DELETE FROM migration_history WHERE migration_name = :name
            """), {"name": migration_name})

            logger.info(f"Rolled back migration: {migration_name}")


# Domain-specific schema definitions for 37-tool integration
DOMAIN_SCHEMAS = {
    "security": {
        "tools": ["misp", "helk", "securityonion", "maltrail", "yara_x", "cyberchef",
                  "nemesis", "apiscout", "brute_ratel", "meterpreter", "lscript", "rita", "software_forensic_kit"],
        "schema": """
            CREATE SCHEMA IF NOT EXISTS security_domain;
            
            -- Security tool configurations and state
            CREATE TABLE IF NOT EXISTS security_domain.tool_configs (
                id SERIAL PRIMARY KEY,
                tool_name VARCHAR(100) NOT NULL,
                config_data JSONB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Security workflow orchestration
            CREATE TABLE IF NOT EXISTS security_domain.security_workflows (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                tools_involved VARCHAR[] NOT NULL,
                workflow_data JSONB NOT NULL,
                status VARCHAR(50) DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    },
    "productivity": {
        "tools": ["n8n", "mealie", "dispatch", "actual", "firecrawl", "goose", "it_tools", "inspector"],
        "schema": """
            CREATE SCHEMA IF NOT EXISTS productivity_domain;
            
            -- Productivity tool data
            CREATE TABLE IF NOT EXISTS productivity_domain.tool_data (
                id SERIAL PRIMARY KEY,
                tool_name VARCHAR(100) NOT NULL,
                user_data JSONB NOT NULL,
                sync_status VARCHAR(50) DEFAULT 'synced',
                last_sync TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Cross-tool workflow tracking
            CREATE TABLE IF NOT EXISTS productivity_domain.workflow_state (
                id SERIAL PRIMARY KEY,
                workflow_id VARCHAR(255) NOT NULL,
                current_step INTEGER DEFAULT 0,
                state_data JSONB NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    },
    "mtg": {
        "tools": ["commander_spellbook", "mtg_commander_map", "mtg_scripting_toolkit", "card_analysis"],
        "schema": """
            CREATE SCHEMA IF NOT EXISTS mtg_domain;
            
            -- MTG deck and card data
            CREATE TABLE IF NOT EXISTS mtg_domain.deck_data (
                id SERIAL PRIMARY KEY,
                deck_name VARCHAR(255) NOT NULL,
                commander VARCHAR(255),
                deck_list JSONB NOT NULL,
                analysis_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- MTG tool integrations
            CREATE TABLE IF NOT EXISTS mtg_domain.tool_integrations (
                id SERIAL PRIMARY KEY,
                tool_name VARCHAR(100) NOT NULL,
                integration_data JSONB NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    },
    "infrastructure": {
        "tools": ["kong", "ghostwriter", "kasmvnc", "chroma_mcp", "filescopemcp", "firecrawl_mcp",
                  "n8n_mcp", "malwarebazaar_mcp", "mcp_virustotal", "onex", "hexstrike_ai", "blackarch"],
        "schema": """
            CREATE SCHEMA IF NOT EXISTS infrastructure_domain;
            
            -- Infrastructure service configurations
            CREATE TABLE IF NOT EXISTS infrastructure_domain.service_configs (
                id SERIAL PRIMARY KEY,
                service_name VARCHAR(100) NOT NULL,
                config_data JSONB NOT NULL,
                status VARCHAR(50) DEFAULT 'active',
                last_health_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            -- MCP server management
            CREATE TABLE IF NOT EXISTS infrastructure_domain.mcp_servers (
                id SERIAL PRIMARY KEY,
                server_name VARCHAR(100) NOT NULL,
                endpoint_url VARCHAR(500) NOT NULL,
                capabilities JSONB NOT NULL,
                status VARCHAR(50) DEFAULT 'running',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """
    }
}


async def initialize_database_schemas() -> None:
    """Initialize all domain schemas for the Mental Prosthetic Platform."""
    from ..config import get_database_url

    migration_manager = MigrationManager(get_database_url())

    # Initialize migration tracking
    await migration_manager.initialize_migration_table()

    # Apply domain schemas
    for domain_name, domain_config in DOMAIN_SCHEMAS.items():
        migration_name = f"001_init_{domain_name}_domain"
        applied_migrations = await migration_manager.get_applied_migrations()

        if migration_name not in applied_migrations:
            rollback_sql = f"DROP SCHEMA IF EXISTS {domain_name}_domain CASCADE;"
            await migration_manager.apply_migration(
                migration_name,
                domain_config["schema"],
                rollback_sql
            )
            logger.info(f"Initialized {domain_name} domain schema")


if __name__ == "__main__":
    asyncio.run(initialize_database_schemas())
