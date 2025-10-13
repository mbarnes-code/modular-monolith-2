# Actual-budget Adapter

Service adapter for Actual-budget integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.actual-budget.src.client import Actual-budgetClient

client = Actual-budgetClient()
health = client.health_check()
```
