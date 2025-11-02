# Project Analysis: [SYSTEM NAME] - Summary Version

**Purpose**: Quick system assessment for LOW-IMPACT systems (business continues normally without system)
**Analysis Type**: SUMMARY (Business Context + Technical Overview + Success Criteria)
**Business Impact**: LOW-IMPACT (requires evidence-based justification - see validation section)
**For More Detail**: [Link to condensed or full analysis if available]

## TECHNICAL CONTENT GUIDANCE (Important for Validation)

**Legitimate Technical Patterns** - These are NOT placeholders:

**✅ JSON/Config Examples**: `{"status": "ok"}`, `[{"id": 1, "name": "test"}]`
**✅ Hex/Binary Patterns**: `{6A 40 68 ?? ?? 00 00}`, `0x41414141`  
**✅ Code Variables**: `{syslog_time}`, `${API_KEY}`, `{match.rule}`
**✅ Technical IDs**: `/api/v1/users/{id}`, `src/lib/entities.ts`
**✅ Domain Syntax**: `{1}{W}{U}` (MTG), `SELECT * WHERE id = ?` (SQL)
**✅ Honest N/A**: "N/A - CLI tool has no frontend" (when section doesn't apply)

**❌ Avoid Placeholders**: `[TODO]`, `{template_var}`, `[Your details here]`

**Domain Flexibility**: Security tools may skip Business Logic, CLI libraries may skip Auth sections.

---

## 1. System Overview & Business Context

### System Identity
- **System Name**: [Exact system name]
- **Primary Function**: [1-2 sentences describing core purpose]  
- **Technology Stack**: [Language + framework + database]
- **Business Criticality**: [CRITICAL/IMPORTANT/LOW-IMPACT]
- **Active Users**: [~X users or "Internal team only"]
- **Business Owner**: [Name]
- **Technical Owner**: [Name]

### Business Value & Migration Priority
**Problem Solved**: [What business problem does this system solve?]

**Business Impact**: [Choose one WITH REQUIRED JUSTIFICATION]
- 🔴 **CRITICAL**: System failure stops revenue/operations (migrate first)
  - **Proof Required**: Revenue loss calculation OR operations stoppage documentation
- 🟡 **IMPORTANT**: System failure degrades customer experience (migrate second)
  - **Proof Required**: Customer impact metrics OR workflow degradation documentation  
- 🟢 **LOW-IMPACT**: Business continues normally without system (migrate last)
  - **Proof Required**: Evidence business operated normally for 24+ hours without system

**LOW-IMPACT Validation** (Required for LOW-IMPACT systems):
- **24-Hour Test Evidence**: [Date when business operated normally for 24+ hours without this system]
- **Alternative Coverage**: [What system/process provides same functionality with X% coverage]
- **User Workaround**: [How users/staff work around system absence - must be documented]
- **Revenue Independence**: [Proof that revenue continues normally without this system]

**Failure Cost**: [What happens if this goes down for 4 hours?]
- **Revenue Impact**: [$ lost or "None"]
- **User Impact**: [Number of users affected + severity]  
- **Business Process Impact**: [What business processes stop working]

### Success Metrics
**Current Performance** (most important metrics only):
- **Response Time**: [Average response time for critical operations]
- **Uptime**: [Current uptime %]  
- **User Satisfaction**: [NPS score, complaint volume, or "Unknown"]
- **Business Metric**: [Revenue per user, transactions per day, etc.]

---

## 2. Technical Architecture Summary

### Technology Overview
```yaml
Architecture: [Monolith/Microservices/Serverless]
Primary Language: [Language + version]
Framework: [Framework + version] 
Database: [Database + version]
Deployment: [Cloud/On-premise + method]
Age: [X years old, last major update: Y years ago]
```

### System Scale & Complexity
**Codebase Size**:
- **Lines of Code**: [Approximate total LOC]
- **Key Files**: [~X critical files that contain main business logic]
- **Dependencies**: [Number of external dependencies]

**Data Scale**:
- **Database Size**: [X GB total]
- **Key Tables**: [3-5 most important tables with record counts]
- **Daily Data Volume**: [X records created per day]

### Critical Dependencies
**External Systems** (failure breaks this system):
- **System**: [Name] - **Purpose**: [What it provides] - **Risk**: [HIGH/MEDIUM/LOW]
- **System**: [Name] - **Purpose**: [What it provides] - **Risk**: [HIGH/MEDIUM/LOW]

**Dependent Systems** (these break if this system fails):  
- **System**: [Name] - **Impact**: [What breaks for them]
- **System**: [Name] - **Impact**: [What breaks for them]

### Current Technical Health
**Known Issues**:
- **Issue**: [Most critical current problem] - **Frequency**: [How often]
- **Issue**: [Second most critical problem] - **Frequency**: [How often]

**Technical Debt Level**: [HIGH/MEDIUM/LOW]
- **Reason**: [Why this debt level - outdated tech, no tests, poor documentation, etc.]

---

## 12. Success Criteria & Acceptance Requirements

### Migration Success Definition
**Functional Requirements** (Must work exactly the same):
- [ ] **Core User Journeys**: [List 3-5 most important user workflows]
  - [ ] [Workflow 1: e.g., "User can create and submit an order"] 
  - [ ] [Workflow 2: e.g., "Admin can process refunds"]
  - [ ] [Workflow 3: e.g., "System generates daily reports"]
  - [ ] [Workflow 4: e.g., "Integration sends data to partner systems"]
  - [ ] [Workflow 5: e.g., "Users can access 2 years of historical data"]

**Performance Requirements**:
- [ ] **Response Time**: [Critical operations complete within X seconds]
- [ ] **Throughput**: [System handles X concurrent users / Y requests per minute]  
- [ ] **Uptime**: [System achieves X% uptime in first month post-migration]

**Data Requirements**:
- [ ] **Zero Data Loss**: [All existing data accessible and intact]
- [ ] **Historical Data**: [X years of historical data remains accessible]
- [ ] **Data Format**: [Reports and exports work identically]

### Business Acceptance Criteria
**User Acceptance**:
- [ ] **Training Required**: [NONE/MINIMAL/MODERATE] - [Users need <X hours training]
- [ ] **User Workflows**: [Users complete existing tasks without confusion]
- [ ] **User Performance**: [Users work at same speed as before]

**Business Process Continuity**:
- [ ] **Partner Integrations**: [All partner systems continue working without changes]
- [ ] **Reporting**: [All existing reports continue to be generated]
- [ ] **Compliance**: [System continues to meet regulatory requirements]

### Technical Acceptance Criteria  
**Operational Readiness**:
- [ ] **Deployment**: [Can deploy updates without downtime]
- [ ] **Monitoring**: [Operations team can monitor system health]
- [ ] **Support**: [Support team can troubleshoot user issues]
- [ ] **Rollback**: [Can rollback to old system within X minutes if needed]

**Code Quality**:
- [ ] **Documentation**: [New team members can understand and modify system]
- [ ] **Tests**: [Changes can be made safely with automated testing]  
- [ ] **Security**: [System passes security review]

### Migration Validation Plan
**Pre-Go-Live Checklist**:
- [ ] **Data Migration Tested**: [Full data migration completed successfully in staging]
- [ ] **Integration Testing**: [All external system connections validated]
- [ ] **Performance Testing**: [System performs adequately under expected load]
- [ ] **User Acceptance Testing**: [Key users validate critical workflows]
- [ ] **Rollback Plan**: [Rollback procedure tested and ready]

**Go-Live Success Criteria** (First 48 hours):
- [ ] **No Critical Issues**: [No P0/P1 incidents in first 48 hours]
- [ ] **User Adoption**: [X% of users successfully complete key workflows]  
- [ ] **Performance**: [Response times within acceptable range]
- [ ] **Integration Health**: [All partner systems reporting successful connections]

**Post-Migration Success** (First 30 days):
- [ ] **Stability**: [Uptime meets SLA target]
- [ ] **Performance**: [Response times stable and within target]
- [ ] **User Satisfaction**: [User complaints <X per week]
- [ ] **Business Metrics**: [Business KPIs remain stable or improve]

---

## Quick Migration Assessment

### Migration Complexity: [SIMPLE/MODERATE/COMPLEX]

**SIMPLE** (2-4 weeks):
- Well-documented system with good test coverage
- Standard technology stack  
- Minimal external integrations
- Small, experienced team can handle

**MODERATE** (1-3 months):
- Some documentation gaps but understandable code
- Standard technology with some customizations
- Multiple external integrations
- Requires dedicated team with domain knowledge

**COMPLEX** (3-12 months):  
- Undocumented business logic or legacy technology
- Custom/proprietary technology or complex integrations
- High business risk or regulatory requirements
- Requires specialist knowledge or significant reverse-engineering

### Recommended Next Steps
**Immediate** (Next 2 weeks):
1. [Specific action - e.g., "Interview 3 key users about critical workflows"]
2. [Specific action - e.g., "Document the 5 most critical business rules"]
3. [Specific action - e.g., "Set up performance monitoring baseline"]

**Short-term** (Next 1-2 months):  
1. [Specific action - e.g., "Create comprehensive test suite for critical paths"]
2. [Specific action - e.g., "Document all external system integration points"]
3. [Specific action - e.g., "Prototype new system architecture"]

**Migration Decision**: 
- **Recommended Strategy**: [Copy & Modernize / Behavior-Driven Rewrite / Incremental Refactor / Retire System]
- **Rationale**: [1-2 sentences explaining why this approach fits]
- **Timeline**: [X months with Y developers]
- **Risk Level**: [HIGH/MEDIUM/LOW]

---

## Analysis Metadata

**Analysis Date**: [Date completed]
**Analyzed By**: [Name and role]
**Analysis Confidence**: [HIGH/MEDIUM/LOW] - [Why this confidence level]
**Analysis Method**: [Interview + Code Review + Documentation Review]

**Key Stakeholders Consulted**:
- **Business**: [Name - role]  
- **Technical**: [Name - role]
- **Users**: [Number of users interviewed]

**Next Analysis Review**: [Date when this should be updated]
**Escalation Needed**: [Yes/No - if Yes, what kind of help is needed]

---

**More Detail Available**: [Link to condensed-analysis-[system].md or project-analysis-[system].md if they exist]