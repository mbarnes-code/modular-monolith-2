# Firecrawl Adapter

Service adapter for Firecrawl integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.firecrawl.src.client import FirecrawlClient

client = FirecrawlClient()
health = client.health_check()
```
