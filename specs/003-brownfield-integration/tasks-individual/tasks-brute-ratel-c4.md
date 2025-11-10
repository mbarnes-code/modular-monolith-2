---
description: "Brute Ratel C4 Community Kit: Red team C2 framework integration"
parent_task: "../tasks.md#T107"
parent_phase: "Phase 5: Security Domain Migrations"
return_to: "../tasks.md#T108"
domain: "security"
target_service: "apps/security-service/src/c2-toolkit/"
legacy_path: "features/Brute-Ratel-C4-Community-Kit"
estimated_hours: 48
total_files: 11
total_loc: 974
critical_algorithms: 3  # DC enumeration, Slack notifications, Outlook harvesting
bof_modules: 7  # getdc, harvester, decltest, rename, shadowclone, vainject, plus examples
---

# Tasks: Brute Ratel C4 Community Kit - Red Team C2 Integration

**⬆️ PARENT TASK**: [`tasks.md#TXXX`](../tasks.md#TXXX)  
**⬇️ RETURN TO**: [`tasks.md#TXXX`](../tasks.md#TXXX)

---

## Handoff Context

**Called From**: `tasks.md` Phase 5, Task T107  
**Entry Condition**: Security service foundation ready (Phase 1-4 complete)  
**Exit Condition**: All tasks below complete + C2 toolkit operational  
**Return Action**: Mark T107 complete in parent `tasks.md`, proceed to T108

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Project Overview

**Type**: Community-contributed security tools for Brute Ratel C4 Command & Control framework  
**Purpose**: Red team operations and adversary emulation capabilities  
**Domain**: Security - Post-exploitation, credential harvesting, domain reconnaissance  
**Codebase**: 974 LOC across 11 files (C, Python, Shell, C#)

**Critical Components**:
1. **Beacon Object Files (BOFs)** - In-memory execution modules for stealth operations
2. **Notification System** - Real-time Slack integration for operational awareness
3. **Credential Harvesting** - Outlook contact extraction via COM automation
4. **Domain Reconnaissance** - Active Directory enumeration capabilities
5. **SSL/TLS Infrastructure** - Secure C2 communications

**Mental Prosthetic Platform Integration**:
- **Priority**: CRITICAL - Core security domain tool
- **Value**: Red team capabilities for security assessments
- **Users**: ~5,000+ security researchers and penetration testers
- **Business Logic**: 100% preservation required (operational security critical)

**Key Challenges**:
- Windows-specific code (C BOFs with Windows API dependencies)
- BRc4 framework coupling (tight integration required)
- Cross-platform concerns (C# utilities, Windows-only operations)
- Real-time notification requirements (operational awareness)

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/security-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/Brute-Ratel-C4-Community-Kit/` accessible
- [ ] Project analysis report validated (brute_ratel_c4_community_kit_analysis.md)
- [ ] Windows development environment available (for C BOF compilation testing)
- [ ] Python 3.x environment configured
- [ ] SSL/TLS certificate infrastructure accessible

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## Migration Strategy: Framework-Agnostic C2 Toolkit

**Core Approach**: Extract operational intelligence while archiving Windows-specific implementations

**What to Migrate** (Business Logic + Cross-Platform Capabilities):
1. **Notification System** → Python-based real-time alerting (badgerNotifier.py)
2. **BOF Concepts** → Documentation and integration patterns
3. **Credential Harvesting Logic** → Algorithm preservation (platform-agnostic design)
4. **Domain Enumeration Patterns** → Reconnaissance methodology documentation
5. **SSL Infrastructure Scripts** → Certificate management automation

**What to Archive** (Windows-Specific Implementations):
1. **C BOF Modules** → Windows API dependencies (getdc.c, harvester.c, etc.)
2. **C# Utilities** → .NET Framework-specific code (patch_envexit/)
3. **PowerShell Templates** → Deprecated payloads (deprecated/ folder)
4. **Platform-Specific Makefiles** → Windows compilation configurations

**Integration Philosophy**:
- Preserve operational workflows and notification capabilities
- Document BOF patterns for future platform-specific implementations
- Maintain C2 framework integration concepts
- Enable cross-platform notification and monitoring

---

## Phase 1: Analysis Validation & Archive Preparation (4 hours)

**Purpose**: Validate project understanding and prepare comprehensive archive of Windows-specific code.

- [ ] T001 [Analysis: Section.1] Validate project analysis completeness: Confirm all BOF modules documented (7 modules)
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate C, Python, C#, PowerShell inventory
- [ ] T003 [Analysis: Section.4.1] Critical algorithm review: Document 3 critical algorithms (DC enum, Slack notifications, Outlook harvesting)
- [ ] T004 [Analysis: Section.11.1] Domain knowledge validation: Review red team operational concepts and C2 terminology
- [ ] T005 Create experimental archive structure: `experimental-archive/brute-ratel-c4-community-kit/`
- [ ] T006 [P] Archive Windows-specific BOFs: Move all .c files from bofs/ (getdc, harvester, decltest, rename, shadowclone, vainject)
- [ ] T007 [P] Archive C# utilities: Move patch_envexit/ directory (Windows process manipulation)
- [ ] T008 [P] Archive deprecated components: Move deprecated/ folder (PowerShell templates, YARA rules)
- [ ] T009 Create archive documentation: INDEX.md, README.md with migration rationale, REVIVAL-GUIDE.md for Windows deployment
- [ ] T010 Document BOF patterns: Create comprehensive guide for future BOF development (badger_exports.h API reference)

**Checkpoint**: All Windows-specific code archived with complete documentation.

---

## Phase 2: Notification System Migration (8 hours)

**Purpose**: Migrate Python-based Slack notification system with cross-platform compatibility.

**Migration Goal**: Real-time C2 check-in notifications via webhook integration  
**Analysis Reference**: Section.4.1 (Slack Notification Algorithm), Section.5.1 (Slack Webhooks Integration)  
**Independent Test**: Badger check-in JSON payload → Formatted Slack message delivery

### Phase 2a: Notification Domain Model

- [ ] T011 [Analysis: Section.2.1] Design BadgerConfig model: Port configuration structure (b_uid, b_h_name, b_p_name, b_pid, b_wver, b_bld)
- [ ] T012 [Analysis: Section.2.1] Create database schema: PostgreSQL tables for check-in history and notification logs
- [ ] T013 [P] Implement data models: SQLAlchemy/Pydantic models matching legacy JSON structure
- [ ] T014 [Ground Truth] Legacy notification test: Capture actual badgerNotifier.py behavior with sample payloads
- [ ] T015 Database migration: Alembic migration for notification tracking tables

**Checkpoint**: Data models ready for notification system.

### Phase 2b: Notification Business Logic Migration

- [ ] T016 [Analysis: Section.4.1] [Logic: badgerNotifier.py::do_POST] Preserve Slack notification algorithm
  - Parse JSON payload (content-length header → body → strip null terminators)
  - Extract badger configuration fields
  - Format message: "Badger *{b_id}* checked in as user *{b_uid}* from host *{b_h_name}*..."
  - POST to Slack webhook with error handling
- [ ] T017 [Analysis: Section.4.1] Implement notification formatting: Exact message template preservation
- [ ] T018 [Analysis: Section.5.1] Webhook integration: Migrate Slack API client with SSL verification control
- [ ] T019 [Analysis: Section.11.2] Configuration system: Replace hardcoded webhook URL with environment variable
- [ ] T020 [Validation Test] Notification parity test: Verify new implementation matches legacy format exactly

**Checkpoint**: Notification algorithm migrated with functional parity.

### Phase 2c: Notification API & Integration

- [ ] T021 [Analysis: Section.3.2] Endpoint: `POST /api/c2-toolkit/notifications` - Receive check-in payloads
- [ ] T022 [Analysis: Section.3.1] SSL/TLS configuration: Certificate-based authentication for C2 communications
- [ ] T023 [P] Error handling: Graceful degradation when Slack unavailable (log locally, continue operation)
- [ ] T024 [Analysis: Section.8.1] Performance validation: <200ms response time (excludes Slack API call)
- [ ] T025 Integration test: End-to-end notification delivery from C2 payload to Slack message

**Checkpoint**: Notification system operational with real-time alerting.

---

## Phase 3: SSL Certificate Management Migration (6 hours)

**Purpose**: Migrate certificate generation and management scripts for secure C2 communications.

**Migration Goal**: Automated SSL/TLS certificate lifecycle management  
**Analysis Reference**: Section.5.2 (Certificate Authentication), Section.5.3 (OpenSSL Server Integration)

### Phase 3a: Certificate Generation Migration

- [ ] T026 [Analysis: Section.5.2] [Logic: genssl.sh] Port certificate generation logic to Python
  - OpenSSL command composition for CSR and self-signed certificates
  - Configurable validity period (default 90 days)
  - Automated file permissions (600/400 for private keys)
- [ ] T027 [Ground Truth] Legacy certificate test: Validate genssl.sh output structure
- [ ] T028 [P] Certificate storage: Database schema for certificate metadata tracking
- [ ] T029 [Analysis: Section.11.2] Configuration extraction: Replace hardcoded paths with configurable storage

### Phase 3b: Certificate Lifecycle Management

- [ ] T030 Certificate monitoring: Automated expiry detection and renewal alerts
- [ ] T031 [Analysis: Section.5.3] OpenSSL server configuration: TLS/SSL server setup automation
- [ ] T032 Certificate validation: Chain validation and hostname verification implementation
- [ ] T033 [Validation Test] Certificate parity: Verify generated certificates match legacy format

**Checkpoint**: SSL infrastructure operational with automated lifecycle management.

---

## Phase 4: BOF Documentation & Integration Patterns (8 hours)

**Purpose**: Document BOF architecture and create integration framework (no C code migration).

**Migration Goal**: Preserve BOF operational knowledge without Windows-specific implementations  
**Analysis Reference**: Section.4.1 (BOF Algorithms), Section.11.1 (Domain Knowledge)

### Phase 4a: BOF Architecture Documentation

- [ ] T034 [Analysis: Section.11.1] Document BOF execution model: In-memory execution, coffee() entry point pattern
- [ ] T035 [Analysis: Section.4.1] Document badger_exports.h API: BadgerDispatch, BadgerAlloc, BadgerFree, memory management
- [ ] T036 [P] Create BOF development guide: Compilation workflow, framework integration, OPSEC considerations
- [ ] T037 [Analysis: Section.11.2] Document known limitations: Windows version compatibility, API dependencies

### Phase 4b: Operational Patterns Preservation

- [ ] T038 [Analysis: Section.4.1] Document DC enumeration pattern: NETAPI32$DsGetDcNameA usage, error handling
- [ ] T039 [Analysis: Section.4.1] Document Outlook harvesting pattern: COM automation, contact extraction algorithm
- [ ] T040 [Analysis: Section.11.3] Document operational workflows: BOF development → compilation → deployment → execution
- [ ] T041 Create BOF template repository: Starter templates for future platform-specific implementations

**Checkpoint**: BOF knowledge preserved without migrating Windows-specific code.

---

## Phase 5: Installation & Automation Scripts Migration (6 hours)

**Purpose**: Migrate installation automation and helper scripts.

**Migration Goal**: Platform-agnostic installation and setup automation  
**Analysis Reference**: Section.5.3 (Build System Integration)

- [ ] T042 [Analysis: Section.5.3] [Logic: install.sh] Port installation script to Python
  - Dependency detection (OpenSSL, Python packages)
  - Environment setup automation
  - Configuration file generation
- [ ] T043 [P] Create setup wizard: Interactive CLI for initial configuration
- [ ] T044 [P] Dependency management: Python requirements.txt for notification system
- [ ] T045 [Ground Truth] Legacy install test: Validate install.sh behavior baseline
- [ ] T046 [Validation Test] Installation parity: Verify new setup matches legacy environment

**Checkpoint**: Installation automation migrated with cross-platform support.

---

## Phase 6: Cross-Cutting Concerns & Integration (8 hours)

**Purpose**: Logging, monitoring, and platform integration.

**Analysis Reference**: Section.10.2 (Logging), Section.9.1 (Security Measures)

- [ ] T047 [Analysis: Section.10.2] Logging infrastructure: Structured logging for check-ins, notifications, errors
- [ ] T048 [Analysis: Section.8.1] Performance monitoring: Response time tracking, webhook latency metrics
- [ ] T049 [Analysis: Section.9.1] Security hardening: SSL certificate validation, webhook URL protection
- [ ] T050 [P] API documentation: OpenAPI/Swagger specs for notification endpoints
- [ ] T051 [Analysis: Section.3.1] Authentication integration: Certificate-based auth for C2 communications
- [ ] T052 Error handling standardization: Consistent error responses and exception logging
- [ ] T053 Configuration management: Environment variables for all configurable parameters

**Checkpoint**: Production-ready infrastructure with monitoring and security.

---

## Phase 7: Testing & Validation (8 hours)

**Purpose**: Comprehensive testing against analysis baselines.

**Analysis Reference**: Section.7.1 (Test Coverage), Section.8.1 (Performance Baselines)

- [ ] T054 [Analysis: Section.4.1] Notification algorithm test: Verify exact message formatting preservation
- [ ] T055 [Analysis: Section.5.1] Webhook integration test: Slack API interaction validation
- [ ] T056 [Analysis: Section.8.1] Performance benchmark: <200ms notification response, <1s including Slack
- [ ] T057 [P] SSL certificate test: Generation, validation, expiry detection
- [ ] T058 [P] Error handling test: Slack unavailable, malformed JSON, missing configuration
- [ ] T059 [Analysis: Section.11.3] Operational workflow test: Simulate complete check-in → notification flow
- [ ] T060 Integration test suite: End-to-end validation of all migrated components
- [ ] T061 Security testing: Certificate validation, webhook URL protection, log sanitization

**Checkpoint**: All tests passing with documented functional and performance parity.

---

## Summary Statistics

**Total Tasks**: 61  
**Estimated Hours**: 48  
**Components Migrated**: 5 (Notification system, SSL management, installation automation, BOF documentation, integration)  
**Components Archived**: 11 files (7 C BOFs, 3 C# utilities, deprecated PowerShell templates)  
**Code Migrated**: ~350 LOC (Python notification + SSL scripts)  
**Code Archived**: ~620 LOC (Windows-specific C/C# implementations)  
**Critical Algorithms Preserved**: 3 (DC enumeration patterns, Slack notifications, Outlook harvesting documentation)  
**Functional Parity**: 100% for cross-platform components (notification, SSL management)

---

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

**Purpose**: Validate project analysis findings and establish baseline testing environment.

- [ ] T001 [Analysis: Section.1] Validate project analysis completeness: Confirm all CRITICAL and IMPORTANT sections are filled
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate current tech stack inventory against actual codebase
- [ ] T003 [P] [Analysis: Section.7.1] Test coverage baseline: Run existing tests and document current coverage metrics
- [ ] T004 [Analysis: Section.8.1] Performance baseline: Measure and document current performance characteristics
- [ ] T005 [Ground Truth] Setup legacy test environment: Create isolated environment for legacy system (Docker/VM) per Section.10.1
- [ ] T006 [Ground Truth] Validate legacy functionality: Run legacy system and confirm all critical workflows function
- [ ] T007 [P] Create new project structure per implementation plan
- [ ] T008 [P] Initialize target framework dependencies (per analysis Section.1.2)

---

## Phase 2: Data Architecture Migration

**Purpose**: Migrate data models and database schema based on analysis Section 2.

- [ ] T009 [Analysis: Section.2.1] Inventory data models: Create comprehensive list from analysis findings
- [ ] T010 [Analysis: Section.2.1] Database schema migration: Implement new schema preserving all relationships from Section.2.2
- [ ] T011 [P] [Analysis: Section.2.1] Port data models: Create new framework models matching legacy field mappings exactly
- [ ] T012 [Analysis: Section.2.3] Database performance patterns: Implement indexes and optimizations per analysis
- [ ] T013 [Ground Truth] Data validation tests: Write tests confirming data integrity and constraints
- [ ] T014 [Analysis: Section.2.1] Data migration scripts: Create scripts for existing data preservation

**Checkpoint**: Data layer migrated with full functional parity.

## Phase 3: Foundational Infrastructure

**Purpose**: Core application infrastructure based on analysis findings.

- [ ] T015 [Analysis: Section.3.1] Authentication/authorization framework: Implement exact auth patterns from Section.3.1
- [ ] T016 [Analysis: Section.9.1] Security measures: Implement all security patterns identified in analysis
- [ ] T017 [P] [Analysis: Section.3.2] API routing framework: Setup endpoint structure (empty routes initially)
- [ ] T018 [Analysis: Section.8.1] Performance monitoring: Implement baseline monitoring per Section.8.1
- [ ] T019 [Analysis: Section.7.1] Testing framework: Setup testing infrastructure matching current patterns
- [ ] T020 Configure error handling and logging infrastructure per Section.10.2

**Checkpoint**: Foundation ready with security and monitoring. NO business logic exists.

## Phase 4: Critical Business Logic Migration (Feature 1) 🎯 MVP

**Migration Goal**: [Brief description based on Analysis Section.4.1 findings]

**Analysis Reference**: Section.4.1 - Critical Algorithms, Section.11.1 - Domain Knowledge

**Independent Test**: [Test case from Analysis Section.4.1 or domain requirements]

### Phase 4a: Analysis Cross-Reference & Ground Truth

- [ ] T021 [Analysis: Section.4.1] Algorithm analysis: Review critical algorithm documentation for this feature
- [ ] T022 [Analysis: Section.11.1] Domain knowledge review: Document business rules and domain concepts
- [ ] T023 [P] [F1] [Analysis: Section.4.1] [Logic: <legacy_file::function>] Ground Truth Test: Write test proving original behavior matches analysis documentation
- [ ] T024 [P] [F1] [Analysis: Section.4.1] [Logic: <legacy_file::function>] Validation Test: Create target framework test (initially failing)
- [ ] T025 [Analysis: Section.8.1] Performance baseline: Document current performance metrics for this feature

### Phase 4b: Incremental Migration & Validation

- [ ] T026 [F1] [Analysis: Section.4.1] [Logic: <legacy_file::function>] Algorithm preservation: Port exact business logic maintaining complexity characteristics
- [ ] T027 [F1] [Analysis: Section.4.1] [Logic: <legacy_file::function>] Validation execution: Run new test against ported logic - MUST pass
- [ ] T028 [F1] [Analysis: Section.11.2] Edge case handling: Implement all quirks and workarounds documented in analysis
- [ ] T029 [F1] [Analysis: Section.3.2] API integration: Wire proven logic into endpoint structure
- [ ] T030 [F1] [Analysis: Section.8.1] Performance validation: Confirm new implementation meets baseline metrics
- [ ] T031 [F1] Integration test: End-to-end validation of feature functionality

**Checkpoint**: Critical feature migrated with documented functional and performance parity.

## Phase 5: Security & Authorization Migration (Feature 2)

**Migration Goal**: [Based on Analysis Section.3.1 and Section.9.1 findings]

**Analysis Reference**: Section.3.1 - Authentication/Authorization, Section.9.1 - Security Measures

**Independent Test**: [Test case from Analysis Section.3.1 authorization patterns]

### Phase 5a: Security Analysis Integration

- [ ] T032 [Analysis: Section.3.1] Authorization pattern analysis: Document current access control implementation
- [ ] T033 [Analysis: Section.9.1] Security measures inventory: Review all security patterns to preserve
- [ ] T034 [P] [F2] [Analysis: Section.3.1] [Logic: <legacy_file::function>] Ground Truth Test: Prove current authorization behavior
- [ ] T035 [P] [F2] [Analysis: Section.3.1] [Logic: <legacy_file::function>] Validation Test: Create target authorization test

### Phase 5b: Authorization Migration

- [ ] T036 [F2] [Analysis: Section.3.1] [Logic: <legacy_file::function>] Authorization logic port: Implement exact access control patterns
- [ ] T037 [F2] [Analysis: Section.9.1] Security validation: Ensure all security measures maintained
- [ ] T038 [F2] [Analysis: Section.3.1] Authorization integration: Wire into API framework
- [ ] T039 [F2] Security testing: Validate all authorization scenarios

**Checkpoint**: Authorization and security patterns migrated with full parity.

## Phase 6: External Integrations Migration

**Migration Goal**: Preserve all third-party service integrations per Analysis Section.5

**Analysis Reference**: Section.5.1 - Third-party APIs, Section.5.2 - Auth Providers

### Phase 6a: Integration Analysis & Testing

- [ ] T040 [Analysis: Section.5.1] External API inventory: Document all third-party integrations
- [ ] T041 [Analysis: Section.5.1] Integration testing: Validate current external service connections
- [ ] T042 [P] [Analysis: Section.5.1] API client migration: Port all external API clients
- [ ] T043 [Analysis: Section.5.1] Error handling preservation: Maintain all fallback behaviors

### Phase 6b: Integration Validation

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

- [ ] T053 [Analysis: Section.11.1] Domain concept validation: Ensure all business rules preserved
- [ ] T054 [Analysis: Section.11.2] Quirk implementation: Implement all documented workarounds
- [ ] T055 [Analysis: Section.11.3] User behavior patterns: Validate user workflow preservation
- [ ] T056 [P] Documentation updates reflecting analysis findings

## Phase N: Cross-Cutting Concerns & Polish

- [ ] TXXX [Analysis: Section.10.2] Logging and monitoring: Implement analysis-documented patterns
- [ ] TXXX [Analysis: Section.9.2] Security hardening: Final security validation
- [ ] TXXX [P] Code cleanup and refactoring (target framework only)
- [ ] TXXX [Analysis: Section.13.1] Documentation updates incorporating analysis findings

## Phase N+1: Migration Validation & Asset Retirement

**Purpose**: Comprehensive validation before legacy asset removal.

### Phase N+1a: Complete Migration Validation

- [ ] TXXX [Analysis: All Sections] Full analysis cross-reference: Verify all analysis findings addressed
- [ ] TXXX [Analysis: Section.4.1] Algorithm parity validation: Confirm all critical algorithms function identically
- [ ] TXXX [Analysis: Section.8.1] Performance regression testing: Validate performance meets or exceeds baselines
- [ ] TXXX [Analysis: Section.12.3] Success criteria verification: Confirm all analysis success criteria met
- [ ] TXXX Verify Full Migration: Confirm all [Logic: ...] tags have corresponding passing validation tests
- [ ] TXXX Run Full Regression Suite: Execute complete test suite including ground truth comparisons

### Phase N+1b: Safe Asset Retirement

- [ ] TXXX [Analysis: Section.12.2] Risk mitigation: Address all identified migration risks
- [ ] TXXX Legacy asset backup: Create secure archive of legacy codebase before deletion
- [ ] TXXX Production validation: Run new system in production-like environment
- [ ] TXXX Stakeholder approval: Obtain sign-off from all analysis-identified stakeholders
- [ ] TXXX Delete Legacy Asset: After 100% validation, remove legacy asset directory

### Phase N+1c: Post-Migration Monitoring

- [ ] TXXX [Analysis: Section.10.2] Monitoring validation: Confirm monitoring systems capture same metrics
- [ ] TXXX [Analysis: Section.8.1] Performance monitoring: Track performance against established baselines
- [ ] TXXX [Analysis: Section.11.3] User behavior monitoring: Validate user workflow preservation

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

- [ ] All tasks T001-T061 marked complete above
- [ ] Archive complete: `experimental-archive/brute-ratel-c4-community-kit/` contains all Windows-specific code
- [ ] Archive documentation complete: INDEX.md, README.md, REVIVAL-GUIDE.md with BOF deployment instructions
- [ ] Notification system migrated: Python badgerNotifier logic ported to FastAPI
- [ ] SSL infrastructure migrated: Certificate generation and management automated
- [ ] BOF documentation complete: Architecture guide, API reference, operational patterns preserved
- [ ] Integration tests pass: `pytest tests/security/c2-toolkit/ -v` (100% pass rate)
- [ ] Performance met: Notification response <200ms, Slack delivery <1s total
- [ ] Slack webhook integration validated: Real check-in payloads → formatted messages delivered
- [ ] Certificate generation validated: Automated SSL/TLS certificate creation with proper permissions
- [ ] Configuration externalized: No hardcoded webhook URLs or paths (environment variables)
- [ ] Security hardening complete: SSL validation, webhook protection, log sanitization
- [ ] API documentation complete: OpenAPI/Swagger specs for notification endpoints
- [ ] Migration validation documented in `migration-validation.md`
- [ ] Windows-specific code properly archived (no migration attempts for platform-dependent BOFs)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:

1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/c2-toolkit/test_brute_ratel_integration.py -v --cov`
3. Document completion in `migration-validation.md`:

```markdown
### Brute Ratel C4 Community Kit Integration (T107)

- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Approach**: Hybrid migration (notification system + SSL automation migrated, Windows BOFs archived)
- **Estimated Hours**: 48
- **Actual Hours**: [ACTUAL]
- **Components Migrated**: 5 (Notification system, SSL management, installation scripts, BOF documentation, integration)
- **Components Archived**: 11 files (7 C BOFs, 3 C# utilities, deprecated PowerShell)
- **Code Migrated**: ~350 LOC (Python notification + SSL automation)
- **Code Archived**: ~620 LOC (Windows-specific implementations)
- **Functional Parity**: 100% for cross-platform components
- **Tests**: [PASSED]/[TOTAL] passed
- **Performance**: Notification <200ms ✓, Slack delivery <1s ✓
- **Notes**: Windows-specific BOF modules archived with comprehensive documentation. Notification system and SSL management successfully migrated to Python/FastAPI with environment-based configuration. BOF operational patterns and development workflows fully documented for future platform-specific implementations.
```

4. Mark parent task T107 complete in `tasks.md`
5. Proceed to return task T108 in `tasks.md`

---

## Final Validation Matrix

| Component                 | Target                       | Status |
| ------------------------- | ---------------------------- | ------ |
| Notification System       | Python/FastAPI migration complete | ⏳     |
| Slack Integration         | Webhook delivery functional   | ⏳     |
| SSL Certificate Management| Automated generation working  | ⏳     |
| BOF Documentation         | Comprehensive architecture guide | ⏳     |
| Installation Automation   | Cross-platform setup scripts  | ⏳     |
| API Endpoints             | OpenAPI documented & tested   | ⏳     |
| Performance (Notifications)| <200ms response time         | ⏳     |
| Performance (Slack)       | <1s total delivery time      | ⏳     |
| Configuration Management  | Environment variables (no hardcoded values) | ⏳     |
| Security Hardening        | SSL validation, webhook protection | ⏳     |
| Windows BOFs Archived     | All 7 BOF modules preserved  | ⏳     |
| C# Utilities Archived     | Process manipulation code preserved | ⏳     |
| Archive Documentation     | Revival guide with deployment steps | ⏳     |

**Success Criteria**: All table rows marked ✅ before marking parent task complete.

---

## Migration Strategy Notes

**Hybrid Approach Rationale**:

This migration uses a **selective migration strategy** based on platform compatibility:

**Migrated (Cross-Platform Value)**:
- **Notification System**: Pure Python → FastAPI (platform-agnostic)
- **SSL Management**: OpenSSL wrappers → Python automation (works anywhere)
- **Installation Scripts**: Bash → Python (cross-platform compatibility)
- **Operational Knowledge**: BOF patterns → comprehensive documentation

**Archived (Windows-Specific)**:
- **C BOF Modules**: Windows API dependencies (getdc.c, harvester.c, etc.)
- **C# Utilities**: .NET Framework coupling (patch_envexit/)
- **PowerShell Templates**: Windows PowerShell specific (deprecated/)

**Key Decision**: Archive Windows-specific implementations rather than attempting cross-platform migration of platform-locked code. Preserve operational intelligence and cross-platform tooling.

**Future-Proofing**: BOF architecture documentation enables future implementation on other platforms (Linux, macOS) using native APIs when required.

**Value Preservation**: 100% of cross-platform operational capabilities maintained (notifications, SSL management, installation automation) while Windows-specific code remains accessible in archive for reference or Windows-only deployments.
- [ ] Ground truth tests confirm functional parity with legacy
- [ ] Legacy `features/brute-ratel-c4/` backed up to `archive/`
- [ ] Migration completion documented in `migration-validation.md`
- [ ] All analysis findings from project_analysis_report.md addressed
- [ ] No regressions in existing functionality
- [ ] Security audit passed (if applicable)
- [ ] Accessibility compliance maintained (WCAG 2.1 AA)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:
1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/test_brute_ratel_c4_integration.py`
3. Document completion in `migration-validation.md`
4. Mark parent task TXXX complete in `tasks.md`
5. Proceed to return task (next in sequence) in `tasks.md`

**Documentation Update Required**:
```markdown
# In migration-validation.md

### Brute Ratel C4 Community Kit Migration (TXXX)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: XX
- **Actual Hours**: XX
- **Tests**: X passed, 0 failed
- **Performance**: All baselines met/exceeded
- **Notes**: [Any notable achievements or challenges]
```

