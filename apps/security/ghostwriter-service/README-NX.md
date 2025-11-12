# Ghostwriter Service - NX Best Practices Implementation

## 🎯 Overview

This is a complete reorganization of Ghostwriter following NX best practices for enterprise-grade monorepo management. The service maintains 100% compatibility with the original Ghostwriter platform while providing modern tooling, better organization, and improved developer experience.

## 📁 Project Structure (NX Optimized)

```text
apps/ghostwriter-service/
├── src/                     # Source code (follows NX conventions)
│   ├── ghostwriter/         # Django application modules
│   │   ├── api/            # REST API endpoints
│   │   ├── home/           # Home/dashboard functionality  
│   │   ├── reporting/      # Report generation & templates
│   │   ├── rolodex/        # Client & contact management
│   │   ├── shepherd/       # Domain & infrastructure tracking
│   │   └── oplog/          # Operation logging
│   ├── config/             # Django settings & configuration
│   │   ├── settings/       # Environment-specific settings
│   │   ├── urls.py         # URL routing
│   │   └── wsgi.py         # WSGI application
│   └── locale/             # Internationalization
├── requirements/           # Python dependencies (layered)
│   ├── base.txt           # Core dependencies
│   ├── local.txt          # Development dependencies
│   └── production.txt     # Production dependencies
├── compose/               # Docker configurations
│   ├── local/            # Development containers
│   └── production/       # Production containers
├── static/               # Static files (served by Django)
├── media/                # User-uploaded files
├── pyproject.toml        # Modern Python project config
├── Dockerfile            # Multi-stage container build
├── project.json          # NX project configuration
└── .env.example          # Environment template
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install Python dependencies (handled by NX)
nx build ghostwriter-service

# Set up environment
cp .env.example .env
# Edit .env with your configuration
```

### Development Server

```bash
# Start development server
nx serve ghostwriter-service

# With specific configuration
nx serve ghostwriter-service:development
nx serve ghostwriter-service:production
```

### Docker Development

```bash
# Local Docker environment
nx serve:docker ghostwriter-service:local

# Production Docker environment  
nx serve:docker ghostwriter-service:production
```

## 🧪 Testing & Quality Assurance

### Testing Strategy

```bash
# Full test suite with coverage
nx test ghostwriter-service

# Specific test types
nx test:unit ghostwriter-service      # Unit tests only
nx test:integration ghostwriter-service # Integration tests only
```

### Code Quality

```bash
# Linting (flake8, pylint, mypy)
nx lint ghostwriter-service

# Code formatting
nx format ghostwriter-service         # Apply formatting
nx format:check ghostwriter-service   # Check without changes
```

### System Checks

```bash
# Django system checks
nx check ghostwriter-service
```

## 🗄️ Database Management

### Migrations

```bash
# Create migrations
nx makemigrations ghostwriter-service

# Apply migrations  
nx migrate ghostwriter-service
```

### Admin & Users

```bash
# Create superuser
nx createsuperuser ghostwriter-service

# Django shell
nx shell ghostwriter-service
```

## 🏗️ Build & Deployment

### Build Process

```bash
# Build for deployment (collects static, prepares dist/)
nx build ghostwriter-service
```

### Static Files

```bash
# Collect static files
nx collectstatic ghostwriter-service
```

### Docker Operations

```bash
# Build Docker image
nx docker:build ghostwriter-service

# Run containerized application
nx docker:run ghostwriter-service
```

## ⚙️ Configuration Management

### Environment Variables

The service uses a layered configuration approach:

- `.env` - Local development overrides
- `src/config/settings/local.py` - Development settings
- `src/config/settings/production.py` - Production settings
- `src/config/settings/test.py` - Test settings

### Key Environment Variables

```bash
# Core Django
DJANGO_DEBUG=True
DJANGO_SECRET_KEY=your-secret-key
DJANGO_SETTINGS_MODULE=config.settings.local

# Database
DATABASE_URL=postgres://user:pass@localhost:5432/ghostwriter

# Redis (for caching/sessions)
REDIS_URL=redis://localhost:6379/0

# Security
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
```

## 🏷️ NX Tags & Dependencies

### Project Tags

- `type:app` - Application project type
- `framework:django` - Django web framework
- `language:python` - Python programming language
- `domain:security` - Security domain functionality
- `scope:ghostwriter` - Ghostwriter project scope

### Dependencies

- **Implicit**: `jane-orchestrator` (API gateway integration)
- **Explicit**: Defined in `project.json` targets

## 📊 Caching & Performance

NX provides intelligent caching for:

- **Build operations** - Static file collection, dist preparation
- **Test runs** - Cached based on source changes
- **Lint checks** - Cached based on code and config changes

### Cache Inputs

- Source files: `{projectRoot}/src/**/*.py`
- Configuration: `pyproject.toml`, `setup.cfg`, `pytest.ini`
- Dependencies: `requirements/*.txt`

## 🔧 Development Tools Integration

### VS Code Integration

Pre-configured tasks available in Command Palette:

- `Tasks: Run Task` → `Serve Ghostwriter Service`
- `Tasks: Run Task` → `Test Ghostwriter Service`
- `Tasks: Run Task` → `Lint Ghostwriter Service`

### Python Tools Configuration

- **Black**: Code formatting (120 char line length)
- **isort**: Import sorting (compatible with Black)
- **Flake8**: Style guide enforcement  
- **Pylint**: Code analysis and quality metrics
- **MyPy**: Static type checking
- **Pytest**: Test framework with coverage

## 🐳 Docker Support

### Multi-stage Dockerfile

- **Development**: Includes dev dependencies, live reload
- **Production**: Optimized image, security hardening

### Docker Compose

- `local.yml` - Development environment with hot reload
- `production.yml` - Production-ready with proper networking

## 🔄 CI/CD Integration

The NX configuration provides CI/CD ready targets:

```yaml
# Example GitHub Actions integration
- name: Test Ghostwriter
  run: nx test ghostwriter-service

- name: Lint Ghostwriter  
  run: nx lint ghostwriter-service

- name: Build Ghostwriter
  run: nx build ghostwriter-service
```

## 🎯 NX Best Practices Applied

1. **Source Organization**: All source code in `src/` directory
2. **Layered Configuration**: Environment-specific settings
3. **Comprehensive Targets**: Build, test, lint, format, deploy
4. **Proper Caching**: Inputs/outputs defined for optimal performance
5. **Modern Tooling**: pyproject.toml, Black, MyPy integration
6. **Container Optimization**: Multi-stage Dockerfile
7. **Development Experience**: VS Code integration, live reload
8. **Quality Gates**: Comprehensive linting and testing
9. **Dependency Management**: Clear implicit/explicit dependencies
10. **Documentation**: Comprehensive setup and usage guides

## 🔗 Integration Points

- **Jane Orchestrator**: API gateway and request routing
- **Security Service**: Domain-specific shared functionality  
- **Shared Libraries**: Common utilities and components
- **Database**: PostgreSQL with Redis caching
- **Authentication**: Integrated with workspace auth system

## 📚 Additional Resources

- [NX Documentation](https://nx.dev/concepts/more-concepts/applications-and-libraries)
- [Original Ghostwriter Wiki](https://ghostwriter.wiki/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/topics/best-practices/)
- [Workspace Development Guidelines](/CONTRIBUTING.md)
