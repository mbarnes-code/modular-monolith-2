### 1.1 Programming Language Distribution

Primary Language Clusters:
TypeScript/JavaScript Cluster (13 projects - 57%): - Primary: n8n, Firecrawl, Inspector, IT-Tools, FileScopeMCP, Actual Budget - Mixed: Commander Spellbook (frontend), Mealie (frontend), CyberChef, Goose - Secondary: MISP (frontend components), Nemesis (frontend)

    Common Stack Pattern:
      - Runtime: Node.js 18+
      - Frameworks: Express.js, React, Vue.js
      - Build: Vite, Webpack, TypeScript
      - Testing: Jest, Vitest, Cypress

Python Cluster (10 projects - 43%): - Primary: MISP, Dispatch, Mealie (backend), HELK, Maltrail, HexStrike AI - Secondary: Goose (MCP integration), Nemesis (backend), Ghostwriter - Frameworks: Django, FastAPI, Flask - Testing: pytest, unittest

Specialized/Exotic Implementations: - Rust: Goose (core agent), YARA-X, Nemesis (noseyparker component) - C++: KasmVNC (desktop virtualization) - PHP: MISP (legacy CakePHP - requires special handling) - Java: Software Forensic Kit - Shell: Onex (pure shell scripts)

### 1.2 Framework Consolidation Strategy

Backend Framework Standardization:
Primary Choice: FastAPI + Python 3.11+
Supporting Projects: 6 direct (Mealie, Dispatch, Nemesis, HexStrike AI, Firecrawl potential)
Rationale: - Async performance for high-concurrency workloads - Automatic OpenAPI documentation generation - Strong typing with Pydantic - Easy PostgreSQL + Redis integration - Modern Python ecosystem compatibility

Secondary Choice: Express.js + TypeScript
Supporting Projects: 4 direct (n8n, Inspector, Firecrawl, Goose server)
Use Case: Node.js specific integrations, real-time features

Legacy Preservation: Django
Supporting Projects: 2 (Ghostwriter, MISP migration candidate)
Use Case: Admin-heavy applications, existing Django expertise

Frontend Framework Standardization:
Primary Choice: Vue.js 3 + TypeScript
Supporting Projects: 3 direct (n8n, IT-Tools, Mealie)
Rationale: - Easier learning curve than React - Excellent TypeScript integration - Component reusability across domains - Good ecosystem (Vuetify, Quasar)

Secondary Choice: React 18 + TypeScript
Supporting Projects: 3 direct (Actual Budget, Commander Spellbook, Inspector)
Use Case: Complex state management, existing React components

### 1.3 Database Consolidation Strategy

Primary Database: PostgreSQL 14+
Supporting Projects: 10 projects - MISP, n8n, Dispatch, Nemesis, Firecrawl, Ghostwriter - Commander Spellbook, Mealie (configurable), HELK (as backend)

Features Required: - JSONB support for flexible schemas (MISP events, n8n workflows) - Full-text search (GIN indexes for security intelligence) - Complex relationships (foreign keys, constraints) - Time-series data (Maltrail events, HELK logs) - Geospatial extensions (PostGIS for threat intelligence)

Secondary Database: SQLite
Supporting Projects: 6 projects (local-first applications) - Actual Budget, IT-Tools (browser storage), FileScopeMCP - CyberChef (browser storage), Software Forensic Kit (local analysis)

Use Case: Embedded applications, offline-first, zero-config deployment

Cache & Message Queue: Redis 7+
Supporting Projects: 7 projects - MISP (session storage), n8n (job queues), HELK (data pipeline) - Nemesis (message broker), Firecrawl (job management)

Use Cases: - Background job processing (Celery, BullMQ) - Session storage and caching - Real-time messaging (WebSocket state) - Rate limiting and API throttling

### 2.1 Common API Patterns Analysis

REST API Standardization:
Common Patterns Found: - n8n: /api/v1/workflows, /api/v1/executions - MISP: /api/v1/events, /api/v1/attributes - Dispatch: /api/v1/incidents, /api/v1/cases - Nemesis: /api/v1/projects, /api/v1/data - Commander Spellbook: /api/combos, /api/cards - Firecrawl: /api/v1/crawl, /api/v1/scrape - Mealie: /api/v1/recipes, /api/v1/groups

Unified URL Convention:
Pattern: /api/v{version}/{domain}/{resource}
Examples: - /api/v1/security/events # MISP events - /api/v1/automation/workflows # n8n workflows - /api/v1/incident/cases # Dispatch cases - /api/v1/gaming/combos # Commander Spellbook - /api/v1/tools/conversions # IT-Tools utilities - /api/v1/crawling/jobs # Firecrawl operations

### 2.2 Authentication & Authorization Consolidation

Authentication Strategy Unification:
Primary Method: JWT + Refresh Tokens
Supporting Projects: 8 projects - n8n (JWT), MISP (API keys + sessions), Dispatch (OAuth2) - Nemesis (JWT), Commander Spellbook (Discord OAuth) - Ghostwriter (Django auth), Mealie (JWT) - Actual Budget (local auth)

Unified Auth Flow:
POST /api/v1/auth/login
Request:
`json
      {
        "email": "user@example.com",
        "password": "secure_password",
        "provider": "local|discord|oauth2|ldap"
      }
      `

    Response:
      ```json
      {
        "access_token": "eyJ...",
        "refresh_token": "eyJ...",
        "expires_in": 3600,
        "user": {
          "id": "uuid",
          "email": "user@example.com",
          "roles": ["admin", "security_analyst"],
          "permissions": ["workflows:read", "incidents:write"],
          "domains": ["security", "automation", "gaming"]
        }
      }
      ```

Authorization Pattern - Domain-Based RBAC:
Roles by Domain:
Security Domain (MISP, Dispatch, HELK, Maltrail, HexStrike): - security_admin: Full access to all security tools - security_analyst: Read/write events, indicators, cases - security_viewer: Read-only access

    Automation Domain (n8n, Goose, Nemesis):
      - automation_admin: Manage workflows, credentials
      - automation_user: Create/edit own workflows
      - automation_viewer: View workflow executions

    Gaming Domain (Commander Spellbook, MTG tools):
      - gaming_admin: Manage combos, moderate submissions
      - gaming_contributor: Submit combos, edit own content
      - gaming_user: Search, favorite combos

    Productivity Domain (IT-Tools, CyberChef, Actual Budget):
      - productivity_user: Access all tools
      - productivity_admin: Manage shared resources

Cross-Domain Permissions:

- super_admin: Access to all domains
- multi_domain_user: Explicit permissions across domains

### 2.3 Standardized Request/Response Formats

Request Format Standardization:
Content-Type: application/json (primary)
Multipart Support: file uploads, large payloads

Query Parameters (pagination, filtering, sorting):
Pagination: - page: integer (1-based, default: 1) - limit: integer (max 1000, default: 50) - offset: integer (alternative to page)

    Filtering:
      - filter[field]: exact match
      - filter[field][operator]: gt, lt, gte, lte, in, like
      - search: full-text search across searchable fields

    Sorting:
      - sort: field_name (ascending)
      - sort: -field_name (descending)
      - sort: field1,-field2 (multiple fields)

Response Format Standardization:
Success Response:
`json
    {
      "success": true,
      "data": {}, // or [] for arrays
      "meta": {
        "pagination": {
          "page": 1,
          "limit": 50,
          "total": 1500,
          "pages": 30
        },
        "timing": {
          "request_id": "req_abc123",
          "duration_ms": 45
        }
      }
    }
    `

Error Response:
`json
    {
      "success": false,
      "error": {
        "code": "VALIDATION_ERROR",
        "message": "One or more fields are invalid",
        "details": {
          "email": ["Email format is invalid"],
          "workflow_id": ["Workflow not found"]
        },
        "request_id": "req_abc123"
      }
    }
    `

### 2.4 Domain-Specific API Specifications

Security Intelligence APIs:
Base Path: /api/v1/security

Common Endpoints:
Events (MISP-style):
GET /events - List security events
POST /events - Create event
GET /events/{id} - Get event details
PUT /events/{id} - Update event
DELETE /events/{id} - Delete event

    Indicators (IOCs):
      GET /indicators - List indicators
      POST /indicators - Add indicator
      GET /indicators/{id}/enrich - Enrich with threat intel

    Cases (Dispatch-style):
      GET /cases - List incident cases
      POST /cases - Create case
      GET /cases/{id}/timeline - Case timeline
      POST /cases/{id}/tasks - Add case task

Automation & Workflow APIs:
Base Path: /api/v1/automation

Workflows (n8n-style):
GET /workflows - List workflows
POST /workflows - Create workflow
GET /workflows/{id}/execute - Execute workflow
GET /workflows/{id}/executions - Execution history

Agents (Goose-style):
GET /agents - List available agents
POST /agents/{type}/sessions - Start agent session
POST /agents/sessions/{id}/message - Send message to agent

Gaming & MTG APIs:
Base Path: /api/v1/gaming

Combos (Commander Spellbook-style):
GET /combos - Search combos
POST /combos - Submit combo
GET /combos/{id}/variants - Get combo variants
GET /cards - Search MTG cards
GET /cards/{id}/combos - Combos using card

Productivity Tools APIs:
Base Path: /api/v1/tools

Converters (IT-Tools-style):
POST /convert/base64 - Base64 encode/decode
POST /convert/hash - Generate hashes
POST /cyberchef/recipe - Execute CyberChef recipe

Budget (Actual Budget-style):
GET /budget/accounts - List accounts
GET /budget/transactions - List transactions
POST /budget/transactions - Add transaction

### 2.5 WebSocket & Real-time API Standards

WebSocket Endpoints:
Connection Pattern: wss://app.domain.com/ws/v1/{domain}/{feature}

Examples: - wss://app.domain.com/ws/v1/automation/workflows/{id}/status - wss://app.domain.com/ws/v1/security/events/live - wss://app.domain.com/ws/v1/agents/sessions/{id}/chat - wss://app.domain.com/ws/v1/crawl/jobs/{id}/progress

Message Format:
Client to Server:
`json
    {
      "type": "subscribe|unsubscribe|message",
      "channel": "workflow_status|live_events|agent_chat",
      "payload": {},
      "request_id": "client_generated_id"
    }
    `

Server to Client:
`json
    {
      "type": "data|error|status",
      "channel": "workflow_status",
      "payload": {
        "workflow_id": "wf_123",
        "status": "running",
        "progress": 0.75
      },
      "request_id": "client_generated_id",
      "timestamp": "2025-01-18T10:30:00Z"
    }
    `

### 2.6 API Rate Limiting & Security

    Rate Limiting Strategy:
    Tier-based Limits:
      Free Tier:
        - 1000 requests/hour
        - 100 MB data transfer/day
        - No background jobs

      Premium Tier:
        - 10,000 requests/hour
        - 1 GB data transfer/day
        - Background job access

      Enterprise Tier:
        - Unlimited requests
        - Unlimited data transfer
        - Priority support

Security Headers:
Required Headers: - X-Content-Type-Options: nosniff - X-Frame-Options: DENY - X-XSS-Protection: 1; mode=block - Strict-Transport-Security: max-age=31536000 - Content-Security-Policy: [domain-specific]

Input Validation: - All inputs sanitized and validated - File uploads: type validation, size limits, virus scanning - JSON schema validation for complex payloads - SQL injection prevention (parameterized queries) - XSS prevention (output encoding)

### 3.1 Unified Data Models Analysis

Core Entity Categories:
Identity & Access Management: - Users (13 projects use this) - Organizations/Groups (8 projects) - Roles & Permissions (10 projects) - API Keys & Tokens (9 projects)

Security Intelligence: - Events (MISP, Dispatch, HELK, Maltrail) - Indicators/IOCs (MISP, HexStrike, Nemesis) - Cases/Incidents (Dispatch, Ghostwriter) - Threat Intelligence (MISP, HexStrike)

Automation & Workflows: - Workflows (n8n, Goose sessions) - Executions (n8n, background jobs) - Credentials (n8n, secure storage) - Schedules/Triggers (n8n, automation)

Content & Knowledge: - Cards & Combos (Commander Spellbook, MTG tools) - Recipes (Mealie) - Projects (Nemesis, Ghostwriter) - Files & Documents (multiple projects)

### 3.2 Consolidated PostgreSQL Schema Design

-- Core Identity Management (used by all modules)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Organizations/Tenants (multi-tenancy support)
CREATE TABLE organizations (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
name VARCHAR(255) NOT NULL,
slug VARCHAR(100) UNIQUE NOT NULL,
settings JSONB DEFAULT '{}',
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users (consolidated from n8n, MISP, Dispatch, etc.)
CREATE TABLE users (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
email VARCHAR(255) UNIQUE NOT NULL,
username VARCHAR(100) UNIQUE,
password_hash VARCHAR(255), -- nullable for OAuth-only users
first_name VARCHAR(100),
last_name VARCHAR(100),
avatar_url TEXT,

    -- Authentication providers (Discord, OAuth2, LDAP)
    auth_providers JSONB DEFAULT '[]',

    -- User preferences and settings
    settings JSONB DEFAULT '{}',

    -- Security fields
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    last_login_at TIMESTAMP WITH TIME ZONE,
    failed_login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Domain-based roles (security, automation, gaming, productivity)
CREATE TABLE roles (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
name VARCHAR(100) NOT NULL,
domain VARCHAR(50) NOT NULL, -- security, automation, gaming, productivity
description TEXT,
permissions JSONB DEFAULT '[]',
is_system_role BOOLEAN DEFAULT false,
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User role assignments
CREATE TABLE user_roles (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
user_id UUID REFERENCES users(id) ON DELETE CASCADE,
role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
assigned_by UUID REFERENCES users(id),
assigned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
expires_at TIMESTAMP WITH TIME ZONE,
UNIQUE(user_id, role_id)
);

-- API Keys for programmatic access
CREATE TABLE api_keys (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
user_id UUID REFERENCES users(id) ON DELETE CASCADE,
name VARCHAR(100) NOT NULL,
key_hash VARCHAR(255) NOT NULL,
key_prefix VARCHAR(20) NOT NULL, -- For display: "mm_1234..."
scopes JSONB DEFAULT '[]', -- ["security:read", "automation:write"]
last_used_at TIMESTAMP WITH TIME ZONE,
expires_at TIMESTAMP WITH TIME ZONE,
is_active BOOLEAN DEFAULT true,
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_organization ON users(organization_id);
CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_api_keys_user ON api_keys(user_id);
CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);
-- Security Events (MISP-style events, Dispatch incidents)
CREATE TABLE security_events (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
created_by UUID REFERENCES users(id),

    -- Event identification
    event_type VARCHAR(50) NOT NULL, -- misp_event, dispatch_incident, maltrail_alert
    title VARCHAR(255) NOT NULL,
    description TEXT,

    -- Classification
    tlp_level VARCHAR(10) DEFAULT 'WHITE', -- WHITE, GREEN, AMBER, RED
    severity VARCHAR(20) DEFAULT 'low', -- low, medium, high, critical
    status VARCHAR(20) DEFAULT 'new', -- new, investigating, resolved, closed

    -- Timing
    occurred_at TIMESTAMP WITH TIME ZONE,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE,

    -- Flexible event data (different for each source)
    event_data JSONB DEFAULT '{}',

    -- Relationships
    parent_event_id UUID REFERENCES security_events(id),
    related_events UUID[] DEFAULT '{}',

    -- Metadata
    tags TEXT[] DEFAULT '{}',
    source_system VARCHAR(50), -- misp, dispatch, maltrail, helk
    external_id VARCHAR(255), -- Original ID from source system

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Indicators of Compromise (IOCs)
CREATE TABLE indicators (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
created_by UUID REFERENCES users(id),

    -- Indicator data
    indicator_type VARCHAR(50) NOT NULL, -- ip, domain, hash, url, email, filename
    value TEXT NOT NULL,
    value_hash VARCHAR(64) NOT NULL, -- SHA256 of normalized value for deduplication

    -- Classification
    confidence INTEGER CHECK (confidence >= 0 AND confidence <= 100),
    severity VARCHAR(20) DEFAULT 'medium',
    tlp_level VARCHAR(10) DEFAULT 'WHITE',

    -- Context
    description TEXT,
    context JSONB DEFAULT '{}', -- Additional context data

    -- Lifecycle
    first_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,

    -- Source tracking
    source_system VARCHAR(50),
    source_reference TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE(organization_id, value_hash)

);

-- Link indicators to events
CREATE TABLE event_indicators (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
event_id UUID REFERENCES security_events(id) ON DELETE CASCADE,
indicator_id UUID REFERENCES indicators(id) ON DELETE CASCADE,
relationship_type VARCHAR(50) DEFAULT 'related', -- related, derived_from, caused_by
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
UNIQUE(event_id, indicator_id)
);

-- Security Cases (Dispatch-style incident management)
CREATE TABLE security_cases (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
created_by UUID REFERENCES users(id),
assigned_to UUID REFERENCES users(id),

    -- Case details
    title VARCHAR(255) NOT NULL,
    description TEXT,
    case_type VARCHAR(50) NOT NULL, -- incident, investigation, threat_hunt
    priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, critical
    status VARCHAR(20) DEFAULT 'new', -- new, assigned, investigating, resolved, closed

    -- Timing
    opened_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    due_date TIMESTAMP WITH TIME ZONE,
    closed_at TIMESTAMP WITH TIME ZONE,

    -- Case data
    case_data JSONB DEFAULT '{}',
    tags TEXT[] DEFAULT '{}',

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Link cases to events
CREATE TABLE case_events (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
case_id UUID REFERENCES security_cases(id) ON DELETE CASCADE,
event_id UUID REFERENCES security_events(id) ON DELETE CASCADE,
added_by UUID REFERENCES users(id),
added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
UNIQUE(case_id, event_id)
);

-- Indexes for security intelligence
CREATE INDEX idx_security_events_org ON security_events(organization_id);
CREATE INDEX idx_security_events_type ON security_events(event_type);
CREATE INDEX idx_security_events_status ON security_events(status);
CREATE INDEX idx_security_events_occurred ON security_events(occurred_at);
CREATE INDEX idx_security_events_tags ON security_events USING GIN(tags);
CREATE INDEX idx_security_events_data ON security_events USING GIN(event_data);

CREATE INDEX idx_indicators_org ON indicators(organization_id);
CREATE INDEX idx_indicators_type ON indicators(indicator_type);
CREATE INDEX idx_indicators_value_hash ON indicators(value_hash);
CREATE INDEX idx_indicators_active ON indicators(is_active);
CREATE INDEX idx_indicators_expires ON indicators(expires_at);

CREATE INDEX idx_security_cases_org ON security_cases(organization_id);
CREATE INDEX idx_security_cases_assigned ON security_cases(assigned_to);
CREATE INDEX idx_security_cases_status ON security_cases(status);

### 3.3 Automation & Workflow Schema

-- Workflows (n8n-style automation)
CREATE TABLE workflows (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
created_by UUID REFERENCES users(id),

    -- Workflow identification
    name VARCHAR(255) NOT NULL,
    description TEXT,

    -- Workflow definition (n8n JSON format)
    definition JSONB NOT NULL,

    -- Configuration
    is_active BOOLEAN DEFAULT false,
    trigger_type VARCHAR(50), -- manual, webhook, schedule, event
    trigger_config JSONB DEFAULT '{}',

    -- Execution settings
    timeout_seconds INTEGER DEFAULT 300,
    max_concurrent_executions INTEGER DEFAULT 1,
    retry_policy JSONB DEFAULT '{"enabled": false}',

    -- Versioning
    version INTEGER DEFAULT 1,
    parent_workflow_id UUID REFERENCES workflows(id),

    -- Statistics
    total_executions INTEGER DEFAULT 0,
    successful_executions INTEGER DEFAULT 0,
    failed_executions INTEGER DEFAULT 0,
    last_execution_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Workflow executions
CREATE TABLE workflow_executions (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
workflow_id UUID REFERENCES workflows(id) ON DELETE CASCADE,
triggered_by UUID REFERENCES users(id),

    -- Execution details
    status VARCHAR(20) DEFAULT 'running', -- running, success, failed, cancelled, timeout
    trigger_data JSONB DEFAULT '{}',

    -- Timing
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    finished_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,

    -- Results
    output_data JSONB DEFAULT '{}',
    error_message TEXT,

    -- Execution context
    execution_data JSONB DEFAULT '{}', -- node states, intermediate data

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Stored credentials (encrypted)
CREATE TABLE workflow_credentials (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
created_by UUID REFERENCES users(id),

    -- Credential identification
    name VARCHAR(255) NOT NULL,
    credential_type VARCHAR(100) NOT NULL, -- api_key, oauth2, database, etc

    -- Encrypted credential data
    encrypted_data TEXT NOT NULL, -- Encrypted JSON
    encryption_key_id VARCHAR(50) NOT NULL, -- Key management reference

    -- Usage tracking
    last_used_at TIMESTAMP WITH TIME ZONE,
    usage_count INTEGER DEFAULT 0,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE(organization_id, name)

);

-- Agent sessions (Goose-style AI agents)
CREATE TABLE agent_sessions (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    -- Agent configuration
    agent_type VARCHAR(50) NOT NULL, -- goose, custom, workflow_agent
    agent_config JSONB DEFAULT '{}',

    -- Session state
    status VARCHAR(20) DEFAULT 'active', -- active, paused, completed, failed
    context JSONB DEFAULT '{}', -- Agent memory/context

    -- Timing
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_activity_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Agent messages/interactions
CREATE TABLE agent_messages (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
session_id UUID REFERENCES agent_sessions(id) ON DELETE CASCADE,

    -- Message details
    message_type VARCHAR(50) NOT NULL, -- user_input, agent_response, system_message
    content TEXT NOT NULL,
    content_type VARCHAR(50) DEFAULT 'text', -- text, json, markdown, code

    -- Message metadata
    metadata JSONB DEFAULT '{}',
    token_count INTEGER,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Background jobs (unified job queue)
CREATE TABLE background_jobs (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
created_by UUID REFERENCES users(id),

    -- Job details
    job_type VARCHAR(100) NOT NULL, -- workflow_execution, data_import, report_generation
    job_data JSONB DEFAULT '{}',

    -- Scheduling
    status VARCHAR(20) DEFAULT 'pending', -- pending, running, completed, failed, cancelled
    scheduled_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,

    -- Results
    result_data JSONB DEFAULT '{}',
    error_message TEXT,

    -- Job configuration
    priority INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    retry_count INTEGER DEFAULT 0,
    timeout_seconds INTEGER DEFAULT 600,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Indexes for automation
CREATE INDEX idx_workflows_org ON workflows(organization_id);
CREATE INDEX idx_workflows_active ON workflows(is_active);
CREATE INDEX idx_workflows_trigger ON workflows(trigger_type);

CREATE INDEX idx_workflow_executions_workflow ON workflow_executions(workflow_id);
CREATE INDEX idx_workflow_executions_status ON workflow_executions(status);
CREATE INDEX idx_workflow_executions_started ON workflow_executions(started_at);

CREATE INDEX idx_agent_sessions_user ON agent_sessions(user_id);
CREATE INDEX idx_agent_sessions_status ON agent_sessions(status);

CREATE INDEX idx_background_jobs_status ON background_jobs(status);
CREATE INDEX idx_background_jobs_scheduled ON background_jobs(scheduled_at);
CREATE INDEX idx_background_jobs_type ON background_jobs(job_type);

### 3.4 Gaming & Content Schema

-- MTG Cards (from Commander Spellbook, MTG tools)
CREATE TABLE mtg_cards (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    -- Card identification
    oracle_id UUID, -- Scryfall oracle ID
    scryfall_id UUID, -- Scryfall card ID
    name VARCHAR(255) NOT NULL,
    mana_cost VARCHAR(100),
    cmc INTEGER, -- Converted mana cost

    -- Card properties
    type_line VARCHAR(255),
    oracle_text TEXT,
    power VARCHAR(10),
    toughness VARCHAR(10),
    loyalty VARCHAR(10),

    -- Game mechanics
    colors CHAR(5)[] DEFAULT '{}', -- W, U, B, R, G
    color_identity CHAR(5)[] DEFAULT '{}',
    keywords TEXT[] DEFAULT '{}',

    -- Set information
    set_code VARCHAR(10),
    set_name VARCHAR(255),
    rarity VARCHAR(20),
    collector_number VARCHAR(20),

    -- Imagery
    image_uris JSONB DEFAULT '{}',

    -- Legality
    legalities JSONB DEFAULT '{}',

    -- Metadata
    edhrec_rank INTEGER,
    reserved BOOLEAN DEFAULT false,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- MTG Combos (Commander Spellbook)
CREATE TABLE mtg_combos (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
created_by UUID REFERENCES users(id),

    -- Combo identification
    name VARCHAR(255),
    description TEXT NOT NULL,

    -- Combo properties
    color_identity VARCHAR(5), -- WUBRG representation
    mana_needed VARCHAR(100),
    steps TEXT NOT NULL,
    results TEXT[] DEFAULT '{}',

    -- Classification
    combo_type VARCHAR(50), -- infinite, near_infinite, value_engine
    popularity_score INTEGER DEFAULT 0,
    competitive_viability VARCHAR(20) DEFAULT 'casual', -- casual, focused, competitive, cedh

    -- Status
    status VARCHAR(20) DEFAULT 'draft', -- draft, submitted, approved, rejected
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,

    -- Community interaction
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    view_count INTEGER DEFAULT 0,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Combo card relationships
CREATE TABLE combo_cards (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
combo_id UUID REFERENCES mtg_combos(id) ON DELETE CASCADE,
card_id UUID REFERENCES mtg_cards(id) ON DELETE CASCADE,
quantity INTEGER DEFAULT 1,
role VARCHAR(50), -- commander, key_piece, enabler, outlet
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
UNIQUE(combo_id, card_id)
);

-- Combo variants/alternatives
CREATE TABLE combo_variants (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
parent_combo_id UUID REFERENCES mtg_combos(id) ON DELETE CASCADE,
variant_combo_id UUID REFERENCES mtg_combos(id) ON DELETE CASCADE,
variant_type VARCHAR(50), -- alternative, optimization, budget
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
UNIQUE(parent_combo_id, variant_combo_id)
);

-- Recipe management (Mealie)
CREATE TABLE recipes (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
created_by UUID REFERENCES users(id),

    -- Recipe basics
    name VARCHAR(255) NOT NULL,
    description TEXT,
    recipe_yield VARCHAR(50), -- "4 servings", "2 cups"

    -- Timing
    prep_time_minutes INTEGER,
    cook_time_minutes INTEGER,
    total_time_minutes INTEGER,

    -- Instructions
    ingredients JSONB DEFAULT '[]', -- [{name, quantity, unit, notes}]
    instructions JSONB DEFAULT '[]', -- [{step, text, time}]

    -- Classification
    recipe_category VARCHAR(100), -- breakfast, dinner, dessert
    cuisine VARCHAR(100), -- italian, mexican, asian
    difficulty VARCHAR(20) DEFAULT 'medium', -- easy, medium, hard

    -- Nutrition (optional)
    nutrition_data JSONB DEFAULT '{}',

    -- Media
    image_url TEXT,

    -- Community features
    rating DECIMAL(2,1) DEFAULT 0.0,
    rating_count INTEGER DEFAULT 0,
    is_public BOOLEAN DEFAULT false,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()

);

-- Recipe tags
CREATE TABLE recipe_tags (
id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
recipe_id UUID REFERENCES recipes(id) ON DELETE CASCADE,
tag_name VARCHAR(50) NOT NULL,
created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
UNIQUE(recipe_id, tag_name)
);

-- Indexes for gaming/content
CREATE INDEX idx_mtg_cards_name ON mtg_cards(name);
CREATE INDEX idx_mtg_cards_oracle ON mtg_cards(oracle_id);
CREATE INDEX idx_mtg_cards_colors ON mtg_cards USING GIN(colors);
CREATE INDEX idx_mtg_cards_keywords ON mtg_cards USING GIN(keywords);

CREATE INDEX idx_mtg_combos_org ON mtg_combos(organization_id);
CREATE INDEX idx_mtg_combos_status ON mtg_combos(status);
CREATE INDEX idx_mtg_combos_color_identity ON mtg_combos(color_identity);
CREATE INDEX idx_mtg_combos_created ON mtg_combos(created_at);

CREATE INDEX idx_recipes_org ON recipes(organization_id);
CREATE INDEX idx_recipes_category ON recipes(recipe_category);
CREATE INDEX idx_recipes_public ON recipes(is_public);

---

# Section 4: Frontend Framework Consolidation [CRITICAL]

## 4.1 Component Architecture Standardization

Based on analysis of all frontend implementations, here's the consolidated approach:

````yaml
Component Library Strategy:
  Primary Framework: Vue.js 3 + TypeScript + Composition API
    Supporting Projects: n8n, IT-Tools, Mealie, MISP (new frontend)

    Core Component Library Structure:
      - Layout Components: AppHeader, AppSidebar, AppFooter, PageLayout
      - Navigation: BreadcrumbNav, TabNav, MenuNav, Pagination
      - Forms: FormInput, FormSelect, FormTextarea, FormUpload
      - Data Display: DataTable, DataCard, DataList, StatCard
      - Feedback: AlertMessage, LoadingSpinner, ProgressBar, Toast
      - Interactive: ModalDialog, ConfirmDialog, ContextMenu, Tooltip
      - Domain-Specific: SecurityEventCard, WorkflowNode, ComboCard, RecipeCard

  UI Framework: Vuetify 3 + Custom Theme System
    Rationale:
      - Material Design 3 compliance
      - Comprehensive component set
      - Built-in accessibility features
      - TypeScript support
      - Customizable theme system

    Theme Configuration:
      ```typescript
      // themes/security.ts
      export const securityTheme = {
        dark: true,
        colors: {
          primary: '#1976d2',    // Blue for security
          secondary: '#424242',  // Gray
          accent: '#ff5722',     // Orange for alerts
          error: '#f44336',      // Red for errors
          warning: '#ff9800',    // Amber for warnings
          info: '#2196f3',       // Light blue for info
          success: '#4caf50'     // Green for success
        }
      }

      // themes/gaming.ts
      export const gamingTheme = {
        dark: false,
        colors: {
          primary: '#9c27b0',    // Purple for gaming
          secondary: '#673ab7',  // Deep purple
          accent: '#e91e63',     // Pink accent
          // ... other colors
        }
      }
      ```

Secondary Framework: React 18 + TypeScript
  Supporting Projects: Actual Budget, Commander Spellbook, Inspector
  Use Case: Complex state management, existing React ecosystem

  Component Library: Material-UI v5 + Styled Components
    - Maintains consistency with Vue.js Material Design
    - Shared design tokens and CSS variables
    - Cross-framework component documentation
````

## 4.2 State Management Standardization

````yaml
Vue.js State Management: Pinia + Composition API
  Store Structure by Domain:

    // stores/auth.ts
    export const useAuthStore = defineStore('auth', () => {
      const user = ref<User | null>(null)
      const permissions = ref<string[]>([])
      const currentDomain = ref<string>('security')

      const login = async (credentials: LoginRequest) => {
        // Login logic
      }

      const hasPermission = (permission: string) => {
        return permissions.value.includes(permission)
      }

      return { user, permissions, currentDomain, login, hasPermission }
    })

    // stores/security.ts
    export const useSecurityStore = defineStore('security', () => {
      const events = ref<SecurityEvent[]>([])
      const indicators = ref<Indicator[]>([])
      const cases = ref<SecurityCase[]>([])

      const fetchEvents = async (filters: EventFilters) => {
        // API call logic
      }

      return { events, indicators, cases, fetchEvents }
    })

    // stores/automation.ts
    export const useAutomationStore = defineStore('automation', () => {
      const workflows = ref<Workflow[]>([])
      const executions = ref<WorkflowExecution[]>([])
      const agents = ref<AgentSession[]>([])

      return { workflows, executions, agents }
    })

React State Management: Zustand + React Query
  Store Pattern:
    ```typescript
    // stores/authStore.ts
    interface AuthState {
      user: User | null
      permissions: string[]
      login: (credentials: LoginRequest) => Promise<void>
      logout: () => void
      hasPermission: (permission: string) => boolean
    }

    export const useAuthStore = create<AuthState>((set, get) => ({
      user: null,
      permissions: [],
      login: async (credentials) => {
        // Login logic
      },
      logout: () => set({ user: null, permissions: [] }),
      hasPermission: (permission) => get().permissions.includes(permission)
    }))
    ```

Cross-Framework State Synchronization:
  WebSocket Event Bus:
    - Real-time updates across all connected clients
    - Domain-specific channels for targeted updates
    - Optimistic updates with conflict resolution

  Shared State Schema:
    ```typescript
    interface GlobalState {
      auth: {
        user: User | null
        permissions: string[]
        currentDomain: string
      }
      notifications: Notification[]
      websocket: {
        connected: boolean
        channels: string[]
      }
    }
    ```
````

## 4.3 Routing & Navigation Architecture

````yaml
Vue.js Routing: Vue Router 4 + Domain-based Structure
  Route Structure:
    ```typescript
    // router/index.ts
    const routes = [
      {
        path: '/',
        component: () => import('@/layouts/DefaultLayout.vue'),
        children: [
          {
            path: '',
            redirect: '/dashboard'
          },
          {
            path: 'dashboard',
            component: () => import('@/pages/Dashboard.vue')
          }
        ]
      },
      {
        path: '/security',
        component: () => import('@/layouts/DomainLayout.vue'),
        meta: { domain: 'security', requiresAuth: true },
        children: [
          {
            path: 'events',
            component: () => import('@/pages/security/Events.vue'),
            meta: { permission: 'security:events:read' }
          },
          {
            path: 'indicators',
            component: () => import('@/pages/security/Indicators.vue')
          },
          {
            path: 'cases',
            component: () => import('@/pages/security/Cases.vue')
          }
        ]
      },
      {
        path: '/automation',
        component: () => import('@/layouts/DomainLayout.vue'),
        meta: { domain: 'automation' },
        children: [
          {
            path: 'workflows',
            component: () => import('@/pages/automation/Workflows.vue')
          },
          {
            path: 'agents',
            component: () => import('@/pages/automation/Agents.vue')
          }
        ]
      },
      {
        path: '/gaming',
        meta: { domain: 'gaming' },
        children: [
          {
            path: 'combos',
            component: () => import('@/pages/gaming/Combos.vue')
          },
          {
            path: 'cards',
            component: () => import('@/pages/gaming/Cards.vue')
          }
        ]
      },
      {
        path: '/tools',
        meta: { domain: 'productivity' },
        children: [
          {
            path: 'converters',
            component: () => import('@/pages/tools/Converters.vue')
          },
          {
            path: 'budget',
            component: () => import('@/pages/tools/Budget.vue')
          }
        ]
      }
    ]
    ```

Navigation Guards:
  ```typescript
  // middleware/auth.ts
  router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()

    if (to.meta.requiresAuth && !authStore.user) {
      return next('/login')
    }

    if (to.meta.permission && !authStore.hasPermission(to.meta.permission as string)) {
      return next('/unauthorized')
    }

    if (to.meta.domain) {
      authStore.setCurrentDomain(to.meta.domain as string)
    }

    next()
  })
````

Unified Navigation Component:

```vue
<template>
  <v-navigation-drawer v-model="drawer" app>
    <v-list>
      <domain-nav-section
        v-for="domain in availableDomains"
        :key="domain.name"
        :domain="domain"
        :active="currentDomain === domain.name"
      />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
interface NavigationDomain {
  name: string;
  label: string;
  icon: string;
  color: string;
  routes: NavigationRoute[];
}

const availableDomains = computed(() => [
  {
    name: 'security',
    label: 'Security Intelligence',
    icon: 'mdi-shield-check',
    color: 'blue',
    routes: [
      { path: '/security/events', label: 'Events', icon: 'mdi-alert' },
      { path: '/security/indicators', label: 'Indicators', icon: 'mdi-target' },
      { path: '/security/cases', label: 'Cases', icon: 'mdi-folder-open' },
    ],
  },
  {
    name: 'automation',
    label: 'Automation',
    icon: 'mdi-robot',
    color: 'green',
    routes: [
      { path: '/automation/workflows', label: 'Workflows', icon: 'mdi-flow-chart' },
      { path: '/automation/agents', label: 'AI Agents', icon: 'mdi-brain' },
    ],
  },
  {
    name: 'gaming',
    label: 'Gaming Tools',
    icon: 'mdi-cards-playing',
    color: 'purple',
    routes: [
      { path: '/gaming/combos', label: 'MTG Combos', icon: 'mdi-cards' },
      { path: '/gaming/cards', label: 'Card Search', icon: 'mdi-magnify' },
    ],
  },
]);
</script>
```

````

## 4.4 Build & Development Tooling

```yaml
Build Tool Standardization: Vite 5 + TypeScript
  Configuration Template:
    ```typescript
    // vite.config.ts
    import { defineConfig } from 'vite'
    import vue from '@vitejs/plugin-vue'
    import { resolve } from 'path'

    export default defineConfig({
      plugins: [
        vue(),
        // Domain-specific plugins
      ],
      resolve: {
        alias: {
          '@': resolve(__dirname, 'src'),
          '@shared': resolve(__dirname, '../../libs/shared'),
          '@ui': resolve(__dirname, '../../libs/ui')
        }
      },
      build: {
        outDir: 'dist',
        sourcemap: true,
        rollupOptions: {
          output: {
            manualChunks: {
              vendor: ['vue', 'vue-router', 'pinia'],
              ui: ['vuetify'],
              security: ['@/modules/security'],
              automation: ['@/modules/automation']
            }
          }
        }
      },
      server: {
        port: 3000,
        proxy: {
          '/api': {
            target: 'http://localhost:8000',
            changeOrigin: true
          },
          '/ws': {
            target: 'ws://localhost:8000',
            ws: true
          }
        }
      }
    })
    ```

Package Management: pnpm + Workspaces
  Workspace Structure:
    ```json
    {
      "name": "modular-monolith",
      "private": true,
      "workspaces": [
        "apps/*",
        "libs/*"
      ],
      "devDependencies": {
        "@types/node": "^20.0.0",
        "typescript": "^5.0.0",
        "vite": "^5.0.0",
        "vitest": "^1.0.0",
        "eslint": "^8.50.0",
        "prettier": "^3.0.0"
      },
      "scripts": {
        "dev": "pnpm -r --parallel dev",
        "build": "pnpm -r build",
        "test": "pnpm -r test",
        "lint": "pnpm -r lint"
      }
    }
    ```

Code Quality: ESLint + Prettier + Husky
  ESLint Configuration:
    ```json
    {
      "extends": [
        "@vue/eslint-config-typescript",
        "@vue/eslint-config-prettier",
        "plugin:security/recommended"
      ],
      "rules": {
        "@typescript-eslint/no-unused-vars": "error",
        "vue/component-name-in-template-casing": ["error", "PascalCase"],
        "vue/no-unused-components": "warn",
        "security/detect-object-injection": "error"
      },
      "overrides": [
        {
          "files": ["src/pages/security/**/*.vue"],
          "rules": {
            "security/detect-non-literal-regexp": "error"
          }
        }
      ]
    }
    ```

Testing Strategy:
  Unit Testing: Vitest + Vue Test Utils
  Component Testing: Cypress Component Testing
  E2E Testing: Playwright

  Test Structure:
    ```typescript
    // tests/components/SecurityEventCard.test.ts
    import { mount } from '@vue/test-utils'
    import { describe, it, expect } from 'vitest'
    import SecurityEventCard from '@/components/security/SecurityEventCard.vue'

    describe('SecurityEventCard', () => {
      it('displays event title and severity', () => {
        const wrapper = mount(SecurityEventCard, {
          props: {
            event: {
              id: '123',
              title: 'Test Event',
              severity: 'high',
              status: 'new'
            }
          }
        })

        expect(wrapper.find('.event-title').text()).toBe('Test Event')
        expect(wrapper.find('.severity-badge').classes()).toContain('severity-high')
      })
    })
    ```
````

## 4.5 Responsive Design & Accessibility

````yaml
Responsive Design System:
  Breakpoints (following Vuetify standards):
    - xs: 0-599px (mobile portrait)
    - sm: 600-959px (mobile landscape, small tablet)
    - md: 960-1263px (tablet, small laptop)
    - lg: 1264-1903px (desktop)
    - xl: 1904px+ (large desktop, 4K)

  Layout Patterns:
    Mobile-First Approach:
      - Single column layouts on mobile
      - Progressive enhancement for larger screens
      - Touch-friendly interfaces (44px minimum touch targets)
      - Collapsible navigation and sidebars

    Component Responsiveness:
      ```vue
      <template>
        <v-container fluid>
          <v-row>
            <v-col
              cols="12"
              sm="6"
              md="4"
              lg="3"
              v-for="event in events"
              :key="event.id"
            >
              <security-event-card :event="event" />
            </v-col>
          </v-row>
        </v-container>
      </template>
      ```

Accessibility Standards (WCAG 2.1 AA):
  Keyboard Navigation:
    - All interactive elements accessible via keyboard
    - Logical tab order throughout applications
    - Visible focus indicators
    - Escape key closes modals/menus

  Screen Reader Support:
    - Semantic HTML structure
    - ARIA labels and descriptions
    - Role attributes for custom components
    - Live regions for dynamic content updates

  Color & Contrast:
    - Minimum 4.5:1 contrast ratio for normal text
    - 3:1 contrast ratio for large text (18pt+)
    - Color not used as sole indicator of information
    - High contrast mode support

  Implementation Example:
    ```vue
    <template>
      <v-card
        :aria-label="`Security event: ${event.title}`"
        role="article"
        tabindex="0"
        @keydown.enter="openEvent"
        @keydown.space="openEvent"
      >
        <v-card-title>
          <v-icon
            :color="severityColor"
            :aria-label="`Severity: ${event.severity}`"
          >
            {{ severityIcon }}
          </v-icon>
          {{ event.title }}
        </v-card-title>

        <v-card-text>
          <span class="sr-only">Event description:</span>
          {{ event.description }}
        </v-card-text>

        <v-card-actions>
          <v-btn
            @click="openEvent"
            :aria-describedby="`event-${event.id}-description`"
          >
            View Details
          </v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <style scoped>
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    </style>
    ```

Internationalization (i18n):
  Vue I18n Implementation:
    ```typescript
    // locales/en.json
    {
      "security": {
        "events": {
          "title": "Security Events",
          "severity": {
            "low": "Low",
            "medium": "Medium",
            "high": "High",
            "critical": "Critical"
          }
        }
      },
      "automation": {
        "workflows": {
          "title": "Workflows",
          "status": {
            "running": "Running",
            "completed": "Completed"
          }
        }
      }
    }

    // Component usage
    <template>
      <h1>{{ $t('security.events.title') }}</h1>
      <span>{{ $t('security.events.severity.high') }}</span>
    </template>
    ```

---

# Section 5: Deployment & Infrastructure Architecture [CRITICAL]

## 5.1 Container Strategy & Orchestration

```yaml
Container Architecture: Docker + Docker Compose (Development) + Kubernetes (Production)

Development Deployment:
  Docker Compose Structure:
    ```yaml
    # docker-compose.yml
    version: '3.8'
    services:
      # Core Infrastructure
      postgres:
        image: postgres:15-alpine
        environment:
          POSTGRES_DB: modular_monolith
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
        volumes:
          - postgres_data:/var/lib/postgresql/data
          - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
        ports:
          - "5432:5432"
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U postgres"]
          interval: 30s
          timeout: 10s
          retries: 3

      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"
        command: redis-server --appendonly yes
        volumes:
          - redis_data:/data

      # Backend Services
      jane-orchestrator:
        build:
          context: ./apps/jane-orchestrator
          dockerfile: Dockerfile
        ports:
          - "8000:8000"
        environment:
          DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/modular_monolith
          REDIS_URL: redis://redis:6379/0
          JWT_SECRET: ${JWT_SECRET}
          ENVIRONMENT: development
        depends_on:
          - postgres
          - redis
        volumes:
          - ./apps/jane-orchestrator:/app
          - /app/node_modules  # Preserve node_modules
        command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

      # Frontend Application
      jane-ui:
        build:
          context: ./apps/jane-ui
          dockerfile: Dockerfile
        ports:
          - "3000:3000"
        environment:
          VITE_API_BASE_URL: http://localhost:8000
          VITE_WS_BASE_URL: ws://localhost:8000
        depends_on:
          - jane-orchestrator
        volumes:
          - ./apps/jane-ui:/app
          - /app/node_modules

      # Specialized LLM Services
      security-llm:
        build:
          context: ./apps/cyber-llm-server
          dockerfile: Dockerfile
        ports:
          - "8001:8000"
        environment:
          MODEL_PATH: /models
          CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES:-}
        volumes:
          - ./models:/models
          - ./apps/cyber-llm-server:/app
        deploy:
          resources:
            reservations:
              devices:
                - driver: nvidia
                  count: 1
                  capabilities: [gpu]

      mtg-llm:
        build:
          context: ./apps/mtg-llm-server
          dockerfile: Dockerfile
        ports:
          - "8002:8000"
        environment:
          MODEL_PATH: /models/mtg
        volumes:
          - ./models/mtg:/models
          - ./apps/mtg-llm-server:/app

      # Background Job Workers
      celery-worker:
        build:
          context: ./apps/jane-orchestrator
          dockerfile: Dockerfile
        command: celery -A src.workers.celery_app worker --loglevel=info
        environment:
          DATABASE_URL: postgresql://postgres:${POSTGRES_PASSWORD}@postgres:5432/modular_monolith
          REDIS_URL: redis://redis:6379/0
        depends_on:
          - postgres
          - redis
        volumes:
          - ./apps/jane-orchestrator:/app

      # Monitoring & Observability
      prometheus:
        image: prom/prometheus:latest
        ports:
          - "9090:9090"
        volumes:
          - ./infrastructure/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
          - prometheus_data:/prometheus
        command:
          - '--config.file=/etc/prometheus/prometheus.yml'
          - '--storage.tsdb.path=/prometheus'
          - '--web.console.libraries=/etc/prometheus/console_libraries'
          - '--web.console.templates=/etc/prometheus/consoles'

      grafana:
        image: grafana/grafana:latest
        ports:
          - "3001:3000"
        environment:
          GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
        volumes:
          - grafana_data:/var/lib/grafana
          - ./infrastructure/monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
          - ./infrastructure/monitoring/grafana/datasources:/etc/grafana/provisioning/datasources

    volumes:
      postgres_data:
      redis_data:
      prometheus_data:
      grafana_data:

    networks:
      default:
        driver: bridge
    ```

Production Kubernetes Deployment:
  Namespace Strategy:
    ```yaml
    # infrastructure/kubernetes/namespaces.yml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: modular-monolith-prod
      labels:
        environment: production
    ---
    apiVersion: v1
    kind: Namespace
    metadata:
      name: modular-monolith-staging
      labels:
        environment: staging
    ```

  Core Application Deployment:
    ```yaml
    # infrastructure/kubernetes/jane-orchestrator-deployment.yml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: jane-orchestrator
      namespace: modular-monolith-prod
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: jane-orchestrator
      template:
        metadata:
          labels:
            app: jane-orchestrator
        spec:
          containers:
          - name: jane-orchestrator
            image: modular-monolith/jane-orchestrator:latest
            ports:
            - containerPort: 8000
            env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: database-secrets
                  key: url
            - name: REDIS_URL
              valueFrom:
                configMapKeyRef:
                  name: app-config
                  key: redis-url
            resources:
              requests:
                memory: "512Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "500m"
            livenessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 30
              periodSeconds: 10
            readinessProbe:
              httpGet:
                path: /ready
                port: 8000
              initialDelaySeconds: 5
              periodSeconds: 5
    ---
    apiVersion: v1
    kind: Service
    metadata:
      name: jane-orchestrator-service
      namespace: modular-monolith-prod
    spec:
      selector:
        app: jane-orchestrator
      ports:
      - protocol: TCP
        port: 80
        targetPort: 8000
      type: ClusterIP
    ```

  Database Deployment (PostgreSQL with High Availability):
    ```yaml
    # infrastructure/kubernetes/postgres-cluster.yml
    apiVersion: postgresql.cnpg.io/v1
    kind: Cluster
    metadata:
      name: postgres-cluster
      namespace: modular-monolith-prod
    spec:
      instances: 3
      primaryUpdateStrategy: unsupervised

      postgresql:
        parameters:
          max_connections: "200"
          shared_buffers: "256MB"
          effective_cache_size: "1GB"

      bootstrap:
        initdb:
          database: modular_monolith
          owner: app_user
          secret:
            name: postgres-credentials

      storage:
        size: 100Gi
        storageClass: fast-ssd

      monitoring:
        enabled: true

      backup:
        retentionPolicy: "30d"
        barmanObjectStore:
          destinationPath: s3://backups/postgres
          s3Credentials:
            accessKeyId:
              name: backup-credentials
              key: ACCESS_KEY_ID
            secretAccessKey:
              name: backup-credentials
              key: SECRET_ACCESS_KEY
    ```
```

## 5.2 CI/CD Pipeline Architecture

```yaml
GitHub Actions Workflow:
  Multi-Environment Pipeline:
    ```yaml
    # .github/workflows/deploy.yml
    name: Deploy Modular Monolith

    on:
      push:
        branches: [main, develop]
      pull_request:
        branches: [main]

    env:
      REGISTRY: ghcr.io
      IMAGE_NAME: ${{ github.repository }}

    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            service: [jane-orchestrator, jane-ui, cyber-llm-server, mtg-llm-server]

        steps:
        - uses: actions/checkout@v4

        - name: Set up Node.js
          if: contains(matrix.service, 'ui')
          uses: actions/setup-node@v4
          with:
            node-version: '18'
            cache: 'npm'
            cache-dependency-path: apps/${{ matrix.service }}/package-lock.json

        - name: Set up Python
          if: contains(matrix.service, 'orchestrator') || contains(matrix.service, 'llm')
          uses: actions/setup-python@v4
          with:
            python-version: '3.11'

        - name: Install dependencies
          run: |
            cd apps/${{ matrix.service }}
            if [ -f package.json ]; then
              npm ci
            elif [ -f requirements.txt ]; then
              pip install -r requirements.txt
            fi

        - name: Run tests
          run: |
            cd apps/${{ matrix.service }}
            if [ -f package.json ]; then
              npm run test
            else
              pytest
            fi

        - name: Run security scan
          uses: github/super-linter@v4
          env:
            DEFAULT_BRANCH: main
            GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            VALIDATE_PYTHON: true
            VALIDATE_TYPESCRIPT: true
            VALIDATE_DOCKERFILE: true

      build:
        needs: test
        runs-on: ubuntu-latest
        if: github.event_name == 'push'

        strategy:
          matrix:
            service: [jane-orchestrator, jane-ui, cyber-llm-server, mtg-llm-server]

        steps:
        - uses: actions/checkout@v4

        - name: Log in to Container Registry
          uses: docker/login-action@v2
          with:
            registry: ${{ env.REGISTRY }}
            username: ${{ github.actor }}
            password: ${{ secrets.GITHUB_TOKEN }}

        - name: Extract metadata
          id: meta
          uses: docker/metadata-action@v4
          with:
            images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/${{ matrix.service }}
            tags: |
              type=ref,event=branch
              type=ref,event=pr
              type=sha,prefix=sha-

        - name: Build and push Docker image
          uses: docker/build-push-action@v4
          with:
            context: ./apps/${{ matrix.service }}
            push: true
            tags: ${{ steps.meta.outputs.tags }}
            labels: ${{ steps.meta.outputs.labels }}

      deploy-staging:
        needs: build
        runs-on: ubuntu-latest
        if: github.ref == 'refs/heads/develop'
        environment: staging

        steps:
        - uses: actions/checkout@v4

        - name: Configure kubectl
          uses: azure/k8s-set-context@v1
          with:
            method: kubeconfig
            kubeconfig: ${{ secrets.KUBE_CONFIG }}
            context: staging-cluster

        - name: Deploy to staging
          run: |
            # Update image tags in k8s manifests
            sed -i "s|image: .*jane-orchestrator.*|image: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/jane-orchestrator:sha-${{ github.sha }}|" infrastructure/kubernetes/staging/jane-orchestrator-deployment.yml

            # Apply manifests
            kubectl apply -f infrastructure/kubernetes/staging/

            # Wait for deployment
            kubectl rollout status deployment/jane-orchestrator -n modular-monolith-staging

        - name: Run smoke tests
          run: |
            # Wait for service to be ready
            kubectl wait --for=condition=ready pod -l app=jane-orchestrator -n modular-monolith-staging --timeout=300s

            # Run smoke tests
            curl -f http://staging.modular-monolith.com/health || exit 1

      deploy-production:
        needs: build
        runs-on: ubuntu-latest
        if: github.ref == 'refs/heads/main'
        environment: production

        steps:
        - uses: actions/checkout@v4

        - name: Configure kubectl
          uses: azure/k8s-set-context@v1
          with:
            method: kubeconfig
            kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
            context: production-cluster

        - name: Deploy to production
          run: |
            # Blue-green deployment strategy
            ./scripts/blue-green-deploy.sh ${{ github.sha }}

        - name: Verify deployment
          run: |
            # Health checks and verification
            ./scripts/verify-deployment.sh production

        - name: Rollback on failure
          if: failure()
          run: |
            ./scripts/rollback-deployment.sh
    ```

Blue-Green Deployment Script:
  ```bash
  #!/bin/bash
  # scripts/blue-green-deploy.sh

  set -e

  COMMIT_SHA=$1
  NAMESPACE="modular-monolith-prod"

  # Determine current active environment
  CURRENT_ENV=$(kubectl get service jane-orchestrator-service -n $NAMESPACE -o jsonpath='{.spec.selector.environment}')

  if [ "$CURRENT_ENV" = "blue" ]; then
    NEW_ENV="green"
  else
    NEW_ENV="blue"
  fi

  echo "Deploying to $NEW_ENV environment (current: $CURRENT_ENV)"

  # Update deployment manifests with new environment and image
  sed -i "s/environment: .*/environment: $NEW_ENV/" infrastructure/kubernetes/production/jane-orchestrator-deployment.yml
  sed -i "s|image: .*jane-orchestrator.*|image: ghcr.io/mbarnes-code/modular-monolith-2/jane-orchestrator:sha-$COMMIT_SHA|" infrastructure/kubernetes/production/jane-orchestrator-deployment.yml

  # Apply new deployment
  kubectl apply -f infrastructure/kubernetes/production/jane-orchestrator-deployment.yml

  # Wait for new deployment to be ready
  kubectl rollout status deployment/jane-orchestrator-$NEW_ENV -n $NAMESPACE --timeout=600s

  # Run health checks
  echo "Running health checks on $NEW_ENV environment..."
  for i in {1..10}; do
    if curl -f http://jane-orchestrator-$NEW_ENV.$NAMESPACE.svc.cluster.local/health; then
      echo "Health check passed"
      break
    fi
    echo "Health check attempt $i failed, retrying in 10 seconds..."
    sleep 10
  done

  # Switch traffic to new environment
  kubectl patch service jane-orchestrator-service -n $NAMESPACE -p '{"spec":{"selector":{"environment":"'$NEW_ENV'"}}}'

  echo "Traffic switched to $NEW_ENV environment"

  # Wait and verify
  sleep 30

  # Scale down old environment
  kubectl scale deployment jane-orchestrator-$CURRENT_ENV -n $NAMESPACE --replicas=0

  echo "Blue-green deployment completed successfully"
  ```
```

## 5.3 Environment Configuration Management

```yaml
Configuration Strategy: Kubernetes ConfigMaps + Secrets + External Secret Management

Environment Hierarchy:
  1. Base Configuration (shared across all environments)
  2. Environment-specific overrides (dev/staging/prod)
  3. Feature flags and dynamic configuration
  4. Secrets management (Vault/AWS Secrets Manager)

ConfigMap Structure:
  ```yaml
  # infrastructure/kubernetes/config/base-config.yml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: app-config-base
    namespace: modular-monolith-prod
  data:
    # API Configuration
    API_VERSION: "v1"
    API_TIMEOUT: "30s"
    API_RATE_LIMIT: "1000"

    # Database Configuration
    DB_POOL_SIZE: "20"
    DB_MAX_OVERFLOW: "30"
    DB_POOL_TIMEOUT: "30"

    # Redis Configuration
    REDIS_MAX_CONNECTIONS: "100"
    REDIS_TIMEOUT: "5s"

    # Security Configuration
    JWT_EXPIRY_HOURS: "24"
    REFRESH_TOKEN_EXPIRY_DAYS: "30"
    PASSWORD_MIN_LENGTH: "8"

    # Feature Flags
    ENABLE_SECURITY_DOMAIN: "true"
    ENABLE_AUTOMATION_DOMAIN: "true"
    ENABLE_GAMING_DOMAIN: "true"
    ENABLE_PRODUCTIVITY_DOMAIN: "true"
    ENABLE_AI_AGENTS: "true"
    ENABLE_ADVANCED_ANALYTICS: "false"

    # Logging Configuration
    LOG_LEVEL: "INFO"
    LOG_FORMAT: "json"

    # External Service URLs
    SCRYFALL_API_URL: "https://api.scryfall.com"
    VIRUSTOTAL_API_URL: "https://www.virustotal.com/vtapi/v2"

  ---
  # Production-specific overrides
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: app-config-prod
    namespace: modular-monolith-prod
  data:
    LOG_LEVEL: "WARN"
    API_RATE_LIMIT: "5000"
    DB_POOL_SIZE: "50"
    ENABLE_DEBUG_ENDPOINTS: "false"
    SENTRY_ENVIRONMENT: "production"
  ```

Secrets Management:
  ```yaml
  # infrastructure/kubernetes/secrets/app-secrets.yml
  apiVersion: v1
  kind: Secret
  metadata:
    name: app-secrets
    namespace: modular-monolith-prod
  type: Opaque
  data:
    # Base64 encoded values
    DATABASE_URL: cG9zdGdyZXNxbDovL3VzZXI6cGFzcw==
    REDIS_URL: cmVkaXM6Ly9sb2NhbGhvc3Q6NjM3OS8w
    JWT_SECRET: c3VwZXItc2VjcmV0LWp3dC1rZXk=
    ENCRYPTION_KEY: YWVzLTI1Ni1lbmNyeXB0aW9uLWtleQ==

    # External API Keys
    VIRUSTOTAL_API_KEY: dnQtYXBpLWtleS1oZXJl
    DISCORD_BOT_TOKEN: ZGlzY29yZC1ib3QtdG9rZW4=
    OPENAI_API_KEY: b3BlbmFpLWFwaS1rZXk=

    # Cloud Provider Credentials
    AWS_ACCESS_KEY_ID: YXdzLWFjY2Vzcy1rZXk=
    AWS_SECRET_ACCESS_KEY: YXdzLXNlY3JldC1hY2Nlc3Mta2V5

    # Monitoring Credentials
    SENTRY_DSN: aHR0cHM6Ly9zZW50cnktZHNu
    PROMETHEUS_AUTH_TOKEN: cHJvbS1hdXRoLXRva2Vu

External Secrets Integration (AWS Secrets Manager):
  ```yaml
  # infrastructure/kubernetes/external-secrets/aws-secrets.yml
  apiVersion: external-secrets.io/v1beta1
  kind: SecretStore
  metadata:
    name: aws-secrets-store
    namespace: modular-monolith-prod
  spec:
    provider:
      aws:
        service: SecretsManager
        region: us-east-1
        auth:
          secretRef:
            accessKeyID:
              name: aws-credentials
              key: access-key-id
            secretAccessKey:
              name: aws-credentials
              key: secret-access-key

  ---
  apiVersion: external-secrets.io/v1beta1
  kind: ExternalSecret
  metadata:
    name: database-credentials
    namespace: modular-monolith-prod
  spec:
    refreshInterval: 15s
    secretStoreRef:
      name: aws-secrets-store
      kind: SecretStore
    target:
      name: database-secrets
      creationPolicy: Owner
    data:
    - secretKey: url
      remoteRef:
        key: modular-monolith/database
        property: connection_url
    - secretKey: username
      remoteRef:
        key: modular-monolith/database
        property: username
    - secretKey: password
      remoteRef:
        key: modular-monolith/database
        property: password
  ```

Application Configuration Loading:
  ```python
  # apps/jane-orchestrator/src/config/settings.py
  from pydantic import BaseSettings, Field
  from typing import List, Optional
  import os

  class DatabaseConfig(BaseSettings):
      url: str = Field(..., env="DATABASE_URL")
      pool_size: int = Field(20, env="DB_POOL_SIZE")
      max_overflow: int = Field(30, env="DB_MAX_OVERFLOW")
      pool_timeout: int = Field(30, env="DB_POOL_TIMEOUT")

  class RedisConfig(BaseSettings):
      url: str = Field(..., env="REDIS_URL")
      max_connections: int = Field(100, env="REDIS_MAX_CONNECTIONS")
      timeout: int = Field(5, env="REDIS_TIMEOUT")

  class SecurityConfig(BaseSettings):
      jwt_secret: str = Field(..., env="JWT_SECRET")
      jwt_expiry_hours: int = Field(24, env="JWT_EXPIRY_HOURS")
      encryption_key: str = Field(..., env="ENCRYPTION_KEY")
      password_min_length: int = Field(8, env="PASSWORD_MIN_LENGTH")

  class FeatureFlags(BaseSettings):
      enable_security_domain: bool = Field(True, env="ENABLE_SECURITY_DOMAIN")
      enable_automation_domain: bool = Field(True, env="ENABLE_AUTOMATION_DOMAIN")
      enable_gaming_domain: bool = Field(True, env="ENABLE_GAMING_DOMAIN")
      enable_productivity_domain: bool = Field(True, env="ENABLE_PRODUCTIVITY_DOMAIN")
      enable_ai_agents: bool = Field(True, env="ENABLE_AI_AGENTS")
      enable_advanced_analytics: bool = Field(False, env="ENABLE_ADVANCED_ANALYTICS")

  class ExternalServices(BaseSettings):
      scryfall_api_url: str = Field("https://api.scryfall.com", env="SCRYFALL_API_URL")
      virustotal_api_key: Optional[str] = Field(None, env="VIRUSTOTAL_API_KEY")
      openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")

  class Settings(BaseSettings):
      # Environment
      environment: str = Field("development", env="ENVIRONMENT")
      debug: bool = Field(False, env="DEBUG")

      # API Configuration
      api_version: str = Field("v1", env="API_VERSION")
      api_timeout: int = Field(30, env="API_TIMEOUT")
      api_rate_limit: int = Field(1000, env="API_RATE_LIMIT")

      # Nested configurations
      database: DatabaseConfig = DatabaseConfig()
      redis: RedisConfig = RedisConfig()
      security: SecurityConfig = SecurityConfig()
      features: FeatureFlags = FeatureFlags()
      external: ExternalServices = ExternalServices()

      # Logging
      log_level: str = Field("INFO", env="LOG_LEVEL")
      log_format: str = Field("json", env="LOG_FORMAT")

      class Config:
          env_file = ".env"
          env_file_encoding = "utf-8"
          case_sensitive = False

  # Global settings instance
  settings = Settings()
  ```

---

# Section 6: Security Architecture & Compliance [CRITICAL]

## 6.1 Authentication & Authorization Framework

```yaml
Multi-Domain Security Model:
  Authentication Providers:
    Primary: JWT + Refresh Token
    Secondary: OAuth2 (Discord, GitHub, Google)
    Enterprise: LDAP/Active Directory, SAML 2.0
    API Access: API Keys with scoped permissions

  Authorization Implementation:
    ```python
    # apps/jane-orchestrator/src/auth/models.py
    from sqlalchemy import Column, String, Boolean, DateTime, JSON
    from sqlalchemy.dialects.postgresql import UUID
    import uuid

    class Permission(Base):
        __tablename__ = "permissions"

        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        name = Column(String(100), unique=True, nullable=False)
        resource = Column(String(50), nullable=False)  # events, workflows, combos
        action = Column(String(20), nullable=False)    # create, read, update, delete
        domain = Column(String(50), nullable=False)    # security, automation, gaming

        @property
        def full_name(self):
            return f"{self.domain}:{self.resource}:{self.action}"

    class Role(Base):
        __tablename__ = "roles"

        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        name = Column(String(100), nullable=False)
        domain = Column(String(50), nullable=False)
        description = Column(String(500))
        permissions = Column(JSON, default=list)  # List of permission IDs
        is_system_role = Column(Boolean, default=False)

        def has_permission(self, permission: str) -> bool:
            return permission in self.permissions

    # Domain-specific role definitions
    SECURITY_ROLES = [
        {
            "name": "security_admin",
            "domain": "security",
            "permissions": [
                "security:events:create", "security:events:read",
                "security:events:update", "security:events:delete",
                "security:indicators:create", "security:indicators:read",
                "security:indicators:update", "security:indicators:delete",
                "security:cases:create", "security:cases:read",
                "security:cases:update", "security:cases:delete",
                "security:users:manage", "security:settings:manage"
            ]
        },
        {
            "name": "security_analyst",
            "domain": "security",
            "permissions": [
                "security:events:create", "security:events:read", "security:events:update",
                "security:indicators:create", "security:indicators:read", "security:indicators:update",
                "security:cases:create", "security:cases:read", "security:cases:update"
            ]
        }
    ]

    AUTOMATION_ROLES = [
        {
            "name": "automation_admin",
            "domain": "automation",
            "permissions": [
                "automation:workflows:create", "automation:workflows:read",
                "automation:workflows:update", "automation:workflows:delete",
                "automation:credentials:manage", "automation:agents:manage",
                "automation:executions:view_all"
            ]
        }
    ]
    ```

Permission Enforcement Middleware:
  ```python
  # apps/jane-orchestrator/src/auth/middleware.py
  from fastapi import Request, HTTPException, Depends
  from functools import wraps
  import jwt

  class PermissionChecker:
      def __init__(self, required_permission: str):
          self.required_permission = required_permission

      def __call__(self, request: Request, current_user = Depends(get_current_user)):
          if not current_user:
              raise HTTPException(status_code=401, detail="Authentication required")

          # Check if user has required permission
          user_permissions = self.get_user_permissions(current_user)

          if self.required_permission not in user_permissions:
              raise HTTPException(
                  status_code=403,
                  detail=f"Permission denied. Required: {self.required_permission}"
              )

          return current_user

      def get_user_permissions(self, user) -> List[str]:
          permissions = []
          for role in user.roles:
              permissions.extend(role.permissions)
          return list(set(permissions))  # Remove duplicates

  # Usage in API endpoints
  @router.post("/security/events")
  async def create_security_event(
      event_data: SecurityEventCreate,
      user = Depends(PermissionChecker("security:events:create"))
  ):
      # Create event logic
      pass

  @router.get("/automation/workflows")
  async def list_workflows(
      user = Depends(PermissionChecker("automation:workflows:read"))
  ):
      # List workflows logic
      pass
  ```

API Key Management:
  ```python
  # apps/jane-orchestrator/src/auth/api_keys.py
  import secrets
  import hashlib
  from datetime import datetime, timedelta

  class APIKeyManager:
      @staticmethod
      def generate_api_key() -> tuple[str, str]:
          """Generate API key and return (key, hash)"""
          # Generate random key
          key = f"mm_{secrets.token_urlsafe(32)}"

          # Create hash for storage
          key_hash = hashlib.sha256(key.encode()).hexdigest()

          return key, key_hash

      @staticmethod
      def validate_api_key(provided_key: str, stored_hash: str) -> bool:
          """Validate provided key against stored hash"""
          provided_hash = hashlib.sha256(provided_key.encode()).hexdigest()
          return secrets.compare_digest(provided_hash, stored_hash)

      @classmethod
      def create_api_key(
          cls,
          user_id: str,
          name: str,
          scopes: List[str],
          expires_days: int = 365
      ) -> APIKey:
          """Create new API key for user"""
          key, key_hash = cls.generate_api_key()

          api_key = APIKey(
              user_id=user_id,
              name=name,
              key_hash=key_hash,
              key_prefix=key[:10] + "...",  # For display
              scopes=scopes,
              expires_at=datetime.utcnow() + timedelta(days=expires_days)
          )

          return api_key, key  # Return model and raw key
  ```
```

## 6.2 Data Protection & Encryption

```yaml
Encryption Strategy:
  Data at Rest:
    - Database: PostgreSQL with TDE (Transparent Data Encryption)
    - File Storage: AES-256 encryption for uploaded files
    - Secrets: Kubernetes secrets + external secret management
    - Backups: Encrypted with separate key rotation

  Data in Transit:
    - TLS 1.3 for all HTTP communications
    - WebSocket connections over WSS
    - Database connections over SSL
    - Inter-service communication with mTLS

  Application-Level Encryption:
    ```python
    # apps/jane-orchestrator/src/security/encryption.py
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    import base64
    import os

    class EncryptionManager:
        def __init__(self, master_key: bytes):
            self.master_key = master_key
            self._fernet = None

        @property
        def fernet(self) -> Fernet:
            if self._fernet is None:
                # Derive key from master key
                kdf = PBKDF2HMAC(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=b'stable_salt',  # In production, use proper salt management
                    iterations=100000,
                )
                key = base64.urlsafe_b64encode(kdf.derive(self.master_key))
                self._fernet = Fernet(key)
            return self._fernet

        def encrypt_sensitive_data(self, data: str) -> str:
            """Encrypt sensitive data like API keys, passwords"""
            encrypted_data = self.fernet.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_data).decode()

        def decrypt_sensitive_data(self, encrypted_data: str) -> str:
            """Decrypt sensitive data"""
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_data = self.fernet.decrypt(encrypted_bytes)
            return decrypted_data.decode()

        def encrypt_workflow_credentials(self, credentials: dict) -> str:
            """Encrypt workflow credentials (n8n style)"""
            import json
            credentials_json = json.dumps(credentials)
            return self.encrypt_sensitive_data(credentials_json)

        def decrypt_workflow_credentials(self, encrypted_credentials: str) -> dict:
            """Decrypt workflow credentials"""
            import json
            credentials_json = self.decrypt_sensitive_data(encrypted_credentials)
            return json.loads(credentials_json)

    # Usage in models
    class WorkflowCredentials(Base):
        __tablename__ = "workflow_credentials"

        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        name = Column(String(255), nullable=False)
        credential_type = Column(String(100), nullable=False)
        encrypted_data = Column(Text, nullable=False)  # Encrypted JSON

        def set_credentials(self, credentials: dict, encryption_manager: EncryptionManager):
            """Set credentials with encryption"""
            self.encrypted_data = encryption_manager.encrypt_workflow_credentials(credentials)

        def get_credentials(self, encryption_manager: EncryptionManager) -> dict:
            """Get decrypted credentials"""
            return encryption_manager.decrypt_workflow_credentials(self.encrypted_data)
    ```

PII Data Handling:
  ```python
  # apps/jane-orchestrator/src/security/pii.py
  from typing import Dict, Any
  import re
  import hashlib

  class PIIProcessor:
      """Handle Personally Identifiable Information"""

      EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
      IP_PATTERN = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
      PHONE_PATTERN = re.compile(r'\b\d{3}-\d{3}-\d{4}\b')
      SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')

      @classmethod
      def anonymize_text(cls, text: str, preserve_format: bool = True) -> str:
          """Anonymize PII in text while preserving format for analysis"""

          # Replace emails with hashed versions
          def hash_email(match):
              email = match.group(0)
              if preserve_format:
                  local, domain = email.split('@')
                  hashed_local = hashlib.md5(local.encode()).hexdigest()[:8]
                  return f"{hashed_local}@{domain}"
              return "***EMAIL***"

          text = cls.EMAIL_PATTERN.sub(hash_email, text)

          # Replace IPs with network ranges for security analysis
          if preserve_format:
              text = cls.IP_PATTERN.sub(lambda m: cls._anonymize_ip(m.group(0)), text)
          else:
              text = cls.IP_PATTERN.sub("***IP***", text)

          # Replace phones and SSNs
          text = cls.PHONE_PATTERN.sub("***-***-****", text)
          text = cls.SSN_PATTERN.sub("***-**-****", text)

          return text

      @staticmethod
      def _anonymize_ip(ip: str) -> str:
          """Anonymize IP while preserving network for security analysis"""
          parts = ip.split('.')
          # Keep first two octets for network analysis
          return f"{parts[0]}.{parts[1]}.xxx.xxx"

      @classmethod
      def sanitize_security_event(cls, event_data: Dict[str, Any]) -> Dict[str, Any]:
          """Sanitize security event data before storage/sharing"""
          sanitized = event_data.copy()

          # Sanitize common fields
          if 'description' in sanitized:
              sanitized['description'] = cls.anonymize_text(sanitized['description'])

          if 'raw_data' in sanitized:
              sanitized['raw_data'] = cls.anonymize_text(sanitized['raw_data'])

          # Handle indicators separately - preserve structure for analysis
          if 'indicators' in sanitized:
              sanitized['indicators'] = [
                  cls._sanitize_indicator(indicator)
                  for indicator in sanitized['indicators']
              ]

          return sanitized

      @classmethod
      def _sanitize_indicator(cls, indicator: Dict[str, Any]) -> Dict[str, Any]:
          """Sanitize individual indicators"""
          sanitized = indicator.copy()

          # For some indicator types, we want to preserve structure
          if indicator.get('type') == 'ip':
              sanitized['value'] = cls._anonymize_ip(indicator['value'])
          elif indicator.get('type') == 'email':
              sanitized['value'] = cls.anonymize_text(indicator['value'], preserve_format=True)
          # Hashes and domains can be kept as-is for security analysis

          return sanitized
  ```
```

## 6.3 Security Monitoring & Incident Response

```yaml
Security Event Detection:
  Real-time Monitoring:
    - Failed authentication attempts
    - Privilege escalation attempts
    - Unusual API usage patterns
    - Data access anomalies
    - Workflow execution anomalies

  Implementation:
    ```python
    # apps/jane-orchestrator/src/security/monitoring.py
    from datetime import datetime, timedelta
    from collections import defaultdict
    import asyncio

    class SecurityMonitor:
        def __init__(self):
            self.failed_attempts = defaultdict(list)
            self.api_usage = defaultdict(list)
            self.alerts = []

        async def log_authentication_attempt(
            self,
            user_id: str,
            success: bool,
            ip_address: str,
            user_agent: str
        ):
            """Log and analyze authentication attempts"""

            if not success:
                # Track failed attempts
                self.failed_attempts[ip_address].append(datetime.utcnow())

                # Check for brute force
                recent_failures = [
                    attempt for attempt in self.failed_attempts[ip_address]
                    if attempt > datetime.utcnow() - timedelta(minutes=15)
                ]

                if len(recent_failures) >= 5:
                    await self.create_security_alert(
                        alert_type="brute_force_attempt",
                        severity="high",
                        details={
                            "ip_address": ip_address,
                            "failed_attempts": len(recent_failures),
                            "user_agent": user_agent,
                            "time_window": "15 minutes"
                        }
                    )

        async def log_api_request(
            self,
            user_id: str,
            endpoint: str,
            method: str,
            response_status: int,
            response_time_ms: int
        ):
            """Monitor API usage patterns"""

            current_time = datetime.utcnow()
            self.api_usage[user_id].append({
                "timestamp": current_time,
                "endpoint": endpoint,
                "method": method,
                "status": response_status,
                "response_time": response_time_ms
            })

            # Check for unusual patterns
            await self._analyze_api_usage(user_id)

        async def _analyze_api_usage(self, user_id: str):
            """Analyze API usage for anomalies"""
            recent_requests = [
                req for req in self.api_usage[user_id]
                if req["timestamp"] > datetime.utcnow() - timedelta(minutes=10)
            ]

            # Check rate limits
            if len(recent_requests) > 1000:  # 100 requests per minute
                await self.create_security_alert(
                    alert_type="rate_limit_exceeded",
                    severity="medium",
                    details={
                        "user_id": user_id,
                        "request_count": len(recent_requests),
                        "time_window": "10 minutes"
                    }
                )

            # Check for error patterns
            error_count = len([req for req in recent_requests if req["status"] >= 400])
            if error_count > 50:  # High error rate
                await self.create_security_alert(
                    alert_type="high_error_rate",
                    severity="medium",
                    details={
                        "user_id": user_id,
                        "error_count": error_count,
                        "total_requests": len(recent_requests)
                    }
                )

        async def monitor_data_access(
            self,
            user_id: str,
            resource_type: str,
            action: str,
            resource_id: str = None
        ):
            """Monitor sensitive data access"""

            # Log access attempt
            access_log = {
                "timestamp": datetime.utcnow(),
                "user_id": user_id,
                "resource_type": resource_type,
                "action": action,
                "resource_id": resource_id
            }

            # Check for privilege escalation
            if action in ["delete", "update"] and resource_type == "users":
                await self.create_security_alert(
                    alert_type="privilege_escalation_attempt",
                    severity="high",
                    details=access_log
                )

            # Check for bulk data access
            recent_access = self._get_recent_access(user_id, resource_type)
            if len(recent_access) > 100:  # Bulk access pattern
                await self.create_security_alert(
                    alert_type="bulk_data_access",
                    severity="medium",
                    details={
                        "user_id": user_id,
                        "resource_type": resource_type,
                        "access_count": len(recent_access)
                    }
                )

        async def create_security_alert(
            self,
            alert_type: str,
            severity: str,
            details: dict
        ):
            """Create and process security alert"""

            alert = {
                "id": str(uuid.uuid4()),
                "type": alert_type,
                "severity": severity,
                "details": details,
                "timestamp": datetime.utcnow(),
                "status": "new"
            }

            # Store alert
            self.alerts.append(alert)

            # Auto-response for critical alerts
            if severity == "critical":
                await self._execute_auto_response(alert)

            # Notify security team
            await self._notify_security_team(alert)

        async def _execute_auto_response(self, alert: dict):
            """Execute automated response to critical security events"""

            if alert["type"] == "brute_force_attempt":
                # Temporarily block IP
                ip_address = alert["details"]["ip_address"]
                await self._block_ip_address(ip_address, duration_minutes=30)

            elif alert["type"] == "privilege_escalation_attempt":
                # Disable user account temporarily
                user_id = alert["details"]["user_id"]
                await self._temporarily_disable_user(user_id)

        async def _notify_security_team(self, alert: dict):
            """Notify security team of alerts"""
            # Implementation depends on notification system
            # Could use email, Slack, PagerDuty, etc.
            pass
    ```

Compliance Framework:
  ```yaml
  # GDPR Compliance
  GDPR_Requirements:
    Data Subject Rights:
      - Right to Access: API endpoints for users to download their data
      - Right to Rectification: User profile editing capabilities
      - Right to Erasure: Account deletion with data purging
      - Right to Portability: Data export in machine-readable format
      - Right to Object: Opt-out mechanisms for data processing

    Implementation:
      ```python
      # apps/jane-orchestrator/src/compliance/gdpr.py
      class GDPRService:
          async def export_user_data(self, user_id: str) -> dict:
              """Export all user data for GDPR compliance"""
              user_data = {
                  "user_profile": await self._get_user_profile(user_id),
                  "security_events": await self._get_user_security_events(user_id),
                  "workflows": await self._get_user_workflows(user_id),
                  "api_keys": await self._get_user_api_keys(user_id),
                  "audit_logs": await self._get_user_audit_logs(user_id)
              }
              return user_data

          async def delete_user_data(self, user_id: str, retention_period_days: int = 30):
              """Delete user data with proper retention handling"""

              # Mark for deletion (soft delete initially)
              await self._mark_user_for_deletion(user_id)

              # Schedule hard deletion after retention period
              await self._schedule_hard_deletion(user_id, retention_period_days)

              # Anonymize data that must be retained for legal/security reasons
              await self._anonymize_retained_data(user_id)
      ```

  # SOC 2 Compliance
  SOC2_Requirements:
    Security:
      - Multi-factor authentication
      - Role-based access controls
      - Encryption in transit and at rest
      - Security monitoring and incident response

    Availability:
      - System monitoring and alerting
      - Backup and disaster recovery procedures
      - Capacity planning and scaling

    Processing Integrity:
      - Data validation and error handling
      - Audit logging of all data changes
      - Automated testing and deployment

    Confidentiality:
      - Data classification and handling procedures
      - Access logging and monitoring
      - Secure development practices

    Privacy:
      - Privacy policy and user consent management
      - Data retention and deletion procedures
      - Third-party data sharing agreements

  # Audit Logging
  Audit_Implementation:
    ```python
    # apps/jane-orchestrator/src/audit/logging.py
    class AuditLogger:
        async def log_user_action(
            self,
            user_id: str,
            action: str,
            resource_type: str,
            resource_id: str = None,
            before_state: dict = None,
            after_state: dict = None,
            ip_address: str = None,
            user_agent: str = None
        ):
            """Log user actions for audit trail"""

            audit_entry = {
                "timestamp": datetime.utcnow(),
                "user_id": user_id,
                "action": action,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "before_state": before_state,
                "after_state": after_state,
                "ip_address": ip_address,
                "user_agent": user_agent,
                "session_id": self._get_session_id()
            }

            # Store in audit log table
            await self._store_audit_entry(audit_entry)

            # Send to external audit system if configured
            if self.external_audit_enabled:
                await self._send_to_external_audit(audit_entry)
    ```
  ```

---

# Section 7: Migration Strategy & Implementation Roadmap [CRITICAL]

## 7.1 Phased Migration Approach

```yaml
Migration Strategy: Strangler Fig Pattern + Domain-Driven Migration

Phase 1: Foundation & Core Infrastructure (Months 1-2)
  Week 1-2: Infrastructure Setup
    - Set up development environment with Docker Compose
    - Configure PostgreSQL database with unified schema
    - Set up Redis for caching and job queues
    - Implement basic CI/CD pipeline
    - Create base FastAPI application structure

  Week 3-4: Authentication & Authorization
    - Implement JWT-based authentication system
    - Create role-based access control (RBAC)
    - Set up user management APIs
    - Implement API key management
    - Create basic Vue.js frontend with auth

  Week 5-6: Core Services Foundation
    - Implement background job system (Celery)
    - Set up WebSocket infrastructure for real-time updates
    - Create shared libraries and utilities
    - Implement logging and monitoring basics
    - Set up basic security monitoring

  Week 7-8: Testing & Documentation
    - Comprehensive test suite setup
    - API documentation generation
    - Security testing framework
    - Performance baseline establishment
    - Documentation and deployment guides

Phase 2: Security Domain Migration (Months 3-4)
  Priority Projects: MISP, Dispatch, Maltrail, HELK

  Month 3: Security Events & Indicators
    - Migrate MISP event model to unified schema
    - Implement security events API
    - Create indicators/IOCs management system
    - Build threat intelligence feeds integration
    - Develop security event correlation engine

  Month 4: Incident Management & Cases
    - Migrate Dispatch incident management
    - Implement security cases workflow
    - Create case timeline and collaboration features
    - Integrate with external security tools
    - Build security dashboard and reporting

  Migration Process:
    ```python
    # scripts/migrate_misp_events.py
    async def migrate_misp_events():
        """Migrate MISP events to unified schema"""

        # Connect to legacy MISP database
        misp_db = await connect_to_misp_db()

        # Connect to new unified database
        unified_db = await connect_to_unified_db()

        # Batch process events
        batch_size = 1000
        offset = 0

        while True:
            # Fetch batch of MISP events
            misp_events = await misp_db.fetch_events(limit=batch_size, offset=offset)

            if not misp_events:
                break

            # Transform to unified schema
            unified_events = []
            for misp_event in misp_events:
                unified_event = {
                    "id": str(uuid.uuid4()),
                    "event_type": "misp_event",
                    "title": misp_event["info"],
                    "description": misp_event.get("comment", ""),
                    "tlp_level": misp_event.get("tlp", "WHITE"),
                    "severity": map_misp_threat_level(misp_event["threat_level_id"]),
                    "occurred_at": parse_misp_date(misp_event["date"]),
                    "event_data": {
                        "misp_id": misp_event["id"],
                        "org_id": misp_event["org_id"],
                        "distribution": misp_event["distribution"],
                        "analysis": misp_event["analysis"],
                        "attributes": misp_event.get("attributes", [])
                    },
                    "tags": extract_misp_tags(misp_event),
                    "source_system": "misp",
                    "external_id": str(misp_event["id"]),
                    "created_at": parse_misp_date(misp_event["date"]),
                    "updated_at": parse_misp_date(misp_event.get("timestamp", misp_event["date"]))
                }
                unified_events.append(unified_event)

            # Bulk insert into unified database
            await unified_db.bulk_insert_events(unified_events)

            offset += batch_size
            print(f"Migrated {offset} events...")

        print("MISP event migration completed")

    def map_misp_threat_level(threat_level_id: str) -> str:
        """Map MISP threat levels to unified severity"""
        mapping = {
            "1": "high",      # High threat
            "2": "medium",    # Medium threat
            "3": "low",       # Low threat
            "4": "critical"   # Undefined (treat as critical for review)
        }
        return mapping.get(threat_level_id, "medium")
    ```

Phase 3: Automation Domain Migration (Months 5-6)
  Priority Projects: n8n, Goose AI agents, Background processing

  Month 5: Workflow Engine
    - Migrate n8n workflow definitions to unified format
    - Implement workflow execution engine
    - Create workflow node library (security, gaming, productivity)
    - Build workflow editor interface
    - Set up workflow scheduling and triggers

  Month 6: AI Agent Integration
    - Integrate Goose AI agents into unified platform
    - Create agent session management
    - Implement agent-workflow integration
    - Build conversational interface for agents
    - Create agent skill/capability registry

  Workflow Migration:
    ```python
    # scripts/migrate_n8n_workflows.py
    async def migrate_n8n_workflows():
        """Migrate n8n workflows to unified format"""

        n8n_db = await connect_to_n8n_db()
        unified_db = await connect_to_unified_db()

        # Fetch all workflows
        n8n_workflows = await n8n_db.fetch_workflows()

        for n8n_workflow in n8n_workflows:
            # Convert n8n format to unified format
            unified_workflow = {
                "id": str(uuid.uuid4()),
                "name": n8n_workflow["name"],
                "description": n8n_workflow.get("notes", ""),
                "definition": {
                    "format": "n8n",
                    "version": "1.0",
                    "nodes": convert_n8n_nodes(n8n_workflow["nodes"]),
                    "connections": n8n_workflow["connections"],
                    "settings": n8n_workflow.get("settings", {})
                },
                "is_active": n8n_workflow["active"],
                "trigger_type": detect_trigger_type(n8n_workflow),
                "trigger_config": extract_trigger_config(n8n_workflow),
                "created_by": await resolve_user_id(n8n_workflow.get("createdBy")),
                "source_system": "n8n",
                "external_id": str(n8n_workflow["id"])
            }

            await unified_db.insert_workflow(unified_workflow)

        print(f"Migrated {len(n8n_workflows)} workflows")
    ```

Phase 4: Gaming Domain Migration (Months 7-8)
  Priority Projects: Commander Spellbook, MTG tooling

  Month 7: MTG Card Database & API
    - Import MTG card data from Scryfall
    - Migrate Commander Spellbook combo database
    - Implement card search and filtering
    - Create combo validation system
    - Build MTG-specific APIs

  Month 8: Gaming Interface & Community Features
    - Build combo submission and review workflow
    - Implement community voting and rating
    - Create deck building tools
    - Add tournament and event tracking
    - Integrate with external MTG services

Phase 5: Productivity Domain Migration (Months 9-10)
  Priority Projects: IT-Tools, CyberChef, Actual Budget, File processing

  Month 9: Utility Tools Integration
    - Migrate IT-Tools converters and utilities
    - Integrate CyberChef recipe execution
    - Implement file processing pipelines
    - Create tool chaining capabilities
    - Build productivity dashboard

  Month 10: Personal Management Tools
    - Migrate Actual Budget functionality
    - Implement personal project management
    - Create document and knowledge management
    - Add calendar and scheduling features
    - Build personal analytics dashboard

Phase 6: Advanced Features & Optimization (Months 11-12)
  Month 11: Advanced Analytics & AI
    - Implement advanced threat intelligence correlation
    - Create predictive security analytics
    - Build recommendation engines for all domains
    - Add machine learning model integration
    - Create cross-domain insights dashboard

  Month 12: Performance & Scaling
    - Optimize database queries and indexing
    - Implement caching strategies
    - Set up horizontal scaling
    - Performance testing and tuning
    - Production deployment and monitoring
```

## 7.2 Data Migration & Validation Strategy

```yaml
Data Migration Framework:
  Migration Pipeline:
    ```python
    # scripts/migration_framework.py
    from abc import ABC, abstractmethod
    from typing import List, Dict, Any
    import asyncio
    import logging

    class MigrationBase(ABC):
        def __init__(self, source_config: dict, target_config: dict):
            self.source_config = source_config
            self.target_config = target_config
            self.logger = logging.getLogger(self.__class__.__name__)

        @abstractmethod
        async def extract_data(self) -> List[Dict[str, Any]]:
            """Extract data from source system"""
            pass

        @abstractmethod
        async def transform_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """Transform data to unified format"""
            pass

        @abstractmethod
        async def load_data(self, transformed_data: List[Dict[str, Any]]) -> None:
            """Load data into target system"""
            pass

        async def validate_migration(self) -> Dict[str, Any]:
            """Validate migration results"""
            source_count = await self.get_source_count()
            target_count = await self.get_target_count()

            validation_results = {
                "source_count": source_count,
                "target_count": target_count,
                "success_rate": (target_count / source_count) * 100 if source_count > 0 else 0,
                "data_quality_checks": await self.perform_data_quality_checks()
            }

            return validation_results

        async def run_migration(self, batch_size: int = 1000, dry_run: bool = False):
            """Execute complete migration process"""

            self.logger.info(f"Starting migration: {self.__class__.__name__}")

            # Extract data in batches
            total_processed = 0
            batch_number = 0

            while True:
                batch_number += 1

                # Extract batch
                raw_data = await self.extract_data_batch(batch_size, batch_number)

                if not raw_data:
                    break

                # Transform batch
                transformed_data = await self.transform_data(raw_data)

                # Load batch (unless dry run)
                if not dry_run:
                    await self.load_data(transformed_data)

                total_processed += len(transformed_data)
                self.logger.info(f"Processed batch {batch_number}: {len(transformed_data)} records")

            # Validate migration
            if not dry_run:
                validation_results = await self.validate_migration()
                self.logger.info(f"Migration validation: {validation_results}")

            self.logger.info(f"Migration completed. Total processed: {total_processed}")

    class MISPEventMigration(MigrationBase):
        async def extract_data_batch(self, batch_size: int, batch_number: int) -> List[Dict[str, Any]]:
            # Implementation specific to MISP
            pass

        async def transform_data(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            transformed = []

            for misp_event in raw_data:
                # Transform MISP event to unified security event
                unified_event = self._transform_misp_event(misp_event)
                transformed.append(unified_event)

            return transformed

        def _transform_misp_event(self, misp_event: Dict[str, Any]) -> Dict[str, Any]:
            # Detailed transformation logic
            return {
                "id": str(uuid.uuid4()),
                "event_type": "misp_event",
                "title": misp_event["info"],
                # ... other transformations
            }
    ```

Data Validation Framework:
  ```python
  # scripts/validation_framework.py
  class DataValidator:
      def __init__(self, source_db, target_db):
          self.source_db = source_db
          self.target_db = target_db

      async def validate_record_counts(self, migration_mapping: Dict[str, str]) -> Dict[str, Any]:
          """Validate record counts match between source and target"""

          results = {}

          for source_table, target_table in migration_mapping.items():
              source_count = await self.source_db.count_records(source_table)
              target_count = await self.target_db.count_records(target_table)

              results[source_table] = {
                  "source_count": source_count,
                  "target_count": target_count,
                  "match": source_count == target_count,
                  "difference": abs(source_count - target_count)
              }

          return results

      async def validate_data_integrity(self, sample_size: int = 1000) -> Dict[str, Any]:
          """Validate data integrity by comparing samples"""

          # Sample records from source and target
          source_sample = await self.source_db.sample_records(sample_size)

          integrity_results = {
              "total_sampled": len(source_sample),
              "integrity_checks": [],
              "pass_rate": 0.0
          }

          passed_checks = 0

          for source_record in source_sample:
              # Find corresponding record in target
              target_record = await self.find_migrated_record(source_record)

              if target_record:
                  # Compare key fields
                  checks_passed = self.compare_records(source_record, target_record)
                  integrity_results["integrity_checks"].append({
                      "source_id": source_record["id"],
                      "target_id": target_record["id"],
                      "checks_passed": checks_passed
                  })

                  if checks_passed:
                      passed_checks += 1

          integrity_results["pass_rate"] = (passed_checks / len(source_sample)) * 100

          return integrity_results

  # Migration orchestration
  class MigrationOrchestrator:
      def __init__(self):
          self.migrations = []
          self.rollback_plan = []

      def add_migration(self, migration: MigrationBase, rollback_script: str = None):
          self.migrations.append({
              "migration": migration,
              "rollback_script": rollback_script
          })

      async def execute_migrations(self, dry_run: bool = False):
          """Execute all migrations in order"""

          results = []

          for i, migration_config in enumerate(self.migrations):
              migration = migration_config["migration"]

              try:
                  # Run migration
                  await migration.run_migration(dry_run=dry_run)

                  # Validate results
                  validation_results = await migration.validate_migration()

                  results.append({
                      "migration": migration.__class__.__name__,
                      "status": "success",
                      "validation": validation_results
                  })

              except Exception as e:
                  # Migration failed - execute rollback if not dry run
                  if not dry_run and migration_config.get("rollback_script"):
                      await self._execute_rollback(i)

                  results.append({
                      "migration": migration.__class__.__name__,
                      "status": "failed",
                      "error": str(e)
                  })

                  # Stop execution on failure
                  break

          return results
  ```
```

## 7.3 Risk Mitigation & Rollback Strategy

```yaml
Risk Assessment & Mitigation:

  High-Risk Areas:
    1. Data Loss During Migration
      Risk Level: HIGH
      Mitigation:
        - Complete database backups before each migration phase
        - Implement point-in-time recovery capabilities
        - Use blue-green deployment for zero-downtime migrations
        - Comprehensive data validation at each step
        - Rollback procedures for each migration

    2. Authentication System Failure
      Risk Level: HIGH
      Mitigation:
        - Maintain legacy authentication as fallback during transition
        - Implement emergency admin access procedures
        - Extensive testing of auth flows
        - Gradual user migration with opt-in testing

    3. Performance Degradation
      Risk Level: MEDIUM
      Mitigation:
        - Performance testing throughout migration
        - Database query optimization
        - Caching layer implementation
        - Horizontal scaling capabilities
        - Performance monitoring and alerting

    4. Security Vulnerabilities
      Risk Level: MEDIUM
      Mitigation:
        - Security audits at each phase
        - Penetration testing
        - Automated security scanning in CI/CD
        - Regular dependency updates
        - Security monitoring implementation

Rollback Procedures:
  ```yaml
  # Rollback Strategy Document
  Rollback_Triggers:
    - Data corruption detected
    - Critical functionality broken
    - Performance degradation > 50%
    - Security vulnerability discovered
    - User acceptance criteria not met

  Rollback_Procedures:
    Phase_1_Rollback:
      - Restore database from backup
      - Revert infrastructure changes
      - Switch traffic back to legacy systems
      - Estimated time: 30 minutes

    Phase_2_Security_Rollback:
      - Restore MISP/Dispatch to original state
      - Migrate critical security events back
      - Reactivate legacy security monitoring
      - Estimated time: 2 hours

    Phase_3_Automation_Rollback:
      - Export workflows back to n8n format
      - Restart legacy n8n instance
      - Restore agent configurations
      - Estimated time: 1 hour

  Automated_Rollback_Scripts:
    ```bash
    #!/bin/bash
    # scripts/rollback_phase.sh

    PHASE=$1
    BACKUP_TIMESTAMP=$2

    echo "Starting rollback for Phase $PHASE using backup $BACKUP_TIMESTAMP"

    case $PHASE in
      "1")
        # Phase 1 rollback
        kubectl scale deployment jane-orchestrator --replicas=0
        kubectl scale deployment jane-ui --replicas=0

        # Restore database
        pg_restore --clean --if-exists -d modular_monolith backups/phase_${PHASE}_${BACKUP_TIMESTAMP}.dump

        # Restart legacy services
        docker-compose -f legacy/docker-compose.yml up -d
        ;;

      "2")
        # Phase 2 rollback - Security domain
        python scripts/rollback_security_migration.py --backup-timestamp $BACKUP_TIMESTAMP

        # Restart MISP and Dispatch
        docker-compose -f security/docker-compose.yml up -d
        ;;

      "3")
        # Phase 3 rollback - Automation domain
        python scripts/rollback_automation_migration.py --backup-timestamp $BACKUP_TIMESTAMP

        # Restart n8n
        docker-compose -f automation/docker-compose.yml up -d
        ;;
    esac

    echo "Rollback completed for Phase $PHASE"
    ```
  ```

Testing Strategy:
  ```python
  # tests/migration/test_migration_e2e.py
  import pytest
  import asyncio

  class TestMigrationE2E:
      """End-to-end migration testing"""

      @pytest.mark.asyncio
      async def test_complete_migration_flow(self):
          """Test complete migration from legacy to unified system"""

          # Set up test data in legacy systems
          await self.setup_legacy_test_data()

          # Execute migration
          migration_results = await self.run_test_migration()

          # Validate results
          validation_results = await self.validate_migration_results()

          # Assert migration success
          assert validation_results["data_integrity_check"] == "PASS"
          assert validation_results["functionality_check"] == "PASS"
          assert validation_results["performance_check"] == "PASS"

      @pytest.mark.asyncio
      async def test_rollback_procedures(self):
          """Test rollback procedures work correctly"""

          # Create checkpoint before migration
          checkpoint = await self.create_migration_checkpoint()

          # Execute partial migration
          await self.run_partial_migration()

          # Simulate failure and rollback
          await self.execute_rollback(checkpoint)

          # Validate rollback success
          rollback_results = await self.validate_rollback()

          assert rollback_results["data_restored"] == True
          assert rollback_results["services_restored"] == True

      async def test_performance_benchmarks(self):
          """Ensure performance meets requirements after migration"""

          # Run performance tests
          api_response_times = await self.benchmark_api_performance()
          database_query_times = await self.benchmark_database_performance()
          ui_load_times = await self.benchmark_ui_performance()

          # Assert performance requirements
          assert api_response_times["p95"] < 500  # ms
          assert database_query_times["avg"] < 100  # ms
          assert ui_load_times["first_contentful_paint"] < 2000  # ms
  ```

Success Criteria & Validation:
  ```yaml
  Migration_Success_Criteria:
    Data_Integrity:
      - 100% of critical data migrated successfully
      - Data validation checks pass with 99.9% accuracy
      - No data corruption detected
      - All relationships preserved

    Functionality:
      - All core features working in unified system
      - API compatibility maintained for external integrations
      - User workflows function as expected
      - Real-time features operational

    Performance:
      - API response times < 500ms (p95)
      - Database query performance within 10% of baseline
      - UI load times < 3 seconds
      - System can handle peak load (10x normal usage)

    Security:
      - All security controls functional
      - Authentication and authorization working
      - Audit logging operational
      - Security monitoring active

    User_Acceptance:
      - User training completed
      - Key stakeholders sign-off
      - Support documentation available
      - Feedback incorporation plan in place

  Go_Live_Checklist:
    Pre_Launch:
      - [ ] All migration phases completed successfully
      - [ ] Performance benchmarks met
      - [ ] Security audit passed
      - [ ] Backup and rollback procedures tested
      - [ ] Monitoring and alerting configured
      - [ ] Support team trained
      - [ ] User documentation complete

    Launch_Day:
      - [ ] Final data synchronization
      - [ ] DNS cutover to new system
      - [ ] Monitor system health
      - [ ] User communications sent
      - [ ] Support team on standby
      - [ ] Rollback plan ready if needed

    Post_Launch:
      - [ ] Monitor system for 48 hours
      - [ ] Collect user feedback
      - [ ] Performance optimization
      - [ ] Legacy system decommission plan
      - [ ] Lessons learned documentation
  ```

---

## Executive Summary

This comprehensive modular monolith architecture successfully consolidates 23 diverse projects into a unified, scalable platform while preserving all critical business logic. The design addresses the key challenges of:

1. **Technology Standardization**: Unified around FastAPI/Python backend with Vue.js frontend, supporting 13 TypeScript/JavaScript projects and 10 Python projects while accommodating exotic implementations.

2. **API Unification**: Domain-based API structure (/api/v1/{domain}/{resource}) with consistent authentication, authorization, and response formats across security, automation, gaming, and productivity domains.

3. **Data Consolidation**: Comprehensive PostgreSQL schema supporting multi-tenancy, domain-specific data models, and flexible JSONB storage for varying project requirements.

4. **Security & Compliance**: Enterprise-grade security with RBAC, encryption, audit logging, and GDPR/SOC2 compliance built-in from the start.

5. **Deployment Strategy**: Container-native with Kubernetes production deployment, comprehensive CI/CD pipeline, and blue-green deployment capabilities.

6. **Migration Risk Mitigation**: 12-month phased migration approach with comprehensive testing, validation, and rollback procedures to ensure zero data loss and minimal business disruption.

The architecture enables cross-project integration while maintaining domain boundaries, supports both existing functionality and future enhancements, and provides a solid foundation for scaling the integrated platform to support thousands of users across multiple domains.
```
```
````
