---
description: "CyberChef web-based data analysis and cryptographic operations tool migration"
parent_task: "../tasks.md#T100"
parent_phase: "Phase 5: Security Migrations"
return_to: "../tasks.md#T101"
domain: "security"
target_service: "apps/security-service/src/"
legacy_path: "features/CyberChef"
estimated_hours: 120
total_files: 500+
total_loc: 100721
critical_algorithms: 5
operation_count: 463
migration_type: "hybrid-web-component"
archive_decision: "none - full migration"
integration_strategy: "web-component-wrapper"
---

# Tasks: [MIGRATION: CyberChef]

**⬆️ PARENT TASK**: [`tasks.md#TXXX`](../tasks.md#TXXX)  
**⬇️ RETURN TO**: [`tasks.md#TXXX`](../tasks.md#TXXX)

---

## Handoff Context

**Called From**: `tasks.md` Phase 5, Task T100
**Entry Condition**: Security service foundation ready (Phase 1-4 complete)
**Exit Condition**: All tasks below complete + validation tests pass
**Return Action**: Mark T100 complete in parent `tasks.md`, proceed to T101

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## ⚠️ MIGRATION STRATEGY: WEB COMPONENT INTEGRATION

**CyberChef is a special case**: 100K+ LOC JavaScript codebase with 463 operations maintained by GCHQ.

**Strategic Decision**: **Web Component Wrapper** (NOT full rewrite)

**Rationale**:
1. **Maintenance Burden**: 463 cryptographic operations = thousands of hours to rewrite
2. **Security Risk**: GCHQ-vetted crypto implementations should not be ported without extensive review
3. **Upstream Updates**: Rewriting prevents pulling security patches from upstream
4. **Value Preservation**: All functionality preserved with minimal effort

**Architecture**:
- **Legacy Code**: Preserve CyberChef as-is in `features/CyberChef/` (reference only)
- **Integration Layer**: Web Component wrapper in `apps/security-service/src/cyberchef/`
- **Build System**: Bundle CyberChef via npm package or git submodule
- **Embedding**: `<cyber-chef-tool>` custom element in Jane UI
- **Data Flow**: Jane UI ↔ CyberChef Web Component ↔ CyberChef Core

**What We Migrate**:
- ✅ Integration wrapper (Web Component API)
- ✅ Recipe storage in Jane database
- ✅ User preferences sync
- ✅ Input/output data persistence
- ✅ Authentication integration

**What We DON'T Migrate**:
- ❌ 463 operations (use CyberChef as-is)
- ❌ Core Chef/Recipe/Dish engine (use CyberChef as-is)
- ❌ UI components (embed existing interface)
- ❌ Crypto implementations (maintain GCHQ security review)

**Estimated Hours**: 120 (was 1000+ for full rewrite)

---

## Project Overview

**Project**: CyberChef - The Cyber Swiss Army Knife
**Type**: Web-based data analysis and cryptographic operations tool
**Maintainer**: GCHQ (UK Government Communications Headquarters)
**Users**: 100,000+ security professionals globally
**Repository**: https://github.com/gchq/CyberChef

**Codebase Statistics**:
- Total LOC: 100,721
- Files: 500+
- Operations: 463 cryptographic/encoding/analysis operations
- Languages: JavaScript (ES2020+), HTML/CSS
- Architecture: Client-side SPA (no backend)

**Critical Components**:
1. **Chef Engine** (src/core/Chef.mjs): Recipe execution orchestrator
2. **Recipe System** (src/core/Recipe.mjs): Operation sequence management
3. **Dish Type System** (src/core/Dish.mjs): Automatic type conversion
4. **463 Operations** (src/core/operations/): Crypto, encoding, analysis
5. **Web Interface** (src/web/): Visual recipe builder

**Key Challenges**:
- **Scale**: 100K+ LOC, 463 operations = massive rewrite effort
- **Security**: Cryptographic implementations require expert review
- **Maintenance**: Upstream updates provide security patches
- **Complexity**: Multi-year operation development by security experts

**Value Proposition**:
- **Data Analysis**: Visual workflow builder for security analysts
- **Offline Security**: No data leaves user's machine
- **Recipe Sharing**: Shareable analysis workflows
- **Comprehensive**: 463 operations covering most security analysis needs

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/security-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] CyberChef analysis report validated (Section 1-12 complete)
- [ ] Web Component support in Jane UI confirmed
- [ ] Decision: Web Component wrapper approach approved (NOT full rewrite)
- [ ] Storage: 50 MB provisioned for CyberChef npm package/bundle

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## Migration Strategy: Web Component Integration

**Integration Pattern**: CyberChef as embedded tool via Web Component wrapper

**What This Means**:
- CyberChef remains a standalone JavaScript application
- Jane provides wrapper API for integration
- Recipes stored in Jane database for persistence
- User preferences synced with Jane user settings
- Authentication handled by Jane, passed to CyberChef context

**NOT Migrating Operations**: All 463 operations remain in upstream CyberChef codebase

**Estimated Breakdown**:
- Phase 1-2: Analysis & web component architecture (16h)
- Phase 3: Recipe persistence layer (24h)
- Phase 4: Web component wrapper implementation (32h)
- Phase 5: Data integration & I/O persistence (20h)
- Phase 6: Authentication & user preferences (16h)
- Phase 7: Testing & validation (12h)
- **Total**: 120 hours

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

---

## Phase 1: Analysis Validation & Architecture Design (8 hours)

**Purpose**: Validate CyberChef analysis and design Web Component integration architecture.

- [ ] T001 [Analysis: Section.1] Validate CyberChef analysis completeness: Confirm all sections filled
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate JavaScript/Webpack build system
- [ ] T003 [Analysis: Section.6.1] Frontend architecture review: Understand SPA structure and state management
- [ ] T004 [Ground Truth] Setup CyberChef demo: Run official demo at <https://gchq.github.io/CyberChef/>
- [ ] T005 [Ground Truth] Test core workflows: Recipe creation, save/load, data processing
- [ ] T006 [P] Web Component architecture design: Define wrapper API and integration patterns
- [ ] T007 [P] Integration strategy documentation: Document Web Component vs. full rewrite decision
- [ ] T008 Upstream dependency strategy: Choose npm package vs. git submodule vs. bundled copy

**Checkpoint**: Analysis validated, integration architecture documented.

---

## Phase 2: Build System & Packaging Strategy (8 hours)

**Purpose**: Establish how CyberChef code will be bundled and served.

- [ ] T009 [P] Evaluate CyberChef npm package: Test @gchq/cyberchef npm installation
- [ ] T010 [P] Evaluate build from source: Test Webpack build process from git repository
- [ ] T011 Dependency analysis: Review CyberChef dependencies for conflicts with Jane stack
- [ ] T012 Bundle size optimization: Evaluate code splitting and lazy loading options
- [ ] T013 Build integration: Configure Nx workspace to build/bundle CyberChef
- [ ] T014 [P] Asset serving strategy: Define CDN vs. self-hosted for CyberChef assets
- [ ] T015 Version pinning strategy: Document update process for upstream security patches
- [ ] T016 Security review: Validate GCHQ cryptographic implementations are preserved

**Checkpoint**: CyberChef successfully bundled and servable from Jane infrastructure.

---

## Phase 3: Recipe Persistence Layer (24 hours)

**Purpose**: Store CyberChef recipes in Jane database for user persistence.

### Phase 3a: Data Model Design (8 hours)

- [ ] T017 [Analysis: Section.2.1] Recipe data model design: Define schema for CyberChef recipes
- [ ] T018 [Analysis: Section.2.1] Recipe database schema: Create PostgreSQL tables for recipes
- [ ] T019 Recipe metadata model: User ID, name, description, tags, visibility (public/private)
- [ ] T020 Recipe content model: JSON storage for operation sequence and arguments
- [ ] T021 Recipe versioning: Track recipe modifications and enable rollback
- [ ] T022 Database migrations: Create Alembic migrations for recipe tables
- [ ] T023 [P] Recipe sharing model: Enable public recipe library
- [ ] T024 [P] Recipe import/export: Support CyberChef native format (.recipe files)

### Phase 3b: Recipe API Implementation (16 hours)

- [ ] T025 [Logic: Recipe.mjs::config] Recipe CRUD API: FastAPI endpoints for recipe management
- [ ] T026 POST /api/security/cyberchef/recipes - Create new recipe
- [ ] T027 GET /api/security/cyberchef/recipes - List user recipes
- [ ] T028 GET /api/security/cyberchef/recipes/{id} - Get recipe by ID
- [ ] T029 PUT /api/security/cyberchef/recipes/{id} - Update recipe
- [ ] T030 DELETE /api/security/cyberchef/recipes/{id} - Delete recipe
- [ ] T031 [P] GET /api/security/cyberchef/recipes/public - List public recipe library
- [ ] T032 [P] POST /api/security/cyberchef/recipes/{id}/fork - Fork public recipe
- [ ] T033 Recipe validation: Validate CyberChef recipe JSON format before storage
- [ ] T034 Recipe search: Full-text search on recipe names, descriptions, tags
- [ ] T035 Recipe authorization: Ensure users can only access their own private recipes
- [ ] T036 Recipe testing: Unit tests for all CRUD operations

**Checkpoint**: Recipes stored in Jane database with full CRUD API.

---

## Phase 4: Web Component Wrapper Implementation (32 hours)

**Purpose**: Create Web Component wrapper for CyberChef embedding.

### Phase 4a: Component Architecture (12 hours)

- [ ] T037 [Analysis: Section.6.2] Web Component scaffold: Create `<cyber-chef-tool>` custom element
- [ ] T038 Component lifecycle: Implement connectedCallback, disconnectedCallback, attributeChangedCallback
- [ ] T039 [Logic: Chef.mjs::bake] CyberChef initialization: Load and initialize CyberChef in shadow DOM
- [ ] T040 Shadow DOM setup: Isolate CyberChef styles from Jane UI
- [ ] T041 Component properties: Define input properties (initialRecipe, readOnly, theme, etc.)
- [ ] T042 Component events: Define custom events (recipe-changed, data-processed, error, etc.)
- [ ] T043 [P] Recipe loading interface: Load saved recipes into CyberChef instance
- [ ] T044 [P] Recipe saving interface: Extract current recipe from CyberChef for persistence

### Phase 4b: Data Integration (12 hours)

- [ ] T045 [Logic: Dish.mjs::get] Input data interface: Pass data into CyberChef from Jane
- [ ] T046 [Logic: Dish.mjs::set] Output data interface: Extract results from CyberChef to Jane
- [ ] T047 Data type mapping: Map CyberChef Dish types to Jane data types
- [ ] T048 Binary data handling: Support ArrayBuffer, Blob, File inputs/outputs
- [ ] T049 Large file streaming: Handle files >10MB with progress tracking
- [ ] T050 [P] Data persistence: Save input/output data to Jane database (optional feature)
- [ ] T051 [P] Data history: Track processing history for audit trails

### Phase 4c: UI Integration (8 hours)

- [ ] T052 Theme integration: Pass Jane UI theme (dark/light) to CyberChef
- [ ] T053 Responsive layout: Ensure CyberChef responsive in Jane UI container
- [ ] T054 Toolbar integration: Add Jane-specific toolbar (save recipe, settings, help)
- [ ] T055 Accessibility: Ensure WCAG 2.1 AA compliance for wrapper interactions
- [ ] T056 Loading states: Display spinner during CyberChef initialization
- [ ] T057 Error boundaries: Graceful error handling for CyberChef failures
- [ ] T058 [P] Fullscreen mode: Enable fullscreen CyberChef for complex workflows

**Checkpoint**: Web Component successfully embeds CyberChef with data I/O.

---

## Phase 5: Data Integration & I/O Persistence (20 hours)

**Purpose**: Connect CyberChef to Jane's data ecosystem.

### Phase 5a: Input Source Integration (10 hours)

- [ ] T059 [Analysis: Section.5.2] File upload integration: Upload files to Jane → CyberChef
- [ ] T060 Database query results: Load data from PostgreSQL queries into CyberChef
- [ ] T061 API response integration: Pipe API responses directly into CyberChef
- [ ] T062 Clipboard integration: Paste data from Jane UI into CyberChef
- [ ] T063 [P] Data source picker: UI for selecting input data source
- [ ] T064 [P] Multi-file processing: Batch process multiple files through same recipe

### Phase 5b: Output Destination Integration (10 hours)

- [ ] T065 [Logic: Chef.mjs::bake] Save results to database: Store CyberChef output in PostgreSQL
- [ ] T066 Download results: Export CyberChef output as files
- [ ] T067 Copy to clipboard: Copy results to Jane UI clipboard
- [ ] T068 Send to another tool: Pipe CyberChef output to other security tools
- [ ] T069 [P] Output history: Track all processing results for audit
- [ ] T070 [P] Result comparison: Compare multiple recipe outputs side-by-side

**Checkpoint**: CyberChef fully integrated with Jane's data flows.

---

## Phase 6: Authentication & User Preferences (16 hours)

**Purpose**: Sync CyberChef with Jane's user management system.

### Phase 6a: Authentication Integration (8 hours)

- [ ] T071 [Analysis: Section.3.1] User context: Pass Jane user ID to CyberChef wrapper
- [ ] T072 Session management: Maintain CyberChef state per user session
- [ ] T073 Recipe ownership: Associate recipes with Jane user accounts
- [ ] T074 [P] Shared recipe permissions: Enable recipe sharing between users
- [ ] T075 [P] Public recipe library: Global recipe repository with attribution

### Phase 6b: User Preferences Sync (8 hours)

- [ ] T076 [Analysis: Section.6.1] Theme preference: Sync dark/light mode with Jane settings
- [ ] T077 Auto-bake preference: Sync CyberChef auto-bake setting with Jane preferences
- [ ] T078 Default input/output formats: Store user-preferred data formats
- [ ] T079 Recipe favorites: Enable starring/favoriting recipes
- [ ] T080 Recent recipes: Track recently used recipes per user
- [ ] T081 Preference storage: Store CyberChef settings in Jane user preferences table
- [ ] T082 [P] Workspace layouts: Save/restore CyberChef UI layout preferences

**Checkpoint**: CyberChef personalized per Jane user.

---

## Phase 7: Testing & Validation (12 hours)

**Purpose**: Comprehensive testing of CyberChef integration.

### Phase 7a: Functional Testing (6 hours)

- [ ] T083 [Ground Truth] Recipe execution parity: Verify recipes execute identically in wrapper
- [ ] T084 [Analysis: Section.4.1] Critical operations testing: Test top 20 most-used operations
- [ ] T085 Recipe save/load testing: Verify recipe persistence and retrieval
- [ ] T086 Data I/O testing: Test all input sources and output destinations
- [ ] T087 [P] Multi-user testing: Verify recipe isolation between users
- [ ] T088 [P] Large file testing: Test files up to 100MB

### Phase 7b: Integration & Performance Testing (6 hours)

- [ ] T089 [Analysis: Section.8.1] Performance baseline: Measure recipe execution performance
- [ ] T090 Component load time: Ensure <2s initial load for CyberChef wrapper
- [ ] T091 Memory leak testing: Verify no memory leaks during extended use
- [ ] T092 Error handling: Test graceful degradation for all error scenarios
- [ ] T093 Cross-browser testing: Validate Chrome, Firefox, Safari, Edge
- [ ] T094 Accessibility testing: WCAG 2.1 AA compliance validation
- [ ] T095 Security testing: Validate no XSS vulnerabilities in recipe storage
- [ ] T096 [P] End-to-end workflows: Test complete analyst workflows

**Checkpoint**: CyberChef integration fully tested and validated.

---

## Phase 8: Documentation & Knowledge Preservation (8 hours)

**Purpose**: Document integration for maintenance and troubleshooting.

- [ ] T097 [Analysis: Section.11.1] Integration architecture documentation: Document Web Component design
- [ ] T098 Recipe API documentation: OpenAPI spec for recipe endpoints
- [ ] T099 User guide: Document how to use CyberChef in Jane UI
- [ ] T100 Developer guide: Document how to update CyberChef upstream version
- [ ] T101 Security considerations: Document cryptographic implementation preservation
- [ ] T102 Troubleshooting guide: Common issues and resolutions
- [ ] T103 [P] Recipe library curation: Create starter recipe collection
- [ ] T104 [P] Video tutorials: Screen recordings for common workflows

**Checkpoint**: Comprehensive documentation for users and developers.

---

## Phase 9: Migration Validation & Deployment (8 hours)

**Purpose**: Final validation before production deployment.

### Phase 9a: Complete Validation

- [ ] T105 [Analysis: All Sections] Full analysis cross-reference: Verify all requirements addressed
- [ ] T106 [Analysis: Section.12.3] Success criteria verification: Confirm all criteria met
- [ ] T107 Recipe functionality: Validate all recipe features work in wrapper
- [ ] T108 [Analysis: Section.8.1] Performance validation: Confirm <10% performance overhead
- [ ] T109 Security review: Final cryptographic implementation validation
- [ ] T110 User acceptance testing: Test with actual security analysts

### Phase 9b: Deployment & Monitoring

- [ ] T111 Production deployment: Deploy CyberChef integration to production
- [ ] T112 [Analysis: Section.10.2] Monitoring setup: Track usage, errors, performance
- [ ] T113 User feedback collection: Establish feedback mechanism
- [ ] T114 Upstream update process: Document procedure for pulling CyberChef updates
- [ ] T115 Rollback plan: Document emergency rollback procedure

**Checkpoint**: CyberChef integration deployed to production.

---

- [ ] T044 [Analysis: Section.5.1] Service connectivity: Test all external integrations
- [ ] T045 [Analysis: Section.5.2] Authentication provider testing: Validate OAuth/SSO flows
- [ ] T046 [Analysis: Section.5.1] Caching strategy: Implement analysis-documented caching patterns

## Phase 7: Performance & Quality Assurance

**Migration Goal**: Meet or exceed baseline performance per Analysis Section.8

**Analysis Reference**: Section.8.1 - Performance Baselines, Section.7.1 - Test Coverage

### Phase 7a: Performance Validation

- [ ] T047 [Analysis: Section.8.1] Performance benchmarking: Measure new implementation against baselines
- [ ] T048 [Analysis: Section.8.2] Bottleneck analysis: Ensure no performance regressions
- [ ] T049 [Analysis: Section.8.3] Scalability testing: Validate scaling characteristics maintained

### Phase 7b: Quality Assurance

- [ ] T050 [Analysis: Section.7.1] Test coverage parity: Achieve analysis-documented coverage levels
- [ ] T051 [Analysis: Section.7.2] Critical test preservation: Migrate all critical test scenarios
- [ ] T052 [P] [Analysis: Section.11.2] Edge case validation: Test all documented quirks and workarounds

## Phase 8: Domain Knowledge Preservation

**Migration Goal**: Capture all tribal knowledge per Analysis Section.11

**Analysis Reference**: Section.11.1 - Business Domain, Section.11.2 - Undocumented Knowledge


## Post-Flight Checklist ✅

**Verify these conditions before marking parent task complete**:

1. Mark all checkboxes above ✅
2. All validation tests pass ✅
3. Post-flight validation complete ✅

**Migration Validation Template**:

```markdown
## CyberChef Integration Validation Report

**Integration Date**: [YYYY-MM-DD]
**Validator**: [Name]

### Web Component Architecture
- [ ] CyberChef bundle integrated (npm/@gchq/cyberchef or build)
- [ ] Web Component `<cyber-chef-tool>` functional
- [ ] Shadow DOM isolation working
- [ ] Component lifecycle methods operational

### Recipe Persistence
- [ ] Recipe database schema migrated
- [ ] All CRUD endpoints functional
- [ ] Recipe save/load working
- [ ] Public recipe library accessible
- [ ] Recipe search operational

### Data Integration
- [ ] Input data sources: file upload, database, API, clipboard
- [ ] Output destinations: database, download, clipboard, other tools
- [ ] Binary data handling (ArrayBuffer, Blob, File)
- [ ] Large file streaming (>10MB) with progress

### User Integration
- [ ] Authentication: Jane user context passed
- [ ] User preferences synced (theme, auto-bake, formats)
- [ ] Recipe ownership enforced
- [ ] Recipe sharing permissions working
- [ ] Recent recipes tracking

### Testing Results
- [ ] Recipe execution parity validated
- [ ] Top 20 operations tested
- [ ] Performance <10% overhead
- [ ] Component load time <2s
- [ ] Cross-browser validation (Chrome, Firefox, Safari, Edge)
- [ ] Accessibility WCAG 2.1 AA compliant
- [ ] Security: No XSS vulnerabilities

### Documentation
- [ ] Integration architecture documented
- [ ] Recipe API OpenAPI spec
- [ ] User guide created
- [ ] Developer guide (upstream updates)
- [ ] Troubleshooting guide

### Production Readiness
- [ ] Deployed to production
- [ ] Monitoring configured
- [ ] User feedback mechanism established
- [ ] Upstream update process documented
- [ ] Rollback plan documented

**Critical Success Metrics**:
- Recipe functionality: 100% preserved
- Performance overhead: <10%
- Component load time: <2s
- User preferences: 100% synced
- 463 operations: Available (via embedded CyberChef)
- GCHQ crypto implementations: Preserved (no modification)

**Upstream Maintenance**:
- CyberChef version: [e.g., v10.5.2]
- Update frequency: [Quarterly security patches recommended]
- Last upstream check: [YYYY-MM-DD]
```

**Migration Strategy Notes**:

This migration uses the **Web Component Wrapper** pattern, NOT a full rewrite:

- **Value**: All 463 operations preserved without porting
- **Security**: GCHQ cryptographic implementations unchanged
- **Maintainability**: Upstream security patches can be pulled
- **Effort**: 120 hours vs. 1000+ for full rewrite
- **Risk**: Minimal - integration layer only, core CyberChef unchanged

**Archive Decision**: NO ARCHIVE - CyberChef remains as upstream dependency, not legacy code.

**Return to Parent**: After validation complete, mark T100 in `tasks.md` complete and proceed to T101.

---

- [ ] All tasks T001-TXXX marked complete above
- [ ] Integration tests pass: `pytest tests/security/test_cyberchef_integration.py`
- [ ] Performance baselines met (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm functional parity with legacy
- [ ] Legacy `features/cyberchef/` backed up to `archive/`
- [ ] Migration completion documented in `migration-validation.md`
- [ ] All analysis findings from project_analysis_report.md addressed
- [ ] No regressions in existing functionality
- [ ] Security audit passed (if applicable)
- [ ] Accessibility compliance maintained (WCAG 2.1 AA)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:
1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/test_cyberchef_integration.py`
3. Document completion in `migration-validation.md`
4. Mark parent task TXXX complete in `tasks.md`
5. Proceed to return task (next in sequence) in `tasks.md`

**Documentation Update Required**:
```markdown
# In migration-validation.md

### CyberChef Migration (TXXX)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: XX
- **Actual Hours**: XX
- **Tests**: X passed, 0 failed
- **Performance**: All baselines met/exceeded
- **Notes**: [Any notable achievements or challenges]
```

