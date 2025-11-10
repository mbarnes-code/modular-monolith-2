---
description: "IT-Tools brownfield asset migration to DDD modular monolith"
parent_task: "../tasks.md#T111"
parent_phase: "Phase 3d: Productivity Domain Migrations"
return_to: "../tasks.md#T112"
domain: "productivity"
target_service: "apps/productivity-service/src/"
legacy_path: "features/it-tools"
estimated_hours: 30
---

# Tasks: [MIGRATION: IT-Tools - 80+ Developer Utilities]

**⬆️ PARENT TASK**: [`tasks.md#T111`](../tasks.md#T111)  
**⬇️ RETURN TO**: [`tasks.md#T112`](../tasks.md#T112)

---

## Handoff Context

**Called From**: `tasks.md` Phase 3d, Task T111  
**Entry Condition**: Productivity service foundation ready (Phase 1-2 complete), apps/productivity-service/ exists with base infrastructure  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark T111 complete in parent `tasks.md`, proceed to T112

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-2 marked complete in `tasks.md`
- [ ] `apps/productivity-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 2 working
- [ ] Test framework from Phase 2 operational
- [ ] Legacy environment setup: `features/it-tools/` accessible and operational
- [ ] Project analysis report completed and validated (`reports/it-tools-analysis.md`)
- [ ] Ground Truth testbed setup with legacy IT-Tools running for comparison validation
- [ ] React/TypeScript component library structure ready in `libs/shared/utilities/`

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

**Input (Spec)**: Analysis report from `/specs/003-brownfield-integration/modular-analysis-repo-main/reports/it-tools-analysis.md`  
**Input (Legacy)**: Legacy codebase path `/features/it-tools/` with 80+ developer utilities  
**Prerequisites**: it-tools-analysis.md (MANDATORY), parent Phase 1-2 complete, Ground Truth testbed operational

**IT-Tools Business Context**: 80+ client-side developer utilities built with Vue 3 + TypeScript, completely stateless with no backend requirements. Critical algorithms include fuzzy search (tool discovery), JSON formatting/validation, and copy-to-clipboard workflows. Migration target is React/TypeScript component library in productivity service.

**DDD Domain Boundaries**: IT-Tools maps to **Infrastructure Domain** within productivity service, containing:

- **Tool Discovery Subdomain**: Search, categorization, navigation (Analysis Section 4.1)
- **Data Transformation Subdomain**: Format converters, validators, generators (Analysis Section 4.1, 4.2)  
- **Developer Utilities Subdomain**: Crypto tools, network tools, text processors (Analysis Section 6.3)
- **UI Infrastructure Subdomain**: Copy-to-clipboard, validation, theming (Analysis Section 6.2)

**Tests**: Ground Truth tests MANDATORY for all critical algorithms. Legacy Vue app must remain operational during migration for validation comparison.

**Migration Strategy**: Category-based migration preserving exact functional behavior of each tool while converting Vue→React and integrating into unified productivity platform.

## Format: [ID] [P?] [Domain.Subdomain] [Analysis: Section.#] [Logic: <legacy_file::function>] Description

- [P]: Can run in parallel  
- [Domain.Subdomain]: DDD boundary (e.g., Infrastructure.ToolDiscovery, Infrastructure.DataTransformation)
- [Analysis]: Reference to it-tools-analysis.md section
- [Logic]: The exact legacy Vue component/function being migrated

## Path Conventions

- **New Components**: `apps/productivity-service/src/domains/infrastructure/tools/` (DDD structure)
- **Shared Utilities**: `libs/shared/utilities/` (framework-agnostic business logic)  
- **Legacy Source**: `features/it-tools/src/tools/` (80+ tool directories)
- **Analysis Report**: `reports/it-tools-analysis.md` sections for validation

## Migration Methodology: DDD Brownfield Asset Relocation

**Core Principle**: Preserve 100% functional parity while establishing proper domain boundaries and React integration.

**Validation Strategy**:

1. Ground Truth Tests → Legacy Vue tools remain operational for comparison
2. Analysis Cross-Reference → Validate against it-tools-analysis.md documented behavior  
3. Domain-by-Domain Migration → Migrate by DDD subdomain maintaining cohesion
4. Component Integration → Ensure React components match Vue behavior exactly
5. Performance Validation → Client-side processing maintains <10ms response times

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

## Phase 1: IT-Tools Analysis Validation & Legacy Environment Setup

**Purpose**: Validate IT-Tools analysis findings and establish Vue.js testbed for React migration validation.

- [ ] T001 [Analysis: Section.1] Validate IT-Tools analysis completeness: Confirm all CRITICAL sections filled in it-tools-analysis.md
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate Vue 3 + TypeScript + Vite stack against actual codebase in features/it-tools/
- [ ] T003 [P] [Analysis: Section.7.1] Test coverage baseline: Run existing Vitest and Playwright tests, document 60% coverage metrics
- [ ] T004 [Analysis: Section.8.1] Performance baseline: Measure and document current client-side processing times (<10ms for most tools)
- [ ] T005 [Ground Truth] Setup legacy Vue environment: Ensure features/it-tools/ runs independently with npm run dev for validation comparisons
- [ ] T006 [Ground Truth] Validate 80+ tools functionality: Test all tool categories (Crypto, Converter, Web, Images, Development, Network, Math, Measurement, Text, Data) 
- [ ] T007 [P] Create DDD structure: Initialize apps/productivity-service/src/domains/infrastructure/tools/ for domain-driven organization
- [ ] T008 [P] Initialize React component library: Setup libs/shared/utilities/ with TypeScript for framework-agnostic business logic

---

## Phase 2: Tool Discovery & Navigation Subdomain (Infrastructure.ToolDiscovery)

**Purpose**: Migrate tool discovery, search, and navigation based on Analysis Section 4.1 - Critical Algorithms.

- [ ] T009 [Infrastructure.ToolDiscovery] [Analysis: Section.4.1] [Logic: fuzzySearch.ts::useFuzzySearch] Migrate fuzzy search algorithm: Port Fuse.js-based tool search to React hook preserving <5ms performance
- [ ] T010 [Infrastructure.ToolDiscovery] [Analysis: Section.2.1] [Logic: tools.types.ts::Tool,ToolCategory] Port tool metadata models: Create TypeScript interfaces for tool definitions and categories
- [ ] T011 [P] [Infrastructure.ToolDiscovery] [Analysis: Section.6.3] [Logic: CollapsibleToolMenu.vue] Convert tool navigation: Port Vue menu component to React with identical categorization
- [ ] T012 [Infrastructure.ToolDiscovery] [Analysis: Section.6.3] [Logic: ToolCard.vue] Convert tool card components: Port Vue tool display cards to React maintaining visual parity
- [ ] T013 [Ground Truth] Search functionality tests: Write React tests validating search results match Vue implementation exactly
- [ ] T014 [Infrastructure.ToolDiscovery] Tool registry migration: Convert Vue-based tool registration to React dynamic imports in productivity service

**Checkpoint**: Tool discovery and navigation fully migrated with functional and visual parity.

## Phase 3: UI Infrastructure Subdomain (Infrastructure.UIInfrastructure)

**Purpose**: Migrate shared UI patterns and infrastructure based on Analysis Section 6.2 - Component Architecture.

- [ ] T015 [Infrastructure.UIInfrastructure] [Analysis: Section.4.1] [Logic: copy.ts::useCopy] Migrate copy-to-clipboard: Port unified copy composable to React hook with toast notifications
- [ ] T016 [Infrastructure.UIInfrastructure] [Analysis: Section.4.2] [Logic: validation.ts::useValidation] Port validation framework: Migrate real-time input validation to React with identical error display
- [ ] T017 [P] [Infrastructure.UIInfrastructure] [Analysis: Section.6.2] [Logic: TextareaCopyable.vue,InputCopyable.vue] Convert copyable components: Port Vue components to React maintaining copy button behavior
- [ ] T018 [Infrastructure.UIInfrastructure] [Analysis: Section.6.2] [Logic: tool.layout.vue] Migrate tool layout: Port consistent tool wrapper layout from Vue to React
- [ ] T019 [Infrastructure.UIInfrastructure] [Analysis: Section.6.1] Theme integration: Integrate dark/light theme switching with productivity service design system
- [ ] T020 [Infrastructure.UIInfrastructure] Error handling framework: Port Vue error boundaries to React error boundaries with user-friendly messages

**Checkpoint**: UI infrastructure ready supporting copy workflows, validation, and theming. No tool logic exists yet.

## Phase 4: Data Transformation Subdomain - JSON & Text Tools (Infrastructure.DataTransformation)

**Migration Goal**: Migrate JSON processing and text transformation tools (Analysis Section.4.1 - JSON algorithms)

**Analysis Reference**: Section.4.1 - Critical Algorithms (formatJson, sortObjectKeys), Section.11.1 - Developer Domain Knowledge

**Independent Test**: JSON formatting with nested objects, key sorting, and error handling validation

### Phase 4a: JSON Processing Tools Migration

- [ ] T021 [Infrastructure.DataTransformation] [Analysis: Section.4.1] [Logic: json.models.ts::formatJson] Port JSON formatter: Migrate exact algorithm preserving indentation, sorting, and JSON5 support
- [ ] T022 [Infrastructure.DataTransformation] [Analysis: Section.4.1] [Logic: json.models.ts::sortObjectKeys] Port recursive key sorting: Maintain exact sorting behavior for nested objects and arrays
- [ ] T023 [P] [Infrastructure.DataTransformation] [Analysis: Section.4.1] [Logic: json-viewer.vue] Ground Truth Test: Validate Vue JSON formatter output matches React implementation
- [ ] T024 [P] [Infrastructure.DataTransformation] [Logic: json-viewer.vue] Convert JSON viewer UI: Port Vue component to React maintaining settings (sort keys, indent size)
- [ ] T025 [Infrastructure.DataTransformation] [Analysis: Section.8.1] Performance validation: Ensure JSON processing maintains <10ms for 1MB documents

### Phase 4b: Text Processing Tools Migration  

- [ ] T026 [Infrastructure.DataTransformation] [Logic: case-converter/] Port case converter: Migrate camelCase, snake_case, kebab-case transformations preserving edge cases
- [ ] T027 [Infrastructure.DataTransformation] [Logic: text-diff/] Port text diff tool: Migrate diff algorithm maintaining visual diff display and performance
- [ ] T028 [Infrastructure.DataTransformation] [Logic: text-statistics/] Migrate text statistics: Port word count, character count, reading time calculations
- [ ] T029 [Infrastructure.DataTransformation] [Logic: slugify-string/] Port URL slugify: Migrate string-to-URL slug conversion with special character handling
- [ ] T030 [Infrastructure.DataTransformation] [Logic: text-to-binary/,text-to-unicode/] Port text encoding: Migrate binary, Unicode, NATO alphabet conversions
- [ ] T031 [Infrastructure.DataTransformation] Integration validation: Test all text tools against Vue originals for functional parity

**Checkpoint**: JSON and text processing tools migrated maintaining exact algorithmic behavior and performance.

## Phase 5: Developer Utilities Subdomain - Crypto & Network Tools (Infrastructure.DeveloperUtilities)  

**Migration Goal**: Migrate crypto, network, and security tools (Analysis Section.11.1 - Developer Domain)

**Analysis Reference**: Section.6.3 - Tool Pattern Architecture, Section.9.1 - Client-side Security

**Independent Test**: Crypto operations, network utilities, and UUID generation validation

### Phase 5a: Crypto & Hashing Tools Migration

- [ ] T032 [Infrastructure.DeveloperUtilities] [Logic: bcrypt/] Port bcrypt tool: Migrate password hashing with salt generation preserving security parameters  
- [ ] T033 [Infrastructure.DeveloperUtilities] [Logic: hash-text/] Port hashing utilities: Migrate MD5, SHA family, HMAC generation maintaining algorithm accuracy
- [ ] T034 [P] [Infrastructure.DeveloperUtilities] [Logic: hmac-generator/] Port HMAC generator: Migrate keyed-hash message authentication preserving key handling
- [ ] T035 [P] [Infrastructure.DeveloperUtilities] [Logic: rsa-key-pair-generator/] Port RSA key generation: Migrate public/private key pair creation with format options

### Phase 5b: Network & Identity Tools Migration

- [ ] T036 [Infrastructure.DeveloperUtilities] [Logic: uuid-generator/] Port UUID generator: Migrate v1, v3, v4, v5 UUID generation maintaining uniqueness guarantees
- [ ] T037 [Infrastructure.DeveloperUtilities] [Logic: ipv4-subnet-calculator/,ipv4-address-converter/] Port IPv4 tools: Migrate subnet calculations and address conversions
- [ ] T038 [Infrastructure.DeveloperUtilities] [Logic: ipv6-ula-generator/] Port IPv6 utilities: Migrate IPv6 address generation and validation
- [ ] T039 [Infrastructure.DeveloperUtilities] [Logic: mac-address-generator/,mac-address-lookup/] Port MAC address tools: Migrate generation and vendor lookup
- [ ] T040 [Infrastructure.DeveloperUtilities] [Logic: jwt-parser/] Port JWT parser: Migrate JSON Web Token decoding and validation 
- [ ] T041 [Infrastructure.DeveloperUtilities] Security validation: Test all crypto tools against Vue originals ensuring identical outputs

**Checkpoint**: All crypto, network, and identity tools migrated with cryptographic accuracy preserved.

## Phase 6: Converter & Generator Tools Migration (Infrastructure.DataTransformation Extended)

**Migration Goal**: Migrate remaining format converters and generators (Analysis Section.11.1 - Tool Categories)

**Analysis Reference**: Section.6.3 - Input/Output Tool Pattern, Section.8.1 - Performance Baselines

### Phase 6a: Format Conversion Tools Migration

- [ ] T042 [Infrastructure.DataTransformation] [Logic: base64-string-converter/,base64-file-converter/] Port Base64 tools: Migrate string/file Base64 encoding/decoding with error handling
- [ ] T043 [Infrastructure.DataTransformation] [Logic: json-to-csv/,json-to-xml/,json-to-yaml-converter/] Port JSON converters: Migrate multi-format output maintaining data fidelity
- [ ] T044 [P] [Infrastructure.DataTransformation] [Logic: yaml-to-json-converter/,toml-to-json/,xml-to-json/] Port format-to-JSON: Migrate YAML, TOML, XML parsing to JSON
- [ ] T045 [P] [Infrastructure.DataTransformation] [Logic: url-encoder/,html-entities/] Port encoding tools: Migrate URL encoding and HTML entity conversion

### Phase 6b: Generator & Utility Tools Migration

- [ ] T046 [Infrastructure.DataTransformation] [Logic: qr-code-generator/,wifi-qr-code-generator/] Port QR generators: Migrate QR code creation with customization options
- [ ] T047 [Infrastructure.DataTransformation] [Logic: lorem-ipsum-generator/,password-strength-analyser/] Port text generators: Migrate placeholder text and password analysis
- [ ] T048 [Infrastructure.DataTransformation] [Logic: crontab-generator/,meta-tag-generator/] Port specialized generators: Migrate cron expression and HTML meta tag tools
- [ ] T049 [Infrastructure.DataTransformation] [Logic: color-converter/,temperature-converter/] Port unit converters: Migrate color space and temperature conversions
- [ ] T050 [Infrastructure.DataTransformation] Performance validation: Ensure all converters maintain client-side processing performance baselines

## Phase 7: Remaining Specialized Tools Migration (Infrastructure.DeveloperUtilities Extended)

**Migration Goal**: Complete migration of specialized development and utility tools

**Analysis Reference**: Section.8.1 - Performance Baselines, Section.7.1 - Test Coverage, Section.11.2 - Edge Cases

### Phase 7a: Development & Code Tools Migration

- [ ] T051 [Infrastructure.DeveloperUtilities] [Logic: regex-tester/,regex-memo/] Port regex tools: Migrate regular expression testing and reference maintaining pattern validation
- [ ] T052 [Infrastructure.DeveloperUtilities] [Logic: sql-prettify/,html-wysiwyg-editor/] Port code formatting: Migrate SQL formatter and HTML editor preserving syntax highlighting
- [ ] T053 [P] [Infrastructure.DeveloperUtilities] [Logic: docker-run-to-docker-compose-converter/] Port Docker converter: Migrate command-to-compose conversion logic
- [ ] T054 [P] [Infrastructure.DeveloperUtilities] [Logic: markdown-to-html/,xml-formatter/] Port markup tools: Migrate markdown rendering and XML formatting

### Phase 7b: System & Math Tools Migration  

- [ ] T055 [Infrastructure.DeveloperUtilities] [Logic: chmod-calculator/,device-information/] Port system tools: Migrate file permissions calculator and device info display
- [ ] T056 [Infrastructure.DeveloperUtilities] [Logic: math-evaluator/,percentage-calculator/] Port math tools: Migrate expression evaluator and percentage calculator
- [ ] T057 [Infrastructure.DeveloperUtilities] [Logic: date-time-converter/,chronometer/] Port time tools: Migrate date/time utilities and stopwatch functionality
- [ ] T058 [Infrastructure.DeveloperUtilities] [Logic: keycode-info/,user-agent-parser/] Port info tools: Migrate keyboard code reference and user agent parsing
- [ ] T059 [Infrastructure.DeveloperUtilities] Complete tool inventory: Verify all 80+ tools migrated with functional validation against Vue originals

## Phase 8: Integration & Performance Validation

**Migration Goal**: Complete React integration and validate performance parity per Analysis Section.8

**Analysis Reference**: Section.8.1 - Performance Baselines, Section.11.3 - User Behavior Patterns

- [ ] T060 [Infrastructure.Integration] Productivity service integration: Wire all IT-Tools into apps/productivity-service/ with unified navigation
- [ ] T061 [Infrastructure.Integration] [Analysis: Section.8.1] Performance benchmarking: Validate all tools maintain client-side processing <10ms baseline
- [ ] T062 [Infrastructure.Integration] [Analysis: Section.11.3] User workflow validation: Test common user workflows (search→tool→copy) maintain identical UX
- [ ] T063 [P] [Infrastructure.Integration] Mobile responsiveness: Ensure React components maintain mobile compatibility from Vue originals
- [ ] T064 [Infrastructure.Integration] [Analysis: Section.11.2] Edge case preservation: Validate all documented quirks and workarounds function identically
- [ ] T065 [Infrastructure.Integration] [Analysis: Section.7.1] Test coverage validation: Achieve 60%+ coverage matching Vue baseline with React implementation

## Phase 9: Documentation & Polish

- [ ] T066 [Infrastructure.Documentation] API documentation: Document all migrated IT-Tools React components for productivity service integration
- [ ] T067 [Infrastructure.Documentation] [Analysis: Section.11.1] Developer guide: Create tool creation guide for extending IT-Tools in React ecosystem
- [ ] T068 [P] [Infrastructure.Documentation] Migration validation: Document functional parity verification between Vue and React implementations
- [ ] T069 [Infrastructure.Documentation] Performance documentation: Document client-side processing benchmarks and optimization guidelines

## Phase 10: Migration Validation & Legacy Asset Retirement

**Purpose**: Comprehensive validation before Vue legacy asset removal from features/it-tools/.

### Phase 10a: Complete Migration Validation

- [ ] T070 [Analysis: All Sections] Full analysis cross-reference: Verify all it-tools-analysis.md findings addressed in React implementation
- [ ] T071 [Analysis: Section.4.1] Algorithm parity validation: Confirm all critical algorithms (fuzzy search, JSON formatting, copy workflows) function identically
- [ ] T072 [Analysis: Section.8.1] Performance regression testing: Validate React tools maintain Vue baseline performance (<10ms processing, <200ms UI response)
- [ ] T073 [Analysis: Section.12.3] Success criteria verification: Confirm all 80+ tools migrated with 100% functional parity
- [ ] T074 Verify Full Migration: Confirm all [Logic: ...] tags have corresponding passing validation tests comparing React vs Vue outputs
- [ ] T075 Run Full Regression Suite: Execute complete test suite including ground truth comparisons across all tool categories

### Phase 10b: Safe Asset Retirement

- [ ] T076 [Analysis: Section.12.2] Risk mitigation: Address all identified Vue→React migration risks (bundle size, mobile compatibility, performance)
- [ ] T077 Legacy asset backup: Create secure archive of features/it-tools/ Vue codebase before deletion
- [ ] T078 Production validation: Run React IT-Tools in productivity service production-like environment
- [ ] T079 Stakeholder approval: Obtain sign-off from productivity service team and IT-Tools stakeholders
- [ ] T080 Delete Legacy Asset: After 100% validation, remove features/it-tools/ directory

### Phase 10c: Post-Migration Monitoring  

- [ ] T081 [Analysis: Section.10.2] Monitoring validation: Confirm React components integrate with productivity service monitoring
- [ ] T082 [Analysis: Section.8.1] Performance monitoring: Track React tool performance against Vue baselines in production
- [ ] T083 [Analysis: Section.11.3] User behavior monitoring: Validate developer workflows maintain efficiency with React integration

### Dependencies & Execution Order

**Sequential Dependencies (Must Complete In Order):**

- **Phase 1 (Analysis Validation & Legacy Setup)**: Must complete first - validates Vue testbed and analysis findings
- **Phase 2 (Tool Discovery Subdomain)**: Must complete before tool migration - establishes search and navigation infrastructure
- **Phase 3 (UI Infrastructure Subdomain)**: Must complete before tool migration - establishes copy, validation, and theming patterns

**Parallel Execution Phases:**

- **Phases 4-7 (Domain Tool Migrations)**: Can proceed in parallel by tool category after Phase 3 infrastructure complete
  - Phase 4: JSON & Text Tools (Data Transformation core)
  - Phase 5: Crypto & Network Tools (Developer Utilities core) 
  - Phase 6: Converter & Generator Tools (Data Transformation extended)
  - Phase 7: Specialized Tools (Developer Utilities extended)
- **Phase 8 (Integration & Performance)**: After all tool migrations complete - validates unified behavior
- **Phases 9-10 (Documentation & Retirement)**: Final phases - document and retire Vue assets

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

**Verify these conditions before marking T111 complete in parent tasks.md**:

- [ ] All tasks T001-T083 marked complete above
- [ ] Integration tests pass: `pytest tests/productivity/test_it_tools_integration.py`
- [ ] All 80+ tools functional parity validated: React outputs match Vue originals exactly
- [ ] Performance baselines met: Client-side processing <10ms, UI interactions <200ms (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm functional parity: Vue testbed comparisons pass
- [ ] Legacy `features/it-tools/` backed up to `features/it-tools-archive/`
- [ ] IT-Tools migration completion documented in `migration-validation.md`
- [ ] All analysis findings from `it-tools-analysis.md` addressed
- [ ] React components integrated into `apps/productivity-service/src/domains/infrastructure/tools/`
- [ ] Tool discovery and search functionality maintains Vue performance baselines
- [ ] Copy-to-clipboard workflows function identically across all tools
- [ ] Mobile compatibility preserved from Vue implementation
- [ ] No regressions in productivity service functionality

**⚠️ If any checklist item fails**: DO NOT mark T111 complete. Fix issues and re-validate.

**Completion Action**:

1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/productivity/test_it_tools_integration.py`
3. Document completion in `migration-validation.md`
4. Return to `tasks.md` and mark T111 complete
5. Proceed to T112 (next task in parent task list)

**Documentation Update Required**:

```markdown
# In migration-validation.md

### IT-Tools Migration (T111)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: 30
- **Actual Hours**: [ACTUAL]
- **Tools Migrated**: 80+ developer utilities
- **Tests**: All passed, 0 failed
- **Performance**: All client-side processing <10ms baselines met
- **DDD Integration**: React components successfully integrated into Infrastructure domain
- **Notes**: Vue→React migration with 100% functional parity achieved
```

