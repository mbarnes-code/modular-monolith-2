# Project Analysis: [SYSTEM NAME] - Condensed Version

**Purpose**: Essential system analysis for brownfield migration (Condensed - covers critical sections only)
**Full Analysis Available**: [Link to complete project-analysis-[system].md if exists]
**Analysis Type**: CONDENSED (Business Logic + Technical + Planning focus)

---

## 1. System Overview & Business Context

### System Identity
- **System Name**: [Exact system name]
- **Primary Function**: [1-2 sentences describing core purpose]
- **Technology Stack**: [Language, framework, database, deployment]
- **Business Criticality**: [CRITICAL/IMPORTANT/LOW-IMPACT]
- **Active Users**: [~X monthly active users or "Internal team only"]
- **Business Owner**: [Name and contact]
- **Technical Owner**: [Name and contact]

### Business Value & Purpose
- **Problem Solved**: [What business problem does this system solve?]
- **Success Metrics**: [How is success measured? Revenue, efficiency, user satisfaction?]
- **Business Dependencies**: [What business processes depend on this system?]
- **Failure Impact**: [What happens if this system goes down for 1 hour? 1 day?]

---

## 2. Technical Architecture

### System Architecture
```yaml
Architecture Pattern: [Monolith/Microservices/Serverless/Hybrid]
Deployment: [Cloud provider + deployment method]
Database: [Primary database + any secondary stores]
Key Technologies:
  - Backend: [Language + framework + version]
  - Frontend: [Framework + version if applicable] 
  - Infrastructure: [Container platform, load balancer, etc.]
  - Monitoring: [APM tools, logging, metrics]
```

### Core Components & Dependencies
**Internal Components**:
- **Component**: [Name] - [Purpose] - [Technology]
- **Component**: [Name] - [Purpose] - [Technology]

**External Dependencies**:
- **Service**: [Name] - [Purpose] - [Criticality: CRITICAL/IMPORTANT/OPTIONAL]
- **Service**: [Name] - [Purpose] - [Criticality: CRITICAL/IMPORTANT/OPTIONAL]

**Database Schema Overview**:
- **Primary Models**: [List 5-10 most important data models]
- **Key Relationships**: [Most critical foreign key relationships]
- **Data Volume**: [Approximate record counts for main tables]

---

## 3. Business Logic & Domain Rules

### Critical Business Logic
**Core Algorithms** (Must be preserved exactly):
1. **Algorithm**: [Name + brief description]
   - **Location**: [File path + function name]
   - **Complexity**: [Lines of code + complexity assessment]
   - **Business Impact**: [What happens if this breaks?]

2. **Algorithm**: [Name + brief description]
   - **Location**: [File path + function name]  
   - **Complexity**: [Lines of code + complexity assessment]
   - **Business Impact**: [What happens if this breaks?]

### Domain-Specific Rules
**Business Rules** (Must be preserved):
- **Rule**: [e.g., "Orders cannot be modified after payment confirmation"]
- **Rule**: [e.g., "Inventory levels must sync with warehouse system hourly"]  
- **Rule**: [e.g., "Customer discounts stack with specific precedence: loyalty > seasonal > bulk"]
- **Rule**: [e.g., "Refunds require manager approval for amounts > $500"]

### Workflow Logic
**Critical User Workflows**:
- **Workflow**: [e.g., User Registration] → [Steps: registration → verification → activation]
- **Workflow**: [e.g., Order Processing] → [Steps: cart → payment → fulfillment → shipping]
- **Workflow**: [e.g., Support Ticket] → [Steps: creation → assignment → resolution → feedback]

---

## 4. Current Performance & Operational Metrics

### Performance Baselines (MEASURED DATA)
**API Response Times**:
```yaml
Critical Endpoints:
  - GET /api/endpoint1: [Avg: Xms, P95: Yms, P99: Zms]
  - POST /api/endpoint2: [Avg: Xms, P95: Yms, P99: Zms]  
  - PUT /api/endpoint3: [Avg: Xms, P95: Yms, P99: Zms]

Database Query Performance:
  - Most frequent query: [Query description] - [Avg: Xms]
  - Slowest regular query: [Query description] - [Avg: Xms]
  - Largest table scan: [Table name] - [Duration: Xms]
```

**System Resource Usage**:
```yaml
Production Load (Peak Hours):
  - CPU Usage: [X%] 
  - Memory Usage: [X GB / Y GB total]
  - Database Connections: [X active / Y max]
  - Disk Usage: [X GB database, Y GB logs]
  
Traffic Patterns:
  - Peak Daily Users: [X concurrent users]
  - Peak API Requests/min: [X requests]
  - Data Transfer: [X GB/day]
```

### Operational Health
**Current Issues**:
- **Issue**: [Description] - **Severity**: [HIGH/MEDIUM/LOW] - **Frequency**: [Daily/Weekly/Monthly]
- **Issue**: [Description] - **Severity**: [HIGH/MEDIUM/LOW] - **Frequency**: [Daily/Weekly/Monthly]

**Reliability Metrics** (Last 90 days):
- **Uptime**: [99.X%]
- **Error Rate**: [X% of requests]  
- **MTTR** (Mean Time to Recovery): [X minutes]
- **Incident Count**: [X incidents total, Y critical]

---

## 5. Integration & Data Flow Architecture

### External System Integrations
**Upstream Dependencies** (Systems this system depends on):
```yaml
System 1: [Name]
  Purpose: [What service it provides]
  Integration Type: [REST API / Database / Message Queue / File Transfer]
  Data Flow: [What data flows from that system to this one]
  Failure Impact: [What breaks if this integration fails]
  SLA/Performance: [Expected response time, availability]

System 2: [Name]
  Purpose: [What service it provides]
  Integration Type: [REST API / Database / Message Queue / File Transfer]  
  Data Flow: [What data flows from that system to this one]
  Failure Impact: [What breaks if this integration fails]
  SLA/Performance: [Expected response time, availability]
```

**Downstream Dependencies** (Systems that depend on this system):
```yaml
System 1: [Name]
  Purpose: [What they use this system for]
  Integration Type: [REST API / Database / Message Queue / File Transfer]
  Data Flow: [What data flows from this system to that one]
  Usage Pattern: [Real-time / Batch / Event-driven]
  Breaking Changes Impact: [How changes to this system affect them]

System 2: [Name] 
  Purpose: [What they use this system for]
  Integration Type: [REST API / Database / Message Queue / File Transfer]
  Data Flow: [What data flows from this system to that one]  
  Usage Pattern: [Real-time / Batch / Event-driven]
  Breaking Changes Impact: [How changes to this system affect them]
```

### Data Flow Patterns
**Critical Data Synchronization**:
- **Flow**: [Source System] → [This System] → [Destination System]
- **Flow**: [Source System] → [This System] → [Destination System]

**Event-Driven Processes**:
- **Event**: [Event Name] → **Triggers**: [What systems respond] → **Data**: [What data is passed]
- **Event**: [Event Name] → **Triggers**: [What systems respond] → **Data**: [What data is passed]

---

## 11. Risk Assessment & Migration Planning

### Business Risk Assessment
**High-Risk Scenarios**:
- **Risk**: [e.g., "Data loss during migration"]
  - **Probability**: [HIGH/MEDIUM/LOW]
  - **Impact**: [Detailed description of business impact]
  - **Mitigation**: [How to prevent or minimize this risk]

- **Risk**: [e.g., "Extended downtime affecting customers"]  
  - **Probability**: [HIGH/MEDIUM/LOW]
  - **Impact**: [Detailed description of business impact]
  - **Mitigation**: [How to prevent or minimize this risk]

### Technical Risk Assessment  
**Migration Complexity Factors**:
- **Factor**: [e.g., "Undocumented legacy algorithms"] - **Risk Level**: [HIGH/MEDIUM/LOW]
- **Factor**: [e.g., "Tight coupling to deprecated database"] - **Risk Level**: [HIGH/MEDIUM/LOW]  
- **Factor**: [e.g., "No comprehensive test suite"] - **Risk Level**: [HIGH/MEDIUM/LOW]
- **Factor**: [e.g., "Complex integration patterns"] - **Risk Level**: [HIGH/MEDIUM/LOW]

### Migration Strategy Recommendation
**Recommended Approach**: [Copy & Modernize / Behavior-Driven Rewrite / Incremental Refactor / API-First Integration]

**Strategy Justification**:
- **Complexity Assessment**: [Why this level of complexity requires this approach]
- **Risk Tolerance**: [Business risk tolerance influences strategy choice]
- **Timeline Constraints**: [How timeline affects strategy selection]
- **Resource Availability**: [Team skill and capacity considerations]

**Estimated Migration Effort**:
- **Developer Weeks**: [X weeks for Y developers with Z skill level]
- **Timeline**: [X months with dependencies and testing]
- **Resource Requirements**: [Specific skills needed, external help required]

---

## 12. Success Criteria & Acceptance Requirements

### Functional Success Criteria
**Must-Have Requirements** (Migration cannot be considered complete without these):
- [ ] **100% Feature Parity**: All existing functionality works identically
- [ ] **Data Integrity**: Zero data loss, all historical data accessible
- [ ] **Integration Continuity**: All upstream/downstream systems continue working
- [ ] **User Experience Continuity**: Users can complete existing workflows without retraining
- [ ] **Performance Parity**: Response times within ±10% of current baseline

**Business Acceptance Criteria**:
- [ ] **User Acceptance**: [X% of users successfully complete key workflows in testing]
- [ ] **Performance Acceptance**: [Key metrics meet or exceed current performance]
- [ ] **Reliability Acceptance**: [System achieves target uptime in first month]
- [ ] **Integration Acceptance**: [All partner systems validate continued functionality]

### Technical Success Criteria
**Code Quality Requirements**:
- [ ] **Test Coverage**: [Minimum X% unit test coverage, Y% integration coverage]
- [ ] **Documentation**: [All APIs documented, deployment procedures documented]  
- [ ] **Monitoring**: [Full observability - metrics, logs, traces, alerts]
- [ ] **Security**: [Security scan passed, authentication/authorization working]

**Operational Readiness**:
- [ ] **Deployment Process**: [Automated deployment pipeline working]
- [ ] **Rollback Capability**: [Can rollback to previous system within X minutes]
- [ ] **Support Documentation**: [Operations team can support new system]
- [ ] **Performance Monitoring**: [All baseline metrics being tracked in new system]

### Migration Validation Plan
**Pre-Migration Validation**:
- [ ] **Environment Parity**: [Staging environment matches production data/load]
- [ ] **Integration Testing**: [All external system integrations validated]
- [ ] **Performance Testing**: [Load testing shows acceptable performance]  
- [ ] **Data Migration Dry Run**: [Complete data migration tested with rollback]

**Post-Migration Validation**:
- [ ] **Smoke Tests**: [Critical user journeys working]
- [ ] **Integration Verification**: [All partner systems communicating successfully]
- [ ] **Performance Verification**: [Response times meeting SLA]
- [ ] **Business Process Verification**: [Key business processes completing successfully]

---

## Analysis Metadata

**Analysis Completed By**: [Name and role]  
**Analysis Date**: [Completion date]  
**Analysis Confidence**: [HIGH/MEDIUM/LOW] - [Brief explanation]
**Last System Update**: [When was the system last significantly modified]
**Analysis Method**: [Interview + Code Review + Documentation + Performance Analysis]

**Stakeholders Consulted**:
- **Business**: [Names and roles of business stakeholders interviewed]
- **Technical**: [Names and roles of technical stakeholders interviewed]  
- **Operations**: [Names and roles of operations stakeholders interviewed]

**Documentation Sources**:
- **Code Repository**: [Link or location]
- **Existing Documentation**: [Links to any existing technical docs]
- **Architecture Diagrams**: [Links to current architecture diagrams]
- **Performance Monitoring**: [Links to dashboards showing current metrics]

**Next Steps**:
1. **Immediate**: [What should be done immediately after this analysis]
2. **Short-term**: [What should be done in next 2-4 weeks] 
3. **Long-term**: [What should be planned for next 3-6 months]

---

**Full Analysis**: [Link to complete project-analysis-[system].md if a full analysis was also completed]