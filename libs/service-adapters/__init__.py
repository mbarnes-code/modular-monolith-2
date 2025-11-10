"""
Service Adapters Package

Base framework and adapters for integrating all 37 mental prosthetic tools
with executive function accommodations and business logic preservation.
"""

from .base_adapter import (AdaptationStrategy, AdapterRegistry,
                           AdapterResponse, BaseServiceAdapter,
                           ExecutiveFunctionContext, ExecutiveFunctionLevel,
                           ToolDomain, ToolMetadata, adapter_registry)

__all__ = [
    'BaseServiceAdapter',
    'AdapterRegistry',
    'AdapterResponse',
    'ToolMetadata',
    'ToolDomain',
    'AdaptationStrategy',
    'ExecutiveFunctionLevel',
    'ExecutiveFunctionContext',
    'adapter_registry'
]

# Package metadata
__version__ = '1.0.0'
__description__ = 'Service adapters for 37 mental prosthetic tools'

# Tool integration constants
TOTAL_TOOLS = 37
DOMAIN_TOOL_COUNTS = {
    'security': 13,
    'productivity': 8,
    'mtg': 4,
    'infrastructure': 12
}

# Performance targets by domain (milliseconds)
DOMAIN_PERFORMANCE_TARGETS = {
    ToolDomain.SECURITY: 1000,      # <1s for threat analysis criticality
    ToolDomain.PRODUCTIVITY: 2000,  # <2s for task management workflows
    ToolDomain.MTG: 3000,          # <3s for game analysis complexity
    ToolDomain.INFRASTRUCTURE: 5000  # <5s for system operations tolerance
}
