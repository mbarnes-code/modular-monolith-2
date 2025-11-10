"""
Adaptive Workflows API module.

Provides endpoints for n8n adaptive workflow management including
pattern detection, workflow generation, and validation.
"""

from .endpoints import router

__all__ = ["router"]
