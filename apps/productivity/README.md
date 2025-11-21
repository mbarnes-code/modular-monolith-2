# Productivity Domain Services

This directory contains automation, workflow management, and productivity enhancement services.

## Performance Target

- **Response Time**: <2s (Task management workflows)
- **Integration Pattern**: Service adapter with business logic preservation

## Services

### Automation & Workflow

- **n8n-service** - Visual workflow automation platform
- **n8n-workflow-service** - Workflow execution and management

### Development Tools

- **inspector-service** - Code analysis and inspection tools
- **onex-service** - Development productivity utilities
- **onex-service-e2e** - End-to-end tests for OneX service

### Personal Productivity

- **actual-service** - Personal finance and budgeting management
- **mealie-service** - Recipe and meal planning management
- **productivity-service** - General productivity service aggregator

## Architecture Patterns

### Service Categories

#### AI-Powered Automation

- **Goose**: Comprehensive development agent with temporal workflows
- **N8N**: Visual workflow builder and automation platform

#### Development Productivity  

- **Inspector**: Code quality and analysis tools
- **Firecrawl**: Data extraction and web automation
- **OneX**: Developer utilities and enhancement tools

#### Personal Management

- **Actual**: Financial tracking and budgeting
- **Mealie**: Meal planning and recipe management

### Integration Patterns

#### Workflow Orchestration

```bash
jane-ui → jane-orchestrator → productivity-service → [automation tools]
                            ↓
                        workflow-engine
```

#### Data Processing Pipeline

```bash
firecrawl → content extraction → analysis → automation triggers
inspector → code analysis → quality metrics → improvement suggestions
```

## Development

### Running Services

```bash
# Individual services
npx nx serve productivity/goose-service
npx nx serve productivity/n8n-service
npx nx serve productivity/actual-service

# All productivity services
npx nx run-many --target=serve --projects=tag:domain:productivity

# Testing
npx nx run-many --target=test --projects=tag:domain:productivity

# Building  
npx nx run-many --target=build --projects=tag:domain:productivity
```

### Project Tags

All productivity services should include:

- `domain:productivity` - Productivity domain identifier
- `scope:backend` or `scope:frontend` - Service type
- `type:service` or `type:application` - Project type

### Performance Monitoring

Monitor automation and workflow performance:

```bash
# Performance validation
python tests/performance/productivity-domain-validation.py
```

## Automation Capabilities

### Workflow Automation

- Visual workflow design with N8N
- Temporal-based reliable execution
- Error handling and retry mechanisms
- Integration with external APIs and services

### AI-Powered Assistance

- Code generation and refactoring with Goose
- Intelligent task automation
- Natural language workflow creation
- Contextual development assistance

### Data Processing

- Web scraping and content extraction
- Document processing and analysis
- Data transformation and cleaning
- Integration with storage systems

## Service Dependencies

### External Dependencies

- Temporal server for workflow orchestration
- Database services for state management
- External APIs for integrations
- File storage for processed content

### Internal Dependencies

- `jane-orchestrator` - Central routing and task management
- `infrastructure-llm-server` - AI-powered automation
- `libs/shared` - Common utilities and types
- `libs/service-adapters` - Integration layer

## Workflow Management

### Temporal Integration

- Durable workflow execution
- State management and persistence
- Retry policies and error handling
- Monitoring and observability

### Task Orchestration

- Multi-step automation workflows
- Conditional logic and branching
- Parallel execution capabilities
- Human-in-the-loop workflows

## Personal Data Management

### Privacy & Security

- Local-first data storage where possible
- Encrypted sensitive information
- User consent and data control
- Minimal data retention policies

### Data Synchronization

- Cross-device synchronization
- Backup and restore capabilities
- Conflict resolution strategies
- Offline functionality support

## Documentation

Each productivity service maintains:

- Workflow automation guides
- API documentation for integrations
- User guides for personal services
- Troubleshooting and optimization tips

## Contributing

When adding new productivity services:

1. Focus on user workflow optimization
2. Implement robust error handling
3. Add comprehensive automation tests
4. Document integration patterns
5. Prioritize user privacy and control