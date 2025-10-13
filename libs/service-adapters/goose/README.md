# Goose Adapter

Service adapter for Goose integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.goose.src.client import GooseClient

client = GooseClient()
health = client.health_check()
```
