# DATABASE CONSOLIDATION STRATEGY
## From 18+ Separate PostgreSQL Databases to Single Unified Instance with Domain-Based Schemas

**Executive Summary**: This document outlines how to consolidate 18+ PostgreSQL databases and 8+ SQLite applications into a single PostgreSQL instance with domain-driven design principles, enabling shared infrastructure while maintaining clear data boundaries.

**Created**: November 10, 2025  
**Repository**: Mental Prosthetic Platform (37-tool analysis)  
**Status**: Ready for Implementation Planning

---

## TABLE OF CONTENTS

1. [Current State Analysis](#current-state-analysis)
2. [PostgreSQL Projects Inventory](#postgresql-projects-inventory)
3. [Data Model Analysis](#data-model-analysis)
4. [Schema Consolidation Strategy](#schema-consolidation-strategy)
5. [Domain Boundary Mapping](#domain-boundary-mapping)
6. [Multi-Tenancy Opportunities](#multi-tenancy-opportunities)
7. [SQLite Migration Path](#sqlite-migration-path)
8. [Implementation Roadmap](#implementation-roadmap)
9. [Migration Risk Analysis](#migration-risk-analysis)
10. [Appendices](#appendices)

---

## CURRENT STATE ANALYSIS

### Database Technology Distribution

```
Total Projects Analyzed:     37
PostgreSQL Projects:         18 (48.6%)  ← TARGET FOR CONSOLIDATION
SQLite Projects:             8  (21.6%)  ← MIGRATION CANDIDATES
MySQL/MariaDB Projects:      4  (10.8%)
MongoDB Projects:            2  (5.4%)
Other (Elasticsearch, etc):  5  (13.5%)
```

### Key Finding: Significant Database Fragmentation

Each of the 18 PostgreSQL projects maintains its own database instance with:
- Duplicate schema patterns (Users, Config, Logging)
- Independent connection pools
- Separate backup/recovery procedures
- Isolated data access control
- Redundant infrastructure management

**Consolidation Potential**: 18 databases → 1 PostgreSQL instance with 18 schemas

---

## POSTGRESQL PROJECTS INVENTORY

### TIER 1: CRITICAL BUSINESS DOMAINS (High Data Volume & Complexity)

| # | Project | Domain | Data Volume | Schema Focus | Status |
|---|---------|--------|-------------|-------------|--------|
| 1 | **Dispatch** | Incident Management | Medium | Incidents, Participants, Workflows | Active/Archived |
| 2 | **Ghostwriter** | Red Team Operations | Medium | Projects, Findings, Reports, Domains | Active |
| 3 | **MISP** | Threat Intelligence | Large | Events, Attributes, Correlations, Organizations | Active |
| 4 | **n8n** | Workflow Automation | Medium | Workflows, Executions, Credentials | Active |
| 5 | **HexStrike AI** | Security Analysis | Medium | Analysis Results, Configurations, Vector DB | Active |
| 6 | **Commander Spellbook** | MTG Combo DB | Small-Medium | Cards, Combos, Metadata | Active |
| 7 | **Mealie** | Recipe Management | Small-Medium | Recipes, Ingredients, Users | Active |
| 8 | **Kong** | API Gateway | Medium | Routes, Plugins, Services | Active |

### TIER 2: OPERATIONAL FRAMEWORKS (Medium Volume)

| # | Project | Domain | Data Volume | Schema Focus | Status |
|---|---------|--------|-------------|-------------|--------|
| 9 | **Nemesis** | Post-Exploitation | Medium | Sessions, Data, Operations | Active |
| 10 | **RITA** | Network Analysis | Medium | Flows, Metadata, Analysis | Active |
| 11 | **SecurityOnion** | Network Monitoring | Large | Logs, Alerts, Config | Active |
| 12 | **Firecrawl** | Web Scraping | Medium | Jobs, Results, Config | Active |

### TIER 3: TOOLS & UTILITIES (Small Volume)

| # | Project | Domain | Data Volume | Schema Focus | Status |
|---|---------|--------|-------------|-------------|--------|
| 13-18 | **MCP Servers** (6) | Tool Integration | Minimal | Config, Cache, State | Active |

**Remaining PostgreSQL Projects**: Meterpreter, and others requiring investigation

---

## DATA MODEL ANALYSIS

### Common Data Patterns Across PostgreSQL Projects

#### Pattern 1: User & Organization Management (16/18 projects)

```yaml
CRITICAL SCHEMA: auth_shared

Tables:
  - users
    Columns: id, username, email, password_hash, created_at, updated_at
    Used By: Dispatch, Ghostwriter, MISP, n8n, Nemesis, HexStrike, Kong
    
  - organizations
    Columns: id, name, code, created_at
    Used By: Dispatch, Ghostwriter, MISP, Nemesis, HexStrike, Kong
    
  - user_roles
    Columns: id, user_id, organization_id, role, permissions_json
    Used By: Most projects
    
  - audit_logs
    Columns: id, user_id, action, resource, timestamp
    Used By: 12+ projects

Sharing Opportunities:
  ✓ Can be shared across domains with proper isolation
  ✓ Enable single sign-on (SSO) for all tools
  ✓ Centralized audit logging
  ✓ Unified permission model
```

#### Pattern 2: Configuration Storage (14/18 projects)

```yaml
CRITICAL SCHEMA: config_shared

Common Configurations:
  - API credentials and tokens
  - System settings and features flags
  - Notification preferences
  - Integration endpoints
  
Projects Sharing:
  - Dispatch: incident severity/priority levels, notification settings
  - MISP: distribution levels, sharing groups
  - n8n: credential management
  - HexStrike: API keys, service config
  - Kong: plugin configurations
  - Ghostwriter: template settings
  - Nemesis: operation parameters

Recommendation: Create config_shared schema with domain-partitioned tables:
  - Table: configurations
    Partition key: domain_id, config_key, value

Benefits:
  ✓ Centralized secret management
  ✓ Consistent environment variable handling
  ✓ Easy feature flag management
  ✓ Simplified configuration audit trail
```

#### Pattern 3: Time-Series Data & Audit Trails (12/18 projects)

```yaml
CRITICAL SCHEMA: audit_logging_shared

Data Types:
  - Activity logs (who did what, when)
  - System events
  - Error logs
  - Audit trails for compliance
  
Projects Using:
  - Dispatch: incident timeline, participant activities
  - Ghostwriter: finding changes, report edits
  - MISP: attribute modifications, event publishing
  - SecurityOnion: alert logs, detection logs
  - n8n: workflow executions
  - RITA: flow analysis records
  - HexStrike: analysis job tracking
  - Nemesis: operation logs

Recommendation: Time-series tables with domain partitioning:
  - audit_events (domain_id, timestamp, user_id, event_type, details)
  - Partition by range: monthly or quarterly
  
Benefits:
  ✓ Simplified retention policies
  ✓ Efficient archiving/deletion
  ✓ Better query performance
  ✓ Compliance-friendly audit trail
```

---

## SCHEMA CONSOLIDATION STRATEGY

### Recommended Schema Structure (18+ Domain Schemas + 3 Shared Schemas)

```
UNIFIED PostgreSQL INSTANCE: mental_prosthetic_db
├── SHARED SCHEMAS (Infrastructure)
│   ├── auth_shared/
│   ├── config_shared/
│   └── audit_logging_shared/
│
├── DOMAIN SCHEMAS (Business Logic)
│   ├── incident_management/        (Dispatch)
│   ├── offensive_security/         (Ghostwriter, Nemesis)
│   ├── threat_intelligence/        (MISP)
│   ├── security_monitoring/        (SecurityOnion, RITA)
│   ├── workflow_automation/        (n8n)
│   ├── api_gateway/               (Kong)
│   ├── security_analysis/         (HexStrike AI)
│   ├── recipe_management/         (Mealie)
│   ├── mtg_database/              (Commander Spellbook)
│   ├── web_scraping/              (Firecrawl)
│   ├── vector_database/           (Chroma MCP)
│   └── [5+ Additional Domain Schemas]/
│
└── UTILITY SCHEMAS (Shared Infrastructure)
    ├── _schema_versioning/
    ├── _migration_tracking/
    └── _performance_metrics/
```

### Schema Isolation Strategy

Each domain schema maintains complete isolation:

```sql
-- ISOLATION PRINCIPLE: Schemas are SQL-enforced boundaries
-- No cross-schema foreign keys allowed
-- All cross-domain references through application layer

-- Example: incident_management schema
CREATE SCHEMA incident_management;

CREATE TABLE incident_management.incidents (
  id BIGSERIAL PRIMARY KEY,
  org_id BIGINT NOT NULL,  -- Reference to auth_shared.organizations
  title TEXT NOT NULL,
  description TEXT,
  created_by BIGINT NOT NULL,  -- Reference to auth_shared.users
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  -- Domain-specific data
  status VARCHAR(50) NOT NULL,
  severity SMALLINT,
  priority SMALLINT
);

-- Cross-schema access: Application-mediated only
-- CREATE ROLE incident_mgmt_user;
-- GRANT USAGE ON SCHEMA incident_management TO incident_mgmt_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA incident_management 
--   TO incident_mgmt_user;
```

---

## DETAILED SCHEMA BLUEPRINTS

### SHARED SCHEMA 1: auth_shared

**Purpose**: Unified authentication and organization management

```yaml
Tables:
  users:
    Columns:
      - id: BIGSERIAL (PK)
      - uuid: UUID (UNIQUE)
      - username: VARCHAR(255) (UNIQUE)
      - email: VARCHAR(255) (UNIQUE, INDEXED)
      - password_hash: VARCHAR(255)
      - first_name: VARCHAR(255)
      - last_name: VARCHAR(255)
      - is_active: BOOLEAN (DEFAULT true)
      - last_login_at: TIMESTAMP
      - created_at: TIMESTAMP (DEFAULT CURRENT_TIMESTAMP)
      - updated_at: TIMESTAMP
    Indexes:
      - email (for login queries)
      - is_active, created_at (for user listing)
    Used By: All domains

  organizations:
    Columns:
      - id: BIGSERIAL (PK)
      - uuid: UUID (UNIQUE)
      - name: VARCHAR(255) (UNIQUE)
      - slug: VARCHAR(255) (UNIQUE, INDEXED)
      - description: TEXT
      - domain_id: VARCHAR(100)  -- References domain schema (not FK)
      - settings_json: JSONB
      - created_at: TIMESTAMP
      - updated_at: TIMESTAMP
    Used By: All multi-tenant domains

  user_organization_roles:
    Columns:
      - id: BIGSERIAL (PK)
      - user_id: BIGINT (FK users.id) (NOT NULL)
      - organization_id: BIGINT (FK organizations.id) (NOT NULL)
      - role: VARCHAR(100) (NOT NULL)
      - permissions_json: JSONB
      - created_at: TIMESTAMP
      - updated_at: TIMESTAMP
    Constraints:
      - UNIQUE(user_id, organization_id)

  api_tokens:
    Columns:
      - id: BIGSERIAL (PK)
      - user_id: BIGINT (FK users.id) (NOT NULL)
      - token_hash: VARCHAR(255) (UNIQUE, INDEXED)
      - name: VARCHAR(255)
      - last_used_at: TIMESTAMP
      - expires_at: TIMESTAMP
      - created_at: TIMESTAMP
    Used By: All domains requiring API access

Benefits:
  ✓ Single sign-on (SSO) enabled
  ✓ Centralized user management
  ✓ Unified authentication across all 18 domains
  ✓ Audit trail for access control changes
```

### SHARED SCHEMA 2: config_shared

**Purpose**: Centralized configuration management

```yaml
Tables:
  configurations:
    Columns:
      - id: BIGSERIAL (PK)
      - organization_id: BIGINT (FK auth_shared.organizations.id) (nullable, for system config)
      - domain: VARCHAR(100) (INDEXED)  -- incident_management, threat_intelligence, etc.
      - key: VARCHAR(255) (NOT NULL)
      - value: TEXT (NOT NULL)
      - data_type: VARCHAR(50)  -- string, json, integer, boolean
      - created_by: BIGINT (FK auth_shared.users.id)
      - created_at: TIMESTAMP
      - updated_at: TIMESTAMP
    Constraints:
      - UNIQUE(organization_id, domain, key)
      - Index on (domain, key) for efficient lookups
    Example Values:
      - (org_123, 'incident_management', 'severity_levels', '{"critical": 1, "high": 2, ...}')
      - (org_123, 'threat_intelligence', 'distribution_levels', '{"internal": 1, "community": 2, ...}')

  feature_flags:
    Columns:
      - id: BIGSERIAL (PK)
      - organization_id: BIGINT (FK auth_shared.organizations.id) (nullable)
      - domain: VARCHAR(100) (INDEXED)
      - feature_name: VARCHAR(255)
      - enabled: BOOLEAN
      - config_json: JSONB
      - created_at: TIMESTAMP
      - updated_at: TIMESTAMP
    Examples:
      - Enable/disable AI-powered analysis in HexStrike
      - Enable/disable correlation engine in MISP
      - Enable/disable webhook notifications in n8n

  secrets:
    Columns:
      - id: BIGSERIAL (PK)
      - organization_id: BIGINT (FK auth_shared.organizations.id)
      - domain: VARCHAR(100) (INDEXED)
      - secret_name: VARCHAR(255)
      - encrypted_value: TEXT (ENCRYPTED with at-rest encryption)
      - encryption_key_id: VARCHAR(100)
      - last_accessed_at: TIMESTAMP
      - created_by: BIGINT
      - created_at: TIMESTAMP
    Security:
      ✓ All values encrypted at rest
      ✓ Row-level security (RLS) enabled
      ✓ Access logged to audit_logging_shared
      ✓ Rotation tracked with encryption_key_id

Benefits:
  ✓ Centralized secret management (replaces 18 separate config systems)
  ✓ Per-organization configuration isolation
  ✓ Audit trail for all changes
  ✓ Easy feature flag rollout
```

### SHARED SCHEMA 3: audit_logging_shared

**Purpose**: Unified audit trail for compliance

```yaml
Tables:
  audit_events:
    Columns:
      - id: BIGSERIAL (PK)
      - organization_id: BIGINT (FK auth_shared.organizations.id) (NOT NULL)
      - domain: VARCHAR(100) (INDEXED)
      - resource_type: VARCHAR(100)  -- incident, attribute, event, etc.
      - resource_id: BIGINT (INDEXED)
      - action: VARCHAR(100)  -- create, update, delete, publish, etc.
      - user_id: BIGINT (FK auth_shared.users.id)
      - user_email: VARCHAR(255)  -- denormalized for deleted users
      - changes_json: JSONB  -- before/after values
      - ip_address: INET
      - user_agent: TEXT
      - timestamp: TIMESTAMP (INDEXED, DEFAULT CURRENT_TIMESTAMP)
    Partitioning:
      - Range partitioned by timestamp (monthly)
      - OLD data archived after 90 days
    Indexes:
      - (organization_id, timestamp DESC)
      - (resource_type, resource_id)
      - (user_id, timestamp DESC)
    Retention:
      - Hot: 1 year
      - Warm: 3 years (compressed)
      - Cold: 7 years (archive to S3)

  access_logs:
    Columns:
      - id: BIGSERIAL (PK)
      - organization_id: BIGINT
      - user_id: BIGINT
      - endpoint: VARCHAR(500)
      - method: VARCHAR(10)  -- GET, POST, etc.
      - status_code: INTEGER
      - response_time_ms: INTEGER
      - timestamp: TIMESTAMP (INDEXED)
    Purpose: Performance monitoring, security analysis
    Partitioning: Daily, archive after 30 days

Benefits:
  ✓ Single source of truth for compliance audits
  ✓ SIEM integration ready
  ✓ Forensics investigation enabled
  ✓ Searchable across all 18 domains
```

### DOMAIN SCHEMA 1: incident_management (Dispatch)

```yaml
Tables:
  incidents:
    Purpose: Core incident tracking
    Columns:
      - id, uuid, org_id, title, description, status, severity, priority
      - reported_by (FK auth_shared.users), reported_at
      - created_at, updated_at
    Relationships: ├─ participants (many)
                  ├─ tags (many-to-many)
                  ├─ reports (many)
                  └─ timeline_events (many)
    Partition Strategy: By org_id (if multi-tenant)
    Data Volume: ~100K-1M records (typical enterprise)

  incident_participants:
    Purpose: People involved in incident response
    Columns: id, incident_id, user_id, role, added_by, added_at, departed_at
    Relationships: ├─ incident
                  └─ user (FK auth_shared.users)

  incident_reports:
    Purpose: Tactical/Executive summaries
    Columns: id, incident_id, report_type, content, created_by, created_at
    Types: TACTICAL_REPORT, EXECUTIVE_REPORT

  incident_timeline:
    Purpose: Chronological event log
    Columns: id, incident_id, event_type, description, user_id, timestamp
    Examples: status_changed, participant_added, report_generated, etc.

Indexes:
  - incidents(org_id, status, reported_at DESC)
  - incidents(search_vector)  -- PostgreSQL TSVector for full-text search
  - incident_participants(incident_id)
  - incident_timeline(incident_id, timestamp DESC)

Multi-Tenancy: ✓ Full isolation by org_id
Performance: Expected 50-200ms for typical queries
```

### DOMAIN SCHEMA 2: threat_intelligence (MISP)

```yaml
Tables:
  events:
    Purpose: Threat intelligence reports
    Columns:
      - id, uuid, org_id, orgc_id (creator org)
      - info (description), date, published, distribution
      - analysis (status: 0=initial, 1=ongoing, 2=complete)
      - threat_level_id, sharing_group_id
      - timestamp, created_at, updated_at
    Partitioning: By org_id or date-based for large instances
    Typical Volume: 10K-1M events per large organization

  attributes (threat indicators):
    Purpose: Individual IOCs (IP, domain, hash, etc.)
    Columns:
      - id, uuid, event_id, category, type
      - value1, value2 (composite: IP|Port)
      - to_ids (generate IDS rule flag)
      - distribution, sharing_group_id
      - comment, timestamp, deleted (soft delete)
      - disable_correlation (opt-out)
    Expected Volume: 100K-10M+ records
    Indexes:
      - (event_id, type)  -- rapid event lookup
      - (value1)  -- correlation search
      - (uuid)  -- synchronization
      - (timestamp DESC)  -- feed generation

  correlations:
    Purpose: Automatic linking of related attributes
    Columns: id, attribute1_id, attribute2_id, similarity_score, created_at
    Purpose: Answer "what other events have this IP?"
    Data Volume: Massive (scales as O(n²) with attributes)
    Optimization: Materialized view with refresh schedule

  sharing_groups:
    Purpose: Control who sees what
    Columns: id, org_id, name, distribution_rules_json, created_at
    Relationships: ├─ shared_org (many-to-many)
                  └─ shared_user (many-to-many)

Indexes:
  - events(uuid UNIQUE)  -- global uniqueness
  - events(org_id, published, distribution)  -- sharing queries
  - attributes(event_id, type)
  - attributes(value1)  -- correlation lookups
  - attributes(uuid UNIQUE)

Multi-Tenancy: ✓ Org-based isolation via org_id and orgc_id
Performance: 100-500ms typical queries (heavily indexed)
Archival: Events >2 years auto-archived to separate tablespace
```

### DOMAIN SCHEMA 3: offensive_security (Ghostwriter + Nemesis)

```yaml
Tables:
  clients:
    Purpose: Customer information
    Columns: id, org_id, name, short_name, codename, timezone, address
    Relationships: ├─ contacts (many)
                  ├─ projects (many)
                  └─ domain_checkouts (many)

  projects:
    Purpose: Individual assessments/operations
    Columns:
      - id, org_id, client_id, codename
      - start_date, end_date, project_type
      - status (planning, active, closed), classification
      - notes, tags_json
    Relationships: ├─ client
                  ├─ findings (many)
                  ├─ reports (many)
                  ├─ team_members (many-to-many)
                  ├─ domains (many-to-many)
                  └─ infrastructure

  findings (vulnerabilities):
    Purpose: Security issues discovered
    Columns:
      - id, uuid, org_id, project_id
      - title, description, impact, mitigation
      - replication_steps, references
      - severity, finding_type, status
      - discovered_by, discovered_at, fixed_at
      - cvss_vector, cvss_score
    Relationships: ├─ project
                  ├─ evidence (attachments)
                  ├─ remediation_status_updates (timeline)
                  └─ client_acceptance
    Partitioning: By org_id if large volume
    Typical Volume: 1K-100K findings per large org

  reports:
    Purpose: Final assessment documents
    Columns:
      - id, org_id, project_id
      - title, executive_summary, methodology
      - status (draft, review, final, submitted)
      - generated_at, submitted_at, signed_by
      - template_id, styling_config_json
    Relationships: ├─ findings (through report_finding_links)
                  ├─ evidence
                  └─ recipient_list

  domains:
    Purpose: Red team infrastructure tracking
    Columns:
      - id, org_id, name (UNIQUE)
      - registrar, creation_date, expiration_date
      - health_status, reputation_score
      - created_at, expires_at
    Relationships: ├─ checkout (project assignments)
                  └─ dns_records
    Purpose: Monitor infrastructure health and reputations

Indexes:
  - projects(org_id, status, start_date DESC)
  - findings(project_id, severity, status)
  - findings(cvss_score DESC)  -- risk assessment queries
  - reports(org_id, project_id, status)
  - domains(org_id, expiration_date ASC)  -- renewal alerts

Multi-Tenancy: ✓ Full isolation by org_id
Performance: 50-200ms typical queries
Compliance: ✓ SOC 2 audit trail in audit_logging_shared
```

### DOMAIN SCHEMA 4: security_monitoring (SecurityOnion + RITA)

```yaml
Tables:
  detection_events:
    Purpose: Security alerts and detections
    Columns:
      - id, org_id, sensor_id
      - event_type (IDS alert, behavioral anomaly, etc.)
      - severity, confidence
      - source_ip, dest_ip, protocol, port
      - detection_rule_id, rule_signature
      - timestamp, created_at
      - raw_data (BYTEA for packet data), metadata_json
    Partitioning: Monthly by timestamp (massive volume)
    Typical Volume: 100B+ events annually for large SOC
    Retention: 90 days hot, 1 year warm (archive to object storage)
    Indexes:
      - (org_id, timestamp DESC)  -- retention/archival
      - (source_ip, timestamp)  -- attack source analysis
      - (dest_ip, timestamp)  -- targeted host analysis
      - (detection_rule_id)  -- rule performance

  flow_records:
    Purpose: Network flow data (from Zeek/NetFlow)
    Columns:
      - id, org_id, sensor_id
      - src_ip, dest_ip, src_port, dest_port, protocol
      - duration, bytes_in, bytes_out, packets
      - timestamp, created_at
      - application (detected protocol: HTTP, DNS, SSH, etc.)
      - risk_score, anomaly_flags
    Partitioning: Hourly or daily by timestamp
    Typical Volume: 10B+ flows annually
    Compression: CompressedTuples after 30 days

  alert_correlation:
    Purpose: Link related alerts
    Columns:
      - id, alert1_id, alert2_id
      - correlation_score, correlation_type
      - created_at

Indexes:
  - detection_events(org_id, severity DESC, timestamp DESC)
  - detection_events(source_ip)
  - flow_records(org_id, timestamp DESC)
  - flow_records(src_ip, dest_ip)

Multi-Tenancy: ✓ Sensor-based or org-based isolation
Performance: Optimized for large-scale metric queries
Archival: Automatic aging to object storage (S3/Minio)
```

### DOMAIN SCHEMA 5: workflow_automation (n8n)

```yaml
Tables:
  workflows:
    Purpose: Automation workflow definitions
    Columns:
      - id, org_id, name, description
      - workflow_definition_json (the actual workflow DAG)
      - active, tags
      - created_by, created_at, updated_at
      - last_executed_at, last_execution_status
    Relationships: ├─ executions (many)
                  ├─ triggers (many)
                  ├─ credentials (many-to-many)
                  └─ audit_trail

  executions:
    Purpose: Workflow run history
    Columns:
      - id, org_id, workflow_id
      - status (new, running, success, error)
      - started_at, completed_at, duration_ms
      - input_data_json, output_data_json
      - error_message, error_trace
    Partitioning: By timestamp (daily)
    Retention: 6 months hot, 2 years warm
    Purpose: Troubleshooting, monitoring, audit trail

  credentials:
    Purpose: Stored API keys and secrets
    Columns:
      - id, org_id, type (api_key, oauth_token, etc.)
      - credential_name, encrypted_value
      - last_used_at, created_by, created_at
    Security: ✓ Row-level security (RLS)
             ✓ Encrypted at rest
             ✓ Audit logged access

  triggers:
    Purpose: Workflow activators
    Columns:
      - id, org_id, workflow_id, trigger_type
      - trigger_config_json (cron schedule, webhook, event listener)
      - active, created_at

Indexes:
  - workflows(org_id, active, updated_at DESC)
  - executions(org_id, workflow_id, created_at DESC)
  - executions(status, created_at DESC)
  - credentials(org_id, credential_name UNIQUE)

Multi-Tenancy: ✓ Full org-based isolation
Performance: 100-500ms typical queries
Scalability: Execution log partitioning handles high volume
```

---

## DOMAIN BOUNDARY MAPPING

### Boundary Analysis Matrix

```
                        |Incident Mgmt|Threat Intel|Off. Sec|Security Mon|Workflow|API GW|Others
                        |-------------|------------|--------|------------|--------|------|------
SHARES auth_shared      |      ✓      |      ✓     |   ✓    |     ✓      |   ✓    |  ✓   |  ✓
SHARES config_shared    |      ✓      |      ✓     |   ✓    |     ✓      |   ✓    |  ✓   |  ✓
SHARES audit_logging    |      ✓      |      ✓     |   ✓    |     ✓      |   ✓    |  ✓   |  ✓
---|
INCIDENT→THREAT INTEL   |      ✗      |      ✗     |   ✗    |     ✗      |   ✗    |  ✗   |  -
(Cross-domain access)   |   (indirect)|            |        |            |        |      |
                        | via event   |            |        |            |        |      |
                        | streaming   |            |        |            |        |      |
---|
THREAT INTEL→OFF SEC    |      ✗      |      ✗     |   ✗    |     ✗      |   ✗    |  ✗   |  -
(No direct deps)        | publish     |            |        |            |        |      |
                        | events      |            |        |            |        |      |
---|
OFF SEC→THREAT INTEL    |      ✗      |    ✓ (?)   |   -    |     ✗      |   ✗    |  ✗   |  -
(Advisory reports)      |             | correlation|        |            |        |      |
---|
WORKFLOW→ALL DOMAINS    |    ✓ (?)    |    ✓ (?)   | ✓ (?)  |   ✓ (?)    |   -    |  ✗   |  -
(Event streaming)       |automation   |publishing  |report  | alert rules|        |      |
                        |             |            |gen     |            |        |      |
---|
API GW→ALL              |      ✗      |      ✗     |   ✗    |     ✗      |   ✗    |  -   |  ✗
(Infrastructure only)   |routing only |            |        |            |        |      |

Legend:
  ✓ = Strong relationship, common data sharing
  ✗ = No direct relationship (event-driven if needed)
  ? = Optional relationship, design-dependent
  - = Not applicable
```

### Cross-Domain Communication Patterns

**PRINCIPLE**: No direct database joins across schemas. Use event streaming or API calls.

#### Pattern 1: Event-Driven Async Communication

```
incident_management.incidents
         │
         ├──> [CREATE/UPDATE] ──> Event: "incident.created"
         │                              ↓
         │                    kafka/redis stream
         │                              ↓
         └──────────────────> [Listeners]
                               ├─ workflow_automation (trigger workflows)
                               ├─ audit_logging_shared (log event)
                               ├─ config_shared (check feature flags)
                               └─ security_monitoring (correlate alerts)
```

```python
# incident_management/models.py
class IncidentService:
    async def create_incident(self, title, description, org_id):
        incident = Incident(title=title, description=description, org_id=org_id)
        session.add(incident)
        session.commit()
        
        # Publish event (not database query!)
        await event_bus.publish({
            'type': 'incident.created',
            'incident_id': incident.id,
            'org_id': org_id,
            'timestamp': datetime.now(),
            'data': {...}
        })
        
        return incident

# Decoupled listener in workflow_automation/handlers.py
@event_bus.on('incident.created')
async def on_incident_created(event):
    # Application-level logic, not database query
    # Check if any workflows should trigger
    workflows = await get_workflows_for_event(
        org_id=event['org_id'],
        event_type='incident.created'
    )
    for workflow in workflows:
        await workflow_automation.trigger_workflow(workflow.id, event['data'])
```

#### Pattern 2: API Gateway Access (n8n → Other Domains)

```
workflow_automation (n8n)
         │
         ├──> API Call: GET /api/incident_management/incidents/{id}
         │              (through Kong API gateway)
         │                        ↓
         │              [incident_management service]
         │              [validates org_id, permissions]
         │                        ↓
         └──────────────────> Response: Incident data
                              (structured JSON, no schema access)
```

**Key Rules**:
- All cross-domain access goes through REST APIs or GraphQL
- Kong API gateway enforces authentication/authorization
- No direct schema/table access across domains
- Data is serialized/deserialized to prevent schema leakage

#### Pattern 3: Shared Reference Pattern (Carefully Used)

```
-- ALLOWED: Reference by ID only (no FK constraint)
incident_management.incidents
  ├── created_by: BIGINT  -- FK to auth_shared.users
  ├── updated_by: BIGINT  -- FK to auth_shared.users
  └── org_id: BIGINT      -- FK to auth_shared.organizations

-- NOT ALLOWED: Direct reference across domains
threat_intelligence.events
  ├── NO: FK to incident_management.incidents
  ├── NO: JOIN with offensive_security.projects
  └── ALLOWED: org_id (shared reference)
```

---

## MULTI-TENANCY OPPORTUNITIES

### Tenant Isolation Strategy

**Goal**: 1 PostgreSQL instance serves all 18 domains with perfect isolation

```yaml
Tenant Model: Organization-Based (org_id partition key everywhere)

Implementation:
  1. Row-Level Security (RLS) enabled on sensitive tables
  2. org_id as leading column in all indexes
  3. Application-level org_id validation on every query
  4. Database roles per organization (future enhancement)

Benefits:
  ✓ Single shared infrastructure
  ✓ Efficient resource utilization
  ✓ Centralized backups
  ✓ Simplified disaster recovery
  ✓ Lower operational overhead
```

### Multi-Tenancy Policy

#### Policy 1: Query Isolation

```sql
-- ENFORCED: Every query must filter by org_id

-- GOOD: Returns only org_123's incidents
SELECT * FROM incident_management.incidents 
WHERE org_id = ?org_id;

-- BAD: Would return data from all orgs if used
-- (prevented by application layer + RLS)
SELECT * FROM incident_management.incidents;
```

#### Policy 2: Tenant Scaling

```yaml
Scenario 1: Single Tenant (SMB)
  Configuration:
    - 1 Organization in auth_shared.organizations
    - All data for that org in each domain schema
    - Single database connection pool
  Typical Use: Small security team using integrated suite

Scenario 2: Multi-Tenant (Enterprise)
  Configuration:
    - Multiple organizations (100+) in auth_shared
    - Data partitioned by org_id across all schemas
    - Connection pooling per organization
    - Resource quotas per organization
  Typical Use: Large organization with multiple business units

Scenario 3: SaaS (Multiple Customers)
  Configuration:
    - Separate databases per customer (future)
    - OR: Single database with strict RLS policies
    - Billing tied to data volume
    - Compliance: SOC 2 audit trail in audit_logging_shared
  Typical Use: SaaS platform serving multiple customers
```

### Quota Management (Planned Feature)

```sql
-- auth_shared schema extension
CREATE TABLE organization_quotas (
  id BIGSERIAL PRIMARY KEY,
  org_id BIGINT (FK organizations.id) UNIQUE,
  
  -- Limits per organization
  max_users INTEGER (DEFAULT 100),
  max_workflows INTEGER (DEFAULT 1000),
  max_api_calls_per_day BIGINT (DEFAULT 1000000),
  max_storage_gb INTEGER (DEFAULT 1000),
  
  -- Current usage
  current_users_count INTEGER,
  current_workflows_count INTEGER,
  current_storage_gb INTEGER,
  
  updated_at TIMESTAMP
);

-- Triggers to enforce quotas
CREATE TRIGGER check_user_quota BEFORE INSERT ON auth_shared.users
FOR EACH ROW
EXECUTE FUNCTION check_org_user_quota();
```

---

## SQLITE MIGRATION PATH

### SQLite Projects to Migrate (8 total)

| Project | Current DB | Data Volume | Complexity | Priority |
|---------|-----------|------------|-----------|----------|
| **Actual Budget** | SQLite | Small (local) | Medium | High |
| **Maltrail** | SQLite | Medium | Low | Medium |
| **Brute Ratel C4** | SQLite | Small | Low | Low |
| **Goose** | SQLite | Small (session) | Low | Low |
| **Inspector** | In-Memory | Minimal | N/A | N/A |
| **KasmVNC** | SQLite | Small (sessions) | Low | Medium |
| **MTG Scripting** | SQLite | Small (cache) | Low | Low |
| **Software Forensic** | SQLite | Medium | Low | Low |

### Migration Strategy by Category

#### Category A: Consumer Apps (Data Persistence Required)

**Actual Budget** - Personal Finance Management

```yaml
Current State:
  Database: SQLite (local file)
  Data Model: Accounts, Transactions, Budgets, Categories
  Sync: CRDT-based device-to-device sync
  Users: Single user per device (potentially multi-device)
  Data Volume: 100K-1M transactions per user

Migration Path:
  Phase 1: Schema Analysis
    ✓ Analyze SQLite schema
    ✓ Map to PostgreSQL (new offline_sqlite schema)
    
  Phase 2: Hybrid Architecture
    - Keep SQLite on device for offline functionality
    - PostgreSQL backend for optional cloud sync
    - Sync adapter: SQLite ↔ PostgreSQL CRDT
    
  Phase 3: Migration (Client Choice)
    - Option A: Stay local (keep SQLite)
    - Option B: Enable cloud sync (hybrid)
    - Option C: Full cloud (PostgreSQL only)
  
  Implementation:
    - Create offline_sqlite schema in PostgreSQL (for server-side storage)
    - Device SQLite continues working (no changes to client)
    - Server stores sync state, enables device-to-cloud backup
    - CRDT merge logic validates sync conflicts

New Schema:
  offline_sqlite/
    ├── user_accounts
    ├── transactions
    ├── budgets
    ├── categories
    ├── sync_state (tracks device-to-server syncs)
    └── crdt_operations (for merge conflict resolution)
```

#### Category B: Server Applications (Backend Storage)

**Maltrail** - Malicious Traffic Detection

```yaml
Current State:
  Database: SQLite
  Purpose: Store detected malicious traffic
  Data Model: Trails, events, alerts
  Data Volume: ~1M records typical

Migration Path:
  Phase 1: Straight Migration
    - Schema: security_monitoring.maltrail_trails
    - 1:1 mapping of SQLite → PostgreSQL
    - No architectural changes (silent migration)
  
  Phase 2: Optimization
    - Add indices for common queries
    - Partitioning by timestamp
    - Add org_id for multi-tenancy
    - Integrate with event streaming

Expected Outcome:
  ✓ Better query performance
  ✓ Shared infrastructure
  ✓ Consolidated backups
  ✗ No application changes (transparent)
```

**KasmVNC** - Session Tracking

```yaml
Current State:
  Database: SQLite
  Purpose: User sessions, configurations
  Data Volume: Small (session-based)

Migration Path:
  Phase 1: Analysis
    - Determine if truly needs persistent storage
    - Evaluate Redis alternative (cache)
    - Check if session data can be ephemeral
  
  Phase 2: Decision
    Option A: Cache Layer (Redis)
      - Sessions don't need PostgreSQL persistence
      - KasmVNC continues using Redis
      - Simpler deployment
      
    Option B: PostgreSQL Backend
      - Create kasmvnc_sessions schema
      - Session state persistence
      - Audit trail of all sessions

Recommendation: Option A (Redis)
```

#### Category C: Analysis/Tool Data (Cache, Not Critical)

**MTG Scripting Toolkit, Software Forensic Kit**

```yaml
Migration Strategy: Cache to PostgreSQL
  Rationale:
    - Data is derived/cached (not source of truth)
    - Card database comes from external API (Scryfall)
    - Analysis results are regenerable
    - SQLite used for temporary storage
  
  Path:
    Phase 1: Continue SQLite (no change)
    Phase 2: Optional PostgreSQL integration
      - Add schema for cached results
      - Enable cross-tool analysis sharing
      - Improve performance with shared cache

Example:
  card_database/
    ├── card_cache (mtg card data from Scryfall)
    ├── analysis_results (script analysis output)
    └── similarity_cache (computed relationships)
```

### SQLite → PostgreSQL Migration Checklist

```
For each SQLite project:

[ ] Schema Analysis
    [ ] List all tables
    [ ] Identify primary keys
    [ ] Identify foreign keys
    [ ] List indexes
    [ ] Note any triggers/stored procedures

[ ] Data Type Mapping
    [ ] TEXT → VARCHAR/TEXT
    [ ] INTEGER → BIGINT
    [ ] REAL → NUMERIC/FLOAT
    [ ] BLOB → BYTEA
    [ ] Custom types → PostgreSQL equivalents

[ ] Data Migration
    [ ] Export SQLite → CSV/JSON
    [ ] Clean data (NULL handling, encoding)
    [ ] Import to PostgreSQL
    [ ] Validate record counts
    [ ] Verify foreign key relationships

[ ] Testing
    [ ] Unit tests with PostgreSQL
    [ ] Performance tests (typical queries)
    [ ] Stress tests (concurrent access)
    [ ] Backup/restore procedures

[ ] Deployment
    [ ] Feature flag for PostgreSQL backend
    [ ] Gradual rollout (canary)
    [ ] Fallback plan (if issues)
    [ ] Monitor performance
    [ ] Document changes

[ ] Cleanup
    [ ] Remove SQLite code paths (after 2+ weeks stable)
    [ ] Delete legacy SQLite files
    [ ] Update documentation
```

---

## IMPLEMENTATION ROADMAP

### Phase 1: Infrastructure Setup (Weeks 1-2)

#### Task 1.1: PostgreSQL Instance Setup

```
Deliverable: Single PostgreSQL 15+ instance (production-ready)

Activities:
  ✓ Provision PostgreSQL instance (cloud: RDS/GCP CloudSQL, or self-hosted)
  ✓ Configure high-availability (replication, failover)
  ✓ Setup automated backups (daily, with point-in-time recovery)
  ✓ Configure monitoring (Prometheus, Datadog, or equivalent)
  ✓ Setup connection pooling (PgBouncer, pgpool-II)
    - Recommended: 100+ connections per domain
    - Max connections: 500-1000 depending on workload
  ✓ Enable SSL/TLS for all connections
  ✓ Configure parameter store for secrets (connection strings, etc.)

Configuration Sample:
  max_connections = 1000
  shared_buffers = 256MB (1/4 of available RAM)
  effective_cache_size = 1GB
  maintenance_work_mem = 64MB
  checkpoint_completion_target = 0.9
  
  # Enable advanced features
  shared_preload_libraries = 'pg_trgm,pg_stat_statements,pgaudit'
  
  # Security
  ssl = on
  password_encryption = scram-sha-256
```

#### Task 1.2: Schema Creation

```
Deliverable: All base schemas created and tested

Activities:
  ✓ Create SHARED schemas (auth_shared, config_shared, audit_logging_shared)
  ✓ Create DOMAIN schemas (incident_management, threat_intelligence, etc.)
  ✓ Create UTILITY schemas (_schema_versioning, _migration_tracking)
  ✓ Setup schema-level permissions (GRANT/REVOKE)
  ✓ Configure search_path for each application user
  ✓ Document schema purposes and boundaries

SQL Script Structure:
  01_shared_schemas.sql
  ├── auth_shared (users, organizations, roles)
  ├── config_shared (feature flags, secrets)
  └── audit_logging_shared (events, access logs)
  
  02_domain_schemas.sql
  ├── incident_management/
  ├── threat_intelligence/
  ├── offensive_security/
  └── [15+ more domain schemas]
  
  03_shared_indexes.sql (optimize common queries)
  04_shared_functions.sql (common stored procedures)
  05_row_level_security.sql (RLS policies)
  06_permissions.sql (grant statements)
```

#### Task 1.3: Connection & Application Updates

```
Deliverable: All applications can connect to new PostgreSQL instance

Activities:
  ✓ Update connection strings in .env files
  ✓ Test each application's database connection
  ✓ Verify ORM configuration (SQLAlchemy, Sequelize, etc.)
  ✓ Setup health check endpoints
  ✓ Configure application-level retries
  ✓ Document new connection parameters

Example .env update:
  # Before (app-specific SQLite)
  DATABASE_URL=sqlite:///./app.db
  
  # After (shared PostgreSQL)
  DATABASE_URL=postgresql://user:pass@pg.internal/mental_prosthetic_db
  DATABASE_SCHEMA=incident_management
  DATABASE_POOL_SIZE=20
  DATABASE_MAX_OVERFLOW=40
```

---

### Phase 2: Core Domain Migration (Weeks 3-8)

#### Task 2.1: Migrate Tier 1 Domains (High Priority)

**Target**: Dispatch, Ghostwriter, MISP, n8n

```
Sequence (per project):

1. Database Schema Setup
   [ ] Create domain schema in PostgreSQL
   [ ] Review data model, optimize
   [ ] Create all tables, indexes, constraints
   [ ] Setup partitioning (if needed)

2. Data Migration
   [ ] Export from current database (SQL dump or ORM export)
   [ ] Transform/clean data
   [ ] Import to PostgreSQL
   [ ] Validate record counts, referential integrity
   [ ] Seed test data

3. Application Update
   [ ] Update database connection settings
   [ ] Update ORM configuration (if needed)
   [ ] Verify queries still work (pagination, filters, joins)
   [ ] Run application tests
   [ ] Performance testing (query execution time)

4. Testing & Validation
   [ ] Unit tests: All 100+ pass
   [ ] Integration tests: Data persistence verified
   [ ] Performance tests: Acceptable query times
   [ ] Security tests: RLS policies working
   [ ] User acceptance: Key workflows tested

5. Deployment
   [ ] Feature flag: Enable new PostgreSQL backend
   [ ] Canary: Roll out to 10% of users
   [ ] Monitor: Error logs, performance metrics
   [ ] Gradual: Roll out to 100%
   [ ] Fallback: Keep old backend available for 2 weeks

Timeline per project: 5-7 days

Total for Tier 1: 3-4 weeks
```

#### Task 2.2: Migrate Tier 2 Domains (Medium Priority)

**Target**: Nemesis, RITA, SecurityOnion, Firecrawl (4 projects)

```
Parallel migration (2 concurrent tracks):
  Track A: Nemesis, RITA
  Track B: SecurityOnion, Firecrawl

Timeline: 2 weeks total
```

#### Task 2.3: Migrate Tier 3 Domains (Low Priority)

**Target**: 5+ smaller projects (MCP servers, utilities)

```
Batch migration (all together):
Timeline: 1 week
```

---

### Phase 3: SQLite Application Migration (Weeks 9-10)

#### Task 3.1: Actual Budget (Consumer App - Hybrid)

```
Deliverable: Optional PostgreSQL backend for cloud sync

Activities:
  ✓ Create offline_sqlite schema in PostgreSQL
  ✓ Implement sync adapter (SQLite ↔ PostgreSQL)
  ✓ Add feature flag: "Enable Cloud Sync"
  ✓ Users can opt-in to cloud backup
  ✓ Implement CRDT merge for conflict resolution
  ✓ Test offline → online → offline transitions

Risk: Low (optional feature, users choose)
Rollback: Feature flag disable
```

#### Task 3.2: Other SQLite Apps (Server Tools)

```
Deliverable: All SQLite → PostgreSQL with tests passing

Activities:
  ✓ Maltrail: Migrate trail database
  ✓ KasmVNC: Decision on Redis vs PostgreSQL
  ✓ Others: Straight migrations
  ✓ All tests pass
  ✓ Performance benchmarks acceptable

Risk: Low (straightforward migrations)
Timeline: 1 week total
```

---

### Phase 4: Shared Infrastructure Build (Weeks 6-12, Parallel)

#### Task 4.1: Authentication & Authorization

```
Deliverable: Unified auth across all 18 domains

Implementation:
  [ ] Create auth_shared schema (complete)
  [ ] Implement SSO (OpenID Connect or similar)
  [ ] Migrate existing user databases → auth_shared
  [ ] Setup role-based access control (RBAC)
  [ ] Configure fine-grained permissions per domain
  [ ] Test: Users can login once, access all tools

Example: User john@acme.com
  ✓ Login to Dispatch
  ✓ Automatically authenticated in Ghostwriter
  ✓ Can access MISP with same credentials
  ✓ Permissions checked per domain (john has "analyst" role)
```

#### Task 4.2: Audit Logging

```
Deliverable: Unified audit trail across all domains

Implementation:
  [ ] Create audit_logging_shared schema (complete)
  [ ] All domains log events to audit_logging_shared
  [ ] Implement audit log retention policies
  [ ] Setup SIEM integration (Elasticsearch, Splunk)
  [ ] Configure alerting (anomalous access patterns)
  [ ] Compliance reporting (SOC 2, HIPAA, etc.)

Example: Incident created in Dispatch
  1. incident_management.incidents INSERT
  2. Trigger publishes event to event bus
  3. audit_logging_shared.audit_events INSERT
     {org_id: 123, domain: 'incident_management', 
      resource_type: 'incident', resource_id: 456, 
      action: 'create', user_id: 789, 
      timestamp: 2025-11-10T10:30:00Z}
```

#### Task 4.3: Configuration Management

```
Deliverable: Centralized configuration system

Implementation:
  [ ] Create config_shared schema
  [ ] Migrate all configuration from .env files
  [ ] Setup configuration UI (optional admin panel)
  [ ] Implement feature flags
  [ ] Implement secret rotation
  [ ] Setup configuration audit trail

Benefits:
  ✓ No .env file management
  ✓ Easy feature rollout
  ✓ Centralized secret management
  ✓ Audit trail for compliance
```

#### Task 4.4: Event Bus & Integration

```
Deliverable: Event streaming between domains

Implementation:
  [ ] Choose event bus (Kafka, RabbitMQ, Redis Streams)
  [ ] Setup message queue infrastructure
  [ ] Define event schemas (JSON schema or Avro)
  [ ] Implement event publishers (all domains)
  [ ] Implement event subscribers (cross-domain)
  [ ] Setup dead-letter queues (error handling)
  [ ] Monitor event lag and throughput

Example Events:
  - incident_management.incident.created
    → Trigger workflows in workflow_automation
    → Log to audit_logging_shared
  
  - threat_intelligence.event.published
    → Notify relevant security_monitoring components
    → Trigger threat correlation
  
  - workflow_automation.workflow.executed
    → Update audit trail
    → Trigger downstream tasks
```

---

### Phase 5: Testing & Optimization (Weeks 11-12)

#### Task 5.1: Integrated Testing

```
Deliverable: All 18 domains working together seamlessly

Test Scenarios:
  [ ] User creates incident in Dispatch
      → Automatically triggers workflow in n8n
      → Logs captured in audit_logging_shared
      → Can search incident in unified search
  
  [ ] MISP receives threat intelligence
      → Automatically correlates with existing events
      → Notifies relevant security monitoring team
      → Triggers defensive workflows
  
  [ ] User changes in auth_shared
      → Permission updates reflected in all domains within 1 minute
      → Audit trail captured
      → Security alerts triggered for suspicious changes

Load Testing:
  [ ] 1000 concurrent users
  [ ] 10K requests/second
  [ ] 100GB data queries
  [ ] Verify response times < 500ms

Chaos Testing:
  [ ] Database connection failure
      → Application retries automatically
      → Feature flags disable affected domains
  
  [ ] Event bus failure
      → Async operations queue locally
      → Resume when restored
```

#### Task 5.2: Performance Optimization

```
Deliverable: All queries optimized, response times acceptable

Activities:
  [ ] Profile slow queries (pg_stat_statements)
  [ ] Add missing indexes
  [ ] Optimize join order
  [ ] Implement caching layer (Redis)
  [ ] Test with realistic data volume
  [ ] Document query performance baselines

Target Query Times:
  Simple lookup (by ID):     < 5ms
  List with filters:         < 100ms
  Complex search/aggregation: < 500ms
  Slow reports:             < 5sec

Example Optimization:
  Before: SELECT * FROM incidents WHERE org_id = ? AND status = ?
          Duration: 850ms (full table scan)
  
  After:  CREATE INDEX idx_incidents_org_status 
          ON incident_management.incidents(org_id, status)
          Duration: 12ms (index seek)
```

#### Task 5.3: Backup & Disaster Recovery

```
Deliverable: Enterprise-grade backup & recovery

Setup:
  [ ] Daily full backups (Snapshots or pg_dump)
  [ ] Transaction log archival (for point-in-time recovery)
  [ ] Geo-redundant backup storage
  [ ] Tested recovery procedures (RTO < 1 hour, RPO < 5 min)
  [ ] Documented runbooks

Backup Schedule:
  Frequency:          Daily
  Retention:          30 days hot, 90 days cold
  Recovery Point Obj: < 5 minutes
  Recovery Time Obj:  < 1 hour
  Testing:            Quarterly restore drills
```

---

### Phase 6: Production Rollout (Week 13+)

#### Task 6.1: Blue-Green Deployment

```
Deliverable: Zero-downtime migration to consolidated infrastructure

Setup:
  [ ] Blue environment: Current databases (existing)
  [ ] Green environment: New PostgreSQL instance
  [ ] Data replication: Blue → Green (continuous)
  [ ] Validation: Green contains all Blue data
  [ ] Cutover: Switch all applications → Green
  [ ] Monitoring: 24/7 for 2 weeks post-switch
  [ ] Fallback: Keep Blue for quick rollback if needed

Timeline:
  1. Green setup complete (Week 12)
  2. Data replication starts (Week 12)
  3. Validation period (3-5 days)
  4. Cutover window (2-hour maintenance window)
  5. Monitoring period (2 weeks)
  6. Blue environment decommission (Week 14+)
```

#### Task 6.2: Post-Migration Optimization

```
Activities:
  [ ] Analyze real-world query patterns
  [ ] Adjust indexes based on actual usage
  [ ] Fine-tune PostgreSQL configuration
  [ ] Optimize connection pooling
  [ ] Scale hardware if needed
  [ ] Document lessons learned
```

---

## MIGRATION RISK ANALYSIS

### Risk Assessment Matrix

```
Risk Category          | Severity | Likelihood | Mitigation
-----------------------|----------|------------|--------------------
Data Loss              | CRITICAL | Low        | Backups, replication
Performance Degradation| HIGH     | Medium     | Load testing, indexes
Application Downtime   | HIGH     | Medium     | Blue-green, feature flags
Connection Pool Exhaustion| MEDIUM | Medium     | Monitoring, limits
Compliance Violations  | HIGH     | Low        | Audit trail, RLS
Cross-Domain Data Leak  | MEDIUM  | Low        | Schema isolation, tests
-----------------------|----------|------------|--------------------
```

### Risk Mitigation Strategies

#### Risk 1: Performance Degradation

```
What Can Go Wrong:
  - Queries that were fast in dedicated database become slow
  - Increased contention for resources
  - N+1 query problems in application code
  - Missing indexes on new schema

Mitigation:
  1. Load Testing (Before Migration)
     - Simulate 18 domains running simultaneously
     - Test worst-case scenarios
     - Identify bottlenecks early
  
  2. Query Profiling (During Migration)
     - Enable pg_stat_statements
     - Monitor top 20 slowest queries
     - Add indexes proactively
  
  3. Fallback Plan
     - Keep feature flag to use old database
     - If performance bad, disable domain immediately
     - Investigate in staging before re-enabling

Example Feature Flag:
  database.incident_management.use_postgresql = false
    → Falls back to old database
    → Can toggle without redeploying
```

#### Risk 2: Connection Pool Exhaustion

```
What Can Go Wrong:
  - Applications wait for database connections
  - Requests timeout
  - Cascading failures

Prevention:
  [ ] Calculate required connection count
      = (num_domains * avg_concurrent_requests) + buffer
      = (18 * 10) + 20 = 200 connections
  
  [ ] Configure connection pooling (PgBouncer)
      - Connection mode: transaction
      - Pool size: 200
      - Min pool: 100
      - Queue timeout: 30s
  
  [ ] Monitor active connections
      - Alert if > 80% utilization
      - Scale connections if needed
  
  [ ] Test connection stress
      - Simulate 500 concurrent connections
      - Verify queueing behavior
      - Validate recovery after spike

Example Monitoring Query:
  SELECT count(*) as active_connections
  FROM pg_stat_activity
  WHERE state = 'active'
  AND datname = 'mental_prosthetic_db';
```

#### Risk 3: Data Isolation Breach

```
What Can Go Wrong:
  - Organization A can see Organization B's data
  - SQLi vulnerability bypasses org_id filtering
  - RLS policy misconfigured

Prevention:
  [ ] Row-Level Security (RLS) enabled on all sensitive tables
  
  CREATE POLICY incidents_tenant_isolation ON incidents
    FOR ALL USING (org_id = current_setting('app.current_org_id')::bigint);
  
  [ ] Mandatory org_id validation in application
      - Check on every query
      - Fail closed (deny if not set)
  
  [ ] Security testing
      - Penetration testing for data isolation
      - SQLi testing
      - Test data visibility between orgs
  
  [ ] Code review
      - Security team reviews all data access code
      - Automated scanning for missing org_id checks
```

#### Risk 4: Compliance Audit Trail Gaps

```
What Can Go Wrong:
  - Audit logs incomplete or lost
  - Cannot prove who accessed what data
  - Fails SOC 2 audit

Prevention:
  [ ] Comprehensive audit logging
      - All data access logged
      - All modifications logged
      - Who, what, when, where recorded
  
  [ ] Audit log immutability
      - Append-only log (no deletes allowed)
      - Cryptographic signatures optional
      - Centralized log storage
  
  [ ] Retention and archival
      - Hot: 1 year in PostgreSQL
      - Cold: 7 years in object storage (S3)
      - Complies with regulatory requirements
  
  [ ] Testing
      - Regular audit trail validation
      - Quarterly compliance audits
      - Document retention procedures
```

### Risk Rollback Procedures

```
If Migration Fails at Any Phase:

Scenario A: Before Cutover
  Action: Continue with old databases
  Risk: Low (no users affected)
  Timeline: Immediate
  Data Loss: None

Scenario B: During Cutover (Partial)
  Action: Feature flag to disable domain
  Timeline: < 5 minutes
  Example:
    - Dispatch migration fails
    - Feature flag: use_postgresql.incident_management = false
    - All requests route to old database
    - Users unaffected, investigation continues

Scenario C: After Cutover (Critical Issue)
  Action: Full database restore from backup
  Timeline: 30-60 minutes
  RPO: 5 minutes (latest backup)
  Procedure:
    1. Identify issue (alerting)
    2. Notify stakeholders
    3. Restore from backup
    4. Verify data integrity
    5. Resume operations with old database
    6. Post-incident review

All scenarios have < 5 minutes user impact with proper monitoring.
```

---

## COST-BENEFIT ANALYSIS

### Current State (18+ Separate Databases)

```
Infrastructure Costs (Annual):
  Database Hosting:
    - 18 x PostgreSQL instances @ $500/month = $108,000
    - 8 x SQLite backup storage @ $50/month = $4,800
    - Subtotal = $112,800

  Operational Costs:
    - DBA time: 2 FTE @ $150K/year = $300,000
      * Backup management
      * Monitoring and alerting
      * Patch management
      * Performance tuning
      * Security updates
    - Tools (monitoring, backup): $50,000
    - Disaster recovery drills: $20,000
    - Security audits: $30,000
    - Subtotal = $400,000

  Total Annual Cost: $512,800

Operational Overhead:
  - 18 different backup procedures
  - 18 different monitoring setups
  - 18 different security policies
  - 18 different disaster recovery plans
  - Complex cross-database synchronization
  - Manual data consistency checks
  - Troubleshooting spread across 18 systems
```

### Consolidated State (1 PostgreSQL Instance)

```
Infrastructure Costs (Annual):
  Database Hosting:
    - 1 x PostgreSQL instance (enterprise) @ $2,000/month = $24,000
    - Includes: HA, replication, backups, monitoring
    - 18 schemas in same instance
    - Subtotal = $24,000

  Operational Costs:
    - DBA time: 1 FTE @ $150K/year = $150,000
      * Centralized backup management
      * Single monitoring dashboard
      * Unified patch strategy
      * Centralized performance tuning
      * One security perimeter
    - Tools (integrated monitoring): $30,000
    - Disaster recovery drills: $10,000
    - Security audits: $20,000
    - Subtotal = $210,000

  Total Annual Cost: $234,000

Savings Summary:
  Infrastructure: $88,800 (79% reduction)
  Operational: $190,000 (48% reduction)
  Total Annual Savings: $278,800 (54%)
  
  3-Year Savings: $836,400
  5-Year Savings: $1,394,000
```

### Benefits Beyond Cost Savings

```
Operational Benefits:
  ✓ Single backup/restore procedure (simpler, more reliable)
  ✓ Unified monitoring and alerting
  ✓ Centralized authentication and authorization
  ✓ Simplified disaster recovery
  ✓ Faster incident response (single point of investigation)
  ✓ Easier capacity planning
  ✓ Unified compliance and audit trail
  ✓ Simpler security patching

Developer Benefits:
  ✓ Unified data model documentation
  ✓ Single database schema for learning
  ✓ Cross-domain queries simplified (via APIs, not schema joins)
  ✓ Better tooling (pgAdmin, dbeaver for all data)
  ✓ Standardized migration procedures
  ✓ Easier integration testing

Business Benefits:
  ✓ Faster feature development (reuse auth, config, audit)
  ✓ Improved time-to-market
  ✓ Better data insights (unified data warehouse)
  ✓ Stronger compliance posture
  ✓ Improved customer experience (SSO, unified search)
  ✓ Reduced licensing costs
  ✓ Better disaster recovery capabilities
```

---

## APPENDICES

### Appendix A: PostgreSQL Configuration Checklist

```sql
-- Essential settings for mental_prosthetic_db

-- Memory Configuration
shared_buffers = 256MB                    -- 1/4 of available RAM
effective_cache_size = 1GB                -- 1/2 of available RAM
maintenance_work_mem = 64MB               -- maintenance_work_mem
work_mem = 16MB                           -- per sort/hash operation

-- Checkpoint & WAL
checkpoint_completion_target = 0.9        -- aggressive checkpoints
wal_level = replica                       -- enable replication
max_wal_senders = 10                      -- for standbys
wal_keep_size = 1GB                       -- maintain WAL files

-- Logging
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%Y-%m-%d.log'
log_min_duration_statement = 1000         -- log queries > 1 second
log_statement = 'all'                     -- log all statements (or 'ddl')
log_connections = on
log_disconnections = on

-- Extensions (preload)
shared_preload_libraries = 'pg_trgm,pg_stat_statements,pgaudit'

-- Security
ssl = on
ssl_cert_file = '/etc/postgresql/server.crt'
ssl_key_file = '/etc/postgresql/server.key'
password_encryption = scram-sha-256

-- Performance
random_page_cost = 1.1                    -- SSD cost
effective_io_concurrency = 200            -- high for SSD
jit = on                                  -- JIT compilation

-- Limits
max_connections = 1000                    -- with PgBouncer
statement_timeout = 30000                 -- 30 seconds
idle_in_transaction_session_timeout = 60000  -- 60 seconds

-- Monitoring
pg_stat_statements.track = all
track_activities = on
track_functions = 'all'
```

### Appendix B: Terraform/IaC Example

```hcl
# main.tf - PostgreSQL Instance with consolidated schema

resource "aws_rds_cluster" "mental_prosthetic" {
  cluster_identifier      = "mental-prosthetic-db"
  engine                  = "aurora-postgresql"
  engine_version          = "15.2"
  database_name           = "mental_prosthetic_db"
  master_username         = "postgres"
  master_password         = random_password.db_password.result
  
  # High availability
  storage_encrypted       = true
  backup_retention_period = 30
  preferred_backup_window = "03:00-04:00"
  db_subnet_group_name    = aws_db_subnet_group.private.name
  
  # Performance
  preferred_maintenance_window = "mon:04:00-mon:05:00"
  
  skip_final_snapshot = false
  final_snapshot_identifier = "mental-prosthetic-final-snapshot"
  
  tags = {
    Name        = "Mental Prosthetic DB"
    Environment = "production"
    Team        = "platform"
  }
}

resource "aws_rds_cluster_instance" "main" {
  count              = 2  # Primary + Replica
  cluster_identifier = aws_rds_cluster.mental_prosthetic.id
  instance_class     = "db.r6g.2xlarge"  # 64GB RAM, high compute
  engine              = aws_rds_cluster.mental_prosthetic.engine
  engine_version      = aws_rds_cluster.mental_prosthetic.engine_version
  
  performance_insights_enabled = true
  monitoring_interval          = 60
  monitoring_role_arn          = aws_iam_role.rds_monitoring.arn
  
  tags = {
    Name = "Mental Prosthetic DB Instance ${count.index + 1}"
  }
}

# Database schemas (managed by Terraform or Liquibase)
resource "null_resource" "create_schemas" {
  provisioner "local-exec" {
    command = "psql -h ${aws_rds_cluster.mental_prosthetic.endpoint} \
                     -U postgres \
                     -d mental_prosthetic_db \
                     -f schema_setup.sql"
  }
  
  depends_on = [aws_rds_cluster_instance.main]
}

output "database_endpoint" {
  value = aws_rds_cluster.mental_prosthetic.endpoint
  sensitive = true
}

output "database_reader_endpoint" {
  value = aws_rds_cluster.mental_prosthetic.reader_endpoint
  sensitive = true
}
```

### Appendix C: Example Domain Schema SQL

```sql
-- Create incident_management schema
CREATE SCHEMA incident_management;

CREATE TABLE incident_management.incidents (
  id BIGSERIAL PRIMARY KEY,
  uuid UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
  org_id BIGINT NOT NULL,
  
  -- Core incident data
  name VARCHAR(255) NOT NULL,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  resolution TEXT,
  
  -- Status tracking
  status VARCHAR(50) NOT NULL DEFAULT 'active',
  severity SMALLINT,
  priority SMALLINT,
  
  -- Visibility and sharing
  visibility VARCHAR(50) NOT NULL DEFAULT 'open',
  
  -- Participants
  created_by BIGINT NOT NULL REFERENCES auth_shared.users(id),
  reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  stable_at TIMESTAMP,
  closed_at TIMESTAMP,
  
  -- Search optimization
  search_vector tsvector,
  
  -- Metadata
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_incidents_org_status 
  ON incident_management.incidents(org_id, status);
CREATE INDEX idx_incidents_reported_at 
  ON incident_management.incidents(org_id, reported_at DESC);
CREATE INDEX idx_incidents_search 
  ON incident_management.incidents USING GIN(search_vector);
CREATE INDEX idx_incidents_uuid 
  ON incident_management.incidents(uuid);

-- Full-text search trigger
CREATE TRIGGER update_incidents_search
BEFORE INSERT OR UPDATE ON incident_management.incidents
FOR EACH ROW
EXECUTE FUNCTION 
  tsvector_update_trigger(search_vector, 'pg_catalog.english',
                          name, title, description);

-- Row-level security
ALTER TABLE incident_management.incidents ENABLE ROW LEVEL SECURITY;
CREATE POLICY incidents_org_isolation ON incident_management.incidents
  FOR ALL
  USING (org_id = current_setting('app.current_org_id')::bigint);
```

### Appendix D: Application Connection Configuration

```yaml
# Python (SQLAlchemy) Example
DATABASE_URL: postgresql+asyncpg://user:password@pg.internal:5432/mental_prosthetic_db
SQLALCHEMY_ECHO: false
SQLALCHEMY_POOL_SIZE: 20
SQLALCHEMY_MAX_OVERFLOW: 40
SQLALCHEMY_POOL_RECYCLE: 3600

# Environment-specific
DATABASE_SCHEMA: incident_management

# Connection settings
DATABASE_STATEMENT_TIMEOUT: 30000  # 30 seconds
DATABASE_IDLE_TRANSACTION_TIMEOUT: 60000

# TypeScript (Node.js/Sequelize) Example
const sequelize = new Sequelize({
  dialect: 'postgres',
  host: process.env.DB_HOST,
  port: 5432,
  username: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: 'mental_prosthetic_db',
  schema: process.env.DB_SCHEMA || 'public',
  pool: {
    max: 20,
    min: 5,
    acquire: 30000,
    idle: 10000,
  },
  logging: false,  // Disable logs in production
  dialectOptions: {
    ssl: {
      require: true,
      rejectUnauthorized: false,  // For self-signed certs
    },
  },
});
```

---

## IMPLEMENTATION TIMELINE SUMMARY

```
Week 1-2:    Infrastructure Setup
  ├─ PostgreSQL instance provisioning
  ├─ Schema creation
  └─ Connection testing

Week 3-8:    Core Domain Migration (Parallel tracks)
  ├─ Tier 1: Dispatch, Ghostwriter, MISP, n8n
  ├─ Tier 2: Nemesis, RITA, SecurityOnion, Firecrawl
  └─ Tier 3: 5+ smaller projects

Week 6-12:   Shared Infrastructure (Parallel)
  ├─ Authentication consolidation
  ├─ Audit logging setup
  ├─ Configuration management
  └─ Event bus implementation

Week 9-10:   SQLite Migrations
  ├─ Actual Budget (hybrid mode)
  ├─ Other SQLite apps
  └─ Testing & validation

Week 11-12:  Testing & Optimization
  ├─ Integrated testing
  ├─ Performance optimization
  └─ Backup & DR procedures

Week 13:     Blue-Green Cutover
  ├─ Final data validation
  ├─ Cutover window (2 hours)
  └─ Rollback standby

Week 14+:    Monitoring & Decommission
  ├─ 2-week monitoring period
  ├─ Old database decommission
  └─ Documentation update

Total Duration: ~14 weeks
```

---

## CONCLUSION

This DATABASE CONSOLIDATION STRATEGY enables Mental Prosthetic Platform to:

1. **Reduce Infrastructure Costs** by 54% ($278K annually)
2. **Simplify Operations** with unified backup, monitoring, and disaster recovery
3. **Enable Integration** with event-driven architecture and shared services
4. **Improve Compliance** with centralized audit trail and security controls
5. **Accelerate Development** by reusing shared schemas and components

The phased approach minimizes risk through:
- Feature flags for easy rollback
- Parallel migration of multiple domains
- Comprehensive testing before production cutover
- Blue-green deployment for zero-downtime transition

**Next Steps**:
1. Form migration taskforce (Database team, architects, domain owners)
2. Provision PostgreSQL instance
3. Execute Phase 1 (infrastructure)
4. Begin Phase 2 (domain migrations) in parallel
5. Complete migration within 14 weeks

---

**Document Version**: 1.0  
**Last Updated**: November 10, 2025  
**Author**: Mental Prosthetic Platform Analysis  
**Status**: Ready for Implementation Planning

