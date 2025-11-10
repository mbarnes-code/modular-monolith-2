"""
Dashboard API module for unified executive function tool access.

This module provides comprehensive API endpoints for the unified dashboard
that serves as the primary interface for all 37 executive function tools
across the 4 constitutional domains.
"""

from .endpoints import router

__all__ = ["router"]
