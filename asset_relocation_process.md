Brownfield Asset Relocation Process (Post-Dependency Hoisting)
Phase 1: Foundation (Completed - Dependency Hoisting)
✅ Dependency Consolidation: Unified package management, build systems
✅ Workspace Structure: Domain boundaries, service adapters
✅ Baseline Configuration: Consolidated configs, linting, Docker
Phase 2: Data Layer Migration
Goal: Establish unified data architecture before moving business logic

Schema Analysis & Mapping

Extract existing schemas from all legacy systems
Design unified schema with domain separation
Create data migration scripts with rollback capabilities
Data Format Conversion

Handle diverse formats (SQL, NoSQL, CRDT, binary, time-series)
Implement conversion utilities with integrity validation
Test data preservation with checksums
Authentication Consolidation

Merge separate user systems into unified auth
Preserve existing access patterns during transition
Implement session management for concurrent tools
Phase 3: API Layer Abstraction
Goal: Create unified API surface before moving UIs

Service Interface Design

Extract existing API patterns from legacy tools
Design domain-specific API boundaries
Create backward-compatible adapters
Business Logic Extraction

Identify core algorithms vs presentation logic
Extract business rules into domain services
Implement validation layers
Phase 4: UI Integration Strategy
Goal: Unified user experience while preserving functionality

Interface Preservation Analysis

Categorize UIs: iframe embedding vs component integration vs API-only
Document existing user workflows
Design unified navigation patterns
Progressive UI Migration

Start with wrapper/iframe approach for complex UIs
Gradually migrate to native components where feasible
Maintain user familiarity during transition
Phase 5: Domain-by-Domain Asset Relocation
Goal: Move complete business domains while maintaining operations

This is where the current tasks pick up. The typical pattern per domain:

Ground Truth Establishment

Document expected behavior from original systems
Create comprehensive test suites
Establish performance baselines
Asset Porting (Category-Based)

Category A (Complex Algorithms): Preserve in microservices if needed
Category B (Domain Logic): Migrate to modular monolith services
Category C (Utilities): Move to shared libraries
Validation & Integration

Run automated regression tests against original
Validate performance meets domain requirements
Test cross-domain workflows
Phase 6: Optimization & Polish
Goal: Performance tuning and production readiness

Performance Optimization

Domain-specific performance validation
Cross-tool synchronization optimization
Resource usage optimization
Production Hardening

Security audit of consolidated system
Monitoring and alerting setup
Disaster recovery procedures
Key Brownfield Principles
1. Incremental Migration
Never "big bang" the entire system at once
Always maintain operational capability
Rollback procedures for every step
2. Ground Truth Preservation
Original systems remain operational during migration
Comprehensive testing against known-good behavior
Data integrity validation at every step
3. Category-Based Preservation
Category A: Complex algorithms that need special handling
Category B: Standard business logic suitable for integration
Category C: Utilities that can be shared/consolidated
4. Risk Mitigation
Extensive backup strategies
Automated testing frameworks
Performance monitoring
User workflow preservation
Why This Order Matters
Dependencies First: Can't move code without proper build/package management
Data Second: Business logic depends on data access patterns
APIs Third: UIs depend on service interfaces
UIs Fourth: User experience depends on underlying services
Domain Migration: Complete vertical slices with full testing
Optimization Last: Performance tuning after functionality is preserved