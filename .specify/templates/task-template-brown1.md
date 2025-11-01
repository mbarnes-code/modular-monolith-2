---
description: "Task list template for feature integration"
---

  # Tasks: [MIGRATION: FEATURE NAME]

**Input (Spec)**: Design documents from `/specs/[###-feature-name]/` 
**Input (Legacy)**: Legacy codebase path [e.g., /features/MISP/] 
**Prerequisites**: plan.md (required), spec.md (required), project_analysis_report.md(required), research.md, data-model.md, contracts/

**Tests**: Tests are MANDATORY for all migration tasks. The "Ground Truth" test (testing the original code) must be written first.
-**project integration** if projects are being imported into an existing project, search for test to base the "Ground Truth" test from.

**Organization**: Tasks are grouped by Legacy Feature (e.g., "Event Publishing Logic") to ensure 1:1 functional parity.

## Format: [ID] [P?] [Feature] [Logic: <legacy_file::function>] Description
- [P]: Can run in parallel
- [Feature]: Which legacy feature this task belongs to (e.g., F1: Publishing)
- [Logic]: The exact legacy code being replaced. This is not optional.

## Path Conventions
- **New Project**: [e.g., apps/PROJECT/src/] at repository root
- **Legacy Project**: [e.g., features/Project/app/Model/]
- Paths shown below assume single project - adjust based on plan.md structure

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

## Phase 1: Setup (New Project & Legacy Testbed)

**Purpose**: Initialize the new project and an environment to test the old one.

- [ ] T001 Create new project structure per implementation plan
- [ ] T002 Initialize Python project with FastAPI dependencies
- [ ] T003 [P] Configure linting and formatting tools
- [ ] T004 [Ground Truth] Setup a test environment for the legacy PHP project (e.g., a Docker container with PHP and dependencies) to run ground-truth tests.

---

## Phase 2: Foundational (New Project Scaffolding)

**Purpose**: Core infrastructure for the new application.

- [ ] T005 Setup database schema and migrations framework
- [ ] T006 [P] Implement shell authentication/authorization framework (will be populated by TDM)
- [ ] T007 [P] Setup API routing and middleware structure (empty routes)
- [ ] T008 [P] Create empty base models/entities (e.g., Event, Attribute shells)
- [ ] T009 Configure error handling and logging infrastructure

**Checkpoint**: Foundation ready. NO business logic exists.

## Phase 3: Logic Migration (Feature 1 - [e.g., Event Publishing]) 🎯 MVP

**Migration Goal**: [Brief description of what this migration step delivers]

**Independent Test**: "A 'Draft' event cannot be published. A 'Validated' event can be published, which triggers a sync."

### Phase 3a: Ground Truth & Validation (Write These First)

NOTE: Write Ground Truth tests against OLD code. Write Validation tests against NEW code.

- [ ] T010 [P] [F1] [Logic: Event.php::publishRouter] Ground Truth Test: Write a PHP test (test_publish_router.php) that proves the original publishRouter function:
        FAILS when given a 'Draft' event.
        PASSES when given a 'Validated' event.
- [ ] T011 [P] [F1] [Logic: Event.php::publishRouter] Validation Test: Translate the PHP test (T010) into a Python pytest (test_publish_router.py). This test must fail initially, as the new code doesn't exist.

### Phase 3b: Porting & Integration

- [ ] T012 [P] [F1] [Logic: Event.php::Event()] Port Models: Implement the Event model in src/models/event.py based on the analysis report (Section 2.1).
- [ ] T013 [F1] [Logic: Event.php::publishRouter] Port Logic: Prompt the LLM to translate only the PHP publishRouter function into a new Python function publish_router_py in src/services/event_service.py.
- [ ] T014 [F1] [Logic: Event.php::publishRouter] Run Validation: Run the pytest (T011) against your new publish_router_py function (T013). It MUST pass. Do not proceed until it passes.
- [ ] T015 [F1] Integrate Logic: After validation passes, create the FastAPI endpoint in src/api/events.py that calls your proven publish_router_py function.
- [ ] T016 [F1] Run Full Test: Run both the pytest (T011) and the integration test for the new API endpoint. Both must pass.

**Checkpoint**: At this point, the "Event Publishing" feature is provably migrated and functional.

## Phase 4: Logic Migration (Feature 2 - [e.g., Access Control])

**Migration Goal**: Port the "Distribution-Based Access Control." Original Asset(s): features/MISP/app/Model/Event.php, features/MISP/app/Controller/AppController.php

**Independent Test**: "User A (Org 1) cannot see User B's (Org 2) 'Org Only' event."

### Phase 4a: Ground Truth & Validation (Write These First)

- [ ] T017 [P] [F2] [Logic: Event.php::beforeFind] Ground Truth Test: Write a PHP test (test_access_control.php) that proves the original beforeFind database query filter:
        Logs in as User B.
        Queries for User A's distribution=0 event.
        Asserts the query returns 0 results.

- [ ] T018 [P] [F2] [Logic: Event.php::beforeFind] Validation Test: Translate the PHP test (T017) into a Python pytest (test_access_control.py) that calls the new API. This test must fail initially.

### Phase 4b: Porting & Integration

- [ ] T019 [F2] [Logic: Event.php::beforeFind] Port Logic: Prompt the LLM to translate the database query filtering logic from beforeFind into a new Python function get_events_for_user(user) in src/services/event_service.py.
- [ ] T020 [F2] [Logic: Event.php::beforeFind] Run Validation: Run the pytest (T018) against your new get_events_for_user logic. It MUST pass.
- [ ] T021 [F2] Integrate Logic: Wire the proven get_events_for_user function into the main FastAPI /events endpoint.

**Checkpoint**: Access control is now provably migrated.

[Add more logic migration phases as needed, following the Ground Truth -> Port -> Validate -> Integrate loop]

## Phase N: Polish & Cross-Cutting Concerns

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring of new Python code only.
- [ ] TXXX [P] Additional unit tests (if requested) in tests/unit/

## Phase N+1: Asset Deletion (The Final Step)

Purpose: To safely remove the legacy code after it has been fully replaced.

- [ ] TXXX Verify Full Migration: Confirm all [Logic: ...] tags for features/MISP/ have a corresponding passing validation test.
- [ ] TXXX Run Full Regression Suite: Run all validation tests for all features simultaneously.
- [ ] TXXX Delete Legacy Asset: After 100% validation, delete the features/MISP/ directory.

### Dependencies & Execution Order

- **Setup (Phase 1) + Foundational (Phase 2)**: Must be completed first.
- **Logic Migration (Phase 3+)**: Can proceed in parallel by feature.
- **Asset Deletion (Phase N+1)**: The very last step.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Within Each Migration Feature (e.g., F1)
  - LOOP: T010 (Ground Truth Test) → T011 (Validation Test) → T012 (Port Logic) → T013 (Run Validation) → T014 (Integrate)
  - A task is not "done" when the code is written. It is "done" when the validation test passes.
