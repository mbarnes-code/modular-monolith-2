# Mealie Service

This service integrates [Mealie](https://github.com/mealie-recipes/mealie) - a self-hosted recipe manager and meal planner - into the Jane platform.

**Note**: This directory contains the complete Mealie application moved from `features/mealie/` into the proper NX project structure.

## Project Structure

Following NX best practices, the Mealie service is organized as a workspace containing multiple applications and shared libraries:

```
apps/mealie-service/
├── src/                           # Node.js integration service (main entry point)
├── apps/                          # NX Applications
│   ├── mealie-api/               # Python/FastAPI backend
│   │   ├── main.py               # FastAPI application entry
│   │   ├── routes/               # API routes
│   │   ├── services/             # Business logic
│   │   ├── db/                   # Database models & migrations
│   │   └── tests/                # Python tests
│   └── mealie-web/               # Nuxt.js/Vue frontend
│       ├── pages/                # Vue pages
│       ├── components/           # Vue components
│       ├── composables/          # Vue composables
│       └── assets/               # Static assets
├── libs/                         # Shared Libraries
│   └── mealie-shared/            # Shared types, constants, utilities
│       ├── src/types.ts          # TypeScript interfaces
│       ├── src/constants.ts      # App constants
│       └── src/utils.ts          # Utility functions
├── tools/                        # Development tools
│   ├── code-generation/          # Code generators
│   └── scripts/                  # Build/dev scripts
├── docker/                       # Docker configuration
├── docs/                         # Documentation
├── nx.json                       # NX workspace configuration
├── pyproject.toml                # Python dependencies
└── LICENSE                       # AGPL license
```

## Features

- **Recipe Management**: Import, organize, and manage recipes
- **Meal Planning**: Plan meals for days, weeks, or months
- **Shopping Lists**: Generate shopping lists from meal plans
- **Recipe Import**: Automatically import recipes from URLs
- **Nutritional Analysis**: Track nutrition information
- **Multi-user Support**: Groups and user management
- **API Integration**: RESTful API for Jane platform integration

## Architecture

This service acts as a Node.js wrapper and integration layer for the existing Mealie codebase:

- **Frontend**: Serves the Nuxt.js/Vue frontend (optional)
- **API Proxy**: Proxies API requests to the Python/FastAPI backend
- **Jane Integration**: Provides standardized endpoints for Jane orchestrator
- **Configuration**: Unified configuration management

## Configuration

Environment variables:

```bash
# Service Configuration
MEALIE_HOST=0.0.0.0
MEALIE_PORT=9925

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mealie

# Frontend
MEALIE_FRONTEND_ENABLED=true
MEALIE_FRONTEND_PATH=./frontend/dist
MEALIE_API_URL=http://localhost:9925

# Authentication
JWT_SECRET=your-secret-key

# Storage
DATA_DIR=./data
BACKUP_DIR=./backups

# Features
ALLOW_SIGNUP=true
ALLOW_GROUP_SELF_JOIN=false
MAX_GROUP_SIZE=50
MAX_FILE_SIZE=100MB
```

## Development

```bash
# Install all dependencies
nx install-all mealie-service

# Start all services in development mode
nx serve-all mealie-service

# Or start services individually:
nx serve mealie-service    # Node.js integration service (port 9925)
nx serve mealie-api        # Python FastAPI backend (port 9000)
nx serve mealie-web        # Nuxt.js frontend (port 3000)

# Build all components
nx build-all mealie-service

# Run tests
nx test mealie-service     # Integration service tests
nx test mealie-api         # Python backend tests
nx test mealie-web         # Frontend tests

# Lint code
nx lint mealie-api         # Python linting
nx lint mealie-web         # Frontend linting
```

## Integration with Jane Platform

The service provides these integration endpoints:

- `GET /api/jane/status` - Service status and capabilities
- `GET /health` - Health check endpoint

## Original Mealie

This integration preserves 100% of the original Mealie functionality:

- Full recipe database and management
- Meal planning and shopping lists
- Recipe sharing and groups
- Import from various sources
- Backup and restore functionality
- All API endpoints from the original Mealie

For complete documentation, see the [official Mealie docs](https://docs.mealie.io/).

## Docker Support

The service can be deployed as part of the Jane platform Docker stack or as a standalone container.

## License

This integration maintains the AGPL license of the original Mealie project.