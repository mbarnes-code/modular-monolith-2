"""Core type definitions for Dispatch."""
from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime

# Basic type aliases for common use cases
JsonDict = Dict[str, Any]
OptionalStr = Optional[str]
OptionalInt = Optional[int]

# Placeholder types until models are migrated
# TODO: Replace with actual imports once models are migrated to lib
Subject = Any  # Will be Case | Incident once models are available


# Base model interface (to be replaced with actual model)
class DispatchBaseModel:
    """Base model interface for Dispatch entities."""
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
