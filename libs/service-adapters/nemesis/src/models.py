"""Nemesis data models."""
from pydantic import BaseModel
from typing import Optional


class BaseResponse(BaseModel):
    """Base response model."""
    status: str
    message: Optional[str] = None
