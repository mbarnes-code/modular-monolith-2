Input: Design documents from /specs/002-mental-prosthetic-refinement/ + Complete source code access for all 37 projects
Prerequisites: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓), Source code inventory (✓)
Organization: Tasks are grouped by user story to enable independent implementation and testing of each story. Architecture implements a modular monolith codebase with layer-based service boundaries (UI, API, Data, AI) across 4 domains (Security, Productivity, MTG, Infrastructure), with comprehensive business logic preservation through source code analysis and extraction.
Format: [ID] [P?] [Story] Description

[P]: Can run in parallel (different files, no dependencies)
[Story]: Which user story this task belongs to (e.g., US1, US2, US3)
Include exact file paths in descriptions
[SOURCE]: References specific source files from projects/ directory

Path Conventions (Modular Monolith Architecture)

Backend: apps/jane-orchestrator/src/
Frontend: apps/jane-ui/src/
Shared Libraries: libs/
Service Adapters: libs/service-adapters/
Source Reference: projects/ (read-only source code for all 37 tools)

Phase 0: Source Code Analysis (NEW - Foundation for All Work)
Purpose: Comprehensive analysis of all 37 source codebases to inform migration strategy and eliminate guesswork

 T000 [SOURCE] Create comprehensive source code inventory mapping all 37 projects in projects/ directory with technology stacks, key files, and complexity assessment
 T000a [P] [SOURCE] Map actual API endpoints and dependencies between all 37 projects by analyzing configuration files, import statements, and API calls
 T000b [P] [SOURCE] Extract all database schemas from projects//migrations/, projects//models/, and projects/*/schema/ to understand data relationships
 T000c [P] [SOURCE] Identify critical business logic files per domain by analyzing core algorithms, complex functions (>100 lines), and business rule implementations
 T000d [P] [SOURCE] Document existing test coverage by inventorying all test files in projects//tests/, projects//test/, and projects/*/tests/
 T000e [P] [SOURCE] Create migration complexity matrix categorizing each of 37 tools as Category A (Complex Algorithms), B (Domain Logic), or C (Utilities) based on actual code analysis
 T000f [SOURCE] Extract configuration dependencies from all projects//config/, projects//.env.example, and projects/*/docker-compose.yml files
 T000g [P] [SOURCE] Document authentication and session management patterns across all 37 tools for unified JWT integration planning
 T000h [P] [SOURCE] Map actual data flow patterns between tools by analyzing API clients, webhooks, and integration points in source code

Checkpoint: Complete understanding of all 37 tools before any implementation begins

Phase 1: Setup (Shared Infrastructure)
Purpose: Project initialization and modular monolith structure for 37-tool consolidation

 T001 Create modular monolith project structure per implementation plan with apps/jane-orchestrator/, apps/jane-ui/, and libs/ based on Phase 0 analysis
 T002 Initialize FastAPI project with Python dependencies in apps/jane-orchestrator/pyproject.toml using exact versions from source analysis
 T003 [P] Initialize React/Next.js project with TypeScript in apps/jane-ui/package.json matching framework versions from source projects
 T004 [P] Configure ESLint, Prettier, and TypeScript strict mode in apps/jane-ui/ compatible with existing tool configurations
 T005 [P] Configure Python linting (black, mypy, ruff) in apps/jane-orchestrator/ using standards from analyzed Python projects
 T006 Setup NX monorepo configuration for cross-app dependencies in nx.json with proper project references for all apps and libs
 T007 [P] Create shared library structure in libs/shared/ for cross-domain utilities based on common patterns found in source analysis
 T008 [P] Create UI design system structure in libs/ui/ for executive function accommodations extracting patterns from existing tool UIs


Phase 2: Foundational (Blocking Prerequisites)
Purpose: Core infrastructure that MUST be complete before ANY user story can be implemented
⚠️ CRITICAL: No user story work can begin until this phase is complete

 T009 [SOURCE] Setup PostgreSQL database schema and migrations framework in apps/jane-orchestrator/src/data/migrations/ incorporating schema patterns from projects/*/models/ analysis
 T010 [P] Configure Redis for caching and session management in apps/jane-orchestrator/src/data/redis/ using cache patterns identified in source analysis
 T011 [P] [SOURCE] Implement JWT-based authentication framework in apps/jane-orchestrator/src/api/auth/ compatible with authentication patterns from all 37 tools
 T012 [P] Setup FastAPI routing structure with domain organization in apps/jane-orchestrator/src/api/ based on API endpoint mapping from T000a
 T013 [SOURCE] Create base entity models for 4 domains in apps/jane-orchestrator/src/data/models/ incorporating data relationships discovered in T000b
 T014 [P] Configure error handling and logging infrastructure in apps/jane-orchestrator/src/utils/ using error patterns from source analysis
 T015 [P] [SOURCE] Setup environment configuration management in apps/jane-orchestrator/src/config/ incorporating configuration patterns from T000f
 T016 [SOURCE] Create React component library with ADHD/autism accommodations in libs/ui/components/ extracting UI patterns from existing tool interfaces
 T017 [P] Setup API client and state management (React Context + Zustand) in apps/jane-ui/src/services/ compatible with existing tool state patterns
 T018 [P] Configure WebSocket infrastructure for real-time sync in apps/jane-orchestrator/src/api/websocket/ based on real-time patterns found in source tools
 T019 [SOURCE] Create service adapter framework for 37-tool integration in libs/service-adapters/base/ using API patterns identified in T000a
 T020 Setup domain-specific performance monitoring (<200ms UI, domain tiers) in apps/jane-orchestrator/src/monitoring/ with benchmarks from existing tools
 T020a [P] Implement tool-specific rollback infrastructure in apps/jane-orchestrator/src/services/rollback/tool_rollback_service.py with rollback patterns from source analysis
 T020b [P] [SOURCE] Create database transaction rollback per tool domain in apps/jane-orchestrator/src/data/transaction_manager.py using transaction patterns from analyzed tools
 T020c [P] Implement service restart capabilities for individual tools in apps/jane-orchestrator/src/services/rollback/service_restart_manager.py
 T020d [P] [SOURCE] Create configuration state restoration from last known good state in apps/jane-orchestrator/src/config/state_backup_service.py using config backup patterns from tools
 T020e [P] Implement data consistency validation after rollback in apps/jane-orchestrator/src/services/rollback/consistency_validator.py
 T020f [P] Create system-wide fallback rollback capabilities in apps/jane-orchestrator/src/services/rollback/system_rollback_service.py

Checkpoint: Foundation ready - user story implementation can now begin in parallel

Phase 3: User Story 1 - Unified Executive Function Dashboard (Priority: P1) 🎯 MVP
Goal: Single unified interface accessing all 37 executive function tools across 4 domains
Independent Test: User can access dashboard and navigate between all 4 domains (Security: 13, Productivity: 8, MTG: 4, Infrastructure: 12 tools) within 200ms response time
Implementation for User Story 1

 T021 [P] [US1] [SOURCE] Create User Profile model with ADHD/autism settings in apps/jane-orchestrator/src/data/models/user_profile.py incorporating user management patterns from analyzed tools
 T022 [P] [US1] [SOURCE] Create Platform Session model for unified authentication in apps/jane-orchestrator/src/data/models/platform_session.py compatible with session patterns from all 37 tools
 T023 [P] [US1] Create Domain Classification model for 4 domains in apps/jane-orchestrator/src/data/models/domain.py based on complexity matrix from T000e
 T024 [P] [US1] [SOURCE] Create Integrated Tool model for 37 tools inventory in apps/jane-orchestrator/src/data/models/integrated_tool.py with metadata from source analysis
 T025 [US1] [SOURCE] Implement UserProfileService with executive function patterns in apps/jane-orchestrator/src/services/user_service.py incorporating user preference patterns from analyzed tools
 T026 [US1] Implement DomainService for 4-domain organization in apps/jane-orchestrator/src/services/domain_service.py based on complexity matrix and performance tiers
 T027 [US1] [SOURCE] Implement ToolRegistryService for 37-tool management in apps/jane-orchestrator/src/services/tool_registry_service.py with service discovery patterns from source analysis
 T028 [US1] [SOURCE] Create dashboard API endpoints in apps/jane-orchestrator/src/api/dashboard/ using API patterns and response structures from analyzed tools
 T029 [US1] [SOURCE] Create authentication API endpoints with JWT in apps/jane-orchestrator/src/api/auth/endpoints.py compatible with auth patterns from all 37 tools
 T030 [P] [US1] [SOURCE] Create executive function dashboard UI components in apps/jane-ui/src/components/Dashboard/ extracting layout patterns from existing tool interfaces
 T031 [P] [US1] [SOURCE] Create domain navigation component with consistent patterns in apps/jane-ui/src/components/Navigation/DomainNav.tsx using navigation patterns from analyzed tools
 T032 [P] [US1] [SOURCE] Create tool grid component for 37-tool display in apps/jane-ui/src/components/Tools/ToolGrid.tsx incorporating grid layouts from existing tools
 T033 [US1] [SOURCE] Implement dashboard page with state management in apps/jane-ui/src/pages/dashboard.tsx using state patterns from analyzed frontend tools
 T034 [US1] [SOURCE] Add session persistence and state management in apps/jane-ui/src/services/session.ts compatible with session management from all tools
 T035 [US1] Integrate WebSocket for real-time updates in apps/jane-ui/src/services/websocket.ts using WebSocket patterns found in source analysis
 T036 [US1] [SOURCE] Add accessibility compliance (WCAG 2.1 AA) to all dashboard components using accessibility patterns from existing tool UIs
 T037 [US1] Add performance monitoring for <200ms response time validation with benchmarks from existing tools
 T037a [P] [US1] [SOURCE] Implement unified user preferences system across all 37 tools in apps/jane-orchestrator/src/services/user_preferences_service.py using preference patterns from source analysis
 T037b [P] [US1] [SOURCE] Create user preferences API endpoints for ADHD/autism customizations in apps/jane-orchestrator/src/api/preferences/ compatible with existing preference APIs
 T037c [P] [US1] [SOURCE] Create user preferences UI components for executive function settings in apps/jane-ui/src/components/UserProfile/PreferencesPanel.tsx using UI patterns from analyzed tools
 T037d [P] [US1] [SOURCE] Implement cross-tool preference synchronization in apps/jane-orchestrator/src/services/preference_sync_service.py using sync patterns from source analysis

Checkpoint: At this point, User Story 1 should provide access to all 37 tools through unified interface

Phase 4: User Story 2 - AI-Enhanced Security Operations (Priority: P1)
Goal: AI-assisted threat hunting across 13 security tools with <1s response time
Independent Test: Security analyst can launch MISP, receive AI correlation, and perform threat hunting workflow within domain performance requirements
Implementation for User Story 2

 T038 [P] [US2] Create AI Enhancement Context model for LLM interactions in apps/jane-orchestrator/src/data/models/ai_context.py
 T039 [P] [US2] Create Security Profile model for airgapped operations in apps/jane-orchestrator/src/data/models/security_profile.py
 T040 [P] [US2] [SOURCE] Create service adapters for MISP integration in libs/service-adapters/security/misp_adapter.py using MISP API patterns from projects/security/misp/app/Controller/
 T041 [P] [US2] [SOURCE] Create service adapters for HELK integration in libs/service-adapters/security/helk_adapter.py using API patterns from projects/security/helk/
 T042 [P] [US2] [SOURCE] Create service adapters for SecurityOnion integration in libs/service-adapters/security/securityonion_adapter.py using patterns from projects/security/securityonion/
 T043 [P] [US2] [SOURCE] Create service adapters for YARA-X integration in libs/service-adapters/security/yarax_adapter.py using API patterns from projects/security/yara-x/
 T044 [US2] Implement AIEnhancementService for security domain in apps/jane-orchestrator/src/services/ai/security_ai_service.py
 T045 [US2] [SOURCE] Implement SecurityToolsService with 13-tool orchestration in apps/jane-orchestrator/src/services/security_service.py using orchestration patterns from security tools
 T046 [US2] [SOURCE] Create security domain API endpoints with <1s performance in apps/jane-orchestrator/src/api/security/ using endpoint patterns from analyzed security tools
 T047 [US2] Setup MCP server infrastructure for security enhancement in apps/jane-orchestrator/src/ai/mcp/
 T048 [P] [US2] [SOURCE] Create security dashboard UI components in apps/jane-ui/src/components/Security/ extracting dashboard patterns from security tool UIs
 T049 [P] [US2] [SOURCE] Create threat correlation interface in apps/jane-ui/src/components/Security/ThreatCorrelation.tsx using correlation UI patterns from MISP and HELK
 T050 [P] [US2] [SOURCE] Create security tool launcher components in apps/jane-ui/src/components/Security/ToolLauncher.tsx using launcher patterns from existing security tools
 T051 [US2] [SOURCE] Implement security workflow pages in apps/jane-ui/src/pages/security/ using workflow UI patterns from analyzed security tools
 T052 [US2] Add AI assistance integration to security components with context awareness
 T053 [US2] Add security-specific performance monitoring for <1s requirement with benchmarks from existing security tools

Checkpoint: Security operations with AI enhancement functional across 13 tools

Phase 5: User Story 6 - AI-Assisted Task Management (Priority: P2)
Goal: AI assistant for task breakdown and executive function support across all 37 tools
Independent Test: User can request AI task breakdown across multiple tool contexts and receive proactive reminders
Implementation for User Story 6

 T054 [P] [US6] Create Task & Workflow model for cross-domain activities in apps/jane-orchestrator/src/data/models/task.py
 T055 [P] [US6] Extend AI Enhancement Context for task management in apps/jane-orchestrator/src/data/models/ai_context.py
 T056 [US6] Implement TaskManagementService with AI integration in apps/jane-orchestrator/src/services/task_service.py
 T057 [US6] Implement AI Assistant Service for executive function support in apps/jane-orchestrator/src/services/ai/assistant_service.py
 T058 [US6] Create task management API endpoints in apps/jane-orchestrator/src/api/tasks/
 T059 [US6] Setup LLM integration with vLLM server in apps/jane-orchestrator/src/ai/llm/
 T060 [P] [US6] Create AI assistant UI components in apps/jane-ui/src/components/AI/
 T061 [P] [US6] Create task breakdown interface in apps/jane-ui/src/components/Tasks/TaskBreakdown.tsx
 T062 [P] [US6] Create reminder system components in apps/jane-ui/src/components/Tasks/Reminders.tsx
 T063 [US6] Implement AI chat interface with context awareness in apps/jane-ui/src/pages/ai-assistant.tsx
 T064 [US6] Add cross-tool context integration for AI suggestions
 T065 [US6] Add proactive reminder system with pattern recognition

Checkpoint: AI-assisted task management functional across all integrated tools

Phase 6: User Story 7 - Cross-Tool Data Integration (Priority: P3)
Goal: Seamless data flow between all 37 integrated applications across 4 domains
Independent Test: User can create data in one tool and verify it's accessible in related tools across domains without manual entry
Implementation for User Story 7

 T066 [P] [US7] Create Sync State model for cross-tool synchronization in apps/jane-orchestrator/src/data/models/sync_state.py
 T067 [P] [US7] [SOURCE] Create data mapping schemas for 37-tool integration in apps/jane-orchestrator/src/data/schemas/ using data relationships from T000b analysis
 T068 [US7] [SOURCE] Implement DataIntegrationService for cross-domain workflows in apps/jane-orchestrator/src/services/data_integration_service.py using integration patterns from source analysis
 T069 [US7] Implement EventBusService for real-time data propagation in apps/jane-orchestrator/src/services/event_bus_service.py
 T070 [US7] [SOURCE] Create data synchronization API endpoints in apps/jane-orchestrator/src/api/sync/ using sync patterns from analyzed tools
 T071 [US7] [SOURCE] Setup conflict resolution for concurrent data modifications in apps/jane-orchestrator/src/services/conflict_resolution.py using conflict resolution patterns from source tools
 T072 [P] [US7] [SOURCE] Create unified insights dashboard components in apps/jane-ui/src/components/Insights/ using dashboard patterns from existing tools
 T073 [P] [US7] [SOURCE] Create cross-domain data visualization in apps/jane-ui/src/components/Data/CrossDomainView.tsx using visualization patterns from analyzed tools
 T074 [P] [US7] Create data flow monitoring interface in apps/jane-ui/src/components/Sync/DataFlow.tsx
 T075 [US7] [SOURCE] Implement unified insights page in apps/jane-ui/src/pages/insights.tsx using insight page patterns from existing tools
 T076 [US7] Add real-time data synchronization indicators with sync patterns from source analysis
 T077 [US7] [SOURCE] Add data consistency validation across all 37 tools using validation patterns from source analysis

Checkpoint: Data flows seamlessly between all integrated applications

Phase 7: User Story 8 - Secure Remote Access (Priority: P4)
Goal: Secure mobile/remote access to all 37 executive function tools with PWA functionality
Independent Test: User can securely access platform from mobile device and perform key tasks across multiple tool domains
Implementation for User Story 8

 T078 [P] [US8] [SOURCE] Configure HTTPS and TLS certificates in apps/jane-orchestrator/src/config/security.py using security configurations from analyzed tools
 T079 [P] [US8] [SOURCE] Implement OAuth2 authentication for external access in apps/jane-orchestrator/src/api/oauth/ compatible with OAuth patterns from existing tools
 T080 [US8] Create RemoteAccessService for secure connectivity in apps/jane-orchestrator/src/services/remote_access_service.py
 T081 [US8] [SOURCE] Setup VPN/tunnel management for secure connections in apps/jane-orchestrator/src/services/vpn_service.py using VPN patterns from security tools
 T082 [US8] [SOURCE] Create secure remote API endpoints in apps/jane-orchestrator/src/api/remote/ using secure API patterns from analyzed tools
 T083 [P] [US8] [SOURCE] Configure PWA manifest and service worker in apps/jane-ui/public/ using PWA patterns from existing tools
 T084 [P] [US8] [SOURCE] Create mobile-responsive components in apps/jane-ui/src/components/Mobile/ using mobile UI patterns from analyzed tools
 T085 [P] [US8] [SOURCE] Optimize UI components for mobile viewports in libs/ui/components/ using responsive patterns from existing tool UIs
 T086 [US8] [SOURCE] Implement offline data caching for 24-hour capability in apps/jane-ui/src/services/cache.ts using caching patterns from source analysis
 T087 [US8] [SOURCE] Add mobile navigation and touch-friendly interactions using mobile interaction patterns from existing tools
 T088 [US8] [SOURCE] Add secure session management for remote connections using session patterns from analyzed tools
 T089 [US8] [SOURCE] Add data synchronization for offline/online transitions using sync patterns from source analysis

Checkpoint: Secure remote access functional with PWA capability

Phase 8: Security Domain Migration (Complex Business Logic)
Goal: Migrate 13 security tools preserving complex algorithms and data schemas per business logic analysis with layer-based service boundaries
Category A: Complex Algorithms (Preserve as Microservices)

 T090 [SOURCE] Extract MISP Event correlation algorithms from projects/security/misp/app/Model/Event.php (lines 2847-3621) preserving all conditional logic and threat intelligence scoring
 T091 [SOURCE] Extract Nemesis file analysis pipeline from projects/security/nemesis/cmd/enrichment/ maintaining all 15 enrichment modules and async processing workflow
 T092 [SOURCE] Preserve CyberChef operations engine from projects/security/cyberchef/src/core/operations/ (300+ operations) as embedded library with REST API wrapper
 T093 [P] [SOURCE] Create MISP database migration from projects/security/misp/INSTALL/MYSQL.sql to unified PostgreSQL schema preserving all threat intelligence relationships
 T094 [P] [SOURCE] Migrate MISP REST API endpoints from projects/security/misp/app/Controller/EventsController.php to FastAPI maintaining identical response schemas and rate limiting

Category B: Domain Logic (Modularize within Monolith)

 T095 [P] [SOURCE] Migrate HELK threat hunting logic from projects/security/helk/docker/helk-logstash/ to apps/jane-orchestrator/src/domains/security/helk/ preserving all Logstash pipeline configurations
 T096 [P] [SOURCE] Migrate SecurityOnion configuration management from projects/security/securityonion/salt/ preserving all Salt states and pillars for network monitoring
 T097 [P] [SOURCE] Migrate Maltrail detection rules from projects/security/maltrail/trails/ to unified security domain preserving all rule logic and detection patterns
 T098 [P] [SOURCE] Migrate YARA-X pattern matching from projects/security/yara-x/src/ to FastAPI endpoint preserving Rust core and WASM compilation
 T099 [P] [SOURCE] Convert APIScout, HexStrike-AI, Rita, OneX utilities from projects/security/ to FastAPI modules in security domain preserving all analysis algorithms

Category C: Utility Functions (Shared Libraries)

 T100 [P] [SOURCE] Extract Meterpreter payloads from projects/security/brute-ratel-c4/community-kit/ to shared security utilities library
 T101 [P] [SOURCE] Migrate Software Forensic Kit tools from projects/security/ to shared analysis library in libs/shared/security/ preserving all forensic algorithms
 T102 [P] [SOURCE] Convert BlackArch script collection from projects/security/blackarch/ to callable Python modules preserving all security tool integrations
 T103 [SOURCE] Convert legacy security tool UIs to React components preserving all functionality and workflow patterns from existing interfaces
 T104 [SOURCE] Create unified security dashboard integrating all migrated tools with FastAPI backend using dashboard patterns from existing security tools

Source-Specific Validation

 T104a [SOURCE] Extract and run MISP test suite from projects/security/misp/tests/ against migrated MISP components
 T104b [SOURCE] Extract and run Nemesis integration tests from projects/security/nemesis/tests/ against migrated pipeline
 T104c [SOURCE] Extract and run CyberChef operation tests from projects/security/cyberchef/tests/ against migrated operations engine
 T104d [SOURCE] Validate YARA-X pattern matching against projects/security/yara-x/tests/ test cases
 T104e [SOURCE] Performance benchmark security tools against baseline metrics from existing deployments


Phase 9: Productivity Domain Migration (FastAPI-Ready Projects)
Goal: Migrate 8 productivity tools leveraging existing FastAPI/TypeScript patterns from analysis with comprehensive framework preservation
Category A: Complex Workflow Engines (Microservice Preservation)

 T105 [SOURCE] Extract n8n workflow engine from projects/productivity/n8n/packages/core/src/WorkflowExecute.ts (2620 lines) preserving all node execution patterns and dependency management
 T106 [SOURCE] Preserve n8n 400+ integrations from projects/productivity/n8n/packages/nodes-base/ as separate service maintaining TypeScript execution engine and webhook handling
 T107 [SOURCE] Create database migration strategy for n8n from projects/productivity/n8n/packages/cli/src/databases/ to unified PostgreSQL schema preserving all workflow definitions and execution history

Category B: FastAPI-Ready Applications (Direct Migration)

 T108 [P] [SOURCE] Migrate Mealie FastAPI backend from projects/productivity/mealie/mealie/ maintaining recipe parsing algorithms and meal planning logic
 T109 [P] [SOURCE] Migrate Dispatch FastAPI incident management from projects/productivity/dispatch/src/dispatch/ preserving workflow orchestration and notification systems
 T110 [P] [SOURCE] Convert Mealie Nuxt.js frontend from projects/productivity/mealie/frontend/ to React/Next.js components compatible with unified dashboard
 T111 [P] [SOURCE] Integrate Dispatch PostgreSQL schema from projects/productivity/dispatch/src/dispatch/database/ with unified database maintaining incident data integrity

Category C: TypeScript Applications (Framework Migration)

 T112 [P] [SOURCE] Migrate Actual Budget CRDT synchronization engine from projects/productivity/actual/packages/crdt/ preserving conflict resolution algorithms and sync protocols
 T113 [P] [SOURCE] Convert Actual Budget SQLite schema from projects/productivity/actual/packages/loot-core/src/server/db/ to PostgreSQL while maintaining sync capabilities
 T114 [P] [SOURCE] Migrate Firecrawl Express.js backend from projects/productivity/firecrawl/apps/api/ to FastAPI preserving web scraping and BullMQ integration patterns
 T115 [P] [SOURCE] Migrate Goose AI agent system from projects/productivity/goose/ preserving Rust core with Python wrapper integration and MCP protocols

Category D: Utility Collections (Library Integration)

 T116 [P] [SOURCE] Convert IT-Tools 80+ developer utilities from projects/productivity/it-tools/src/tools/ to integrated React library modules preserving all utility algorithms
 T117 [P] [SOURCE] Migrate Inspector MCP protocol debugging from projects/productivity/inspector/ to unified development tools section preserving protocol validation
 T118 [SOURCE] Create unified productivity dashboard with FastAPI backend and React/Next.js frontend using dashboard patterns from existing productivity tools
 T119 [SOURCE] Integrate all productivity tools with shared authentication and session management using auth patterns from source analysis

Source-Specific Validation

 T119a [SOURCE] Extract and run n8n workflow tests from projects/productivity/n8n/packages/core/test/ against migrated workflow engine
 T119b [SOURCE] Extract and run Mealie recipe tests from projects/productivity/mealie/tests/ against migrated recipe management
 T119c [SOURCE] Extract and run Actual Budget sync tests from projects/productivity/actual/packages/loot-core/src/server/sync/ against migrated CRDT engine
 T119d [SOURCE] Validate Dispatch incident workflows against test cases from projects/productivity/dispatch/tests/
 T119e [SOURCE] Performance benchmark productivity tools against baseline metrics from existing deployments


Phase 10: MTG Domain Migration (Gaming/Algorithm-Heavy Projects)
Goal: Migrate 4 MTG tools preserving complex combo algorithms and card databases with framework-specific preservation
Category A: Complex Algorithms (Critical Business Logic)

 T120 [SOURCE] Extract Commander Spellbook variant generation algorithm from projects/mtg/commander-spellbook/spellbook/variants/variants_generator.py (1400+ lines) preserving graph traversal and combinatorial expansion
 T121 [SOURCE] Migrate Commander Spellbook Django backend from projects/mtg/commander-spellbook/backend/ preserving combo graph algorithms, variant computation, and color identity logic
 T122 [SOURCE] Create database migration from Commander Spellbook PostgreSQL schema in projects/mtg/commander-spellbook/backend/spellbook/migrations/ to unified schema preserving all card relationships
 T123 [P] [SOURCE] Preserve MTG Commander Map visualization algorithms from projects/mtg/mtg-commander-map/ maintaining card interaction network analysis and graph layouts

Category B: Domain Logic (Modular Integration)

 T124 [P] [SOURCE] Migrate MTG Scripting Toolkit card analysis from projects/mtg/mtg-scripting-toolkit/ to unified MTG domain preserving card parsing and deck analysis algorithms
 T125 [P] [SOURCE] Convert Commander Spellbook React frontend from projects/mtg/commander-spellbook/frontend/ to unified React/Next.js components preserving all search filters and combo displays
 T126 [P] [SOURCE] Integrate MTG Commander Map visualization with unified UI component library using visualization patterns from projects/mtg/mtg-commander-map/src/
 T127 [P] [SOURCE] Create unified MTG API endpoints in FastAPI preserving all card search and combo functionality from existing APIs

Category C: Utility Integration

 T128 [P] [SOURCE] Consolidate MTG card databases and Scryfall integration from projects/mtg/*/scryfall/ into shared card data service preserving rate limiting and caching
 T129 [P] [SOURCE] Create unified MTG dashboard with combo search, deck building, and card analysis tools using interface patterns from existing MTG tools
 T130 [SOURCE] Integrate MTG tools with AI assistant for deck building and combo suggestions using AI patterns from source analysis

Source-Specific Validation

 T130a [SOURCE] Extract and run Commander Spellbook tests from projects/mtg/commander-spellbook/backend/spellbook/tests/ against migrated variant generation
 T130b [SOURCE] Validate combo generation against test cases from projects/mtg/commander-spellbook/backend/spellbook/tests/test_variants.py
 T130c [SOURCE] Extract and run MTG Scripting Toolkit tests against migrated card analysis algorithms
 T130d [SOURCE] Performance benchmark MTG tools against baseline response times from existing deployments
 T130e [SOURCE] Validate color identity algorithms against test matrices from Commander Spellbook test suite


Phase 11: Infrastructure Domain Migration
Goal: Migrate all 12 infrastructure/integration tools from projects/ directory preserving business logic with layer-based service boundaries
Infrastructure Tools Business Logic Migration

 T131 [P] [SOURCE] Migrate Kong business logic from projects/infrastructure/kong/ preserving Lua plugin ecosystem and API gateway configurations
 T132 [P] [SOURCE] Migrate KasmVNC business logic from projects/infrastructure/kasmvnc/ preserving VNC protocol handling and desktop streaming capabilities
 T133 [P] [SOURCE] Migrate Ghostwriter business logic from projects/infrastructure/ghostwriter/ preserving report generation templates and engagement management
 T134 [P] [SOURCE] Migrate FileScopeMCP business logic from projects/infrastructure/filescope-mcp/ preserving file analysis protocols and MCP integrations
 T135 [P] [SOURCE] Migrate Chroma MCP business logic from projects/infrastructure/chroma-mcp/ preserving vector database operations and embedding management
 T136 [P] [SOURCE] Migrate Firecrawl MCP business logic from projects/infrastructure/firecrawl-mcp-server/ preserving web crawling protocols and content extraction
 T137 [P] [SOURCE] Migrate MalwareBazaar MCP business logic from projects/infrastructure/malwarebazaar-mcp/ preserving malware intelligence APIs and threat feeds
 T138 [P] [SOURCE] Migrate VirusTotal MCP business logic from projects/infrastructure/mcp-virustotal/ preserving threat analysis APIs and reputation scoring
 T139 [P] [SOURCE] Migrate n8n MCP business logic from projects/infrastructure/n8n-mcp-server/ preserving workflow automation protocols and node integrations
 T140 [P] [SOURCE] Migrate SecurityOnion n8n workflows from projects/infrastructure/securityonion-n8n-workflows/ preserving security automation and alert processing
 T141 [P] [SOURCE] Migrate Brute-Ratel-C4 business logic from projects/infrastructure/brute-ratel-c4-community-kit/ preserving red team frameworks and payload generation
 T142 [P] [SOURCE] Migrate LScript business logic from projects/infrastructure/lscript/ preserving automation scripting and system administration tools

Source-Specific Validation

 T142a [SOURCE] Extract and run Kong plugin tests from projects/infrastructure/kong/spec/ against migrated API gateway functionality
 T142b [SOURCE] Validate MCP server implementations against protocol specifications from projects/infrastructure/*/mcp/
 T142c [SOURCE] Extract and run Ghostwriter template tests from projects/infrastructure/ghostwriter/tests/ against migrated report generation
 T142d [SOURCE] Performance benchmark infrastructure tools against baseline metrics from existing deployments


Phase 12: LLM Server Enhancement
Goal: Enhance existing LLM servers for integrated tool support with layer-based AI service boundaries
LLM Integration Enhancement

 T143 [P] [SOURCE] Enhance cyber-llm-server with security tool integration in apps/cyber-llm-server/src/integrations/ using integration patterns from security tools
 T144 [P] [SOURCE] Enhance mtg-llm-server with MTG tool integration in apps/mtg-llm-server/src/integrations/ using integration patterns from MTG tools
 T145 [P] [SOURCE] Enhance code-llm-server with development tool integration in apps/code-llm-server/src/integrations/ using integration patterns from dev tools
 T146 [SOURCE] Create unified LLM router in apps/jane-orchestrator/src/services/llm_router.py using routing patterns identified in source analysis
 T147 [SOURCE] Implement AI context sharing across all tools in apps/jane-orchestrator/src/services/ai_context_sharing.py using context patterns from analyzed tools


Phase 13: Features Directory Migration Completion
Goal: Complete migration of all business logic from features/ directory, ensuring empty directory per spec requirements with comprehensive validation
Migration Validation and Cleanup

 T148 [SOURCE] Validate all business logic preservation with measurable criteria using original test suites and performance benchmarks from source analysis:

 T148a [SOURCE] Extract and run original test suites from all 37 projects in projects/*/tests/ against migrated implementations in apps/jane-orchestrator/tests/preservation/
 T148b [SOURCE] Implement API endpoint parity validation comparing original API schemas from projects/*/api/ with migrated endpoints for identical input/output behavior
 T148c [SOURCE] Create UI workflow automation tests comparing original interfaces from projects/*/frontend/ with integrated components for behavioral equivalence
 T148d [SOURCE] Validate algorithm preservation through identical test suite execution using test cases from projects/*/tests/ against migrated algorithms
 T148e [SOURCE] Measure performance benchmarks comparing original deployment metrics from projects/*/benchmarks/ with integrated tools for performance parity
 T148f [SOURCE] Create preservation compliance report generator comparing original functionality documentation from projects/*/docs/ with migrated capabilities


 T149 [SOURCE] Create migration status tracking in apps/jane-orchestrator/src/services/migration_tracker.py monitoring migration completeness across all 37 tools
 T150 [SOURCE] Implement automated validation that features/ directory is completely empty and all business logic successfully migrated to monolith structure
 T151 [P] [SOURCE] Create integration status dashboard in apps/jane-ui/src/components/Migration/IntegrationStatus.tsx showing migration progress and validation results for all 37 tools
 T152 [P] [SOURCE] Document all migrated tools and their new locations in docs/migration-log.md with source file mappings from projects/ to apps/ and libs/
 T153 Remove all remaining code from features/ directory after successful migration validation with 100% business logic preservation confirmed
 T154 [SOURCE] Update project documentation to reflect completed integration with features/ directory empty and comprehensive source code preservation documented

Checkpoint: All 37 tools fully migrated with 100% business logic preservation validated through original test suites

Phase 14: Polish & Cross-Cutting Concerns
Purpose: Final improvements affecting multiple user stories and production readiness with comprehensive system optimization

 T155 [P] [SOURCE] Performance optimization across all service adapters using performance patterns identified in source analysis
 T156 [P] [SOURCE] Security hardening for all API endpoints using security configurations from analyzed tools
 T157 [P] [SOURCE] Accessibility improvements (WCAG 2.1 AA compliance) using accessibility patterns from existing tool UIs
 T158 [P] [SOURCE] Error handling enhancement using error handling patterns from all 37 tools in source analysis
 T159 [P] [SOURCE] Logging and monitoring setup using logging patterns from analyzed tools for production deployment
 T160 [P] [SOURCE] Documentation updates and API documentation using documentation patterns from projects/*/docs/ for all 37 integrated tools
 T161 [P] [SOURCE] Docker composition optimization using containerization patterns from projects/*/docker/
 T162 [P] [SOURCE] Database performance tuning using database optimization patterns from analyzed tools
 T163 [P] [SOURCE] WebSocket connection scaling using WebSocket patterns from analyzed tools
 T164 [P] [SOURCE] Implement automated backup to Synology NAS using backup patterns from existing tools:

 T164a [SOURCE] Create PostgreSQL backup automation using database backup patterns from projects/*/backup/
 T164b [SOURCE] Implement SQLite database backup using local backup patterns from analyzed tools
 T164c [SOURCE] Create Synology NAS integration using file transfer patterns from existing tools
 T164d [SOURCE] Implement backup verification using validation patterns from source analysis
 T164e [SOURCE] Add backup monitoring using monitoring patterns from analyzed tools


 T165 [P] [SOURCE] Add vulnerability scanning using security scanning patterns from analyzed security tools
 T166 [P] [SOURCE] Create user documentation using documentation patterns from projects/*/docs/ for all 37 integrated tools
 T167 [P] [SOURCE] Implement load testing with performance benchmarks from existing tool deployments
 T168 [P] [SOURCE] Setup CI/CD pipeline using deployment patterns from projects//.github/ and projects//ci/
 T169a [P] [SOURCE] Implement Security Domain performance validation using benchmarks from existing security tool deployments
 T169b [P] [SOURCE] Implement Productivity Domain performance validation using benchmarks from existing productivity tool deployments
 T169c [P] [SOURCE] Implement MTG Domain performance validation using benchmarks from existing MTG tool deployments
 T169d [P] [SOURCE] Implement Infrastructure Domain performance validation using benchmarks from existing infrastructure tool deployments
 T169e [P] [SOURCE] Create automated domain performance monitoring dashboard using monitoring patterns from analyzed tools
 T169 [SOURCE] Final validation of constitutional requirements using validation frameworks from source analysis
 T170 [SOURCE] Run complete quickstart.md validation and deployment verification using deployment patterns from all 37 tools


Dependencies & Execution Order
Phase Dependencies

Source Analysis (Phase 0): No dependencies - MUST complete before any other work
Setup (Phase 1): Depends on Phase 0 completion - uses source analysis results
Foundational (Phase 2): Depends on Setup completion - BLOCKS all user stories
User Stories (Phases 3-7): All depend on Foundational phase completion

User stories can proceed in parallel (if staffed) after foundational phase
Or sequentially in priority order (P1 → P2 → P3 → P4)


Domain Migrations (Phases 8-11): Depend on User Stories 1-3 completion (core platform stability)
LLM Enhancement (Phase 12): Depends on User Story 2 (AI-Assisted Task Management) completion
Migration Completion (Phase 13): Depends on all domain migrations (Phases 8-11) completion
Polish (Phase 14): Depends on all core functionality and migration being complete

Source Code Analysis Benefits
Risk Mitigation Through Source Access:

Hidden Dependencies: Discovered through T000a API mapping and T000f configuration analysis
Business Logic Preservation: Validated through original test suites (T148a-T148f)
Performance Baselines: Established through existing deployment metrics (T148e)
Integration Patterns: Identified through source code analysis (T000c)

Enhanced Validation Strategy
Original Test Suite Integration:

Extract tests from projects/*/tests/ directories
Run against migrated implementations
Prove identical behavior through automated testing
Maintain performance parity through benchmarking


Implementation Strategy
MVP First (Enhanced with Source Analysis)

Complete Phase 0: Source Analysis (T000-T000h) - 8 tasks - CRITICAL FOUNDATION
Complete Phase 1: Setup (T001-T008) - 8 tasks
Complete Phase 2: Foundational (T009-T020f) - 18 tasks
Complete Phase 3: User Story 1 (T021-T037d) - 21 tasks
Complete Phase 4: User Story 2 (T038-T053) - 16 tasks
STOP and VALIDATE: Test both P1 stories independently using original test suites
Deploy/demo core executive function platform with AI security

Comprehensive Delivery (Source-Enhanced Migration)

Source Foundation: Phase 0 (T000-T000h) → Complete understanding of all 37 tools
Technical Foundation: Setup + Foundational (T001-T020f) → Core platform ready
MVP: Add User Stories 1 & 2 (T021-T053) → Test with original test suites → Deploy unified dashboard with AI
Core Platform: Add User Stories 6 & 7 (T054-T077) → Test AI assistance and data integration → Deploy enhanced version
Remote Access: Add User Story 8 (T078-T089) → Test secure remote capabilities → Deploy mobile-ready platform
Security Migration: Phase 8 (T090-T104e) → Comprehensive security tool preservation with original test validation
Productivity Migration: Phase 9 (T105-T119e) → FastAPI-ready applications with original test validation
MTG Migration: Phase 10 (T120-T130e) → Complex algorithms with original test validation
Infrastructure Migration: Phase 11 (T131-T142d) → MCP servers and utility integration with test validation
AI Enhancement: Phase 12 (T143-T147) → LLM server integration → Validate cross-domain AI support
Migration Completion: Phase 13 (T148-T154) → Validate 100% business logic preservation using original test suites → Empty features/ directory
Production Polish: Phase 14 (T155-T170) → Production readiness and optimization → Full deployment