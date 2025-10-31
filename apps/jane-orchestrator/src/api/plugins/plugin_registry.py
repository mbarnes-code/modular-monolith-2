"""Plugin registration system preserving MISP's plugin patterns."""

import importlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type

logger = logging.getLogger(__name__)


class PluginType(Enum):
    """Types of plugins supported by MISP."""
    ENRICHMENT = "enrichment"
    EXPORT = "export"
    IMPORT = "import"
    ACTION = "action"
    EXPANSION = "expansion"
    HOVER = "hover"
    CORTEX = "cortex"
    WORKFLOW = "workflow"


@dataclass
class PluginInfo:
    """Plugin information and metadata."""
    name: str
    version: str
    description: str
    author: str
    plugin_type: PluginType
    config_template: Dict[str, Any]
    requirements: List[str]
    enabled: bool = False
    module_path: Optional[str] = None


class BasePlugin(ABC):
    """Base class for all MISP plugins."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"plugin.{self.__class__.__name__}")

    @abstractmethod
    def get_info(self) -> PluginInfo:
        """Return plugin information."""
        pass

    @abstractmethod
    async def execute(self, data: Any, **kwargs) -> Any:
        """Execute plugin functionality."""
        pass

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate plugin configuration."""
        return True

    async def initialize(self) -> bool:
        """Initialize plugin resources."""
        return True

    async def cleanup(self) -> None:
        """Cleanup plugin resources."""
        pass


class EnrichmentPlugin(BasePlugin):
    """Base class for enrichment plugins."""

    @abstractmethod
    async def enrich(self, attribute: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich an attribute with external data."""
        pass

    async def execute(self, data: Any, **kwargs) -> Any:
        """Execute enrichment."""
        return await self.enrich(data)


class ExportPlugin(BasePlugin):
    """Base class for export plugins."""

    @abstractmethod
    async def export(self, event: Dict[str, Any]) -> bytes:
        """Export event data in specific format."""
        pass

    async def execute(self, data: Any, **kwargs) -> Any:
        """Execute export."""
        return await self.export(data)


class ImportPlugin(BasePlugin):
    """Base class for import plugins."""

    @abstractmethod
    async def import_data(self, data: bytes) -> Dict[str, Any]:
        """Import data from external format."""
        pass

    async def execute(self, data: Any, **kwargs) -> Any:
        """Execute import."""
        return await self.import_data(data)


class ActionPlugin(BasePlugin):
    """Base class for action plugins."""

    @abstractmethod
    async def perform_action(self, event: Dict[str, Any]) -> bool:
        """Perform action on event."""
        pass

    async def execute(self, data: Any, **kwargs) -> Any:
        """Execute action."""
        return await self.perform_action(data)


class PluginRegistry:
    """
    Plugin registry preserving MISP's plugin management patterns:
    - Dynamic plugin loading
    - Plugin configuration management
    - Plugin lifecycle management
    - Operation catalog maintenance
    """

    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugin_info: Dict[str, PluginInfo] = {}
        self._plugin_configs: Dict[str, Dict[str, Any]] = {}
        self._operation_catalog: Dict[PluginType, List[str]] = {
            plugin_type: [] for plugin_type in PluginType
        }

    def register_plugin(
        self,
        plugin_class: Type[BasePlugin],
        config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Register a plugin class."""
        try:
            # Create plugin instance
            plugin_config = config or {}
            plugin = plugin_class(plugin_config)

            # Get plugin info
            info = plugin.get_info()

            # Validate configuration
            if not plugin.validate_config(plugin_config):
                logger.error(f"Invalid configuration for plugin {info.name}")
                return False

            # Store plugin and info
            self._plugins[info.name] = plugin
            self._plugin_info[info.name] = info
            self._plugin_configs[info.name] = plugin_config

            # Update operation catalog
            if info.plugin_type not in self._operation_catalog:
                self._operation_catalog[info.plugin_type] = []
            self._operation_catalog[info.plugin_type].append(info.name)

            logger.info(f"Registered plugin: {info.name} v{info.version}")
            return True

        except Exception as e:
            logger.error(f"Failed to register plugin: {str(e)}", exc_info=True)
            return False

    async def load_plugin_from_module(
        self,
        module_path: str,
        config: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Dynamically load plugin from module path."""
        try:
            # Import module
            module = importlib.import_module(module_path)

            # Find plugin class
            plugin_class = None
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and
                    issubclass(attr, BasePlugin) and
                        attr != BasePlugin):
                    plugin_class = attr
                    break

            if not plugin_class:
                logger.error(f"No plugin class found in module {module_path}")
                return False

            # Register plugin
            return self.register_plugin(plugin_class, config)

        except Exception as e:
            logger.error(
                f"Failed to load plugin from {module_path}: {str(e)}",
                exc_info=True
            )
            return False

    async def initialize_plugin(self, plugin_name: str) -> bool:
        """Initialize a specific plugin."""
        if plugin_name not in self._plugins:
            logger.error(f"Plugin not found: {plugin_name}")
            return False

        try:
            plugin = self._plugins[plugin_name]
            success = await plugin.initialize()

            if success:
                self._plugin_info[plugin_name].enabled = True
                logger.info(f"Initialized plugin: {plugin_name}")
            else:
                logger.error(f"Failed to initialize plugin: {plugin_name}")

            return success

        except Exception as e:
            logger.error(
                f"Error initializing plugin {plugin_name}: {str(e)}",
                exc_info=True
            )
            return False

    async def initialize_all_plugins(self) -> None:
        """Initialize all registered plugins."""
        for plugin_name in self._plugins.keys():
            await self.initialize_plugin(plugin_name)

    async def execute_plugin(
        self,
        plugin_name: str,
        data: Any,
        **kwargs
    ) -> Any:
        """Execute a specific plugin."""
        if plugin_name not in self._plugins:
            raise ValueError(f"Plugin not found: {plugin_name}")

        info = self._plugin_info[plugin_name]
        if not info.enabled:
            raise ValueError(f"Plugin not enabled: {plugin_name}")

        plugin = self._plugins[plugin_name]
        return await plugin.execute(data, **kwargs)

    async def execute_plugins_by_type(
        self,
        plugin_type: PluginType,
        data: Any,
        **kwargs
    ) -> List[Any]:
        """Execute all enabled plugins of a specific type."""
        results = []

        for plugin_name in self._operation_catalog.get(plugin_type, []):
            if self._plugin_info[plugin_name].enabled:
                try:
                    result = await self.execute_plugin(plugin_name, data, **kwargs)
                    results.append(result)
                except Exception as e:
                    logger.error(
                        f"Error executing plugin {plugin_name}: {str(e)}",
                        exc_info=True
                    )

        return results

    def get_plugin_info(self, plugin_name: str) -> Optional[PluginInfo]:
        """Get information about a specific plugin."""
        return self._plugin_info.get(plugin_name)

    def list_plugins(
        self,
        plugin_type: Optional[PluginType] = None,
        enabled_only: bool = False
    ) -> List[PluginInfo]:
        """List all plugins, optionally filtered by type and status."""
        plugins = []

        for info in self._plugin_info.values():
            if plugin_type and info.plugin_type != plugin_type:
                continue
            if enabled_only and not info.enabled:
                continue
            plugins.append(info)

        return plugins

    def get_operation_catalog(self) -> Dict[PluginType, List[str]]:
        """Get the complete operation catalog."""
        return self._operation_catalog.copy()

    async def update_plugin_config(
        self,
        plugin_name: str,
        config: Dict[str, Any]
    ) -> bool:
        """Update plugin configuration."""
        if plugin_name not in self._plugins:
            return False

        plugin = self._plugins[plugin_name]

        if not plugin.validate_config(config):
            return False

        self._plugin_configs[plugin_name] = config
        plugin.config = config

        # Reinitialize plugin with new config
        await plugin.cleanup()
        return await self.initialize_plugin(plugin_name)

    async def cleanup_all_plugins(self) -> None:
        """Cleanup all plugins."""
        for plugin in self._plugins.values():
            try:
                await plugin.cleanup()
            except Exception as e:
                logger.error(f"Error during plugin cleanup: {str(e)}")


# Global plugin registry instance
plugin_registry = PluginRegistry()
