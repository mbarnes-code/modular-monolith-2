# Nemesis Service - NX Integration

This directory contains the Nemesis offensive file enrichment pipeline, integrated into the NX workspace.

## Overview

Nemesis is an offensive file enrichment pipeline built on Docker with Dapr integration, designed to function as an "offensive VirusTotal". The platform consists of multiple microservices for file processing, threat intelligence, and security analysis.

## Architecture

The Nemesis service consists of several components:

### Core Services
- **web-api**: FastAPI-based frontend API
- **file-enrichment**: File processing and enrichment workflows  
- **document-conversion**: Document processing service
- **alerting**: Alert management service
- **triage**: File triage and analysis
- **housekeeping**: System maintenance tasks

### Supporting Infrastructure
- **PostgreSQL**: Primary database
- **RabbitMQ**: Message queue for service communication
- **MinIO**: Object storage for files
- **Hasura**: GraphQL API layer
- **Traefik**: Reverse proxy and load balancer

### Optional Components  
- **Monitoring Stack**: Grafana, Prometheus, Loki, Jaeger
- **Jupyter**: Analysis notebooks
- **NoSEy Parker**: Secret scanning

## Quick Start

### 1. Setup Environment
```bash
# Initialize the environment
npx nx setup nemesis-service

# Copy and configure environment variables
cp apps/nemesis-service/env.example apps/nemesis-service/.env
# Edit .env with your configuration
```

### 2. Build and Run
```bash
# Build all services
npx nx build nemesis-service

# Start all services
npx nx serve nemesis-service

# Or run in background
npx nx serve:background nemesis-service
```

### 3. Access the Platform
- **Web UI**: https://localhost:7443 (default)
- **API**: https://localhost:7443/api
- **Hasura Console**: https://localhost:7443/hasura
- **Documentation**: `npx nx docs:serve nemesis-service`

## Development

### Install Dependencies
```bash
# Install all Python dependencies
npx nx install nemesis-service

# Install development dependencies
npx nx install:dev nemesis-service
```

### Testing
```bash
# Run all tests
npx nx test nemesis-service

# Test specific components
npx nx test:web-api nemesis-service
npx nx test:file-enrichment nemesis-service
```

### Code Quality
```bash
# Lint all Python code
npx nx lint nemesis-service

# Auto-fix linting issues
npx nx lint:fix nemesis-service

# Type checking
npx nx type-check nemesis-service
```

### Docker Management
```bash
# Build containers
npx nx docker:build nemesis-service

# Start services
npx nx docker:up nemesis-service

# View logs
npx nx docker:logs nemesis-service

# Stop services
npx nx docker:down nemesis-service

# Clean up resources
npx nx docker:clean nemesis-service
```

### Monitoring (Optional)
```bash
# Start with monitoring stack
npx nx monitoring:up nemesis-service

# Access monitoring tools:
# - Grafana: https://localhost:7443/grafana
# - Prometheus: https://localhost:7443/prometheus
# - Jaeger: https://localhost:7443/jaeger
```

### Jupyter Analysis (Optional)
```bash
# Start Jupyter notebooks
npx nx jupyter:up nemesis-service

# Access: https://localhost:7443/jupyter
```

## Project Structure

```
apps/nemesis-service/
├── projects/           # Individual microservices
│   ├── web_api/       # FastAPI frontend API
│   ├── file_enrichment/ # File processing workflows
│   ├── document_conversion/ # Document processing
│   ├── alerting/      # Alert management
│   ├── triage/        # File triage
│   ├── housekeeping/  # System maintenance
│   └── frontend/      # React web interface
├── libs/              # Shared libraries
│   ├── common/        # Common utilities
│   └── file_enrichment_modules/ # File processing modules
├── infra/             # Infrastructure configuration
│   ├── docker/        # Container configurations
│   ├── dapr/          # Dapr component definitions
│   ├── postgres/      # Database schemas
│   └── monitoring/    # Monitoring configurations
├── docs/              # Documentation
├── tools/             # Utility scripts
└── compose.*          # Docker Compose files
```

## Configuration

Key configuration files:
- `.env`: Environment variables (copy from `env.example`)
- `compose.yaml`: Main Docker Compose configuration
- `compose.override.yaml`: Development overrides
- `compose.prod.build.yaml`: Production build configuration

## Security Considerations

Nemesis is designed for offensive security operations:
- Runs privileged containers for system analysis
- Processes potentially malicious files
- Requires proper network isolation
- Use dedicated infrastructure for production deployments

## Contributing

1. Follow the existing Python code style (Ruff + Black)
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure all services pass health checks

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure port 7443 is available
2. **Docker resources**: Nemesis requires significant RAM and CPU
3. **File permissions**: Ensure proper permissions for volume mounts
4. **Environment variables**: Verify all required variables in `.env`

### Useful Commands
```bash
# Check service status
npx nx status nemesis-service

# View service logs
npx nx logs nemesis-service

# Reset environment
npx nx docker:clean nemesis-service
npx nx docker:up nemesis-service
```

## Documentation

- **Original README**: [README.md](README.md)
- **Quickstart Guide**: [docs/quickstart.md](docs/quickstart.md)  
- **Usage Guide**: [docs/usage_guide.md](docs/usage_guide.md)
- **API Documentation**: Available at runtime via web interface
- **Build Documentation**: `npx nx docs:build nemesis-service`

## License

See [LICENSE](LICENSE) for license information.