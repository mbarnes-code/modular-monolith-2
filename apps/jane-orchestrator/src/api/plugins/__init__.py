"""Plugin system initialization."""

from .endpoint_registry import (EndpointRegistry, ExtensibleAPI, endpoint,
                                get_endpoint_registry,
                                initialize_endpoint_registry)
from .interceptors import (BaseInterceptor, ErrorInterceptor, InterceptorType,
                           RequestInterceptor, ResponseInterceptor,
                           interceptor_chain)
from .operation_catalog import (OperationMetadata, OperationType,
                                operation_catalog)
from .plugin_manager import PluginManager
from .plugin_registry import BasePlugin, PluginType, plugin_registry

__all__ = [
    # Plugin Registry
    "plugin_registry",
    "BasePlugin",
    "PluginType",

    # Endpoint Registry
    "EndpointRegistry",
    "endpoint",
    "ExtensibleAPI",
    "initialize_endpoint_registry",
    "get_endpoint_registry",

    # Operation Catalog
    "operation_catalog",
    "OperationType",
    "OperationMetadata",

    # Interceptors
    "interceptor_chain",
    "BaseInterceptor",
    "RequestInterceptor",
    "ResponseInterceptor",
    "ErrorInterceptor",
    "InterceptorType",

    # Plugin Manager
    "PluginManager"
]
