# Tasks: Mental Prosthetic Platform (Refined)

**Input**: Design documents from `/specs/002-mental-prosthetic-refinement/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. Architecture implements a modular monolith codebase with layer-based service boundaries (UI, API, Data, AI) across 4 domains (Security, Productivity, MTG, Infrastructure), provisioned for flexible deployment including optional 3-device distribution (NUC frontend, dedicated AI server, security laptop) while maintaining comprehensive business logic preservation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions (Modular Monolith Architecture)

- **Backend**: `apps/jane-orchestrator/src/`
- **Frontend**: `apps/jane-ui/src/`
- **Shared Libraries**: `libs/`
- **Service Adapters**: `libs/service-adapters/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and modular monolith structure for 37-tool consolidation

- [ ] T001 Create modular monolith project structure per implementation plan with apps/jane-orchestrator/ and apps/jane-ui/
- [ ] T002 Initialize FastAPI project with Python dependencies in apps/jane-orchestrator/pyproject.toml
- [ ] T003 [P] Initialize React/Next.js project with TypeScript in apps/jane-ui/package.json
- [ ] T004 [P] Configure ESLint, Prettier, and TypeScript strict mode in apps/jane-ui/
- [ ] T005 [P] Configure Python linting (black, mypy, ruff) in apps/jane-orchestrator/
- [ ] T006 Setup NX monorepo configuration for cross-app dependencies in nx.json
- [ ] T007 [P] Create shared library structure in libs/shared/ for cross-domain utilities
- [ ] T008 [P] Create UI design system structure in libs/ui/ for executive function accommodations

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T009 Setup PostgreSQL database schema and migrations framework in apps/jane-orchestrator/src/data/migrations/
- [ ] T010 [P] Configure Redis for caching and session management in apps/jane-orchestrator/src/data/redis/
- [ ] T011 [P] Implement JWT-based authentication framework in apps/jane-orchestrator/src/api/auth/
- [ ] T012 [P] Setup FastAPI routing structure with domain organization in apps/jane-orchestrator/src/api/
- [ ] T013 Create base entity models for 4 domains in apps/jane-orchestrator/src/data/models/
- [ ] T014 [P] Configure error handling and logging infrastructure in apps/jane-orchestrator/src/utils/
- [ ] T015 [P] Setup environment configuration management in apps/jane-orchestrator/src/config/
- [ ] T016 Create React component library with ADHD/autism accommodations in libs/ui/components/
- [ ] T017 [P] Setup API client and state management (React Context + Zustand) in apps/jane-ui/src/services/
- [ ] T018 [P] Configure WebSocket infrastructure for real-time sync in apps/jane-orchestrator/src/api/websocket/
- [ ] T019 Create service adapter framework for 37-tool integration in libs/service-adapters/base/
- [ ] T020 Setup domain-specific performance monitoring (<200ms UI, domain tiers) in apps/jane-orchestrator/src/monitoring/
- [ ] T020a [P] Implement tool-specific rollback infrastructure in apps/jane-orchestrator/src/services/rollback/tool_rollback_service.py
- [ ] T020b [P] Create database transaction rollback per tool domain in apps/jane-orchestrator/src/data/transaction_manager.py
- [ ] T020c [P] Implement service restart capabilities for individual tools in apps/jane-orchestrator/src/services/rollback/service_restart_manager.py
- [ ] T020d [P] Create configuration state restoration from last known good state in apps/jane-orchestrator/src/config/state_backup_service.py
- [ ] T020e [P] Implement data consistency validation after rollback in apps/jane-orchestrator/src/services/rollback/consistency_validator.py
- [ ] T020f [P] Create system-wide fallback rollback capabilities in apps/jane-orchestrator/src/services/rollback/system_rollback_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Unified Executive Function Dashboard (Priority: P1) 🎯 MVP

**Goal**: Single unified interface accessing all 37 executive function tools across 4 domains

**Independent Test**: User can access dashboard and navigate between all 4 domains (Security: 13, Productivity: 8, MTG: 4, Infrastructure: 12 tools) within 200ms response time

### Implementation for User Story 1

- [ ] T021 [P] [US1] Create User Profile model with ADHD/autism settings in apps/jane-orchestrator/src/data/models/user_profile.py
- [ ] T022 [P] [US1] Create Platform Session model for unified authentication in apps/jane-orchestrator/src/data/models/platform_session.py
- [ ] T023 [P] [US1] Create Domain Classification model for 4 domains in apps/jane-orchestrator/src/data/models/domain.py
- [ ] T024 [P] [US1] Create Integrated Tool model for 37 tools inventory in apps/jane-orchestrator/src/data/models/integrated_tool.py
- [ ] T025 [US1] Implement UserProfileService with executive function patterns in apps/jane-orchestrator/src/services/user_service.py
- [ ] T026 [US1] Implement DomainService for 4-domain organization in apps/jane-orchestrator/src/services/domain_service.py
- [ ] T027 [US1] Implement ToolRegistryService for 37-tool management in apps/jane-orchestrator/src/services/tool_registry_service.py
- [ ] T028 [US1] Create dashboard API endpoints in apps/jane-orchestrator/src/api/dashboard/
- [ ] T029 [US1] Create authentication API endpoints with JWT in apps/jane-orchestrator/src/api/auth/endpoints.py
- [ ] T030 [P] [US1] Create executive function dashboard UI components in apps/jane-ui/src/components/Dashboard/
- [ ] T031 [P] [US1] Create domain navigation component with consistent patterns in apps/jane-ui/src/components/Navigation/DomainNav.tsx
- [ ] T032 [P] [US1] Create tool grid component for 37-tool display in apps/jane-ui/src/components/Tools/ToolGrid.tsx
- [ ] T033 [US1] Implement dashboard page with state management in apps/jane-ui/src/pages/dashboard.tsx
- [ ] T034 [US1] Add session persistence and state management in apps/jane-ui/src/services/session.ts
- [ ] T035 [US1] Integrate WebSocket for real-time updates in apps/jane-ui/src/services/websocket.ts
- [ ] T036 [US1] Add accessibility compliance (WCAG 2.1 AA) to all dashboard components
- [ ] T037 [US1] Add performance monitoring for <200ms response time validation
- [ ] T037a [P] [US1] Implement unified user preferences system across all 37 tools in apps/jane-orchestrator/src/services/user_preferences_service.py
- [ ] T037b [P] [US1] Create user preferences API endpoints for ADHD/autism customizations in apps/jane-orchestrator/src/api/preferences/
- [ ] T037c [P] [US1] Create user preferences UI components for executive function settings in apps/jane-ui/src/components/UserProfile/PreferencesPanel.tsx
- [ ] T037d [P] [US1] Implement cross-tool preference synchronization in apps/jane-orchestrator/src/services/preference_sync_service.py

**Checkpoint**: At this point, User Story 1 should provide access to all 37 tools through unified interface

---

## Phase 4: User Story 2 - AI-Enhanced Security Operations (Priority: P1)

**Goal**: AI-assisted threat hunting across 13 security tools with <1s response time

**Independent Test**: Security analyst can launch MISP, receive AI correlation, and perform threat hunting workflow within domain performance requirements

### Implementation for User Story 2

- [ ] T038 [P] [US2] Create AI Enhancement Context model for LLM interactions in apps/jane-orchestrator/src/data/models/ai_context.py
- [ ] T039 [P] [US2] Create Security Profile model for airgapped operations in apps/jane-orchestrator/src/data/models/security_profile.py
- [ ] T040 [P] [US2] Create service adapters for MISP integration in libs/service-adapters/security/misp_adapter.py
- [ ] T041 [P] [US2] Create service adapters for HELK integration in libs/service-adapters/security/helk_adapter.py
- [ ] T042 [P] [US2] Create service adapters for SecurityOnion integration in libs/service-adapters/security/securityonion_adapter.py
- [ ] T043 [P] [US2] Create service adapters for YARA-X integration in libs/service-adapters/security/yarax_adapter.py
- [ ] T044 [US2] Implement AIEnhancementService for security domain in apps/jane-orchestrator/src/services/ai/security_ai_service.py
- [ ] T045 [US2] Implement SecurityToolsService with 13-tool orchestration in apps/jane-orchestrator/src/services/security_service.py
- [ ] T046 [US2] Create security domain API endpoints with <1s performance in apps/jane-orchestrator/src/api/security/
- [ ] T047 [US2] Setup MCP server infrastructure for security enhancement in apps/jane-orchestrator/src/ai/mcp/
- [ ] T048 [P] [US2] Create security dashboard UI components in apps/jane-ui/src/components/Security/
- [ ] T049 [P] [US2] Create threat correlation interface in apps/jane-ui/src/components/Security/ThreatCorrelation.tsx
- [ ] T050 [P] [US2] Create security tool launcher components in apps/jane-ui/src/components/Security/ToolLauncher.tsx
- [ ] T051 [US2] Implement security workflow pages in apps/jane-ui/src/pages/security/
- [ ] T052 [US2] Add AI assistance integration to security components
- [ ] T053 [US2] Add security-specific performance monitoring for <1s requirement

**Checkpoint**: Security operations with AI enhancement functional across 13 tools

---

## Phase 5: User Story 6 - AI-Assisted Task Management (Priority: P2)

**Goal**: AI assistant for task breakdown and executive function support across all 37 tools

**Independent Test**: User can request AI task breakdown across multiple tool contexts and receive proactive reminders

### Implementation for User Story 6

- [ ] T054 [P] [US6] Create Task & Workflow model for cross-domain activities in apps/jane-orchestrator/src/data/models/task.py
- [ ] T055 [P] [US6] Extend AI Enhancement Context for task management in apps/jane-orchestrator/src/data/models/ai_context.py
- [ ] T056 [US6] Implement TaskManagementService with AI integration in apps/jane-orchestrator/src/services/task_service.py
- [ ] T057 [US6] Implement AI Assistant Service for executive function support in apps/jane-orchestrator/src/services/ai/assistant_service.py
- [ ] T058 [US6] Create task management API endpoints in apps/jane-orchestrator/src/api/tasks/
- [ ] T059 [US6] Setup LLM integration with vLLM server in apps/jane-orchestrator/src/ai/llm/
- [ ] T060 [P] [US6] Create AI assistant UI components in apps/jane-ui/src/components/AI/
- [ ] T061 [P] [US6] Create task breakdown interface in apps/jane-ui/src/components/Tasks/TaskBreakdown.tsx
- [ ] T062 [P] [US6] Create reminder system components in apps/jane-ui/src/components/Tasks/Reminders.tsx
- [ ] T063 [US6] Implement AI chat interface with context awareness in apps/jane-ui/src/pages/ai-assistant.tsx
- [ ] T064 [US6] Add cross-tool context integration for AI suggestions
- [ ] T065 [US6] Add proactive reminder system with pattern recognition

**Checkpoint**: AI-assisted task management functional across all integrated tools

---

## Phase 6: User Story 7 - Cross-Tool Data Integration (Priority: P3)

**Goal**: Seamless data flow between all 37 integrated applications across 4 domains

**Independent Test**: User can create data in one tool and verify it's accessible in related tools across domains without manual entry

### Implementation for User Story 7

- [ ] T066 [P] [US7] Create Sync State model for cross-tool synchronization in apps/jane-orchestrator/src/data/models/sync_state.py
- [ ] T067 [P] [US7] Create data mapping schemas for 37-tool integration in apps/jane-orchestrator/src/data/schemas/
- [ ] T068 [US7] Implement DataIntegrationService for cross-domain workflows in apps/jane-orchestrator/src/services/data_integration_service.py
- [ ] T069 [US7] Implement EventBusService for real-time data propagation in apps/jane-orchestrator/src/services/event_bus_service.py
- [ ] T070 [US7] Create data synchronization API endpoints in apps/jane-orchestrator/src/api/sync/
- [ ] T071 [US7] Setup conflict resolution for concurrent data modifications in apps/jane-orchestrator/src/services/conflict_resolution.py
- [ ] T072 [P] [US7] Create unified insights dashboard components in apps/jane-ui/src/components/Insights/
- [ ] T073 [P] [US7] Create cross-domain data visualization in apps/jane-ui/src/components/Data/CrossDomainView.tsx
- [ ] T074 [P] [US7] Create data flow monitoring interface in apps/jane-ui/src/components/Sync/DataFlow.tsx
- [ ] T075 [US7] Implement unified insights page in apps/jane-ui/src/pages/insights.tsx
- [ ] T076 [US7] Add real-time data synchronization indicators
- [ ] T077 [US7] Add data consistency validation across all 37 tools

**Checkpoint**: Data flows seamlessly between all integrated applications

---

## Phase 7: User Story 8 - Secure Remote Access (Priority: P4)

**Goal**: Secure mobile/remote access to all 37 executive function tools with PWA functionality

**Independent Test**: User can securely access platform from mobile device and perform key tasks across multiple tool domains

### Implementation for User Story 8

- [ ] T078 [P] [US8] Configure HTTPS and TLS certificates in apps/jane-orchestrator/src/config/security.py
- [ ] T079 [P] [US8] Implement OAuth2 authentication for external access in apps/jane-orchestrator/src/api/oauth/
- [ ] T080 [US8] Create RemoteAccessService for secure connectivity in apps/jane-orchestrator/src/services/remote_access_service.py
- [ ] T081 [US8] Setup VPN/tunnel management for secure connections in apps/jane-orchestrator/src/services/vpn_service.py
- [ ] T082 [US8] Create secure remote API endpoints in apps/jane-orchestrator/src/api/remote/
- [ ] T083 [P] [US8] Configure PWA manifest and service worker in apps/jane-ui/public/
- [ ] T084 [P] [US8] Create mobile-responsive components in apps/jane-ui/src/components/Mobile/
- [ ] T085 [P] [US8] Optimize UI components for mobile viewports in libs/ui/components/
- [ ] T086 [US8] Implement offline data caching for 24-hour capability in apps/jane-ui/src/services/cache.ts
- [ ] T087 [US8] Add mobile navigation and touch-friendly interactions
- [ ] T088 [US8] Add secure session management for remote connections
- [ ] T089 [US8] Add data synchronization for offline/online transitions

**Checkpoint**: Secure remote access functional with PWA capability

---

## Phase 8: Security Domain Migration (Complex Business Logic)

**Goal**: Migrate 13 security tools preserving complex algorithms and data schemas per business logic analysis with layer-based service boundaries

### Category A: Complex Algorithms (Preserve as Microservices)

- [ ] T090 Analyze MISP threat intelligence correlation algorithms (8,733 lines in Event.php) and create microservice preservation plan
- [ ] T091 Extract Nemesis file analysis pipeline from features/Nemesis/ maintaining multi-stage processing workflow  
- [ ] T092 Preserve CyberChef operations engine (300+ operations) as embedded library with REST API wrapper
- [ ] T093 [P] Create MISP database migration from CakePHP/MySQL to unified PostgreSQL schema preserving threat intelligence data
- [ ] T094 [P] Migrate MISP REST API endpoints from CakePHP to FastAPI maintaining backward compatibility

### Category B: Domain Logic (Modularize within Monolith)

- [ ] T095 [P] Migrate HELK threat hunting logic from features/HELK/ to apps/jane-orchestrator/src/domains/security/helk/
- [ ] T096 [P] Migrate SecurityOnion configuration management from features/securityonion/ preserving Salt states and pillars
- [ ] T097 [P] Migrate Maltrail detection rules from features/maltrail/ to unified security domain with rule engine
- [ ] T098 [P] Migrate YARA-X pattern matching from features/yara-x/ to FastAPI endpoint preserving Rust core
- [ ] T099 [P] Convert APIScout, Hexstrike-AI, Rita, OneX utilities to FastAPI modules in security domain

### Category C: Utility Functions (Shared Libraries)

- [ ] T100 [P] Extract Meterpreter payloads to shared security utilities library  
- [ ] T101 [P] Migrate Software Forensic Kit tools to shared analysis library in libs/shared/security/
- [ ] T102 [P] Convert BlackArch script collection to callable Python modules
- [ ] T103 Convert legacy security tool UIs to React components preserving functionality
- [ ] T104 Create unified security dashboard integrating all migrated tools with FastAPI backend

---

## Phase 9: Productivity Domain Migration (FastAPI-Ready Projects)

**Goal**: Migrate 8 productivity tools leveraging existing FastAPI/TypeScript patterns from analysis with comprehensive framework preservation

### Category A: Complex Workflow Engines (Microservice Preservation)

- [ ] T105 Analyze n8n workflow engine (packages/core/src/WorkflowExecute.ts - 10,000+ lines) for microservice extraction
- [ ] T106 Preserve n8n 400+ integrations (packages/nodes-base/) as separate service maintaining TypeScript execution engine
- [ ] T107 Create database migration strategy for n8n TypeORM to unified PostgreSQL schema preserving workflow definitions

### Category B: FastAPI-Ready Applications (Direct Migration)

- [ ] T108 [P] Migrate Mealie FastAPI backend from features/mealie/ maintaining recipe parsing and meal planning algorithms
- [ ] T109 [P] Migrate Dispatch FastAPI incident management from features/dispatch/ preserving workflow orchestration
- [ ] T110 [P] Convert Mealie Nuxt.js frontend to React/Next.js components compatible with unified dashboard
- [ ] T111 [P] Integrate Dispatch PostgreSQL schema with unified database maintaining incident data integrity

### Category C: TypeScript Applications (Framework Migration)

- [ ] T112 [P] Migrate Actual Budget CRDT synchronization engine from features/actual/packages/crdt/ preserving conflict resolution
- [ ] T113 [P] Convert Actual Budget SQLite schema to PostgreSQL while maintaining sync capabilities  
- [ ] T114 [P] Migrate Firecrawl Express.js backend to FastAPI preserving web scraping and BullMQ integration
- [ ] T115 [P] Migrate Goose AI agent system preserving Rust core with Python wrapper integration

### Category D: Utility Collections (Library Integration)

- [ ] T116 [P] Convert IT-Tools 80+ developer utilities from Vue.js SPA to integrated React library modules
- [ ] T117 [P] Migrate Inspector MCP protocol debugging to unified development tools section
- [ ] T118 Create unified productivity dashboard with FastAPI backend and React/Next.js frontend
- [ ] T119 Integrate all productivity tools with shared authentication and session management

---

## Phase 10: MTG Domain Migration (Gaming/Algorithm-Heavy Projects)

**Goal**: Migrate 4 MTG tools preserving complex combo algorithms and card databases with framework-specific preservation

### Category A: Complex Algorithms (Critical Business Logic)

- [ ] T120 Analyze Commander Spellbook variant generation algorithm (1400+ lines) for combo-to-variant generation preservation
- [ ] T121 Migrate Commander Spellbook Django backend preserving combo graph algorithms and variant computation
- [ ] T122 Create database migration from Commander Spellbook PostgreSQL to unified schema preserving card relationships
- [ ] T123 [P] Preserve MTG Commander Map visualization algorithms maintaining card interaction network analysis

### Category B: Domain Logic (Modular Integration)

- [ ] T124 [P] Migrate MTG Scripting Toolkit card analysis from features/mtg-scripting-toolkit/ to unified MTG domain
- [ ] T125 [P] Convert Commander Spellbook React frontend to unified React/Next.js components for dashboard integration
- [ ] T126 [P] Integrate MTG Commander Map visualization with unified UI component library
- [ ] T127 [P] Create unified MTG API endpoints in FastAPI preserving all card search and combo functionality

### Category C: Utility Integration  

- [ ] T128 [P] Consolidate MTG card databases (Scryfall integration) into shared card data service
- [ ] T129 [P] Create unified MTG dashboard with combo search, deck building, and card analysis tools
- [ ] T130 Integrate MTG tools with AI assistant for deck building and combo suggestions

---

## Phase 11: Infrastructure Domain Migration

**Goal**: Migrate all 12 infrastructure/integration tools from features/ directory preserving business logic with layer-based service boundaries

### Infrastructure Tools Business Logic Migration

- [ ] T131 [P] Migrate Kong business logic from features/kong/ to apps/jane-orchestrator/src/domains/infrastructure/kong/
- [ ] T132 [P] Migrate KasmVNC business logic from features/KasmVNC/ to apps/jane-orchestrator/src/domains/infrastructure/kasmvnc/
- [ ] T133 [P] Migrate Ghostwriter business logic from features/Ghostwriter/ to apps/jane-orchestrator/src/domains/infrastructure/ghostwriter/
- [ ] T134 [P] Migrate FileScopeMCP business logic from features/FileScopeMCP/ to apps/jane-orchestrator/src/domains/infrastructure/filescope/
- [ ] T135 [P] Migrate Chroma MCP business logic from features/chroma-mcp/ to apps/jane-orchestrator/src/domains/infrastructure/chroma-mcp/
- [ ] T136 [P] Migrate Firecrawl MCP business logic from features/firecrawl-mcp-server/ to apps/jane-orchestrator/src/domains/infrastructure/firecrawl-mcp/
- [ ] T137 [P] Migrate MalwareBazaar MCP business logic from features/MalwareBazaar_MCP/ to apps/jane-orchestrator/src/domains/infrastructure/malwarebazaar-mcp/
- [ ] T138 [P] Migrate VirusTotal MCP business logic from features/mcp-virustotal/ to apps/jane-orchestrator/src/domains/infrastructure/virustotal-mcp/
- [ ] T139 [P] Migrate n8n MCP business logic from features/n8n-mcp-server/ to apps/jane-orchestrator/src/domains/infrastructure/n8n-mcp/
- [ ] T140 [P] Migrate SecurityOnion n8n workflows from features/securityonion-n8n-workflows/ to apps/jane-orchestrator/src/domains/infrastructure/securityonion-workflows/
- [ ] T141 [P] Migrate Brute-Ratel-C4 business logic from features/Brute-Ratel-C4-Community-Kit/ to apps/jane-orchestrator/src/domains/infrastructure/brute-ratel/
- [ ] T142 [P] Migrate LScript business logic from features/lscript/ to apps/jane-orchestrator/src/domains/infrastructure/lscript/

---

## Phase 12: LLM Server Enhancement

**Goal**: Enhance existing LLM servers for integrated tool support with layer-based AI service boundaries

### LLM Integration Enhancement

- [ ] T143 [P] Enhance cyber-llm-server with security tool integration in apps/cyber-llm-server/src/integrations/
- [ ] T144 [P] Enhance mtg-llm-server with MTG tool integration in apps/mtg-llm-server/src/integrations/
- [ ] T145 [P] Enhance code-llm-server with development tool integration in apps/code-llm-server/src/integrations/
- [ ] T146 Create unified LLM router in apps/jane-orchestrator/src/services/llm_router.py
- [ ] T147 Implement AI context sharing across all tools in apps/jane-orchestrator/src/services/ai_context_sharing.py

---

## Phase 13: Features Directory Migration Completion

**Goal**: Complete migration of all business logic from features/ directory, ensuring empty directory per spec requirements with comprehensive validation

### Migration Validation and Cleanup

- [ ] T148 Validate all business logic preservation with measurable criteria:
  - [ ] T148a Create automated functionality comparison tests for all 37 tools in apps/jane-orchestrator/tests/preservation/
  - [ ] T148b Implement API endpoint parity validation (input/output schema matching) in apps/jane-orchestrator/tests/preservation/api-parity.py
  - [ ] T148c Create UI workflow automation tests comparing original vs integrated tools in apps/jane-ui/tests/preservation/
  - [ ] T148d Validate algorithm preservation through identical test suite execution in apps/jane-orchestrator/tests/preservation/algorithm-validation.py
  - [ ] T148e Measure performance benchmarks (original vs integrated) for all tools in tests/performance/preservation-benchmarks.py
  - [ ] T148f Create preservation compliance report generator in apps/jane-orchestrator/src/services/preservation_validator.py
- [ ] T149 Create migration status tracking in apps/jane-orchestrator/src/services/migration_tracker.py
- [ ] T150 Implement automated validation that features/ directory is completely empty
- [ ] T151 [P] Create integration status dashboard in apps/jane-ui/src/components/Migration/IntegrationStatus.tsx
- [ ] T152 [P] Document all migrated tools and their new locations in docs/migration-log.md
- [ ] T153 Remove all remaining code from features/ directory after successful migration validation
- [ ] T154 Update project documentation to reflect completed integration with features/ directory empty

**Checkpoint**: All 37 tools fully migrated with 100% business logic preservation validated

---

## Phase 14: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements affecting multiple user stories and production readiness with comprehensive system optimization

- [ ] T155 [P] Performance optimization across all service adapters and domain boundaries in libs/service-adapters/
- [ ] T156 [P] Security hardening for all API endpoints and WebSocket connections in apps/jane-orchestrator/src/security/
- [ ] T157 [P] Accessibility improvements (WCAG 2.1 AA compliance) across UI components in libs/ui/
- [ ] T158 [P] Error handling enhancement across all domains in apps/jane-orchestrator/src/utils/error_handling.py
- [ ] T159 [P] Logging and monitoring setup for production deployment in apps/jane-orchestrator/src/monitoring/
- [ ] T160 [P] Documentation updates and API documentation for all 37 integrated tools in docs/
- [ ] T161 [P] Docker composition optimization with layer-based service boundaries in infrastructure/docker/
- [ ] T162 [P] Database performance tuning and index optimization in apps/jane-orchestrator/src/database/
- [ ] T163 [P] WebSocket connection scaling and load balancing in apps/jane-orchestrator/src/websocket/
- [ ] T164 [P] Implement automated backup to Synology NAS in apps/jane-orchestrator/src/backup/
  - [ ] T164a Create PostgreSQL backup automation with daily schedule in apps/jane-orchestrator/src/backup/postgres_backup.py
  - [ ] T164b Implement SQLite database backup for local-first tools in apps/jane-orchestrator/src/backup/sqlite_backup.py
  - [ ] T164c Create Synology NAS integration with secure file transfer in apps/jane-orchestrator/src/backup/synology_integration.py
  - [ ] T164d Implement backup verification and restoration testing in apps/jane-orchestrator/src/backup/backup_validator.py
  - [ ] T164e Add backup monitoring and failure alerting in apps/jane-orchestrator/src/backup/backup_monitor.py
- [ ] T165 [P] Add vulnerability scanning and security monitoring in apps/jane-orchestrator/src/security/
- [ ] T166 [P] Create user documentation for all 37 integrated tools in docs/user-guide/
- [ ] T167 [P] Implement load testing with Artillery.js for domain-specific performance tiers in tests/performance/
- [ ] T168 [P] Setup CI/CD pipeline with constitution compliance checks in .github/workflows/
- [ ] T169a [P] Implement Security Domain performance validation (<1s response time) across all 13 security tools in tests/performance/security-domain-validation.py
- [ ] T169b [P] Implement Productivity Domain performance validation (<2s response time) across all 8 productivity tools in tests/performance/productivity-domain-validation.py
- [ ] T169c [P] Implement MTG Domain performance validation (<3s response time) across all 4 MTG tools in tests/performance/mtg-domain-validation.py
- [ ] T169d [P] Implement Infrastructure Domain performance validation (<5s response time) across all 12 infrastructure tools in tests/performance/infrastructure-domain-validation.py
- [ ] T169e [P] Create automated domain performance monitoring dashboard in apps/jane-ui/src/components/Performance/DomainMetrics.tsx
- [ ] T169 Final validation of constitutional requirements (<200ms UI, 95% context reduction, 100% functionality preservation)
- [ ] T170 Run complete quickstart.md validation and deployment verification

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) after foundational phase
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Security Domain Migration (Phase 8)**: Depends on User Stories 1-3 completion (core platform stability)
- **Productivity Domain Migration (Phase 9)**: Depends on User Story 3 (Cross-Tool Data Integration) completion
- **MTG Domain Migration (Phase 10)**: Depends on User Stories 1-3 completion (core platform stability)  
- **Infrastructure Domain Migration (Phase 11)**: Depends on User Story 3 (Cross-Tool Data Integration) completion
- **LLM Enhancement (Phase 12)**: Depends on User Story 2 (AI-Assisted Task Management) completion
- **Migration Completion (Phase 13)**: Depends on all domain migrations (Phases 8-11) completion
- **Polish (Phase 14)**: Depends on all core functionality and migration being complete

### User Story Dependencies

- **User Story 1 (P1)**: Independent after Foundational - Core dashboard functionality
- **User Story 2 (P1)**: Independent after Foundational - Security operations with AI
- **User Story 6 (P2)**: Depends on US1 completion - AI task management builds on unified interface
- **User Story 7 (P3)**: Depends on US1, US2, US6 - Cross-tool integration needs multiple tools active
- **User Story 8 (P4)**: Independent after Foundational - Remote access can be developed separately

### Within Each User Story

- Models before services (data layer foundation)
- Services before API endpoints (business logic before interfaces)  
- API endpoints before UI components (backend before frontend)
- Core components before integration features
- Performance monitoring throughout development

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel within Phase 2
- Once Foundational completes, User Stories 1, 2, and 8 can start in parallel
- All service adapter tasks marked [P] can run in parallel (different tools/files)
- Models within each user story marked [P] can run in parallel
- UI components within each story marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: T021 "Create User Profile model"  
Task: T022 "Create Platform Session model"
Task: T023 "Create Domain Classification model"
Task: T024 "Create Integrated Tool model"

# Launch all UI components for User Story 1 together:
Task: T030 "Create dashboard UI components"
Task: T031 "Create domain navigation component" 
Task: T032 "Create tool grid component"
```

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only - Both P1)

1. Complete Phase 1: Setup (T001-T008) - 8 tasks
2. Complete Phase 2: Foundational (T009-T020) - **CRITICAL BLOCKING PHASE** - 12 tasks
3. Complete Phase 3: User Story 1 (T021-T037) - 17 tasks
4. Complete Phase 4: User Story 2 (T038-T053) - 16 tasks
5. **STOP and VALIDATE**: Test both P1 stories independently
6. Deploy/demo core executive function platform with AI security

### Comprehensive Delivery (Full Business Logic Migration)

1. **Foundation**: Setup + Foundational (T001-T020) → Core platform ready
2. **MVP**: Add User Stories 1 & 2 (T021-T053) → Test independently → Deploy unified dashboard with AI
3. **Core Platform**: Add User Stories 6 & 7 (T054-T077) → Test AI assistance and data integration → Deploy enhanced version
4. **Remote Access**: Add User Story 8 (T078-T089) → Test secure remote capabilities → Deploy mobile-ready platform
5. **Security Migration**: Phase 8 (T090-T104) → Comprehensive security tool preservation → Validate business logic
6. **Productivity Migration**: Phase 9 (T105-T119) → FastAPI-ready applications with framework preservation → Validate workflows
7. **MTG Migration**: Phase 10 (T120-T130) → Complex algorithms and Django preservation → Validate combo generation
8. **Infrastructure Migration**: Phase 11 (T131-T142) → MCP servers and utility integration → Validate tool ecosystem
9. **AI Enhancement**: Phase 12 (T143-T147) → LLM server integration → Validate cross-domain AI support
10. **Migration Completion**: Phase 13 (T148-T154) → Validate 100% business logic preservation → Empty features/ directory
11. **Production Polish**: Phase 14 (T155-T170) → Production readiness and optimization → Full deployment

### Parallel Team Strategy

With multiple developers after Foundational completion:

#### Phase 3-7: User Story Development (Parallel)

- **Developer A**: User Story 1 (Unified Dashboard) - Foundation for others
- **Developer B**: User Story 2 (AI Security) - Independent P1 priority  
- **Developer C**: User Story 6 (AI Task Management) - After US1 integration points
- **Developer D**: User Story 8 (Remote Access) - Independent infrastructure work

#### Phase 8-11: Domain Migration (Parallel by Domain)

- **Security Team**: Phase 8 (Security Domain) - Complex algorithms and microservice preservation
- **Productivity Team**: Phase 9 (Productivity Domain) - FastAPI-ready applications and framework migration
- **MTG Team**: Phase 10 (MTG Domain) - Django backend and React frontend preservation  
- **Infrastructure Team**: Phase 11 (Infrastructure Domain) - MCP servers and utility integration

#### Phase 12-14: Integration and Polish (Sequential)

- **AI Team**: Phase 12 (LLM Enhancement) - Requires all domains for context
- **QA Team**: Phase 13 (Migration Validation) - Comprehensive business logic verification
- **DevOps Team**: Phase 14 (Production Polish) - System optimization and deployment readiness

---

## Notes

- [P] tasks = different files, no dependencies within the same phase
- [Story] label maps task to specific user story for traceability  
- Each user story should be independently completable and testable
- Comprehensive business logic migration preserves complex algorithms through microservices when needed
- Framework-specific preservation maintains Django backends, React frontends, and TypeScript execution engines
- Database migration strategies ensure zero data loss from original schemas (MySQL, PostgreSQL, SQLite)
- Layer-based service boundaries enable optional device distribution while maintaining monolith benefits
- Domain-specific performance requirements must be validated throughout development
- Constitutional requirements (<200ms UI, 95% context reduction, 100% functionality preservation) validated continuously
- Stop at any checkpoint to validate story independence before proceeding
- React/Next.js frontend provides consistent executive function accommodations across all 37 tools
