"""
Performance Validation API Module

Provides REST API endpoints for domain performance validation system.
"""

from .endpoints import performance_router

__all__ = ["performance_router"]
