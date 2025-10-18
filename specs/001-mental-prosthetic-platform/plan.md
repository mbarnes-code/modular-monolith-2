# Implementation Plan: Mental Prosthetic Platform

**Branch**: `001-mental-prosthetic-platform` | **Date**: 2025-10-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-mental-prosthetic-platform/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

The Mental Prosthetic Platform consolidates 30+ executive function tools from the features/ directory into a unified modular monolithic application. The platform provides a single interface for ADHD/autism users to access productivity, security, MTG, and development tools while integrating with a local LLM server for AI-assisted executive function support. Technical approach involves analyzing existing codebases in docs/modular-analysis-repo-main/, systematically integrating projects into the existing NX monorepo structure, and ensuring seamless data flow between all tools.

## Technical Context

**Language/Version**: TypeScript 5.9.3, Python 3.12, Node.js 20
**Primary Dependencies**: Next.js 15.5.4, React 19.2.0, FastAPI 0.119.0, NX 21.6.4, vLLM 0.11.0, Chroma DB
**Storage**: PostgreSQL for transactional data, Chroma DB for vector embeddings, Synology NAS for backups
**Testing**: Jest/Playwright for frontend, pytest for Python services, contract testing for APIs
**Target Platform**: Linux server (home deployment), PWA for mobile support, future native mobile app
**Project Type**: web - modular monolithic application with frontend and multiple backend services
**Performance Goals**: 1000+ req/s for orchestrator, <2s LLM inference, <200ms UI interactions
**Constraints**: <500ms API response times, <8GB memory per LLM server, 99.9% uptime during active hours
**Scale/Scope**: Single user (ADHD/autism support), 37 integrated projects across 4 domains, complete features/ directory consolidation

## Constitution Check (Re-evaluated after Phase 1 Design)

*GATE: Re-evaluation after Phase 1 design completion*

**Code Quality Standards**:

- [x] TypeScript strict mode enabled, type safety maintained ✅ (Enforced in NX configuration)
- [x] Python code includes comprehensive type hints ✅ (FastAPI requires type hints, documented in quickstart)
- [x] Documentation plan for public APIs included ✅ (OpenAPI specs generated, quickstart guide created)

**Testing Strategy**:

- [x] Unit test strategy covers 80%+ business logic ✅ (Jest/Playwright for frontend, pytest for Python)
- [x] Integration tests planned for service interactions ✅ (API contracts, WebSocket protocols, service adapters)
- [x] Performance testing approach defined for affected endpoints ✅ (<200ms UI, <500ms API, <2s LLM inference)

**User Experience**:

- [x] UI components use shared design system (`libs/ui/`) ✅ (Enhanced domain-specific UI components planned)
- [x] Response time requirements <200ms UI, <500ms API documented ✅ (Performance criteria in success criteria)
- [x] Error handling and accessibility considerations included ✅ (WCAG 2.1 AA compliance, graceful degradation)

**Performance Requirements**:

- [x] Service-specific performance benchmarks identified ✅ (1000+ req/s orchestrator, <2s LLM, <200ms UI)
- [x] Memory and resource constraints documented ✅ (<8GB per LLM server, container limits)
- [x] Load testing approach defined where applicable ✅ (Performance testing in CI/CD)

**Modular Architecture**:

- [x] Service boundaries clearly defined and justified ✅ (Domain-specific service adapters, clear data flow)
- [x] Dependency graph maintains proper separation ✅ (Features/ → service-adapters/ → apps/ structure)
- [x] API versioning strategy documented ✅ (OpenAPI contracts with versioning, WebSocket protocol specs)

**Additional Constitution Compliance**:

- [x] **Executive Function Focus**: All design decisions prioritize ADHD/autism user needs ✅
- [x] **No Wrappers**: Service adapters preserve original business logic without shortcuts ✅  
- [x] **Integration Completion**: Clear criteria for features/ directory emptiness ✅
- [x] **AI Enhancement**: Comprehensive LLM integration for executive function support ✅

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```
apps/
├── jane-orchestrator/          # Enhanced FastAPI orchestrator with AI integration
├── jane-ui/                    # Enhanced Next.js UI with unified dashboard
├── cyber-llm-server/           # Enhanced for integrated security tools
├── mtg-llm-server/             # Enhanced for MTG tool integration
└── code-llm-server/            # Enhanced for development tool integration

libs/
├── shared/                     # Cross-domain shared utilities
│   ├── types/                  # Unified type definitions
│   ├── utils/                  # Common utility functions
│   └── config/                 # Configuration management
├── service-adapters/           # Integration adapters for features/ projects
│   ├── security/               # MISP, Nemesis, HELK, etc.
│   ├── productivity/           # n8n, actual, mealie, etc.
│   ├── mtg/                    # commander-spellbook, mtg-commander-map
│   └── development/            # goose, inspector, it-tools, etc.
└── ui/                         # Enhanced shared UI components
    ├── core/                   # Base components
    ├── domain-security/        # Security tool UI components
    ├── domain-mtg/             # MTG tool UI components
    ├── domain-productivity/    # Productivity tool UI components
    └── theme/                  # Unified theming

features/ → EMPTY              # All projects integrated into above structure
docs/                          # Analysis documentation guiding integration
infrastructure/                # Enhanced deployment configs
```

**Structure Decision**: Web application pattern with enhanced modular monolith structure. Projects from features/ directory will be integrated into appropriate domain-specific service adapters and UI components, maintaining the existing NX monorepo architecture while consolidating all executive function tools into a unified platform.

## Complexity Tracking

No constitution violations identified. All principles satisfied through the design:

- **Code Quality**: TypeScript strict mode, Python type hints, comprehensive documentation
- **Testing**: Multi-layer testing strategy with 80%+ coverage requirements  
- **User Experience**: ADHD/autism-focused design with shared component library
- **Performance**: Clear benchmarks and constraints for all service components
- **Modular Architecture**: Clean separation via service adapters and domain boundaries

