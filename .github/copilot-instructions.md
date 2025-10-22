# modular-monolith-2 Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-10-22

## Project Structure

```
backend/
frontend/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

 Follow standard conventions

## Recent Changes


<!-- MANUAL ADDITIONS START -->

Auto-generated from constitutional requirements and feature plans. Last updated: 2025-10-19

## CONSTITUTIONAL PLATFORM SCOPE (NON-NEGOTIABLE)

**Mental Prosthetic Platform**: Exactly 37 executive function tools across 4 domains

- **Security Domain**: 13 tools (MISP, HELK, SecurityOnion, Maltrail, YARA-X, CyberChef, Nemesis, etc.)
- **Productivity Domain**: 8 tools (n8n, Mealie, Dispatch, Actual Budget, Firecrawl, Goose, IT-Tools, Inspector)
- **MTG Domain**: 4 tools (Commander Spellbook, MTG Commander Map, MTG Scripting Toolkit, card analysis)
- **Infrastructure Domain**: 12 tools (Kong, Ghostwriter, KasmVNC, MCP servers, workflow automation, etc.)

**Executive Function Requirements**: ADHD/Autism accommodations are constitutional requirements

- UI interactions <200ms (focus maintenance)
- 37→1 interface consolidation (95% context switching reduction)
- Consistent navigation across all tools
- WCAG 2.1 AA compliance with focus indicators

## Active Technologies (Constitutional Stack)

- **Frontend**: Technology-agnostic approach (framework choice driven by business logic preservation needs)
  - **Primary Approach**: React/Next.js + TypeScript for unified interface
  - **Legacy Support**: Preserve existing frameworks where essential for business logic integrity
  - **Integration**: Framework-agnostic shared components via Web Components and service adapters
- **Backend**: Python 3.12 + FastAPI (latest) for modular monolith architecture
- **Database**: PostgreSQL (latest) primary, SQLite (local-first tools), Redis (latest) caching/sessions
- **AI Integration**: vLLM (latest), Chroma DB (vector embeddings), MCP protocol framework
- **Build/Dev**: Node.js 20, NX workspace for monorepo management
- **Deployment**: Modular monolith codebase provisioned for flexible deployment (single server or 3-device distribution)

## Project Structure (Modular Monolith with Layer-Based Service Boundaries)

```
apps/
├── jane-orchestrator/    # FastAPI backend (37-tool consolidation)
│   └── src/
│       ├── api/          # API Layer - REST endpoints, WebSocket, routing
│       ├── data/         # Data Layer - models, migrations, schemas  
│       ├── services/     # Business Logic Layer - domain services, rollback
│       ├── ai/           # AI Layer - LLM integration, MCP servers
│       └── domains/      # Domain-specific business logic (Security, Productivity, MTG, Infrastructure)
├── jane-ui/             # Frontend application (React/Next.js + TypeScript)
├── cyber-llm-server/    # Specialized AI server for security domain
├── mtg-llm-server/      # Specialized AI server for MTG domain  
├── code-llm-server/     # Specialized AI server for development tools
libs/
├── shared/              # Cross-domain utilities and common services
├── ui/                 # Design system with executive function accommodations
└── service-adapters/   # 37-tool integration adapters with business logic preservation
features/               # SOURCE: 37 tools (to be migrated to apps/ - target: empty directory)
```

## Commands (Constitutional Stack Only)

cd apps/jane-orchestrator && pytest tests/ -v
cd apps/jane-ui && npm run test
ruff check apps/jane-orchestrator/src/
npx eslint apps/jane-ui/src/ --ext .ts,.tsx
docker-compose -f infrastructure/docker/docker-compose.yml up -d

## Domain-Specific Performance Validation

# Validate Security Domain (<1s response time)
python tests/performance/security-domain-validation.py

# Validate Productivity Domain (<2s response time)  
python tests/performance/productivity-domain-validation.py

# Validate MTG Domain (<3s response time)
python tests/performance/mtg-domain-validation.py

# Validate Infrastructure Domain (<5s response time)
python tests/performance/infrastructure-domain-validation.py

## Code Quality (Constitutional Requirements)

- **TypeScript**: Strict mode enabled, no `any` types without justification
- **Python**: Type hints required for all functions, black formatting, ruff linting
- **Testing**: 80%+ unit coverage, integration tests for cross-domain workflows, E2E with Playwright
- **Documentation**: Public APIs require comprehensive documentation with examples
- **Business Logic Preservation**: 100% functionality preservation across all 37 tools
- **User Preferences**: Unified user preference system with ADHD/autism accommodations
- **Rollback Capabilities**: Tool-specific and system-wide rollback infrastructure required
- **Performance Validation**: Automated domain-specific performance monitoring

## Performance Requirements (Constitutional Tiers)

- **Security Tools**: <1s response (threat analysis criticality)
- **Productivity Tools**: <2s response (task management workflows)
- **MTG Tools**: <3s response (game analysis complexity)
- **Infrastructure Tools**: <5s response (system operations tolerance)
- **Cross-Tool Sync**: 250ms WebSocket latency (real-time data flow)
- **UI Interactions**: <200ms (ADHD focus maintenance)

## Migration Strategy (Constitutional)

- **Approach**: Big-bang migration (all 37 tools simultaneously) with framework preservation
- **Categories**: A (Complex Algorithms → microservices when needed), B (Domain Logic → modular with framework preservation), C (Utilities → shared libs, technology choice based on preservation requirements)
- **Completion Criteria**: features/ directory empty, 100% functionality preserved, evidence-based technology choices
- **Validation**: Automated testing, feature parity verification, performance benchmarks, framework compatibility

## Implementation Status (196 Tasks Total)

- **Phase 1-2**: Setup and foundational infrastructure (20 tasks)
- **Phase 3-7**: User story implementation with testable acceptance criteria (69 tasks)
- **Phase 8-13**: Comprehensive domain migration with business logic preservation (87 tasks)  
- **Phase 14**: Production polish and performance validation (20 tasks)
- **Key Features Added**: User preferences (FR-008), domain performance validation (NFR-006), rollback capabilities (FR-013)

## Recent Changes (Constitutional Updates)

- 2025-10-22: Architecture clarification - Modular monolith codebase with optional 3-device deployment, framework-agnostic approach based on business logic needs
- 2025-10-22: Task expansion - Added 26 new tasks for user preferences, domain performance validation, and rollback capabilities (170→196 tasks)
- 2025-10-22: User story enhancement - Added comprehensive testable acceptance criteria for User Stories 3-5 with measurable thresholds
- 2025-10-19: Constitution v1.2.0 - Multi-framework integration strategy, technology choice driven by preservation requirements
- 2025-10-19: Constitution v1.1.0 - Added 37-tool platform scope, executive function accommodations
- 2025-10-18: Initial constitution v1.0.0 - Established core principles, testing standards, performance requirements
<!-- MANUAL ADDITIONS END -->
