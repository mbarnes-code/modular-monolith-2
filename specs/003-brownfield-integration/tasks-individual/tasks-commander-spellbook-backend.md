---
description: "DDD-based migration of Commander Spellbook backend to modular monolith architecture"
parent_task: "../tasks.md#T130"
parent_phase: "Phase 8: MTG Migrations"
return_to: "../tasks.md#T131"
domain: "mtg"
target_service: "apps/mtg-service/src/"
legacy_path: "features/commander-spellbook-backend"
estimated_hours: 85
critical_algorithms: ["variant_generation", "combo_graph", "color_identity", "mana_parsing"]
external_dependencies: ["scryfall_api", "discord_oauth", "card_pricing_apis"]
---

# Tasks: [MIGRATION: Commander Spellbook Backend - MTG Combo Database]

**⬆️ PARENT TASK**: [`tasks.md#T130`](../tasks.md#T130)  
**⬇️ RETURN TO**: [`tasks.md#T131`](../tasks.md#T131)

---

## Handoff Context

**Called From**: `tasks.md` Phase X, Task TXXX  
**Entry Condition**: Mtg service foundation ready (Phase 1-4 complete)  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark TXXX complete in parent `tasks.md`, proceed to next task

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/mtg-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/commander-spellbook-backend/` accessible
- [ ] Project analysis report completed and validated

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

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


## Phase 1: Analysis Validation & Legacy Environment Setup

**Purpose**: Validate Commander Spellbook analysis and establish baseline testing for MTG combo database.

- [ ] T001 [Analysis: Section.1] Validate Commander Spellbook analysis completeness: Confirm Django/DRF architecture documented
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Python 3.x, Django 4.x, PostgreSQL, DRF confirmed
- [ ] T003 [P] [Analysis: Section.7.1] MTG test coverage baseline: Run pytest suite, document combo generation test results  
- [ ] T004 [Analysis: Section.8.1] Variant generation performance baseline: Measure current combo-to-variant generation times
- [ ] T005 [Ground Truth] Setup Commander Spellbook environment: Docker compose up, verify Scryfall integration works
- [ ] T006 [Ground Truth] Validate core MTG functionality: Test combo search, variant generation, card lookup workflows
- [ ] T007 [P] Create MTG service DDD structure: `domains/combos/`, `domains/cards/`, `domains/variants/`  
- [ ] T008 [P] Initialize FastAPI dependencies: Async PostgreSQL, Pydantic models, dependency injection setup

---

## Phase 2: MTG Domain Data Architecture Migration

**Purpose**: Migrate MTG-specific data models with complex relationships and validation rules.

- [ ] T009 [Analysis: Section.2.1] MTG Entity modeling: Card, Combo, Variant, Feature, Template domain models  
- [ ] T010 [Analysis: Section.2.1] Complex relationship schema: Many-to-many with through tables, variant hashing logic
- [ ] T011 [P] [Card Domain] [Logic: models/card.py::Card] Port Card model: Oracle ID, Scryfall integration, mana cost validation
- [ ] T012 [P] [Combo Domain] [Logic: models/combo.py::Combo] Port Combo model: Recipe pattern, status workflow, prefetch manager
- [ ] T013 [P] [Variant Domain] [Logic: models/variant.py::Variant] Port Variant model: Hash-based IDs, popularity computation
- [ ] T014 [P] [Feature Domain] [Logic: models/feature.py::Feature] Port Feature model: MTG effect taxonomy, dependency chains
- [ ] T015 [Analysis: Section.2.3] MTG-specific indexes: Combo search, variant lookup, card filtering optimizations
- [ ] T016 [Ground Truth] MTG data validation: Mana cost format, color identity rules, Commander legality tests
- [ ] T017 [Analysis: Section.2.1] Legacy data migration: Commander Spellbook PostgreSQL to new schema scripts

**Checkpoint**: MTG domain data layer with complex relationships and validation migrated.

## Phase 3: Foundational Infrastructure

**Purpose**: Core application infrastructure based on analysis findings.

- [ ] T015 [Analysis: Section.3.1] Authentication/authorization framework: Implement exact auth patterns from Section.3.1
- [ ] T016 [Analysis: Section.9.1] Security measures: Implement all security patterns identified in analysis
- [ ] T017 [P] [Analysis: Section.3.2] API routing framework: Setup endpoint structure (empty routes initially)
- [ ] T018 [Analysis: Section.8.1] Performance monitoring: Implement baseline monitoring per Section.8.1
- [ ] T019 [Analysis: Section.7.1] Testing framework: Setup testing infrastructure matching current patterns
- [ ] T020 Configure error handling and logging infrastructure per Section.10.2

**Checkpoint**: Foundation ready with security and monitoring. NO business logic exists.

## Phase 4: Combo Variant Generation Algorithm Migration 🎯 MVP

**Migration Goal**: Port the exponentially complex variant generation algorithm (O(C^N)) that auto-generates specific MTG combo implementations from general recipes

**Analysis Reference**: Section.4.1 - Variant Generation Algorithm (1400+ LOC), Section.11.1 - MTG Domain Knowledge

**Independent Test**: Generate variants from simple 2-card combo vs complex multi-template combo with cyclical dependencies

### Phase 4a: Variant Generation Algorithm Analysis & Ground Truth

- [ ] T021 [Analysis: Section.4.1] Variant generation deep dive: Document Graph, VariantSet, FrozenMultiset algorithms
- [ ] T022 [Analysis: Section.11.1] MTG combo mechanics: Card interactions, mana costs, color identity, feature chains
- [ ] T023 [P] [Variant Gen] [Analysis: Section.4.1] [Logic: variants/variants_generator.py::get_variants_from_graph] Ground Truth: Test current variant generation with known combo sets
- [ ] T024 [P] [Variant Gen] [Analysis: Section.4.1] [Logic: variants/combo_graph.py::Graph] Ground Truth: Test combo dependency graph construction
- [ ] T025 [P] [Variant Gen] [Analysis: Section.4.1] [Logic: variants/multiset.py::FrozenMultiset] Ground Truth: Test immutable card collection handling
- [ ] T026 [Analysis: Section.8.1] Performance baseline: Document variant generation times for small/medium/large combo sets

### Phase 4b: Critical Algorithm Migration & Validation

- [ ] T027 [Variant Gen] [Analysis: Section.4.1] [Logic: variants/variants_generator.py::VariantDefinition] Port variant definition data structures with hash-based IDs
- [ ] T028 [Variant Gen] [Analysis: Section.4.1] [Logic: variants/combo_graph.py::Graph.variants] Port directed graph traversal for combo dependencies
- [ ] T029 [Variant Gen] [Analysis: Section.4.1] [Logic: variants/multiset.py] Port immutable multiset collections for card management
- [ ] T030 [Variant Gen] [Analysis: Section.4.1] [Logic: variants/variants_generator.py::get_variants_from_graph] Port main generation algorithm preserving exponential complexity handling
- [ ] T031 [Variant Gen] [Analysis: Section.11.2] Edge case handling: Cyclical dependencies, missing features, timeout prevention
- [ ] T032 [Variant Gen] Async adaptation: Convert synchronous Django ORM to async FastAPI patterns
- [ ] T033 [Variant Gen] [Analysis: Section.8.1] Performance validation: Ensure generation times match or improve on baseline
- [ ] T034 [Variant Gen] Integration test: End-to-end combo submission → variant generation → result storage

**Checkpoint**: Core variant generation algorithm migrated with documented exponential complexity preservation.

## Phase 5: MTG Search & Parsing Engine Migration

**Migration Goal**: Migrate complex MTG card search, mana parsing, and Scryfall query grammar systems

**Analysis Reference**: Section.4.1 - Card Search Algorithm, Section.5.1 - Scryfall Integration

**Independent Test**: Search "Infinite mana WUB commander legal" with complex mana cost filters

### Phase 5a: MTG Search & Parsing Analysis

- [ ] T035 [Analysis: Section.4.1] MTG search complexity: Multi-dimensional card search with color, mana, text filters
- [ ] T036 [Analysis: Section.5.1] Scryfall integration patterns: API client, caching, error handling strategies  
- [ ] T037 [P] [MTG Search] [Logic: parsers/scryfall_query_grammar.py] Ground Truth: Test current search query parsing
- [ ] T038 [P] [MTG Search] [Logic: views/filters.py] Ground Truth: Test card filtering and ranking algorithms
- [ ] T039 [P] [MTG Search] [Logic: parsers/color_parser.py] Ground Truth: Test color identity parsing and merging

### Phase 5b: Search & Parsing Migration

- [ ] T040 [MTG Search] [Analysis: Section.4.1] [Logic: parsers/scryfall_query_grammar.lark] Port Lark grammar for MTG search syntax
- [ ] T041 [MTG Search] [Analysis: Section.4.1] [Logic: parsers/color_parser.py] Port color identity calculation and WUBRG validation
- [ ] T042 [MTG Search] [Analysis: Section.4.1] [Logic: views/filters.py::CardFilter] Port multi-dimensional card filtering system
- [ ] T043 [MTG Search] [Analysis: Section.5.1] [Logic: models/scryfall.py] Port Scryfall API client with async patterns
- [ ] T044 [MTG Search] Text parsing optimization: Async card search with proper indexing for FastAPI
- [ ] T045 [MTG Search] Search result ranking: Port relevance algorithms for combo discovery
- [ ] T046 [MTG Search] Integration test: Full search flow from query parse → filter → rank → return

**Checkpoint**: MTG-specific search and parsing systems migrated with domain expertise preserved.

## Phase 6: API Endpoints & External Integrations Migration

**Migration Goal**: Migrate DRF REST API to FastAPI while preserving Scryfall, Discord OAuth, and card pricing integrations

**Analysis Reference**: Section.3.2 - API Endpoints, Section.5.1 - Scryfall Critical Integration

### Phase 6a: API Architecture & External Dependencies

- [ ] T047 [Analysis: Section.3.2] REST API inventory: Variants, Cards, Features, FindMyCombos endpoints
- [ ] T048 [Analysis: Section.5.1] Scryfall dependency analysis: Card sync, image hosting, Oracle ID management
- [ ] T049 [P] [API] [Logic: views/variants.py] Ground Truth: Test current variant API pagination and filtering
- [ ] T050 [P] [API] [Logic: views/find_my_combos.py] Ground Truth: Test "find combos from my cards" algorithm
- [ ] T051 [P] [External] [Logic: models/scryfall.py] Ground Truth: Test Scryfall API integration and caching

### Phase 6b: API & Integration Migration

- [ ] T052 [API] [Analysis: Section.3.2] [Logic: views/variants.py::VariantViewSet] Port variant API with async FastAPI patterns
- [ ] T053 [API] [Analysis: Section.3.2] [Logic: views/cards.py::CardViewSet] Port card search API with performance optimizations
- [ ] T054 [API] [Analysis: Section.3.2] [Logic: views/find_my_combos.py] Port "find my combos" complex matching algorithm
- [ ] T055 [External] [Analysis: Section.5.1] [Logic: models/scryfall.py] Port Scryfall async client with proper error handling
- [ ] T056 [External] Discord OAuth integration: Adapt authentication to FastAPI dependency injection
- [ ] T057 [External] Card pricing API clients: Port TCGPlayer/CardKingdom async integrations
- [ ] T058 [API] OpenAPI documentation: Generate comprehensive MTG API docs with examples
- [ ] T059 [Integration] End-to-end API testing: Validate all endpoints with external service dependencies

**Checkpoint**: REST API migrated to FastAPI with external integrations preserved and documented.

## Phase 7: MTG Performance Optimization & Quality Assurance

**Migration Goal**: Optimize exponential algorithms and achieve MTG domain performance targets (<3s response)

**Analysis Reference**: Section.8.1 - Variant Generation Performance, Section.7.1 - MTG Test Coverage

### Phase 7a: MTG-Specific Performance Validation

- [ ] T060 [Analysis: Section.8.1] Variant generation benchmarking: Measure combo-to-variant generation performance
- [ ] T061 [Analysis: Section.8.2] Combo search optimization: Ensure sub-second card search with complex filters
- [ ] T062 [Analysis: Section.8.3] Database query optimization: Async PostgreSQL with proper indexing for MTG queries
- [ ] T063 [Performance] Exponential algorithm scaling: Test variant generation with large card sets, implement timeouts

### Phase 7b: MTG Domain Quality Assurance

- [ ] T064 [Analysis: Section.7.1] MTG test coverage: Achieve comprehensive coverage for combo rules and edge cases
- [ ] T065 [Analysis: Section.7.2] MTG rules compliance testing: Validate color identity, mana costs, Commander legality
- [ ] T066 [P] [Analysis: Section.11.2] MTG edge cases: Test infinite combos, mana loops, complex interactions
- [ ] T067 [Quality] Load testing: Validate system handles concurrent combo generation and card searches

## Phase 8: MTG Domain Knowledge & Business Rules Preservation

**Migration Goal**: Preserve deep MTG knowledge and Commander format expertise embedded in the system

**Analysis Reference**: Section.11.1 - MTG Business Domain, Section.11.2 - Commander Format Rules

- [ ] T068 [Analysis: Section.11.1] MTG rules engine validation: Color identity calculations, mana cost parsing, legality checks
- [ ] T069 [Analysis: Section.11.2] Commander format quirks: Singleton rules, color identity restrictions, banned list handling  
- [ ] T070 [Analysis: Section.11.3] Combo discovery patterns: Feature matching algorithms, infinite loop detection
- [ ] T071 [P] MTG documentation: Comprehensive domain documentation for combo mechanics and card interactions
- [ ] T072 [Domain] User workflow preservation: Combo submission, variant browsing, card discovery patterns

## Phase 9: Cross-Cutting Concerns & Integration Polish

- [ ] T073 [Analysis: Section.10.2] MTG service logging: Implement comprehensive logging for combo generation and search
- [ ] T074 [Analysis: Section.9.2] Security hardening: JWT validation, rate limiting, input sanitization
- [ ] T075 [P] Code cleanup and MTG service optimization: Async patterns, dependency injection refinements
- [ ] T076 [Analysis: Section.13.1] MTG API documentation: Complete OpenAPI docs with MTG domain examples

## Phase 10: Commander Spellbook Migration Validation & Asset Retirement

**Purpose**: Comprehensive validation of Commander Spellbook migration before legacy removal.

### Phase 10a: Complete Commander Spellbook Migration Validation

- [ ] T077 [Analysis: All Sections] Full Commander Spellbook analysis cross-reference: All critical algorithms migrated
- [ ] T078 [Analysis: Section.4.1] Variant generation algorithm parity: Exponential complexity performance maintained
- [ ] T079 [Analysis: Section.8.1] MTG performance regression testing: <3s combo generation, <1s card search confirmed
- [ ] T080 [Analysis: Section.12.3] MTG success criteria: All combo workflows, card search, variant browsing functional
- [ ] T081 Verify Complete Migration: All 72 tasks with [Logic: ...] have passing validation tests  
- [ ] T082 Run Commander Spellbook Regression Suite: Ground truth tests pass for all migrated features

### Phase 10b: Safe Commander Spellbook Asset Retirement

- [ ] T083 [Analysis: Section.12.2] MTG migration risk mitigation: Data backup, rollback procedures documented
- [ ] T084 Commander Spellbook legacy backup: Archive `features/commander-spellbook-backend/` to secure storage
- [ ] T085 Production MTG validation: Deploy to staging, validate with MTG community subset
- [ ] T086 MTG stakeholder approval: Commander community and maintainer sign-off on migration
- [ ] T087 Delete Commander Spellbook Legacy Asset: Remove `features/commander-spellbook-backend/` directory

### Phase 10c: Post-Migration MTG Service Monitoring

- [ ] T088 [Analysis: Section.10.2] MTG monitoring systems: Track combo generation performance, search latency  
- [ ] T089 [Analysis: Section.8.1] MTG performance baselines: Monitor variant generation times, alert on regressions
- [ ] T090 [Analysis: Section.11.3] MTG user workflow monitoring: Track combo discovery, submission, browsing patterns

### Dependencies & Execution Order

**Sequential Dependencies (Must Complete In Order):**
- **Phase 1 (Analysis Validation)**: Must complete first - validates analysis completeness
- **Phase 2 (Data Architecture)**: Must complete before business logic - establishes data foundation
- **Phase 3 (Foundational Infrastructure)**: Must complete before feature migration - establishes framework

**Parallel Execution Phases:**
- **Phases 4-6 (Business Logic, Security, Integrations)**: Can proceed in parallel by feature after Phase 3
- **Phase 7 (Performance & Quality)**: Can run in parallel with feature phases
- **Phase 8 (Domain Knowledge)**: Can run in parallel with feature phases

**Final Sequential Dependencies:**
- **Phase N (Cross-Cutting Concerns)**: After all feature phases complete
- **Phase N+1 (Asset Retirement)**: The absolute final step - only after complete validation

---

## Implementation Strategy: Analysis-Driven Migration

### Analysis-First Approach

1. **Complete Phase 1**: Analysis validation and baseline establishment (MANDATORY FIRST)
2. **Complete Phase 2**: Data architecture migration (foundation for all features)
3. **Complete Phase 3**: Infrastructure setup (framework foundation)
4. **Begin Feature Migration**: Start with highest priority features from analysis

### Critical Feature Priority (Based on Analysis Section 12.1)

1. **CRITICAL Priority Features**: Must migrate first (usually from Analysis Section 4.1)
2. **IMPORTANT Priority Features**: Second wave migration
3. **NICE-TO-HAVE Features**: Final migration wave

### Incremental Delivery Strategy

1. **Foundation Phase** (Phases 1-3): Complete infrastructure → Validate baseline functionality
2. **Critical Feature MVP**: Migrate one critical feature → **STOP and VALIDATE** → Deploy
3. **Feature Increment**: Add next priority feature → Validate independently → Deploy
4. **Continue Incrementally**: Each feature adds value without breaking previous functionality

### Risk-Minimized Parallel Strategy

**Sequential Foundation** (Team Together):
1. Analysis validation (Phase 1) - entire team validates findings
2. Data migration (Phase 2) - critical shared foundation
3. Infrastructure setup (Phase 3) - framework foundation

**Parallel Feature Migration** (After Foundation):
- Developer A: Critical Feature 1 (Analysis Section 4.1 priority)
- Developer B: Critical Feature 2 (Analysis Section 4.1 priority) 
- Developer C: Security/Integration (Analysis Sections 5 & 9)
- All developers: Continuous validation against analysis baselines

**Validation Requirements**:
- Each feature must pass ground truth tests before integration
- Performance must meet Analysis Section 8.1 baselines
- All Analysis Section 11 domain knowledge must be preserved

---

## Brownfield Migration Methodology Notes

**Task Completion Criteria:**
- [P] tasks = different files, no dependencies (can run in parallel)
- [Analysis] references are MANDATORY - every task must trace to analysis findings
- [Logic] preservation is CRITICAL - exact functional behavior must be maintained
- Ground Truth Test → Analysis Cross-Reference → Port Logic → Validate → Integrate (core loop)
- A task is not "done" when code is written - it's "done" when validation passes AND analysis criteria are met

**Quality Gates:**
- Every phase has explicit checkpoints requiring validation before proceeding
- All critical algorithms (Analysis Section 4.1) must have functional parity tests
- All performance baselines (Analysis Section 8.1) must be met or exceeded
- All domain knowledge (Analysis Section 11) must be preserved and validated

**Risk Mitigation:**
- Analysis findings drive task creation - never skip analysis integration
- Ground truth tests establish irrefutable behavioral baselines
- Incremental migration reduces blast radius of changes
- Performance monitoring prevents regressions
- Stakeholder validation ensures business continuity

**Success Validation:**
- Functional parity: New system behaviors match legacy system exactly
- Performance parity: New system meets or exceeds performance baselines
- Integration parity: All external services continue working without changes
- Domain parity: All business rules and domain knowledge preserved
- User parity: All user workflows continue functioning identically

---

## Post-Flight Checklist ✅

**Verify these conditions before marking parent task complete**:

- [ ] All tasks T001-T090 marked complete above  
- [ ] Integration tests pass: `pytest tests/mtg/test_commander_spellbook_integration.py`
- [ ] MTG performance baselines met: <3s variant generation, <1s card search (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm MTG functional parity: combo generation, search, card parsing
- [ ] Legacy `features/commander-spellbook-backend/` backed up to `archive/commander-spellbook-backend-YYYY-MM-DD/`
- [ ] Commander Spellbook migration completion documented in `migration-validation.md`
- [ ] All Commander Spellbook analysis findings from commander-spellbook-analysis.md addressed
- [ ] No regressions in existing MTG service functionality  
- [ ] MTG API security audit passed: input validation, rate limiting, authentication
- [ ] MTG domain expertise preserved: combo rules, color identity, mana parsing, Commander format compliance

**⚠️ If any checklist item fails**: DO NOT mark parent task T130 complete. Fix issues and re-validate.

**Completion Action**:
1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/mtg/test_commander_spellbook_integration.py -v`
3. Document completion in `migration-validation.md`  
4. Mark parent task T130 complete in `tasks.md`
5. Proceed to return task T131 in `tasks.md`

**Documentation Update Required**:

```markdown
# In migration-validation.md

### Commander Spellbook Backend Migration (T130)

- **Status**: ✅ Complete
- **Completed**: [DATE]  
- **Estimated Hours**: 85
- **Actual Hours**: XX
- **Tasks Completed**: 90/90
- **Tests**: MTG integration tests passed, variant generation performance validated
- **Performance**: <3s combo generation, <1s card search - baselines met/exceeded
- **Critical Algorithms Preserved**: Variant generation (1400+ LOC), combo graph traversal, MTG parsing
- **External Dependencies**: Scryfall API, Discord OAuth, card pricing APIs - all functional
- **Domain Knowledge**: MTG rules, Commander format, combo mechanics - fully preserved
```
- **Notes**: [Any notable achievements or challenges]
```

