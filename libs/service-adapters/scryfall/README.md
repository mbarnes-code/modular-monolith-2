# Scryfall Adapter

Service adapter for Scryfall integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.scryfall.src.client import ScryfallClient

client = ScryfallClient()
health = client.health_check()
```
