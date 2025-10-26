# MTG Scripting Toolkit Integration Directory

This directory will contain the MTG Scripting Toolkit integration.

## Migration Instructions

When migrating from `features/mtg-scripting-toolkit/`, move the following:

### Core Components
- **Application Code**: Move main application files and business logic
- **Configuration**: Move config files to `../services/mtg-scripting-toolkit_config.py`
- **Database Schema**: Migrate database models to `../data/models/`
- **API Integration**: Create FastAPI endpoints in `../api/mtg-scripting-toolkit_api.py`

### Description
Automation scripts for MTG workflows

### Integration Points
- **Mtg-service Service API**: Expose operations via FastAPI endpoints
- **Database**: Convert schemas to PostgreSQL models
- **Authentication**: Integrate with unified JWT authentication
- **n8n Integration**: Create workflow nodes for automation

### Performance Requirements
- Response time: <3s for game analysis
- Support for concurrent operations
- Caching for frequently accessed data

## TODO: Delete this README when migration is complete

This placeholder will be replaced with actual integration code during the migration process.
