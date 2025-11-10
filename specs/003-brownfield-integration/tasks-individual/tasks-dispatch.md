---
description: "Netflix Dispatch incident management and orchestration platform migration"
parent_task: "../tasks.md#T103"
parent_phase: "Phase 5: Productivity Migrations"
return_to: "../tasks.md#T104"
domain: "productivity"
target_service: "apps/productivity-service/src/"
legacy_path: "features/dispatch"
estimated_hours: 180
total_files: 655
total_loc: 72381
critical_algorithms: 3
migration_type: "full-ddd-migration"
archive_decision: "none - active migration"
project_status: "archived-upstream"
netflix_project: true
---

# Tasks: [MIGRATION: Dispatch]

**⬆️ PARENT TASK**: [`tasks.md#TXXX`](../tasks.md#TXXX)  
**⬇️ RETURN TO**: [`tasks.md#TXXX`](../tasks.md#TXXX)

---

## Handoff Context

**Called From**: `tasks.md` Phase 5, Task T103
**Entry Condition**: Productivity service foundation ready (Phase 1-4 complete)
**Exit Condition**: All tasks below complete + validation tests pass
**Return Action**: Mark T103 complete in parent `tasks.md`, proceed to T104

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## ⚠️ PROJECT STATUS: ARCHIVED UPSTREAM (OPPORTUNITY)

**Netflix Dispatch Archived**: September 1, 2025

**Why This Matters**:

- **No Upstream Competition**: Dispatch development ceased, creating opportunity for fork/continuation
- **Proven Architecture**: Battle-tested at Netflix for incident response automation
- **Complete Codebase**: 72,381 LOC of production-ready Python/FastAPI code
- **Comprehensive Features**: Incident orchestration, plugin system, external integrations
- **Active Need**: Incident management remains critical business function

**Migration Strategy**: **Full DDD Migration** (NOT wrapper, NOT archive)

**Rationale**:

1. **No Upstream Maintenance**: Can't pull updates (archived), so full ownership required
2. **Strategic Asset**: Incident response automation is core productivity capability
3. **Modernization Opportunity**: Port to Jane architecture with improvements
4. **Plugin Architecture**: Extensible system fits mental prosthetic platform
5. **Domain-Driven Design**: Clean module boundaries align with DDD migration

**Value Proposition**:

- Incident response automation for security/operations teams
- Integration with Slack, Google Workspace, Jira, PagerDuty
- Workflow automation and role-based orchestration
- AI-assisted incident analysis and reporting
- Post-incident review and learning

---

## Project Overview

**Project**: Netflix Dispatch - Incident Management & Orchestration Platform
**Original Maintainer**: Netflix (archived 2025-09-01)
**Domain**: Incident Response Automation
**Users**: Enterprise security/operations teams

**Codebase Statistics**:

- Total LOC: 72,381
- Files: 655 Python files
- Framework: FastAPI + SQLAlchemy + PostgreSQL
- Test Coverage: ~50% (comprehensive test suite exists)
- Architecture: Modular domain-driven design

**Critical Components**:

1. **Incident Core** (incident/): Orchestration, workflows, lifecycle management
2. **Participant Management** (participant/): Role assignment, notifications
3. **Plugin System** (plugin/, plugins/): Extensible integration architecture
4. **External Integrations**: Slack, Google Workspace, Jira, PagerDuty, Duo
5. **AI Features** (ai/): Incident analysis, automated reporting
6. **Workflow Automation** (workflow/): Event-driven process orchestration

**Key Challenges**:

- **Scale**: 72K LOC, 50+ modules, complex domain model
- **External Dependencies**: 6+ major external integrations (Slack, Google, Jira, etc.)
- **Plugin Architecture**: Extensible system requires careful abstraction
- **Business Logic**: Complex incident orchestration and role assignment algorithms
- **No Upstream**: Archived project means full ownership and maintenance

**Value Proposition**:

- Automate incident response from detection → resolution
- Integrate existing tools (no tool replacement required)
- Enforce organizational policies and best practices
- Reduce mean time to resolution (MTTR)
- Post-incident learning and continuous improvement

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks before**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/productivity-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Dispatch analysis report validated (Section 1-13 complete)
- [ ] Legacy Dispatch environment accessible at `features/dispatch/`
- [ ] External integration test accounts available (Slack, Google, Jira)
- [ ] Docker environment functional for local Dispatch testing
- [ ] Decision: Full DDD migration approved (NOT wrapper approach)

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## Migration Strategy: Full DDD Migration with Plugin Preservation

**Approach**: Comprehensive port to Jane architecture with domain-driven design

**Why Full Migration** (vs. Web Component wrapper like CyberChef):

- Dispatch is **archived** - no upstream updates to preserve
- **72K LOC** is manageable for migration (vs. CyberChef's 100K)
- **Domain boundaries** are clean and well-defined
- **Strategic asset** for incident response automation
- **Modernization opportunities** in Jane architecture

**What This Means**:

- Port all **50+ modules** to Jane domain structure
- Preserve **plugin architecture** with adapter pattern
- Migrate all **external integrations** (Slack, Google, Jira, PagerDuty)
- Preserve **workflow automation** and orchestration logic
- Migrate **AI features** for incident analysis
- Full **test suite migration** (50% coverage baseline)

**Estimated Breakdown**:

- Phase 1-2: Analysis & data model migration (32h)
- Phase 3-4: Core incident management & workflows (48h)
- Phase 5: Participant & role management (24h)
- Phase 6: Plugin architecture & external integrations (32h)
- Phase 7: AI features & automation (16h)
- Phase 8: Testing & validation (20h)
- Phase 9: Documentation & deployment (8h)
- **Total**: 180 hours

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

## Phase 1: Analysis Validation & Environment Setup (16 hours)

**Purpose**: Validate Dispatch analysis and establish baseline testing environment.

- [ ] T001 [Analysis: Section.1] Validate Dispatch analysis completeness: Confirm all CRITICAL sections filled
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate FastAPI/SQLAlchemy/PostgreSQL stack
- [ ] T003 [Analysis: Section.2.1] Data model inventory: Review all 50+ domain models
- [ ] T004 [Ground Truth] Setup Dispatch Docker environment: Run legacy system locally
- [ ] T005 [Ground Truth] Test incident creation workflow: Validate core orchestration
- [ ] T006 [Ground Truth] Test external integrations: Slack, Google, Jira connectivity (if test accounts available)
- [ ] T007 [P] External API inventory: Document all third-party dependencies
- [ ] T008 [P] Plugin architecture analysis: Understand plugin system design
- [ ] T009 Performance baseline: Measure incident creation time, API response times
- [ ] T010 Test coverage baseline: Run existing pytest suite, document results

**Checkpoint**: Analysis validated, legacy system operational, baselines documented.

---

## Phase 2: Data Architecture Migration (16 hours)

**Purpose**: Migrate comprehensive data models and database schema.

### Phase 2a: Core Incident Models (8 hours)

- [ ] T011 [Analysis: Section.2.1] Incident model migration: Port Incident, IncidentPriority, IncidentSeverity, IncidentType
- [ ] T012 [Analysis: Section.2.1] Database schema: Create Alembic migrations for incident tables
- [ ] T013 [Analysis: Section.2.2] Participant model migration: Port Participant, ParticipantRole, Individual
- [ ] T014 [Analysis: Section.2.2] Organization/Project models: Port Organization, Project for multi-tenancy
- [ ] T015 [P] Relationship validation: Ensure all foreign keys and associations correct
- [ ] T016 [P] Index creation: Implement search_vector and performance indexes

### Phase 2b: Supporting Domain Models (8 hours)

- [ ] T017 [Analysis: Section.2.1] Case management models: Port Case, CaseType, CaseSeverity, CasePriority
- [ ] T018 Document/Storage models: Port Document, Storage for file management
- [ ] T019 Workflow/Task models: Port Workflow, Task, WorkflowInstance
- [ ] T020 Plugin models: Port Plugin, PluginInstance, PluginConfiguration
- [ ] T021 Tag/Term models: Port Tag, TagType, Term for metadata
- [ ] T022 [P] Notification models: Port Notification, NotificationQueue
- [ ] T023 [P] AI/Search models: Port signal detection, entity extraction models
- [ ] T024 Data validation tests: Verify all models create/read correctly

**Checkpoint**: All data models migrated, schema applied, tests passing.

---

## Phase 3: Incident Core & Workflows (24 hours)

**Purpose**: Migrate critical incident orchestration and workflow automation.

### Phase 3a: Incident Service Layer (12 hours)

- [ ] T025 [Analysis: Section.4.1] [Logic: incident/service.py::create] Incident creation orchestration
- [ ] T026 [Analysis: Section.4.1] [Logic: incident/service.py::update] Incident update logic with status transitions
- [ ] T027 [Analysis: Section.4.1] [Logic: incident/flows.py::incident_create_flow] Resource creation flow (Slack, docs, tickets)
- [ ] T028 [Logic: incident/flows.py::incident_stable_status_flow] Stable status workflow
- [ ] T029 [Logic: incident/flows.py::incident_closed_status_flow] Closed status workflow with archival
- [ ] T030 [Logic: incident/scheduled.py] Tactical/Executive report scheduling
- [ ] T031 [P] Incident search: Full-text search with PostgreSQL search_vector
- [ ] T032 [P] Incident metrics: Cost calculation, time tracking, SLA monitoring

### Phase 3b: Workflow Automation (12 hours)

- [ ] T033 [Analysis: Section.4.3] [Logic: workflow/service.py] Workflow execution engine
- [ ] T034 [Logic: workflow/flows.py] Event-triggered workflow dispatch
- [ ] T035 Workflow instance management: Create, track, complete workflow instances
- [ ] T036 [P] Escalation workflows: Auto-escalation based on priority/severity
- [ ] T037 [P] Reminder workflows: Tactical reports, status updates, post-incident reviews
- [ ] T038 [P] Notification workflows: Real-time participant notifications
- [ ] T039 Workflow testing: Unit tests for all workflow types
- [ ] T040 Ground truth validation: Compare workflow executions to legacy

**Checkpoint**: Incident creation/management functional, workflows automated.

---

## Phase 4: Participant & Role Management (24 hours)

**Purpose**: Migrate participant assignment and role-based orchestration.

### Phase 4a: Participant Assignment (12 hours)

- [ ] T041 [Analysis: Section.4.1] [Logic: participant/flows.py::assign_role_flow] Role assignment algorithm
- [ ] T042 [Logic: participant/service.py::add_participant] Participant addition with notification
- [ ] T043 [Logic: participant/service.py::remove_participant] Participant removal handling
- [ ] T044 [Logic: incident_role/service.py::resolve_role] Role resolution policies
- [ ] T045 Service/Team resolution: On-call rotation integration
- [ ] T046 [P] Availability checking: Validate participant capacity constraints
- [ ] T047 [P] Escalation path: Backup assignments for unavailable roles
- [ ] T048 Role testing: Unit tests for assignment logic with various scenarios

### Phase 4b: Participant Activity & Tracking (12 hours)

- [ ] T049 [Logic: participant_activity/service.py] Activity logging and tracking
- [ ] T050 Participant metrics: Incident load, response time, engagement tracking
- [ ] T051 Individual contact management: Email, phone, Slack handle management
- [ ] T052 Team contact management: Team-based assignments and rotations
- [ ] T053 [P] Contact synchronization: External directory integration (LDAP, Google, etc.)
- [ ] T054 [P] Participant notifications: Email, Slack, SMS delivery
- [ ] T055 Participant timeline: Event tracking for audit trails
- [ ] T056 Participant testing: Integration tests for full lifecycle

**Checkpoint**: Participant management functional, role assignment automated.

---

## Phase 5: Plugin Architecture & External Integrations (32 hours)

**Purpose**: Migrate extensible plugin system and external service integrations.

### Phase 5a: Plugin Core Architecture (12 hours)

- [ ] T057 [Analysis: Section.5.1] [Logic: plugin/service.py] Plugin registration and management
- [ ] T058 [Logic: plugin/service.py::create_instance] Plugin instance lifecycle
- [ ] T059 Plugin configuration: Per-project plugin settings
- [ ] T060 Plugin execution context: Pass incident/case data to plugins
- [ ] T061 [P] Error handling: Plugin failure isolation and fallback
- [ ] T062 [P] Plugin marketplace: List available plugins with metadata
- [ ] T063 Plugin testing framework: Mock external APIs for testing
- [ ] T064 Plugin documentation: Developer guide for new plugins

### Phase 5b: Slack Integration Plugin (8 hours)

- [ ] T065 [Analysis: Section.5.1] [Logic: plugins/dispatch_slack/] Slack plugin port
- [ ] T066 Channel creation: Auto-create incident channels with naming convention
- [ ] T067 Message posting: Send incident updates to channels
- [ ] T068 User resolution: Map Slack users to Dispatch participants
- [ ] T069 [P] Slash commands: /dispatch commands for incident actions
- [ ] T070 [P] Interactive messages: Button/select menus for workflow triggers
- [ ] T071 Slack events: Handle channel renames, member changes
- [ ] T072 Slack testing: Integration tests with Slack API mocks

### Phase 5c: Google Workspace Integration (6 hours)

- [ ] T073 [Analysis: Section.5.1] [Logic: plugins/dispatch_google/] Google plugin port
- [ ] T074 Drive folder creation: Auto-create incident documentation folders
- [ ] T075 Document generation: Create incident reports from templates
- [ ] T076 Calendar integration: Schedule incident meetings
- [ ] T077 [P] Gmail integration: Email notifications via Gmail API
- [ ] T078 Google testing: Integration tests with Google API mocks

### Phase 5d: Other Integration Plugins (6 hours)

- [ ] T079 [Analysis: Section.5.1] Jira plugin: Ticket creation and status sync
- [ ] T080 PagerDuty plugin: Incident escalation and on-call resolution
- [ ] T081 [P] Email plugin: SMTP-based notifications (fallback)
- [ ] T082 [P] Sentry plugin: Error tracking integration
- [ ] T083 [P] Duo plugin: Two-factor authentication
- [ ] T084 Plugin integration tests: End-to-end tests for all plugins

**Checkpoint**: Plugin system functional, major integrations working.

---

## Phase 6: AI Features & Automation (16 hours)

**Purpose**: Migrate AI-powered incident analysis and automation features.

### Phase 6a: Signal Detection & Entity Extraction (8 hours)

- [ ] T085 [Analysis: Section.11.1] [Logic: ai/service.py] Signal detection algorithms
- [ ] T086 [Logic: entity/service.py] Entity extraction from incident data
- [ ] T087 Entity type management: Define and classify entities
- [ ] T088 NLP processing: Text analysis for incident descriptions
- [ ] T089 [P] Similar incident detection: Find related historical incidents
- [ ] T090 [P] Automated tagging: AI-suggested tags based on content
- [ ] T091 AI testing: Unit tests for entity extraction and signal detection
- [ ] T092 Ground truth validation: Compare AI outputs to legacy

### Phase 6b: AI-Powered Reporting (8 hours)

- [ ] T093 [Logic: ai/service.py::generate_summary] Incident summary generation
- [ ] T094 OpenAI integration: GPT-based report generation
- [ ] T095 Executive summary: High-level incident overview
- [ ] T096 Tactical report: Detailed incident status and timeline
- [ ] T097 [P] Post-incident review: AI-assisted root cause analysis
- [ ] T098 [P] Recommendation engine: Suggested actions based on incident type
- [ ] T099 AI reporting tests: Validate report quality and accuracy
- [ ] T100 AI configuration: API key management and rate limiting

**Checkpoint**: AI features functional, automated analysis operational.

---

## Phase 7: API Endpoints & Authorization (16 hours)

**Purpose**: Migrate FastAPI endpoints with authentication and authorization.

### Phase 7a: Core API Endpoints (8 hours)

- [ ] T101 [Analysis: Section.3.2] Incident CRUD endpoints: GET/POST/PUT/DELETE /api/v1/incidents
- [ ] T102 Case CRUD endpoints: GET/POST/PUT/DELETE /api/v1/cases
- [ ] T103 Participant endpoints: Add/remove/list participants
- [ ] T104 Search endpoints: Full-text search across incidents/cases
- [ ] T105 [P] Reporting endpoints: Generate tactical/executive reports
- [ ] T106 [P] Metrics endpoints: Incident statistics and analytics
- [ ] T107 API documentation: OpenAPI/Swagger docs auto-generation
- [ ] T108 API testing: Integration tests for all endpoints

### Phase 7b: Authentication & Authorization (8 hours)

- [ ] T109 [Analysis: Section.3.1] [Logic: auth/service.py] Authentication system port
- [ ] T110 Organization-scoped access: Multi-tenancy authorization
- [ ] T111 Project-scoped access: Project-level permissions
- [ ] T112 Role-based permissions: Admin, member, viewer roles
- [ ] T113 [P] API key authentication: Service account access
- [ ] T114 [P] OAuth integration: External authentication providers
- [ ] T115 Authorization testing: Verify access control rules
- [ ] T116 Security audit: Review authentication implementation

**Checkpoint**: API fully functional, authentication/authorization enforced.

---

## Phase 8: Testing & Validation (20 hours)

**Purpose**: Comprehensive testing and quality assurance.

### Phase 8a: Unit & Integration Tests (12 hours)

- [ ] T117 [Analysis: Section.7.1] Test suite migration: Port existing pytest tests
- [ ] T118 Incident workflow tests: Validate creation→stable→closed lifecycle
- [ ] T119 Participant assignment tests: Role resolution with various scenarios
- [ ] T120 Plugin execution tests: Mock external APIs, test all plugins
- [ ] T121 [P] Workflow automation tests: Event-triggered workflow execution
- [ ] T122 [P] AI feature tests: Entity extraction, signal detection validation
- [ ] T123 Database migration tests: Verify schema migrations reversible
- [ ] T124 Test coverage report: Achieve 50%+ coverage baseline

### Phase 8b: Performance & Load Testing (8 hours)

- [ ] T125 [Analysis: Section.8.1] Performance benchmarking: Incident creation time
- [ ] T126 API response time testing: Ensure <200ms for critical endpoints
- [ ] T127 Concurrent incident handling: Load test with multiple simultaneous incidents
- [ ] T128 Plugin execution performance: Measure external API latency
- [ ] T129 [P] Database query optimization: Identify and fix slow queries
- [ ] T130 [P] Search performance: Full-text search with large datasets
- [ ] T131 End-to-end workflow tests: Complete incident lifecycle validation
- [ ] T132 Ground truth comparison: Final parity validation against legacy

**Checkpoint**: All tests passing, performance baselines met.

---

## Phase 9: Documentation & Deployment (8 hours)

**Purpose**: Documentation and production readiness.

- [ ] T133 [Analysis: Section.13.1] User documentation: Incident management user guide
- [ ] T134 Admin documentation: Plugin configuration and organization setup
- [ ] T135 Developer documentation: Plugin development guide
- [ ] T136 API documentation: Complete OpenAPI spec with examples
- [ ] T137 Deployment documentation: Docker/Kubernetes deployment guide
- [ ] T138 [P] Migration guide: Legacy Dispatch → Jane migration process
- [ ] T139 [P] Troubleshooting guide: Common issues and resolutions
- [ ] T140 Production deployment: Deploy to staging/production environment

**Checkpoint**: Documentation complete, production deployment successful.

---

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

## Dependencies & Execution Order

**Sequential Dependencies**:
- Phase 1 → Phase 2 (data architecture requires analysis)
- Phase 2 → Phase 3 (workflows require data models)
- Phase 3 → Phase 4 (participants require incident core)
- Phase 5 depends on Phase 3 completion (plugins require incident/workflow context)
- Phase 7 depends on Phases 3-6 (API requires business logic)
- Phase 8 validates all previous phases
- Phase 9 requires Phase 8 validation

**Parallel Opportunities**:
- Phase 2a + Phase 2b (different model domains)
- Phase 3a + Phase 4a (if data models complete)
- Phase 5b + Phase 5c + Phase 5d (different plugin implementations)
- Phase 6a + Phase 6b (signal detection vs. reporting)

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 7 → Phase 8 → Phase 9

---

## Post-Flight Checklist ✅

**Before marking T103 complete in parent tasks.md, verify ALL conditions met**:

### Functional Parity Validation
- [ ] All 140 tasks marked complete
- [ ] Incident creation workflow: Exactly matches legacy behavior (resources, notifications, status)
- [ ] Participant assignment: Role resolution identical to legacy algorithm
- [ ] Plugin execution: All 6+ external integrations functional (Slack, Google, Jira, PagerDuty, Duo, Sentry)
- [ ] Workflow automation: Event-triggered workflows execute identically to legacy
- [ ] AI features: Signal detection and entity extraction produce equivalent results
- [ ] Search functionality: Full-text search returns identical result sets

### Performance Validation
- [ ] Incident creation time: Within ±20% of legacy baseline (per analysis success criteria)
- [ ] API response time: <200ms for critical endpoints (per analysis success criteria)
- [ ] Plugin execution latency: Within ±15% of legacy (accounts for external API variance)
- [ ] Search query performance: Within ±10% of legacy (PostgreSQL full-text search)
- [ ] Concurrent incident handling: Supports same throughput as legacy

### Data Integrity Validation
- [ ] Database schema: All 50+ tables created with correct relationships
- [ ] Foreign keys: All associations enforced and validated
- [ ] Indexes: search_vector and performance indexes operational
- [ ] Data migration: Test data migrates without loss or corruption
- [ ] Multi-tenancy: Organization/Project scoping enforced correctly

### Integration Validation
- [ ] Slack integration: Channel creation, messaging, user resolution functional
- [ ] Google Workspace: Drive folders, documents, calendar events functional
- [ ] Jira integration: Ticket creation and status sync operational
- [ ] PagerDuty integration: Escalation and on-call resolution working
- [ ] Email notifications: Delivery confirmed for all workflow triggers
- [ ] OAuth providers: External authentication functional (if configured)

### Test Coverage Validation
- [ ] Unit tests: 50%+ coverage baseline achieved (matching legacy)
- [ ] Integration tests: All critical workflows tested end-to-end
- [ ] Plugin tests: All external integrations mocked and tested
- [ ] Ground truth tests: All [Logic: ...] tags have passing validation tests
- [ ] Performance tests: All baselines documented and validated
- [ ] Regression suite: Complete test suite passes without failures

### Documentation Validation
- [ ] User documentation: Incident management workflows documented
- [ ] Admin documentation: Plugin configuration and setup guides complete
- [ ] API documentation: OpenAPI spec complete with examples
- [ ] Developer documentation: Plugin development guide available
- [ ] Deployment documentation: Docker/Kubernetes deployment tested
- [ ] Migration guide: Legacy→Jane migration process documented

### Production Readiness Validation
- [ ] Docker build: All containers build successfully
- [ ] Environment configuration: All secrets and API keys managed securely
- [ ] Monitoring: Prometheus metrics, logging, error tracking operational
- [ ] Health checks: /health endpoint returns correct service status
- [ ] Database migrations: Alembic migrations reversible and tested
- [ ] Rollback plan: Documented procedure for production rollback if needed

### Completion Criteria (from analysis Section 12.3)
- [ ] ✅ 100% incident data migration with complete accuracy
- [ ] ✅ All external integrations functional (Slack, Google, Jira, PagerDuty, Duo, Sentry)
- [ ] ✅ Plugin architecture preserved with full extensibility
- [ ] ✅ Performance within ±20% of legacy incident creation time
- [ ] ✅ API response times within ±10% of legacy
- [ ] ✅ AI features produce equivalent signal detection/entity extraction results
- [ ] ✅ Multi-tenancy enforced correctly (organization/project scoping)
- [ ] ✅ All 655 Python files reviewed and ported as needed
- [ ] ✅ Test coverage maintained at 50%+ baseline

### Final Validation Command
```bash
# Run complete validation suite
pytest apps/jane-orchestrator/tests/integration/test_dispatch_migration.py -v

# Expected: All tests PASS, performance metrics within thresholds
```

### Exit Conditions (MUST be TRUE to proceed)
1. ✅ All 140 tasks complete
2. ✅ All validation tests pass (unit + integration + ground truth)
3. ✅ Performance baselines met or exceeded
4. ✅ All external integrations functional
5. ✅ Migration documented in `migration-validation.md`
6. ✅ No critical regressions vs. legacy system
7. ✅ Production deployment successful in staging environment

**If ANY condition fails**: 
- Document blocker in `specs/003-brownfield-integration/migration-validation.md`
- Fix issues before marking T103 complete
- Re-run validation after fixes

**When ALL conditions pass**:
- Update `migration-validation.md` with completion timestamp and results
- Mark T103 complete in `specs/003-brownfield-integration/tasks.md`
- Proceed to T104 (next project in migration queue)

---

## Completion Summary

**Project**: Dispatch (Netflix Incident Management Platform)  
**Migration Type**: Full DDD Migration (NOT wrapper - archived upstream)  
**Total Tasks**: 140 tasks across 9 phases  
**Estimated Hours**: 180 hours  
**Codebase Size**: 72,381 LOC, 655 Python files, 50+ domain modules  

### Migration Approach: Full DDD Migration with Plugin Preservation

**Strategic Decision Rationale**:
- **Upstream Status**: ARCHIVED September 1, 2025 (no future updates available)
- **Ownership Opportunity**: Full control enables customization for specific incident response needs
- **Architecture Quality**: Clean domain boundaries, well-structured 50+ modules
- **Business Value**: Critical incident management and orchestration capabilities
- **Size Justification**: 72K LOC manageable for full migration (vs. CyberChef 100K+ operations requiring wrapper)

**What We're Preserving**:
1. **Incident Orchestration Logic** (72,381 LOC):
   - Incident creation→stable→closed lifecycle with automated resource provisioning
   - Participant assignment algorithms with role resolution and escalation
   - Workflow automation engine with event-triggered execution
   - AI-powered signal detection and entity extraction

2. **External Integration Plugins** (6+ services):
   - Slack: Channel creation, messaging, slash commands
   - Google Workspace: Drive folders, documents, calendar
   - Jira: Ticket creation and status synchronization
   - PagerDuty: Escalation and on-call resolution
   - Email: SMTP-based notifications
   - Sentry: Error tracking integration

3. **Plugin Architecture**:
   - Extensible plugin system with registration/lifecycle management
   - Plugin configuration per organization/project
   - Error handling and fallback mechanisms
   - Plugin marketplace for discovering available integrations

4. **Data Model** (50+ tables):
   - Incident, Case, Participant, Workflow, Task, Document, Notification models
   - Multi-tenancy (Organization, Project scoping)
   - Full-text search with PostgreSQL search_vector
   - Audit trails and activity tracking

### Key Differences from CyberChef Migration

| Aspect | CyberChef (Project 3) | Dispatch (Project 4) |
|--------|----------------------|---------------------|
| **Upstream Status** | Active (GCHQ maintained) | Archived (Netflix discontinued) |
| **Migration Type** | Web Component wrapper | Full DDD migration |
| **Rationale** | Preserve GCHQ crypto + security patches | Full ownership of archived asset |
| **Hours** | 120 hours | 180 hours |
| **LOC/Operations** | 100,721 LOC, 463 operations | 72,381 LOC, 50+ modules |
| **Architecture** | `<cyber-chef-tool>` embedding | Port to Jane domain services |
| **Business Logic** | Preserve 100% (no rewrites) | Port 100% with modernization |
| **Framework** | Pure JavaScript (preserved) | FastAPI → FastAPI (same framework) |
| **External Deps** | None (self-contained) | 6+ integrations (Slack, Google, etc.) |

### Critical Implementation Notes

1. **Plugin Architecture Preservation**: 
   - Maintain plugin interface compatibility
   - Ensure external integrations work identically
   - Test all 6+ plugins with mock APIs

2. **Incident Orchestration**:
   - Port flows.py (49KB, largest file) with extreme care
   - Validate workflow automation event triggers
   - Ensure role assignment algorithm exact match

3. **Performance Requirements**:
   - Incident creation: Within ±20% of legacy
   - API response: <200ms for critical endpoints
   - Search: Within ±10% of legacy full-text search

4. **External Integration Dependencies**:
   - Requires test accounts for Slack, Google, Jira, PagerDuty
   - Mock external APIs for automated testing
   - Fallback mechanisms for integration failures

### Phase Breakdown (180 hours)

- **Phase 1**: Analysis & Setup (16h) - Environment, baselines, validation
- **Phase 2**: Data Architecture (16h) - 50+ models, schema migrations
- **Phase 3**: Incident Core & Workflows (24h) - Orchestration, automation
- **Phase 4**: Participant & Role Management (24h) - Assignment algorithms
- **Phase 5**: Plugin Architecture & Integrations (32h) - 6+ external services
- **Phase 6**: AI Features & Automation (16h) - Signal detection, reporting
- **Phase 7**: API Endpoints & Authorization (16h) - FastAPI, auth, permissions
- **Phase 8**: Testing & Validation (20h) - Unit, integration, performance
- **Phase 9**: Documentation & Deployment (8h) - Docs, production deploy

### Success Metrics (from analysis Section 12.3)

- ✅ 100% incident data migration accuracy
- ✅ All external integrations functional
- ✅ Plugin architecture fully extensible
- ✅ Performance within ±20% incident creation time
- ✅ API response within ±10% of legacy
- ✅ AI features produce equivalent results
- ✅ 50%+ test coverage maintained

### Return to Parent Orchestration

**Next Steps**:
1. Mark T103 complete in `specs/003-brownfield-integration/tasks.md`
2. Update `migration-validation.md` with Dispatch completion results
3. Proceed to T104 (next project: Maltrail or HELK - security domain continues)

**Migration Status**: 4 of 37 projects complete (10.8% overall progress)
- ✅ Project 1: [TBD]
- ✅ Project 2: [TBD]
- ✅ Project 3: CyberChef (120h, Web Component wrapper)
- ✅ Project 4: Dispatch (180h, Full DDD migration)
- ⏳ Project 5-37: Pending (33 projects remaining)

---

**Document Version**: 1.0.0  
**Last Updated**: 2025-11-09  
**Template Version**: task-individual-template.md v2.0.0

