<!--
Sync Impact Report:
- Version change: 1.1.0 → 1.2.0 (Multi-Framework Integration Strategy)
- Modified principles: Platform Architecture Standards (business logic preservation clarification)
- Added sections: Frontend Framework Integration Strategy, Framework-Specific Migration Criteria
- Templates requiring updates: ✅ All templates updated with multi-framework approach
- Follow-up TODOs: Update copilot-instructions.md with multi-framework strategy, update jane-ui project configuration
-->

# Jane Monorepo Constitution

## Core Principles

### I. Code Quality Standards (NON-NEGOTIABLE)
All code MUST adhere to strict quality standards across the modular monolith:
- **TypeScript**: Strict mode enabled, no `any` types without explicit justification
- **Python**: Type hints required for all functions, black formatting, ruff linting
- **Code Reviews**: Mandatory for all changes, minimum 2 approvals for core services
- **Documentation**: Public APIs MUST have comprehensive documentation with examples
- **Dependency Management**: Exact versions specified, regular security updates scheduled

**Rationale**: Maintaining code quality across multiple applications and services prevents technical debt accumulation and ensures long-term maintainability.

### II. Comprehensive Testing Standards
Testing strategy MUST cover all layers of the modular monolith:
- **Unit Tests**: 80%+ coverage for all business logic, libraries MUST be independently testable
- **Integration Tests**: Required for service-to-service communication, API contracts, database interactions
- **End-to-End Tests**: Critical user journeys MUST be automated using Playwright for UI flows
- **Contract Tests**: APIs MUST have OpenAPI specifications with contract validation
- **Performance Tests**: Load testing required for all public endpoints (>1000 req/s baseline)

**Rationale**: Complex modular systems require comprehensive testing to prevent integration failures and ensure reliability across multiple domains (security, MTG, productivity, dev tools).

### III. User Experience Consistency
Consistent user experience MUST be maintained across all applications and domains:
- **Design System**: Shared UI component library (`libs/ui/`) MUST be used for all interfaces
- **Response Times**: UI interactions <200ms, API responses <500ms for standard operations
- **Error Handling**: Standardized error messages and recovery flows across all applications
- **Accessibility**: WCAG 2.1 AA compliance required, keyboard navigation supported
- **Mobile Responsiveness**: All UI components MUST support mobile viewports

**Rationale**: Users interact with multiple domains (security tools, MTG apps, productivity features) and expect consistent interaction patterns and performance.

### IV. Performance Requirements
All services MUST meet domain-specific performance benchmarks:
- **Jane Orchestrator**: Handle 1000+ concurrent requests, <500ms p95 response time
- **LLM Servers**: <2s inference time for standard queries, memory usage <8GB per server
- **Jane UI**: <2s initial page load, <100ms component interactions, bundle size <1MB
- **Database Operations**: <100ms for read operations, <500ms for complex queries
- **Memory Efficiency**: Services MUST operate within allocated container limits

**Domain-Specific Performance Tiers (CONSTITUTIONAL)**:

- **Security Tools**: <1s response (threat analysis criticality)
- **Productivity Tools**: <2s response (task management workflows)
- **MTG Tools**: <3s response (game analysis complexity)
- **Infrastructure Tools**: <5s response (system operations tolerance)
- **Cross-Tool Synchronization**: 250ms latency (real-time data flow)

**Rationale**: The platform serves real-time security analysis, interactive MTG tools, and productivity applications where performance directly impacts user effectiveness. Domain-specific tiers ensure critical security operations maintain sub-second response while allowing complexity-appropriate timing for other domains.

### V. Modular Architecture Integrity
The monorepo structure MUST maintain clear boundaries and dependencies:

- **Service Independence**: Each app MUST be deployable independently with minimal coupling
- **Library Reusability**: Shared libraries MUST be domain-agnostic and well-documented
- **Feature Organization**: Domain features (`features/`) MUST not create circular dependencies
- **API Contracts**: Service interfaces MUST be versioned and backward compatible
- **Configuration Management**: Environment-specific configs MUST be externalized and validated

**Rationale**: Modular architecture enables independent development teams, selective deployments, and prevents monolithic coupling while maintaining shared infrastructure benefits.

## Platform Architecture Standards (CONSTITUTIONAL)

**Mental Prosthetic Platform Scope**: Exactly 37 executive function tools across 4 domains (NON-NEGOTIABLE)

- **Security Domain**: 13 tools (MISP, HELK, SecurityOnion, Maltrail, YARA-X, CyberChef, Nemesis, etc.)
- **Productivity Domain**: 8 tools (n8n, Mealie, Dispatch, Actual Budget, Firecrawl, Goose, IT-Tools, Inspector)
- **MTG Domain**: 4 tools (Commander Spellbook, MTG Commander Map, MTG Scripting Toolkit, card analysis)
- **Infrastructure Domain**: 12 tools (Kong, Ghostwriter, KasmVNC, MCP servers, workflow automation, etc.)

**Executive Function Accommodations (CONSTITUTIONAL)**: ADHD/Autism-specific requirements are NON-NEGOTIABLE

- **Response Times**: UI interactions <200ms (focus maintenance), API responses <500ms standard
- **Navigation Consistency**: Identical patterns across all 37 tools, no external redirects
- **Context Switching Reduction**: 37→1 interface consolidation (95% reduction target)
- **Accessibility**: WCAG 2.1 AA compliance, keyboard navigation, focus indicators

**Business Logic Preservation (CONSTITUTIONAL)**: 100% functionality preservation across all 37 tools is NON-NEGOTIABLE

- **Framework Integrity**: Existing React-based tools (8 tools) maintain their current technology stacks to prevent business logic disruption
- **Migration Categories**:
  - **Category A (Complex Algorithms)**: Preserve as microservices or embedded libraries with existing frontend frameworks
  - **Category B (Domain Logic)**: Modularize within monolith maintaining workflow integrity and frontend technology choices
  - **Category C (Utilities)**: Integrate as shared libraries with API compatibility, migrate to Vue.js only when rewriting substantially
- **Migration Strategy**: Big-bang integration (all 37 tools simultaneously) with framework preservation approach
- **Quality Assurance**: Automated testing ensures identical functionality before and after integration regardless of frontend framework

## Development Quality Gates

**Pre-commit**: Type checking, linting, unit tests MUST pass
**Pull Request**: Integration tests, security scans, performance regression checks required
**Pre-deployment**: End-to-end test suite, load testing for affected services
**Production**: Health checks, rollback procedures, incident response documentation
**Code Complexity**: Cyclomatic complexity <10, function length <50 lines (exceptions require justification)

## Governance

This constitution supersedes all other development practices and standards. All code changes MUST demonstrate compliance with these principles.

**Amendment Process**: Constitution changes require RFC document, team review, and migration plan for existing code
**Compliance Review**: Monthly audits of code quality metrics, test coverage, and performance benchmarks
**Exception Handling**: Technical debt requiring principle violations MUST be documented with remediation timeline
**Enforcement**: CI/CD pipelines MUST enforce quality gates; non-compliance blocks deployment

**Version**: 1.2.0 | **Ratified**: 2025-10-18 | **Last Amended**: 2025-10-19
