# Chroma MCP Integration Directory

This directory will contain the Chroma MCP integration.

## Migration Instructions

When migrating from `features/mcp-servers/chroma-mcp/`, move the following:

### Core Components
- **Application Code**: Move main application files and business logic
- **Configuration**: Move config files to `../services/mcp-servers/chroma-mcp_config.py`
- **Database Schema**: Migrate database models to `../data/models/`
- **API Integration**: Create FastAPI endpoints in `../api/mcp-servers/chroma-mcp_api.py`

### Description
Vector database MCP server integration

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
