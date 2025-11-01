---
description: Generate migration-strategy.md for brownfield projects based on legacy system assessment in spec.md
scripts:
  sh: scripts/bash/setup-plan.sh --json
  ps: scripts/powershell/setup-plan.ps1 -Json
agent_scripts:
  sh: scripts/bash/update-agent-context.sh __AGENT__
  ps: scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `{SCRIPT}` from repo root and parse JSON for FEATURE_SPEC, SPECS_DIR, PROJECT_TYPE. Verify PROJECT_TYPE is "BROWNFIELD" - this command is only for brownfield projects.

2. **Load context**: Read FEATURE_SPEC and extract:
   - Legacy System Assessment section (system count, technology stacks, business value, complexity)
   - Critical Business Logic Preservation requirements
   - Migration Constraints (business continuity, technical, timeline)

3. **Determine project scale**: Based on system count from spec.md:
   - SMALL (1-3 systems): Standard brownfield migration
   - MEDIUM (4-10 systems): Complex brownfield migration
   - LARGE (11+ systems): Enterprise brownfield integration  
   - EXTREME (25+ systems): Platform consolidation

4. **Migration method recommendation**: Based on scale, constraints, and technology diversity:
   - **Strangler Fig**: Gradual replacement (safest, slower)
   - **API Gateway**: Route-based switchover (balanced)
   - **Blue-Green**: Parallel environment (faster, higher cost)
   - **Event-Driven**: Event streaming migration (loose coupling)
   - **Database-First**: Data migration then apps (risky but sometimes necessary)

5. **Technology consolidation analysis**:
   - Identify high-overlap stacks (CONSOLIDATE strategy)
   - Identify low-usage stacks (ISOLATE strategy)  
   - Recommend database consolidation approach
   - Plan service adapter patterns

6. **Implementation strategy matrix**: Classify each legacy system:
   - **Category A - Complex Algorithms**: Copy & Modernize (preserve exact logic)
   - **Category B - Domain Logic**: Behavior-Driven Rewrite (from specs)
   - **Category C - Utilities**: Replace or Integrate (modern equivalents)

7. **Generate migration-strategy.md**: Use `/templates/migration-strategy-template.md` and fill:
   - Migration overview with selected method and justification
   - Legacy system analysis and classification
   - Technology stack consolidation plan
   - Asset relocation plan with file transformation strategy
   - Business logic preservation requirements
   - Risk mitigation and rollback strategy
   - Migration phases with timeline estimates
   - Success criteria and validation procedures

8. **Validate completeness**: Ensure all sections filled with actionable information:
   - Every legacy system classified with implementation strategy
   - Technology consolidation decisions for all identified stacks
   - Clear migration method selection with alternatives considered
   - Rollback procedures defined for each migration phase
   - Success criteria measurable and testable

9. **Report**: Output path to generated migration-strategy.md and summary:
   - Project scale assessment
   - Selected migration method
   - Number of systems by implementation strategy
   - Technology consolidation approach
   - Estimated timeline based on scale

## Migration Method Selection Guidelines

**Strangler Fig Pattern** (Recommended for most brownfield):
- Gradual replacement with parallel operation
- Lower risk, longer timeline
- Good rollback capability
- Best for: Most brownfield projects, risk-averse organizations

**API Gateway Migration**:
- Route-based gradual switchover
- Transparent to users
- Medium risk, medium timeline
- Best for: Service-oriented architectures, microservices targets

**Blue-Green Deployment**:
- Complete parallel environment
- Fast switchover, easy rollback
- Higher cost (2x infrastructure)
- Best for: High availability requirements, sufficient resources

**Event-Driven Migration**:
- Event streaming for loose coupling
- Real-time synchronization
- Complex event system setup
- Best for: Event-sourced architectures, real-time systems

**Database-First Migration**:
- Migrate data first, then applications
- Higher risk of data corruption
- Faster application migration after data moved
- Best for: Data consolidation priorities, simple application logic

## Implementation Strategy Guidelines

**Strategy 1: Copy & Modernize** - Use for:
- Complex algorithms that took years to perfect
- Mathematical computations and formulas
- Critical business logic with edge cases
- Systems where rewriting risks introducing bugs

**Strategy 2: Behavior-Driven Rewrite** - Use for:
- Well-documented standard business processes
- Simple CRUD operations
- Systems with clear, documented requirements
- Areas where modern patterns would significantly improve maintainability

**Strategy 3: Incremental Refactor** - Use for:
- Systems with mixed complexity
- Layered architectures (data → logic → API)
- Cases where partial migration provides value
- When full rewrite is too risky but copy isn't ideal

**Strategy 4: API-First Integration** - Use for:
- Systems that can be treated as services
- Well-defined interfaces
- External integration candidates
- Cases where internal migration can be deferred