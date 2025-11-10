# Dispatch Service

Integration service for Netflix's Dispatch incident management platform within the Mental Prosthetic Platform.

## Overview

Dispatch is an incident management and orchestration platform that provides:

- **Incident Management**: Create, track, and manage security incidents
- **Task Orchestration**: Automatic task assignment and tracking
- **Communication Workflows**: Integration with Slack, email, and other communication tools
- **Post-Incident Analysis**: Review and learning capabilities
- **Tool Integration**: Deep integration with existing organizational tools

## Architecture

This service follows the modular monolith architecture with:

- **API Layer** (`src/api/`): FastAPI endpoints and routing
- **Data Layer** (`src/data/`): SQLAlchemy models and database schemas
- **Services Layer** (`src/services/`): Business logic and external integrations
- **Domains Layer** (`src/domains/`): Domain-specific business rules

## Performance Target

- **Response Time**: <2s for incident management workflows
- **Integration Pattern**: Service adapter with business logic preservation

## Development

### Prerequisites

- Python 3.12+
- FastAPI
- SQLAlchemy
- Alembic for database migrations

### Running the Service

```bash
# From the workspace root
npx nx serve dispatch-service

# Or directly with uvicorn
cd apps/dispatch-service
uvicorn src.main:app --reload --host 0.0.0.0 --port 8013
```

### Testing

```bash
# Run tests
npx nx test dispatch-service

# Or directly with pytest
cd apps/dispatch-service
python -m pytest tests/ -v
```

### Linting

```bash
# Run linting
npx nx lint dispatch-service

# Or directly with ruff
cd apps/dispatch-service
ruff check src/
```

## API Endpoints

### Core Endpoints

- `GET /` - Service information and health
- `GET /health` - Health check endpoint
- `GET /incidents` - List all incidents
- `POST /incidents` - Create new incident
- `GET /incidents/{id}` - Get incident details

### Integration Status

🚧 **Current Status**: Service skeleton created, Dispatch integration pending

The service currently provides placeholder implementations. Full Dispatch integration requires:

1. Database schema migration from original Dispatch
2. Authentication and authorization setup
3. Integration with external services (Slack, Jira, etc.)
4. Business logic porting with preservation requirements
5. Performance optimization for <2s response times

## Related Documentation

- [Original Dispatch Repository](https://github.com/Netflix/dispatch) (Archived)
- [Dispatch Documentation](https://netflix.github.io/dispatch/)
- [Mental Prosthetic Platform Architecture](../../docs/)

## Tags

- `type:service` - Service application
- `domain:productivity` - Productivity domain (incident management)
- `scope:backend` - Backend service
