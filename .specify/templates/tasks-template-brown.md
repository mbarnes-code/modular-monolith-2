---
description: "Task list template for brownfield asset relocation and incremental migration - Scales from 1-3 projects to 37+ project integrations"
---

# Tasks: [MIGRATION: FEATURE NAME]

**EXTERNAL REFERENCES**: 
- Requirements: `specs/[###-feature]/spec.md`
- Architecture: `specs/[###-feature]/plan.md`
- Migration Strategy: `specs/[###-feature]/migration-strategy.md`

## � PROJECT SCALE ASSESSMENT

**MANDATORY FIRST STEP**: Determine project scale to apply appropriate risk assessment and methodology.

### Project Scale Classification

**Count your projects and select the appropriate scale:**

- **🟢 SMALL SCALE (1-3 projects)**: Standard brownfield migration
- **🟡 MEDIUM SCALE (4-10 projects)**: Complex brownfield migration  
- **🔴 LARGE SCALE (11+ projects)**: Enterprise brownfield integration
- **🚨 EXTREME SCALE (25+ projects)**: Platform consolidation

### Scale-Specific Characteristics

```yaml
Small Scale (1-3 projects):
  Risk Level: MEDIUM
  Timeline: 4-8 weeks
  Team Size: 1-3 developers
  Architecture: Simple consolidation or API integration
  Technology: Usually aligned stacks
  
Medium Scale (4-10 projects):
  Risk Level: HIGH  
  Timeline: 8-16 weeks
  Team Size: 3-6 developers
  Architecture: Domain-based services
  Technology: Some stack diversity requiring bridges

Large Scale (11+ projects):
  Risk Level: VERY HIGH
  Timeline: 16-24 weeks  
  Team Size: 6-12 specialized developers
  Architecture: Complex domain architecture + isolation
  Technology: Diverse stacks requiring isolation strategies
  
Extreme Scale (25+ projects):
  Risk Level: EXTREME
  Timeline: 24+ weeks
  Team Size: 12+ highly specialized developers  
  Architecture: Platform architecture with extensive isolation
  Technology: Highly diverse, extensive isolation required
```

**YOUR PROJECT SCALE**: [User must specify: SMALL / MEDIUM / LARGE / EXTREME]

---

## 🚨 SCALE-APPROPRIATE RISK ASSESSMENT

**USER APPROVAL REQUIRED**: Risk assessment varies dramatically by project scale.

### Scale-Specific Risk Assessment

#### 🟢 SMALL SCALE (1-3 projects) - Standard Risks

**🔴 MEDIUM RISK: Data Loss & Corruption**

- Risk: Data conversion errors during migration (2-3 databases, similar schemas)
- Impact: Limited data loss scope, manageable recovery
- Mitigation: Standard backup procedures, test migration, rollback capability
- **USER DECISION REQUIRED**: Accept risk of data migration? [Y/N]

**� LOW-MEDIUM RISK: Security & Privacy Changes**

- Risk: Security patterns altered during migration (similar auth systems)
- Impact: Limited exposure scope, similar security models
- Mitigation: Standard security audit, testing
- **USER DECISION REQUIRED**: Accept security pattern changes? [Y/N]

**🟡 LOW RISK: Performance Degradation**

- Risk: Some performance impact from integration (similar technology stacks)
- Impact: Minor user experience changes, <50% performance impact expected
- Mitigation: Performance monitoring, optimization
- **USER DECISION REQUIRED**: Accept potential performance impact? [Y/N]

**🟢 LOW RISK: System Complexity**

- Risk: Moderate increase in system complexity (3 systems → 1)
- Impact: Manageable maintenance increase, clear architecture
- Mitigation: Standard documentation, testing procedures
- **USER DECISION REQUIRED**: Accept increased maintenance complexity? [Y/N]

#### 🟡 MEDIUM SCALE (4-10 projects) - Elevated Risks

**🔴 HIGH RISK: Data Loss & Corruption**

- Risk: Data conversion across multiple databases with varying schemas
- Impact: Significant data loss potential, complex recovery scenarios
- Mitigation: Comprehensive backup strategy, staged migration, extensive testing
- **USER DECISION REQUIRED**: Accept risk of multi-database migration? [Y/N]

**� MEDIUM-HIGH RISK: Security & Privacy Changes**

- Risk: Multiple security models being consolidated
- Impact: Potential security gaps during consolidation
- Mitigation: Security audit per project, unified security framework design
- **USER DECISION REQUIRED**: Accept security consolidation risks? [Y/N]

**🟡 MEDIUM RISK: Performance Degradation**

- Risk: Integration overhead across multiple systems
- Impact: User experience degradation, up to 2x slower operations possible
- Mitigation: Performance baselines, optimization, caching strategies
- **USER DECISION REQUIRED**: Accept potential performance impact? [Y/N]

**🟡 MEDIUM RISK: Technology Stack Compatibility**

- Risk: Some incompatible technologies requiring bridges
- Impact: Integration complexity, maintenance overhead
- Mitigation: Technology bridge design, service adapter layers
- **USER DECISION REQUIRED**: Accept technology integration challenges? [Y/N]

#### 🔴 LARGE SCALE (11+ projects) - High Risks

**🔴 VERY HIGH RISK: Multi-Project Data Loss & Corruption**

- Risk: Data conversion across 11+ different systems with diverse schemas
- Impact: Major data loss potential, complex interdependencies
- Mitigation: Project-by-project backup, staged migration with checkpoints
- **USER DECISION REQUIRED**: Accept risk of large-scale data migration? [Y/N]

**🔴 HIGH RISK: Security Pattern Consolidation**

- Risk: 11+ different security models being merged
- Impact: Security vulnerabilities during complex consolidation
- Mitigation: Comprehensive security audit, unified framework, penetration testing
- **USER DECISION REQUIRED**: Accept complex security consolidation risks? [Y/N]

**🔴 HIGH RISK: Technology Stack Incompatibility**

- Risk: Multiple incompatible technologies requiring isolation strategies
- Impact: Complex architecture, significant integration challenges
- Mitigation: Domain isolation design, service adapters, technology bridges
- **USER DECISION REQUIRED**: Accept major technology integration complexity? [Y/N]

**🟡 MEDIUM-HIGH RISK: Team & Organizational Scaling**

- Risk: Requires specialized teams across multiple technology domains
- Impact: Knowledge management complexity, coordination challenges
- Mitigation: Specialized team structure, comprehensive documentation
- **USER DECISION REQUIRED**: Accept team scaling and coordination complexity? [Y/N]

#### 🚨 EXTREME SCALE (25+ projects) - Extreme Risks

**🔴 EXTREME RISK: Platform-Level Data Loss & Corruption**

- Risk: Data conversion across 25+ projects with highly diverse schemas, formats
- Impact: Catastrophic data loss potential, complex recovery scenarios
- Mitigation: Enterprise backup strategy, phased migration, extensive test environments
- **USER DECISION REQUIRED**: Accept risk of platform-scale data migration? [Y/N]

**🔴 EXTREME RISK: Security Model Consolidation**

- Risk: 25+ different security patterns being merged into unified platform
- Impact: Major security vulnerabilities, compliance violations possible
- Mitigation: Enterprise security framework, extensive auditing, gradual rollout
- **USER DECISION REQUIRED**: Accept platform security consolidation risks? [Y/N]

**🔴 EXTREME RISK: Technology Ecosystem Compatibility**

- Risk: Diverse technology ecosystem requiring extensive isolation and bridges
- Impact: Architectural complexity, long-term maintenance challenges
- Mitigation: Domain isolation architecture, extensive service adapter layers
- **USER DECISION REQUIRED**: Accept ecosystem integration complexity? [Y/N]

**🔴 HIGH RISK: Organizational Transformation**

- Risk: Requires major organizational changes, specialized expertise
- Impact: Change management complexity, potential project failure
- Mitigation: Organizational change management, phased approach, specialized teams
- **USER DECISION REQUIRED**: Accept organizational transformation requirements? [Y/N]

### 📋 SCALE-APPROPRIATE APPROVAL CHECKLIST

#### 🟢 SMALL SCALE (1-3 projects) Approval Checklist

**BEFORE PROCEEDING, USER MUST EXPLICITLY APPROVE:**

- [ ] **Data Migration Risk**: I accept standard data conversion risks with proper backups
- [ ] **Security Changes**: I approve limited security pattern modifications  
- [ ] **Performance Impact**: I accept minor performance changes for integration benefits
- [ ] **Complexity Increase**: I understand moderate system complexity increase
- [ ] **Feature Changes**: I accept that some features may work differently
- [ ] **Timeline**: I accept 4-8 week timeline with 1-3 developers

**REQUIRED USER INPUT**: Type "I ACCEPT SMALL SCALE MIGRATION RISKS" to proceed.

#### 🟡 MEDIUM SCALE (4-10 projects) Approval Checklist  

**BEFORE PROCEEDING, USER MUST EXPLICITLY APPROVE:**

- [ ] **Multi-Project Data Migration**: I accept elevated data conversion risks across multiple databases
- [ ] **Security Consolidation**: I approve consolidating multiple security patterns with validation
- [ ] **Performance Impact**: I accept potential significant performance impact for integration benefits
- [ ] **Technology Integration**: I accept technology stack compatibility challenges
- [ ] **Team Requirements**: I can provide 3-6 specialized developers for 8-16 weeks
- [ ] **Architectural Complexity**: I understand domain-based architecture complexity
- [ ] **Rollback Complexity**: I understand rollback may require domain-level coordination

**REQUIRED USER INPUT**: Type "I ACCEPT MEDIUM SCALE MIGRATION RISKS" to proceed.

#### 🔴 LARGE SCALE (11+ projects) Approval Checklist

**BEFORE PROCEEDING, USER MUST EXPLICITLY APPROVE:**

- [ ] **Large-Scale Data Migration**: I accept high risk of data conversion across 11+ systems
- [ ] **Complex Security Consolidation**: I approve merging 11+ security patterns with extensive validation
- [ ] **Technology Stack Isolation**: I accept complex technology integration requiring isolation strategies  
- [ ] **Performance Complexity**: I accept potential major performance impact across multiple systems
- [ ] **Specialized Team Requirements**: I can provide 6-12 specialized developers across multiple technology stacks
- [ ] **Extended Timeline**: I accept 16-24 week timeline with complex coordination requirements
- [ ] **Architectural Complexity**: I understand complex domain architecture with isolation requirements
- [ ] **Organizational Impact**: I accept organizational changes required for complex system management

**REQUIRED USER INPUT**: Type "I ACCEPT LARGE SCALE MIGRATION RISKS" to proceed.

#### 🚨 EXTREME SCALE (25+ projects) Approval Checklist

**BEFORE PROCEEDING, USER MUST EXPLICITLY APPROVE:**

- [ ] **Platform Data Migration Risk**: I accept extreme risk of data conversion across 25+ diverse systems
- [ ] **Enterprise Security Consolidation**: I approve platform-level security consolidation with extensive validation
- [ ] **Technology Ecosystem Integration**: I accept highly complex technology integration with extensive isolation
- [ ] **Platform Performance Impact**: I accept major performance considerations across entire platform
- [ ] **Enterprise Team Requirements**: I can provide 12+ highly specialized developers across diverse technology stacks
- [ ] **Extended Enterprise Timeline**: I accept 24+ week timeline with complex project management requirements
- [ ] **Platform Architecture Complexity**: I understand platform architecture with extensive domain isolation
- [ ] **Organizational Transformation**: I accept major organizational transformation requirements
- [ ] **Change Management**: I have change management capabilities for large-scale user transition
- [ ] **Risk Tolerance**: I have high organizational risk tolerance for potential service disruption

**REQUIRED USER INPUT**: Type "I ACCEPT EXTREME SCALE PLATFORM INTEGRATION RISKS" to proceed.

### 🤔 SCALE-APPROPRIATE ALTERNATIVE APPROACHES

#### 🟢 SMALL SCALE (1-3 projects) Alternatives

**1. Direct Integration (Recommended)**
- Consolidate all 1-3 projects into unified system
- 4-8 week timeline, manageable complexity
- Choose this for maximum integration benefits

**2. API-First Integration**  
- Keep projects separate, add unified API layer
- Lower risk, faster implementation (2-4 weeks)
- Choose this if want to minimize risks

**3. Selective Feature Integration**
- Integrate high-value features only, keep projects mostly separate
- Reduced scope, some integration benefits
- Choose this if only specific features need integration

**USER DECISION**: [DIRECT_INTEGRATION / API_FIRST / SELECTIVE / CANCEL]

#### 🟡 MEDIUM SCALE (4-10 projects) Alternatives

**1. Domain-Based Integration (Recommended)**
- Group projects into 2-3 domains, integrate within domains first
- 8-16 week phased approach, manageable complexity
- Choose this for balanced risk and integration benefits

**2. High-Value Project Integration**
- Integrate 3-5 most critical projects, leave others as services
- Reduced scope, focus on highest impact
- Choose this if want to limit integration complexity

**3. API Federation Approach**
- Unified API gateway with separate project services
- Lower integration risk, limited cross-project features
- Choose this if integration risks too high

**4. Technology Stack Integration**  
- Integrate projects with similar technology stacks first
- Focus on Python projects, or JavaScript projects, etc.
- Choose this to minimize technology integration complexity

**USER DECISION**: [DOMAIN_BASED / HIGH_VALUE / API_FEDERATION / TECH_STACK / CANCEL]

#### 🔴 LARGE SCALE (11+ projects) Alternatives

**1. Phased Domain Integration (Recommended)**
- Phase 1: Integrate similar projects (4-6 weeks)
- Phase 2: Add next domain (4-6 weeks)  
- Phase 3: Cross-domain integration (4-8 weeks)
- Choose this to manage complexity and validate approach

**2. Technology-First Integration**
- Phase 1: All Python projects (8-12 weeks)
- Phase 2: All JavaScript projects (8-12 weeks)
- Phase 3: Integrate isolated stacks (4-8 weeks)
- Choose this to minimize technology complexity

**3. Critical Path Integration**
- Identify 6-8 most critical projects for integration
- Leave remaining projects as isolated services
- Choose this to focus on highest business value

**4. API Platform Approach**
- Create unified platform with API-connected services
- Preserve individual project integrity, add unified access
- Choose this if full integration too risky

**USER DECISION**: [PHASED_DOMAIN / TECHNOLOGY_FIRST / CRITICAL_PATH / API_PLATFORM / CANCEL]

#### 🚨 EXTREME SCALE (25+ projects) Alternatives

**1. Enterprise Phased Approach (Recommended)**
- Phase 1: Pilot with 3-5 projects (8-12 weeks)
- Phase 2: Domain integration (12-16 weeks per domain)
- Phase 3: Platform integration (8-16 weeks)
- Choose this for enterprise risk management

**2. Technology Ecosystem Approach**
- Phase 1: Python ecosystem integration (12-20 weeks)
- Phase 2: JavaScript ecosystem integration (12-20 weeks)  
- Phase 3: Isolated technology bridges (8-12 weeks)
- Choose this for technology-focused consolidation

**3. Business Domain Approach**
- Phase 1: Security domain (16-20 weeks)
- Phase 2: Productivity domain (12-16 weeks)
- Phase 3: Specialized domains (8-12 weeks each)
- Choose this for business-focused consolidation

**4. Federation Platform Approach**
- Create enterprise API platform with microservice architecture
- Preserve all individual projects, add unified platform layer
- 12-20 week implementation for platform layer only
- Choose this for minimal disruption to existing projects

**5. Selective Platform Integration**
- Identify 8-12 highest value projects for platform integration
- Leave remaining 15+ projects as federated services
- Focus resources on highest impact integration
- Choose this for focused value delivery

**USER DECISION**: [ENTERPRISE_PHASED / TECHNOLOGY_ECOSYSTEM / BUSINESS_DOMAIN / FEDERATION_PLATFORM / SELECTIVE_PLATFORM / CANCEL]

---

## 📊 SCALE-APPROPRIATE COMPLETION VERIFICATION

### Project Scale Completion Tracking

#### 🟢 SMALL SCALE (1-3 projects) - Simple Tracking

**Total Projects to Migrate**: [1-3] projects
**Timeline**: 4-8 weeks

```yaml
Project Migration Status:
  ✅ Project 1 (Primary): 0/1 completed
  ⏳ Project 2 (Secondary): 0/1 completed  
  ⏳ Project 3 (Optional): 0/1 completed

Feature Categories per Project:
  ✅ Critical Business Logic: 0/X completed
  ⏳ Data Models: 0/X completed
  ⏳ API Integration: 0/X completed
  ⏳ User Interface: 0/X completed

Integration Features:
  ⏳ Cross-Project Workflows: 0/X completed
  ⏳ Unified Authentication: 0/1 completed
  ⏳ Performance Optimization: 0/X completed

OVERALL COMPLETION: 0/X features (0%)
```

#### 🟡 MEDIUM SCALE (4-10 projects) - Domain Tracking

**Total Projects to Migrate**: [4-10] projects organized into 2-3 domains
**Timeline**: 8-16 weeks

```yaml
Domain Migration Status:
  ✅ Domain 1 (Primary): 0/X projects completed
  ⏳ Domain 2 (Secondary): 0/X projects completed
  ⏳ Domain 3 (Optional): 0/X projects completed

Per-Domain Completion:
  Domain 1:
    ✅ Critical Algorithms: 0/X completed
    ⏳ Data Integration: 0/X completed
    ⏳ API Consolidation: 0/X completed
    
Technology Stack Consolidation:
  ✅ Primary Stack (Python/JavaScript): 0/X projects
  ⏳ Secondary Stack Integration: 0/X projects
  ⏳ Technology Bridge Implementation: 0/X bridges

Cross-Domain Integration:
  ⏳ Inter-Domain APIs: 0/X completed
  ⏳ Unified Authentication: 0/1 completed
  ⏳ Cross-Domain Workflows: 0/X completed

OVERALL COMPLETION: 0/X projects (0%)
```

#### 🔴 LARGE SCALE (11+ projects) - Complex Domain Tracking  

**Total Projects to Migrate**: [11+] projects across 3-4 domains
**Timeline**: 16-24 weeks

```yaml
Domain Service Migration Status:
  ✅ Security Domain: 0/X projects completed
  ⏳ Productivity Domain: 0/X projects completed
  ⏳ Infrastructure Domain: 0/X projects completed
  ⏳ Specialized Domain: 0/X projects completed

Technology Stack Status:
  High-Overlap Stacks (Consolidation):
    ✅ Python Projects: 0/X consolidated
    ⏳ JavaScript/TypeScript: 0/X consolidated
    ⏳ Database Consolidation: 0/X databases
    
  Low-Usage Stacks (Isolation):
    ⏳ Rust Projects: 0/X isolated
    ⏳ Go Projects: 0/X isolated  
    ⏳ C/C++ Projects: 0/X isolated
    ⏳ Other Languages: 0/X isolated

Architecture Components:
  ⏳ Domain Service Infrastructure: 0/4 domains
  ⏳ Service Adapter Layer: 0/X adapters
  ⏳ API Gateway Configuration: 0/1 completed
  ⏳ Cross-Domain Orchestration: 0/1 completed

OVERALL COMPLETION: 0/X projects (0%)
```

#### 🚨 EXTREME SCALE (25+ projects) - Platform Tracking

**Total Projects to Migrate**: [25+] projects across platform architecture  
**Timeline**: 24+ weeks

```yaml
Platform Integration Status:
  Phase 1 - Foundation:
    ✅ Platform Architecture: 0/1 completed
    ⏳ Domain Service Infrastructure: 0/X domains
    ⏳ Technology Isolation Framework: 0/1 completed
    
  Phase 2 - Domain Integration:  
    ✅ Security Domain (X projects): 0/X completed
    ⏳ Productivity Domain (X projects): 0/X completed
    ⏳ MTG Domain (X projects): 0/X completed
    ⏳ Infrastructure Domain (X projects): 0/X completed
    
  Phase 3 - Platform Features:
    ⏳ Cross-Domain Orchestration: 0/1 completed
    ⏳ Unified Platform UI: 0/1 completed
    ⏳ Platform-Level Monitoring: 0/1 completed

Technology Ecosystem Status:
  Primary Consolidation (High Overlap):
    ✅ Python Ecosystem: 0/X projects
    ⏳ JavaScript/TypeScript Ecosystem: 0/X projects
    ⏳ Database Consolidation: 0/X databases
    
  Isolation Architecture (Low Usage):
    ⏳ Rust Isolation: 0/X projects
    ⏳ Go Isolation: 0/X projects
    ⏳ PHP Isolation: 0/X projects
    ⏳ Java Isolation: 0/X projects
    ⏳ C/C++ Isolation: 0/X projects

Platform Architecture Components:
  ⏳ Domain Service Framework: 0/X domains
  ⏳ Service Adapter Architecture: 0/X adapters  
  ⏳ API Gateway Platform: 0/1 completed
  ⏳ Orchestration Platform: 0/1 completed
  ⏳ Monitoring & Observability: 0/1 completed

OVERALL COMPLETION: 0/X projects (0%)
```

### Completion Validation Protocol

**Phase-by-Phase Completion Criteria:**

**Foundation Complete** ✅ When:
- [ ] Legacy environment operational with baseline testing
- [ ] Target framework infrastructure ready
- [ ] All analysis cross-references validated
- [ ] Performance baselines documented

**Feature Complete** ✅ When:
- [ ] Ground truth test passes (proves legacy behavior)
- [ ] Validation test passes (proves new implementation matches)
- [ ] Integration test passes (proves end-to-end functionality)
- [ ] Performance test meets baseline requirements
- [ ] Security validation passes (if applicable)

**Migration Complete** ✅ When:
- [ ] ALL [Logic: ...] references have passing validation tests
- [ ] ALL analysis findings addressed and validated
- [ ] Performance benchmarks meet acceptance criteria
- [ ] User acceptance testing completed successfully
- [ ] Production validation in real environment successful
- [ ] Documentation and rollback procedures complete

### Automated Completion Verification

**Run this command to check completion status:**
```bash
python scripts/verify_migration_completion.py --full-report
```

**Expected Output When Complete:**
```
🎉 MIGRATION COMPLETION VERIFIED
================================
✅ All Features Migrated: X/X (100%)
✅ All Tests Passing: Ground Truth, Validation, Integration
✅ Performance Validated: Within acceptable thresholds  
✅ User Acceptance: Completed and approved
✅ Production Ready: All environments validated

📋 SUMMARY:
- Features Successfully Migrated: X
- Technical Debt Eliminated: [List eliminated complexities]
- Performance Impact: [Actual measured impact]
- Integration Benefits: [New cross-system capabilities]

🔄 NEXT STEPS:
- Archive legacy systems: [List legacy assets to remove]
- Begin production deployment
- Monitor system performance and user feedback
```

### User Acceptance Criteria

**Migration is NOT complete until user confirms:**
- [ ] **Functional Parity**: "I can perform ALL my original workflows"
- [ ] **Performance Acceptable**: "System performance meets my daily use needs"  
- [ ] **Data Integrity**: "All my data migrated correctly with no loss"
- [ ] **Integration Value**: "New integrated features provide expected benefits"
- [ ] **Stability**: "System runs reliably for my production use"

**Required User Sign-off**: "MIGRATION COMPLETE - APPROVED FOR PRODUCTION USE"

---

## Progressive Technology Stack Consolidation Strategy

**PURPOSE**: Systematic approach to consolidate high-overlap technology stacks first, then address remaining isolated stacks strategically. **Technology consolidation and business logic migration are separate concerns that should be addressed in phases.**

### Technology Stack Analysis and Consolidation Planning

**MANDATORY FOR MEDIUM+ SCALE**: Before business logic migration, analyze and prioritize technology stack consolidation opportunities.

#### High-Overlap Stack Consolidation (Phase A - Infrastructure First)

**Identify your high-overlap stacks from project analysis:**

```yaml
Technology Stack Analysis Template:
  [Language 1] Projects: [Count, e.g., 15/20 projects]
    Frameworks: [List, e.g., FastAPI (5), Django (4), Flask (6)]
    Consolidation Strategy: [e.g., Unified Python 3.12 environment + FastAPI primary]
    
  [Language 2] Projects: [Count, e.g., 12/20 projects]  
    Frameworks: [List, e.g., React (6), Vue (3), Express (3)]
    Consolidation Strategy: [e.g., Node.js 20 + TypeScript 5.9 + React primary]
    
  [Database] Projects: [Count, e.g., 10/20 projects]
    Current State: [e.g., 10 separate PostgreSQL instances, varying schemas]
    Consolidation Strategy: [Choose from database strategies below]
```

### Database Consolidation Strategies

**Choose based on your project analysis and domain boundaries:**

**Option 1: Central Database Consolidation**
- **Approach**: Single database instance with consolidated schemas
- **Benefits**: Simplified management, cross-project queries, unified backup
- **Risks**: Schema conflicts, single point of failure, complex migrations
- **Best For**: Projects with similar data models and access patterns

**Option 2: Domain-Based Database Architecture**  
- **Approach**: Separate databases per domain (e.g., Security, Admin, Analytics)
- **Benefits**: Domain isolation, parallel development, clearer boundaries
- **Risks**: Cross-domain queries require API calls, data synchronization complexity
- **Best For**: Projects with distinct business domains

**Option 3: Federated Database Strategy** 
- **Approach**: Keep existing databases, add data synchronization and unified query layer
- **Benefits**: Minimal disruption, gradual consolidation, preserve existing optimizations
- **Risks**: Data synchronization complexity, potential consistency issues
- **Best For**: Complex existing schemas that are difficult to merge

**Option 4: Hybrid Database Architecture**
- **Approach**: Central shared data + domain-specific databases
- **Benefits**: Flexibility, shared reference data, domain autonomy
- **Risks**: Most complex to manage, requires careful data architecture
- **Best For**: Mixed scenarios with both shared and domain-specific data needs

### Technology Consolidation Decision Matrix

**For each technology stack in your project, evaluate:**

| Stack | Project Count | Consolidation Complexity | Business Impact | Decision |
|-------|---------------|-------------------------|-----------------|----------|
| [Primary Language] | X/Total | Low-Medium | High | **CONSOLIDATE** |
| [Secondary Language] | X/Total | Low-Medium | High | **CONSOLIDATE** |  
| [Primary Database] | X/Total | Medium | High | **CONSOLIDATE** (choose strategy) |
| [Container Tech] | X/Total | Low | Medium | **CONSOLIDATE** |
| [Specialized Tech 1] | X/Total | High | Medium | **ISOLATE** with adapters |
| [Specialized Tech 2] | X/Total | Medium | Medium | **ISOLATE** with monitoring |
| [Legacy Tech] | X/Total | High | High* | **ISOLATE** with data bridges |

*High business impact due to critical legacy systems

### Progressive Consolidation Phases (MEDIUM+ Scale)

#### Phase A: High-Overlap Stack Consolidation (Weeks 1-X)

**Purpose**: Consolidate the technology stacks with highest project overlap first to maximize integration benefits.

**Example Tasks for Primary Language Stack:**
- [ ] **[Language] Environment Unification**: Create unified environment supporting all current frameworks
- [ ] **Database Schema Analysis**: Analyze all database schemas for consolidation opportunities  
- [ ] **Database Consolidation Strategy**: Implement chosen database strategy (Central/Domain/Federated/Hybrid)
- [ ] **[Language] Framework Bridges**: Create bridges between framework patterns in unified environment
- [ ] **Cross-Project Testing**: Validate all projects work in unified environment

**Example Tasks for Secondary Language Stack:**
- [ ] **[Language] Toolchain Unification**: Standardize on unified build tools and dependencies
- [ ] **Framework Strategy**: Choose primary framework and create bridges for others
- [ ] **Package Management**: Consolidate dependencies, resolve version conflicts
- [ ] **Cross-Project Testing**: Validate all projects work with unified toolchain

#### Phase B: Low-Usage Stack Isolation Assessment (Weeks X+1 to X+2)

**Purpose**: After high-overlap consolidation, assess remaining isolated stacks and their integration needs.

**Remaining Stacks Analysis Template:**
```yaml
Remaining Isolated Stacks:
  [Specialized Tech 1] (X projects): 
    Assessment: [e.g., Complex native dependencies, performance critical]
    Strategy: Keep isolated with service adapters
    Integration: [e.g., REST APIs or gRPC to communicate with consolidated stacks]
    
  [Legacy Tech] (X projects):
    Assessment: [e.g., Legacy framework, complex business logic]
    Strategy: Isolate but enhance with data bridges
    Integration: [e.g., Database synchronization + API adapters]
```

#### Phase C: Service Adapter and Integration Layer (Weeks X+3 to X+4)

**Purpose**: Connect isolated stacks to consolidated environment through service adapters.

- [ ] **API Gateway Configuration**: Route requests to appropriate consolidated or isolated services
- [ ] **Service Adapter Development**: Create adapters for each isolated stack 
- [ ] **Data Synchronization**: Implement data bridges between consolidated and isolated systems
- [ ] **Unified Authentication**: Extend consolidated auth system to isolated stacks via adapters
- [ ] **Monitoring Integration**: Include isolated stacks in unified monitoring and logging

### Consolidation Benefits Tracking

**High-Overlap Stack Consolidation Delivers:**
- **Unified Development Environment**: Single environment for majority of projects  
- **Simplified Database Management**: Reduced from X databases to [chosen strategy]
- **Shared Dependencies**: Eliminated duplicate libraries and version conflicts
- **Cross-Project Features**: Easier data sharing and API integration
- **Simplified CI/CD**: Unified build and deployment pipelines
- **Reduced Infrastructure**: Fewer containers, databases, and services to manage

**Isolated Stack Strategy Delivers:**
- **Technology Preservation**: Keep critical tools in their optimal environments
- **Risk Mitigation**: Avoid disrupting complex legacy systems
- **Integration Benefits**: Service adapters provide unified access without code changes
- **Future Flexibility**: Can progressively consolidate isolated stacks later

### Integration with Migration Phases

**Technology consolidation phases integrate with existing template phases:**

1. **Phase 1 (Setup)**: Project analysis and scale assessment
2. **Phase A-C (Technology Consolidation)**: Infrastructure consolidation BEFORE business logic
3. **Phase 2+ (Foundation & Business Logic)**: Business logic migration with pre-consolidated stacks

This approach **separates technology concerns from business logic concerns**, reducing risk and complexity.

### Key Template Improvements Summary

**Insight from 37-Project Test Scenario**: Technology stack consolidation and business logic migration are separate concerns that should be addressed in phases.

**Template Enhancements Added**:

1. **Progressive Technology Consolidation Strategy**: New Phase A for MEDIUM+ scale projects
   - High-overlap stack consolidation BEFORE business logic migration
   - Database consolidation strategies with clear decision framework
   - Low-usage stack isolation with service adapters
   - Technology consolidation decision matrix for systematic evaluation

2. **Separated Phase Structure**: 
   - **Phase 1**: Setup & Legacy Environment (all scales)
   - **Phase A**: Technology Stack Consolidation (MEDIUM+ scale only) 
   - **Phase 2**: Business Logic Foundation (using consolidated infrastructure)
   - **Phase 3+**: Feature Migration (business logic with simplified infrastructure)

3. **Scale-Specific Technology Integration**:
   - **SMALL scale**: Skip Phase A, direct integration (infrastructure usually aligned)
   - **MEDIUM scale**: Technology-first domain methodology with consolidated stacks
   - **LARGE scale**: Enterprise technology consolidation before domain migration  
   - **EXTREME scale**: Platform technology ecosystem consolidation first

4. **Benefits of Separation**:
   - Reduced risk through progressive consolidation of proven compatible stacks
   - Simplified business logic migration with pre-consolidated infrastructure
   - Clear decision points for database strategies and technology choices
   - Parallel development enabled after technology infrastructure ready
   - "Fail fast" on technology compatibility before business logic investment

**When to Use Technology Consolidation Phase A**:
- MEDIUM+ scale projects (4+ projects)
- Multiple technology stacks with high overlap (e.g., Python in 15+ projects)
- Database consolidation opportunities (multiple instances of same database)
- Mix of consolidatable and specialized technologies requiring isolation strategy

**When to Skip Phase A**:
- SMALL scale projects (1-3 projects) with usually aligned technology stacks
- Projects already using identical technology stacks
- Single-project migrations or simple API integrations

---

**Input (Spec)**: Design documents from `/specs/[###-feature-name]/` 
**Input (Legacy)**: Legacy codebase path [e.g., /features/MISP/] 
**Prerequisites**: plan.md (required), spec.md (required), **project_analysis_report.md (MANDATORY)**, research.md, data-model.md, contracts/

**Project Analysis Integration**: This template requires a comprehensive project analysis (using project_analysis_template.md) to understand:
- Section 4 (Business Logic) - Critical algorithms that must be preserved exactly
- Section 2 (Data Architecture) - Data models and relationships for migration planning  
- Section 3 (API Architecture) - Authentication, endpoints, and integration patterns
- Section 5 (External Integrations) - Third-party services and failure handling
- Section 8 (Performance Characteristics) - Baseline metrics for regression prevention
- Section 11 (Domain Knowledge) - Business rules and tribal knowledge preservation
- Section 9 (Security & Compliance) - Security patterns that must be maintained

**Migration Philosophy**: Evidence-based brownfield asset relocation with incremental feature migration to preserve 100% functional parity while modernizing architecture.

**Core Migration Loop**: For each feature, follow the repeating cycle informed by analysis findings:
1. **Ground Truth Test** → Establish current behavior baseline against legacy code
2. **Validation Test** → Create target test that initially fails (new code doesn't exist yet)  
3. **Port Logic** → Migrate exact business logic maintaining behavioral characteristics
4. **Run Validation** → New code must pass validation test (MUST pass before proceeding)
5. **Integrate** → Wire proven logic into target architecture
6. **Full Test** → End-to-end validation of complete feature

**Tests**: Tests are MANDATORY for all migration tasks. The "Ground Truth" test (testing the original code) must be written first to establish irrefutable behavioral baselines from analysis documentation.

**Implementation Requirement**: This template requires ACTUAL feature implementation, not scaffolding. Tasks marked "Port Logic" must result in working business logic that passes validation tests. Use the implementation strategies provided (Copy & Modernize, Behavior-Driven Rewrite, Incremental Refactor, API-First Integration) to ensure complete feature migration.

**Organization**: Tasks are grouped by Legacy Feature AND cross-referenced with Project Analysis sections to ensure 1:1 functional parity and comprehensive coverage of all documented behaviors.

## Format: [ID] [P?] [Feature] [Logic: <legacy_file::function>] [Analysis: Section.#] Description
- [P]: Can run in parallel
- [Feature]: Which legacy feature this task belongs to (e.g., F1: Publishing)  
- [Logic]: The exact legacy code being replaced. This is not optional.
- [Analysis]: MANDATORY reference to project_analysis_report.md section for validation and context

## Path Conventions
- **New Project**: [e.g., apps/PROJECT/src/] at repository root
- **Legacy Project**: [e.g., features/MISP/app/Model/]
- **Analysis Report**: project_analysis_report.md sections for comprehensive validation and behavioral documentation
- Paths shown below assume single project - adjust based on plan.md structure

## Analysis-Driven Migration Benefits

**Why Project Analysis is Mandatory:**
- **Business Logic Preservation**: Section 4 documents critical algorithms with complexity analysis - essential for determining what can/cannot be refactored
- **Performance Baseline Protection**: Section 8 provides concrete metrics - prevents regressions during migration  
- **Integration Continuity**: Section 5 documents external service dependencies and failure modes - prevents production outages
- **Domain Knowledge Capture**: Section 11 captures tribal knowledge and workarounds - prevents loss of undocumented business rules
- **Security Pattern Preservation**: Section 9 documents auth flows and security measures - prevents vulnerabilities
- **Data Integrity Assurance**: Section 2 maps exact field relationships and constraints - prevents data corruption during migration

## Incremental Migration Methodology

**Core Principle**: Preserve 100% functional parity through incremental feature-by-feature migration with continuous validation.

**The Repeating Loop**: Each feature follows this exact pattern:
```
Ground Truth Test (Legacy) → Validation Test (Target) → Port Logic → Run Validation (MUST PASS) → Integrate → Full Test
```

**Key Success Criteria**: 
- A task is NOT "done" when code is written - it's "done" when validation tests pass AND analysis requirements met
- Each feature can be migrated independently and in parallel (after analysis validation)
- Ground truth tests provide irrefutable behavioral baselines informed by analysis documentation
- No feature proceeds to integration until validation passes AND analysis cross-checks complete
- Analysis findings drive migration decisions and validation criteria

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

## Phase 1: Setup & Legacy Environment

**Purpose**: Initialize target project and establish legacy testing environment for ground truth validation.

**Phase 1 Risks & Mitigation:**
- **Risk**: Legacy environment setup fails or performs differently than production
- **Mitigation**: Document exact legacy environment requirements, use containerization for consistency
- **Validation**: Legacy system must pass all existing workflows before proceeding

- [ ] T001 Create new project structure per implementation plan
- [ ] T002 [Ground Truth] Setup legacy test environment: Create isolated environment for legacy system (Docker/VM/local setup)
- [ ] T003 [Ground Truth] Validate legacy functionality: Run legacy system and confirm all critical workflows function as baseline
- [ ] T004 [Analysis: Section.1] Validate project analysis completeness: Confirm all CRITICAL and IMPORTANT sections filled per analysis template
- [ ] T005 [Analysis: Section.8.1] Document performance baselines: Extract and validate baseline metrics from analysis Section 8
- [ ] T006 [Analysis: Section.7.1] Assess test coverage baseline: Review current test coverage and critical test cases from analysis
- [ ] T007 [Analysis: Section.11] Review domain knowledge: Study business rules, quirks, and tribal knowledge documentation

---

## Phase A: Technology Stack Consolidation (MEDIUM+ Scale Only)

**Purpose**: **INFRASTRUCTURE FIRST** - Consolidate high-overlap technology stacks before business logic migration. Skip for SMALL scale projects.

### File Transformation Lifecycle

**CRITICAL UNDERSTANDING**: Legacy files are **NEVER transformed in-place**. The migration process follows a **Copy & Preserve** methodology to maintain rollback capabilities and validation integrity.

#### Phase 1: Legacy Preservation (Files Remain Untouched)
```bash
# Original files stay exactly as they are during entire migration process
legacy-project/src/core/business-logic.ts     # ACTIVE - used for ground truth testing
legacy-project/database/migrations/001.sql   # ACTIVE - baseline validation
legacy-project/config/app.config.json        # ACTIVE - configuration reference
# Status: ACTIVE - All legacy files remain functional and unchanged
```

#### Phase 2: Target Creation (Business Logic Copied & Modernized) 
```bash
# New implementations created in target structure
target-project/src/domains/core/
├── business-logic.py          # NEW - copied from business-logic.ts
├── models.py                  # NEW - derived from legacy models
└── services.py                # NEW - business logic preservation

target-project/src/data/migrations/
└── 001_baseline_schema.py     # NEW - converted from legacy migrations

# Status: PARALLEL - Legacy and new systems run simultaneously
```

#### Phase 3: Validation & Retirement (Only After 100% Validation)
```bash
# Legacy files archived only after comprehensive validation passes
archive/legacy/project-name-YYYYMMDD/     # ARCHIVED - safely preserved
├── src/                                  # All original files preserved
├── database/                            # Migration history maintained
└── config/                              # Configuration preserved for reference

# Status: RETIRED - Legacy files safely archived, new system is primary
```

### File Transformation Categories

#### Files That Get **COPIED** (Business Logic Preservation)
- **Core Algorithms**: Complex business logic, calculations, data processing
- **Database Models**: Entity relationships, schema definitions, constraints  
- **Business Rules**: Validation logic, workflow definitions, decision trees
- **API Logic**: Authentication patterns, authorization, request handling

#### Files That Get **CONVERTED** (Format Change, Logic Preserved)
- **Migrations**: `.sql`/`.js` → target language with identical data transformations
- **Configuration**: `package.json`/`requirements.txt` → unified dependency management
- **Tests**: Jest/PHPUnit → target framework with same test cases
- **Documentation**: Updated with new architecture references, preserved content

#### Files That Get **ADAPTED** (Framework Integration)
- **UI Components**: Wrapped as Web Components or rewritten for unified framework
- **Build Scripts**: Individual build systems → unified build pipeline
- **Docker Config**: Individual containers → consolidated deployment strategy
- **CI/CD**: Individual workflows → unified continuous integration

#### Files That Get **ARCHIVED** (Legacy Preservation)
- **Original Directory**: Complete legacy project preserved after validation
- **Legacy Tests**: Original test suites kept for behavioral reference
- **Documentation History**: Original docs preserved for institutional knowledge
- **Configuration History**: Environment setup preserved for rollback scenarios

### Rollback Capability Strategy

**PRINCIPLE**: Complete rollback capability maintained until final validation passes. No irreversible changes until migration success confirmed.

#### Git-Based Rollback Infrastructure
```bash
# Branch strategy maintains multiple rollback points
main                           # Original stable system
├── migration/foundation       # Phase 2 foundation work
├── migration/feature-1        # Individual feature migration
├── migration/feature-2        # Parallel feature development
└── migration/integration      # Integration and validation

# Rollback commands available at each phase
git checkout main                    # Complete rollback to original system
git checkout migration/foundation    # Rollback to pre-feature state  
git revert <feature-commit>         # Rollback specific feature only
```

#### Database Rollback Procedures
```yaml
Schema Changes:
  Strategy: "Reversible migrations with down() methods for every up() method"
  Validation: "All migrations tested in both directions before deployment"
  Rollback Command: "migrate down --to=<baseline-version>"
  
Data Migration:
  Strategy: "Preserve original data during conversion, backup before transformation"  
  Validation: "Original data preserved in archive tables with restore procedures"
  Rollback Command: "restore-data --from-archive --feature=<feature-name>"

Configuration Changes:
  Strategy: "Environment configuration versioning with rollback profiles"
  Validation: "Each configuration change includes rollback environment"
  Rollback Command: "deploy-config --profile=<previous-version>"
```

#### Service-Level Rollback (For Isolated Stacks)
```yaml
Phase A Service Adapters:
  Strategy: "Feature flags control new vs legacy system routing"
  Rollback: "Toggle feature flags to route traffic back to legacy systems"
  Command: "toggle-feature --feature=<migrated-service> --state=legacy"
  
API Integration:
  Strategy: "Dual endpoint support (legacy + new) during migration period"
  Rollback: "Switch API routing back to legacy endpoints"
  Command: "route-api --service=<service> --target=legacy"
```

#### File-Level Rollback Requirements
- [ ] **Legacy System Preservation**: Original files remain active and unmodified until validation complete
- [ ] **Parallel System Operation**: Both legacy and new systems operational during migration
- [ ] **Configuration Rollback**: Environment allows switching between legacy and new systems  
- [ ] **Data Migration Reversibility**: Database changes include rollback procedures for schema and data
- [ ] **Service Isolation**: Service adapters allow individual feature rollback without affecting others
- [ ] **Documentation**: Rollback procedures documented and tested for each migration phase

**Phase A is SEPARATE from business logic migration and addresses infrastructure concerns first.**

### Technology Consolidation Impact on File Transformation

**Phase A determines HOW files will be transformed by establishing the target technology environment.**

#### Database File Transformations
```yaml
Source Pattern: "Multiple database technologies across projects"
Target Strategy: "[Chosen from Phase A] - Central/Domain/Federated/Hybrid"
File Impact:
  - Multiple *.sql migrations → Unified migration framework
  - Various ORM configs → Single ORM configuration 
  - Different schema files → Consolidated schema management
  - Separate connection configs → Unified connection pooling
```

#### Configuration File Consolidation
```yaml
Source Pattern: "Individual project configurations"
Target Strategy: "Unified configuration management"
File Impact:
  - package.json/requirements.txt/composer.json → Single dependency management
  - Multiple docker-compose.yml → Unified container orchestration
  - Various .env configurations → Centralized environment management
  - Individual CI/CD configs → Shared pipeline configuration
```

#### Framework Integration Patterns
```yaml
High-Overlap Stack (Consolidated):
  Source: "Multiple React apps, Express servers, Python Flask"
  Target: "Unified React frontend + consolidated backend framework"
  File Strategy: "Direct integration into unified codebase"
  
Low-Usage Stack (Isolated):
  Source: "PHP legacy app, specialized C++ tool, proprietary system"
  Target: "Service adapters + API integration"
  File Strategy: "Preserve in isolation + create adapter layer"
```

#### Build System Transformation  
```yaml
Before Phase A: "Multiple build systems (npm, pip, composer, make)"
After Phase A: "Unified build system (chosen in consolidation)"
File Impact:
  - Multiple build configs → Single build configuration
  - Various task runners → Unified task execution  
  - Different deployment scripts → Consolidated deployment strategy
  - Separate dependency managers → Single dependency resolution
```

### Phase A.1: High-Overlap Stack Consolidation

- [ ] TA01 [Analysis: All Projects] **Technology Stack Inventory**: Identify high-overlap vs low-usage stacks across all projects
- [ ] TA02 [Analysis: All Projects] **Consolidation Strategy Decision**: Choose database consolidation strategy (Central/Domain/Federated/Hybrid)
- [ ] TA03 **[Primary Language] Environment Unification**: Create unified environment for majority language stack
- [ ] TA04 **[Secondary Language] Toolchain Unification**: Standardize toolchain for secondary language stack  
- [ ] TA05 **Database Consolidation Implementation**: Execute chosen database consolidation strategy
- [ ] TA06 **Framework Bridge Development**: Create bridges between framework patterns in unified environments
- [ ] TA07 **Cross-Stack Testing**: Validate all projects work in consolidated technology environment

### Phase A.2: Low-Usage Stack Isolation Strategy

- [ ] TA08 **Isolated Stack Assessment**: Analyze remaining low-usage stacks for isolation needs
- [ ] TA09 **Service Adapter Framework**: Create framework for connecting isolated stacks to consolidated environment
- [ ] TA10 **Isolation Environment Setup**: Setup isolated environments for specialized/legacy stacks
- [ ] TA11 **Integration Layer Implementation**: Implement API gateway and service adapters for isolated stacks

**Checkpoint A**: Technology stacks consolidated/isolated. Business logic migration can now proceed with simplified infrastructure.

---

## Phase 2: Business Logic Foundation  

**Purpose**: Core target application infrastructure - the foundation for all business logic migration. **Technology stacks already consolidated in Phase A.**

- [ ] T010 Initialize target framework dependencies using consolidated technology stack from Phase A
- [ ] T011 [P] Configure linting and formatting tools for consolidated technology stack
- [ ] T012 [P] [Analysis: Section.2.1] Setup consolidated database schema and migrations framework 
- [ ] T013 [P] [Analysis: Section.3.1] Implement authentication/authorization framework shell (empty - will be populated by feature migrations)
- [ ] T014 [P] [Analysis: Section.3.2] Setup API routing and middleware structure (empty routes initially)
- [ ] T015 [P] [Analysis: Section.2.1] Create empty base models/entities based on analysis (shells only - actual models come from feature migration)
- [ ] T016 [Analysis: Section.10.2] Configure error handling, logging, and monitoring infrastructure
- [ ] T017 [P] [Analysis: Section.7.1] Setup testing framework infrastructure matching analysis patterns
- [ ] T018 [Analysis: Section.9.1] Implement security and performance monitoring per analysis patterns

**Checkpoint 2**: Business logic foundation ready. NO business logic exists yet, but technology infrastructure is consolidated and ready.

## Phase 3: Feature Migration (Feature 1 - [e.g., Event Publishing]) 🎯 MVP

**Phase 3 Risks & Mitigation:**
- **Risk**: Critical business logic corruption during migration
- **Mitigation**: Comprehensive ground truth tests, validation at every step, rollback capability
- **Risk**: Performance regression in core features  
- **Mitigation**: Performance baselines documented, continuous performance validation
- **Validation**: All features must pass integration tests before proceeding to next phase

**Migration Goal**: [Brief description of what this feature migration delivers based on Analysis Section 4.1]

**Analysis Reference**: Section 4.1 - Critical Algorithms, Section 11.1 - Domain Knowledge

**Independent Test**: [Concrete test case from Analysis Section 4.1, e.g., "A 'Draft' event cannot be published. A 'Validated' event can be published and triggers sync."]

**Original Asset(s)**: [e.g., features/MISP/app/Model/Event.php, features/MISP/app/Controller/EventsController.php]

### Phase 3a: Analysis Cross-Reference & Ground Truth Tests (Write These First)

**NOTE**: Analysis-informed Ground Truth tests against OLD code. Validation tests against NEW code.

- [ ] T017 [Analysis: Section.4.1] Algorithm analysis review: Study critical algorithm documentation for publishRouter function from analysis
- [ ] T018 [Analysis: Section.11.1] Domain knowledge review: Review business rules and domain concepts for event publishing from analysis
- [ ] T019 [P] [F1] [Logic: Event.php::publishRouter] [Analysis: Section.4.1] Ground Truth Test: Write test against legacy code proving original publishRouter function behavior per analysis documentation:
        - FAILS when given a 'Draft' event (confirmed in Analysis Section 4.1)
        - PASSES when given a 'Validated' event (confirmed in Analysis Section 4.1)  
        - [Include edge cases documented in Analysis Section 11.2]
- [ ] T020 [P] [F1] [Logic: Event.php::publishRouter] [Analysis: Section.4.1] Validation Test: Translate analysis-informed ground truth test to target framework test (initially fails - new code doesn't exist)
- [ ] T021 [Analysis: Section.8.1] Performance baseline documentation: Record current publishRouter performance metrics from analysis

### Phase 3b: Analysis-Guided Incremental Migration Loop

- [ ] T022 [P] [F1] [Logic: Event.php::Event()] [Analysis: Section.2.1] Port Models: Implement Event model in target framework based on analysis data model section
- [ ] T023 [F1] [Logic: Event.php::publishRouter] [Analysis: Section.4.1] Port Logic: **IMPLEMENTATION REQUIRED** - Choose implementation strategy:
        * **Copy & Modernize**: Copy Event.php::publishRouter code to target framework, replace framework calls, preserve exact business logic
        * **Behavior-Driven Rewrite**: Reimplement from analysis documentation, ensuring all documented behaviors preserved
        * **Incremental Refactor**: Port in layers (data→logic→API) maintaining exact functionality
- [ ] T024 [F1] [Logic: Event.php::publishRouter] [Analysis: Section.4.1] Run Validation: Execute validation test against ported logic - MUST pass before proceeding
- [ ] T025 [F1] [Analysis: Section.11.2] Edge case handling: Implement all quirks and workarounds documented in analysis
- [ ] T026 [F1] [Analysis: Section.3.2] Integrate Logic: Wire proven publishRouter logic into target framework API endpoint per analysis endpoint patterns
- [ ] T027 [F1] Full Integration Test: End-to-end test of complete feature through API - MUST pass
- [ ] T028 [F1] [Analysis: Section.8.1] Performance validation: Confirm new implementation meets baseline metrics from analysis

**Checkpoint**: Feature 1 migrated with analysis-validated functional and performance parity. Ready for production use.

---

## Implementation Strategies: How to Actually Port the Code

**CRITICAL**: These are implementation approaches, not just scaffolding. Each strategy results in working, tested features.

### Strategy 1: Direct Copy & Modernize (Recommended for Complex Logic)
**When to use**: Complex business algorithms, critical domain logic that must be preserved exactly
**Approach**: Copy legacy code and systematically modernize to target framework patterns

Implementation Steps:
- [ ] Copy legacy file(s) into target framework directory structure
- [ ] Rename functions/classes to match target framework conventions  
- [ ] Replace legacy framework calls with target framework equivalents (e.g., database queries, HTTP responses)
- [ ] Maintain exact business logic flow and conditional branches
- [ ] Update data types and imports for target language/framework
- [ ] Run validation tests continuously during modernization

Example Task Pattern:
```
- [ ] T023 [F1] [Logic: Event.php::publishRouter] [Analysis: Section.4.1] Copy & Modernize: 
      1. Copy Event.php::publishRouter to target/services/event_service.py::publish_router
      2. Replace PHP database calls with SQLAlchemy/Django ORM equivalents
      3. Replace PHP arrays with Python dictionaries/lists maintaining exact structure
      4. Replace PHP conditional logic with Python equivalents (if/elif/else)
      5. Preserve ALL edge case handling and error conditions from original
      6. Validate business logic flow matches original exactly
```

### Strategy 2: Behavior-Driven Rewrite (For Well-Documented Features)
**When to use**: Features with comprehensive analysis documentation and clear behavioral specifications
**Approach**: Rewrite from scratch guided by ground truth tests and analysis behavioral documentation

Implementation Steps:
- [ ] Study analysis Section 4 algorithm documentation thoroughly
- [ ] Write comprehensive ground truth tests covering all documented behaviors
- [ ] Implement new version guided by test requirements and analysis specifications
- [ ] Ensure all documented edge cases and quirks are preserved
- [ ] Validate against performance baselines from analysis Section 8

Example Task Pattern:
```
- [ ] T023 [F1] [Logic: Event.php::publishRouter] [Analysis: Section.4.1] Behavior-Driven Rewrite:
      1. Review Analysis Section 4.1 algorithm documentation for publishRouter
      2. Implement publish_router() function in target framework using documented behavior specifications
      3. Handle state transitions: Draft→Published, with sync trigger (per analysis)
      4. Implement all validation rules documented in Analysis Section 11.1
      5. Preserve error handling patterns documented in Analysis Section 11.2
      6. Ensure performance matches Analysis Section 8.1 baseline metrics
```

### Strategy 3: Incremental Refactor (For Mixed Simple/Complex Features)
**When to use**: Features with both simple CRUD and complex business logic components
**Approach**: Migrate in layers - data access first, then business rules, then API layer

Implementation Steps:
- [ ] Port data models first (Strategy 1: Copy & Modernize for model structure)
- [ ] Port simple CRUD operations (Strategy 2: Rewrite with standard patterns)
- [ ] Port complex business logic (Strategy 1: Copy & Modernize for exact behavior preservation)
- [ ] Port API layer (Strategy 2: Rewrite with target framework REST patterns)

Example Task Pattern:
```
- [ ] T022 [F1] [Logic: Event.php::Event] [Analysis: Section.2.1] Incremental Refactor - Models:
      1. Copy Event.php model structure to target framework model
      2. Translate PHP field types to target framework field types (maintaining constraints)
      3. Preserve all relationships and foreign keys per Analysis Section 2.2
      4. Maintain all validation rules and database constraints
      
- [ ] T023 [F1] [Logic: Event.php::publishRouter] [Analysis: Section.4.1] Incremental Refactor - Business Logic:
      1. Copy publishRouter business logic preserving all conditional branches
      2. Replace database access with new model methods
      3. Preserve all error handling and edge cases
      4. Maintain exact state transition logic
```

### Strategy 4: API-First Integration (For Service-Oriented Features)  
**When to use**: Features that primarily expose functionality through APIs with external integrations
**Approach**: Build target API layer first, then integrate legacy business logic as internal services

Implementation Steps:
- [ ] Design target framework API endpoints matching legacy functionality
- [ ] Create service adapter layer that calls legacy code temporarily
- [ ] Incrementally replace adapter calls with ported business logic
- [ ] Maintain API contract compatibility throughout migration

Example Task Pattern:
```
- [ ] T023 [F1] [Logic: EventsController.php::publish] [Analysis: Section.3.2] API-First Integration:
      1. Create target framework API endpoint POST /api/events/{id}/publish
      2. Implement temporary service adapter that calls legacy publishRouter via internal API/CLI
      3. Validate API responses match legacy behavior exactly
      4. Incrementally replace adapter with direct business logic port
      5. Maintain all authentication and authorization patterns per Analysis Section 3.1
```

## Alternative Migration Patterns (Choose Based on Project Needs)

### Pattern A: Simple Feature Migration (No Complex Business Logic)
For features with straightforward CRUD operations and minimal business rules:

- [ ] TXXX [Pattern A] [F1] [Logic: <file::function>] **Implementation Strategy**: Use Strategy 2 (Behavior-Driven Rewrite) with standard framework patterns
- [ ] TXXX [Pattern A] [F1] [Logic: <file::function>] Simple Ground Truth: Basic behavioral test for CRUD operations
- [ ] TXXX [Pattern A] [F1] [Logic: <file::function>] Direct Port: Rewrite using target framework ORM/router patterns maintaining exact API behavior
- [ ] TXXX [Pattern A] [F1] Basic Integration: Wire into target with standard REST/GraphQL patterns

### Pattern B: Complex Algorithm Migration (High Business Logic Complexity)
For features with critical algorithms documented in Analysis Section 4:

- [ ] TXXX [Pattern B] [F1] [Logic: <file::function>] **Implementation Strategy**: Use Strategy 1 (Direct Copy & Modernize) to preserve exact algorithm behavior
- [ ] TXXX [Pattern B] [F1] [Logic: <file::function>] [Analysis: Section.4.1] Deep Algorithm Analysis: Study complexity characteristics and performance requirements
- [ ] TXXX [Pattern B] [F1] [Logic: <file::function>] [Analysis: Section.4.1] Comprehensive Ground Truth: Test all documented edge cases and performance scenarios
- [ ] TXXX [Pattern B] [F1] [Logic: <file::function>] [Analysis: Section.4.1] Algorithm Preservation: **Copy legacy algorithm code and systematically modernize** maintaining O(n) characteristics and behavioral quirks
- [ ] TXXX [Pattern B] [F1] [Logic: <file::function>] [Analysis: Section.11.2] Quirk Implementation: **Copy and adapt all documented workarounds** and undocumented behaviors
- [ ] TXXX [Pattern B] [F1] [Analysis: Section.8.1] Performance Regression Testing: Validate performance against analysis baselines

### Pattern C: External Integration Migration (Third-Party Dependencies)
For features with external service dependencies documented in Analysis Section 5:

- [ ] TXXX [Pattern C] [F1] [Logic: <file::function>] **Implementation Strategy**: Use Strategy 4 (API-First Integration) or Strategy 1 (Copy & Modernize) based on integration complexity
- [ ] TXXX [Pattern C] [F1] [Logic: <file::function>] [Analysis: Section.5.1] Integration inventory: Review external API usage and error handling patterns  
- [ ] TXXX [Pattern C] [F1] [Logic: <file::function>] [Analysis: Section.5.1] Dependency Ground Truth: Test current external service integration behaviors
- [ ] TXXX [Pattern C] [F1] [Logic: <file::function>] [Analysis: Section.5.1] Error handling preservation: **Copy and adapt all fallback behaviors and caching strategies** from legacy code
- [ ] TXXX [Pattern C] [F1] [Analysis: Section.5.1] Service connectivity validation: Test all external integrations in target environment

## Phase 4: Feature Migration (Feature 2 - [e.g., Access Control])

**Migration Goal**: [Brief description based on Analysis Section 3.1/9.1, e.g., "Migrate distribution-based access control system"]

**Analysis Reference**: Section 3.1 - Authentication/Authorization, Section 9.1 - Security Measures

**Independent Test**: [Concrete test case from Analysis Section 3.1, e.g., "User A (Org 1) cannot see User B's (Org 2) 'Org Only' event"]

**Original Asset(s)**: [e.g., features/MISP/app/Model/Event.php::beforeFind, features/MISP/app/Controller/AppController.php::checkAuth]

### Phase 4a: Analysis-Informed Security Migration

- [ ] T029 [Analysis: Section.3.1] Authorization pattern analysis: Study current access control implementation documented in analysis
- [ ] T030 [Analysis: Section.9.1] Security measures review: Review all security patterns that must be preserved from analysis
- [ ] T031 [P] [F2] [Logic: Event.php::beforeFind] [Analysis: Section.3.1] Ground Truth Test: Write legacy test proving original beforeFind database query filter per analysis security documentation:
        - Login as User B
        - Query for User A's distribution=0 event  
        - Assert query returns 0 results (confirmed behavior in Analysis Section 3.1)
- [ ] T032 [P] [F2] [Logic: Event.php::beforeFind] [Analysis: Section.3.1] Validation Test: Translate analysis-informed ground truth test to target framework (initially fails)

### Phase 4b: Security-Validated Migration Loop  

- [ ] T033 [F2] [Logic: Event.php::beforeFind] [Analysis: Section.3.1] Authorization logic port: **IMPLEMENTATION REQUIRED** - Copy Event.php::beforeFind database filtering logic to target framework:
        * Copy exact WHERE clause conditions and JOIN logic
        * Replace PHP database calls with target framework ORM equivalents  
        * Preserve all user permission checking and organization filtering
        * Maintain exact SQL query behavior and performance characteristics
- [ ] T034 [F2] [Logic: Event.php::beforeFind] [Analysis: Section.3.1] Run Validation: Execute validation test against ported logic - MUST pass before proceeding  
- [ ] T035 [F2] [Analysis: Section.9.1] Security validation: Ensure all security measures maintained per analysis documentation
- [ ] T036 [F2] [Analysis: Section.3.1] Integrate Logic: Wire proven access control logic into target framework API endpoints per analysis patterns
- [ ] T037 [F2] [Analysis: Section.9.1] Security testing: Validate all authorization scenarios documented in analysis
- [ ] T038 [F2] Full Integration Test: End-to-end access control validation through API - MUST pass

**Checkpoint**: Feature 2 migrated with analysis-validated security and access control parity.

[Continue with additional feature migrations following the same pattern...]

## Phase N-2: Feature Migration (Feature N - [e.g., External Integrations])

**Migration Goal**: [Brief description of integration features being migrated]

**Independent Test**: [Concrete test case, e.g., "API call to ThirdPartyService returns expected data format"]

**Original Asset(s)**: [e.g., features/PROJECT/lib/ExternalAPI/*, features/PROJECT/config/integrations.php]

### Phase N-2a: Ground Truth & Validation Tests

- [ ] TXXX [P] [FN] [Logic: <legacy_file::function>] Ground Truth Test: Write legacy test proving original integration behavior
- [ ] TXXX [P] [FN] [Logic: <legacy_file::function>] Validation Test: Translate ground truth test to target framework

### Phase N-2b: Incremental Migration Loop

- [ ] TXXX [FN] [Logic: <legacy_file::function>] Port Logic: Migrate integration logic to target framework
- [ ] TXXX [FN] [Logic: <legacy_file::function>] Run Validation: Execute validation test - MUST pass before proceeding
- [ ] TXXX [FN] Integrate Logic: Wire proven integration logic into target framework
- [ ] TXXX [FN] Full Integration Test: End-to-end integration test - MUST pass

**Checkpoint**: Integration feature migrated with proven parity.

## Phase N-1: Cross-Cutting Concerns & Polish

- [ ] TXXX [Analysis: Section.10.2] Implement logging and monitoring patterns per analysis documentation
- [ ] TXXX [Analysis: Section.9.2] Security hardening and final security validation per analysis security requirements
- [ ] TXXX [P] Code cleanup and refactoring (target framework code only)
- [ ] TXXX [Analysis: Section.13.1] Documentation updates incorporating analysis findings and migration lessons learned

## Phase N: Migration Validation & Legacy Asset Retirement

**Purpose**: Final validation and safe removal of legacy assets.

### Phase N.1: Analysis-Validated Complete Migration Validation

- [ ] TXXX [Analysis: All Sections] Full analysis cross-reference: Verify ALL analysis findings have been addressed in migration
- [ ] TXXX Verify Full Migration: Confirm ALL [Logic: ...] tags have corresponding passing validation tests
- [ ] TXXX [Analysis: Section.4.1] Algorithm parity validation: Confirm all critical algorithms function identically per analysis
- [ ] TXXX Run Full Regression Suite: Execute complete test suite including all ground truth comparisons  
- [ ] TXXX [Analysis: Section.8.1] Performance regression testing: Validate performance meets or exceeds analysis baselines
- [ ] TXXX [Analysis: Section.12.3] Success criteria verification: Confirm all analysis success criteria met
- [ ] TXXX Production validation: Run new system in production-like environment with real data
- [ ] TXXX Stakeholder approval: Obtain sign-off from analysis-identified business stakeholders and users

### Phase N.2: Safe Legacy Asset Retirement

- [ ] TXXX [Analysis: Section.12.2] Risk mitigation: Address all identified migration risks from analysis
- [ ] TXXX Legacy asset backup: Create secure archive of legacy codebase before deletion
- [ ] TXXX Final validation checkpoint: Confirm new system handles ALL legacy use cases documented in analysis
- [ ] TXXX Delete Legacy Asset: After 100% validation and approval, remove legacy asset directory
- [ ] TXXX [Analysis: Section.10.2] Post-migration monitoring: Track performance and behavior against analysis-established baselines

### Dependencies & Execution Order

**Sequential Dependencies (Must Complete In Order):**

- **Phase 1 (Setup)**: Must complete first - establishes legacy testing environment and target project structure
- **Phase 2 (Foundation)**: Must complete before any feature migration - establishes core infrastructure
- **Feature Migration Phases**: Can proceed in parallel by feature after Phase 2 foundation is complete
- **Phase N (Asset Retirement)**: The absolute final step - only after ALL feature validations pass

---

## Implementation Strategy: Incremental Feature Migration

### Foundation-First Approach

1. **Complete Phase 1**: Setup and legacy environment (MANDATORY FIRST)
2. **Complete Phase 2**: Foundation infrastructure (framework foundation)  
3. **Begin Feature Migration**: Start with highest priority/risk features
4. **Continue Incrementally**: Each feature adds value without breaking previous functionality

### MVP-Driven Incremental Delivery

1. **Foundation Phase**: Complete setup and infrastructure → Foundation ready for features
2. **Critical Feature MVP**: Migrate one critical feature → **STOP and VALIDATE** → Deploy/Demo
3. **Feature Increments**: Add next priority feature → Validate independently → Deploy/Demo  
4. **Parallel Development**: Multiple features can be developed in parallel after foundation

### Team Parallel Strategy

**Sequential Foundation** (Team Together):

1. Setup (Phase 1) - establish legacy baseline and target structure
2. Foundation (Phase 2) - critical shared infrastructure

**Parallel Feature Migration** (After Foundation):

- Developer A: Critical Feature 1 (highest business priority)
- Developer B: Critical Feature 2 (highest technical risk)
- Developer C: Integration Features (external dependencies)
- All developers: Follow the Ground Truth → Port → Validate → Integrate loop

**Success Criteria for Each Feature:**

- Ground truth test establishes legacy behavior baseline
- Validation test passes against new implementation  
- Integration test confirms end-to-end functionality
- Optional: Performance meets or exceeds legacy baseline

---

## Core Migration Loop Methodology

**The Repeating Pattern** (for each feature):

```text
1. Ground Truth Test (Legacy) → Establish irrefutable behavioral baseline
2. Validation Test (Target)    → Create test that initially fails
3. Port Logic                  → IMPLEMENT ACTUAL BUSINESS LOGIC (not scaffolding!)
4. Run Validation             → New test MUST pass before proceeding
5. Integrate                  → Wire working logic into target architecture
6. Full Test                  → End-to-end validation of complete feature
```

**Implementation vs. Scaffolding Distinction:**

❌ **WRONG - Scaffolding Only:**
```python
def publish_router(event):
    # TODO: Implement event publishing logic
    pass
```

✅ **CORRECT - Actual Implementation:**
```python  
def publish_router(event):
    if event.status == 'Draft':
        raise ValidationError("Cannot publish draft events")
    
    if event.status == 'Validated':
        event.status = 'Published'
        event.published_at = datetime.utcnow()
        event.save()
        
        # Trigger sync as in legacy system
        sync_service.schedule_sync(event.id)
        return {'status': 'published', 'sync_scheduled': True}
    
    raise ValidationError(f"Invalid event status: {event.status}")
```

**Critical Success Principles:**

- A task is NOT "done" when code is written - it's "done" when validation tests pass AND feature is fully functional
- Each feature follows the EXACT same pattern for consistency and reliability
- Ground truth tests provide irrefutable behavioral baselines that eliminate arguments
- "Port Logic" means COMPLETE working implementation, not placeholder code
- No feature proceeds to integration until validation passes with real working logic
- Features can be migrated independently and in parallel after foundation is ready

---

## Scale-Specific Implementation Methodologies

### 🟢 SMALL SCALE (1-3 projects) - Direct Integration Methodology

**Timeline**: 4-8 weeks | **Team**: 1-3 developers | **Risk**: MEDIUM

**Approach**: Direct consolidation with standard brownfield practices

**Phase Structure**:
```yaml
Week 1-2: Foundation Setup
  - Legacy environment setup
  - Target framework initialization  
  - Ground truth test establishment

Week 3-5: Feature Migration
  - Core business logic migration
  - Data model consolidation
  - API integration

Week 6-8: Integration & Polish
  - Cross-project features
  - Performance optimization
  - User acceptance testing
```

**Success Criteria**:
- All 1-3 projects functionally consolidated
- Performance maintained or improved
- Single authentication system
- Unified user interface

**Risk Mitigation**:
- Standard backup and rollback procedures
- Feature-by-feature validation
- Continuous integration testing

### 🟡 MEDIUM SCALE (4-10 projects) - Technology-First Domain Methodology

**Timeline**: 8-16 weeks | **Team**: 3-6 developers | **Risk**: HIGH

**Approach**: **Technology consolidation first, then domain-based business logic integration**

**Phase Structure**:
```yaml  
Week 1-2: Setup & Analysis (Phase 1)
  - Multi-project analysis and legacy environment setup
  - Technology stack inventory and consolidation planning
  
Week 3-5: Technology Stack Consolidation (Phase A)
  - High-overlap stack consolidation (languages, databases, frameworks)
  - Low-usage stack isolation strategy implementation
  - Service adapter framework for isolated stacks

Week 6-7: Business Logic Foundation (Phase 2)
  - Target framework infrastructure using consolidated stacks
  - Unified authentication, API routing, testing framework

Week 8-12: Domain Business Logic Migration (Phase 3+)
  - Domain 1: Projects 1-3 (business logic only - infrastructure ready)
  - Domain 2: Projects 4-6 (parallel development possible)  
  - Domain 3: Projects 7-10 (parallel development possible)

Week 13-16: Integration & Optimization
  - Cross-domain business logic integration
  - Performance optimization and user acceptance
```

**Success Criteria**:  
- 2-3 coherent domain services
- Technology stack consolidation where possible
- Cross-domain feature integration
- Maintained performance across all domains

**Risk Mitigation**:
- Domain-level rollback capability
- Technology bridge architecture
- Phased validation and testing

### 🔴 LARGE SCALE (11+ projects) - Enterprise Domain Methodology

**Timeline**: 16-24 weeks | **Team**: 6-12 developers | **Risk**: VERY HIGH

**Approach**: Complex domain architecture with isolation strategies

**Phase Structure**:
```yaml
Week 1-4: Setup & Technology Ecosystem Analysis (Phase 1)
  - Enterprise analysis across all projects
  - Technology stack inventory and consolidation strategy
  - Domain architecture design with technology considerations
  - Team specialization planning

Week 5-10: Technology Stack Consolidation (Phase A)
  - High-overlap stack integration (Primary/Secondary languages, databases)
  - Low-usage stack isolation strategy (Specialized technologies)
  - Service adapter architecture implementation
  - Enterprise infrastructure consolidation

Week 11-12: Business Logic Foundation (Phase 2)
  - Enterprise framework infrastructure using consolidated stacks
  - Cross-domain authentication, API gateway, monitoring
  - Enterprise testing and deployment infrastructure

Week 13-20: Domain Business Logic Migration (Phase 3+)
  - Security Domain: 3-5 projects (parallel with consolidated infrastructure)
  - Productivity Domain: 3-5 projects (parallel development)
  - Infrastructure Domain: 3-5 projects (parallel development)
  - Specialized Domains: Remaining projects (parallel development)

Week 21-24: Platform Integration & Enterprise Optimization
  - Cross-domain business logic orchestration
  - Enterprise performance optimization and monitoring
  - Phased enterprise validation and rollout
```

**Success Criteria**:
- 3-4 enterprise domain services
- Technology consolidation with appropriate isolation
- Cross-domain platform capabilities
- Enterprise-grade monitoring and management

**Risk Mitigation**:
- Specialized team structure
- Complex rollback procedures
- Extensive testing and validation
- Phased enterprise deployment

### 🚨 EXTREME SCALE (25+ projects) - Platform Transformation Methodology

**Timeline**: 24+ weeks | **Team**: 12+ specialized developers | **Risk**: EXTREME

**Approach**: Enterprise platform transformation with extensive isolation

**Phase Structure**:
```yaml
Week 1-6: Platform Architecture & Technology Ecosystem Analysis (Phase 1)
  - Comprehensive 25+ project analysis and legacy environment setup  
  - Technology ecosystem inventory and consolidation strategy
  - Platform architecture design based on technology consolidation
  - Organizational change and specialized team planning

Week 7-18: Technology Ecosystem Consolidation (Phase A) 
  - Primary Language Ecosystem: Majority projects (e.g., Python 15+, JavaScript 10+)
  - Secondary Language Consolidation: Significant minority projects
  - Specialized Technology Isolation: Low-usage but critical stacks (5+ projects)
  - Enterprise service adapter architecture and API gateway platform

Week 19-24: Platform Business Logic Foundation (Phase 2)
  - Enterprise framework infrastructure using consolidated technology ecosystem
  - Cross-platform authentication, API gateway, enterprise monitoring
  - Platform-level testing, deployment, and orchestration infrastructure

Week 25-36: Domain Platform Business Logic Migration (Phase 3+)
  - Security Platform Domain (business logic with pre-consolidated infrastructure)
  - Productivity Platform Domain (parallel development enabled)  
  - Infrastructure Platform Domain (parallel development enabled)
  - Specialized Platform Domains (parallel development enabled)

Week 37-42: Platform Integration & Enterprise Rollout
  - Cross-platform business logic orchestration and workflow automation
  - Enterprise performance optimization and platform management
  - Organizational change management and phased enterprise deployment

Week 43+: Platform Optimization & Evolution
  - Continuous platform performance optimization
  - Platform feature enhancement and capability expansion
  - Ongoing organizational adoption and platform evolution
```

**Success Criteria**:
- Unified platform serving 25+ integrated projects
- Technology ecosystem with appropriate consolidation/isolation
- Cross-platform automation and orchestration  
- Enterprise platform management capabilities
- Organizational adoption and change management success

**Risk Mitigation**:
- Enterprise project management  
- Extensive organizational change management
- Complex multi-level rollback strategies
- Comprehensive enterprise testing
- Phased organizational rollout

## Template Usage Summary

**This template is designed for scale-appropriate, risk-assessed, evidence-based brownfield asset relocation projects where:**

- You have 1 to 37+ existing legacy systems that must continue working during migration
- 100% functional parity is required (no behavior changes during migration)  
- Comprehensive project analysis provides the migration roadmap and validation criteria
- **MANDATORY scale-appropriate risk approval** obtained from users before proceeding
- Scale-appropriate team structure and timeline planning
- Risk mitigation strategies adapted to project scale and complexity

**Risk-First Approach:**
- All migrations start with comprehensive risk assessment and user approval
- Alternative approaches offered when risks are unacceptable  
- Continuous risk monitoring and mitigation throughout migration process
- Clear rollback procedures and completion verification requirements

**Pre-Migration Requirements (MANDATORY):**

1. **Risk Assessment**: Present risk framework to user, obtain explicit approval for all risks
2. **Project Analysis**: Complete comprehensive project analysis using project_analysis_template.md  
3. **User Decision**: User must choose migration approach (FULL/SELECTIVE/PHASED/API_ONLY/CANCEL)
4. **Completion Plan**: Establish clear completion criteria and verification procedures

**Key Template Adaptations (Scale-Specific):**

**MANDATORY For All Scales:**
- **MANDATORY**: Determine project scale (SMALL/MEDIUM/LARGE/EXTREME) before proceeding
- **MANDATORY**: User approval of scale-appropriate migration risks before generating tasks
- **MANDATORY**: Complete project_analysis_template.md for each project BEFORE using this task template
- **MANDATORY**: All "Port Logic" tasks must result in working implementations, not scaffolding

**Scale-Specific Adaptations:**

**🟢 SMALL SCALE (1-3 projects)**:
- Use direct integration methodology with 4-8 week timeline
- Single team approach (1-3 developers)
- Standard risk assessment and mitigation
- Simple completion tracking per project
- Direct consolidation task structure

**🟡 MEDIUM SCALE (4-10 projects)**:
- Use domain-based methodology with 8-16 week timeline  
- Specialized team structure (3-6 developers)
- Enhanced risk assessment with domain considerations
- Domain-based completion tracking
- Technology bridge task structure

**🔴 LARGE SCALE (11+ projects)**:
- Use enterprise domain methodology with 16-24 week timeline
- Large specialized team structure (6-12 developers)
- Complex risk assessment with isolation strategies
- Complex domain tracking with technology consolidation
- Service adapter and isolation task structure

**🚨 EXTREME SCALE (25+ projects)**:
- Use platform transformation methodology with 24+ week timeline
- Enterprise team structure (12+ specialized developers)
- Extreme risk assessment with platform considerations
- Platform-level completion tracking with ecosystem management
- Enterprise platform task structure with extensive isolation

**Template Customization:**
- Replace `[MIGRATION: FEATURE NAME]` with actual project name and scale
- Replace `[e.g., Event Publishing]` with actual feature names from analysis Section 4 (Business Logic)
- Replace `[Logic: <legacy_file::function>]` with actual legacy code references from analysis
- Replace `[Independent Test]` descriptions with concrete test scenarios from analysis documentation
- Replace `[Analysis: Section.#]` with actual section references from completed analysis
- Adjust framework references to match target technology and scale-appropriate architecture
- Choose implementation strategies based on scale and complexity
- Adapt phase structure to match selected scale methodology

**Multiple Migration Approaches Supported:**

- **Pattern A**: Simple features with minimal business logic
- **Pattern B**: Complex algorithms requiring exact behavioral preservation 
- **Pattern C**: External integrations with dependency management
- **Analysis-Driven**: All patterns informed by comprehensive project analysis findings

**Expected Outcomes:**

- Legacy asset safely migrated with analysis-validated functional parity
- New system architecture modernized while preserving ALL documented business logic and domain knowledge
- Team can work in parallel after analysis-informed foundation phase
- Each feature increment can be deployed independently with confidence
- Risk minimized through analysis-driven continuous validation against documented behavior baselines
- Performance maintained or improved per analysis baseline metrics
- All external integrations preserved per analysis dependency documentation
