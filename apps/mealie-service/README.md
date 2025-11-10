# Mealie Service

This service integrates [Mealie](https://github.com/mealie-recipes/mealie) - a self-hosted recipe manager and meal planner - into the Jane platform.

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
# Start development server
nx serve mealie-service

# Build for production
nx build mealie-service

# Run tests
nx test mealie-service

# Lint code
nx lint mealie-service
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