# Jane Monorepo - AI Coding Agent Instructions

Mental prosthetic platform with 37 integrated executive function tools in NX monorepo.

**Last updated**: 2025-11-28

## 🏗️ Architecture Overview

This is an **EXTREME SCALE** brownfield migration consolidating 37 specialized tools into a hybrid domain-based architecture:

```
apps/
├── core/
│   ├── jane-orchestrator/     # Legacy FastAPI backend (being phased out)
│   ├── jane-ui/               # Next.js 15 + React 19 unified interface
│   └── infrastructure-service/ # Infrastructure domain (12 tools)
├── ai/                        # Specialized LLM servers (Python vLLM)
├── security/                  # Security domain (13 tools)
├── productivity/              # Productivity domain (8 tools)
└── tcg/                       # Trading Card Game domain (4 tools)
```

**Migration Status**: Active transition from `features/` (legacy) → `apps/` (target architecture)
**Key Principle**: 100% business logic preservation across all 37 tools

## ⚡ Essential Workflows

### NX Monorepo Commands

```bash
npx nx serve jane-ui                    # Start main UI (port 4200)
npx nx serve jane-orchestrator          # Start FastAPI backend (port 8000)
npx nx affected:build                   # Build only changed projects
npx nx affected:test                    # Test only affected projects
npx nx graph                            # Visual dependency graph
```

### Domain-Specific Services

```bash
# Security domain
npx nx serve nemesis-service
npx nx serve cyberchef-service
npx nx serve misp-service

# Productivity domain
npx nx serve n8n-service
npx nx serve goose-service
npx nx serve actual-service

# Use make for orchestration
make serve-security                     # All security services
make serve-productivity                 # All productivity services
```

### Python Services (FastAPI backends)

```bash
cd apps/jane-orchestrator && pytest tests/ -v
ruff check apps/jane-orchestrator/src/
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

## 🔧 Code Patterns & Integration

### Service Adapter Pattern

All 37 tools integrate via standardized service adapters:

```python
# libs/service-adapters/base/adapter_base.py
class BaseServiceAdapter(ABC):
    def __init__(self, service_name: str, config: Dict[str, Any]):
        self.service_name = service_name
        self.config = config
        self.health_status = "unknown"

    @abstractmethod
    async def initialize(self) -> bool:
        """Tool-specific initialization with rollback capability"""

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Constitutional requirement for all 37 tools"""
```

### Domain-Specific Performance Requirements

```python
# Performance tiers by domain criticality
DOMAIN_RESPONSE_LIMITS = {
    "security": 1000,      # <1s (threat analysis critical)
    "productivity": 2000,  # <2s (workflow efficiency)
    "tcg": 3000,          # <3s (game analysis complexity)
    "infrastructure": 5000 # <5s (ops tolerance)
}
```

### Cross-Component Communication

- **FastAPI → Next.js**: REST + WebSocket (<250ms latency requirement)
- **Service Adapters**: Standardized interface preserving original business logic
- **MCP Protocol**: Model Context Protocol for AI server integration
- **n8n Workflows**: Central orchestration with AI enhancement

## 🧠 AI Integration Patterns

### Specialized LLM Servers

```bash
# Domain-specific AI servers
apps/ai/cyber-llm-server/      # Security domain AI (vLLM)
apps/ai/mtg-llm-server/        # MTG domain AI (vLLM)
apps/ai/infrastructure-llm-server/  # Infrastructure AI (vLLM)
```

### MCP Server Integration

```typescript
// Features being migrated to apps/
features/chroma-mcp/           # Vector embeddings
features/firecrawl-mcp-server/ # Web scraping
features/n8n-mcp-server/       # Workflow automation
```

## 📁 Migration Strategy (CRITICAL)

**ALWAYS** check migration status before modifying files:

### Migration Decision Matrix

1. **features/** → Legacy code (being migrated to apps/)
2. **apps/** → Target architecture (modify here)
3. **libs/service-adapters/** → Integration layer (preserve business logic)

### Migration Task Protocol

```bash
# BEFORE any migration work, check:
specs/003-brownfield-integration/tasks.md        # Master orchestration
specs/003-brownfield-integration/tasks-individual/  # Detailed migration tasks

# Each tool migration follows:
# 1. Pre-flight checklist ✅
# 2. Business logic preservation validation
# 3. Performance benchmark maintenance
# 4. Post-flight validation ✅
```

## 🎯 Executive Function Accommodations

This platform serves users with ADHD/autism - **critical UX requirements**:

- **UI Response Time**: <200ms (cognitive load reduction)
- **Context Switching**: Unified navigation patterns across all 37 tools
- **Focus Maintenance**: Consistent interface design system
- **WCAG 2.1 AA**: Enhanced focus indicators and accessibility

## 🏛️ Architecture Deep Dive

### Technology Stack

- **Frontend**: Next.js 15 + React 19 + TypeScript (strict mode)
- **Backend**: Python 3.12 + FastAPI (uvicorn server)
- **Database**: PostgreSQL (primary), SQLite (local tools), Redis (sessions)
- **AI**: vLLM servers, Chroma DB vectors, MCP protocol
- **Build**: NX monorepo, pnpm workspaces, Rust (Goose AI)
- **Infrastructure**: Docker Compose, Terraform, Kubernetes ready

### Key Dependencies & Patterns

```json
// package.json - Key frameworks
"@nx/workspace": "^20.x",     # Monorepo management
"next": "15.x",               # React 19 compatibility
"@types/node": "20.x",        # Node.js LTS
"typescript": "~5.6.2"        # Strict typing
```

```python
# Python stack - apps/jane-orchestrator/pyproject.toml
fastapi = "^0.115.0"          # High-performance async API
uvicorn = "^0.32.0"          # ASGI server
pydantic = "^2.9.0"          # Data validation
asyncpg = "^0.29.0"          # PostgreSQL async driver
```

### Service Integration Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   jane-ui       │───▶│  jane-orchestrator │───▶│ service-adapters │
│   (Next.js 15)  │    │    (FastAPI)      │    │   (37 tools)    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AI Servers    │    │   Databases      │    │  External APIs  │
│ (vLLM/Chroma)   │    │ (Postgres/Redis) │    │ (MCP Protocol)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 🛠️ Development Workflows

### Project Setup & Dependencies

```bash
# Fresh setup (run once)
make install                           # Install all deps (Node + Python)
make setup-dev                        # Complete dev environment

# Daily development
pnpm install                          # Node dependencies
cd apps/jane-orchestrator && pip install -e .  # Python dependencies
```

### Testing Strategy

```bash
# Comprehensive testing
make test                             # All tests (NX + Python)
make test-security                    # Domain-specific tests
nx affected:test                      # Only changed projects

# Python-specific
cd apps/jane-orchestrator && pytest tests/ -v --cov=src
cd apps/ai/goose-service && cargo test

# Performance validation (constitutional requirement)
python tests/performance/security-domain-validation.py    # <1s target
python tests/performance/productivity-domain-validation.py # <2s target
```

### Code Quality & Linting

```bash
# TypeScript (strict mode enforced)
npx eslint apps/jane-ui/src/ --ext .ts,.tsx
nx format                             # Prettier formatting

# Python (constitutional standards)
ruff check apps/jane-orchestrator/src/ # Fast linter
black apps/jane-orchestrator/src/     # Code formatting
mypy apps/jane-orchestrator/src/      # Type checking required

# Rust (Goose AI service)
cd apps/ai/goose-service && cargo fmt && cargo clippy
```

## 🔍 Debugging & Troubleshooting

### Service Health Monitoring

```bash
# Check all service status
make status                           # Cross-platform service check
make health-check                     # HTTP health endpoints

# Individual service debugging
npx nx serve jane-ui --verbose        # Frontend debugging
uvicorn src.api.main:app --reload --log-level debug  # Backend debugging
docker-compose logs nemesis-service   # Container logs
```

### Common Integration Issues

1. **Cross-domain API calls**: Check CORS middleware in FastAPI
2. **Service adapter failures**: Verify `BaseServiceAdapter.health_check()`
3. **Performance violations**: Run domain-specific validation scripts
4. **Migration conflicts**: Always check `features/` → `apps/` status first

## 📋 Code Quality Standards

### TypeScript (Constitutional Requirements)

- **Strict mode**: `"strict": true` in tsconfig.json - NO exceptions
- **Type safety**: No `any` types without documented justification
- **Performance**: UI interactions <200ms (executive function critical)

### Python (FastAPI Services)

- **Type hints**: Required for ALL functions (mypy enforcement)
- **Formatting**: `black` + `ruff` (automated in CI/CD)
- **Testing**: 80%+ coverage + integration tests for cross-domain workflows
- **Async patterns**: Use `async`/`await` for I/O operations

### Service Integration Patterns

```python
# Standard service adapter implementation
class CyberChefAdapter(BaseServiceAdapter):
    async def initialize(self) -> bool:
        """Initialize with rollback capability"""

    async def health_check(self) -> Dict[str, Any]:
        """Required for all 37 tools"""

    async def preserve_business_logic(self) -> None:
        """Constitutional requirement - 100% functionality preservation"""
```

## 🚨 Critical Migration Protocols

### Before ANY Code Changes

1. **Check migration status**: Is this in `features/` (legacy) or `apps/` (target)?
2. **Read task documentation**: `specs/003-brownfield-integration/tasks.md`
3. **Verify dependencies**: Run `nx graph` to understand project relationships
4. **Business logic preservation**: Identify core functionality to maintain

### Domain-Specific Performance Targets

- **Security**: <1000ms (threat analysis critical)
- **Productivity**: <2000ms (workflow efficiency)
- **TCG**: <3000ms (game analysis acceptable)
- **Infrastructure**: <5000ms (operations tolerance)
- **WebSocket latency**: <250ms (real-time data sync)

## 📖 Document Handoff Protocol for Migration Tasks

When working with brownfield migration tasks, follow this hierarchical workflow:

### 1. Starting Point: Top-Level Orchestration

**Always begin with**: `specs/003-brownfield-integration/tasks.md`

This is the master orchestration document that coordinates:

- Foundation phases (1-4): Shared infrastructure setup
- Individual project migrations (Phase 5+): Delegated to individual task files
- Integration and polish phases: Final validation

### 2. Detecting Handoff Points

**Look for the `[HANDOFF]` tag** in task descriptions:

```markdown
- [ ] T100 [HANDOFF] Migrate CyberChef
  - **File**: tasks-individual/tasks-cyberchef.md
  - **Entry Condition**: Phase 1-4 complete, security-service foundation ready
  - **Exit Condition**: All tasks complete + validation tests pass
  - **Validation**: pytest tests/security/test_cyberchef_integration.py
  - **Return To**: T101
```

This signals delegation to a child document for detailed implementation.

### 3. Handoff Execution Workflow

When encountering a `[HANDOFF]` task:

**Step 1: Verify Entry Condition**

- Read the entry condition from the handoff task
- Verify all prerequisites are met (e.g., foundation phases complete)
- If NOT met: Complete prerequisites first before proceeding

**Step 2: Open Child Document**

- Navigate to the file specified in the "File:" field
- Review the handoff context and metadata at the top
- Example: `specs/003-brownfield-integration/tasks-individual/tasks-cyberchef.md`

**Step 3: Execute Pre-Flight Checklist**

- Work through the Pre-Flight Checklist ✅ section at the top of child document
- Verify ALL items before starting any tasks
- If any item fails: STOP and return to parent document to resolve

**Step 4: Complete All Child Tasks**

- Execute all tasks in the child document sequentially (unless marked `[P]` for parallel)
- Follow the brownfield migration methodology
- Maintain functional parity with legacy code
- Run validation tests as specified

**Step 5: Execute Post-Flight Checklist**

- Work through the Post-Flight Checklist ✅ section at the bottom
- Verify ALL completion criteria are met
- Run the validation command specified in the handoff task
- Document completion in `migration-validation.md`

**Step 6: Return to Parent**

- Mark the parent `[HANDOFF]` task complete in `tasks.md`
- Proceed to the "Return To" task specified in handoff metadata
- Continue with next task in parent orchestration

### 4. Parallel Handoffs

Tasks marked `[P] [HANDOFF]` can execute in parallel:

```markdown
- [ ] T100 [P] [HANDOFF] Migrate CyberChef
- [ ] T101 [P] [HANDOFF] Migrate Maltrail
- [ ] T102 [P] [HANDOFF] Migrate HELK
```

**Parallel Execution Rules**:

1. Each can start independently (no dependencies between them)
2. Create separate branches: `migration/cyberchef`, `migration/maltrail`, etc.
3. Each must complete fully (all exit conditions met) before merging
4. All parallel tasks must complete before proceeding past that phase

### 5. Completion Criteria

**A task is NOT complete until**:

- ✅ All checkboxes in the child document are marked
- ✅ All validation tests pass
- ✅ Exit conditions verified
- ✅ Completion documented in migration-validation.md
- ✅ Parent handoff task marked complete
- ✅ No regressions introduced

**Never skip**:

- Pre-flight checklists (prevents wasted work on incomplete foundations)
- Post-flight validation (ensures quality before returning)
- Documentation updates (maintains audit trail)

### 6. Error Handling

**If Entry Conditions Fail**:

- STOP child task execution
- Document blocker in migration-validation.md
- Return to parent tasks.md to resolve prerequisites
- Do not proceed until conditions are met

**If Exit Conditions Fail**:

- DO NOT mark parent task complete
- Debug and fix issues in child implementation
- Re-run validation tests
- Only mark complete when all exit criteria pass

**If Validation Tests Fail**:

- Review test failures and fix implementation
- Ensure ground truth tests confirm functional parity
- Re-test until all pass
- Document results before marking complete

### 7. Complete Handoff Protocol Documentation

For full details, see: `specs/003-brownfield-integration/HANDOFF-PROTOCOL.md`

This document includes:

- Complete workflow examples
- State tracking guidance
- Branching strategies for parallel work
- Progress tracking in migration-validation.md
- Quality gates and checkpoints

### 8. Practical Example Flow

```
1. Start: specs/003-brownfield-integration/tasks.md
2. Find: [ ] T100 [HANDOFF] Migrate CyberChef
3. Verify: Entry condition met (Phase 1-4 complete)
4. Open: tasks-individual/tasks-cyberchef.md
5. Check: Pre-Flight Checklist (all ✅)
6. Execute: All tasks T001-T040 in child doc
7. Check: Post-Flight Checklist (all ✅)
8. Validate: pytest tests/security/test_cyberchef_integration.py (pass)
9. Document: Update migration-validation.md
10. Return: Mark T100 complete in tasks.md
11. Continue: Proceed to T101 in tasks.md
```

### 9. Key Principles

**Sequential Foundation** → Complete phases 1-4 before ANY individual migrations
**Parallel Execution** → Multiple projects can migrate simultaneously after foundation
**Quality Gates** → Never skip pre-flight or post-flight validation
**Complete Return** → Only mark parent complete when ALL child work is done
**Continuous Documentation** → Update migration-validation.md throughout

---

## Recent Changes

- 2025-11-09: Document handoff protocol v1.0.0 - Hierarchical task delegation system for brownfield migrations
- 2025-10-26: Constitutional reform v2.0.0 - Separated universal principles from platform-specific requirements
- 2025-10-26: Technology stack confirmation - React/Next.js primary frontend based on evidence-based analysis
- 2025-10-22: Architecture clarification - Modular monolith codebase with optional 3-device deployment, framework-agnostic approach based on business logic needs
- 2025-10-22: Task expansion - Added 26 new tasks for user preferences, domain performance validation, and rollback capabilities (170→196 tasks)
- 2025-10-22: User story enhancement - Added comprehensive testable acceptance criteria for User Stories 3-5 with measurable thresholds
- 2025-10-19: Constitution v1.2.0 - Multi-framework integration strategy, technology choice driven by preservation requirements
- 2025-10-19: Constitution v1.1.0 - Added 37-tool platform scope, executive function accommodations
- 2025-10-18: Initial constitution v1.0.0 - Established core principles, testing standards, performance requirements
<!-- MANUAL ADDITIONS END -->
