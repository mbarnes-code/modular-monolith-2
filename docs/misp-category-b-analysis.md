# MISP Category B Domain Logic Analysis

**Date**: 2025-10-31  
**Task**: T1531b - Identify Category B (Domain Logic 1,000-5,000 lines) for modular monolith integration  
**Criteria**: Components 1,000-5,000 lines with domain-specific business logic suitable for modular monolith services

## Category B Components Identified

### 1. MispAttribute Model - Threat Indicator Management
**File**: `app/Model/MispAttribute.php`  
**Lines of Code**: 4,198 lines  
**Complexity**: MEDIUM-HIGH - Data validation and normalization  

**Domain Logic**:
- **IOC Type Validation**: Complex validation for 50+ indicator types (IP, domain, hash, etc.)
- **Value Normalization**: Format standardization for threat indicators
- **Type-Category Compatibility**: Business rules for valid indicator combinations
- **IDS Signature Generation**: Logic for converting IOCs to detection rules
- **Distribution Inheritance**: Attribute-level sharing control logic
- **Correlation Participation**: Rules for correlation eligibility

**Integration Strategy**: Security domain service within monolith  
**Migration Risk**: MEDIUM - Data quality affects entire threat intelligence pipeline  
**Performance Requirements**: <1s attribute validation, <200ms type detection

### 2. User Authentication & Authorization
**File**: `app/Model/User.php`  
**Lines of Code**: 2,381 lines  
**Complexity**: MEDIUM - Security-critical user management  

**Domain Logic**:
- **Multi-Factor Authentication**: TOTP implementation and validation
- **Role-Based Access Control**: Complex permission hierarchy (Site Admin, Org Admin, User, Read Only)
- **API Key Management**: Cryptographic key generation and validation
- **Session Security**: Secure session management with timeout controls
- **Password Policy Enforcement**: Configurable password complexity and history
- **Account Lockout Protection**: Brute force protection mechanisms

**Integration Strategy**: Unified authentication service within monolith  
**Migration Risk**: MEDIUM - Security controls affect all system access  
**Performance Requirements**: <200ms authentication, <100ms authorization checks

### 3. ComplexTypeTool - IOC Validation Engine
**File**: `app/Lib/Tools/ComplexTypeTool.php`  
**Estimated Lines**: 2,000-3,000 lines  
**Complexity**: MEDIUM - Advanced validation logic  

**Domain Logic**:
- **Automatic Type Detection**: Machine learning-like pattern recognition for IOC types
- **Format Validation**: Regex and algorithmic validation for each IOC type
- **Composite Value Handling**: Multi-part indicators (IP|Port, filename|hash)
- **Security Validation**: Prevention of malicious indicator injection
- **Normalization Rules**: Standardization of indicator formats
- **False Positive Detection**: Integration with warninglist validation

**Integration Strategy**: Shared validation service within monolith  
**Migration Risk**: MEDIUM - Validation accuracy affects data quality  
**Performance Requirements**: <100ms validation per attribute, batch processing support

### 4. Organization Management
**File**: `app/Model/Organisation.php`  
**Estimated Lines**: 1,500-2,000 lines  
**Complexity**: MEDIUM - Multi-tenancy logic  

**Domain Logic**:
- **Organization Hierarchy**: Parent-child organization relationships
- **Trust Relationships**: Inter-organization trust and sharing configurations
- **User Association**: Organization membership and role assignment
- **Data Isolation**: Organization-based data access controls
- **Sharing Group Management**: Organization participation in sharing groups
- **Synchronization Rules**: Cross-organization data sharing protocols

**Integration Strategy**: Organization domain service within monolith  
**Migration Risk**: MEDIUM - Multi-tenancy affects data access patterns  
**Performance Requirements**: <500ms organization operations, efficient multi-tenant queries

### 5. Synchronization Engine
**File**: `app/Model/Server.php` + sync components  
**Estimated Lines**: 2,500-3,500 lines  
**Complexity**: MEDIUM - Distributed system coordination  

**Domain Logic**:
- **Pull/Push Synchronization**: Bidirectional data synchronization between MISP instances
- **Conflict Resolution**: Handling of concurrent modifications across instances
- **Distribution Validation**: Ensuring sharing rules are respected during sync
- **Incremental Sync**: Efficient delta synchronization for large datasets
- **Error Handling**: Robust error recovery and retry mechanisms
- **Authentication**: Secure authentication between MISP instances

**Integration Strategy**: Synchronization service within monolith with external API  
**Migration Risk**: MEDIUM - Affects inter-instance communication  
**Performance Requirements**: <30s for incremental sync, <5min for full sync

### 6. Tag & Taxonomy Management
**File**: `app/Model/Tag.php`, `app/Model/Taxonomy.php`  
**Estimated Lines**: 1,800-2,500 lines combined  
**Complexity**: MEDIUM - Classification and metadata management  

**Domain Logic**:
- **Hierarchical Taxonomies**: Complex taxonomy tree structures (MITRE ATT&CK, etc.)
- **Tag Application Rules**: Business rules for tag assignment and validation
- **Taxonomy Updates**: Handling of taxonomy version updates and migrations
- **Color Coding**: Visual classification system for threat levels
- **Export Integration**: Tag inclusion in various export formats
- **Search Integration**: Tag-based search and filtering logic

**Integration Strategy**: Metadata service within monolith  
**Migration Risk**: LOW-MEDIUM - Affects classification and search  
**Performance Requirements**: <200ms tag operations, efficient taxonomy queries

## Category B Integration Strategy

### Modular Monolith Domain Services

**1. Security Domain Service**
```yaml
Service Name: SecurityDomain
Components: MispAttribute, ComplexTypeTool, IOC validation
Responsibility: Threat indicator management and validation
Database Schema: Attributes, types, validation rules
API Endpoints: /api/security/attributes, /api/security/validation
Performance: <1s attribute operations, <200ms validation
```

**2. Identity Domain Service**
```yaml
Service Name: IdentityDomain  
Components: User, Organization, authentication
Responsibility: User management and authentication
Database Schema: Users, organizations, roles, sessions
API Endpoints: /api/identity/auth, /api/identity/users
Performance: <200ms authentication, <500ms user operations
```

**3. Synchronization Domain Service**
```yaml
Service Name: SynchronizationDomain
Components: Server, sync logic, conflict resolution
Responsibility: Inter-instance data synchronization
Database Schema: Servers, sync state, conflict logs
API Endpoints: /api/sync/pull, /api/sync/push
Performance: <30s incremental sync, robust error handling
```

**4. Metadata Domain Service**
```yaml
Service Name: MetadataDomain
Components: Tag, Taxonomy, classification logic
Responsibility: Data classification and metadata management
Database Schema: Tags, taxonomies, classifications
API Endpoints: /api/metadata/tags, /api/metadata/taxonomies
Performance: <200ms tag operations, efficient search integration
```

### Migration Approach for Category B

**Domain Service Integration**:
- Implement as separate modules within monolith architecture
- Maintain clear service boundaries with defined APIs
- Share common infrastructure (database, logging, monitoring)
- Enable independent testing and deployment of domain logic

**Database Integration**:
- Shared PostgreSQL database with schema separation
- Domain-specific tables with cross-domain foreign keys
- Optimized indexes for domain-specific query patterns
- Transaction coordination for cross-domain operations

**API Design**:
- RESTful APIs for each domain service
- Consistent authentication and authorization across domains
- Versioned APIs for backward compatibility
- OpenAPI documentation for all endpoints

### Performance Optimization

**Caching Strategy**:
- Redis caching for frequently accessed validation rules
- Organization and user data caching for authentication
- Taxonomy and tag caching for classification operations
- Correlation cache for performance-critical operations

**Database Optimization**:
- Domain-specific database indexes for optimal query performance
- Connection pooling for efficient database resource utilization
- Query optimization for complex cross-domain operations
- Database partitioning for large attribute datasets

## Next Steps

1. **Detailed Component Analysis**: Deep dive into each Category B component
2. **API Contract Design**: Define internal APIs for domain services
3. **Database Schema Design**: Plan domain separation within shared database
4. **Integration Testing**: Plan testing strategy for domain service interactions
5. **Performance Benchmarking**: Establish baseline metrics for optimization