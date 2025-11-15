# HexStrike Service

NX Application for HexStrike AI MCP Cybersecurity Automation Platform following NX best practices.

## Overview

This NX project contains the HexStrike AI MCP service, organized as a modern Python application with proper module structure:

- AI-Powered MCP Cybersecurity Automation Platform
- Advanced penetration testing framework with 150+ security tools  
- 12+ autonomous AI agents
- MCP (Model Context Protocol) integration
- Modular architecture following NX best practices

## Project Structure

```
apps/hexstrike-service/
├── src/
│   └── hexstrike/                 # Main package
│       ├── __init__.py           # Package initialization
│       ├── api/                  # API layer
│       │   └── main.py          # Server entry point
│       ├── core/                 # Core business logic
│       ├── mcp/                  # MCP integration
│       │   └── client.py        # MCP client entry point
│       ├── tools/                # Security tools integration
│       ├── config/               # Configuration management
│       │   └── settings.py      # Environment-based configuration
│       └── utils/                # Utility functions
│           └── helpers.py       # Common helper functions
│   ├── hexstrike_server.py      # Legacy server (for compatibility)
│   └── hexstrike_mcp.py         # Legacy MCP client (for compatibility)
├── tests/                        # Test suite
├── assets/                       # Static assets and images
├── .env.example                  # Environment template
├── .env                         # Local environment (git-ignored)
├── Dockerfile                   # Multi-stage Docker build
├── docker-compose.yml           # Development stack
├── project.json                 # NX project configuration
├── pyproject.toml              # Python project configuration
├── requirements.txt            # Python dependencies
└── README_NX.md               # This file
```

## Available Commands

### Development
- `nx serve hexstrike-service` - Start the modern HexStrike server
- `nx serve-legacy hexstrike-service` - Start the legacy server
- `nx serve-mcp hexstrike-service` - Start the modern MCP client
- `nx serve-mcp-legacy hexstrike-service` - Start the legacy MCP client
- `nx test hexstrike-service` - Run test suite
- `nx lint hexstrike-service` - Run code linting
- `nx format hexstrike-service` - Format code with Black
- `nx type-check hexstrike-service` - Run type checking with mypy

### Docker Operations
- `nx docker:build hexstrike-service` - Build Docker image
- `nx docker:up hexstrike-service` - Start services with Docker Compose
- `nx docker:down hexstrike-service` - Stop Docker services

### Maintenance
- `nx install hexstrike-service` - Install Python dependencies
- `nx clean hexstrike-service` - Clean Python cache files

## Configuration

The service uses environment-based configuration:

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings:
   ```bash
   HEXSTRIKE_ENV=development
   HEXSTRIKE_DEBUG=true
   HEXSTRIKE_PORT=8000
   ```

3. Available environments:
   - `development` - Development with debug enabled
   - `production` - Production-optimized settings
   - `testing` - Testing configuration

## Getting Started

### Local Development

1. Install dependencies:
   ```bash
   nx install hexstrike-service
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. Start the server:
   ```bash
   nx serve hexstrike-service
   ```

### Docker Development

1. Start with Docker Compose:
   ```bash
   nx docker:up hexstrike-service
   ```

2. View logs:
   ```bash
   docker-compose logs -f hexstrike-service
   ```

3. Stop services:
   ```bash
   nx docker:down hexstrike-service
   ```

## Architecture

### Modern Structure (Recommended)
- **API Layer**: `hexstrike.api.main` - Modern Flask application
- **MCP Client**: `hexstrike.mcp.client` - Model Context Protocol integration
- **Configuration**: Environment-based settings with `hexstrike.config.settings`
- **Utilities**: Common functions in `hexstrike.utils.helpers`

### Legacy Support
- Legacy entry points preserved for backward compatibility
- Original `hexstrike_server.py` and `hexstrike_mcp.py` files available
- Use `serve-legacy` and `serve-mcp-legacy` commands for legacy mode

## Features

- **Security Tools**: 150+ integrated cybersecurity tools
- **AI Agents**: 12+ autonomous AI agents for automated tasks
- **MCP Integration**: Model Context Protocol support
- **Modern Architecture**: Modular structure following NX best practices
- **Docker Support**: Multi-stage builds for development and production
- **Environment Configuration**: Flexible configuration management
- **Type Safety**: Full type hints and mypy support
- **Testing**: Comprehensive test suite with pytest

## Dependencies

Core dependencies include:
- Flask (web framework)
- Requests (HTTP client)
- psutil (system utilities)
- FastMCP (MCP framework)
- BeautifulSoup4 (HTML parsing)

Development dependencies:
- pytest (testing framework)
- black (code formatting)
- ruff (fast linting)
- mypy (type checking)

See `requirements.txt` and `pyproject.toml` for complete dependency lists.

## Testing

Run the test suite:
```bash
nx test hexstrike-service
```

Run with coverage:
```bash
python -m pytest --cov=hexstrike tests/
```

## Type Checking

Run type checking:
```bash
nx type-check hexstrike-service
```

## Code Quality

Format code:
```bash
nx format hexstrike-service
```

Lint code:
```bash
nx lint hexstrike-service
```

## License

MIT License - see original project documentation for details.