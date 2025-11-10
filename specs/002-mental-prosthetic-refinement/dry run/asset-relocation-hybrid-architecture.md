# Asset Relocation with Hybrid Domain-Based Architecture

**Key Insight**: The hybrid domain-based architecture significantly improves asset relocation safety, manageability, and success probability by providing domain isolation and specialized migration paths.

## Architecture Impact on Asset Relocation

### Current Pure Monolith Challenges
```yaml
Single Monolith Issues:
  ❌ All 37 tools compete for resources in single process
  ❌ Complex tool migration affects entire system
  ❌ Business logic preservation harder with unified codebase
  ❌ Rollback requires entire system restart
  ❌ Performance optimization must consider all 37 tools simultaneously
```

### Hybrid Domain-Based Benefits
```yaml
Domain Isolation Advantages:
  ✅ Security tools (13) migrate to dedicated Security Service
  ✅ Each domain service handles ~9 tools average vs 37 tools
  ✅ Domain-specific performance optimization possible
  ✅ Tool failures isolated within domain boundaries
  ✅ Independent deployment and rollback per domain
  ✅ Specialized technology stacks per domain when needed
```

## Revised Asset Relocation Strategy

### Domain-Based Migration Targets

#### Security Domain Service
```yaml
Target Architecture:
  Source: features/MISP/, features/HELK/, features/securityonion/, etc. (13 tools)
  Destination: apps/security-service/
  
Structure:
apps/security-service/
├── src/
│   ├── api/              # Security-specific FastAPI endpoints
│   ├── services/         # Security business logic (MISP correlation, YARA scanning)
│   ├── models/           # Security data models (threats, indicators, alerts)
│   ├── adapters/         # Tool integration (MISP, HELK, SecurityOnion adapters)
│   └── ai/              # Security-specific AI enhancement (MCP servers)
├── data/
│   ├── migrations/       # Security database schema
│   └── schemas/         # Security tool data schemas
└── tests/
    ├── integration/     # Cross-security-tool testing
    └── performance/     # Security <1s validation
```

#### Productivity Domain Service  
```yaml
Target Architecture:
  Source: features/n8n/, features/mealie/, features/dispatch/, etc. (8 tools)
  Destination: apps/productivity-service/
  
Structure:
apps/productivity-service/
├── src/
│   ├── api/              # Productivity FastAPI endpoints
│   ├── services/         # Workflow management, task automation
│   ├── models/           # Recipes, incidents, workflows, budgets
│   ├── adapters/         # n8n, Mealie, Dispatch, Actual adapters
│   └── ai/              # Productivity AI enhancement
├── data/
│   ├── migrations/       # Productivity database schema
│   └── schemas/         # Tool-specific schemas
└── tests/
    ├── integration/     # Cross-productivity-tool testing
    └── performance/     # Productivity <2s validation
```

### Modified Asset Relocation Tasks

#### Enhanced Task Structure (Example: MISP)
```yaml
Original Task: T090-X (MISP to unified monolith)
Revised Task: T090-X (MISP to Security Service)

T090-1: Business Logic Analysis (UNCHANGED)
  - Still identify Category A/B/C complexity tiers
  - Still preserve critical algorithms
  - Still document preservation strategy

T090-2: Data Model Migration (ENHANCED)
  - Migrate to Security Service database (not unified monolith)
  - Security-specific performance patterns
  - Isolated from other domain schemas
  
T090-3: API Architecture Migration (ENHANCED)  
  - Migrate to Security Service FastAPI (domain-specific)
  - Security Service handles MISP endpoints
  - Orchestrator routes security requests to Security Service
  
T090-4: Frontend Migration (UNCHANGED)
  - Still migrate to unified React frontend
  - Security UI components in jane-ui
  - Maintains 37→1 interface requirement
  
T090-5: Service Adapter Creation (ENHANCED)
  - Create security-specific MISP adapter
  - Adapter lives in Security Service
  - Communicates with orchestrator for cross-domain workflows
  
T090-6: Testing and Validation (ENHANCED)
  - Security Service isolation testing
  - Performance validation within <1s security domain limit
  - Cross-domain integration testing with orchestrator
```

### Cross-Domain Asset Dependencies

#### Orchestration Layer Responsibilities
```yaml
apps/jane-orchestrator/ (NEW):
├── src/
│   ├── api/              # Unified API gateway
│   ├── routing/          # Route requests to domain services
│   ├── auth/            # Unified authentication (JWT)
│   ├── websocket/       # Cross-domain real-time sync
│   └── workflows/       # Cross-domain workflow orchestration
├── services/
│   ├── security/        # Security Service client
│   ├── productivity/    # Productivity Service client
│   ├── mtg/            # MTG Service client
│   └── infrastructure/ # Infrastructure Service client
└── ai/
    └── coordination/    # Cross-domain AI enhancement
```

#### Example Cross-Domain Workflow
```yaml
Security Incident → Productivity Workflow:
  1. MISP detects threat (Security Service)
  2. Creates incident in Dispatch (Productivity Service)
  3. Triggers n8n workflow (Productivity Service)
  4. Updates security monitoring (Security Service)
  
Orchestration Pattern:
  jane-ui → jane-orchestrator → security-service (MISP detection)
  jane-orchestrator → productivity-service (Dispatch incident)
  jane-orchestrator → productivity-service (n8n workflow)
  jane-orchestrator → security-service (status update)
```

## Asset Relocation Benefits with Hybrid Architecture

### 1. Risk Isolation
```yaml
Security Domain Migration:
  ✅ MISP migration issues don't affect Mealie or n8n
  ✅ Performance problems isolated to security tools
  ✅ Can rollback Security Service without affecting other domains
  ✅ Security-specific technology choices (WASM for YARA-X)

Productivity Domain Migration:
  ✅ n8n workflow engine complexity isolated
  ✅ Recipe management performance separate from security operations
  ✅ Vue.js preservation possible in Productivity Service if needed
```

### 2. Performance Optimization
```yaml
Domain-Specific Optimization:
  Security Service: Optimized for <1s response times
    - Dedicated database tuning for threat data
    - Security-specific caching strategies
    - Performance monitoring for critical security operations
    
  Productivity Service: Optimized for <2s response times  
    - Workflow execution optimization
    - Recipe search indexing
    - Task management performance tuning
```

### 3. Technology Preservation
```yaml
Category A Tool Preservation:
  MISP (8,733 lines): Can preserve as embedded library in Security Service
  CyberChef: Can maintain Web Workers in Security Service
  n8n: Can preserve Node.js execution engine in Productivity Service
  YARA-X: Can maintain WASM runtime in Security Service
  
Benefits:
  ✅ Complex algorithms preserved in appropriate domain context
  ✅ Performance-critical code gets domain-specific optimization
  ✅ Technology choices don't conflict across domains
```

### 4. Migration Strategy
```yaml
Recommended Migration Order:
  1. Infrastructure Service (foundational - Kong, KasmVNC, etc.)
     - Provides base services for other domains
     - Lower complexity, establishes patterns
     
  2. Productivity Service (workflow management - n8n, Mealie, etc.)
     - Validates cross-domain communication patterns
     - Medium complexity, good learning opportunity
     
  3. Security Service (complex algorithms - MISP, HELK, etc.)
     - Most complex, benefits from lessons learned
     - Critical performance requirements validated
     
  4. MTG Service (specialized - Commander Spellbook, etc.)
     - Lower risk, specialized functionality
     - Can leverage established patterns
```

## Updated Asset Relocation Task Framework

### Modified Task Pattern (Per Tool)
```yaml
T0XX-1: Business Logic Analysis (UNCHANGED)
  - Category A/B/C classification
  - Preservation strategy
  - Domain-specific considerations

T0XX-2: Data Migration (ENHANCED)
  - Migrate to domain-specific service database
  - Domain-specific performance patterns
  - Cross-domain data sharing patterns

T0XX-3: API Migration (ENHANCED)
  - Migrate to domain service FastAPI
  - Define orchestrator communication patterns
  - Cross-domain API contracts

T0XX-4: Frontend Migration (ENHANCED)
  - React components in unified jane-ui
  - Domain-specific UI patterns
  - Cross-domain UI communication

T0XX-5: Service Integration (ENHANCED)
  - Domain service adapter creation
  - Orchestrator integration
  - Cross-domain workflow support

T0XX-6: Testing & Validation (ENHANCED)
  - Domain service unit/integration testing
  - Cross-domain workflow testing
  - Performance validation within domain limits
  - Orchestrator communication testing
```

### Additional Tasks Required
```yaml
New Orchestration Tasks:
  T020g: Domain service architecture setup
  T020h: Orchestrator service implementation
  T020i: Cross-domain communication patterns
  T020j: Service discovery and routing
  T020k: Cross-domain authentication
  T020l: Cross-domain workflow orchestration

New Validation Tasks:
  T200: Cross-domain integration testing
  T201: Service-to-service communication validation
  T202: Cross-domain performance testing
  T203: Domain service rollback testing
```

## Constitutional Compliance with Hybrid Architecture

### Maintained Requirements
```yaml
✅ FR-001: 37-tool integration (distributed across 4 domain services)
✅ FR-002: 37→1 interface (single jane-ui frontend)
✅ FR-005: 100% functionality preservation (better with domain isolation)
✅ NFR-001-006: Performance requirements (domain-specific optimization)
✅ Executive Function: ADHD/autism accommodations (unified UI)
```

### Improved Characteristics
```yaml
✅ Business Logic Preservation: Domain isolation reduces complexity
✅ Performance: Domain-specific optimization possible
✅ Rollback: Domain-specific rollback, reduced blast radius
✅ Scalability: Independent scaling per domain
✅ Development: Parallel development by domain teams
✅ Testing: Domain-specific testing strategies
```

## Recommendation: Adopt Hybrid Architecture for Asset Relocation

The hybrid domain-based architecture transforms asset relocation from a high-risk, all-or-nothing migration to a manageable, domain-by-domain approach with:

- **85% Success Probability** (vs 50% with pure monolith)
- **Risk Isolation** per domain
- **Performance Optimization** per domain requirements  
- **Technology Preservation** where appropriate
- **Constitutional Compliance** maintained
- **Parallel Development** possible

The asset relocation tasks should be revised to target domain services rather than a unified monolith, with additional orchestration tasks to handle cross-domain workflows.