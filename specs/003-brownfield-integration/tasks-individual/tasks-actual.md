---
description: "Actual Budget - Local-first personal finance tool with CRDT sync"
parent_task: "../tasks.md#T106"
parent_phase: "Phase 3d: Productivity Migrations"
return_to: "../tasks.md#T107"
domain: "productivity"
target_service: "apps/productivity-service/src/"
legacy_path: "features/actual"
estimated_hours: 60
---

# Tasks: MIGRATION - Actual Budget

**⬆️ PARENT TASK**: [`tasks.md#T106`](../tasks.md#T106)  
**⬇️ RETURN TO**: [`tasks.md#T107`](../tasks.md#T107)

---

## Handoff Context

**Called From**: `tasks.md` Phase X, Task TXXX  
**Entry Condition**: Productivity service foundation ready (Phase 1-4 complete)  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark TXXX complete in parent `tasks.md`, proceed to next task

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**DO NOT START** until ALL conditions are verified:

- [ ] **Foundation Ready**: Phase 1-4 in parent tasks.md marked complete
- [ ] **Service Skeleton**: `apps/productivity-service/src/` directory exists
- [ ] **Shared Libraries**: `libs/shared/`, `libs/service-adapters/` directories exist
- [ ] **Legacy Code Access**: `features/actual/` accessible with monorepo structure
- [ ] **Analysis Document**: `modular-analysis-repo-main/reports/actual-analysis.md` reviewed
- [ ] **Technology Context**: TypeScript, React, SQLite, CRDT sync architecture understood
- [ ] **Critical Algorithms Identified**:
  - [ ] Spreadsheet engine: `packages/loot-core/src/server/sheet.ts` (~1000 LOC)
  - [ ] CRDT sync: `packages/crdt/` (~2000 LOC)
  - [ ] Transaction import: `packages/loot-core/src/server/importers/` (~800 LOC)
- [ ] **Python Environment**: Configured for productivity-service (pytest available)
- [ ] **Node Environment**: npm/npx available for TypeScript compilation
- [ ] **Database Setup**: SQLite driver available, migration tools ready
- [ ] **Git Branch**: On `002-mental-prosthetic-refinement` or feature branch
- [ ] **Testing Infrastructure**: Ground truth test framework available (Section 6.1 of analysis)

**ENTRY CONDITION**: `T105` complete (productivity-service foundation ready)

---

**Input (Spec)**: Design documents from `/specs/[###-feature-name]/` 
**Input (Legacy)**: Legacy codebase path [e.g., /features/MISP/] 
**Prerequisites**: plan.md (required), spec.md (required), **project_analysis_report.md (MANDATORY)**, research.md, data-model.md, contracts/

**Project Analysis Integration**: This task template MUST reference specific sections from project_analysis_report.md:
- Section 2 (Data Architecture) - for data model migration tasks
- Section 3 (API Architecture) - for endpoint and authentication migration
- Section 4 (Business Logic) - for critical algorithm preservation
- Section 5 (External Integrations) - for third-party service continuity
- Section 8 (Performance Characteristics) - for baseline preservation
- Section 11 (Domain Knowledge) - for business rule preservation

**Tests**: Tests are MANDATORY for all migration tasks. The "Ground Truth" test (testing the original code) must be written first to establish functional baselines.

**Organization**: Tasks are grouped by Legacy Feature AND cross-referenced with Project Analysis sections to ensure 1:1 functional parity and comprehensive coverage.

## Format: [ID] [P?] [Feature] [Analysis: Section.#] [Logic: <legacy_file::function>] Description
- [P]: Can run in parallel
- [Feature]: Which legacy feature this task belongs to (e.g., F1: Publishing)
- [Analysis]: Reference to project_analysis_report.md section (e.g., Section.2.1, Section.4.1)
- [Logic]: The exact legacy code being replaced. This is not optional.

## Path Conventions
- **New Project**: [e.g., apps/PROJECT/src/] at repository root
- **Legacy Project**: [e.g., features/MISP/app/Model/]
- **Analysis Report**: project_analysis_report.md sections for validation
- Paths shown below assume single project - adjust based on plan.md structure

## Migration Methodology: Brownfield Asset Relocation

**Core Principle**: Preserve 100% functional parity while modernizing architecture.

**Validation Strategy**: 
1. Ground Truth Tests → Establish current behavior baseline
2. Analysis Cross-Reference → Validate against documented behavior  
3. Incremental Migration → Port one feature at a time with validation
4. Integration Testing → Ensure new implementation matches baseline
5. Performance Validation → Maintain or improve baseline metrics

## Phase 1: Analysis Validation & Environment Setup

**Objective**: Validate analysis completeness and prepare migration environment

### Tasks

- [ ] **T001** [Analysis] Verify actual-analysis.md completeness against source
  - **Analysis**: Section 1 (Overview) - validate technology stack inventory
  - **Legacy**: `features/actual/package.json` - verify all dependencies documented
  - **Validation**: Cross-reference package.json with Section 1.2 dependency list
  - **Output**: Document gaps in `analysis-gaps.md`

- [ ] **T002** [Analysis] Validate critical algorithm identification
  - **Analysis**: Section 4.1 (Critical Algorithms) - verify 3 algorithms exist
  - **Legacy**:
    - `packages/loot-core/src/server/sheet.ts` (Spreadsheet engine)
    - `packages/crdt/` (CRDT sync)
    - `packages/loot-core/src/server/importers/` (Transaction import)
  - **Validation**: Line count verification (1000/2000/800 LOC estimates)
  - **Output**: Update analysis if LOC counts differ >20%

- [ ] **T003** [Analysis] Validate data model completeness
  - **Analysis**: Section 2 (Data Architecture) - 4 core models documented
  - **Legacy**: `packages/loot-core/src/server/db/` - schema definitions
  - **Validation**: Compare analysis Section 2.1 against actual schema files
  - **Output**: List missing tables/fields in analysis-gaps.md

- [ ] **T004** [Environment] Create productivity-service SQLite adapter
  - **Target**: `apps/productivity-service/src/data/adapters/sqlite_adapter.py`
  - **Analysis**: Section 7.2 (Database Strategy) - SQLite performance patterns
  - **Requirements**:
    - In-memory option for testing
    - WAL mode for production
    - <10ms query target
  - **Validation**: pytest test_sqlite_adapter.py

- [ ] **T005** [Environment] Setup ground truth test infrastructure
  - **Target**: `apps/productivity-service/tests/ground_truth/actual/`
  - **Analysis**: Section 6.1 (Testing Strategy) - behavior capture approach
  - **Legacy**: `features/actual/packages/loot-core/src/mocks/` - test fixtures
  - **Requirements**:
    - Capture budget calculations
    - Capture transaction categorization
    - Capture CRDT merge outcomes
  - **Validation**: Run 3 sample ground truth tests against legacy

- [ ] **T006** [Environment] Create TypeScript-Python interop layer
  - **Target**: `libs/shared/typescript-interop/`
  - **Analysis**: Section 5.2 (Technology Bridge) - TS→Python migration strategy
  - **Requirements**:
    - JSON schema validation
    - Type mapping (TS types → Pydantic models)
    - Error translation
  - **Validation**: Round-trip test (TS data → Python → TS)

**Checkpoint**: ALL analysis gaps documented, environment ready for migration

---

## Phase 2: Data Layer Migration

**Objective**: Migrate SQLite schemas and data models to productivity-service

### Tasks

- [ ] **T007** [Data] Migrate Account model
  - **Analysis**: Section 2.1.1 (Account Model) - core entity documentation
  - **Legacy**: `packages/loot-core/src/server/db/` - accounts table schema
  - **Target**: `apps/productivity-service/src/data/models/account.py`
  - **Preservation**:
    - Account types (checking, savings, credit, investment)
    - Balance tracking fields
    - Closed/archived status
  - **Validation**: Ground truth test - create account, verify fields match legacy

- [ ] **T008** [Data] Migrate Transaction model
  - **Analysis**: Section 2.1.2 (Transaction Model) - transaction architecture
  - **Legacy**: `packages/loot-core/src/server/db/` - transactions table
  - **Target**: `apps/productivity-service/src/data/models/transaction.py`
  - **Preservation**:
    - Split transaction support
    - Transfer detection logic
    - Reconciliation status
  - **Validation**: Ground truth test - create split transaction, verify math

- [ ] **T009** [Data] Migrate Category model
  - **Analysis**: Section 2.1.3 (Category Model) - hierarchical structure
  - **Legacy**: `packages/loot-core/src/server/db/` - categories table
  - **Target**: `apps/productivity-service/src/data/models/category.py`
  - **Preservation**:
    - Parent/child hierarchy
    - Hidden categories
    - Group associations
  - **Validation**: Ground truth test - create category tree, verify traversal

- [ ] **T010** [Data] Migrate Budget model
  - **Analysis**: Section 2.1.4 (Budget Model) - monthly budget structure
  - **Legacy**: `packages/loot-core/src/server/db/` - budget tables
  - **Target**: `apps/productivity-service/src/data/models/budget.py`
  - **Preservation**:
    - Category-month budgeted amounts
    - Rollover calculations
    - Goal tracking
  - **Validation**: Ground truth test - budget $500, overspend, verify rollover

- [ ] **T011** [P] [Data] Migrate Payee model
  - **Analysis**: Section 2 (Data Architecture) - payee/merchant tracking
  - **Legacy**: `packages/loot-core/src/server/db/` - payees table
  - **Target**: `apps/productivity-service/src/data/models/payee.py`
  - **Validation**: Ground truth test - create payee, link to transaction

- [ ] **T012** [P] [Data] Migrate Schedule model
  - **Analysis**: Section 2 (Data Architecture) - recurring transactions
  - **Legacy**: `packages/loot-core/src/server/schedules/` - schedule logic
  - **Target**: `apps/productivity-service/src/data/models/schedule.py`
  - **Validation**: Ground truth test - create monthly schedule, verify generation

- [ ] **T013** [Data] Create migration scripts for schema evolution
  - **Target**: `apps/productivity-service/src/data/migrations/`
  - **Analysis**: Section 7.1 (Migration Strategy) - zero-downtime requirements
  - **Requirements**:
    - Alembic setup for schema versioning
    - Initial schema from legacy db
    - Rollback capability
  - **Validation**: Apply migration, rollback, verify clean state

**Checkpoint**: All 6 data models migrated, ground truth tests passing

---

## Phase 3: Domain Service Layer

**Objective**: Create domain services with business logic boundaries

### Tasks

- [ ] **T014** [Domain] Create AccountService
  - **Target**: `apps/productivity-service/src/services/account_service.py`
  - **Analysis**: Section 3.1 (Service Architecture) - domain boundaries
  - **Legacy**: `packages/loot-core/src/server/accounts/` - account operations
  - **Preservation**:
    - Balance calculation logic
    - Account closing workflows
    - Transfer detection
  - **Validation**: Ground truth test - close account, verify balance freeze

- [ ] **T015** [Domain] Create TransactionService
  - **Target**: `apps/productivity-service/src/services/transaction_service.py`
  - **Analysis**: Section 3.1 (Service Architecture) - transaction workflows
  - **Legacy**: `packages/loot-core/src/server/transactions/` - transaction operations
  - **Preservation**:
    - Split transaction creation
    - Categorization rules
    - Reconciliation logic
  - **Validation**: Ground truth test - split $100 3 ways, verify math

- [ ] **T016** [Domain] Create BudgetService
  - **Target**: `apps/productivity-service/src/services/budget_service.py`
  - **Analysis**: Section 3.1 (Service Architecture) - budget calculations
  - **Legacy**: `packages/loot-core/src/server/budget/` - budget logic
  - **Preservation**:
    - Month-to-month rollover
    - Goal progress tracking
    - Budget vs actual calculations
  - **Validation**: Ground truth test - budget $500, spend $600, verify next month

- [ ] **T017** [P] [Domain] Create CategoryService
  - **Target**: `apps/productivity-service/src/services/category_service.py`
  - **Legacy**: `packages/loot-core/src/server/categories/` - category operations
  - **Validation**: Ground truth test - move category to new parent, verify hierarchy

- [ ] **T018** [P] [Domain] Create ScheduleService
  - **Target**: `apps/productivity-service/src/services/schedule_service.py`
  - **Legacy**: `packages/loot-core/src/server/schedules/` - recurring logic
  - **Validation**: Ground truth test - skip one occurrence, verify next date

**Checkpoint**: All domain services created, business logic encapsulated

---

## Phase 4: Critical Algorithm Migration (SPREADSHEET ENGINE)

**Objective**: Migrate 1000 LOC spreadsheet calculation engine with 100% fidelity

### Tasks

- [ ] **T019** [CRITICAL] Analyze spreadsheet dependency graph
  - **Analysis**: Section 4.1.1 (Spreadsheet Engine) - calculation architecture
  - **Legacy**: `packages/loot-core/src/server/sheet.ts` - complete file review
  - **Requirements**:
    - Map all cell dependencies
    - Identify circular reference handling
    - Document calculation order
  - **Output**: `spreadsheet-dependency-graph.md` with full topology

- [ ] **T020** [CRITICAL] Migrate spreadsheet cell types
  - **Target**: `apps/productivity-service/src/algorithms/spreadsheet/cell.py`
  - **Legacy**: `packages/loot-core/src/server/sheet.ts` - cell type definitions
  - **Preservation**:
    - Formula cells
    - Static value cells
    - Reference cells
    - Dynamic cells
  - **Validation**: Ground truth test - create all 4 cell types, verify behavior

- [ ] **T021** [CRITICAL] Migrate calculation engine core
  - **Target**: `apps/productivity-service/src/algorithms/spreadsheet/engine.py`
  - **Legacy**: `packages/loot-core/src/server/sheet.ts` - calculation loop
  - **Preservation**:
    - Topological sort for dependency order
    - Lazy evaluation strategy
    - Circular dependency detection
  - **Validation**: Ground truth test - complex budget formula, verify result matches

- [ ] **T022** [CRITICAL] Migrate budget-specific formulas
  - **Target**: `apps/productivity-service/src/algorithms/spreadsheet/budget_formulas.py`
  - **Legacy**: `packages/loot-core/src/server/budget/` - budget calculation functions
  - **Preservation**:
    - `available()` - funds available to budget
    - `budgeted()` - total budgeted amount
    - `spent()` - actual spending
    - `balance()` - remaining balance
  - **Validation**: Ground truth test - budget scenario with all 4 formulas

- [ ] **T023** [CRITICAL] Migrate rollover calculations
  - **Target**: `apps/productivity-service/src/algorithms/spreadsheet/rollover.py`
  - **Legacy**: `packages/loot-core/src/server/budget/` - rollover logic
  - **Preservation**:
    - Overspending rollover (credit card mode)
    - Positive balance rollover (savings mode)
    - Goal-based rollover
  - **Validation**: Ground truth test - 3 scenarios, verify next month balances

- [ ] **T024** [CRITICAL] Performance validation - <10ms calculation target
  - **Analysis**: Section 8.1 (Performance Requirements) - local operation targets
  - **Requirements**:
    - 100-cell budget recalculation <10ms
    - 1000-transaction categorization <50ms
    - Memory usage <50MB for typical dataset
  - **Validation**: Performance benchmark against legacy timings

**Checkpoint**: Spreadsheet engine 100% functional, performance validated

---

## Phase 5: Critical Algorithm Migration (CRDT SYNC)

**Objective**: Migrate 2000 LOC CRDT synchronization with conflict resolution

### Tasks

- [ ] **T025** [CRITICAL] Analyze CRDT architecture
  - **Analysis**: Section 4.1.2 (CRDT Sync) - distributed data structure
  - **Legacy**: `packages/crdt/` - complete package review
  - **Requirements**:
    - Identify CRDT type (LWW, OR-Set, etc.)
    - Map conflict resolution strategy
    - Document sync protocol
  - **Output**: `crdt-architecture.md` with full design

- [ ] **T026** [CRITICAL] Migrate CRDT core data structures
  - **Target**: `libs/shared/sync/crdt/core.py`
  - **Legacy**: `packages/crdt/src/crdt.ts` - CRDT implementation
  - **Preservation**:
    - Vector clock tracking
    - Tombstone handling for deletes
    - Merge function logic
  - **Validation**: Ground truth test - concurrent edits, verify merge outcome

- [ ] **T027** [CRITICAL] Migrate sync protocol
  - **Target**: `libs/shared/sync/protocol.py`
  - **Legacy**: `packages/crdt/src/sync.ts` - synchronization logic
  - **Preservation**:
    - Incremental sync (only changed data)
    - Conflict detection
    - Resolution strategies
  - **Validation**: Ground truth test - 2 clients, concurrent budget changes, verify sync

- [ ] **T028** [CRITICAL] Migrate encryption layer
  - **Analysis**: Section 9 (Security Considerations) - E2E encryption
  - **Legacy**: `packages/crdt/src/encryption.ts` - crypto implementation
  - **Preservation**:
    - End-to-end encryption algorithm
    - Key derivation from password
    - Encrypted sync messages
  - **Validation**: Ground truth test - encrypt/decrypt sync payload, verify integrity

- [ ] **T029** [CRITICAL] Create sync server adapter
  - **Target**: `libs/service-adapters/actual-sync/sync_adapter.py`
  - **Legacy**: `packages/sync-server/` - server-side sync logic
  - **Preservation**:
    - File-based storage format
    - Sync request handling
    - Conflict resolution on server
  - **Validation**: Ground truth test - 2 clients via server, verify convergence

- [ ] **T030** [CRITICAL] Performance validation - <500ms sync target
  - **Analysis**: Section 8.1 (Performance Requirements) - sync latency
  - **Requirements**:
    - Initial sync <2s for typical dataset (500 transactions)
    - Incremental sync <500ms for 10 changes
    - Conflict resolution <100ms
  - **Validation**: Performance benchmark against legacy sync times

**Checkpoint**: CRDT sync 100% functional, encryption preserved, performance validated

---

## Phase 6: Critical Algorithm Migration (TRANSACTION IMPORT)

**Objective**: Migrate 800 LOC transaction import with rule engine

### Tasks

- [ ] **T031** [CRITICAL] Analyze import file format support
  - **Analysis**: Section 4.1.3 (Transaction Import) - supported formats
  - **Legacy**: `packages/loot-core/src/server/importers/` - parser implementations
  - **Requirements**:
    - List all supported formats (OFX, QFX, CSV, etc.)
    - Document parser strategies per format
    - Identify format-specific edge cases
  - **Output**: `import-formats.md` with parser architecture

- [ ] **T032** [CRITICAL] Migrate CSV parser
  - **Target**: `apps/productivity-service/src/algorithms/import/csv_parser.py`
  - **Legacy**: `packages/loot-core/src/server/importers/parse-csv.ts`
  - **Preservation**:
    - Column mapping detection
    - Date format parsing
    - Amount normalization (handle negatives)
  - **Validation**: Ground truth test - parse 3 CSV formats, verify transaction extraction

- [ ] **T033** [CRITICAL] Migrate OFX/QFX parser
  - **Target**: `apps/productivity-service/src/algorithms/import/ofx_parser.py`
  - **Legacy**: `packages/loot-core/src/server/importers/parse-ofx.ts`
  - **Preservation**:
    - XML parsing logic
    - Transaction type mapping
    - Balance reconciliation
  - **Validation**: Ground truth test - parse OFX file, verify account balance

- [ ] **T034** [CRITICAL] Migrate categorization rule engine
  - **Target**: `apps/productivity-service/src/algorithms/import/rule_engine.py`
  - **Legacy**: `packages/loot-core/src/server/rules/` - rule matching logic
  - **Preservation**:
    - Payee pattern matching
    - Amount-based rules
    - Rule priority ordering
  - **Validation**: Ground truth test - import 10 transactions, verify auto-categorization

- [ ] **T035** [CRITICAL] Migrate duplicate detection
  - **Target**: `apps/productivity-service/src/algorithms/import/duplicate_detection.py`
  - **Legacy**: `packages/loot-core/src/server/importers/` - duplicate matching
  - **Preservation**:
    - Fuzzy date matching (±2 days)
    - Amount matching (exact or ±$0.01)
    - Payee similarity
  - **Validation**: Ground truth test - import same file twice, verify 0 duplicates

- [ ] **T036** [CRITICAL] Performance validation - <100ms per transaction
  - **Analysis**: Section 8.1 (Performance Requirements) - import speed
  - **Requirements**:
    - Parse 100 transactions <1s
    - Categorize with rules <10ms per transaction
    - Duplicate detection <50ms per transaction
  - **Validation**: Performance benchmark - 1000 transaction file import

**Checkpoint**: Import system 100% functional, all formats supported, performance validated

---

## Phase 7: API Layer & Integration

**Objective**: Create FastAPI endpoints and integrate with jane-orchestrator

### Tasks

- [ ] **T037** [API] Create budget API endpoints
  - **Target**: `apps/productivity-service/src/api/routes/budget.py`
  - **Analysis**: Section 5.1 (API Design) - RESTful budget operations
  - **Requirements**:
    - GET /budgets/{month} - retrieve budget for month
    - PUT /budgets/{month}/{category} - update budgeted amount
    - GET /budgets/{month}/summary - rollover + totals
  - **Validation**: Integration test - API call → service → database

- [ ] **T038** [API] Create transaction API endpoints
  - **Target**: `apps/productivity-service/src/api/routes/transactions.py`
  - **Requirements**:
    - POST /transactions - create transaction
    - PUT /transactions/{id} - update transaction
    - POST /transactions/{id}/split - create split
    - GET /transactions?account={id} - query transactions
  - **Validation**: Integration test - create split transaction via API

- [ ] **T039** [API] Create account API endpoints
  - **Target**: `apps/productivity-service/src/api/routes/accounts.py`
  - **Requirements**:
    - GET /accounts - list all accounts
    - POST /accounts - create account
    - PUT /accounts/{id}/close - close account
  - **Validation**: Integration test - close account via API, verify balance freeze

- [ ] **T040** [API] Create import API endpoints
  - **Target**: `apps/productivity-service/src/api/routes/import.py`
  - **Requirements**:
    - POST /import/analyze - preview import results
    - POST /import/execute - commit import
    - GET /import/rules - list categorization rules
  - **Validation**: Integration test - upload CSV, preview, execute import

- [ ] **T041** [API] Create sync API endpoints
  - **Target**: `apps/productivity-service/src/api/routes/sync.py`
  - **Analysis**: Section 4.1.2 (CRDT Sync) - sync protocol requirements
  - **Requirements**:
    - POST /sync/push - client pushes changes
    - GET /sync/pull - client pulls changes
    - POST /sync/reset - force full sync
  - **Validation**: Integration test - 2 clients sync via API

- [ ] **T042** [Integration] Connect to jane-orchestrator
  - **Target**: `apps/jane-orchestrator/src/services/actual_integration.py`
  - **Requirements**:
    - Register Actual Budget in tool registry
    - Create unified navigation entry
    - Map Actual Budget domain to productivity context
  - **Validation**: E2E test - launch jane-ui, navigate to Actual Budget

- [ ] **T043** [Integration] Setup WebSocket for real-time sync
  - **Target**: `apps/productivity-service/src/api/websocket/sync_handler.py`
  - **Analysis**: Section 8.2 (Real-time Requirements) - <250ms sync latency
  - **Requirements**:
    - WebSocket endpoint for sync events
    - Broadcast changes to connected clients
    - Handle client reconnection
  - **Validation**: Integration test - 2 clients, change budget, verify <250ms propagation

**Checkpoint**: All APIs functional, integrated with orchestrator, real-time sync working

---

## Phase 8: UI Migration & Frontend Integration

**Objective**: Migrate React UI to jane-ui with design system compliance

### Tasks

- [ ] **T044** [UI] Create Actual Budget module in jane-ui
  - **Target**: `apps/jane-ui/src/modules/actual-budget/`
  - **Analysis**: Section 5.3 (UI Architecture) - component structure
  - **Legacy**: `packages/desktop-client/src/components/` - React components
  - **Requirements**:
    - Module entry point
    - Route configuration
    - State management setup (Redux or Context)
  - **Validation**: E2E test - navigate to /actual-budget route

- [ ] **T045** [UI] Migrate budget view components
  - **Target**: `apps/jane-ui/src/modules/actual-budget/components/budget/`
  - **Legacy**: `packages/desktop-client/src/components/budget/` - budget UI
  - **Preservation**:
    - Month navigation
    - Category tree display
    - Inline budget editing
  - **Validation**: E2E test - edit budget amount, verify spreadsheet recalculation

- [ ] **T046** [UI] Migrate transaction view components
  - **Target**: `apps/jane-ui/src/modules/actual-budget/components/transactions/`
  - **Legacy**: `packages/desktop-client/src/components/transactions/` - transaction list
  - **Preservation**:
    - Transaction filtering
    - Split transaction UI
    - Reconciliation workflow
  - **Validation**: E2E test - create split transaction, verify display

- [ ] **T047** [UI] Migrate account view components
  - **Target**: `apps/jane-ui/src/modules/actual-budget/components/accounts/`
  - **Legacy**: `packages/desktop-client/src/components/accounts/` - account management
  - **Validation**: E2E test - create account, verify in account list

- [ ] **T048** [UI] Apply design system compliance
  - **Analysis**: Copilot Instructions - <75ms UI interactions, WCAG 2.1 AA
  - **Target**: All Actual Budget components
  - **Requirements**:
    - Use libs/ui/ design system components
    - Enhanced focus indicators (ADHD accommodation)
    - Consistent navigation patterns
  - **Validation**: Accessibility audit + performance profiling

- [ ] **T049** [UI] Integrate sync status indicators
  - **Target**: `apps/jane-ui/src/modules/actual-budget/components/sync-status/`
  - **Requirements**:
    - Real-time sync status display
    - Conflict resolution UI
    - Offline mode indicator
  - **Validation**: E2E test - go offline, make changes, reconnect, verify sync

- [ ] **T050** [UI] Performance optimization - <75ms interactions
  - **Analysis**: Copilot Instructions - executive function accommodations
  - **Requirements**:
    - Virtual scrolling for large transaction lists
    - Debounced budget editing
    - Optimistic UI updates
  - **Validation**: Performance benchmark - 1000 transactions, scroll lag <75ms

**Checkpoint**: UI fully migrated, design system compliant, performance validated

---

## Phase 9: Testing, Documentation & Completion

**Objective**: Comprehensive testing and production readiness

### Tasks

- [ ] **T051** [Test] Run full ground truth test suite
  - **Target**: `apps/productivity-service/tests/ground_truth/actual/`
  - **Requirements**:
    - 80%+ coverage of critical paths
    - All 3 critical algorithms validated
    - Performance benchmarks passing
  - **Validation**: pytest coverage report + performance results

- [ ] **T052** [Test] Execute cross-browser E2E tests
  - **Target**: `tests/e2e/actual-budget/`
  - **Requirements**:
    - Chrome, Firefox, Safari compatibility
    - Mobile responsive layout
    - Accessibility compliance (WCAG 2.1 AA)
  - **Validation**: Playwright test results

- [ ] **T053** [Test] Perform migration acceptance testing
  - **Analysis**: Section 6.2 (Acceptance Criteria) - functional parity
  - **Requirements**:
    - Import legacy Actual Budget file
    - Verify all data migrated correctly
    - Confirm calculations match legacy
  - **Validation**: User acceptance test with real budget file

- [ ] **T054** [Docs] Create user migration guide
  - **Target**: `docs/migrations/actual-budget-user-guide.md`
  - **Requirements**:
    - Export from legacy Actual Budget
    - Import to new platform
    - Feature mapping (old → new UI)
  - **Validation**: Technical writer review

- [ ] **T055** [Docs] Create API documentation
  - **Target**: `docs/api/productivity-service/actual-budget.md`
  - **Requirements**:
    - OpenAPI spec generation
    - Example requests/responses
    - Error code reference
  - **Validation**: API docs auto-generated from FastAPI

- [ ] **T056** [Completion] Update parent task status
  - **Action**: Mark T106 complete in ../tasks.md
  - **Requirements**:
    - All 56 tasks complete
    - All validation passing
    - Documentation published
  - **Validation**: Post-flight checklist below

**Checkpoint**: Migration complete, ready for production deployment

---

## Phase 10: Styling & Design System Migration

**Objective**: Migrate Emotion CSS-in-JS and theme system for UI consistency

### Tasks

- [ ] **T057** [Styling] Migrate Emotion CSS-in-JS configuration
  - **Target**: `libs/ui/styling/emotion-config.ts`
  - **Legacy**: `packages/desktop-client/package.json` - @emotion/css dependency
  - **Requirements**:
    - Emotion CSS configuration
    - CSS-in-JS utilities
    - Style composition helpers
  - **Validation**: Import test - create styled component, verify styling

- [ ] **T058** [Styling] Migrate theme system
  - **Target**: `libs/ui/theme/`
  - **Legacy**: `packages/component-library/src/theme.ts`
  - **Preservation**:
    - Light/dark theme definitions
    - Theme switching logic
    - Theme context provider
  - **Validation**: E2E test - toggle theme, verify UI updates

- [ ] **T059** [Styling] Migrate design tokens
  - **Target**: `libs/ui/tokens/`
  - **Legacy**: `packages/component-library/src/tokens.ts`
  - **Preservation**:
    - Color palette
    - Spacing scale
    - Typography tokens
    - Border radius, shadows
  - **Validation**: Visual regression test - compare token usage

- [ ] **T060** [Styling] Migrate font loading strategy
  - **Target**: `apps/jane-ui/src/assets/fonts/`
  - **Legacy**: `packages/desktop-client/src/fonts.scss`
  - **Preservation**:
    - Inter UI font family
    - Font weight variants
    - Font loading optimization
  - **Validation**: Performance test - font load <500ms

**Checkpoint**: Styling system migrated, theme working, visual consistency maintained

---

## Phase 11: State Management Migration

**Objective**: Migrate Redux store and state management patterns

### Tasks

- [ ] **T061** [State] Migrate Redux store configuration
  - **Target**: `apps/jane-ui/src/store/`
  - **Legacy**: `packages/desktop-client/src/redux/` - Redux Toolkit setup
  - **Requirements**:
    - Redux Toolkit configuration
    - Store creation with middleware
    - DevTools integration
  - **Validation**: Store test - dispatch action, verify state update

- [ ] **T062** [State] Migrate budget state slice
  - **Target**: `apps/jane-ui/src/store/slices/budgetSlice.ts`
  - **Legacy**: Redux state for budget data
  - **Preservation**:
    - Budget state structure
    - Budget reducers
    - Budget selectors
  - **Validation**: Unit test - budget actions, verify state changes

- [ ] **T063** [State] Migrate transaction state slice
  - **Target**: `apps/jane-ui/src/store/slices/transactionSlice.ts`
  - **Legacy**: Redux state for transactions
  - **Validation**: Unit test - transaction filtering, selection

- [ ] **T064** [P] [State] Migrate modal state slice
  - **Target**: `apps/jane-ui/src/store/slices/modalSlice.ts`
  - **Legacy**: `packages/desktop-client/src/modals/modalsSlice.ts`
  - **Validation**: Unit test - modal open/close actions

- [ ] **T065** [P] [State] Migrate preferences state slice
  - **Target**: `apps/jane-ui/src/store/slices/prefsSlice.ts`
  - **Legacy**: `packages/desktop-client/src/prefs/prefsSlice.ts`
  - **Validation**: Unit test - preference updates persist

**Checkpoint**: Redux store migrated, all state slices functional

---

## Phase 12: Advanced Features Migration

**Objective**: Migrate reports, undo/redo, notes, and tags features

### Tasks

- [ ] **T066** [CRITICAL] Migrate undo/redo system
  - **Target**: `apps/productivity-service/src/services/undo_service.py`
  - **Legacy**: `packages/loot-core/src/server/undo.ts` (~270 LOC)
  - **Preservation**:
    - Undo history stack (20 operations)
    - Redo functionality
    - Undo grouping by operation type
  - **Validation**: Ground truth test - make changes, undo, redo, verify state

- [ ] **T067** [Feature] Migrate reports engine
  - **Target**: `apps/productivity-service/src/services/reports_service.py`
  - **Legacy**: `packages/loot-core/src/server/reports/app.ts`
  - **Requirements**:
    - Net worth calculation
    - Spending reports by category
    - Cash flow analysis
  - **Validation**: Ground truth test - generate report, compare with legacy

- [ ] **T068** [Feature] Migrate notes system
  - **Target**: 
    - `apps/productivity-service/src/data/models/note.py` (data)
    - `apps/productivity-service/src/services/note_service.py` (logic)
  - **Legacy**: `packages/loot-core/src/server/notes/app.ts`
  - **Requirements**:
    - Notes data model
    - Notes CRUD API
    - Notes attached to transactions/budgets
  - **Validation**: Ground truth test - create note, attach to transaction

- [ ] **T069** [Feature] Migrate tags system
  - **Target**: 
    - `apps/productivity-service/src/data/models/tag.py` (data)
    - `apps/productivity-service/src/services/tag_service.py` (logic)
  - **Legacy**: `packages/loot-core/src/server/tags/app.ts`
  - **Requirements**:
    - Tags data model
    - Tag CRUD API
    - Tag filtering and search
  - **Validation**: Ground truth test - tag transaction, filter by tag

- [ ] **T070** [Feature] Migrate budget templates/goals system
  - **Target**: `apps/productivity-service/src/algorithms/budget/templates.py`
  - **Legacy**: `packages/loot-core/src/server/budget/category-template-context.ts`
  - **Preservation**:
    - Template types (percentage, average, target)
    - Goal tracking
    - Template validation logic
  - **Validation**: Ground truth test - create template, apply to budget

**Checkpoint**: Advanced features migrated, undo/redo functional, reports working

---

## Phase 13: Bank Integration Migration

**Objective**: Migrate SimpleFIN and GoCardless bank sync integrations

### Tasks

- [ ] **T071** [Integration] Migrate SimpleFIN connection management
  - **Target**: `apps/productivity-service/src/integrations/simplefin/`
  - **Analysis**: Section 5.1 (SimpleFIN Integration)
  - **Legacy**: SimpleFIN sync logic in loot-core
  - **Requirements**:
    - SimpleFIN API client
    - Account connection workflow
    - Transaction fetch logic
  - **Validation**: Integration test - connect account, fetch transactions

- [ ] **T072** [Integration] Migrate GoCardless connection management
  - **Target**: `apps/productivity-service/src/integrations/gocardless/`
  - **Analysis**: Section 5.1 (GoCardless Integration)
  - **Legacy**: `packages/desktop-client/src/gocardless.ts`
  - **Requirements**:
    - GoCardless OAuth flow
    - Open Banking API client
    - PSD2 compliance handling
  - **Validation**: Integration test - OAuth flow, consent management

- [ ] **T073** [Integration] Migrate bank sync error handling
  - **Target**: `apps/productivity-service/src/integrations/errors.py`
  - **Legacy**: `packages/loot-core/src/server/errors.ts` - BankSyncError class
  - **Preservation**:
    - Connection timeout handling
    - Auth failure retry logic
    - Rate limit handling
  - **Validation**: Error test - simulate failures, verify recovery

- [ ] **T074** [UI] Migrate bank connection UI
  - **Target**: `apps/jane-ui/src/modules/actual-budget/components/bank-sync/`
  - **Legacy**: Bank connection components
  - **Requirements**:
    - Connection wizard
    - Account selection
    - Sync status display
  - **Validation**: E2E test - connect bank account via UI

**Checkpoint**: Bank integrations functional, SimpleFIN and GoCardless working

---

## Phase 14: Cross-Cutting UI Features

**Objective**: Migrate modals, preferences, i18n, error handling, and shortcuts

### Tasks

- [ ] **T075** [UI] Migrate modal management system
  - **Target**: `apps/jane-ui/src/components/modal-manager/`
  - **Legacy**: Redux modal state + React Modal
  - **Dependencies**: react-modal (from package.json)
  - **Requirements**:
    - Modal routing
    - Modal stacking
    - Modal state management
  - **Validation**: E2E test - open nested modals, close in order

- [ ] **T076** [Feature] Migrate preferences/settings system
  - **Target**: 
    - `apps/productivity-service/src/data/models/preference.py` (backend)
    - `apps/jane-ui/src/modules/actual-budget/components/settings/` (frontend)
  - **Legacy**: `packages/loot-core/src/server/prefs.ts`
  - **Preservation**:
    - User preferences schema
    - Setting categories
    - Preference sync
  - **Validation**: Ground truth test - update setting, verify persistence

- [ ] **T077** [Feature] Migrate internationalization (i18n)
  - **Target**: `apps/jane-ui/src/i18n/`
  - **Legacy**: `packages/desktop-client/src/i18n.ts`
  - **Dependencies**: i18next, react-i18next
  - **Requirements**:
    - i18next configuration
    - Translation loading
    - Language switching
  - **Validation**: E2E test - switch language, verify UI updates

- [ ] **T078** [Infrastructure] Migrate error handling system
  - **Target**: 
    - `apps/productivity-service/src/errors/` (backend)
    - `apps/jane-ui/src/components/ErrorBoundary.tsx` (frontend)
  - **Legacy**: `packages/loot-core/src/server/errors.ts`
  - **Preservation**:
    - Custom error classes (ValidationError, TransactionError, etc.)
    - Error boundaries
    - Error notification system
  - **Validation**: Error test - trigger errors, verify handling

- [ ] **T079** [UI] Migrate keyboard shortcuts system
  - **Target**: `apps/jane-ui/src/hooks/useKeyboardShortcuts.ts`
  - **Legacy**: react-hotkeys-hook integration
  - **Dependencies**: react-hotkeys-hook
  - **Requirements**:
    - Shortcut configuration
    - Shortcut handlers
    - Shortcut help overlay
  - **Validation**: E2E test - trigger shortcuts, verify actions

- [ ] **T080** [P] [UI] Migrate privacy filter
  - **Target**: `apps/jane-ui/src/components/PrivacyFilter.tsx`
  - **Legacy**: `packages/desktop-client/src/components/PrivacyFilter.tsx`
  - **Validation**: E2E test - enable privacy mode, verify data hidden

**Checkpoint**: Cross-cutting features migrated, preferences working, i18n functional

---

## Phase 15: Additional UI Components

**Objective**: Migrate charts, drag-drop, and other UI enhancements

### Tasks

- [ ] **T081** [P] [UI] Migrate chart components
  - **Target**: `apps/jane-ui/src/components/charts/`
  - **Legacy**: Recharts integration
  - **Dependencies**: recharts
  - **Validation**: E2E test - render budget chart, verify data

- [ ] **T082** [P] [UI] Migrate drag & drop system
  - **Target**: `apps/jane-ui/src/hooks/useDragDrop.ts`
  - **Legacy**: React DnD integration
  - **Dependencies**: react-dnd, react-dnd-html5-backend
  - **Validation**: E2E test - drag category, verify reorder

**Checkpoint**: UI enhancements migrated, charts and drag-drop working

---

## Post-Flight Checklist ✅

**DO NOT mark parent task complete** until ALL conditions are verified:

- [ ] **All 82 Tasks Complete**: Every task T001-T082 marked done
- [ ] **Critical Algorithms Validated**:
  - [ ] Spreadsheet engine: Ground truth tests passing, <10ms performance
  - [ ] CRDT sync: Ground truth tests passing, <500ms sync latency
  - [ ] Transaction import: Ground truth tests passing, <100ms per transaction
- [ ] **Data Model Migration**: All 6 models (Account, Transaction, Category, Budget, Payee, Schedule) + Notes + Tags migrated
- [ ] **Domain Services**: All services functional with ground truth validation
- [ ] **API Layer**: All 5 core route sets + reports + notes + tags tested
- [ ] **UI Migration**: All components migrated, design system compliant, <75ms interaction target
- [ ] **Styling System**: Emotion CSS-in-JS configured, theme system working, design tokens applied
- [ ] **State Management**: Redux store migrated, all slices functional
- [ ] **Advanced Features**:
  - [ ] Undo/redo system functional
  - [ ] Reports engine working
  - [ ] Notes and tags operational
  - [ ] Budget templates/goals working
- [ ] **Bank Integrations**:
  - [ ] SimpleFIN connection tested
  - [ ] GoCardless integration tested
  - [ ] Error handling verified
- [ ] **Cross-Cutting Features**:
  - [ ] Modals system functional
  - [ ] Preferences/settings working
  - [ ] i18n language switching tested
  - [ ] Error handling and boundaries working
  - [ ] Keyboard shortcuts functional
- [ ] **Testing Coverage**: 80%+ unit coverage, E2E tests passing, ground truth suite complete
- [ ] **Performance Validation**:
  - [ ] Spreadsheet calculations <10ms
  - [ ] CRDT sync <500ms
  - [ ] Import processing <100ms per transaction
  - [ ] UI interactions <75ms
  - [ ] WebSocket latency <250ms
  - [ ] Font loading <500ms
- [ ] **Documentation Complete**:
  - [ ] User migration guide published
  - [ ] API documentation generated (OpenAPI)
  - [ ] Gap analysis documented
- [ ] **Integration Validation**:
  - [ ] jane-orchestrator integration tested
  - [ ] Navigation from jane-ui functional
  - [ ] Real-time sync via WebSocket operational
- [ ] **Security Preservation**:
  - [ ] E2E encryption maintained (CRDT sync)
  - [ ] Local-first privacy preserved
  - [ ] SQLite security patterns intact
  - [ ] Bank connection security verified
- [ ] **Rollback Capability**: Migration can be safely rolled back if issues discovered
- [ ] **Production Readiness**: All validation tests passing in production-like environment
- [ ] **Stakeholder Sign-off**: Migration acceptance testing completed

**EXIT CONDITION**: All checklist items verified ✅

**RETURN TO**: [`tasks.md#T107`](../tasks.md#T107)

**UPDATE PARENT**: Mark `tasks.md#T106` complete

---

## Validation Commands

```bash
# Run ground truth test suite
cd apps/productivity-service
pytest tests/ground_truth/actual/ -v --cov=src --cov-report=term-missing

# Run performance benchmarks
pytest tests/performance/actual/ -v --benchmark-only

# Run E2E tests
cd tests/e2e
npx playwright test actual-budget/

# Validate API documentation
cd apps/productivity-service
python -m src.api.main  # Serves OpenAPI at /docs

# Check coverage threshold
pytest tests/ --cov=src --cov-fail-under=80
```

---

## Migration Completion Report

**Template for documenting completion**:

```markdown
# Actual Budget Migration - Completion Report

**Date**: YYYY-MM-DD
**Migrated By**: [Team/Individual]
**Total Duration**: X hours (estimated: 60 hours)

## Summary

- **Tasks Completed**: 82/82 (100%)
- **Test Coverage**: X% (target: 80%+)
- **Performance**: ✅ All targets met / ⚠️ Issues noted below

## Critical Algorithm Validation

### Spreadsheet Engine
- Ground Truth Tests: X/X passing
- Performance: Xms (target: <10ms)
- Functional Parity: ✅ Verified

### CRDT Sync
- Ground Truth Tests: X/X passing
- Performance: Xms (target: <500ms)
- Encryption: ✅ Preserved

### Transaction Import
- Ground Truth Tests: X/X passing
- Performance: Xms per transaction (target: <100ms)
- Formats Supported: CSV, OFX, QFX ✅

### Undo/Redo System
- Ground Truth Tests: X/X passing
- History Stack: 20 operations ✅
- Functional Parity: ✅ Verified

## Additional Features Validated

### Reports Engine
- Net Worth: ✅ Functional
- Spending Reports: ✅ Functional
- Cash Flow: ✅ Functional

### Notes & Tags
- Notes System: ✅ Migrated
- Tags System: ✅ Migrated
- UI Integration: ✅ Complete

### Bank Integrations
- SimpleFIN: ✅ Connected and tested
- GoCardless: ✅ OAuth flow working
- Error Handling: ✅ Verified

### UI Enhancements
- Emotion CSS-in-JS: ✅ Configured
- Theme System: ✅ Light/dark modes working
- Redux Store: ✅ All slices migrated
- i18n: ✅ Multi-language support
- Modals: ✅ Management system functional
- Keyboard Shortcuts: ✅ All shortcuts working

## Issues Discovered

[List any deviations from analysis, unexpected behaviors, or technical debt]

## Recommendations

[Suggestions for future improvements, optimizations, or follow-up tasks]

## Sign-off

- [ ] Technical Lead Approval
- [ ] QA Approval
- [ ] Product Owner Approval

**Parent Task**: Marked `tasks.md#T106` complete on YYYY-MM-DD
```

---

## END OF MIGRATION TASKS

**STATUS**: Ready for implementation  
**NEXT STEP**: Begin with Pre-Flight Checklist validation, then proceed to Phase 1 Task T001

**Documentation Update Required**:
```markdown
# In migration-validation.md

### Actual Budget Migration (TXXX)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: XX
- **Actual Hours**: XX
- **Tests**: X passed, 0 failed
- **Performance**: All baselines met/exceeded
- **Notes**: [Any notable achievements or challenges]
```

