# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Project Type & Migration Strategy

**Project Type**: [GREENFIELD/BROWNFIELD] *(from spec.md selection)*

### [BROWNFIELD ONLY] Migration Strategy Summary

*Fill this section ONLY if project type is BROWNFIELD*

**Migration Method**: [Strangler Fig / API Gateway / Blue-Green / Event-Driven / etc.]
**Project Scale**: [SMALL/MEDIUM/LARGE/EXTREME] *(from spec.md assessment)*
**Migration Timeline**: [X weeks based on scale and method]
**Risk Level**: [MEDIUM/HIGH/VERY HIGH/EXTREME] *(corresponds to scale)*

**Selected Approach Justification**: [Why this migration method was chosen over alternatives]

**Legacy System Retirement Plan**: [How and when legacy systems will be decommissioned]

**Reference Documents**:
- See `specs/[###-feature]/migration-strategy.md` for detailed asset relocation approach
- See `specs/[###-feature]/legacy-analysis.md` for existing system documentation

---

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
  
  For BROWNFIELD projects: Include both legacy and target technology decisions
  For GREENFIELD projects: Include target technology stack only
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Code Quality Standards**:

- [ ] TypeScript strict mode enabled, type safety maintained
- [ ] Python code includes comprehensive type hints
- [ ] Documentation plan for public APIs included

**Testing Strategy**:

- [ ] Unit test strategy covers 80%+ business logic
- [ ] Integration tests planned for service interactions
- [ ] Performance testing approach defined for affected endpoints

**User Experience**:

- [ ] UI components use shared design system (`libs/ui/`)
- [ ] Response time requirements <200ms UI, <500ms API documented
- [ ] Error handling and accessibility considerations included

**Performance Requirements**:

- [ ] Service-specific performance benchmarks identified
- [ ] Memory and resource constraints documented
- [ ] Load testing approach defined where applicable

**Modular Architecture**:

- [ ] Service boundaries clearly defined and justified
- [ ] Dependency graph maintains proper separation
- [ ] API versioning strategy documented

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── [BROWNFIELD ONLY]
    ├── migration-strategy.md    # Brownfield asset relocation strategy
    ├── legacy-analysis.md       # Existing system documentation
    └── data-mapping.md          # Database migration mapping
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

