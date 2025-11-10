# MISP Integration Directory

This directory will contain the MISP (Malware Information Sharing Platform) integration.

## Migration Instructions

When migrating from `features/misp/`, move the following:

### Core MISP Components:
- **Application Code**: Move MISP's CakePHP application from `features/misp/app/`
- **Database Schema**: Migrate MySQL schema to PostgreSQL in `../data/models/`
- **Configuration**: Move config files to `../services/misp_config.py`
- **API Endpoints**: Extract MISP's REST API and integrate with FastAPI in `../api/misp_api.py`

### Key Files to Migrate:
- `features/misp/app/Model/Event.php` → Business logic preservation (8,733 lines)
- `features/misp/app/Controller/EventsController.php` → API endpoint logic
- `features/misp/app/webroot/` → Static assets to appropriate location
- `features/misp/INSTALL/` → Documentation and setup scripts

### Integration Points:
- **Security Service API**: Expose MISP operations via FastAPI endpoints
- **Database**: Convert MySQL schema to PostgreSQL models
- **Authentication**: Integrate with unified JWT authentication
- **n8n Integration**: Create MISP-specific n8n nodes for workflow automation

### Performance Requirements:
- Response time: <1s for threat analysis operations
- Support for concurrent threat intelligence queries
- Caching for frequently accessed IOCs and attributes

## TODO: Delete this README when migration is complete

This placeholder will be replaced with actual MISP integration code during the migration process.