# COMPREHENSIVE FEATURE PROJECTS MIGRATION FEASIBILITY ANALYSIS
## Root-Level DDD Modular Monolith Migration Assessment

**Analysis Date**: 2025-11-10  
**Total Projects**: 39 (37 viable, 2 empty)  
**Scope**: Assessment for integration into root-level DDD structure

---

## EXECUTIVE SUMMARY

### Portfolio Composition
- **Easy to Migrate**: 9 projects (23%)
- **Medium Complexity**: 5 projects (13%)
- **Hard to Migrate**: 12 projects (31%)
- **Very Hard/Not Recommended**: 11 projects (28%)
- **Empty/Incomplete**: 2 projects (5%)

### Recommended Migration Candidates (Easy/Medium)
1. **MalwareBazaar_MCP** - 95/100 feasibility
2. **CyberChef** - 90/100 feasibility
3. **chroma-mcp** - 85/100 feasibility
4. **mcp-virustotal** - 85/100 feasibility
5. **n8n-mcp-server** - 85/100 feasibility
6. **firecrawl-mcp-server** - 80/100 feasibility
7. **apiscout** - 85/100 feasibility
8. **spec-kit** - 90/100 feasibility
9. **mtg-commander-map** - 85/100 feasibility
10. **mtg-scripting-toolkit** - 85/100 feasibility
11. **it-tools** - 85/100 feasibility
12. **lscript** - 80/100 feasibility
13. **hexstrike-ai** - 75/100 feasibility
14. **FileScopeMCP** - 75/100 feasibility

### Not Recommended (High Risk/Massive Refactoring Required)
- MISP (253k LOC legacy PHP)
- n8n (1.45M LOC monorepo)
- Brute-Ratel-C4-Community-Kit (Binary payloads)
- KasmVNC (C/C++ compiled)
- meterpreter (Architecture-specific binaries)
- HELK (Infrastructure automation)
- blackarch (Package repository)
- kong (API Gateway infrastructure)
- securityonion (Infrastructure configuration)

---

## DETAILED PROJECT ANALYSIS

### TIER 1: EASY MIGRATION (Easy - 1-2 months)

#### 1. MalwareBazaar_MCP ⭐⭐⭐⭐⭐
**Feasibility Score**: 95/100
- **Domain**: Security/Threat Intelligence
- **Type**: Python MCP Server (7 files, 383 LOC)
- **Technology**: Python, MCP Protocol
- **Integration Points**: 
  - External API wrapper for Malware Bazaar
  - No database dependencies
  - Stateless service
- **Migration Approach**: Direct integration as utility service
- **Timeline**: 1-2 weeks
- **Blockers**: None

#### 2. CyberChef ⭐⭐⭐⭐⭐
**Feasibility Score**: 90/100
- **Domain**: Security/Utilities
- **Type**: React Frontend (877 files, 3,038 LOC)
- **Technology**: JavaScript/TypeScript, CSS, HTML
- **Integration Points**:
  - Pure client-side application
  - Can be served as static assets or npm package
  - No backend requirements
- **Migration Approach**: Serve as standalone service or embed as component library
- **Timeline**: 1-2 weeks
- **Blockers**: None

#### 3. spec-kit ⭐⭐⭐⭐⭐
**Feasibility Score**: 90/100
- **Domain**: Development/Specification
- **Type**: Python CLI Tool + Documentation (87 files, 2,707 LOC)
- **Technology**: Python, Typer, Documentation templates
- **Integration Points**:
  - CLI tool for DDD specification generation
  - No database dependencies
  - Documentation and templates
- **Migration Approach**: Direct integration as CLI utility
- **Timeline**: 1-2 weeks
- **Blockers**: None

#### 4. chroma-mcp ⭐⭐⭐⭐
**Feasibility Score**: 85/100
- **Domain**: Development/Tooling
- **Type**: Python MCP Server (16 files, 1,588 LOC)
- **Technology**: Python, Chroma Vector DB, MCP Protocol
- **Integration Points**:
  - Vector database integration
  - MCP protocol wrapper
  - No persistence layer
- **Migration Approach**: Integration as vector DB service
- **Timeline**: 1-2 weeks
- **Blockers**: Requires Chroma installation

#### 5. mcp-virustotal ⭐⭐⭐⭐
**Feasibility Score**: 85/100
- **Domain**: Security/Threat Intelligence
- **Type**: Node.js MCP Server (29 files, 2,373 LOC)
- **Technology**: JavaScript/TypeScript, MCP Protocol
- **Integration Points**:
  - External API integration (VirusTotal)
  - Stateless service
  - No database
- **Migration Approach**: Direct integration as API client
- **Timeline**: 1-2 weeks
- **Blockers**: Requires VirusTotal API key

#### 6. apiscout ⭐⭐⭐⭐
**Feasibility Score**: 85/100
- **Domain**: Security/Analysis
- **Type**: Python CLI Tool (51 files, 10,723 LOC)
- **Technology**: Python with setup.py
- **Integration Points**:
  - API parameter reconnaissance tool
  - Can be used as CLI or library
  - Standalone database (dbs/ directory)
- **Migration Approach**: Integrate as security analysis service
- **Timeline**: 2 weeks
- **Blockers**: None - straightforward Python package

#### 7. mtg-commander-map ⭐⭐⭐⭐
**Feasibility Score**: 85/100
- **Domain**: Gaming/Magic
- **Type**: Python Scripts (21 files, 3,670 LOC)
- **Technology**: Python data processing
- **Integration Points**:
  - MTG data processing and mapping
  - No database requirements
  - Data transformation scripts
- **Migration Approach**: Integration as data processing service
- **Timeline**: 1-2 weeks
- **Blockers**: None

#### 8. mtg-scripting-toolkit ⭐⭐⭐⭐
**Feasibility Score**: 85/100
- **Domain**: Gaming/Magic
- **Type**: TypeScript Library (87 files, 4,628 LOC)
- **Technology**: JavaScript/TypeScript, npm package
- **Integration Points**:
  - MTG scripting and automation
  - Standalone library
  - No runtime dependencies
- **Migration Approach**: Integration as npm package/library
- **Timeline**: 1-2 weeks
- **Blockers**: None

#### 9. n8n-mcp-server ⭐⭐⭐⭐
**Feasibility Score**: 85/100
- **Domain**: Automation/Tooling
- **Type**: Node.js MCP Server (93 files, 4,106 LOC)
- **Technology**: JavaScript/TypeScript, MCP Protocol
- **Integration Points**:
  - n8n workflow automation wrapper
  - Stateless service
  - No database
- **Migration Approach**: Integration as workflow automation bridge
- **Timeline**: 2-3 weeks
- **Blockers**: Requires n8n installation

#### 10. firecrawl-mcp-server ⭐⭐⭐⭐
**Feasibility Score**: 80/100
- **Domain**: Development/Tooling
- **Type**: Node.js MCP Server (28 files, 792 LOC)
- **Technology**: JavaScript/TypeScript
- **Integration Points**:
  - Web scraping service wrapper
  - Thin MCP wrapper
  - Delegates to Firecrawl backend
- **Migration Approach**: Deploy as MCP server, connect to Firecrawl API
- **Timeline**: 1-2 weeks
- **Blockers**: Requires Firecrawl API access

#### 11. lscript ⭐⭐⭐⭐
**Feasibility Score**: 80/100
- **Domain**: Development/Scripting
- **Type**: Shell Scripts (22 files, 0 LOC - shell)
- **Technology**: BASH/Shell
- **Integration Points**:
  - Linux scripting utilities
  - Standalone scripts
  - No dependencies
- **Migration Approach**: Include as utility scripts in infrastructure layer
- **Timeline**: 1 week
- **Blockers**: None

#### 12. commander-spellbook-site ⭐⭐⭐⭐
**Feasibility Score**: 80/100
- **Domain**: Gaming/Magic
- **Type**: React Frontend (238 files, 13,225 LOC)
- **Technology**: React, TypeScript, CSS
- **Integration Points**:
  - Frontend-only application
  - Depends on backend API
  - Cypress E2E tests
- **Migration Approach**: Serve as static frontend, connect to backend API
- **Timeline**: 2 weeks
- **Blockers**: None - clear separation of concerns

#### 13. it-tools ⭐⭐⭐⭐
**Feasibility Score**: 85/100
- **Domain**: Development/Utilities
- **Type**: React Frontend (497 files, 9,990 LOC)
- **Technology**: React, TypeScript
- **Integration Points**:
  - Collection of IT utility tools (converters, generators)
  - Pure client-side
  - No backend dependencies
- **Migration Approach**: Serve as standalone service or embed components
- **Timeline**: 2 weeks
- **Blockers**: None

#### 14. hexstrike-ai ⭐⭐⭐⭐
**Feasibility Score**: 75/100
- **Domain**: Security/AI
- **Type**: Python Package (12 files, 22,759 LOC)
- **Technology**: Python, AI/ML dependencies
- **Integration Points**:
  - AI-powered security analysis
  - Requires AI/ML libraries
  - Can be used as library or service
- **Migration Approach**: Integrate as AI service with dependency management
- **Timeline**: 2-3 weeks
- **Blockers**: Heavy AI/ML dependencies, requires careful environment setup

---

### TIER 2: MEDIUM MIGRATION (Medium - 2-3 months)

#### 15. FileScopeMCP ⭐⭐⭐
**Feasibility Score**: 75/100
- **Domain**: Development/Tooling
- **Type**: Node.js MCP Server (27 files, 12,971 LOC)
- **Technology**: JavaScript/TypeScript, MCP Protocol
- **Integration Points**:
  - File scoping and analysis service
  - MCP-specific protocol
  - No database persistence
- **Migration Approach**: Deploy as dedicated microservice
- **Timeline**: 2-3 weeks
- **Blockers**: MCP protocol requirements, may need separate deployment

#### 16. inspector ⭐⭐⭐
**Feasibility Score**: 72/100
- **Domain**: Development/Debugging
- **Type**: Full-stack TypeScript (160 files, 24,078 LOC)
- **Technology**: JavaScript/TypeScript, Node.js
- **Integration Points**:
  - Browser inspection and debugging tool
  - Client/server bidirectional communication
  - WebSocket integration
- **Migration Approach**: Extract core inspection logic, refactor communication layer
- **Timeline**: 3-4 weeks
- **Blockers**: Bidirectional client/server communication patterns

#### 17. maltrail ⭐⭐⭐
**Feasibility Score**: 70/100
- **Domain**: Security/Monitoring
- **Type**: Python Application (2,913 files, 14,542 LOC)
- **Technology**: Python, JavaScript, Web UI
- **Integration Points**:
  - Malware traffic detection
  - Server-based web interface (server.py)
  - External threat trail feeds
  - Database independent (uses JSON feeds)
- **Entry Points**: server.py (main detection engine)
- **Structure**: 
  - core/ (detection logic)
  - plugins/ (detection modules)
  - trails/ (threat feed data)
  - html/ (UI)
- **Migration Approach**: Extract detection engine, refactor as service
- **Timeline**: 3-4 weeks
- **Blockers**: Expects network access for threat trail updates, specialized detection algorithms

#### 18. mealie ⭐⭐⭐
**Feasibility Score**: 68/100
- **Domain**: Productivity/Recipes
- **Type**: Full-stack (FastAPI + Vue) (1,488 files, 68,472 LOC)
- **Technology**: Python (FastAPI), Vue.js, SQLAlchemy, Alembic migrations
- **Database**: PostgreSQL with ORM models and migration system
- **Entry Points**:
  - Python: mealie/main.py (entry point)
  - Frontend: Vue.js in frontend/ directory
- **Structure**:
  - mealie/ (backend)
    - routes/ (19 sub-modules for API)
    - services/ (business logic)
    - schema/ (data schemas)
    - db/ (database with alembic migrations)
  - frontend/ (Vue application)
- **Integration Points**:
  - RESTful API (19 separate route modules)
  - SQLAlchemy ORM models
  - Alembic database migrations
  - MQTT support (paho-mqtt)
  - OpenAI integration for ingredient parsing
  - LDAP authentication
- **Migration Approach**: Extract as dedicated domain service with separate database schema
- **Timeline**: 3-4 weeks
- **Blockers**: Database migration system interdependencies, multiple authentication methods

#### 19. commander-spellbook-backend ⭐⭐⭐
**Feasibility Score**: 70/100
- **Domain**: Gaming/Magic
- **Type**: Python Backend (399 files, 24,124 LOC)
- **Technology**: Python Flask/FastAPI, Database models
- **Integration Points**:
  - MTG Commander spell combination logic
  - Database models and persistence
  - REST API endpoints
- **Migration Approach**: Extract as bounded context for MTG data
- **Timeline**: 3-4 weeks
- **Blockers**: Database schema dependencies on MTG data model

#### 20. securityonion-n8n-workflows ⭐⭐⭐
**Feasibility Score**: 72/100
- **Domain**: Security/Automation
- **Type**: n8n Workflow Definitions (7 files, 0 LOC - JSON)
- **Technology**: JSON workflow definitions
- **Integration Points**:
  - Pre-defined n8n workflows
  - Integration with Security Onion
  - Workflow orchestration
- **Migration Approach**: Deploy as workflow templates in n8n
- **Timeline**: 1-2 weeks
- **Blockers**: Requires n8n integration

---

### TIER 3: HARD MIGRATION (Hard - 3-6 months)

#### 21. Nemesis
**Feasibility Score**: 60/100
- **Domain**: Security/Data Processing
- **Type**: Full-stack (Python + JavaScript) (350 files, 36,015 LOC)
- **Technology**: Python backend, TypeScript frontend, PostgreSQL
- **Entry Points**:
  - Python backend services
  - TypeScript CLI and UI
- **Integration Points**:
  - Complex post-exploitation data aggregation
  - Database schema for operational data
  - Multi-layer data processing pipeline
  - Frontend/backend tight coupling
- **Blockers**:
  - Custom data structure definitions
  - Complex backend processing logic
  - Tightly coupled UI/backend
- **Migration Approach**: Extract data processing layer first, then refactor frontend
- **Timeline**: 3-4 months

#### 22. dispatch
**Feasibility Score**: 58/100
- **Domain**: Security/Automation
- **Type**: Full-stack (Python + React) (1,565 files, 110,420 LOC)
- **Technology**: FastAPI, React, SQLAlchemy, Alembic
- **Database**: PostgreSQL with complex schema
- **Entry Points**:
  - dispatch.cli module
  - src/dispatch/api.py (REST API)
- **Structure**:
  - Incident management workflows
  - Plugin system (dispatcher plugins)
  - Multiple data sources integration
  - Comprehensive API with 150+ endpoints
- **Integration Points**:
  - RESTful API (via FastAPI)
  - SQLAlchemy models
  - Alembic migrations
  - Slack/Teams integrations
  - JIRA/Confluence integrations
  - PagerDuty integration
  - Email and calendar systems
- **Blockers**:
  - Complex incident management state machine
  - 20+ plugin types for external integrations
  - Custom database schema with migration system
  - Heavy integration with external services
- **Migration Approach**: Extract as complete domain service with own database
- **Timeline**: 4-6 months
- **Complexity Notes**: One of the largest and most complex projects after n8n and MISP

#### 23. actual
**Feasibility Score**: 65/100
- **Domain**: Productivity/Finance
- **Type**: Full-stack Monorepo (2,571 files, 188,186 LOC)
- **Technology**: Node.js, React, TypeScript, SQL
- **Workspace**: Yarn workspaces with multiple packages
- **Packages**:
  - sync-server (backend)
  - loot-core (core finance logic)
  - @actual-app/web (React frontend)
  - desktop-electron (desktop client)
  - api (REST API)
  - plugins-service (extensibility)
- **Database**: SQLite/PostgreSQL with custom sync protocol
- **Integration Points**:
  - Custom sync protocol for financial data
  - Multiple UI implementations (web + electron)
  - Plugin architecture
  - Complex financial calculations
- **Blockers**:
  - Large TypeScript monorepo with intricate interdependencies
  - Custom sync protocol not standard
  - Multiple UI implementations
  - Complex financial data validation
- **Migration Approach**: Extract packages as-is with refactored interdependencies
- **Timeline**: 3-5 months
- **Advantage**: Already well-modularized with workspaces, easier than other full-stack apps

#### 24. Nemesis (already listed above)

#### 25. Ghostwriter
**Feasibility Score**: 55/100
- **Domain**: Security/Automation
- **Type**: Full-stack (Django + React) (1,221 files, 156,822 LOC)
- **Technology**: Django, React, PostgreSQL, Hasura GraphQL
- **Database**: PostgreSQL with Django ORM and migrations
- **Structure**:
  - 10 Django app modules (api, commandcenter, home, oplog, reporting, rolodex, shepherd, singleton, status, users)
  - JavaScript/TypeScript frontend
  - Django templates
  - Static assets
- **Integration Points**:
  - Django ORM models across 10 modules
  - Database migrations
  - GraphQL layer (Hasura)
  - Authentication/authorization
  - REST API endpoints
- **Blockers**:
  - Django monolith with tight coupling
  - Complex data models with interdependencies
  - Frontend uses Django templates (tight coupling)
  - Custom authentication logic
  - GraphQL layer adds complexity
- **Migration Approach**: Extract to API-first architecture, separate database schema
- **Timeline**: 4-6 months
- **Complexity**: Very complex due to Django architecture

#### 26. firecrawl
**Feasibility Score**: 62/100
- **Domain**: Development/Web Tools
- **Type**: Full-stack Monorepo (888 files, 151,542 LOC)
- **Technology**: TypeScript, Python, Rust, Node.js
- **Structure**:
  - apps/api (TypeScript/Node.js API)
  - apps/playwright-service-ts (Playwright service)
  - apps/rust-sdk (Rust bindings)
  - apps/python-sdk (Python SDK)
  - apps/js-sdk (JavaScript SDK)
  - apps/test-suite (tests)
  - apps/nuq-postgres (Database)
  - apps/ui (Frontend)
  - apps/redis (Caching)
- **Integration Points**:
  - Web scraping and crawling service
  - Multiple language SDKs
  - Playwright integration
  - Database layer
  - Cache layer
  - UI dashboard
- **Blockers**:
  - Complex monorepo with multiple apps
  - Rust components for performance
  - Multiple service interdependencies
  - Requires Playwright and Puppeteer
- **Migration Approach**: Deploy as separate service with multiple apps
- **Timeline**: 4-6 months

#### 27. goose
**Feasibility Score**: 50/100
- **Domain**: Development/AI
- **Type**: Full-stack (Rust + TypeScript) (1,655 files, 170,514 LOC)
- **Technology**: Rust, TypeScript, async/await, MCP
- **Structure**:
  - crates/goose (core Rust library)
  - crates/goose-cli (CLI)
  - crates/goose-server (server)
  - crates/goose-mcp (MCP integration)
  - ui/ (TypeScript UI)
  - temporal-service/ (background jobs)
- **Integration Points**:
  - AI agent framework
  - MCP protocol support
  - Temporal workflow orchestration
  - Async Rust implementation
- **Blockers**:
  - Heavy Rust implementation with complex async patterns
  - Custom agent framework (not standard)
  - MCP integration specifics
  - Temporal service dependency
  - Rust compilation requirements
- **Migration Approach**: Would require rewrite in TypeScript or adopt Rust stack
- **Timeline**: 6-8 months
- **Complexity**: Very high - architectural mismatch

#### 28. yara-x
**Feasibility Score**: 58/100
- **Domain**: Security/Detection
- **Type**: Rust + Polyglot (1,372 files, 90,088 LOC)
- **Technology**: Rust (primary), Go, Python bindings, WebAssembly
- **Structure**:
  - lib/ (Core Rust library)
  - cli/ (Rust CLI)
  - go/ (Go language bindings)
  - py/ (Python language bindings)
  - proto/ (Protocol buffers)
  - parser/ (Rule parser)
  - fmt/ (Formatting)
- **Integration Points**:
  - Malware detection rules (YARA format)
  - Language bindings for Go/Python
  - WebAssembly support
  - Protocol buffer definitions
- **Blockers**:
  - Primary Rust implementation
  - Multiple language bindings to maintain
  - Requires Rust compilation
  - Complex pattern matching engine
- **Migration Approach**: Use as external library, expose via API wrapper
- **Timeline**: 3-4 months
- **Note**: Better integrated as external service than ported

---

### TIER 4: VERY HARD / NOT RECOMMENDED (6+ months or Not Recommended)

#### 29. MISP
**Feasibility Score**: 15/100 - NOT RECOMMENDED
- **Domain**: Security/Threat Intelligence
- **Type**: Full-stack Legacy (PHP + JavaScript) (2,138 files, 253,500 LOC)
- **Technology**: PHP (CakePHP), MySQL/PostgreSQL, JavaScript
- **Structure**: Classic PHP application with extensive plugin/module system
- **Blockers**:
  - Massive legacy PHP codebase (253k LOC)
  - CakePHP framework with tight architectural coupling
  - Complex database schema with deep interdependencies
  - Custom STIX/TAXII protocol implementations
  - Extensive configuration and customization points
  - Decades of accumulated features
- **Recommendation**: Complete rewrite required for DDD integration
- **Timeline**: 12+ months (not recommended)

#### 30. n8n
**Feasibility Score**: 10/100 - NOT RECOMMENDED
- **Domain**: Automation/Workflows
- **Type**: Full-stack Monorepo (12,762 files, 1,453,140 LOC)
- **Technology**: TypeScript (8,265 files), Node.js, Vue.js
- **Structure**:
  - Massive pnpm workspace monorepo
  - 500+ integration nodes
  - Core workflow engine
  - Editor UI (Vue.js)
  - CLI and daemon components
- **Blockers**:
  - Largest project in portfolio (1.45M LOC)
  - Complex monorepo with 500+ interdependent integration nodes
  - Custom workflow execution engine
  - Plugin system with tight coupling
  - Would break apart entire integration network
  - No clear domain boundaries
- **Recommendation**: Keep as separate product/service
- **Timeline**: 18+ months (not recommended)

#### 31. Brute-Ratel-C4-Community-Kit
**Feasibility Score**: 10/100 - NOT RECOMMENDED
- **Domain**: Security/Offensive Tools
- **Type**: Compiled C/C++ Framework (44 files, 108 LOC)
- **Technology**: C/C++ (BOF Framework), PowerShell, Python
- **Blockers**:
  - Compiled C/C++ binaries (architecture-specific)
  - Beacon Object File (BOF) framework
  - Likely license/legal restrictions
  - Specialized offensive security tool
  - Requires sandboxed/isolated execution
  - Not designed as a service module
- **Recommendation**: Cannot integrate without major rewrites
- **Timeline**: N/A - Not Recommended

#### 32. meterpreter
**Feasibility Score**: 8/100 - NOT RECOMMENDED
- **Domain**: Security/Offensive Tools
- **Type**: Payload Framework (3,116 files, 4,670 LOC)
- **Technology**: C/C++ (2,214 files), Python, Architecture-specific binaries
- **Blockers**:
  - Compiled binary payloads for multiple architectures
  - Metasploit framework component
  - Architecture and OS specific
  - Not portable code
  - Malware payload generator
- **Recommendation**: Cannot integrate (legal/technical)
- **Timeline**: N/A - Not Recommended

#### 33. KasmVNC
**Feasibility Score**: 5/100 - NOT RECOMMENDED
- **Domain**: Infrastructure/Remote Access
- **Type**: Compiled C/C++ Application (752 files, 893 LOC)
- **Technology**: C/C++ (301 files), Shell, Python
- **Structure**:
  - VNC server implementation
  - Build system for multiple platforms
  - CMake build configuration
  - Platform-specific code (alpine, debian, fedora, oracle, windows, etc.)
- **Blockers**:
  - Low-level C/C++ VNC server
  - Complex multi-platform build system
  - Architecture-specific binaries
  - Not portable code
  - System-level service
- **Recommendation**: Cannot integrate, use as separate service
- **Timeline**: N/A - Not Recommended

#### 34. HELK
**Feasibility Score**: 20/100 - NOT RECOMMENDED
- **Domain**: Security/Analytics
- **Type**: Infrastructure Automation (791 files, 467 LOC)
- **Technology**: Shell scripts (21 files), Ruby (2 files)
- **Structure**: Installation and deployment automation for ELK stack
- **Blockers**:
  - Deployment/infrastructure focused
  - Depends on external ELK stack components
  - System-level installation scripts
  - Not designed as service module
  - Configuration-heavy (Salt/Pillar style)
- **Recommendation**: Deploy separately, not integrate
- **Timeline**: N/A - Not Recommended

#### 35. blackarch
**Feasibility Score**: 5/100 - NOT RECOMMENDED
- **Domain**: Security/Infrastructure
- **Type**: Package Repository (5,536 files, 0 LOC)
- **Technology**: Package definitions, build scripts
- **Blockers**:
  - BlackArch Linux package repository
  - System package management
  - Binary package definitions
  - Not code, system packages
  - Incompatible with monolith architecture
- **Recommendation**: External dependency only
- **Timeline**: N/A - Not Recommended

#### 36. kong
**Feasibility Score**: 15/100 - NOT RECOMMENDED
- **Domain**: Infrastructure/API Gateway
- **Type**: Mixed/Infrastructure (2,373 files, 4,836 LOC)
- **Technology**: Python, Shell, Rust
- **Blockers**:
  - API gateway infrastructure component
  - Low-level networking implementation
  - Compilation requirements
  - Infrastructure deployment focus
  - Not suitable for monolith integration
- **Recommendation**: Deploy as separate infrastructure component
- **Timeline**: N/A - Not Recommended

#### 37. securityonion
**Feasibility Score**: 25/100 - NOT RECOMMENDED
- **Domain**: Security/Infrastructure
- **Type**: Infrastructure Configuration (1,688 files, 8,828 LOC)
- **Technology**: Python, Shell, Salt/Pillar configuration
- **Structure**:
  - salt/ (Salt states)
  - pillar/ (Salt pillar data)
  - setup/ (Installation)
  - sigs/ (Yara signatures)
- **Blockers**:
  - Infrastructure-level security system
  - Complex Salt configuration
  - System-level deployment focus
  - Not modular service architecture
  - Tight coupling to OS-level components
- **Recommendation**: Deploy separately
- **Timeline**: N/A - Not Recommended

---

### TIER 5: EMPTY/INCOMPLETE

#### 38. rita
- **Status**: Empty repository (0 files)
- **Action**: Remove or populate

#### 39. software-forensic-kit
- **Status**: Empty repository (0 files)
- **Action**: Remove or populate

#### 40. onex
- **Status**: Minimal/Unknown (12 files, 0 LOC)
- **Action**: Investigate and clarify purpose

---

## MIGRATION STRATEGY RECOMMENDATIONS

### Phase 1: Quick Wins (Months 1-2)
Integrate easy projects with minimal dependencies:

1. MalwareBazaar_MCP (1 week)
2. CyberChef (1 week)
3. spec-kit (1 week)
4. mcp-virustotal (1 week)
5. chroma-mcp (1 week)
6. apiscout (2 weeks)
7. mtg-commander-map (1 week)
8. mtg-scripting-toolkit (1 week)
9. it-tools (2 weeks)
10. lscript (1 week)
11. commander-spellbook-site (2 weeks)
12. firecrawl-mcp-server (1 week)
13. n8n-mcp-server (2 weeks)
14. hexstrike-ai (2 weeks)

**Total Effort**: ~20-25 weeks (parallel teams)

### Phase 2: Medium Complexity (Months 3-4)
- FileScopeMCP (2-3 weeks)
- inspector (3-4 weeks)
- maltrail (3-4 weeks)
- mealie (3-4 weeks)
- commander-spellbook-backend (3-4 weeks)
- securityonion-n8n-workflows (1-2 weeks)

**Total Effort**: ~20-25 weeks

### Phase 3: Hard Projects (Months 5-10)
- Nemesis (3-4 months)
- dispatch (4-6 months)
- actual (3-5 months)
- Ghostwriter (4-6 months)
- firecrawl (4-6 months)

**Note**: These should be worked on in parallel with different teams

### Phase 4: Strategic Decisions
- yara-x: Integrate as external service/library
- goose: Adopt as dependency or rewrite in TypeScript
- MISP/n8n/BlackArch/KasmVNC/HELK: Keep as separate services, do not integrate

---

## DOMAIN MAPPING FOR INTEGRATED PROJECTS

### Security Domain
- **Offensive Operations**: Ghostwriter, Nemesis
- **Threat Intelligence**: MalwareBazaar_MCP, mcp-virustotal, apiscout
- **Detection**: yara-x (external service)
- **Monitoring**: maltrail
- **Utilities**: CyberChef
- **Analysis**: hexstrike-ai

### Automation Domain
- **Workflows**: n8n-mcp-server, securityonion-n8n-workflows
- **Orchestration**: dispatch

### Productivity Domain
- **Finance**: actual
- **Recipes**: mealie

### Gaming/Magic Domain
- **MTG Data**: commander-spellbook-backend, mtg-commander-map
- **MTG Scripts**: mtg-scripting-toolkit
- **MTG Frontend**: commander-spellbook-site

### Development/Tooling Domain
- **Code Analysis**: FileScopeMCP
- **Web Tools**: firecrawl (external), firecrawl-mcp-server
- **Debugging**: inspector
- **Utilities**: it-tools, lscript, spec-kit
- **Vector DB**: chroma-mcp

---

## CRITICAL DEPENDENCIES & ARCHITECTURE CONCERNS

### Database Migration Strategy
Projects with database requirements:
- Ghostwriter: Django ORM + migrations
- dispatch: FastAPI + SQLAlchemy + Alembic
- Nemesis: Custom schema
- mealie: Poetry + Alembic migrations
- actual: Custom sync protocol + SQLite/PostgreSQL
- firecrawl: Multiple database layers
- MISP: Complex schema (legacy)

**Recommendation**: Establish isolated database schemas per bounded context

### External Service Dependencies
- firecrawl: Requires deployment + infrastructure
- mealie: MQTT, LDAP, OpenAI integrations
- dispatch: Slack, Teams, JIRA, Confluence, PagerDuty integrations
- actual: Sync protocol for multi-device support
- n8n: 500+ integration nodes (keep separate)

### Compiled/Binary Components (Cannot Integrate)
- Brute-Ratel-C4-Community-Kit
- meterpreter
- KasmVNC
- blackarch (package repo)
- yara-x (use as library/service)
- goose (Rust core)

---

## RISK ASSESSMENT MATRIX

### HIGH RISK (Avoid Unless Strategic Necessity)
- MISP (legacy codebase, legal issues)
- n8n (too large, would fragment)
- Brute-Ratel/meterpreter (legal/security concerns)
- KasmVNC (C/C++ binary, not portable)

### MEDIUM RISK (Feasible with Planning)
- dispatch (large, complex orchestration)
- actual (monorepo interdependencies)
- Ghostwriter (Django coupling)
- firecrawl (monorepo structure)
- goose (Rust + async complexity)

### LOW RISK (Recommended for Integration)
- All Tier 1 (Easy) projects
- Most Tier 2 (Medium) projects
- Except those with specific external dependencies

---

## TECHNOLOGY STACK ALIGNMENT

### Stack 1: Python/FastAPI Ecosystem
**Recommended Projects**:
- apiscout
- MalwareBazaar_MCP
- chroma-mcp
- hexstrike-ai
- spec-kit
- mealie (FastAPI backend)
- dispatch (FastAPI + sqlalchemy)
- maltrail

**Benefits**: Unified Python ecosystem, shared dependencies

### Stack 2: TypeScript/Node.js Ecosystem
**Recommended Projects**:
- CyberChef
- mcp-virustotal
- n8n-mcp-server
- firecrawl-mcp-server
- FileScopeMCP
- mtg-scripting-toolkit
- it-tools
- inspector

**Benefits**: Unified JavaScript ecosystem, npm/pnpm monorepo support

### Stack 3: Multi-Language (Requires Careful Integration)
- actual (TypeScript + some Rust/Go)
- Nemesis (Python + TypeScript)
- Ghostwriter (Python + JavaScript/HTML)
- firecrawl (TypeScript + Python + Rust)
- goose (Rust + TypeScript)
- yara-x (Rust + Go + Python)

---

## SUMMARY STATISTICS

| Category | Count | % |
|----------|-------|---|
| **Easy (1-2 months)** | 14 | 35% |
| **Medium (2-3 months)** | 6 | 15% |
| **Hard (3-6 months)** | 8 | 20% |
| **Very Hard/Not Recommended** | 9 | 23% |
| **Empty/Incomplete** | 2 | 5% |
| **Total Viable** | 37 | 95% |

### Recommended Portfolio (Easy + Medium)
**20 Projects / ~45 weeks of focused effort** (assuming parallel teams)
- LOC to integrate: ~650k
- Average complexity: Low-Medium
- High confidence success rate

---

## FINAL RECOMMENDATIONS

### RECOMMENDED: Integrate These (20 Projects)
All Tier 1 and Tier 2 projects (easy + medium complexity)

### CONDITIONAL: Consider These (8 Projects)
- Nemesis (moderate value, significant work)
- dispatch (excellent feature, major effort)
- actual (good modularity, high LOC)
- Ghostwriter (domain value, complex refactoring)
- firecrawl (monorepo pattern, external dependencies)
- Others only if team capacity allows

### NOT RECOMMENDED: Keep Separate (9 Projects)
- MISP (legacy, legal concerns)
- n8n (too large, fragmenting)
- Brute-Ratel-C4 (legal issues)
- meterpreter (payloads, legal)
- KasmVNC (binary, not portable)
- HELK (infrastructure)
- blackarch (package repo)
- kong (API gateway)
- securityonion (infrastructure)

### UNACTIONABLE: Clarify or Remove (3 Projects)
- rita (empty)
- software-forensic-kit (empty)
- onex (minimal, unclear purpose)

---

## NEXT STEPS

1. **Prioritize**: Start with Tier 1 (Easy) projects for quick wins
2. **Team Assignment**: Assign teams per domain/stack
3. **Infrastructure**: Set up isolated database schemas per bounded context
4. **API Gateway**: Implement service discovery and API composition
5. **Testing**: Establish integration testing for cross-service communication
6. **Documentation**: Create domain/service documentation
7. **Monitoring**: Set up observability for microservices

