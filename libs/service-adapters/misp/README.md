# Misp Adapter

Service adapter for Misp integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.misp.src.client import MispClient

client = MispClient()
health = client.health_check()
```
