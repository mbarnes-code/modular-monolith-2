# Actual Budget - Experimental Archive

**Location**: `/workspaces/modular-monolith-2/experimental-archive/actual/`  
**Parent Archive**: `experimental-archive/` (project-wide)

---

## What's Here?

**~1900 LOC** of Actual Budget features excluded from migration due to **0% business value** for web deployment.

---

## Archive Contents

```
.experimental-archive/
├── README.md              # Full analysis (why archived, what's lost, when to revive)
├── REVIVAL-GUIDE.md       # Step-by-step revival instructions
├── MANIFEST.txt           # Archive inventory
├── desktop-electron/      # 4.4MB - Electron desktop wrapper (~682 LOC)
├── plugins-service/       # 36KB - Plugin system (INCOMPLETE, ~150 LOC)
└── platform/              # 240KB - Platform abstraction (~700 LOC)
```

**Total**: 154 files, 4.7MB

---

## Quick Reference

### What Got Archived?

1. **Electron Desktop** (desktop-electron/)
   - Desktop installers, native menus, file dialogs
   - OAuth redirect server, window management
   - **Why skipped**: Web deployment (0% value)
   - **Revival effort**: 8-10 hours

2. **Plugin System** (plugins-service/)
   - Service worker, Module Federation support
   - **Why skipped**: Incomplete feature (disabled in UI)
   - **Revival effort**: 8-10 hours (after upstream ready)

3. **Platform Layer** (platform/)
   - Node.js/Browser/React Native abstraction
   - **Why skipped**: Python has better equivalents
   - **Revival effort**: 3-4 hours

**Total saved**: 17-21 hours

---

### What's Still in Migration? (82 tasks)

✅ All business logic (spreadsheet, CRDT, import)  
✅ All user features (reports, bank sync, undo/redo)  
✅ All UI (React, Emotion, Redux)  
✅ All integrations (SimpleFIN, GoCardless)

**Coverage**: 95%+ of user-facing functionality

---

## How to Use

### Explore Archive

```bash
# View Electron implementation
cd /workspaces/modular-monolith-2/experimental-archive/actual
cat desktop-electron/index.ts

# View plugin service worker
cat plugins-service/src/plugin-service-worker.ts

# View platform adapters
ls -la platform/server/
```

### Revive a Feature

1. **Read**: `README.md` (context & analysis)
2. **Plan**: `REVIVAL-GUIDE.md` (step-by-step process)
3. **Decide**: Is effort worth it? (8-10 hours typically)
4. **Check**: Upstream status (especially for plugins)
5. **Create**: New tasks in `tasks-actual.md` Phase 16+

---

## Decision Matrix

| Need | Use Archive? | Alternative |
|------|-------------|-------------|
| Desktop installers | ✅ Yes (Electron) | Progressive Web App (PWA) |
| Offline-first | ✅ Yes (Electron) | Service Worker (already in migration) |
| Native file access | ✅ Yes (Electron) | Web File System API |
| Plugin system | ⏳ Wait | Upstream issue #4049 |
| Multi-platform | ❌ No (Platform) | Use Python stdlib |
| TypeScript + Python | ✅ Maybe (Platform) | FastAPI + React is enough |

---

## When NOT to Revive

- ❌ "Just because it's there"
- ❌ Before upstream ready (plugins)
- ❌ Without user demand
- ❌ If Python equivalent exists (platform)
- ❌ If it adds complexity without value

---

## Documentation Map

```
experimental-archive/
├── README.md                              ← Project-wide archive overview
└── actual/                                ← Actual Budget archive
    ├── INDEX.md                           ← YOU ARE HERE (quick start)
    ├── README.md                          ← Deep dive (why archived)
    ├── REVIVAL-GUIDE.md                   ← How to bring features back
    ├── MANIFEST.txt                       ← File inventory
    ├── desktop-electron/                  ← Archived code
    ├── plugins-service/                   ← Archived code
    └── platform/                          ← Archived code

Related (outside archive):
├── /tmp/actual-platform-analysis.md       ← Comprehensive evaluation
├── /tmp/actual-gaps-analysis.md           ← Second-pass findings
├── /tmp/actual-migration-final-summary.md ← Complete overview
└── specs/.../tasks-actual.md              ← 82 migration tasks
```

---

## Questions?

**"Should I revive Electron?"**  
→ Only if desktop distribution is required. Otherwise, use PWA.

**"Should I revive plugins?"**  
→ Wait for upstream (issue #4049). Feature is incomplete.

**"Should I revive platform layer?"**  
→ No, unless running TypeScript services. Python has better equivalents.

**"Will I lose functionality?"**  
→ No. 95%+ coverage in 82 tasks. Archive is non-essential.

---

## Stats

- **Archived**: 1900 LOC, 154 files, 4.7MB
- **Saved**: 17-21 hours migration effort
- **Lost**: 0% business value (web deployment)
- **Coverage**: 95%+ without archive

---

## Contact

See main project README for migration team contacts.

---

**Bottom Line**: Archive preserves code for "maybe later" scenarios. Current 82-task migration is complete without it.
