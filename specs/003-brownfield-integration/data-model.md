# Data Model: Brownfield Integration - Mental Prosthetic Platform

**Branch**: `003-brownfield-integration` | **Date**: 2025-11-03 | **Phase**: 1 - Design
**Input**: Research findings from Phase 0 research.md
**Context**: Unified data architecture for 37-tool consolidation with business logic preservation

## Data Model Overview

This data model consolidates 37 executive function tools into a unified modular monolith while preserving existing business logic and maintaining domain boundaries. The architecture supports mixed storage patterns (PostgreSQL, SQLite, Elasticsearch) with federated identity and cross-domain data synchronization.

## 1. Core Architecture Principles

### 1.1 Domain-Driven Data Design

```yaml
Data Architecture Strategy:
  Primary Pattern: Domain-separated schemas within unified PostgreSQL
  Local-First Pattern: SQLite preservation for offline tools with CRDT sync
  Search Pattern: Elasticsearch consolidation for security and search workloads
  Identity Pattern: Federated authentication with tool-specific permission mapping

Runtime Environment Strategy (Evidence-Based Optimization):
  Investigation Results: "Version requirement analysis revealed 60% legacy constraints vs 40% legitimate requirements"
  Optimization: "Reduced container complexity from 11 to 7 runtime versions (36% reduction)"
  
  Standard Runtime Environment:
    - Node 20 LTS: 60% of JavaScript/TypeScript tools (CyberChef, IT-Tools, Actual, Commander Spellbook)
    - Python 3.12: 60% of Python tools (Firecrawl SDK, Goose MCP Wiki, n8n Task Runner)
    - Rationale: "Evidence analysis showed no functional dependencies on higher/lower versions"
    
  Version-Specific Containers (Legitimate Requirements Only):
    - Inspector Tool: Node 22.7.5+ (ES Modules import.meta.url usage verified)
    - Goose Desktop: Node 22.17.1 (Electron native module compatibility verified)
    - YARA-X Python: 3.9+ (PyO3 Rust bindings requirement verified)
    - Dispatch: Python 3.11+ (pending verification of exception groups usage)
    
  Reference: "../analysis/version-requirement-legitimacy.md" for detailed investigation
  
DDD Integration Patterns:
  Module Boundaries: Strict async-only communication between domains
  Rich Domain Models: Business logic encapsulation within aggregate roots
  Event Sourcing: Outbox/Inbox pattern for cross-domain reliability
  Command Processing: Decorator pattern for cross-cutting concerns
  Architecture Testing: Automated boundary compliance validation
```

### 1.2 Data Preservation Categories

**Category A (Complex Algorithms)**: Maintain original data structures with domain model encapsulation

- Implementation: Rich domain objects with factory methods preserving business rules
- Example: YARA-X pattern matching, MISP threat correlation algorithms
- DDD Pattern: Aggregate roots with encapsulated complex behavior

**Category B (Domain Logic)**: Schema modernization within PostgreSQL with business logic preservation

- Implementation: Domain services with command/query separation
- Example: Productivity workflows, TCG deck analysis, security tool orchestration
- DDD Pattern: Domain services with decorator-based cross-cutting concerns

**Category C (Utilities)**: Standardized configuration and user data models

- Implementation: Shared kernel patterns with unified interfaces
- Example: User preferences, audit logging, system configuration
- DDD Pattern: Shared infrastructure with anti-corruption layers

## 2. Unified Database Schema Architecture

### 2.1 PostgreSQL Domain Schemas

```sql
-- Core platform schemas
CREATE SCHEMA core;           -- Shared services (users, audit, config)
CREATE SCHEMA security;       -- 13 security tools consolidation
CREATE SCHEMA productivity;   -- 8 productivity tools consolidation  
CREATE SCHEMA tcg;           -- 4 TCG tools consolidation
CREATE SCHEMA infrastructure; -- 12 infrastructure tools consolidation

-- Cross-cutting schemas
CREATE SCHEMA auth;          -- Federated identity and permissions
CREATE SCHEMA events;        -- Domain event sourcing
CREATE SCHEMA sync;          -- Cross-domain data synchronization
```

### 2.2 Cross-Domain Shared Entities

#### Core Identity Management

```sql
-- Core schema: Unified user management
CREATE TABLE core.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(255),
    
    -- Executive function accommodations
    ui_preferences JSONB DEFAULT '{}', -- Focus indicators, response times
    accessibility_settings JSONB DEFAULT '{}', -- WCAG 2.1 AA+ settings
    
    -- Authentication
    password_hash VARCHAR(255), -- Optional for SSO-only users
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMP WITH TIME ZONE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES core.users(id),
    updated_by UUID REFERENCES core.users(id)
);

-- Core schema: Organization structure for multi-tenancy
CREATE TABLE core.organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    settings JSONB DEFAULT '{}', -- Org-wide configurations
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Core schema: User-organization relationships
CREATE TABLE core.user_organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES core.users(id) ON DELETE CASCADE,
    organization_id UUID NOT NULL REFERENCES core.organizations(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- admin, member, viewer
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, organization_id)
);
```

#### Audit and Event Sourcing

```sql
-- Core schema: Comprehensive audit trail
CREATE TABLE core.audit_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event identification
    event_type VARCHAR(100) NOT NULL, -- user.created, tool.migrated, etc.
    aggregate_type VARCHAR(100) NOT NULL, -- user, security_tool, productivity_task
    aggregate_id VARCHAR(255) NOT NULL,
    
    -- Event data
    event_data JSONB NOT NULL, -- Complete event payload
    metadata JSONB DEFAULT '{}', -- Request ID, IP, user agent, etc.
    
    -- Context
    user_id UUID REFERENCES core.users(id),
    organization_id UUID REFERENCES core.organizations(id),
    domain VARCHAR(50), -- security, productivity, tcg, infrastructure
    
    -- Timing
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexing for performance
    INDEX idx_audit_events_aggregate (aggregate_type, aggregate_id),
    INDEX idx_audit_events_user (user_id, occurred_at),
    INDEX idx_audit_events_domain (domain, occurred_at)
);
```

### 2.3 Domain-Specific Data Models

#### Security Domain Schema (13 Tools)

```sql
-- Security schema: Threat intelligence consolidation (MISP, MalwareBazaar, etc.)
CREATE TABLE security.threat_indicators (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Indicator data
    type VARCHAR(50) NOT NULL, -- hash, domain, ip, url, yara_rule
    value TEXT NOT NULL,
    confidence_score INTEGER CHECK (confidence_score >= 0 AND confidence_score <= 100),
    
    -- Source tool preservation
    source_tool VARCHAR(100) NOT NULL, -- misp, malware_bazaar, virustotal
    source_id VARCHAR(255), -- Original tool's identifier
    source_data JSONB, -- Complete original data for Category A preservation
    
    -- Classification
    threat_types TEXT[] DEFAULT '{}', -- malware, phishing, apt, etc.
    tags TEXT[] DEFAULT '{}',
    tlp_level VARCHAR(20) DEFAULT 'white', -- Traffic Light Protocol
    
    -- Relationships
    related_indicators UUID[] DEFAULT '{}', -- References to other indicators
    campaigns TEXT[] DEFAULT '{}',
    
    -- Temporal data
    first_seen TIMESTAMP WITH TIME ZONE,
    last_seen TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    
    -- Audit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES core.users(id),
    
    -- Indexing for <1s performance requirement
    INDEX idx_threat_indicators_type_value (type, value),
    INDEX idx_threat_indicators_source (source_tool, source_id),
    INDEX idx_threat_indicators_tags USING gin(tags),
    INDEX idx_threat_indicators_temporal (first_seen, last_seen)
);

-- Security schema: YARA rule management
CREATE TABLE security.yara_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Rule data
    name VARCHAR(255) NOT NULL,
    rule_text TEXT NOT NULL, -- Complete YARA rule
    description TEXT,
    
    -- Metadata
    author VARCHAR(255),
    version VARCHAR(50),
    rule_hash VARCHAR(64) UNIQUE, -- SHA-256 of rule_text
    
    -- Performance tracking
    match_count INTEGER DEFAULT 0,
    false_positive_count INTEGER DEFAULT 0,
    last_match_at TIMESTAMP WITH TIME ZONE,
    
    -- Categories and tags
    categories TEXT[] DEFAULT '{}', -- malware_family, apt_group, etc.
    severity VARCHAR(20) DEFAULT 'medium', -- low, medium, high, critical
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_validated BOOLEAN DEFAULT false,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES core.users(id),
    
    INDEX idx_yara_rules_active (is_active, severity),
    INDEX idx_yara_rules_categories USING gin(categories)
);

-- Security schema: Network monitoring events (SecurityOnion, HELK)
CREATE TABLE security.network_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event identification
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    source_ip INET,
    destination_ip INET,
    source_port INTEGER,
    destination_port INTEGER,
    protocol VARCHAR(20),
    
    -- Event data
    event_type VARCHAR(100) NOT NULL, -- alert, connection, dns, http
    severity VARCHAR(20) DEFAULT 'info',
    signature_id INTEGER,
    signature VARCHAR(500),
    
    -- Raw data preservation
    raw_event JSONB, -- Complete original event for Category A preservation
    source_tool VARCHAR(100) NOT NULL, -- security_onion, helk, suricata
    
    -- Analysis results
    is_malicious BOOLEAN,
    risk_score INTEGER CHECK (risk_score >= 0 AND risk_score <= 100),
    analysis_results JSONB DEFAULT '{}',
    
    -- Relationships
    related_indicators UUID[] DEFAULT '{}',
    incident_id UUID, -- Link to incident management
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Performance indexes for security analysis
    INDEX idx_network_events_timestamp (event_timestamp),
    INDEX idx_network_events_ips (source_ip, destination_ip),
    INDEX idx_network_events_severity (severity, event_timestamp),
    INDEX idx_network_events_source (source_tool, event_type)
);
```

#### Productivity Domain Schema (8 Tools)

```sql
-- Productivity schema: Task and project management (n8n, Dispatch, etc.)
CREATE TABLE productivity.projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Project data
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active', -- active, completed, archived, on_hold
    
    -- Organization
    organization_id UUID REFERENCES core.organizations(id),
    team_id UUID, -- Reference to team management
    
    -- Workflow integration (n8n workflows)
    workflow_configs JSONB DEFAULT '{}', -- n8n workflow mappings
    automation_rules JSONB DEFAULT '{}',
    
    -- Dates and scheduling
    start_date DATE,
    end_date DATE,
    estimated_hours INTEGER,
    actual_hours INTEGER DEFAULT 0,
    
    -- Settings
    settings JSONB DEFAULT '{}', -- Project-specific configurations
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES core.users(id),
    
    INDEX idx_projects_org_status (organization_id, status),
    INDEX idx_projects_dates (start_date, end_date)
);

-- Productivity schema: Task management with executive function support
CREATE TABLE productivity.tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Task data
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'todo', -- todo, in_progress, blocked, completed
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, urgent
    
    -- Relationships
    project_id UUID REFERENCES productivity.projects(id) ON DELETE CASCADE,
    parent_task_id UUID REFERENCES productivity.tasks(id),
    assigned_to UUID REFERENCES core.users(id),
    
    -- Executive function accommodations
    estimated_duration INTERVAL, -- Time estimates for task planning
    actual_duration INTERVAL,
    break_reminders BOOLEAN DEFAULT false, -- ADHD accommodation
    focus_mode_enabled BOOLEAN DEFAULT false,
    
    -- Workflow automation
    workflow_triggers JSONB DEFAULT '{}', -- n8n automation triggers
    notification_settings JSONB DEFAULT '{}',
    
    -- Temporal data
    due_date TIMESTAMP WITH TIME ZONE,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_tasks_assigned (assigned_to, status, due_date),
    INDEX idx_tasks_project (project_id, status),
    INDEX idx_tasks_priority (priority, due_date)
);

-- Productivity schema: Recipe management (Mealie integration)
CREATE TABLE productivity.recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Recipe data
    name VARCHAR(255) NOT NULL,
    description TEXT,
    instructions TEXT,
    prep_time INTERVAL,
    cook_time INTERVAL,
    total_time INTERVAL,
    servings INTEGER,
    
    -- Categories and tags
    category VARCHAR(100), -- breakfast, lunch, dinner, snack, dessert
    cuisine VARCHAR(100),
    tags TEXT[] DEFAULT '{}',
    dietary_restrictions TEXT[] DEFAULT '{}', -- vegetarian, vegan, gluten_free
    
    -- Source data preservation (Mealie)
    original_url VARCHAR(500),
    source_data JSONB, -- Complete Mealie recipe data
    
    -- User data
    owner_id UUID REFERENCES core.users(id),
    is_public BOOLEAN DEFAULT false,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_recipes_owner (owner_id, category),
    INDEX idx_recipes_tags USING gin(tags),
    INDEX idx_recipes_dietary USING gin(dietary_restrictions)
);

-- Productivity schema: Ingredients and shopping integration
CREATE TABLE productivity.ingredients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Ingredient data
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100), -- produce, dairy, meat, pantry, etc.
    unit VARCHAR(50), -- cup, pound, piece, etc.
    
    -- Nutrition data (optional)
    calories_per_unit DECIMAL(8,2),
    nutrition_data JSONB DEFAULT '{}',
    
    -- Shopping integration
    typical_price DECIMAL(10,2),
    preferred_brand VARCHAR(255),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_ingredients_name (name),
    INDEX idx_ingredients_category (category)
);
```

#### TCG Domain Schema (4 Tools)

```sql
-- TCG schema: Card database (Commander Spellbook, TCG Scripting Toolkit)
CREATE TABLE tcg.cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Card identification
    name VARCHAR(255) NOT NULL,
    mana_cost VARCHAR(100),
    converted_mana_cost INTEGER DEFAULT 0,
    type_line VARCHAR(255),
    oracle_text TEXT,
    
    -- Card attributes
    power VARCHAR(10), -- Can be *, X, etc.
    toughness VARCHAR(10),
    loyalty VARCHAR(10), -- For planeswalkers
    colors TEXT[] DEFAULT '{}', -- W, U, B, R, G
    color_identity TEXT[] DEFAULT '{}',
    
    -- Set information
    set_code VARCHAR(10),
    set_name VARCHAR(255),
    collector_number VARCHAR(20),
    rarity VARCHAR(20), -- common, uncommon, rare, mythic
    
    -- Legality
    legalities JSONB DEFAULT '{}', -- Format: legal/banned/restricted status
    
    -- External data integration
    scryfall_id UUID, -- Scryfall API integration
    edhrec_rank INTEGER, -- EDHREC popularity ranking
    price_data JSONB DEFAULT '{}', -- Current market prices
    
    -- Source tool preservation
    source_data JSONB DEFAULT '{}', -- Complete card data from tools
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Performance indexes for <3s TCG analysis requirement
    INDEX idx_cards_name (name),
    INDEX idx_cards_colors USING gin(colors),
    INDEX idx_cards_color_identity USING gin(color_identity),
    INDEX idx_cards_legalities USING gin(legalities),
    INDEX idx_cards_set (set_code, collector_number)
);

-- TCG schema: Combo database (Commander Spellbook)
CREATE TABLE tcg.combos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Combo data
    name VARCHAR(255),
    description TEXT,
    steps TEXT[], -- Array of combo steps
    results TEXT[], -- What the combo achieves
    
    -- Requirements
    required_cards UUID[] NOT NULL, -- References to tcg.cards
    required_mana VARCHAR(100), -- Total mana cost
    required_setup TEXT[], -- Additional requirements
    
    -- Metadata
    difficulty VARCHAR(20) DEFAULT 'medium', -- easy, medium, hard, jank
    popularity_score INTEGER DEFAULT 0,
    competitive_viability VARCHAR(20) DEFAULT 'casual',
    
    -- Categories
    combo_types TEXT[] DEFAULT '{}', -- infinite_mana, infinite_damage, etc.
    formats TEXT[] DEFAULT '{}', -- commander, legacy, vintage, etc.
    
    -- Community data
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    featured BOOLEAN DEFAULT false,
    
    -- Source preservation
    spellbook_id VARCHAR(255), -- Original Commander Spellbook ID
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES core.users(id),
    
    INDEX idx_combos_cards USING gin(required_cards),
    INDEX idx_combos_types USING gin(combo_types),
    INDEX idx_combos_formats USING gin(formats),
    INDEX idx_combos_popularity (popularity_score DESC)
);

-- TCG schema: Deck management and analysis
CREATE TABLE tcg.decks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Deck data
    name VARCHAR(255) NOT NULL,
    description TEXT,
    format VARCHAR(50) NOT NULL, -- commander, standard, modern, etc.
    
    -- Commander-specific
    commander_id UUID REFERENCES tcg.cards(id),
    partner_commander_id UUID REFERENCES tcg.cards(id),
    color_identity TEXT[] DEFAULT '{}',
    
    -- Deck composition (stored as JSONB for flexibility)
    decklist JSONB NOT NULL, -- {card_id: quantity} mapping
    sideboard JSONB DEFAULT '{}',
    maybeboard JSONB DEFAULT '{}',
    
    -- Analysis results
    curve_analysis JSONB DEFAULT '{}', -- Mana curve data
    strategy_tags TEXT[] DEFAULT '{}', -- aggro, control, combo, etc.
    power_level INTEGER CHECK (power_level >= 1 AND power_level <= 10),
    
    -- Ownership
    owner_id UUID REFERENCES core.users(id),
    is_public BOOLEAN DEFAULT false,
    
    -- Versioning
    version INTEGER DEFAULT 1,
    parent_deck_id UUID REFERENCES tcg.decks(id), -- For deck forks/versions
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_decks_owner (owner_id, format),
    INDEX idx_decks_format (format, power_level),
    INDEX idx_decks_commander (commander_id),
    INDEX idx_decks_color_identity USING gin(color_identity)
);
```

#### Infrastructure Domain Schema (12 Tools)

```sql
-- Infrastructure schema: Service monitoring and management
CREATE TABLE infrastructure.services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Service identification
    name VARCHAR(255) NOT NULL,
    description TEXT,
    service_type VARCHAR(100), -- web, api, database, cache, queue
    
    -- Configuration
    config JSONB DEFAULT '{}', -- Service-specific configuration
    environment VARCHAR(50) DEFAULT 'production', -- dev, staging, production
    
    -- Networking
    internal_url VARCHAR(500),
    external_url VARCHAR(500),
    health_check_url VARCHAR(500),
    
    -- Status
    status VARCHAR(50) DEFAULT 'unknown', -- healthy, degraded, down, maintenance
    last_health_check TIMESTAMP WITH TIME ZONE,
    uptime_percentage DECIMAL(5,2), -- 99.99%
    
    -- Resource requirements
    cpu_limit VARCHAR(20), -- 1000m, 2 cores, etc.
    memory_limit VARCHAR(20), -- 512Mi, 2Gi, etc.
    storage_requirements JSONB DEFAULT '{}',
    
    -- Tool integration
    kong_service_id VARCHAR(255), -- Kong API Gateway integration
    monitoring_configs JSONB DEFAULT '{}', -- Monitoring tool configurations
    
    -- Relationships
    depends_on UUID[] DEFAULT '{}', -- Service dependencies
    organization_id UUID REFERENCES core.organizations(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES core.users(id),
    
    INDEX idx_services_status (status, last_health_check),
    INDEX idx_services_org (organization_id, service_type),
    INDEX idx_services_dependencies USING gin(depends_on)
);

-- Infrastructure schema: IT tool configurations and utilities
CREATE TABLE infrastructure.tool_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Tool identification
    tool_name VARCHAR(255) NOT NULL, -- it-tools, kong, kasmnvnc, etc.
    instance_name VARCHAR(255), -- For multiple instances of same tool
    
    -- Configuration data
    config_data JSONB NOT NULL, -- Complete tool configuration
    config_schema_version VARCHAR(20), -- For migration management
    
    -- Access control
    owner_id UUID REFERENCES core.users(id),
    shared_with UUID[] DEFAULT '{}', -- User IDs with access
    access_level VARCHAR(50) DEFAULT 'private', -- private, team, organization, public
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    last_validated TIMESTAMP WITH TIME ZONE,
    validation_errors TEXT[],
    
    -- Versioning
    version INTEGER DEFAULT 1,
    previous_version_id UUID REFERENCES infrastructure.tool_configurations(id),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_tool_configs_tool (tool_name, is_active),
    INDEX idx_tool_configs_owner (owner_id, access_level),
    INDEX idx_tool_configs_shared USING gin(shared_with)
);
```

## 3. Local-First Data Architecture (SQLite Integration)

### 3.1 SQLite Preservation Strategy

```yaml
SQLite Tools Requiring Local-First Architecture:
  - Actual Budget: Local financial data with cloud sync
  - Mealie: Recipe storage with offline access  
  - Personal task management: Executive function support
  - User preferences: UI/UX customization data
  - Cached data: Performance optimization
```

### 3.2 SQLite Schema Design

```sql
-- Local SQLite database per user/organization
-- File naming: {user_id}_{org_id}.db

-- Local user preferences and settings
CREATE TABLE user_preferences (
    id TEXT PRIMARY KEY,
    
    -- UI/UX preferences
    theme VARCHAR(50) DEFAULT 'system',
    font_size VARCHAR(20) DEFAULT 'medium',
    reduced_motion BOOLEAN DEFAULT false,
    high_contrast BOOLEAN DEFAULT false,
    
    -- Executive function accommodations
    break_reminder_interval INTEGER DEFAULT 1800, -- 30 minutes
    focus_session_duration INTEGER DEFAULT 1500, -- 25 minutes (Pomodoro)
    auto_save_frequency INTEGER DEFAULT 30, -- seconds
    
    -- Performance preferences
    animation_speed VARCHAR(20) DEFAULT 'normal',
    data_refresh_rate INTEGER DEFAULT 300, -- 5 minutes
    offline_mode_enabled BOOLEAN DEFAULT true,
    
    -- Sync metadata
    last_synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sync_version INTEGER DEFAULT 1,
    
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Local task cache for offline productivity
CREATE TABLE local_tasks (
    id TEXT PRIMARY KEY,
    
    -- Task data (mirrors productivity.tasks)
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'todo',
    priority TEXT DEFAULT 'medium',
    
    -- Local-specific fields
    is_offline_created BOOLEAN DEFAULT false,
    local_modifications JSONB DEFAULT '{}',
    conflict_resolution TEXT, -- For CRDT conflict handling
    
    -- Sync metadata
    server_id TEXT, -- UUID from PostgreSQL
    last_synced_at TIMESTAMP,
    sync_status TEXT DEFAULT 'pending', -- pending, synced, conflict
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Local cache for frequently accessed data
CREATE TABLE data_cache (
    cache_key TEXT PRIMARY KEY,
    
    -- Cache data
    data_type TEXT NOT NULL, -- cards, recipes, threat_indicators
    data_content JSONB NOT NULL,
    
    -- Cache metadata
    expires_at TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 3.3 CRDT (Conflict-free Replicated Data Types) Implementation

```yaml
CRDT Strategy for Offline-First Tools:
  Data Types:
    - G-Counter: View counts, usage statistics
    - PN-Counter: Ratings, scores (can be negative)
    - LWW-Register: Last-Writer-Wins for simple fields
    - OR-Set: Tags, categories (add/remove operations)
    
  Sync Algorithm:
    1. Local SQLite changes tracked with vector clocks
    2. Periodic sync with PostgreSQL authoritative source
    3. Conflict resolution using CRDT semantics
    4. Merge results written to both local and remote stores
```

## 4. Elasticsearch Integration Architecture

### 4.1 Search and Analytics Indexes

```yaml
Elasticsearch Index Strategy:
  Security Indexes:
    - security-events-*: Network events, alerts, logs
    - threat-intelligence-*: IOCs, YARA rules, signatures
    - malware-samples-*: File hashes, analysis results
    
  Infrastructure Indexes:
    - service-logs-*: Application logs, metrics
    - monitoring-data-*: Performance metrics, health checks
    
  Cross-Domain Indexes:
    - audit-trail-*: User actions, system changes
    - search-index-*: Global search across all domains
```

### 4.2 Document Mapping Templates

```json
{
  "template": {
    "mappings": {
      "properties": {
        "@timestamp": {
          "type": "date"
        },
        "domain": {
          "type": "keyword"
        },
        "event_type": {
          "type": "keyword"
        },
        "severity": {
          "type": "keyword"
        },
        "user_id": {
          "type": "keyword"
        },
        "organization_id": {
          "type": "keyword"
        },
        "data": {
          "type": "object",
          "dynamic": true
        },
        "tags": {
          "type": "keyword"
        },
        "full_text": {
          "type": "text",
          "analyzer": "standard"
        }
      }
    },
    "settings": {
      "number_of_shards": 3,
      "number_of_replicas": 1,
      "refresh_interval": "5s"
    }
  }
}
```

## 5. Cross-Domain Data Synchronization

### 5.1 Event-Driven Architecture

```sql
-- Events schema: Cross-domain event sourcing
CREATE TABLE events.domain_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event identification
    event_type VARCHAR(100) NOT NULL,
    domain VARCHAR(50) NOT NULL, -- security, productivity, tcg, infrastructure
    aggregate_id VARCHAR(255) NOT NULL,
    
    -- Event payload
    event_data JSONB NOT NULL,
    event_version INTEGER DEFAULT 1,
    
    -- Causation and correlation
    causation_id UUID, -- What caused this event
    correlation_id UUID, -- Group of related events
    
    -- Metadata
    user_id UUID REFERENCES core.users(id),
    organization_id UUID REFERENCES core.organizations(id),
    
    -- Processing
    processed_by TEXT[] DEFAULT '{}', -- List of processors that handled this event
    processing_errors JSONB DEFAULT '{}',
    
    occurred_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    INDEX idx_domain_events_type (event_type, occurred_at),
    INDEX idx_domain_events_domain (domain, aggregate_id),
    INDEX idx_domain_events_correlation (correlation_id)
);
```

### 5.2 Data Consistency Patterns

```yaml
Consistency Patterns by Use Case:
  Strong Consistency:
    - User authentication and authorization
    - Financial data (Actual Budget)
    - Security incident response
    
  Eventual Consistency:
    - Recipe synchronization (Mealie)
    - TCG card data updates
    - Performance metrics and monitoring
    
  Conflict Resolution:
    - Last-Writer-Wins: Simple configuration changes
    - CRDT Merge: Collaborative editing (task lists)
    - User Choice: Critical data conflicts require manual resolution
```

## 6. Migration Data Mapping

### 6.1 Tool-Specific Migration Mappings

```yaml
Migration Mapping Strategy:
  Category A Tools (Preserve Data Structures):
    MISP: 
      - Maintain PHP data models in containerized service
      - API adapter layer for PostgreSQL integration
      - Event correlation through events schema
      
    YARA-X:
      - Rust binary preservation with database integration
      - Rule storage in security.yara_rules table
      - Performance tracking and analytics
      
    CyberChef:
      - Recipe format preservation in JSONB fields
      - Operation history tracking
      - Result caching for performance
      
  Category B Tools (Schema Modernization):
    n8n:
      - Workflow definitions → productivity.projects.workflow_configs
      - Execution history → events.domain_events
      - User credentials → secure credential store
      
    Mealie:
      - Recipe data → productivity.recipes table
      - User preferences → local SQLite + sync
      - Image storage → blob storage with references
      
    Commander Spellbook:
      - Combo data → tcg.combos table
      - Card references → tcg.cards table
      - Community features → user interaction tracking
      
  Category C Tools (Complete Modernization):
    IT-Tools:
      - Utility configurations → infrastructure.tool_configurations
      - User preferences → user_preferences table
      - Usage analytics → events schema
```

## 6. Migration Validation Methodology (Strategy 5)

### 6.1 Data Migration Requirements (CHK004-CHK006)

#### Data Migration Specifications (CHK004)

**Per-Tool Persistent State Migration**:

```yaml
Security Domain Migration:
  MISP:
    - Event correlation data (8,733 lines of PHP logic preservation)
    - Attribute relationships (complex many-to-many mappings)
    - Object templates (JSON structure preservation)
    - Threat intelligence feeds (API key management)
    
  HELK:
    - Elasticsearch indices (security logs, network data)
    - Kibana dashboards (visualization preservation)
    - Logstash configurations (parsing rules maintenance)
    
  SecurityOnion:
    - Salt pillar data (configuration state)
    - Suricata rules (detection logic preservation)
    - PCAP file references (forensic data integrity)

Productivity Domain Migration:
  n8n:
    - Workflow definitions (2,620 lines execution engine)
    - Credential vault (encrypted secrets migration)
    - Execution history (state transition logs)
    
  Actual Budget:
    - CRDT synchronization state (~2,000 lines)
    - Budget categories (financial logic preservation)
    - Transaction history (audit trail integrity)
    
  Mealie:
    - Recipe database (ingredient relationships)
    - Shopping lists (user preference data)
    - Nutritional calculations (algorithm preservation)

TCG Domain Migration:
  Commander Spellbook:
    - Combo variant data (~1,400 lines generation algorithm)
    - Card relationship mappings (rules engine data)
    - User deck collections (personalization data)
    
Infrastructure Domain Migration:
  IT-Tools:
    - 80+ utility configurations (tool-specific settings)
    - User customizations (interface preferences)
    - Usage analytics (behavioral data patterns)
```

#### Configuration Migration Requirements (CHK005)

**All 37 Tools Settings Migration**:

```sql
-- Unified configuration schema per domain
CREATE TABLE migration.tool_configurations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Tool identification
    source_tool VARCHAR(255) NOT NULL, -- Original tool name (e.g., 'misp', 'n8n')
    target_domain VARCHAR(50) NOT NULL, -- security, productivity, tcg, infrastructure
    
    -- Configuration data
    config_key VARCHAR(255) NOT NULL, -- Setting identifier
    config_value JSONB NOT NULL, -- Original setting value
    config_type VARCHAR(50) NOT NULL, -- string, integer, boolean, json, encrypted
    
    -- Migration metadata
    migration_status VARCHAR(50) DEFAULT 'pending', -- pending, migrated, failed, skipped
    migration_notes TEXT, -- Conversion logic applied
    requires_manual_review BOOLEAN DEFAULT false,
    
    -- Validation
    source_checksum VARCHAR(64), -- Original configuration hash
    target_checksum VARCHAR(64), -- Migrated configuration hash
    
    -- Audit trail
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    migrated_at TIMESTAMP WITH TIME ZONE,
    validated_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(source_tool, config_key)
);
```

#### User Preference Migration (CHK006)

**Cross-Domain User Preference Specifications**:

```sql
-- User preferences with domain boundary respect
CREATE TABLE core.user_domain_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES core.users(id),
    
    -- Domain-specific preferences
    domain VARCHAR(50) NOT NULL, -- security, productivity, tcg, infrastructure
    preference_category VARCHAR(100) NOT NULL, -- ui, notifications, integrations
    
    -- Preference data
    preferences JSONB NOT NULL, -- Domain-specific preference structure
    
    -- Cross-domain sync
    sync_enabled BOOLEAN DEFAULT true, -- Allow cross-domain preference sharing
    sync_whitelist TEXT[], -- Specific preferences to sync across domains
    
    -- Migration tracking
    migrated_from_tool VARCHAR(255), -- Original tool that provided this preference
    migration_confidence DECIMAL(3,2), -- 0.00-1.00 confidence in migration accuracy
    
    -- Audit
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, domain, preference_category)
);
```

### 6.2 Edge Case Migration Requirements (CHK040-CHK046)

#### Zero-Data Scenarios (CHK039, CHK040)

**Domain-Specific Empty State Handling**:

```yaml
Security Domain Zero-Data:
  - No threat indicators: Default taxonomy installation, placeholder IOCs
  - No security events: Sample event templates, monitoring baseline
  - No YARA rules: Core rule set from yara-rules repository
  - No network logs: Generate synthetic test data for dashboard validation

Productivity Domain Zero-Data:
  - No tasks: Sample project template, getting-started workflow
  - No recipes: Basic recipe database seed (public domain recipes)
  - No budget categories: Standard personal finance categories
  - No workflows: Tutorial n8n workflows for user onboarding

TCG Domain Zero-Data:
  - No cards: MTG basic land database minimum
  - No decks: Preconstructed deck examples
  - No combos: Popular combo database seed
  - No tournaments: Historical tournament data sample

Infrastructure Domain Zero-Data:
  - No services: Default system monitoring templates
  - No configurations: Standard IT-Tools utility defaults
  - No monitoring data: Health check baseline establishment
```

#### Large Dataset Migration (CHK040)

**High-Volume Data Handling**:

```sql
-- Large dataset migration tracking
CREATE TABLE migration.bulk_migration_status (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Dataset identification
    source_tool VARCHAR(255) NOT NULL,
    dataset_type VARCHAR(100) NOT NULL, -- threats, logs, cards, workflows
    estimated_record_count BIGINT,
    
    -- Batch processing
    batch_size INTEGER DEFAULT 1000,
    current_batch INTEGER DEFAULT 0,
    total_batches INTEGER,
    
    -- Progress tracking
    records_processed BIGINT DEFAULT 0,
    records_failed BIGINT DEFAULT 0,
    processing_rate DECIMAL(10,2), -- records per second
    
    -- Resource management
    memory_usage_mb INTEGER,
    cpu_usage_percent DECIMAL(5,2),
    estimated_completion_time TIMESTAMP WITH TIME ZONE,
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    error_details JSONB,
    
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE
);
```

#### Legacy Data Format Incompatibilities (CHK041)

**Format Conversion Requirements**:

```yaml
Database Format Conversions:
  MySQL → PostgreSQL:
    - MISP Event.php: Complex PHP serialization → JSON/JSONB
    - Character encoding: latin1 → UTF-8 with special character handling
    - Auto-increment IDs → UUID conversion with relationship preservation
    
  SQLite → PostgreSQL:
    - Actual Budget CRDT: Maintain conflict resolution capabilities
    - Timestamp formats: SQLite datetime → PostgreSQL timestamptz
    - BLOB data: Binary data migration with integrity verification
    
  Elasticsearch → PostgreSQL:
    - HELK indices: JSON document → relational schema normalization
    - Full-text search: Elasticsearch queries → PostgreSQL text search
    - Time-based indices: Partition strategy preservation

File Format Conversions:
  Configuration Files:
    - YAML configs → JSON/JSONB with comment preservation
    - INI files → structured JSON with section mapping
    - XML configs → JSON with schema validation
    
  Data Exports:
    - CSV exports → structured imports with type inference
    - JSON exports → schema validation and normalization
    - Binary formats → base64 encoding with metadata preservation
```

### 6.3 Data Validation and Quality Assurance

```sql
-- Migration validation framework (Enhanced with 822 CRUD + 743 API tests)
CREATE TABLE migration.validation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Validation context
    tool_name VARCHAR(255) NOT NULL,
    validation_type VARCHAR(100) NOT NULL, -- schema, data_integrity, performance, business_logic
    test_suite VARCHAR(100) NOT NULL, -- crud_operations, api_operations, exotic_patterns
    
    -- Test execution details
    total_tests INTEGER NOT NULL, -- From 822 CRUD + 743 API + 1970 exotic tests
    tests_passed INTEGER NOT NULL,
    tests_failed INTEGER NOT NULL,
    tests_skipped INTEGER NOT NULL,
    
    -- Results
    status VARCHAR(50) NOT NULL, -- passed, failed, warning
    details JSONB NOT NULL, -- Validation results and metrics
    failure_details JSONB, -- Specific test failures for analysis
    
    -- Comparison data (Business Logic Preservation Validation)
    source_record_count INTEGER,
    target_record_count INTEGER,
    data_checksum VARCHAR(64), -- For integrity verification
    business_logic_hash VARCHAR(64), -- Algorithm output verification
    
    -- Performance metrics
    migration_duration INTERVAL,
    validation_duration INTERVAL,
    
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    executed_by UUID REFERENCES core.users(id)
);
```

## 7. DDD Implementation Patterns

### 7.1 Module Boundary Enforcement

#### Strict Async-Only Communication Between Domains

```python
# Domain interface contracts - no direct method calls allowed
from abc import ABC, abstractmethod
from typing import Any, TypeVar

TCommand = TypeVar('TCommand')
TQuery = TypeVar('TQuery')
TResult = TypeVar('TResult')

class IDomainModule(ABC):
    """Base interface for all domain modules - async-only communication"""
    
    @abstractmethod
    async def execute_command_async(self, command: TCommand) -> TResult:
        """Process commands asynchronously with internal command queuing"""
        pass
        
    @abstractmethod
    async def execute_query_async(self, query: TQuery) -> TResult:
        """Process queries with read model optimization"""
        pass

# Example domain interfaces
class ISecurityModule(IDomainModule):
    """Security domain - 13 tools consolidation"""
    pass

class IProductivityModule(IDomainModule):
    """Productivity domain - 8 tools consolidation"""
    pass

class ITCGModule(IDomainModule):
    """TCG domain - 4 tools consolidation"""
    pass

class IInfrastructureModule(IDomainModule):
    """Infrastructure domain - 12 tools consolidation"""
    pass
```

### 7.2 Rich Domain Models with Business Logic Encapsulation

#### Category A Tool Preservation - Complex Algorithm Encapsulation

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import uuid

class AggregateRoot:
    """Base class for domain aggregates with business logic encapsulation"""
    def __init__(self):
        self._domain_events: List[DomainEvent] = []
        
    def add_domain_event(self, event: 'DomainEvent'):
        self._domain_events.append(event)
        
    def clear_domain_events(self):
        self._domain_events.clear()

# Example: MISP Threat Indicator with preserved business logic
class ThreatIndicator(AggregateRoot):
    def __init__(self):
        super().__init__()
        self._id: Optional[uuid.UUID] = None
        self._confidence_score: Optional[int] = None
        self._threat_types: List[str] = []
        self._misp_correlation_data: Optional[Dict] = None
        
    @classmethod
    def create_from_misp_analysis(
        cls, 
        misp_data: Dict, 
        confidence_rules: 'MISPConfidenceRules'
    ) -> 'ThreatIndicator':
        """Factory method preserving MISP's complex confidence algorithms"""
        indicator = cls()
        indicator._id = uuid.uuid4()
        
        # Preserve MISP's sophisticated confidence calculation
        indicator._confidence_score = confidence_rules.calculate_confidence(
            misp_data.get('sighting_count', 0),
            misp_data.get('source_reliability', 'unknown'),
            misp_data.get('temporal_decay_factor', 1.0)
        )
        
        # Preserve complex threat type correlation logic
        indicator._threat_types = confidence_rules.correlate_threat_types(
            misp_data.get('tags', []),
            misp_data.get('galaxy_clusters', [])
        )
        
        indicator._misp_correlation_data = misp_data
        indicator.add_domain_event(ThreatIndicatorCreatedEvent(indicator._id))
        
        return indicator
        
    def correlate_with_yara_match(self, yara_result: 'YaraMatchResult') -> 'CorrelationResult':
        """Cross-tool correlation preserving both MISP and YARA-X business logic"""
        if not self._can_correlate_with_yara(yara_result):
            return CorrelationResult.no_correlation()
            
        # Preserved MISP correlation algorithm enhanced with YARA-X results
        correlation_strength = self._calculate_correlation_strength(yara_result)
        
        if correlation_strength > 0.7:  # MISP's correlation threshold
            self._enhance_confidence_from_yara(yara_result)
            self.add_domain_event(ThreatIndicatorEnhancedEvent(self._id, yara_result.rule_id))
            
        return CorrelationResult(correlation_strength, self._confidence_score)
        
    def _can_correlate_with_yara(self, yara_result: 'YaraMatchResult') -> bool:
        """MISP's correlation eligibility rules"""
        return (
            'malware' in self._threat_types and
            yara_result.match_confidence > 0.8 and
            self._confidence_score > 50
        )

# Example: YARA-X Rule Engine with preserved Rust performance characteristics
class YaraRuleEngine(AggregateRoot):
    """Encapsulates YARA-X rule compilation and matching logic"""
    
    @classmethod
    def create_rule_from_source(cls, rule_source: str, metadata: Dict) -> 'YaraRule':
        """Factory preserving YARA-X compilation optimizations"""
        engine = cls()
        
        # Preserve YARA-X's sophisticated rule validation
        validation_result = engine._validate_rule_syntax(rule_source)
        if not validation_result.is_valid:
            raise InvalidYaraRuleError(validation_result.errors)
            
        # Preserve optimization patterns from original YARA-X implementation
        compiled_rule = engine._compile_with_optimizations(rule_source, metadata)
        
        return YaraRule(compiled_rule, metadata, validation_result.performance_metrics)
```

### 7.3 Internal Command System for Migration Workflows

#### Async Processing for Complex Tool Migrations

```python
from abc import ABC, abstractmethod
from enum import Enum
import asyncio
from typing import Dict, Any

class InternalCommandBase(ABC):
    """Base class for internal commands with retry and rollback capabilities"""
    
    def __init__(self, command_id: uuid.UUID = None):
        self.command_id = command_id or uuid.uuid4()
        self.created_at = datetime.now()
        self.retry_count = 0
        self.max_retries = 3
        
    @abstractmethod
    async def execute(self) -> 'CommandResult':
        """Execute the internal command with error handling"""
        pass
        
    @abstractmethod
    async def compensate(self) -> 'CompensationResult':
        """Rollback command effects if execution fails"""
        pass

class MigrateMispDataInternalCommand(InternalCommandBase):
    """Complex MISP data transformation with preserved business logic"""
    
    def __init__(self, misp_instance_id: uuid.UUID, target_schema: str, preserve_relationships: bool):
        super().__init__()
        self.misp_instance_id = misp_instance_id
        self.target_schema = target_schema
        self.preserve_relationships = preserve_relationships
        
    async def execute(self) -> 'CommandResult':
        """Execute MISP data migration with relationship preservation"""
        try:
            # Phase 1: Extract MISP data with relationship mapping
            misp_data = await self._extract_misp_data_with_relationships()
            
            # Phase 2: Transform while preserving MISP's correlation algorithms
            transformed_data = await self._transform_preserving_misp_logic(misp_data)
            
            # Phase 3: Load into target schema with validation
            load_result = await self._load_with_integrity_validation(transformed_data)
            
            return CommandResult.success(load_result)
            
        except Exception as e:
            await self.compensate()
            return CommandResult.failure(str(e))
            
    async def compensate(self) -> 'CompensationResult':
        """Rollback MISP migration with data consistency guarantees"""
        # Implement sophisticated rollback preserving MISP instance integrity
        pass

class ProcessYaraRuleInternalCommand(InternalCommandBase):
    """Async YARA-X rule processing with performance preservation"""
    
    def __init__(self, rule_content: str, source_tool: str, validation_required: bool):
        super().__init__()
        self.rule_content = rule_content
        self.source_tool = source_tool
        self.validation_required = validation_required
        
    async def execute(self) -> 'CommandResult':
        """Process YARA rules preserving Rust-level performance characteristics"""
        # Preserve YARA-X compilation optimizations in Python wrapper
        pass
```

### 7.4 Outbox/Inbox Pattern for Cross-Domain Reliability

#### Guaranteed Event Delivery Between Domains

```sql
-- Events schema: Outbox pattern implementation
CREATE TABLE events.domain_outbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event identification
    event_type VARCHAR(100) NOT NULL,
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id UUID NOT NULL,
    
    -- Event payload
    event_data JSONB NOT NULL,
    metadata JSONB DEFAULT '{}',
    
    -- Delivery tracking
    source_domain VARCHAR(50) NOT NULL, -- security, productivity, tcg, infrastructure
    target_domains TEXT[] NOT NULL, -- Array of target domains
    published_at TIMESTAMP WITH TIME ZONE,
    
    -- Reliability
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 5,
    next_retry_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexing for performance
    INDEX idx_outbox_unpublished (published_at) WHERE published_at IS NULL,
    INDEX idx_outbox_retry (next_retry_at) WHERE next_retry_at IS NOT NULL
);

-- Events schema: Inbox pattern for idempotent processing
CREATE TABLE events.domain_inbox (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Event identification (for deduplication)
    event_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    source_domain VARCHAR(50) NOT NULL,
    target_domain VARCHAR(50) NOT NULL,
    
    -- Event payload
    event_data JSONB NOT NULL,
    
    -- Processing tracking
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, processing, completed, failed
    processed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    received_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure idempotency
    UNIQUE(event_id, target_domain),
    INDEX idx_inbox_pending (target_domain, status) WHERE status = 'pending'
);
```

### 7.5 Architecture Compliance Testing Framework

#### Automated Boundary Enforcement for 37-Tool Consolidation

```python
import importlib
import ast
import os
from pathlib import Path
from typing import List, Set

class ArchitectureComplianceChecker:
    """Validates modular monolith boundaries during development"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.domain_boundaries = {
            'security': ['apps/jane-orchestrator/src/domains/security'],
            'productivity': ['apps/jane-orchestrator/src/domains/productivity'], 
            'tcg': ['apps/jane-orchestrator/src/domains/tcg'],
            'infrastructure': ['apps/jane-orchestrator/src/domains/infrastructure']
        }
        
    def validate_domain_dependencies(self) -> List['ComplianceViolation']:
        """Ensure domains only communicate through async interfaces"""
        violations = []
        
        for domain_name, domain_paths in self.domain_boundaries.items():
            for domain_path in domain_paths:
                violations.extend(
                    self._check_direct_domain_imports(domain_name, domain_path)
                )
                
        return violations
        
    def validate_database_access_patterns(self) -> List['ComplianceViolation']:
        """Ensure domain services don't directly access other domain schemas"""
        violations = []
        
        # Check that security domain doesn't access productivity.* tables directly
        # Implementation would scan for SQL queries and ORM usage
        
        return violations
        
    def _check_direct_domain_imports(self, domain_name: str, domain_path: str) -> List['ComplianceViolation']:
        """Scan Python files for forbidden cross-domain imports"""
        violations = []
        forbidden_patterns = [
            f"from ..{other_domain}" for other_domain in self.domain_boundaries.keys() 
            if other_domain != domain_name
        ]
        
        # Implementation would use AST parsing to detect violations
        return violations

# pytest tests for architecture compliance
def test_security_domain_isolation():
    """Security domain must not depend on other domains directly"""
    checker = ArchitectureComplianceChecker(Path(__file__).parent.parent)
    violations = checker.validate_domain_dependencies()
    
    security_violations = [v for v in violations if v.domain == 'security']
    assert len(security_violations) == 0, f"Security domain boundary violations: {security_violations}"

def test_no_direct_database_cross_domain_access():
    """Domain services should access only their own schemas"""
    checker = ArchitectureComplianceChecker(Path(__file__).parent.parent)
    violations = checker.validate_database_access_patterns()
    
    assert len(violations) == 0, f"Database access violations: {violations}"
```

### 7.6 Decorator Pattern for Cross-Cutting Concerns

#### Consistent Command/Query Processing Across All 37 Tools

```python
from functools import wraps
from typing import Callable, Any
import time
import logging
from contextlib import asynccontextmanager

def logging_decorator(func: Callable) -> Callable:
    """Log all command/query execution with domain context"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")
        
        command_name = args[0].__class__.__name__ if args else "unknown"
        logger.info(f"Executing {command_name}", extra={
            'domain': getattr(self, 'domain_name', 'unknown'),
            'command_type': command_name,
            'user_id': kwargs.get('user_id'),
        })
        
        try:
            result = await func(self, *args, **kwargs)
            logger.info(f"Completed {command_name}")
            return result
        except Exception as e:
            logger.error(f"Failed {command_name}: {str(e)}")
            raise
            
    return wrapper

def performance_monitoring_decorator(domain_sla_seconds: float):
    """Monitor domain-specific SLA compliance"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            start_time = time.time()
            
            try:
                result = await func(self, *args, **kwargs)
                
                execution_time = time.time() - start_time
                if execution_time > domain_sla_seconds:
                    # Log SLA violation for monitoring
                    logging.warning(f"SLA violation: {execution_time:.2f}s > {domain_sla_seconds}s")
                    
                return result
            finally:
                # Always record metrics for performance analysis
                pass
                
        return wrapper
    return decorator

def validation_decorator(func: Callable) -> Callable:
    """Validate command/query data using domain-specific rules"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if args:
            command_or_query = args[0]
            # Run validation logic specific to the command/query type
            validator = getattr(command_or_query, 'validate', None)
            if validator:
                validation_result = await validator()
                if not validation_result.is_valid:
                    raise ValidationError(validation_result.errors)
                    
        return await func(self, *args, **kwargs)
    return wrapper

def unit_of_work_decorator(func: Callable) -> Callable:
    """Manage database transactions and domain event publishing"""
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        async with self.unit_of_work() as uow:
            try:
                result = await func(self, *args, **kwargs)
                
                # Publish domain events as part of transaction
                await self.event_publisher.publish_domain_events(
                    getattr(self, '_domain_events', [])
                )
                
                await uow.commit()
                return result
            except Exception:
                await uow.rollback()
                raise
                
    return wrapper

# Example usage: Security domain command handler
class CreateThreatIndicatorCommandHandler:
    domain_name = 'security'
    
    @logging_decorator
    @performance_monitoring_decorator(domain_sla_seconds=1.0)  # Security SLA: <1s
    @validation_decorator
    @unit_of_work_decorator
    async def handle(self, command: 'CreateThreatIndicatorCommand') -> 'ThreatIndicator':
        """Pure business logic - all cross-cutting concerns handled by decorators"""
        
        # Business logic only - preserved from original MISP implementation
        threat_indicator = ThreatIndicator.create_from_misp_analysis(
            command.misp_data,
            self.misp_confidence_rules
        )
        
        await self.threat_repository.save(threat_indicator)
        return threat_indicator
```

## 8. Performance Optimization Strategy

### 8.1 Domain-Specific Performance Targets

```yaml
Performance Requirements by Domain:
  Security Domain (<1s response):
    - Indexed threat indicator lookups
    - YARA rule compilation caching
    - Network event streaming with buffering
    
  Productivity Domain (<2s response):
    - Task query optimization with user-based partitioning
    - Recipe search with full-text indexing
    - Workflow execution with async processing
    
  TCG Domain (<3s response):
    - Card database with materialized views
    - Combo search with graph traversal optimization
    - Deck analysis with cached statistics
    
  Infrastructure Domain (<5s response):
    - Service monitoring with time-series optimization
    - Configuration management with versioning
    - Bulk operations with batch processing
```

### 7.2 Caching Strategy

```yaml
Multi-Layer Caching Architecture:
  Level 1 - Application Cache:
    - Redis for session data and frequently accessed objects
    - Memory caching for configuration data
    - Query result caching with TTL management
    
  Level 2 - Database Cache:
    - PostgreSQL shared_buffers optimization
    - Materialized views for complex queries  
    - Partial indexes for domain-specific queries
    
  Level 3 - Client Cache:
    - SQLite local storage for offline data
    - Browser storage for UI state
    - CDN for static assets and documentation
```

## 7. API Contract Standardization (Strategy 11)

### 7.1 Rich Domain Models Implementation (CHK016)

**Concrete Implementation Criteria for Domain Models**:

```python
# Security Domain Rich Models
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

@dataclass
class ThreatIndicator:
    """Rich domain model for threat intelligence with encapsulated business logic"""
    
    # Core identity
    id: uuid.UUID
    indicator_value: str
    indicator_type: str  # ip, domain, hash, url
    
    # Rich behavior methods (preserve MISP correlation logic)
    def correlate_with_threats(self, threat_database: 'IThreatRepository') -> List['CorrelationResult']:
        """Implements 8,733 lines of MISP Event.php correlation logic"""
        pass
    
    def calculate_threat_score(self, context: 'SecurityContext') -> float:
        """Business logic for threat scoring algorithm preservation"""
        pass
    
    def generate_yara_rule(self) -> Optional[str]:
        """Convert indicator to YARA rule using preserved YARA-X logic"""
        pass
    
    # Domain invariants (business rule enforcement)
    def validate_indicator_format(self) -> bool:
        """Ensures indicator format matches type requirements"""
        pass

@dataclass 
class WorkflowExecution:
    """Rich domain model for n8n workflow with 2,620 lines execution engine logic"""
    
    # Core identity
    id: uuid.UUID
    workflow_definition: Dict[str, Any]
    execution_context: 'ExecutionContext'
    
    # Rich behavior (preserve n8n WorkflowExecute engine)
    def execute_nodes(self) -> 'ExecutionResult':
        """Implements complex node execution with state management"""
        pass
    
    def handle_node_error(self, node_id: str, error: Exception) -> 'ErrorHandlingResult':
        """Preserve n8n error handling and retry logic"""
        pass
    
    def manage_workflow_state(self) -> None:
        """State transition management with rollback capabilities"""
        pass

@dataclass
class ComboVariant:
    """Rich domain model for MTG combo analysis with ~1,400 lines generation logic"""
    
    # Core identity
    id: uuid.UUID
    cards: List['Card']
    combo_steps: List[str]
    
    # Rich behavior (preserve Commander Spellbook variant generation)
    def generate_variants(self, card_database: 'ICardRepository') -> List['ComboVariant']:
        """Implements complex combo variant generation algorithm"""
        pass
    
    def calculate_combo_probability(self, deck: 'Deck') -> float:
        """Statistical analysis of combo viability in deck context"""
        pass
    
    def validate_combo_legality(self, format_rules: 'FormatRules') -> bool:
        """Ensure combo complies with MTG format restrictions"""
        pass
```

### 7.2 Domain API Contracts with Security Alignment (CHK021-CHK022)

#### Security-First API Design

```typescript
// Security domain API with comprehensive security requirements
interface ISecurityDomainAPI {
    // Threat Intelligence Operations (preserve MISP functionality)
    analyzeThreat(request: {
        indicator: ThreatIndicator;
        context: SecurityAnalysisContext;
        // Security: All threat analysis requires authentication + authorization
        credentials: SecurityCredentials;
        // Security: Audit trail for all threat analysis operations  
        auditContext: AuditContext;
    }): Promise<ThreatAnalysisResult>;
    
    // Cross-Domain Security Event Publishing
    publishSecurityAlert(event: {
        alert: SecurityAlert;
        severity: AlertSeverity; // CRITICAL, HIGH, MEDIUM, LOW
        // Security: Encrypted event payload for sensitive threat data
        encryptedPayload: EncryptedEventData;
        // Security: Digital signature for event integrity verification
        eventSignature: DigitalSignature;
    }): Promise<PublishResult>;
    
    // Security: Data in transit encryption for all API calls
    // Security: Rate limiting per user/organization to prevent abuse
    // Security: IP whitelisting for critical threat intelligence operations
}

// Productivity domain API with unified security model
interface IProductivityDomainAPI {
    // Task Management (preserve n8n + Dispatch functionality)
    executeWorkflow(request: {
        workflowId: UUID;
        executionContext: WorkflowContext;
        // Security: Consistent authentication across all domains
        credentials: SecurityCredentials;
        // Security: Workflow execution audit for compliance
        auditContext: AuditContext;
    }): Promise<WorkflowExecutionResult>;
    
    // Budget Management (preserve Actual Budget CRDT logic)  
    syncBudgetData(request: {
        budgetUpdates: BudgetCRDT[];
        // Security: Financial data encryption requirements
        encryptionLevel: EncryptionLevel.HIGH;
        // Security: Multi-factor authentication for financial operations
        mfaToken: MFAToken;
    }): Promise<SyncResult>;
    
    // Security: All productivity APIs inherit security model from unified platform
    // Security: Data segregation between users/organizations in productivity workflows
}
```

#### API Version Compatibility Management (CHK061)

```yaml
API Versioning Strategy:
  External API Dependencies:
    MISP API: 
      - Current: v2.4.156+ (threat intelligence operations)
      - Compatibility: Maintain v2.4+ support for 24 months
      - Breaking Changes: Automated migration scripts for correlation engine
      
    VirusTotal API:
      - Current: v3 (file/URL analysis integration)
      - Rate Limiting: 500 requests/day public, 1000/minute premium
      - Error Handling: Graceful fallback to local analysis when quota exceeded
      
    Scryfall API (MTG Data):
      - Current: v1.7+ (card database synchronization)
      - Bulk Data: Daily card database updates with delta sync
      - Caching: 24-hour cache for card data to reduce API calls
      
  Internal API Versioning:
    Domain APIs:
      - Semantic Versioning: MAJOR.MINOR.PATCH
      - Backward Compatibility: 1 major version overlap (12 months)
      - Breaking Change Policy: 
        * 6-month deprecation notice for major changes
        * Automated migration tooling for data structure changes
        * Rollback capabilities for failed API updates
        
    Database Schema Versioning:
      - Alembic migrations: Sequential version management
      - Zero-Downtime Migrations: Blue-green deployment with schema compatibility
      - Rollback Testing: Automated rollback verification for all schema changes

Cross-Domain API Contracts:
  Event Schema Versioning:
    - AsyncAPI 2.5 specifications for all domain events
    - Event evolution strategy: additive changes only, no field removal
    - Schema registry: Centralized event schema management with validation
    
  Authentication API:
    - OAuth2/OIDC compliance for federated identity
    - Token refresh: Automatic token renewal with 5-minute buffer
    - Session management: Redis-based session store with domain isolation
```

### 7.3 Database Migration Dependency Resolution (CHK060)

**Cross-Domain Relationship Management**:

```sql
-- Foreign key relationships between domains (controlled via events)
CREATE TABLE core.cross_domain_references (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Source domain reference
    source_domain VARCHAR(50) NOT NULL,
    source_table VARCHAR(255) NOT NULL, 
    source_id UUID NOT NULL,
    
    -- Target domain reference  
    target_domain VARCHAR(50) NOT NULL,
    target_table VARCHAR(255) NOT NULL,
    target_id UUID NOT NULL,
    
    -- Relationship metadata
    relationship_type VARCHAR(100) NOT NULL, -- user_activity, security_alert, workflow_trigger
    relationship_strength VARCHAR(20) DEFAULT 'weak', -- weak, strong (affects cascade behavior)
    
    -- Synchronization tracking
    sync_status VARCHAR(50) DEFAULT 'active', -- active, pending_deletion, archived
    last_sync_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Migration metadata
    migrated_from_tool VARCHAR(255), -- Original tool that created this relationship
    migration_batch_id UUID, -- Links to migration batch for rollback
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Ensure referential integrity across domains
    UNIQUE(source_domain, source_table, source_id, target_domain, target_table, target_id),
    
    -- Performance indexes
    INDEX idx_cross_domain_source (source_domain, source_id),
    INDEX idx_cross_domain_target (target_domain, target_id),
    INDEX idx_cross_domain_type (relationship_type),
    INDEX idx_cross_domain_sync (sync_status, last_sync_at)
);

-- Migration dependency ordering (ensures proper sequence)
CREATE TABLE migration.domain_dependencies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    -- Dependency relationship
    dependent_domain VARCHAR(50) NOT NULL, -- Domain that depends on another
    dependency_domain VARCHAR(50) NOT NULL, -- Domain that must be migrated first
    
    -- Dependency details
    dependency_type VARCHAR(100) NOT NULL, -- schema, data, configuration, users
    dependency_reason TEXT NOT NULL, -- Human-readable explanation
    
    -- Migration coordination
    migration_order INTEGER NOT NULL, -- Execution sequence (lower = earlier)
    parallel_safe BOOLEAN DEFAULT false, -- Can this dependency be migrated in parallel
    
    -- Validation requirements
    validation_required BOOLEAN DEFAULT true,
    validation_criteria JSONB, -- Specific tests that must pass
    
    -- Status tracking
    status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, failed
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Prevent circular dependencies
    CHECK (dependent_domain != dependency_domain),
    UNIQUE(dependent_domain, dependency_domain, dependency_type)
);
```

---

**Data Model Complete** | **Phase 1 Progress**: 50% | **Next**: Contracts & API Design
