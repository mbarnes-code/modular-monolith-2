# Implementation Plan: Mental Prosthetic Platform (Refined)

**Branch**: `002-mental-prosthetic-refinement` | **Date**: 2025-10-19 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-mental-prosthetic-refinement/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Consolidate 37 executive function tools from the features/ directory into a unified modular monolithic application to serve as a mental prosthetic for ADHD/autism support. The platform integrates Security (13 tools), Productivity (8 tools), MTG (4 tools), and Infrastructure (12 tools) using a layer-based architecture (UI, API, Data, AI) with big-bang migration strategy. Core technologies: Vue.js 3 + TypeScript frontend, FastAPI backend, PostgreSQL primary database, with local LLM server integration for AI-assisted executive function support.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.12 (backend), TypeScript 5.9.3 (frontend), Node.js 20 (build/dev)  
**Primary Dependencies**: FastAPI 0.119.0, Vue.js 3 + TypeScript, PostgreSQL 14+, Redis 7+, vLLM 0.11.0, Chroma DB  
**Storage**: PostgreSQL (primary database for 18/37 projects), SQLite (local-first apps: 5/37 projects), Redis (caching, job queues), Vector DB (AI embeddings)  
**Testing**: pytest (Python backend), Vitest (Vue.js frontend), Playwright (E2E), NEEDS CLARIFICATION: specific testing strategy for 37-tool integration  
**Target Platform**: Linux server (home server deployment), PWA (mobile remote access), HTTPS (secure remote access)
**Project Type**: web application (modular monolithic architecture)  
**Performance Goals**: Domain-based performance (Security <1s, Productivity <2s, MTG <3s, Infrastructure <5s), 500ms p95 API responses, sub-1-second WebSocket latency  
**Constraints**: Single-user deployment, 24-hour offline capability, 99.9% uptime during active hours, 15-minute recovery from failures  
**Scale/Scope**: 37 integrated tools across 4 domains, single ADHD/autism user, estimated 100+ API endpoints, comprehensive UI consolidation from 37 to 1 interface

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Code Quality Standards**:

- [x] TypeScript strict mode enabled, type safety maintained (Vue.js 3 + TypeScript specified)
- [x] Python code includes comprehensive type hints (Python 3.12 with FastAPI requires type hints)
- [x] Documentation plan for public APIs included (OpenAPI specifications for 37-tool integration)

**Testing Strategy**:

- [x] Unit test strategy covers 80%+ business logic - RESOLVED: Multi-layer testing with pytest (backend) + Vitest (frontend)
- [x] Integration tests planned for service interactions - RESOLVED: Cross-domain workflow testing with domain boundary validation  
- [x] Performance testing approach defined for affected endpoints - RESOLVED: Artillery.js load testing with domain-specific performance tiers

**User Experience**:

- [x] UI components use shared design system (`libs/ui/`) - Vue.js component consolidation specified
- [x] Response time requirements <200ms UI, <500ms API documented - Domain-based performance tiers defined
- [x] Error handling and accessibility considerations included - Executive function accommodations specified

**Performance Requirements**:

- [x] Service-specific performance benchmarks identified - Domain-based tiers: Security <1s, Productivity <2s, MTG <3s, Infrastructure <5s
- [x] Memory and resource constraints documented - Single-user deployment with 24-hour offline capability
- [x] Load testing approach defined where applicable - RESOLVED: Comprehensive performance testing with domain-specific scenarios

**Modular Architecture**:

- [x] Service boundaries clearly defined and justified - Layer-based architecture (UI, API, Data, AI) with big-bang migration
- [x] Dependency graph maintains proper separation - Category A/B/C complexity tiers defined
- [x] API versioning strategy documented - RESOLVED: Domain-based versioning with backward compatibility layers

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
# Modular Monolith Structure (Web Application)
apps/
├── jane-orchestrator/           # FastAPI backend (consolidates 37 tools)
│   ├── src/
│   │   ├── api/                # API layer endpoints
│   │   ├── domains/            # Business logic (Security, Productivity, MTG, Infrastructure)
│   │   ├── data/               # Data layer (PostgreSQL, SQLite, Redis)
│   │   └── ai/                 # AI layer (LLM integration)
│   └── tests/
│       ├── unit/               # 80%+ coverage requirement
│       ├── integration/        # Cross-domain testing
│       └── contract/           # API contract validation
├── jane-ui/                    # Vue.js 3 + TypeScript frontend
│   ├── src/
│   │   ├── components/         # Shared UI components (libs/ui integration)
│   │   ├── domains/            # Domain-specific views (37-tool consolidation)
│   │   └── services/           # API integration layer
│   └── tests/
│       ├── unit/               # Component testing
│       └── e2e/                # Playwright E2E tests
└── [existing LLM servers]/     # code-llm-server, cyber-llm-server, mtg-llm-server

libs/
├── shared/                     # Cross-domain utilities
├── ui/                        # Design system components
└── service-adapters/          # 37-tool integration adapters

features/                      # SOURCE: 37 tools to be integrated
├── [Security tools - 13]/     # → apps/jane-orchestrator/src/domains/security/
├── [Productivity tools - 8]/  # → apps/jane-orchestrator/src/domains/productivity/  
├── [MTG tools - 4]/          # → apps/jane-orchestrator/src/domains/mtg/
└── [Infrastructure tools - 12]/ # → apps/jane-orchestrator/src/domains/infrastructure/
```

**Structure Decision**: Web application structure selected due to frontend (Vue.js) + backend (FastAPI) architecture. The modular monolith approach consolidates 37 tools from features/ directory into domain-organized modules within jane-orchestrator while maintaining layer-based service boundaries.

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

*No Constitution Check violations - all requirements satisfied through research and design decisions.*

## Phase 0 & 1 Completion

### Generated Artifacts

- [x] **research.md**: Complete technical research resolving all NEEDS CLARIFICATION items
- [x] **data-model.md**: Unified database schema supporting all 37 tools across 4 domains
- [x] **contracts/api.yaml**: Complete OpenAPI specification with 50+ endpoints
- [x] **quickstart.md**: Development setup guide with executive function accommodations
- [x] **Agent Context**: Updated GitHub Copilot context with confirmed technology stack

### Constitution Validation (Post-Design)

All constitution requirements have been satisfied:

- **Code Quality**: TypeScript strict mode and Python type hints confirmed
- **Testing Strategy**: 80%+ coverage plan with multi-layer testing approach
- **User Experience**: Domain-based performance tiers and executive function accommodations
- **Performance**: Domain-specific benchmarks and load testing strategy
- **Modular Architecture**: Layer-based service boundaries with clear separation

### Technology Stack Confirmation

- **Backend**: Python 3.12 + FastAPI 0.119.0
- **Frontend**: Vue.js 3 + TypeScript 5.9.3 + Node.js 20
- **Database**: PostgreSQL 14+ (primary), SQLite (local-first), Redis 7+ (caching)
- **AI Integration**: vLLM 0.11.0 + Chroma DB for executive function support
- **Architecture**: Modular monolith with layer-based service boundaries

### Ready for Phase 2

The implementation plan is complete through Phase 1. All technical clarifications have been resolved, data models designed, API contracts specified, and development environment documented.

**Next Command**: `/speckit.tasks` to generate detailed implementation tasks for the 37-tool consolidation.

