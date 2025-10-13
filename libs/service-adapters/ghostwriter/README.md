# Ghostwriter Adapter

Service adapter for Ghostwriter integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.ghostwriter.src.client import GhostwriterClient

client = GhostwriterClient()
health = client.health_check()
```
