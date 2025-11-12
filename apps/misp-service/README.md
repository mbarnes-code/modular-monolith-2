# MISP Service

MISP threat intelligence sharing platform integrated into the NX monorepo.

## Quick Start

```bash
# Install dependencies
nx install misp-service

# Initialize project  
nx setup misp-service

# Start development server
nx serve misp-service

# Run tests
nx test misp-service
```

## Available Commands

- `nx serve misp-service` - Start development server
- `nx build misp-service` - Build application
- `nx test misp-service` - Run tests
- `nx lint misp-service` - Check code quality
- `nx docker:build misp-service` - Build Docker image
- `nx docker:run misp-service` - Start with Docker

See [NX_README.md](NX_README.md) for detailed documentation.
