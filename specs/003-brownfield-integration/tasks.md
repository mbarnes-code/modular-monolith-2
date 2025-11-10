# Tasks: MIGRATION - Brownfield Integration Mental Prosthetic Platform

**EXTERNAL REFERENCES**:

- Requirements: `specs/003-brownfield-integration/spec.md`
- Architecture: `specs/003-brownfield-integration/plan.md`
- Migration Strategy: `specs/003-brownfield-integration/migration-strategy.md`

## 🎯 PROJECT SCALE ASSESSMENT

**MANDATORY FIRST STEP**: Determine project scale to apply appropriate risk assessment and methodology.

### Project Scale Classification

**Count your projects and select the appropriate scale:**

- [ ] **🟢 SMALL SCALE (1-3 projects)**: Standard brownfield migration
- [ ] **🟡 MEDIUM SCALE (4-10 projects)**: Complex brownfield migration  
- [ ] **🔴 LARGE SCALE (11+ projects)**: Enterprise brownfield integration
- [x] **🚨 EXTREME SCALE (25+ projects)**: Platform consolidation

**YOUR PROJECT SCALE**: EXTREME (37 executive function tools)

### Scale-Specific Characteristics

```yaml
Extreme Scale (37 projects):
  Risk Level: EXTREME
  Timeline: 24+ weeks with extensive validation
  Team Size: 12+ highly specialized developers across diverse stacks
  Architecture: Platform architecture with extensive domain isolation
  Technology: Highly diverse ecosystem requiring extensive isolation
  Organization: Major organizational transformation requirements
```

**Migration Type**: BROWNFIELD Asset Relocation - 37 existing tools with preserved business logic
**Input**: Legacy codebase analysis from `/specs/003-brownfield-integration/modular-analysis-repo-main/`

---

## 🚨 EXTREME SCALE RISK ASSESSMENT

**USER APPROVAL REQUIRED**: Risk assessment for 37+ system platform consolidation.

### ⚠️ EXTREME SCALE (37 projects) - Extreme Risks

#### 🔴 EXTREME RISK: Platform-Level Data Loss & Corruption

- **Risk**: Data conversion across 37 projects with highly diverse schemas and formats
- **Evidence**: 18 PostgreSQL, 8 SQLite, 4 MySQL, 2 MongoDB, plus binary/CRDT data
- **Impact**: Catastrophic data loss potential across executive function workflows
- **Mitigation**: Enterprise backup strategy, phased migration with domain isolation, extensive test environments using existing 3,795 test files
- **USER DECISION REQUIRED**: Accept risk of platform-scale data migration? [Y/N]

#### 🔴 EXTREME RISK: Security Model Consolidation  

- **Risk**: 13 different security tools with distinct threat models being unified
- **Evidence**: MISP (threat intel), SecurityOnion (network monitoring), YARA-X (malware detection) with different security paradigms
- **Impact**: Major security vulnerabilities during consolidation, potential compliance violations
- **Mitigation**: Domain isolation for security tools, extensive penetration testing, gradual rollout per CHK022 framework
- **USER DECISION REQUIRED**: Accept platform security consolidation risks? [Y/N]

#### 🔴 EXTREME RISK: Technology Ecosystem Compatibility

- **Risk**: Diverse technology ecosystem requiring extensive isolation (Python, Node.js, Rust, PHP, etc.)
- **Evidence**: 37 different runtime environments, 8 CSS frameworks, multiple database engines
- **Impact**: Architectural complexity, potential runtime conflicts, long-term maintenance challenges
- **Mitigation**: Domain isolation architecture with microservice containers for Category A algorithms
- **USER DECISION REQUIRED**: Accept ecosystem integration complexity? [Y/N]

#### 🔴 HIGH RISK: Business Logic Preservation

- **Risk**: Preserving complex algorithms across 37 tools without functionality loss
- **Evidence**: MISP correlation (8,733 lines), n8n workflows (2,620 lines), CyberChef operations (300+)
- **Impact**: Loss of critical executive function capabilities, workflow disruption
- **Mitigation**: Category A/B/C preservation strategies, comprehensive regression testing framework
- **USER DECISION REQUIRED**: Accept business logic preservation complexity? [Y/N]

### 📋 EXTREME SCALE APPROVAL CHECKLIST

**BEFORE PROCEEDING, USER MUST EXPLICITLY APPROVE:**

- [ ] **Platform Data Migration Risk**: I accept extreme risk of data conversion across 37 diverse systems with comprehensive backup strategies
- [ ] **Enterprise Security Consolidation**: I approve platform-level security consolidation with extensive validation and domain isolation
- [ ] **Technology Ecosystem Integration**: I accept highly complex technology integration with extensive isolation strategies  
- [ ] **Business Logic Preservation**: I accept complexity of preserving 37 different algorithmic systems with regression testing
- [ ] **Enterprise Team Requirements**: I can provide 12+ specialized developers across multiple technology stacks for 24+ weeks
- [ ] **Extended Timeline**: I accept 24+ week timeline with complex project management and validation requirements
- [ ] **Platform Architecture Complexity**: I understand platform architecture with extensive domain isolation requirements
- [ ] **Organizational Transformation**: I accept major organizational transformation from 37 separate tools to unified platform
- [ ] **Executive Function Impact**: I understand potential temporary impact on executive function workflows during migration
- [ ] **Constitutional Compliance**: I accept requirements for 100% functionality preservation and constitutional quality standards

**REQUIRED USER INPUT**: Type "I ACCEPT EXTREME SCALE PLATFORM INTEGRATION RISKS" to proceed.

### 🤔 EXTREME SCALE ALTERNATIVE APPROACHES

#### 1. Enterprise Phased Approach (Recommended)

- **Phase 1**: Pilot with 3-5 highest priority tools (8-12 weeks)
- **Phase 2**: Domain-by-domain integration (12-16 weeks per domain)
- **Phase 3**: Platform unification (8-16 weeks)
- **Choose this for**: Enterprise risk management, validation-driven approach

#### 2. Technology Ecosystem Approach

- **Phase 1**: Python ecosystem integration (12-20 weeks)  
- **Phase 2**: JavaScript ecosystem integration (12-20 weeks)
- **Phase 3**: Isolated technology bridges (8-12 weeks)
- **Choose this for**: Technology-focused consolidation, stack standardization

#### 3. Business Domain Approach (SELECTED)

- **Phase 1**: Security domain (16-20 weeks) - Critical for threat monitoring
- **Phase 2**: Infrastructure domain (12-16 weeks) - Platform foundation
- **Phase 3**: Productivity domain (12-16 weeks) - Executive function core
- **Phase 4**: TCG domain (8-12 weeks) - Specialized tools
- **Choose this for**: Business-focused consolidation matching user workflows

#### 4. Federation Platform Approach

- **Create**: Enterprise API platform with microservice architecture
- **Preserve**: All individual projects with unified platform layer  
- **Timeline**: 12-20 weeks for platform layer only
- **Choose this for**: Minimal disruption to existing tools

**USER DECISION**: BUSINESS DOMAIN APPROACH (Security → Infrastructure → Productivity → TCG)

---

## Brownfield Asset Relocation Context

**Critical Success Factor**: This is NOT a greenfield project. We are migrating 37 existing, working tools with specific algorithms, data structures, and business logic that MUST be preserved exactly.

**Existing Assets**:

- **3,795 test files** providing validation baseline
- **37 analyzed tools** with documented business logic in modular-analysis-repo-main/reports/
- **Category A/B/C classification** for preservation strategies
- **Asset Relocation Process** defined in consolidated-business-logic-analysis.md

**User Stories**: 5 user stories focused on integration validation and functionality preservation

**Technology Stack**:

- **Backend**: Python 3.12 + FastAPI (unified backend)
- **Frontend**: TypeScript/Next.js 14+ (unified frontend)
- **Database**: PostgreSQL (primary), SQLite (local-first), Redis (caching)
- **AI Integration**: vLLM server, ChromaDB, MCP protocol
- **Architecture**: Modular monolith with domain boundaries (Security, Productivity, TCG, Infrastructure)

**Performance Requirements**: Domain-specific tiers - Security <1s, Productivity <2s, TCG <3s, Infrastructure <5s, UI <200ms

## Task Organization Strategy

Tasks are organized by user story to enable independent implementation and testing. Each phase represents a complete, independently testable increment with clear acceptance criteria.

**Migration Sequence**: Setup → Foundational → User Story 1 (P1) → User Story 2 (P1) → User Story 3 (P2) → User Story 4 (P2) → User Story 5 (P3) → Polish

**Validation Framework**: Each user story includes regression testing against original tools, performance validation, and business logic preservation verification using existing tests/ directory infrastructure.

## Task Format

- **Checkbox**: `- [ ]` (markdown checkbox)
- **Task ID**: Sequential number (T001, T002, T003...)
- **[P] marker**: Parallelizable tasks (different files, no dependencies)
- **[Story] label**: User story association ([US1], [US2], etc.)
- **Description**: Clear action with exact file path

---

## Phase 0: Pre-Migration Validation & Risk Mitigation (Week 1)

**Purpose**: MANDATORY brownfield validation before any migration work begins

### Phase 0a: Legacy System Health Assessment & Ground Truth Testbed

- [ ] T001 **[CRITICAL]** Validate all 37 tools operational status: Execute health checks on every tool to establish baseline functionality
- [ ] T002 **[CRITICAL]** Execute comprehensive backup of all 37 systems: Full data, configuration, and state backup with verification
- [ ] T003 **[CRITICAL]** Document current system dependencies: Map all external dependencies, APIs, and service interconnections
- [ ] T004 **[CRITICAL]** **[Ground Truth]** Setup legacy testbed environment: Create Docker containers and test environments for all 37 original tools to run ground-truth tests per template requirement
- [ ] T005 **[CRITICAL]** Validate existing test infrastructure: Confirm all 3,795 test files execute successfully on current systems with documented baselines

### Phase 0b: Migration Risk Validation & Ground Truth Baseline

- [ ] T006 **[RISK MITIGATION]** Create rollback procedures for each tool: Document 15-minute recovery processes in docs/operations/rollback/ per constitutional requirement
- [ ] T007 **[RISK MITIGATION]** **[Ground Truth]** Establish monitoring baselines: Capture current performance metrics for all 37 tools in tests/baselines/ with automated baseline comparison framework
- [ ] T008 **[RISK MITIGATION]** Validate data export capabilities: Test data extraction from all databases and file systems with validation scripts in scripts/data-export/
- [ ] T009 **[RISK MITIGATION]** Create migration communication plan: User notification strategy for executive function workflow impacts
- [ ] T010 **[Ground Truth]** Create comprehensive Ground Truth test suite: Document expected behavior and outputs from all 37 tools in tests/ground-truth/ using existing 3,795 test files as validation baseline

### Phase 0c: Technical Debt Pre-Assessment

- [ ] T011 **[TECHNICAL DEBT]** Execute security vulnerability scan across all 37 tools per plan.md Strategy 3
- [ ] T012 **[TECHNICAL DEBT]** Identify critical security patches required before migration per CHK047-CHK048
- [ ] T013 **[TECHNICAL DEBT]** Document configuration drift across similar tools per consolidated-technical-debt-analysis.md

**Phase 0 Checkpoint**: All T001-T013 must complete successfully before proceeding to Phase 1. Legacy testbed must be fully operational with documented Ground Truth baselines.

---

## Phase 1: Foundation & Analysis Validation (Weeks 2-3)

**Purpose**: Establish development environment, validate analysis findings, create unified project structure, and connect to legacy testbed for Ground Truth validation

### Phase 1a: Legacy Analysis Validation & Ground Truth Connection

- [ ] T014 **[BROWNFIELD ANALYSIS]** Validate consolidated analysis reports completeness: Verify all 37 tools have analysis reports in modular-analysis-repo-main/reports/
- [ ] T015 **[BROWNFIELD ANALYSIS]** Cross-reference analysis reports with live systems: Validate documented business logic matches actual tool behavior using Ground Truth testbed
- [ ] T016 **[Ground Truth]** Connect new project to legacy testbed: Establish testing connection between new unified platform and original 37 tools for validation
- [ ] T017 **[Ground Truth]** Create validation test framework: Setup automated comparison testing between original and migrated functionality per template requirement

### Phase 1b: New Project Scaffolding (Foundation Infrastructure)

- [ ] T018 Create unified project structure: Initialize apps/jane-orchestrator/ (FastAPI backend) and apps/jane-ui/ (React frontend) per plan.md
- [ ] T019 [P] Setup development environment: Configure Docker Compose, Node.js 20, Python 3.12, PostgreSQL, Redis per constitutional tech stack
- [ ] T020 [P] Initialize backend framework: Create FastAPI application structure with domain routing (security, productivity, tcg, infrastructure)
- [ ] T021 [P] Initialize frontend framework: Create React/Next.js application with TypeScript strict mode and executive function UI accommodations
- [ ] T022 Create shared libraries structure: Initialize libs/shared/, libs/ui/, libs/service-adapters/ for cross-domain utilities
- [ ] T023 [P] Configure linting and formatting tools: Setup ruff, black, eslint, prettier per constitutional code quality standards
- [ ] T024 [P] Setup error handling and logging infrastructure: Configure structured logging with performance monitoring integration

### Phase 1c: Dependency Hoisting & Baseline Files (Critical Foundation)

**Purpose**: Consolidate 1,076 scattered configuration files into unified workspace baseline per features-file-enumeration.md analysis

#### Phase 1c1: Root Workspace Baseline Files (Consolidating 432 unique extensions)

- [ ] T025 **[DEPENDENCY HOISTING]** Create root Node.js workspace: Consolidate 96 package.json files into single workspace package.json with NX orchestration for TypeScript ecosystem (31.48% of files)
- [ ] T026 **[DEPENDENCY HOISTING]** Create unified lock file: Replace 33 scattered lock files (package-lock.json, yarn.lock, pnpm-lock.yaml) with single pnpm-lock.yaml for dependency management
- [ ] T027 **[DEPENDENCY HOISTING]** Create root TypeScript config: Consolidate TypeScript configurations into tsconfig.base.json supporting all 11,303 TypeScript files across tools
- [ ] T028 **[DEPENDENCY HOISTING]** Create NX workspace config: Setup nx.json with project graph for 37 tools migration and build orchestration
- [ ] T029 **[DEPENDENCY HOISTING]** Create root Python workspace: Consolidate 55 requirements.txt + 19 pyproject.toml into unified Poetry workspace for Python ecosystem (12.64% of code files)
- [ ] T030 **[DEPENDENCY HOISTING]** Create unified linting config: Consolidate 155 linting/format files (.eslintrc, .prettierrc, .editorconfig) into workspace standards
- [ ] T031 **[DEPENDENCY HOISTING]** Create consolidated .gitignore: Merge 112 separate .gitignore files into unified workspace ignore patterns

#### Phase 1c2: Domain-Specific Configuration Hoisting

- [ ] T032 **[SECURITY DOMAIN CONFIG]** Create security domain baseline: Setup apps/security-service/ configuration for 18,467 files (Python-heavy with C/C++ tools)
- [ ] T033 **[PRODUCTIVITY DOMAIN CONFIG]** Create productivity domain baseline: Setup apps/productivity-service/ configuration for 20,276 files (TypeScript-heavy with n8n monorepo)
- [ ] T034 **[INFRASTRUCTURE DOMAIN CONFIG]** Create infrastructure domain baseline: Setup apps/infrastructure-service/ configuration for 6,785 files (mixed technology stack)
- [ ] T035 **[MTG DOMAIN CONFIG]** Create MTG domain baseline: Setup apps/mtg-service/ configuration for 745 files (simple Next.js + Python stack)

#### Phase 1c3: Build System Consolidation

- [ ] T036 **[DOCKER CONSOLIDATION]** Create unified Docker strategy: Consolidate 71 Dockerfiles and 24 docker-compose files into multi-stage base containers per domain
- [ ] T037 **[BUILD CONSOLIDATION]** Create unified Makefile: Consolidate 17 scattered Makefiles into root workspace build coordination
- [ ] T038 **[RUST WORKSPACE]** Create Rust workspace: Consolidate 25 Cargo.toml files into unified Cargo workspace for Rust tools (yara-x, goose components)
- [ ] T039 **[C/C++ BUILD SYSTEM]** Create C/C++ build integration: Unify 22 CMakeLists.txt files into consolidated build system for systems programming tools

#### Phase 1c4: Service Adapter Framework (Supporting 432 unique file extensions)

- [ ] T040 **[SERVICE ADAPTER]** Create Node.js adapter framework: Setup libs/service-adapters/node-adapter/ for TypeScript/JavaScript tools integration
- [ ] T041 **[SERVICE ADAPTER]** Create Python adapter framework: Setup libs/service-adapters/python-adapter/ for Python tools integration  
- [ ] T042 **[SERVICE ADAPTER]** Create Rust adapter framework: Setup libs/service-adapters/rust-adapter/ for Rust tools (yara-x) integration
- [ ] T043 **[SERVICE ADAPTER]** Create C/C++ adapter framework: Setup libs/service-adapters/cpp-adapter/ for systems tools (meterpreter) integration
- [ ] T044 **[SERVICE ADAPTER]** Create binary tools adapter: Setup libs/service-adapters/binary-adapter/ for binary tools (blackarch) integration

#### Phase 1c5: Configuration Migration Validation

- [ ] T045 **[CONFIG VALIDATION]** Validate dependency hoisting: Test that consolidated configurations work with all 37 tools' original functionality
- [ ] T046 **[BASELINE TESTING]** Test workspace baseline files: Validate root workspace package.json, nx.json, and domain configurations build successfully
- [ ] T047 **[ADAPTER TESTING]** Test service adapter framework: Validate that all service adapters can interface with their target tools
- [ ] T048 **[CONSOLIDATION METRICS]** Measure consolidation success: Validate 97% configuration reduction (1,076 → ~36 baseline files) achievement per enumeration analysis

### Phase 1d: Brownfield Testing Infrastructure

- [ ] T049 **[BROWNFIELD TESTING]** Setup regression testing framework: Configure automated comparison between original tools and integrated versions in tests/regression/
- [ ] T050 [P] Configure CI/CD pipeline: Setup GitHub Actions with brownfield-specific validation steps per existing test infrastructure
- [ ] T051 **[BASELINE PRESERVATION]** Establish performance baselines: Document current performance characteristics from 37 individual tools per domain-specific tiers
- [ ] T052 Setup monitoring infrastructure: Configure performance monitoring for constitutional <200ms UI, domain-specific API response requirements with baseline comparison

**Phase 1 Checkpoint**: Foundation ready. NO business logic exists. Legacy testbed connected and validation framework operational.

---

## Phase 2: Data Architecture & Authentication Foundation (Weeks 4-5)

**Purpose**: Migrate database schemas from 37 tools into unified PostgreSQL schema with Redis caching, implementing shared authentication and session management following Ground Truth → Port → Validate → Integrate loop

### Phase 2a: Legacy Data Ground Truth & Validation (Write These First)

- [ ] T053 **[Ground Truth]** [CHK041] Create Ground Truth data tests: Document expected data behavior from original 37 tools with specific schema validation and data integrity tests
- [ ] T054 **[Ground Truth]** [CHK041] Analyze legacy data formats: Extract schemas from 18 PostgreSQL, 8 SQLite, 4 MySQL, 2 MongoDB projects per consolidated-technology-stack-inventory.md with documented baselines
- [ ] T055 **[Validation Test]** [CHK041] Create data conversion validation tests: Design validation tests for unified PostgreSQL schema that must fail initially until conversion is complete
- [ ] T056 **[BROWNFIELD DATA]** [CHK041] Create data preservation matrix: Document critical data relationships and constraints across all 37 tools with Ground Truth validation

### Phase 2b: Data Format Porting & Migration Planning

- [ ] T057 **[BROWNFIELD DATA]** [CHK041] Create format conversion strategies: Design migration paths for CRDT (Actual Budget), NoSQL (MongoDB tools), time-series (HELK), binary data (YARA-X)
- [ ] T058 [P] [CHK041] **[Logic: various::database_schemas]** Implement data format converters: Create conversion utilities for MySQL→PostgreSQL, MongoDB→PostgreSQL, complex CRDT preservation
- [ ] T059 **[DATA VALIDATION]** Create data integrity checksum system: Implement validation framework for data preservation during migration
- [ ] T060 **[Run Validation]** Test data conversion validation: Run validation tests (T055) against converted data - must pass before proceeding

### Phase 2c: Unified Schema Design & Integration

- [ ] T061 **[SCHEMA DESIGN]** Design unified database schema: Create consolidated PostgreSQL schema with domain separation supporting all 37 tools per Ground Truth requirements
- [ ] T062 **[LEGACY COMPAT]** Create legacy data adapters: Build compatibility layer for existing data access patterns during transition
- [ ] T063 [P] **[Logic: various::data_models]** Implement core data models: Create SQLAlchemy models for User Profile, Integrated Tool, Platform Session, AI Enhancement Context
- [ ] T064 [P] Setup Redis caching layer: Configure Redis for session management, cross-tool state, and performance optimization with existing data patterns
- [ ] T065 **[Integration Test]** Test unified schema integration: Validate that all 37 tools can access data through new unified schema while maintaining functionality

### Phase 2d: Authentication Consolidation Ground Truth → Port → Validate → Integrate

- [ ] T066 **[Ground Truth]** **[Logic: various::authentication]** Document existing authentication patterns: Capture current login flows and user management from all 37 tools with Ground Truth tests
- [ ] T067 **[AUTH MIGRATION]** **[Logic: various::auth_systems]** Implement unified authentication: Create JWT-based authentication system replacing 37 separate login requirements per FR-008
- [ ] T068 **[USER MIGRATION]** Create user preferences system: Implement unified user profile supporting ADHD/autism accommodations and customizations per FR-013
- [ ] T069 **[USER MIGRATION]** **[Logic: various::user_accounts]** Migrate existing user accounts: Consolidate user identities from tools with authentication systems while preserving access patterns
- [ ] T070 [P] [CHK044] **[Logic: various::session_mgmt]** Implement concurrent access control: Create session management for single-user tools (CyberChef, IT-Tools, KasmVNC) with conflict resolution
- [ ] T071 **[Run Validation]** Test authentication consolidation: Validate unified auth system maintains access patterns and user data integrity from Ground Truth

### Phase 2e: Data Migration Infrastructure & Final Validation

- [ ] T072 [P] Setup database migrations: Create Alembic migration system for schema version management with format-specific converters
- [ ] T073 [P] **[BACKUP STRATEGY]** Implement data backup integration: Configure automated backup system with rollback capabilities per FR-014 and 15-minute recovery requirement
- [ ] T074 **[SYNC FRAMEWORK]** Create sync state management: Implement real-time bi-directional synchronization framework for cross-domain workflows
- [ ] T075 **[PERFORMANCE VALIDATION]** Validate data layer performance: Ensure <15ms read operations, <150ms complex queries per constitutional performance requirements
- [ ] T076 **[MIGRATION TESTING]** [CHK041] Test data format migrations: Validate conversion accuracy for all legacy formats with rollback verification and data integrity checksums

**Phase 2 Checkpoint**: Unified data architecture operational with validated authentication. All Ground Truth data validation tests must pass.

---

## Phase 3: User Story 1 - Unified Executive Function Dashboard (P1) 🎯

**Story Goal**: Single interface for all 37 tools with 95% context switching reduction  
**Independent Test**: Access unified dashboard and verify all 37 tools accessible with preserved functionality
**Brownfield Focus**: Preserve existing UI patterns and workflows while providing unified access

### Phase 3a: Legacy UI Ground Truth & Validation (Write These First)

- [ ] T077 **[Ground Truth]** [US1] **[Logic: various::ui_interfaces]** Document existing UI patterns: Extract Ground Truth UI behavior from all 37 tools with screenshot documentation and interaction flow validation
- [ ] T078 **[Ground Truth]** [US1] Create UI interaction baseline tests: Document expected UI behavior, context switching patterns, and tool-specific workflows from original tools
- [ ] T079 **[Validation Test]** [US1] Create unified dashboard validation tests: Design tests for single interface access to all 37 tools - must fail initially until integration complete
- [ ] T080 **[UI PRESERVATION]** [US1] Create UI preservation matrix: Document which tools require iframe embedding vs component integration vs API-only access per Ground Truth analysis

### Phase 3b: Dashboard Infrastructure Porting & Integration

- [ ] T081 [P] [US1] [CHK045] **[Logic: various::ui_frameworks]** Create responsive design system: Implement PWA framework with unified breakpoints (512px/730px/1100px) supporting all 8 CSS frameworks per gap_ideas.md
- [ ] T082 [P] [US1] **[LEGACY COMPAT]** **[Logic: various::navigation]** Create navigation wrapper preserving tool-specific interfaces in libs/ui/components/ with fallback mechanisms
- [ ] T083 [P] [US1] **[FUNCTIONALITY MAP]** Setup tool registry with existing functionality mapping from business logic analysis and live system validation
- [ ] T084 [US1] [CHK045] **[Logic: various::responsive_ui]** Implement cross-device UI: PWA installation, offline capability, responsive components for desktop/tablet/mobile per executive function requirements
- [ ] T085 [US1] **[UI INTEGRATION]** **[Logic: various::ui_embedding]** Implement iframe/web component integration for tools requiring UI preservation with security isolation
- [ ] T086 **[Run Validation]** Test unified dashboard functionality: Run validation tests (T079) against integrated UI - must pass before proceeding to asset relocation

### Phase 3c: Individual Project Migrations (Using Handoff Protocol)

**PROJECT SCOPE**: 38 brownfield migrations (MISP already complete, 37 remaining)

- **Security Domain**: 19 projects (T063-T105)
- **Productivity Domain**: 7 projects (T106-T112)
- **MTG Domain**: 4 projects (T113-T116)
- **Infrastructure Domain**: 8 projects (T117-T124)

**ORCHESTRATION NOTE**: This phase delegates to individual project task files using the handoff protocol.
Each `[HANDOFF]` task represents completion of an entire project migration. See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for workflow.

**Handoff Protocol Rules**:

1. Verify entry condition before starting child task file
2. Execute all tasks in referenced file with Pre-Flight validation
3. Verify exit condition and run validation tests
4. Mark handoff task complete only after child document fully complete
5. Continue to next task

**Entry Condition for ALL Phase 3c tasks**: Phase 1-2 complete (foundation infrastructure and data layer operational)

#### Phase 3c1: Security Domain Migrations (19 projects)

**Priority**: CRITICAL - These tools maintain threat monitoring requiring zero-downtime migration

- [ ] T087 [P] [HANDOFF] Migrate APIScout
  - **File**: [`tasks-individual/tasks-apiscout.md`](tasks-individual/tasks-apiscout.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-apiscout.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_apiscout_integration.py`
  - **Return To**: T064
  - **Est. Hours**: 25

- [ ] T088 [P] [HANDOFF] Migrate BlackArch
  - **File**: [`tasks-individual/tasks-blackarch.md`](tasks-individual/tasks-blackarch.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-blackarch.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_blackarch_integration.py`
  - **Return To**: T089
  - **Est. Hours**: 30

- [ ] T089 [P] [HANDOFF] Migrate Brute Ratel C4 Community Kit
  - **File**: [`tasks-individual/tasks-brute-ratel-c4.md`](tasks-individual/tasks-brute-ratel-c4.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-brute-ratel-c4.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_brute_ratel_c4_integration.py`
  - **Return To**: T090
  - **Est. Hours**: 40

- [ ] T090 [P] [HANDOFF] Migrate CyberChef
  - **File**: [`tasks-individual/tasks-cyberchef.md`](tasks-individual/tasks-cyberchef.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-cyberchef.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_cyberchef_integration.py`
  - **Return To**: T091
  - **Est. Hours**: 40

- [ ] T091 [P] [HANDOFF] Migrate Ghostwriter
  - **File**: [`tasks-individual/tasks-ghostwriter.md`](tasks-individual/tasks-ghostwriter.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-ghostwriter.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_ghostwriter_integration.py`
  - **Return To**: T092
  - **Est. Hours**: 50

- [ ] T092 [P] [HANDOFF] Migrate HELK
  - **File**: [`tasks-individual/tasks-helk.md`](tasks-individual/tasks-helk.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-helk.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_helk_integration.py`
  - **Return To**: T093
  - **Est. Hours**: 45

- [ ] T093 [P] [HANDOFF] Migrate HexStrike AI
  - **File**: [`tasks-individual/tasks-hexstrike-ai.md`](tasks-individual/tasks-hexstrike-ai.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-hexstrike-ai.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_hexstrike_ai_integration.py`
  - **Return To**: T094
  - **Est. Hours**: 35

- [ ] T094 [P] [HANDOFF] Migrate LScript
  - **File**: [`tasks-individual/tasks-lscript.md`](tasks-individual/tasks-lscript.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-lscript.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_lscript_integration.py`
  - **Return To**: T095
  - **Est. Hours**: 20

- [ ] T095 [CRITICAL] [HANDOFF] Migrate Maltrail Network Security Monitor
  - **File**: [`tasks-individual/tasks-maltrail.md`](tasks-individual/tasks-maltrail.md)
  - **Description**: DDD-based migration of real-time network threat detection system (400K+ indicators, 50+ feeds)
  - **Entry Condition**: Phase 1-4 complete, security-service foundation ready, packet capture environment available
  - **Exit Condition**: All 115 tasks complete + network monitoring domain operational + performance validated
  - **Validation**: `pytest apps/security-service/tests/domains/network_monitoring/ -v --ground-truth`
  - **Return To**: T096
  - **Est. Hours**: 65 (CRITICAL security capability - requires network security expert)

- [ ] T096 [P] [HANDOFF] Migrate MalwareBazaar MCP
  - **File**: [`tasks-individual/tasks-malwarebazaar-mcp.md`](tasks-individual/tasks-malwarebazaar-mcp.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-malwarebazaar-mcp.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_malwarebazaar_mcp_integration.py`
  - **Return To**: T097
  - **Est. Hours**: 25

- [ ] T097 [P] [HANDOFF] Migrate MCP VirusTotal
  - **File**: [`tasks-individual/tasks-mcp-virustotal.md`](tasks-individual/tasks-mcp-virustotal.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-mcp-virustotal.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_mcp_virustotal_integration.py`
  - **Return To**: T098
  - **Est. Hours**: 25

- [ ] T098 [P] [HANDOFF] Migrate Meterpreter
  - **File**: [`tasks-individual/tasks-meterpreter.md`](tasks-individual/tasks-meterpreter.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-meterpreter.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_meterpreter_integration.py`
  - **Return To**: T099
  - **Est. Hours**: 35

- [ ] T099 [P] [HANDOFF] Migrate Nemesis
  - **File**: [`tasks-individual/tasks-nemesis.md`](tasks-individual/tasks-nemesis.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-nemesis.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_nemesis_integration.py`
  - **Return To**: T100
  - **Est. Hours**: 45

- [ ] T100 [P] [HANDOFF] Migrate Onex
  - **File**: [`tasks-individual/tasks-onex.md`](tasks-individual/tasks-onex.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-onex.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_onex_integration.py`
  - **Return To**: T101
  - **Est. Hours**: 25

- [ ] T101 [P] [HANDOFF] Migrate RITA
  - **File**: [`tasks-individual/tasks-rita.md`](tasks-individual/tasks-rita.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-rita.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_rita_integration.py`
  - **Return To**: T102
  - **Est. Hours**: 30

- [ ] T102 [P] [HANDOFF] Migrate Security Onion
  - **File**: [`tasks-individual/tasks-securityonion.md`](tasks-individual/tasks-securityonion.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-securityonion.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_securityonion_integration.py`
  - **Return To**: T103
  - **Est. Hours**: 50

- [ ] T103 [P] [HANDOFF] Migrate Security Onion n8n Workflows
  - **File**: [`tasks-individual/tasks-securityonion-n8n-workflows.md`](tasks-individual/tasks-securityonion-n8n-workflows.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready, T102 (SecurityOnion) complete
  - **Exit Condition**: All tasks in tasks-securityonion-n8n-workflows.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_securityonion_n8n_workflows_integration.py`
  - **Return To**: T104
  - **Est. Hours**: 30

- [ ] T104 [P] [HANDOFF] Migrate Software Forensic Kit
  - **File**: [`tasks-individual/tasks-software-forensic-kit.md`](tasks-individual/tasks-software-forensic-kit.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-software-forensic-kit.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_software_forensic_kit_integration.py`
  - **Return To**: T105
  - **Est. Hours**: 35

- [ ] T105 [P] [HANDOFF] Migrate YARA-X
  - **File**: [`tasks-individual/tasks-yara-x.md`](tasks-individual/tasks-yara-x.md)
  - **Entry Condition**: Phase 1-2 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-yara-x.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_yara_x_integration.py`
  - **Return To**: T106
  - **Est. Hours**: 30

**Security Domain Checkpoint**: All 19 security tools migrated with threat monitoring continuity validated.

### Phase 3d: Productivity Domain Migrations (Using Handoff Protocol)

**EXECUTIVE FUNCTION PRIORITY**: These tools are core to daily productivity workflows

**Entry Condition for ALL Phase 3d tasks**: Phase 1-2 complete (foundation infrastructure and data layer operational)

#### Phase 3d1: Productivity Domain Migrations (7 projects)

- [ ] T106 [P] [HANDOFF] Migrate Actual Budget
  - **File**: [`tasks-individual/tasks-actual.md`](tasks-individual/tasks-actual.md)
  - **Entry Condition**: Phase 1-2 complete, apps/productivity-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-actual.md complete + validation tests pass
  - **Validation**: `pytest tests/productivity/test_actual_integration.py`
  - **Return To**: T107
  - **Est. Hours**: 35

- [ ] T107 [P] [HANDOFF] Migrate Dispatch
  - **File**: [`tasks-individual/tasks-dispatch.md`](tasks-individual/tasks-dispatch.md)
  - **Entry Condition**: Phase 1-2 complete, apps/productivity-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-dispatch.md complete + validation tests pass
  - **Validation**: `pytest tests/productivity/test_dispatch_integration.py`
  - **Return To**: T108
  - **Est. Hours**: 45

- [ ] T108 [P] [HANDOFF] Migrate Firecrawl
  - **File**: [`tasks-individual/tasks-firecrawl.md`](tasks-individual/tasks-firecrawl.md)
  - **Entry Condition**: Phase 1-2 complete, apps/productivity-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-firecrawl.md complete + validation tests pass
  - **Validation**: `pytest tests/productivity/test_firecrawl_integration.py`
  - **Return To**: T109
  - **Est. Hours**: 30

- [ ] T109 [P] [HANDOFF] Migrate Goose
  - **File**: [`tasks-individual/tasks-goose.md`](tasks-individual/tasks-goose.md)
  - **Entry Condition**: Phase 1-2 complete, apps/productivity-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-goose.md complete + validation tests pass
  - **Validation**: `pytest tests/productivity/test_goose_integration.py`
  - **Return To**: T110
  - **Est. Hours**: 40

- [ ] T110 [P] [HANDOFF] Migrate Inspector
  - **File**: [`tasks-individual/tasks-inspector.md`](tasks-individual/tasks-inspector.md)
  - **Entry Condition**: Phase 1-2 complete, apps/productivity-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-inspector.md complete + validation tests pass
  - **Validation**: `pytest tests/productivity/test_inspector_integration.py`
  - **Return To**: T111
  - **Est. Hours**: 25

- [ ] T111 [P] [HANDOFF] Migrate IT Tools
  - **File**: [`tasks-individual/tasks-it-tools.md`](tasks-individual/tasks-it-tools.md)
  - **Entry Condition**: Phase 1-2 complete, apps/productivity-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-it-tools.md complete + validation tests pass
  - **Validation**: `pytest tests/productivity/test_it_tools_integration.py`
  - **Return To**: T112
  - **Est. Hours**: 30

- [ ] T112 [P] [HANDOFF] Migrate Mealie
  - **File**: [`tasks-individual/tasks-mealie.md`](tasks-individual/tasks-mealie.md)
  - **Entry Condition**: Phase 1-2 complete, apps/productivity-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-mealie.md complete + validation tests pass
  - **Validation**: `pytest tests/productivity/test_mealie_integration.py`
  - **Return To**: T113
  - **Est. Hours**: 40

**Productivity Domain Checkpoint**: All 7 productivity tools migrated with task management data preserved.

### Phase 3e: MTG Domain Migrations (Using Handoff Protocol)

**TCG DOMAIN**: Complex algorithmic tools for trading card game analysis

**Entry Condition for ALL Phase 3e tasks**: Phase 1-2 complete (foundation infrastructure and data layer operational)

#### Phase 3e1: MTG Domain Migrations (4 projects)

- [ ] T113 [P] [HANDOFF] Migrate Commander Spellbook Backend
  - **File**: [`tasks-individual/tasks-commander-spellbook-backend.md`](tasks-individual/tasks-commander-spellbook-backend.md)
  - **Entry Condition**: Phase 1-2 complete, apps/mtg-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-commander-spellbook-backend.md complete + validation tests pass
  - **Validation**: `pytest tests/mtg/test_commander_spellbook_backend_integration.py`
  - **Return To**: T114
  - **Est. Hours**: 45

- [ ] T114 [P] [HANDOFF] Migrate Commander Spellbook Site
  - **File**: [`tasks-individual/tasks-commander-spellbook-site.md`](tasks-individual/tasks-commander-spellbook-site.md)
  - **Entry Condition**: Phase 1-2 complete, TCG domain foundation ready, T113 (backend) complete
  - **Exit Condition**: All tasks T001-T079 in tasks-commander-spellbook-site.md complete + Cypress E2E tests pass
  - **Validation**: `npm run test:integration` (TCG domain)
  - **Return To**: T115
  - **Est. Hours**: 42

- [ ] T115 [P] [HANDOFF] Migrate MTG Commander Map
  - **File**: [`tasks-individual/tasks-mtg-commander-map.md`](tasks-individual/tasks-mtg-commander-map.md)
  - **Entry Condition**: Phase 1-2 complete, apps/mtg-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-mtg-commander-map.md complete + validation tests pass
  - **Validation**: `pytest tests/mtg/test_mtg_commander_map_integration.py`
  - **Return To**: T116
  - **Est. Hours**: 40

- [ ] T116 [P] [HANDOFF] Migrate MTG Scripting Toolkit
  - **File**: [`tasks-individual/tasks-mtg-scripting-toolkit.md`](tasks-individual/tasks-mtg-scripting-toolkit.md)
  - **Entry Condition**: Phase 1-2 complete, apps/mtg-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-mtg-scripting-toolkit.md complete + validation tests pass
  - **Validation**: `pytest tests/mtg/test_mtg_scripting_toolkit_integration.py`
  - **Return To**: T117
  - **Est. Hours**: 30

**MTG Domain Checkpoint**: All 4 MTG tools migrated with combo generation and deck analysis algorithms preserved.

### Phase 3f: Infrastructure Domain Migrations (Using Handoff Protocol)

**INFRASTRUCTURE PRIORITY**: Platform and system administration tools, MCP servers, workflow automation

**Entry Condition for ALL Phase 3f tasks**: Phase 1-2 complete (foundation infrastructure and data layer operational)

#### Phase 3f1: Infrastructure Domain Migrations (8 core projects)

- [ ] T117 [P] [HANDOFF] Migrate Chroma MCP
  - **File**: [`tasks-individual/tasks-chroma-mcp.md`](tasks-individual/tasks-chroma-mcp.md)
  - **Entry Condition**: Phase 1-2 complete, apps/infrastructure-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-chroma-mcp.md complete + validation tests pass
  - **Validation**: `pytest tests/infrastructure/test_chroma_mcp_integration.py`
  - **Return To**: T118
  - **Est. Hours**: 25

- [ ] T118 [P] [HANDOFF] Migrate FileScope MCP
  - **File**: [`tasks-individual/tasks-filescope-mcp.md`](tasks-individual/tasks-filescope-mcp.md)
  - **Entry Condition**: Phase 1-2 complete, apps/infrastructure-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-filescope-mcp.md complete + validation tests pass
  - **Validation**: `pytest tests/infrastructure/test_filescope_mcp_integration.py`
  - **Return To**: T119
  - **Est. Hours**: 20

- [ ] T119 [P] [HANDOFF] Migrate Firecrawl MCP Server
  - **File**: [`tasks-individual/tasks-firecrawl-mcp-server.md`](tasks-individual/tasks-firecrawl-mcp-server.md)
  - **Entry Condition**: Phase 1-2 complete, apps/infrastructure-service/ foundation ready, T108 (Firecrawl) complete
  - **Exit Condition**: All tasks in tasks-firecrawl-mcp-server.md complete + validation tests pass
  - **Validation**: `pytest tests/infrastructure/test_firecrawl_mcp_server_integration.py`
  - **Return To**: T120
  - **Est. Hours**: 20

- [ ] T120 [P] [HANDOFF] Migrate KasmVNC
  - **File**: [`tasks-individual/tasks-kasmvnc.md`](tasks-individual/tasks-kasmvnc.md)
  - **Entry Condition**: Phase 1-2 complete, apps/infrastructure-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-kasmvnc.md complete + validation tests pass
  - **Validation**: `pytest tests/infrastructure/test_kasmvnc_integration.py`
  - **Return To**: T121
  - **Est. Hours**: 45

- [ ] T121 [P] [HANDOFF] Migrate Kong
  - **File**: [`tasks-individual/tasks-kong.md`](tasks-individual/tasks-kong.md)
  - **Entry Condition**: Phase 1-2 complete, apps/infrastructure-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-kong.md complete + validation tests pass
  - **Validation**: `pytest tests/infrastructure/test_kong_integration.py`
  - **Return To**: T122
  - **Est. Hours**: 40

- [ ] T122 [P] [HANDOFF] Migrate n8n
  - **File**: [`tasks-individual/tasks-n8n.md`](tasks-individual/tasks-n8n.md)
  - **Entry Condition**: Phase 1-2 complete, apps/n8n-workflow-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-n8n.md complete + validation tests pass
  - **Validation**: `pytest tests/infrastructure/test_n8n_integration.py`
  - **Return To**: T123
  - **Est. Hours**: 50

- [ ] T123 [P] [HANDOFF] Migrate n8n MCP Server
  - **File**: [`tasks-individual/tasks-n8n-mcp-server.md`](tasks-individual/tasks-n8n-mcp-server.md)
  - **Entry Condition**: Phase 1-2 complete, apps/infrastructure-service/ foundation ready, T122 (n8n) complete
  - **Exit Condition**: All tasks in tasks-n8n-mcp-server.md complete + validation tests pass
  - **Validation**: `pytest tests/infrastructure/test_n8n_mcp_server_integration.py`
  - **Return To**: T124
  - **Est. Hours**: 25

- [ ] T124 [P] [HANDOFF] Migrate Spec Kit
  - **File**: [`tasks-individual/tasks-spec-kit.md`](tasks-individual/tasks-spec-kit.md)
  - **Entry Condition**: Phase 1-2 complete, apps/infrastructure-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-spec-kit.md complete + validation tests pass
  - **Validation**: `pytest tests/infrastructure/test_spec_kit_integration.py`
  - **Return To**: T125
  - **Est. Hours**: 30

### Phase 3g: Dashboard Integration & Final Validation

**Entry Condition**: Phase 3c-3f complete (all 38 individual project migrations complete)

- [ ] T125 [US1] **[STATE UNIFICATION]** **[Logic: various::state_management]** Implement unified state management across all integrated tools in apps/jane-ui/src/store/ with cross-tool context preservation
- [ ] T126 [US1] [CHK045] **[SEAMLESS SWITCHING]** **[Logic: various::navigation]** Create seamless tool switching with context preservation and responsive transitions in apps/jane-ui/src/navigation/
- [ ] T127 [US1] [CHK045] **[PERFORMANCE VALIDATION]** Validate <200ms UI interactions across all devices (desktop/tablet/mobile) with performance testing vs baseline
- [ ] T128 [US1] **[INTEGRATION TESTING]** Execute comprehensive integration testing - verify all 37 tools accessible through single responsive interface
- [ ] T129 [US1] [CHK081] **[TRACEABILITY SYSTEM]** Implement lightweight traceability: Create automated mapping from 3,795+ test files to business logic preservation per gap_ideas.md evidence-based approach

### Phase 3h: User Story 1 Validation Gate

**MANDATORY VALIDATION**: All tasks from Phase 3c-3g must pass validation before proceeding to Phase 4

- [ ] T130 [US1] **[FUNCTIONALITY GATE]** Execute functionality validation: Test all 37 tools through unified interface vs original tool functionality with Ground Truth comparison
- [ ] T131 [US1] **[PERFORMANCE GATE]** Execute performance validation: Confirm <200ms UI response times and domain-specific API performance vs established baselines
- [ ] T132 [US1] **[USER EXPERIENCE GATE]** Execute user experience validation: Verify executive function accommodations and context switching reduction
- [ ] T133 [US1] **[ROLLBACK VERIFICATION]** Test rollback procedures: Verify 15-minute recovery capability for dashboard failure scenarios

**Phase 3 Checkpoint**: All 37 tools accessible through unified interface, <200ms transitions, consistent navigation, Ground Truth validation complete.

---

## Phase 4: User Story 2 - Business Logic Preservation Validation (P1) 🎯

**Story Goal**: 100% preservation using Asset Relocation Process across all 37 tools  
**Independent Test**: Execute 3,795 existing test files against relocated assets with 100% pass rate
**Brownfield Focus**: Follow 5-step Asset Relocation Process per consolidated-business-logic-analysis.md

### Phase 4a: Category A Algorithm Ground Truth & Validation (Write These First)

**Critical Success Factor**: Ground Truth tests against original algorithms before any migration

- [ ] T134 **[Ground Truth]** [US2] **[Logic: MISP/app/Model/Event.php::correlation]** Ground Truth Test: Execute MISP correlation engine with test threat data and document expected correlation results with performance baselines
- [ ] T135 **[Ground Truth]** [US2] **[Logic: n8n/packages/core/src/WorkflowExecute.ts::execute]** Ground Truth Test: Execute n8n workflow engine with test workflows and document expected execution states and outcomes  
- [ ] T136 **[Ground Truth]** [US2] **[Logic: CyberChef/src/core/operations/*.mjs]** Ground Truth Test: Execute CyberChef operations with test data sets and document expected bit-perfect transformations
- [ ] T137 **[Ground Truth]** [US2] **[Logic: commander-spellbook-backend/backend/spellbook/variants/combo_generator.py]** Ground Truth Test: Execute combo generation with test card sets and document expected variant outputs
- [ ] T138 **[Ground Truth]** [US2] **[Logic: yara-x/lib/src/scanner.rs::scan]** Ground Truth Test: Execute YARA-X pattern matching with test malware samples and document detection accuracy
- [ ] T139 **[Ground Truth]** [US2] **[Logic: actual/packages/loot-core/src/server/crdt/*]** Ground Truth Test: Execute Actual Budget CRDT with test transaction conflicts and document conflict resolution behavior
- [ ] T140 **[Validation Test]** [US2] Create Category A algorithm validation tests: Translate Ground Truth tests to new microservice architecture - must fail initially

### Phase 4b: Category A Algorithm Preservation (Complex Algorithms >5,000 lines) - MICROSERVICE PRESERVATION

**Critical Success Factor**: Preserve existing algorithms exactly - no rewrites, use containers/microservices to maintain original runtimes

- [ ] T141 [US2] **[CRITICAL ALGO - MISP]** **[Logic: MISP/app/Model/Event.php::correlation]** Preserve MISP threat correlation: Migrate Event.php correlation engine (8,733 lines) from features/MISP/app/Model/ maintaining CakePHP business logic per reports/misp-analysis.md with bit-perfect correlation preservation
- [ ] T142 [US2] **[CRITICAL ALGO - N8N]** **[Logic: n8n/packages/core/src/WorkflowExecute.ts::execute]** Preserve n8n workflow execution: Migrate WorkflowExecute.ts (2,620 lines) from features/n8n/packages/core/ as TypeScript microservice per reports/n8n-analysis.md with workflow state preservation
- [ ] T143 [P] [US2] **[CRITICAL ALGO - CYBERCHEF]** **[Logic: CyberChef/src/core/operations/*.mjs]** Preserve CyberChef operations: Integrate 300+ operations engine from features/CyberChef/src/core/ as embedded library with REST wrapper per reports/CyberChef-analysis.md with operation accuracy validation
- [ ] T144 [P] [US2] **[CRITICAL ALGO - SPELLBOOK]** **[Logic: commander-spellbook-backend/backend/spellbook/variants/combo_generator.py]** Preserve Commander Spellbook variants: Migrate combo generation (1,400 lines) from features/commander-spellbook-backend/ preserving Django ORM per reports/commander-spellbook-analysis.md with graph algorithm preservation
- [ ] T145 [P] [US2] **[CRITICAL ALGO - YARA]** **[Logic: yara-x/lib/src/scanner.rs::scan]** Preserve YARA-X pattern matching: Integrate Rust pattern engine from features/yara-x/lib/src/ with WASM compilation per reports/yara-x-analysis.md with pattern matching accuracy
- [ ] T146 [P] [US2] [CHK041] **[CRITICAL ALGO - BUDGET]** **[Logic: actual/packages/loot-core/src/server/crdt/*]** Preserve Actual Budget CRDT: Migrate spreadsheet engine (2,000 lines) with specialized CRDT→PostgreSQL conversion preserving conflict-free replication per reports/actual-analysis.md with CRDT semantic preservation
- [ ] T147 **[Run Validation]** Test Category A algorithm preservation: Run validation tests (T069) against preserved algorithms - must pass with Ground Truth accuracy

### Phase 4b: Category A Asset Relocation Process Validation

**BROWNFIELD ASSET RELOCATION**: Follow 6-step process for complex algorithms

- [ ] T148 [P] [US2] **[CAT A - STEP 2]** Migrate tech stacks per consolidated-technology-stack-inventory.md (preserve runtimes: PHP, Node.js, Rust containers)
- [ ] T149 [P] [US2] **[CAT A - STEP 3]** Resolve technical debt per consolidated-technical-debt-analysis.md with algorithm preservation priority
- [ ] T150 [P] [US2] **[CAT A - STEP 4]** Create service adapters in libs/service-adapters/ for unified access with performance monitoring
- [ ] T151 [US2] **[CAT A - STEP 5]** Implement validation using existing test suites (3,795 files) with baseline comparison for complex algorithms
- [ ] T152 [US2] **[CAT A - STEP 6]** Remove from features/ only after 100% validation success and performance baseline confirmation

### Phase 4c: Category B Domain Logic Preservation (1,000-5,000 lines) - MODULAR INTEGRATION

**Strategy**: Modular migration within unified platform preserving domain-specific workflows and business rules

- [ ] T153 [P] [US2] **[CAT B - HELK]** Migrate HELK analytics: Preserve ELK stack integration and Jupyter notebooks from features/HELK/docker/ in apps/jane-orchestrator/src/domains/security/helk/ per reports/HELK-analysis.md with query optimization preservation
- [ ] T154 [P] [US2] **[CAT B - SECURITYONION]** Migrate SecurityOnion workflows: Preserve Salt states and network monitoring configuration from features/securityonion/salt/ per reports/securityonion-analysis.md with configuration logic preservation
- [ ] T155 [P] [US2] **[CAT B - DISPATCH]** Migrate Dispatch incident management: Preserve PostgreSQL schema and workflow orchestration from features/dispatch/src/ per reports/dispatch-analysis.md with incident workflow preservation
- [ ] T156 [P] [US2] **[CAT B - MEALIE]** Migrate Mealie recipe management: Preserve recipe parsing algorithms from features/mealie/mealie/ maintaining FastAPI backend per reports/mealie-analysis.md with parsing logic preservation
- [ ] T157 [P] [US2] **[CAT B - NEMESIS]** Migrate Nemesis framework: Preserve post-exploitation workflows and data processing from features/Nemesis/cmd/ per reports/nemesis-analysis.md with pipeline logic preservation

### Phase 4d: Category C Utility Integration (<1,000 lines) - LIBRARY INTEGRATION

**Strategy**: Convert to shared libraries and React components maintaining API compatibility and utility function access patterns

- [ ] T158 [P] [US2] **[CAT C - IT-TOOLS]** Migrate IT-Tools utilities: Convert 80+ utilities from features/it-tools/src/tools/ to React component library in libs/shared/utilities/ per reports/it-tools-analysis.md with function signature preservation
- [ ] T159 [P] [US2] **[CAT C - INSPECTOR]** Migrate Inspector MCP debugger: Convert from features/inspector/src/ to shared development library in libs/shared/development/ per reports/inspector-analysis.md with debugging interface preservation  
- [ ] T160 [P] [US2] **[CAT C - BLACKARCH]** Migrate BlackArch scripts: Convert security scripts to callable Python modules preserving functionality and command-line compatibility
- [ ] T161 [P] [US2] **[CAT C - MCP SERVERS]** Migrate MCP servers: Integrate 6+ MCP servers from features/ as FastAPI modules maintaining protocol compliance and model access patterns
- [ ] T162 [P] [US2] **[CAT C - FORENSICS]** Migrate Software Forensic Kit: Convert to shared analysis library maintaining tool compatibility and evidence processing workflows

### Phase 4e: Business Logic Validation Framework - CRITICAL VALIDATION GATE

**Critical Success Factor**: 100% functionality preservation validated through automated testing comparing original vs integrated behavior

#### Phase 4e1: Baseline Validation & Regression Framework

- [ ] T163 [US2] **[BASELINE CAPTURE]** Execute baseline validation: Run all 3,795 existing test files on original tools and document results with performance metrics
- [ ] T164 [US2] **[REGRESSION FRAMEWORK]** Create regression testing framework: Implement automated comparison testing between original and integrated behavior in tests/regression/
- [ ] T165 [US2] [CHK041] **[DATA FORMAT TESTS]** Execute data format conversion tests: Validate all legacy format migrations (MySQL, SQLite, MongoDB, CRDT) with rollback verification and data integrity checksums

#### Phase 4e2: Comprehensive Validation Test Execution

- [ ] T166 [US2] **[CRUD VALIDATION]** Execute 822 CRUD operation tests: Validate data migration against relocated data layers for all database operations with performance comparison
- [ ] T167 [US2] **[API VALIDATION]** Execute 743 API operation tests: Validate interface preservation against service adapters for all API endpoints with response time validation
- [ ] T168 [US2] **[EDGE CASE VALIDATION]** Execute 1,970 exotic pattern tests: Validate edge case coverage using existing comprehensive test infrastructure with original behavior comparison
- [ ] T169 [US2] [CHK044] **[CONCURRENCY TESTS]** Execute concurrent access tests: Validate single-user tool isolation and conflict resolution under concurrent load scenarios

#### Phase 4e3: Algorithm Precision Validation

- [ ] T170 [US2] **[MISP PRECISION]** Validate MISP correlation precision: Confirm ±0.001 tolerance for threat correlation algorithms using existing MISP tests with statistical validation
- [ ] T171 [US2] **[CYBERCHEF ACCURACY]** Validate CyberChef bit-perfect accuracy: Confirm identical outputs for all 300+ operations using existing operation tests with binary comparison
- [ ] T172 [US2] **[N8N WORKFLOW]** Validate n8n workflow execution: Confirm identical workflow results using existing n8n test suites with state comparison
- [ ] T173 [US2] [CHK045] **[RESPONSIVE TESTS]** Execute responsive design tests: Validate <200ms performance across all device categories (desktop/tablet/mobile/large displays)

#### Phase 4e4: Final Validation & Traceability

- [ ] T174 [US2] **[COMPREHENSIVE GATE]** Execute comprehensive validation: Require 100% test pass rate before removing any tool from features/ directory with detailed failure analysis
- [ ] T175 [US2] [CHK081] **[TRACEABILITY DASHBOARD]** Implement automated traceability dashboard: Create test→business logic mapping using existing 4,263 test functions per gap_ideas.md evidence-based approach
- [ ] T176 [US2] **[PRESERVATION VALIDATION]** Implement business logic preservation testing: Automated validation framework per consolidated-business-logic-analysis.md with constitutional compliance verification

**Acceptance Criteria**: 100% functionality preservation validated, all regression tests pass, bit-perfect accuracy for critical algorithms

---

## Phase 5: User Story 3 - AI-Enhanced Cross-Tool Intelligence (P2)

**Story Goal**: AI assistance with context awareness across all 37 integrated tools
**Independent Test**: AI provides contextual recommendations referencing multiple tool data  
**Why Enhanced Value**: Leverages integration for AI capabilities impossible with separate tools

### Phase 5a: AI Infrastructure Ground Truth & Enhancement

- [ ] T177 **[Ground Truth]** [US3] Document existing AI patterns: Analyze current AI usage in original 37 tools (MCP servers, AI agents, ML models) for baseline comparison
- [ ] T178 **[Validation Test]** [US3] Create AI enhancement validation tests: Design tests for cross-domain AI intelligence - must fail initially until AI integration complete
- [ ] T179 [P] [US3] **[Logic: various::ai_models]** Setup local vLLM server: Configure RTX 3090 with Llama-3.1-8B-Instruct, CodeLlama-13B models in apps/cyber-llm-server/
- [ ] T180 [P] [US3] Setup ChromaDB vector database: Configure domain-specific collections (security_knowledge, productivity_workflows, tcg_strategies, infrastructure_configs)
- [ ] T181 [P] [US3] **[Logic: various::mcp_servers]** Create domain-specific MCP servers: Deploy security, productivity, TCG, infrastructure MCP servers for specialized AI assistance
- [ ] T182 [US3] Implement cross-domain context aggregation: Create AI context engine for multi-domain intelligence in apps/jane-orchestrator/src/ai/context/

### Phase 5b: Domain-Specific AI Enhancement (Preserve Original Logic)

- [ ] T183 [P] [US3] **[Logic: MISP/app/Model/Event.php::correlation + AI wrapper]** Implement AI-Enhanced MISP correlation: Wrap original Event.php algorithms with cross-domain context enhancement per AI integration framework
- [ ] T184 [P] [US3] **[Logic: n8n/packages/core/src/WorkflowExecute.ts + AI optimization]** Implement AI-Enhanced n8n workflows: Add intelligent optimization to preserved WorkflowExecute engine
- [ ] T185 [P] [US3] **[Logic: commander-spellbook-backend + AI strategy]** Implement AI-Enhanced TCG analysis: Create deck strategy AI using preserved Commander Spellbook algorithms
- [ ] T186 [P] [US3] **[Logic: various::monitoring + AI prediction]** Implement AI-Enhanced infrastructure monitoring: Add predictive analysis to system operations

### Phase 5c: Cross-Domain Intelligence Implementation

- [ ] T187 [P] [US3] Create AI recommendation engine: Multi-domain context for security→productivity→budget workflows
- [ ] T188 [P] [US3] Implement proactive workflow suggestions: Pattern detection from user behavior across all 37 tools
- [ ] T189 [P] [US3] Setup automated task breakdown: AI-assisted workflow creation with cross-domain impact assessment
- [ ] T190 [P] [US3] Create intelligent assistant: Executive function accommodations with <2s response time

### Phase 5d: AI Integration Validation & Ground Truth Comparison

- [ ] T191 [US3] **[Run Validation]** Test AI enhancement validation: Run validation tests (T083) against AI-enhanced system - must pass with Ground Truth functionality preservation
- [ ] T192 [US3] Test cross-domain AI scenarios: Security incidents→task creation→budget impact analysis
- [ ] T193 [US3] Test AI workflow optimization: Validate 2-10x improvement in execution speed while preserving original algorithm accuracy
- [ ] T194 [US3] Test proactive automation: Usage pattern detection and workflow suggestions
- [ ] T195 [US3] Validate AI performance: <2s inference, fallback to original algorithms if AI unavailable

**Phase 5 Checkpoint**: AI enhancement operational with original algorithm preservation verified. Ground Truth functionality maintained with AI augmentation.

**Acceptance Criteria**: AI provides contextual recommendations across domains, proactive suggestions work, <2s inference times

---

## Phase 6: User Story 4 - Performance-Optimized Domain Operations (P2)

**Story Goal**: Domain-specific performance tiers for executive function support
**Independent Test**: Measure response times across all domains and verify SLA compliance
**Why Enhanced Value**: Performance requirements are constitutionally mandated for cognitive support

### Phase 6a: Performance Ground Truth & Monitoring Implementation  

- [ ] T196 **[Ground Truth]** [US4] Document original tool performance baselines: Capture current performance characteristics from all 37 tools for optimization comparison
- [ ] T197 **[Validation Test]** [US4] Create performance optimization validation tests: Design tests for domain-specific SLA requirements - must fail initially until optimization complete
- [ ] T198 [US4] **[Logic: various::monitoring]** Implement domain-specific SLA monitoring in libs/shared/performance/monitoring/
- [ ] T199 [P] [US4] Setup performance dashboards with real-time SLA tracking in apps/jane-ui/src/monitoring/
- [ ] T200 [P] [US4] Create automated performance regression detection in tests/performance/
- [ ] T201 [US4] Implement performance alerting with SLA violation triggers

### Phase 6b: Security Domain Optimization (<1s requirement) - Algorithm Preservation Priority

- [ ] T202 [P] [US4] **[Logic: MISP/app/Model/Event.php::correlation + optimization]** Optimize MISP threat correlation for <500ms response while preserving correlation accuracy in apps/jane-orchestrator/src/domains/security/misp/
- [ ] T203 [P] [US4] **[Logic: yara-x/lib/src/scanner.rs::scan + optimization]** Optimize YARA-X pattern matching for <100ms per sample while preserving detection accuracy in apps/jane-orchestrator/src/domains/security/yara/
- [ ] T204 [P] [US4] Implement predictive caching for threat intelligence lookups
- [ ] T205 [P] [US4] Setup parallel processing for bulk threat analysis
- [ ] T206 [US4] **[Run Validation]** Validate security domain performance <1s for 95% of operations with Ground Truth accuracy preservation

### Phase 6c: Productivity Domain Optimization (<2s requirement)

- [ ] T207 [P] [US4] Optimize n8n workflow execution for <1s average in apps/jane-orchestrator/src/domains/productivity/n8n/
- [ ] T208 [P] [US4] Optimize Actual Budget CRDT operations for <500ms sync times
- [ ] T209 [P] [US4] Implement batch processing for workflow operations
- [ ] T210 [P] [US4] Setup smart prefetching for task management data
- [ ] T211 [US4] Validate productivity domain performance <2s for 95% of operations

### Phase 6d: TCG and Infrastructure Optimization

- [ ] T212 [P] [US4] Optimize Commander Spellbook combo search for <1.5s in apps/jane-orchestrator/src/domains/tcg/
- [ ] T213 [P] [US4] Optimize IT-Tools operations for <2.5s in apps/jane-orchestrator/src/domains/infrastructure/
- [ ] T214 [P] [US4] Implement streaming results for large dataset operations
- [ ] T215 [P] [US4] Setup distributed caching for system metrics
- [ ] T216 [US4] Validate TCG domain <3s and Infrastructure domain <5s performance requirements

### Phase 6e: UI Performance Optimization

- [ ] T217 [US4] Optimize UI interactions for <100ms response (50% better than baseline)
- [ ] T218 [P] [US4] Implement virtual scrolling for large data lists in libs/ui/components/
- [ ] T219 [P] [US4] Setup progressive web app caching strategies  
- [ ] T220 [US4] Validate <200ms UI interaction requirement with executive function accommodations

**Acceptance Criteria**: All domain SLAs met (Security <1s, Productivity <2s, TCG <3s, Infrastructure <5s), UI <200ms

---

## Phase 7: User Story 5 - Rollback and Recovery Capabilities (P3)

**Story Goal**: Comprehensive rollback for tool failures and system-wide issues
**Independent Test**: Simulate failure scenarios and verify 15-minute recovery objective  
**Why Operational**: Supports reliability requirements, essential for production use

### Phase 7a: Rollback Ground Truth & Infrastructure

- [ ] T221 **[Ground Truth]** [US5] Document existing rollback capabilities: Analyze current backup/recovery mechanisms from original 37 tools for integration baseline
- [ ] T222 **[Validation Test]** [US5] Create rollback validation tests: Design tests for 15-minute recovery objective - must fail initially until rollback infrastructure complete
- [ ] T223 [US5] **[Logic: various::backup_systems]** Implement tool-specific rollback capabilities in libs/shared/recovery/tool-rollback/
- [ ] T224 [P] [US5] Implement system-wide rollback with blue-green deployment in infrastructure/deployment/
- [ ] T225 [P] [US5] Setup automated backup system with hourly snapshots in infrastructure/backup/
- [ ] T226 [US5] Create rollback orchestration with dependency management

### Phase 7b: Recovery Automation

- [ ] T227 [P] [US5] Implement automated failure detection with health checks in apps/jane-orchestrator/src/monitoring/
- [ ] T228 [P] [US5] Setup automated recovery workflows with escalation policies
- [ ] T229 [P] [US5] Create data consistency verification for rollback operations  
- [ ] T230 [US5] Implement audit logging for all rollback operations

### Phase 7c: Recovery Testing and Validation

- [ ] T231 [US5] **[Run Validation]** Test rollback validation: Run validation tests (T079) against rollback infrastructure - must meet 15-minute recovery objective
- [ ] T232 [US5] Test individual tool rollback scenarios for all 37 tools with Ground Truth state restoration
- [ ] T233 [US5] Test system-wide rollback with full state restoration
- [ ] T234 [US5] Validate 15-minute recovery objective under various failure conditions
- [ ] T235 [US5] Test rollback during concurrent user sessions and data modifications

**Phase 7 Checkpoint**: Rollback infrastructure operational with 15-minute recovery objective verified for all 37 tools.

### Phase 7d: Recovery Documentation and Training

- [ ] T236 [P] [US5] Create recovery procedure documentation in docs/operations/
- [ ] T237 [P] [US5] Setup monitoring dashboards for recovery operations
- [ ] T238 [US5] Validate recovery capabilities meet constitutional 15-minute requirement

**Acceptance Criteria**: Tool-specific rollback <5min, system-wide rollback <15min, data consistency maintained

---

## Phase 8: Production Polish and Cross-Cutting Concerns (3 weeks)

**Purpose**: Final optimization, monitoring, and production readiness per constitutional requirements

### Phase 8a: Final Ground Truth Validation & Migration Completion

- [ ] T239 **[Final Ground Truth]** [US6] Execute comprehensive Ground Truth comparison: Compare all 37 integrated tools against original tool behavior with documented evidence
- [ ] T240 **[Final Validation]** [US6] Run complete validation test suite: All Ground Truth and validation tests must pass before production deployment
- [ ] T241 [P] [US6] **[Logic: features/*/]** Empty features/ directory validation: Constitutional completion requirement - zero tools remaining (NOTE: This happens in Phase N+1 Asset Deletion)
- [ ] T242 [P] [US6] Archive original tool containers: Create migration audit trail in docs/migration/archive/ with functionality verification
- [ ] T243 [P] [US6] Validate zero legacy containers: Confirm all 37 tools successfully migrated with preserved business logic
- [ ] T244 [US6] Create migration completion certificate: Document constitutional compliance with Asset Relocation Process

### Phase 8b: Comprehensive Testing and Validation with Ground Truth

- [ ] T245 [US6] Execute end-to-end testing: All 37 integrated tools with cross-domain workflow validation vs Ground Truth behavior
- [ ] T246 [P] [US6] Performance validation: Load testing confirms all domain SLAs (Security <1s, Productivity <2s, TCG <3s, Infrastructure <5s) vs original baselines
- [ ] T247 [P] [US6] Security penetration testing: Integrated tools maintain original security posture
- [ ] T248 [P] [US6] Accessibility validation: WCAG 2.1 AA compliance with executive function accommodations
- [ ] T249 [US6] User acceptance testing: Validate executive function support improvements with Ground Truth comparison

### Phase 8c: Production Deployment and Documentation

- [ ] T250 [P] [US6] Setup production infrastructure: Configure monitoring, alerting, and deployment pipelines for unified platform
- [ ] T251 [P] [US6] Create operational runbooks: Troubleshooting guides for all 37 integrated tools in docs/operations/
- [ ] T252 [P] [US6] Setup comprehensive monitoring: Health checks, performance metrics, and alerting for entire platform
- [ ] T253 [US6] Deploy to production environment: Full platform deployment with rollback capabilities and validation
- [ ] T254 [US6] Validate constitutional compliance: Confirm 37-tool mental prosthetic platform meets all requirements

**Acceptance Criteria**: Production deployment operational, all 37 tools accessible through unified interface, constitutional requirements satisfied

---

---

## Dependencies and Parallel Execution

### User Story Completion Order

1. **Setup + Foundational** (Weeks 1-4) - Prerequisites for all user stories
2. **User Story 1 + User Story 2** (Weeks 5-12) - Can run in parallel (P1 priorities)
3. **User Story 3 + User Story 4** (Weeks 13-18) - Can run in parallel (P2 priorities, depend on US1+US2)
4. **User Story 5** (Weeks 19-20) - Depends on core platform (P3 priority)
5. **Production Polish** (Weeks 21-24) - Final validation and deployment

### Parallel Execution Examples per User Story

**User Story 1 - Dashboard Integration**:

- T025-T032 (Security domain) + T033-T039 (Productivity domain) + T040-T043 (TCG domain) + T044-T048 (Infrastructure domain) can run in parallel

**User Story 2 - Business Logic Preservation**:

- T053-T058 (Category A algorithms) can run in parallel
- T066-T070 (Category B domain logic) can run in parallel
- T064-T066 (Category C utilities) can run in parallel

**User Story 4 - Performance Optimization**:

- T093-T097 (Security optimization) + T098-T102 (Productivity optimization) + T103-T107 (TCG/Infrastructure optimization) can run in parallel

### Independent Test Criteria per User Story

**US1**: Dashboard provides access to all 37 tools through single interface
**US2**: Regression tests pass comparing original vs integrated tool behavior  
**US3**: AI provides contextual recommendations using data from multiple domains
**US4**: Performance measurements meet domain-specific SLA requirements
**US5**: Recovery scenarios complete within 15-minute objective

## Brownfield Implementation Strategy

**Critical Success Factors**:

- **Asset Relocation Process**: Must follow 6-step process for each of 37 tools
- **Validation-Driven**: 3,795 existing test files provide validation baseline
- **Business Logic Preservation**: Category A/B/C strategies based on complexity analysis
- **Constitutional Compliance**: Migration must meet all constitutional quality standards

**MVP Scope**: User Story 1 + User Story 2 (asset relocation + validation framework)
**Risk Mitigation**: Tool-by-tool migration with validation before features/ removal
**Success Criteria**: Features/ directory empty AND 100% test pass rate on relocated assets

---

## Summary

**Total Tasks**: 180+ tasks across 10 phases (26-28 weeks) including Phase N+1 Asset Deletion
**Project Scale**: EXTREME SCALE (37 projects) with comprehensive brownfield risk mitigation  
**User Stories**: 6 stories (Setup + 5 user stories) with independent test criteria and validation gates
**Brownfield Template Compliance**: Ground Truth → Port → Validate → Integrate loops, [Logic: file::function] tags, legacy testbed setup, asset deletion phase
**Ground Truth Framework**: Comprehensive Ground Truth testing against original 37 tools before any migration work
**Logic Migration Tags**: All migration tasks reference specific legacy code with [Logic: file::function] format per template requirement
**Validation-Driven**: Each phase includes validation tests that must fail initially until integration complete, then pass with Ground Truth accuracy
**Asset Deletion Strategy**: Phase N+1 safe removal of features/ directory only after 100% validation success
**CHK Requirements Coverage**: Enhanced with specific tasks addressing CHK041 (data format migration), CHK044 (concurrent access), CHK045 (responsive design), CHK081 (automated traceability)
**Validation Framework**: Comprehensive regression testing using existing 3,795 test files with Ground Truth baseline comparison
**Parallel Opportunities**: Domain-specific tasks can run simultaneously within phases with validation gates, enhanced [P] marking
**Critical Path**: Pre-Migration → Foundation → Asset Relocation → Validation → AI Enhancement → Performance → Rollback → Production → Asset Deletion
**Success Metrics**: Features/ directory empty + 100% Ground Truth test pass rate + constitutional compliance + CHK requirements satisfied + 15-minute rollback capability
**Quality Assurance**: Each task references specific analysis reports and preservation strategies from modular-analysis-repo-main/ with CHK requirement validation and brownfield template compliance

---

## 🔍 Brownfield Migration Completion Checklist

### Pre-Migration Validation (Phase 0)

- [ ] All 37 tools operational and baseline captured
- [ ] Comprehensive backup completed and verified
- [ ] System dependencies mapped and documented
- [ ] Rollback procedures tested and validated

### Asset Relocation Validation (Phases 1-3)

- [ ] All 37 tools successfully integrated into unified platform
- [ ] Original functionality preserved with 100% test pass rate
- [ ] UI patterns preserved with <200ms response times
- [ ] Cross-domain workflows functioning correctly

### Business Logic Preservation (Phase 4)

- [ ] Category A algorithms (6 tools) preserved as microservices with bit-perfect accuracy
- [ ] Category B domain logic (5 tools) preserved with workflow continuity
- [ ] Category C utilities integrated with API compatibility
- [ ] All 3,795 existing tests pass on integrated system

### Constitutional Compliance

- [ ] Features/ directory completely empty
- [ ] Domain-specific performance tiers met (Security <1s, Productivity <2s, TCG <3s, Infrastructure <5s)
- [ ] Executive function accommodations validated (<200ms UI interactions)
- [ ] 15-minute rollback capability verified for all components

### Risk Mitigation Verification

- [ ] Data migration completed with zero data loss
- [ ] Security model consolidation completed without vulnerabilities
- [ ] Technology ecosystem integration stable and performant
- [ ] Organizational transformation successfully managed
