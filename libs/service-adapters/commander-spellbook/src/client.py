"""Commander Spellbook API client."""
import requests
from typing import Optional, Dict, Any


class CommanderSpellbookClient:
    """Client for Commander Spellbook API."""

    def __init__(self, base_url: str = "https://commanderspellbook.com/api"):
        self.base_url = base_url
        self.session = requests.Session()

    def get_combo(self, combo_id: str) -> Optional[Dict[str, Any]]:
        """Get a combo by ID."""
        response = self.session.get(f"{self.base_url}/combos/{combo_id}")
        response.raise_for_status()
        return response.json()

    def search_combos(self, query: str) -> list:
        """Search for combos."""
        response = self.session.get(f"{self.base_url}/combos", params={"q": query})
        response.raise_for_status()
        return response.json()
