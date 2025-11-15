# Ghostwriter Service - NX Integration

This is the NX-integrated version of Ghostwriter, an open-source platform designed to enhance offensive security operations by simplifying report writing, asset tracking, and assessment management.

## Original Project

Ghostwriter is developed by SpecterOps and available at: <https://github.com/GhostManager/Ghostwriter>

## NX Best Practices Implementation

This service follows NX best practices with a structured approach:

### Project Structure

```text
apps/ghostwriter-service/
├── src/                     # Source code (NX best practice)
│   ├── ghostwriter/         # Django application modules
│   ├── config/              # Django configuration
│   └── locale/              # Internationalization files
├── tests/                   # Test files (if needed beyond Django tests)
├── requirements/            # Python dependencies
├── compose/                 # Docker configurations
├── pyproject.toml          # Modern Python project configuration
├── Dockerfile              # Optimized for production
└── project.json            # NX project configuration
```

### Available Commands

#### Core Development

```bash
# Development server (with configurations)
nx serve ghostwriter-service                    # Default development
nx serve ghostwriter-service:development        # Explicit development
nx serve ghostwriter-service:production         # Production mode

# Docker deployment
nx serve:docker ghostwriter-service             # Local Docker
nx serve:docker ghostwriter-service:local       # Explicit local
nx serve:docker ghostwriter-service:production  # Production Docker

# Build for deployment
nx build ghostwriter-service
```

#### Testing & Quality

```bash
# Testing
nx test ghostwriter-service           # Full test suite with coverage
nx test:unit ghostwriter-service      # Unit tests only
nx test:integration ghostwriter-service # Integration tests only

# Code Quality
nx lint ghostwriter-service           # Full linting (flake8, pylint, mypy)
nx format ghostwriter-service         # Format code (black, isort)
nx format:check ghostwriter-service   # Check formatting without changes
```

#### Django Management

```bash
# Database operations
nx migrate ghostwriter-service        # Run migrations
nx makemigrations ghostwriter-service # Create migrations

# Static files and utilities
nx collectstatic ghostwriter-service  # Collect static files
nx shell ghostwriter-service          # Django shell
nx createsuperuser ghostwriter-service # Create admin user
nx check ghostwriter-service          # Django system checks
```

#### Docker Operations

```bash
# Docker operations
nx docker:build ghostwriter-service   # Build Docker image
nx docker:run ghostwriter-service     # Run containerized app
```

### Configuration

The service is configured as a Django application with the following tags:

- `type:app` - Application type
- `framework:django` - Django framework  
- `language:python` - Python language
- `domain:security` - Security domain
- `scope:ghostwriter` - Project scope

### Dependencies

See the `requirements/` directory for Python dependencies:

- `requirements/base.txt` - Base requirements
- `requirements/local.txt` - Local development requirements  
- `requirements/production.txt` - Production requirements

### Docker Support

The service supports both local and production Docker deployments:

- `local.yml` - Local Docker Compose configuration
- `production.yml` - Production Docker Compose configuration

## Architecture Integration

This service is part of the larger modular monolith architecture and integrates with:

- Jane Orchestrator (main API gateway)
- Security Service (domain-specific services)
- Shared libraries and utilities

## Documentation

For detailed Ghostwriter documentation, see:

- [Ghostwriter Wiki](https://ghostwriter.wiki/)
- Local documentation in the `DOCS/` directory
- Original README.md for project-specific information

## License

This project maintains the original BSD-3-Clause license from the upstream Ghostwriter project.
