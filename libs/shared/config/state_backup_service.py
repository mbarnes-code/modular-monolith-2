"""
Configuration State Backup Service for Mental Prosthetic Platform

Provides comprehensive state backup and restoration capabilities for all 37 integrated tools.
Supports automatic backup scheduling, selective restoration, and configuration consistency validation.

Key Features:
- Automatic backup of configuration states across all domains
- Point-in-time restoration from last known good state
- Configuration drift detection and alerting
- Granular backup control per tool and domain
- Executive function accommodations with clear recovery workflows
"""

import asyncio
import hashlib
import json
import logging
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import yaml

from ..utils.file_operations import atomic_write, ensure_directory
from ..utils.logging import get_logger
from .config_manager import ConfigManager

logger = get_logger(__name__)


class BackupStatus(Enum):
    """Status of backup operations"""
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    PARTIAL = "partial"
    CORRUPTED = "corrupted"


class RestoreStatus(Enum):
    """Status of restore operations"""
    SUCCESS = "success"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    VALIDATION_FAILED = "validation_failed"
    ROLLBACK_COMPLETED = "rollback_completed"


@dataclass
class ConfigBackup:
    """Configuration backup metadata"""
    backup_id: str
    timestamp: datetime
    domain: str
    tool_name: str
    config_path: str
    backup_path: str
    config_hash: str
    size_bytes: int
    status: BackupStatus
    metadata: Dict[str, Any]


@dataclass
class BackupPolicy:
    """Backup policy configuration"""
    domain: str
    tool_name: str
    backup_frequency_minutes: int
    retention_days: int
    enabled: bool
    critical: bool  # Critical configs get immediate backup on change
    validation_required: bool


class StateBackupService:
    """
    Configuration state backup and restoration service

    Manages backup lifecycle for all 37 integrated tools across 4 domains.
    Provides point-in-time recovery and configuration consistency validation.
    """

    def __init__(self, config_manager: ConfigManager, backup_root: str = "/var/lib/jane/backups"):
        self.config_manager = config_manager
        self.backup_root = Path(backup_root)
        self.backup_metadata_file = self.backup_root / "backup_metadata.json"
        self.policies_file = self.backup_root / "backup_policies.yaml"

        # Initialize backup storage
        ensure_directory(str(self.backup_root))
        ensure_directory(str(self.backup_root / "configs"))
        ensure_directory(str(self.backup_root / "metadata"))

        # Load backup policies
        self.policies = self._load_backup_policies()

        # Backup metadata cache
        self.backup_metadata: Dict[str, ConfigBackup] = {}
        self._load_backup_metadata()

        # Track last backup times
        self.last_backup_times: Dict[str, datetime] = {}

    def _load_backup_policies(self) -> Dict[str, BackupPolicy]:
        """Load backup policies from configuration file"""
        try:
            if self.policies_file.exists():
                with open(self.policies_file, 'r') as f:
                    policy_data = yaml.safe_load(f)
                    return {
                        f"{p['domain']}_{p['tool_name']}": BackupPolicy(**p)
                        for p in policy_data.get('policies', [])
                    }
            else:
                # Create default policies for all 37 tools
                return self._create_default_policies()
        except Exception as e:
            logger.error(f"Failed to load backup policies: {e}")
            return self._create_default_policies()

    def _create_default_policies(self) -> Dict[str, BackupPolicy]:
        """Create default backup policies for all integrated tools"""
        policies = {}

        # Security domain (13 tools) - Critical, frequent backups
        security_tools = [
            "misp", "helk", "securityonion", "maltrail", "yara-x", "cyberchef",
            "nemesis", "apiscout", "blackarch", "brute-ratel", "hexstrike",
            "meterpreter", "onex"
        ]
        for tool in security_tools:
            key = f"security_{tool}"
            policies[key] = BackupPolicy(
                domain="security",
                tool_name=tool,
                backup_frequency_minutes=15,  # Every 15 minutes
                retention_days=30,
                enabled=True,
                critical=True,
                validation_required=True
            )

        # Productivity domain (8 tools) - Regular backups
        productivity_tools = [
            "n8n", "mealie", "dispatch", "actual-budget", "firecrawl",
            "goose", "it-tools", "inspector"
        ]
        for tool in productivity_tools:
            key = f"productivity_{tool}"
            policies[key] = BackupPolicy(
                domain="productivity",
                tool_name=tool,
                backup_frequency_minutes=30,  # Every 30 minutes
                retention_days=14,
                enabled=True,
                critical=False,
                validation_required=True
            )

        # MTG domain (4 tools) - Moderate backups
        mtg_tools = [
            "commander-spellbook", "mtg-commander-map", "mtg-scripting-toolkit",
            "card-analysis"
        ]
        for tool in mtg_tools:
            key = f"mtg_{tool}"
            policies[key] = BackupPolicy(
                domain="mtg",
                tool_name=tool,
                backup_frequency_minutes=60,  # Every hour
                retention_days=7,
                enabled=True,
                critical=False,
                validation_required=False
            )

        # Infrastructure domain (12+ tools) - System-critical backups
        infrastructure_tools = [
            "kong", "ghostwriter", "kasmvnc", "chroma-mcp", "virustotal-mcp",
            "n8n-mcp", "firecrawl-mcp", "malwarebazaar-mcp", "filescopemcp",
            "lscript", "rita", "software-forensic-kit"
        ]
        for tool in infrastructure_tools:
            key = f"infrastructure_{tool}"
            policies[key] = BackupPolicy(
                domain="infrastructure",
                tool_name=tool,
                backup_frequency_minutes=60,  # Every hour
                retention_days=14,
                enabled=True,
                critical=True,
                validation_required=True
            )

        # Save default policies
        self._save_backup_policies(policies)
        return policies

    def _save_backup_policies(self, policies: Dict[str, BackupPolicy]):
        """Save backup policies to file"""
        try:
            policy_data = {
                'policies': [asdict(policy) for policy in policies.values()]
            }
            with open(self.policies_file, 'w') as f:
                yaml.dump(policy_data, f, default_flow_style=False)
        except Exception as e:
            logger.error(f"Failed to save backup policies: {e}")

    def _load_backup_metadata(self):
        """Load backup metadata from storage"""
        try:
            if self.backup_metadata_file.exists():
                with open(self.backup_metadata_file, 'r') as f:
                    metadata_data = json.load(f)
                    self.backup_metadata = {
                        k: ConfigBackup(
                            backup_id=v['backup_id'],
                            timestamp=datetime.fromisoformat(v['timestamp']),
                            domain=v['domain'],
                            tool_name=v['tool_name'],
                            config_path=v['config_path'],
                            backup_path=v['backup_path'],
                            config_hash=v['config_hash'],
                            size_bytes=v['size_bytes'],
                            status=BackupStatus(v['status']),
                            metadata=v['metadata']
                        )
                        for k, v in metadata_data.items()
                    }
        except Exception as e:
            logger.error(f"Failed to load backup metadata: {e}")
            self.backup_metadata = {}

    def _save_backup_metadata(self):
        """Save backup metadata to storage"""
        try:
            metadata_data = {
                k: {
                    'backup_id': v.backup_id,
                    'timestamp': v.timestamp.isoformat(),
                    'domain': v.domain,
                    'tool_name': v.tool_name,
                    'config_path': v.config_path,
                    'backup_path': v.backup_path,
                    'config_hash': v.config_hash,
                    'size_bytes': v.size_bytes,
                    'status': v.status.value,
                    'metadata': v.metadata
                }
                for k, v in self.backup_metadata.items()
            }
            atomic_write(str(self.backup_metadata_file),
                         json.dumps(metadata_data, indent=2))
        except Exception as e:
            logger.error(f"Failed to save backup metadata: {e}")

    def _calculate_config_hash(self, config_path: str) -> str:
        """Calculate hash of configuration file for change detection"""
        try:
            with open(config_path, 'rb') as f:
                content = f.read()
                return hashlib.sha256(content).hexdigest()
        except Exception as e:
            logger.error(f"Failed to calculate hash for {config_path}: {e}")
            return ""

    async def create_backup(self, domain: str, tool_name: str, config_path: str,
                            metadata: Optional[Dict[str, Any]] = None) -> Optional[ConfigBackup]:
        """Create backup of configuration file"""
        try:
            key = f"{domain}_{tool_name}"
            if key not in self.policies:
                logger.warning(f"No backup policy found for {key}")
                return None

            policy = self.policies[key]
            if not policy.enabled:
                logger.debug(f"Backup disabled for {key}")
                return None

            # Check if config file exists
            config_file = Path(config_path)
            if not config_file.exists():
                logger.error(f"Configuration file not found: {config_path}")
                return None

            # Calculate config hash
            config_hash = self._calculate_config_hash(config_path)
            if not config_hash:
                return None

            # Check if backup is needed (hash comparison)
            latest_backup = self.get_latest_backup(domain, tool_name)
            if latest_backup and latest_backup.config_hash == config_hash:
                logger.debug(f"No changes detected for {key}, skipping backup")
                return latest_backup

            # Create backup
            timestamp = datetime.utcnow()
            backup_id = f"{domain}_{tool_name}_{timestamp.strftime('%Y%m%d_%H%M%S')}"

            # Create domain-specific backup directory
            backup_dir = self.backup_root / "configs" / domain
            ensure_directory(str(backup_dir))

            backup_path = backup_dir / f"{backup_id}.backup"

            # Copy configuration file
            shutil.copy2(config_path, backup_path)

            # Get file size
            size_bytes = backup_path.stat().st_size

            # Create backup metadata
            backup = ConfigBackup(
                backup_id=backup_id,
                timestamp=timestamp,
                domain=domain,
                tool_name=tool_name,
                config_path=config_path,
                backup_path=str(backup_path),
                config_hash=config_hash,
                size_bytes=size_bytes,
                status=BackupStatus.SUCCESS,
                metadata=metadata or {}
            )

            # Store backup metadata
            self.backup_metadata[backup_id] = backup
            self._save_backup_metadata()

            # Update last backup time
            self.last_backup_times[key] = timestamp

            logger.info(f"Created backup {backup_id} for {key}")
            return backup

        except Exception as e:
            logger.error(
                f"Failed to create backup for {domain}_{tool_name}: {e}")
            return None

    async def restore_from_backup(self, backup_id: str, validate: bool = True) -> RestoreStatus:
        """Restore configuration from backup"""
        try:
            if backup_id not in self.backup_metadata:
                logger.error(f"Backup not found: {backup_id}")
                return RestoreStatus.FAILED

            backup = self.backup_metadata[backup_id]

            # Check if backup file exists
            backup_file = Path(backup.backup_path)
            if not backup_file.exists():
                logger.error(f"Backup file not found: {backup.backup_path}")
                return RestoreStatus.FAILED

            # Validate backup integrity if requested
            if validate:
                backup_hash = self._calculate_config_hash(backup.backup_path)
                if backup_hash != backup.config_hash:
                    logger.error(
                        f"Backup integrity check failed for {backup_id}")
                    backup.status = BackupStatus.CORRUPTED
                    self._save_backup_metadata()
                    return RestoreStatus.VALIDATION_FAILED

            # Create backup of current config before restore
            current_config = Path(backup.config_path)
            if current_config.exists():
                current_backup_path = f"{backup.config_path}.restore_backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(backup.config_path, current_backup_path)
                logger.info(
                    f"Created current config backup: {current_backup_path}")

            # Restore configuration
            shutil.copy2(backup.backup_path, backup.config_path)

            logger.info(
                f"Successfully restored configuration from backup {backup_id}")
            return RestoreStatus.SUCCESS

        except Exception as e:
            logger.error(f"Failed to restore from backup {backup_id}: {e}")
            return RestoreStatus.FAILED

    def get_latest_backup(self, domain: str, tool_name: str) -> Optional[ConfigBackup]:
        """Get the latest backup for a specific tool"""
        tool_backups = [
            backup for backup in self.backup_metadata.values()
            if backup.domain == domain and backup.tool_name == tool_name
        ]

        if not tool_backups:
            return None

        return max(tool_backups, key=lambda b: b.timestamp)

    def get_backups_by_tool(self, domain: str, tool_name: str) -> List[ConfigBackup]:
        """Get all backups for a specific tool, sorted by timestamp (newest first)"""
        tool_backups = [
            backup for backup in self.backup_metadata.values()
            if backup.domain == domain and backup.tool_name == tool_name
        ]

        return sorted(tool_backups, key=lambda b: b.timestamp, reverse=True)

    def cleanup_old_backups(self):
        """Clean up old backups based on retention policies"""
        try:
            for key, policy in self.policies.items():
                if not policy.enabled:
                    continue

                cutoff_date = datetime.utcnow() - timedelta(days=policy.retention_days)

                # Find old backups
                old_backups = [
                    backup for backup in self.backup_metadata.values()
                    if (backup.domain == policy.domain and
                        backup.tool_name == policy.tool_name and
                        backup.timestamp < cutoff_date)
                ]

                # Delete old backups
                for backup in old_backups:
                    try:
                        backup_file = Path(backup.backup_path)
                        if backup_file.exists():
                            backup_file.unlink()

                        # Remove from metadata
                        del self.backup_metadata[backup.backup_id]

                        logger.info(
                            f"Cleaned up old backup: {backup.backup_id}")

                    except Exception as e:
                        logger.error(
                            f"Failed to cleanup backup {backup.backup_id}: {e}")

            # Save updated metadata
            self._save_backup_metadata()

        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {e}")

    async def automatic_backup_scheduler(self):
        """Background scheduler for automatic backups"""
        while True:
            try:
                current_time = datetime.utcnow()

                for key, policy in self.policies.items():
                    if not policy.enabled:
                        continue

                    # Check if backup is due
                    last_backup = self.last_backup_times.get(key)
                    if (not last_backup or
                            current_time - last_backup >= timedelta(minutes=policy.backup_frequency_minutes)):

                        # Get current config path from config manager
                        config_path = await self.config_manager.get_config_path(
                            policy.domain, policy.tool_name
                        )

                        if config_path:
                            await self.create_backup(
                                policy.domain,
                                policy.tool_name,
                                config_path,
                                {"automated": True, "policy": key}
                            )

                # Cleanup old backups
                self.cleanup_old_backups()

                # Wait before next check (5 minutes)
                await asyncio.sleep(300)

            except Exception as e:
                logger.error(f"Error in automatic backup scheduler: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry

    def get_backup_statistics(self) -> Dict[str, Any]:
        """Get backup statistics and health information"""
        stats = {
            "total_backups": len(self.backup_metadata),
            "backup_size_mb": sum(b.size_bytes for b in self.backup_metadata.values()) / (1024 * 1024),
            "domains": {},
            "status_counts": {},
            "health_score": 0.0
        }

        # Domain statistics
        for backup in self.backup_metadata.values():
            domain = backup.domain
            if domain not in stats["domains"]:
                stats["domains"][domain] = {
                    "backup_count": 0,
                    "size_mb": 0,
                    "tools": set()
                }

            stats["domains"][domain]["backup_count"] += 1
            stats["domains"][domain]["size_mb"] += backup.size_bytes / \
                (1024 * 1024)
            stats["domains"][domain]["tools"].add(backup.tool_name)

        # Convert sets to lists for JSON serialization
        for domain_stats in stats["domains"].values():
            domain_stats["tools"] = list(domain_stats["tools"])

        # Status counts
        for backup in self.backup_metadata.values():
            status = backup.status.value
            stats["status_counts"][status] = stats["status_counts"].get(
                status, 0) + 1

        # Calculate health score (percentage of successful backups)
        total = len(self.backup_metadata)
        successful = stats["status_counts"].get("success", 0)
        stats["health_score"] = (
            successful / total * 100) if total > 0 else 0.0

        return stats


# Global backup service instance
_backup_service: Optional[StateBackupService] = None


def get_backup_service(config_manager: Optional[ConfigManager] = None) -> StateBackupService:
    """Get or create the global backup service instance"""
    global _backup_service
    if _backup_service is None:
        if config_manager is None:
            raise ValueError("ConfigManager required for first initialization")
        _backup_service = StateBackupService(config_manager)
    return _backup_service


async def create_backup(domain: str, tool_name: str, config_path: str) -> Optional[ConfigBackup]:
    """Convenience function to create a backup"""
    service = get_backup_service()
    return await service.create_backup(domain, tool_name, config_path)


async def restore_backup(backup_id: str) -> RestoreStatus:
    """Convenience function to restore from backup"""
    service = get_backup_service()
    return await service.restore_from_backup(backup_id)
