# Data Model: Mental Prosthetic Platform

**Feature**: Mental Prosthetic Platform (Refined)  
**Date**: 2025-10-19  
**Phase**: 1 - Data Design  

## Overview

Unified data model supporting 37 executive function tools across 4 domains (Security, Productivity, MTG, Infrastructure) with PostgreSQL as primary database and SQLite for local-first applications.

## Core Entities

### User Management

```sql
-- Single user system with comprehensive ADHD/autism support preferences
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Executive function support preferences
    adhd_preferences JSONB DEFAULT '{}',
    autism_preferences JSONB DEFAULT '{}',
    executive_function_settings JSONB DEFAULT '{}',
    
    -- AI learning context
    ai_interaction_history JSONB DEFAULT '{}',
    personalization_data JSONB DEFAULT '{}'
);

-- Session management for unified authentication across 37 tools
CREATE TABLE user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_token VARCHAR(512) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    last_activity TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Cross-tool session persistence
    tool_contexts JSONB DEFAULT '{}',
    active_domains TEXT[] DEFAULT '{}'
);
```

### Domain Classification

```sql
-- Organizational structure for 37 tools across 4 domains
CREATE TABLE domains (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL, -- Security, Productivity, MTG, Infrastructure
    description TEXT,
    tool_count INTEGER NOT NULL,
    performance_tier_ms INTEGER NOT NULL, -- Domain-based performance requirements
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Individual tools within domains (37 total)
CREATE TABLE integrated_tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain_id UUID NOT NULL REFERENCES domains(id),
    name VARCHAR(100) NOT NULL,
    original_path TEXT NOT NULL, -- Path in features/ directory
    integration_status VARCHAR(50) DEFAULT 'pending', -- pending, migrating, completed, failed
    
    -- Business logic preservation
    original_config JSONB,
    migrated_config JSONB,
    api_endpoints JSONB DEFAULT '{}',
    
    -- Category classification (A: Complex, B: Domain Logic, C: Utilities)
    complexity_category CHAR(1) CHECK (complexity_category IN ('A', 'B', 'C')),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(domain_id, name)
);
```

### Security Domain (13 tools)

```sql
-- Security incidents and threat intelligence (MISP integration)
CREATE TABLE security_incidents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    severity VARCHAR(20) CHECK (severity IN ('low', 'medium', 'high', 'critical')),
    status VARCHAR(20) DEFAULT 'open',
    
    -- MISP integration fields
    misp_event_id INTEGER,
    indicators JSONB DEFAULT '{}',
    attributes JSONB DEFAULT '{}',
    
    -- Cross-domain relationships
    related_tasks UUID[], -- References to productivity tasks
    infrastructure_impact JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Malware analysis and YARA rules
CREATE TABLE malware_samples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    file_hash VARCHAR(128) UNIQUE NOT NULL,
    file_name VARCHAR(255),
    file_size BIGINT,
    
    -- YARA-X integration
    yara_matches JSONB DEFAULT '{}',
    analysis_results JSONB DEFAULT '{}',
    
    -- CyberChef processing
    processing_recipes JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Network monitoring (RITA integration)
CREATE TABLE network_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_ip INET,
    dest_ip INET,
    protocol VARCHAR(10),
    
    -- RITA analysis
    beacon_score DECIMAL(5,2),
    dns_tunneling_score DECIMAL(5,2),
    long_connections JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Productivity Domain (8 tools)

```sql
-- Task management with AI-assisted breakdown
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'todo' CHECK (status IN ('todo', 'in_progress', 'done', 'blocked')),
    priority VARCHAR(10) CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    
    -- Executive function support
    ai_breakdown JSONB, -- AI-generated task steps
    executive_function_hints JSONB,
    adhd_accommodations JSONB,
    
    -- Cross-domain relationships  
    security_incident_id UUID REFERENCES security_incidents(id),
    mtg_deck_id UUID, -- Will reference MTG domain
    infrastructure_project_id UUID,
    
    -- Scheduling and reminders
    due_date TIMESTAMP WITH TIME ZONE,
    reminder_settings JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- n8n workflow automation
CREATE TABLE automation_workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    
    -- n8n integration
    n8n_workflow_id VARCHAR(255),
    workflow_definition JSONB,
    trigger_conditions JSONB,
    
    -- Executive function automation
    adhd_triggers JSONB, -- Automated reminders and task creation
    cross_domain_integrations JSONB,
    
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- IT-Tools utilities integration
CREATE TABLE utility_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    tool_name VARCHAR(100) NOT NULL,
    session_data JSONB,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### MTG Domain (4 tools)

```sql
-- Magic: The Gathering deck management
CREATE TABLE mtg_decks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    format VARCHAR(50), -- Commander, Standard, etc.
    
    -- Commander Spellbook integration
    commander_card_name VARCHAR(255),
    combo_data JSONB DEFAULT '{}',
    
    -- Deck analysis
    mana_curve JSONB,
    card_analysis JSONB,
    win_conditions JSONB,
    
    -- Cross-domain integration
    analysis_tasks UUID[], -- Links to productivity tasks for deck improvement
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- MTG card collection and scripting
CREATE TABLE mtg_cards (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    scryfall_id UUID UNIQUE,
    name VARCHAR(255) NOT NULL,
    mana_cost VARCHAR(50),
    type_line TEXT,
    oracle_text TEXT,
    
    -- Scripting toolkit integration
    custom_scripts JSONB DEFAULT '{}',
    automation_rules JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User's card collection
CREATE TABLE user_card_collection (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    card_id UUID NOT NULL REFERENCES mtg_cards(id),
    quantity INTEGER DEFAULT 1,
    condition VARCHAR(20) DEFAULT 'near_mint',
    
    -- Collection management
    acquisition_date DATE,
    notes TEXT,
    
    UNIQUE(user_id, card_id, condition)
);
```

### Infrastructure Domain (12 tools)

```sql
-- Container and service management
CREATE TABLE infrastructure_services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    service_type VARCHAR(50), -- docker, kubernetes, systemd
    
    -- Docker/Kubernetes integration
    container_config JSONB,
    deployment_status VARCHAR(20) DEFAULT 'stopped',
    
    -- Kong API gateway integration
    api_routes JSONB DEFAULT '{}',
    
    -- Monitoring integration (HELK, Security Onion)
    monitoring_config JSONB DEFAULT '{}',
    health_checks JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System monitoring and logs
CREATE TABLE system_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    source_service VARCHAR(255),
    event_type VARCHAR(50),
    
    -- HELK/Security Onion integration
    log_data JSONB,
    alert_level VARCHAR(10),
    
    -- Cross-domain correlation
    security_incident_id UUID REFERENCES security_incidents(id),
    related_task_id UUID REFERENCES tasks(id)
);

-- File analysis and forensics
CREATE TABLE file_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    file_path TEXT NOT NULL,
    file_hash VARCHAR(128),
    
    -- Software forensic kit integration
    analysis_results JSONB DEFAULT '{}',
    metadata JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### AI Integration

```sql
-- AI context and learning for executive function support
CREATE TABLE ai_contexts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    context_type VARCHAR(50) NOT NULL, -- task_breakdown, reminder, suggestion
    
    -- LLM interaction data
    prompt_history JSONB DEFAULT '{}',
    response_history JSONB DEFAULT '{}',
    feedback_scores JSONB DEFAULT '{}',
    
    -- Cross-tool learning context
    tool_usage_patterns JSONB DEFAULT '{}',
    executive_function_insights JSONB DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Real-time synchronization state
CREATE TABLE sync_states (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id),
    entity_type VARCHAR(100) NOT NULL,
    entity_id UUID NOT NULL,
    
    -- Synchronization tracking
    last_sync TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    sync_status VARCHAR(20) DEFAULT 'pending', -- pending, syncing, completed, failed
    conflict_data JSONB,
    
    -- WebSocket session tracking
    websocket_session_id VARCHAR(255),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(entity_type, entity_id)
);
```

## Database Configuration

### PostgreSQL Primary Database

- **Primary Use**: 18/37 tools requiring complex relational data
- **Domains**: Security (threat intelligence), Productivity (task management), Infrastructure (monitoring)
- **Features**: Full-text search, JSONB indexing, temporal data, vector extensions for AI embeddings

### SQLite Local-First Applications

- **Primary Use**: 5/37 tools requiring offline capability
- **Tools**: Specific productivity tools, MTG collection management, utility sessions
- **Sync Strategy**: Periodic synchronization with PostgreSQL primary database

### Redis Caching Layer

- **Session Management**: JWT token storage and validation
- **Real-time Data**: WebSocket session state, temporary AI context
- **Job Queues**: Background processing for cross-domain operations

## Relationships and Constraints

### Cross-Domain Relationships

1. **Security → Productivity**: Incidents generate tasks automatically
2. **Infrastructure → Security**: System events correlate with security incidents  
3. **All Domains → AI**: Every interaction feeds AI learning context
4. **Productivity → All**: Task system coordinates activities across domains

### Data Consistency

- **Model**: Eventual consistency with conflict resolution
- **Conflict Resolution**: Last-writer-wins with user notification
- **Synchronization**: Real-time WebSocket updates with 500ms target latency
- **Backup**: Daily automated backup to Synology NAS

### Performance Optimization

- **Indexing**: Domain-specific indexes for performance tier compliance
- **Partitioning**: Time-based partitioning for event tables
- **Caching**: Redis layer for frequently accessed executive function data
- **Connection Pooling**: Optimized for single-user deployment with burst capacity

## Migration Strategy

### Big-Bang Migration Approach

1. **Schema Creation**: Deploy complete unified schema
2. **Data Migration**: Parallel migration from 37 individual tool databases
3. **Validation**: Cross-domain relationship verification
4. **Rollback Plan**: Tool-specific rollback with system-wide fallback capability

### Integration Validation

- **Data Integrity**: Foreign key constraints and validation rules
- **Performance Testing**: Domain-specific performance tier validation
- **Cross-Domain Testing**: Workflow validation across all 4 domains
- **Executive Function Testing**: ADHD/autism accommodation verification