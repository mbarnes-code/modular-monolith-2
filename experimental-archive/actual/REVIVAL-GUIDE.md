# Revival Guide - Experimental Features

**Quick reference for bringing archived features back into active migration**

---

## Quick Decision Matrix

| Feature | When to Revive | Estimated Effort | Prerequisites |
|---------|----------------|------------------|---------------|
| **Electron Desktop** | Desktop app requirement | 8-10 hours | Migration complete, FastAPI stable |
| **Plugin System** | Upstream ships API | 8-10 hours | Actual v26+ with plugin support |
| **Platform Layer** | Multi-runtime needed | 3-4 hours | TypeScript services coexist |

---

## Revival Process Template

### Step 1: Validate Need

**Questions to Ask**:
- [ ] Is this feature available in upstream Actual Budget?
- [ ] Have users explicitly requested this capability?
- [ ] Does it provide value beyond current 82-task migration?
- [ ] Can we achieve the goal without this feature?

**Go/No-Go**: Only proceed if answering YES to questions 1-3.

---

### Step 2: Review Archived Code

**Electron Desktop**:
```bash
cd /workspaces/modular-monolith-2/features/actual/.experimental-archive
less desktop-electron/index.ts          # Main process
less desktop-electron/preload.ts        # Renderer preload
less desktop-electron/menu.ts           # Native menus
less desktop-electron/package.json      # Dependencies
```

**Plugin System**:
```bash
less plugins-service/src/plugin-service-worker.ts  # Service worker
less plugins-service/package.json                   # Dependencies
# Check upstream: https://github.com/actualbudget/actual/issues/4049
```

**Platform Layer**:
```bash
ls -la platform/server/    # Server adapters
ls -la platform/client/    # Client adapters
```

---

### Step 3: Create Migration Tasks

**Template**: Copy from `tasks-actual.md` Phase structure

```markdown
## Phase 16: [Feature Name] Revival

**Objective**: Integrate [archived feature] into migrated architecture

### Tasks

- [ ] **T083** [Analysis] Review archived code for API changes
  - **Legacy**: `.experimental-archive/[feature]/`
  - **Analysis**: Compare with current upstream (v25.10.0 → latest)
  - **Output**: List breaking changes, deprecated APIs
  - **Validation**: Document all differences

- [ ] **T084** [Environment] Setup [feature] dependencies
  - **Target**: `apps/productivity-service/` or `apps/jane-ui/`
  - **Dependencies**: [List from package.json]
  - **Validation**: Dependencies install without conflicts

- [ ] **T085** [Integration] Connect to migrated services
  - **Target**: Replace IPC/platform calls with FastAPI/WebSocket
  - **Legacy**: [Original implementation path]
  - **Validation**: Feature works with migrated backend

- [ ] **T086** [Testing] Validate feature parity
  - **Ground Truth**: Test against archived version
  - **Validation**: All capabilities preserved
```

---

### Step 4: Effort Estimation

#### Electron Desktop Revival

**Phase 16: Desktop Electron Wrapper** (8-10 hours)

| Task | Description | Hours |
|------|-------------|-------|
| T083 | Analyze Electron version changes | 1 |
| T084 | Setup electron + electron-builder | 1 |
| T085 | Replace IPC with HTTP/WebSocket | 3 |
| T086 | Native file dialogs integration | 1 |
| T087 | OAuth redirect server | 1 |
| T088 | Window state persistence | 0.5 |
| T089 | Native menus | 0.5 |
| T090 | Platform-specific packaging | 2 |
| **Total** | | **10 hours** |

**Dependencies**:
- electron ^38.3.0
- electron-builder ^26.0.12
- better-sqlite3 ^12.4.1

**Integration Points**:
- Replace `serverProcess.postMessage()` → `fetch('http://localhost:8000/api')`
- Replace IPC → WebSocket (`ws://localhost:8000/ws`)
- File dialogs → Multi-part form upload to FastAPI

---

#### Plugin System Revival

**Phase 16: Plugin System** (8-10 hours)

**PREREQUISITES** ⚠️:
1. Upstream Actual Budget completes plugin API (issue #4049)
2. Example plugins exist for reference
3. Plugin security model documented

| Task | Description | Hours |
|------|-------------|-------|
| T083 | Review upstream plugin API | 1 |
| T084 | Migrate service worker | 2 |
| T085 | Create plugin API bridge | 3 |
| T086 | Plugin loading mechanism | 2 |
| T087 | Plugin sandbox/security | 2 |
| **Total** | | **10 hours** |

**Check Upstream First**:
```bash
# Before starting, verify upstream status
curl -s https://api.github.com/repos/actualbudget/actual/issues/4049 | jq '.state'
# If "closed", proceed. If "open", wait.
```

---

#### Platform Layer Revival

**Phase 16: Platform Abstraction** (3-4 hours)

**USE CASE**: Only if running TypeScript services alongside Python

| Task | Description | Hours |
|------|-------------|-------|
| T083 | Create TypeScript interop layer | 2 |
| T084 | Map platform APIs to Python | 1 |
| T085 | Test cross-runtime calls | 1 |
| **Total** | | **4 hours** |

**Note**: Most platform needs already covered by Python stdlib (see README.md)

---

### Step 5: Update Migration Metadata

**In `tasks-actual.md`**:

```diff
 estimated_hours: 60
+revival_hours: 10  # If Electron/Plugins added
```

**Update Post-Flight Checklist**:

```diff
+- [ ] **Revival Feature Complete**: [Feature name] validated
+  - [ ] Ground truth tests passing
+  - [ ] Integration with migrated services verified
+  - [ ] User documentation updated
```

---

### Step 6: Testing Strategy

#### Electron Desktop Testing

1. **Ground Truth**: Run legacy Electron app
2. **Migrated**: Run new Electron wrapper → migrated backend
3. **Compare**:
   - File dialogs work
   - OAuth redirect works
   - Window state persists
   - Native menus functional

#### Plugin System Testing

1. **Ground Truth**: Test upstream plugin example (if available)
2. **Migrated**: Load same plugin in migrated app
3. **Compare**:
   - Plugin loads
   - Plugin API calls work
   - Theme customization works
   - Security sandbox enforced

---

## Integration Examples

### Electron → FastAPI Integration

**Before (IPC)**:
```typescript
// desktop-electron/index.ts
serverProcess.postMessage({
  type: 'load-budget',
  budgetId: '123'
});
```

**After (HTTP)**:
```typescript
// desktop-electron/index.ts
fetch('http://localhost:8000/api/budgets/123', {
  method: 'GET',
  headers: { 'Authorization': `Bearer ${token}` }
});
```

---

### Plugin → Service Integration

**Before (Message Channel)**:
```typescript
// plugin-service-worker.ts
client.postMessage(
  { type: 'plugin-files', eventData: { pluginUrl: slug } },
  [channel.port2]
);
```

**After (HTTP + WebSocket)**:
```typescript
// Register plugin with backend
await fetch('http://localhost:8000/api/plugins/register', {
  method: 'POST',
  body: JSON.stringify({ slug, manifest })
});

// Subscribe to plugin updates
const ws = new WebSocket('ws://localhost:8000/ws/plugins');
ws.onmessage = (event) => {
  // Handle plugin events
};
```

---

## Common Pitfalls

### Electron

❌ **Don't**: Keep utility process spawning  
✅ **Do**: Connect to existing FastAPI server

❌ **Don't**: Use Node.js better-sqlite3  
✅ **Do**: Use HTTP API to Python SQLite service

❌ **Don't**: Replicate backend logic  
✅ **Do**: Thin client, all logic in productivity-service

### Plugins

❌ **Don't**: Start before upstream ready  
✅ **Do**: Wait for Actual v26+ with plugin API

❌ **Don't**: Allow arbitrary code execution  
✅ **Do**: Implement CSP sandbox, permission model

❌ **Don't**: Store plugins in service worker only  
✅ **Do**: Backend plugin registry with versioning

### Platform

❌ **Don't**: Port all platform adapters  
✅ **Do**: Only port what Python doesn't provide

❌ **Don't**: Maintain two implementations  
✅ **Do**: Use Python as source of truth

---

## Success Criteria

### Electron Revival Complete When:
- [ ] Desktop app launches successfully
- [ ] Connects to productivity-service FastAPI
- [ ] File dialogs work for import/export
- [ ] OAuth redirect completes for bank connections
- [ ] All 82 tasks still pass validation

### Plugin Revival Complete When:
- [ ] Example plugin loads from upstream
- [ ] Plugin API calls reach backend services
- [ ] Theme customization works
- [ ] Security audit passes
- [ ] All 82 tasks still pass validation

### Platform Revival Complete When:
- [ ] TypeScript services call Python services
- [ ] Cross-runtime data serialization works
- [ ] No business logic duplicated
- [ ] All 82 tasks still pass validation

---

## Questions Before Revival

1. **Why is this needed now?**
2. **Can we achieve the goal another way?**
3. **Is upstream ready (for plugins)?**
4. **Do we have 8-10 hours to invest?**
5. **Will this impact the 82 existing tasks?**

**If any answer is "No", consider waiting.**

---

## Contacts

- **Migration Lead**: See main project README
- **Actual Budget Upstream**: https://github.com/actualbudget/actual
- **Plugin Issue Tracker**: https://github.com/actualbudget/actual/issues/4049

---

**Remember**: These features were archived because they provided 0% business value for web deployment. Revive only when that calculus changes.
