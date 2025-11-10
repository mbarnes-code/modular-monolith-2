---
description: "DDD-based migration: Commander Spellbook Site frontend to unified Jane UI"
parent_task: "../tasks.md#T114"
parent_phase: "Phase 8: TCG Migrations"
return_to: "../tasks.md#T115"
domain: "tcg"
target_service: "apps/jane-ui/src/"
legacy_path: "features/commander-spellbook-site"
estimated_hours: 42
---

# Tasks: [MIGRATION: Commander Spellbook Site]

**⬆️ PARENT TASK**: [`tasks.md#T114`](../tasks.md#T114)  
**⬇️ RETURN TO**: [`tasks.md#T115`](../tasks.md#T115)

---

## Handoff Context

**Called From**: `tasks.md` Phase 8, Task T114  
**Entry Condition**: TCG service foundation ready (Phase 1-4 complete), Commander Spellbook Backend migrated (T113)  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark T114 complete in parent `tasks.md`, proceed to T115

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/jane-ui/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/commander-spellbook-site/` accessible
- [ ] Project analysis report completed and validated

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

**Input (Spec)**: Design documents from `/specs/003-brownfield-integration/` 
**Input (Legacy)**: Legacy codebase path `/features/commander-spellbook-site/` 
**Prerequisites**: plan.md (required), spec.md (required), **commander-spellbook-analysis.md (MANDATORY)**, migration-strategy.md

**Project Analysis Integration**: This task references commander-spellbook-analysis.md sections:
- Section 6 (Frontend Architecture) - Next.js/React component migration to unified Jane UI
- Section 3 (API Architecture) - API service layer integration with jane-orchestrator  
- Section 11 (Domain Knowledge) - MTG business rules and UI/UX patterns preservation
- Section 8 (Performance Characteristics) - <3s TCG domain response requirements
- Section 5 (External Integrations) - Scryfall API, Discord OAuth integration

**Tests**: Ground Truth testing is MANDATORY - Next.js app must be running for component validation.

**Organization**: Tasks organized by DDD bounded contexts within TCG domain, following modular monolith patterns.

## Format: [ID] [P?] [Domain Context] [Analysis: Section.#] [Logic: <component_file::component>] Description

- [P]: Can run in parallel
- [Domain Context]: TCG bounded context (F1: Search, F2: Combo Display, F3: User Management)  
- [Analysis]: Reference to commander-spellbook-analysis.md section
- [Logic]: The exact React component/service being migrated

## Path Conventions

- **Target UI**: `apps/jane-ui/src/domains/tcg/` (TCG domain within unified UI)
- **Legacy Frontend**: `features/commander-spellbook-site/src/`
- **Analysis Reference**: `commander-spellbook-analysis.md` sections for UI/UX validation
- **Shared Components**: `libs/ui/` for cross-domain reusable components

## Migration Methodology: Frontend DDD Integration

**Core Principle**: Integrate Next.js frontend components into unified Jane UI while preserving MTG user experience.

**Validation Strategy:**

1. **Component Ground Truth** → Capture current behavior via Cypress tests
2. **Domain Boundary Analysis** → Identify TCG-specific vs shared UI components  
3. **Incremental Integration** → Migrate components by bounded context
4. **API Integration** → Connect to unified jane-orchestrator backend
5. **Performance Validation** → Maintain <3s TCG domain response requirements

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

## Phase 1: Analysis Validation & Frontend Architecture Assessment

**Purpose**: Validate Commander Spellbook Site analysis and establish frontend migration baseline.

- [ ] T001 [Analysis: Section.6.1] Validate Next.js architecture: Confirm Pages Router, SSG/SSR patterns match analysis findings
- [ ] T002 [Analysis: Section.6.2] Component architecture review: Validate feature-based organization and design system findings  
- [ ] T003 [P] [Analysis: Section.7.1] Frontend test coverage baseline: Run Cypress tests and document current E2E coverage
- [ ] T004 [Analysis: Section.8.1] Frontend performance baseline: Measure FCP, LCP, CLS for combo pages per analysis
- [ ] T005 [Ground Truth] Setup Commander Spellbook Site: Run Next.js dev server and validate all routes functional
- [ ] T006 [Ground Truth] Validate MTG user workflows: Test search, combo display, submissions end-to-end
- [ ] T007 [P] Initialize TCG domain structure: Create `apps/jane-ui/src/domains/tcg/` directory structure
- [ ] T008 [P] Setup shared UI components: Initialize `libs/ui/mtg/` for MTG-specific reusable components

---

## Phase 2: API Service Layer Integration

**Purpose**: Integrate frontend API services with unified jane-orchestrator backend.

- [ ] T009 [Analysis: Section.3.2] API endpoints inventory: Document all frontend API calls to commander-spellbook backend
- [ ] T010 [Analysis: Section.3.2] Create TCG API service: Implement `apps/jane-ui/src/domains/tcg/services/tcg-api.service.ts`
- [ ] T011 [P] [Analysis: Section.3.1] [Logic: src/services/api.service.ts::apiConfiguration] Migrate API configuration: Port authentication and base URL configuration
- [ ] T012 [Analysis: Section.5.1] External integrations: Preserve Scryfall API integration patterns in unified service layer
- [ ] T013 [Ground Truth] API service tests: Create tests validating API service parity with legacy @space-cow-media/spellbook-client
- [ ] T014 [Analysis: Section.3.3] Error handling patterns: Implement DRF-compatible error handling in jane-orchestrator integration

**Checkpoint**: API service layer provides identical functionality to legacy spellbook-client.

## Phase 3: Shared UI Component Migration

**Purpose**: Migrate reusable UI components to shared library for cross-domain use.

- [ ] T015 [Analysis: Section.6.2] [Logic: src/components/layout/TextWithMagicSymbol/::TextWithMagicSymbol] MTG Symbol Parser: Migrate to `libs/ui/mtg/TextWithMagicSymbol/`
- [ ] T016 [Analysis: Section.6.2] [Logic: src/components/ui/::ThemeSelector] Theme Management: Migrate theme selector to `libs/ui/theme/`
- [ ] T017 [P] [Analysis: Section.6.3] [Logic: src/components/SearchBar/::SearchBar] Search Components: Extract search patterns to `libs/ui/search/`
- [ ] T018 [Analysis: Section.11.1] MTG Design Tokens: Create design system tokens for WUBRG colors, mana symbols, card layouts
- [ ] T019 [Analysis: Section.6.2] Layout Components: Migrate header, footer, navigation to `libs/ui/layout/`
- [ ] T020 Component Documentation: Create Storybook stories for all migrated shared components

**Checkpoint**: Shared UI library contains reusable MTG and general components.

## Phase 4: Search Domain Components Migration 🎯 CORE

**Migration Goal**: Migrate combo search functionality - the primary user workflow (60% of traffic per analysis)

**Analysis Reference**: Section.6.3 - SearchBar Component, Section.11.3 - User Behavior Patterns

**Independent Test**: Combo search with filters returns expected results in <3s

### Phase 4a: Search Interface Components

- [ ] T021 [Analysis: Section.6.3] [Logic: src/components/SearchBar/SearchBar.tsx::SearchBar] Search Bar Migration: Port to `apps/jane-ui/src/domains/tcg/components/SearchBar/`
- [ ] T022 [Analysis: Section.11.1] MTG Search Grammar: Preserve color identity, mana cost, legality search syntax
- [ ] T023 [P] [F1: Search] [Analysis: Section.6.3] [Logic: src/components/advancedSearch/::AdvancedSearchForm] Advanced Search: Migrate form components with MTG-specific filters
- [ ] T024 [P] [F1: Search] [Analysis: Section.6.3] [Logic: src/pages/search.tsx::SearchPage] Search Results: Port search results page with pagination and sorting
- [ ] T025 [Analysis: Section.8.1] Search Performance: Document current search response times for baseline

### Phase 4b: Search Integration & Validation  

- [ ] T026 [F1: Search] [Analysis: Section.11.3] Search Behavior: Implement user workflow patterns (card name → filter → browse)
- [ ] T027 [F1: Search] [Analysis: Section.3.2] API Integration: Connect search components to unified TCG API service
- [ ] T028 [F1: Search] [Analysis: Section.11.2] Search Quirks: Implement EDHREC integration and search result ranking
- [ ] T029 [F1: Search] [Analysis: Section.6.4] Routing: Setup Next.js routing for search pages in jane-ui
- [ ] T030 [F1: Search] [Analysis: Section.8.1] Performance Validation: Ensure search results load <1.5s per TCG domain requirements
- [ ] T031 [F1: Search] [Ground Truth] End-to-End Search: Validate complete search workflow matches legacy behavior

**Checkpoint**: Search functionality provides identical user experience with improved performance.

## Phase 5: Combo Display Domain Migration

**Migration Goal**: Migrate combo detail pages and variant display - core content presentation

**Analysis Reference**: Section.6.3 - Variant Display Components, Section.11.1 - MTG Domain Knowledge

**Independent Test**: Combo page displays complete variant information with MTG symbols and pricing

### Phase 5a: Combo Display Components

- [ ] T032 [Analysis: Section.6.3] [Logic: src/components/combo/ComboList/ComboList.tsx::ComboList] Combo Instructions: Migrate step-by-step combo display with MTG symbol parsing
- [ ] T033 [Analysis: Section.6.3] [Logic: src/components/combo/::VariantDisplay] Variant Cards: Port card list display with quantity, mana cost, color identity
- [ ] T034 [P] [F2: Display] [Logic: src/pages/combo/[id].tsx::ComboDetailPage] Combo Detail Page: Migrate dynamic combo page with SSG/ISR
- [ ] T035 [P] [F2: Display] [Analysis: Section.11.1] MTG Formatting: Preserve mana symbol rendering, color identity calculation

### Phase 5b: Content Integration & Performance

- [ ] T036 [F2: Display] [Analysis: Section.6.4] Dynamic Routing: Setup combo/[id] routes in unified jane-ui structure
- [ ] T037 [F2: Display] [Analysis: Section.5.1] Scryfall Integration: Connect card images and data to unified external services
- [ ] T038 [F2: Display] [Analysis: Section.8.1] Page Performance: Implement ISR with 3600s revalidation for combo pages
- [ ] T039 [F2: Display] [Ground Truth] Combo Display: Validate all MTG-specific formatting and data display matches legacy

**Checkpoint**: Combo pages display identical information with maintained performance characteristics.

## Phase 6: User Management & Authentication Migration

**Migration Goal**: Integrate Discord OAuth and user submission workflows

**Analysis Reference**: Section.5.2 - Discord OAuth, Section.3.1 - JWT Authentication

### Phase 6a: Authentication Integration

- [ ] T040 [Analysis: Section.5.2] [Logic: src/services/token.service.ts::tokenService] Token Management: Migrate JWT token service to unified authentication
- [ ] T041 [Analysis: Section.5.2] Discord OAuth Flow: Integrate Discord authentication with jane-orchestrator auth system
- [ ] T042 [P] [Analysis: Section.3.1] [Logic: src/components/layout/UserDropdown/::UserDropdown] User Interface: Port user dropdown and profile management
- [ ] T043 [Analysis: Section.9.1] Session Management: Implement secure session handling with 5-minute access tokens

### Phase 6b: User Workflows & Submissions

- [ ] T044 [Analysis: Section.11.3] [Logic: src/pages/submit-a-combo.tsx::SubmitComboPage] Combo Submission: Migrate combo submission form and workflow
- [ ] T045 [Analysis: Section.11.3] [Logic: src/pages/my-submissions/::UserSubmissionsPage] User Dashboard: Port user submission management interface
- [ ] T046 [Analysis: Section.3.1] Authorization Guards: Implement editor permissions for combo review workflows

## Phase 7: Specialized Tools & Features Migration

**Migration Goal**: Migrate specialized MTG tools like "Find My Combos" and random combo features

**Analysis Reference**: Section.11.3 - User Workflows, Section.4.1 - Find My Combos Algorithm

### Phase 7a: Find My Combos Feature

- [ ] T047 [Analysis: Section.4.1] [Logic: src/pages/find-my-combos.tsx::FindMyCombosPage] Find My Combos: Port deck analysis tool to TCG domain
- [ ] T048 [Analysis: Section.11.3] Deck Import Logic: Migrate commander color identity validation and deck parsing
- [ ] T049 [Analysis: Section.8.1] Combo Matching: Ensure <2s response time for deck analysis queries

### Phase 7b: Additional MTG Features

- [ ] T050 [Analysis: Section.6.3] [Logic: src/components/RandomButton/::RandomButton] Random Combo: Migrate random combo discovery feature
- [ ] T051 [Analysis: Section.11.1] [Logic: src/pages/syntax-guide.tsx::SyntaxGuidePage] Search Syntax: Port MTG search syntax documentation
- [ ] T052 [P] [Analysis: Section.6.1] Static Pages: Migrate about, privacy policy, style guide pages with SSG

## Phase 8: Testing & Quality Assurance

**Migration Goal**: Comprehensive E2E testing and performance validation for TCG domain

**Analysis Reference**: Section.7.1 - Cypress Tests, Section.8.1 - Performance Baselines

### Phase 8a: Test Migration & Enhancement

- [ ] T053 [Analysis: Section.7.1] [Logic: cypress/e2e/::CypressTests] E2E Test Migration: Port Cypress tests to unified jane-ui structure
- [ ] T054 [Analysis: Section.7.2] MTG-Specific Testing: Create tests for mana symbol parsing, color identity, combo validation
- [ ] T055 [Analysis: Section.8.1] Performance Testing: Implement automated testing for <3s TCG domain requirements

### Phase 8b: Integration Validation

- [ ] T056 [Analysis: Section.11.3] User Workflow Validation: Test complete user journeys (search → view → submit)
- [ ] T057 [P] [Analysis: Section.11.2] Edge Case Testing: Validate all documented MTG rules quirks and workarounds
- [ ] T058 Cross-Domain Testing: Ensure TCG domain integrates properly with security, productivity domains

## Phase 9: Production Optimization & Polish

**Migration Goal**: Production-ready TCG domain with optimized performance and monitoring

### Phase 9a: Performance Optimization

- [ ] T059 [Analysis: Section.8.1] Bundle Optimization: Implement code splitting for TCG domain components
- [ ] T060 [Analysis: Section.8.1] Image Optimization: Setup Scryfall image caching and Next.js Image optimization
- [ ] T061 [Analysis: Section.6.1] SSG/ISR Optimization: Optimize static generation for frequently accessed combo pages

### Phase 9b: Production Polish  

- [ ] T062 [Analysis: Section.10.2] Monitoring Integration: Add TCG domain metrics to unified monitoring system
- [ ] T063 [Analysis: Section.9.2] Security Validation: Final security review for Discord OAuth and user submissions
- [ ] T064 [P] Code cleanup and documentation: TypeScript strict mode compliance, component documentation
- [ ] T065 [Analysis: Section.13.1] Migration documentation: Update architecture docs reflecting TCG domain integration

## Phase 10: Migration Validation & Legacy Asset Retirement

**Purpose**: Final validation and safe removal of Commander Spellbook Site legacy assets.

### Phase 10a: Complete Migration Validation

- [ ] T066 [Analysis: All Sections] Full analysis cross-reference: Verify all commander-spellbook-analysis.md findings addressed in TCG domain
- [ ] T067 [Analysis: Section.6.1] Frontend parity validation: Confirm all Next.js pages and components function identically in jane-ui
- [ ] T068 [Analysis: Section.8.1] Performance regression testing: Validate TCG domain meets <3s response requirements
- [ ] T069 [Analysis: Section.12.3] Success criteria verification: Confirm 100% functional parity with 50K+ user base support
- [ ] T070 Verify Complete Migration: Confirm all [Logic: ...] component migrations have passing validation tests
- [ ] T071 Run Full E2E Regression Suite: Execute complete Cypress test suite against unified jane-ui

### Phase 10b: Safe Asset Retirement

- [ ] T072 [Analysis: Section.12.2] Risk mitigation: Address MTG community user experience risks during transition
- [ ] T073 Legacy asset backup: Archive `features/commander-spellbook-site/` before deletion with git tag
- [ ] T074 Production validation: Deploy TCG domain to staging environment and validate with test users
- [ ] T075 Community communication: Notify MTG community of migration completion and new URLs
- [ ] T076 Delete Legacy Asset: After 100% validation and community notification, remove legacy directory

### Phase 10c: Post-Migration Monitoring

- [ ] T077 [Analysis: Section.10.2] TCG domain monitoring: Confirm unified monitoring captures MTG-specific metrics
- [ ] T078 [Analysis: Section.8.1] Performance monitoring: Track combo search, display performance against baselines
- [ ] T079 [Analysis: Section.11.3] User behavior tracking: Monitor search patterns, combo submissions, community engagement

### Dependencies & Execution Order

**Sequential Dependencies (Must Complete In Order):**

- **Phase 1 (Frontend Architecture Assessment)**: Must complete first - validates analysis and establishes baseline
- **Phase 2 (API Service Layer)**: Must complete before component migration - establishes backend connectivity  
- **Phase 3 (Shared UI Components)**: Must complete before domain components - establishes reusable component library

**Parallel Execution Phases:**

- **Phases 4-6 (Domain Components)**: Can proceed in parallel by feature after Phase 3 (Search, Display, User Management)
- **Phase 7 (Specialized Tools)**: Can run in parallel with Phases 4-6 after shared components ready
- **Phase 8 (Testing & QA)**: Can run incrementally with each feature phase completion

**Final Sequential Dependencies:**

- **Phase 9 (Production Optimization)**: After all feature phases complete
- **Phase 10 (Migration Validation)**: Must be final phase before asset retirement
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

1. **Analysis validation** (Phase 1) - Frontend architect validates Next.js patterns and performance baselines
2. **API integration** (Phase 2) - Connect to jane-orchestrator backend services  
3. **Shared components** (Phase 3) - Establish reusable MTG UI component library

**Parallel Domain Migration** (After Foundation):

- **Frontend Developer A**: Search Domain (Phases 4) - Core user workflows
- **Frontend Developer B**: Display Domain (Phase 5) - Combo presentation  
- **Frontend Developer C**: User Management (Phase 6) - Authentication flows
- **Frontend Developer D**: Testing & Performance (Phase 8) - Validation

**Validation Requirements**:

- Each React component must render identically to legacy versions
- Performance must meet <3s TCG domain requirements  
- All MTG domain knowledge (mana symbols, color identity) preserved

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

- [ ] All tasks T001-TXXX marked complete above
- [ ] Integration tests pass: `pytest tests/mtg/test_commander_spellbook_site_integration.py`
- [ ] Performance baselines met (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm functional parity with legacy
- [ ] Legacy `features/commander-spellbook-site/` backed up to `archive/`
- [ ] Migration completion documented in `migration-validation.md`
- [ ] All analysis findings from project_analysis_report.md addressed
- [ ] No regressions in existing functionality
- [ ] Security audit passed (if applicable)
- [ ] Accessibility compliance maintained (WCAG 2.1 AA)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:

1. Mark all checkboxes T001-T079 complete ✅
2. Run validation command: `npm run test:integration` (TCG domain Cypress tests)
3. Document completion in `migration-validation.md`
4. Mark parent task T114 complete in `tasks.md`
5. Proceed to T115 in `tasks.md`

**Documentation Update Required**:

```markdown
# In migration-validation.md

### Commander Spellbook Site Migration (T114)
- **Status**: ✅ Complete  
- **Completed**: [DATE]
- **Estimated Hours**: 42
- **Actual Hours**: [ACTUAL]
- **Tests**: Cypress E2E tests passed
- **Performance**: <3s TCG domain requirements met
- **Components Migrated**: 15+ React components to jane-ui/domains/tcg/
- **Notes**: MTG community workflows preserved, Discord OAuth integrated
```

