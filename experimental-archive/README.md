# Experimental Archive

**Purpose**: Preserve non-essential features from all 38 projects for potential future exploration

**Created**: 2025-11-09  
**Location**: `/workspaces/modular-monolith-2/experimental-archive/`

---

## Overview

This directory contains features, components, and code from the brownfield migration that were excluded from the initial migration due to:
- **0% business value** for web deployment
- **Platform-specific** requirements not needed (Electron, React Native)
- **Incomplete features** in upstream projects (experimental flags, disabled features)
- **Better alternatives** in target stack (Python equivalents, modern libraries)

**Key Principle**: Archive preserves code for "maybe later" scenarios while keeping migration focused on essential functionality.

---

## Archive Structure

```
experimental-archive/
├── README.md                  ← This file (project-wide overview)
├── actual/                    ← Actual Budget non-essential features
│   ├── INDEX.md               ← Quick start for Actual archive
│   ├── README.md              ← Full Actual analysis
│   ├── REVIVAL-GUIDE.md       ← Revival instructions
│   ├── MANIFEST.txt           ← File inventory
│   ├── desktop-electron/      ← Electron desktop wrapper
│   ├── plugins-service/       ← Plugin system (incomplete)
│   └── platform/              ← Platform abstraction layer
├── [project-name]/            ← Future archives (CyberChef, MISP, etc.)
│   └── ...
└── [project-name]/
    └── ...
```

---

## Current Archives

### 1. Actual Budget (`actual/`)

**Archived**: 2025-11-09  
**Size**: 4.7MB, 154 files, ~1900 LOC  
**Time Saved**: 17-21 hours  

**Contents**:
- `desktop-electron/` - Electron desktop wrapper (4.4MB)
- `plugins-service/` - Plugin system (36KB, incomplete feature)
- `platform/` - Platform abstraction layer (240KB)

**Why Archived**:
- Electron: Web deployment doesn't need desktop packaging
- Plugins: Incomplete feature (disabled in upstream UI)
- Platform: Python has superior equivalents

**Revival Conditions**:
- Desktop distribution requirement emerges
- Upstream completes plugin API (issue #4049)
- Multi-runtime architecture needed

**Documentation**: See `actual/INDEX.md` for quick start

---

## Usage Guidelines

### When to Archive Features

**DO Archive**:
- ✅ Platform-specific packaging (Electron, React Native wrappers)
- ✅ Incomplete/experimental features (disabled in upstream)
- ✅ Features with better alternatives in target stack
- ✅ Features providing 0% business value for deployment target
- ✅ Edge case handlers that duplicate main functionality
- ✅ Legacy platform abstractions (when Python/modern equivalents exist)

**DON'T Archive**:
- ❌ Core business logic (algorithms, domain services)
- ❌ User-facing features (even if rarely used)
- ❌ Data models and schemas
- ❌ API endpoints and integrations
- ❌ Critical infrastructure (auth, sync, state management)
- ❌ Unique functionality without alternatives

### Archive Process

1. **Analyze**: Determine if feature is essential (use decision matrix below)
2. **Create Directory**: `mkdir experimental-archive/[project-name]/`
3. **Copy Code**: `cp -r features/[project]/[feature] experimental-archive/[project]/`
4. **Document**: Create INDEX.md, README.md, REVIVAL-GUIDE.md
5. **Update Tasks**: Document exclusion in migration tasks
6. **Validate**: Ensure migration coverage remains >90%

### Revival Process

1. **Validate Need**: Read archived README.md for context
2. **Check Upstream**: Verify feature status in original project
3. **Review Guide**: Follow REVIVAL-GUIDE.md in project directory
4. **Create Tasks**: Add Phase 16+ to migration task file
5. **Estimate**: Use archived documentation for effort estimates
6. **Integrate**: Connect to migrated services (not legacy code)

---

## Decision Matrix

Use this matrix to decide if a feature should be archived:

| Criteria | Archive? | Reason |
|----------|----------|--------|
| **Desktop packaging** (Electron, MSI, DMG) | ✅ Yes | Web deployment target |
| **Mobile wrappers** (React Native, Cordova) | ✅ Yes | Web-only deployment |
| **Platform abstractions** (if Python equivalent exists) | ✅ Yes | Better alternatives |
| **Experimental features** (disabled in UI) | ✅ Yes | Not ready upstream |
| **Incomplete features** (no API, no docs) | ✅ Yes | Can't migrate what doesn't work |
| **Plugin systems** (if no plugins exist) | ✅ Yes | No ecosystem to migrate |
| **Build tools** (webpack configs, package scripts) | ⚠️ Maybe | Depends on architecture |
| **Dev tooling** (linters, formatters) | ✅ Yes | Use target stack tools |
| **Core algorithms** | ❌ No | Essential business logic |
| **Data models** | ❌ No | Foundation of application |
| **User features** | ❌ No | Direct user value |
| **API integrations** | ❌ No | External dependencies |
| **Authentication/Authorization** | ❌ No | Security critical |

---

## Statistics

### Overall Archive Stats

| Metric | Actual Budget | [Project 2] | [Project 3] | Total |
|--------|---------------|-------------|-------------|-------|
| **Files** | 154 | TBD | TBD | 154 |
| **Size** | 4.7MB | TBD | TBD | 4.7MB |
| **LOC** | ~1900 | TBD | TBD | ~1900 |
| **Hours Saved** | 17-21 | TBD | TBD | 17-21 |
| **Value Lost** | 0% | TBD | TBD | 0% |

### Migration Coverage Impact

**Target**: Maintain >90% user-facing functionality coverage

| Project | Migration Coverage | Archive Size | Acceptable? |
|---------|-------------------|--------------|-------------|
| Actual Budget | 95%+ | 1900 LOC | ✅ Yes |
| [Project 2] | TBD | TBD | TBD |
| [Project 3] | TBD | TBD | TBD |

---

## Per-Project Documentation Standards

Each archived project MUST include:

### Required Files

1. **INDEX.md** - Quick start guide
   - What's archived and why
   - Quick decision matrix
   - Links to other docs

2. **README.md** - Full analysis
   - Detailed evaluation of each component
   - Cost-benefit analysis
   - What's lost vs. what's kept
   - Revival conditions

3. **REVIVAL-GUIDE.md** - Step-by-step instructions
   - When to revive
   - How to revive (task templates)
   - Effort estimates
   - Integration examples

4. **MANIFEST.txt** - File inventory
   - Complete file list
   - LOC counts
   - Dependencies
   - Checksums/verification

### Optional Files

- **ANALYSIS.md** - Technical deep-dive
- **BENCHMARKS.md** - Performance data
- **DEPENDENCIES.txt** - Package dependencies
- **MIGRATION-NOTES.md** - Lessons learned

---

## Archive Integrity

### Verification

Each project archive should be verified:

```bash
# Count files
find experimental-archive/[project]/ -type f | wc -l

# Check size
du -sh experimental-archive/[project]/

# Verify documentation
test -f experimental-archive/[project]/INDEX.md && echo "✅ INDEX.md exists"
test -f experimental-archive/[project]/README.md && echo "✅ README.md exists"
test -f experimental-archive/[project]/REVIVAL-GUIDE.md && echo "✅ REVIVAL-GUIDE.md exists"
test -f experimental-archive/[project]/MANIFEST.txt && echo "✅ MANIFEST.txt exists"
```

### Source Tracking

Each archive MUST document:
- Original repository URL
- Commit hash or version tag
- Archive date
- Reason for archival
- Revival conditions

---

## Examples

### Good Archive Candidates

1. **Electron Desktop Wrapper** (Actual Budget)
   - Pure packaging, 0 business logic
   - Web deployment doesn't need it
   - 8-10 hours saved

2. **React Native Mobile Wrapper** (Any Project)
   - Platform-specific, no shared logic
   - Web-only deployment
   - 10-15 hours saved

3. **Plugin System** (Incomplete Feature)
   - Disabled in UI, no API
   - Can't migrate what doesn't work
   - 4-5 hours saved

4. **Platform Abstraction** (When Python Equivalent Exists)
   - TypeScript wrappers for Node.js APIs
   - Python has better built-ins
   - 5-6 hours saved

### Bad Archive Candidates

1. ❌ **CRDT Sync Algorithm**
   - Core business logic
   - No alternative exists
   - User-critical feature

2. ❌ **Data Models**
   - Foundation of application
   - Required for any deployment
   - Migration essential

3. ❌ **API Integrations** (SimpleFIN, GoCardless)
   - External dependencies
   - User-facing features
   - Must migrate

4. ❌ **Authentication**
   - Security critical
   - No shortcuts available
   - Always migrate

---

## Future Considerations

### When Archives Grow

If `experimental-archive/` exceeds 100MB or 1000 files:

1. **Compress**: Create `.tar.gz` archives per project
2. **Remote Storage**: Move to S3/Azure Blob Storage
3. **Documentation Only**: Keep only docs in repo, link to storage
4. **Selective Cleanup**: Remove truly obsolete features

### When to Clean Up

**DO Delete**:
- Features obsolete in upstream (removed, deprecated)
- Projects abandoned (no upstream activity >2 years)
- Features definitively not needed (confirmed by stakeholders)

**DON'T Delete**:
- Recent archives (<1 year old)
- Features with active upstream development
- Uncertain future requirements
- Reference implementations

---

## Related Documentation

- **Migration Tasks**: `specs/003-brownfield-integration/tasks.md`
- **Individual Projects**: `specs/003-brownfield-integration/tasks-individual/`
- **Handoff Protocol**: `specs/003-brownfield-integration/HANDOFF-PROTOCOL.md`
- **Platform Analysis**: `/tmp/actual-platform-analysis.md` (example)

---

## Contact

See main project README for migration team contacts.

---

**Archive Principle**: Preserve today, decide tomorrow. Migration focuses on essentials; archive keeps options open.
