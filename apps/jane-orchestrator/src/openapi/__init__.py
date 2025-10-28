"""
OpenAPI Package

Enhanced OpenAPI documentation generation with executive function 
accommodations and 37-tool integration documentation.
"""

from .generator import (ExecutiveFunctionTag, ToolIntegrationInfo,
                        generate_mental_prosthetic_openapi_schema,
                        save_openapi_spec, setup_openapi_docs)

__all__ = [
    'generate_mental_prosthetic_openapi_schema',
    'save_openapi_spec',
    'setup_openapi_docs',
    'ExecutiveFunctionTag',
    'ToolIntegrationInfo'
]
