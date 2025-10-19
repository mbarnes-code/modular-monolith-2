# modular-monolith-2 Development Guidelines

Auto-generated from all feature plans. Last updated: 2025-10-18

## Active Technologies

- TypeScript 5.9.3, Python 3.12, Node.js 20 + Next.js 15.5.4, React 19.2.0, FastAPI 0.119.0, NX 21.6.4, vLLM 0.11.0, Chroma DB (001-mental-prosthetic-platform)

## Project Structure

```
backend/
frontend/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

TypeScript 5.9.3, Python 3.12, Node.js 20: Follow standard conventions

## Recent Changes

- 001-mental-prosthetic-platform: Added TypeScript 5.9.3, Python 3.12, Node.js 20 + Next.js 15.5.4, React 19.2.0, FastAPI 0.119.0, NX 21.6.4, vLLM 0.11.0, Chroma DB

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

- **Frontend**: Multi-framework approach (constitutional evidence-based strategy)
  - **React Preservation**: 8 tools maintain React/Next.js (Actual Budget, Commander Spellbook, Inspector, Nemesis, etc.)
  - **Vue.js Standardization**: 3 tools use Vue.js/Nuxt.js (n8n, IT-Tools, Mealie) + new development
  - **Legacy Support**: 26 tools use vanilla JS/server-side rendering
  - **Integration**: Framework-agnostic shared components via Web Components
- **Backend**: Python 3.12 + FastAPI 0.119.0
- **Database**: PostgreSQL 14+ (primary: 18/37 projects), SQLite (local-first: 5/37 projects), Redis 7+ (caching)
- **AI Integration**: vLLM 0.11.0, Chroma DB (vector embeddings)
- **Build/Dev**: Node.js 20, NX 21.6.4
- **Performance**: Domain tiers - Security <1s, Productivity <2s, MTG <3s, Infrastructure <5s

## Project Structure (Modular Monolith)

```
apps/
├── jane-orchestrator/    # FastAPI backend (37-tool consolidation)
├── jane-ui/             # Vue.js 3 + TypeScript frontend
├── [llm-servers]/       # Existing LLM infrastructure
libs/
├── shared/              # Cross-domain utilities
├── ui/                 # Design system (constitutional requirement)
└── service-adapters/   # 37-tool integration adapters
features/               # SOURCE: 37 tools (to be migrated to apps/)
```

## Commands (Constitutional Stack Only)

cd apps/jane-orchestrator && pytest tests/ -v
cd apps/jane-ui && npm run test
ruff check apps/jane-orchestrator/src/
npx eslint apps/jane-ui/src/ --ext .ts,.vue
docker-compose -f infrastructure/docker/docker-compose.yml up -d

## Code Quality (Constitutional Requirements)

- **TypeScript**: Strict mode enabled, no `any` types without justification
- **Python**: Type hints required, black formatting, ruff linting
- **Testing**: 80%+ unit coverage, integration tests for cross-domain workflows, E2E with Playwright
- **Documentation**: Public APIs require comprehensive documentation with examples
- **Business Logic Preservation**: 100% functionality preservation across all 37 tools

## Performance Requirements (Constitutional Tiers)

- **Security Tools**: <1s response (threat analysis criticality)
- **Productivity Tools**: <2s response (task management workflows)
- **MTG Tools**: <3s response (game analysis complexity)
- **Infrastructure Tools**: <5s response (system operations tolerance)
- **Cross-Tool Sync**: 250ms WebSocket latency (real-time data flow)
- **UI Interactions**: <200ms (ADHD focus maintenance)

## Migration Strategy (Constitutional)

- **Approach**: Big-bang migration (all 37 tools simultaneously) with framework preservation
- **Categories**: A (Complex Algorithms → microservices with existing frameworks), B (Domain Logic → modular with framework preservation), C (Utilities → shared libs, Vue.js for substantial rewrites)
- **Completion Criteria**: features/ directory empty, 100% functionality preserved, React tools maintain React
- **Validation**: Automated testing, feature parity verification, performance benchmarks, framework compatibility

## Recent Changes (Constitutional Updates)

- 2025-10-19: Constitution v1.2.0 - Multi-framework integration strategy, React preservation mandate, evidence-based technology choices
- 2025-10-19: Constitution v1.1.0 - Added 37-tool platform scope, executive function accommodations, Vue.js framework confirmation
- 2025-10-19: Spec refinement - Added NFR section, measurable business logic preservation criteria, constitution alignment
- 2025-10-18: Initial constitution v1.0.0 - Established core principles, testing standards, performance requirements
<!-- MANUAL ADDITIONS END -->
