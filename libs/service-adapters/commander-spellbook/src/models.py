"""Commander Spellbook data models."""
from pydantic import BaseModel
from typing import List, Optional


class Card(BaseModel):
    """MTG Card model."""
    name: str
    oracle_id: Optional[str] = None


class Combo(BaseModel):
    """Commander Spellbook combo model."""
    id: str
    cards: List[Card]
    description: str
    prerequisites: Optional[str] = None
    steps: Optional[str] = None
