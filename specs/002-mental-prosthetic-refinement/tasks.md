# Tasks: Mental Prosthetic Platform (Refined)

**Input**: Design documents from `/specs/002-mental-prosthetic-refinement/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story based on the clarified single modular monolith architecture with React frontend.

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

## Phase 8: Service Adapter Integration (37 Tools)

**Goal**: Complete integration of all 37 tools from features/ directory into service adapters

**Independent Test**: All 37 tools accessible through unified interface with original functionality preserved

### Security Domain (13 tools)
- [ ] T090 [P] [TOOLS] Create Maltrail adapter in libs/service-adapters/security/maltrail_adapter.py
- [ ] T091 [P] [TOOLS] Create CyberChef adapter in libs/service-adapters/security/cyberchef_adapter.py
- [ ] T092 [P] [TOOLS] Create Nemesis adapter in libs/service-adapters/security/nemesis_adapter.py
- [ ] T093 [P] [TOOLS] Create Ghostwriter adapter in libs/service-adapters/security/ghostwriter_adapter.py
- [ ] T094 [P] [TOOLS] Create Brute Ratel C4 adapter in libs/service-adapters/security/brute_ratel_adapter.py
- [ ] T095 [P] [TOOLS] Create ApiScout adapter in libs/service-adapters/security/apiscout_adapter.py
- [ ] T096 [P] [TOOLS] Create RITA adapter in libs/service-adapters/security/rita_adapter.py
- [ ] T097 [P] [TOOLS] Create OneX adapter in libs/service-adapters/security/onex_adapter.py
- [ ] T098 [P] [TOOLS] Create BlackArch adapter in libs/service-adapters/security/blackarch_adapter.py

### Productivity Domain (8 tools)
- [ ] T099 [P] [TOOLS] Create Actual Budget adapter in libs/service-adapters/productivity/actual_adapter.py
- [ ] T100 [P] [TOOLS] Create Mealie adapter in libs/service-adapters/productivity/mealie_adapter.py
- [ ] T101 [P] [TOOLS] Create Dispatch adapter in libs/service-adapters/productivity/dispatch_adapter.py
- [ ] T102 [P] [TOOLS] Create IT-Tools adapter in libs/service-adapters/productivity/it_tools_adapter.py
- [ ] T103 [P] [TOOLS] Create Firecrawl adapter in libs/service-adapters/productivity/firecrawl_adapter.py
- [ ] T104 [P] [TOOLS] Create Goose adapter in libs/service-adapters/productivity/goose_adapter.py
- [ ] T105 [P] [TOOLS] Create Inspector adapter in libs/service-adapters/productivity/inspector_adapter.py

### MTG Domain (4 tools)
- [ ] T106 [P] [TOOLS] Create Commander Spellbook adapter in libs/service-adapters/mtg/spellbook_adapter.py
- [ ] T107 [P] [TOOLS] Create MTG Commander Map adapter in libs/service-adapters/mtg/commander_map_adapter.py
- [ ] T108 [P] [TOOLS] Create MTG Scripting Toolkit adapter in libs/service-adapters/mtg/scripting_toolkit_adapter.py
- [ ] T109 [P] [TOOLS] Create MTG card analysis adapter in libs/service-adapters/mtg/card_analysis_adapter.py

### Infrastructure Domain (12 tools)
- [ ] T110 [P] [TOOLS] Create Kong adapter in libs/service-adapters/infrastructure/kong_adapter.py
- [ ] T111 [P] [TOOLS] Create KasmVNC adapter in libs/service-adapters/infrastructure/kasmvnc_adapter.py
- [ ] T112 [P] [TOOLS] Create n8n adapter in libs/service-adapters/infrastructure/n8n_adapter.py
- [ ] T113 [P] [TOOLS] Create LScript adapter in libs/service-adapters/infrastructure/lscript_adapter.py
- [ ] T114 [P] [TOOLS] Create Chroma MCP adapter in libs/service-adapters/infrastructure/chroma_mcp_adapter.py
- [ ] T115 [P] [TOOLS] Create FileScopeMCP adapter in libs/service-adapters/infrastructure/filescope_mcp_adapter.py
- [ ] T116 [P] [TOOLS] Create n8n MCP adapter in libs/service-adapters/infrastructure/n8n_mcp_adapter.py
- [ ] T117 [P] [TOOLS] Create MalwareBazaar MCP adapter in libs/service-adapters/infrastructure/malwarebazaar_mcp_adapter.py
- [ ] T118 [P] [TOOLS] Create VirusTotal MCP adapter in libs/service-adapters/infrastructure/virustotal_mcp_adapter.py

### Integration Validation
- [ ] T119 [TOOLS] Validate all 37 tool adapters maintain original functionality
- [ ] T120 [TOOLS] Verify features/ directory migration completion (should be empty)
- [ ] T121 [TOOLS] Run comprehensive integration tests across all domains
- [ ] T122 [TOOLS] Validate domain-specific performance requirements achieved

**Checkpoint**: All 37 tools fully integrated with functionality preserved

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final system optimization

- [ ] T123 [P] Documentation updates for 37-tool integration in docs/
- [ ] T124 [P] Code cleanup and refactoring across service adapters
- [ ] T125 Performance optimization across all user stories and domains
- [ ] T126 [P] Security hardening for production deployment
- [ ] T127 [P] Accessibility audit and improvements (WCAG 2.1 AA compliance)
- [ ] T128 [P] Load testing with Artillery.js for domain-specific performance tiers
- [ ] T129 Final validation of constitutional requirements (<200ms UI, 95% context reduction)
- [ ] T130 Run quickstart.md validation and development environment verification

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) after foundational phase
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Service Adapter Integration (Phase 8)**: Can start after foundational infrastructure
- **Polish (Phase 9)**: Depends on all desired user stories and tool integration being complete

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

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Unified Dashboard)
4. Complete Phase 4: User Story 2 (AI-Enhanced Security)
5. **STOP and VALIDATE**: Test both P1 stories independently
6. Deploy/demo core executive function platform with AI security

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test unified dashboard → Deploy/Demo (Basic MVP)
3. Add User Story 2 → Test AI security → Deploy/Demo (Enhanced MVP with security AI)
4. Add User Story 6 → Test AI task management → Deploy/Demo
5. Add User Story 7 → Test cross-tool integration → Deploy/Demo  
6. Add User Story 8 → Test remote access → Deploy/Demo
7. Complete service adapter integration → All 37 tools available

### Parallel Team Strategy

With multiple developers after Foundational completion:

- **Developer A**: User Story 1 (Unified Dashboard) - Foundation for others
- **Developer B**: User Story 2 (AI Security) - Independent P1 priority
- **Developer C**: Service Adapter Integration - Can proceed in parallel
- **Developer D**: User Story 8 (Remote Access) - Independent infrastructure work

---

## Notes

- [P] tasks = different files, no dependencies within the same phase
- [Story] label maps task to specific user story for traceability  
- [TOOLS] label indicates service adapter integration tasks
- Each user story should be independently completable and testable
- 37-tool integration is distributed across multiple phases to enable parallel development
- Domain-specific performance requirements must be validated throughout development
- Constitutional requirements (<200ms UI, 95% context reduction, 100% functionality preservation) validated continuously
- Stop at any checkpoint to validate story independence before proceeding
- Modular monolith architecture enables easier testing and deployment compared to microservices approach