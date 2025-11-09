---
description: "Firecrawl web scraping & AI extraction platform migration"
parent_task: "../tasks.md#T105"
parent_phase: "Phase 5: Productivity Migrations"
return_to: "../tasks.md#T106"
domain: "productivity"
target_service: "apps/productivity-service/src/"
legacy_path: "features/firecrawl"
estimated_hours: 220
total_files: 333
total_loc: 98539
critical_algorithms: 2
migration_type: "service-adapter-with-modernization"
project_status: "active-upstream"
firecrawl_project: true
---

# Tasks: [MIGRATION: Firecrawl]

**⬆️ PARENT TASK**: [`tasks.md#T105`](../tasks.md#T105)  
**⬇️ RETURN TO**: [`tasks.md#T106`](../tasks.md#T106)

---

## Handoff Context

**Called From**: `tasks.md` Phase 5, Task T105
**Entry Condition**: Productivity service foundation ready (Phase 1-4 complete)
**Exit Condition**: All tasks below complete + validation tests pass
**Return Action**: Mark T105 complete in parent `tasks.md`, proceed to T106

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](../HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Project Overview: Firecrawl Web Scraping & AI Extraction Platform

**Type**: Web scraping API service with AI-powered data extraction  
**Upstream**: Active development (https://github.com/firecrawl/firecrawl)  
**Codebase**: 98,539 LOC, 333 TypeScript files  
**Architecture**: Monorepo with API service, browser automation, multiple SDKs  

### Business Value

Firecrawl is a sophisticated web scraping platform that converts websites into LLM-ready formats:

- **Web Scraping**: Convert URLs to clean markdown/structured data
- **Intelligent Crawling**: Discover and scrape entire websites with depth control
- **AI Extraction**: Extract structured data using LLM models (OpenAI, Anthropic, Google)
- **Multi-Format Output**: Markdown, HTML, screenshots, links, metadata
- **Browser Automation**: JavaScript rendering with Playwright for modern SPAs
- **Developer SDKs**: Python, JavaScript, Rust client libraries

### Critical Components (from analysis)

1. **Web Crawling Engine** (`apps/api/src/scraper/WebScraper/crawler.ts`, ~859 LOC):
   - Intelligent URL discovery with robots.txt compliance
   - Depth-based traversal with include/exclude filters
   - Sitemap integration for efficient discovery
   - Link extraction and normalization
   - **Critical**: This algorithm is the core differentiator

2. **AI-Powered Extraction** (`apps/api/src/scraper/scrapeURL/transformers/llmExtract.ts`, ~200+ LOC):
   - Multi-provider AI integration (OpenAI, Anthropic, Google, Groq)
   - JSON Schema-based structured data extraction
   - Token limit handling and content truncation
   - Retry logic and error handling
   - **Critical**: Key feature that makes Firecrawl valuable for AI apps

3. **Browser Automation Service** (`apps/playwright-service-ts/`):
   - Dedicated Playwright microservice for JavaScript rendering
   - Screenshot capture and visual content extraction
   - Dynamic content handling for modern SPAs
   - **Critical**: Essential for modern web scraping

4. **Queue Management** (BullMQ-based):
   - Background job processing for long-running crawls
   - Job status tracking and progress monitoring
   - Webhook notifications for completion
   - **Important**: Enables scalable async operations

5. **API Versioning** (`v1/` and `v2/` controllers):
   - Dual API versions with different feature sets
   - Backward compatibility for existing users
   - **Important**: Migration must preserve both versions

### Key Challenges

1. **Active Upstream**: Must maintain upstream compatibility for security patches
2. **Multi-Service Architecture**: API + Playwright service + Redis + PostgreSQL
3. **AI Provider Integration**: Multiple LLM providers with different APIs
4. **Performance Sensitivity**: 2-10s response times, users expect speed
5. **SDK Ecosystem**: Python, JS, Rust SDKs must remain compatible

---

## Migration Strategy: Service Adapter with Selective Modernization

**Strategic Decision**: **Service Adapter** (NOT full rewrite, NOT pure wrapper)

### Rationale

**Why NOT Full Rewrite**:
- 98K LOC of TypeScript with complex browser automation
- Active upstream maintenance provides security patches
- Multi-language SDK ecosystem (Python, JS, Rust) requires API stability
- Crawling algorithm (859 LOC) is proven and battle-tested
- AI extraction logic is sophisticated and working well

**Why NOT Pure Wrapper**:
- Integration with Jane's unified API surface requires adaptation
- User preference system needs Jane-native implementation
- Authentication needs to integrate with Jane's auth system
- Monitoring and logging should use Jane's infrastructure
- Data persistence should use Jane's PostgreSQL schema

**What This Means - Service Adapter Approach**:

1. **Preserve Core Engine** (80% of Firecrawl codebase):
   - Keep web crawling algorithm exactly as-is
   - Keep AI extraction transformers unchanged
   - Keep Playwright service integration
   - Keep BullMQ queue management
   - Keep scraper transformers and processors

2. **Adapt Integration Layer** (20% new code):
   - Create Jane API adapter for `/scrape`, `/crawl`, `/extract` endpoints
   - Integrate with Jane's authentication and authorization
   - Port to Jane's user preference system
   - Implement Jane-native job tracking and status
   - Add Jane monitoring and logging hooks

3. **Modernize Where Beneficial**:
   - Use Jane's PostgreSQL for job persistence (vs. Redis-only)
   - Integrate with Jane's unified webhook system
   - Add cross-tool data flow (e.g., scrape → firecrawl, analyze → AI service)
   - Implement Jane's rate limiting and usage tracking

### Implementation Architecture

```
Jane Productivity Service
│
├── Firecrawl Adapter Layer (NEW - 20% of work)
│   ├── /api/scrape → firecrawl-service.scrape()
│   ├── /api/crawl → firecrawl-service.crawl()
│   ├── /api/extract → firecrawl-service.extract()
│   ├── Jane Auth Integration
│   ├── Jane User Preferences
│   └── Jane Job Tracking
│
└── Firecrawl Core Engine (PRESERVED - 80% existing)
    ├── apps/api/src/scraper/ (web scraping logic)
    ├── apps/api/src/controllers/ (endpoint handlers)
    ├── apps/playwright-service-ts/ (browser automation)
    └── AI Transformers (llmExtract, etc.)
```

### Estimated Breakdown (220 hours)

- **Phase 1-2**: Analysis & Environment Setup (20h)
- **Phase 3**: Service Adapter Layer (40h) - Jane API integration
- **Phase 4**: Authentication & User Preferences (32h) - Jane auth integration
- **Phase 5**: Job Management & Queue Integration (32h) - PostgreSQL persistence
- **Phase 6**: AI Provider Configuration (24h) - Multi-provider management
- **Phase 7**: Browser Automation Integration (24h) - Playwright service
- **Phase 8**: SDK Compatibility Layer (24h) - Maintain Python/JS/Rust SDKs
- **Phase 9**: Testing & Validation (32h) - Comprehensive testing
- **Phase 10**: Documentation & Deployment (12h) - Docs and deployment

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/productivity-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment: `features/firecrawl/` accessible and Docker-compose functional
- [ ] Firecrawl analysis report validated (all CRITICAL sections complete)
- [ ] External API test accounts: OpenAI, Anthropic (optional: Google, Groq)
- [ ] Playwright browser dependencies installed
- [ ] Redis and PostgreSQL available for queue management
- [ ] Decision approval for service adapter migration strategy

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## Migration Strategy: Service Adapter with Selective Modernization

**Core Principle**: Preserve 98K LOC battle-tested scraping engine while adapting integration layer for Jane platform.

**Validation Strategy**:

1. Ground Truth Tests → Establish current behavior baseline
2. Analysis Cross-Reference → Validate against documented behavior
3. Adapter Layer Implementation → Create Jane integration without touching core
4. Integration Testing → Ensure adapter produces identical results
5. Performance Validation → Maintain or improve baseline metrics

---

## Phase 1: Analysis Validation & Environment Setup (12 hours)

**Purpose**: Validate Firecrawl analysis and establish baseline testing environment.

- [ ] T001 [Analysis: Section.1] Validate Firecrawl analysis completeness: Confirm all CRITICAL sections filled
- [ ] T002 [Analysis: Section.1.2] Technology stack verification: Validate TypeScript/Express/BullMQ stack
- [ ] T003 [Analysis: Section.4.1] Critical algorithm inventory: Review web crawling and AI extraction algorithms
- [ ] T004 [Ground Truth] Setup Firecrawl Docker environment: Run legacy system locally with docker-compose
- [ ] T005 [Ground Truth] Test scraping workflow: Validate /scrape endpoint with various URLs
- [ ] T006 [Ground Truth] Test crawling workflow: Validate /crawl endpoint with depth limits
- [ ] T007 [Ground Truth] Test AI extraction: Validate /extract endpoint with JSON schema
- [ ] T008 [P] AI provider configuration: Setup OpenAI, Anthropic API keys (test accounts)
- [ ] T009 [P] Playwright service validation: Confirm browser automation working
- [ ] T010 Performance baseline: Measure scrape/crawl/extract response times

**Checkpoint**: Analysis validated, legacy system operational, baselines documented.

---

## Phase 2: Data Architecture Integration (8 hours)

**Purpose**: Define job tracking and scraping result persistence in Jane's PostgreSQL.

- [ ] T011 [Analysis: Section.2.1] Job model design: Create ScrapeJob, CrawlJob, ExtractJob models
- [ ] T012 Database schema: Alembic migrations for job tracking tables
- [ ] T013 Result storage model: Design ScrapeResult, CrawlResult, ExtractResult entities
- [ ] T014 [P] User preference model: Define Firecrawl-specific user settings
- [ ] T015 [P] API key management: Integrate with Jane's auth system for Firecrawl API keys
- [ ] T016 Job status tracking: Implement queued/processing/completed/failed states
- [ ] T017 Data validation tests: Verify models create/read correctly

**Checkpoint**: Data models migrated, schema applied, tests passing.

---

## Phase 3: Service Adapter Layer (40 hours)

**Purpose**: Create Jane API adapter that wraps Firecrawl core engine.

### Phase 3a: Scrape Endpoint Adapter (12 hours)

- [ ] T018 [Analysis: Section.3.2] Scrape endpoint design: POST /api/productivity/scrape
- [ ] T019 [Analysis: Section.4.1] [Logic: controllers/v2/scrape.ts] Adapter implementation: Wrap Firecrawl scraper
- [ ] T020 Request transformation: Convert Jane request format to Firecrawl ScrapeOptions
- [ ] T021 Response transformation: Convert Firecrawl Document to Jane response format
- [ ] T022 [P] Format handling: Support markdown, HTML, screenshot, links, metadata
- [ ] T023 [P] Error handling: Graceful degradation and error mapping
- [ ] T024 Scrape adapter tests: Unit tests for request/response transformation
- [ ] T025 Ground truth validation: Compare adapter output to legacy scrape endpoint

### Phase 3b: Crawl Endpoint Adapter (16 hours)

- [ ] T026 [Analysis: Section.3.2] Crawl endpoint design: POST /api/productivity/crawl
- [ ] T027 [Analysis: Section.4.1] [Logic: controllers/v2/crawl.ts] Adapter implementation: Wrap Firecrawl crawler
- [ ] T028 Request transformation: Convert Jane crawl request to Firecrawl CrawlOptions
- [ ] T029 Job creation: Create CrawlJob in PostgreSQL and queue with BullMQ
- [ ] T030 Status tracking: Implement /api/productivity/crawl/status/:id endpoint
- [ ] T031 [P] Webhook integration: Connect Firecrawl webhooks to Jane's webhook system
- [ ] T032 [P] Depth and filtering: Preserve include/exclude patterns, depth limits
- [ ] T033 [P] Robots.txt compliance: Ensure crawler respects robots.txt rules
- [ ] T034 Crawl adapter tests: Unit tests for crawl job lifecycle
- [ ] T035 Ground truth validation: Compare crawl results to legacy endpoint

### Phase 3c: Extract Endpoint Adapter (12 hours)

- [ ] T036 [Analysis: Section.3.2] Extract endpoint design: POST /api/productivity/extract
- [ ] T037 [Analysis: Section.4.1] [Logic: controllers/v2/extract.ts] Adapter implementation: Wrap AI extraction
- [ ] T038 Schema validation: Validate JSON Schema input from user
- [ ] T039 AI provider routing: Route to OpenAI, Anthropic, Google, Groq based on config
- [ ] T040 [P] Token limit handling: Implement content truncation for large documents
- [ ] T041 [P] Retry logic: Exponential backoff for AI API failures
- [ ] T042 Extract adapter tests: Unit tests for AI extraction workflow
- [ ] T043 Ground truth validation: Compare extraction accuracy to legacy

**Checkpoint**: Service adapter functional, all endpoints working.

---

## Phase 4: Authentication & User Preferences (32 hours)

**Purpose**: Integrate Firecrawl with Jane's authentication and user preference system.

### Phase 4a: Authentication Integration (16 hours)

- [ ] T044 [Analysis: Section.3.1] Jane auth integration: Replace Firecrawl API keys with Jane auth
- [ ] T045 API key migration: Map existing Firecrawl API keys to Jane user accounts
- [ ] T046 Rate limiting: Implement Jane-native rate limiting per user/tier
- [ ] T047 [P] Usage tracking: Track scrape/crawl/extract operations per user
- [ ] T048 [P] Subscription tier enforcement: Free/Pro/Enterprise feature access
- [ ] T049 Authorization testing: Verify access control rules
- [ ] T050 Security audit: Review authentication implementation
- [ ] T051 Auth migration script: Migrate existing users to Jane auth

### Phase 4b: User Preferences (16 hours)

- [ ] T052 Preference schema: Define Firecrawl user preferences
- [ ] T053 Default AI provider: Allow users to choose OpenAI, Anthropic, Google, Groq
- [ ] T054 Default scrape format: Markdown, HTML, screenshot preferences
- [ ] T055 Crawl defaults: Depth limits, include/exclude patterns
- [ ] T056 [P] Webhook configuration: User-defined webhook URLs for job completion
- [ ] T057 [P] Cache preferences: User control over result caching
- [ ] T058 Preference API endpoints: GET/PUT /api/user/preferences/firecrawl
- [ ] T059 Preference integration tests: Validate user settings applied correctly

**Checkpoint**: Authentication integrated, user preferences functional.

---

## Phase 5: Job Management & Queue Integration (32 hours)

**Purpose**: Integrate Firecrawl's BullMQ queue system with Jane's job tracking.

### Phase 5a: Queue Infrastructure (16 hours)

- [ ] T060 [Analysis: Section.5.1] BullMQ integration: Connect Firecrawl queues to Jane infrastructure
- [ ] T061 Queue configuration: Redis-backed job queues for scrape/crawl/extract
- [ ] T062 Job serialization: Store job parameters and results in PostgreSQL
- [ ] T063 Progress tracking: Real-time progress updates for long-running crawls
- [ ] T064 [P] Job prioritization: Priority queue for Pro/Enterprise users
- [ ] T065 [P] Concurrency limits: Per-user concurrent job limits
- [ ] T066 Queue monitoring: Implement job queue health checks
- [ ] T067 Queue tests: Unit tests for job lifecycle management

### Phase 5b: Job Status & Results (16 hours)

- [ ] T068 Status API: GET /api/productivity/jobs/:id endpoint
- [ ] T069 Job listing: GET /api/productivity/jobs with filtering/pagination
- [ ] T070 Result retrieval: GET /api/productivity/jobs/:id/results
- [ ] T071 Job cancellation: DELETE /api/productivity/jobs/:id
- [ ] T072 [P] Job expiration: Auto-delete old job results after retention period
- [ ] T073 [P] Result caching: Cache scrape results for duplicate requests
- [ ] T074 Webhook delivery: Trigger Jane webhooks on job completion
- [ ] T075 Job management tests: Integration tests for job CRUD operations

**Checkpoint**: Job tracking functional, queue processing working.

---

## Phase 6: AI Provider Configuration (24 hours)

**Purpose**: Manage multiple AI providers with graceful failover.

### Phase 6a: Multi-Provider Management (12 hours)

- [ ] T076 [Analysis: Section.5.1] AI provider abstraction: Unified interface for OpenAI, Anthropic, Google, Groq
- [ ] T077 [Logic: scraper/scrapeURL/transformers/llmExtract.ts] Provider routing: Select provider based on user preference
- [ ] T078 API key management: Secure storage for AI provider API keys
- [ ] T079 Provider failover: Automatic fallback to secondary provider on failure
- [ ] T080 [P] Cost tracking: Track AI API usage and costs per provider
- [ ] T081 [P] Rate limit handling: Respect provider-specific rate limits
- [ ] T082 Provider tests: Unit tests for each AI provider integration
- [ ] T083 Ground truth validation: Verify extraction quality matches legacy

### Phase 6b: Extraction Configuration (12 hours)

- [ ] T084 Schema validation: JSON Schema validation for extraction requests
- [ ] T085 Prompt engineering: Configurable system prompts per provider
- [ ] T086 Token optimization: Content truncation strategies for large documents
- [ ] T087 Result validation: Validate extracted data against schema
- [ ] T088 [P] Caching strategy: Cache extraction results by content hash + schema
- [ ] T089 [P] Retry configuration: User-configurable retry attempts
- [ ] T090 Extraction tests: Integration tests for AI extraction workflow
- [ ] T091 Performance validation: Ensure extraction speed within baseline

**Checkpoint**: AI providers configured, extraction functional.

---

## Phase 7: Browser Automation Integration (24 hours)

**Purpose**: Integrate Playwright service for JavaScript rendering.

### Phase 7a: Playwright Service (12 hours)

- [ ] T092 [Analysis: Section.5.1] Playwright service integration: Connect to browser automation microservice
- [ ] T093 [Logic: playwright-service-ts/] Service communication: HTTP API for scrape requests
- [ ] T094 Browser pool management: Manage Playwright browser instances
- [ ] T095 Screenshot capture: Implement screenshot functionality
- [ ] T096 [P] JavaScript execution: Support custom JavaScript injection
- [ ] T097 [P] Wait strategies: Implement wait-for-selector, wait-for-network-idle
- [ ] T098 Browser tests: Unit tests for Playwright integration
- [ ] T099 Ground truth validation: Verify dynamic content rendering matches legacy

### Phase 7b: Dynamic Content Handling (12 hours)

- [ ] T100 SPA detection: Auto-detect JavaScript-heavy sites
- [ ] T101 Rendering strategy: Choose between static fetch vs. Playwright rendering
- [ ] T102 Performance optimization: Minimize browser usage for simple pages
- [ ] T103 Error handling: Graceful degradation when Playwright unavailable
- [ ] T104 [P] Resource blocking: Block ads, trackers, analytics for faster rendering
- [ ] T105 [P] Mobile emulation: Support mobile viewport rendering
- [ ] T106 Dynamic content tests: Integration tests for SPA scraping
- [ ] T107 Performance validation: Ensure rendering speed within baseline

**Checkpoint**: Browser automation functional, dynamic content handled.

---

## Phase 8: SDK Compatibility Layer (24 hours)

**Purpose**: Maintain compatibility with existing Python, JavaScript, Rust SDKs.

### Phase 8a: SDK Analysis (8 hours)

- [ ] T108 [Analysis: Section.1.2] Python SDK review: Analyze firecrawl-py client library
- [ ] T109 JavaScript SDK review: Analyze @mendable/firecrawl-js client library
- [ ] T110 Rust SDK review: Analyze firecrawl-rs client library
- [ ] T111 API contract documentation: Document all SDK-expected endpoints
- [ ] T112 [P] Breaking change analysis: Identify any incompatible changes
- [ ] T113 [P] Versioning strategy: Plan v1 vs. v2 API support
- [ ] T114 SDK compatibility matrix: Document which SDKs work with Jane adapter
- [ ] T115 SDK update plan: Identify required SDK changes for Jane integration

### Phase 8b: SDK Testing & Updates (16 hours)

- [ ] T116 Python SDK tests: Validate firecrawl-py works with Jane adapter
- [ ] T117 JavaScript SDK tests: Validate @mendable/firecrawl-js works with Jane adapter
- [ ] T118 Rust SDK tests: Validate firecrawl-rs works with Jane adapter
- [ ] T119 [P] SDK documentation: Update SDK docs for Jane-specific configuration
- [ ] T120 [P] Example updates: Update SDK examples for Jane platform
- [ ] T121 [P] Migration guide: Create guide for SDK users migrating to Jane
- [ ] T122 SDK integration tests: End-to-end tests with each SDK
- [ ] T123 Backward compatibility validation: Ensure existing SDK code works unchanged

**Checkpoint**: All SDKs functional, backward compatibility maintained.

---

## Phase 9: Testing & Validation (32 hours)

**Purpose**: Comprehensive testing and quality assurance.

### Phase 9a: Unit & Integration Tests (16 hours)

- [ ] T124 [Analysis: Section.7.1] Test suite migration: Port existing Jest tests
- [ ] T125 Adapter layer tests: Validate request/response transformations
- [ ] T126 Authentication tests: Verify Jane auth integration
- [ ] T127 Job management tests: Validate queue lifecycle
- [ ] T128 [P] AI extraction tests: Mock AI providers, test extraction logic
- [ ] T129 [P] Browser automation tests: Mock Playwright, test rendering
- [ ] T130 Database tests: Verify job persistence and retrieval
- [ ] T131 Test coverage report: Achieve 70%+ coverage baseline

### Phase 9b: Performance & Load Testing (16 hours)

- [ ] T132 [Analysis: Section.8.1] Performance benchmarking: Scrape/crawl/extract response times
- [ ] T133 Load testing: Concurrent scrape requests (Artillery)
- [ ] T134 Crawl performance: Large site crawling (100+ pages)
- [ ] T135 AI extraction performance: Measure token processing speed
- [ ] T136 [P] Browser automation performance: Playwright rendering speed
- [ ] T137 [P] Queue throughput: Measure job processing rate
- [ ] T138 End-to-end workflow tests: Complete user journeys
- [ ] T139 Ground truth comparison: Final parity validation against legacy

**Checkpoint**: All tests passing, performance baselines met.

---

## Phase 10: Documentation & Deployment (12 hours)

**Purpose**: Documentation and production readiness.

- [ ] T140 [Analysis: Section.13.1] User documentation: Firecrawl scraping guide
- [ ] T141 API documentation: OpenAPI spec for /scrape, /crawl, /extract endpoints
- [ ] T142 Configuration documentation: Environment variables, AI provider setup
- [ ] T143 SDK migration guide: How to use Firecrawl with Jane platform
- [ ] T144 [P] Example gallery: Showcase Firecrawl + Jane AI integration examples
- [ ] T145 [P] Troubleshooting guide: Common issues and resolutions
- [ ] T146 Deployment documentation: Docker/Kubernetes deployment for Firecrawl + Playwright
- [ ] T147 Production deployment: Deploy to staging/production environment

**Checkpoint**: Documentation complete, production deployment successful.

---

## Dependencies & Execution Order

**Sequential Dependencies**:
- Phase 1 → Phase 2 (data architecture requires analysis)
- Phase 2 → Phase 3 (adapter requires data models)
- Phase 3 → Phase 4-7 (auth, jobs, AI, browser all require adapter)
- Phase 8 depends on Phases 3-7 (SDK testing requires functional endpoints)
- Phase 9 validates all previous phases
- Phase 10 requires Phase 9 validation

**Parallel Opportunities**:
- Phase 4a + Phase 5a (auth and queue can develop independently)
- Phase 6 + Phase 7 (AI providers and browser automation independent)
- Phase 8a + Phase 9a (SDK analysis and test migration)

**Critical Path**: Phase 1 → Phase 2 → Phase 3 → Phase 4-7 → Phase 9 → Phase 10

---

## Post-Flight Checklist ✅

**Before marking T105 complete in parent tasks.md, verify ALL conditions met**:

### Functional Parity Validation
- [ ] All 147 tasks marked complete
- [ ] Scrape endpoint: Produces identical markdown/HTML output to legacy
- [ ] Crawl endpoint: Discovers same URLs with depth/filter rules
- [ ] Extract endpoint: AI extraction quality matches legacy accuracy
- [ ] Browser automation: JavaScript rendering produces identical results
- [ ] Job tracking: Queue processing and status tracking functional
- [ ] Webhook delivery: Job completion notifications working

### Performance Validation
- [ ] Scrape response time: Within ±20% of legacy baseline (2-10s depending on page)
- [ ] Crawl discovery: Within ±15% of legacy URL discovery speed
- [ ] AI extraction: Within ±10% of legacy extraction speed (accounting for AI API variance)
- [ ] Browser rendering: Playwright performance within ±20% of legacy
- [ ] Queue throughput: Job processing rate maintained or improved

### Integration Validation
- [ ] Jane authentication: API key auth working with user accounts
- [ ] User preferences: Firecrawl settings persisted correctly
- [ ] PostgreSQL persistence: Job data stored and retrievable
- [ ] BullMQ queues: Background processing functional
- [ ] AI providers: OpenAI, Anthropic, Google, Groq all working
- [ ] Playwright service: Browser automation microservice operational

### SDK Compatibility Validation
- [ ] Python SDK: firecrawl-py works with Jane adapter
- [ ] JavaScript SDK: @mendable/firecrawl-js works with Jane adapter
- [ ] Rust SDK: firecrawl-rs works with Jane adapter
- [ ] API compatibility: v1 and v2 endpoints preserved
- [ ] No breaking changes for existing SDK users

### Test Coverage Validation
- [ ] Unit tests: 70%+ coverage achieved
- [ ] Integration tests: All critical workflows tested
- [ ] Ground truth tests: All [Logic: ...] tags validated
- [ ] Performance tests: Baselines documented and met
- [ ] SDK tests: All client libraries tested end-to-end

### Documentation Validation
- [ ] User documentation: Scraping workflows documented
- [ ] API documentation: OpenAPI spec complete with examples
- [ ] SDK documentation: Migration guide for existing users
- [ ] Configuration guide: Environment setup documented
- [ ] Example gallery: AI integration examples available

### Production Readiness Validation
- [ ] Docker deployment: Firecrawl + Playwright containers working
- [ ] Environment configuration: All secrets and API keys secure
- [ ] Monitoring: Metrics, logging, error tracking operational
- [ ] Health checks: /health endpoint functional
- [ ] Rollback plan: Documented procedure for production rollback

### Completion Criteria (from analysis Section 12.3)
- [ ] ✅ All API endpoints working with identical response formats
- [ ] ✅ AI extraction functionality preserved with same accuracy
- [ ] ✅ Browser automation capabilities maintained
- [ ] ✅ Queue processing and job management reliable
- [ ] ✅ Multi-language SDK compatibility maintained
- [ ] ✅ Rate limiting and authentication functional
- [ ] ✅ All output formats working (markdown, HTML, screenshot, etc.)

### Final Validation Command
```bash
# Run complete validation suite
pytest apps/productivity-service/tests/integration/test_firecrawl_migration.py -v
npm test -- apps/productivity-service/tests/firecrawl-sdk.test.ts

# Expected: All tests PASS, performance metrics within thresholds
```

### Exit Conditions (MUST be TRUE to proceed)
1. ✅ All 147 tasks complete
2. ✅ All validation tests pass (unit + integration + ground truth)
3. ✅ Performance baselines met or exceeded
4. ✅ All AI providers functional
5. ✅ SDK compatibility maintained
6. ✅ Migration documented in `migration-validation.md`
7. ✅ No critical regressions vs. legacy system
8. ✅ Production deployment successful in staging

**If ANY condition fails**: 
- Document blocker in `specs/003-brownfield-integration/migration-validation.md`
- Fix issues before marking T105 complete
- Re-run validation after fixes

**When ALL conditions pass**:
- Update `migration-validation.md` with completion timestamp and results
- Mark T105 complete in `specs/003-brownfield-integration/tasks.md`
- Proceed to T106 (next project in migration queue)

---

## Completion Summary

**Project**: Firecrawl (Web Scraping & AI Extraction Platform)  
**Migration Type**: Service Adapter with Selective Modernization  
**Total Tasks**: 147 tasks across 10 phases  
**Estimated Hours**: 220 hours  
**Codebase Size**: 98,539 LOC, 333 TypeScript files  

### Migration Approach: Service Adapter (80% Preserve, 20% Adapt)

**Strategic Decision Rationale**:
- **Active Upstream**: Maintained by Firecrawl team, security patches needed
- **Proven Engine**: 98K LOC battle-tested scraping and AI extraction logic
- **SDK Ecosystem**: Python, JS, Rust libraries require API stability
- **Complexity**: Browser automation and multi-provider AI integration too complex to rewrite
- **Integration Need**: Jane platform requires auth, user prefs, job tracking integration

**What We're Preserving** (80% of codebase):
1. **Web Crawling Algorithm** (`apps/api/src/scraper/WebScraper/crawler.ts`, ~859 LOC):
   - Intelligent URL discovery with robots.txt compliance
   - Sitemap integration and link extraction
   - Depth-based traversal with include/exclude filters
   - **Zero changes** - algorithm is core differentiator

2. **AI Extraction Engine** (`apps/api/src/scraper/scrapeURL/transformers/llmExtract.ts`, ~200+ LOC):
   - Multi-provider support (OpenAI, Anthropic, Google, Groq)
   - JSON Schema-based extraction
   - Token limit handling and retry logic
   - **Zero changes** - proven AI integration

3. **Browser Automation** (`apps/playwright-service-ts/`):
   - Playwright microservice for JavaScript rendering
   - Screenshot capture and dynamic content handling
   - **Zero changes** - essential for modern web scraping

4. **Scraper Transformers** (`apps/api/src/scraper/scrapeURL/`):
   - Markdown conversion, HTML cleaning, link extraction
   - Screenshot processing, metadata extraction
   - **Zero changes** - transformation logic is solid

**What We're Adapting** (20% new code):
1. **API Adapter Layer** (40h):
   - Jane-native `/scrape`, `/crawl`, `/extract` endpoints
   - Request/response transformation
   - Error mapping and standardization

2. **Authentication Integration** (32h):
   - Replace Firecrawl API keys with Jane auth
   - User-based rate limiting and usage tracking
   - Subscription tier enforcement

3. **Job Management** (32h):
   - PostgreSQL job persistence (vs. Redis-only)
   - BullMQ integration with Jane queue system
   - Webhook integration with Jane's webhook service

4. **User Preferences** (16h):
   - Jane-native preference storage
   - Default AI provider, scrape format, crawl settings
   - User-specific configurations

### Key Differences from Dispatch Migration

| Aspect | Dispatch (Project 4) | Firecrawl (Project 5) |
|--------|---------------------|----------------------|
| **Upstream Status** | Archived (Netflix discontinued) | Active (Firecrawl maintained) |
| **Migration Type** | Full DDD migration | Service adapter (80% preserve) |
| **Rationale** | Own archived asset | Preserve active upstream + adapt integration |
| **Hours** | 180 hours | 220 hours |
| **LOC** | 72,381 LOC (Python) | 98,539 LOC (TypeScript) |
| **Architecture** | Full port to Jane domains | Adapter layer wrapping core engine |
| **Business Logic** | 100% ported | 80% preserved, 20% adapted |
| **Framework** | FastAPI → FastAPI | TypeScript/Express → Jane adapter |
| **External Deps** | 6 integrations (Slack, Google, etc.) | 4+ AI providers + Playwright service |

### Critical Implementation Notes

1. **Crawling Algorithm Preservation**:
   - Keep `apps/api/src/scraper/WebScraper/crawler.ts` exactly as-is
   - This 859 LOC algorithm is the core differentiator
   - Validate with ground truth tests for URL discovery parity

2. **AI Extraction Quality**:
   - Preserve multi-provider abstraction exactly
   - Validate extraction accuracy matches legacy
   - Test with various JSON schemas and content types

3. **Playwright Service Integration**:
   - Maintain as separate microservice (don't consolidate)
   - Browser automation requires process isolation
   - Validate JavaScript rendering produces identical results

4. **SDK Backward Compatibility**:
   - Python, JS, Rust SDKs must work unchanged
   - Adapter must preserve API contract exactly
   - Test all SDKs end-to-end before completion

### Phase Breakdown (220 hours)

- **Phase 1**: Analysis & Setup (12h) - Environment, baselines
- **Phase 2**: Data Architecture (8h) - Job models, PostgreSQL schema
- **Phase 3**: Service Adapter (40h) - Scrape/crawl/extract endpoint adapters
- **Phase 4**: Authentication & Preferences (32h) - Jane auth, user settings
- **Phase 5**: Job Management (32h) - Queue integration, job tracking
- **Phase 6**: AI Provider Configuration (24h) - Multi-provider management
- **Phase 7**: Browser Automation (24h) - Playwright service integration
- **Phase 8**: SDK Compatibility (24h) - Python/JS/Rust testing
- **Phase 9**: Testing & Validation (32h) - Unit, integration, performance
- **Phase 10**: Documentation & Deployment (12h) - Docs, production deploy

### Success Metrics (from analysis Section 12.3)

- ✅ All API endpoints working with identical response formats
- ✅ AI extraction accuracy matches legacy (same AI providers)
- ✅ Browser automation capabilities maintained (Playwright unchanged)
- ✅ Queue processing reliable (BullMQ preserved)
- ✅ SDK compatibility maintained (Python, JS, Rust)
- ✅ Performance within ±20% of legacy baselines

### Return to Parent Orchestration

**Next Steps**:
1. Mark T105 complete in `specs/003-brownfield-integration/tasks.md`
2. Update `migration-validation.md` with Firecrawl completion results
3. Proceed to T106 (next project in productivity domain)

**Migration Status**: 5 of 37 projects complete (13.5% overall progress)
- ✅ Project 1: [TBD]
- ✅ Project 2: [TBD]
- ✅ Project 3: CyberChef (120h, Web Component wrapper)
- ✅ Project 4: Dispatch (180h, Full DDD migration)
- ✅ Project 5: Firecrawl (220h, Service adapter)
- ⏳ Project 6-37: Pending (32 projects remaining)

---

**Document Version**: 1.0.0  
**Last Updated**: 2025-11-09  
**Template Version**: task-individual-template.md v2.0.0
