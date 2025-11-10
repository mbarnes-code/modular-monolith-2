---
description: "MTG Commander Map data science pipeline migration to modular monolith"
parent_task: "../tasks.md#T115"
parent_phase: "Phase 5: MTG Domain Migrations" 
return_to: "../tasks.md#T116"
domain: "mtg"
target_service: "apps/mtg-service/src/"
legacy_path: "features/mtg-commander-map"
estimated_hours: 40
---

# Tasks: [MIGRATION: MTG Commander Map]

**⬆️ PARENT TASK**: [`tasks.md#T115`](../tasks.md#T115)  
**⬇️ RETURN TO**: [`tasks.md#T116`](../tasks.md#T116)

---

## Handoff Context

**Called From**: `tasks.md` Phase 5, Task T115  
**Entry Condition**: Phase 1-2 complete, apps/mtg-service/ foundation ready  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark T115 complete in parent `tasks.md`, proceed to T116

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/mtg-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/mtg-commander-map/` accessible
- [ ] Project analysis report completed and validated

4. Confirm all child task completion criteria met
5. Update migration-validation.md with completion status and any notes

**⚠️ Do not return to parent until ALL items above are complete.**

---

## Post-Flight Checklist ✅

**Verify these conditions before marking parent T115 complete**:

- [ ] All T001-T074 tasks marked complete with passing tests
- [ ] UMAP algorithm generates coordinates matching legacy output (within 0.000001 tolerance)
- [ ] HDBSCAN clustering produces identical cluster assignments and defining cards
- [ ] External data integration (Scryfall API + EDHREC) functions correctly with error handling
- [ ] Submap generation produces all archetype-specific maps matching legacy format
- [ ] Full pipeline execution completes within 24-48 hour baseline timeframe
- [ ] Memory usage monitored and stays within 32GB+ cloud deployment requirements
- [ ] Ground truth validation tests pass for all critical algorithms
- [ ] Output CSV/JSON files maintain Lucky Paper website compatibility
- [ ] Production dataset processing validation completed successfully
- [ ] Legacy `features/mtg-commander-map/` safely archived before removal
- [ ] MTG domain knowledge and algorithmic parameter wisdom documented
- [ ] Validation test: `pytest tests/mtg/test_mtg_commander_map_integration.py` passes

**Algorithm Fidelity Validation**:
- [ ] UMAP embedding preserves deck similarity relationships (Jaccard metric)
- [ ] HDBSCAN clustering discovers same number and quality of archetypes
- [ ] Defining cards statistical significance matches legacy binomial calculations
- [ ] Adaptive parameter selection maintains clustering quality across dataset sizes
- [ ] Edge case handling (disconnected decks, memory overflow, too-few-decks) functions identically

**⚠️ If any checklist item fails**: Fix implementation before marking T115 complete in parent `tasks.md`.

---

**Input (Spec)**: Analysis from `modular-analysis-repo-main/reports/mtg-commander-map-analysis.md`  
**Input (Legacy)**: Legacy codebase path `features/mtg-commander-map/`  
**Prerequisites**: `mtg-commander-map-analysis.md` (MANDATORY), plan.md, spec.md

**Project Analysis Integration**: This migration MUST reference specific sections from `mtg-commander-map-analysis.md`:
- Section 2 (Data Architecture) - Commander Deck, Magic Card, and Cluster models
- Section 4 (Business Logic) - CRITICAL UMAP/HDBSCAN algorithms that MUST be preserved exactly
- Section 5 (External Integrations) - Scryfall API and EDHREC data dependencies
- Section 8 (Performance Characteristics) - Memory requirements (32GB+) and runtime baselines
- Section 11 (Domain Knowledge) - MTG Commander format rules and algorithm parameters

**Migration Architecture**: Data Science Processing Service (Category A - Complex Algorithms)
- **Deployment Strategy**: Separate microservice for memory-intensive ML operations
- **Integration Pattern**: Job queue + result storage for async processing
- **Preservation Priority**: 100% algorithmic fidelity - UMAP/HDBSCAN parameters and logic must be identical

**Tests**: Ground Truth validation against existing generated maps is MANDATORY for algorithm preservation.

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

**Purpose**: Validate MTG Commander Map analysis and establish data science processing baseline.

- [ ] T001 [Analysis: Section.1] Validate MTG Commander Map analysis completeness: Confirm CRITICAL algorithms (UMAP, HDBSCAN) and data models documented
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Python data science pipeline (UMAP, HDBSCAN, pandas, numpy, scikit-learn)
- [ ] T003 [P] [Analysis: Section.7.1] Test baseline: Run existing `scripts/test.py` and document algorithm validation coverage
- [ ] T004 [Analysis: Section.8.1] Performance baseline: Measure UMAP embedding (4-8hrs), HDBSCAN clustering (1-3hrs), memory usage (32GB+)
- [ ] T005 [Ground Truth] Setup legacy Docker environment: Build `jcrowdis/commander-map` container for algorithm validation per Section.10.1
- [ ] T006 [Ground Truth] Validate legacy pipeline: Execute full `make-map.sh` workflow and confirm map generation functionality
- [ ] T007 [P] Create `apps/mtg-service/src/commander_map/` module structure for data science pipeline
- [ ] T008 [P] Initialize Python ML dependencies: `umap-learn`, `hdbscan`, `pandas`, `numpy`, `scikit-learn` per analysis Section.1.2

---

## Phase 2: Data Architecture Migration

**Purpose**: Migrate MTG data models for Commander deck analysis pipeline based on Section 2.

- [ ] T009 [Analysis: Section.2.1] Commander Deck model: Implement CommanderDeck class with colorIdentity, commander, partner, tribe, theme, cards, url fields
- [ ] T010 [Analysis: Section.2.1] Magic Card model: Implement MagicCard class with name, mana_cost, cmc, color_identity, type_line, price_usd, earliest_release
- [ ] T011 [P] [Analysis: Section.2.1] Cluster model: Implement DeckCluster with cluster_id, defining_cards, defining_traits, coordinates per ML algorithm needs
- [ ] T012 [Analysis: Section.2.3] In-memory processing: Implement pandas DataFrame patterns and sparse matrix representation for 1.2M+ decks
- [ ] T013 [Ground Truth] Data validation tests: Write tests validating Commander format legality, color identity consistency, card existence
- [ ] T014 [Analysis: Section.2.1] Trait mapping system: Implement `replace_traits_with_ints` function for ML algorithm compatibility per `scripts/calculate.py`

**Checkpoint**: MTG data models support machine learning pipeline processing with 32GB+ memory optimization.

## Phase 3: Data Science Processing Infrastructure

**Purpose**: Core data science pipeline infrastructure for Commander Map generation.

- [ ] T015 [Analysis: Section.3.2] Async job processing: Setup Celery/RQ job queue for memory-intensive UMAP/HDBSCAN operations (no auth needed - batch processing)
- [ ] T016 [Analysis: Section.9.1] Data security: Implement input validation for EDHREC JSON and Scryfall API responses (minimal security - public data)
- [ ] T017 [P] [Analysis: Section.3.2] Processing endpoints: Create job submission and status endpoints for map generation pipeline
- [ ] T018 [Analysis: Section.8.1] Memory monitoring: Implement RAM usage tracking for 32GB+ embedding operations and cloud deployment detection
- [ ] T019 [Analysis: Section.7.1] Ground truth framework: Setup algorithm validation infrastructure comparing generated maps with legacy outputs
- [ ] T020 Configure error handling for memory exhaustion, card validation failures, and clustering edge cases per Section.10.2

**Checkpoint**: Processing infrastructure ready for ML algorithm implementation. NO algorithms implemented yet.

## Phase 4: UMAP Dimensionality Reduction Algorithm 🎯 CRITICAL

**Migration Goal**: Preserve exact UMAP embedding algorithm that reduces 1.2M+ Commander decks from ~20K dimensions to 2D coordinates

**Analysis Reference**: Section.4.1 - UMAP Algorithm (MUST PRESERVE), Section.11.1 - Jaccard Similarity Domain Knowledge

**Independent Test**: Generated 2D coordinates must match legacy output within numerical precision tolerance

### Phase 4a: UMAP Algorithm Analysis & Ground Truth

- [ ] T021 [Analysis: Section.4.1] UMAP algorithm analysis: Review `map_classes.py::CommanderMap.reduce_dimensionality()` implementation details
- [ ] T022 [Analysis: Section.11.1] Domain knowledge: Document Jaccard metric necessity for MTG deck similarity and sparse binary vector optimization  
- [ ] T023 [P] [F1] [Analysis: Section.4.1] [Logic: map_classes.py::reduce_dimensionality] Ground Truth Test: Generate known dataset embedding with legacy algorithm
- [ ] T024 [P] [F1] [Analysis: Section.4.1] [Logic: map_classes.py::reduce_dimensionality] Validation Test: Create coordinate comparison test (initially failing)
- [ ] T025 [Analysis: Section.8.1] Performance baseline: Document UMAP 4-8 hour runtime and 32GB+ memory requirements for 1.2M decks

### Phase 4b: UMAP Implementation & Validation

- [ ] T026 [F1] [Analysis: Section.4.1] [Logic: map_classes.py::reduce_dimensionality] Algorithm preservation: Port exact UMAP parameters (jaccard metric, random_state=0, n_components=2)
- [ ] T027 [F1] [Analysis: Section.4.1] [Logic: map_classes.py::reduce_dimensionality] NaN handling: Implement disconnected deck assignment to nearest commander neighbor + noise
- [ ] T028 [F1] [Analysis: Section.11.2] Edge cases: Handle memory overflow, too-few-decks (<threshold), and sparse matrix optimization
- [ ] T029 [F1] [Analysis: Section.3.2] Processing integration: Wire UMAP algorithm into async job processing pipeline
- [ ] T030 [F1] [Analysis: Section.8.1] Performance validation: Confirm 2D embedding generation meets memory and runtime baselines
- [ ] T031 [F1] Ground truth validation: End-to-end coordinate comparison test - MUST match legacy within 0.000001 tolerance

**Checkpoint**: UMAP dimensionality reduction algorithm migrated with identical mathematical output and performance characteristics.

## Phase 5: HDBSCAN Density-Based Clustering Algorithm 🎯 CRITICAL  

**Migration Goal**: Preserve exact HDBSCAN clustering that identifies natural Commander deck archetypes without predefined categories

**Analysis Reference**: Section.4.1 - HDBSCAN Algorithm (MUST PRESERVE), Section.11.1 - Density-Based Meta Discovery

**Independent Test**: Cluster assignments and defining cards must match legacy output for statistical significance validation

### Phase 5a: HDBSCAN Algorithm Analysis & Ground Truth

- [ ] T032 [Analysis: Section.4.1] HDBSCAN algorithm analysis: Review `map_classes.py::CommanderMap.cluster_decks()` density-based clustering implementation
- [ ] T033 [Analysis: Section.11.1] Clustering domain knowledge: Document min_cluster_size=15, adaptive parameters, and archetype discovery principles
- [ ] T034 [P] [F2] [Analysis: Section.4.1] [Logic: map_classes.py::cluster_decks] Ground Truth Test: Generate known dataset clustering with legacy algorithm
- [ ] T035 [P] [F2] [Analysis: Section.4.1] [Logic: map_classes.py::cluster_decks] Validation Test: Create cluster assignment comparison test

### Phase 5b: HDBSCAN Implementation & Validation

- [ ] T036 [F2] [Analysis: Section.4.1] [Logic: map_classes.py::cluster_decks] Algorithm preservation: Port exact HDBSCAN parameters and min_cluster_size logic
- [ ] T037 [F2] [Analysis: Section.4.1] [Logic: calculate.py::get_parameters] Adaptive parameters: Implement dataset-size-based parameter selection (4-25 neighbors, 4-12 min cluster size)
- [ ] T038 [F2] [Analysis: Section.4.1] Edge case handling: Implement too-few-decks assignment and noise deck nearest-cluster assignment
- [ ] T039 [F2] [Analysis: Section.4.1] Statistical significance: Port defining cards algorithm using binomial distribution for cluster characterization

**Checkpoint**: HDBSCAN clustering algorithm migrated with identical archetype discovery and statistical characterization.

## Phase 6: External Data Integration (Scryfall API + EDHREC Data)

**Migration Goal**: Preserve critical external data dependencies for MTG card validation and deck datasets per Section 5

**Analysis Reference**: Section.5.1 - Scryfall API (CRITICAL), EDHREC Data (CRITICAL)

### Phase 6a: External Data Source Analysis & Testing

- [ ] T040 [Analysis: Section.5.1] Scryfall API integration: Document oracle-cards + default-cards endpoints for card reference data
- [ ] T041 [Analysis: Section.5.1] EDHREC data integration: Document 1.2M+ deck dataset access and preprocessing requirements  
- [ ] T042 [P] [Analysis: Section.5.1] [Logic: card.py::fetch_cards] Scryfall client migration: Port card fetching with double-faced card handling
- [ ] T043 [Analysis: Section.5.1] [Logic: load.py::load_magic_cards] Error handling: Implement network failure and card validation fallbacks

### Phase 6b: Data Pipeline Integration Validation

- [ ] T044 [Analysis: Section.5.1] [Logic: card.py::find_price_and_release] Price/date aggregation: Test card pricing and release date processing across all printings
- [ ] T045 [Analysis: Section.5.1] [Logic: preprocess_data.py] EDHREC preprocessing: Validate deck parsing, card validation, and trait mapping pipeline 
- [ ] T046 [Analysis: Section.5.1] Mapping files: Implement `edhrec-to-scryfall.json` and `duplicates.txt` correction systems for data quality

## Phase 7: Submap Generation & Output Pipeline

**Migration Goal**: Implement per-archetype submap generation and CSV/JSON output matching Lucky Paper website requirements per Section 8

**Analysis Reference**: Section.8.1 - Performance Baselines (12-24hr submap generation), Section 4.1 - Submap Algorithm

### Phase 7a: Submap Algorithm Implementation

- [ ] T047 [Analysis: Section.4.1] [Logic: generate_submaps.py] Submap generation: Port individual archetype map creation with cluster-specific UMAP parameters
- [ ] T048 [Analysis: Section.8.2] Parallelization optimization: Implement multiprocessing for thousands of independent submaps (current bottleneck)
- [ ] T049 [Analysis: Section.4.1] Adaptive parameters: Apply `get_parameters()` scaling for different submap sizes (300-20K+ decks)

### Phase 7b: Output Format & Quality Validation

- [ ] T050 [Analysis: Section.7.1] CSV/JSON export: Generate `commander-map-coordinates.csv`, `trait-mapping.csv`, and cluster definition files
- [ ] T051 [Analysis: Section.7.2] Lucky Paper compatibility: Validate output format matches website consumption requirements  
- [ ] T052 [P] [Analysis: Section.11.2] Edge case handling: Test statistical significance thresholds and cluster quality metrics validation

## Phase 8: MTG Domain Knowledge & Algorithmic Wisdom Preservation  

**Migration Goal**: Capture all MTG Commander format expertise and data science algorithm parameter wisdom per Section 11

**Analysis Reference**: Section.11.1 - MTG Domain Rules, Section.11.2 - Algorithm Parameter Selection Tribal Knowledge

- [ ] T053 [Analysis: Section.11.1] MTG Commander rules: Preserve color identity constraints, legendary commander requirements, and format legality validation
- [ ] T054 [Analysis: Section.11.2] Algorithm quirks: Implement double-faced card name splitting, Scryfall token classification overrides, and parameter sensitivity handling
- [ ] T055 [Analysis: Section.11.3] User workflow preservation: Validate deck similarity browsing, archetype discovery, and meta trend analysis patterns match community expectations  
- [ ] T056 [P] [Analysis: Section.11.2] Parameter documentation: Document why Jaccard > Euclidean, UMAP > t-SNE, HDBSCAN > k-means for Commander deck analysis

## Phase 9: Production Processing Pipeline & Deployment

- [ ] T057 [Analysis: Section.10.2] Cloud processing setup: Configure high-memory (32GB+) instances for UMAP embedding operations
- [ ] T058 [Analysis: Section.10.1] Docker deployment: Implement containerized pipeline matching `jcrowdis/commander-map` production requirements
- [ ] T059 [P] Processing monitoring: Add memory usage tracking, algorithm progress logging, and error notification for 24-48 hour pipeline runs
- [ ] T060 [Analysis: Section.13.1] Algorithm documentation: Document UMAP/HDBSCAN parameter selection wisdom and MTG domain knowledge for future maintenance

## Phase 10: Algorithm Validation & Production Readiness

**Purpose**: Comprehensive validation of data science algorithms before Lucky Paper deployment.

### Phase 10a: Complete Algorithm Validation

- [ ] T061 [Analysis: All Sections] Full algorithm cross-reference: Verify UMAP, HDBSCAN, and submap generation match legacy mathematical outputs
- [ ] T062 [Analysis: Section.4.1] Ground truth parity validation: Confirm generated maps are visually and numerically identical to legacy versions
- [ ] T063 [Analysis: Section.8.1] Performance regression testing: Validate 24-48 hour pipeline runtime and 32GB memory usage within acceptable bounds
- [ ] T064 [Analysis: Section.12.3] Success criteria verification: Confirm clustering quality metrics and defining card statistical significance maintained
- [ ] T065 Verify all algorithmic Logic preservation: Confirm all [Logic: map_classes.py::*, calculate.py::*, etc.] have passing validation tests
- [ ] T066 Run full dataset regression: Execute complete pipeline on production EDHREC data and compare outputs with legacy system

### Phase 10b: Lucky Paper Production Integration

- [ ] T067 [Analysis: Section.12.2] Output format validation: Ensure CSV/JSON files maintain exact compatibility with Lucky Paper website consumption
- [ ] T068 Legacy pipeline backup: Archive `features/mtg-commander-map/` with working Docker environment before removal  
- [ ] T069 Production dataset validation: Run new pipeline on latest EDHREC data and validate map quality with MTG domain experts
- [ ] T070 Lucky Paper team approval: Obtain sign-off on map quality and website integration compatibility
- [ ] T071 Safe legacy retirement: After 100% validation and stakeholder approval, remove `features/mtg-commander-map/` directory

### Phase 10c: Post-Migration Algorithm Monitoring

- [ ] T072 [Analysis: Section.10.2] Processing monitoring: Implement algorithm runtime tracking and memory usage alerts for cloud deployments
- [ ] T073 [Analysis: Section.8.1] Quality baseline tracking: Monitor clustering metrics and defining card statistical significance over time
- [ ] T074 [Analysis: Section.11.3] Community feedback monitoring: Track MTG community reception of map quality and archetype discovery accuracy

### Dependencies & Execution Order

**Sequential Dependencies (Must Complete In Order):**
- **Phase 1 (Analysis Validation)**: Must complete first - validates MTG Commander Map analysis and sets up ground truth environment
- **Phase 2 (Data Architecture)**: Must complete before algorithms - establishes MTG data models and in-memory processing patterns  
- **Phase 3 (Processing Infrastructure)**: Must complete before algorithms - establishes async job processing for memory-intensive operations

**Critical Algorithm Dependencies:**
- **Phase 4 (UMAP Algorithm)**: Must complete before Phase 5 - clustering requires dimensionality-reduced embeddings
- **Phase 5 (HDBSCAN Algorithm)**: Must complete before Phase 7 - submap generation requires cluster assignments
- **Phase 6 (External Data)**: Can run in parallel with Phase 4-5 - data sources needed for full pipeline testing

**Parallel Execution Phases:**
- **Phases 4-6 (UMAP, HDBSCAN, Data Integration)**: Core algorithms can be developed in parallel after Phase 3
- **Phase 7 (Submap Generation)**: Requires Phases 4-5 complete for cluster-based processing
- **Phase 8 (Domain Knowledge)**: Can document throughout all phases  

**Final Sequential Dependencies:**
- **Phase 9 (Production Pipeline)**: Requires all algorithms (Phases 4-7) complete
- **Phase 10 (Validation & Retirement)**: Must be final phase - validates complete system before legacy removal
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

- [ ] All tasks T001-TXXX marked complete above
- [ ] Integration tests pass: `pytest tests/mtg/test_mtg_commander_map_integration.py`
- [ ] Performance baselines met (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm functional parity with legacy
- [ ] Legacy `features/mtg-commander-map/` backed up to `archive/`
- [ ] Migration completion documented in `migration-validation.md`
- [ ] All analysis findings from project_analysis_report.md addressed
- [ ] No regressions in existing functionality
- [ ] Security audit passed (if applicable)
- [ ] Accessibility compliance maintained (WCAG 2.1 AA)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:
1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/mtg/test_mtg_commander_map_integration.py`
3. Document completion in `migration-validation.md`
4. Mark parent task TXXX complete in `tasks.md`
5. Proceed to return task (next in sequence) in `tasks.md`

**Documentation Update Required**:
```markdown
# In migration-validation.md

### MTG Commander Map Migration (TXXX)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: XX
- **Actual Hours**: XX
- **Tests**: X passed, 0 failed
- **Performance**: All baselines met/exceeded
- **Notes**: [Any notable achievements or challenges]
```

