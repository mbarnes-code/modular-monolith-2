<!--
Sync Impact Report:
- Version change: none → 1.0.0
- Modified principles: none (initial creation)
- Added sections: Core Principles (5), Technology Standards, Development Quality Gates, Governance
- Removed sections: none
- Templates requiring updates: ✅ All templates reviewed and aligned
- Follow-up TODOs: none
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

**Rationale**: The platform serves real-time security analysis, interactive MTG tools, and productivity applications where performance directly impacts user effectiveness.

### V. Modular Architecture Integrity
The monorepo structure MUST maintain clear boundaries and dependencies:
- **Service Independence**: Each app MUST be deployable independently with minimal coupling
- **Library Reusability**: Shared libraries MUST be domain-agnostic and well-documented
- **Feature Organization**: Domain features (`features/`) MUST not create circular dependencies
- **API Contracts**: Service interfaces MUST be versioned and backward compatible
- **Configuration Management**: Environment-specific configs MUST be externalized and validated

**Rationale**: Modular architecture enables independent development teams, selective deployments, and prevents monolithic coupling while maintaining shared infrastructure benefits.

## Technology Standards

**Approved Stack**: Node.js 20, Python 3.12, TypeScript 5.9.3, Next.js 15.5.4, React 19.2.0, FastAPI 0.119.0, NX 21.6.4
**Database**: PostgreSQL for transactional data, appropriate vector databases for LLM embeddings
**Security**: HTTPS required, authentication via JWT, input validation on all endpoints
**Containerization**: Docker required for all services, Kubernetes manifests for production
**Monitoring**: Structured logging (JSON), metrics collection, distributed tracing for multi-service operations

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

**Version**: 1.0.0 | **Ratified**: 2025-10-18 | **Last Amended**: 2025-10-18
