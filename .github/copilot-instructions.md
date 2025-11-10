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

Auto-generated from specifications and constitutional requirements. Last updated: 2025-10-26

## MENTAL PROSTHETIC PLATFORM SCOPE (SPECIFICATION-BASED)

**Platform Objective**: 37 executive function tools consolidated into unified interface

- **Security Domain**: 13 tools (MISP, HELK, SecurityOnion, Maltrail, YARA-X, CyberChef, Nemesis, etc.)
- **Productivity Domain**: 8 tools (n8n, Mealie, Dispatch, Actual Budget, Firecrawl, Goose, IT-Tools, Inspector)
- **MTG Domain**: 4 tools (Commander Spellbook, MTG Commander Map, MTG Scripting Toolkit, card analysis)
- **Infrastructure Domain**: 12 tools (Kong, Ghostwriter, KasmVNC, MCP servers, workflow automation, etc.)

**Executive Function Accommodations**: User experience requirements for focus maintenance

- UI interactions <75ms (enhanced ADHD-friendly responsiveness based on test analysis)
- Unified navigation patterns (context switching reduction)
- Consistent interface design across all integrated tools
- WCAG 2.1 AA compliance with enhanced focus indicators

## Active Technologies (Evidence-Based Selection)

- **Frontend**: React/Next.js + TypeScript (data-driven decision based on technology stack analysis)
  - **Framework Strategy**: Primary React/Next.js with framework-agnostic service adapters
  - **Business Logic Preservation**: 100% functionality preservation across all 37 tools
  - **Integration Approach**: Web Components and service adapters for cross-framework compatibility
- **Backend**: Python 3.12 + FastAPI for modular monolith architecture
- **Database**: PostgreSQL (primary), SQLite (local-first tools), Redis (caching/sessions)
- **AI Integration**: vLLM, Chroma DB (vector embeddings), MCP protocol framework
- **Build/Dev**: Node.js 20, NX workspace for monorepo management
- **Deployment**: Modular monolith with flexible deployment options (single server or distributed)

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

## Code Quality (Constitutional Standards)

- **TypeScript**: Strict mode enabled, no `any` types without justification
- **Python**: Type hints required for all functions, black formatting, ruff linting
- **Testing**: 80%+ unit coverage, integration tests for cross-domain workflows, E2E with Playwright
- **Documentation**: Public APIs require comprehensive documentation with examples
- **Business Logic Preservation**: 100% functionality preservation across all 37 tools
- **User Preferences**: Unified user preference system with executive function accommodations
- **Rollback Capabilities**: Tool-specific and system-wide rollback infrastructure required
- **Performance Validation**: Automated domain-specific performance monitoring

## Performance Requirements (Domain-Based Tiers)

- **Security Tools**: <1s response (threat analysis criticality)
- **Productivity Tools**: <2s response (task management workflows)
- **TCG Tools**: <3s response (game analysis complexity)
- **Infrastructure Tools**: <5s response (system operations tolerance)
- **Cross-Tool Sync**: 250ms WebSocket latency (real-time data flow)
- **UI Interactions**: <200ms (executive function support)

## Migration Strategy (Constitutional)

 **Categories**: A (Complex Algorithms → microservices when needed), B (Domain Logic → modular with framework preservation), C (Utilities → shared libs, technology choice based on preservation requirements)
- **Completion Criteria**: features/ directory empty, 100% functionality preserved, evidence-based technology choices
- **Validation**: Automated testing, feature parity verification, performance benchmarks, framework compatibility

## Implementation Status (196 Tasks Total)

- **Phase 1-2**: Setup and foundational infrastructure (20 tasks)
- **Phase 3-7**: User story implementation with testable acceptance criteria (69 tasks)
- **Phase 8-13**: Comprehensive domain migration with business logic preservation (87 tasks)
- **Phase 14**: Production polish and performance validation (20 tasks)
- **Key Features Added**: User preferences (FR-008), domain performance validation (NFR-006), rollback capabilities (FR-013)

## Document Handoff Protocol for Migration Tasks

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
