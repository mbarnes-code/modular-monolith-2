"""
Configuration management for service adapters.

Handles loading and validation of configuration for all 37 mental
prosthetic tools with executive function accommodations.
"""

import json
import logging
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


@dataclass
class AdapterConfig:
    """Configuration for a service adapter."""
    tool_id: str
    enabled: bool = True
    version: str = "1.0.0"
    host: str = "localhost"
    port: Optional[int] = None
    database_url: Optional[str] = None
    api_key: Optional[str] = None

    # Executive function settings
    executive_function_level: str = "moderate"
    ui_response_threshold_ms: int = 200
    adhd_mode_enabled: bool = False
    focus_assist_enabled: bool = True

    # Performance settings
    performance_target_ms: int = 2000
    max_concurrent_requests: int = 10
    timeout_seconds: int = 30

    # Business logic preservation
    business_logic_preserved: bool = True
    migration_completed: bool = False

    # Tool-specific settings
    tool_specific_config: Dict[str, Any] = None

    def __post_init__(self):
        if self.tool_specific_config is None:
            self.tool_specific_config = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AdapterConfig':
        """Create configuration from dictionary."""
        return cls(**data)


class ConfigurationManager:
    """Manages configuration for all service adapters."""

    def __init__(self, config_dir: str = "config/adapters"):
        self.config_dir = Path(config_dir)
        self.configs: Dict[str, AdapterConfig] = {}
        self.default_configs = self._get_default_configurations()

    def _get_default_configurations(self) -> Dict[str, Dict[str, Any]]:
        """Get default configurations for all 37 tools."""
        return {
            # Security domain
            "misp": {
                "port": 80,
                "performance_target_ms": 1000,
                "tool_specific_config": {
                    "api_version": "v2.4",
                    "ssl_verify": True
                }
            },
            "helk": {
                "port": 5601,
                "performance_target_ms": 1000,
                "tool_specific_config": {
                    "elasticsearch_url": "http://localhost:9200"
                }
            },
            "securityonion": {
                "port": 443,
                "performance_target_ms": 1000,
                "tool_specific_config": {
                    "ssl_enabled": True
                }
            },
            "maltrail": {
                "port": 8338,
                "performance_target_ms": 1000
            },
            "yara-x": {
                "port": None,
                "performance_target_ms": 1000,
                "tool_specific_config": {
                    "rules_path": "/etc/yara/rules"
                }
            },
            "cyberchef": {
                "port": 8000,
                "performance_target_ms": 1000
            },
            "nemesis": {
                "port": 8080,
                "performance_target_ms": 1000,
                "database_url": "postgresql://localhost:5432/nemesis"
            },

            # Productivity domain
            "n8n": {
                "port": 5678,
                "performance_target_ms": 2000,
                "database_url": "postgresql://localhost:5432/n8n"
            },
            "mealie": {
                "port": 9925,
                "performance_target_ms": 2000,
                "database_url": "postgresql://localhost:5432/mealie"
            },
            "dispatch": {
                "port": 8000,
                "performance_target_ms": 2000,
                "database_url": "postgresql://localhost:5432/dispatch"
            },
            "actual": {
                "port": 5006,
                "performance_target_ms": 2000,
                "tool_specific_config": {
                    "data_dir": "/data/actual"
                }
            },
            "firecrawl": {
                "port": 3002,
                "performance_target_ms": 2000,
                "tool_specific_config": {
                    "redis_url": "redis://localhost:6379"
                }
            },
            "goose": {
                "port": None,
                "performance_target_ms": 2000,
                "tool_specific_config": {
                    "model_provider": "openai"
                }
            },
            "it-tools": {
                "port": 8080,
                "performance_target_ms": 2000
            },
            "inspector": {
                "port": 8000,
                "performance_target_ms": 2000
            },

            # MTG domain
            "commander-spellbook": {
                "port": 8000,
                "performance_target_ms": 3000,
                "database_url": "postgresql://localhost:5432/spellbook"
            },
            "mtg-commander-map": {
                "port": 3000,
                "performance_target_ms": 3000
            },
            "mtg-scripting-toolkit": {
                "port": None,
                "performance_target_ms": 3000,
                "tool_specific_config": {
                    "scryfall_api_delay_ms": 100
                }
            },
            "scryfall": {
                "port": None,
                "performance_target_ms": 3000,
                "tool_specific_config": {
                    "api_base_url": "https://api.scryfall.com",
                    "rate_limit_delay_ms": 100
                }
            },

            # Infrastructure domain
            "kong": {
                "port": 8000,
                "performance_target_ms": 5000,
                "database_url": "postgresql://localhost:5432/kong"
            },
            "ghostwriter": {
                "port": 8000,
                "performance_target_ms": 5000,
                "database_url": "postgresql://localhost:5432/ghostwriter"
            },
            "kasmvnc": {
                "port": 6901,
                "performance_target_ms": 5000,
                "tool_specific_config": {
                    "vnc_password": "secret"
                }
            }
        }

    def load_config(self, tool_id: str) -> AdapterConfig:
        """Load configuration for a specific tool."""
        if tool_id in self.configs:
            return self.configs[tool_id]

        # Try to load from file
        config_file = self.config_dir / f"{tool_id}.yaml"
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    file_config = yaml.safe_load(f)
                config = AdapterConfig.from_dict(file_config)
                self.configs[tool_id] = config
                return config
            except Exception as e:
                logger.warning(
                    f"Failed to load config file for {tool_id}: {e}")

        # Use default configuration
        default_config = self.default_configs.get(tool_id, {})
        config_dict = {
            "tool_id": tool_id,
            **default_config
        }
        config = AdapterConfig.from_dict(config_dict)
        self.configs[tool_id] = config

        return config

    def save_config(self, tool_id: str, config: AdapterConfig) -> bool:
        """Save configuration to file."""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            config_file = self.config_dir / f"{tool_id}.yaml"

            with open(config_file, 'w') as f:
                yaml.dump(config.to_dict(), f, default_flow_style=False)

            self.configs[tool_id] = config
            logger.info(f"Saved configuration for {tool_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to save config for {tool_id}: {e}")
            return False

    def load_all_configs(self) -> Dict[str, AdapterConfig]:
        """Load configurations for all tools."""
        all_tool_ids = set(self.default_configs.keys())

        # Add any additional config files found
        if self.config_dir.exists():
            for config_file in self.config_dir.glob("*.yaml"):
                tool_id = config_file.stem
                all_tool_ids.add(tool_id)

        configs = {}
        for tool_id in all_tool_ids:
            configs[tool_id] = self.load_config(tool_id)

        return configs

    def validate_config(self, config: AdapterConfig) -> List[str]:
        """Validate adapter configuration."""
        errors = []

        # Basic validation
        if not config.tool_id:
            errors.append("tool_id is required")

        # Performance validation
        if config.performance_target_ms <= 0:
            errors.append("performance_target_ms must be positive")

        if config.ui_response_threshold_ms <= 0:
            errors.append("ui_response_threshold_ms must be positive")

        # Executive function validation
        valid_ef_levels = ["minimal", "moderate", "comprehensive"]
        if config.executive_function_level not in valid_ef_levels:
            errors.append(
                f"executive_function_level must be one of: {valid_ef_levels}")

        # Network validation
        if config.port is not None and (config.port < 1 or config.port > 65535):
            errors.append("port must be between 1 and 65535")

        return errors


def load_adapter_configs(config_dir: str = "config/adapters") -> Dict[str, AdapterConfig]:
    """Load all adapter configurations."""
    manager = ConfigurationManager(config_dir)
    return manager.load_all_configs()


def validate_config(config: AdapterConfig) -> List[str]:
    """Validate a single adapter configuration."""
    manager = ConfigurationManager()
    return manager.validate_config(config)


# Global configuration manager
config_manager = ConfigurationManager()
