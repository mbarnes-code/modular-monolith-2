# Document Handoff Protocol

**Version**: 1.0.0  
**Last Updated**: 2025-11-09  
**Purpose**: Define the orchestration pattern for delegating work between top-level task orchestration and individual project migration task files.

---

## Overview

The handoff protocol enables hierarchical task delegation across multiple documentation levels:

1. **Top-Level Orchestration** (`tasks.md`) - Coordinates overall migration phases and delegates to individual projects
2. **Individual Project Tasks** (`tasks-individual/tasks-[project].md`) - Contains detailed migration tasks for specific legacy features
3. **Validation & Return** - Ensures completion before returning control to parent orchestration

This creates a "call stack" pattern where:
- Parent delegates to child → Child executes all tasks → Child validates completion → Control returns to parent

---

## Document Hierarchy

```
specs/003-brownfield-integration/
├── tasks.md                           # TOP-LEVEL ORCHESTRATOR
│   ├── Phase 1-4: Foundation (shared infrastructure)
│   ├── Phase 5: [HANDOFF] → Individual project migrations
│   │   ├── → tasks-individual/tasks-cyberchef.md
│   │   ├── → tasks-individual/tasks-maltrail.md
│   │   └── → tasks-individual/tasks-*.md (38 projects)
│   └── Phase N: Integration & polish
│
└── tasks-individual/                  # INDIVIDUAL PROJECT TASKS
    ├── tasks-cyberchef.md            # Detailed CyberChef migration
    ├── tasks-maltrail.md             # Detailed Maltrail migration
    └── ...                           # 38 total project files
```

---

## Handoff Mechanism

### 1. Parent Task Format (in `tasks.md`)

Parent tasks use the `[HANDOFF]` tag to delegate to individual project files:

```markdown
## Phase 5: Individual Project Migrations

### Phase 5.1: Security Domain Migrations

- [ ] T100 [HANDOFF] Migrate CyberChef
  - **File**: [`tasks-individual/tasks-cyberchef.md`](tasks-individual/tasks-cyberchef.md)
  - **Entry Condition**: Phase 1-4 complete, apps/security-service/ foundation ready
  - **Exit Condition**: All tasks in tasks-cyberchef.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_cyberchef_integration.py`
  - **Return To**: T101
  - **Est. Hours**: 40

- [ ] T101 [HANDOFF] Migrate Maltrail
  - **File**: [`tasks-individual/tasks-maltrail.md`](tasks-individual/tasks-maltrail.md)
  - **Entry Condition**: T100 complete
  - **Exit Condition**: All tasks in tasks-maltrail.md complete + validation tests pass
  - **Validation**: `pytest tests/security/test_maltrail_integration.py`
  - **Return To**: T102
  - **Est. Hours**: 35
```

**Key Elements**:
- `[HANDOFF]` tag - Signals delegation to child document
- **File** - Exact path to child task file (clickable link)
- **Entry Condition** - Prerequisites that must be met before starting
- **Exit Condition** - Completion criteria before returning
- **Validation** - Specific test command to verify completion
- **Return To** - Next task ID after completion
- **Est. Hours** - Time estimate for planning

### 2. Child Task Format (in `tasks-individual/tasks-*.md`)

Individual task files include handoff metadata in frontmatter and explicit entry/exit checklists:

```markdown
---
description: "Task list for CyberChef migration"
parent_task: "../tasks.md#T100"
parent_phase: "Phase 5.1: Security Domain Migrations"
return_to: "../tasks.md#T101"
domain: "security"
target_service: "apps/security-service"
legacy_path: "features/CyberChef"
estimated_hours: 40
---

# Tasks: [MIGRATION: CyberChef]

**⬆️ PARENT TASK**: [`tasks.md#T100`](../tasks.md#T100)  
**⬇️ RETURN TO**: [`tasks.md#T101`](../tasks.md#T101)

## Handoff Context

**Called From**: `tasks.md` Phase 5.1, Task T100  
**Entry Condition**: Security service foundation ready (Phase 1-4 complete)  
**Exit Condition**: All tasks below complete + validation tests pass  
**Return Action**: Mark T100 complete in parent `tasks.md`, proceed to T101

---

## Pre-Flight Checklist ✅

**Verify these conditions before starting any tasks below**:

- [ ] Parent Phase 1-4 marked complete in `tasks.md`
- [ ] `apps/security-service/src/` exists with base infrastructure
- [ ] Database migrations from Phase 2 applied
- [ ] Authentication/authorization from Phase 3 working
- [ ] Test framework from Phase 3 operational
- [ ] Legacy environment setup: `features/CyberChef/` accessible

**If any checklist item fails**: STOP and return to parent `tasks.md` to complete prerequisites.

---

## CyberChef Migration Tasks

[... detailed migration tasks here ...]

---

## Post-Flight Checklist ✅

**Verify these conditions before marking parent task complete**:

- [ ] All tasks T001-T100 marked complete above
- [ ] Integration tests pass: `pytest tests/security/test_cyberchef_integration.py`
- [ ] Performance baselines met (documented in `migration-validation.md`)
- [ ] Ground truth tests confirm functional parity with legacy
- [ ] Legacy `features/CyberChef/` backed up to `archive/`
- [ ] Migration completion documented in `migration-validation.md`

**Completion Action**:
1. Mark all checkboxes above ✅
2. Run validation command: `pytest tests/security/test_cyberchef_integration.py`
3. Document completion in `migration-validation.md`
4. Mark parent task T100 complete in `tasks.md`
5. Proceed to return task T101 in `tasks.md`
```

---

## Workflow Execution

### For AI Agents (Copilot)

When processing tasks, follow this workflow:

#### Step 1: Start at Top-Level
```
1. Open specs/003-brownfield-integration/tasks.md
2. Identify current phase and next incomplete task
3. Check for [HANDOFF] tag
```

#### Step 2: Detect Handoff
```
IF task contains [HANDOFF]:
  1. Read Entry Condition
  2. Verify entry condition is met
  3. If NOT met: complete prerequisites first
  4. If met: proceed to child document
```

#### Step 3: Execute Child Tasks
```
1. Open file specified in "File:" field
2. Execute Pre-Flight Checklist
   - If any item fails: return to parent, complete prerequisites
3. Execute all tasks in child document sequentially
4. Execute Post-Flight Checklist
5. Run validation command
```

#### Step 4: Return to Parent
```
1. Verify ALL exit conditions met
2. Mark parent [HANDOFF] task complete
3. Document completion in migration-validation.md
4. Proceed to "Return To" task
```

### For Human Developers

1. **Check Parent Task**: Review entry conditions in `tasks.md`
2. **Open Child Document**: Click the file link to open detailed tasks
3. **Execute Pre-Flight**: Verify all prerequisites before starting
4. **Complete Tasks**: Work through all tasks in child document
5. **Execute Post-Flight**: Verify all completion criteria
6. **Update Parent**: Mark handoff task complete, proceed to next task

---

## Parallel Handoffs

Tasks marked `[P] [HANDOFF]` can be executed in parallel:

```markdown
- [ ] T100 [P] [HANDOFF] Migrate CyberChef → tasks-individual/tasks-cyberchef.md
- [ ] T101 [P] [HANDOFF] Migrate Maltrail → tasks-individual/tasks-maltrail.md
- [ ] T102 [P] [HANDOFF] Migrate HELK → tasks-individual/tasks-helk.md
```

**Parallel Execution Rules**:
1. Each can start independently (no dependencies)
2. Each gets own working branch: `migration/cyberchef`, `migration/maltrail`, etc.
3. Each must complete fully before merging
4. All parallel tasks must complete before proceeding past that phase

**Branching Strategy**:
```bash
# For parallel migrations
git checkout -b migration/cyberchef
# Complete all tasks in tasks-cyberchef.md
git commit -m "Complete CyberChef migration (T100)"

# Meanwhile, in parallel:
git checkout main
git checkout -b migration/maltrail
# Complete all tasks in tasks-maltrail.md
git commit -m "Complete Maltrail migration (T101)"

# After both complete:
git checkout main
git merge migration/cyberchef
git merge migration/maltrail
# Mark T100, T101 complete in tasks.md
```

---

## State Tracking

### Completion States

Each level tracks its own completion state:

**Parent Level** (`tasks.md`):
```markdown
- [x] T099 Phase 4 complete
- [x] T100 [HANDOFF] Migrate CyberChef  ← Marked complete ONLY after child complete
- [ ] T101 [HANDOFF] Migrate Maltrail  ← Currently in progress
```

**Child Level** (`tasks-individual/tasks-cyberchef.md`):
```markdown
- [x] T001 Analysis validation
- [x] T002 Setup legacy environment
- [ ] T003 Data model migration  ← Currently working
```

### Progress Tracking

Track overall migration progress in `migration-validation.md`:

```markdown
## Migration Progress

### Phase 5.1: Security Domain (18 projects)

- [x] CyberChef (T100) - Completed 2025-11-08 - 42 hours
- [ ] Maltrail (T101) - In Progress - 15/35 hours
- [ ] HELK (T102) - Not Started
...
```

---

## Error Handling

### Entry Condition Failures

If entry conditions not met:

```markdown
**Action**: STOP task execution
**Record**: Document blocker in migration-validation.md
**Return**: Go back to parent task to resolve prerequisites
**Example**:
  - Entry requires: "apps/security-service/ foundation ready"
  - Found: Directory doesn't exist
  - Action: Return to tasks.md Phase 3 to complete infrastructure setup
```

### Exit Condition Failures

If exit conditions not met:

```markdown
**Action**: DO NOT mark parent task complete
**Record**: Document failing validation in migration-validation.md
**Debug**: Review task completion, fix issues
**Re-validate**: Re-run validation tests
**Example**:
  - Exit requires: "Integration tests pass"
  - Found: 3 tests failing
  - Action: Fix test failures, re-run, then mark complete
```

### Validation Test Failures

If validation command fails:

```markdown
**Action**: Investigate and fix before marking complete
**Process**:
  1. Run validation: pytest tests/security/test_cyberchef_integration.py
  2. If failures: Review logs, fix implementation
  3. Re-test until all pass
  4. Document results in migration-validation.md
  5. Only then mark parent task complete
```

---

## Best Practices

### 1. Always Verify Entry Conditions
Never skip the pre-flight checklist. Starting without prerequisites leads to:
- Wasted effort on incomplete foundations
- Test failures due to missing infrastructure
- Rework when dependencies aren't ready

### 2. Complete Tasks Sequentially in Child Docs
Within individual task files, complete tasks in order unless marked `[P]`:
- Ensures dependencies are met
- Establishes proper testing baselines
- Maintains validation checkpoints

### 3. Document as You Go
Update `migration-validation.md` continuously:
- Record completion timestamps
- Note any deviations or issues
- Document actual hours vs. estimates
- Track performance baselines

### 4. Never Mark Parent Complete Until Child Fully Done
Parent `[HANDOFF]` task stays unchecked until:
- All child tasks complete ✅
- All validation tests pass ✅
- Exit conditions verified ✅
- Documentation updated ✅

### 5. Use Branches for Parallel Work
When executing parallel handoffs:
- Create feature branches per project
- Keep changes isolated
- Merge only after full completion
- Resolve conflicts at integration time

---

## Example: Complete Handoff Flow

### Scenario: Migrating CyberChef

**Starting State**: Working in `tasks.md`, Phase 4 complete

#### Step 1: Identify Next Task
```markdown
tasks.md:
- [x] T099 Phase 4 complete - All foundations ready
- [ ] T100 [HANDOFF] Migrate CyberChef
      File: tasks-individual/tasks-cyberchef.md
      Entry: Phase 1-4 complete, security-service ready
      Exit: All tasks complete + tests pass
```

#### Step 2: Verify Entry Condition
```bash
# Check infrastructure exists
ls apps/security-service/src/
# Output: api/ data/ services/ tests/ ✅

# Check database ready
psql -c "SELECT 1 FROM schema_migrations WHERE version='2025-11-08-phase2';"
# Output: 1 row ✅

# Entry condition MET ✅
```

#### Step 3: Open Child Document
```
Open: specs/003-brownfield-integration/tasks-individual/tasks-cyberchef.md
```

#### Step 4: Execute Pre-Flight Checklist
```markdown
- [x] Parent Phase 1-4 marked complete
- [x] apps/security-service/src/ exists
- [x] Database migrations applied
- [x] Auth working
- [x] Test framework operational
- [x] Legacy features/CyberChef/ accessible

ALL CHECKS PASS ✅ → Proceed with tasks
```

#### Step 5: Execute Child Tasks
```markdown
- [x] T001 Analysis validation
- [x] T002 Setup legacy test environment
- [x] T003 Ground truth tests
...
- [x] T040 Final integration tests
```

#### Step 6: Execute Post-Flight Checklist
```markdown
- [x] All tasks T001-T040 complete
- [x] Integration tests pass: pytest tests/security/test_cyberchef_integration.py
      Output: 47 passed in 12.3s ✅
- [x] Performance baselines met (documented)
- [x] Ground truth tests confirm parity
- [x] Legacy backed up to archive/
- [x] Completion documented in migration-validation.md

ALL CHECKS PASS ✅ → Ready to return
```

#### Step 7: Return to Parent
```markdown
1. Open: tasks.md
2. Mark complete:
   - [x] T100 [HANDOFF] Migrate CyberChef ✅
3. Proceed to:
   - [ ] T101 [HANDOFF] Migrate Maltrail ← Next task
```

#### Step 8: Document Completion
```markdown
Update migration-validation.md:

### CyberChef Migration (T100)
- **Status**: ✅ Complete
- **Completed**: 2025-11-09
- **Estimated Hours**: 40
- **Actual Hours**: 42
- **Tests**: 47 passed
- **Performance**: All baselines met
- **Notes**: Excellent functional parity achieved
```

**Handoff Complete** ✅ → Proceed to next migration

---

## Migration Validation Tracking

Maintain completion tracking in `migration-validation.md`:

```markdown
# Migration Validation Log

## Overall Progress

**Total Projects**: 38  
**Completed**: 2 (5%)  
**In Progress**: 1 (3%)  
**Remaining**: 35 (92%)

## Domain Breakdown

### Security Domain (19 projects)
- [x] MISP (Pre-existing) - Complete
- [x] CyberChef (T100) - Complete 2025-11-09
- [ ] Maltrail (T101) - In Progress
- [ ] HELK (T102) - Not Started
...

### Productivity Domain (7 projects)
- [ ] Actual Budget (T200) - Not Started
...

### MTG Domain (3 projects)
- [ ] Commander Spellbook Backend (T300) - Not Started
...

### Infrastructure Domain (8 projects)
- [ ] Kong (T400) - Not Started
...

## Completion Details

### CyberChef (T100)
- **Parent Task**: tasks.md#T100
- **Child Doc**: tasks-individual/tasks-cyberchef.md
- **Started**: 2025-11-08
- **Completed**: 2025-11-09
- **Est. Hours**: 40
- **Actual Hours**: 42 (+5%)
- **Tasks Completed**: 40/40 (100%)
- **Tests**: 47 passed, 0 failed
- **Performance**: All baselines met or exceeded
- **Entry Verified**: ✅ All prerequisites met
- **Exit Verified**: ✅ All completion criteria met
- **Notes**: Smooth migration, excellent test coverage
```

---

## Summary

The handoff protocol provides:

✅ **Clear Delegation** - Parent delegates to child with explicit contract  
✅ **Validation Gates** - Entry/exit conditions prevent premature execution  
✅ **Progress Tracking** - Multi-level completion state  
✅ **Parallel Execution** - Support for concurrent migrations  
✅ **Error Handling** - Clear process for handling failures  
✅ **Documentation** - Complete audit trail of all migrations  

This creates a robust, scalable pattern for managing complex multi-project migrations while maintaining quality and traceability.
