# Legacy System Analysis Templates

This directory contains comprehensive analysis templates for brownfield migration projects.

## 📋 Template Overview

### Analysis Template Selection Matrix

| System Business Value | Template to Use | Sections Covered | Output Document |
|----------------------|-----------------|------------------|-----------------|
| **CRITICAL** (Revenue/Operations) | `project-analysis-template.md` | All 13 sections | `project-analysis-[system].md` |
| **IMPORTANT** (Customer Experience) | `project-analysis-condensed-template.md` | Sections 1-5, 11-12 | `project-analysis-condensed-[system].md` |
| **LOW-IMPACT** (Business Continues Normally) | `project-analysis-summary-template.md` | Sections 1-2, 12 | `project-analysis-summary-[system].md` |

**Always Create**: `ai-context-summary-[system].md` (2-page LLM-friendly summary) for ALL systems

## 🎯 Template Details

### 1. Full Project Analysis Template (`project-analysis-template.md`)
**Use For**: CRITICAL systems where failure blocks revenue or core operations
**Covers**: All 13 sections of Universal Project Analysis Framework
- **Section 1**: Project Identity & Context
- **Section 2**: Data Architecture  
- **Section 3**: API Architecture
- **Section 4**: Business Logic (CRITICAL for migration)
- **Section 5**: External Integrations
- **Section 6**: Frontend Architecture
- **Section 7**: Testing Strategy
- **Section 8**: Performance Characteristics
- **Section 9**: Security Assessment
- **Section 10**: Deployment & Operations
- **Section 11**: Documentation Assessment
- **Section 12**: Migration Readiness
- **Section 13**: Risk Assessment

### 2. Condensed Analysis Template (`project-analysis-condensed-template.md`)
**Use For**: IMPORTANT systems that impact customer experience but aren't mission-critical
**Covers**: Essential sections only (1-5, 11-12)
- Business Context + Technical Architecture (Sections 1-5)
- Migration Planning + Success Criteria (Sections 11-12)

### 3. Summary Analysis Template (`project-analysis-summary-template.md`)
**Use For**: LOW-IMPACT systems where business continues normally without the system
**Covers**: Minimal analysis (Sections 1-2, 12) + **Evidence-based LOW-IMPACT validation**
- System Identity + Technical Overview (Sections 1-2)
- Success Criteria + Migration Decision (Section 12)
- **Required Proof**: Evidence that business operated normally for 24+ hours without system

### 4. AI Context Summary Template (`ai-context-summary-template.md`)
**Use For**: ALL systems - creates LLM-friendly 2-page context document
**Purpose**: Efficient AI context loading without token overflow
**Always Required**: Every system needs this for AI-assisted migration work

## 🚀 Getting Started

### Step 1: System Inventory
List all legacy systems and categorize business value with evidence-based justification:
- **CRITICAL**: System failure stops revenue/operations (requires revenue/operations proof)
- **IMPORTANT**: System failure degrades customer experience (requires customer impact metrics)
- **LOW-IMPACT**: Business continues normally without system (requires 24+ hour evidence)

### Step 2: Scale Assessment
Determine project scale to apply appropriate analysis depth:
- **SMALL (1-3 systems)**: FULL analysis for all systems
- **MEDIUM (4-10 systems)**: Use business value matrix
- **LARGE (11-25 systems)**: Use business value matrix  
- **EXTREME (25+ systems)**: Tiered approach with SUMMARY for evidence-based LOW-IMPACT systems

### Step 3: Template Selection
Use the Analysis Requirements Matrix in `../spec.md` to select appropriate template depth.

### Step 4: Analysis Execution
1. Copy appropriate template: `cp [template].md [system]-analysis.md`
2. Fill out analysis sections thoroughly
3. Create AI context summary: `cp ai-context-summary-template.md ai-context-summary-[system].md`
4. Reference completed analysis in `../migration-strategy.md`

## 📁 File Naming Convention

```
analysis/
├── project-analysis-crm-system.md          # Full analysis for CRITICAL system
├── ai-context-summary-crm-system.md        # AI context for CRM system
├── project-analysis-condensed-portal.md    # Condensed analysis for IMPORTANT system  
├── ai-context-summary-portal.md            # AI context for portal system
├── project-analysis-summary-reports.md     # Summary analysis for NICE-TO-HAVE system
├── ai-context-summary-reports.md           # AI context for reports system
└── README.md                               # This file
```

## 🔗 Integration with Migration Strategy

Each completed analysis document should be referenced in the main `../migration-strategy.md` file:

```yaml
Category A - Complex Algorithms (Strategy: Copy & Modernize):
  - CRM System: [Reference: analysis/project-analysis-crm-system.md - Complex business logic]
  
Category B - Domain Logic (Strategy: Behavior-Driven Rewrite):  
  - Customer Portal: [Reference: analysis/project-analysis-condensed-portal.md - Clear business rules]
```

## ⚡ AI-Assisted Migration Benefits

The AI context summaries enable efficient LLM-assisted migration:
- **Token Efficient**: 2-page max prevents context overflow
- **Critical Info Focus**: Highlights must-preserve business logic
- **Migration Ready**: Includes specific migration strategy recommendations
- **Performance Baselines**: Provides measurable success criteria

## 🎯 Quality Assurance

### Analysis Completeness Checklist
- [ ] Business logic algorithms documented with complexity assessment
- [ ] External dependencies mapped with failure impact analysis  
- [ ] Performance baselines measured (not estimated)
- [ ] Success criteria defined with measurable thresholds
- [ ] AI context summary created for LLM efficiency
- [ ] Analysis referenced in migration strategy document

### Validation Questions
1. **Can a new team member understand the system** from this analysis?
2. **Are all critical algorithms preserved** with documented complexity?
3. **Will this prevent production outages** during migration?
4. **Can AI assistants load this context** without token limits?
5. **Is migration readiness clearly assessed** with actionable next steps?

---

**Template System Version**: v2.0.0  
**Last Updated**: [DATE]  
**Created by**: Enhanced Brownfield Migration System  
**Integration**: Part of spec-kit comprehensive migration planning framework