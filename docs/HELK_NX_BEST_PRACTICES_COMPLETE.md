# HELK Service - NX Best Practices Implementation

## Overview

The HELK service has been reorganized to follow NX workspace best practices, providing a clean, maintainable, and testable structure for the HELK (Hunting ELK) security analysis platform.

## Directory Structure (Post-Reorganization)

```
apps/helk-service/
├── src/                          # Source code (NX convention)
│   ├── main.ts                   # Application entry point
│   ├── app/                      # Business logic layer
│   │   ├── docker.service.ts     # Docker management service
│   │   └── config.service.ts     # Configuration management service
│   └── assets/                   # Static assets
│       ├── docs/                 # Original HELK documentation
│       └── resources/            # HELK resources and papers
├── tests/                        # Test files (NX convention)
│   ├── docker.service.spec.ts    # Docker service tests
│   └── config.service.spec.ts    # Configuration service tests
├── infrastructure/               # Infrastructure files
│   ├── docker/                   # Docker compose files and images
│   │   ├── helk-*/              # Individual service containers
│   │   ├── *.yml                # Docker compose configurations
│   │   └── *.sh                 # Management scripts
│   ├── configs/                  # Configuration templates
│   │   ├── filebeat/
│   │   ├── winlogbeat/
│   │   └── firewalld/
│   └── scripts/                  # Additional utility scripts
├── package.json                  # Node.js package configuration
├── project.json                  # NX project configuration
├── tsconfig.json                 # TypeScript configuration
├── tsconfig.spec.json           # Test TypeScript configuration
├── jest.config.ts               # Jest test configuration
├── .eslintrc.json               # ESLint configuration
└── README.md                     # Service documentation
```

## Key Improvements

### 1. **Separation of Concerns**
- **`src/main.ts`**: CLI entry point and command orchestration
- **`src/app/docker.service.ts`**: Docker container management logic
- **`src/app/config.service.ts`**: Configuration management and validation
- **`tests/`**: Comprehensive unit tests for all services

### 2. **NX Standard Project Configuration**
- **TypeScript Build**: Proper TypeScript compilation with `@nx/js:tsc`
- **Testing**: Jest integration with coverage reporting
- **Linting**: ESLint with TypeScript rules
- **Type Checking**: Separate type-check target for CI/CD

### 3. **Infrastructure Organization**
- **`infrastructure/docker/`**: All Docker-related files
- **`infrastructure/configs/`**: Configuration templates
- **`infrastructure/scripts/`**: Management scripts

### 4. **CLI Interface**
Enhanced command-line interface with proper error handling and TypeScript support.

## Available Commands

### NX Targets (Recommended)

```bash
# Development
npx nx serve helk-service           # Start HELK basic configuration
npx nx serve:full helk-service      # Start HELK full configuration (with alerts)
npx nx build helk-service           # Build TypeScript application
npx nx test helk-service            # Run unit tests
npx nx test:watch helk-service      # Run tests in watch mode
npx nx lint helk-service            # Lint TypeScript code
npx nx type-check helk-service      # Type check without compilation

# Docker Operations
npx nx docker:start helk-service    # Start Docker containers (basic)
npx nx docker:start:full helk-service  # Start Docker containers (full)
npx nx docker:stop helk-service     # Stop all containers
npx nx docker:build helk-service    # Build Docker images
npx nx docker:install helk-service  # First-time installation

# Monitoring
npx nx status helk-service          # Check service status
npx nx logs helk-service            # View service logs
```

### Direct CLI Usage

```bash
cd apps/helk-service

# Using the built CLI
npm run dev start                   # Start basic configuration
npm run dev start:full             # Start full configuration
npm run dev stop                   # Stop services
npm run dev status                 # Check status
npm run dev logs                   # View logs
npm run dev build                  # Build Docker images
npm run dev install                # Install HELK
```

## Service Architecture

### Docker Service (`src/app/docker.service.ts`)
- Manages Docker Compose operations
- Provides service status monitoring
- Handles container lifecycle management
- Supports both basic and full HELK configurations

**Key Methods:**
- `start(config, detached)` - Start HELK services
- `stop()` - Stop all services
- `build(config)` - Build Docker images
- `getStatus(config)` - Get service status
- `getLogs(config, service, lines)` - Retrieve logs

### Configuration Service (`src/app/config.service.ts`)
- Manages HELK configuration
- Validates configuration settings
- Provides Docker environment variables
- Supports custom configuration overrides

**Key Methods:**
- `loadConfig()` - Load and merge configuration
- `saveConfig(config)` - Save configuration to file
- `validateConfig(config)` - Validate configuration
- `getDockerEnv()` - Get environment variables for Docker

## Testing Strategy

### Unit Tests
- **Docker Service Tests**: Mock Docker operations, test service lifecycle
- **Config Service Tests**: Test configuration loading, validation, and merging
- **Coverage Target**: 80%+ code coverage across all services

### Integration Tests (Future)
- End-to-end HELK deployment testing
- Service health check validation
- Cross-service communication testing

## Configuration Management

### Default Configuration
```typescript
{
  elasticsearch: {
    host: 'helk-elasticsearch',
    port: 9200,
    cluster_name: 'helk-cluster',
    heap_size: '2g'
  },
  kibana: {
    host: 'helk-kibana',
    port: 5601,
    elasticsearch_url: 'http://helk-elasticsearch:9200'
  },
  // ... additional services
}
```

### Custom Configuration
Place custom configuration in `infrastructure/configs/helk.config.json`:

```json
{
  "elasticsearch": {
    "heap_size": "4g",
    "port": 9201
  },
  "spark": {
    "worker_memory": "4g",
    "worker_cores": 4
  }
}
```

## Development Workflow

### 1. **Local Development**
```bash
# Install dependencies
npm install

# Run in development mode
npm run dev start

# Run tests
npx nx test helk-service

# Lint code
npx nx lint helk-service
```

### 2. **Building for Production**
```bash
# Build TypeScript
npx nx build helk-service

# Build Docker images
npx nx docker:build helk-service
```

### 3. **CI/CD Integration**
```bash
# Type check
npx nx type-check helk-service

# Run tests with coverage
npx nx test helk-service --coverage

# Lint and format
npx nx lint helk-service
```

## Docker Configurations

### Basic Configuration (`helk-kibana-notebook-analysis-basic.yml`)
- Elasticsearch
- Kibana
- Logstash
- Jupyter Notebooks
- Apache Spark (Master + Worker)

### Full Configuration (`helk-kibana-notebook-analysis-alert-basic.yml`)
- All basic services
- ElastAlert for alerting
- Additional monitoring components

## Security Considerations

### Network Configuration
- Services run on isolated Docker network (10.0.0.0/16)
- Configurable firewall rules via `setup-firewall` command
- Service-to-service communication over internal network

### Access Control
- Jupyter notebooks support token-based authentication
- Kibana can be configured with authentication plugins
- Elasticsearch cluster security can be enabled via configuration

## Performance Tuning

### Resource Allocation
- **Elasticsearch**: Configurable heap size (default: 2g)
- **Spark Workers**: Configurable cores and memory
- **Container Resources**: Adjustable via Docker Compose overrides

### Monitoring
- Service health checks via Docker Compose
- Log aggregation through central logging
- Performance metrics collection (future enhancement)

## Integration with Mental Prosthetic Platform

### Service Discovery
- Registered in NX workspace as `helk-service`
- Tagged with appropriate domain and technology markers
- Integrated with centralized build and deployment pipeline

### Data Flow
- **Input**: Security logs from platform services
- **Processing**: ELK stack with custom Logstash pipelines
- **Analytics**: Jupyter notebooks with Spark processing
- **Output**: Kibana dashboards and alerts

### API Integration (Future)
- REST API for service management
- GraphQL integration for dashboard embedding
- WebSocket support for real-time updates

## Troubleshooting

### Common Issues

1. **Docker Not Running**
   ```bash
   # Check Docker status
   docker info
   
   # Start Docker service
   sudo systemctl start docker
   ```

2. **Port Conflicts**
   ```bash
   # Check for port usage
   npx nx status helk-service
   
   # Modify configuration if needed
   ```

3. **Memory Issues**
   ```bash
   # Reduce Elasticsearch heap size
   # Edit infrastructure/configs/helk.config.json
   {
     "elasticsearch": {
       "heap_size": "1g"
     }
   }
   ```

### Debug Mode
```bash
# Enable verbose Docker output
DEBUG=true npx nx docker:start helk-service

# View real-time logs
npx nx logs helk-service
```

## Future Enhancements

1. **Web API**: REST API for service management
2. **Dashboard Integration**: Embed Kibana in Jane UI
3. **Alert Integration**: Route alerts through platform notification system
4. **Auto-scaling**: Dynamic resource allocation based on load
5. **Backup/Restore**: Automated data backup and recovery
6. **Multi-tenant**: Support for multiple isolated HELK instances

## Migration from Legacy Structure

The reorganization maintains 100% backward compatibility with the original HELK functionality while adding modern development practices:

- ✅ All Docker containers and configurations preserved
- ✅ All management scripts maintained
- ✅ Original documentation and resources available
- ✅ Enhanced with TypeScript services and testing
- ✅ Integrated with NX workspace tooling
- ✅ Ready for platform integration