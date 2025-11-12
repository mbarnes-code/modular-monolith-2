# Core Platform Services

This directory contains the foundational services that orchestrate and manage the entire Jane platform.

## Performance Target

- **Response Time**: <200ms (Executive function support)
- **Integration Pattern**: Central orchestration with modular service coordination

## Services

### Platform Orchestration

- **jane-orchestrator** - Central FastAPI backend coordinating all 37 tools
- **jane-ui** - Primary React/Next.js frontend with TypeScript
- **infrastructure-service** - Infrastructure management and deployment coordination

## Architecture Overview

### Central Orchestration Pattern

```
jane-ui (Frontend) ←→ jane-orchestrator (Backend) ←→ Domain Services
                              ↓
                     infrastructure-service
                              ↓
                        [All Domain Services]
```

### Service Responsibilities

#### Jane Orchestrator

**Purpose**: Central coordination hub for all platform services
**Technology**: Python 3.12 + FastAPI
**Architecture**: Modular monolith with domain-specific service adapters

**Core Functions**:
- **API Layer**: REST endpoints, WebSocket real-time communication, request routing
- **Data Layer**: Models, migrations, database schemas (PostgreSQL/SQLite/Redis)
- **Services Layer**: Business logic, domain services, rollback capabilities
- **AI Layer**: LLM integration, MCP server coordination, intelligent routing
- **Domains Layer**: Security, Productivity, MTG, Infrastructure domain logic

#### Jane UI

**Purpose**: Unified frontend interface with executive function accommodations
**Technology**: React/Next.js + TypeScript
**Architecture**: Design system with cross-framework compatibility

**Core Functions**:
- **Executive Function Support**: <75ms UI interactions, consistent navigation
- **Unified Interface**: Single entry point for all 37 integrated tools
- **Real-time Updates**: WebSocket integration for live data synchronization
- **Accessibility**: WCAG 2.1 AA compliance with enhanced focus indicators

#### Infrastructure Service

**Purpose**: Platform deployment and infrastructure management
**Technology**: Framework-agnostic deployment coordination
**Architecture**: Flexible deployment patterns (monolith or distributed)

**Core Functions**:
- **Deployment Management**: Docker orchestration, service discovery
- **Resource Monitoring**: Performance tracking, health checks
- **Configuration Management**: Environment-based settings, secrets management
- **Scaling Coordination**: Load balancing, service scaling decisions

## Platform Integration

### Domain Coordination

The core platform coordinates across all domains:

```bash
# Security Domain (21 services)
jane-orchestrator/domains/security → apps/security/*

# AI Domain (3 services) 
jane-orchestrator/domains/ai → apps/ai/*

# TCG Domain (6 services)
jane-orchestrator/domains/tcg → apps/tcg/*

# Productivity Domain (13 services)
jane-orchestrator/domains/productivity → apps/productivity/*
```

### Service Adapter Pattern

Each external service integrates through standardized adapters:

```python
# Business logic preservation pattern
class ServiceAdapter:
    def preserve_functionality(self) -> bool
    def provide_rollback(self) -> RollbackCapability  
    def maintain_preferences(self) -> UserPreferences
    def ensure_performance(self) -> PerformanceMetrics
```

## Development

### Running Core Platform

```bash
# Start backend orchestrator
cd apps/jane-orchestrator
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Start frontend UI
npx nx serve jane-ui

# Start infrastructure coordination
npx nx serve infrastructure-service

# Complete platform startup
npm run start:platform
```

### Testing

```bash
# Core platform tests
cd apps/jane-orchestrator && pytest tests/ -v
cd apps/jane-ui && npm run test

# Integration tests
pytest tests/integration/core-platform/
npm run test:e2e

# Performance validation
python tests/performance/core-platform-validation.py
```

### Environment Configuration

```bash
# Development environment
export NODE_ENV=development
export PYTHON_ENV=development
export DATABASE_URL=postgresql://localhost/jane_dev

# Production environment  
export NODE_ENV=production
export PYTHON_ENV=production
export DATABASE_URL=postgresql://prod-server/jane_prod
```

## Core Capabilities

### Executive Function Accommodations

**ADHD-Friendly Design**:
- UI interactions <75ms response time
- Consistent navigation patterns reduce context switching
- Enhanced focus indicators and visual cues
- Unified interface eliminates tool-switching overhead

### Business Logic Preservation

**37-Tool Integration**:
- 100% functionality preservation across all integrated tools
- Tool-specific rollback capabilities for safe experimentation
- Unified user preference system across all services
- Framework-agnostic adapters maintain original tool capabilities

### Performance Management

**Domain-Specific SLAs**:
- Security tools: <1s response (threat analysis criticality)
- Productivity tools: <2s response (workflow management)
- TCG tools: <3s response (game analysis complexity)
- Infrastructure tools: <5s response (system operations)
- Cross-tool sync: 250ms WebSocket latency

### Data Management

**Multi-Database Strategy**:
- **PostgreSQL**: Primary relational data, user preferences, domain coordination
- **SQLite**: Local-first tools, offline functionality, personal data
- **Redis**: Caching, session management, real-time data synchronization

## Architecture Principles

### Modular Monolith Benefits

1. **Single Deployment**: Simplified ops with optional service extraction
2. **Shared Libraries**: Common utilities and business logic
3. **Coordinated Transactions**: Cross-domain data consistency
4. **Unified Monitoring**: Single observability pipeline
5. **Flexible Scaling**: Extract services when needed without rewrite

### Service Boundaries

**Layer-Based Separation**:
- **API Layer**: External interfaces, routing, authentication
- **Data Layer**: Persistence, migrations, schema management  
- **Services Layer**: Business logic, domain coordination, rollback
- **AI Layer**: LLM integration, intelligent routing, MCP servers

### Migration Strategy

**Constitutional Approach**:
- Preserve 100% functionality during migrations
- Evidence-based technology choices
- Comprehensive testing at each migration step
- User preference continuity across tool changes

## Monitoring & Observability

### Health Checks

```bash
# Platform health
curl http://localhost:8000/health
curl http://localhost:3000/api/health

# Domain service health
curl http://localhost:8000/api/domains/security/health
curl http://localhost:8000/api/domains/productivity/health
```

### Performance Monitoring

```python
# Domain-specific performance validation
python tests/performance/security-domain-validation.py     # <1s
python tests/performance/productivity-domain-validation.py # <2s  
python tests/performance/tcg-domain-validation.py         # <3s
python tests/performance/infrastructure-domain-validation.py # <5s
```

### Metrics & Analytics

- Request/response latency by domain
- User interaction patterns and bottlenecks
- Cross-tool workflow efficiency
- Executive function accommodation effectiveness

## Security & Privacy

### Authentication & Authorization

- Unified authentication across all 37 tools
- Role-based access control per domain
- API key management for external integrations
- Session management with Redis backing

### Data Privacy

- User data sovereignty and control
- Local-first storage for personal information
- Encrypted sensitive data at rest and in transit
- GDPR compliance with data export/deletion

## Contributing to Core Platform

### Development Guidelines

1. **Modular Design**: Keep domain boundaries clean and well-defined
2. **Performance First**: Every change must meet domain SLAs
3. **User Experience**: Prioritize executive function accommodations
4. **Business Logic**: Preserve 100% tool functionality during changes
5. **Documentation**: Update architecture diagrams and integration guides

### Quality Standards

- **TypeScript**: Strict mode, no `any` without justification
- **Python**: Type hints required, black formatting, ruff linting  
- **Testing**: 80%+ unit coverage, integration tests, E2E with Playwright
- **Performance**: Automated domain-specific validation required

### Code Review Focus

- Cross-domain impact assessment
- Performance regression prevention
- User experience consistency
- Business logic preservation validation
- Documentation completeness

## Roadmap

### Phase 1: Foundation (Complete)
- ✅ Core platform architecture established
- ✅ Domain-based service organization
- ✅ Basic orchestration and UI integration

### Phase 2: Integration (In Progress)  
- 🔄 Complete 37-tool service adapter implementation
- 🔄 Unified user preference system
- 🔄 Cross-domain workflow orchestration

### Phase 3: Optimization
- Performance tuning and caching strategies
- Advanced AI integration and intelligent routing
- Enhanced executive function accommodations
- Comprehensive monitoring and observability

### Phase 4: Scale
- Optional microservice extraction patterns
- Multi-deployment topology support
- Advanced workflow orchestration
- Community plugin architecture