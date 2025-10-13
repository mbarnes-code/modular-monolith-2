# Nemesis Adapter

Service adapter for Nemesis integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.nemesis.src.client import NemesisClient

client = NemesisClient()
health = client.health_check()
```
