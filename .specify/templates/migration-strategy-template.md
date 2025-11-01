# Migration Strategy: [MIGRATION NAME]

**Project**: `[###-feature-name]` | **Date**: [DATE] | **Scale**: [SMALL/MEDIUM/LARGE/EXTREME]
**Input**: Brownfield project specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.migration-strategy` command for BROWNFIELD projects only.

## Migration Overview

### Project Scale Assessment

**System Count**: [X] existing systems
**Migration Scale**: **[SMALL/MEDIUM/LARGE/EXTREME]**
**Selected Migration Method**: **[Method Name]**

```yaml
Scale Characteristics:
  Risk Level: [MEDIUM/HIGH/VERY HIGH/EXTREME]
  Timeline: [X weeks]
  Team Size: [X developers]
  Architecture Complexity: [Simple/Domain-based/Enterprise/Platform]
  Technology Diversity: [Aligned/Some diversity/Diverse/Highly diverse]
```

### Migration Method Selection

**Primary Method**: [Strangler Fig / API Gateway / Blue-Green / Event-Driven / Database-First / Branch by Abstraction]

**Method Justification**: 
[Explain why this method was selected over alternatives, considering scale, risk tolerance, resources, and business constraints]

**Alternative Methods Considered**:
- [Method 1]: [Why rejected - e.g., "Too risky for 37 projects"]
- [Method 2]: [Why rejected - e.g., "Insufficient resources for parallel infrastructure"]

## Legacy System Analysis

### System Classification

```yaml
Category A - Complex Algorithms (Strategy: Copy & Modernize):
  - [System Name]: [Complex business logic that must be preserved exactly]
  - [System Name]: [Critical algorithms, difficult to rewrite]
  
Category B - Domain Logic (Strategy: Behavior-Driven Rewrite):  
  - [System Name]: [Well-documented business rules, suitable for rewrite]
  - [System Name]: [Standard CRUD operations with clear requirements]

Category C - Utilities (Strategy: Replace or Integrate):
  - [System Name]: [Simple utilities, easy to replace]
  - [System Name]: [Standard functionality available in modern frameworks]
```

### Technology Stack Consolidation

#### High-Overlap Stacks (CONSOLIDATE)
```yaml
Primary Language Stack:
  Technology: [e.g., "Python"]
  Project Count: [X of Y total]
  Consolidation Target: [e.g., "FastAPI + SQLAlchemy unified backend"]
  
Secondary Language Stack:  
  Technology: [e.g., "JavaScript/TypeScript"]
  Project Count: [X of Y total]  
  Consolidation Target: [e.g., "React + Next.js unified frontend"]
```

#### Low-Usage Stacks (ISOLATE)
```yaml
Specialized Technology:
  Technology: [e.g., "Rust"]
  Project Count: [X of Y total]
  Isolation Strategy: [e.g., "Service adapters with gRPC interfaces"]
  
Legacy Technology:
  Technology: [e.g., "PHP 5.6"]  
  Project Count: [X of Y total]
  Isolation Strategy: [e.g., "Preserve with REST API wrappers"]
```

### Database Consolidation Strategy

**Selected Strategy**: [Central / Domain-Separated / Federated / Hybrid]

```yaml
Database Consolidation Plan:
  PostgreSQL Projects: [X projects] → [Consolidation approach]
  MySQL Projects: [X projects] → [Migration/bridge approach]  
  SQLite Projects: [X projects] → [Integration approach]
  NoSQL Projects: [X projects] → [Adaptation approach]
  File-based Storage: [X projects] → [Migration approach]
```

## Asset Relocation Plan

### File Transformation Strategy

**Philosophy**: **Copy & Preserve** (Never transform legacy files in-place)

#### File Lifecycle Process
```yaml
Phase 1 - Legacy Preservation:
  Status: "All legacy files remain untouched and active"
  Purpose: "Ground truth validation and rollback capability"
  
Phase 2 - Target Creation:  
  Status: "Business logic copied and modernized in target structure"
  Purpose: "Parallel system development with validation"
  
Phase 3 - Validation & Retirement:
  Status: "Legacy files archived after 100% validation passes" 
  Purpose: "Safe transition with preservation for reference"
```

#### Implementation Strategy Matrix
```yaml
Complex Algorithms → Strategy 1: Copy & Modernize
  Approach: "Preserve exact business logic, update syntax/framework"
  Examples: [List systems with complex algorithms]
  
Well-Documented Features → Strategy 2: Behavior-Driven Rewrite
  Approach: "Reimplement from specifications, ensure behavioral parity"
  Examples: [List well-documented systems]
  
Mixed Complexity → Strategy 3: Incremental Refactor  
  Approach: "Port in layers (data→logic→API) maintaining functionality"
  Examples: [List mixed-complexity systems]
  
Service Integration → Strategy 4: API-First Integration
  Approach: "Create service wrappers, gradual internal modernization"  
  Examples: [List service-oriented systems]
```

### Business Logic Preservation Requirements

#### Critical Preservation Areas
- **[Algorithm/System 1]**: [Why critical, what must be preserved exactly]
- **[Algorithm/System 2]**: [Specific business rules that cannot be altered]
- **[Data Process 1]**: [Data transformations that must maintain exact behavior]

#### Validation Requirements
- **Ground Truth Testing**: [How legacy behavior will be captured and validated]
- **Performance Baselines**: [Metrics that must be maintained or improved]
- **Data Integrity**: [Validation procedures for data migration]

## Risk Mitigation & Rollback Strategy

### Rollback Capabilities

#### Git-Based Rollback
```bash
# Complete system rollback
git checkout main                    # Return to pre-migration state
git checkout migration/foundation    # Rollback to foundation only
git revert [feature-commit]         # Rollback specific migration only
```

#### Service-Level Rollback
```yaml
Feature Flags:
  Purpose: "Route traffic between legacy and new systems"
  Granularity: "[Feature/Service/Domain] level switching"
  
API Gateway:
  Purpose: "Dynamic routing to legacy or new backends" 
  Rollback: "Switch routing rules without code deployment"
  
Database Rollback:
  Strategy: "[Reversible migrations / Data archival / Schema versioning]"
  Recovery Time: "[X minutes/hours] to restore legacy state"
```

### Risk Mitigation Procedures

#### Data Protection
- **Backup Strategy**: [Comprehensive backup procedures before any migration step]
- **Validation Gates**: [Checkpoints where migration can be safely halted]
- **Recovery Procedures**: [Step-by-step data recovery processes]

#### Business Continuity  
- **Parallel Operation**: [How long legacy and new systems run simultaneously]
- **Gradual Switchover**: [Process for moving users from legacy to new system]
- **Emergency Rollback**: [Procedures for immediate rollback if issues detected]

## Migration Phases

### Phase Breakdown
```yaml
Phase 1 - Setup & Legacy Environment:
  Duration: [X weeks]
  Deliverables: [Legacy system documentation, test environment setup]
  
Phase A - Technology Stack Consolidation: # MEDIUM+ scale only
  Duration: [X weeks] 
  Deliverables: [Unified development environment, database consolidation]
  
Phase 2 - Business Logic Foundation:
  Duration: [X weeks]
  Deliverables: [Target application infrastructure, empty service shells]
  
Phase 3-N - Feature Migration Phases:
  Duration: [X weeks per phase]
  Deliverables: [Migrated features with validation, parallel operation]
  
Phase Final - Legacy Retirement:
  Duration: [X weeks]
  Deliverables: [Legacy systems decommissioned, documentation archived]
```

### Success Criteria

#### Technical Milestones
- [ ] **Functional Parity**: All legacy functionality replicated in new system
- [ ] **Performance Parity**: New system meets or exceeds legacy performance benchmarks
- [ ] **Data Integrity**: 100% data migration validation with zero loss
- [ ] **Integration Continuity**: All external system integrations preserved

#### Business Milestones  
- [ ] **User Acceptance**: [X%] user acceptance rate for new system
- [ ] **Business Continuity**: Zero business disruption during migration
- [ ] **Support Reduction**: [X%] reduction in support tickets post-migration
- [ ] **Legacy Retirement**: All legacy systems safely decommissioned

## Reference Documentation

**Generated Files**:
- `specs/[###-feature]/spec.md` - Requirements and user stories
- `specs/[###-feature]/plan.md` - Technical implementation plan
- `specs/[###-feature]/tasks.md` - Detailed migration task breakdown

**Legacy Documentation**:
- `specs/[###-feature]/legacy-analysis.md` - Existing system documentation  
- `specs/[###-feature]/data-mapping.md` - Database and data migration mapping
- `specs/[###-feature]/integration-inventory.md` - External system dependencies