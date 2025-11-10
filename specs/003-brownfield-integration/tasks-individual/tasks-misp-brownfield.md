---
description: "MISP Brownfield Asset Relocation - Ground Truth Migration"
---

# Tasks: [MIGRATION: MISP Threat Intelligence Platform]

**Input (Spec)**: Design documents from `/specs/002-mental-prosthetic-refinement/` 
**Input (Legacy)**: Legacy codebase path `/features/MISP/` 
**Prerequisites**: misp-business-logic-analysis.md (✓), phase8-misp-preservation-strategy.md (✓), **misp-analysis.md (MANDATORY ANALYSIS REPORT)** (✓), MISP_Asset_Relocation_After_Action_Review.md (✓)

**Project Analysis Integration**: This MISP migration MUST reference specific sections from misp-analysis.md:

- Section 2 (Data Architecture) - for Event, MispAttribute, and correlation models (8,733 lines of business logic)
- Section 3 (Business Logic) - for threat intelligence algorithms and validation rules
- Section 4 (API Architecture) - for REST API preservation and PyMISP compatibility
- Section 5 (Authentication/Security) - for RBAC, distribution controls, and security measures
- Section 6 (Infrastructure) - for performance baselines and scaling characteristics
- Section 7 (Dependencies) - for external integrations (SIEM, STIX, feeds)

**Critical Context**: This migration addresses the systematic failure identified in the after-action review where scaffolding was mistaken for implementation. **NO TASK IS COMPLETE WITHOUT DEMONSTRATED FUNCTIONAL EQUIVALENCE TO ORIGINAL MISP.**

**Tests**: Tests are MANDATORY and must validate against original MISP behavior. Ground Truth tests (testing original PHP code) must be written FIRST and pass before any Python implementation.

**Organization**: Tasks are grouped by MISP business logic features to ensure 1:1 functional parity with the original 8,733 lines of threat intelligence algorithms.

## Format: [ID] [P?] [Feature] [Analysis: Section.#] [Logic: <legacy_file::function>] Description

- [P]: Can run in parallel
- [Feature]: Which MISP feature this task belongs to (e.g., F1: Event Publishing, F2: Access Control, F3: Correlation)
- [Analysis]: Reference to misp-analysis.md section (e.g., Section.2.1, Section.3.1, Section.4.1)
- [Logic]: The exact legacy PHP code being replaced. **This is not optional.**

## Path Conventions

- **New Project**: `apps/jane-orchestrator/src/` (integrated monolith)
- **Legacy Project**: `features/MISP/app/Model/` and `features/MISP/app/Controller/`
- **Analysis Report**: `misp-analysis.md` sections for validation and cross-reference
- **Ground Truth Tests**: `tests/brownfield/misp/php/` (original behavior validation)
- **Validation Tests**: `tests/brownfield/misp/python/` (new implementation validation)

---

## Phase 1: Analysis Validation & Legacy Environment Setup

**Purpose**: Validate misp-analysis.md findings and establish comprehensive baseline testing environment.

- [ ] T001 [Analysis: All Sections] Validate project analysis completeness: Confirm all CRITICAL sections (2,3,4,5) filled with MISP-specific data
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate CakePHP 2.x, MySQL/PostgreSQL, PHP 7.4+ against actual MISP installation
- [ ] T003 [Analysis: Section.2.1] Data model cross-reference: Validate Event.php (8,733 lines) and MispAttribute.php (4,198 lines) analysis accuracy
- [ ] T004 [Analysis: Section.3.1] Business logic verification: Confirm threat intelligence algorithms documented in analysis
- [ ] T005 [Analysis: Section.6.3] Performance baseline measurement: Document current MISP correlation processing and sync performance
- [ ] T006 [Ground Truth] Setup Docker environment for legacy MISP (CakePHP + MySQL) per analysis Section.6.1 requirements
- [ ] T007 [Ground Truth] Configure MISP test database with representative threat intelligence data matching analysis Section.2.1 models
- [ ] T008 [Ground Truth] Verify original MISP critical functions: publishRouter, beforeFind, correlateValue per analysis Section.3.1
- [ ] T009 Remove existing skeletal MISP implementation that provides false completion signal
- [ ] T010 [P] Create new project structure per implementation plan
- [ ] T011 [P] Initialize Python project with FastAPI dependencies matching analysis Section.1.2 requirements

**Checkpoint**: Analysis validated, original MISP running and testable. NO new Python code exists yet.

---

## Phase 2: Data Architecture Migration

**Purpose**: Migrate MISP data models and database schema based on analysis Section 2.

- [ ] T012 [Analysis: Section.2.1] Inventory MISP data models: Create comprehensive list of 50+ models from analysis findings
- [ ] T013 [Analysis: Section.2.1] Event model migration: Implement Event model preserving all 50+ fields from analysis Section.2.1
- [ ] T014 [Analysis: Section.2.1] MispAttribute model migration: Implement MispAttribute model with correlation relationships from analysis
- [ ] T015 [Analysis: Section.2.2] Database schema implementation: Create PostgreSQL schema preserving all MISP relationships from analysis Section.2.2
- [ ] T016 [Analysis: Section.2.3] Performance optimization: Implement indexes and query patterns per analysis Section.2.3
- [ ] T017 [Analysis: Section.2.1] Organization and User models: Implement RBAC foundation models per analysis Section.5.2
- [ ] T018 [Ground Truth] Data validation tests: Write tests confirming data integrity matches MISP constraints
- [ ] T019 [Analysis: Section.2.1] Data migration scripts: Create scripts for existing MISP data preservation
- [ ] T020 [Analysis: Section.2.2] Correlation model implementation: Implement threat intelligence correlation data structures

**Checkpoint**: Data layer migrated with full functional parity to MISP data architecture.

## Phase 3: Foundational Infrastructure

**Purpose**: Core application infrastructure based on MISP analysis findings.

- [ ] T021 [Analysis: Section.5.1] Authentication framework: Implement MISP RBAC patterns from analysis Section.5.1
- [ ] T022 [Analysis: Section.5.3] Security measures: Implement input validation, XSS prevention per analysis Section.5.3
- [ ] T023 [Analysis: Section.4.1] API routing framework: Setup REST API structure matching MISP API from analysis Section.4.1
- [ ] T024 [Analysis: Section.6.3] Performance monitoring: Implement baseline monitoring per analysis Section.6.3
- [ ] T025 [Analysis: Section.5.2] Distribution control framework: Implement sharing group and distribution level infrastructure
- [ ] T026 [P] Testing framework: Setup testing infrastructure matching MISP patterns
- [ ] T027 Configure error handling and logging infrastructure per analysis Section.6.2
- [ ] T028 Setup service adapter framework in `libs/service-adapters/security/misp_adapter.py` (empty - populated by proven logic)

**Checkpoint**: Foundation ready with security and monitoring. NO business logic exists - prevents scaffolding confusion.

---

## Phase 4: Logic Migration (Feature 1 - Event Publishing System) 🎯 MVP

**Migration Goal**: Port the core event publication workflow that determines when and how threat intelligence events are shared across organizations.

**Analysis Reference**: Section.3.1 - Threat Intelligence Event Lifecycle, Section.2.1 - Event Model

**Original Asset**: `features/MISP/app/Model/Event.php::publishRouter` (lines 5074-5095) and `features/MISP/app/Model/Event.php::publish` (lines 5134-5200+)

**Independent Test**: "A 'Draft' event cannot be published. A 'Validated' event can be published, which updates published=1 and triggers sync to external servers."

### Phase 4a: Analysis Cross-Reference & Ground Truth

- [ ] T029 [Analysis: Section.3.1] Algorithm analysis: Review threat intelligence event lifecycle documentation from analysis
- [ ] T030 [Analysis: Section.2.1] Event model analysis: Document Event.php business rules from analysis Section.2.1
- [ ] T031 [Analysis: Section.6.3] Performance baseline: Document current publication performance metrics from analysis
- [ ] T032 [P] [F1] [Analysis: Section.3.1] [Logic: Event.php::publishRouter] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_publish_router.php` that proves original publishRouter function:
        - ACCEPTS event with published=0, analysis=2 (Completed) 
        - REJECTS event with published=0, analysis=0 (Initial)
        - REJECTS event with published=0, analysis=1 (Ongoing)
        - Updates event.published=1 on successful publication
        - Triggers background job when MISP.background_jobs=true
        - Returns proper success/failure response codes

- [ ] T015 [P] [F1] [Logic: Event.php::publish] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_publish_workflow.php` that proves original publish function:
        - Validates event exists and user has publication permissions
        - Processes ZeroMQ notifications if enabled
        - Handles Kafka notifications if configured  
        - Manages sync server push operations
        - Updates event modification timestamp
        - Handles publication state transitions correctly

- [ ] T036 [P] [F1] [Analysis: Section.3.1] [Logic: Event.php::publishRouter] Validation Test: Translate PHP test (T032) into Python pytest `tests/brownfield/misp/python/test_publish_router.py`. **This test MUST fail initially** as new code doesn't exist.

- [ ] T037 [P] [F1] [Analysis: Section.3.1] [Logic: Event.php::publish] Validation Test: Translate PHP test (T033) into Python pytest `tests/brownfield/misp/python/test_publish_workflow.py`. **This test MUST fail initially**.

### Phase 4b: Incremental Migration & Validation

**CRITICAL**: Do not proceed unless Ground Truth tests (T032-T033) pass against original MISP.

- [ ] T038 [F1] [Analysis: Section.2.1] [Logic: Event.php::Event] Algorithm preservation: Implement Event model in `apps/jane-orchestrator/src/data/models/event.py` with exact field mapping from analysis Section.2.1
- [ ] T039 [F1] [Analysis: Section.3.1] [Logic: Event.php::publishRouter] Port Logic: Implement `publish_router_py` function in `apps/jane-orchestrator/src/services/events/publication_service.py` maintaining analysis-documented complexity
- [ ] T040 [F1] [Analysis: Section.3.1] [Logic: Event.php::publishRouter] Validation execution: Execute pytest (T036) against new publish_router_py function. **IT MUST PASS.** Do not proceed until it passes.
- [ ] T041 [F1] [Analysis: Section.3.1] [Logic: Event.php::publish] Port Logic: Implement `publish_workflow_py` function with exact behavioral equivalent per analysis
- [ ] T042 [F1] [Analysis: Section.3.1] [Logic: Event.php::publish] Validation execution: Execute pytest (T037) against new publish_workflow_py function. **IT MUST PASS.**
- [ ] T043 [F1] [Analysis: Section.4.1] API integration: Create FastAPI endpoint `/api/events/{id}/publish` matching MISP API from analysis Section.4.1
- [ ] T044 [F1] [Analysis: Section.6.3] Performance validation: Confirm new implementation meets publication performance baseline from analysis
- [ ] T045 [F1] Integration test: Execute complete test suite validating end-to-end publication workflow

**Checkpoint**: Event Publishing feature is **provably equivalent** to original MISP. Any deviation fails validation.

---

## Phase 5: Security & Authorization Migration (Feature 2 - Distribution-Based Access Control) 🔒

**Migration Goal**: Port MISP's sophisticated access control system that determines which users/organizations can see which events based on distribution levels and sharing groups.

**Analysis Reference**: Section.5.2 - Authorization & Access Control, Section.3.1 - Information Sharing & Distribution Controls

**Original Asset**: `features/MISP/app/Model/Event.php::beforeFind`, `features/MISP/app/Model/AppModel.php`, distribution filtering logic

**Independent Test**: "User A (Org 1) cannot see User B's (Org 2) 'Organization only' event (distribution=0). User A can see User B's 'Community' event (distribution=1)."

### Phase 5a: Security Analysis Integration

- [ ] T046 [Analysis: Section.5.2] Authorization pattern analysis: Document RBAC implementation from analysis Section.5.2
- [ ] T047 [Analysis: Section.3.1] Distribution control analysis: Review sharing group patterns from analysis Section.3.1
- [ ] T048 [P] [F2] [Analysis: Section.5.2] [Logic: Event.php::beforeFind] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_access_control.php` that proves original access control:
        - Creates User A (Org 1) and User B (Org 2)
        - Creates Event with distribution=0 (Organization only) owned by User B
        - Creates Event with distribution=1 (Community) owned by User B  
        - Logs in as User A, queries events
        - Asserts User A sees distribution=1 event, NOT distribution=0 event
        - Tests all distribution levels: 0=Organization, 1=Community, 2=Connected, 3=All, 4=Sharing Group

- [ ] T026 [P] [F2] [Logic: SharingGroup.php] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_sharing_groups.php` that proves sharing group access:
        - Creates sharing group with specific organizations
        - Creates event with distribution=4, sharing_group_id set
        - Tests access for users in/out of sharing group
        - Validates sharing group inheritance rules

- [ ] T027 [P] [F2] [Logic: Event.php::beforeFind] Validation Test: Translate PHP test (T025) into Python pytest `tests/brownfield/misp/python/test_access_control.py`. **Must fail initially.**

- [ ] T028 [P] [F2] [Logic: SharingGroup.php] Validation Test: Translate PHP test (T026) into Python pytest `tests/brownfield/misp/python/test_sharing_groups.py`. **Must fail initially.**

### Phase 4b: Porting & Integration

- [ ] T029 [F2] [Logic: Event.php::beforeFind] Port Logic: Implement `filter_events_by_access` function in `apps/jane-orchestrator/src/services/events/access_control_service.py` with exact distribution filtering logic
- [ ] T030 [F2] [Logic: Event.php::beforeFind] Run Validation: Execute pytest (T027) against new access control logic. **MUST PASS.**
- [ ] T031 [F2] [Logic: SharingGroup.php] Port Logic: Implement sharing group access validation in `apps/jane-orchestrator/src/services/events/sharing_group_service.py`
- [ ] T032 [F2] [Logic: SharingGroup.php] Run Validation: Execute pytest (T028) against sharing group logic. **MUST PASS.**
- [ ] T033 [F2] Integrate Logic: Wire access control into main FastAPI `/api/events` endpoint with request user context
- [ ] T034 [F2] Integration Test: Create full workflow test that validates API respects access control for all distribution levels

**Checkpoint**: Distribution-based access control **provably equivalent** to original MISP security model.

---

## Phase 5: Logic Migration (Feature 3 - Threat Intelligence Correlation) 🔍

**Migration Goal**: Port MISP's correlation engine that identifies relationships between threat indicators across events.

**Original Asset**: `features/MISP/app/Model/Event.php::correlateValue`, correlation algorithms, attribute correlation logic

**Independent Test**: "When Attribute A (hash) is added to Event 1, system automatically identifies existing Attribute B (same hash) in Event 2 and creates correlation record."

### Phase 5a: Ground Truth & Validation (Write These First)

- [ ] T035 [P] [F3] [Logic: Event.php::correlateValue] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_correlation.php` that proves original correlation:
        - Creates Event 1 with MD5 hash attribute
        - Creates Event 2 with same MD5 hash attribute  
        - Triggers correlation processing
        - Validates correlation record created between events
        - Tests different attribute types (IP, domain, URL, etc.)
        - Validates correlation scoring and confidence

- [ ] T036 [P] [F3] [Logic: Attribute.php::correlate] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_attribute_correlation.php` for attribute-level correlation logic

- [ ] T037 [P] [F3] [Logic: Event.php::correlateValue] Validation Test: Translate PHP test (T035) to Python pytest `tests/brownfield/misp/python/test_correlation.py`. **Must fail initially.**

### Phase 5b: Porting & Integration

- [ ] T038 [F3] [Logic: Event.php::correlateValue] Port Logic: Implement correlation engine in `apps/jane-orchestrator/src/services/events/correlation_service.py`
- [ ] T039 [F3] [Logic: Event.php::correlateValue] Run Validation: Execute pytest (T037). **MUST PASS.**
- [ ] T040 [F3] Integrate Logic: Wire correlation into attribute creation/modification workflows
- [ ] T041 [F3] Integration Test: Validate correlation API endpoints return proper correlation data

**Checkpoint**: Threat intelligence correlation **provably equivalent** to original MISP algorithms.

---

## Phase 6: External Integrations Migration

**Migration Goal**: Preserve all third-party service integrations per Analysis Section.7

**Analysis Reference**: Section.7.1 - Core Dependencies, Section.7.2 - External System Integrations

### Phase 6a: Integration Analysis & Testing

- [ ] T084 [Analysis: Section.7.2] External API inventory: Document SIEM/SOAR integrations from analysis
- [ ] T085 [Analysis: Section.7.2] Integration testing: Validate current PyMISP and external service connections
- [ ] T086 [P] [Analysis: Section.7.2] API client migration: Port PyMISP compatibility and external API clients
- [ ] T087 [Analysis: Section.7.2] Error handling preservation: Maintain all fallback behaviors for external systems

### Phase 6b: Integration Validation

- [ ] T088 [Analysis: Section.7.2] Service connectivity: Test PyMISP compatibility and external integrations
- [ ] T089 [Analysis: Section.5.1] Authentication provider testing: Validate LDAP/SAML flows from analysis
- [ ] T090 [Analysis: Section.7.2] Caching strategy: Implement analysis-documented external service caching

**Checkpoint**: External integrations preserved with full PyMISP compatibility.

---

## Phase 7: Performance & Quality Assurance

**Migration Goal**: Meet or exceed MISP baseline performance per Analysis Section.6

**Analysis Reference**: Section.6.3 - Performance Optimization, Section.2.3 - Database Performance

### Phase 7a: Performance Validation

- [ ] T091 [Analysis: Section.6.3] Performance benchmarking: Measure new implementation against MISP correlation/sync baselines
- [ ] T092 [Analysis: Section.2.3] Database optimization: Ensure query performance matches analysis Section.2.3 patterns
- [ ] T093 [Analysis: Section.6.3] Scalability testing: Validate scaling characteristics for large MISP installations

### Phase 7b: Quality Assurance

- [ ] T094 [Analysis: Section.6.1] Configuration preservation: Implement all MISP configuration options from analysis
- [ ] T095 [Analysis: Section.3.2] Validation engine: Port ComplexTypeTool validation from analysis Section.3.2
- [ ] T096 [P] Critical workflow testing: Test all threat intelligence workflows end-to-end

**Checkpoint**: Performance meets or exceeds MISP baselines.

---

## Phase 8: Domain Knowledge Preservation

**Migration Goal**: Capture all MISP threat intelligence domain knowledge per Analysis Section.3

**Analysis Reference**: Section.3.1 - Core Business Rules, Section.3.2 - Validation & Business Logic

- [ ] T097 [Analysis: Section.3.1] Domain concept validation: Ensure all threat intelligence business rules preserved
- [ ] T098 [Analysis: Section.3.2] Validation preservation: Implement all ComplexTypeTool validation rules
- [ ] T099 [Analysis: Section.4.2] API compatibility: Validate complete MISP REST API compatibility
- [ ] T100 [P] Documentation updates reflecting MISP analysis findings

**Checkpoint**: All MISP domain knowledge and business rules preserved.

---

## Phase 9: Logic Migration (Feature 4 - STIX Import/Export) 📄

**Migration Goal**: Port MISP's STIX format handling for threat intelligence data exchange.

**Original Asset**: `features/MISP/app/Lib/Export/`, STIX export/import modules

**Independent Test**: "MISP event exports to valid STIX 2.1 format and can be imported back with 100% data fidelity."

### Phase 6a: Ground Truth & Validation 

- [ ] T042 [P] [F4] [Logic: StixExport.php] Ground Truth Test: Write PHP test for STIX export behavioral validation
- [ ] T043 [P] [F4] [Logic: StixImport.php] Ground Truth Test: Write PHP test for STIX import behavioral validation  
- [ ] T044 [P] [F4] [Logic: StixExport.php] Validation Test: Python pytest for STIX export. **Must fail initially.**

### Phase 6b: Porting & Integration

- [ ] T045 [F4] [Logic: StixExport.php] Port Logic: Implement STIX export in `apps/jane-orchestrator/src/services/export/stix_service.py`
- [ ] T046 [F4] [Logic: StixExport.php] Run Validation: Execute pytest. **MUST PASS.**
- [ ] T047 [F4] Integrate Logic: Create STIX export/import API endpoints

**Checkpoint**: STIX import/export **provably equivalent** to original MISP.

---

## Phase 7: Logic Migration (Feature 5 - Feed Management) 📡

**Migration Goal**: Port MISP's threat intelligence feed ingestion and processing system.

**Original Asset**: `features/MISP/app/Model/Feed.php`, feed processing workflows

### Phase 7a: Ground Truth & Validation

- [ ] T048 [P] [F5] [Logic: Feed.php::downloadAndParse] Ground Truth Test: Write PHP test for feed processing
- [ ] T049 [P] [F5] [Logic: Feed.php::downloadAndParse] Validation Test: Python pytest. **Must fail initially.**

### Phase 7b: Porting & Integration

- [ ] T050 [F5] [Logic: Feed.php::downloadAndParse] Port Logic: Implement feed processing
- [ ] T051 [F5] [Logic: Feed.php::downloadAndParse] Run Validation: Execute pytest. **MUST PASS.**

---

## Phase 7.1: Logic Migration (Feature 6 - Background Job Processing) ⚙️

**Migration Goal**: Port MISP's critical background job system for asynchronous processing of publications, correlations, and sync operations.

**Original Asset**: `features/MISP/app/Lib/Tools/BackgroundJobsTool.php`, `features/MISP/app/Console/Command/WorkerShell.php`, job queue management

**Independent Test**: "Publishing an event triggers background job that processes publication, correlation updates, and server synchronization without blocking UI."

### Phase 7.1a: Ground Truth & Validation

- [ ] T052 [P] [F6] [Logic: BackgroundJobsTool.php::enqueue] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_background_jobs.php` that proves job queuing:
        - Job creation with proper priority and type
        - Job processing by worker processes
        - Job status tracking and completion reporting
        - Failed job retry mechanism and error handling
        - Concurrent job processing without conflicts

- [ ] T053 [P] [F6] [Logic: WorkerShell.php::main] Ground Truth Test: Write PHP test for worker process behavior:
        - Worker process startup and job consumption
        - Graceful shutdown and job completion
        - Memory management and leak prevention
        - Error handling and job failure reporting

- [ ] T054 [P] [F6] [Logic: BackgroundJobsTool.php::enqueue] Validation Test: Python pytest `tests/brownfield/misp/python/test_background_jobs.py`. **Must fail initially.**

### Phase 7.1b: Porting & Integration

- [ ] T055 [F6] [Logic: BackgroundJobsTool.php::enqueue] Port Logic: Implement job queue system in `apps/jane-orchestrator/src/services/jobs/background_job_service.py`
- [ ] T056 [F6] [Logic: BackgroundJobsTool.php::enqueue] Run Validation: Execute pytest (T054). **MUST PASS.**
- [ ] T057 [F6] Integrate Logic: Wire background jobs into publication, correlation, and sync workflows

**Checkpoint**: Background job processing **provably equivalent** to original MISP async operations.

---

## Phase 7.2: Logic Migration (Feature 7 - Server Synchronization) 🔄

**Migration Goal**: Port MISP's server-to-server synchronization system for threat intelligence sharing between instances.

**Original Asset**: `features/MISP/app/Lib/Tools/ServerSyncTool.php`, `features/MISP/app/Model/Server.php`, sync protocols

**Independent Test**: "Changes to events are automatically pushed to configured sync servers with proper authentication and conflict resolution."

### Phase 7.2a: Ground Truth & Validation

- [ ] T058 [P] [F7] [Logic: ServerSyncTool.php::sync] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_server_sync.php` that proves sync behavior:
        - Authentication with remote MISP instances
        - Event push/pull operations with proper filtering
        - Conflict detection and resolution algorithms
        - Incremental sync and timestamp tracking
        - Error handling and retry mechanisms

- [ ] T059 [P] [F7] [Logic: Server.php::push] Ground Truth Test: Write PHP test for server push operations
- [ ] T060 [P] [F7] [Logic: ServerSyncTool.php::sync] Validation Test: Python pytest `tests/brownfield/misp/python/test_server_sync.py`. **Must fail initially.**

### Phase 7.2b: Porting & Integration

- [ ] T061 [F7] [Logic: ServerSyncTool.php::sync] Port Logic: Implement server sync in `apps/jane-orchestrator/src/services/sync/server_sync_service.py`
- [ ] T062 [F7] [Logic: ServerSyncTool.php::sync] Run Validation: Execute pytest (T060). **MUST PASS.**
- [ ] T063 [F7] Integrate Logic: Wire sync operations into event lifecycle and background jobs

**Checkpoint**: Server synchronization **provably equivalent** to original MISP multi-instance sharing.

---

## Phase 7.3: Logic Migration (Feature 8 - Workflow Engine) 🔧

**Migration Goal**: Port MISP's workflow automation system for event processing, enrichment, and response automation.

**Original Asset**: `features/MISP/app/Lib/WorkflowModules/`, workflow processing engine

**Independent Test**: "Workflows automatically trigger on event creation/modification, execute enrichment modules, and update event data based on configured rules."

### Phase 7.3a: Ground Truth & Validation

- [ ] T064 [P] [F8] [Logic: WorkflowModules] Ground Truth Test: Write PHP test for workflow execution
- [ ] T065 [P] [F8] [Logic: WorkflowModules] Validation Test: Python pytest. **Must fail initially.**

### Phase 7.3b: Porting & Integration

- [ ] T066 [F8] [Logic: WorkflowModules] Port Logic: Implement workflow engine
- [ ] T067 [F8] [Logic: WorkflowModules] Run Validation: Execute pytest. **MUST PASS.**

---

## Phase 7.4: Logic Migration (Feature 9 - Complex Export System) 📤

**Migration Goal**: Port MISP's comprehensive export system supporting 20+ formats for threat intelligence sharing.

**Original Asset**: `features/MISP/app/Lib/Export/` (25+ export modules including STIX, YARA, Suricata, etc.)

**Independent Test**: "Events export correctly to all supported formats (STIX 1.x/2.x, YARA, Suricata, CSV, etc.) with proper data transformation and format validation."

### Phase 7.4a: Ground Truth & Validation

- [ ] T068 [P] [F9] [Logic: Stix2Export.php] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_export_formats.php` for critical export formats:
        - STIX 2.x export with proper object relationships
        - YARA rule generation from attributes
        - Suricata rule export with network indicators
        - CSV export with proper data formatting
        - Format-specific validation and compliance

- [ ] T069 [P] [F9] [Logic: YaraExport.php] Ground Truth Test: Write PHP test for YARA rule generation
- [ ] T070 [P] [F9] [Logic: Stix2Export.php] Validation Test: Python pytest `tests/brownfield/misp/python/test_export_formats.py`. **Must fail initially.**

### Phase 7.4b: Porting & Integration

- [ ] T071 [F9] [Logic: Stix2Export.php] Port Logic: Implement export system in `apps/jane-orchestrator/src/services/export/export_service.py`
- [ ] T072 [F9] [Logic: Stix2Export.php] Run Validation: Execute pytest (T070). **MUST PASS.**
- [ ] T073 [F9] Integrate Logic: Create export API endpoints with format negotiation

**Checkpoint**: Export system **provably equivalent** to original MISP's 25+ export formats.

---

## Phase 8: Logic Migration (Feature 10 - Data Validation & Enrichment) 🔍

**Migration Goal**: Port MISP's sophisticated data validation and enrichment system for threat intelligence quality assurance.

**Original Asset**: `features/MISP/app/Lib/Tools/ComplexTypeTool.php`, `features/MISP/app/Lib/Tools/AttributeValidationTool.php`, validation frameworks

**Independent Test**: "Attributes are automatically validated by type (IP, domain, hash, etc.), enriched with additional context, and flagged for quality issues."

### Phase 8a: Ground Truth & Validation

- [ ] T074 [P] [F10] [Logic: ComplexTypeTool.php::checkComplexRouter] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_data_validation.php`:
        - Automatic type detection from attribute values
        - Format validation for all supported attribute types
        - Data enrichment and normalization processes
        - Quality scoring and confidence assessment
        - Duplicate detection and merging logic

- [ ] T075 [P] [F10] [Logic: AttributeValidationTool.php] Ground Truth Test: Write PHP test for attribute validation pipeline
- [ ] T076 [P] [F10] [Logic: ComplexTypeTool.php::checkComplexRouter] Validation Test: Python pytest `tests/brownfield/misp/python/test_data_validation.py`. **Must fail initially.**

### Phase 8b: Porting & Integration

- [ ] T077 [F10] [Logic: ComplexTypeTool.php::checkComplexRouter] Port Logic: Implement validation system in `apps/jane-orchestrator/src/services/validation/data_validation_service.py`
- [ ] T078 [F10] [Logic: ComplexTypeTool.php::checkComplexRouter] Run Validation: Execute pytest (T076). **MUST PASS.**
- [ ] T079 [F10] Integrate Logic: Wire validation into attribute creation/modification workflows

**Checkpoint**: Data validation and enrichment **provably equivalent** to original MISP quality assurance system.

---

## Phase 9: Frontend Migration (MISP Web Interface) 🖥️

**Goal**: Port MISP's web interface to React while preserving exact functionality.

**Original Asset**: `features/MISP/app/View/`, CakePHP views and JavaScript

### Phase 9a: Ground Truth & UI Validation

- [ ] T080 [P] [F11] [Logic: Events/view.ctp] Ground Truth Test: Write Playwright test capturing original MISP event view behavior
- [ ] T081 [P] [F11] [Logic: Events/index.ctp] Ground Truth Test: Write Playwright test for event listing with filters
- [ ] T082 [P] [F11] [Logic: Events/view.ctp] Validation Test: React component test. **Must fail initially.**

### Phase 9b: Component Porting

- [ ] T083 [F11] [Logic: Events/view.ctp] Port Logic: Implement EventView React component with exact UI behavior
- [ ] T084 [F11] [Logic: Events/view.ctp] Run Validation: Execute React tests. **MUST PASS.**
- [ ] T085 [F11] Integration Test: Full E2E test comparing original vs new UI workflows

---

## Phase 10: Logic Migration (Feature 11 - Event Lifecycle Management) 📋

**Migration Goal**: Port MISP's complete event lifecycle management including creation, modification, validation, and deletion workflows.

**Original Asset**: `features/MISP/app/Model/Event.php::beforeSave`, `features/MISP/app/Model/Event.php::afterSave`, lifecycle hooks

**Independent Test**: "Event creation triggers proper validation, UUID generation, timestamp management, and audit logging with user context preservation."

### Phase 10a: Ground Truth & Validation

- [ ] T086 [P] [F12] [Logic: Event.php::beforeSave] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_event_lifecycle.php`:
        - Automatic UUID generation and validation
        - Timestamp management for creation/modification
        - User context and organization assignment
        - Data validation and business rule enforcement
        - Audit trail creation and change tracking

- [ ] T087 [P] [F12] [Logic: Event.php::afterSave] Ground Truth Test: Write PHP test for post-save operations:
        - Automatic correlation triggering
        - Cache invalidation and updates
        - Notification system triggering
        - Index updates for search functionality

- [ ] T088 [P] [F12] [Logic: Event.php::beforeSave] Validation Test: Python pytest `tests/brownfield/misp/python/test_event_lifecycle.py`. **Must fail initially.**

### Phase 10b: Porting & Integration

- [ ] T089 [F12] [Logic: Event.php::beforeSave] Port Logic: Implement lifecycle management in `apps/jane-orchestrator/src/services/events/lifecycle_service.py`
- [ ] T090 [F12] [Logic: Event.php::beforeSave] Run Validation: Execute pytest (T088). **MUST PASS.**
- [ ] T091 [F12] Integrate Logic: Wire lifecycle hooks into all event operations

**Checkpoint**: Event lifecycle management **provably equivalent** to original MISP data integrity system.

---

## Phase 11: Logic Migration (Feature 12 - Advanced Search & Filtering) 🔎

**Migration Goal**: Port MISP's sophisticated search and filtering capabilities for threat intelligence discovery.

**Original Asset**: `features/MISP/app/Model/Event.php::fetchEventIds`, advanced query building, search optimization

**Independent Test**: "Complex searches with multiple filters (tags, attributes, timeframes, organizations) return accurate results with proper access control enforcement."

### Phase 11a: Ground Truth & Validation

- [ ] T092 [P] [F13] [Logic: Event.php::fetchEventIds] Ground Truth Test: Write PHP test `tests/brownfield/misp/php/test_advanced_search.php`:
        - Multi-criteria search with AND/OR logic
        - Tag-based filtering with taxonomy support
        - Temporal filtering with date ranges
        - Attribute-based search with type filtering
        - Full-text search across event metadata
        - Performance optimization for large datasets

- [ ] T093 [P] [F13] [Logic: Event.php::fetchEventIds] Validation Test: Python pytest `tests/brownfield/misp/python/test_advanced_search.py`. **Must fail initially.**

### Phase 11b: Porting & Integration

- [ ] T094 [F13] [Logic: Event.php::fetchEventIds] Port Logic: Implement search system in `apps/jane-orchestrator/src/services/search/advanced_search_service.py`
- [ ] T095 [F13] [Logic: Event.php::fetchEventIds] Run Validation: Execute pytest (T093). **MUST PASS.**
- [ ] T096 [F13] Integrate Logic: Create search API endpoints with query optimization

**Checkpoint**: Advanced search capabilities **provably equivalent** to original MISP discovery system.

---

## Phase 12: Service Adapter Integration 🔌

**Goal**: Create working service adapter that actually integrates MISP with the modular monolith.

- [ ] T097 [F14] Replace placeholder service adapter with functional implementation calling proven business logic
- [ ] T098 [F14] Implement adapter methods that delegate to proven services (publication, access control, correlation, sync, validation, search)
- [ ] T099 [F14] Validate adapter provides 100% API compatibility with existing integrations
- [ ] T100 [F14] Performance test: Ensure <1s response time requirement for security domain

---

## Phase 13: Full Integration Testing 🧪

**Goal**: Validate complete MISP integration works as unified system.

- [ ] T101 [F15] Run complete test suite: All Ground Truth tests still pass
- [ ] T102 [F15] Run complete validation suite: All Python implementation tests pass  
- [ ] T103 [F15] Cross-feature integration: Test complete workflows (creation → validation → publication → correlation → sync → export)
- [ ] T104 [F15] Performance validation: All operations meet <1s security domain requirement under production load
- [ ] T105 [F15] Security audit: Validate no vulnerabilities introduced in migration
- [ ] T106 [F15] Data integrity validation: Verify all data relationships and constraints preserved
- [ ] T107 [F15] User acceptance: Original MISP users validate functional equivalence across all features
- [ ] T108 [F15] Load testing: Validate system handles original MISP's capacity requirements
- [ ] T109 [F15] Failover testing: Validate error handling and recovery mechanisms

---

## Phase 14: Asset Deletion (The Final Step)

**Purpose**: Remove legacy code ONLY after complete functional validation.

**⚠️ CRITICAL**: Do not proceed unless ALL validation tests pass and stakeholders confirm functional equivalence.

- [ ] T110 Verify Full Migration: Confirm ALL [Logic: ...] tags have passing Ground Truth AND Validation tests
- [ ] T111 Run Complete Regression Suite: Execute all tests (Ground Truth + Validation + Integration) - ALL MUST PASS
- [ ] T112 Stakeholder Sign-off: Security team confirms new MISP provides equivalent threat intelligence capabilities
- [ ] T113 Performance Validation: Confirm <1s response times under production load for all operations
- [ ] T114 **FINAL VALIDATION**: Independent security audit confirms no capability gaps vs original MISP
- [ ] T115 Operational Readiness: Confirm monitoring, alerting, and maintenance procedures in place
- [ ] T116 Documentation Validation: Confirm all user and administrative documentation updated
- [ ] T117 Delete Legacy Asset: Only after 100% validation success, remove `features/MISP/` directory

---

## Implementation Strategy

### Critical Success Factors

1. **Ground Truth First**: NEVER write Python code without first proving PHP behavior
2. **Behavioral Equivalence**: New code must pass identical tests to original code
3. **No Scaffolding Without Logic**: Empty frameworks are prohibited until business logic is proven
4. **Continuous Validation**: Every change must maintain passing validation tests
5. **Independent Verification**: External validation required before claiming completion

### MVP Approach (Single Feature)

1. Complete Phase 1: Setup + Phase 2: Foundational
2. Complete Phase 3: Event Publishing (F1 ONLY) 
3. **STOP**: Validate F1 works identically to original MISP
4. Deploy/demo publishing functionality as MVP proof-of-concept

### Critical Feature Dependencies Identified

**High Priority (Core MISP Functionality)**:
- F1: Event Publishing System → F6: Background Job Processing (dependency)
- F2: Access Control → F7: Server Synchronization (uses distribution logic)
- F3: Correlation Engine → F10: Data Validation (requires validated data)
- F12: Event Lifecycle → All features (foundational dependency)

**Medium Priority (Operational Requirements)**:
- F4: STIX Import/Export → F9: Complex Export System (related functionality)
- F5: Feed Management → F6: Background Job Processing (async processing)
- F8: Workflow Engine → F6: Background Job Processing (async execution)

**Lower Priority (User Experience)**:
- F11: Web Interface → All backend features (presentation layer)
- F13: Advanced Search → F12: Event Lifecycle (search indexed data)

### Risk Mitigation

- **No Parallel Development**: Complete each feature fully before starting next
- **Validation Gate**: Each phase requires passing tests before proceeding  
- **Regression Prevention**: All previous tests must continue passing
- **External Audit**: Independent verification at key milestones

---

## Notes

---

## MISP Brownfield Migration Methodology Notes

**Task Completion Criteria:**
- [P] tasks = different files, no dependencies (can run in parallel)
- [Analysis] references are MANDATORY - every task must trace to misp-analysis.md findings
- [Logic] preservation is CRITICAL - exact MISP functional behavior must be maintained
- Ground Truth Test → Analysis Cross-Reference → Port Logic → Validate → Integrate (core loop)
- A task is not "done" when code is written - it's "done" when validation passes AND analysis criteria are met

**MISP-Specific Quality Gates:**
- Every phase has explicit checkpoints requiring validation before proceeding
- All critical MISP algorithms (Event.php 8,733 lines, MispAttribute.php 4,198 lines) must have functional parity tests
- All MISP performance baselines (correlation processing, sync operations) must be met or exceeded
- All threat intelligence domain knowledge must be preserved and validated
- PyMISP compatibility must be maintained throughout migration

**Risk Mitigation:**
- Analysis findings drive task creation - never skip misp-analysis.md integration
- Ground truth tests establish irrefutable MISP behavioral baselines
- Incremental migration reduces blast radius of changes to threat intelligence workflows
- Performance monitoring prevents regressions in correlation and sync operations
- Security validation ensures no degradation of MISP's sophisticated access controls

**Success Validation:**
- Functional parity: New system behaviors match MISP exactly (all 8,733 lines of Event.php logic)
- Performance parity: New system meets or exceeds MISP correlation and sync performance baselines
- Integration parity: PyMISP and all SIEM integrations continue working without changes
- Domain parity: All threat intelligence business rules and validation logic preserved
- Security parity: All MISP distribution controls and RBAC patterns maintained identically

### MISP Success Criteria

A task is **COMPLETE** when:
1. Ground Truth test passes against original MISP ✅
2. Analysis cross-reference validates against misp-analysis.md findings ✅
3. Validation test passes against Python implementation ✅  
4. Integration test confirms MISP API functionality ✅
5. Performance test meets MISP baseline requirements ✅
6. Security audit finds no degradation vs original MISP ✅

**The measure of success is functional equivalence to original MISP, not code completion.**
