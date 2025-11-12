# Brute Ratel C4 Integration Directory

This directory will contain the Brute Ratel C4 integration.

## Migration Instructions

When migrating from `features/brute-ratel/`, move the following:

### Core Components
- **Application Code**: Move main application files and business logic
- **Configuration**: Move config files to `../services/brute-ratel_config.py`
- **Database Schema**: Migrate database models to `../data/models/`
- **API Integration**: Create FastAPI endpoints in `../api/brute-ratel_api.py`

### Description
Red team C2 framework and toolkit

### Integration Points
- **Security-service Service API**: Expose operations via FastAPI endpoints
- **Database**: Convert schemas to PostgreSQL models
- **Authentication**: Integrate with unified JWT authentication
- **n8n Integration**: Create workflow nodes for automation

### Performance Requirements
- Response time: <1s for threat analysis
- Support for concurrent operations
- Caching for frequently accessed data

## TODO: Delete this README when migration is complete

This placeholder will be replaced with actual integration code during the migration process.
