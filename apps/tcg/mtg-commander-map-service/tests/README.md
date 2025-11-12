# Tests for MTG Commander Map Service

This directory contains test files for the MTG Commander Map Service.

## Test Structure

```
tests/
├── __init__.py
├── conftest.py          # pytest configuration and fixtures
├── test_card.py         # Tests for card module
├── test_calculate.py    # Tests for calculate module
├── test_load.py         # Tests for load module
└── integration/         # Integration tests
    └── test_map_generation.py
```

## Running Tests

```bash
# Run all tests
nx run mtg-commander-map-service:test

# Run specific test file
cd apps/mtg-commander-map-service
python -m pytest tests/test_card.py -v
```