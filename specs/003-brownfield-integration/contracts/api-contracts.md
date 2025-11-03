# API Contracts: Brownfield Integration - Mental Prosthetic Platform

**Branch**: `003-brownfield-integration` | **Date**: 2025-11-03 | **Phase**: 1 - Design
**Context**: Unified API contracts for 37-tool consolidation with domain-based architecture

## Contract Overview

This document defines the API contracts for the unified modular monolith platform, consolidating 37 executive function tools into domain-based services with consistent interfaces, authentication, and performance guarantees.

## 1. Core API Architecture

### 1.1 Domain-Based Service Structure

```yaml
API Architecture:
  Base URL: https://api.jane-platform.org/v1
  
  Domain Services:
    /security/*     - Security tools (MISP, YARA-X, SecurityOnion, etc.)
    /productivity/* - Productivity tools (n8n, Mealie, Dispatch, etc.)
    /tcg/*         - TCG tools (Commander Spellbook, card analysis, etc.)
    /infrastructure/* - Infrastructure tools (Kong, IT-Tools, etc.)
    
  Core Services:
    /auth/*        - Authentication and authorization
    /users/*       - User management and preferences
    /organizations/* - Multi-tenant organization management
    /events/*      - Domain event sourcing and audit
    /sync/*        - Cross-domain data synchronization
```

### 1.2 API Standards and Conventions

```yaml
API Standards:
  Protocol: HTTP/1.1, HTTP/2 (WebSocket for real-time)
  Authentication: JWT with refresh tokens, OAuth 2.0/OIDC support
  Content-Type: application/json (primary), multipart/form-data (file uploads)
  Error Format: RFC 7807 (Problem Details for HTTP APIs)
  Versioning: URL path versioning (/v1/, /v2/)
  Rate Limiting: Domain-specific limits with 429 responses
  
  Response Format:
    Success: HTTP 2xx with JSON payload
    Error: HTTP 4xx/5xx with Problem Details JSON
    Pagination: RFC 5988 Link headers + JSON metadata
    
  DDD Integration Patterns:
    Command Processing: Decorator-based cross-cutting concerns
    Async Communication: Domain event streaming via WebSocket
    Architecture Compliance: Runtime boundary validation
    Performance Monitoring: Domain-specific SLA enforcement
```

## 1.5 DDD Integration Architecture

### 1.5.1 Command/Query Processing Pipeline

```yaml
Request Processing Pipeline:
  1. API Gateway: Route to appropriate domain service
  2. Authentication: JWT validation and user context injection
  3. Authorization: Permission-based access control
  4. Domain Routing: Async-only inter-domain communication
  5. Decorator Chain: Logging → Validation → Performance → UoW
  6. Business Logic: Pure domain service execution
  7. Event Publishing: Domain events via Outbox pattern
  8. Response Formation: Consistent API response format
  
Performance SLA Enforcement:
  Security Domain: 1000ms timeout with circuit breaker
  Productivity Domain: 2000ms timeout with retry logic
  TCG Domain: 3000ms timeout with caching optimization
  Infrastructure Domain: 5000ms timeout with background processing
```

### 1.5.2 Domain Event Streaming

```yaml
Real-time Event Streaming:
  Protocol: WebSocket with JSON message format
  Authentication: JWT token validation on connection
  Subscription Model: Domain-based event filtering
  
Event Types:
  security.threat-detected: Real-time threat intelligence updates
  security.yara-match: YARA rule pattern matches
  productivity.task-updated: Task management changes
  productivity.workflow-triggered: n8n workflow executions
  tcg.deck-analyzed: TCG deck optimization results
  infrastructure.service-alert: System monitoring alerts
  
Connection Endpoints:
  - `/ws/{domain}` - Domain-specific WebSocket endpoints where domain is security, productivity, tcg, or infrastructure
  /ws/events/all: Cross-domain event aggregation (admin only)
```

### 1.5.3 Architecture Compliance API

```yaml
GET /internal/architecture/compliance
Summary: Real-time architecture boundary validation
Authentication: Internal service token required
Headers:
  X-Service-Token: {internal_service_token}
  
Response (200):
  domain_boundaries: DomainBoundaryStatus[]
  dependency_violations: ArchitectureViolation[]
  performance_metrics: DomainPerformanceMetrics[]
  
DomainBoundaryStatus:
  domain: string
  isolation_score: number (0-100)
  async_compliance: boolean
  direct_dependency_violations: number
  
ArchitectureViolation:
  type: string (direct_import|database_cross_access|sync_communication)
  source_domain: string
  target_domain: string
  severity: string (warning|error|critical)
  violation_details: string
  file_path: string
  line_number: integer
```

### 1.5.4 Internal Command Processing

```yaml
POST /internal/commands/execute
Summary: Execute internal commands for migration workflows
Authentication: Internal service token required
Content-Type: application/json

Request Body:
  command_type: string (migrate_misp_data|process_yara_rule|sync_productivity_data)
  command_data: object (command-specific payload)
  priority: string (low|normal|high|critical)
  retry_policy: object
    max_retries: integer (default: 3)
    backoff_strategy: string (linear|exponential)
    timeout_seconds: integer
    
Response (202):
  command_id: uuid
  status: string (queued)
  estimated_completion: datetime
  
Response (400):
  Problem Details for invalid command data
```

## 2. Authentication & Authorization Contracts

### 2.1 Authentication API

```yaml
POST /auth/login
Summary: User authentication with email/password or SSO
Request:
  Content-Type: application/json
  Body:
    email: string (required)
    password: string (required if not SSO)
    sso_provider: string (optional: google, github, microsoft)
    organization_slug: string (optional)
    
Response (200):
  Content-Type: application/json
  Body:
    access_token: string (JWT, 15 min expiry)
    refresh_token: string (7 day expiry)
    expires_in: number (seconds)
    user: UserProfile
    organization: Organization (if selected)
    
Response (401):
  Problem Details:
    type: /errors/authentication-failed
    title: Authentication Failed
    detail: Invalid email or password
    status: 401
```

```yaml
POST /auth/refresh
Summary: Refresh access token using refresh token
Request:
  Content-Type: application/json
  Body:
    refresh_token: string (required)
    
Response (200):
  access_token: string (new JWT)
  expires_in: number
  
Response (401):
  Problem Details:
    type: /errors/token-expired
    title: Refresh Token Expired
    status: 401
```

### 2.2 User Management API

```yaml
GET /users/me
Summary: Get current user profile with preferences
Headers:
  Authorization: Bearer {jwt_token}
  
Response (200):
  id: uuid
  email: string
  username: string
  display_name: string
  ui_preferences: object
    theme: string (light|dark|system)
    font_size: string (small|medium|large)
    reduced_motion: boolean
    high_contrast: boolean
  accessibility_settings: object
    break_reminder_interval: number (seconds)
    focus_session_duration: number (seconds)
    auto_save_frequency: number (seconds)
  organizations: Organization[]
  last_login_at: datetime
  created_at: datetime
```

```yaml
PATCH /users/me
Summary: Update user profile and preferences
Headers:
  Authorization: Bearer {jwt_token}
  Content-Type: application/json
  
Request Body:
  display_name: string (optional)
  ui_preferences: object (optional)
  accessibility_settings: object (optional)
  
Response (200):
  Updated UserProfile
  
Response (400):
  Problem Details for validation errors
```

## 3. Security Domain API Contracts

### 3.1 Threat Intelligence API

```yaml
GET /security/threats/indicators
Summary: Search and retrieve threat indicators
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  type: string (hash|domain|ip|url|yara_rule)
  value: string (partial match support)
  confidence_min: integer (0-100)
  source_tool: string (misp|malware_bazaar|virustotal)
  tags: string[] (comma-separated)
  limit: integer (default: 50, max: 1000)
  offset: integer (default: 0)
  
Response (200):
  Content-Type: application/json
  Headers:
    X-Total-Count: integer
    Link: string (pagination links)
  Body:
    indicators: ThreatIndicator[]
    
ThreatIndicator:
  id: uuid
  type: string
  value: string
  confidence_score: integer (0-100)
  source_tool: string
  source_id: string
  threat_types: string[]
  tags: string[]
  tlp_level: string (white|green|amber|red)
  first_seen: datetime
  last_seen: datetime
  expires_at: datetime (nullable)
  created_at: datetime
```

```yaml
POST /security/threats/indicators
Summary: Create new threat indicator
Headers:
  Authorization: Bearer {jwt_token}
  Content-Type: application/json
  
Request Body:
  type: string (required)
  value: string (required)
  confidence_score: integer (required, 0-100)
  source_tool: string (required)
  threat_types: string[] (optional)
  tags: string[] (optional)
  tlp_level: string (default: white)
  first_seen: datetime (optional, defaults to now)
  
Response (201):
  Location: /security/threats/indicators/{id}
  Created ThreatIndicator
  
Response (400):
  Problem Details for validation errors
  
Response (409):
  Problem Details for duplicate indicators
```

### 3.2 YARA Rules API

```yaml
GET /security/yara/rules
Summary: Retrieve YARA rules with filtering
Performance Requirement: <1s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  name: string (partial match)
  author: string
  categories: string[] (comma-separated)
  severity: string (low|medium|high|critical)
  is_active: boolean
  is_validated: boolean
  limit: integer (default: 50)
  offset: integer (default: 0)
  
Response (200):
  rules: YaraRule[]
  
YaraRule:
  id: uuid
  name: string
  rule_text: string
  description: string
  author: string
  version: string
  categories: string[]
  severity: string
  is_active: boolean
  is_validated: boolean
  match_count: integer
  false_positive_count: integer
  last_match_at: datetime (nullable)
  created_at: datetime
```

```yaml
POST /security/yara/rules/validate
Summary: Validate YARA rule syntax and compilation
Headers:
  Authorization: Bearer {jwt_token}
  Content-Type: application/json
  
Request Body:
  rule_text: string (required)
  
Response (200):
  valid: boolean
  compilation_time_ms: number
  warnings: string[] (compilation warnings)
  
Response (400):
  valid: false
  errors: string[] (syntax errors)
  line_numbers: integer[] (error locations)
```

### 3.3 Network Events API

```yaml
GET /security/events/network
Summary: Query network security events
Performance Requirement: <1s response time with streaming support
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  start_time: datetime (required)
  end_time: datetime (required)
  source_ip: string (CIDR support: 192.168.1.0/24)
  destination_ip: string
  event_type: string (alert|connection|dns|http)
  severity: string (info|low|medium|high|critical)
  source_tool: string
  limit: integer (default: 100, max: 10000)
  stream: boolean (default: false, enables WebSocket)
  
Response (200):
  events: NetworkEvent[]
  
NetworkEvent:
  id: uuid
  event_timestamp: datetime
  source_ip: string
  destination_ip: string
  source_port: integer
  destination_port: integer
  protocol: string
  event_type: string
  severity: string
  signature: string
  is_malicious: boolean (nullable)
  risk_score: integer (0-100, nullable)
  source_tool: string
  created_at: datetime
```

```yaml
WebSocket /security/events/network/stream
Summary: Real-time network event streaming
Headers:
  Authorization: Bearer {jwt_token}
  
Connection Parameters:
  filters: JSON (same as GET query parameters)
  
Messages:
  event: NetworkEvent (real-time events)
  heartbeat: object (every 30s)
  error: Problem Details
  
Client Messages:
  subscribe: object (update filters)
  unsubscribe: object (stop streaming)
```

### 3.5 DDD Integration - Security Domain

#### Domain Event Publishing

```yaml
POST /security/events/publish
Summary: Publish domain events for cross-domain integration
Headers:
  Authorization: Bearer {jwt_token}
  X-Source-Domain: security
  Content-Type: application/json
  
Request Body:
  event_type: string (threat_detected|yara_match|network_anomaly|malware_classified)
  aggregate_id: uuid
  event_data: object
  target_domains: string[] (productivity|tcg|infrastructure)
  
Response (202):
  event_id: uuid
  published_to_outbox: boolean
  target_domains: string[]
  
Event Types:
  threat_detected:
    indicator_id: uuid
    threat_type: string
    confidence_score: integer
    affected_assets: string[]
    
  yara_match:
    rule_id: uuid
    file_hash: string
    match_details: object
    severity: string
```

#### Architecture Compliance Validation

```yaml
GET /security/architecture/validate
Summary: Validate security domain architectural boundaries
Headers:
  X-Internal-Service: true
  
Response (200):
  domain_isolation: object
    direct_dependencies: string[] (should be empty)
    async_communications: number
    database_schema_access: string[] (security schemas only)
    
  performance_compliance: object
    avg_response_time_ms: number (should be < 1000)
    sla_violations_24h: number
    circuit_breaker_status: string
    
  business_logic_preservation: object
    misp_algorithms_intact: boolean
    yara_performance_maintained: boolean
    original_confidence_calculations: boolean
```

#### Internal Command Processing

```yaml
POST /security/commands/internal/execute
Summary: Execute security domain internal commands
Headers:
  X-Internal-Service: true
  Content-Type: application/json
  
Request Body:
  command_type: string (migrate_misp_data|compile_yara_rules|process_malware_sample)
  command_data: object
  
migrate_misp_data Command:
  misp_instance_id: uuid
  preserve_relationships: boolean
  target_schema: string
  
compile_yara_rules Command:
  rule_sources: string[]
  optimization_level: string (performance|memory)
  validation_required: boolean
  
Response (202):
  command_id: uuid
  estimated_completion_seconds: number
  status: string (queued|processing|completed|failed)
```

## 4. Productivity Domain API Contracts

### 4.1 Project Management API

```yaml
GET /productivity/projects
Summary: List projects with filtering and sorting
Performance Requirement: <2s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  organization_id: uuid (defaults to user's primary org)
  status: string (active|completed|archived|on_hold)
  team_id: uuid
  search: string (name and description search)
  sort: string (name|created_at|updated_at|start_date)
  order: string (asc|desc, default: desc)
  limit: integer (default: 25)
  offset: integer (default: 0)
  
Response (200):
  projects: Project[]
  
Project:
  id: uuid
  name: string
  description: string
  status: string
  organization_id: uuid
  start_date: date (nullable)
  end_date: date (nullable)
  estimated_hours: integer (nullable)
  actual_hours: integer
  workflow_configs: object (n8n integration data)
  task_count: integer
  completed_task_count: integer
  created_at: datetime
  updated_at: datetime
  created_by: UserProfile (minimal)
```

```yaml
POST /productivity/projects
Summary: Create new project
Headers:
  Authorization: Bearer {jwt_token}
  Content-Type: application/json
  
Request Body:
  name: string (required, max: 255)
  description: string (optional)
  organization_id: uuid (optional, defaults to primary)
  start_date: date (optional)
  end_date: date (optional)
  estimated_hours: integer (optional)
  workflow_configs: object (optional)
  
Response (201):
  Location: /productivity/projects/{id}
  Created Project
  
Response (400):
  Problem Details for validation errors
```

### 4.2 Task Management API (Executive Function Support)

```yaml
GET /productivity/tasks
Summary: List tasks with executive function optimizations
Performance Requirement: <200ms for UI responsiveness
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  project_id: uuid
  assigned_to: uuid (defaults to current user)
  status: string (todo|in_progress|blocked|completed)
  priority: string (low|medium|high|urgent)
  due_before: datetime
  focus_mode: boolean (tasks suitable for current focus session)
  limit: integer (default: 50)
  offset: integer (default: 0)
  
Response (200):
  tasks: Task[]
  focus_recommendations: Task[] (AI-suggested focus tasks)
  
Task:
  id: uuid
  title: string
  description: string
  status: string
  priority: string
  project_id: uuid
  assigned_to: uuid
  estimated_duration: string (ISO 8601 duration)
  actual_duration: string (nullable)
  break_reminders: boolean
  focus_mode_enabled: boolean
  due_date: datetime (nullable)
  started_at: datetime (nullable)
  completed_at: datetime (nullable)
  created_at: datetime
  updated_at: datetime
```

```yaml
PATCH /productivity/tasks/{id}/focus
Summary: Start/stop focus session for task (executive function support)
Headers:
  Authorization: Bearer {jwt_token}
  Content-Type: application/json
  
Request Body:
  action: string (start|pause|complete|break)
  session_duration: integer (seconds, for break calculations)
  
Response (200):
  task: Task (updated with timing data)
  focus_session: object
    session_id: uuid
    started_at: datetime
    duration_seconds: integer
    break_due_at: datetime (nullable)
    productivity_score: integer (1-10, nullable)
    
Response (400):
  Problem Details for invalid focus actions
```

### 4.3 Recipe Management API (Mealie Integration)

```yaml
GET /productivity/recipes
Summary: Search and browse recipes
Performance Requirement: <2s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  search: string (name, description, ingredients)
  category: string (breakfast|lunch|dinner|snack|dessert)
  cuisine: string
  tags: string[] (comma-separated)
  dietary_restrictions: string[] (vegetarian|vegan|gluten_free)
  max_prep_time: integer (minutes)
  max_total_time: integer (minutes)
  rating_min: integer (1-5)
  owner_id: uuid (optional, defaults to current user + public)
  limit: integer (default: 24)
  offset: integer (default: 0)
  
Response (200):
  recipes: Recipe[]
  
Recipe:
  id: uuid
  name: string
  description: string
  prep_time: string (ISO 8601 duration)
  cook_time: string
  total_time: string
  servings: integer
  category: string
  cuisine: string
  tags: string[]
  dietary_restrictions: string[]
  rating: integer (1-5, nullable)
  owner_id: uuid
  is_public: boolean
  ingredient_count: integer
  created_at: datetime
```

```yaml
GET /productivity/recipes/{id}/ingredients
Summary: Get recipe ingredients with shopping integration
Headers:
  Authorization: Bearer {jwt_token}
  
Response (200):
  ingredients: RecipeIngredient[]
  shopping_list_compatible: boolean
  estimated_cost: number (nullable)
  
RecipeIngredient:
  ingredient_id: uuid
  name: string
  quantity: number
  unit: string
  notes: string (optional preparation notes)
  optional: boolean
  category: string (produce|dairy|meat|pantry)
  estimated_price: number (nullable)
```

### 4.5 DDD Integration - Productivity Domain

#### Domain Event Publishing for Executive Function Support

```yaml
POST /productivity/events/publish
Summary: Publish productivity domain events for cross-domain workflows
Performance Requirement: <2s response time
Headers:
  Authorization: Bearer {jwt_token}
  X-Source-Domain: productivity
  
Request Body:
  event_type: string (task_completed|workflow_triggered|recipe_planned|deadline_approaching)
  aggregate_id: uuid
  event_data: object
  executive_function_context: object
    user_focus_session_id: uuid (optional)
    attention_priority: string (low|medium|high|urgent)
    cognitive_load_impact: string (minimal|moderate|high)
    
Event Types:
  task_completed:
    task_id: uuid
    completion_time: datetime
    focus_duration_minutes: number
    interruption_count: number
    
  workflow_triggered:
    workflow_id: uuid (n8n workflow)
    trigger_source: string
    estimated_duration_minutes: number
    requires_user_attention: boolean
```

#### Executive Function Accommodation API

```yaml
GET /productivity/executive-functions/accommodations
Summary: Retrieve user-specific executive function accommodations
Headers:
  Authorization: Bearer {jwt_token}
  
Response (200):
  focus_preferences: object
    break_reminder_interval_minutes: number
    focus_session_max_duration_minutes: number
    distraction_blocking_enabled: boolean
    
  cognitive_load_management: object
    max_concurrent_tasks: number
    task_complexity_auto_assessment: boolean
    deadline_buffer_percentage: number
    
  interface_accommodations: object
    reduce_visual_complexity: boolean
    consistent_navigation_required: boolean
    progress_indicators_verbose: boolean
```

## 5. TCG Domain API Contracts

### 5.1 Card Database API

```yaml
GET /tcg/cards
Summary: Search Magic: The Gathering cards
Performance Requirement: <3s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  name: string (partial match with fuzzy search)
  colors: string[] (W|U|B|R|G, comma-separated)
  color_identity: string[] (for Commander format)
  type: string (creature|instant|sorcery|enchantment|artifact|planeswalker)
  mana_cost: string (exact match: {2}{R}{R})
  cmc: integer (converted mana cost)
  cmc_min: integer
  cmc_max: integer
  set_code: string
  rarity: string (common|uncommon|rare|mythic)
  legal_in: string[] (format names)
  text: string (oracle text search)
  limit: integer (default: 50, max: 500)
  offset: integer (default: 0)
  
Response (200):
  cards: TcgCard[]
  
TcgCard:
  id: uuid
  name: string
  mana_cost: string
  converted_mana_cost: integer
  type_line: string
  oracle_text: string
  power: string (nullable)
  toughness: string (nullable)
  loyalty: string (nullable)
  colors: string[]
  color_identity: string[]
  set_code: string
  set_name: string
  rarity: string
  legalities: object (format: legal|banned|restricted)
  edhrec_rank: integer (nullable)
  price_usd: number (nullable)
  scryfall_id: uuid (nullable)
```

```yaml
GET /tcg/cards/{id}/combos
Summary: Find combos using specific card
Performance Requirement: <3s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  format: string (commander|legacy|vintage)
  difficulty: string (easy|medium|hard|jank)
  competitive: boolean (competitive viability filter)
  limit: integer (default: 25)
  
Response (200):
  combos: TcgCombo[]
  
TcgCombo:
  id: uuid
  name: string
  description: string
  steps: string[]
  results: string[]
  required_cards: TcgCard[] (simplified)
  required_mana: string
  difficulty: string
  popularity_score: integer
  upvotes: integer
  downvotes: integer
```

### 5.2 Deck Management API

```yaml
GET /tcg/decks
Summary: List user's decks and public decks
Performance Requirement: <3s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  owner_id: uuid (optional, defaults to current user)
  format: string (commander|standard|modern|legacy|vintage)
  commander_id: uuid (for Commander format)
  color_identity: string[] (WUBRG combinations)
  power_level: integer (1-10)
  is_public: boolean
  strategy_tags: string[] (aggro|control|combo|midrange)
  limit: integer (default: 20)
  offset: integer (default: 0)
  
Response (200):
  decks: TcgDeck[]
  
TcgDeck:
  id: uuid
  name: string
  description: string
  format: string
  commander: TcgCard (nullable)
  partner_commander: TcgCard (nullable)
  color_identity: string[]
  power_level: integer (1-10)
  strategy_tags: string[]
  card_count: integer
  estimated_price: number (nullable)
  owner_id: uuid
  is_public: boolean
  version: integer
  last_modified: datetime
  created_at: datetime
```

```yaml
POST /tcg/decks/{id}/analyze
Summary: Analyze deck composition and performance
Performance Requirement: <3s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Response (200):
  analysis: DeckAnalysis
  
DeckAnalysis:
  mana_curve: object
    cmc_0: integer
    cmc_1: integer
    # ... up to cmc_7_plus
  color_distribution: object
    white: number (percentage)
    blue: number
    black: number
    red: number
    green: number
    colorless: number
  card_types: object
    creatures: integer
    instants: integer
    sorceries: integer
    enchantments: integer
    artifacts: integer
    planeswalkers: integer
    lands: integer
  synergy_score: integer (1-100)
  consistency_score: integer (1-100)
  speed_score: integer (1-100)
  resilience_score: integer (1-100)
  recommendations: string[] (improvement suggestions)
```

### 5.5 DDD Integration - TCG Domain

#### Domain Event Publishing for Game Analysis

```yaml
POST /tcg/events/publish
Summary: Publish TCG domain events for cross-domain integration
Performance Requirement: <3s response time
Headers:
  Authorization: Bearer {jwt_token}
  X-Source-Domain: tcg
  
Request Body:
  event_type: string (deck_optimized|combo_discovered|card_price_alert|tournament_result)
  aggregate_id: uuid
  event_data: object
  
Event Types:
  deck_optimized:
    deck_id: uuid
    optimization_type: string (budget|competitive|casual)
    performance_improvement_percentage: number
    estimated_cost_change: number
    
  combo_discovered:
    combo_id: uuid
    card_ids: uuid[]
    combo_type: string (infinite|synergy|engine)
    mana_cost_total: number
    reliability_score: integer
```

#### Commander Spellbook Integration

```yaml
GET /tcg/combos/search
Summary: Search infinite combos and synergies (Commander Spellbook integration)
Performance Requirement: <3s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  cards: string[] (card names, minimum 1 required)
  colors: string[] (W|U|B|R|G)
  max_cards: integer (maximum combo pieces)
  combo_type: string (infinite|synergy|engine)
  format: string (commander|legacy|modern|standard)
  
Response (200):
  combos: TCGCombo[]
  
TCGCombo:
  id: uuid
  name: string
  card_names: string[]
  mana_cost_total: number
  color_identity: string[]
  combo_type: string
  reliability_score: integer (1-100)
  description: string
  source_url: string (Commander Spellbook reference)
```

## 6. Infrastructure Domain API Contracts

### 6.1 Service Management API

```yaml
GET /infrastructure/services
Summary: Monitor and manage platform services
Performance Requirement: <5s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  organization_id: uuid
  service_type: string (web|api|database|cache|queue)
  status: string (healthy|degraded|down|maintenance)
  environment: string (dev|staging|production)
  search: string (name search)
  limit: integer (default: 50)
  offset: integer (default: 0)
  
Response (200):
  services: InfrastructureService[]
  
InfrastructureService:
  id: uuid
  name: string
  description: string
  service_type: string
  status: string
  environment: string
  internal_url: string (nullable)
  external_url: string (nullable)
  health_check_url: string (nullable)
  last_health_check: datetime (nullable)
  uptime_percentage: number (nullable)
  cpu_usage: number (nullable, percentage)
  memory_usage: number (nullable, percentage)
  depends_on: string[] (service names)
  created_at: datetime
```

```yaml
POST /infrastructure/services/{id}/health-check
Summary: Trigger manual health check for service
Headers:
  Authorization: Bearer {jwt_token}
  
Response (200):
  health_check: HealthCheckResult
  
HealthCheckResult:
  service_id: uuid
  status: string (healthy|degraded|down)
  response_time_ms: integer
  checks: HealthCheck[]
  timestamp: datetime
  
HealthCheck:
  name: string (database|external_api|disk_space)
  status: string (pass|warn|fail)
  message: string
  details: object (check-specific data)
```

### 6.2 Configuration Management API

```yaml
GET /infrastructure/configs
Summary: Manage tool configurations and settings
Performance Requirement: <5s response time
Headers:
  Authorization: Bearer {jwt_token}
  
Query Parameters:
  tool_name: string (it-tools|kong|kasmvnc)
  owner_id: uuid
  access_level: string (private|team|organization|public)
  is_active: boolean
  limit: integer (default: 25)
  offset: integer (default: 0)
  
Response (200):
  configurations: ToolConfiguration[]
  
ToolConfiguration:
  id: uuid
  tool_name: string
  instance_name: string (nullable)
  config_data: object (tool-specific configuration)
  config_schema_version: string
  owner_id: uuid
  access_level: string
  is_active: boolean
  version: integer
  last_validated: datetime (nullable)
  validation_errors: string[] (nullable)
  created_at: datetime
  updated_at: datetime
```

### 6.5 DDD Integration - Infrastructure Domain

#### Cross-Domain Service Management

```yaml
POST /infrastructure/events/publish
Summary: Publish infrastructure domain events for system-wide monitoring
Performance Requirement: <5s response time
Headers:
  Authorization: Bearer {jwt_token}
  X-Source-Domain: infrastructure
  
Request Body:
  event_type: string (service_deployed|config_updated|health_degraded|scaling_triggered)
  aggregate_id: uuid
  event_data: object
  
Event Types:
  service_deployed:
    service_name: string
    version: string
    deployment_environment: string
    health_status: string
    
  config_updated:
    config_id: uuid
    tool_name: string
    change_summary: string
    rollback_available: boolean
```

#### Architecture Validation for 37-Tool Integration

```yaml
GET /infrastructure/architecture/migration-status
Summary: Monitor architectural compliance during 37-tool migration
Headers:
  X-Internal-Service: true
  
Response (200):
  migration_progress: object
    total_tools: integer (37)
    migrated_tools: integer
    tools_in_progress: string[]
    tools_pending: string[]
    
  domain_health: object
    security_domain_isolation: boolean
    productivity_domain_isolation: boolean
    tcg_domain_isolation: boolean
    infrastructure_domain_isolation: boolean
    
  performance_compliance: object
    domain_sla_violations_24h: object
      security: integer (should be 0)
      productivity: integer (should be 0)
      tcg: integer (should be 0)
      infrastructure: integer (should be 0)
```

## 7. Real-Time & Event Contracts

### 7.1 WebSocket Event Streaming

```yaml
WebSocket /events/stream
Summary: Real-time event streaming across all domains
Headers:
  Authorization: Bearer {jwt_token}
  
Connection Parameters:
  domains: string[] (security|productivity|tcg|infrastructure)
  event_types: string[] (specific event filtering)
  user_events_only: boolean (default: false)
  
Server Messages:
  event: DomainEvent
  heartbeat: object (every 30s)
  error: Problem Details
  connection_info: object (on connect)
  
Client Messages:
  subscribe: object (update filters)
  unsubscribe: object (stop specific events)
  ping: object (connectivity test)
  
DomainEvent:
  id: uuid
  event_type: string
  domain: string
  aggregate_id: string
  event_data: object
  user_id: uuid (nullable)
  organization_id: uuid (nullable)
  occurred_at: datetime
```

### 7.2 Webhook Integration

```yaml
POST /events/webhooks
Summary: Register webhook endpoints for external integrations
Headers:
  Authorization: Bearer {jwt_token}
  Content-Type: application/json
  
Request Body:
  url: string (required, HTTPS only)
  event_types: string[] (required)
  secret: string (for signature verification)
  is_active: boolean (default: true)
  
Response (201):
  webhook: WebhookRegistration
  
WebhookRegistration:
  id: uuid
  url: string
  event_types: string[]
  secret_hash: string (hashed version)
  is_active: boolean
  last_delivery_at: datetime (nullable)
  failure_count: integer
  created_at: datetime
```

## 8. Error Handling & Problem Details

### 8.1 Standard Error Responses

```yaml
RFC 7807 Problem Details Format:
  Content-Type: application/problem+json
  
  Base Structure:
    type: string (URI identifying the problem type)
    title: string (human-readable summary)
    status: integer (HTTP status code)
    detail: string (explanation specific to this occurrence)
    instance: string (URI identifying this specific occurrence)
    
  Extensions:
    error_code: string (internal error code)
    trace_id: string (for logging correlation)
    timestamp: datetime
    validation_errors: object[] (for 400 responses)
```

### 8.2 Common Problem Types

```yaml
Authentication Problems:
  /errors/authentication-required (401)
  /errors/token-expired (401)
  /errors/insufficient-permissions (403)
  
Validation Problems:
  /errors/validation-failed (400)
  /errors/duplicate-resource (409)
  /errors/resource-not-found (404)
  
Rate Limiting Problems:
  /errors/rate-limit-exceeded (429)
  
Server Problems:
  /errors/internal-server-error (500)
  /errors/service-unavailable (503)
  /errors/performance-degraded (503)
```

## 9. Performance & Rate Limiting

### 9.1 Domain-Specific Rate Limits

```yaml
Rate Limiting by Domain:
  Security APIs:
    - Standard: 1000 req/hour per user
    - Threat indicator queries: 5000 req/hour
    - YARA compilation: 100 req/hour (resource intensive)
    
  Productivity APIs:
    - Task operations: 2000 req/hour per user
    - Recipe searches: 1000 req/hour
    - File uploads: 50 req/hour (size-based limits)
    
  TCG APIs:
    - Card searches: 2000 req/hour per user
    - Deck analysis: 200 req/hour (computation intensive)
    - Combo queries: 500 req/hour
    
  Infrastructure APIs:
    - Configuration updates: 100 req/hour
    - Health checks: 1000 req/hour
    - Service monitoring: 5000 req/hour
```

### 9.2 Performance Monitoring Headers

```yaml
Response Headers for Performance Tracking:
  X-Response-Time: string (processing time in ms)
  X-Rate-Limit-Remaining: integer
  X-Rate-Limit-Reset: integer (Unix timestamp)
  X-Domain-Performance-Tier: string (security|productivity|tcg|infrastructure)
  X-Cache-Status: string (hit|miss|stale)
  X-Request-ID: string (for tracing and debugging)
```

---

**API Contracts Complete** | **Phase 1 Progress**: 67% | **Next**: Quickstart Guide
