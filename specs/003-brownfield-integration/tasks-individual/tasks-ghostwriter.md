---
description: "DDD-based asset relocation for Ghostwriter red team operations platform"
parent_task: "../tasks.md#TXXX"
parent_phase: "Phase X: Security Migrations"
return_to: "../tasks.md#TXXX"
domain: "security"
target_service: "apps/security-service/src/"
legacy_path: "features/Ghostwriter"
estimated_hours: 320
---

# Tasks: [MIGRATION: Ghostwriter - Red Team Operations Platform]

**⬆️ PARENT TASK**: [`tasks.md#TXXX`](../tasks.md#TXXX)  
**⬇️ RETURN TO**: [`tasks.md#TXXX`](../tasks.md#TXXX)

---

## Handoff Context

**Called From**: `tasks.md` Phase X, Task TXXX  
**Entry Condition**: Security service foundation ready (Phase 1-4 complete)  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark TXXX complete in parent `tasks.md`, proceed to next task

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/security-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/Ghostwriter/` accessible
- [ ] Project analysis report completed and validated (Ghostwriter-analysis.md)

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## Ghostwriter Domain Architecture Overview

**Platform Purpose**: Red team operations management - assessment coordination, infrastructure tracking, report generation

**Identified Bounded Contexts (DDD)**:
1. **Client Management (Rolodex)**: Client relationships, contacts, project assignments
2. **Reporting**: Finding library, report generation, evidence management, collaborative editing
3. **Infrastructure Management (Shepherd)**: Domain/server inventory, health monitoring, resource checkout
4. **Operations Logging (OpLog)**: Activity tracking, real-time collaboration, audit trails
5. **User Management**: Authentication, authorization, team coordination

**Cross-Cutting Concerns**:
- Real-time collaboration (Django Channels + WebSockets)
- GraphQL API (Hasura integration)
- Multi-factor authentication (Django Allauth + 2FA)
- External API integrations (AWS, DigitalOcean, Namecheap, VirusTotal)

**Legacy Structure**:
```
features/Ghostwriter/ghostwriter/
├── rolodex/          # Client Management BC
├── reporting/        # Reporting BC
├── shepherd/         # Infrastructure Management BC
├── oplog/            # Operations Logging BC
├── users/            # User Management BC
├── commandcenter/    # Global Settings
├── home/             # Dashboard
└── api/              # REST API Actions
```

**Target Structure** (Modular Monolith):
```
apps/security-service/src/
├── domains/
│   ├── client_management/     # Rolodex BC
│   ├── reporting/             # Reporting BC
│   ├── infrastructure/        # Shepherd BC
│   ├── operations/            # OpLog BC
│   └── shared/                # Cross-domain types
├── api/                       # GraphQL + REST endpoints
├── services/                  # Domain services
└── data/                      # Data models (organized by domain)
```

**Migration Strategy**: Domain-by-domain migration with shared kernel approach

**Migration Strategy**: Domain-by-domain migration with shared kernel approach

---

## Phase 1: Foundation & Analysis Validation

**Purpose**: Validate analysis findings, establish testing infrastructure, setup domain boundaries

- [ ] T001 [Analysis: Section.1] Validate project analysis completeness for all 5 bounded contexts
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Django 4.2, PostgreSQL, Redis, Hasura GraphQL
- [ ] T003 [Ground Truth] Setup legacy test environment: Docker compose with all Ghostwriter services
- [ ] T004 [Ground Truth] Validate legacy functionality: Run full test suite (1043+ tests)
- [ ] T005 [Analysis: Section.8.1] Performance baseline: Document current performance across all domains
- [ ] T006 [P] Create domain directory structure in `apps/security-service/src/domains/`
- [ ] T007 [P] Initialize shared kernel: Common types, exceptions, base classes
- [ ] T008 [Analysis: Section.7.1] Setup pytest infrastructure with domain isolation

**Checkpoint**: Foundation ready with validated analysis and test infrastructure

---

## Phase 2: Shared Kernel & Cross-Cutting Concerns

**Purpose**: Implement cross-domain infrastructure before domain migration

### Phase 2a: Data Layer Foundation

- [ ] T009 [Analysis: Section.2.1] Database schema design: Review all 5 domain models
- [ ] T010 [Analysis: Section.2.2] Shared models migration: User, tags, extra_fields pattern
- [ ] T011 [Analysis: Section.2.3] Database performance setup: Indexes, constraints, triggers
- [ ] T012 [P] [Logic: ghostwriter/users/models.py::User] Port User model with privilege system
- [ ] T013 [P] Create Alembic migrations for shared schema
- [ ] T014 [Ground Truth] Data integrity tests: Validate constraints and relationships

### Phase 2b: Authentication & Authorization Infrastructure

- [ ] T015 [Analysis: Section.3.1] [Logic: ghostwriter/users/models.py::User.is_privileged] Port privilege-based access control
- [ ] T016 [Analysis: Section.3.1] [Logic: config/settings/base.py::AUTHENTICATION_BACKENDS] Multi-factor authentication setup (Django Allauth + 2FA)
- [ ] T017 [Analysis: Section.3.1] JWT token generation for GraphQL API
- [ ] T018 [P] [Logic: ghostwriter/middleware.py] Port custom middleware (permission filtering, audit logging)
- [ ] T019 [Ground Truth] Auth integration tests: Session + JWT flows

### Phase 2c: GraphQL API Infrastructure

- [ ] T020 [Analysis: Section.3.2] Setup Hasura GraphQL Engine integration
- [ ] T021 [Analysis: Section.3.2] [Logic: config/urls.py::/graphql] GraphQL endpoint configuration
- [ ] T022 [Analysis: Section.3.2] Hasura permission webhook implementation
- [ ] T023 [Analysis: Section.3.3] WebSocket infrastructure for real-time features
- [ ] T024 [P] Apollo Client integration for frontend state management

**Checkpoint**: Shared infrastructure ready with auth, API, real-time support

---

## Phase 3: Domain 1 - Client Management (Rolodex BC) 🎯 MVP

**Business Value**: Core client relationship management - foundational for all other domains

**Analysis Reference**: Section.2.1 (Client/Project models), Section.11.1 (Assessment lifecycle)

### Phase 3a: Client Aggregate

- [ ] T025 [Analysis: Section.2.1] [Logic: rolodex/models.py::Client] Port Client entity with all fields
- [ ] T026 [Analysis: Section.2.1] [Logic: rolodex/models.py::Client.for_user] Implement privilege-based filtering
- [ ] T027 [P] [Logic: rolodex/models.py::ClientContact] Port ClientContact entity
- [ ] T028 [P] [Logic: rolodex/models.py::ClientInvite] Port ClientInvite for access control
- [ ] T029 [Analysis: Section.2.2] Client validation rules: unique name, timezone validation
- [ ] T030 [Ground Truth] Client CRUD tests: Verify exact legacy behavior

### Phase 3b: Project Aggregate

- [ ] T031 [Analysis: Section.2.1] [Logic: rolodex/models.py::Project] Port Project entity with lifecycle states
- [ ] T032 [Analysis: Section.4.3] [Logic: rolodex/models.py::Project state management] Project workflow state machine
- [ ] T033 [P] [Logic: rolodex/models.py::ProjectAssignment] Port team assignment functionality
- [ ] T034 [P] [Logic: rolodex/models.py::ProjectInvite] Port project invitation system
- [ ] T035 [P] [Logic: rolodex/models.py::ProjectType] Port project type classification
- [ ] T036 [Analysis: Section.2.2] Project validation: end_date > start_date, team requirements
- [ ] T037 [Ground Truth] Project lifecycle tests: PLANNING → ACTIVE → COMPLETE → ARCHIVED

### Phase 3c: Client Management API

- [ ] T038 [Analysis: Section.3.2] GraphQL schema: Client and Project queries/mutations
- [ ] T039 [Analysis: Section.3.2] [Logic: rolodex/views.py] REST endpoints for complex operations
- [ ] T040 [P] [Logic: rolodex/forms_client.py] Form validation logic
- [ ] T041 [P] [Logic: rolodex/forms_project.py] Project form validation
- [ ] T042 [Analysis: Section.3.3] Permission enforcement in GraphQL resolvers
- [ ] T043 [Ground Truth] API integration tests: Client/Project CRUD with permissions

### Phase 3d: Client Management Domain Services

- [ ] T044 [Analysis: Section.4.2] [Logic: rolodex/signals.py] Project lifecycle event handlers
- [ ] T045 [Logic: rolodex/tasks.py] Background tasks: project archival, notifications
- [ ] T046 [Analysis: Section.8.1] Performance optimization: Query prefetching, caching
- [ ] T047 [Ground Truth] Domain service tests: Event handling, background tasks

**Checkpoint**: Client management domain fully operational with GraphQL API

---

## Phase 4: Domain 2 - Infrastructure Management (Shepherd BC)

**Business Value**: Red team infrastructure tracking and health monitoring

**Analysis Reference**: Section.4.1 (Domain health monitoring), Section.5.1 (External APIs)

### Phase 4a: Domain Aggregate

- [ ] T048 [Analysis: Section.2.1] [Logic: shepherd/models.py::Domain] Port Domain entity
- [ ] T049 [P] [Logic: shepherd/models.py::HealthStatus] Port health status classification
- [ ] T050 [P] [Logic: shepherd/models.py::DomainStatus] Port domain status (Available, Checked Out, Burned)
- [ ] T051 [P] [Logic: shepherd/models.py::WhoisStatus] Port WHOIS privacy status
- [ ] T052 [Logic: shepherd/models.py::DomainCheckout] Port domain checkout/release workflow
- [ ] T053 [Analysis: Section.4.3] Domain checkout state machine: conflict detection
- [ ] T054 [Ground Truth] Domain CRUD tests: Checkout conflicts, release validation

### Phase 4b: Server Aggregate

- [ ] T055 [Analysis: Section.2.1] [Logic: shepherd/models.py::Server] Port Server entity
- [ ] T056 [P] [Logic: shepherd/models.py::ServerStatus] Port server status classification
- [ ] T057 [P] [Logic: shepherd/models.py::ServerRole] Port server role taxonomy
- [ ] T058 [Logic: shepherd/models.py::ServerCheckout] Port server checkout workflow
- [ ] T059 [Ground Truth] Server management tests: Checkout/release operations

### Phase 4c: Infrastructure Health Monitoring (CRITICAL ALGORITHM)

- [ ] T060 [Analysis: Section.4.1] [Logic: shepherd/tasks.py::domain_health_check] Port domain health monitoring algorithm
- [ ] T061 [Analysis: Section.5.1] [Logic: ghostwriter/modules/dns_toolkit.py] DNS resolution and analysis
- [ ] T062 [Analysis: Section.5.1] VirusTotal API integration for reputation checking
- [ ] T063 [Analysis: Section.4.1] Health scoring algorithm: Weighted reputation metrics
- [ ] T064 [Analysis: Section.5.3] Slack notification integration for burned infrastructure
- [ ] T065 [Ground Truth] Health monitoring tests: Reputation scoring, alert triggering
- [ ] T066 [Analysis: Section.8.1] Performance validation: 30min for 100 domains (baseline)

### Phase 4d: Cloud Provider Integrations

- [ ] T067 [Analysis: Section.5.1] [Logic: ghostwriter/modules/cloud_monitors.py::AWS] AWS infrastructure monitoring
- [ ] T068 [Analysis: Section.5.1] [Logic: ghostwriter/modules/cloud_monitors.py::DigitalOcean] DigitalOcean droplet monitoring
- [ ] T069 [Analysis: Section.5.1] [Logic: shepherd/tasks.py::namecheap_dns] Namecheap DNS automation
- [ ] T070 [Analysis: Section.5.1] Error handling: Retry logic, fallback mechanisms
- [ ] T071 [Ground Truth] External integration tests: API connectivity, error handling

### Phase 4e: Infrastructure API

- [ ] T072 [Analysis: Section.3.2] GraphQL schema: Domain, Server, health status queries
- [ ] T073 [Analysis: Section.3.2] [Logic: shepherd/views.py] Domain checkout/release endpoints
- [ ] T074 [P] [Logic: shepherd/forms.py] Infrastructure form validation
- [ ] T075 [Analysis: Section.3.3] Real-time updates for infrastructure status changes
- [ ] T076 [Ground Truth] Infrastructure API tests: Checkout workflows, health updates

**Checkpoint**: Infrastructure management operational with health monitoring

---

## Phase 5: Domain 3 - Reporting Engine (CRITICAL - Core Deliverable)

**Business Value**: Report generation - the primary deliverable for assessments

**Analysis Reference**: Section.4.1 (Report generation), Section.6 (Frontend architecture)

### Phase 5a: Finding Library Aggregate

- [ ] T077 [Analysis: Section.2.1] [Logic: reporting/models.py::Finding] Port Finding entity (master template library)
- [ ] T078 [P] [Logic: reporting/models.py::Severity] Port Severity classification with CVSS
- [ ] T079 [P] [Logic: reporting/models.py::FindingType] Port finding type taxonomy
- [ ] T080 [Analysis: Section.2.1] Finding validation: Required fields, CVSS scoring
- [ ] T081 [Analysis: Section.4.1] [Logic: reporting/models.py::Finding.cvss_score] CVSS calculation algorithm
- [ ] T082 [Ground Truth] Finding library tests: Template reusability, CVSS scoring

### Phase 5b: Report Aggregate

- [ ] T083 [Analysis: Section.2.1] [Logic: reporting/models.py::Report] Port Report entity
- [ ] T084 [P] [Logic: reporting/models.py::ReportTemplate] Port template management
- [ ] T085 [P] [Logic: reporting/models.py::ReportFindingLink] Port finding-to-report association
- [ ] T086 [Analysis: Section.2.2] Report validation: Template integrity, finding associations
- [ ] T087 [Ground Truth] Report CRUD tests: Template application, finding integration

### Phase 5c: Evidence Management

- [ ] T088 [Analysis: Section.2.1] [Logic: reporting/models.py::Evidence] Port Evidence entity with file storage
- [ ] T089 [Analysis: Section.4.2] [Logic: reporting/validators.py::validate_evidence_extension] File type validation
- [ ] T090 [Logic: reporting/views.py::upload_evidence] Evidence upload with thumbnail generation
- [ ] T091 [Analysis: Section.5.1] File storage: Local filesystem + cloud storage support
- [ ] T092 [Ground Truth] Evidence tests: Upload validation, thumbnail generation, storage

### Phase 5d: Report Generation Engine (MOST CRITICAL ALGORITHM)

- [ ] T093 [Analysis: Section.4.1] [Logic: ghostwriter/modules/reportwriter/report/base.py::ReportGenerator] Core generation engine
- [ ] T094 [Analysis: Section.4.1] [Logic: reporting/serializers.py::ReportDataSerializer] Report data serialization
- [ ] T095 [Analysis: Section.4.1] Jinja2 template processing with security context
- [ ] T096 [Analysis: Section.4.1] DOCX generation: python-docx integration, rich text formatting
- [ ] T097 [Analysis: Section.4.1] XLSX generation: Spreadsheet export for findings
- [ ] T098 [Analysis: Section.4.1] JSON generation: Structured data export
- [ ] T099 [Analysis: Section.4.1] PPTX generation: PowerPoint slide generation
- [ ] T100 [Analysis: Section.4.1] Evidence integration: File embedding, image insertion
- [ ] T101 [Analysis: Section.8.1] Performance optimization: Memory management for large reports
- [ ] T102 [Ground Truth] Report generation tests: All formats, evidence integration
- [ ] T103 [Analysis: Section.8.1] Performance validation: 15-45s for DOCX (baseline)

### Phase 5e: Collaborative Editing (Real-time Feature)

- [ ] T104 [Analysis: Section.6.3] [Logic: javascript/src/collab] TipTap collaborative editor setup
- [ ] T105 [Analysis: Section.6.3] Hocuspocus server integration (ProseMirror collaboration)
- [ ] T106 [Analysis: Section.3.3] [Logic: reporting/consumers.py] WebSocket handlers for real-time sync
- [ ] T107 [Analysis: Section.6.3] Conflict resolution for simultaneous edits
- [ ] T108 [Analysis: Section.6.3] User presence indicators
- [ ] T109 [Ground Truth] Collaborative editing tests: Multi-user scenarios, conflict resolution

### Phase 5f: Reporting API

- [ ] T110 [Analysis: Section.3.2] GraphQL schema: Report, Finding, Evidence queries
- [ ] T111 [Analysis: Section.3.2] [Logic: api/views.py::graphql_generate_report] Report generation REST action
- [ ] T112 [Analysis: Section.3.2] [Logic: api/views.py::graphql_upload_evidence] Evidence upload REST action
- [ ] T113 [P] [Logic: reporting/forms.py] Reporting form validation
- [ ] T114 [Analysis: Section.3.3] Real-time report updates via subscriptions
- [ ] T115 [Ground Truth] Reporting API tests: Generation, upload, collaboration

**Checkpoint**: Reporting engine operational with all formats and collaboration

---

## Phase 6: Domain 4 - Operations Logging (OpLog BC)

**Business Value**: Real-time activity tracking and audit trail for assessments

**Analysis Reference**: Section.3.3 (Real-time features), Section.11.1 (OpLog domain concept)

### Phase 6a: OpLog Aggregate

- [ ] T116 [Analysis: Section.2.1] [Logic: oplog/models.py::OplogEntry] Port OplogEntry entity
- [ ] T117 [P] [Logic: oplog/models.py::OplogCategory] Port activity categorization
- [ ] T118 [Analysis: Section.2.2] OplogEntry validation: Timestamp integrity, user attribution
- [ ] T119 [Ground Truth] OpLog CRUD tests: Entry creation, querying

### Phase 6b: Real-time Activity Streaming

- [ ] T120 [Analysis: Section.3.3] [Logic: oplog/consumers.py] WebSocket consumer for live activity
- [ ] T121 [Analysis: Section.3.3] [Logic: oplog/routing.py] WebSocket routing for OpLog channels
- [ ] T122 [Analysis: Section.3.3] Activity broadcasting: Redis-backed channel layer
- [ ] T123 [Analysis: Section.6.3] Frontend integration: Live activity feed component
- [ ] T124 [Ground Truth] Real-time tests: Activity broadcast, WebSocket connectivity

### Phase 6c: OpLog API

- [ ] T125 [Analysis: Section.3.2] GraphQL schema: OplogEntry queries and subscriptions
- [ ] T126 [P] [Logic: oplog/views.py] OpLog filtering and export endpoints
- [ ] T127 [Analysis: Section.3.3] Real-time subscriptions for activity updates
- [ ] T128 [Ground Truth] OpLog API tests: Querying, filtering, subscriptions

**Checkpoint**: Operations logging operational with real-time streaming

---

## Phase 7: Cross-Domain Integration & Workflows

**Purpose**: Wire domains together for complete assessment workflows

### Phase 7a: Project-to-Infrastructure Workflow

- [ ] T129 [Analysis: Section.4.3] [Logic: rolodex/signals.py::project_assignment] Project activation triggers infrastructure checkout
- [ ] T130 [Logic: shepherd/signals.py::project_complete] Project completion releases infrastructure
- [ ] T131 [Ground Truth] Integration tests: Full project lifecycle with infrastructure

### Phase 7b: Project-to-Reporting Workflow

- [ ] T132 [Analysis: Section.2.2] Report creation from project template
- [ ] T133 [Logic: reporting/signals.py::finding_added] Finding addition updates project status
- [ ] T134 [Ground Truth] Integration tests: Report generation within project context

### Phase 7c: Activity Logging Integration

- [ ] T135 [Logic: oplog/signals.py] OpLog entry creation for all domain events
- [ ] T136 [Analysis: Section.11.2] Audit trail: User attribution, timestamp integrity
- [ ] T137 [Ground Truth] Integration tests: Activity logging across all domains

**Checkpoint**: Cross-domain workflows operational

---

## Phase 8: Frontend Migration (Hybrid Approach)

**Purpose**: Migrate UI while preserving Django templates and adding React components

**Analysis Reference**: Section.6 (Frontend architecture)

### Phase 8a: Base Template System

- [ ] T138 [Analysis: Section.6.1] [Logic: ghostwriter/templates/base.html] Port base template structure
- [ ] T139 [P] [Logic: ghostwriter/static/css/styles.css] Port custom CSS and Bootstrap 5 theme
- [ ] T140 [P] [Logic: ghostwriter/static/js/] Port jQuery legacy interactions
- [ ] T141 [Analysis: Section.6.2] Component library: Font Awesome icons, custom widgets
- [ ] T142 [Ground Truth] UI rendering tests: Template inheritance, asset loading

### Phase 8b: Dashboard & Navigation

- [ ] T143 [Analysis: Section.6.3] [Logic: home/templates/home/dashboard.html] Port dashboard template
- [ ] T144 [Logic: home/views.py::dashboard] Dashboard data aggregation
- [ ] T145 [Analysis: Section.6.2] FullCalendar integration for project timeline
- [ ] T146 [P] Navigation component: Project/client switching
- [ ] T147 [Ground Truth] Dashboard tests: Data aggregation, calendar rendering

### Phase 8c: React Component Migration

- [ ] T148 [Analysis: Section.6.3] Vite build configuration for TypeScript/React
- [ ] T149 [Logic: javascript/src/components/] Port reusable React components
- [ ] T150 [Analysis: Section.6.1] Apollo Client setup for GraphQL state management
- [ ] T151 [P] Evidence upload component (drag-and-drop)
- [ ] T152 [P] Activity feed component (real-time)
- [ ] T153 [Ground Truth] Component tests: React component behavior

### Phase 8d: Forms & Validation

- [ ] T154 [Logic: rolodex/templates/] Client/Project form templates
- [ ] T155 [Logic: reporting/templates/] Report/Finding form templates
- [ ] T156 [Logic: shepherd/templates/] Infrastructure management forms
- [ ] T157 [Analysis: Section.6.2] Client-side validation matching backend rules
- [ ] T158 [Ground Truth] Form tests: Validation, submission, error handling

**Checkpoint**: Frontend fully migrated with hybrid Django + React architecture

---

## Phase 9: External Integrations & Background Tasks

**Purpose**: Implement all external service integrations

**Analysis Reference**: Section.5 (External integrations)

### Phase 9a: Cloud Provider Monitoring

- [ ] T159 [Analysis: Section.5.1] [Logic: ghostwriter/modules/cloud_monitors.py] AWS boto3 integration
- [ ] T160 [Analysis: Section.5.1] DigitalOcean API client
- [ ] T161 [Analysis: Section.5.1] Caching strategy: 1-hour TTL for instance data
- [ ] T162 [Analysis: Section.5.1] Error handling: Retry logic, credential validation
- [ ] T163 [Ground Truth] Cloud monitoring tests: API connectivity, data caching

### Phase 9b: DNS & Domain Management

- [ ] T164 [Analysis: Section.5.1] [Logic: ghostwriter/modules/dns_toolkit.py] DNS resolution toolkit
- [ ] T165 [Analysis: Section.5.1] Namecheap API integration: DNS record management
- [ ] T166 [Analysis: Section.5.1] WHOIS data collection
- [ ] T167 [Analysis: Section.5.1] Error handling: Timeout fallbacks, rate limiting
- [ ] T168 [Ground Truth] DNS tests: Resolution, WHOIS lookups, Namecheap API

### Phase 9c: Notification Services

- [ ] T169 [Analysis: Section.5.3] [Logic: ghostwriter/modules/notifications_slack.py] Slack webhook integration
- [ ] T170 [Logic: ghostwriter/modules/notifications_slack.py] Slack message formatting (blocks API)
- [ ] T171 [Analysis: Section.5.3] Event triggers: Project completion, burned infrastructure
- [ ] T172 [Ground Truth] Notification tests: Slack integration, message formatting

### Phase 9d: Background Task Infrastructure

- [ ] T173 [Analysis: Section.8.1] Celery setup for asynchronous processing
- [ ] T174 [Logic: shepherd/tasks.py::domain_health_monitoring] Scheduled health checks
- [ ] T175 [Logic: rolodex/tasks.py::project_archival] Automated archival (90-day trigger)
- [ ] T176 [Logic: reporting/tasks.py::report_cleanup] Report cleanup tasks
- [ ] T177 [Ground Truth] Background task tests: Scheduling, execution, error handling

**Checkpoint**: All external integrations operational

---

## Phase 10: Performance Optimization & Scaling

**Purpose**: Meet or exceed performance baselines

**Analysis Reference**: Section.8 (Performance characteristics)

### Phase 10a: Database Optimization

- [ ] T178 [Analysis: Section.8.1] Index optimization: Permission filtering queries
- [ ] T179 [Analysis: Section.2.3] Query optimization: select_related, prefetch_related
- [ ] T180 [Analysis: Section.8.2] Bottleneck analysis: N+1 query elimination
- [ ] T181 [Ground Truth] Performance tests: Query execution time baselines

### Phase 10b: API Performance

- [ ] T182 [Analysis: Section.8.1] GraphQL query optimization via Hasura
- [ ] T183 [Analysis: Section.8.1] Caching strategy: Apollo Client + Redis
- [ ] T184 [Analysis: Section.8.1] Response time validation: <100ms simple queries, <500ms complex
- [ ] T185 [Ground Truth] API performance tests: Response time benchmarks

### Phase 10c: Report Generation Optimization

- [ ] T186 [Analysis: Section.8.2] Memory management for large reports
- [ ] T187 [Analysis: Section.8.1] Chunked processing for 100+ finding reports
- [ ] T188 [Analysis: Section.8.1] Async task queue for report generation
- [ ] T189 [Ground Truth] Report performance tests: 15-45s DOCX baseline validation

**Checkpoint**: Performance meets or exceeds baselines

---

## Phase 11: Security Hardening & Compliance

**Purpose**: Ensure security best practices and compliance

**Analysis Reference**: Section.9 (Security measures)

### Phase 11a: Authentication Security

- [ ] T190 [Analysis: Section.9.1] 2FA enforcement configuration
- [ ] T191 [Analysis: Section.9.1] Session security: HTTPS-only, secure cookies
- [ ] T192 [Analysis: Section.9.1] JWT token security: Expiration, rotation
- [ ] T193 [Ground Truth] Security tests: Auth bypass attempts, token validation

### Phase 11b: Authorization Security

- [ ] T194 [Analysis: Section.9.1] Permission boundary enforcement
- [ ] T195 [Analysis: Section.9.1] Privilege escalation prevention
- [ ] T196 [Analysis: Section.9.1] Data isolation verification: User can only see assigned resources
- [ ] T197 [Ground Truth] Authorization tests: Access control boundary validation

### Phase 11c: Data Security

- [ ] T198 [Analysis: Section.9.1] Sensitive data encryption at rest
- [ ] T199 [Analysis: Section.9.1] Evidence file access control
- [ ] T200 [Analysis: Section.9.1] Audit logging for sensitive operations
- [ ] T201 [Ground Truth] Data security tests: Encryption, access control

### Phase 11d: API Security

- [ ] T202 [Analysis: Section.3.3] Rate limiting implementation
- [ ] T203 [Analysis: Section.9.1] GraphQL query depth limiting
- [ ] T204 [Analysis: Section.9.1] Input validation and sanitization
- [ ] T205 [Ground Truth] API security tests: Injection attempts, rate limiting

**Checkpoint**: Security hardened and validated

---

## Phase 12: Testing & Quality Assurance

**Purpose**: Comprehensive testing for production readiness

**Analysis Reference**: Section.7 (Testing & quality)

### Phase 12a: Test Coverage Parity

- [ ] T206 [Analysis: Section.7.1] Achieve 80%+ unit test coverage (baseline: 1043+ tests)
- [ ] T207 [Analysis: Section.7.2] Migrate critical test scenarios from legacy
- [ ] T208 [Analysis: Section.7.2] Edge case validation: All documented quirks tested
- [ ] T209 [Ground Truth] Coverage report: Verify parity with legacy coverage

### Phase 12b: Integration Testing

- [ ] T210 [Analysis: Section.7.2] Cross-domain integration tests: All 5 bounded contexts
- [ ] T211 [Analysis: Section.7.2] External integration tests: AWS, DigitalOcean, Namecheap
- [ ] T212 [Analysis: Section.7.2] Real-time feature tests: WebSocket connectivity, collaboration
- [ ] T213 [Ground Truth] Integration test suite execution and validation

### Phase 12c: End-to-End Testing

- [ ] T214 [Analysis: Section.11.3] User workflow tests: Complete assessment lifecycle
- [ ] T215 [Analysis: Section.11.3] Report generation workflow: Finding → Evidence → Report → Download
- [ ] T216 [Analysis: Section.11.3] Infrastructure workflow: Checkout → Monitor → Release
- [ ] T217 [Ground Truth] E2E test suite execution and validation

### Phase 12d: Performance Testing

- [ ] T218 [Analysis: Section.8.1] Load testing: 50-100 concurrent users
- [ ] T219 [Analysis: Section.8.1] Stress testing: Report generation under load
- [ ] T220 [Analysis: Section.8.3] Scalability testing: Database growth, file storage
- [ ] T221 [Ground Truth] Performance benchmark comparison with legacy

**Checkpoint**: Testing complete with validated parity

---

## Phase 13: Documentation & Knowledge Transfer

**Purpose**: Capture domain knowledge and tribal knowledge

**Analysis Reference**: Section.11 (Domain knowledge)

### Phase 13a: Domain Documentation

- [ ] T222 [Analysis: Section.11.1] Client Management domain: Business rules, workflows
- [ ] T223 [Analysis: Section.11.1] Reporting domain: Report generation, template system
- [ ] T224 [Analysis: Section.11.1] Infrastructure domain: Health monitoring, OPSEC concepts
- [ ] T225 [Analysis: Section.11.1] Operations domain: Activity logging, audit trail
- [ ] T226 [P] API documentation: GraphQL schema, REST endpoints

### Phase 13b: Operational Documentation

- [ ] T227 [Analysis: Section.11.2] Deployment guide: Docker, configuration, environment variables
- [ ] T228 [Analysis: Section.11.2] Admin guide: User management, system configuration
- [ ] T229 [Analysis: Section.11.2] Troubleshooting guide: Common issues, workarounds
- [ ] T230 [Analysis: Section.11.2] External integration setup: API keys, credentials

### Phase 13c: Developer Documentation

- [ ] T231 Architecture decision records: DDD boundaries, technology choices
- [ ] T232 Development setup guide: Local environment, testing
- [ ] T233 [Analysis: Section.11.2] Quirks and workarounds: Documented technical debt
- [ ] T234 Migration notes: Differences from legacy, upgrade path

**Checkpoint**: Documentation complete

---

## Phase 14: Migration Validation & Cutover

**Purpose**: Final validation before production cutover

**Analysis Reference**: Section.12 (Migration readiness)

### Phase 14a: Complete Functional Validation

- [ ] T235 [Analysis: Section.12.3] Full regression suite: All 1043+ tests passing
- [ ] T236 [Analysis: Section.4.1] Algorithm parity: Report generation identical to legacy
- [ ] T237 [Analysis: Section.4.1] Domain health monitoring: Identical reputation scoring
- [ ] T238 [Analysis: Section.11.3] User workflow parity: All assessment workflows function
- [ ] T239 [Ground Truth] Side-by-side comparison: Legacy vs new system

### Phase 14b: Performance Validation

- [ ] T240 [Analysis: Section.8.1] GraphQL API: <100ms simple, <500ms complex queries
- [ ] T241 [Analysis: Section.8.1] Report generation: 15-45s DOCX baseline met
- [ ] T242 [Analysis: Section.8.1] Domain health monitoring: 30min/100 domains baseline
- [ ] T243 [Analysis: Section.8.1] Dashboard load: <800ms FCP, <1200ms LCP

### Phase 14c: Security Validation

- [ ] T244 [Analysis: Section.9.1] Security audit: Penetration testing
- [ ] T245 [Analysis: Section.9.1] Authorization boundary testing: Data isolation verified
- [ ] T246 [Analysis: Section.9.1] Vulnerability scan: No critical or high severity issues
- [ ] T247 [Analysis: Section.9.1] Compliance check: WCAG 2.1 AA accessibility

### Phase 14d: Data Migration & Cutover

- [ ] T248 [Analysis: Section.12.2] Production data export: Full database backup
- [ ] T249 [Analysis: Section.12.2] Data migration execution: Client, projects, reports, findings
- [ ] T250 [Analysis: Section.12.2] Evidence file migration: Checksums, integrity verification
- [ ] T251 [Analysis: Section.12.2] Data validation: Row counts, relationship integrity
- [ ] T252 [Analysis: Section.12.2] Rollback plan: Tested and documented

### Phase 14e: Production Deployment

- [ ] T253 Production environment setup: Infrastructure, database, Redis, Hasura
- [ ] T254 Configuration validation: Environment variables, API keys, credentials
- [ ] T255 Smoke tests: Critical workflows in production environment
- [ ] T256 Monitoring setup: Application metrics, error tracking, alerts
- [ ] T257 Stakeholder sign-off: User acceptance testing passed

### Phase 14f: Legacy Asset Retirement

- [ ] T258 [Analysis: Section.12.2] Legacy asset archive: Full backup to secure storage
- [ ] T259 Post-migration monitoring: 30-day observation period
- [ ] T260 Performance monitoring: Validate sustained performance
- [ ] T261 User feedback collection: Address any migration issues
- [ ] T262 Delete legacy asset: Remove `features/Ghostwriter/` after validation complete

**Checkpoint**: Migration complete, production operational

---

## Dependencies & Execution Order

**Strict Sequential Dependencies**:

1. **Phase 1** (Foundation) → MUST complete first - validates analysis and sets up infrastructure
2. **Phase 2** (Shared Kernel) → MUST complete before domain migration - establishes cross-cutting concerns
3. **Phases 3-6** (Domain Migration) → CAN run in parallel after Phase 2:
   - Phase 3: Client Management (Rolodex) - **MVP CRITICAL**
   - Phase 4: Infrastructure (Shepherd) - Can start in parallel
   - Phase 5: Reporting - Depends on Phase 3 (needs Project context)
   - Phase 6: OpLog - Can start in parallel
4. **Phase 7** (Integration) → MUST complete after all domain phases
5. **Phases 8-14** (Frontend, Security, Testing, Deployment) → Sequential after Phase 7

**Parallel Execution Strategy**:

- **After Phase 2 Complete**:
  - Team A: Phase 3 (Client Management) - highest priority for MVP
  - Team B: Phase 4 (Infrastructure) - parallel track
  - Team C: Phase 6 (OpLog) - parallel track
- **After Phase 3 Complete**:
  - Phase 5 (Reporting) can begin - needs Client/Project context
- **After All Domains Complete**:
  - Phase 7 (Cross-domain integration) - wires everything together

**Critical Path for MVP**:

Phase 1 → Phase 2 → Phase 3 (Client Management) → Phase 5 (Reporting - core features) → Phase 7 → Phase 8 (Dashboard UI) → Deployment

---

## Implementation Strategy: DDD-Driven Migration

### Bounded Context Isolation

Each domain (Rolodex, Reporting, Shepherd, OpLog) migrates independently with:

- **Separate data models**: Domain-specific tables with clear boundaries
- **Domain services**: Business logic encapsulated within context
- **API boundaries**: GraphQL schema per domain
- **Test isolation**: Domain-specific test suites

### Shared Kernel Management

Cross-domain concerns handled through shared kernel:

- **User model**: Single source of truth for authentication
- **Permission system**: Centralized authorization
- **Tagging system**: Shared across all domains
- **Extra fields pattern**: Extensible JSON fields for all entities

### Anti-Corruption Layer

For external integrations:

- **Service adapters**: Wrap external APIs (AWS, DigitalOcean, Namecheap)
- **Error boundaries**: Graceful degradation when services fail
- **Caching layer**: Reduce external dependency impact

### Event-Driven Integration

Cross-domain workflows use events:

- **Django signals**: Domain event publication
- **Event handlers**: Cross-domain subscription
- **WebSocket broadcasts**: Real-time updates

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

- [ ] All tasks T001-T262 marked complete above (262 total tasks)
- [ ] Integration tests pass: `pytest tests/security/test_ghostwriter_integration.py`
- [ ] Performance baselines met (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm functional parity with legacy (1043+ test suite)
- [ ] All 5 bounded contexts operational: Rolodex, Reporting, Shepherd, OpLog, Users
- [ ] GraphQL API functional with Hasura integration
- [ ] Real-time collaboration working (WebSocket connectivity)
- [ ] All external integrations validated: AWS, DigitalOcean, Namecheap, Slack
- [ ] Report generation in all formats: DOCX, XLSX, JSON, PPTX
- [ ] Domain health monitoring operational
- [ ] Legacy `features/Ghostwriter/` backed up to `archive/`
- [ ] Migration completion documented in `migration-validation.md`
- [ ] All analysis findings from Ghostwriter-analysis.md addressed
- [ ] No regressions in existing functionality
- [ ] Security audit passed: 2FA, JWT auth, permission boundaries
- [ ] Accessibility compliance maintained (WCAG 2.1 AA)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:

1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/test_ghostwriter_integration.py -v`
3. Run performance benchmarks: `python tests/performance/ghostwriter_benchmarks.py`
4. Document completion in `migration-validation.md`
5. Mark parent task TXXX complete in `tasks.md`
6. Proceed to return task (next in sequence) in `tasks.md`

**Documentation Update Required**:

```markdown
# In migration-validation.md

### Ghostwriter Migration (TXXX)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: 320
- **Actual Hours**: [ACTUAL]
- **Tasks Completed**: 262/262
- **Tests**: 1043+ passed, 0 failed
- **Performance**: All baselines met/exceeded
  - GraphQL API: <100ms simple queries ✅
  - Report generation: 15-45s DOCX ✅
  - Domain health: 30min/100 domains ✅
- **Bounded Contexts Migrated**:
  - ✅ Client Management (Rolodex)
  - ✅ Reporting Engine
  - ✅ Infrastructure Management (Shepherd)
  - ✅ Operations Logging (OpLog)
  - ✅ User Management
- **External Integrations**:
  - ✅ AWS (EC2, S3 monitoring)
  - ✅ DigitalOcean (Droplet monitoring)
  - ✅ Namecheap (DNS automation)
  - ✅ Slack (Notifications)
  - ✅ VirusTotal (Domain reputation)
- **Critical Algorithms Preserved**:
  - ✅ Report generation engine (4 formats)
  - ✅ Domain health monitoring
  - ✅ Collaborative editing (TipTap + Hocuspocus)
  - ✅ CVSS scoring integration
- **Notes**: [Any notable achievements or challenges]
```

