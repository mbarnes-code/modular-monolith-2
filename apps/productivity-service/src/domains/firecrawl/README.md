# Firecrawl Integration Directory

This directory will contain the Firecrawl integration.

## Migration Instructions

When migrating from `features/firecrawl/`, move the following:

### Core Components
- **Application Code**: Move main application files and business logic
- **Configuration**: Move config files to `../services/firecrawl_config.py`
- **Database Schema**: Migrate database models to `../data/models/`
- **API Integration**: Create FastAPI endpoints in `../api/firecrawl_api.py`

### Description
Web scraping and content extraction service

### Integration Points
- **Productivity-service Service API**: Expose operations via FastAPI endpoints
- **Database**: Convert schemas to PostgreSQL models
- **Authentication**: Integrate with unified JWT authentication
- **n8n Integration**: Create workflow nodes for automation

### Performance Requirements
- Response time: <2s for task management
- Support for concurrent operations
- Caching for frequently accessed data

## TODO: Delete this README when migration is complete

This placeholder will be replaced with actual integration code during the migration process.
