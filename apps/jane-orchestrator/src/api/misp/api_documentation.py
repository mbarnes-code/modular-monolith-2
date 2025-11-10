"""
MISP API Documentation Generator

Preserves OpenAPI/Swagger specs, API versioning, and developer documentation
from original MISP CakePHP implementation to FastAPI integration.

Generates comprehensive API documentation maintaining compatibility with
original MISP REST API specifications.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from fastapi import FastAPI
from pydantic import BaseModel, Field


# OpenAPI specification models
class MISPAPIVersion(BaseModel):
    """MISP API Version information"""
    version: str = Field(..., description="API version number")
    misp_version: str = Field(..., description="MISP platform version")
    pymisp_version: str = Field(..., description="PyMISP library version")
    compatibility: str = Field(..., description="API compatibility level")


class MISPEndpointDoc(BaseModel):
    """MISP API endpoint documentation structure"""
    endpoint: str = Field(..., description="API endpoint path")
    method: str = Field(..., description="HTTP method")
    summary: str = Field(..., description="Brief endpoint description")
    description: str = Field(..., description="Detailed endpoint description")
    parameters: Dict[str, Any] = Field(
        default_factory=dict,
        description="URL and query parameters"
    )
    request_body: Optional[Dict[str, Any]] = Field(
        None,
        description="Request body schema"
    )
    responses: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Response schemas by status code"
    )
    examples: Dict[str, Any] = Field(
        default_factory=dict,
        description="Request/response examples"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="OpenAPI tags for grouping"
    )


class MISPAPIDocGenerator:
    """
    Generates comprehensive API documentation for MISP integration

    Preserves original CakePHP API documentation while generating
    modern OpenAPI/Swagger specifications for FastAPI implementation.
    """

    def __init__(self, app: FastAPI):
        self.app = app
        self.base_path = "/api/v1"
        self.misp_version = "2.5.22"
        self.api_version = "1.0.0"
        self.pymisp_version = "2.5.17.1"

        # Load original MISP API documentation
        self.original_docs = self._load_original_api_docs()

        # Define MISP-specific OpenAPI components
        self.openapi_components = self._define_openapi_components()

    def _load_original_api_docs(self) -> Dict[str, Any]:
        """Load original MISP API documentation structure"""
        return {
            "attributes": {
                "add": {
                    "method": "POST",
                    "path": "/attributes/add/{event_id}",
                    "summary": "Add MISP Attribute",
                    "description": ("POST a MISP Attribute JSON to this API "
                                    "to create an Attribute."),
                    "url_params": {
                        "event_id": {
                            "type": "integer",
                            "description": "Event ID to add attribute to"
                        }
                    },
                    "body_params": {
                        "mandatory": {
                            "value": {
                                "type": "string",
                                "description": "Attribute value"
                            },
                            "type": {
                                "type": "string",
                                "description": "The type of the attribute"
                            }
                        },
                        "optional": {
                            "category": {"type": "string"},
                            "to_ids": {
                                "type": "integer",
                                "description": "State of the to_ids flag"
                            },
                            "uuid": {"type": "string"},
                            "distribution": {"type": "integer"},
                            "sharing_group_id": {"type": "integer"},
                            "timestamp": {"type": "integer"},
                            "comment": {"type": "string"},
                            "data": {
                                "type": "string",
                                "description": "Base64 encoded file contents"
                            },
                            "encrypt": {"type": "integer"},
                            "first_seen": {
                                "type": "string",
                                "format": "date-time"
                            },
                            "last_seen": {
                                "type": "string",
                                "format": "date-time"
                            }
                        }
                    }
                },
                "edit": {
                    "method": "POST",
                    "path": "/attributes/edit/{attribute_id}",
                    "summary": "Edit MISP Attribute",
                    "description": ("POST a MISP Attribute JSON to update. "
                                    "Timestamp must be newer if set."),
                    "url_params": {
                        "attribute_id": {
                            "type": "integer",
                            "description": "Attribute ID to edit"
                        }
                    }
                },
                "restSearch": {
                    "method": "POST",
                    "path": "/attributes/restSearch",
                    "summary": "Search MISP Attributes",
                    "description": ("Search MISP using filter parameters. "
                                    "Supports pagination via page and limit."),
                    "body_params": {
                        "mandatory": {
                            "returnFormat": {
                                "type": "string",
                                "enum": ["json", "xml", "csv", "stix", "stix2"]
                            }
                        }
                    }
                }
            },
            "events": {
                "add": {
                    "method": "POST",
                    "path": "/events/add",
                    "summary": "Add MISP Event",
                    "description": "Create new MISP event"
                },
                "edit": {
                    "method": "POST",
                    "path": "/events/edit/{event_id}",
                    "summary": "Edit MISP Event",
                    "description": "Update existing MISP event"
                },
                "restSearch": {
                    "method": "POST",
                    "path": "/events/restSearch",
                    "summary": "Search MISP Events",
                    "description": "Search events with filter parameters"
                }
            },
            "organisations": {
                "index": {
                    "method": "GET",
                    "path": "/organisations",
                    "summary": "List Organizations",
                    "description": "Get list of MISP organizations"
                }
            },
            "tags": {
                "index": {
                    "method": "GET",
                    "path": "/tags",
                    "summary": "List Tags",
                    "description": "Get list of MISP tags"
                }
            },
            "galaxies": {
                "index": {
                    "method": "GET",
                    "path": "/galaxies",
                    "summary": "List Galaxies",
                    "description": "Get list of MISP galaxies"
                }
            }
        }

    def _define_openapi_components(self) -> Dict[str, Any]:
        """Define OpenAPI components for MISP data structures"""
        return {
            "schemas": {
                "MISPAttribute": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "event_id": {"type": "integer"},
                        "object_id": {"type": "integer"},
                        "object_relation": {"type": "string"},
                        "category": {"type": "string"},
                        "type": {"type": "string"},
                        "value": {"type": "string"},
                        "to_ids": {"type": "boolean"},
                        "uuid": {"type": "string", "format": "uuid"},
                        "timestamp": {"type": "integer"},
                        "distribution": {"type": "integer"},
                        "sharing_group_id": {"type": "integer"},
                        "comment": {"type": "string"},
                        "deleted": {"type": "boolean"},
                        "disable_correlation": {"type": "boolean"},
                        "first_seen": {"type": "string", "format": "date-time"},
                        "last_seen": {"type": "string", "format": "date-time"}
                    },
                    "required": ["type", "value"]
                },
                "MISPEvent": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "orgc_id": {"type": "integer"},
                        "org_id": {"type": "integer"},
                        "date": {"type": "string", "format": "date"},
                        "threat_level_id": {"type": "integer"},
                        "info": {"type": "string"},
                        "published": {"type": "boolean"},
                        "uuid": {"type": "string", "format": "uuid"},
                        "attribute_count": {"type": "integer"},
                        "analysis": {"type": "integer"},
                        "timestamp": {"type": "integer"},
                        "distribution": {"type": "integer"},
                        "sharing_group_id": {"type": "integer"},
                        "proposal_email_lock": {"type": "boolean"},
                        "locked": {"type": "boolean"},
                        "publish_timestamp": {"type": "integer"},
                        "sighting_timestamp": {"type": "integer"},
                        "disable_correlation": {"type": "boolean"},
                        "extends_uuid": {"type": "string"}
                    },
                    "required": ["info", "distribution"]
                },
                "MISPOrganisation": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "date_created": {"type": "string", "format": "date-time"},
                        "date_modified": {"type": "string", "format": "date-time"},
                        "description": {"type": "string"},
                        "type": {"type": "string"},
                        "nationality": {"type": "string"},
                        "sector": {"type": "string"},
                        "created_by": {"type": "integer"},
                        "uuid": {"type": "string", "format": "uuid"},
                        "contacts": {"type": "string"},
                        "local": {"type": "boolean"},
                        "restricted_to_domain": {"type": "array"}
                    },
                    "required": ["name"]
                }
            },
            "responses": {
                "MISPStandardResponse": {
                    "description": "Standard MISP API Response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "response": {"type": "array"},
                                    "message": {"type": "string"},
                                    "name": {"type": "string"},
                                    "url": {"type": "string"},
                                    "errors": {"type": "array"}
                                }
                            }
                        }
                    }
                },
                "ValidationError": {
                    "description": "Validation Error Response",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "message": {"type": "string"},
                                    "url": {"type": "string"},
                                    "errors": {"type": "array"}
                                }
                            }
                        }
                    }
                }
            },
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization"
                },
                "AuthKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-MISP-AuthKey"
                }
            }
        }

    def generate_openapi_spec(self) -> Dict[str, Any]:
        """Generate complete OpenAPI specification for MISP API"""

        # Base OpenAPI structure
        openapi_spec = {
            "openapi": "3.0.3",
            "info": {
                "title": "MISP Threat Intelligence Platform API",
                "description": (
                    "REST API for MISP (Malware Information Sharing Platform) "
                    "threat intelligence sharing platform. This API provides "
                    "access to events, attributes, organizations, tags, and "
                    "other threat intelligence data."
                ),
                "version": self.api_version,
                "contact": {
                    "name": "MISP Project",
                    "url": "https://www.misp-project.org",
                    "email": "info@misp-project.org"
                },
                "license": {
                    "name": "AGPL-3.0",
                    "url": "https://www.gnu.org/licenses/agpl-3.0.html"
                },
                "x-misp-version": self.misp_version,
                "x-pymisp-version": self.pymisp_version
            },
            "servers": [
                {
                    "url": f"{self.base_path}",
                    "description": "MISP API Server"
                }
            ],
            "components": self.openapi_components,
            "paths": {},
            "tags": [
                {
                    "name": "attributes",
                    "description": "MISP Attribute operations"
                },
                {
                    "name": "events",
                    "description": "MISP Event operations"
                },
                {
                    "name": "organisations",
                    "description": "Organization management"
                },
                {
                    "name": "tags",
                    "description": "Tag management"
                },
                {
                    "name": "galaxies",
                    "description": "Galaxy and cluster operations"
                },
                {
                    "name": "admin",
                    "description": "Administrative operations"
                }
            ]
        }

        # Generate paths from original documentation
        for resource, endpoints in self.original_docs.items():
            for endpoint_name, endpoint_info in endpoints.items():
                path = endpoint_info["path"]
                method = endpoint_info["method"].lower()

                if path not in openapi_spec["paths"]:
                    openapi_spec["paths"][path] = {}

                openapi_spec["paths"][path][method] = {
                    "tags": [resource],
                    "summary": endpoint_info["summary"],
                    "description": endpoint_info["description"],
                    "operationId": f"{method}_{resource}_{endpoint_name}",
                    "security": [
                        {"ApiKeyAuth": []},
                        {"AuthKeyAuth": []}
                    ],
                    "responses": {
                        "200": {
                            "$ref": "#/components/responses/MISPStandardResponse"
                        },
                        "400": {
                            "$ref": "#/components/responses/ValidationError"
                        },
                        "401": {
                            "description": "Unauthorized - Invalid API key"
                        },
                        "403": {
                            "description": "Forbidden - Insufficient permissions"
                        },
                        "404": {
                            "description": "Not Found"
                        },
                        "500": {
                            "description": "Internal Server Error"
                        }
                    }
                }

                # Add parameters if they exist
                if "url_params" in endpoint_info:
                    parameters = []
                    for param_name, param_info in endpoint_info["url_params"].items():
                        parameters.append({
                            "name": param_name,
                            "in": "path",
                            "required": True,
                            "schema": {"type": param_info["type"]},
                            "description": param_info.get("description", "")
                        })
                    openapi_spec["paths"][path][method]["parameters"] = parameters

                # Add request body for POST/PUT methods
                if method in ["post", "put"] and "body_params" in endpoint_info:
                    request_schema = {"type": "object", "properties": {}}
                    required_fields = []

                    if "mandatory" in endpoint_info["body_params"]:
                        for param, info in endpoint_info["body_params"]["mandatory"].items():
                            request_schema["properties"][param] = info
                            required_fields.append(param)

                    if "optional" in endpoint_info["body_params"]:
                        for param, info in endpoint_info["body_params"]["optional"].items():
                            request_schema["properties"][param] = info

                    if required_fields:
                        request_schema["required"] = required_fields

                    openapi_spec["paths"][path][method]["requestBody"] = {
                        "required": bool(required_fields),
                        "content": {
                            "application/json": {
                                "schema": request_schema
                            }
                        }
                    }

        return openapi_spec

    def save_openapi_spec(self, output_path: str = None) -> None:
        """Save OpenAPI specification to file"""
        if output_path is None:
            output_path = "/workspaces/modular-monolith-2/apps/jane-orchestrator/src/api/misp/openapi.yaml"

        spec = self.generate_openapi_spec()

        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # Save as YAML
        with open(output_path, 'w') as f:
            yaml.dump(spec, f, default_flow_style=False, sort_keys=False)

        # Also save as JSON
        json_path = output_path.replace('.yaml', '.json')
        with open(json_path, 'w') as f:
            json.dump(spec, f, indent=2)

    def generate_api_documentation_markdown(self) -> str:
        """Generate comprehensive API documentation in Markdown format"""

        doc_content = f"""# MISP API Documentation

**Version**: {self.api_version}  
**MISP Version**: {self.misp_version}  
**PyMISP Version**: {self.pymisp_version}  
**Generated**: {datetime.utcnow().isoformat()}

## Overview

This API provides access to the MISP (Malware Information Sharing Platform) 
threat intelligence data and functionality. The API maintains compatibility 
with the original MISP REST API while providing modern OpenAPI/Swagger 
specifications.

## Authentication

The API supports two authentication methods:

1. **Authorization Header**: `Authorization: Bearer <api-key>`
2. **X-MISP-AuthKey Header**: `X-MISP-AuthKey: <api-key>`

## Response Formats

The API supports multiple response formats:

- **JSON** (default): `Accept: application/json`
- **XML**: `Accept: application/xml` or append `.xml` to endpoint
- **CSV**: `Accept: text/csv` or append `.csv` to endpoint

## API Endpoints

"""

        # Generate documentation for each endpoint
        for resource, endpoints in self.original_docs.items():
            doc_content += f"\n### {resource.title()}\n\n"

            for endpoint_name, endpoint_info in endpoints.items():
                doc_content += f"#### {endpoint_info['summary']}\n\n"
                doc_content += f"**Method**: `{endpoint_info['method']}`  \n"
                doc_content += f"**Path**: `{endpoint_info['path']}`\n\n"
                doc_content += f"{endpoint_info['description']}\n\n"

                # URL Parameters
                if "url_params" in endpoint_info:
                    doc_content += "**URL Parameters**:\n\n"
                    doc_content += "| Parameter | Type | Description |\n"
                    doc_content += "|-----------|------|-------------|\n"
                    for param, info in endpoint_info["url_params"].items():
                        desc = info.get("description", "")
                        doc_content += f"| {param} | {info['type']} | {desc} |\n"
                    doc_content += "\n"

                # Body Parameters
                if "body_params" in endpoint_info:
                    if "mandatory" in endpoint_info["body_params"]:
                        doc_content += "**Required Parameters**:\n\n"
                        doc_content += "| Parameter | Type | Description |\n"
                        doc_content += "|-----------|------|-------------|\n"
                        for param, info in endpoint_info["body_params"]["mandatory"].items():
                            desc = info.get("description", "")
                            doc_content += f"| {param} | {info['type']} | {desc} |\n"
                        doc_content += "\n"

                    if "optional" in endpoint_info["body_params"]:
                        doc_content += "**Optional Parameters**:\n\n"
                        doc_content += "| Parameter | Type | Description |\n"
                        doc_content += "|-----------|------|-------------|\n"
                        for param, info in endpoint_info["body_params"]["optional"].items():
                            desc = info.get("description", "")
                            doc_content += f"| {param} | {info['type']} | {desc} |\n"
                        doc_content += "\n"

                doc_content += "---\n\n"

        return doc_content

    def save_api_documentation(self, output_path: str = None) -> None:
        """Save API documentation to Markdown file"""
        if output_path is None:
            output_path = "/workspaces/modular-monolith-2/apps/jane-orchestrator/src/api/misp/API_Documentation.md"

        doc_content = self.generate_api_documentation_markdown()

        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(doc_content)

    def setup_fastapi_docs(self) -> None:
        """Configure FastAPI app with custom OpenAPI specification"""

        def custom_openapi():
            if self.app.openapi_schema:
                return self.app.openapi_schema

            openapi_schema = self.generate_openapi_spec()
            self.app.openapi_schema = openapi_schema
            return self.app.openapi_schema

        self.app.openapi = custom_openapi


def setup_misp_api_documentation(app: FastAPI) -> MISPAPIDocGenerator:
    """
    Setup MISP API documentation for FastAPI application

    Args:
        app: FastAPI application instance

    Returns:
        Configured API documentation generator
    """
    doc_generator = MISPAPIDocGenerator(app)
    doc_generator.setup_fastapi_docs()

    # Generate and save documentation files
    doc_generator.save_openapi_spec()
    doc_generator.save_api_documentation()

    return doc_generator
