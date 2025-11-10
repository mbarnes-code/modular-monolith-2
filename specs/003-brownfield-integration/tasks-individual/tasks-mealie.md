---
description: "DDD-based modular monolith asset migration for Mealie recipe management system"
parent_task: "../tasks.md#T112"
parent_phase: "Phase 3c2: Productivity Domain Migrations"
return_to: "../tasks.md#T113"
domain: "productivity"
target_service: "apps/productivity-service/src/"
legacy_path: "features/mealie"
estimated_hours: 40
ddd_domains: ["recipe", "scraper", "user-management", "meal-planning", "parser"]
---

# Tasks: [MIGRATION: Mealie - Recipe Management & Meal Planning System]

**⬆️ PARENT TASK**: [`tasks.md#T112`](../tasks.md#T112)  
**⬇️ RETURN TO**: [`tasks.md#T113`](../tasks.md#T113)

---

## Handoff Context

**Called From**: `tasks.md` Phase 3c2, Task T112  
**Entry Condition**: Productivity service foundation ready (Phase 1-2 complete)  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark T112 complete in parent `tasks.md`, proceed to T113

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-2 marked complete in `tasks.md`
- [ ] `apps/productivity-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/mealie/` accessible and functional
- [ ] Project analysis report: `reports/mealie-analysis.md` completed and validated

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## Migration Context

**Input (Spec)**: `reports/mealie-analysis.md` (MANDATORY analysis reference)  
**Input (Legacy)**: `features/mealie/` - FastAPI backend + Nuxt.js frontend recipe management system  
**Prerequisites**: Phase 1-2 infrastructure, productivity service foundation

**Project Analysis Integration**: This migration MUST reference specific sections from `mealie-analysis.md`:

- Section 2 (Data Architecture) - Recipe/Group/User models with critical relationships
- Section 3 (API Architecture) - FastAPI endpoints with JWT authentication 
- Section 4 (Business Logic) - Recipe scraping, ingredient parsing, meal planning algorithms
- Section 5 (External Integrations) - recipe-scrapers library, OpenAI API integration
- Section 8 (Performance Characteristics) - Response time baselines for scraping operations

**DDD Domain Boundaries Identified**:

1. **Recipe Domain** - Recipe CRUD, categorization, rating, asset management
2. **Scraper Domain** - URL parsing, website scraping, data extraction algorithms  
3. **User Management Domain** - Groups, users, authentication, multi-tenancy
4. **Meal Planning Domain** - Meal plans, shopping lists, nutrition tracking
5. **Parser Domain** - Ingredient parsing, quantity/unit extraction, food matching

**Critical Algorithms to Preserve** (Category A):

- Recipe URL Scraper (`mealie/services/scraper/scraper_strategies.py`) - 400 LOC, Very Complex
- Ingredient Parser (`mealie/services/parser_services/ingredient_parser.py`) - 200 LOC, Complex  
- Meal Planning Generator (`mealie/services/meal_plan/meal_plan_service.py`) - 300 LOC, Medium

**Architecture Pattern**: FastAPI backend → Unified backend integration, Nuxt.js frontend → React component integration

## Migration Methodology: DDD Brownfield Asset Relocation

**Core Principle**: Preserve 100% functional parity while establishing clear domain boundaries for modular monolith architecture.

**DDD Strategy**: 

1. **Domain Identification** → Map existing services to bounded contexts
2. **Domain Model Preservation** → Maintain exact entity relationships and business rules
3. **Domain Service Migration** → Preserve complex algorithms within domain boundaries  
4. **Anti-Corruption Layer** → Create adapters for external integrations
5. **Domain Event Integration** → Enable cross-domain communication via events

**Validation Strategy**: 

1. Ground Truth Tests → Establish current behavior baseline for each domain
2. Analysis Cross-Reference → Validate against documented behavior per `mealie-analysis.md`
3. Domain-by-Domain Migration → Port one bounded context at a time with validation
4. Integration Testing → Ensure cross-domain workflows function correctly
5. Performance Validation → Maintain scraping and API response baselines

---

## Phase 1: Analysis Validation & Legacy Environment Setup

**Purpose**: Validate project analysis findings and establish baseline testing environment with domain validation.

- [ ] T001 [Analysis: Section.1] Validate project analysis completeness: Confirm all CRITICAL sections filled in `mealie-analysis.md`
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate FastAPI + Nuxt.js + SQLAlchemy stack against actual codebase
- [ ] T003 [P] [Analysis: Section.7.1] Test coverage baseline: Run existing test suite `tests/unit_tests/` and document coverage metrics (85%+ per analysis)
- [ ] T004 [Analysis: Section.8.1] Performance baseline: Measure scraping performance (3-8s typical, 15s max) and API response times (50-200ms)
- [ ] T005 [Ground Truth] Setup legacy test environment: Create isolated Docker environment for Mealie per `docker/docker-compose.dev.yml`
- [ ] T006 [Ground Truth] Validate legacy functionality: Run legacy system and confirm all critical workflows (recipe import, meal planning, user auth)
- [ ] T007 [P] Create productivity service domain structure: Setup `apps/productivity-service/src/domains/{recipe,scraper,user_mgmt,meal_planning,parser}/`
- [ ] T008 [P] Initialize target framework dependencies: Setup FastAPI integration in productivity service per analysis Section.1.2

**Phase 1 Checkpoint**: Legacy environment operational, domain structure established, baselines documented.

---

## Phase 2: Data Architecture Migration (Domain Model Foundation)

**Purpose**: Migrate data models and establish domain boundaries based on DDD analysis of Section 2.

### Phase 2a: Core Domain Models (Recipe & User Management Domains)

- [ ] T009 [Analysis: Section.2.1] **[Recipe Domain]** Recipe model migration: Port Recipe entity with all relationships per analysis
  - **Logic**: `features/mealie/mealie/db/models/recipe/recipe.py::Recipe`
  - **Target**: `apps/productivity-service/src/domains/recipe/models/recipe.py`
  - **Preserve**: Auto-slug generation, group-based filtering, asset relationships

- [ ] T010 [Analysis: Section.2.1] **[Recipe Domain]** RecipeIngredient model migration: Port ingredient relationships with parsing metadata
  - **Logic**: `features/mealie/mealie/db/models/recipe/ingredient.py::RecipeIngredient`  
  - **Target**: `apps/productivity-service/src/domains/recipe/models/ingredient.py`
  - **Preserve**: Food reference linking, quantity/unit validation, original text preservation

- [ ] T011 [Analysis: Section.2.1] **[User Management Domain]** Group model migration: Port multi-tenancy foundation
  - **Logic**: `features/mealie/mealie/db/models/group/__init__.py::Group`
  - **Target**: `apps/productivity-service/src/domains/user_mgmt/models/group.py`
  - **Preserve**: Slug uniqueness constraints, recipe isolation, user membership

- [ ] T012 [Analysis: Section.2.1] **[User Management Domain]** User model migration: Port authentication and group relationships
  - **Logic**: `features/mealie/mealie/db/models/users/user.py::User`
  - **Target**: `apps/productivity-service/src/domains/user_mgmt/models/user.py`
  - **Preserve**: Password hashing, email validation, admin privileges, group membership

### Phase 2b: Extended Domain Models (Meal Planning Domain)

- [ ] T013 [P] [Analysis: Section.2.2] **[Meal Planning Domain]** MealPlan model migration: Port scheduling and recipe relationships
  - **Logic**: `features/mealie/mealie/db/models/group/mealplan.py`
  - **Target**: `apps/productivity-service/src/domains/meal_planning/models/meal_plan.py`
  - **Preserve**: Date ranges, recipe scheduling, group isolation, nutrition aggregation

- [ ] T014 [P] [Analysis: Section.2.2] **[Meal Planning Domain]** ShoppingList model migration: Port ingredient aggregation logic
  - **Logic**: `features/mealie/mealie/db/models/group/shopping_list.py`  
  - **Target**: `apps/productivity-service/src/domains/meal_planning/models/shopping_list.py`
  - **Preserve**: Multi-recipe aggregation, ingredient consolidation, completion tracking

### Phase 2c: Database Schema & Relationships Validation

- [ ] T015 [Analysis: Section.2.2] Database schema migration: Create Alembic migrations preserving all relationships from Section.2.2
  - **Preserve**: Group(1)→Recipe(many), Recipe(1)→Ingredient(many), User(1)→Group(many), critical path integrity
- [ ] T016 [Analysis: Section.2.3] Database performance patterns: Implement indexes and query optimizations per analysis
  - **Preserve**: Recipe search indexing, group-based filtering, ingredient lookup performance
- [ ] T017 [Ground Truth] Data validation tests: Write tests confirming entity relationships and business rules
- [ ] T018 [Analysis: Section.2.1] Data migration scripts: Create scripts for existing recipe/user data preservation with group isolation

**Phase 2 Checkpoint**: All domain models migrated with relationships preserved, database schema operational.

---

## Phase 3: Domain Service Foundations & Authentication

**Purpose**: Establish domain service infrastructure and preserve authentication patterns.

### Phase 3a: Authentication & Authorization (User Management Domain)

- [ ] T019 [Analysis: Section.3.1] **[User Management Domain]** JWT authentication preservation: Port exact auth patterns from Section.3.1
  - **Logic**: `features/mealie/mealie/routes/auth/`
  - **Target**: `apps/productivity-service/src/domains/user_mgmt/services/auth_service.py`
  - **Preserve**: JWT token generation, refresh logic, group-based access control

- [ ] T020 [Analysis: Section.9.1] **[User Management Domain]** Group-based authorization: Implement multi-tenant access control per analysis
  - **Logic**: `features/mealie/mealie/core/security/`
  - **Target**: `apps/productivity-service/src/domains/user_mgmt/services/authorization_service.py`
  - **Preserve**: Recipe isolation by group, admin privilege escalation, user permission inheritance

### Phase 3b: Domain Service Infrastructure 

- [ ] T021 [P] [Analysis: Section.3.2] **[Recipe Domain]** Recipe service foundation: Setup CRUD operations with business rule enforcement
  - **Target**: `apps/productivity-service/src/domains/recipe/services/recipe_service.py`
  - **Preserve**: Group filtering, slug generation, asset management, category/tag relationships

- [ ] T022 [Analysis: Section.8.1] Performance monitoring: Implement baseline monitoring per Section.8.1 for domain operations
- [ ] T023 [Analysis: Section.7.1] Domain testing framework: Setup domain-specific test infrastructure matching current patterns
- [ ] T024 Configure domain event infrastructure: Setup event bus for cross-domain communication and state synchronization

**Phase 3 Checkpoint**: Domain services operational with authentication, no complex algorithms yet.

## Phase 4: Critical Business Logic Migration - Recipe Scraper Domain 🎯

**Migration Goal**: Preserve recipe URL scraping algorithms - core value proposition per Analysis Section.4.1

**Analysis Reference**: Section.4.1 - Recipe URL Scraper Algorithm (Very Complex, 400 LOC, MUST PRESERVE)

**Independent Test**: Import recipe from allrecipes.com URL and verify structured data extraction matches original

### Phase 4a: Scraper Domain Ground Truth & Algorithm Analysis

- [ ] T025 [Analysis: Section.4.1] **[Scraper Domain]** Scraper algorithm analysis: Review critical algorithm documentation from analysis
  - **Focus**: JSON-LD parsing → microdata → recipe-scrapers → OpenAI fallback → heuristic parsing strategy chain
- [ ] T026 [Analysis: Section.11.1] **[Scraper Domain]** Domain knowledge review: Document web scraping business rules and anti-detection patterns
- [ ] T027 [P] **[Scraper Domain]** [Analysis: Section.4.1] **[Logic: scraper_strategies.py::scrape_url]** Ground Truth Test: Prove original scraping behavior with real websites
  - **Test Cases**: JSON-LD site, microdata site, recipe-scrapers supported site, fallback heuristic site
  - **Baseline**: 3-8s typical, 15s max, 85%+ success rate on common cooking sites
- [ ] T028 [P] **[Scraper Domain]** [Analysis: Section.4.1] **[Logic: scraper_strategies.py::scrape_url]** Validation Test: Create target test for new domain service (initially failing)

### Phase 4b: Scraper Algorithm Preservation & Domain Implementation

- [ ] T029 **[Scraper Domain]** [Analysis: Section.4.1] **[Logic: scraper_strategies.py::scrape_url]** Core scraping algorithm preservation:
  - **Source**: `features/mealie/mealie/services/scraper/scraper_strategies.py`
  - **Target**: `apps/productivity-service/src/domains/scraper/services/recipe_scraper_service.py`
  - **Preserve**: 5-strategy parsing chain, timeout protection, user agent rotation, confidence scoring
  - **Complexity**: Very Complex - maintain exact algorithm flow and edge case handling

- [ ] T030 **[Scraper Domain]** [Analysis: Section.4.1] **[Logic: scraper_strategies.py]** Parser strategy chain preservation:
  - **Source**: `features/mealie/mealie/services/scraper/`  
  - **Target**: `apps/productivity-service/src/domains/scraper/strategies/`
  - **Preserve**: JSON-LD extractor, microdata parser, recipe-scrapers integration, OpenAI fallback, heuristic parser
  - **Dependencies**: `recipe-scrapers`, `extruct`, `BeautifulSoup`, OpenAI API integration

- [ ] T031 **[Scraper Domain]** [Analysis: Section.4.1] **[Logic: scraper_strategies.py::scrape_url]** Validation execution: Run new test against ported logic - MUST pass Ground Truth baseline
- [ ] T032 **[Scraper Domain]** [Analysis: Section.11.2] Edge case handling: Implement documented anti-detection and error recovery patterns
- [ ] T033 **[Scraper Domain]** [Analysis: Section.3.2] API integration: Wire proven scraper domain into FastAPI endpoint structure
- [ ] T034 **[Scraper Domain]** [Analysis: Section.8.1] Performance validation: Confirm scraping maintains 3-8s typical, 15s max baseline
- [ ] T035 **[Scraper Domain]** Integration test: End-to-end recipe import workflow with real website sources

**Phase 4 Checkpoint**: Recipe scraping domain migrated with documented functional and performance parity.

## Phase 5: Ingredient Parsing Domain Migration 🧠

**Migration Goal**: Preserve ingredient text parsing algorithms per Analysis Section.4.1 

**Analysis Reference**: Section.4.1 - Ingredient Parser Algorithm (Complex, 200 LOC, MUST PRESERVE)

**Independent Test**: Parse "2 1/2 cups all-purpose flour, sifted" and verify structured extraction matches original

### Phase 5a: Parser Domain Analysis & Ground Truth

- [ ] T036 [Analysis: Section.4.1] **[Parser Domain]** Ingredient parser algorithm analysis: Review natural language parsing documentation
  - **Focus**: Quantity extraction (fractions), unit matching (fuzzy), food identification, preparation notes
- [ ] T037 [Analysis: Section.11.1] **[Parser Domain]** Parser domain knowledge: Document ingredient parsing business rules and edge cases  
- [ ] T038 [P] **[Parser Domain]** [Analysis: Section.4.1] **[Logic: ingredient_parser.py::parse_ingredient]** Ground Truth Test: Prove original parsing behavior
  - **Test Cases**: Fractions (1/2, 1 1/2), measurements (cups, tbsp), foods (flour, butter), preparations (sifted, chopped)
  - **Baseline**: 90%+ accuracy on common ingredient formats per analysis
- [ ] T039 [P] **[Parser Domain]** [Analysis: Section.4.1] **[Logic: ingredient_parser.py::parse_ingredient]** Validation Test: Create target parser test

### Phase 5b: Parser Algorithm Migration

- [ ] T040 **[Parser Domain]** [Analysis: Section.4.1] **[Logic: ingredient_parser.py::parse_ingredient]** Ingredient parsing algorithm preservation:
  - **Source**: `features/mealie/mealie/services/parser_services/ingredient_parser.py`
  - **Target**: `apps/productivity-service/src/domains/parser/services/ingredient_parser_service.py`
  - **Preserve**: Regex quantity extraction, fuzzy unit matching, food item identification, confidence scoring
  - **Dependencies**: `fractions` library, fuzzy string matching, existing foods/units database

- [ ] T041 **[Parser Domain]** [Analysis: Section.4.1] **[Logic: ingredient_parser.py]** Parser validation: Run validation test - MUST pass Ground Truth accuracy baseline
- [ ] T042 **[Parser Domain]** [Analysis: Section.11.2] Parser edge cases: Implement fraction handling, unicode normalization, measurement conversions  
- [ ] T043 **[Parser Domain]** Parser domain integration: Wire ingredient parsing into recipe creation workflow
- [ ] T044 **[Parser Domain]** Parser performance validation: Ensure parsing maintains sub-100ms performance per ingredient

**Phase 5 Checkpoint**: Ingredient parsing domain migrated with accuracy and performance parity.

## Phase 6: Cross-Domain Integration & Migration Validation

**Migration Goal**: Complete domain integration with comprehensive validation before legacy asset removal.

### Phase 6a: Domain Integration & Event Communication

- [ ] T045 **[Cross-Domain]** Recipe creation events: Implement events for recipe parsing completion, scraping success/failure
- [ ] T046 **[Cross-Domain]** Cross-domain workflow validation: Test recipe import → parsing → storage workflow
- [ ] T047 **[Integration]** Frontend component integration: Convert key Vue.js components to React for unified dashboard
- [ ] T048 **[Performance]** End-to-end performance validation: Validate all domains meet baseline requirements

### Phase 6b: Complete Migration Validation

- [ ] T049 [Analysis: All Sections] **[All Domains]** Full analysis cross-reference: Verify all analysis findings addressed across domains
- [ ] T050 [Analysis: Section.4.1] **[Critical Algorithms]** Algorithm parity validation: Confirm scraper and parser algorithms function identically  
- [ ] T051 [Analysis: Section.8.1] **[Performance]** Performance regression testing: Validate all domains meet baseline performance requirements
- [ ] T052 **[Ground Truth]** Verify Full Domain Migration: Confirm all [Logic: ...] tags have corresponding passing validation tests
- [ ] T053 **[Integration]** Run Full Domain Regression Suite: Execute complete test suite including cross-domain workflow validation

---

## Post-Flight Checklist ✅

**Verify these conditions before marking parent task T112 complete**:

**Domain Migration Completeness**:

- [ ] Recipe Domain: All recipe CRUD operations functional with business rules preserved
- [ ] Scraper Domain: Recipe URL scraping maintains 3-8s performance and parsing accuracy
- [ ] Parser Domain: Ingredient parsing maintains 90%+ accuracy on standard formats  
- [ ] User Management Domain: Multi-tenant authentication and group isolation working
- [ ] Meal Planning Domain: Meal plan generation and shopping list creation operational

**Integration Validation**:

- [ ] Cross-domain events: Recipe creation → parsing → storage workflow functional
- [ ] API compatibility: All FastAPI endpoints maintain original contracts and performance
- [ ] Frontend integration: React components provide equivalent functionality to Nuxt.js originals
- [ ] External integrations: recipe-scrapers library and OpenAI API integration preserved

**Quality Assurance**:

- [ ] Test coverage: 85%+ coverage maintained across all domains
- [ ] Performance baselines: All domains meet analysis-documented performance requirements
- [ ] Security validation: Multi-tenant isolation and authentication working correctly
- [ ] Documentation: Domain architecture and API changes documented

**Asset Retirement**:

- [ ] Legacy backup: `features/mealie/` securely archived
- [ ] Ground Truth validation: All critical workflows tested and passing  
- [ ] Production readiness: Domain-integrated system validated in production-like environment
- [ ] Stakeholder approval: All domain migrations approved and functionality confirmed

**Final Validation Command**: 

```bash
pytest tests/productivity/test_mealie_integration.py -v
pytest tests/domains/recipe/ tests/domains/scraper/ tests/domains/meal_planning/ -v
```

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Debug and fix issues within domain boundaries before proceeding.

---

## Dependencies & Execution Order

**Sequential Dependencies (Must Complete In Order):**

- **Phase 1 (Analysis Validation)**: Must complete first - validates analysis and establishes domain boundaries
- **Phase 2 (Data Architecture)**: Must complete before business logic - establishes domain model foundation  
- **Phase 3 (Domain Services)**: Must complete before complex algorithms - establishes domain service infrastructure

**Parallel Execution by Domain:**

- **Phases 4-5 (Domain Migrations)**: Can proceed in parallel by domain after Phase 3
  - Recipe Domain (Phase 6) + Scraper Domain (Phase 4) + Parser Domain (Phase 5) can run parallel
  - Meal Planning Domain depends on Recipe Domain completion
- **Phase 6 (Integration)**: Must complete after all domains migrated  

**Final Sequential Dependencies:**

- **Phase 6 (Cross-Domain Integration)**: Must complete after all domains migrated
- **Asset Retirement**: Must be final step - validates entire domain-integrated system

**Domain Boundary Validation**: Each domain must pass independent validation before cross-domain integration testing.

**Estimated Total Hours**: 40 hours (distributed across domains: Recipe=8h, Scraper=12h, Parser=6h, User Mgmt=4h, Meal Planning=6h, Integration=4h)



