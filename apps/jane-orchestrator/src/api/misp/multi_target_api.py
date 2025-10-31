"""
MISP Multi-Target API Compatibility Layer

Maintains dual-mode APIs (web/node), platform-specific endpoints,
and cross-environment compatibility for MISP threat intelligence platform.

Preserves original CakePHP REST patterns while providing modern FastAPI
interface.
"""

import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import Depends, Request, Response
from fastapi.responses import JSONResponse, XMLResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class APICompatibilityConfig(BaseModel):
    """Configuration for API compatibility modes"""
    web_mode: bool = True
    node_mode: bool = True
    legacy_endpoints: bool = True
    xml_support: bool = True
    csv_support: bool = True
    json_default: bool = True


class MultiTargetAPIManager:
    """
    Manages multi-target API compatibility for MISP integration

    Supports:
    - Web API mode (traditional REST)
    - Node.js API mode (optimized for server-side)
    - Legacy CakePHP endpoint compatibility
    - Cross-format responses (JSON, XML, CSV)
    """

    def __init__(self, config: APICompatibilityConfig):
        self.config = config
        self.legacy_routes = self._build_legacy_route_map()
        self.format_handlers = self._build_format_handlers()

    def _build_legacy_route_map(self) -> Dict[str, str]:
        """Map legacy CakePHP routes to modern FastAPI endpoints"""
        return {
            # Events API
            "/events.json": "/api/v1/events",
            "/events.xml": "/api/v1/events",
            "/events/index": "/api/v1/events",
            "/events/view/{id}": "/api/v1/events/{id}",
            "/events/add": "/api/v1/events",
            "/events/edit/{id}": "/api/v1/events/{id}",
            "/events/delete/{id}": "/api/v1/events/{id}",

            # Attributes API
            "/attributes.json": "/api/v1/attributes",
            "/attributes.xml": "/api/v1/attributes",
            "/attributes/index": "/api/v1/attributes",
            "/attributes/view/{id}": "/api/v1/attributes/{id}",
            "/attributes/add": "/api/v1/attributes",
            "/attributes/edit/{id}": "/api/v1/attributes/{id}",
            "/attributes/delete/{id}": "/api/v1/attributes/{id}",

            # Organizations API
            "/organisations.json": "/api/v1/organisations",
            "/organisations/index": "/api/v1/organisations",
            "/organisations/view/{id}": "/api/v1/organisations/{id}",

            # Tags API
            "/tags.json": "/api/v1/tags",
            "/tags/index": "/api/v1/tags",
            "/tags/view/{id}": "/api/v1/tags/{id}",

            # Galaxies API
            "/galaxies.json": "/api/v1/galaxies",
            "/galaxies/index": "/api/v1/galaxies",
            "/galaxies/view/{id}": "/api/v1/galaxies/{id}",

            # Admin routes
            "/admin/users": "/api/v1/admin/users",
            "/admin/roles": "/api/v1/admin/roles",
            "/admin/logs": "/api/v1/admin/logs",
        }

    def _build_format_handlers(self) -> Dict[str, callable]:
        """Build response format handlers for different content types"""
        return {
            "application/json": self._format_json,
            "application/xml": self._format_xml,
            "text/xml": self._format_xml,
            "text/csv": self._format_csv,
            "application/csv": self._format_csv,
        }

    def detect_api_mode(self, request: Request) -> str:
        """
        Detect API access mode based on request characteristics

        Returns:
            - 'web': Browser-based access
            - 'node': Server-side Node.js access
            - 'legacy': Legacy CakePHP client
            - 'modern': Modern REST client
        """
        user_agent = request.headers.get("user-agent", "").lower()

        # Node.js detection
        if "node" in user_agent or "nodejs" in user_agent:
            return "node"

        # Legacy CakePHP client detection
        if ("misp-" in user_agent or ".xml" in request.url.path or
                ".json" in request.url.path):
            return "legacy"

        # Browser detection
        browsers = ["mozilla", "chrome", "safari", "firefox"]
        if any(browser in user_agent for browser in browsers):
            return "web"

        return "modern"

    def get_response_format(self, request: Request) -> str:
        """Determine appropriate response format based on request"""
        # Check URL extension first (.json, .xml, .csv)
        path = request.url.path.lower()
        if path.endswith('.json'):
            return "application/json"
        elif path.endswith('.xml'):
            return "application/xml"
        elif path.endswith('.csv'):
            return "text/csv"

        # Check Accept header
        accept = request.headers.get("accept", "")
        if "application/xml" in accept or "text/xml" in accept:
            return "application/xml"
        elif "text/csv" in accept or "application/csv" in accept:
            return "text/csv"

        # Default to JSON
        return "application/json"

    def _format_json(self, data: Any, request: Request) -> JSONResponse:
        """Format response as JSON with MISP-compatible structure"""
        api_mode = self.detect_api_mode(request)

        if api_mode == "legacy":
            # Legacy CakePHP format
            if isinstance(data, list):
                response_data = {"response": data}
            else:
                response_data = {"response": [data] if data else []}
        else:
            # Modern REST format
            response_data = {
                "data": data,
                "status": "success",
                "timestamp": datetime.utcnow().isoformat(),
                "api_version": "2.5",
                "format": "json"
            }

        return JSONResponse(content=response_data)

    def _format_xml(self, data: Any, request: Request) -> XMLResponse:
        """Format response as XML with MISP-compatible structure"""
        root = ET.Element("response")

        def dict_to_xml(parent, data_dict):
            if isinstance(data_dict, dict):
                for key, value in data_dict.items():
                    element = ET.SubElement(parent, str(key))
                    if isinstance(value, (dict, list)):
                        dict_to_xml(element, value)
                    else:
                        element.text = str(value) if value is not None else ""
            elif isinstance(data_dict, list):
                for item in data_dict:
                    item_element = ET.SubElement(parent, "item")
                    dict_to_xml(item_element, item)
            else:
                parent.text = str(data_dict) if data_dict is not None else ""

        dict_to_xml(root, data)

        xml_string = ET.tostring(root, encoding='unicode')
        return Response(content=xml_string, media_type="application/xml")

    def _format_csv(self, data: Any, request: Request) -> Response:
        """Format response as CSV for data export"""
        import csv
        import io

        if not isinstance(data, list):
            data = [data] if data else []

        if not data:
            return Response(content="", media_type="text/csv")

        output = io.StringIO()
        writer = csv.writer(output)

        # Write headers (keys from first item)
        if data and isinstance(data[0], dict):
            headers = list(data[0].keys())
            writer.writerow(headers)

            # Write data rows
            for item in data:
                row = [str(item.get(header, "")) for header in headers]
                writer.writerow(row)

        csv_content = output.getvalue()
        output.close()

        return Response(content=csv_content, media_type="text/csv")

    def create_compatible_response(
        self,
        data: Any,
        request: Request,
        status_code: int = 200
    ) -> Response:
        """
        Create API response compatible with multiple targets

        Args:
            data: Response data
            request: FastAPI request object
            status_code: HTTP status code

        Returns:
            Formatted response based on request requirements
        """
        response_format = self.get_response_format(request)
        api_mode = self.detect_api_mode(request)

        try:
            formatter = self.format_handlers.get(
                response_format, self._format_json)
            response = formatter(data, request)
            response.status_code = status_code

            # Add compatibility headers
            response.headers["X-API-Mode"] = api_mode
            response.headers["X-MISP-Version"] = "2.5.22"
            response.headers["X-Compatibility-Layer"] = "Jane-Orchestrator"

            # CORS headers for web mode
            if api_mode == "web":
                response.headers["Access-Control-Allow-Origin"] = "*"
                cors_methods = "GET, POST, PUT, DELETE, OPTIONS"
                response.headers["Access-Control-Allow-Methods"] = cors_methods
                cors_headers = "Content-Type, Authorization"
                response.headers["Access-Control-Allow-Headers"] = cors_headers

            return response

        except Exception as e:
            logger.error(f"Error creating compatible response: {e}")
            error_data = {
                "error": "Response formatting failed",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
            return JSONResponse(content=error_data, status_code=500)

    def handle_legacy_route(self, request: Request) -> Optional[str]:
        """
        Handle legacy CakePHP route mapping

        Args:
            request: Incoming request

        Returns:
            Modern route path if mapping exists, None otherwise
        """
        path = request.url.path

        # Strip file extensions for mapping
        clean_path = path
        for ext in ['.json', '.xml', '.csv']:
            if clean_path.endswith(ext):
                clean_path = clean_path[:-len(ext)]
                break

        # Check direct mapping
        if clean_path in self.legacy_routes:
            return self.legacy_routes[clean_path]

        # Check pattern-based mapping
        for pattern, target in self.legacy_routes.items():
            if '{id}' in pattern:
                # Extract ID from path
                pattern_parts = pattern.split('/')
                path_parts = clean_path.split('/')

                if len(pattern_parts) == len(path_parts):
                    match = True
                    extracted_id = None

                    for p_part, path_part in zip(pattern_parts, path_parts):
                        if p_part == '{id}':
                            extracted_id = path_part
                        elif p_part != path_part:
                            match = False
                            break

                    if match and extracted_id:
                        return target.replace('{id}', extracted_id)

        return None

    def create_platform_specific_endpoint(
        self,
        endpoint_name: str,
        web_handler: callable,
        node_handler: callable = None,
        legacy_handler: callable = None
    ):
        """
        Create platform-specific endpoint with different handlers

        Args:
            endpoint_name: Base endpoint name
            web_handler: Handler for web requests
            node_handler: Handler for Node.js requests (optional)
            legacy_handler: Handler for legacy requests (optional)
        """
        async def platform_router(request: Request):
            api_mode = self.detect_api_mode(request)

            if api_mode == "node" and node_handler:
                return await node_handler(request)
            elif api_mode == "legacy" and legacy_handler:
                return await legacy_handler(request)
            else:
                return await web_handler(request)

        return platform_router


# Global compatibility manager instance
compatibility_config = APICompatibilityConfig()
api_compatibility = MultiTargetAPIManager(compatibility_config)


def get_api_compatibility() -> MultiTargetAPIManager:
    """Dependency injection for API compatibility manager"""
    return api_compatibility


class PlatformSpecificResponse(BaseModel):
    """Platform-specific response wrapper"""
    data: Any
    platform: str
    format: str
    timestamp: datetime
    compatibility_headers: Dict[str, str] = {}


def create_misp_compatible_response(
    request: Request,
    data: Any,
    status_code: int = 200,
    compatibility_manager: MultiTargetAPIManager = Depends(
        get_api_compatibility
    )
) -> Response:
    """
    FastAPI dependency for creating MISP-compatible responses

    Usage:
        @app.get("/api/v1/events")
        async def get_events(
            request: Request,
            response: Response = Depends(create_misp_compatible_response)
        ):
            events_data = await get_events_data()
            return compatibility_manager.create_compatible_response(
                events_data, request
            )
    """
    return compatibility_manager.create_compatible_response(
        data, request, status_code
    )
