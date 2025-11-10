# MISP Data Models Migration

**Task**: T1642 - Extract data models from MISP per Section 2 (Data Architecture) of analysis

**Migration Date**: 2025-01-25  
**Source**: MISP CakePHP/MySQL models → PostgreSQL/SQLAlchemy
**Target**: apps/security-service/src/data/models/misp/

## Core Entity Models

Based on analysis of MISP's data architecture, the following core entities have been identified for migration:

### Critical Models (Category A - Complex Relationships)
1. **Event** - Central threat intelligence entity (8,740 lines)
2. **MispAttribute** - Event attributes and indicators 
3. **MispObject** - Structured threat intelligence objects
4. **User** - User management and authentication
5. **Organisation** - Organization management
6. **Correlation** - Threat intelligence correlation

### Domain Models (Category B - Business Logic)
7. **Tag** - Classification and labeling system
8. **Galaxy** - Threat actor and technique clustering
9. **SharingGroup** - Data sharing controls
10. **Feed** - External data feeds
11. **Server** - MISP instance federation
12. **Workflow** - Automation and processing

### Utility Models (Category C - Supporting Data)
13. **ThreatLevel** - Risk classification
14. **Taxonomy** - Standardized classifications  
15. **Sighting** - Indicator sightings
16. **AuditLog** - System auditing
17. **Job** - Background processing
18. **Log** - System logging

## Schema Migration Strategy

### Field Type Mapping (MySQL → PostgreSQL)
```yaml
MySQL Types → PostgreSQL Types:
  int(11) → INTEGER
  bigint(20) → BIGINT  
  varchar(255) → VARCHAR(255)
  text → TEXT
  longtext → TEXT
  mediumtext → TEXT
  datetime → TIMESTAMP WITH TIME ZONE
  timestamp → TIMESTAMP WITH TIME ZONE
  tinyint(1) → BOOLEAN
  decimal(10,2) → NUMERIC(10,2)
  json → JSONB
  blob → BYTEA
  enum → VARCHAR with CHECK constraints
```

### Relationship Preservation
```yaml
Foreign Key Constraints:
  - All belongsTo relationships preserved
  - hasMany relationships with proper cascading
  - Many-to-many through junction tables
  - Self-referential relationships maintained

Index Migration:
  - All performance-critical indexes preserved
  - Multi-column indexes for correlation queries
  - Full-text search indexes where applicable
  - UUID indexes for distributed operations
```

### Performance Optimizations
```yaml
PostgreSQL Enhancements:
  - JSONB for flexible metadata storage
  - Partial indexes for conditional queries  
  - GIN indexes for array and JSON searches
  - Table partitioning for large datasets
  - Connection pooling and query optimization
```

## Migration Progress

- [x] Analysis completed - Core entities identified
- [ ] Base model classes created
- [ ] Critical models migrated (Event, Attribute, Object)
- [ ] Domain models migrated (User, Org, Tag, etc.)
- [ ] Utility models migrated
- [ ] Relationships established
- [ ] Indexes and constraints applied
- [ ] Data migration scripts created
- [ ] Validation and testing completed

**Next**: Create base SQLAlchemy model classes for MISP entities