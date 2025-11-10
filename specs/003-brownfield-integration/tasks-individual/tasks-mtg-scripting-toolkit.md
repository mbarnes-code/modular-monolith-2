---
description: "MTG Scripting Toolkit - TypeScript toolkit migration to unified MTG service"
parent_task: "../tasks.md#T116"
parent_phase: "Phase 3e: MTG Domain Migrations"
return_to: "../tasks.md#T117"
domain: "mtg"
target_service: "apps/mtg-service/src/"
legacy_path: "features/mtg-scripting-toolkit"
estimated_hours: 35
migration_type: "Category B - Domain Logic Preservation"
complexity: "HIGH - Complex algorithms + external API integrations"
---

# Tasks: [MIGRATION: MTG Scripting Toolkit]

**⬆️ PARENT TASK**: [`tasks.md#T116`](../tasks.md#T116)  
**⬇️ RETURN TO**: [`tasks.md#T117`](../tasks.md#T117)

---

## Migration Summary

**Project**: MTG Scripting Toolkit - TypeScript research toolkit → Python FastAPI service  
**Complexity**: HIGH - Complex MTG domain algorithms + external API integrations  
**Key Assets**: Color sorting algorithm, spell checking, Scryfall API integration, 28 example scripts  
**Migration Approach**: Domain-Driven Design with MTG bounded contexts preservation

**Critical Success Factors**:

- **Algorithm Preservation**: Magic color sorting (WUBRG) must maintain exact player-familiar ordering
- **Performance Baselines**: Sorting <10ms, spell checking ~100ms, bulk processing ~50ms  
- **External APIs**: Scryfall, Commander Spellbook, Cube Cobra integrations preserved
- **Domain Knowledge**: MTG color identity rules, card naming conventions maintained exactly
- **Functional Parity**: All 28 TypeScript example scripts → Python equivalents with identical outputs

## Handoff Context

**Called From**: `tasks.md` Phase 3e, Task T116  
**Entry Condition**: Phase 1-2 complete, apps/mtg-service/ foundation ready  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark T116 complete in parent `tasks.md`, proceed to T117

**Migration Context**: TypeScript-based MTG analysis toolkit with critical domain algorithms

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/mtg-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/mtg-scripting-toolkit/` accessible
- [ ] Project analysis report completed and validated

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

**Input (Spec)**: MTG Scripting Toolkit Analysis Report from `modular-analysis-repo-main/reports/mtg-scripting-toolkit-analysis.md`  
**Input (Legacy)**: TypeScript codebase at `features/mtg-scripting-toolkit/`  
**Prerequisites**: **mtg-scripting-toolkit-analysis.md (MANDATORY)**, Phase 1-2 foundation complete, apps/mtg-service/ base structure ready

**Project Analysis Integration**: This migration MUST reference specific sections from mtg-scripting-toolkit-analysis.md:

- Section 2 (Data Architecture) - Card models, Combo structures, Cube data relationships
- Section 3 (API Architecture) - Scryfall API integration, caching patterns, error handling
- Section 4 (Business Logic) - Critical MTG algorithms (color sorting, spell checking, deduplication)
- Section 5 (External Integrations) - Scryfall API, Commander Spellbook, Cube Cobra integrations
- Section 8 (Performance Characteristics) - Bulk data processing, caching strategy optimization
- Section 11 (Domain Knowledge) - MTG color identity, card naming conventions, format legalities

**Tests**: Ground Truth tests MANDATORY for all critical algorithms. TypeScript to Python validation required.

**Organization**: Tasks grouped by MTG Domain Features with DDD bounded context preservation.

## MTG Domain Bounded Contexts

- **Card Data Context**: Scryfall integration, card models, search functionality
- **Analysis Context**: Color sorting, spell checking, deduplication algorithms  
- **Integration Context**: External APIs, caching layer, bulk data management
- **Scripting Context**: Analysis workflows, example patterns, utility functions

## Migration Methodology: TypeScript → Python Domain Logic Preservation

**Core Principle**: Preserve MTG domain expertise while migrating to unified Python service architecture.

**Validation Strategy**:

1. Ground Truth Tests → Run existing TypeScript examples to establish behavioral baselines
2. Analysis Cross-Reference → Validate against documented MTG domain rules in analysis
3. Algorithm Preservation → Port critical algorithms maintaining functional and performance parity
4. Integration Continuity → Preserve all external API integrations with enhanced error handling
5. Domain Validation → Ensure MTG-specific business rules are maintained exactly

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Analysis Validation & Legacy Environment Setup

**Purpose**: Validate MTG Scripting Toolkit analysis findings and establish TypeScript baseline testing environment.

- [ ] T001 [Analysis: Section.1] Validate MTG toolkit analysis completeness: Confirm all CRITICAL sections for TypeScript toolkit documented
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate TypeScript, Node.js, tsx runtime against actual codebase at `features/mtg-scripting-toolkit/`
- [ ] T003 [P] [Analysis: Section.7.1] Example scripts baseline: Run all 28 example scripts and document current outputs as Ground Truth
- [ ] T004 [Analysis: Section.8.1] Performance baseline: Measure bulk data download (10-30s), card sorting (<10ms), spell checking (~100ms)
- [ ] T005 [Ground Truth] Setup TypeScript test environment: Install Node.js 18+, npm dependencies, validate tsx execution
- [ ] T006 [Ground Truth] Validate critical workflows: Execute card search, combo analysis, cube comparison scripts
- [ ] T007 [P] Create MTG service structure: Initialize `apps/mtg-service/src/` with Python FastAPI foundation
- [ ] T008 [P] Initialize Python MTG dependencies: Setup Python equivalents for TypeScript libraries (requests, pandas, pydantic)

---

## Phase 2: MTG Data Models Migration

**Purpose**: Migrate MTG-specific data models from TypeScript types to Python models based on analysis Section 2.

- [ ] T009 [Analysis: Section.2.1] Inventory MTG data models: Card (Scryfall), Combo (Commander Spellbook), CubeCobraCard from `utils/*/types.ts`
- [ ] T010 [Analysis: Section.2.1] Create Python Card model: Port `utils/scryfall/types.ts` Card interface to Pydantic model preserving all fields
- [ ] T011 [P] [Analysis: Section.2.1] Create Python Combo model: Port Commander Spellbook types with card relationships
- [ ] T012 [Analysis: Section.2.3] Implement caching data models: File-based cache structure for bulk data and API responses
- [ ] T013 [Ground Truth] Data model validation tests: Ensure Python models handle all TypeScript data cases exactly
- [ ] T014 [Analysis: Section.2.2] Card relationship mappings: Oracle ID grouping, set relationships, combo card associations

**Checkpoint**: MTG data models migrated maintaining Scryfall API compatibility.

## Phase 3: External API Integration Infrastructure

**Purpose**: Core infrastructure for Scryfall API and external service integration based on analysis Section 3.

- [ ] T015 [Analysis: Section.3.1] No authentication required: Document public API access patterns (Scryfall, Commander Spellbook, Cube Cobra)
- [ ] T016 [Analysis: Section.9.1] API security measures: Implement rate limiting, request throttling, error handling
- [ ] T017 [P] [Analysis: Section.3.2] API client framework: Setup HTTP client infrastructure for external APIs
- [ ] T018 [Analysis: Section.8.1] Caching infrastructure: Implement file-based caching matching TypeScript `.cache` directory pattern
- [ ] T019 [Analysis: Section.7.1] API testing framework: Setup testing infrastructure for external API mocking and validation
- [ ] T020 Configure error handling: Network failures, rate limiting, service degradation per Section.5.1

**Checkpoint**: External API infrastructure ready. NO MTG business logic exists yet.

## Phase 4: Critical MTG Algorithm Migration (Magic Color Sorting) 🎯 MVP

**Migration Goal**: Port Magic Color Identity Sorting algorithm from `utils/mtg/sort.ts` and `utils/mtg/magicSort.ts`

**Analysis Reference**: Section.4.1 - Critical Algorithm (MUST PRESERVE), Section.11.1 - MTG Domain Knowledge

**Independent Test**: WUBRG color order validation with multicolor groupings

### Phase 4a: Algorithm Analysis & Ground Truth

- [ ] T021 [Analysis: Section.4.1] Magic color sorting analysis: Review critical WUBRG ordering algorithm (~90 lines, Medium complexity)
- [ ] T022 [Analysis: Section.11.1] MTG color domain knowledge: Document color identity rules, multicolor groupings, land categorization
- [ ] T023 [P] [F1] [Analysis: Section.4.1] [Logic: utils/mtg/sort.ts::magicSort] Ground Truth Test: Test current TypeScript sorting with all color combinations
- [ ] T024 [P] [F1] [Analysis: Section.4.1] [Logic: utils/mtg/sort.ts::magicSort] Python Validation Test: Create Python test (initially failing)
- [ ] T025 [Analysis: Section.8.1] Performance baseline: Document <10ms sort time for 360-720 cards, O(n log n) complexity

### Phase 4b: Algorithm Migration & Validation

- [ ] T026 [F1] [Analysis: Section.4.1] [Logic: utils/mtg/sort.ts::magicSort] Algorithm preservation: Port exact WUBRG ordering maintaining lodash.sortBy patterns
- [ ] T027 [F1] [Analysis: Section.4.1] [Logic: utils/mtg/colorGroup.ts] Color group determination: Port color group logic (mono/multi/colorless/land)
- [ ] T028 [F1] [Analysis: Section.11.2] MTG edge cases: Double-faced cards, hybrid mana, colorless cards that produce colored mana
- [ ] T029 [F1] [Analysis: Section.3.2] Sorting API endpoint: Create FastAPI endpoint for card sorting functionality
- [ ] T030 [F1] [Analysis: Section.8.1] Performance validation: Confirm Python implementation maintains <10ms sort time
- [ ] T031 [F1] Integration test: End-to-end test with complete Magic card database (~25,000 cards in ~50ms)

**Checkpoint**: Magic color sorting migrated with MTG player-familiar ordering preserved.

## Phase 5: Card Name Spell Checking Migration (Feature 2)

**Migration Goal**: Port spell checking algorithm from `utils/mtg/spellCheckCardNames.ts` with fuzzy matching

**Analysis Reference**: Section.4.1 - Critical Algorithm (MUST PRESERVE), Section.11.2 - MTG Card Naming

**Independent Test**: Card name validation against Scryfall database with fuzzy suggestions

### Phase 5a: Spell Checking Analysis Integration

- [ ] T032 [Analysis: Section.4.1] Spell checking analysis: Document fuzzy matching algorithm (~50 lines, Medium complexity)
- [ ] T033 [Analysis: Section.11.2] MTG card naming conventions: Double-faced cards (//), Adventure cards, special characters
- [ ] T034 [P] [F2] [Analysis: Section.4.1] [Logic: utils/mtg/spellCheckCardNames.ts::spellCheckCardNames] Ground Truth Test: Test current validation behavior
- [ ] T035 [P] [F2] [Analysis: Section.4.1] [Logic: utils/mtg/spellCheckCardNames.ts::spellCheckCardNames] Python Validation Test: Create Fuse.js equivalent test

### Phase 5b: Spell Checking Migration

- [ ] T036 [F2] [Analysis: Section.4.1] [Logic: utils/mtg/spellCheckCardNames.ts] Fuzzy matching port: Implement Python equivalent of Fuse.js fuzzy search
- [ ] T037 [F2] [Analysis: Section.11.2] Card name format handling: Double-faced cards, Adventure cards, special character support
- [ ] T038 [F2] [Analysis: Section.5.1] Scryfall bulk data integration: Connect spell checker to bulk card name database
- [ ] T039 [F2] Performance validation: Maintain ~100ms for small lists, ~1s for hundreds of names

**Checkpoint**: Card name spell checking migrated with MTG-specific name format support.

## Phase 6: Scryfall API Integration Migration

**Migration Goal**: Preserve all external API integrations per Analysis Section.5 (Scryfall, Commander Spellbook, Cube Cobra)

**Analysis Reference**: Section.5.1 - Third-party APIs (CRITICAL - no auth required)

### Phase 6a: External API Integration Analysis

- [ ] T040 [Analysis: Section.5.1] Scryfall API integration: Port `utils/scryfall/` client with search, bulk data, card lookup
- [ ] T041 [Analysis: Section.5.1] Commander Spellbook integration: Port Google Sheets CSV fetching for combo data
- [ ] T042 [P] [Analysis: Section.5.1] Cube Cobra integration: Port cube list fetching (unofficial API)
- [ ] T043 [Analysis: Section.5.1] Caching layer migration: Port `.cache` directory pattern with TTL management

### Phase 6b: API Integration Validation

- [ ] T044 [Analysis: Section.5.1] Scryfall connectivity: Test search API (~100-175 req/sec), bulk data downloads (no limits)
- [ ] T045 [Analysis: Section.5.1] Rate limiting implementation: Client-side throttling to respect Scryfall limits
- [ ] T046 [Analysis: Section.5.1] Error handling: Network failures, service outages, cache fallback strategies

## Phase 7: First Printing Deduplication & Utility Functions

**Migration Goal**: Complete utility function migration and performance optimization per Analysis Section.8

**Analysis Reference**: Section.8.1 - Performance Baselines, Section.4.1 - Simple Algorithms

### Phase 7a: Utility Algorithm Migration

- [ ] T047 [Analysis: Section.4.1] [Logic: utils/mtg/uniqueFirstPrintings.ts] First printing deduplication: Port O(n) algorithm for removing reprints
- [ ] T048 [Analysis: Section.4.1] [Logic: utils/mtg/compareLists.ts] Card list comparison: Port cube comparison utilities
- [ ] T049 [Analysis: Section.4.1] [Logic: utils/mtg/card.ts] Card property utilities: Port power/toughness parsing, word count functions

### Phase 7b: Performance & Quality Validation

- [ ] T050 [Analysis: Section.8.1] Bulk processing performance: Validate ~50ms for complete Magic database deduplication
- [ ] T051 [Analysis: Section.7.1] Example script migration: Port 28 TypeScript example scripts to Python equivalents
- [ ] T052 [P] [Analysis: Section.11.2] MTG edge case validation: Test all documented card format quirks and special cases

## Phase 8: MTG Domain Knowledge Preservation & API Endpoints

**Migration Goal**: Preserve MTG domain expertise and create unified API per Analysis Section.11

**Analysis Reference**: Section.11.1 - MTG Domain Rules, Section.11.2 - Card Format Quirks

- [ ] T053 [Analysis: Section.11.1] MTG color identity validation: Ensure Commander format rules preserved exactly
- [ ] T054 [Analysis: Section.11.2] Card naming quirks: Double-faced cards, Adventure cards, special characters, ligatures
- [ ] T055 [Analysis: Section.11.1] Format legality business rules: Standard, Pioneer, Modern, Legacy, Vintage, Commander restrictions
- [ ] T056 [P] FastAPI endpoint creation: Expose MTG toolkit functions as REST API endpoints for unified platform integration

## Phase 9: Cross-Cutting Concerns & Polish

- [ ] T057 [Analysis: Section.10.2] Structured logging: Implement console output patterns for analysis workflow debugging
- [ ] T058 [Analysis: Section.9.1] API security hardening: Rate limiting, request validation, error message sanitization
- [ ] T059 [P] Code optimization: Python performance tuning for bulk data processing and algorithm execution
- [ ] T060 [Analysis: Section.13.1] Documentation migration: Port README examples and TypeScript patterns to Python equivalents

## Phase 10: Migration Validation & Asset Retirement

**Purpose**: Comprehensive validation before TypeScript asset removal.

### Phase 10a: Complete MTG Migration Validation

- [ ] T061 [Analysis: All Sections] Full analysis cross-reference: Verify all MTG toolkit analysis findings addressed
- [ ] T062 [Analysis: Section.4.1] Algorithm parity validation: Confirm color sorting, spell checking, deduplication function identically
- [ ] T063 [Analysis: Section.8.1] Performance regression testing: Validate all performance baselines maintained (sorting <10ms, etc.)
- [ ] T064 [Analysis: Section.12.3] Success criteria verification: All 28 example scripts have Python equivalents
- [ ] T065 Verify Full Migration: All [Logic: ...] references have passing Ground Truth validation tests
- [ ] T066 Run Full Regression Suite: Execute complete test suite with TypeScript vs Python output comparison

### Phase 10b: Safe TypeScript Asset Retirement

- [ ] T067 [Analysis: Section.12.2] Risk mitigation: Verify all external API integrations preserved
- [ ] T068 TypeScript toolkit backup: Archive `features/mtg-scripting-toolkit/` before removal
- [ ] T069 Production validation: Run Python MTG service in unified platform environment
- [ ] T070 Lucky Paper stakeholder approval: Validate content creation workflows preserved
- [ ] T071 Delete Legacy Asset: After 100% validation, remove `features/mtg-scripting-toolkit/`

### Phase 10c: Post-Migration MTG Service Monitoring

- [ ] T072 [Analysis: Section.10.2] API monitoring: Track MTG service endpoint performance and usage
- [ ] T073 [Analysis: Section.8.1] Performance monitoring: Continuous validation against TypeScript baselines
- [ ] T074 [Analysis: Section.11.3] MTG workflow monitoring: Ensure cube analysis and content creation workflows remain optimal

### Dependencies & Execution Order

**Sequential Dependencies (Must Complete In Order):**

- **Phase 1 (Analysis Validation)**: Must complete first - validates MTG toolkit analysis and establishes TypeScript baseline
- **Phase 2 (Data Models)**: Must complete before algorithms - establishes MTG data foundation (Card, Combo models)
- **Phase 3 (API Infrastructure)**: Must complete before feature migration - establishes Scryfall integration framework

**Parallel Execution Phases:**

- **Phases 4-5 (Critical Algorithms)**: Can proceed in parallel - Color sorting and Spell checking are independent
- **Phase 6 (External APIs)**: Can run in parallel with algorithm migration
- **Phase 7 (Utility Functions)**: Can run in parallel after Phase 4-5 complete
- **Phase 8 (Domain Knowledge)**: Can run in parallel with utility migration

**Final Sequential Dependencies:**

- **Phase 9 (Polish)**: After all algorithm and API phases complete
- **Phase 10 (Validation & Retirement)**: Must be final phase - comprehensive testing before TypeScript removal
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

### MTG Toolkit Migration Strategy

**Sequential Foundation** (Required Order):

1. TypeScript Analysis Validation (Phase 1) - Establish Ground Truth baselines from all 28 example scripts
2. MTG Data Models (Phase 2) - Card, Combo, Cube data structures in Python
3. External API Infrastructure (Phase 3) - Scryfall, Commander Spellbook, Cube Cobra integrations

**Parallel Algorithm Migration** (After Foundation):

- **Magic Color Sorting** (Phase 4) - Critical WUBRG ordering algorithm
- **Card Name Spell Checking** (Phase 5) - Fuzzy matching with MTG naming conventions  
- **External API Integration** (Phase 6) - Can proceed parallel to algorithms
- **Utility Functions** (Phase 7) - After core algorithms complete

**MTG-Specific Validation Requirements**:

- Ground Truth tests compare TypeScript vs Python outputs exactly
- Performance baselines: Sorting <10ms, spell checking ~100ms, bulk processing ~50ms
- MTG domain knowledge preserved: Color identity rules, card naming conventions, format legalities

---

## MTG Domain Migration Notes

**Task Completion Criteria:**

- **[Analysis] references** are MANDATORY - every task traces to `mtg-scripting-toolkit-analysis.md`
- **[Logic] preservation** is CRITICAL - MTG algorithms must maintain exact functional behavior
- **Ground Truth Test → TypeScript Baseline → Port to Python → Validate Parity → API Integration** (core loop)
- A task is "done" when Python output matches TypeScript output exactly AND performance baselines are met

**MTG-Specific Quality Gates:**

- Color sorting MUST maintain WUBRG ordering that MTG players expect
- Card name validation MUST handle double-faced cards, Adventure cards, special characters
- External API integrations MUST preserve rate limiting and caching strategies
- All 28 example scripts MUST have functional Python equivalents

**Success Criteria:**

- **Performance**: All Analysis Section 8.1 baselines met or exceeded
- **Functional Parity**: TypeScript toolkit completely replaced by Python service
- **MTG Domain**: All Magic-specific business rules preserved exactly
- **Integration**: FastAPI endpoints ready for unified platform

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

**MTG Toolkit Success Validation:**

- **Functional Parity**: Python MTG service produces identical outputs to TypeScript toolkit
- **Performance Parity**: All analysis baselines met (sorting <10ms, spell checking ~100ms, bulk processing ~50ms)
- **Integration Parity**: Scryfall API, Commander Spellbook, Cube Cobra connections preserved
- **Domain Parity**: All MTG business rules (color identity, card naming, format legalities) preserved exactly
- **Workflow Parity**: All 28 TypeScript example scripts have functional Python equivalents

---

## Post-Flight Checklist ✅

**Verify these conditions before marking parent task complete**:

- [ ] All tasks T001-T074 marked complete above  
- [ ] MTG Integration tests pass: `pytest tests/mtg/test_mtg_scripting_toolkit_integration.py`
- [ ] Performance baselines met: Color sorting <10ms, spell checking ~100ms, bulk processing ~50ms
- [ ] Ground truth tests confirm functional parity: All 28 example scripts have Python equivalents with identical outputs
- [ ] TypeScript toolkit backed up: `features/mtg-scripting-toolkit/` → `archive/mtg-scripting-toolkit-backup/`
- [ ] Migration completion documented in `migration-validation.md`
- [ ] All analysis findings from `mtg-scripting-toolkit-analysis.md` addressed
- [ ] No regressions in Scryfall API integration or external service connectivity
- [ ] MTG domain expertise preserved: Color identity rules, card naming conventions, format legalities
- [ ] FastAPI endpoints functional: MTG service integrates with unified platform

**⚠️ If any checklist item fails**: DO NOT mark parent task T116 complete. Fix issues and re-validate.

**Completion Action**:

1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/mtg/test_mtg_scripting_toolkit_integration.py`
3. Document completion in `migration-validation.md`
4. Mark parent task T116 complete in `tasks.md`
5. Proceed to return task T117 in `tasks.md`

**Documentation Update Required**:

```markdown
# In migration-validation.md

### MTG Scripting Toolkit Migration (T116)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: 35
- **Actual Hours**: [ACTUAL]
- **Tests**: All Ground Truth tests passed, TypeScript vs Python parity confirmed
- **Performance**: Color sorting <10ms ✅, spell checking ~100ms ✅, bulk processing ~50ms ✅
- **External APIs**: Scryfall, Commander Spellbook, Cube Cobra integrations preserved
- **Domain Knowledge**: All MTG business rules and conventions preserved
- **Legacy Asset**: features/mtg-scripting-toolkit/ backed up and removed
- **Notes**: TypeScript research toolkit successfully migrated to Python FastAPI service
```

