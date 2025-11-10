# Dispatch Core Library

Shared core utilities, types, and foundational components for the Dispatch incident management ecosystem.

## Overview

`dispatch-core` is a foundational library that provides shared components used across all Dispatch-related projects. This library follows NX best practices by extracting common functionality into a reusable, well-tested module.

## Architecture

This library provides the foundational building blocks for the Dispatch ecosystem:

### **Core Components**
- **Types** (`types.py`): Shared data structures and type definitions
- **Enums** (`enums.py`): Application-wide enumeration values
- **Exceptions** (`exceptions.py`): Custom exception hierarchy
- **Utils** (`utils.py`): Common utility functions

### **Design Principles**
- **Zero Business Logic**: Contains only foundational, domain-agnostic code
- **High Reusability**: All exports designed for use across multiple projects
- **Minimal Dependencies**: Keeps the dependency footprint small
- **Type Safety**: Full TypeScript-style type hints for Python

## Usage

### Installing in your NX project

Add to your project's dependencies in `project.json`:

```json
{
  "targets": {
    "build": {
      "dependsOn": ["^build"],
      "options": {
        "dependencies": ["dispatch-core"]
      }
    }
  }
}
```

### Importing Components

```python
# Type definitions
from dispatch_core.types import (
    DispatchModel,
    BaseModel,
    PaginatedResponse,
    FilterSpec
)

# Enumerations
from dispatch_core.enums import (
    IncidentStatus,
    IncidentPriority,
    TaskStatus,
    EventType
)

# Exception handling
from dispatch_core.exceptions import (
    DispatchException,
    ValidationError,
    NotFoundError,
    ConfigurationError
)

# Utility functions
from dispatch_core.utils import (
    generate_uuid,
    format_timestamp,
    sanitize_input,
    parse_filters
)
```

## API Reference

### Types (`dispatch_core.types`)

#### `DispatchModel`
Base model class for all Dispatch entities with common fields.

```python
class DispatchModel:
    id: Optional[int]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    def to_dict(self) -> dict
    def from_dict(cls, data: dict) -> 'DispatchModel'
```

#### `PaginatedResponse`
Standard pagination response format.

```python
class PaginatedResponse:
    items: List[Any]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool
```

### Enums (`dispatch_core.enums`)

#### `IncidentStatus`
```python
class IncidentStatus(str, Enum):
    ACTIVE = "Active"
    STABLE = "Stable" 
    CLOSED = "Closed"
```

#### `IncidentPriority`
```python
class IncidentPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
```

### Exceptions (`dispatch_core.exceptions`)

#### `DispatchException`
Base exception class for all Dispatch-related errors.

```python
class DispatchException(Exception):
    def __init__(self, message: str, error_code: Optional[str] = None)
```

#### `ValidationError`
Raised when input validation fails.

#### `NotFoundError`
Raised when a requested resource cannot be found.

#### `ConfigurationError`
Raised when there are configuration issues.

### Utils (`dispatch_core.utils`)

#### `generate_uuid() -> str`
Generates a UUID4 string for entity identification.

#### `format_timestamp(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str`
Formats datetime objects consistently.

#### `sanitize_input(input_str: str) -> str`
Sanitizes user input to prevent injection attacks.

#### `parse_filters(filter_params: dict) -> List[FilterSpec]`
Parses query parameters into standardized filter specifications.

## Development

### NX Commands

```bash
# Testing
npx nx test dispatch-core              # Run unit tests
npx nx test-cov dispatch-core         # Run tests with coverage

# Code Quality
npx nx lint dispatch-core             # Run linting
npx nx lint-fix dispatch-core         # Fix linting issues
npx nx format dispatch-core           # Format code
npx nx type-check dispatch-core       # Type checking

# Building
npx nx build dispatch-core            # Build library
```

### Adding New Components

1. **Types**: Add to `src/types.py` - ensure they're generic and reusable
2. **Enums**: Add to `src/enums.py` - use string enums for JSON serialization
3. **Exceptions**: Add to `src/exceptions.py` - inherit from `DispatchException`
4. **Utils**: Add to `src/utils.py` - ensure they're pure functions when possible

### Testing Guidelines

- **Unit Tests**: Test all public functions and classes
- **Type Safety**: Verify all exports have proper type hints
- **Documentation**: Include docstrings for all public APIs
- **Examples**: Provide usage examples in docstrings

## Dependencies

### Runtime Dependencies
- `pydantic`: For data validation and serialization
- `typing-extensions`: For advanced type hints

### Development Dependencies  
- `pytest`: Testing framework
- `mypy`: Type checking
- `ruff`: Linting and formatting

## Migration Notes

This library was extracted from the main `dispatch-service` to follow NX best practices:

- **Before**: All utilities mixed with application code
- **After**: Clean separation with reusable, well-tested components
- **Benefits**: Improved maintainability, better testing, clear dependencies

## Related Libraries

- **dispatch-database**: Database models and data access (depends on dispatch-core)
- **dispatch-service**: Main application service (depends on dispatch-core)

## Project Tags

- `type:library` - Shared library
- `domain:utilities` - Core utilities domain  
- `scope:shared` - Cross-project shared code