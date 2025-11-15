# MISP NX Integration

This document describes the integration of MISP (Threat Intelligence Sharing Platform) into the NX monorepo architecture.

## Migration Summary

**Date**: November 12, 2025  
**Source**: `features/MISP/` → `apps/misp-service/`  
**Project Type**: PHP/CakePHP Application  
**Domain**: Security (Threat Intelligence)

## Project Overview

MISP is an open source software solution for collecting, storing, distributing and sharing cyber security indicators and threats about cyber security incidents analysis and malware analysis. It's built with:

- **Backend**: PHP with CakePHP framework (version 2.x)
- **Database**: MySQL/PostgreSQL support
- **Frontend**: CakePHP views with JavaScript enhancements
- **Dependencies**: Multiple git submodules for threat intelligence data

## NX Integration Features

### Available Targets

```bash
# Development
nx serve misp-service              # Start PHP development server
nx serve:apache misp-service       # Start with Apache (production-like)

# Building
nx build misp-service              # Basic build verification
nx build:deb misp-service          # Build Debian package

# Testing
nx test misp-service               # Run CakePHP test suite
nx test:unit misp-service          # Run unit tests only
nx test:controller misp-service    # Run controller tests only

# Quality
nx lint misp-service               # PHP syntax check

# Setup
nx setup misp-service              # Initialize submodules and permissions
nx install misp-service            # Install Python and PHP dependencies
nx install:python misp-service     # Install Python dependencies only

# Console
nx console misp-service            # Access CakePHP console
nx migration misp-service          # Run database migrations

# Docker
nx docker:build misp-service       # Build Docker container
nx docker:run misp-service         # Start with Docker Compose
nx docker:stop misp-service        # Stop Docker services
```

### Project Structure

```text
apps/misp-service/
├── project.json                   # NX project configuration
├── app/                          # CakePHP application
│   ├── Config/                   # Configuration files
│   ├── Console/                  # CLI commands
│   ├── Controller/               # Application controllers
│   ├── Model/                    # Data models
│   ├── View/                     # Templates and views
│   ├── Lib/                      # Libraries and CakePHP core
│   └── webroot/                  # Web assets
├── requirements.txt              # Python dependencies
├── requirements-dev.txt          # Development Python dependencies
├── INSTALL/                      # Installation scripts and configs
├── docs/                         # Documentation
├── tests/                        # Test suites
├── tools/                        # Utility scripts
└── .git*                         # Git configuration files
```

## Dependencies and Submodules

MISP uses multiple git submodules for threat intelligence data:

- **CakePHP Framework**: `app/Lib/cakephp` (MISP fork, 2.x branch)
- **Taxonomies**: `app/files/taxonomies` (threat categorization)
- **Warning Lists**: `app/files/warninglists` (false positive filters)
- **Galaxy**: `app/files/misp-galaxy` (threat actor profiles)
- **Objects**: `app/files/misp-objects` (IOC object definitions)
- **STIX Libraries**: Various STIX/CybOX implementation libraries

### Initialization

After migration, run the setup target to initialize all submodules:

```bash
nx setup misp-service
```

This will:

- Initialize and update git submodules recursively
- Set proper file permissions
- Create necessary cache and log directories

## Integration Notes

### PHP/CakePHP in NX Environment

- **Framework**: CakePHP 2.x (legacy but actively maintained by MISP team)
- **Entry Point**: `app/webroot/index.php`
- **Development Server**: Uses PHP's built-in server for development
- **Production**: Designed for Apache/Nginx with proper PHP-FPM

### Security Considerations

- Contains sensitive security intelligence data
- Requires proper database configuration
- Uses GPG keys for data signing and encryption
- Implements role-based access control

### Performance Notes

- Large dataset capabilities (millions of indicators)
- Background job processing for heavy operations
- Caching layers for API performance
- Feed synchronization capabilities

## Development Workflow

1. **Setup**: `nx setup misp-service && nx install misp-service`
2. **Configure**: Set up database and basic configuration files
3. **Develop**: `nx serve misp-service` for local development
4. **Test**: `nx test misp-service` before committing
5. **Build**: `nx build misp-service` to verify production readiness

## Tags and Metadata

- **type**: application
- **scope**: security  
- **framework**: php, cakephp
- **domain**: threat-intelligence

## Migration Validation

✅ All source files copied from `features/MISP/`  
✅ Hidden files and directories preserved (.github, .forgejo, .git*)  
✅ NX project configuration created  
✅ Project registered in workspace nx.json  
✅ Development and production targets configured  
✅ Documentation updated

## Next Steps

1. Test the NX integration with `nx serve misp-service`
2. Configure database connections for your environment
3. Initialize git submodules with `nx setup misp-service`
4. Set up proper Apache/Nginx configuration for production
5. Configure MISP-specific settings (GPG, feeds, etc.)

## Related Projects

This project integrates with other security tools in the monorepo:

- **security-service**: Central security service orchestration
- **helk-service**: Security data analytics platform
- **maltrail-service**: Malicious traffic detection
- **cyber-llm-server**: AI-powered security analysis