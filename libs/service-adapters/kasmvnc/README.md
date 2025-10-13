# Kasmvnc Adapter

Service adapter for Kasmvnc integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.kasmvnc.src.client import KasmvncClient

client = KasmvncClient()
health = client.health_check()
```
