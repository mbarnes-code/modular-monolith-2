"""
Data Consistency Validation API Module.

Provides REST API endpoints for managing data consistency validation
across all 37 integrated tools.
"""

from .endpoints import router

__all__ = ["router"]
