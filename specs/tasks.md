---
description: "Task list template for brownfield asset relocation and incremental migration"
---

# Tasks: [MIGRATION: FEATURE NAME]

**Input**: Migration strategy from `/specs/[###-feature-name]/migration-strategy.md`
**Prerequisites**: spec.md (required), plan.md (required), migration-strategy.md (required)

**External References**: 
- Requirements: `specs/[###-feature]/spec.md`
- Architecture: `specs/[###-feature]/plan.md`
- Migration Strategy: `specs/[###-feature]/migration-strategy.md`

## Project Scale Assessment

**Project Scale**: [SMALL/MEDIUM/LARGE/EXTREME] *(from spec.md)*
**Migration Method**: [Method Name] *(from migration-strategy.md)*
**Selected Risk Level**: [MEDIUM/HIGH/VERY HIGH/EXTREME]

## Migration Decision Summary

**Technology Consolidation Strategy**: *(from migration-strategy.md)*
- **High-Overlap Stacks (CONSOLIDATE)**: [List technologies]
- **Low-Usage Stacks (ISOLATE)**: [List technologies]

**Implementation Strategy Matrix**: *(from migration-strategy.md)*
- **Complex Algorithms → Strategy 1: Copy & Modernize**
- **Well-Documented Features → Strategy 2: Behavior-Driven Rewrite**
- **Mixed Complexity → Strategy 3: Incremental Refactor**
- **Service Integration → Strategy 4: API-First Integration**

## Format: `[ID] [P?] [Feature] [Strategy] Description`

- **[P]**: Can run in parallel (different systems, no dependencies)
- **[Feature]**: Which legacy system/feature this task migrates (e.g., F1, F2, F3)
- **[Strategy]**: Implementation strategy (S1: Copy&Modernize, S2: Rewrite, S3: Refactor, S4: API-First)
- Include exact source and target file paths in descriptions

## File Transformation Lifecycle

**CRITICAL**: Legacy files are **NEVER transformed in-place**. Migration follows **Copy & Preserve** methodology:

1. **Legacy Preservation**: Original files remain untouched and active
2. **Target Creation**: Business logic copied and modernized in target structure  
3. **Validation & Retirement**: Legacy files archived only after 100% validation passes

---

## Phase 1: Setup & Legacy Environment

**Purpose**: Initialize target project and establish legacy testing environment for ground truth validation.

- [ ] T001 Create new project structure per implementation plan
- [ ] T002 [Ground Truth] Setup legacy test environment: Create isolated environment for legacy systems
- [ ] T003 [Ground Truth] Validate legacy functionality: Run legacy systems and confirm all critical workflows function as baseline
- [ ] T004 [Analysis] Validate project analysis completeness: Confirm all migration strategy sections filled per template
- [ ] T005 [Analysis] Document performance baselines: Extract and validate baseline metrics from legacy systems
- [ ] T006 [Analysis] Assess test coverage baseline: Review current test coverage and critical test cases
- [ ] T007 [Analysis] Review business logic inventory: Study critical algorithms and business rules documentation

---

## Phase A: Technology Stack Consolidation (MEDIUM+ Scale Only)

**Purpose**: **INFRASTRUCTURE FIRST** - Consolidate high-overlap technology stacks before business logic migration. Skip for SMALL scale projects.

### Phase A.1: High-Overlap Stack Consolidation

- [ ] TA01 [Analysis] **Technology Stack Inventory**: Identify high-overlap vs low-usage stacks across all legacy systems
- [ ] TA02 [Analysis] **Consolidation Strategy Decision**: Choose database consolidation strategy (Central/Domain/Federated/Hybrid)
- [ ] TA03 **[Primary Language] Environment Unification**: Create unified environment for majority language stack
- [ ] TA04 **[Secondary Language] Toolchain Unification**: Standardize toolchain for secondary language stack  
- [ ] TA05 **Database Consolidation Implementation**: Execute chosen database consolidation strategy
- [ ] TA06 **Framework Bridge Development**: Create bridges between framework patterns in unified environments
- [ ] TA07 **Cross-Stack Testing**: Validate all legacy systems work in consolidated technology environment

### Phase A.2: Low-Usage Stack Isolation Strategy

- [ ] TA08 **Isolated Stack Assessment**: Analyze remaining low-usage stacks for isolation needs
- [ ] TA09 **Service Adapter Framework**: Create framework for connecting isolated stacks to consolidated environment
- [ ] TA10 **Isolation Environment Setup**: Setup isolated environments for specialized/legacy stacks
- [ ] TA11 **Integration Layer Implementation**: Implement API gateway and service adapters for isolated stacks

**Checkpoint A**: Technology stacks consolidated/isolated. Business logic migration can now proceed with simplified infrastructure.

---

## Phase 2: Business Logic Foundation  

**Purpose**: Core target application infrastructure - the foundation for all business logic migration.

- [ ] T010 Initialize target framework dependencies using consolidated technology stack from Phase A
- [ ] T011 [P] Configure linting and formatting tools for consolidated technology stack
- [ ] T012 [P] Setup consolidated database schema and migrations framework 
- [ ] T013 [P] Implement authentication/authorization framework shell (empty - will be populated by feature migrations)
- [ ] T014 [P] Setup API routing and middleware structure (empty routes initially)
- [ ] T015 [P] Create empty base models/entities based on migration strategy (shells only - actual models come from feature migration)
- [ ] T016 Configure error handling, logging, and monitoring infrastructure
- [ ] T017 [P] Setup testing framework infrastructure matching legacy system patterns

---

## Phase 3: Feature Migration (Repeat per Legacy System/Feature)

**Purpose**: Migrate individual legacy systems using appropriate implementation strategies. Each feature can be migrated independently and in parallel after analysis validation.

### Feature Migration Pattern (Template - Copy per Feature)

Replace [FX] with feature identifier (F1, F2, etc.) and [SYSTEM_NAME] with legacy system name.

#### [FX] Ground Truth & Analysis Validation

- [ ] T0[X]1 [FX] [Ground Truth] Test legacy [SYSTEM_NAME]: Write comprehensive test against legacy system proving original behavior
- [ ] T0[X]2 [FX] [Analysis] Validate feature analysis: Cross-check analysis documentation against actual legacy system behavior
- [ ] T0[X]3 [FX] [Analysis] Document critical algorithms: Extract and document business-critical algorithms that must be preserved exactly

#### [FX] Implementation (Choose Strategy Based on Migration Analysis)

**Strategy 1: Copy & Modernize (Complex Algorithms)**
- [ ] T0[X]4 [FX] [S1] Copy legacy files: Copy [SYSTEM_NAME] files from `legacy/path/` to `target/path/`
- [ ] T0[X]5 [FX] [S1] Update framework calls: Replace legacy framework calls with target framework equivalents
- [ ] T0[X]6 [FX] [S1] Preserve business logic: Ensure all business logic remains functionally identical

**Strategy 2: Behavior-Driven Rewrite (Well-Documented Features)**
- [ ] T0[X]4 [FX] [S2] Study analysis documentation: Review analysis Section 4 algorithm documentation thoroughly
- [ ] T0[X]5 [FX] [S2] Implement from analysis: Write new implementation based on documented behaviors and requirements
- [ ] T0[X]6 [FX] [S2] Validate against ground truth: Ensure new implementation matches all documented legacy behaviors

**Strategy 3: Incremental Refactor (Mixed Complexity)**
- [ ] T0[X]4 [FX] [S3] Port data layer: Copy and modernize data models from legacy system
- [ ] T0[X]5 [FX] [S3] Port business logic: Copy and modernize business logic layer, preserving algorithms
- [ ] T0[X]6 [FX] [S3] Port API layer: Modernize API/interface layer while maintaining backward compatibility

**Strategy 4: API-First Integration (Service-Oriented)**
- [ ] T0[X]4 [FX] [S4] Create service wrapper: Build REST/GraphQL wrapper around existing legacy system
- [ ] T0[X]5 [FX] [S4] Implement service adapter: Create adapter connecting legacy service to target architecture
- [ ] T0[X]6 [FX] [S4] Plan gradual modernization: Define roadmap for internal service modernization over time

#### [FX] Validation & Integration

- [ ] T0[X]7 [FX] [Validation] Run validation tests: Execute validation tests against migrated feature (MUST PASS)
- [ ] T0[X]8 [FX] [Integration] Integrate with target app: Connect migrated feature to target application infrastructure
- [ ] T0[X]9 [FX] [Testing] Full feature testing: Test complete feature workflow in target environment

---

## Phase 4: Cross-System Integration

**Purpose**: Enable features that span multiple legacy systems, now that individual systems are migrated.

- [ ] T040 [Integration] Cross-system data sharing: Implement data sharing between previously separate legacy systems
- [ ] T041 [Integration] Unified authentication: Integrate all migrated systems with unified authentication system
- [ ] T042 [Integration] Cross-system workflows: Implement workflows that span multiple previously separate systems
- [ ] T043 [Integration] Unified monitoring: Integrate all systems into consolidated monitoring and logging
- [ ] T044 [Performance] Performance optimization: Optimize cross-system performance using consolidated architecture

---

## Phase 5: Legacy System Retirement

**Purpose**: Safely decommission legacy systems after validation and user migration.

- [ ] T050 [Validation] Final validation suite: Run comprehensive validation of all migrated functionality
- [ ] T051 [Migration] User migration plan: Execute plan to migrate users from legacy to new system
- [ ] T052 [Monitoring] Monitor parallel operation: Monitor both systems during parallel operation period
- [ ] T053 [Retirement] Legacy system shutdown: Safely shutdown legacy systems after user migration complete
- [ ] T054 [Archive] Archive legacy systems: Archive legacy codebases and documentation for reference
- [ ] T055 [Documentation] Update documentation: Update all documentation to reflect new unified system
- [ ] T056 [Cleanup] Infrastructure cleanup: Remove legacy infrastructure and dependencies

---

## Implementation Strategies Reference

### Strategy 1: Copy & Modernize (Recommended for Complex Logic)

**Use When**: Complex algorithms, critical business logic, mathematical computations
**Approach**: Copy legacy code exactly, update syntax/framework, preserve business logic

**Steps**:
- Copy legacy file(s) into target framework directory structure
- Replace framework-specific calls (database, HTTP, etc.) with target framework equivalents
- Update syntax (language version, deprecated features) while preserving logic
- Maintain exact same input/output behavior and edge cases

### Strategy 2: Behavior-Driven Rewrite (For Well-Documented Features)

**Use When**: Well-documented features, standard CRUD operations, clear requirements
**Approach**: Reimplement from specifications, ensure behavioral parity

**Steps**:
- Study analysis Section 4 algorithm documentation thoroughly
- Implement feature from scratch using modern patterns and target framework
- Use ground truth tests to validate behavior matches legacy exactly
- Focus on modern, maintainable code while preserving all legacy behaviors

### Strategy 3: Incremental Refactor (For Mixed Simple/Complex Features)

**Use When**: Mix of simple and complex logic, layered architectures
**Approach**: Port in phases (data → logic → API) maintaining exact functionality

**Steps**:
- Phase 1: Port data models and database layer
- Phase 2: Port business logic layer, preserving critical algorithms
- Phase 3: Port API/presentation layer
- Validate each phase independently before proceeding

### Strategy 4: API-First Integration (For Service-Oriented Features)

**Use When**: Microservice candidates, well-defined interfaces, external integrations
**Approach**: Create service wrapper, enable gradual internal modernization

**Steps**:
- Create REST/GraphQL API wrapper around existing system
- Implement service adapter for target architecture integration
- Plan gradual internal modernization without affecting external interface
- Enable parallel development of API consumers

---

**Key Success Criteria**: 
- A task is NOT "done" when code is written - it's "done" when validation tests pass AND migration strategy requirements met
- Each feature can be migrated independently and in parallel (after analysis validation)
- Ground truth tests provide irrefutable behavioral baselines from legacy systems
- No feature proceeds to integration until validation passes AND legacy behavior confirmed preserved
- Migration strategy findings drive implementation decisions and validation criteria