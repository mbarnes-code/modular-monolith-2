"""
Data synchronization API module.

Contains FastAPI endpoints for managing cross-tool data synchronization
across all 37 integrated tools.
"""

from .endpoints import router

__all__ = ["router"]
