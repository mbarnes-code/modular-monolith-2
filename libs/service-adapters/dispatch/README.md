# Dispatch Adapter

Service adapter for Dispatch integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.dispatch.src.client import DispatchClient

client = DispatchClient()
health = client.health_check()
```
