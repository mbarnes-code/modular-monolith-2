# Generic Asset Relocation Task Template

**Purpose**: Universal task template for relocating any of the 37 executive function tools from features/ directory to unified modular monolith structure, leveraging completed analysis documentation.

**Usage Instructions**: 
1. Replace `[TOOL-NAME]` with actual tool name (e.g., MISP, n8n, CyberChef)
2. Replace `[DOMAIN]` with target domain (security, productivity, mtg, infrastructure)
3. Reference the tool's analysis file: `docs/modular-analysis-repo-main/reports/[tool-name]-analysis.md`

## Universal Asset Relocation Pattern (6-Step Process)

### Step 1: Analysis Review & Business Logic Preservation Planning
- [ ] T0XX-1 Review `docs/modular-analysis-repo-main/reports/[TOOL-NAME]-analysis.md` Section 4 (Business Logic) and Section 11 (Domain Knowledge) to identify critical algorithms, validation rules, and workflows that MUST be preserved without modification
- [ ] T0XX-1a Identify Category A (Complex Algorithms >5,000 lines) from Section 4.1 requiring microservice preservation 
- [ ] T0XX-1b Identify Category B (Domain Logic 1,000-5,000 lines) from Section 4.2-4.3 for modular monolith integration
- [ ] T0XX-1c Identify Category C (Utilities <1,000 lines) from remaining business logic for shared library integration
- [ ] T0XX-1d **Configuration Assets**: Review Section 6/10 for config files, environment variables, initialization scripts, and bootstrapping code that must be preserved
- [ ] T0XX-1e **Multi-Language Components**: Identify secondary language components (Python libs, Node.js tools, shell scripts) requiring separate migration paths
- [ ] T0XX-1f **Infrastructure Dependencies**: Catalog external service dependencies, database engines, message queues, and system-level requirements
- [ ] T0XX-1g **Plugin & Extension Systems**: Identify dynamic loading mechanisms, plugin registries, operation catalogs, and extensibility frameworks requiring preservation
- [ ] T0XX-1h **Multi-Build Architectures**: Document specialized build targets (web, mobile, desktop, server), dual-mode exports, and platform-specific entry points
- [ ] T0XX-1i **Performance-Critical Systems**: Catalog worker threads, background processing, caching layers, and performance-optimized components requiring specialized migration
- [ ] T0XX-1j **Development Toolchains**: Identify code generators, scaffolding tools, custom build workflows, and developer experience utilities
- [ ] T0XX-1k **Monorepo Architecture**: Document workspace configurations, package interdependencies, build orchestration systems (Turbo, Nx, Lerna), and shared dependency management requiring coordinated migration
- [ ] T0XX-1l Document preservation strategy based on analysis findings and create migration plan

### Step 2: Data Architecture Migration
- [ ] T0XX-2 Extract data models from `features/[TOOL-NAME]/` per Section 2 (Data Architecture) of analysis, migrating database schemas to unified PostgreSQL while preserving relationships, validation rules, and performance patterns identified in Section 2.1-2.3
- [ ] T0XX-2a Migrate critical data models from Section 2.1 maintaining field types, business rules, and relationships
- [ ] T0XX-2b Preserve database performance patterns from Section 2.3 (indexes, query optimizations, caching strategies)
- [ ] T0XX-2c **Schema Artifacts**: Migrate database initialization scripts, stored procedures, triggers, and custom data types
- [ ] T0XX-2d **Data Seeding**: Preserve initial data, reference data, and configuration data migration scripts
- [ ] T0XX-2e Update data model imports and references throughout codebase

### Step 3: API Integration & Endpoint Preservation

- [ ] T0XX-3 Migrate API architecture from `features/[TOOL-NAME]/` per Section 3 (API Architecture) of analysis, converting endpoints to FastAPI while preserving authentication patterns, request/response schemas, and business logic identified in Section 3.1-3.3
- [ ] T0XX-3a Convert API endpoints from Section 3.2 to FastAPI maintaining identical request/response behavior
- [ ] T0XX-3b Integrate authentication/authorization patterns from Section 3.1 with unified JWT system
- [ ] T0XX-3c Preserve external API integrations from Section 5.1 maintaining error handling and fallback behavior
- [ ] T0XX-3d **Middleware & Plugins**: Migrate custom middleware, request interceptors, and API extensions
- [ ] T0XX-3e **Plugin Registration Systems**: Preserve operation registries, dynamic endpoint discovery, and extensible API architectures
- [ ] T0XX-3f **Multi-Target API Compatibility**: Maintain dual-mode APIs (web/node), platform-specific endpoints, and cross-environment compatibility
- [ ] T0XX-3g **API Documentation**: Preserve OpenAPI/Swagger specs, API versioning, and developer documentation


### Step 4: Frontend Component Integration

- [ ] T0XX-4 Migrate frontend components from `features/[TOOL-NAME]/` per Section 6 (Frontend Architecture) of analysis to React/Next.js unified interface, preserving component architecture, state management patterns, and critical user interactions identified in Section 6.1-6.4
- [ ] T0XX-4a Convert critical frontend components from Section 6.3 to React maintaining functionality and user experience
- [ ] T0XX-4b Integrate state management patterns from Section 6.1 with unified application state
- [ ] T0XX-4c Preserve complex user interactions and performance optimizations from Section 6.2-6.4
- [ ] T0XX-4d **Static Assets**: Migrate CSS files, images, fonts, icons, and other static resources
- [ ] T0XX-4e **Client Libraries**: Preserve custom JavaScript libraries, web workers, and browser-specific code
- [ ] T0XX-4f **Worker Thread Systems**: Migrate web workers, service workers, background processing, and threading architectures for performance-critical operations
- [ ] T0XX-4g **Interactive UI Systems**: Preserve drag-and-drop interfaces, real-time editors, canvas/WebGL components, and specialized user interaction patterns
- [ ] T0XX-4h **Templates & Views**: Convert template engines (Jinja2, Handlebars, etc.) to React components

### Step 5: Service Adapter Creation & Dependency Resolution

- [ ] T0XX-5 Create service adapter in `libs/service-adapters/[DOMAIN]/[TOOL-NAME]_adapter.py` based on analysis Section 1.2 (Technology Stack), resolving all dependencies, import paths, and external integrations while maintaining 100% API compatibility for downstream consumers
- [ ] T0XX-5a Resolve technology stack dependencies from Section 1.2 integrating with unified monolith stack
- [ ] T0XX-5b Handle external integrations from Section 5 (External Integrations) maintaining service contracts
- [ ] T0XX-5c Create unified configuration management integrating tool-specific configs from Section 10.1
- [ ] T0XX-5d **Package Dependencies**: Migrate package.json/requirements.txt dependencies, resolve version conflicts
- [ ] T0XX-5e **Build Assets**: Preserve build scripts, compilation steps, and deployment artifacts
- [ ] T0XX-5f **Runtime Dependencies**: Handle system packages, external binaries, and service dependencies
- [ ] T0XX-5g **Custom Libraries**: Migrate internal libraries, utilities, and shared components to libs/shared/
- [ ] T0XX-5h **Multi-Target Build Systems**: Preserve specialized build configurations, platform-specific builds, and export compatibility layers
- [ ] T0XX-5i **Development Tooling Integration**: Migrate code generators, scaffolding systems, and custom development workflow tools to unified toolchain
- [ ] T0XX-5j **Package Patch Management**: Preserve custom patches to third-party libraries, patch-package configurations, and modified external dependencies

### Step 6: Testing, Validation & Cleanup

- [ ] T0XX-6 Implement comprehensive testing strategy based on analysis Section 7 (Testing & Quality), validate functionality preservation through automated tests comparing original vs integrated behavior, achieve performance baselines from Section 8, and remove tool from `features/[TOOL-NAME]/` only after 100% validation success
- [ ] T0XX-6a Implement test coverage matching Section 7.1-7.2 requirements maintaining critical test cases
- [ ] T0XX-6b Validate performance baselines from Section 8.1 meet or exceed original tool performance
- [ ] T0XX-6c Execute migration readiness criteria from Section 12.3 ensuring all success criteria met
- [ ] T0XX-6d **Integration Testing**: Validate cross-service communication, data flow, and API contracts
- [ ] T0XX-6e **Plugin System Testing**: Validate dynamic loading, operation registration, extensibility frameworks, and plugin compatibility
- [ ] T0XX-6f **Multi-Target Testing**: Verify functionality across all build targets (web, node, mobile, desktop) and platform-specific features
- [ ] T0XX-6g **Performance-Critical Testing**: Validate worker thread performance, background processing, and optimization-dependent functionality
- [ ] T0XX-6h **Monorepo Integration Testing**: Validate package interdependencies, workspace build orchestration, and cross-package functionality
- [ ] T0XX-6i **Security Testing**: Preserve security controls, authentication flows, and access patterns
- [ ] T0XX-6j **Documentation Migration**: Update README files, API docs, deployment guides, and user manuals
- [ ] T0XX-6k **Cleanup Validation**: Verify no orphaned files, unused dependencies, or broken references remain
- [ ] T0XX-6l Remove `features/[TOOL-NAME]/` directory only after all validation passes

## Domain-Specific Application Examples

### Security Domain Asset Relocation (13 Tools)
**Target Location**: `apps/jane-orchestrator/src/domains/security/[TOOL-NAME]/`
**Performance Requirement**: <1s response time per FR-020

- Replace `[TOOL-NAME]` with: MISP, HELK, SecurityOnion, YARA-X, Maltrail, CyberChef, Nemesis, Ghostwriter, Brute-Ratel-C4, APIScout, RITA, OneX, BlackArch
- Replace `[DOMAIN]` with: security

### Productivity Domain Asset Relocation (8 Tools)  
**Target Location**: `apps/jane-orchestrator/src/domains/productivity/[TOOL-NAME]/`
**Performance Requirement**: <2s response time per FR-021

- Replace `[TOOL-NAME]` with: Actual, Mealie, Dispatch, n8n, IT-Tools, Firecrawl, Goose, Inspector
- Replace `[DOMAIN]` with: productivity

### MTG Domain Asset Relocation (4 Tools)
**Target Location**: `apps/jane-orchestrator/src/domains/mtg/[TOOL-NAME]/`
**Performance Requirement**: <3s response time per FR-022

- Replace `[TOOL-NAME]` with: Commander-Spellbook, MTG-Commander-Map, MTG-Scripting-Toolkit, [Card-Analysis-Tool]
- Replace `[DOMAIN]` with: mtg

### Infrastructure Domain Asset Relocation (12 Tools)
**Target Location**: `apps/jane-orchestrator/src/domains/infrastructure/[TOOL-NAME]/`  
**Performance Requirement**: <5s response time per FR-023

- Replace `[TOOL-NAME]` with: Kong, KasmVNC, LScript, Chroma-MCP, FileScopeMCP, Firecrawl-MCP, MalwareBazaar-MCP, MCP-VirusTotal, n8n-MCP, SecurityOnion-n8n-Workflows, Brute-Ratel-C4-Kit, Ghostwriter
- Replace `[DOMAIN]` with: infrastructure

## Analysis Section Reference Guide

**Section 1**: Project Identity & Context - Use for technology stack and project structure understanding  
**Section 2**: Data Architecture - Critical for database migration and data model preservation  
**Section 3**: API Architecture - Essential for endpoint migration and authentication integration  
**Section 4**: Business Logic - MUST PRESERVE algorithms, validation rules, and workflows  
**Section 5**: External Integrations - Maintain all third-party service connections  
**Section 6**: Frontend Architecture - Component migration and state management  
**Section 7**: Testing & Quality - Maintain test coverage and critical test cases  
**Section 8**: Performance Characteristics - Meet or exceed baseline performance  
**Section 9**: Security & Compliance - Preserve security measures and compliance requirements  
**Section 10**: Deployment & Operations - Configuration and monitoring integration  
**Section 11**: Domain Knowledge - Critical tribal knowledge and business rules  
**Section 12**: Migration Readiness - Success criteria and risk assessment
