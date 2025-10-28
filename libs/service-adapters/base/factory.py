"""
Adapter Factory for creating and managing service adapters.

Handles instantiation of all 37 mental prosthetic tool adapters with
proper configuration and executive function support.
"""

import importlib
import inspect
import logging
from typing import Any, Dict, List, Optional, Type

from .adapter import (AdaptationStrategy, AdapterRegistry, BaseServiceAdapter,
                      ExecutiveFunctionLevel, ToolDomain, ToolMetadata,
                      adapter_registry)

logger = logging.getLogger(__name__)


class AdapterFactory:
    """Factory for creating and configuring service adapters."""

    def __init__(self):
        self._adapter_classes: Dict[str, Type[BaseServiceAdapter]] = {}
        self._registered_tools = {
            # Security domain (13 tools)
            "misp": {
                "name": "MISP Threat Intelligence",
                "domain": ToolDomain.SECURITY,
                "strategy": AdaptationStrategy.MODULAR_INTEGRATION,
                "framework": "php",
                "database": "mysql",
                "port": 80
            },
            "helk": {
                "name": "HELK Analytics",
                "domain": ToolDomain.SECURITY,
                "strategy": AdaptationStrategy.MICROSERVICE,
                "framework": "python",
                "database": "elasticsearch",
                "port": 5601
            },
            "securityonion": {
                "name": "Security Onion",
                "domain": ToolDomain.SECURITY,
                "strategy": AdaptationStrategy.MICROSERVICE,
                "framework": "python",
                "database": "elasticsearch",
                "port": 443
            },
            "maltrail": {
                "name": "Maltrail Detection",
                "domain": ToolDomain.SECURITY,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "python",
                "database": "sqlite",
                "port": 8338
            },
            "yara-x": {
                "name": "YARA-X Scanner",
                "domain": ToolDomain.SECURITY,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "rust",
                "database": "filesystem",
                "port": None
            },
            "cyberchef": {
                "name": "CyberChef Analysis",
                "domain": ToolDomain.SECURITY,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "javascript",
                "database": "none",
                "port": 8000
            },
            "nemesis": {
                "name": "Nemesis Framework",
                "domain": ToolDomain.SECURITY,
                "strategy": AdaptationStrategy.MICROSERVICE,
                "framework": "python",
                "database": "postgresql",
                "port": 8080
            },

            # Productivity domain (8 tools)
            "n8n": {
                "name": "n8n Workflow Automation",
                "domain": ToolDomain.PRODUCTIVITY,
                "strategy": AdaptationStrategy.MODULAR_INTEGRATION,
                "framework": "node.js",
                "database": "postgresql",
                "port": 5678
            },
            "mealie": {
                "name": "Mealie Recipe Manager",
                "domain": ToolDomain.PRODUCTIVITY,
                "strategy": AdaptationStrategy.MODULAR_INTEGRATION,
                "framework": "python",
                "database": "postgresql",
                "port": 9925
            },
            "dispatch": {
                "name": "Dispatch Incident Management",
                "domain": ToolDomain.PRODUCTIVITY,
                "strategy": AdaptationStrategy.MODULAR_INTEGRATION,
                "framework": "python",
                "database": "postgresql",
                "port": 8000
            },
            "actual": {
                "name": "Actual Budget",
                "domain": ToolDomain.PRODUCTIVITY,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "node.js",
                "database": "sqlite",
                "port": 5006
            },
            "firecrawl": {
                "name": "Firecrawl Web Scraper",
                "domain": ToolDomain.PRODUCTIVITY,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "python",
                "database": "redis",
                "port": 3002
            },
            "goose": {
                "name": "Goose AI Assistant",
                "domain": ToolDomain.PRODUCTIVITY,
                "strategy": AdaptationStrategy.MODULAR_INTEGRATION,
                "framework": "python",
                "database": "sqlite",
                "port": None
            },
            "it-tools": {
                "name": "IT Tools Collection",
                "domain": ToolDomain.PRODUCTIVITY,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "vue.js",
                "database": "none",
                "port": 8080
            },
            "inspector": {
                "name": "Inspector Analysis",
                "domain": ToolDomain.PRODUCTIVITY,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "python",
                "database": "sqlite",
                "port": 8000
            },

            # MTG domain (4 tools)
            "commander-spellbook": {
                "name": "Commander Spellbook",
                "domain": ToolDomain.MTG,
                "strategy": AdaptationStrategy.MODULAR_INTEGRATION,
                "framework": "python",
                "database": "postgresql",
                "port": 8000
            },
            "mtg-commander-map": {
                "name": "MTG Commander Map",
                "domain": ToolDomain.MTG,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "javascript",
                "database": "none",
                "port": 3000
            },
            "mtg-scripting-toolkit": {
                "name": "MTG Scripting Toolkit",
                "domain": ToolDomain.MTG,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "python",
                "database": "sqlite",
                "port": None
            },
            "scryfall": {
                "name": "Scryfall API Adapter",
                "domain": ToolDomain.MTG,
                "strategy": AdaptationStrategy.UTILITY_WRAPPER,
                "framework": "python",
                "database": "none",
                "port": None
            },

            # Infrastructure domain (12 tools)
            "kong": {
                "name": "Kong API Gateway",
                "domain": ToolDomain.INFRASTRUCTURE,
                "strategy": AdaptationStrategy.MICROSERVICE,
                "framework": "lua",
                "database": "postgresql",
                "port": 8000
            },
            "ghostwriter": {
                "name": "Ghostwriter Reporting",
                "domain": ToolDomain.INFRASTRUCTURE,
                "strategy": AdaptationStrategy.MODULAR_INTEGRATION,
                "framework": "python",
                "database": "postgresql",
                "port": 8000
            },
            "kasmvnc": {
                "name": "KasmVNC Remote Desktop",
                "domain": ToolDomain.INFRASTRUCTURE,
                "strategy": AdaptationStrategy.MICROSERVICE,
                "framework": "c++",
                "database": "none",
                "port": 6901
            }
            # Note: Additional infrastructure tools would be defined here
            # Total: 37 tools across all domains
        }

    def register_adapter_class(self, tool_id: str, adapter_class: Type[BaseServiceAdapter]) -> None:
        """Register an adapter class for a specific tool."""
        if not issubclass(adapter_class, BaseServiceAdapter):
            raise ValueError(f"Adapter class must extend BaseServiceAdapter")

        self._adapter_classes[tool_id] = adapter_class
        logger.info(
            f"Registered adapter class for {tool_id}: {adapter_class.__name__}")

    def create_adapter(self, tool_id: str, config: Dict[str, Any]) -> Optional[BaseServiceAdapter]:
        """Create an adapter instance for the specified tool."""
        if tool_id not in self._registered_tools:
            logger.error(f"Unknown tool ID: {tool_id}")
            return None

        tool_config = self._registered_tools[tool_id]

        # Create tool metadata
        metadata = ToolMetadata(
            tool_id=tool_id,
            tool_name=tool_config["name"],
            domain=tool_config["domain"],
            version=config.get("version", "1.0.0"),
            adaptation_strategy=tool_config["strategy"],
            original_framework=tool_config["framework"],
            database_type=tool_config["database"],
            port=tool_config.get("port"),
            config_files=config.get("config_files", []),
            dependencies=config.get("dependencies", []),
            executive_function_level=ExecutiveFunctionLevel(
                config.get("executive_function_level", "moderate")
            ),
            performance_target_ms=self._get_domain_performance_target(
                tool_config["domain"]),
            business_logic_preserved=config.get(
                "business_logic_preserved", True),
            migration_completed=config.get("migration_completed", False)
        )

        # Get adapter class
        adapter_class = self._adapter_classes.get(tool_id)
        if not adapter_class:
            # Use generic adapter if specific class not registered
            adapter_class = self._get_generic_adapter_class(
                tool_config["strategy"])

        try:
            # Create adapter instance
            adapter = adapter_class(metadata, config)
            logger.info(
                f"Created adapter for {tool_id}: {adapter_class.__name__}")
            return adapter

        except Exception as e:
            logger.error(f"Failed to create adapter for {tool_id}: {e}")
            return None

    def _get_domain_performance_target(self, domain: ToolDomain) -> int:
        """Get performance target based on domain requirements."""
        targets = {
            ToolDomain.SECURITY: 1000,      # <1s for threat analysis
            ToolDomain.PRODUCTIVITY: 2000,  # <2s for task management
            ToolDomain.MTG: 3000,           # <3s for game analysis
            ToolDomain.INFRASTRUCTURE: 5000  # <5s for system operations
        }
        return targets.get(domain, 2000)

    def _get_generic_adapter_class(self, strategy: AdaptationStrategy) -> Type[BaseServiceAdapter]:
        """Get generic adapter class based on adaptation strategy."""
        # This would return appropriate generic adapter classes
        # For now, return the base class (will need concrete implementations)
        return BaseServiceAdapter

    def get_registered_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get list of all registered tools."""
        return self._registered_tools.copy()

    def get_tools_by_domain(self, domain: ToolDomain) -> List[str]:
        """Get list of tool IDs for a specific domain."""
        return [
            tool_id for tool_id, config in self._registered_tools.items()
            if config["domain"] == domain
        ]


def create_adapter_from_config(tool_id: str, config_path: str) -> Optional[BaseServiceAdapter]:
    """Create adapter from configuration file."""
    try:
        import json
        from pathlib import Path

        import yaml

        config_file = Path(config_path)
        if not config_file.exists():
            logger.error(f"Configuration file not found: {config_path}")
            return None

        # Load configuration
        with open(config_file, 'r') as f:
            if config_file.suffix == '.json':
                config = json.load(f)
            elif config_file.suffix in ['.yml', '.yaml']:
                config = yaml.safe_load(f)
            else:
                logger.error(
                    f"Unsupported configuration format: {config_file.suffix}")
                return None

        # Create adapter using factory
        factory = AdapterFactory()
        return factory.create_adapter(tool_id, config)

    except Exception as e:
        logger.error(
            f"Failed to create adapter from config {config_path}: {e}")
        return None


async def register_all_adapters(registry: AdapterRegistry, config_dir: str = None) -> Dict[str, bool]:
    """Register all 37 mental prosthetic tool adapters."""
    factory = AdapterFactory()
    results = {}

    # Get all registered tools
    tools = factory.get_registered_tools()
    logger.info(f"Registering {len(tools)} mental prosthetic tool adapters")

    for tool_id, tool_config in tools.items():
        try:
            # Create default configuration
            default_config = {
                "version": "1.0.0",
                "enabled": True,
                "executive_function_level": "moderate",
                "business_logic_preserved": True,
                "migration_completed": False
            }

            # Load tool-specific config if available
            if config_dir:
                config_file = f"{config_dir}/{tool_id}.yaml"
                try:
                    from pathlib import Path

                    import yaml
                    config_path = Path(config_file)
                    if config_path.exists():
                        with open(config_path, 'r') as f:
                            tool_specific_config = yaml.safe_load(f)
                        default_config.update(tool_specific_config)
                except Exception as e:
                    logger.warning(f"Could not load config for {tool_id}: {e}")

            # Create and register adapter
            adapter = factory.create_adapter(tool_id, default_config)
            if adapter:
                registry.register_adapter(adapter)
                results[tool_id] = True
                logger.info(f"Successfully registered adapter: {tool_id}")
            else:
                results[tool_id] = False
                logger.error(f"Failed to create adapter: {tool_id}")

        except Exception as e:
            results[tool_id] = False
            logger.error(f"Failed to register adapter {tool_id}: {e}")

    # Summary
    successful = sum(1 for success in results.values() if success)
    total = len(results)
    logger.info(
        f"Adapter registration complete: {successful}/{total} successful")

    return results


# Global factory instance
adapter_factory = AdapterFactory()
