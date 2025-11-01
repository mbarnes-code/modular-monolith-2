# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## Project Type Selection *(mandatory)*

**Select project type** (this determines template sections and planning approach):

- [ ] **🟢 Greenfield Project**: Building new system from scratch
- [ ] **🔄 Brownfield Migration**: Migrating/consolidating existing systems

**Selected Project Type**: GREENFIELD

---

## [BROWNFIELD ONLY] Legacy System Assessment

*Fill this section ONLY if Brownfield Migration selected above*

### Existing Systems Inventory

**System Count**: [Number] existing systems to migrate/consolidate
**Project Scale**: [SMALL (1-3) / MEDIUM (4-10) / LARGE (11+) / EXTREME (25+)]

**Analysis Depth Requirements by Scale:**
- **SMALL (1-3 systems)**: Full Project Analysis Template for ALL systems
- **MEDIUM (4-10 systems)**: Full analysis for CRITICAL systems, condensed for others
- **LARGE/EXTREME (11+ systems)**: Full analysis for CRITICAL systems, condensed for IMPORTANT, summary for NICE-TO-HAVE

```yaml
Legacy Systems:
  System 1:
    Name: [e.g., "Legacy CRM"]
    Technology: [e.g., "PHP 7.4 + MySQL"]
    Business Value: [CRITICAL/IMPORTANT/NICE-TO-HAVE]
    Migration Complexity: [HIGH/MEDIUM/LOW]
    Analysis Required: [FULL/CONDENSED/SUMMARY] # Based on business value + scale
    Analysis Status: [PENDING/IN_PROGRESS/COMPLETE]
    Analysis Location: [specs/[###-feature]/analysis/system-1-crm-analysis.md]
    
  System 2:
    Name: [e.g., "Customer Portal"] 
    Technology: [e.g., "React + Node.js"]
    Business Value: [CRITICAL/IMPORTANT/NICE-TO-HAVE]
    Migration Complexity: [HIGH/MEDIUM/LOW]
    Analysis Required: [FULL/CONDENSED/SUMMARY]
    Analysis Status: [PENDING/IN_PROGRESS/COMPLETE]
    Analysis Location: [specs/[###-feature]/analysis/system-2-portal-analysis.md]
```

### Analysis Requirements Matrix

| Business Value | SMALL Scale | MEDIUM Scale | LARGE/EXTREME Scale |
|----------------|-------------|--------------|---------------------|
| **CRITICAL**   | FULL        | FULL         | FULL                |
| **IMPORTANT**  | FULL        | CONDENSED    | CONDENSED           |
| **NICE-TO-HAVE** | FULL      | CONDENSED    | SUMMARY             |

### Mandatory Analysis Deliverables

**For EACH Legacy System, create:**
1. **System Analysis Document**: Using appropriate template depth (FULL/CONDENSED/SUMMARY)
2. **AI Context Summary**: 2-page max summary for LLM context loading
3. **Critical Algorithms Extract**: Code snippets for CRITICAL business logic only

**Template Selection Guide:**
- **FULL Analysis**: Complete Universal Project Analysis Template (13 sections)
- **CONDENSED Analysis**: Sections 1-5, 11-12 from Project Analysis Template
- **SUMMARY Analysis**: Sections 1-2, 12 from Project Analysis Template

**File Organization:**
```
specs/[###-feature]/analysis/
├── system-1-crm-analysis.md          # Full analysis (if required)
├── system-1-crm-ai-summary.md        # 2-page AI context summary
├── system-2-portal-analysis.md       # Condensed analysis (if required)  
├── system-2-portal-ai-summary.md     # 2-page AI context summary
├── critical-algorithms/               # Code extracts for CRITICAL systems
│   ├── crm-billing-algorithm.md      # Extracted business logic
│   └── portal-auth-flow.md           # Extracted authentication logic
└── analysis-completion-checklist.md  # Validation checklist
```

### Critical Business Logic Preservation

**Mission-Critical Algorithms**: [List algorithms that MUST be preserved exactly]
**Data Migration Requirements**: [Database schemas, file formats, etc.]
**Integration Dependencies**: [External systems that must continue working]

### Migration Constraints

**Business Continuity**: [Uptime requirements, rollback needs]
**Technical Constraints**: [Technology limitations, performance requirements]
**Timeline Constraints**: [Business deadlines, regulatory requirements]

---

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
