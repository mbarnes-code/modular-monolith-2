# MISP Business Logic Analysis - Phase 8 Asset Relocation

**Date**: 2025-10-31  
**Purpose**: Analysis of MISP business logic for asset relocation into modular monolith architecture  
**Source**: `/docs/modular-analysis-repo-main/reports/misp-analysis.md`

## Section 4 (Business Logic) - Critical Threat Intelligence Correlation Algorithms

### Core Business Rules Identified

**Event Lifecycle Management**
- **Source**: Section 3.1 - Event Creation and Publication
- **Complexity**: HIGH - Critical threat intelligence workflow
- **Lines of Code**: Event.php (8,733 lines) - Category A (Complex Algorithms >5,000 lines)
- **Preservation Priority**: CRITICAL - 100% functionality preservation required

**Key Components**:
1. **Event State Machine**:
   - States: Draft → Validated → Published
   - Business Logic: State transitions with validation rules
   - Implementation: `app/Model/Event.php` with complex state management
   - **CRITICAL**: Event publication workflow affects entire threat intelligence sharing network

2. **Distribution Control System**:
   - **Complexity**: CRITICAL - Multi-level information sharing security
   - **Business Impact**: Controls who can access threat intelligence data
   - **Lines**: Distributed across Event.php and related models
   - **Security Requirements**: Granular access control with audit trail

3. **Threat Intelligence Correlation Engine**:
   - **Source**: `app/Model/Correlation.php`
   - **Business Logic**: Automatic relationship detection between threat indicators
   - **Complexity**: HIGH - CPU and memory intensive algorithms
   - **Performance**: Critical for threat hunting and attribution
   - **Preservation**: Algorithm logic MUST be preserved exactly

### Category A (Complex Algorithms >5,000 lines) - Microservice Preservation

**1. Event Model (8,733 lines)**
```yaml
Component: Event.php
Location: app/Model/Event.php
Complexity: VERY HIGH
Business Logic:
  - Event lifecycle state machine
  - Distribution control validation
  - Cross-organization sharing rules
  - Publication workflow orchestration
  - Correlation trigger management
Preservation Strategy: Dedicated microservice with API compatibility
Migration Risk: CRITICAL - Core threat intelligence functionality
```

**2. Correlation Engine**
```yaml
Component: Correlation.php  
Location: app/Model/Correlation.php
Complexity: HIGH
Business Logic:
  - Automatic threat indicator correlation
  - Cross-event relationship detection
  - Performance-optimized matching algorithms
  - Distribution-aware correlation (respects sharing rules)
Preservation Strategy: Dedicated correlation microservice
Migration Risk: HIGH - Performance and accuracy critical
```

### Category B (Domain Logic 1,000-5,000 lines) - Modular Monolith Integration

**1. MispAttribute Model (4,198 lines)**
```yaml
Component: MispAttribute.php
Location: app/Model/MispAttribute.php  
Complexity: MEDIUM-HIGH
Business Logic:
  - Threat indicator validation and normalization
  - Type-category compatibility checking
  - Value format validation (IP, domain, hash, etc.)
  - IDS signature generation rules
Preservation Strategy: Domain service within monolith
Migration Risk: MEDIUM - Data quality and validation critical
```

**2. Authentication & Authorization (2,381 lines)**
```yaml
Component: User.php
Location: app/Model/User.php
Complexity: MEDIUM
Business Logic:
  - Multi-factor authentication (TOTP)
  - Role-based access control (RBAC)
  - API key management
  - Session security management
Preservation Strategy: Unified authentication service
Migration Risk: MEDIUM - Security controls critical
```

**3. ComplexTypeTool Validation**
```yaml
Component: ComplexTypeTool.php
Location: app/Lib/Tools/ComplexTypeTool.php
Complexity: MEDIUM
Business Logic:
  - Automatic IOC type detection
  - Format validation and normalization
  - Multi-part value handling (IP|Port)
  - Security validation (prevent malicious indicators)
Preservation Strategy: Shared validation service
Migration Risk: MEDIUM - Data quality affects entire system
```

### Category C (Utilities <1,000 lines) - Shared Library Integration

**1. UUID Generation & Management**
```yaml
Components: Various UUID utilities
Complexity: LOW
Business Logic:
  - RFC 4122 compliant UUID generation
  - Global uniqueness for cross-MISP sync
Preservation Strategy: Shared utility library
Migration Risk: LOW - Standard functionality
```

**2. Data Export Utilities**
```yaml
Components: Export format handlers
Complexity: LOW-MEDIUM
Business Logic:
  - STIX/TAXII format conversion
  - OpenIOC XML generation
  - IDS rule generation (Snort, Suricata, YARA)
Preservation Strategy: Shared export service
Migration Risk: LOW - Format conversion utilities
```

### Section 11 (Domain Knowledge) - Critical Intelligence Operations

**Threat Intelligence Domain Expertise**:
1. **Malware Analysis Integration**: YARA rule generation, sample correlation
2. **Network Security Integration**: IDS/IPS rule generation from IOCs
3. **SIEM Integration**: Real-time threat feed generation
4. **Cross-Instance Synchronization**: Distributed threat intelligence sharing

**Domain-Specific Performance Requirements**:
- **Correlation Processing**: <1s for new attribute correlation (Security domain requirement)
- **Export Generation**: <30s for IDS rule generation
- **Synchronization**: Real-time data propagation between MISP instances
- **Search Performance**: <5s for complex IOC searches

## Business Logic Preservation Strategy

### Critical Preservation Requirements

1. **100% Algorithm Preservation**: Correlation engine algorithms must be preserved exactly
2. **State Machine Integrity**: Event lifecycle state machine must maintain exact behavior
3. **Security Model Preservation**: Distribution and sharing controls must be identical
4. **Performance Characteristics**: Response times must meet or exceed current system
5. **API Compatibility**: External integrations must continue to function

### Migration Approach per Category

**Category A - Microservices**:
- Event management microservice with API gateway
- Correlation engine microservice with dedicated resources
- Maintain exact API contracts for external integrations

**Category B - Domain Services**:
- Authentication service within monolith
- Attribute validation service with shared validation logic
- User management with role-based access control

**Category C - Shared Libraries**:
- Common utilities in `libs/shared/`
- Export format handlers as pluggable services
- UUID and data normalization utilities

## Next Steps

1. **Complete asset categorization** (Tasks T1521a-T1541c)
2. **Review configuration assets** (Task T1551d)
3. **Analyze multi-language components** (Task T1561e)
4. **Document infrastructure dependencies** (Task T1571f)
5. **Plan preservation strategy implementation**
