# Helk Adapter

Service adapter for Helk integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.helk.src.client import HelkClient

client = HelkClient()
health = client.health_check()
```
