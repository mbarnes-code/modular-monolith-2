"""
Authentication API module for executive function platform.

This module provides JWT-based authentication with unified session management
and executive function user preferences support.
"""

from .endpoints import router

__all__ = ["router"]
