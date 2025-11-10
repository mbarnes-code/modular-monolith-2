"""Plugin initialization system preserving MISP's plugin patterns."""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .endpoint_registry import EndpointRegistry, initialize_endpoint_registry
from .interceptors import interceptor_chain
from .operation_catalog import (OperationMetadata, OperationType,
                                operation_catalog)
from .plugin_registry import PluginType, plugin_registry

logger = logging.getLogger(__name__)


class PluginManager:
    """
    Plugin manager preserving MISP's plugin management patterns:
    - Plugin discovery and loading
    - Lifecycle management
    - Configuration management
    - Operation catalog integration
    """

    def __init__(self, app, config: Optional[Dict[str, Any]] = None):
        self.app = app
        self.config = config or {}
        self.endpoint_registry: Optional[EndpointRegistry] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the plugin system."""
        if self._initialized:
            return

        logger.info("Initializing plugin system...")

        # Initialize endpoint registry
        self.endpoint_registry = initialize_endpoint_registry(self.app)

        # Load core MISP plugins
        await self._load_core_plugins()

        # Load external plugins
        await self._load_external_plugins()

        # Initialize all plugins
        await plugin_registry.initialize_all_plugins()

        # Mount dynamic endpoints
        if self.endpoint_registry:
            self.endpoint_registry.mount_routers()

        self._initialized = True
        logger.info("Plugin system initialized successfully")

    async def _load_core_plugins(self) -> None:
        """Load core MISP plugins."""
        core_plugins = [
            # Enrichment plugins
            {
                "name": "ip_enrichment",
                "type": PluginType.ENRICHMENT,
                "module": "src.api.plugins.enrichment.ip_enrichment",
                "config": {"enabled": True}
            },
            {
                "name": "domain_enrichment",
                "type": PluginType.ENRICHMENT,
                "module": "src.api.plugins.enrichment.domain_enrichment",
                "config": {"enabled": True}
            },

            # Export plugins
            {
                "name": "json_export",
                "type": PluginType.EXPORT,
                "module": "src.api.plugins.export.json_export",
                "config": {"enabled": True}
            },
            {
                "name": "csv_export",
                "type": PluginType.EXPORT,
                "module": "src.api.plugins.export.csv_export",
                "config": {"enabled": True}
            },

            # Action plugins
            {
                "name": "email_notification",
                "type": PluginType.ACTION,
                "module": "src.api.plugins.action.email_notification",
                "config": {"enabled": True}
            }
        ]

        for plugin_config in core_plugins:
            try:
                await self._load_plugin_from_config(plugin_config)
            except Exception as e:
                logger.warning(
                    f"Failed to load core plugin {plugin_config['name']}: {str(e)}"
                )

    async def _load_external_plugins(self) -> None:
        """Load external plugins from configured directories."""
        plugin_dirs = self.config.get("plugin_directories", [])

        for plugin_dir in plugin_dirs:
            await self._scan_plugin_directory(plugin_dir)

    async def _scan_plugin_directory(self, plugin_dir: str) -> None:
        """Scan a directory for plugins."""
        try:
            plugin_path = Path(plugin_dir)
            if not plugin_path.exists():
                logger.warning(f"Plugin directory not found: {plugin_dir}")
                return

            # Look for plugin configuration files
            for config_file in plugin_path.glob("**/plugin.json"):
                await self._load_plugin_from_file(config_file)

        except Exception as e:
            logger.error(
                f"Error scanning plugin directory {plugin_dir}: {str(e)}")

    async def _load_plugin_from_file(self, config_file: Path) -> None:
        """Load plugin from configuration file."""
        try:
            import json
            with open(config_file, 'r') as f:
                plugin_config = json.load(f)

            await self._load_plugin_from_config(plugin_config)

        except Exception as e:
            logger.error(f"Failed to load plugin from {config_file}: {str(e)}")

    async def _load_plugin_from_config(self, plugin_config: Dict[str, Any]) -> None:
        """Load plugin from configuration."""
        plugin_name = plugin_config.get("name")
        plugin_module = plugin_config.get("module")
        plugin_config_data = plugin_config.get("config", {})

        if not plugin_name or not plugin_module:
            logger.error("Plugin configuration missing name or module")
            return

        # Load plugin module
        success = await plugin_registry.load_plugin_from_module(
            plugin_module,
            plugin_config_data
        )

        if success:
            logger.info(f"Loaded plugin: {plugin_name}")

            # Register operations in catalog
            await self._register_plugin_operations(plugin_name, plugin_config)
        else:
            logger.error(f"Failed to load plugin: {plugin_name}")

    async def _register_plugin_operations(
        self,
        plugin_name: str,
        plugin_config: Dict[str, Any]
    ) -> None:
        """Register plugin operations in the operation catalog."""
        operations = plugin_config.get("operations", [])

        for op_config in operations:
            try:
                metadata = OperationMetadata(
                    name=op_config["name"],
                    operation_type=OperationType(op_config["type"]),
                    version=op_config.get("version", "1.0.0"),
                    description=op_config.get("description", ""),
                    author=op_config.get("author", "Unknown"),
                    plugin_name=plugin_name,
                    supported_attributes=op_config.get(
                        "supported_attributes", []),
                    config_template=op_config.get("config_template", {}),
                    input_schema=op_config.get("input_schema", {}),
                    output_schema=op_config.get("output_schema", {}),
                    enabled=op_config.get("enabled", True),
                    rate_limited=op_config.get("rate_limited", False),
                    auth_required=op_config.get("auth_required", True)
                )

                operation_catalog.register_operation(metadata)

            except Exception as e:
                logger.error(
                    f"Failed to register operation {op_config.get('name')}: {str(e)}"
                )

    def get_plugin_status(self) -> Dict[str, Any]:
        """Get status of all plugins."""
        plugins = plugin_registry.list_plugins()

        status = {
            "total_plugins": len(plugins),
            "enabled_plugins": len([p for p in plugins if p.enabled]),
            "plugins_by_type": {},
            "plugins": []
        }

        # Count by type
        for plugin in plugins:
            plugin_type = plugin.plugin_type.value
            if plugin_type not in status["plugins_by_type"]:
                status["plugins_by_type"][plugin_type] = 0
            status["plugins_by_type"][plugin_type] += 1

            # Add plugin details
            status["plugins"].append({
                "name": plugin.name,
                "version": plugin.version,
                "type": plugin_type,
                "enabled": plugin.enabled,
                "description": plugin.description,
                "author": plugin.author
            })

        return status

    def get_operation_catalog_status(self) -> Dict[str, Any]:
        """Get status of the operation catalog."""
        return operation_catalog.get_catalog_summary()

    async def reload_plugin(self, plugin_name: str) -> bool:
        """Reload a specific plugin."""
        try:
            # Get current plugin info
            plugin_info = plugin_registry.get_plugin_info(plugin_name)
            if not plugin_info:
                logger.error(f"Plugin not found: {plugin_name}")
                return False

            # Cleanup current plugin
            if plugin_name in plugin_registry._plugins:
                await plugin_registry._plugins[plugin_name].cleanup()

            # Reload plugin module
            if plugin_info.module_path:
                success = await plugin_registry.load_plugin_from_module(
                    plugin_info.module_path,
                    plugin_registry._plugin_configs.get(plugin_name, {})
                )

                if success:
                    await plugin_registry.initialize_plugin(plugin_name)
                    logger.info(f"Reloaded plugin: {plugin_name}")
                    return True

            return False

        except Exception as e:
            logger.error(f"Failed to reload plugin {plugin_name}: {str(e)}")
            return False

    async def shutdown(self) -> None:
        """Shutdown the plugin system."""
        if not self._initialized:
            return

        logger.info("Shutting down plugin system...")

        # Cleanup all plugins
        await plugin_registry.cleanup_all_plugins()

        self._initialized = False
        logger.info("Plugin system shutdown complete")
