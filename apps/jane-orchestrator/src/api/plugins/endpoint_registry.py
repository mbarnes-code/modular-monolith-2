"""Dynamic endpoint discovery preserving MISP's extensible API patterns."""

import inspect
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type

from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.openapi.models import Tag
from fastapi.routing import APIRoute

logger = logging.getLogger(__name__)


class EndpointCategory(Enum):
    """Categories of dynamically registered endpoints."""
    MISP_CORE = "misp_core"
    PLUGIN = "plugin"
    EXTENSION = "extension"
    ENRICHMENT = "enrichment"
    EXPORT = "export"
    IMPORT = "import"
    ACTION = "action"
    WORKFLOW = "workflow"


@dataclass
class EndpointInfo:
    """Information about a dynamically registered endpoint."""
    path: str
    method: str
    category: EndpointCategory
    plugin_name: Optional[str]
    handler: Callable
    dependencies: List[str]
    description: str
    tags: List[str]
    auth_required: bool = True
    rate_limited: bool = False


class EndpointRegistry:
    """
    Registry for dynamically discovered and registered endpoints.
    Preserves MISP's extensible API architecture patterns.
    """

    def __init__(self, app: FastAPI):
        self.app = app
        self._endpoints: Dict[str, EndpointInfo] = {}
        self._routers: Dict[str, APIRouter] = {}
        self._categories: Dict[EndpointCategory, List[str]] = {
            category: [] for category in EndpointCategory
        }

    def register_endpoint(
        self,
        path: str,
        method: str,
        handler: Callable,
        category: EndpointCategory,
        plugin_name: Optional[str] = None,
        description: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None,
        auth_required: bool = True,
        rate_limited: bool = False,
        router_prefix: str = "/api"
    ) -> bool:
        """Register a dynamic endpoint."""
        try:
            endpoint_key = f"{method.upper()}:{router_prefix}{path}"

            if endpoint_key in self._endpoints:
                logger.warning(f"Endpoint already registered: {endpoint_key}")
                return False

            # Create endpoint info
            endpoint_info = EndpointInfo(
                path=path,
                method=method.upper(),
                category=category,
                plugin_name=plugin_name,
                handler=handler,
                dependencies=dependencies or [],
                description=description,
                tags=tags or [],
                auth_required=auth_required,
                rate_limited=rate_limited
            )

            # Get or create router for this category
            router_key = f"{category.value}_{plugin_name}" if plugin_name else category.value
            if router_key not in self._routers:
                self._routers[router_key] = APIRouter(
                    prefix=router_prefix,
                    tags=[category.value] + (tags or [])
                )

            router = self._routers[router_key]

            # Add endpoint to router
            self._add_endpoint_to_router(router, endpoint_info)

            # Store endpoint info
            self._endpoints[endpoint_key] = endpoint_info
            self._categories[category].append(endpoint_key)

            logger.info(
                f"Registered dynamic endpoint: {endpoint_key} "
                f"(category: {category.value}, plugin: {plugin_name})"
            )

            return True

        except Exception as e:
            logger.error(
                f"Failed to register endpoint {path}: {str(e)}", exc_info=True)
            return False

    def _add_endpoint_to_router(self, router: APIRouter, endpoint_info: EndpointInfo) -> None:
        """Add endpoint to FastAPI router with proper configuration."""
        method = endpoint_info.method.lower()
        path = endpoint_info.path
        handler = endpoint_info.handler

        # Create endpoint kwargs
        endpoint_kwargs = {
            "path": path,
            "response_model": None,  # Let FastAPI infer from handler
            "summary": endpoint_info.description,
            "tags": endpoint_info.tags,
            "dependencies": self._create_dependencies(endpoint_info)
        }

        # Add endpoint based on method
        if method == "get":
            router.get(**endpoint_kwargs)(handler)
        elif method == "post":
            router.post(**endpoint_kwargs)(handler)
        elif method == "put":
            router.put(**endpoint_kwargs)(handler)
        elif method == "patch":
            router.patch(**endpoint_kwargs)(handler)
        elif method == "delete":
            router.delete(**endpoint_kwargs)(handler)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

    def _create_dependencies(self, endpoint_info: EndpointInfo) -> List[Depends]:
        """Create FastAPI dependencies for endpoint."""
        dependencies = []

        # Add authentication dependency if required
        if endpoint_info.auth_required:
            dependencies.append(Depends(self._auth_dependency))

        # Add rate limiting dependency if required
        if endpoint_info.rate_limited:
            dependencies.append(Depends(self._rate_limit_dependency))

        return dependencies

    async def _auth_dependency(self, request: Request) -> Dict[str, Any]:
        """Authentication dependency."""
        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(
                status_code=401, detail="Authentication required")
        return user

    async def _rate_limit_dependency(self, request: Request) -> None:
        """Rate limiting dependency."""
        # Rate limiting is handled by middleware, this is just a marker
        pass

    def mount_routers(self) -> None:
        """Mount all registered routers to the main app."""
        for router_key, router in self._routers.items():
            if router not in [route.app for route in self.app.routes if hasattr(route, 'app')]:
                self.app.include_router(router)
                logger.info(f"Mounted router: {router_key}")

    def discover_endpoints_from_module(self, module_path: str, category: EndpointCategory) -> int:
        """Discover endpoints from a module using decorators."""
        try:
            import importlib
            module = importlib.import_module(module_path)

            registered_count = 0

            # Look for functions with endpoint metadata
            for name in dir(module):
                obj = getattr(module, name)
                if hasattr(obj, '__endpoint_info__'):
                    endpoint_info = obj.__endpoint_info__

                    success = self.register_endpoint(
                        path=endpoint_info.get('path', f'/{name}'),
                        method=endpoint_info.get('method', 'GET'),
                        handler=obj,
                        category=category,
                        plugin_name=endpoint_info.get('plugin_name'),
                        description=endpoint_info.get('description', ''),
                        tags=endpoint_info.get('tags', []),
                        dependencies=endpoint_info.get('dependencies', []),
                        auth_required=endpoint_info.get('auth_required', True),
                        rate_limited=endpoint_info.get('rate_limited', False)
                    )

                    if success:
                        registered_count += 1

            logger.info(
                f"Discovered {registered_count} endpoints from {module_path}")
            return registered_count

        except Exception as e:
            logger.error(
                f"Failed to discover endpoints from {module_path}: {str(e)}")
            return 0

    def get_endpoint_info(self, endpoint_key: str) -> Optional[EndpointInfo]:
        """Get information about a registered endpoint."""
        return self._endpoints.get(endpoint_key)

    def list_endpoints(
        self,
        category: Optional[EndpointCategory] = None,
        plugin_name: Optional[str] = None
    ) -> List[EndpointInfo]:
        """List registered endpoints with optional filtering."""
        endpoints = []

        for endpoint_info in self._endpoints.values():
            if category and endpoint_info.category != category:
                continue
            if plugin_name and endpoint_info.plugin_name != plugin_name:
                continue
            endpoints.append(endpoint_info)

        return endpoints

    def unregister_endpoint(self, endpoint_key: str) -> bool:
        """Unregister an endpoint."""
        if endpoint_key not in self._endpoints:
            return False

        endpoint_info = self._endpoints[endpoint_key]

        # Remove from category list
        if endpoint_key in self._categories[endpoint_info.category]:
            self._categories[endpoint_info.category].remove(endpoint_key)

        # Remove from endpoints registry
        del self._endpoints[endpoint_key]

        logger.info(f"Unregistered endpoint: {endpoint_key}")
        return True

    def get_operation_catalog(self) -> Dict[EndpointCategory, List[str]]:
        """Get the complete operation catalog."""
        return {
            category: [
                self._endpoints[endpoint_key].path
                for endpoint_key in endpoint_keys
            ]
            for category, endpoint_keys in self._categories.items()
        }


def endpoint(
    path: str,
    method: str = "GET",
    plugin_name: Optional[str] = None,
    description: str = "",
    tags: Optional[List[str]] = None,
    dependencies: Optional[List[str]] = None,
    auth_required: bool = True,
    rate_limited: bool = False
):
    """
    Decorator for marking functions as dynamic endpoints.
    Preserves MISP's plugin endpoint registration patterns.
    """
    def decorator(func: Callable) -> Callable:
        func.__endpoint_info__ = {
            'path': path,
            'method': method,
            'plugin_name': plugin_name,
            'description': description,
            'tags': tags or [],
            'dependencies': dependencies or [],
            'auth_required': auth_required,
            'rate_limited': rate_limited
        }
        return func

    return decorator


class ExtensibleAPI(ABC):
    """
    Base class for extensible API modules.
    Preserves MISP's extensible architecture patterns.
    """

    def __init__(self, endpoint_registry: EndpointRegistry):
        self.endpoint_registry = endpoint_registry
        self.logger = logging.getLogger(f"api.{self.__class__.__name__}")

    @abstractmethod
    def register_endpoints(self) -> int:
        """Register all endpoints for this API module."""
        pass

    @abstractmethod
    def get_category(self) -> EndpointCategory:
        """Get the category for endpoints in this module."""
        pass

    def get_plugin_name(self) -> Optional[str]:
        """Get the plugin name if this is a plugin API."""
        return None


# Example plugin API implementation
class MISPEnrichmentAPI(ExtensibleAPI):
    """Example extensible API for MISP enrichment plugins."""

    def get_category(self) -> EndpointCategory:
        return EndpointCategory.ENRICHMENT

    def register_endpoints(self) -> int:
        """Register enrichment endpoints."""
        registered = 0

        # Register enrichment query endpoint
        success = self.endpoint_registry.register_endpoint(
            path="/enrichment/query",
            method="POST",
            handler=self._query_enrichment,
            category=self.get_category(),
            description="Query enrichment modules",
            tags=["enrichment"],
            auth_required=True,
            rate_limited=True
        )
        if success:
            registered += 1

        # Register enrichment modules list endpoint
        success = self.endpoint_registry.register_endpoint(
            path="/enrichment/modules",
            method="GET",
            handler=self._list_modules,
            category=self.get_category(),
            description="List available enrichment modules",
            tags=["enrichment"],
            auth_required=True
        )
        if success:
            registered += 1

        return registered

    async def _query_enrichment(self, request: Request) -> Dict[str, Any]:
        """Handle enrichment query."""
        return {"message": "Enrichment query endpoint"}

    async def _list_modules(self, request: Request) -> Dict[str, Any]:
        """List enrichment modules."""
        return {"modules": []}


# Global endpoint registry instance
_endpoint_registry: Optional[EndpointRegistry] = None


def get_endpoint_registry() -> Optional[EndpointRegistry]:
    """Get the global endpoint registry instance."""
    return _endpoint_registry


def initialize_endpoint_registry(app: FastAPI) -> EndpointRegistry:
    """Initialize the global endpoint registry."""
    global _endpoint_registry
    _endpoint_registry = EndpointRegistry(app)
    return _endpoint_registry
