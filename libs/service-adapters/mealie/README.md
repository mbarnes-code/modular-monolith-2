# Mealie Adapter

Service adapter for Mealie integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.mealie.src.client import MealieClient

client = MealieClient()
health = client.health_check()
```
