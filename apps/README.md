# Jane Platform - Domain-Based Service Organization

This directory contains all services organized by functional domain for the Jane Mental Prosthetic Platform.

## Domain Architecture

The Jane platform consolidates **37 executive function tools** into a unified interface, organized across 5 functional domains:

### 🔒 [Security Domain](./security/README.md) (21 services)
**Target**: <1s response time (threat analysis criticality)

Cybersecurity tools, penetration testing, incident management, and threat analysis:
- **Core Security**: dispatch-service, nemesis-*, misp-service, helk-service
- **Penetration Testing**: blackarch-service, brute-ratel-service, hexstrike-service
- **Analysis Tools**: cyberchef-service, yara-x-service, apiscout-service
- **Forensics**: software-forensic-kit-service, meterpreter-service

### 🤖 [AI Domain](./ai/README.md) (3 services)  
**Target**: Variable by use case

Specialized LLM servers for domain-specific AI assistance:
- **cyber-llm-server** - Security and threat analysis AI
- **mtg-llm-server** - Trading card game rule and strategy AI
- **infrastructure-llm-server** - DevOps and system administration AI

### 🃏 [TCG Domain](./tcg/README.md) (6 services)
**Target**: <3s response time (game analysis complexity)

Magic: The Gathering and trading card game tools:
- **Commander Tools**: commander-spellbook-backend, commander-spellbook-site
- **Game Analysis**: mtg-service, mtg-commander-map-service
- **Scripting**: mtg-scripts, mtg-scripts-e2e

### ⚡ [Productivity Domain](./productivity/README.md) (13 services)
**Target**: <2s response time (workflow management)

Automation, workflow management, and productivity enhancement:
- **AI Automation**: goose-service, goose-docs, goose-ui, goose-temporal-service
- **Workflow Tools**: n8n-service, n8n-workflow-service
- **Dev Tools**: inspector-service, firecrawl-service, onex-service
- **Personal**: actual-service, mealie-service, productivity-service

### 🏗️ [Core Platform](./core/README.md) (3 services)
**Target**: <200ms response time (executive function support)

Foundation services that orchestrate the entire platform:
- **jane-orchestrator** - Central FastAPI backend (37-tool coordination)
- **jane-ui** - Primary React/Next.js frontend with executive function accommodations
- **infrastructure-service** - Infrastructure management and deployment

## Executive Function Accommodations

The Jane platform is specifically designed to support users with executive function challenges (ADHD, autism, etc.):

### ⚡ Performance Requirements
- **UI Interactions**: <75ms (ADHD-friendly responsiveness)
- **Context Switching**: Unified navigation reduces cognitive load
- **Visual Consistency**: WCAG 2.1 AA with enhanced focus indicators
- **Real-time Sync**: 250ms WebSocket latency for immediate feedback

### 🧠 Cognitive Load Reduction
- **Single Interface**: Access all 37 tools through one consistent UI
- **Unified Preferences**: Single preference system across all tools
- **Persistent Context**: Maintain work state across tool switches
- **Smart Defaults**: AI-powered configuration recommendations

## Technology Stack

### Frontend Architecture
- **Primary**: React/Next.js + TypeScript (evidence-based selection)
- **Framework Strategy**: Framework-agnostic service adapters
- **Business Logic**: 100% functionality preservation across all tools
- **Integration**: Web Components for cross-framework compatibility

### Backend Architecture  
- **Core**: Python 3.12 + FastAPI (modular monolith)
- **Databases**: PostgreSQL (primary), SQLite (local-first), Redis (caching/sessions)
- **AI Integration**: vLLM, Chroma DB (vector embeddings), MCP protocol
- **Build System**: Node.js 20, NX workspace for monorepo management

### Deployment Strategy
- **Architecture**: Modular monolith with flexible deployment
- **Options**: Single server deployment or distributed microservices
- **Scaling**: Extract services when needed without architectural rewrite

## Development Workflow

### Quick Start

```bash
# Install all dependencies
make install

# Start core platform
npx nx serve jane-ui          # Frontend (port 3000)
npx nx run jane-orchestrator:serve  # Backend (port 8000)

# Start domain services
npx nx run-many --target=serve --projects=tag:domain:security
npx nx run-many --target=serve --projects=tag:domain:productivity
```

### Testing by Domain

```bash
# Domain-specific testing
pytest tests/performance/security-domain-validation.py      # <1s validation
pytest tests/performance/productivity-domain-validation.py  # <2s validation  
pytest tests/performance/tcg-domain-validation.py          # <3s validation
pytest tests/performance/infrastructure-domain-validation.py # <5s validation

# Cross-domain integration tests
pytest tests/integration/cross-domain-workflows.py
npm run test:e2e
```

### Build and Deploy

```bash
# Build all services
npx nx run-many --target=build --all

# Docker deployment
docker-compose -f infrastructure/docker/docker-compose.yml up -d

# Domain-specific builds
npx nx run-many --target=build --projects=tag:domain:security
npx nx run-many --target=build --projects=tag:domain:productivity
```

## Service Integration Patterns

### Central Orchestration

```
jane-ui ←→ jane-orchestrator ←→ Domain Services
              ↓
        service-adapters
              ↓  
        [37 integrated tools]
```

### Business Logic Preservation

All integrations use the **Service Adapter Pattern** to ensure:
- **100% Functionality**: No features lost during integration
- **User Preferences**: Unified settings across all tools
- **Rollback Capabilities**: Safe experimentation with instant revert
- **Performance SLAs**: Domain-specific response time guarantees

### Data Flow Architecture

```bash
# Real-time synchronization
WebSocket (250ms) ←→ jane-orchestrator ←→ Domain Services
                            ↓
                      Redis Cache
                            ↓
                   PostgreSQL/SQLite
```

## Quality Standards

### Code Quality
- **TypeScript**: Strict mode, no `any` without justification
- **Python**: Type hints required, black formatting, ruff linting
- **Testing**: 80%+ unit coverage, integration tests, E2E with Playwright
- **Documentation**: Public APIs require comprehensive examples

### Performance Validation
- **Automated Monitoring**: Domain-specific performance benchmarks
- **User Experience**: Executive function accommodation metrics
- **Integration Testing**: Cross-tool workflow validation
- **Rollback Testing**: Ensure safe experimentation capabilities

## Project Structure

```
apps/
├── core/                    # Platform orchestration (3 services)
│   ├── jane-orchestrator/   # Central FastAPI backend
│   ├── jane-ui/            # Primary React frontend  
│   └── infrastructure-service/ # Deployment coordination
├── security/               # Security tools (21 services)
│   ├── dispatch-service/   # Incident management
│   ├── nemesis-*/          # Threat hunting platform
│   ├── cyberchef-service/ # Data analysis toolkit
│   └── ...
├── productivity/           # Automation & workflow (13 services)
│   ├── goose-*/           # AI development agent
│   ├── n8n-*/             # Visual workflow automation
│   ├── actual-service/    # Personal finance
│   └── ...
├── ai/                    # LLM servers (3 services)
│   ├── cyber-llm-server/  # Security AI
│   ├── mtg-llm-server/    # Gaming AI
│   └── infrastructure-llm-server/ # DevOps AI
└── tcg/                   # Trading card games (6 services)
    ├── commander-spellbook-*/ # MTG combo analysis
    ├── mtg-scripts/       # Game automation
    └── ...
```

## Migration Status

### Brownfield Integration Strategy

Following the **Constitutional Migration Approach**:
- ✅ **Phase 1-4**: Foundation and shared infrastructure complete
- 🔄 **Phase 5+**: Individual service migrations using handoff protocol
- 📋 **Validation**: Each migration requires 100% functionality preservation
- 🔄 **Active**: Comprehensive documentation and domain organization

### Document Handoff Protocol

Complex migrations follow hierarchical task delegation:
1. **Master Orchestration**: `specs/003-brownfield-integration/tasks.md`
2. **Individual Migrations**: `tasks-individual/tasks-[service].md`  
3. **Quality Gates**: Pre-flight and post-flight validation required
4. **Completion Criteria**: All exit conditions must pass before return

## Contributing

### Domain-Specific Contributions

1. **Identify Domain**: Determine which domain your contribution affects
2. **Review Domain README**: Understand architecture patterns and constraints
3. **Follow Quality Standards**: Meet domain-specific performance targets
4. **Preserve Functionality**: Maintain 100% business logic preservation
5. **Test Comprehensively**: Include unit, integration, and performance tests

### Cross-Domain Changes

For changes affecting multiple domains:
1. **Central Coordination**: Start with `jane-orchestrator` impact assessment
2. **Performance Validation**: Run all domain-specific performance tests
3. **User Experience**: Verify executive function accommodations remain intact
4. **Integration Testing**: Test cross-domain workflow preservation

### Documentation Requirements

- **Service Documentation**: Each service maintains comprehensive API docs
- **Domain Architecture**: Domain-level patterns and integration guides
- **User Guides**: End-user documentation for tool functionality
- **Migration Guides**: Brownfield integration documentation

## Support & Community

### Getting Help

- **Technical Issues**: Check domain-specific README troubleshooting sections
- **Integration Questions**: Review service adapter documentation
- **Performance Problems**: Run domain-specific validation scripts
- **User Experience**: Consult executive function accommodation guides

### Roadmap

The Jane platform follows a **196-task implementation plan**:
- **Phases 1-2**: Setup and foundational infrastructure (20 tasks) ✅
- **Phases 3-7**: User story implementation (69 tasks) 🔄
- **Phases 8-13**: Domain migration with business logic preservation (87 tasks) 🔄  
- **Phase 14**: Production polish and performance validation (20 tasks) ⏳

## Constitutional Principles

The Jane platform operates under **Constitutional Requirements**:

1. **Business Logic Preservation**: 100% functionality maintained across all integrations
2. **Executive Function Support**: UI/UX designed for cognitive accessibility
3. **Performance Guarantees**: Domain-specific SLAs with automated validation
4. **User Sovereignty**: Complete control over personal data and preferences
5. **Framework Agnostic**: Technology choices based on preservation requirements
6. **Evidence-Based Decisions**: All architectural choices supported by analysis
7. **Rollback Capabilities**: Safe experimentation with instant revert options

---

*The Jane platform transforms executive function challenges into systematic advantages through intelligent tool consolidation and cognitive accessibility design.*