---
description: "BlackArch: Security tool catalog with bulk download (HYBRID MIGRATION)"
parent_task: "../tasks.md#T106"
parent_phase: "Phase 5: Security Domain Migrations"
return_to: "../tasks.md#T107"
domain: "security"
target_service: "apps/security-service/src/tool-catalog/"
legacy_path: "features/blackarch"
estimated_hours: 70  # Updated from 26 (metadata-only) to 70 (bulk download)
migration_type: "hybrid-bulk-download"  # Updated from metadata-extraction-only
archive_decision: "partial-infrastructure"  # Updated from complete-repository
package_count: 4599  # PKGBUILD files for 2,865 tools
script_loc: 5804  # Bash infrastructure scripts
categories: 49  # Tool classification groups
storage_required: "200 GB"  # Local mirror for all tool sources
download_size: "150 GB (estimated)"  # One-time bulk download
setup_time: "3-5 hours"  # Initial platform setup
strategy_pivot: "2025-11-09"  # Date of bulk download decision

# STRATEGY PIVOT (2025-11-09)
# ────────────────────────────────────────────────────────────────────────
# Original Plan: Metadata extraction only (26 hours)
#   - Parse PKGBUILD files → tool catalog database → discovery UI
#   - Users browse catalog, manually install tools
#   - Risk: Link rot, upstream abandonment, no offline capability
#
# REVISED Plan: Bulk download + local installation (70 hours)
#   - ONE-TIME bulk download of ALL 2,865 tool sources during platform setup
#   - Store in /var/lib/mental-prosthetic/blackarch-mirror/ (~200 GB)
#   - Future-proof: Complete offline capability, survives upstream abandonment
#   - User experience: Browse catalog → one-click install from LOCAL cache
#   - Performance: <100ms search, 1-5min builds (no network dependency)
#
# Key Benefits:
#   ✓ Future-proofing: Frozen snapshot (Nov 9, 2025), survives BlackArch shutdown
#   ✓ Offline capability: Air-gapped deployments, secure environments
#   ✓ Performance: Zero runtime downloads, instant catalog, fast local builds
#   ✓ Reliability: No upstream rate limits, no network failures
#   ✓ Compliance: All sources locally auditable, security scanning possible
#
# Migration Components:
#   ✓ PKGBUILD parser (Python) - extract metadata + source URLs
#   ✓ Bulk download engine - parallel downloader with checksum verification
#   ✓ Database importer - PostgreSQL catalog with local file paths
#   ✓ Docker build system - generate containers from local sources
#   ✓ Discovery UI - search/browse/install interface
#
# Archived Components (NOT migrated):
#   ✗ babuild, barelease (Arch-specific build/release infrastructure)
#   ✗ Mirror management (replaced by local archive)
#   ✗ GPG signing system (not needed for local installation)
#
# Implementation Status: DOCUMENTED (tasks below need rewrite for bulk download)
# ────────────────────────────────────────────────────────────────────────
---

# Tasks: BlackArch - Security Tool Catalog Integration

**⬆️ PARENT TASK**: [`tasks.md#T106`](../tasks.md#T106)  
**⬇️ RETURN TO**: [`tasks.md#T107`](../tasks.md#T107)

---

## ⚠️ STRATEGY PIVOT: Bulk Download Architecture (2025-11-09)

**BlackArch is a Linux distribution package repository (like APT/YUM), not an application.**

**What BlackArch Is**:
- Package repository manager for 2,865 security tools
- Build/release infrastructure (Bash scripts)
- Tool categorization system (49 categories)
- Mirror network for package distribution

**What BlackArch Is NOT**:
- ❌ A security tool implementation
- ❌ An application with business logic to migrate wholesale
- ❌ Platform-independent code (Arch Linux-specific)

**REVISED Decision**: **Bulk Download + Local Installation** (NOT metadata-only)

**Rationale for Strategy Pivot**:
1. **Future-Proofing Critical**: 2,865 tools downloaded during platform setup → survives upstream abandonment
2. **Offline Capability**: Air-gapped deployments possible (secure environments)
3. **Performance**: Zero runtime downloads, instant catalog access, fast local builds
4. **User Experience**: One-click install from local cache (executive function support)
5. **Storage Trade-off Acceptable**: 200 GB for 2,865 tools = 0.07 GB/tool (reasonable)

**Architecture Shift**:
- ❌ OLD: Browse catalog → manual installation → link rot risk
- ✅ NEW: One-time bulk download (3-5h setup) → lifetime offline access → zero external dependencies

---

## Handoff Context

**Called From**: `tasks.md` Phase 5, Task T106  
**Entry Condition**: Security service foundation ready (Phase 1-4 complete)  
**Exit Condition**: All tasks below complete + tool catalog service operational  
**Return Action**: Mark T106 complete in parent `tasks.md`, proceed to T107

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Project Overview

**Type**: Linux Distribution Package Repository (Arch Linux-based)  
**Purpose**: Curated catalog of 2,865+ penetration testing and security tools  
**Domain**: Security - Tool discovery and distribution infrastructure  
**Codebase**: 4,599 PKGBUILD files + 5,804 LOC Bash scripts

**NOT Migratable**:
- Infrastructure layer (like migrating APT, YUM, or Homebrew)
- Tightly coupled to Arch Linux package management (pacman)
- Zero original tool implementations (all tools sourced from upstream projects)
- No platform-independent business logic

**Value Proposition**:
- Curated collection of 2,865 security tools
- 49-category classification system (webapp, forensic, scanner, malware, etc.)
- Pre-built packages with resolved dependencies
- Community-maintained PKGBUILD build scripts

**Mental Prosthetic Platform Integration**:
- **NOT** one of the 37 core tools to migrate
- **INSTEAD**: Optional tool discovery catalog
- **Priority**: NICE-TO-HAVE (not CRITICAL)
- **Approach**: Metadata extraction, not code migration

---

## Archive Decision: Complete Repository

**Files to Archive** (100% of codebase):

1. **4,599 PKGBUILD files** - Package build scripts for all tools
2. **5,804 LOC Bash scripts** - Repository management infrastructure
   - `babuild` (206 LOC) - Package building in clean chroot
   - `barelease` (368 LOC) - Package release management
   - `group-official` (~150 LOC) - Category meta-package creation
   - ~55 other maintenance/automation scripts
3. **Category definitions** - 49 tool classification groups
4. **Mirror configuration** - Distribution network setup
5. **Documentation** - Developer guides, TODO, licenses

**Archive Location**: `experimental-archive/blackarch/`

**Decision Matrix Results**:

| Criteria                  | Score | Reasoning                                    |
| ------------------------- | ----- | -------------------------------------------- |
| Business Value (migrate)  | 0/10  | Reinventing package management serves no purpose |
| Migration Complexity      | 200-300h | Bash → Python, rebuild pacman functionality |
| Platform Independence     | ❌ FAIL | Arch Linux package management only          |
| Better Alternative        | ✅ YES  | Metadata extraction provides 90% value      |
| Original Code             | 0%    | All tools sourced from upstream projects    |
| Integration Value         | 8/10  | Tool catalog discovery valuable             |

**Rationale**:

1. **Zero Original Tools**: BlackArch packages existing tools (nmap, metasploit, etc.) - doesn't implement them
2. **Infrastructure, Not Logic**: Package management system, not business application
3. **Platform Lock-In**: Requires Arch Linux pacman ecosystem
4. **Massive Wasted Effort**: 200-300 hours to reinvent package management with zero unique value
5. **Better Approach**: Extract metadata (tool names, categories, descriptions) for discovery catalog

**Functionality Preserved**: 100% via metadata extraction + optional BlackArch installation commands

---

## Integration Strategy: Bulk Download + Local Installation

**Approach**: Download all 2,865 tool sources during platform setup, enable offline installation

**Phase 1: Setup-Time Bulk Download** (One-Time, During Platform Install):

1. **Parse PKGBUILD Files** (4,599 files)
   - Extract metadata: name, version, description, category, dependencies
   - Extract source URLs: git repos, tarballs, upstream projects
   - Build dependency graph

2. **Bulk Download All Sources**
   - Parallel downloader (100 concurrent connections)
   - Download all upstream sources (git clone, wget, curl)
   - Verify checksums (SHA256, MD5 from PKGBUILD)
   - Store in: `/var/lib/mental-prosthetic/blackarch-mirror/`
   - Size: ~150 GB download → ~200 GB on disk
   - Time: 3-5 hours (internet speed dependent)

3. **Populate Database**
   - Import tool metadata → PostgreSQL
   - Index by category, name, description
   - Store LOCAL file paths (not URLs)
   - Create dependency resolution tables

**Phase 2: Runtime Usage** (After Platform Installed):

1. **User Workflow**:
   - Browse 2,865 tools in catalog (instant - local DB)
   - Search/filter by category, name, description (<100ms)
   - Select tool → view dependencies/details
   - Click "Install" → build from LOCAL archive (1-5 min, no download)
   - Tool ready in isolated Docker container

**What to Build**:

1. **PKGBUILD Parser** (Python): Extract metadata + source URLs
2. **Bulk Download Engine**: Parallel downloader with retry/checksum verification
3. **Tool Database**: PostgreSQL with local file path references
4. **Docker Build System**: Generate containers from local sources
5. **Discovery API**: FastAPI endpoints for search/browse/install
6. **UI Components**: Catalog browser with one-click local install

**What to Archive** (NOT migrate):
- ❌ babuild, barelease (Arch-specific build/release infrastructure)
- ❌ Mirror management (replaced by local archive)
- ❌ GPG signing system (not needed for local installation)

**Storage Requirements**:
- BlackArch mirror: ~200 GB
- Database + indexes: ~100 MB
- Total platform (with 37 core tools): ~260 GB

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/security-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment: `features/blackarch/` accessible
- [ ] **CRITICAL**: Bulk download strategy documented and approved
- [ ] **CRITICAL**: Storage provisioned: 200 GB for BlackArch mirror
- [ ] **CRITICAL**: Team understands this is HYBRID migration (bulk download + local install)
- [ ] Docker infrastructure available for container-based tool installation

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## ⚠️ TASKS BELOW REQUIRE REWRITE FOR BULK DOWNLOAD ARCHITECTURE

**Current Status**: Tasks T001-T061 reflect original metadata-extraction-only approach (26 hours)

**Required Update**: Rewrite for bulk download architecture (70 hours, ~95 tasks):
- Phase 1: Setup-time bulk download (20 hours) - PKGBUILD parsing, parallel downloader, checksum verification
- Phase 2: Docker build system (16 hours) - local-first installer, dependency resolver
- Phase 3: Discovery UI (12 hours) - catalog browser with one-click install from local cache
- Phase 4: Platform integration (8 hours) - API endpoints for install/status tracking
- Phase 5: Testing & validation (14 hours) - bulk download validation, Docker build tests

**When to Rewrite**: Before starting implementation (return to this file when ready to execute)

**Reference**: See frontmatter STRATEGY PIVOT comment for complete bulk download architecture

---

---

## Phase 1: Archive Preparation & Analysis (2 hours)

**Purpose**: Create complete BlackArch archive with documentation explaining non-migration decision.

- [ ] T001 Create experimental archive structure: `experimental-archive/blackarch/` with subdirectories
- [ ] T002 [P] Move all BlackArch code to archive: packages/, scripts/, lists/, docs/, mirror/
- [ ] T003 Create INDEX.md: Quick start explaining BlackArch nature and integration approach
- [ ] T004 Create README.md: Comprehensive analysis of why migration is inappropriate (reference /tmp/blackarch-project-evaluation.md)
- [ ] T005 Create REVIVAL-GUIDE.md: Document how to use BlackArch directly (not revival of code, but installation guide)
- [ ] T006 Create MANIFEST.txt: Complete file inventory (4,599 PKGBUILD + 5,804 LOC scripts)
- [ ] T007 Document alternative usage: Instructions for installing BlackArch as package source if user wants actual tools

**Checkpoint**: Complete repository archived with rationale documentation.

---

## Phase 2: PKGBUILD Metadata Parser (4 hours)

**Purpose**: Extract tool metadata from 4,599 PKGBUILD files.

**Files**: Archive `experimental-archive/blackarch/packages/*/PKGBUILD`

- [ ] T008 Design PKGBUILD parser: Python script to parse Bash PKGBUILD syntax
- [ ] T009 [P] Extract basic fields: pkgname, pkgver, pkgrel, pkgdesc, arch
- [ ] T010 [P] Extract source information: url, source array, upstream project links
- [ ] T011 [P] Extract dependencies: depends, makedepends, optdepends arrays
- [ ] T012 [P] Extract licensing: license field, custom license handling
- [ ] T013 Handle edge cases: VCS packages (-git, -svn suffixes), epoch versions, custom variables
- [ ] T014 Parse category assignments: Cross-reference with lists/groups file
- [ ] T015 Error handling: Skip broken/malformed PKGBUILD files, log parsing failures
- [ ] T016 Validation: Test parser on sample of 50 packages (varied categories), verify accuracy
- [ ] T017 Bulk extraction: Run parser across all 4,599 PKGBUILD files, export to JSON

**Checkpoint**: Complete tool metadata extracted (JSON format).

---

## Phase 3: Category System Migration (2 hours)

**Purpose**: Port BlackArch's 49-category classification system.

**Files**: Archive `experimental-archive/blackarch/lists/groups`

- [ ] T018 Extract category definitions: Parse lists/groups file (49 categories)
- [ ] T019 Create category hierarchy: Map relationships (all tools → specific categories → meta-categories)
- [ ] T020 [P] Category metadata: Document each category purpose (webapp, forensic, scanner, etc.)
- [ ] T021 Validation: Ensure all 2,865 tools assigned to at least one category
- [ ] T022 Category statistics: Count tools per category, identify largest/smallest groups

**Checkpoint**: Category system documented and validated.

---

## Phase 4: Tool Database Schema (2 hours)

**Purpose**: Create PostgreSQL schema for tool catalog.

**Target**: `apps/security-service/src/tool-catalog/models.py`

- [ ] T023 Design Tool model: Fields for name, version, description, category, architecture, dependencies, source_url, homepage, license
- [ ] T024 Design Category model: Fields for name, description, tool_count, meta_group
- [ ] T025 Design relationship: Many-to-many (tools can belong to multiple categories)
- [ ] T026 [P] Create database migration: Alembic migration for tool catalog tables
- [ ] T027 [P] Indexes: Add indexes on tool_name, category, architecture for fast search
- [ ] T028 Seed database: Import extracted metadata from Phase 2 (4,599 tools)
- [ ] T029 Validation queries: Test search by name, category, architecture

**Checkpoint**: Tool catalog database populated with 2,865 tools.

---

## Phase 5: Discovery API (4 hours)

**Purpose**: Build FastAPI endpoints for tool search and browsing.

**Target**: `apps/security-service/src/tool-catalog/api.py`

- [ ] T030 Endpoint: `GET /api/tools` - List all tools (paginated, filterable by category/arch)
- [ ] T031 Endpoint: `GET /api/tools/{tool_name}` - Get detailed tool information
- [ ] T032 Endpoint: `GET /api/tools/search?q=<query>` - Full-text search by name/description
- [ ] T033 Endpoint: `GET /api/categories` - List all 49 categories with tool counts
- [ ] T034 Endpoint: `GET /api/categories/{category}/tools` - Get tools in specific category
- [ ] T035 [P] Pagination: Implement cursor-based pagination for large result sets
- [ ] T036 [P] Filtering: Support multi-category filter, architecture filter, license filter
- [ ] T037 Sorting: Support sort by name (alpha), popularity (install count), date added
- [ ] T038 Response caching: Cache category lists and popular searches (Redis)
- [ ] T039 API documentation: OpenAPI/Swagger docs with examples

**Checkpoint**: Fully functional tool discovery API.

---

## Phase 6: Web UI Components (6 hours)

**Purpose**: Build tool catalog browser in jane-ui.

**Target**: `apps/jane-ui/src/features/security/tool-catalog/`

- [ ] T040 Category browser: Grid view of 49 categories with icons and tool counts
- [ ] T041 Tool list view: Table with name, description, version, category, architecture
- [ ] T042 Tool detail view: Full information display (dependencies, license, source URL, installation command)
- [ ] T043 Search interface: Real-time search with auto-complete (debounced)
- [ ] T044 [P] Filters: Category multi-select, architecture filter, license filter
- [ ] T045 [P] Sorting controls: Sort by name, category, version
- [ ] T046 Installation instructions: Generate BlackArch installation commands (`pacman -S <tool>`)
- [ ] T047 Alternative installation: Links to upstream project source (for non-Arch users)
- [ ] T048 Accessibility: WCAG 2.1 AA compliance (keyboard navigation, screen reader support)
- [ ] T049 Performance: Virtualized list for 2,865 tools (<200ms rendering)

**Checkpoint**: Tool catalog UI complete and responsive.

---

## Phase 7: Optional Enhancement - Installation Helper (4 hours)

**Purpose**: Provide Docker-based isolated tool installation (optional).

**Target**: `apps/security-service/src/tool-catalog/installer.py`

- [ ] T050 [OPTIONAL] Docker integration: Create BlackArch base image
- [ ] T051 [OPTIONAL] Installation API: Endpoint to install tool in Docker container
- [ ] T052 [OPTIONAL] Container management: Start/stop tool containers
- [ ] T053 [OPTIONAL] Volume mapping: Persist tool data/results
- [ ] T054 [OPTIONAL] Security sandbox: Isolate tools from host system

**Checkpoint**: Optional Docker-based tool sandbox (skip if not needed).

---

## Phase 8: Documentation & Testing (2 hours)

**Purpose**: Finalize documentation and validate integration.

- [ ] T055 API documentation: Complete FastAPI auto-docs with usage examples
- [ ] T056 User guide: How to browse tool catalog, search tools, view installation instructions
- [ ] T057 Archive documentation: Update experimental-archive/blackarch/README.md with integration approach
- [ ] T058 Integration tests: Test API endpoints with realistic queries
- [ ] T059 UI testing: Validate search, filter, sort, pagination functionality
- [ ] T060 Performance testing: Load 2,865 tools, measure response times (<500ms)
- [ ] T061 Accessibility testing: Screen reader compatibility, keyboard navigation

**Checkpoint**: Complete documentation and validated integration.

---

## Summary Statistics

**⚠️ OUTDATED - REQUIRES UPDATE FOR BULK DOWNLOAD**

**Original Plan** (Metadata Extraction Only):
- Total Tasks: 61  
- Estimated Hours: 26
- Code Migrated: 0 LOC
- Tools: Browsable catalog only

**REVISED Plan** (Bulk Download + Local Installation):
- Total Tasks: ~95 (needs rewrite)
- Estimated Hours: 70
- Storage Required: 200 GB (local mirror)
- Setup Time: 3-5 hours (one-time bulk download)
- Code Migrated: PKGBUILD parser, bulk downloader, Docker installer, discovery UI
- Tools: 2,865 installable from local cache (100% offline)
- Categories: 49 (full taxonomy preserved)
- Performance: <100ms search, 1-5min local builds
- Future-Proofing: Survives upstream abandonment, zero external dependencies

---

## Comparison to Other Projects

| Project      | Migration Type        | Tasks | Hours | Storage | Key Deliverable |
| ------------ | --------------------- | ----- | ----- | ------- | --------------- |
| APIScout     | Full migration        | 82    | 37    | ~50 MB  | Windows PE analysis service |
| Actual Budget| Full migration        | 82    | 60    | ~100 MB | Personal finance web app |
| **BlackArch**| **Bulk download + local install** | **~95** | **70** | **200 GB** | **2,865 offline-installable security tools** |

**Key Difference**: BlackArch is infrastructure (like APT/YUM), but bulk download approach preserves 2,865 tools for offline installation - critical for future-proofing and air-gapped environments. Higher effort justified by 411x tool expansion (7 core → 2,865 total).

---

## Post-Flight Checklist ✅

**Verify these conditions before marking parent task complete**:

- [ ] All tasks T001-T061 marked complete above
- [ ] Archive complete: `experimental-archive/blackarch/` contains all code with documentation
- [ ] Archive documentation complete: INDEX.md, README.md, REVIVAL-GUIDE.md, MANIFEST.txt
- [ ] Metadata extraction complete: 2,865 tools parsed from 4,599 PKGBUILD files
- [ ] Database populated: Tool catalog database contains all tools with categories
- [ ] API functional: `pytest tests/security/tool-catalog/ -v` (100% pass rate)
- [ ] Web UI operational: Tool catalog browser functional in jane-ui
- [ ] Search working: Full-text search returns relevant results (<500ms)
- [ ] Categories validated: All 49 categories display with accurate tool counts
- [ ] Installation instructions: BlackArch installation commands generated correctly
- [ ] Performance met: Catalog browsing <200ms, search <500ms
- [ ] Accessibility: WCAG 2.1 AA validated (keyboard navigation, screen reader support)
- [ ] Migration validation documented in `migration-validation.md`
- [ ] No actual code migrated (metadata extraction only, as intended)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:

1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/tool-catalog/ -v --cov=apps.security_service.src.tool_catalog`
3. Document completion in `migration-validation.md`:

```markdown
### BlackArch Integration (T106)

- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Approach**: Metadata extraction (NOT code migration)
- **Estimated Hours**: 26
- **Actual Hours**: [ACTUAL]
- **Code Migrated**: 0 LOC (infrastructure archived, metadata extracted)
- **Tools Accessible**: 2,865 tools in catalog
- **Categories**: 49 (complete taxonomy)
- **Archive**: 100% (4,599 PKGBUILD + 5,804 LOC scripts)
- **Time Saved**: 174-274 hours (avoided reinventing package management)
- **Tests**: [PASSED]/[TOTAL] passed
- **Performance**: Catalog <200ms, search <500ms
- **Notes**: BlackArch is package repository infrastructure (like APT/YUM) - metadata extraction provides tool discovery without pointless infrastructure migration. Archive contains complete repository for reference.
```

4. Mark parent task T106 complete in `tasks.md`
5. Proceed to return task T107 in `tasks.md`

---

## Final Validation Matrix

| Component                 | Target                       | Status |
| ------------------------- | ---------------------------- | ------ |
| Archive Completeness      | 100% (all code archived)     | ⏳     |
| Archive Documentation     | 4 files (INDEX, README, REVIVAL, MANIFEST) | ⏳ |
| Metadata Extraction       | 2,865 tools parsed           | ⏳     |
| Category System           | 49 categories preserved      | ⏳     |
| Database Population       | All tools imported           | ⏳     |
| API Functionality         | All endpoints operational    | ⏳     |
| Web UI Completeness       | Browse, search, filter working | ⏳   |
| Search Performance        | <500ms                       | ⏳     |
| Catalog Performance       | <200ms                       | ⏳     |
| Accessibility Compliance  | WCAG 2.1 AA                  | ⏳     |
| Zero Code Migrated        | Verified (metadata only)     | ⏳     |
| Installation Commands     | Correctly generated          | ⏳     |

**Success Criteria**: All table rows marked ✅ before marking parent task complete.

---

## Key Learnings for Remaining Projects

**When to Use Bulk Download Strategy**:

1. **Package Repositories**: Projects that aggregate/distribute other tools (not implement them)
2. **Future-Proofing Critical**: Risk of upstream abandonment threatens long-term value
3. **Offline Capability Required**: Air-gapped deployments, secure environments
4. **Large Tool Collections**: Significant catalog (hundreds/thousands of tools)
5. **Storage Acceptable**: Modern hardware can accommodate download size

**BlackArch Pattern Evolution**:
- ❌ INITIAL: "Archive everything" (metadata-only) - missed strategic value
- ✅ REVISED: "Bulk download + local install" - preserves tools, enables offline use
- **Lesson**: Infrastructure projects may have hidden value in their CATALOG, not code

**For Remaining 35 Projects**: Evaluate if project is:
- ✅ **Application/Tool**: Migrate algorithms + business logic (e.g., CyberChef, MISP)
- ✅ **Tool Aggregator**: Bulk download catalog if future-proofing critical (e.g., BlackArch)
- ❌ **Pure Infrastructure**: Archive if no catalog value (e.g., build scripts only)

**BlackArch's Strategic Value**: 
- 411x tool expansion (7 core security tools → 2,865 total)
- Frozen snapshot (Nov 9, 2025) survives upstream abandonment
- Offline installation capability (air-gapped deployments)
- Acceptable storage trade-off: 200 GB for 2,865 tools
- 70 hours effort justified by long-term future-proofing
- [ ] Security audit passed (if applicable)
- [ ] Accessibility compliance maintained (WCAG 2.1 AA)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:
1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/test_blackarch_integration.py`
3. Document completion in `migration-validation.md`
4. Mark parent task TXXX complete in `tasks.md`
5. Proceed to return task (next in sequence) in `tasks.md`

**Documentation Update Required**:
```markdown
# In migration-validation.md

### BlackArch Migration (TXXX)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: XX
- **Actual Hours**: XX
- **Tests**: X passed, 0 failed
- **Performance**: All baselines met/exceeded
- **Notes**: [Any notable achievements or challenges]
```

