# Library Overlap Audit - Apps Directory Analysis

**Analysis Date:** November 19, 2025  
**Scope:** Root `/apps` directory structure and dependencies analysis  
**Purpose:** Identify overlapping libraries, dependencies, and consolidation opportunities

## Executive Summary

The apps directory contains 55+ individual services across 5 domain categories, with significant dependency overlaps and potential consolidation opportunities. This audit identifies patterns, redundancies, and recommendations for library management optimization.

## Directory Structure Overview

```
apps/
├── ai/                    # 3 services: LLM servers
├── core/                  # 3 services: orchestrator, UI, infrastructure
├── productivity/          # 13 services: workflow, budget, recipes, etc.
├── security/              # 21 services: threat intel, incident response, etc.
└── tcg/                   # 6 services: MTG tools, commander spellbook, etc.
```

**Total:** 46 identified services with individual package management

## Dependency Analysis

### JavaScript/TypeScript Dependencies

#### Major Framework Overlaps

**Express.js Usage:**
- Root monorepo: `express: ^4.21.2`
- mealie-service: `express: ^4.18.2`
- firecrawl-service: `express: ^4.21.2`
- cyberchef-service: Not using Express (custom Grunt build)
- **Consolidation Opportunity:** Standardize Express version across services

**React/Next.js Ecosystem:**
- Root monorepo: `next: 15.5.6`, `react: 19.2.0`
- commander-spellbook-site: Independent React setup
- nemesis-frontend: Independent React setup
- jane-ui: Uses root dependencies
- **Recommendation:** Migrate independent React apps to shared dependencies

**Common Utilities:**
- `axios`: Used in root + firecrawl-service (different versions)
- `lodash`: Used in root + cyberchef-service + firecrawl-service
- `uuid`: Multiple versions across services
- `cors`: Duplicated in multiple services

#### Heavy Dependencies with Overlaps

**CyberChef Service (121 dependencies):**
```json
// Major duplications with root:
"lodash": "^4.17.21"        // Also in root
"d3": "7.9.0"               // Also in root  
"uuid": "^11.1.0"           // Different version in root
"moment": "^2.30.1"         // Not in root, could be shared
"crypto-js": "^4.2.0"       // Security-specific, could be in shared/security
```

**Firecrawl Service (80+ dependencies):**
```json
// Major duplications:
"express": "^4.21.2"        // Same as root
"axios": "^1.12.2"          // Different version than root
"lodash": "^4.17.21"        // Same as root
"uuid": "^13.0.0"           // Different version than root/cyberchef
"winston": "^3.14.2"        // Logging - could be shared
"zod": "^3.24.2"            // Validation - could be shared
```

**N8N Service (Monorepo within monorepo):**
- Has its own pnpm workspace with 40+ internal packages
- Version: 1.116.0 with extensive workflow automation dependencies
- **Issue:** Complex nested monorepo structure

### Python Dependencies

#### FastAPI Ecosystem Overlaps

**Standardized FastAPI Stack:**
```python
# Consistent across: jane-orchestrator, cyber-llm-server, dispatch-service
fastapi==0.119.0
uvicorn==0.37.0-0.38.0    # Minor version differences
pydantic==2.12.0-2.12.3   # Minor version differences
```

**Database Dependencies:**
```python
# SQLAlchemy usage:
sqlalchemy==2.0.0-2.0.44  # Version inconsistencies
alembic>=1.12.0           # Migration tool overlap
```

**HTTP Client Libraries:**
```python
# Duplicated across services:
requests==2.32.5          # Standard HTTP
httpx>=0.25.0-0.28.1      # Async HTTP - version drift
```

### Build Tool Analysis

#### NX Project Configuration Patterns

**Consistent Structure Found In:**
- All libs/ projects use standardized project.json
- Apps have mixed configuration approaches
- Some services (like n8n) ignore NX structure entirely

**Build Tool Diversity:**
- **Webpack:** CyberChef, some React components
- **Vite:** Some libraries in libs/
- **Grunt:** CyberChef (legacy build system)
- **Turbo:** N8N internal monorepo
- **NX:** Root monorepo orchestration
- **Custom:** Multiple services with bespoke build scripts

## Container Analysis

### Dockerfile Patterns

**Base Image Inconsistencies:**
```dockerfile
# Python services:
FROM python:3.11-slim     # cyber-llm-server
FROM python:3.12-slim     # dispatch-service  
FROM python:3.9           # Some legacy services

# Node services:
FROM node:18-slim         # Some services
FROM node:20-alpine       # Other services
FROM alpine:3.18          # Custom builds
```

**Infrastructure Docker Standardization:**
- `/infrastructure/docker/base-images/` contains standardized base images:
  - `python-base/Dockerfile`
  - `node-base/Dockerfile` 
  - `rust-base/Dockerfile`
- **Issue:** Many services not using standardized base images

## Library Consolidation Opportunities

### High Priority (Immediate Impact)

#### 1. JavaScript Common Utilities
**Current State:** Duplicated across 8+ services
**Recommendation:** Create `libs/shared/utils-js`
```json
{
  "axios": "1.6.0",      // Standardize version
  "lodash": "4.17.21",   // Already consistent
  "uuid": "10.0.0",      // Resolve version conflicts
  "cors": "2.8.5",       // Centralize CORS config
  "winston": "3.14.2"    // Shared logging
}
```

#### 2. FastAPI Service Template
**Current State:** 6+ services with similar FastAPI setup
**Recommendation:** Create `libs/shared/fastapi-base`
```python
# Standardized versions:
fastapi==0.119.0
uvicorn==0.38.0
pydantic==2.12.3
sqlalchemy==2.0.44
alembic==1.12.0
httpx==0.28.1
```

#### 3. React Component Library
**Current State:** 3+ independent React setups
**Recommendation:** Extend existing `libs/ui/` structure
- Migrate `nemesis-frontend` to shared components
- Migrate `commander-spellbook-site` to shared components
- Standardize on React 19 + Next.js 15

### Medium Priority (Architecture Impact)

#### 4. Build System Standardization
**Issue:** Multiple build systems creating maintenance overhead
**Recommendation:**
- Migrate CyberChef from Grunt to NX/Webpack
- Standardize on NX + Vite for libraries
- Create build templates for common patterns

#### 5. Security Library Consolidation
**Current State:** Security tools have overlapping crypto/analysis libraries
**Recommendation:** Create `libs/shared/security`
```javascript
// Shared security utilities:
"crypto-js": "4.2.0",
"node-forge": "1.3.1",
"bcryptjs": "2.4.3",
"argon2-browser": "1.18.0"
```

#### 6. Container Base Image Adoption
**Issue:** Inconsistent base images across 20+ services
**Recommendation:**
- Mandate use of standardized base images
- Update all Dockerfiles to use `/infrastructure/docker/base-images/`
- Version lock base images for consistency

### Low Priority (Long-term Optimization)

#### 7. Monorepo-in-Monorepo Resolution
**Issue:** N8N service contains its own pnpm workspace
**Recommendation:**
- Evaluate extracting N8N as separate repository
- Or flatten N8N packages into root workspace
- **Impact:** Complex migration, low immediate value

#### 8. Python Data Science Libraries
**Current State:** Multiple services importing pandas, numpy independently
**Future Consideration:** Create `libs/shared/data-analysis` when usage patterns mature

## Consolidation Implementation Plan

### Phase 1: Quick Wins (1-2 weeks)
1. **Standardize JavaScript utilities**
   - Create `libs/shared/utils-js`
   - Migrate axios, lodash, uuid usage
   - Update 5+ services to use shared library

2. **Python dependency standardization**
   - Lock FastAPI ecosystem versions
   - Update requirements.txt files across 6+ services
   - Test compatibility

### Phase 2: Architecture Changes (3-4 weeks)
1. **React component migration**
   - Migrate nemesis-frontend to shared UI components
   - Migrate commander-spellbook-site React parts
   - Standardize styling system

2. **Container standardization**
   - Update 10+ Dockerfiles to use base images
   - Test container compatibility
   - Update CI/CD pipelines

### Phase 3: Build System Optimization (4-6 weeks)
1. **CyberChef build modernization**
   - Migrate from Grunt to NX
   - Preserve existing functionality
   - Update development workflow

2. **Security library consolidation**
   - Extract common crypto utilities
   - Update 8+ security services
   - Performance testing

## Risk Assessment

### High Risk
- **CyberChef migration:** Complex legacy build system, high functionality risk
- **N8N workspace changes:** Could break internal dependencies

### Medium Risk
- **React migrations:** UI/UX changes may affect user experience
- **Container base images:** Potential runtime environment differences

### Low Risk
- **JavaScript utility consolidation:** Well-tested libraries, minimal breaking changes
- **Python dependency updates:** Minor version changes, good test coverage

## Success Metrics

### Immediate (Post Phase 1)
- **Dependency count reduction:** 15-20% fewer duplicate dependencies
- **Build time improvement:** 10-15% faster builds for affected services
- **Version consistency:** 95% of common utilities on same version

### Long-term (Post Phase 3)
- **Maintenance overhead:** 30% reduction in dependency management tasks
- **Container size optimization:** 10-15% smaller average container sizes
- **Development velocity:** Faster onboarding for new services using templates

## Recommendations Summary

### Immediate Actions Required
1. ✅ **Create shared JavaScript utilities library**
2. ✅ **Standardize FastAPI service dependencies**
3. ✅ **Implement container base image adoption**

### Strategic Decisions Needed
1. 🤔 **N8N monorepo strategy:** Extract vs. flatten vs. maintain
2. 🤔 **CyberChef modernization priority:** High-impact but high-risk
3. 🤔 **React consolidation scope:** Full migration vs. selective

### Long-term Architecture Evolution
1. 🔮 **Service mesh consideration:** As services multiply, consider Istio/Linkerd
2. 🔮 **Micro-frontend architecture:** Evaluate for complex UI services
3. 🔮 **Shared data layer:** Consider when cross-service data needs mature

---

**Next Steps:**
1. Review findings with architecture team
2. Prioritize Phase 1 implementation
3. Create implementation issues with detailed acceptance criteria
4. Begin dependency consolidation with lowest-risk services first

**Document Maintenance:**
- Update after each consolidation phase
- Track metrics and validate assumptions
- Review quarterly for new overlap patterns