"""Misp API client."""
import requests
from typing import Optional, Dict, Any


class MispClient:
    """Client for Misp API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def health_check(self) -> Dict[str, Any]:
        """Check service health."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
