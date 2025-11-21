# AI Domain Services

This directory contains all AI and machine learning services within the Mental Prosthetic Platform.

## Performance Target

- **Response Time**: Variable based on model complexity
- **Integration Pattern**: Service adapter with business logic preservation

## Services

### Large Language Model Servers

- **cyber-llm-server** - Specialized AI server for security domain analysis and operations
- **mtg-llm-server** - Specialized AI server for Magic: The Gathering and TCG domain
- **infrastructure-llm-server** - Specialized AI server for infrastructure and DevOps operations

### AI-Powered Services

- **firecrawl-service** - AI-enhanced web scraping and data extraction service
- **goose-service** - AI-powered coding assistant and automation engine (Rust-based)
- **goose-docs** - Documentation and knowledge base for Goose (Docusaurus)
- **goose-ui** - Desktop application for Goose interactions (Electron)
- **goose-temporal-service** - Workflow orchestration service for Goose (Go-based)

## Architecture Patterns

### Service Categories

#### Domain-Specific LLM Servers

Each LLM server is optimized for specific domain expertise:

- **Cyber LLM**: Security analysis, vulnerability assessment, threat detection
- **MTG LLM**: Card interactions, rule analysis, deck optimization
- **Infrastructure LLM**: DevOps workflows, system administration, monitoring

#### Model Management

- Model loading and optimization
- Context management and memory
- Token usage tracking and optimization
- Response quality monitoring

### Integration Patterns

#### Service Routing

```bash
jane-ui → jane-orchestrator → [domain-specific LLM server]
                            ↓
                        response aggregation
```

#### Multi-Model Configuration

- Primary model selection based on query type
- Fallback models for reliability
- Cost optimization through model selection
- Performance monitoring and switching

## Development

### Running Services

```bash
# Individual LLM servers
npx nx serve ai/cyber-llm-server
npx nx serve ai/mtg-llm-server  
npx nx serve ai/infrastructure-llm-server

# All AI services
npx nx run-many --target=serve --projects=tag:domain:ai

# Testing
npx nx run-many --target=test --projects=tag:domain:ai

# Building
npx nx run-many --target=build --projects=tag:domain:ai
```

### Project Tags

All AI services should include:

- `domain:ai` - AI domain identifier
- `scope:backend` - Service type (all LLM servers are backend)
- `type:service` - Project type

### Performance Monitoring

Monitor model performance and resource usage:

```bash
# Performance validation
python tests/performance/ai-domain-validation.py
```

## Model Configuration

### Environment Variables

Each LLM server requires:

- Model endpoints and credentials
- Context window configurations
- Rate limiting parameters
- Fallback model settings

### Resource Management

- GPU allocation and sharing
- Memory management for large models
- CPU optimization for inference
- Network bandwidth optimization

## Service Dependencies

### External Dependencies

- Model hosting services (OpenAI, Anthropic, etc.)
- GPU infrastructure for local models
- Vector databases for embeddings
- Cache systems for response optimization

### Internal Dependencies

- `jane-orchestrator` - Central routing and query classification
- `libs/shared` - Common utilities and types
- `libs/service-adapters` - Integration layer

## Security Considerations

### Data Privacy

- No storage of sensitive queries
- Encrypted communication with model providers
- Audit logging for compliance
- Data sanitization before model queries

### Access Control

- API key management
- Rate limiting per user/domain
- Query filtering and validation
- Model access permissions

## Documentation

Each AI service maintains:

- Model configuration documentation
- API endpoint specifications
- Performance benchmarks
- Troubleshooting guides

## Contributing

When adding new AI services:

1. Follow domain-specific patterns
2. Implement proper error handling
3. Add comprehensive performance tests
4. Document model requirements
5. Include security considerations