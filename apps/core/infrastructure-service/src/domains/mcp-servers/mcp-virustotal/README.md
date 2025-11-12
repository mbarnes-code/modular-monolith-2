# VirusTotal MCP Integration Directory

This directory will contain the VirusTotal MCP integration.

## Migration Instructions

When migrating from `features/mcp-servers/mcp-virustotal/`, move the following:

### Core Components
- **Application Code**: Move main application files and business logic
- **Configuration**: Move config files to `../services/mcp-servers/mcp-virustotal_config.py`
- **Database Schema**: Migrate database models to `../data/models/`
- **API Integration**: Create FastAPI endpoints in `../api/mcp-servers/mcp-virustotal_api.py`

### Description
VirusTotal integration MCP server

### Integration Points
- **Infrastructure-service Service API**: Expose operations via FastAPI endpoints
- **Database**: Convert schemas to PostgreSQL models
- **Authentication**: Integrate with unified JWT authentication
- **n8n Integration**: Create workflow nodes for automation

### Performance Requirements
- Response time: <5s for system operations
- Support for concurrent operations
- Caching for frequently accessed data

## TODO: Delete this README when migration is complete

This placeholder will be replaced with actual integration code during the migration process.
