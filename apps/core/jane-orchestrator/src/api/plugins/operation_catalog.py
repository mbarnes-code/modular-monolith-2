"""Operation catalog preserving MISP's operation registry patterns."""

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class OperationType(Enum):
    """Types of operations in the catalog."""
    API_ENDPOINT = "api_endpoint"
    PLUGIN_OPERATION = "plugin_operation"
    ENRICHMENT = "enrichment"
    EXPORT = "export"
    IMPORT = "import"
    ACTION = "action"
    WORKFLOW = "workflow"
    CORRELATION = "correlation"
    EXPANSION = "expansion"
    HOVER = "hover"


@dataclass
class OperationMetadata:
    """Metadata for operations in the catalog."""
    name: str
    operation_type: OperationType
    version: str
    description: str
    author: str
    module_path: Optional[str] = None
    plugin_name: Optional[str] = None
    config_template: Dict[str, Any] = field(default_factory=dict)
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Dict[str, Any] = field(default_factory=dict)
    supported_attributes: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)
    enabled: bool = True
    rate_limited: bool = False
    auth_required: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)


@dataclass
class OperationStats:
    """Statistics for operation usage."""
    operation_name: str
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    avg_response_time: float = 0.0
    last_called: Optional[datetime] = None
    error_rate: float = 0.0


class OperationCatalog:
    """
    Operation catalog preserving MISP's operation registry patterns:
    - Dynamic operation discovery
    - Operation metadata management
    - Usage statistics tracking
    - Plugin operation registration
    """

    def __init__(self):
        self._operations: Dict[str, OperationMetadata] = {}
        self._stats: Dict[str, OperationStats] = {}
        self._type_index: Dict[OperationType, Set[str]] = {
            op_type: set() for op_type in OperationType
        }
        self._plugin_index: Dict[str, Set[str]] = {}
        self._attribute_index: Dict[str, Set[str]] = {}

    def register_operation(self, metadata: OperationMetadata) -> bool:
        """Register an operation in the catalog."""
        try:
            operation_key = self._generate_operation_key(
                metadata.name,
                metadata.plugin_name
            )

            if operation_key in self._operations:
                logger.warning(
                    f"Operation already registered: {operation_key}")
                return False

            # Store operation metadata
            self._operations[operation_key] = metadata

            # Initialize stats
            self._stats[operation_key] = OperationStats(
                operation_name=operation_key
            )

            # Update indexes
            self._update_indexes(operation_key, metadata)

            logger.info(
                f"Registered operation: {operation_key} "
                f"(type: {metadata.operation_type.value})"
            )

            return True

        except Exception as e:
            logger.error(
                f"Failed to register operation {metadata.name}: {str(e)}",
                exc_info=True
            )
            return False

    def _generate_operation_key(
        self,
        name: str,
        plugin_name: Optional[str] = None
    ) -> str:
        """Generate unique key for operation."""
        if plugin_name:
            return f"{plugin_name}.{name}"
        return name

    def _update_indexes(self, operation_key: str, metadata: OperationMetadata) -> None:
        """Update all indexes with new operation."""
        # Update type index
        self._type_index[metadata.operation_type].add(operation_key)

        # Update plugin index
        if metadata.plugin_name:
            if metadata.plugin_name not in self._plugin_index:
                self._plugin_index[metadata.plugin_name] = set()
            self._plugin_index[metadata.plugin_name].add(operation_key)

        # Update attribute index
        for attr_type in metadata.supported_attributes:
            if attr_type not in self._attribute_index:
                self._attribute_index[attr_type] = set()
            self._attribute_index[attr_type].add(operation_key)

    def unregister_operation(self, operation_key: str) -> bool:
        """Unregister an operation from the catalog."""
        if operation_key not in self._operations:
            return False

        metadata = self._operations[operation_key]

        # Remove from indexes
        self._type_index[metadata.operation_type].discard(operation_key)

        if metadata.plugin_name and metadata.plugin_name in self._plugin_index:
            self._plugin_index[metadata.plugin_name].discard(operation_key)

        for attr_type in metadata.supported_attributes:
            if attr_type in self._attribute_index:
                self._attribute_index[attr_type].discard(operation_key)

        # Remove from main storage
        del self._operations[operation_key]
        if operation_key in self._stats:
            del self._stats[operation_key]

        logger.info(f"Unregistered operation: {operation_key}")
        return True

    def get_operation(self, operation_key: str) -> Optional[OperationMetadata]:
        """Get operation metadata by key."""
        return self._operations.get(operation_key)

    def list_operations(
        self,
        operation_type: Optional[OperationType] = None,
        plugin_name: Optional[str] = None,
        attribute_type: Optional[str] = None,
        enabled_only: bool = False
    ) -> List[OperationMetadata]:
        """List operations with optional filtering."""
        operations = []

        # Start with all operations or filter by type
        if operation_type:
            candidate_keys = self._type_index.get(operation_type, set())
        else:
            candidate_keys = set(self._operations.keys())

        # Filter by plugin name
        if plugin_name and plugin_name in self._plugin_index:
            candidate_keys &= self._plugin_index[plugin_name]

        # Filter by attribute type
        if attribute_type and attribute_type in self._attribute_index:
            candidate_keys &= self._attribute_index[attribute_type]

        # Apply additional filters
        for key in candidate_keys:
            metadata = self._operations[key]

            if enabled_only and not metadata.enabled:
                continue

            operations.append(metadata)

        return operations

    def find_operations_for_attribute(self, attribute_type: str) -> List[OperationMetadata]:
        """Find all operations that support a specific attribute type."""
        return self.list_operations(attribute_type=attribute_type, enabled_only=True)

    def get_plugin_operations(self, plugin_name: str) -> List[OperationMetadata]:
        """Get all operations for a specific plugin."""
        return self.list_operations(plugin_name=plugin_name)

    def update_operation_stats(
        self,
        operation_key: str,
        success: bool,
        response_time: float
    ) -> None:
        """Update operation usage statistics."""
        if operation_key not in self._stats:
            return

        stats = self._stats[operation_key]
        stats.total_calls += 1
        stats.last_called = datetime.now()

        if success:
            stats.successful_calls += 1
        else:
            stats.failed_calls += 1

        # Update average response time
        if stats.total_calls == 1:
            stats.avg_response_time = response_time
        else:
            stats.avg_response_time = (
                (stats.avg_response_time * (stats.total_calls - 1) + response_time) /
                stats.total_calls
            )

        # Update error rate
        stats.error_rate = stats.failed_calls / stats.total_calls

    def get_operation_stats(self, operation_key: str) -> Optional[OperationStats]:
        """Get usage statistics for an operation."""
        return self._stats.get(operation_key)

    def get_catalog_summary(self) -> Dict[str, Any]:
        """Get summary of the entire operation catalog."""
        summary = {
            "total_operations": len(self._operations),
            "enabled_operations": len([
                op for op in self._operations.values() if op.enabled
            ]),
            "operations_by_type": {
                op_type.value: len(operations)
                for op_type, operations in self._type_index.items()
            },
            "operations_by_plugin": {
                plugin: len(operations)
                for plugin, operations in self._plugin_index.items()
            },
            "supported_attributes": list(self._attribute_index.keys()),
            "last_updated": datetime.now().isoformat()
        }

        return summary

    def export_catalog(self, include_stats: bool = False) -> Dict[str, Any]:
        """Export the entire catalog to a dictionary."""
        catalog_data = {
            "operations": {},
            "metadata": self.get_catalog_summary()
        }

        for key, metadata in self._operations.items():
            operation_data = {
                "name": metadata.name,
                "operation_type": metadata.operation_type.value,
                "version": metadata.version,
                "description": metadata.description,
                "author": metadata.author,
                "module_path": metadata.module_path,
                "plugin_name": metadata.plugin_name,
                "config_template": metadata.config_template,
                "input_schema": metadata.input_schema,
                "output_schema": metadata.output_schema,
                "supported_attributes": metadata.supported_attributes,
                "requirements": metadata.requirements,
                "enabled": metadata.enabled,
                "rate_limited": metadata.rate_limited,
                "auth_required": metadata.auth_required,
                "created_at": metadata.created_at.isoformat(),
                "last_modified": metadata.last_modified.isoformat()
            }

            if include_stats and key in self._stats:
                stats = self._stats[key]
                operation_data["stats"] = {
                    "total_calls": stats.total_calls,
                    "successful_calls": stats.successful_calls,
                    "failed_calls": stats.failed_calls,
                    "avg_response_time": stats.avg_response_time,
                    "error_rate": stats.error_rate,
                    "last_called": stats.last_called.isoformat() if stats.last_called else None
                }

            catalog_data["operations"][key] = operation_data

        return catalog_data

    def import_catalog(self, catalog_data: Dict[str, Any]) -> int:
        """Import catalog data from a dictionary."""
        imported_count = 0

        for key, data in catalog_data.get("operations", {}).items():
            try:
                metadata = OperationMetadata(
                    name=data["name"],
                    operation_type=OperationType(data["operation_type"]),
                    version=data["version"],
                    description=data["description"],
                    author=data["author"],
                    module_path=data.get("module_path"),
                    plugin_name=data.get("plugin_name"),
                    config_template=data.get("config_template", {}),
                    input_schema=data.get("input_schema", {}),
                    output_schema=data.get("output_schema", {}),
                    supported_attributes=data.get("supported_attributes", []),
                    requirements=data.get("requirements", []),
                    enabled=data.get("enabled", True),
                    rate_limited=data.get("rate_limited", False),
                    auth_required=data.get("auth_required", True),
                    created_at=datetime.fromisoformat(data["created_at"]),
                    last_modified=datetime.fromisoformat(data["last_modified"])
                )

                if self.register_operation(metadata):
                    imported_count += 1

            except Exception as e:
                logger.error(f"Failed to import operation {key}: {str(e)}")

        logger.info(f"Imported {imported_count} operations to catalog")
        return imported_count


# Global operation catalog instance
operation_catalog = OperationCatalog()
