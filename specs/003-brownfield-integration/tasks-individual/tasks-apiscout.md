---
description: "APIScout: Windows API import recovery and malware analysis tool migration"
parent_task: "../tasks.md#T105"
parent_phase: "Phase 5: Security Domain Migrations"
return_to: "../tasks.md#T106"
domain: "security"
target_service: "apps/security-service/src/"
legacy_path: "features/apiscout"
estimated_hours: 22
critical_algorithms: 3  # API resolution, ApiVector compression, memory crawling
cli_tools: 4  # scout.py, match.py, collect.py, export.py
archive_files: 5  # IDA/Ghidra plugins (920 LOC saved)
time_saved_by_archive: 20  # 18-26 hours not migrating IDE plugins
---

# Tasks: APIScout - Windows API Analysis Tool

**⬆️ PARENT TASK**: [`tasks.md#T105`](../tasks.md#T105)  
**⬇️ RETURN TO**: [`tasks.md#T106`](../tasks.md#T106)

---

**Handoff Context**

**Called From**: `tasks.md` Phase 5, Task T105  
**Entry Condition**: Security service foundation ready (Phase 1-4 complete)  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark T105 complete in parent `tasks.md`, proceed to T106

**Handoff Protocol**: See [`HANDOFF-PROTOCOL.md`](./HANDOFF-PROTOCOL.md) for complete workflow documentation.

---

## Project Overview

**Type**: Windows API import recovery and malware analysis tool  
**Language**: Python 3.12 (legacy: Python 2.7/3.x)  
**Domain**: Security - malware analysis, forensics, threat intelligence  
**Size**: ~10,723 LOC across 34 Python files + 920 LOC archived (IDE plugins)

**Core Functionality**:

- API address resolution from memory dumps (O(1) lookup via hash maps)
- ApiVector compression using run-length encoding (WinAPI 1024 standard)
- Memory crawling for Windows API references (O(n*m) pattern matching)
- Malpedia integration for malware family classification
- CLI tools for analysis, matching, and collection building

**Critical Algorithms** (from analysis Section 4.1):

1. **API Address Resolution** (`ApiScout.py::crawl()`): O(1) lookup using pre-built hash maps from API databases
2. **ApiVector Compression** (`ApiVector.py::getVectorFromApiList()`): Run-length encoding for compact representation
3. **Memory Crawling** (`ApiScout.py::crawl()`): Sliding window pattern matching across memory dumps

**Integrations**:

- Malpedia API (malware intelligence)
- LIEF library (PE parsing)
- NumPy/SciPy (vector operations)
- Optional: IDA Pro, Ghidra (ARCHIVED - see experimental-archive/apiscout/)

**Archive Decision**: 5 IDE plugin files (920 LOC) archived to `experimental-archive/apiscout/`:

- `ida_scout.py`, `IdaProxy.py`, `IdaTools.py`, `IdaForm.py` (IDA Pro plugins)
- `GhidraScout.java` (Ghidra plugin)
- **Rationale**: Low business value (3-4/10), high migration cost (18-26 hours), better web UI alternative exists
- **Time Saved**: 20 hours (migration + testing avoided)
- **Functionality Preserved**: 100% via CLI tools (`scout.py`, `match.py`) + planned web UI

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/security-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/apiscout/` accessible with Python 3.12
- [ ] Dependencies: numpy, lief, Pillow, requests installed
- [ ] Archive decision documented: `experimental-archive/apiscout/` created with IDE plugins
- [ ] Test data: `tests/example_dump.bin`, `tests/minimal_db.json` available

**⚠️ If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## Phase 1: Environment Setup & Archive Preparation (3 hours)

**Purpose**: Validate legacy functionality and create experimental archive for IDE plugins.

- [ ] T001 Validate legacy environment: Install dependencies, run `pytest tests/` (should pass all existing tests)
- [ ] T002 Baseline performance: Run `scout.py tests/example_dump.bin dbs/*.json` and document execution time (<5s for 2MB dump)
- [ ] T003 [P] Create experimental archive structure: `experimental-archive/apiscout/` with required documentation files
- [ ] T004 [Archive] Move IDE plugins to archive: `ida_scout.py`, `IdaProxy.py`, `IdaTools.py`, `IdaForm.py`, `GhidraScout.java` (920 LOC)
- [ ] T005 [Archive] Create REVIVAL-GUIDE.md: Document IDA Pro/Ghidra setup process for potential future use
- [ ] T006 Create project structure: `apps/security-service/src/apiscout/` with subdirectories (core/, cli/, db/, utils/)
- [ ] T007 [P] Initialize test structure: `tests/security/apiscout/` with fixtures and test data

**Checkpoint**: Legacy system validated, IDE plugins archived, new structure ready.

---

## Phase 2: Core API Database Migration (4 hours)

**Purpose**: Migrate API database loading and management (critical foundation for all features).

**Files**: `apiscout/ApiScout.py` (database loading), `apiscout/db_builder/DatabaseBuilder.py`

- [ ] T008 [Ground Truth] Test legacy DB loading: Write test validating `ApiScout().loadDbFile()` behavior with minimal_db.json
- [ ] T009 [P] [Logic: ApiScout.py::loadDbFile] Port database loading logic: Preserve exact hash map structure, ASLR offset handling
- [ ] T010 [Logic: ApiScout.py::loadDbFile] API collision detection: Maintain collision counting and logging (Section 4.1: O(1) lookup requirement)
- [ ] T011 [P] Database schema migration: Create SQLite tables for API databases (dll, exports, base_address, aslr_offset fields)
- [ ] T012 [Logic: DatabaseBuilder.py::main] Port database builder: CLI tool for creating API databases from Windows DLLs
- [ ] T013 Validation: Compare hash maps between legacy and new implementation (exact key/value pairs)
- [ ] T014 Performance validation: Database loading <100ms for typical 50MB database (vs. legacy baseline)

**Checkpoint**: API database loading migrated with O(1) lookup performance maintained.

---

## Phase 3: Critical Algorithm #1 - API Address Resolution (5 hours)

**Purpose**: Migrate core API crawling algorithm (highest priority from Section 4.1).

**Files**: `apiscout/ApiScout.py::crawl()`, `apiscout/PeTools.py`

- [ ] T015 [Ground Truth] Test legacy crawl: Write test proving `ApiScout().crawl(binary)` behavior with example_dump.bin
- [ ] T016 Algorithm analysis: Document sliding window algorithm, DWORD/QWORD pointer detection, bitness handling
- [ ] T017 [Logic: ApiScout.py::crawl] Port memory crawling loop: Exact 4-byte/8-byte sliding window with struct unpacking
- [ ] T018 [Logic: ApiScout.py::crawl] API candidate detection: Preserve exact pointer validation logic (base_address checks)
- [ ] T019 [Logic: ApiScout.py::crawl] Reference counting: Maintain exact reference tracking and offset calculation
- [ ] T020 [Logic: PeTools.py::getReferencesFromTo] Port PE analysis utilities: Import table parsing, section analysis
- [ ] T021 [P] LIEF integration: Preserve optional LIEF library support for enhanced PE parsing
- [ ] T022 Edge case handling: NULL pointers, overlapping addresses, ASLR offset edge cases
- [ ] T023 Validation: Exact API matches vs. legacy on 10 test dumps (100% identical results required)
- [ ] T024 Performance validation: Crawl speed >1MB/s (maintain legacy performance for <1s response time requirement)

**Checkpoint**: API crawling algorithm migrated with functional and performance parity.

---

## Phase 4: Critical Algorithm #2 - ApiVector Compression (4 hours)

**Purpose**: Migrate WinAPI 1024 vector compression/decompression (Section 4.1).

**Files**: `apiscout/ApiVector.py`, `data/winapi1024v1.txt`

- [ ] T025 [Ground Truth] Test legacy vector compression: Validate `ApiVector().getVectorFromApiList()` with known API lists
- [ ] T026 [Logic: ApiVector.py::_loadWinApi1024] Port WinAPI 1024 loading: Exact rank-based sorting, DLL!function parsing
- [ ] T027 [Logic: ApiVector.py::getVectorFromApiList] Run-length encoding: Preserve exact compression algorithm (base64 encoding)
- [ ] T028 [Logic: ApiVector.py::getApiVectorFromVector] Vector decompression: Exact reverse algorithm maintaining fidelity
- [ ] T029 [P] NumPy optimization: Maintain optional NumPy acceleration for vector operations (10x speedup)
- [ ] T030 Base64 character mapping: Preserve custom base64 alphabet for compact representation
- [ ] T031 Validation: Compress/decompress 100 test vectors (100% reconstruction accuracy required)
- [ ] T032 Performance validation: Compression <10ms for 1024-element vector (maintain legacy speed)

**Checkpoint**: ApiVector compression migrated with perfect fidelity and performance.

---

## Phase 5: Critical Algorithm #3 - Memory Fingerprinting (3 hours)

**Purpose**: Migrate fingerprint crawler and QR code generation.

**Files**: `apiscout/FingerprintCrawler.py`, `apiscout/ApiQR.py`, `apiscout/ApiQRContext.py`

- [ ] T033 [Ground Truth] Test legacy fingerprinting: Validate `FingerprintCrawler().crawl()` with memory dumps
- [ ] T034 [Logic: FingerprintCrawler.py::crawl] Port fingerprint extraction: Exact API pattern detection algorithm
- [ ] T035 [Logic: ApiQR.py::generateApiQRCode] QR code generation: Preserve Pillow-based QR encoding
- [ ] T036 [Logic: ApiQRContext.py::getApiContextFromVector] Context extraction: API categorization by functionality
- [ ] T037 Validation: Fingerprint 20 malware samples (exact match vs. legacy fingerprints)
- [ ] T038 Performance validation: Fingerprinting <500ms per 10MB dump

**Checkpoint**: Memory fingerprinting migrated with functional parity.

---

## Phase 6: CLI Tools Migration (4 hours)

**Purpose**: Migrate 4 CLI tools preserving 100% functionality (no IDE plugins needed).

**Files**: `scout.py`, `match.py`, `collect.py`, `export.py`

- [ ] T039 [P] [Logic: scout.py::main] Port scout.py: Memory dump analysis CLI (argparse, filtering, JSON output)
- [ ] T040 [P] [Logic: match.py::main] Port match.py: Vector matching CLI (collection file support)
- [ ] T041 [P] [Logic: collect.py::main] Port collect.py: Collection building from sample directories
- [ ] T042 [P] [Logic: export.py::main] Port export.py: Export results in multiple formats (JSON, CSV, HTML)
- [ ] T043 [Ground Truth] Test all CLI tools: Run each with legacy test data, compare outputs byte-for-byte
- [ ] T044 Argument compatibility: Maintain exact CLI argument names and behaviors (backwards compatibility)
- [ ] T045 Output format preservation: JSON schema, CSV columns, HTML template exactly as legacy
- [ ] T046 Integration: Wire CLI tools to FastAPI endpoints for web-based execution

**Checkpoint**: All CLI tools migrated with CLI/web dual access.

---

## Phase 7: Malpedia Integration (2 hours)

**Purpose**: Migrate Malpedia API integration for malware family classification.

**Files**: `update.py` (Malpedia API client)

- [ ] T047 [Logic: update.py::download_apivector_db] Port Malpedia API client: Database download functionality
- [ ] T048 [Logic: update.py::check_malpedia_version] Version checking: Automated update detection
- [ ] T049 API key management: Environment variable support, secure credential handling
- [ ] T050 [P] Caching strategy: Local database caching to reduce API calls (7-day TTL)
- [ ] T051 Validation: Download test database, verify integrity and version metadata
- [ ] T052 Error handling: Network failures, rate limiting, authentication errors

**Checkpoint**: Malpedia integration migrated with caching and error resilience.

---

## Phase 8: Utility Modules Migration (2 hours)

**Purpose**: Migrate supporting utilities and helper functions.

**Files**: `apiscout/utility.py`, `apiscout/OrdinalHelper.py`, `apiscout/ImportTableLoader.py`

- [ ] T053 [P] [Logic: utility.py::*] Port utility functions: Logging, file I/O, data conversion helpers
- [ ] T054 [P] [Logic: OrdinalHelper.py::*] Port ordinal lookup: DLL export ordinal resolution
- [ ] T055 [P] [Logic: ImportTableLoader.py::*] Port import table parsing: PE import table extraction
- [ ] T056 Unit tests: Each utility function tested independently (>90% coverage)

**Checkpoint**: All utilities migrated and tested.

---

## Phase 9: Data Migration & Assets (1 hour)

**Purpose**: Migrate static data files and resources.

**Files**: `data/winapi1024v1.txt`, `data/winapi_contexts.csv`, `data/html_frame.html`, `dbs/`

- [ ] T057 Copy WinAPI 1024 data: Preserve exact file format and ranking
- [ ] T058 Copy API context data: Functionality categorization metadata
- [ ] T059 Copy HTML template: Preserve exact template for export.py HTML output
- [ ] T060 Database migration: Copy existing API database files to new structure
- [ ] T061 Validation: Verify file integrity (checksums match legacy files)

**Checkpoint**: All data assets migrated and validated.

---

## Phase 10: Testing & Validation (3 hours)

**Purpose**: Comprehensive testing ensuring functional parity.

- [ ] T062 Unit tests: Achieve >85% coverage for all migrated modules (pytest-cov)
- [ ] T063 Integration tests: End-to-end workflows (upload dump → crawl → export)
- [ ] T064 Ground truth validation: Run 50 test dumps through legacy and new systems (exact match required)
- [ ] T065 Performance regression: Validate all performance baselines maintained or improved
- [ ] T066 [P] Edge case testing: NULL pointers, corrupted dumps, invalid databases, network failures
- [ ] T067 CLI compatibility: Test all CLI argument combinations (backwards compatibility)
- [ ] T068 Web UI testing: FastAPI endpoint testing (file upload, streaming results, error handling)

**Checkpoint**: All tests passing, functional parity validated.

---

## Phase 11: Web UI & UX Enhancements (4 hours)

**Purpose**: Build web-based alternative to archived IDE plugins.

**Target**: `apps/jane-ui/src/features/security/apiscout/`

- [ ] T069 Design upload interface: Drag-drop memory dump upload (<200ms interaction time)
- [ ] T070 API integration: Connect to FastAPI endpoints (scout, match, export)
- [ ] T071 Results visualization: Table view replicating IDA/Ghidra plugin UI (API list, references, DLLs)
- [ ] T072 Export controls: JSON, CSV, HTML download buttons
- [ ] T073 [P] Performance optimization: Streaming results for large dumps (>100MB)
- [ ] T074 [P] Executive function accommodations: Focus indicators, keyboard navigation, WCAG 2.1 AA compliance
- [ ] T075 Real-time progress: WebSocket updates during analysis (estimated time remaining)
- [ ] T076 Accessibility: Screen reader support, color contrast, focus management

**Checkpoint**: Web UI providing superior UX to archived IDE plugins.

---

## Phase 12: Documentation & Production Polish (2 hours)

**Purpose**: Finalize documentation and deployment preparation.

- [ ] T077 API documentation: FastAPI auto-generated docs + custom examples
- [ ] T078 User guide: Web UI walkthrough, CLI tool reference
- [ ] T079 Migration notes: Document changes from legacy (minimal - 95%+ compatibility)
- [ ] T080 Archive documentation: Update experimental-archive/apiscout/README.md with final stats
- [ ] T081 Performance documentation: Document all baselines and validation results
- [ ] T082 Deployment guide: Docker configuration, environment variables, database setup

**Checkpoint**: Complete documentation and deployment readiness.

---

## Summary Statistics

**Total Tasks**: 82  
**Estimated Hours**: 37 (vs. original 25 + 20 saved from archive = 45 hours, net 8 hours under budget)  
**Archive Savings**: 20 hours (IDE plugins not migrated)  
**Critical Algorithms**: 3 (all migrated with functional parity)  
**CLI Tools**: 4 (all migrated with CLI + web access)  
**Test Coverage**: >85% (maintaining legacy quality standards)  
**Performance**: All baselines maintained (<1s security domain requirement)  
**Functionality Preserved**: 100% (archive + migration strategy)

---

## Post-Flight Checklist ✅

**Verify these conditions before marking parent task complete**:

- [ ] All tasks T001-T082 marked complete above
- [ ] Integration tests pass: `pytest tests/security/apiscout/ -v` (100% pass rate)
- [ ] Performance baselines met: API crawling >1MB/s, database loading <100ms, vector compression <10ms
- [ ] Ground truth validation: 50 test dumps produce identical results vs. legacy (100% match)
- [ ] CLI compatibility: All 4 CLI tools (`scout`, `match`, `collect`, `export`) function identically to legacy
- [ ] Web UI functional: Upload, analyze, visualize, export workflows complete
- [ ] Archive validated: `experimental-archive/apiscout/` contains 5 IDE plugin files with documentation
- [ ] Legacy `features/apiscout/` backed up to `archive/` (excluding archived IDE plugins)
- [ ] Migration completion documented in `migration-validation.md`
- [ ] No regressions in existing security-service functionality
- [ ] Test coverage >85% across all migrated modules
- [ ] Accessibility compliance: WCAG 2.1 AA validated for web UI
- [ ] Performance validation: <1s response time maintained (security domain requirement)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:

1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/apiscout/ -v --cov=apps.security_service.src.apiscout --cov-report=term-missing`
3. Document completion in `migration-validation.md`:

```markdown
### APIScout Migration (T105)

- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: 37
- **Actual Hours**: [ACTUAL]
- **Tests**: [PASSED]/[TOTAL] passed (>85% coverage)
- **Performance**: All baselines met (crawl >1MB/s, DB load <100ms, vector <10ms)
- **Archive**: 5 IDE plugin files (920 LOC, 20 hours saved)
- **Functionality Preserved**: 100% (CLI + web UI)
- **Ground Truth Validation**: 50 dumps tested, 100% match
- **Notes**: Web UI provides superior UX to archived IDE plugins, all critical algorithms migrated with functional parity
```

4. Mark parent task T105 complete in `tasks.md`
5. Proceed to return task T106 in `tasks.md`

---

**Final Validation Matrix**:

| Component              | Legacy Baseline      | New Implementation | Status |
| ---------------------- | -------------------- | ------------------ | ------ |
| API Database Loading   | <100ms (50MB)        | [MEASURED]         | ⏳     |
| Memory Crawling        | >1MB/s               | [MEASURED]         | ⏳     |
| Vector Compression     | <10ms (1024 elem)    | [MEASURED]         | ⏳     |
| Ground Truth Accuracy  | 100% (reference)     | [MEASURED]         | ⏳     |
| Test Coverage          | 75% (legacy)         | >85% (target)      | ⏳     |
| CLI Compatibility      | 4/4 tools            | [MEASURED]         | ⏳     |
| Web UI Responsiveness  | N/A (new feature)    | <200ms             | ⏳     |
| Security Response Time | <1s (domain req)     | [MEASURED]         | ⏳     |
| Archive Completeness   | 5 files (920 LOC)    | [VERIFIED]         | ⏳     |
| Malpedia Integration   | Functional           | [TESTED]           | ⏳     |

**Success Criteria**: All table rows marked ✅ before marking parent task complete.

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

**Verify these conditions before marking parent task complete**:

- [ ] All tasks T001-TXXX marked complete above
- [ ] Integration tests pass: `pytest tests/security/test_apiscout_integration.py`
- [ ] Performance baselines met (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm functional parity with legacy
- [ ] Legacy `features/apiscout/` backed up to `archive/`
- [ ] Migration completion documented in `migration-validation.md`
- [ ] All analysis findings from project_analysis_report.md addressed
- [ ] No regressions in existing functionality
- [ ] Security audit passed (if applicable)
- [ ] Accessibility compliance maintained (WCAG 2.1 AA)

**⚠️ If any checklist item fails**: DO NOT mark parent task complete. Fix issues and re-validate.

**Completion Action**:
1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/test_apiscout_integration.py`
3. Document completion in `migration-validation.md`
4. Mark parent task TXXX complete in `tasks.md`
5. Proceed to return task (next in sequence) in `tasks.md`

**Documentation Update Required**:
```markdown
# In migration-validation.md

### APIScout Migration (TXXX)
- **Status**: ✅ Complete
- **Completed**: [DATE]
- **Estimated Hours**: XX
- **Actual Hours**: XX
- **Tests**: X passed, 0 failed
- **Performance**: All baselines met/exceeded
- **Notes**: [Any notable achievements or challenges]
```

