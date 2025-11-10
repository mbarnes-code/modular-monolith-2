# Dispatch Service

Integration service for Netflix's Dispatch incident management platform within the Mental Prosthetic Platform, organized following NX best practices.

## Overview

Dispatch is an incident management and orchestration platform that provides:

- **Incident Management**: Create, track, and manage security incidents
- **Task Orchestration**: Automatic task assignment and tracking
- **Communication Workflows**: Integration with Slack, email, and other communication tools
- **Post-Incident Analysis**: Review and learning capabilities
- **Tool Integration**: Deep integration with existing organizational tools

## NX Architecture

This service follows NX best practices with a clean separation of concerns:

### **Project Structure**
```
apps/dispatch-service/           # Main application
├── src/
│   ├── app/                    # Application core (config, extensions, models)
│   ├── api/                    # FastAPI endpoints and routing
│   ├── domains/                # Domain-specific business logic
│   ├── services/               # Business logic and external integrations
│   └── main.py                 # Application entry point
└── tests/                      # Application tests

libs/dispatch-core/              # Shared core library
├── src/
│   ├── types.py               # Shared type definitions
│   ├── enums.py               # Application enumerations
│   ├── exceptions.py          # Custom exceptions
│   └── utils.py               # Utility functions

libs/dispatch-database/          # Database library
└── src/
    └── data/                   # Database models, migrations, schemas
```

### **Dependencies**
- **dispatch-service** → depends on → **dispatch-core**, **dispatch-database**
- **dispatch-database** → depends on → **dispatch-core**

## Performance Target

- **Response Time**: <2s for incident management workflows
- **Integration Pattern**: Service adapter with business logic preservation

## Development

### Prerequisites

- Python 3.12+
- NX workspace
- FastAPI, SQLAlchemy, Alembic

### NX Commands

```bash
# Development
npx nx serve dispatch-service              # Start development server
npx nx serve-prod dispatch-service         # Start production server

# Building
npx nx build dispatch-service              # Build the service

# Testing
npx nx test dispatch-service               # Run tests
npx nx test-cov dispatch-service          # Run tests with coverage

# Code Quality
npx nx lint dispatch-service              # Run linting
npx nx lint-fix dispatch-service          # Fix linting issues
npx nx format dispatch-service            # Format code
npx nx type-check dispatch-service        # Type checking

# Database
npx nx migrations-upgrade dispatch-service # Run database migrations
npx nx migrations-downgrade dispatch-service # Rollback migrations
```

### Running Multiple Commands

```bash
# Quality checks
npx nx run-many --target=lint --projects=dispatch-service,dispatch-core,dispatch-database

# Build all dispatch projects
npx nx run-many --target=build --projects=dispatch-service,dispatch-core,dispatch-database
```

## API Endpoints

### Core Endpoints

- `GET /` - Service information and health
- `GET /health` - Health check endpoint
- `GET /incidents` - List all incidents
- `POST /incidents` - Create new incident
- `GET /incidents/{id}` - Get incident details

### Integration Status

🚧 **Current Status**: NX reorganization complete, API integration in progress

The service has been restructured following NX best practices:

✅ **Completed**:
- Clean project structure with shared libraries
- Proper dependency management
- Enhanced NX targets (lint, format, type-check, etc.)
- Separated core utilities and database layer
- Improved build and test processes

🚧 **In Progress**:
- Full API router integration
- Database connection setup
- Authentication and authorization
- External service integrations

## Shared Libraries

### **dispatch-core** (`libs/dispatch-core`)
Shared utilities, types, enums, and exceptions used across the Dispatch ecosystem.

**Key Features**:
- Type definitions for consistent data structures
- Application-wide enumerations
- Custom exception classes
- Common utility functions

**Usage**: 
```python
from dispatch_core.types import DispatchModel
from dispatch_core.enums import IncidentStatus
from dispatch_core.exceptions import DispatchException
```

### **dispatch-database** (`libs/dispatch-database`)
Database models, migrations, and data access utilities.

**Key Features**:
- SQLAlchemy models and relationships
- Alembic migration configurations
- Database connection utilities
- Data access patterns

**Usage**:
```python
from dispatch_database.data.database import get_db
from dispatch_database.data.models import Incident
```

## NX Best Practices Implemented

✅ **Project Organization**: Clean separation between apps and libs
✅ **Dependency Management**: Explicit project dependencies
✅ **Build Targets**: Comprehensive build, test, lint, format targets
✅ **Code Quality**: Ruff formatting, MyPy type checking, pytest testing
✅ **Caching**: Proper .gitignore with cache directories excluded
✅ **Tagging**: Proper project tags for type, domain, and scope
✅ **Library Extraction**: Common code moved to reusable libraries

## Related Documentation

- [Original Dispatch Repository](https://github.com/Netflix/dispatch) (Archived)
- [Dispatch Documentation](https://netflix.github.io/dispatch/)
- [NX Documentation](https://nx.dev)
- [Mental Prosthetic Platform Architecture](../../docs/)

## Project Tags

- `type:service` - Service application
- `domain:incident-management` - Incident management domain
- `scope:backend` - Backend service
- **Dependencies**: `dispatch-core`, `dispatch-database`
