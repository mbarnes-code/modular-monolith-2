# Commander Spellbook Adapter

Service adapter for Commander Spellbook API integration.

## Files

- `src/client.py` - API client implementation
- `src/models.py` - Data models
- `tests/` - Unit tests

## Usage

```python
from libs.service_adapters.commander_spellbook.src.client import CommanderSpellbookClient

client = CommanderSpellbookClient()
combo = client.get_combo("combo-id")
```
