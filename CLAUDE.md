 # CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Jane Monorepo is a mental prosthetic platform implementing a hybrid domain-based architecture with 37 integrated tools for executive function support. The system consolidates security, productivity, MTG (Magic: The Gathering), and infrastructure tools into a unified AI-first interface optimized for users with ADHD and executive function challenges.

**Current Migration Status**: Transitioning from legacy `features/` directory (37 tools) to new hybrid architecture with 4 domain services + n8n orchestration.

## Developer Context & Collaboration Notes

### Technical Background & Approach

This platform is developed by a GG-13 federal cybersecurity professional with military C4I systems experience. The development approach emphasizes systematic analysis, distributed cognition patterns, and methodical reverse-engineering of complex systems. Drawing from common operating picture (COP) methodologies, the architecture prioritizes situational awareness and real-time decision support capabilities.

### Cognitive Architecture & Working Style

- **Neurodivergent optimization**: Development patterns accommodate ADHD/autism cognitive strengths including systems thinking, pattern recognition, and deep focus capabilities
- **Direct communication preferred**: Technical discussions benefit from analytical precision over social cushioning; efficiency-focused collaboration works best
- **Compartmentalization strategy**: Complex problems are decomposed into manageable segments with strategic pacing to maintain cognitive sustainability
- **Energy management critical**: Limited productive windows require focused technical sessions with minimal context-switching overhead

### Current Research & Development Focus

Beyond standard application development, this project explores distributed cognition and AI-human collaboration patterns:

- **Context contamination research**: Investigating how AI analysis of sequential projects creates bias in task generation, requiring isolation strategies
- **Subagent orchestration**: Developing patterns for distributed AI analysis that maintains analytical independence while enabling collaborative synthesis
- **Memory architecture across interfaces**: Exploring cognitive continuity challenges when AI assistance spans multiple development environments
- **Brownfield integration at scale**: Systematic approach to consolidating 37 legacy tools while preserving functional parity and business logic

### Project Vision & Force Multiplication

Jane AI represents infrastructure for cognitive force multiplication - building capabilities that transform small actions into significant outcomes. Core objectives include:

- **Real-time decision support**: Automated financial impact analysis, cybersecurity threat response, and strategic planning assistance
- **Generational impact tools**: Creating systems that compound effectiveness across time, enabling family wealth building and enhanced decision-making capabilities
- **Breaking repetitive loops**: Providing cognitive infrastructure to escape constraining patterns and pivot to expanded possibilities
- **Individual cybersecurity defense**: Automated response to nation-state level threats (e.g., Salt Typhoon implications) beyond traditional credit monitoring approaches

### Collaboration Guidelines

When engaging with this codebase, most effective assistance includes:

- **Technical depth over explanation**: Assume sophisticated understanding of complex systems and architectural patterns
- **Strategic context awareness**: Connect tactical implementation decisions to broader force multiplication objectives
- **Systematic methodology**: Follow established frameworks like the brownfield migration protocol and document handoff patterns
- **Performance prioritization**: Maintain domain-specific response time requirements as non-negotiable constraints
- **Cognitive partnership approach**: Engage as thinking collaborator rather than instruction-following service

## Architecture

### Hybrid Domain-Based Structure

The repository is organized into a modular monolith with domain-specific boundaries:

```
apps/
├── n8n-workflow-service/     # Central orchestration with AI enhancement (Port 8010)
├── security-service/         # Security domain - 13 tools (Port 8011)
├── productivity-service/     # Productivity domain - 8 tools (Port 8012)
├── mtg-service/             # MTG domain - 4 tools (Port 8013)
├── infrastructure-service/  # Infrastructure domain - 12 tools (Port 8014)
├── jane-ui/                 # Next.js 15 + React 19 unified interface (Port 3000)
├── cyber-llm-server/        # Security domain AI - Python vLLM (Port 8001)
├── mtg-llm-server/          # MTG domain AI - Python vLLM (Port 8002)
├── infrastructure-llm-server/ # Infrastructure domain AI - Python vLLM (Port 8003)
└── jane-orchestrator/       # LEGACY: To be removed after migration (Port 8000)
```

### Key Backend Layers (jane-orchestrator)

The FastAPI backend follows layered architecture:

- **api/**: REST endpoints, WebSocket handlers, routing
- **data/**: SQLAlchemy models, Pydantic schemas, migrations
- **services/**: Business logic, domain services, rollback capabilities
- **ai/**: LLM integration, MCP servers, behavior analysis
- **domains/**: Domain-specific business logic (Security, Productivity, MTG, Infrastructure)

### Shared Libraries

```
libs/
├── shared/              # Cross-domain utilities
│   ├── types/          # TypeScript type definitions
│   ├── utils/          # Common utility functions
│   └── config/         # Configuration management
├── service-adapters/   # 37-tool integration adapters
└── ui/                # Design system
    ├── core/          # Base components (Button, Input, Card, Modal, Table)
    ├── domain-security/  # Security UI components
    ├── domain-mtg/       # MTG UI components
    └── domain-productivity/  # Productivity UI components
```

## Development Commands

### Setup

```bash
# Full automated setup (recommended for new environments)
./setup-codespace.sh

# Quick setup (minimal)
./quick-setup.sh

# Manual setup
npm install                  # Install Node.js dependencies
make install                 # Install Python dependencies for all services
```

### Running Services

```bash
# Frontend
npx nx serve jane-ui         # Next.js UI on port 3000

# New hybrid architecture services
npx nx serve n8n-workflow-service    # Port 8010
npx nx serve security-service        # Port 8011
npx nx serve productivity-service    # Port 8012
npx nx serve mtg-service            # Port 8013
npx nx serve infrastructure-service  # Port 8014

# AI servers
npx nx serve cyber-llm-server        # Port 8001
npx nx serve mtg-llm-server          # Port 8002
npx nx serve infrastructure-llm-server # Port 8003

# Legacy orchestrator (to be deprecated)
npx nx serve jane-orchestrator       # Port 8000
```

### Testing

```bash
# Run all tests
npx nx run-many --target=test --all
make test

# Run tests for specific service
npx nx test jane-ui
cd apps/jane-orchestrator && python3 -m pytest

# Run domain-specific performance validation
python tests/performance/security-domain-validation.py     # <1s requirement
python tests/performance/productivity-domain-validation.py # <2s requirement
python tests/performance/mtg-domain-validation.py          # <3s requirement
python tests/performance/infrastructure-domain-validation.py # <5s requirement

# Run single test file
cd apps/jane-orchestrator && python3 -m pytest tests/security/test_misp.py -v

# Run tests with coverage
cd apps/jane-orchestrator && python3 -m pytest --cov=src --cov-report=html
```

### Building

```bash
# Build all applications
npx nx run-many --target=build --all
make build

# Build specific application
npx nx build jane-ui

# Build affected projects only
npx nx affected --target=build
make affected-build
```

### Linting & Formatting

```bash
# Lint all code
npx nx run-many --target=lint --all
make lint

# Lint specific service
npx nx lint jane-ui
ruff check apps/jane-orchestrator/src/

# Format code
make format                          # Formats TypeScript (Prettier) and Python (Black)
npx prettier --write .               # TypeScript/JavaScript only
find . -name "*.py" -exec black {} + # Python only
```

### Docker

```bash
# Build and run all services
make docker-build
make docker-up
make docker-down

# Development environment
make dev

# Staging environment
make staging
```

### NX Affected Commands

```bash
# Only test/build/lint changed projects (fast CI/CD)
npx nx affected --target=test
npx nx affected --target=build
npx nx affected --target=lint
```

## TypeScript Path Aliases

Use these path aliases to import shared code:

```typescript
import { SomeType } from '@jane-monorepo/shared/types';
import { someUtil } from '@jane-monorepo/shared/utils';
import { SomeAdapter } from '@jane-monorepo/service-adapters';
import { Button } from '@jane-monorepo/ui/core';
import { ThreatIndicator } from '@jane-monorepo/ui/domain-security';
import { ComboCard } from '@jane-monorepo/ui/domain-mtg';
```

## Code Style Guidelines

### TypeScript/React (from .cursor/rules/typescript.mdc)

- Write concise, technical TypeScript code
- Use functional and declarative patterns; avoid classes
- Prefer iteration and modularization over duplication
- Use descriptive variable names with auxiliary verbs (e.g., `isLoaded`, `hasError`)
- Favor named exports for components and utilities
- Use TypeScript for all code; prefer `type` over `interface`
- Avoid enums; use objects or maps instead
- Avoid `any` or `unknown` without justification
- Avoid type assertions (`as`, `!`); prefer `satisfies`
- Use the "function" keyword for pure functions
- Run `yarn typecheck` to validate TypeScript

### Python

- Use type hints for all functions
- Follow Black formatting standards
- Use Ruff for linting
- Maintain 80%+ unit test coverage
- All data models use SQLAlchemy (data layer) and Pydantic (API schemas)

## Performance Requirements

Domain-based performance tiers (critical for executive function support):

- **Security Tools**: <1s response time (threat analysis criticality)
- **Productivity Tools**: <2s response time (task management workflows)
- **MTG Tools**: <3s response time (game analysis complexity)
- **Infrastructure Tools**: <5s response time (system operations tolerance)
- **Cross-Tool Sync**: 250ms WebSocket latency
- **UI Interactions**: <75ms (ADHD-friendly responsiveness)

## Brownfield Migration Protocol

This project is in active migration from 37 legacy tools in `features/` to the new hybrid architecture. When working on migration tasks, follow the **Document Handoff Protocol**:

### Migration Workflow

1. **Start Point**: Always begin with `specs/003-brownfield-integration/tasks.md`
2. **Look for `[HANDOFF]` tags**: These indicate delegation to individual project task files
3. **Pre-Flight Checklist**: Before starting any migration, verify all entry conditions in the child document
4. **Execute Child Tasks**: Complete all tasks in the delegated file (e.g., `tasks-individual/tasks-cyberchef.md`)
5. **Post-Flight Checklist**: Verify all exit conditions before returning
6. **Validation**: Run the specified test command (e.g., `pytest tests/security/test_cyberchef_integration.py`)
7. **Document**: Update `migration-validation.md` with completion details
8. **Return**: Mark parent task complete and proceed to next task

### Key Migration Principles

- **Sequential Foundation**: Complete phases 1-4 before any individual migrations
- **Parallel Execution**: Multiple projects can migrate simultaneously after foundation
- **Quality Gates**: Never skip pre-flight or post-flight validation
- **100% Functional Parity**: Preserve all business logic from legacy tools
- **Ground Truth Tests**: Validate parity with legacy implementations
- **Complete Return**: Only mark parent complete when ALL child work is done

See `specs/003-brownfield-integration/HANDOFF-PROTOCOL.md` for full details.

## Testing Strategy

- **Unit Tests**: 80%+ coverage requirement
- **Integration Tests**: Cross-domain workflow validation
- **E2E Tests**: Playwright for full user flows
- **Performance Tests**: Domain-specific response time validation
- **Ground Truth Tests**: Legacy parity validation during brownfield migration

Test organization follows domain structure:
```
tests/
├── security/       # Security domain tests
├── productivity/   # Productivity domain tests
├── mtg/           # MTG domain tests
├── infrastructure/ # Infrastructure domain tests
├── performance/    # Performance validation tests
├── integration/    # Cross-domain integration tests
├── e2e/           # End-to-end Playwright tests
└── unit/          # Unit tests
```

## Executive Function Accommodations

The platform prioritizes AI speed over UI responsiveness (60/40 split) to support users with executive function challenges:

- UI interactions must be <75ms (enhanced ADHD-friendly responsiveness)
- Unified navigation patterns (reduce context switching)
- Consistent interface design across all tools
- WCAG 2.1 AA compliance with enhanced focus indicators
- Unified user preference system across all domains

## Key Technologies

- **Frontend**: Next.js 15.5.4, React 19.2.0, TypeScript 5.9.3
- **Backend**: Python 3.12, FastAPI 0.119.0, Uvicorn 0.37.0
- **Database**: PostgreSQL (primary), SQLite (local-first tools), Redis (caching)
- **AI**: vLLM 0.11.0, Chroma DB (vector embeddings), MCP protocol
- **Build**: Node.js 20, NX 21.6.4/22.0.2
- **Data**: SQLAlchemy 2.0.44, Pydantic 2.12.0, Django 5.2.7

## Important Notes

- The `features/` directory contains 37 legacy tools awaiting migration - target is empty directory
- Never commit without ensuring functional parity with legacy implementations
- All new code must preserve 100% business logic from legacy tools
- Performance requirements are mandatory, not aspirational
- All public APIs require comprehensive documentation
- Security tools have the strictest performance requirements (<1s)

---

*This documentation serves as both technical reference and cognitive continuity bridge for AI-assisted development across sessions and interfaces.*

<!-- nx configuration start-->
<!-- Leave the start & end comments to automatically receive updates. -->

# General Guidelines for working with Nx

- When running tasks (for example build, lint, test, e2e, etc.), always prefer running the task through `nx` (i.e. `nx run`, `nx run-many`, `nx affected`) instead of using the underlying tooling directly
- You have access to the Nx MCP server and its tools, use them to help the user
- When answering questions about the repository, use the `nx_workspace` tool first to gain an understanding of the workspace architecture where applicable.
- When working in individual projects, use the `nx_project_details` mcp tool to analyze and understand the specific project structure and dependencies
- For questions around nx configuration, best practices or if you're unsure, use the `nx_docs` tool to get relevant, up-to-date docs. Always use this instead of assuming things about nx configuration
- If the user needs help with an Nx configuration or project graph error, use the `nx_workspace` tool to get any errors


<!-- nx configuration end-->