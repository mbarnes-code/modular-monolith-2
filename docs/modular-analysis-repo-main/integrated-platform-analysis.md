# Integrated Platform Analysis - Modular Monolith Migration Strategy (v1.0)

**Purpose**: Comprehensive analysis for consolidating 23 cybersecurity and development tools into a unified modular monolith deployment

**Analysis Date:** October 12, 2025  
**Analyzed By:** GitHub Copilot  
**Scope:** 23 projects from reports directory  
**Goal:** Minimize deployment containers while preserving critical business logic

---

## Section 1: Project Portfolio Overview & Technology Consolidation

### 1.1 Portfolio Summary
```yaml
Total Projects Analyzed: 23
Primary Domains:
  - Cybersecurity Tools: 8 projects (MISP, Maltrail, HELK, Nemesis, CyberChef, HexStrike AI, Software Forensic Kit, Onex)
  - Workflow Automation: 3 projects (n8n, Dispatch, Goose)
  - Development Tools: 4 projects (Inspector, IT-Tools, FileScopeMCP, Firecrawl)
  - Specialized Applications: 4 projects (Mealie, Actual Budget, Ghostwriter, KasmVNC)
  - MTG/Gaming: 4 projects (Commander Spellbook, MTG Commander Map, MTG Scripting Toolkit)

Business Criticality Distribution:
  - CRITICAL (must preserve): 15 projects
  - IMPORTANT: 6 projects  
  - NICE-TO-HAVE: 2 projects

Estimated Total Monthly Users: 500,000+ across all platforms
```

### 1.2 Technology Stack Consolidation Analysis

#### Programming Language Clusters
```yaml
Node.js/TypeScript Cluster (13 projects - 57%):
  Primary: n8n, Firecrawl, Inspector, IT-Tools, FileScopeMCP, Actual Budget
  Secondary: Commander Spellbook (frontend), Mealie (frontend), MTG Scripting Toolkit
  Mixed: Goose, Nemesis, MISP, CyberChef
  
  Technology Stack:
    - Language: TypeScript/JavaScript (ES2020+)
    - Runtime: Node.js 18+
    - Frameworks: Express.js, FastAPI proxies, Vue.js, React
    - Databases: PostgreSQL, SQLite
    - Build: Vite, Webpack, tsc
    
Python Cluster (10 projects - 43%):
  Primary: MISP, Dispatch, Mealie, HELK, Maltrail, Nemesis, HexStrike AI, MTG Commander Map
  Secondary: Goose (MCP integration), n8n (AI features)
  
  Technology Stack:
    - Language: Python 3.11+
    - Frameworks: FastAPI, Django, Flask
    - Databases: PostgreSQL, SQLite
    - Build: Poetry, pip, pytest

Specialized/Native Clusters:
  C++ Cluster: KasmVNC (desktop virtualization)
  PHP Cluster: MISP (legacy CakePHP - requires special handling)
  Rust Cluster: Goose (core agent), Nemesis (noseyparker)
  Java Cluster: Software Forensic Kit
  Shell Scripts: Onex (pure shell)
```

#### Framework Consolidation Opportunities
```yaml
Web Frameworks:
  FastAPI (6 projects): Mealie, Dispatch, Nemesis, HexStrike AI, Firecrawl (potential)
    - Pros: Async support, auto-docs, type hints, modern Python
    - Consolidation: Primary backend framework choice
    
  Express.js (4 projects): n8n, Inspector, Firecrawl, Goose server
    - Pros: Mature ecosystem, TypeScript support
    - Consolidation: Node.js services framework
    
  Django (2 projects): Ghostwriter, Commander Spellbook
    - Pros: Admin interface, ORM, mature
    - Consolidation: Keep for complex admin-heavy applications

Frontend Frameworks:
  Vue.js (3 projects): n8n, IT-Tools, Mealie
    - Pros: Easy learning curve, good TypeScript support
    - Consolidation: Primary frontend framework
    
  React (3 projects): Actual Budget, Commander Spellbook, Inspector
    - Pros: Large ecosystem, component reuse
    - Consolidation: Alternative frontend framework
```

#### Database Consolidation Strategy
```yaml
Primary Database: PostgreSQL
  Supporting Projects: 10 projects (MISP, n8n, Dispatch, Nemesis, Firecrawl, Ghostwriter, Commander Spellbook, Mealie optional)
  Why: JSONB support, full-text search, mature, handles complex relationships
  
Secondary Database: SQLite  
  Supporting Projects: 6 projects (Actual Budget, IT-Tools local, FileScopeMCP, CyberChef browser storage)
  Why: Embedded apps, local-first architecture, zero-config
  
Cache Layer: Redis
  Supporting Projects: 7 projects (MISP, n8n optional, HELK, Nemesis via RabbitMQ, Firecrawl)
  Why: Job queues, session storage, rate limiting
```

### 1.3 Deployment Consolidation Strategy

#### Container Reduction Plan
```yaml
Current State: 23 separate deployments
Target State: 6 consolidated containers

Container 1: Core Web Platform (FastAPI + Vue.js)
  Projects: Mealie, Dispatch, HexStrike AI, IT-Tools, Inspector
  Base: Python 3.11 + Node.js (for frontend builds)
  Database: PostgreSQL + Redis
  Estimated Resources: 2GB RAM, 2 CPU cores

Container 2: Workflow Automation Hub
  Projects: n8n (primary), Goose (API mode), FileScopeMCP
  Base: Node.js 20 + TypeScript
  Database: PostgreSQL + Redis  
  Estimated Resources: 4GB RAM, 2 CPU cores (workflow execution intensive)

Container 3: Security Intelligence Platform  
  Projects: MISP, Nemesis (core services), Maltrail, HELK integration
  Base: Python 3.11 + PHP 8.2 (MISP legacy)
  Database: PostgreSQL + Redis
  Estimated Resources: 8GB RAM, 4 CPU cores (data processing intensive)

Container 4: Financial & Content Management
  Projects: Actual Budget, Ghostwriter, Commander Spellbook
  Base: Node.js 20 + Python 3.11
  Database: PostgreSQL + SQLite (Actual Budget)
  Estimated Resources: 2GB RAM, 1 CPU core

Container 5: Data Processing & Analysis
  Projects: Firecrawl, MTG Commander Map, MTG Scripting Toolkit, Software Forensic Kit
  Base: Python 3.11 + Java 11 + Node.js 20
  Database: PostgreSQL + file storage
  Estimated Resources: 4GB RAM, 2 CPU cores

Container 6: Specialized Services
  Projects: KasmVNC, CyberChef (hosted), Onex (CLI wrapper)
  Base: Multi-architecture (C++ native + JavaScript)
  Database: File-based storage
  Estimated Resources: 4GB RAM, 2 CPU cores (VNC intensive)
```

---

## Section 2: Business Logic Preservation Matrix [CRITICAL]

### 2.1 Core Business Logic Categories

#### Category A: Complex Algorithms (Must Preserve as Microservices)
```yaml
n8n Workflow Engine:
  Location: packages/core/src/WorkflowExecute.ts
  Complexity: Very High (10,000+ lines)
  Business Value: Core automation orchestration with 400+ integrations
  Preservation: Dedicated microservice with REST/GraphQL API
  Dependencies: Redis for queuing, PostgreSQL for workflow storage
  
MISP Threat Intelligence Correlation:
  Location: app/Model/Event.php correlation methods (8,733 lines)
  Complexity: Very High 
  Business Value: Automated threat indicator correlation and sharing
  Preservation: Dedicated microservice with REST API
  Dependencies: PostgreSQL, Redis, external feed integrations

CyberChef Operations Engine:
  Location: src/core/operations/ (300+ operations)
  Complexity: High (each operation has specific algorithm)
  Business Value: Cryptographic and data analysis transformations
  Preservation: Embedded JavaScript library + REST API wrapper
  Dependencies: Browser localStorage, minimal server resources

Goose AI Agent System:
  Location: crates/goose/src/agent/ (Rust core)
  Complexity: Very High (LLM integration, conversation management)
  Business Value: Autonomous AI development assistance
  Preservation: Dedicated Rust microservice with gRPC/REST API
  Dependencies: External LLM APIs, conversation storage

Nemesis File Analysis Pipeline:
  Location: Multiple Python services (enrichment modules)
  Complexity: High (multi-stage analysis pipeline)
  Business Value: Automated file analysis and threat detection
  Preservation: Microservice cluster with message queuing
  Dependencies: PostgreSQL, RabbitMQ, external scanners
```

#### Category B: Domain-Specific Logic (Modularize within Monolith)
```yaml
Mealie Recipe Management:
  Location: mealie/services/ (recipe parsing, meal planning)
  Complexity: Medium
  Business Value: Recipe parsing, meal planning algorithms
  Preservation: Module within FastAPI monolith
  Integration: Shared PostgreSQL, common auth system

Actual Budget Financial Engine:
  Location: packages/loot-core/ (budgeting rules)
  Complexity: Medium 
  Business Value: Zero-based budgeting, transaction sync
  Preservation: Module within Node.js monolith
  Integration: Maintain SQLite for local-first, add PostgreSQL sync

Commander Spellbook Combo Engine:
  Location: backend/spellbook/ (combo generation, validation)
  Complexity: High
  Business Value: MTG combo search and validation
  Preservation: Module within Django monolith
  Integration: Shared PostgreSQL, common search infrastructure

Dispatch Incident Orchestration:
  Location: src/dispatch/incident/ (workflow automation)
  Complexity: High
  Business Value: Automated incident response coordination
  Preservation: Module within FastAPI monolith  
  Integration: Shared PostgreSQL, common notification system
```

#### Category C: Utility Functions (Shared Libraries)
```yaml
IT-Tools Utility Functions:
  Location: src/tools/ (80+ developer utilities)
  Complexity: Low-Medium
  Business Value: Developer productivity tools
  Preservation: Shared JavaScript library + UI components
  Integration: Client-side execution, shared component library

MTG Data Processing:
  Location: Various TypeScript utilities (Scryfall API, card analysis)
  Complexity: Medium
  Business Value: MTG card data processing and analysis
  Preservation: Shared TypeScript library
  Integration: Common API layer, cached responses

FileScopeMCP Integration:
  Location: src/ (MCP server implementation) 
  Complexity: Low
  Business Value: File system integration for AI agents
  Preservation: Shared Node.js library
  Integration: Common MCP protocol handling
```

### 2.2 API Standardization Requirements

#### Authentication Consolidation
```yaml
Current Authentication Patterns:
  - OAuth2/OIDC: n8n, Ghostwriter, Commander Spellbook (Discord)
  - JWT: MISP, Dispatch, Nemesis, Firecrawl  
  - Session-based: Mealie, Actual Budget
  - API Keys: IT-Tools, CyberChef (stateless)
  - None: Onex, KasmVNC (system-level)

Unified Authentication Strategy:
  Primary: OAuth2/OIDC with JWT tokens
  Implementation: FastAPI-Users or similar middleware
  Providers: Discord, Google, GitHub, local accounts
  Fallback: API keys for programmatic access
  Integration: Shared auth middleware across all modules
```

#### API Pattern Standardization  
```yaml
REST API Patterns:
  Base Path: /api/v1/{service}/{resource}
  Examples:
    - /api/v1/workflows/{id} (n8n integration)
    - /api/v1/recipes/{id} (Mealie)
    - /api/v1/incidents/{id} (Dispatch)
    - /api/v1/indicators/{id} (MISP)
    
  Response Format:
    Success: {"data": {...}, "meta": {...}}
    Error: {"error": {"code": 400, "message": "...", "details": {...}}}
    
  Pagination: 
    Standard: offset/limit with Link headers
    Alternative: cursor-based for large datasets (MISP events)
    
  Filtering:
    Query params: ?filter[field]=value&sort=field&include=relations
    Complex: POST /api/v1/{resource}/search with JSON body
```

### 2.3 API Endpoints Consolidation Strategy

#### Unified API Gateway Pattern
```yaml
Core Platform Endpoints (FastAPI):
  Authentication & Authorization:
    - POST /api/v1/auth/login
      Request: {"username": "string", "password": "string", "mfa_code": "string?"}
      Response: {"access_token": "jwt", "refresh_token": "jwt", "expires_in": 3600}
      Business Logic: OAuth2 flow, MFA validation, session creation
      
    - POST /api/v1/auth/refresh  
      Request: {"refresh_token": "jwt"}
      Response: {"access_token": "jwt", "expires_in": 3600}
      Business Logic: Token refresh with sliding expiration
      
    - POST /api/v1/auth/oauth/discord
      Request: {"code": "oauth_code", "state": "csrf_token"}
      Response: {"access_token": "jwt", "user": {...}}
      Business Logic: Discord OAuth callback, guild membership validation
      
  User & Organization Management:
    - GET /api/v1/organizations/{org_id}/users
      Authentication: Required, organization member
      Response: Paginated user list with roles and permissions
      Business Logic: RBAC filtering, audit logging
      
    - PUT /api/v1/users/{user_id}/roles
      Request: {"roles": ["admin", "editor"], "organization_id": "uuid"}
      Authentication: Required, admin only
      Business Logic: Role assignment with permission validation

  Workflow Management (n8n + Dispatch + Goose):
    - GET /api/v1/workflows
      Query: ?type=n8n_workflow&active=true&page=1&limit=50
      Authentication: Required, project member
      Response: {"items": [...], "total": 150, "has_more": true}
      Business Logic: Multi-tenant filtering, execution history inclusion
      
    - POST /api/v1/workflows
      Request: {"name": "string", "type": "n8n_workflow", "definition": {...}}
      Authentication: Required, editor role
      Response: {"id": "uuid", "created_at": "timestamp"}
      Business Logic: Workflow validation, node dependency checking
      
    - POST /api/v1/workflows/{workflow_id}/execute
      Request: {"trigger_data": {...}, "wait_for_completion": false}
      Authentication: Required, executor permission
      Response: {"execution_id": "uuid", "status": "running"}
      Business Logic: Async execution with progress tracking
      
    - GET /api/v1/workflows/{workflow_id}/executions
      Authentication: Required, workflow owner
      Response: Paginated execution history with logs
      Business Logic: Performance metrics, error analysis
      
  Security Intelligence (MISP + Nemesis + Maltrail):
    - GET /api/v1/security-events
      Query: ?severity=high&status=new&source_system=misp&limit=25
      Authentication: Required, security analyst role
      Response: {"events": [...], "total_count": 1250}
      Business Logic: Multi-source aggregation, correlation scoring
      
    - POST /api/v1/security-events
      Request: {"title": "string", "indicators": [...], "event_type": "threat_intel"}
      Authentication: Required, analyst role
      Response: {"id": "uuid", "correlation_score": 0.85}
      Business Logic: Auto-correlation with existing events, IOC extraction
      
    - GET /api/v1/indicators/search
      Query: ?ioc_type=domain&value=malicious.com&confidence_min=0.7
      Authentication: Required, security user
      Response: {"matches": [...], "related_events": [...]}
      Business Logic: Fuzzy matching, threat intelligence enrichment
      
  File Analysis (Nemesis + CyberChef + Software Forensic Kit):
    - POST /api/v1/files/upload
      Request: Multipart file upload with metadata
      Authentication: Required, analyst role
      Response: {"object_id": "uuid", "analysis_job_id": "uuid"}
      Business Logic: File type detection, malware scanning, analysis pipeline trigger
      
    - GET /api/v1/files/{file_id}/analysis
      Authentication: Required, file owner or admin
      Response: {"results": {...}, "security_findings": [...], "status": "completed"}
      Business Logic: Multi-tool analysis aggregation, finding prioritization
      
    - POST /api/v1/files/{file_id}/cyberchef-operation
      Request: {"operation": "Base64_Decode", "parameters": [...]}
      Authentication: Required, file access permission
      Response: {"output": "string", "operation_history": [...]}
      Business Logic: CyberChef operation execution, result chaining
      
  Content Management (Ghostwriter + Mealie):
    - GET /api/v1/content
      Query: ?content_type=recipe&tags=vegetarian&search=pasta
      Authentication: Required, organization member
      Response: Paginated content with full-text search ranking
      Business Logic: Multi-tenant content filtering, search optimization
      
    - POST /api/v1/content/recipes
      Request: {"title": "string", "ingredients": [...], "instructions": [...]}
      Authentication: Required, content creator role
      Response: {"id": "uuid", "slug": "auto-generated-slug"}
      Business Logic: Recipe parsing, nutrition calculation, meal planning integration
      
    - GET /api/v1/content/recipes/{recipe_id}/meal-plan
      Authentication: Required, recipe owner
      Response: {"suggested_dates": [...], "shopping_list": [...]}
      Business Logic: Calendar integration, inventory tracking
      
  Financial Management (Actual Budget):
    - GET /api/v1/financial/accounts
      Authentication: Required, budget owner
      Response: {"accounts": [...], "total_balance": 1234567}
      Business Logic: Multi-currency support, balance calculation
      
    - POST /api/v1/financial/transactions
      Request: {"account_id": "uuid", "amount": -1250, "payee": "string"}
      Authentication: Required, account owner
      Response: {"id": "uuid", "running_balance": 98750}
      Business Logic: Real-time balance update, category auto-assignment
      
    - GET /api/v1/financial/budget/{month}
      Authentication: Required, budget owner
      Response: {"categories": [...], "budget_vs_actual": {...}}
      Business Logic: Zero-based budgeting calculations, variance analysis
      
  Data Processing (Firecrawl + MTG Tools):
    - POST /api/v1/analysis/web-scraping
      Request: {"url": "string", "options": {...}, "formats": ["markdown"]}
      Authentication: Required, analyst role
      Response: {"job_id": "uuid", "estimated_completion": "timestamp"}
      Business Logic: Rate limiting, content extraction, data cleaning
      
    - GET /api/v1/analysis/{job_id}/results
      Authentication: Required, job owner
      Response: {"status": "completed", "data": {...}, "expires_at": "timestamp"}
      Business Logic: TTL-based cleanup, result caching
      
    - POST /api/v1/analysis/mtg/combo-search
      Request: {"cards": ["Card Name"], "format": "commander", "max_cmc": 7}
      Authentication: Required, user
      Response: {"combos": [...], "total_matches": 42}
      Business Logic: MTG rules validation, combo generation algorithms

Specialized Services Integration:
  KasmVNC Proxy:
    - GET /api/v1/remote-desktop/sessions
      Authentication: Required, admin role
      Response: {"active_sessions": [...], "capacity": "80%"}
      Business Logic: Session management, resource allocation
      
    - POST /api/v1/remote-desktop/connect
      Request: {"application": "forensic-tools", "duration_hours": 2}
      Authentication: Required, analyst role
      Response: {"vnc_url": "wss://...", "session_id": "uuid"}
      Business Logic: Dynamic container allocation, security isolation
      
  IT-Tools Integration:
    - GET /api/v1/dev-tools/available
      Authentication: Required, user
      Response: {"tools": [...], "categories": [...]}
      Business Logic: Tool discovery, permission-based filtering
      
    - POST /api/v1/dev-tools/execute/{tool_name}
      Request: {"input": "string", "options": {...}}
      Authentication: Required, user
      Response: {"output": "string", "execution_time": 125}
      Business Logic: Tool execution in sandboxed environment, result logging

Background Job Management:
  - GET /api/v1/jobs
    Query: ?status=running&service=workflow-engine&limit=50
    Authentication: Required, admin role
    Response: {"jobs": [...], "queue_depth": 15}
    Business Logic: Multi-service job monitoring, performance metrics
    
  - POST /api/v1/jobs/{job_id}/cancel
    Authentication: Required, job owner or admin
    Response: {"cancelled": true, "cleanup_status": "in_progress"}
    Business Logic: Graceful job termination, resource cleanup
```

#### WebSocket & Real-time Endpoints
```yaml
Real-time Communication:
  - WS /api/v1/ws/workflow-executions/{execution_id}
    Authentication: WebSocket auth token
    Purpose: Live workflow execution updates
    Events: {"type": "node_start", "node_id": "...", "timestamp": "..."}
    
  - WS /api/v1/ws/security-events
    Authentication: Required, security role
    Purpose: Real-time threat intelligence feed
    Events: {"type": "new_indicator", "severity": "high", "data": {...}}
    
  - WS /api/v1/ws/notifications/{user_id}
    Authentication: Required, user-specific token
    Purpose: Live notifications and alerts
    Events: {"type": "alert", "message": "...", "priority": "high"}
```

#### Legacy API Compatibility Layers
```yaml
MISP Compatibility:
  - All existing MISP REST endpoints preserved
  - Base path: /api/v1/misp-compat/*
  - Authentication: X-Authkey header support
  - Purpose: Seamless migration for existing MISP integrations
  
n8n Webhook Compatibility:
  - Webhook endpoints: /webhook/{workflow_id}
  - Authentication: Webhook-specific tokens
  - Purpose: External service integrations (Zapier, webhooks)
  
CyberChef Recipe URLs:
  - Recipe sharing: /api/v1/cyberchef/recipe/{recipe_id}
  - Purpose: Recipe sharing and bookmark compatibility
  - Response: CyberChef-compatible recipe JSON format
```

---

## Section 3: Integration Architecture Design [CRITICAL]

### 3.1 Modular Monolith Structure

```yaml
Proposed Architecture:
modular-security-platform/
├── apps/                           # Application entry points
│   ├── web-platform/              # FastAPI main application
│   ├── workflow-engine/           # n8n integration service
│   ├── security-intel/            # MISP + Nemesis integration
│   ├── content-management/        # Ghostwriter + Mealie + Actual Budget
│   ├── data-processing/           # Firecrawl + MTG tools
│   └── specialized-services/      # KasmVNC + CyberChef
├── modules/                       # Shared business logic modules
│   ├── auth/                     # Unified authentication
│   ├── notifications/            # Cross-platform notifications
│   ├── storage/                  # File storage abstraction
│   ├── queues/                   # Background job management
│   ├── search/                   # Elasticsearch/PostgreSQL search
│   └── integrations/             # External API clients
├── shared/                       # Common utilities
│   ├── database/                 # Database models and migrations
│   ├── api/                      # API utilities and middleware
│   ├── security/                 # Security utilities
│   └── monitoring/               # Logging and metrics
├── frontend/                     # Unified frontend
│   ├── components/               # Reusable UI components
│   ├── views/                    # Application-specific views
│   └── plugins/                  # Tool-specific plugins (IT-Tools, CyberChef)
└── docker/                       # Container configurations
```

### 3.2 Data Integration Strategy

#### Unified Database Schema Design
```yaml
Core Entities:
  users:                          # Unified user management
    - id: UUID (primary key)
    - username: VARCHAR(255) UNIQUE NOT NULL
    - email: VARCHAR(255) UNIQUE NOT NULL  
    - password_hash: VARCHAR(255) NOT NULL (bcrypt)
    - full_name: VARCHAR(255)
    - admin: BOOLEAN DEFAULT FALSE
    - active: BOOLEAN DEFAULT TRUE
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - last_login: TIMESTAMP WITH TIME ZONE
    - preferences: JSONB DEFAULT '{}'
    - oauth_providers: JSONB DEFAULT '[]' # Discord, Google, GitHub tokens
    
  organizations:                  # Multi-tenant support
    - id: UUID (primary key)
    - name: VARCHAR(255) NOT NULL
    - slug: VARCHAR(100) UNIQUE NOT NULL
    - settings: JSONB DEFAULT '{}'
    - subscription_tier: VARCHAR(50) DEFAULT 'free'
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - billing_info: JSONB
    
  projects:                      # Namespace for different tools
    - id: UUID (primary key) 
    - name: VARCHAR(255) NOT NULL
    - type: ENUM('workflow', 'security', 'content', 'analysis', 'financial')
    - organization_id: UUID REFERENCES organizations(id)
    - settings: JSONB DEFAULT '{}'
    - created_by: UUID REFERENCES users(id)
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - active: BOOLEAN DEFAULT TRUE

Application-Specific Entities:

  # n8n + Workflow Automation
  workflows:                     # n8n workflows + Dispatch incidents + Goose recipes
    - id: UUID (primary key)
    - name: VARCHAR(255) NOT NULL
    - type: ENUM('n8n_workflow', 'incident', 'ai_recipe', 'generic')
    - definition: JSONB NOT NULL  # Nodes, connections, settings
    - project_id: UUID REFERENCES projects(id)
    - created_by: UUID REFERENCES users(id)
    - active: BOOLEAN DEFAULT FALSE
    - tags: TEXT[] DEFAULT '{}'
    - trigger_count: INTEGER DEFAULT 0
    - last_execution: TIMESTAMP WITH TIME ZONE
    - execution_history: JSONB DEFAULT '[]'
    
  workflow_executions:           # Execution history and logs
    - id: UUID (primary key)
    - workflow_id: UUID REFERENCES workflows(id)
    - status: ENUM('running', 'success', 'failed', 'cancelled')
    - started_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - finished_at: TIMESTAMP WITH TIME ZONE  
    - execution_data: JSONB
    - error_message: TEXT
    - triggered_by: UUID REFERENCES users(id)
    
  # Security Intelligence (MISP + Nemesis + Maltrail + HELK)
  security_events:               # MISP events + Nemesis findings + Maltrail alerts
    - id: UUID (primary key)
    - event_uuid: UUID UNIQUE # For MISP compatibility
    - title: VARCHAR(500) NOT NULL
    - description: TEXT
    - event_type: ENUM('threat_intel', 'file_analysis', 'network_alert', 'incident')
    - severity: ENUM('info', 'low', 'medium', 'high', 'critical')
    - status: ENUM('new', 'in_progress', 'resolved', 'false_positive')
    - source_system: VARCHAR(100) # 'misp', 'nemesis', 'maltrail', 'helk'
    - indicators: JSONB DEFAULT '[]' # IOCs, file hashes, IPs, domains
    - tags: TEXT[] DEFAULT '{}'
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - organization_id: UUID REFERENCES organizations(id)
    - correlation_data: JSONB DEFAULT '{}'
    
  files_analyzed:                # Nemesis + CyberChef + Software Forensic Kit
    - id: UUID (primary key)
    - original_name: VARCHAR(500)
    - file_path: TEXT NOT NULL
    - mime_type: VARCHAR(100)
    - file_size: BIGINT
    - hashes: JSONB # MD5, SHA1, SHA256, etc.
    - upload_source: VARCHAR(100) # 'nemesis', 'cyberchef', 'forensic_kit'
    - analysis_results: JSONB DEFAULT '{}'
    - security_findings: TEXT[] DEFAULT '{}'
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - project_id: UUID REFERENCES projects(id)
    - analyzed_by: UUID REFERENCES users(id)
    
  # Content & Document Management (Ghostwriter + Mealie + Actual Budget)
  content_items:                 # Ghostwriter projects + Mealie recipes + Reports
    - id: UUID (primary key)
    - title: VARCHAR(500) NOT NULL
    - content_type: ENUM('ghostwriter_project', 'recipe', 'report', 'document')
    - content: TEXT # Recipe instructions, project notes, etc.
    - metadata: JSONB DEFAULT '{}' # Ingredients, client info, etc.
    - organization_id: UUID REFERENCES organizations(id)
    - created_by: UUID REFERENCES users(id)  
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - tags: TEXT[] DEFAULT '{}'
    - search_vector: TSVECTOR # PostgreSQL full-text search
    
  # Financial Data (Actual Budget)  
  financial_accounts:            # Actual Budget accounts
    - id: UUID (primary key)
    - name: VARCHAR(255) NOT NULL
    - account_type: ENUM('checking', 'savings', 'credit', 'investment', 'loan')
    - balance_current: BIGINT # Amount in cents
    - offbudget: BOOLEAN DEFAULT FALSE
    - closed: BOOLEAN DEFAULT FALSE
    - organization_id: UUID REFERENCES organizations(id)
    - sync_source: VARCHAR(100) # 'simpleFin', 'goCardless', etc.
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    
  financial_transactions:        # Actual Budget transactions
    - id: UUID (primary key)
    - account_id: UUID REFERENCES financial_accounts(id)
    - amount: BIGINT NOT NULL # Amount in cents, negative for expenses
    - payee: VARCHAR(255)
    - category: VARCHAR(255)  
    - date: DATE NOT NULL
    - cleared: BOOLEAN DEFAULT FALSE
    - notes: TEXT
    - parent_id: UUID REFERENCES financial_transactions(id) # For splits
    - imported_id: VARCHAR(255) # External sync ID
    
  # Analysis & Processing (Firecrawl + MTG Tools + IT-Tools results)
  analysis_results:              # Firecrawl results + MTG analysis + IT-Tools output
    - id: UUID (primary key)
    - tool_type: ENUM('firecrawl', 'mtg_analysis', 'it_tool', 'forensic_analysis')
    - input_data: JSONB NOT NULL # URLs, card data, input files, etc.
    - output_data: JSONB NOT NULL # Scraped content, analysis results, etc.
    - status: ENUM('pending', 'processing', 'completed', 'failed')
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - completed_at: TIMESTAMP WITH TIME ZONE
    - expires_at: TIMESTAMP WITH TIME ZONE # TTL for cleanup
    - created_by: UUID REFERENCES users(id)
    - project_id: UUID REFERENCES projects(id)

Shared Supporting Tables:
  files:                         # Unified file storage
    - id: UUID (primary key)
    - filename: VARCHAR(500) NOT NULL
    - file_path: TEXT NOT NULL # S3 path, local path, etc.
    - mime_type: VARCHAR(100)
    - file_size: BIGINT
    - file_hash: VARCHAR(64) # SHA256 for deduplication
    - created_by: UUID REFERENCES users(id)
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - associated_entity_type: VARCHAR(100) # 'workflow', 'security_event', etc.
    - associated_entity_id: UUID
    
  notifications:                 # Cross-platform notifications
    - id: UUID (primary key)
    - recipient_id: UUID REFERENCES users(id)
    - title: VARCHAR(500) NOT NULL
    - message: TEXT NOT NULL
    - channel: ENUM('email', 'slack', 'webhook', 'in_app')
    - status: ENUM('pending', 'sent', 'delivered', 'failed')
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - sent_at: TIMESTAMP WITH TIME ZONE
    - metadata: JSONB DEFAULT '{}' # Channel-specific data
    
  audit_logs:                    # Unified audit trail
    - id: UUID (primary key) 
    - user_id: UUID REFERENCES users(id)
    - action: VARCHAR(100) NOT NULL # 'create', 'update', 'delete', 'login'
    - entity_type: VARCHAR(100) NOT NULL # 'workflow', 'security_event', etc.
    - entity_id: UUID
    - changes: JSONB # Before/after values
    - ip_address: INET
    - user_agent: TEXT
    - timestamp: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    
  tags:                         # Global tagging system
    - id: UUID (primary key)
    - name: VARCHAR(100) NOT NULL
    - color: VARCHAR(7) # Hex color code
    - organization_id: UUID REFERENCES organizations(id)
    - created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    
  # Many-to-many relationship tables
  content_tags:                 # Tags for content items
    - content_id: UUID REFERENCES content_items(id)
    - tag_id: UUID REFERENCES tags(id)
    - PRIMARY KEY (content_id, tag_id)
    
  workflow_tags:                # Tags for workflows
    - workflow_id: UUID REFERENCES workflows(id)
    - tag_id: UUID REFERENCES tags(id)  
    - PRIMARY KEY (workflow_id, tag_id)
    
  user_organizations:           # User membership in organizations
    - user_id: UUID REFERENCES users(id)
    - organization_id: UUID REFERENCES organizations(id)
    - role: ENUM('owner', 'admin', 'editor', 'viewer')
    - joined_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    - PRIMARY KEY (user_id, organization_id)
```

#### Database Connection Strategy
```yaml
Primary Database: PostgreSQL 15+
  Configuration:
    - Max connections: 200
    - Shared among all modules via connection pooling
    - Connection pooling: pgbouncer (transaction mode)
    - Read replicas: For reporting and analytics queries
    
  Extensions Required:
    - pg_trgm: Full-text search capabilities (content_items, security_events)
    - pgcrypto: Encryption functions for sensitive data
    - uuid-ossp: UUID generation functions
    - pg_stat_statements: Query performance monitoring
    - pg_partman: Table partitioning for large datasets (audit_logs, workflow_executions)
    
  Indexing Strategy:
    - B-tree indexes: Foreign keys, timestamps, status fields
    - GIN indexes: JSONB columns (metadata, analysis_results, indicators)
    - GiST indexes: Full-text search vectors (search_vector columns)  
    - Partial indexes: Active records only (WHERE active = TRUE)
    - Composite indexes: Multi-column queries (organization_id + created_at)
    
Cache Layer: Redis 7+
  Usage:
    - Session storage: User sessions with 24h TTL
    - Rate limiting: API rate limits per user/IP with sliding window
    - Job queues: Background processing queues (Celery, BullMQ)
    - Caching: API responses (5min TTL), search results (1h TTL), file metadata (24h TTL)
    - Real-time data: WebSocket connections, live notifications
    
  Configuration:
    - Memory allocation: 4GB for production, 1GB for development
    - Persistence: AOF (append-only file) + RDB snapshots every 15min
    - Clustering: Single instance initially, Redis Cluster for horizontal scaling
    - Eviction policy: allkeys-lru for cache data, noeviction for sessions
```

### 3.3 Service Communication Patterns

#### Internal API Communication
```yaml
Pattern 1: Direct Module Imports (Preferred)
  Usage: Within same container/process
  Example: Mealie recipe parser → Notification module
  Benefits: Type safety, no network overhead, transaction support
  
Pattern 2: REST API Calls
  Usage: Cross-container communication
  Example: Workflow engine → Security intel platform
  Implementation: HTTP client with retry, circuit breaker
  Authentication: Internal JWT tokens, mutual TLS
  
Pattern 3: Message Queues (Async Operations)  
  Usage: Background processing, event-driven updates
  Example: File upload → Virus scanning → Notification
  Implementation: Redis Streams or RabbitMQ
  Benefits: Decoupling, reliability, scalability
  
Pattern 4: Database Events (Data Consistency)
  Usage: Cross-module data synchronization
  Example: User update triggers notification to all modules
  Implementation: PostgreSQL triggers + NOTIFY/LISTEN
  Benefits: ACID compliance, immediate consistency
```

#### External Integration Patterns  
```yaml
API Clients (Consolidated):
  Scryfall API: MTG card data (Commander Spellbook, MTG Toolkit)
    - Shared client library with caching
    - Rate limiting: 50-100 requests/second
    - Cache TTL: 24 hours for card data
    
  Discord OAuth: Authentication for multiple services
    - Shared OAuth handler
    - Guild membership validation
    - Webhook notifications
    
  LLM APIs: Goose agent integration
    - Shared client with multiple provider support
    - Token management and rate limiting
    - Conversation context handling
    
  MISP Feed APIs: Threat intelligence ingestion
    - Automated feed synchronization
    - Duplicate detection and correlation
    - Format standardization
```

### 3.4 Deployment Architecture

#### Container Orchestration Strategy
```yaml
Development Environment:
  Tool: Docker Compose
  Containers: 6 main services + PostgreSQL + Redis
  Resource Allocation: 16GB RAM, 8 CPU cores total
  Networking: Bridge network with service discovery
  
Production Environment:  
  Tool: Kubernetes or Docker Swarm
  High Availability: Multiple replicas per service
  Load Balancing: nginx ingress controller
  Resource Management: Resource limits and requests
  Monitoring: Prometheus + Grafana + ELK stack
  
Scaling Strategy:
  Horizontal: Add replicas for stateless services
  Vertical: Increase resources for data-intensive services
  Database: Read replicas, connection pooling
  Caching: Redis cluster for high-traffic scenarios
```

#### Service Dependencies and Startup Order
```yaml
Startup Sequence:
  1. Infrastructure: PostgreSQL, Redis
  2. Core Platform: Auth service, shared modules
  3. Data Services: Security intel, content management  
  4. Processing Services: Workflow engine, data processing
  5. Frontend: Web interface, specialized UIs
  6. Monitoring: Health checks, metrics collection
  
Health Check Strategy:
  Database: Connection test + simple query
  Redis: Ping command + memory check  
  Services: HTTP endpoint /health with dependency status
  Overall: Kubernetes readiness/liveness probes
```

---

## Section 5: External Integrations [IMPORTANT]

### 5.1 Third-Party API Consolidation Strategy

The integrated platform will consolidate external API usage across 23+ projects, reducing redundant integrations and implementing shared client libraries with unified authentication, caching, and rate limiting.

#### Critical APIs (Platform-Dependent)

**Scryfall Magic: The Gathering API**
```yaml
Service Name: Scryfall API
Purpose: MTG card database for Commander Spellbook, MTG Toolkit, and MTG Commander Map
Criticality: CRITICAL - 3 projects depend on this data
Projects Using: Commander Spellbook, MTG Scripting Toolkit, MTG Commander Map

Consolidation Strategy:
  - Shared Client Library: FastAPI service with unified caching
  - Rate Limiting: 100-175 requests/second shared pool
  - Cache Strategy: PostgreSQL + Redis, 24-hour TTL
  - Bulk Downloads: Daily synchronization of complete card database
  
Integration Details:
  - API Type: REST
  - Base URL: https://api.scryfall.com
  - Authentication: None (public API)
  
Unified Endpoints:
  - GET /cards/search: Complex queries with filtering
  - GET /cards/named: Individual card lookups  
  - GET /bulk-data/{type}: Complete database downloads
  - Image CDN: Scryfall card image hosting
  
Data Flow:
  - Direction: INBOUND - fetch card reference data
  - Format: JSON bulk downloads (~50MB compressed)
  - Volume: ~50,000 cards, daily sync
  - Local Storage: Full card database in PostgreSQL
  
Error Handling:
  - Network failure: Retry with exponential backoff
  - Rate limits: Respect 100req/sec, queue overflow requests
  - Service down: Use cached data, graceful degradation
```

**Large Language Model APIs (OpenAI, Anthropic, Others)**
```yaml
Service Name: LLM Provider APIs  
Purpose: AI-powered analysis for Goose, Firecrawl, HexStrike AI
Criticality: CRITICAL - Core functionality for multiple projects
Projects Using: Goose, Firecrawl, HexStrike AI, potentially others

Consolidation Strategy:
  - Multi-Provider Client: Unified interface supporting OpenAI, Claude, local models
  - Token Management: Shared token pools with cost tracking
  - Fallback Chain: Automatic provider switching on failures
  - Caching: Redis cache for similar requests
  
Integration Details:
  - Primary: OpenAI GPT-4/3.5 via https://api.openai.com/v1
  - Secondary: Anthropic Claude via https://api.anthropic.com/v1  
  - Local: Ollama integration for privacy-sensitive operations
  
Unified Endpoints:
  - POST /chat/completions: Conversation and analysis
  - POST /embeddings: Content similarity and search
  - POST /images/generations: Image analysis and generation
  
Authentication:
  - OpenAI: OPENAI_API_KEY bearer token
  - Anthropic: ANTHROPIC_API_KEY with custom headers
  - Ollama: Local service, no authentication
  
Data Flow:
  - Direction: BIDIRECTIONAL - send prompts, receive responses
  - Volume: Variable, potentially thousands of requests/day
  - Cost Management: Token counting and budget limits
  
Error Handling:
  - Rate limits: Provider-specific backoff strategies
  - Service failures: Automatic fallback to alternative providers
  - Token limits: Context window management and truncation
```

#### Important APIs (Feature Enhancement)

**Discord OAuth & Webhooks**
```yaml
Service Name: Discord Integration
Purpose: Authentication and community integration
Criticality: IMPORTANT - Affects user accounts, community features
Projects Using: Commander Spellbook, Ghostwriter, potentially others

Consolidation Strategy:
  - Shared OAuth Handler: Unified Discord authentication service
  - Webhook Management: Centralized Discord bot and notifications
  - Guild Integration: Community membership validation
  
Integration Details:
  - OAuth Base URL: https://discord.com/api/oauth2/
  - Bot API: https://discord.com/api/
  - Authentication: Client ID + Client Secret + Bot Token
  
OAuth Configuration:
  - Scopes: identify, email, guilds.members.read
  - Redirect URI: /auth/discord/callback/
  - Token Lifetime: 5 minutes (JWT), 1 day refresh
  
Webhook Endpoints:
  - POST /channels/{id}/messages: Send notifications
  - GET /users/@me/guilds: Verify guild membership
  - GET /users/@me: User profile information
  
Data Flow:
  - Direction: BIDIRECTIONAL - OAuth flow + webhook notifications
  - User Data: Discord ID, username, email, guild memberships
  - Notifications: Real-time updates to Discord channels
```

**Google Workspace APIs**
```yaml
Service Name: Google Workspace (Drive, Docs, Calendar, Sheets)
Purpose: Document generation, scheduling, data import
Criticality: IMPORTANT - Enhances workflow automation
Projects Using: Dispatch, Commander Spellbook (sheets), n8n workflows

Consolidation Strategy:
  - Service Account: Unified Google service account
  - OAuth Management: Shared user consent flows
  - API Client: Single client library for all Google services
  
Integration Details:
  - Base URL: https://www.googleapis.com/
  - Authentication: Service Account + OAuth 2.0
  - Credentials: GOOGLE_SERVICE_ACCOUNT_KEY + user tokens
  
Key Endpoints:
  - Drive API: Document and folder creation
  - Docs API: Document content generation and updates
  - Calendar API: Meeting scheduling and management
  - Sheets API: Data import and export
  
Use Cases:
  - Dispatch: Incident documentation and meeting scheduling
  - Commander Spellbook: Data import from community sheets
  - n8n: Workflow automation with Google services
  
Rate Limits:
  - Drive: 1000 requests per 100 seconds
  - Docs: 100 requests per 100 seconds per user
  - Calendar: Standard API limits per service
```

**Financial Institution APIs**
```yaml
Service Name: Banking and Payment Integration
Purpose: Transaction import and payment processing
Criticality: IMPORTANT - Core functionality for Actual Budget
Projects Using: Actual Budget, potentially Mealie (receipts)

Consolidation Strategy:
  - Unified Banking Client: Support multiple providers
  - Secure Credential Storage: Encrypted token management
  - Transaction Normalization: Standardized transaction format
  
Banking Providers:
  - SimpleFIN: US bank account synchronization
  - GoCardless: European Open Banking API
  - Plaid: Alternative US banking integration
  
Integration Details:
  - SimpleFIN: https://bridge.simplefin.org
  - GoCardless: https://ob.gocardless.com
  - Authentication: Provider-specific OAuth + API keys
  
Data Flow:
  - Direction: INBOUND - fetch account and transaction data
  - Frequency: User-triggered or scheduled sync
  - Security: End-to-end encryption, PCI compliance
  - Volume: Varies by user activity, typically daily sync
```

#### Nice-to-Have APIs (Optional Features)

**Notification and Communication Services**
```yaml
Service Name: Multi-Channel Notifications
Purpose: Email, SMS, push notifications across platform
Criticality: NICE-TO-HAVE - Improves user experience
Projects Using: Multiple projects for alerts and notifications

Consolidation Strategy:
  - Notification Gateway: Unified service for all channels
  - Template Management: Shared notification templates
  - Preference Engine: User notification preferences
  
Providers:
  - Email: SendGrid, AWS SES, or SMTP
  - SMS: Twilio, AWS SNS
  - Push: Firebase Cloud Messaging
  - Slack: Shared workspace notifications
  
Integration Pattern:
  - Unified API: POST /notifications with channel selection
  - Template Engine: Jinja2 templates with localization
  - Delivery Tracking: Read receipts and bounce handling
```

**Analytics and Monitoring Services**
```yaml
Service Name: Analytics and Performance Monitoring
Purpose: User behavior tracking, performance monitoring, error reporting
Criticality: NICE-TO-HAVE - Operational insights
Projects Using: All web-based projects

Consolidation Strategy:
  - Unified Analytics: Single analytics service for all projects
  - Privacy Compliance: GDPR/CCPA compliant data collection
  - Custom Events: Standardized event tracking schema
  
Providers:
  - Analytics: Google Analytics 4, Plausible, or self-hosted
  - Error Tracking: Sentry, Rollbar, or self-hosted
  - Performance: New Relic, DataDog, or Prometheus
  
Implementation:
  - Client-Side: Unified JavaScript tracking library
  - Server-Side: Structured logging with event correlation
  - Privacy: Cookie consent and data anonymization
```

### 5.2 Authentication Provider Consolidation

#### Primary Authentication Strategy

**Unified Identity Service**
```yaml
Architecture: FastAPI-based identity service with multi-provider support
Database: PostgreSQL users table with provider linking
Session Management: JWT with Redis session storage

Supported Providers:
  - Discord OAuth: Primary for gaming/community features
  - Google OAuth: Enterprise and productivity workflows
  - GitHub OAuth: Developer-focused tools
  - LDAP/Active Directory: Enterprise deployments
  
Multi-Factor Authentication:
  - TOTP: Time-based one-time passwords via QR codes
  - SMS: Optional SMS-based 2FA via Twilio
  - Hardware Keys: FIDO2/WebAuthn support
  - Backup Codes: Generated recovery codes
```

#### User Data Mapping Strategy

```yaml
Unified User Schema:
  - user_id: UUID (primary identifier)
  - email: Primary email from any provider
  - username: Display name (provider-specific fallback)
  - avatar_url: Profile image from provider
  - provider_id: External provider identifier
  - provider_type: discord, google, github, ldap
  
Cross-Provider Linking:
  - Same Email: Automatic account linking
  - Manual Linking: User-initiated account connection
  - Provider Migration: Transfer data between providers
  
Permission Mapping:
  - Discord Guilds → User Groups
  - Google Workspace → Organization Roles  
  - GitHub Organizations → Team Memberships
  - LDAP Groups → Application Permissions
```

### 5.3 External Service Dependencies

#### Critical Infrastructure Dependencies

**Database and Caching**
```yaml
PostgreSQL 15+:
  - Purpose: Primary data store for all consolidated projects
  - Criticality: CRITICAL - Complete platform dependency
  - Backup Strategy: Automated daily backups + point-in-time recovery
  - High Availability: Master-slave replication for production
  
Redis 7+:
  - Purpose: Session storage, caching, message queues
  - Criticality: IMPORTANT - Performance and session management
  - Persistence: AOF + RDB for data durability
  - Clustering: Redis cluster for horizontal scaling
```

**Content Delivery and Storage**
```yaml
File Storage:
  - Local: Docker volumes for development
  - Production: S3-compatible storage (AWS S3, MinIO, DigitalOcean Spaces)
  - Purpose: File uploads, generated reports, cached content
  
CDN Integration:
  - Scryfall Images: Direct hotlinking (permitted by Scryfall)
  - Static Assets: Optional CDN for CSS/JS (CloudFlare, AWS CloudFront)
  - User Uploads: CDN distribution for uploaded files
```

#### External Monitoring and Alerting

**Health Check Integrations**
```yaml
Health Check Strategy:
  - Internal: /health endpoints for each service
  - External API: Automated testing of third-party API availability
  - Database: Connection pool monitoring and query performance
  - Queue Health: Redis queue depth and processing rates
  
Alerting Channels:
  - Email: Critical system alerts
  - Discord: Community notifications for service status
  - Slack: Team notifications for operational issues
  - PagerDuty: Escalation for production incidents
```

#### Tribal Knowledge & Integration Gotchas

**Rate Limiting and API Limits**
```yaml
Critical Lessons Learned:
  - Scryfall API: Undocumented ~100-175 req/sec limit, needs User-Agent header
  - Google APIs: Scope management crucial to avoid user consent issues  
  - Discord API: Rate limits aggressive, requires proper queuing
  - OpenAI API: Token counting varies by model, context window management critical
  - Slack API: Block kit formatting complex, rate limits poorly documented
  
Best Practices:
  - Always implement exponential backoff with jitter
  - Cache aggressively but respect cache invalidation
  - Monitor API quotas and costs proactively
  - Implement circuit breakers for external service failures
  - Log all API interactions for debugging and billing
```

**Security and Compliance Considerations**
```yaml
API Security Standards:
  - HTTPS Only: All external API communication over TLS 1.3+
  - Secret Management: HashiCorp Vault or Kubernetes secrets
  - API Key Rotation: Automated rotation for long-lived keys
  - Network Security: API calls through VPC/private networks when possible
  
Compliance Requirements:
  - PCI DSS: Financial data handling (Actual Budget)
  - GDPR: User data processing and right to deletion
  - SOC 2: Security controls for business-critical integrations
  - Data Residency: Location restrictions for certain data types
```

---

## Section 6: Frontend Architecture Consolidation [IMPORTANT]

### 6.1 Framework Standardization Strategy

The integrated platform will consolidate multiple frontend frameworks (Vue.js, React, Next.js, Django templates) into a unified Vue.js 3 + TypeScript architecture, while preserving specialized applications where migration costs exceed benefits.

#### Primary Frontend Stack Decision

**Vue.js 3 + TypeScript + Vite (Primary)**
```yaml
Framework Selection: Vue.js 3 with Composition API + TypeScript
Rationale:
  - Used by: n8n, IT-Tools, Mealie (3 major projects)
  - Learning Curve: Easier than React, better DX
  - TypeScript Integration: Excellent native support
  - Component Reusability: High reuse potential across projects
  - Build Performance: Vite for fast development and builds
  - Ecosystem: Rich component library ecosystem

Migration Priority:
  - Migrate: Commander Spellbook (Next.js → Vue.js)
  - Migrate: Ghostwriter admin panels (Django + React → Vue.js)
  - Migrate: Nemesis frontend (React → Vue.js)
  - Preserve: Actual Budget (mature React codebase, migration cost too high)
  
Component Library: Naive UI (proven in IT-Tools) + Vuetify (proven in Mealie)
Styling Strategy: Tailwind CSS + CSS Modules for component-specific styles
```

**React 18 + TypeScript (Secondary - Specialized Applications)**
```yaml
Preserved Applications:
  - Actual Budget: Complex financial UI with mature React ecosystem integration
  - Inspector MCP: Debugging tool with React ecosystem dependencies
  
Rationale for Preservation:
  - Migration cost exceeds benefits
  - Specialized component libraries (financial charts, debugging tools)
  - Stable, well-functioning codebases
  - Integration with React-specific ecosystems
```

### 6.2 Unified Component Architecture

#### Shared Design System

**Component Organization Strategy**
```yaml
Shared Component Library:
  Location: packages/shared-ui/
  Framework: Vue.js 3 components with TypeScript
  Compatibility: Web Components wrapper for React interop
  
Organization Pattern:
  - Feature-based: components/[feature]/
  - Atomic Design: atoms/, molecules/, organisms/, templates/
  - Domain-specific: components/security/, components/workflow/, etc.

Design System Components:
  Navigation:
    - UnifiedTopbar: Global navigation with user authentication
    - ProjectSidebar: Per-project navigation menu
    - Breadcrumbs: Hierarchical navigation component
    
  Data Display:
    - DataTable: Unified table with sorting, filtering, pagination
    - MetricsCard: Consistent metrics display (for dashboards)
    - StatusIndicator: Health status for systems/services
    - ChartContainer: Wrapper for different chart libraries
    
  Forms:
    - FormBuilder: Dynamic form generation from JSON schemas
    - ValidationInput: Consistent validation and error display
    - FileUpload: Multi-format file upload with progress
    - SearchInput: Unified search with autocomplete
    
  Security-Specific:
    - ThreatIndicator: IOC display with risk scoring
    - LogViewer: Structured log display with highlighting
    - NetworkDiagram: Visual network topology representation
```

**Styling Consolidation**
```yaml
CSS Framework: Tailwind CSS v3+ (utility-first)
Component Styling: CSS Modules for component-specific styles
Theme System: CSS custom properties with dark/light mode support

Color Palette:
  - Primary: Blue (#2563eb) - Actions, links, primary CTAs
  - Secondary: Gray (#6b7280) - Text, borders, backgrounds  
  - Success: Green (#10b981) - Success states, positive metrics
  - Warning: Amber (#f59e0b) - Warnings, pending states
  - Error: Red (#ef4444) - Errors, critical alerts
  - Security: Orange (#f97316) - Security alerts, IOCs

Typography:
  - Primary Font: Inter (web-safe, excellent readability)
  - Monospace: JetBrains Mono (code, logs, technical data)
  - Heading Scale: Tailwind's default scale (text-xs to text-9xl)
  
Responsive Strategy:
  - Mobile-first: sm (640px), md (768px), lg (1024px), xl (1280px)
  - Primary Target: Desktop (most cybersecurity tools are desktop-focused)
  - Mobile Support: Essential for notifications, basic monitoring
```

#### Application-Specific UI Patterns

**Cybersecurity Tools (MISP, Rita, Maltrail, Nemesis)**
```yaml
UI Pattern: Dark theme, high-density information display
Key Components:
  - ThreatDashboard: Real-time threat visualization
  - IOCList: Indicators of Compromise with metadata
  - Timeline: Security event chronology
  - NetworkMap: Interactive network topology
  - AlertPanel: Priority-based alert display

Data Visualization:
  - Charts: Chart.js for time series, D3.js for network diagrams
  - Maps: Leaflet for geolocation visualization
  - Tables: Virtual scrolling for large datasets (thousands of IOCs)
  - Real-time: WebSocket updates for live threat feeds
```

**Workflow & Automation (n8n, Dispatch, Goose)**
```yaml
UI Pattern: Process-oriented, step-by-step interfaces
Key Components:
  - WorkflowBuilder: Drag-and-drop workflow editor (n8n style)
  - ProcessStepper: Multi-step process with validation
  - TaskQueue: Background job status and management
  - ExecutionLog: Detailed execution trace with debugging
  - TemplateLibrary: Reusable workflow/recipe templates

Interaction Patterns:
  - Drag-and-Drop: Vue Draggable for workflow nodes
  - Real-time Updates: Live execution status via WebSocket
  - Form Validation: Real-time validation with error recovery
  - Progressive Disclosure: Show detail on demand
```

**Content & Productivity (Mealie, Actual Budget, IT-Tools)**
```yaml
UI Pattern: Clean, user-friendly, mobile-responsive
Key Components:
  - ContentCard: Recipe cards, budget summaries, tool cards
  - SearchInterface: Faceted search with filters
  - ImportWizard: Multi-step data import process
  - Calculator: Tool-specific calculation interfaces
  - ReportBuilder: Generate and export reports

User Experience:
  - Progressive Web App: Offline capability for mobile use
  - Accessibility: WCAG 2.1 AA compliance
  - Internationalization: Multi-language support via Vue I18n
  - Performance: Lazy loading, virtual scrolling, code splitting
```

### 6.3 State Management Consolidation

#### Unified State Architecture

**Pinia (Vue.js Global State)**
```yaml
State Management: Pinia stores for Vue.js applications
Architecture: Feature-based stores with composition API

Core Stores:
  - AuthStore: Authentication, user sessions, permissions
  - ProjectStore: Current project context, settings, preferences  
  - NotificationStore: Toast notifications, alerts, system messages
  - ThemeStore: UI theme, dark/light mode, user preferences
  
Application Stores:
  - SecurityStore: Threat data, IOCs, security events (MISP, Rita, etc.)
  - WorkflowStore: Workflow state, execution status (n8n, Dispatch)
  - ContentStore: Recipes, budgets, tool results (Mealie, Actual, IT-Tools)

Store Communication:
  - Cross-store composables for shared functionality
  - Event-driven updates via custom event system
  - WebSocket integration for real-time data sync
```

**React State Management (Preserved Applications)**
```yaml
Actual Budget: Redux Toolkit + Custom IPC layer
  - Mature state management for financial data
  - Complex undo/redo functionality
  - File-based data synchronization
  
Inspector MCP: React Context + useState
  - Debugging tool with simple state requirements
  - Connection state and transport configuration
  - Live data updates from MCP servers
```

#### Data Synchronization Strategy

**API State Management**
```yaml
Vue.js Applications:
  - HTTP Client: Axios with interceptors for auth/error handling
  - Caching: Vue Query (TanStack Query for Vue) for server state
  - Real-time: WebSocket composables with automatic reconnection
  - Offline: Service Worker with background sync

React Applications:
  - Actual Budget: Custom IPC layer (existing)
  - Inspector: Fetch API with custom hooks
  
Cross-Framework Communication:
  - Shared WebSocket connections via browser events
  - Local Storage for cross-app user preferences
  - Browser events for navigation coordination
```

### 6.4 Routing & Navigation Consolidation

#### Unified Navigation Experience

**Multi-Application Router**
```yaml
Architecture: Client-side routing with cross-app navigation
Primary Router: Vue Router 4 for Vue.js applications
Secondary: React Router for preserved React applications

Navigation Pattern:
  - Global Navigation: Unified top bar across all applications
  - Application Switcher: Dropdown/sidebar to switch between tools
  - Breadcrumb Navigation: Hierarchical context across applications
  - Deep Linking: Direct links to specific application states

URL Structure:
  - Base: https://platform.domain.com/
  - Applications: /[app-name]/[feature]/[resource]
  - Examples:
    - /misp/events/timeline
    - /n8n/workflows/editor
    - /mealie/recipes/search
    - /actual/budgets/monthly
```

**Authentication & Authorization Guards**
```yaml
Route Protection:
  - Authentication Guard: JWT token validation
  - Authorization Guard: Role-based access control (RBAC)
  - Project Guard: Project membership validation
  - Feature Guard: Feature flag-based access control

Implementation:
  - Vue.js: Vue Router beforeEach navigation guards
  - React: Higher-order components (HOCs) for route protection
  - Shared: JWT validation service with role checking
  
Session Management:
  - Single Sign-On (SSO): Shared JWT across all applications
  - Session Persistence: Refresh token rotation
  - Logout Propagation: Global logout across all apps
```

### 6.5 Performance & Optimization Strategy

#### Bundle Optimization

**Code Splitting & Lazy Loading**
```yaml
Application-Level Splitting:
  - Each major application as separate chunk
  - Shared components in common chunk
  - Third-party libraries in vendor chunk

Route-Level Splitting:
  - Each route/page as separate chunk
  - On-demand loading for better initial load time
  - Prefetch critical routes based on user behavior

Component-Level Splitting:
  - Heavy components (charts, editors) as async components
  - Modal dialogs and overlays as separate chunks
  - Large data tables with virtual scrolling

Build Optimization:
  - Vite: Fast build system with Hot Module Replacement (HMR)
  - Tree Shaking: Remove unused code from final bundles
  - Asset Optimization: Image compression, font subsetting
  - Service Worker: Caching strategy for offline functionality
```

**Performance Monitoring**
```yaml
Core Web Vitals Tracking:
  - Largest Contentful Paint (LCP): Target <2.5s
  - First Input Delay (FID): Target <100ms
  - Cumulative Layout Shift (CLS): Target <0.1

Bundle Analysis:
  - Bundle size monitoring with alerts for regression
  - Dependency analysis to identify optimization opportunities
  - Performance budgets enforced in CI/CD pipeline

Runtime Performance:
  - Vue Devtools for component performance profiling
  - React DevTools for preserved React applications
  - Memory leak detection and prevention
  - Long-running task monitoring (security scans, data processing)
```

#### User Experience Optimization

**Progressive Enhancement**
```yaml
Mobile-First Design:
  - Responsive breakpoints: 640px, 768px, 1024px, 1280px
  - Touch-friendly interfaces for mobile devices
  - Offline-first approach with service worker caching
  - Progressive Web App (PWA) capabilities

Accessibility (WCAG 2.1 AA):
  - Keyboard navigation support
  - Screen reader compatibility
  - High contrast mode support
  - Focus management and aria labels

International Support:
  - Vue I18n for internationalization
  - RTL language support
  - Timezone handling for global deployments
  - Localized number, date, and currency formatting
```

---

## Section 4: Migration Strategy & Risk Assessment [CRITICAL]

### 4.1 Migration Phases

#### Phase 1: Infrastructure Consolidation (Weeks 1-4)
```yaml
Objectives:
  - Set up unified PostgreSQL and Redis infrastructure
  - Implement shared authentication system
  - Create base container images and deployment scripts
  
Priority Projects (Low Risk):
  - IT-Tools: Pure client-side, minimal backend integration
  - FileScopeMCP: Simple Node.js service, easy to containerize
  - Inspector: Stateless proxy service
  - MTG Scripting Toolkit: Data processing scripts, file-based
  
Migration Approach:
  1. Set up base FastAPI application with shared modules
  2. Migrate IT-Tools as Vue.js frontend plugin
  3. Integrate FileScopeMCP as Node.js module
  4. Package Inspector as service endpoint
  5. Convert MTG Toolkit to API endpoints
  
Success Criteria:
  - [ ] Unified authentication working
  - [ ] 4 projects successfully integrated
  - [ ] Basic monitoring and logging in place
  - [ ] CI/CD pipeline established
  
Risk Level: LOW
```

#### Phase 2: Core Applications (Weeks 5-12)  
```yaml
Priority Projects (Medium Risk):
  - Mealie: Well-structured FastAPI, PostgreSQL-ready
  - Actual Budget: TypeScript/React, needs database migration
  - Commander Spellbook: Django application, complex data model
  - Dispatch: FastAPI application, incident management logic
  
Migration Approach:
  1. Migrate Mealie backend to shared FastAPI instance
  2. Convert Actual Budget to PostgreSQL while preserving SQLite sync
  3. Integrate Commander Spellbook Django app as module
  4. Move Dispatch incident management to shared platform
  5. Unify frontend components and authentication flows
  
Database Migration Strategy:
  - Create unified schema with project-specific namespaces
  - Implement data migration scripts with rollback capability
  - Maintain API compatibility during transition
  - Use feature flags for gradual rollout
  
Success Criteria:
  - [ ] 8 total projects integrated (4 new + 4 from Phase 1)
  - [ ] All core functionality preserved
  - [ ] Performance within 10% of standalone versions
  - [ ] Zero data loss during migration
  
Risk Level: MEDIUM
```

#### Phase 3: Complex Workflow Systems (Weeks 13-20)
```yaml
Priority Projects (High Risk):
  - n8n: Complex workflow engine, 400+ integrations
  - MISP: Legacy PHP application, extensive data model
  - Goose: Rust-based AI agent, complex LLM integration
  - Nemesis: Multi-service architecture, async processing
  
Migration Approach:
  1. Deploy n8n as dedicated microservice with API integration
  2. Create MISP compatibility layer (REST API to legacy PHP)
  3. Containerize Goose as standalone service with gRPC API
  4. Rebuild Nemesis core services in unified Python environment
  5. Implement workflow orchestration between services
  
Special Considerations:
  - n8n: Preserve workflow execution engine, migrate UI to unified frontend
  - MISP: Gradual migration from CakePHP to FastAPI modules
  - Goose: Maintain Rust performance, add REST API wrapper
  - Nemesis: Consolidate microservices while preserving processing pipeline
  
Success Criteria:
  - [ ] 12 total projects integrated
  - [ ] All workflow automation preserved
  - [ ] Threat intelligence sharing operational  
  - [ ] AI agent functionality maintained
  
Risk Level: HIGH
```

#### Phase 4: Specialized Services (Weeks 21-24)
```yaml
Priority Projects (Variable Risk):
  - KasmVNC: C++ desktop virtualization (Complex deployment)
  - CyberChef: JavaScript operations (Easy integration)
  - Security Tools: HELK, Maltrail, HexStrike AI, Software Forensic Kit
  - Content Management: Ghostwriter, Firecrawl
  
Migration Approach:
  1. Integrate CyberChef as frontend plugin with API endpoints
  2. Deploy KasmVNC as specialized container with proxy integration
  3. Consolidate security tools into unified analysis platform
  4. Merge Ghostwriter and Firecrawl into content management module
  5. Implement cross-tool data sharing and workflow integration
  
Success Criteria:
  - [ ] All 23 projects integrated or accessible
  - [ ] Unified user experience across all tools
  - [ ] Performance optimization completed
  - [ ] Full documentation and training materials ready
  
Risk Level: VARIABLE
```

### 4.2 Risk Assessment Matrix

#### Technical Risks
```yaml
Data Migration Risks:
  Risk: Data loss during PostgreSQL consolidation
  Likelihood: Medium
  Impact: High
  Mitigation:
    - Complete database backups before migration
    - Implement migration scripts with rollback capability
    - Test migrations on production data copies
    - Gradual migration with parallel systems during transition
  
  Risk: Performance degradation in shared database
  Likelihood: High
  Impact: Medium
  Mitigation:
    - Implement connection pooling (pgbouncer)
    - Use read replicas for reporting queries
    - Database query optimization and indexing
    - Implement caching layer (Redis) for frequently accessed data
    
  Risk: API compatibility breaking during consolidation
  Likelihood: Medium
  Impact: High
  Mitigation:
    - Version all APIs during transition
    - Implement API compatibility layer
    - Gradual deprecation of old endpoints
    - Extensive integration testing

Authentication Integration Risks:
  Risk: User access disruption during auth system migration
  Likelihood: Medium
  Impact: High
  Mitigation:
    - Implement authentication federation during transition
    - Preserve existing login methods during migration
    - Gradual user migration with fallback options
    - Extensive testing of OAuth flows
```

#### Business Risks
```yaml
Service Availability Risks:
  Risk: Extended downtime during migration
  Likelihood: Medium
  Impact: High
  Mitigation:
    - Blue-green deployment strategy
    - Rolling updates for non-critical services
    - Maintenance windows during low-usage periods
    - Comprehensive rollback procedures
    
  Risk: User adoption resistance due to interface changes
  Likelihood: High
  Impact: Medium
  Mitigation:
    - Preserve existing UI workflows where possible
    - Implement interface customization options
    - Comprehensive user training and documentation
    - Gradual feature rollout with user feedback integration
    
  Risk: Integration complexity exceeding timeline
  Likelihood: High
  Impact: Medium
  Mitigation:
    - Prioritize critical business functions
    - Implement minimum viable product approach
    - Plan for extended timeline buffer (25% additional)
    - Consider keeping some services as external integrations
```

#### Security Risks
```yaml
Attack Surface Risks:
  Risk: Increased attack surface due to consolidated authentication
  Likelihood: Medium
  Impact: High
  Mitigation:
    - Implement multi-factor authentication
    - Use OAuth2/OIDC best practices
    - Regular security audits and penetration testing
    - Implement comprehensive audit logging
    
  Risk: Cross-service data exposure
  Likelihood: Low
  Impact: High
  Mitigation:
    - Implement strict role-based access control (RBAC)
    - Data encryption at rest and in transit
    - Service-level authorization checks
    - Regular access reviews and compliance audits
```

---

## Section 5: Implementation Roadmap [IMPORTANT]

### 5.1 Technology Stack Decisions

#### Primary Technology Choices
```yaml
Backend Framework: FastAPI + Python 3.11
  Rationale: 
    - Used by 6 projects already (Mealie, Dispatch, Nemesis, HexStrike AI)
    - Excellent async support for high-performance APIs
    - Automatic OpenAPI documentation generation
    - Strong typing support with Pydantic
    - Easy integration with PostgreSQL and Redis
  
  Alternative: Express.js + TypeScript for Node.js modules
  
Frontend Framework: Vue.js 3 + TypeScript
  Rationale:
    - Used by n8n, IT-Tools, Mealie
    - Easier learning curve than React
    - Excellent TypeScript integration
    - Component reusability across projects
    - Good ecosystem for UI libraries (Vuetify, Quasar)
  
  Alternative: React 18 for projects requiring it (Actual Budget, Commander Spellbook)

Database: PostgreSQL 15 + Redis 7
  Rationale:
    - PostgreSQL: JSONB support, full-text search, mature ecosystem
    - Redis: Session storage, caching, job queues
    - Both have excellent Python and Node.js support
    - Proven scalability and reliability
```

#### Development Tools Standardization  
```yaml
Package Management:
  Python: Poetry (modern dependency management, virtual environments)
  Node.js: pnpm (fast installs, workspace support)
  
Build Tools:
  Backend: Poetry build + Docker multi-stage builds
  Frontend: Vite (fast builds, HMR, TypeScript support)
  
Code Quality:
  Python: Ruff (linting + formatting), pytest (testing), mypy (type checking)
  TypeScript: ESLint + Prettier, Vitest (testing)
  
CI/CD: GitHub Actions
  - Automated testing on all PRs
  - Security scanning (Snyk, CodeQL)
  - Automated deployment to staging/production
  - Performance regression testing
```

### 5.2 Infrastructure Architecture

#### Container Strategy (Final)
```yaml
Container 1: Core Web Platform
  Services: FastAPI main app + Vue.js frontend + nginx
  Projects: Mealie, Dispatch, HexStrike AI, IT-Tools (frontend)
  Resources: 4GB RAM, 2 CPU cores
  Scaling: Horizontal (2-4 replicas)
  
Container 2: Workflow & Automation Hub  
  Services: n8n engine + Goose API + FileScopeMCP
  Resources: 6GB RAM, 3 CPU cores  
  Scaling: Vertical (workflow execution memory intensive)
  
Container 3: Security Intelligence Platform
  Services: MISP integration + Nemesis services + Security tools
  Resources: 8GB RAM, 4 CPU cores
  Scaling: Horizontal for analysis, vertical for data processing
  
Container 4: Content & Financial Management
  Services: Ghostwriter + Actual Budget + Commander Spellbook
  Resources: 3GB RAM, 2 CPU cores
  Scaling: Horizontal (stateless after database migration)
  
Container 5: Data Processing Services
  Services: Firecrawl + MTG tools + Software Forensic Kit
  Resources: 4GB RAM, 2 CPU cores
  Scaling: Horizontal with job queuing
  
Container 6: Specialized Infrastructure
  Services: KasmVNC + CyberChef host + proxy services
  Resources: 4GB RAM, 2 CPU cores
  Scaling: Vertical (desktop virtualization intensive)
  
Total Resources: 29GB RAM, 15 CPU cores (vs 100GB+ for 23 separate containers)
```

#### Networking & Security
```yaml
Network Architecture:
  External: nginx load balancer with SSL termination
  Internal: Service mesh with mutual TLS (Istio or similar)
  Database: Private network, connection pooling
  
Security Implementation:
  Authentication: OAuth2 + JWT with refresh tokens
  Authorization: RBAC with project-level permissions
  API Security: Rate limiting, input validation, SQL injection prevention
  Container Security: Non-root users, read-only filesystems, security scanning
  
Monitoring Stack:
  Metrics: Prometheus + Grafana
  Logging: ELK Stack (Elasticsearch, Logstash, Kibana)
  Tracing: Jaeger for distributed tracing
  Alerting: PagerDuty integration for critical issues
```

### 5.3 Success Metrics & KPIs

#### Performance Metrics
```yaml
Response Time Targets:
  - API endpoints: <200ms 95th percentile
  - Database queries: <100ms average
  - Frontend loading: <2s initial load, <500ms subsequent navigation
  - Background jobs: Start within 5 seconds of queuing
  
Availability Targets:
  - Overall system: 99.9% uptime (8.7 hours downtime/year)
  - Critical services: 99.99% uptime (52 minutes downtime/year)
  - Planned maintenance: <4 hours/month during low-usage windows
  
Scalability Targets:
  - Concurrent users: Support 1000 concurrent users per container
  - Database connections: <80% of max connections during peak
  - Memory usage: <80% of allocated memory during normal operations
  - CPU usage: <70% average during peak loads
```

#### Business Metrics  
```yaml
Migration Success:
  - Feature parity: 100% of critical features preserved
  - Data integrity: Zero data loss during migration
  - User adoption: >90% of users successfully migrated within 3 months
  - Performance: No more than 10% performance degradation
  
Operational Efficiency:
  - Deployment time: <30 minutes for full stack deployment
  - Recovery time: <15 minutes for critical service recovery
  - Development velocity: 50% reduction in deployment complexity
  - Resource utilization: 70% reduction in total resource requirements
```

---

## Section 7: Testing & Quality Assurance Strategy [IMPORTANT]

### 7.1 Unified Testing Architecture

The consolidated platform requires a comprehensive testing strategy that spans multiple languages, frameworks, and testing concerns while maintaining consistency across all integrated projects.

#### Testing Framework Consolidation

**Python/FastAPI Services (Primary Backend)**
```yaml
Unit Testing Framework: pytest + pytest-asyncio
Coverage Target: 85%+ for critical business logic
Location: tests/ directory mirroring src/ structure
Configuration: pytest.ini with async support, coverage reporting

Test Categories:
  unit_tests:
    - Business Logic: Core algorithms, data processing, security analysis
    - API Endpoints: FastAPI route handlers, validation, error handling
    - Data Models: Pydantic models, SQLAlchemy entities, validation
    - Utilities: Helper functions, data transformers, format converters
  
  integration_tests:
    - Database Operations: PostgreSQL queries, transactions, migrations
    - External APIs: Third-party integrations with mocking
    - Message Queues: Redis pub/sub, job queue processing
    - Authentication: JWT validation, OAuth flows, permission checking
  
  async_tests:
    - Concurrent Operations: Multi-threaded security scanning
    - WebSocket Connections: Real-time updates, pub/sub patterns
    - Background Tasks: Long-running analysis jobs, data synchronization
    - Resource Management: Connection pooling, cleanup procedures

Critical Components Requiring High Coverage:
  - Security Analysis Engines (MISP, Nemesis, YARA-X)
  - Workflow Execution Logic (n8n, Dispatch automation)
  - Data Processing Pipelines (Firecrawl, HexStrike AI)
  - Financial Calculations (Actual Budget import/export)
```

**Vue.js Frontend Applications**
```yaml
Unit Testing Framework: Vitest (Vite-native, fast execution)
Component Testing: Vue Test Utils + @testing-library/vue
E2E Testing Framework: Playwright (cross-browser, reliable)
Coverage Target: 75%+ for critical user interfaces

Test Structure:
  unit_tests:
    - Component Logic: Vue components, computed properties, watchers
    - Composables: Reusable composition functions, API clients
    - Utilities: Pure functions, data formatters, validation helpers
    - Store Logic: Pinia stores, state mutations, getters
  
  integration_tests:
    - Component Integration: Parent-child component communication
    - API Integration: HTTP clients, error handling, caching
    - Router Testing: Navigation guards, route parameters
    - State Management: Cross-store communication, persistence
  
  e2e_tests:
    - User Workflows: Login, data entry, report generation
    - Cross-Application Navigation: Switching between tools
    - Data Persistence: Form data, user preferences, session state
    - Error Scenarios: Network failures, validation errors, recovery

Critical Frontend Testing Areas:
  - Security Dashboards: Real-time threat visualization (MISP, Rita)
  - Workflow Builders: Drag-and-drop editors (n8n, Dispatch)
  - Data Entry Forms: Recipe import (Mealie), transaction entry (Actual)
  - Analysis Interfaces: MTG analysis (Commander Spellbook, Toolkit)
```

**React Applications (Preserved Specialized Tools)**
```yaml
Actual Budget: Jest + React Testing Library
  - Financial calculations and CRDT operations
  - Complex budget interface components
  - File import/export workflows
  - Offline synchronization logic

Inspector MCP: Jest + Playwright
  - MCP protocol debugging interface
  - Real-time connection status monitoring
  - Transport configuration validation
  - Message inspection and formatting
```

### 7.2 Comprehensive Test Data Strategy

#### Test Data Management

**Unified Test Data Approach**
```yaml
Test Database Strategy:
  - Development: PostgreSQL test database with fixtures
  - CI/CD: SQLite in-memory for speed
  - Integration: Docker containers with realistic data volumes
  - E2E: Dedicated test environment with production-like data

Fixture Organization:
  Location: tests/fixtures/ in each service
  Format: JSON files for easy human review and Git tracking
  Categories:
    - users.json: Test users with various permission levels
    - projects.json: Sample projects across different domains
    - security_events.json: IOCs, alerts, and threat intelligence
    - workflows.json: n8n workflows, Dispatch procedures, Goose recipes
    - content.json: Recipes, budgets, MTG cards, analysis results

Factory Pattern Implementation:
  - Python: Factory Boy for complex object creation
  - Vue/TypeScript: Custom factory functions for frontend testing
  - Dynamic Generation: Property-based testing with Hypothesis (Python)
  - Relationship Handling: Automatic foreign key management
```

**Domain-Specific Test Data**

**Security Intelligence Testing**
```yaml
Threat Intelligence Test Data:
  - IOCs: IP addresses, domains, file hashes (safe test data only)
  - Network Events: Synthetic traffic patterns for analysis
  - YARA Rules: Test malware signatures for validation
  - MISP Events: Threat intelligence sharing scenarios
  - Alert Patterns: Known attack sequences for detection testing

Test Data Sources:
  - Synthetic Data: Generated safe IOCs and network patterns
  - Open Datasets: Public threat intelligence for validation
  - Sanitized Production: Anonymized real data where appropriate
  - Community Contributions: Test scenarios from security community
```

**Content & Productivity Testing**
```yaml
Application-Specific Test Data:
  Mealie:
    - Recipe Data: Various cuisines, dietary restrictions, formats
    - Import Formats: Different recipe website structures
    - Meal Planning: Weekly/monthly planning scenarios
    - User Preferences: Allergies, shopping lists, nutrition goals
  
  Actual Budget:
    - Transaction Data: Various categories, payees, account types
    - Import Formats: Bank CSVs, QIF files, OFX data
    - Budget Scenarios: Monthly, annual, irregular income
    - Account Types: Checking, savings, credit cards, investments
  
  MTG Tools:
    - Card Database: Representative sample from Scryfall API
    - Combo Data: Known interactions for validation
    - Cube Lists: Various cube archetypes and formats
    - Price Data: Historical pricing for analysis validation
```

### 7.3 Continuous Integration & Quality Gates

#### CI/CD Pipeline Integration

**Automated Testing Pipeline**
```yaml
Stage 1: Fast Feedback (< 5 minutes)
  - Code Quality: ESLint, Prettier, Black, isort
  - Type Checking: TypeScript compilation, mypy validation
  - Security Scanning: Bandit, ESLint security, dependency audit
  - Unit Tests: Fast unit test execution with parallel runners

Stage 2: Integration Testing (< 15 minutes)
  - Database Tests: PostgreSQL integration with migrations
  - API Tests: FastAPI endpoint testing with test database
  - Component Tests: Vue component integration testing
  - Mock Integration: Third-party API mocking validation

Stage 3: End-to-End Validation (< 30 minutes)
  - Browser Testing: Playwright cross-browser execution
  - User Workflows: Critical path testing for each application
  - Performance Testing: Basic performance regression detection
  - Accessibility Testing: WCAG 2.1 compliance validation

Stage 4: Security & Compliance (< 15 minutes)
  - SAST Scanning: Static application security testing
  - Dependency Scanning: Known vulnerability detection
  - Container Scanning: Docker image security validation
  - License Compliance: Open source license validation
```

**Quality Gates & Metrics**

**Coverage Requirements**
```yaml
Minimum Coverage Thresholds:
  - Critical Security Code: 95% (IOC processing, authentication)
  - Business Logic: 85% (workflows, calculations, data processing)
  - API Endpoints: 80% (all public APIs and internal services)
  - UI Components: 75% (user-facing components and interactions)
  - Utility Functions: 70% (helpers, formatters, validators)

Coverage Enforcement:
  - PR Blocking: PRs blocked if coverage drops below thresholds
  - Trend Monitoring: Coverage trends tracked over time
  - Exemption Process: Formal process for coverage exemptions
  - Regular Reviews: Monthly coverage reviews with team leads
```

**Performance Benchmarks**
```yaml
Performance Testing Requirements:
  API Response Times:
    - Search Operations: <500ms (MTG card search, recipe search)
    - Security Queries: <2s (IOC lookups, threat correlation)  
    - Workflow Execution: <10s (n8n simple workflows)
    - Data Import: <30s (recipe import, transaction import)
  
  Frontend Performance:
    - Page Load Time: <3s (initial page load)
    - Time to Interactive: <5s (full interactivity)
    - Bundle Size: <2MB (initial JavaScript bundle)
    - Memory Usage: <100MB (peak memory in browser)

Load Testing Scenarios:
  - Concurrent Users: 50+ simultaneous users
  - Data Volume: 10,000+ records per entity type
  - API Throughput: 1000+ requests/minute peak load
  - Background Processing: Multiple concurrent analysis jobs
```

### 7.4 Testing Environment Strategy

#### Environment Configuration

**Local Development Testing**
```yaml
Developer Workstation Setup:
  - Docker Compose: Full stack with test data
  - Fast Feedback: Unit tests run on file changes
  - Browser Testing: Headless for development, headed for debugging
  - Database: PostgreSQL container with fixture data pre-loaded

IDE Integration:
  - VS Code: Jest/Vitest extensions for inline test results
  - PyCharm: pytest integration with coverage visualization
  - Test Runners: Integrated test execution and debugging
  - Code Coverage: Real-time coverage highlighting in editor
```

**Staging Environment Testing**
```yaml
Pre-Production Validation:
  - Production Mirror: Identical to production infrastructure
  - Realistic Data: Production-like data volumes and patterns
  - External Integrations: Real API connections with test accounts
  - Performance Testing: Load testing with production-like traffic

Deployment Validation:
  - Smoke Tests: Critical path validation after deployment
  - Integration Tests: Cross-service communication validation
  - Security Tests: Authentication and authorization validation
  - Rollback Testing: Automated rollback procedures validation
```

#### Monitoring & Observability in Testing

**Test Result Analytics**
```yaml
Test Metrics Collection:
  - Test Execution Times: Track test performance over time
  - Flaky Test Detection: Identify unreliable tests automatically
  - Coverage Trends: Monitor coverage changes across releases
  - Failure Analysis: Categorize and track test failures

Quality Dashboards:
  - Real-time Status: Current test suite health across all projects
  - Historical Trends: Long-term quality metrics and improvements
  - Performance Tracking: Test execution time and resource usage
  - Team Metrics: Individual and team testing contributions

Alerting & Notifications:
  - Test Failures: Immediate notification for critical test failures
  - Coverage Drops: Alerts when coverage falls below thresholds
  - Performance Regression: Notification when tests become slow
  - Security Issues: Immediate alerts for security test failures
```

### 7.5 Domain-Specific Testing Strategies

#### Security Tool Testing

**Cybersecurity Application Testing**
```yaml
MISP & Threat Intelligence:
  - IOC Validation: Test indicator parsing and normalization
  - Feed Processing: Validate threat feed ingestion and correlation
  - API Security: Test authentication, authorization, rate limiting
  - Data Integrity: Validate threat intelligence accuracy and consistency

Network Security (Rita, Maltrail):
  - Traffic Analysis: Test with synthetic network traffic patterns
  - Anomaly Detection: Validate detection algorithms with known patterns
  - Performance Testing: Large-scale network log processing
  - False Positive Testing: Minimize false alerts in security detection

Forensics & Analysis (Nemesis, YARA-X):
  - File Analysis: Test with known malware samples (safely sandboxed)
  - Pattern Matching: Validate YARA rule execution and performance
  - Evidence Chain: Test forensic data integrity and chain of custody
  - Scale Testing: Large file processing and memory management
```

#### Workflow & Automation Testing

**Process Automation Testing**
```yaml
n8n Workflow Engine:
  - Workflow Execution: Test complex multi-step workflows
  - Error Handling: Validate retry logic and failure recovery
  - Integration Testing: Test 400+ third-party service integrations
  - Performance Testing: Concurrent workflow execution under load

Dispatch Incident Management:
  - Incident Lifecycle: Test complete incident response workflows
  - Communication: Validate Slack, email, and notification integrations
  - Documentation: Test automated document generation and updates
  - Escalation: Validate complex escalation and approval workflows

Goose AI Agent:
  - Conversation Flow: Test multi-turn AI conversations
  - Tool Integration: Validate external tool calling and result processing
  - Context Management: Test conversation context and memory handling
  - Safety Testing: Validate AI safety measures and content filtering
```

---

## Section 8: Security Architecture & Performance Strategy [CRITICAL]

### 8.1 Unified Security Architecture

The consolidated platform requires enterprise-grade security that protects sensitive cybersecurity data while maintaining usability across diverse application domains.

#### Authentication & Identity Management

**Multi-Provider Identity Service**
```yaml
Primary Authentication: OAuth 2.0 + OpenID Connect
Framework: FastAPI OAuth2 with multiple provider support
Database: PostgreSQL users table with provider federation
Session Management: JWT with Redis-backed sessions

Supported Authentication Methods:
  primary_oauth:
    - Discord OAuth: Community-focused tools (Commander Spellbook, Ghostwriter)
    - Google Workspace: Enterprise deployments and productivity tools
    - GitHub OAuth: Developer-focused integrations (n8n, IT-Tools)
    - Microsoft Azure AD: Enterprise SSO integration
    
  enterprise_auth:
    - LDAP/Active Directory: Enterprise user directory integration
    - SAML 2.0: Enterprise identity federation
    - X.509 Certificates: High-security environments (MISP, Nemesis)
    - Multi-Factor Authentication: TOTP, SMS, Hardware tokens (FIDO2/WebAuthn)

  api_access:
    - API Keys: Service-to-service authentication, CLI tools
    - JWT Tokens: Frontend application authentication  
    - Basic Auth: Legacy tool compatibility (configurable)
    - Webhook Tokens: Secure webhook validation and processing

Security Configuration:
  token_management:
    - Access Token Lifetime: 15 minutes (short-lived for security)
    - Refresh Token Lifetime: 30 days (secure rotation)
    - API Key Format: Prefixed keys with entropy validation (api_XXXXXXXX)
    - Token Encryption: AES-256-GCM for token storage and transmission
  
  session_security:
    - Cookie Security: HTTPOnly, Secure, SameSite=Strict
    - Session Storage: Redis with encryption at rest
    - Session Timeout: 8 hours idle, 24 hours absolute
    - Concurrent Sessions: Limited to 5 active sessions per user
```

#### Role-Based Access Control (RBAC)

**Hierarchical Permission System**
```yaml
Role Architecture: Project-based RBAC with global administrative roles
Permission Granularity: Resource-level permissions with action controls
Inheritance Model: Role hierarchies with permission delegation

Global Roles:
  - System Administrator:
    permissions: [system:admin, user:manage, project:create, audit:view]
    access_scope: All projects and system configuration
    special_privileges: User management, system monitoring, security configuration
  
  - Security Analyst:
    permissions: [security:read, security:analyze, incident:manage, ioc:manage]
    access_scope: All security-related projects (MISP, Nemesis, Rita, Maltrail)
    special_privileges: Cross-project threat correlation, global IOC management
  
  - Project Manager:
    permissions: [project:admin, user:invite, workflow:manage, report:generate]
    access_scope: Assigned projects only
    special_privileges: Project configuration, user role assignment within projects

Project-Specific Roles:
  - Project Admin: Full project control, user management, data export
  - Editor: Content creation, workflow modification, data analysis
  - Analyst: Read-only analysis, query execution, report generation  
  - Viewer: Read-only access to project data and reports
  - Guest: Limited access to public/shared resources only

Permission Matrix (Resource × Action):
  security_data:
    - read: [security_analyst, project_admin, editor, analyst, viewer]
    - write: [security_analyst, project_admin, editor]
    - delete: [security_analyst, project_admin]
    - export: [security_analyst, project_admin] # Sensitive data protection
  
  workflows:
    - read: [project_admin, editor, analyst, viewer]
    - create: [project_admin, editor]
    - execute: [project_admin, editor, analyst]
    - delete: [project_admin]
  
  user_data:
    - read: [project_admin, editor] # PII protection
    - write: [project_admin]
    - delete: [system_administrator] # Global privilege required
```

#### Data Security & Encryption

**Comprehensive Data Protection**
```yaml
Encryption at Rest:
  database_encryption:
    - Implementation: PostgreSQL Transparent Data Encryption (TDE)
    - Algorithm: AES-256-CBC with key rotation
    - Key Management: HashiCorp Vault or cloud KMS integration
    - Scope: All database files, WAL files, and backups
  
  application_encryption:
    - Sensitive Fields: API keys, passwords, PII data, IOCs
    - Implementation: Field-level encryption using Fernet (symmetric)
    - Key Rotation: Monthly automated rotation with zero-downtime
    - Storage: Encrypted keys in dedicated key management service

Encryption in Transit:
  tls_configuration:
    - Minimum Version: TLS 1.3
    - Cipher Suites: ECDHE-RSA-AES256-GCM-SHA384, ChaCha20-Poly1305
    - Certificate Management: Let's Encrypt with automated renewal
    - HSTS: Enabled with includeSubDomains and preload
  
  internal_communication:
    - Service Mesh: Mutual TLS (mTLS) for service-to-service communication
    - Certificate Authority: Internal CA with automatic certificate rotation
    - Protocol: HTTP/2 with gRPC for high-performance internal APIs
    - Validation: Certificate pinning and identity verification

Data Classification & Handling:
  security_intelligence:
    - Classification: Confidential (IOCs, threat data, incident details)
    - Handling: Encrypted storage, access logging, export controls
    - Retention: 7 years for compliance, automated purging
    - Sharing: Controlled sharing with encryption and watermarking
  
  user_data:
    - Classification: Personal (emails, names, preferences)
    - Handling: GDPR-compliant processing, right to deletion
    - Retention: Active account + 30 days after deletion
    - Anonymization: PII anonymization for analytics and testing
  
  application_data:
    - Classification: Internal (workflows, configurations, logs)
    - Handling: Standard encryption, backup protection
    - Retention: Business requirements (varies by data type)
    - Access: Role-based access with audit trails
```

#### Security Monitoring & Incident Response

**Comprehensive Security Operations**
```yaml
Security Information and Event Management (SIEM):
  log_aggregation:
    - Sources: Application logs, authentication events, system metrics
    - Format: Structured JSON with correlation IDs
    - Storage: Elasticsearch cluster with hot/warm/cold tiers
    - Retention: 90 days hot, 1 year warm, 7 years cold storage
  
  threat_detection:
    - Failed Authentication: Brute force detection and account lockout
    - Anomaly Detection: Unusual access patterns, privilege escalation
    - Data Exfiltration: Large data exports, unusual API usage patterns
    - Malicious Activity: Known IOC matches, suspicious file uploads

Real-Time Security Monitoring:
  metrics_collection:
    - Authentication Events: Login attempts, failures, suspicious patterns
    - API Security: Rate limiting violations, invalid requests, token misuse
    - Data Access: Sensitive data queries, export activities, permission changes
    - System Health: Resource usage, performance degradation, error rates
  
  alerting_system:
    - Critical Alerts: Security incidents, authentication bypasses, data breaches
    - Warning Alerts: Unusual patterns, performance issues, configuration changes
    - Information: Successful actions, system events, maintenance activities
    - Escalation: Automated escalation to security team, management notification

Incident Response Procedures:
  automated_response:
    - Account Lockout: Automatic lockout after failed authentication attempts
    - Rate Limiting: Dynamic rate limiting based on threat intelligence
    - Access Revocation: Automatic token revocation on suspicious activity
    - Quarantine: Automatic quarantine of suspicious files or activities
  
  manual_response:
    - Incident Classification: Critical, High, Medium, Low severity levels
    - Response Team: Security team, system administrators, project owners
    - Communication: Incident notifications, status updates, post-incident reviews
    - Documentation: Incident timeline, actions taken, lessons learned
```

### 8.2 Performance Optimization Strategy

#### Database Performance Architecture

**PostgreSQL Optimization for Multi-Tenant Workloads**
```yaml
Connection Management:
  connection_pooling:
    - Implementation: PgBouncer with transaction-level pooling
    - Pool Size: 100 connections per application server
    - Max Connections: 500 total database connections
    - Timeout Configuration: 30s connection timeout, 5s query timeout
  
  connection_optimization:
    - Prepared Statements: All frequent queries pre-compiled
    - Statement Caching: 1000 statement cache per connection
    - Connection Multiplexing: Shared connections for read-only queries
    - Health Monitoring: Connection health checks and automatic failover

Query Performance:
  indexing_strategy:
    - Primary Indexes: All foreign keys, frequently queried columns
    - Composite Indexes: Multi-column indexes for complex queries
    - Partial Indexes: Filtered indexes for specific conditions (active records)
    - Gin Indexes: Full-text search, JSONB queries, array operations
  
  query_optimization:
    - Query Analysis: Regular EXPLAIN ANALYZE for slow queries
    - Index Monitoring: pg_stat_user_indexes for index usage tracking
    - Partition Tables: Time-based partitioning for large datasets (logs, events)
    - Materialized Views: Pre-computed aggregations for reporting queries

Database Scaling:
  read_replicas:
    - Configuration: 2 read replicas for analytical workloads
    - Replication: Streaming replication with async commit
    - Load Balancing: Application-level read/write splitting
    - Failover: Automatic promotion of read replica on master failure
  
  sharding_strategy:
    - Horizontal Partitioning: By project_id for multi-tenant isolation
    - Vertical Partitioning: Separate databases for different data types
    - Federation: Cross-shard queries through application layer
    - Migration: Online shard migration with zero downtime
```

#### Caching Strategy & Redis Optimization

**Multi-Layer Caching Architecture**
```yaml
Redis Cluster Configuration:
  cluster_topology:
    - Master Nodes: 3 masters for high availability
    - Replica Nodes: 6 replicas (2 per master) for read scaling
    - Memory Allocation: 16GB per node, 144GB total cluster memory
    - Persistence: RDB snapshots + AOF for durability
  
  cache_hierarchies:
    - L1 Cache: Application memory cache (30s TTL, frequently accessed data)
    - L2 Cache: Redis cache (5-60min TTL, session and query data)
    - L3 Cache: CDN cache (1-24hr TTL, static content and API responses)
    - Persistent Cache: Database result cache with invalidation triggers

Cache Patterns by Application:
  security_intelligence:
    - IOC Lookups: 60-minute TTL, write-through pattern
    - Threat Feeds: 24-hour TTL, refresh-ahead pattern
    - Search Results: 15-minute TTL, cache-aside pattern
    - Real-time Alerts: Event-driven invalidation, no TTL
  
  workflow_automation:
    - Workflow Definitions: 1-hour TTL, write-behind pattern
    - Execution State: No cache (real-time consistency required)
    - Node Templates: 24-hour TTL, immutable caching
    - User Sessions: 8-hour TTL, sliding expiration
  
  content_productivity:
    - Recipe Data: 4-hour TTL, lazy loading pattern
    - Financial Data: No cache (consistency critical)
    - MTG Card Data: 24-hour TTL, bulk refresh pattern
    - User Preferences: Session-based, manual invalidation

Cache Performance Optimization:
  memory_management:
    - Eviction Policy: allkeys-lru for general cache, volatile-ttl for sessions
    - Memory Monitoring: Alert at 80% usage, auto-scaling at 85%
    - Key Compression: JSON compression for large cached objects
    - Pipeline Operations: Batch Redis operations for better throughput
```

#### API Performance & Rate Limiting

**High-Performance API Gateway**
```yaml
API Gateway Configuration:
  request_routing:
    - Load Balancer: nginx with least_conn algorithm
    - Service Discovery: Consul-based service registry
    - Health Checks: Active health monitoring with circuit breakers
    - Failover: Automatic failover to healthy service instances
  
  performance_optimization:
    - HTTP/2: Full HTTP/2 support with server push
    - Compression: Gzip/Brotli compression for responses >1KB
    - Keep-Alive: Persistent connections with 60s timeout
    - Request Buffering: Streaming for large uploads, buffering for small requests

Rate Limiting Strategy:
  multi_tier_limits:
    - Global Limits: 10,000 requests/hour per IP address
    - User Limits: 1,000 requests/hour per authenticated user
    - API Key Limits: Tier-based limits (100-10,000 requests/hour)
    - Endpoint Limits: Specific limits for resource-intensive operations
  
  rate_limiting_implementation:
    - Algorithm: Token bucket with burst allowance
    - Storage: Redis-based counters with sliding windows
    - Response: HTTP 429 with Retry-After header
    - Bypass: Whitelist for internal services and administrative access

API Response Optimization:
  response_caching:
    - Static Data: 24-hour cache for reference data (MTG cards, countries)
    - Dynamic Data: 5-minute cache for frequently requested data
    - User-Specific: No cache for personalized data
    - Real-time Data: No cache for security alerts and live updates
  
  payload_optimization:
    - Field Selection: GraphQL-style field selection for REST APIs
    - Pagination: Cursor-based pagination with configurable page sizes
    - Compression: Automatic JSON minification and compression
    - Batch Operations: Bulk API endpoints for multiple operations
```

#### Frontend Performance Optimization

**Modern Web Performance Standards**
```yaml
Bundle Optimization:
  code_splitting:
    - Route-Level: Each major application route as separate chunk
    - Component-Level: Heavy components (charts, editors) lazy-loaded
    - Vendor Splitting: Third-party libraries in separate chunks
    - Dynamic Imports: On-demand loading based on user actions
  
  build_optimization:
    - Tree Shaking: Remove unused code from final bundles
    - Minification: JavaScript, CSS, and HTML minification
    - Asset Optimization: Image compression, font subsetting
    - Service Worker: Aggressive caching with cache-first strategy

Performance Targets:
  core_web_vitals:
    - Largest Contentful Paint (LCP): <2.5s
    - First Input Delay (FID): <100ms
    - Cumulative Layout Shift (CLS): <0.1
    - Time to Interactive (TTI): <3.5s
  
  custom_metrics:
    - Bundle Size: <500KB initial JavaScript
    - Memory Usage: <50MB peak memory usage
    - Network Requests: <20 requests for initial page load
    - Cache Hit Rate: >90% for repeat visitors

Runtime Performance:
  client_side_optimization:
    - Virtual Scrolling: For large data tables (>1000 rows)
    - Image Lazy Loading: Below-the-fold image loading
    - Component Memoization: React.memo, Vue computed properties
    - Event Throttling: Debounced search, throttled scroll events
  
  progressive_enhancement:
    - Progressive Web App: Service worker, app manifest, offline capability
    - Critical CSS: Inline critical path CSS, async load non-critical
    - Resource Hints: Preload, prefetch, preconnect for performance
    - Adaptive Loading: Adjust features based on device capabilities
```

### 8.3 Infrastructure Security & Compliance

#### Container Security & DevSecOps

**Secure Container Architecture**
```yaml
Container Security Standards:
  base_images:
    - Source: Official base images from Docker Hub or Red Hat UBI
    - Scanning: Automated vulnerability scanning with Trivy/Clair
    - Minimal Images: Distroless images where possible, Alpine for others
    - Updates: Weekly base image updates and security patches
  
  runtime_security:
    - Non-Root Users: All containers run as non-root users (UID >1000)
    - Read-Only Filesystems: Read-only root filesystem with tmpfs for writable areas
    - Capability Dropping: Drop unnecessary Linux capabilities
    - Seccomp Profiles: Restrict system calls to necessary subset
  
  secrets_management:
    - No Secrets in Images: No hardcoded secrets in container images
    - Vault Integration: HashiCorp Vault for secret injection at runtime
    - Encrypted Storage: Secrets encrypted at rest and in transit
    - Rotation: Automated secret rotation with zero-downtime deployment

Kubernetes Security:
  cluster_hardening:
    - RBAC: Strict role-based access control for all resources
    - Network Policies: Segmented network access between namespaces
    - Pod Security Standards: Enforce restricted pod security standards
    - Admission Controllers: OPA Gatekeeper for policy enforcement
  
  workload_isolation:
    - Namespaces: Project-based namespace isolation
    - Resource Limits: CPU, memory, and storage quotas per namespace
    - Service Mesh: Istio for encrypted service-to-service communication
    - Monitoring: Continuous security monitoring with Falco
```

#### Compliance & Audit Framework

**Regulatory Compliance Strategy**
```yaml
Security Frameworks:
  compliance_standards:
    - ISO 27001: Information security management system
    - NIST Cybersecurity Framework: Risk management and incident response
    - SOC 2 Type II: Security, availability, and confidentiality controls
    - GDPR: Data protection and privacy for EU users
  
  implementation_controls:
    - Access Control: Multi-factor authentication, role-based permissions
    - Data Protection: Encryption, backup, and recovery procedures
    - Incident Response: 24/7 monitoring, automated response, communication plans
    - Audit Trails: Comprehensive logging, tamper-evident audit logs

Audit & Compliance Monitoring:
  continuous_compliance:
    - Policy Engine: Open Policy Agent for automated compliance checking
    - Configuration Drift: Continuous monitoring and automated remediation
    - Vulnerability Management: Regular scanning and patching procedures
    - Access Reviews: Quarterly access reviews and permission audits
  
  documentation:
    - Security Policies: Written security policies and procedures
    - Risk Assessments: Regular risk assessments and mitigation plans
    - Incident Reports: Documented incident response and lessons learned
    - Compliance Reports: Regular compliance status reports and certifications

Data Governance:
  data_lifecycle:
    - Classification: Automatic data classification based on content and context
    - Retention: Automated retention policies with legal hold capabilities
    - Disposal: Secure data destruction with certificate of destruction
    - Privacy: Data minimization, pseudonymization, and anonymization
  
  cross_border_transfers:
    - Data Residency: Geographic data residency controls
    - Transfer Agreements: Standard contractual clauses for data transfers
    - Encryption Requirements: Encryption for data crossing jurisdictions
    - Compliance Monitoring: Regular audits of data transfer compliance
```

---

## Section 6: Final Integration Plan Summary

### 6.1 Executive Summary

This analysis of 23 cybersecurity and development tools reveals significant opportunities for consolidation into a unified modular monolith platform. By leveraging shared technology stacks and common infrastructure patterns, we can reduce deployment complexity from 23 separate containers to 6 consolidated containers while preserving all critical business logic.

#### Key Findings:
- **Technology Alignment**: 13 projects (57%) use Node.js/TypeScript stack, 10 projects (43%) use Python
- **Database Consolidation**: PostgreSQL can support 18 projects, SQLite for 5 local-first applications  
- **Framework Standardization**: FastAPI + Vue.js can serve as primary platform for 15+ projects
- **Resource Optimization**: 70% reduction in total resource requirements (29GB vs 100GB+ RAM)

#### Strategic Approach:
1. **Preserve Critical Logic**: Complex algorithms (n8n workflows, MISP correlation, CyberChef operations) maintained as dedicated microservices with API integration
2. **Consolidate Common Functions**: Authentication, notifications, file storage, and database access shared across all modules
3. **Gradual Migration**: 4-phase approach over 24 weeks with rollback capabilities and risk mitigation
4. **Unified Experience**: Single sign-on, consistent UI components, integrated workflows across all tools

### 6.2 Expected Benefits

#### Technical Benefits:
- **Reduced Operational Complexity**: Single deployment pipeline, shared infrastructure monitoring
- **Improved Security**: Consolidated authentication, unified audit logging, reduced attack surface per service
- **Enhanced Performance**: Shared caching, optimized database queries, reduced network latency between services
- **Better Integration**: Native data sharing, unified search, cross-tool workflows

#### Business Benefits:  
- **Lower Infrastructure Costs**: 70% reduction in server resources, simplified licensing
- **Faster Development**: Shared components, common APIs, unified development environment
- **Improved User Experience**: Single interface, consistent navigation, integrated workflows
- **Enhanced Maintainability**: Consolidated documentation, unified deployment procedures, shared security updates

### 6.3 Recommended Next Steps

#### Immediate Actions (Week 1):
1. **Infrastructure Setup**: Deploy PostgreSQL + Redis cluster with backup/recovery procedures
2. **Base Platform**: Create FastAPI application template with shared modules (auth, database, API)
3. **Development Environment**: Set up Docker Compose with all 6 containers and development tooling
4. **CI/CD Pipeline**: Implement GitHub Actions workflow with testing, security scanning, deployment

#### Phase 1 Priorities (Weeks 2-4):  
1. **Low-Risk Migrations**: IT-Tools, FileScopeMCP, Inspector, MTG Scripting Toolkit
2. **Authentication System**: Implement OAuth2/OIDC with Discord, Google, GitHub providers  
3. **Frontend Framework**: Create Vue.js application shell with shared components
4. **Monitoring Setup**: Deploy Prometheus + Grafana with basic application metrics

#### Long-term Success Factors:
1. **Team Training**: Ensure development team proficiency in chosen tech stack (FastAPI + Vue.js)
2. **Documentation**: Maintain comprehensive API documentation, deployment guides, troubleshooting procedures
3. **Performance Monitoring**: Establish baseline metrics and continuous performance monitoring
4. **Security Compliance**: Regular security audits, penetration testing, compliance verification (GDPR, SOX, etc.)

This integration strategy transforms a complex ecosystem of 23 separate tools into a cohesive, scalable platform that maintains all critical functionality while dramatically reducing operational overhead and improving user experience.