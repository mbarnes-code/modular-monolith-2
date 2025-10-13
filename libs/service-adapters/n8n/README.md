# N8n Adapter

Service adapter for N8n integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.n8n.src.client import N8nClient

client = N8nClient()
health = client.health_check()
```
