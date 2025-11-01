# AI Context Summary: [SYSTEM NAME]

**Purpose**: Condensed system overview for AI context loading (2-page max for token efficiency)
**Full Analysis**: Link to complete analysis document
**Created**: [DATE] | **System Priority**: [CRITICAL/IMPORTANT/NICE-TO-HAVE]

---

## Quick System Identity

```yaml
System: [System Name]
Technology: [Primary language + framework + database]
Business Purpose: [1 sentence - why this exists]
Migration Priority: [CRITICAL/IMPORTANT/NICE-TO-HAVE]
Users: [~X monthly active users or "Internal team only"]
Full Analysis: [Link to complete project-analysis-[system].md]
```

---

## Critical Business Logic [CRITICAL SYSTEMS ONLY]

### Must-Preserve Algorithms
```yaml
Algorithm 1:
  Name: [e.g., "Customer Billing Calculator"]
  Location: [file path + function name]
  Complexity: [Lines of code + complexity rating]
  Why Critical: [1 sentence - business impact if lost]
  
Algorithm 2:
  Name: [e.g., "Inventory Sync Process"]  
  Location: [file path + function name]
  Complexity: [Lines of code + complexity rating]
  Why Critical: [1 sentence - business impact if lost]
```

### Domain-Specific Business Rules
- **Rule**: [e.g., "Orders can't be modified after payment"]
- **Rule**: [e.g., "Inventory must sync hourly with warehouse"]
- **Rule**: [e.g., "Customer discounts stack with specific precedence rules"]

---

## Data Architecture Essentials

### Primary Data Models
```yaml
Model 1: [e.g., Customer]
  Fields: [5 most important fields only]
  Relationships: [Key relationships to other models]
  
Model 2: [e.g., Order]  
  Fields: [5 most important fields only]
  Relationships: [Key relationships to other models]
```

### Critical Data Flows
- **Flow**: [e.g., "User registration → Email verification → Account activation"]
- **Flow**: [e.g., "Order creation → Payment processing → Fulfillment"]

---

## Integration Dependencies

### External APIs [CRITICAL DEPENDENCIES ONLY]
```yaml
Service 1: [e.g., Stripe Payments]
  Purpose: [Payment processing]
  Criticality: [CRITICAL - app won't work without]
  Failure Impact: [Users can't complete purchases]
  
Service 2: [e.g., Email Service]
  Purpose: [Transactional emails]  
  Criticality: [IMPORTANT - degrades UX]
  Failure Impact: [Users don't get confirmations]
```

### Internal System Dependencies  
- **Dependency**: [System X provides user authentication for this system]
- **Dependency**: [System Y receives inventory updates from this system]

---

## Technical Migration Notes

### Migration Strategy Classification
```yaml
Recommended Strategy: [Copy & Modernize / Behavior-Driven Rewrite / Incremental Refactor / API-First Integration]
Reason: [Why this strategy fits - complexity/documentation/risk factors]
Estimated Effort: [X weeks for Y developers]
Risk Level: [HIGH/MEDIUM/LOW]
```

### Key Migration Challenges
- **Challenge**: [e.g., "Complex algorithm with no documentation"]
  **Mitigation**: [e.g., "Extract behavior through comprehensive testing"]
  
- **Challenge**: [e.g., "Tightly coupled to legacy database schema"]  
  **Mitigation**: [e.g., "Create data adapter layer during transition"]

### Performance Baselines [MEASURED, NOT ESTIMATED]
```yaml
Critical Endpoints:
  - GET /api/customers: [150ms avg, 500ms p95]
  - POST /api/orders: [300ms avg, 1200ms p95]
  
Database Queries:
  - Customer search: [50ms avg]
  - Order history: [200ms avg]
  
Background Jobs:
  - Daily inventory sync: [15 minutes]
```

---

## Tribal Knowledge Capture

### Undocumented Quirks
- **Quirk**: [e.g., "Payment webhook must be retried exactly 3 times or duplicate charges occur"]
- **Quirk**: [e.g., "Customer search breaks on special characters unless escaped"]
- **Quirk**: [e.g., "Database connection pool must be <20 or timeouts happen"]

### Historical Context  
- **Decision**: [Why X technology was chosen over Y]
- **Workaround**: [Temporary fix that became permanent - document why]
- **Constraint**: [External limitation that affects architecture]

---

## Migration Readiness Assessment

### Ready to Migrate?
- [ ] **Business logic documented**: All critical algorithms identified and understood
- [ ] **Dependencies mapped**: All external and internal dependencies documented  
- [ ] **Performance baseline**: Key metrics measured and recorded
- [ ] **Test coverage**: Adequate tests exist or ground truth tests planned
- [ ] **Stakeholder approval**: Business stakeholders approve migration approach

### Migration Blockers
- **Blocker**: [e.g., "Customer data export API not yet available"]
  **Resolution**: [What needs to happen + timeline]
  
- **Blocker**: [e.g., "Critical algorithm not understood by any current team member"]
  **Resolution**: [Find original developer / reverse engineer through testing]

### Success Criteria for Migration
- [ ] **100% functional parity**: All features work exactly as before
- [ ] **Performance parity**: Response times within ±10% of baseline  
- [ ] **Data integrity**: Zero data loss during migration
- [ ] **Integration continuity**: All external systems continue working
- [ ] **User acceptance**: Users can complete existing workflows without retraining

---

## Quick Reference Links

**Full Documentation**:
- Complete System Analysis: [Link to project-analysis-[system].md]
- Critical Algorithm Code: [Link to critical-algorithms/[system]-algorithms.md]
- API Documentation: [Link to existing docs or note if missing]
- Test Suite: [Link to test files or note coverage gaps]

**Migration Planning**:
- Migration Strategy Details: [Link to migration-strategy.md section for this system]
- Task Breakdown: [Link to tasks.md section for this system]  
- Risk Mitigation: [Link to detailed risk analysis]

---

**Analysis Completed By**: [Name]  
**Date Completed**: [Date]  
**Confidence Level**: [HIGH/MEDIUM/LOW] - [Brief reason]  
**Next Review Date**: [Date - for systems that may change]