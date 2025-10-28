"""
Service Adapter Framework for Mental Prosthetic Platform

This module provides the base framework for integrating all 37 mental
prosthetic tools with unified interface, business logic preservation,
and executive function accommodations.

Key Features:
- Domain-specific performance targets (Security <1s, Productivity <2s, MTG <3s, Infrastructure <5s)
- ADHD/autism accommodations with <200ms UI responsiveness
- Business logic preservation across all original frameworks
- Rollback capabilities and version management
- Cross-tool data synchronization
"""

from .adapter import (AdaptationStrategy, AdapterRegistry, AdapterResponse,
                      BaseServiceAdapter, ExecutiveFunctionContext,
                      ExecutiveFunctionLevel, ToolDomain, ToolMetadata,
                      adapter_registry)
from .config import AdapterConfig, load_adapter_configs, validate_config
from .factory import (AdapterFactory, create_adapter_from_config,
                      register_all_adapters)
from .monitoring import (DomainMetrics, ExecutiveFunctionMetrics,
                         PerformanceMonitor, performance_monitor)
from .validation import (AdapterValidationResult,
                         validate_adapter_implementation,
                         validate_business_logic_preservation)

__all__ = [
    # Core adapter framework
    'BaseServiceAdapter',
    'AdapterRegistry',
    'AdapterResponse',
    'ToolMetadata',
    'ExecutiveFunctionContext',
    'ToolDomain',
    'AdaptationStrategy',
    'ExecutiveFunctionLevel',
    'adapter_registry',

    # Factory and creation
    'AdapterFactory',
    'create_adapter_from_config',
    'register_all_adapters',

    # Validation
    'validate_adapter_implementation',
    'validate_business_logic_preservation',
    'AdapterValidationResult',

    # Monitoring
    'PerformanceMonitor',
    'DomainMetrics',
    'ExecutiveFunctionMetrics',
    'performance_monitor',

    # Configuration
    'AdapterConfig',
    'load_adapter_configs',
    'validate_config'
]

__version__ = "1.0.0"
__description__ = "Mental Prosthetic Platform Service Adapter Framework"
