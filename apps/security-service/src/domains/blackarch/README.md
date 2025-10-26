# BlackArch Integration Directory

This directory will contain the BlackArch integration.

## Migration Instructions

When migrating from `features/blackarch/`, move the following:

### Core Components
- **Application Code**: Move main application files and business logic
- **Configuration**: Move config files to `../services/blackarch_config.py`
- **Database Schema**: Migrate database models to `../data/models/`
- **API Integration**: Create FastAPI endpoints in `../api/blackarch_api.py`

### Description
Collection of penetration testing tools

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
