# Universal Project Analysis Template (v1.1)

**Purpose**: Capture 90%+ of project information needed for migration, integration, or reimplementation

**Instructions**: 
- Fill out ALL sections, even if answer is "N/A" or "None"
- Use concrete examples, not generic descriptions
- Copy actual code snippets for critical business logic
- Include WHY decisions were made, not just WHAT exists
- Mark sections as [CRITICAL], [IMPORTANT], or [NICE-TO-HAVE] based on migration priority

## TECHNICAL CONTENT GUIDANCE (Important for Validation)

**Legitimate Technical Patterns** - These are NOT placeholders and should be included as examples:

**✅ JSON Configurations & API Responses**:
```json
{"rules": [{"identifier": "suspicious_strings"}]}
{"status": "ok", "data": {"users": 1250}}
[{"name": "admin", "permissions": ["read", "write"]}]
```

**✅ Hex Patterns & Binary Data** (Security/Analysis Tools):
```
{6A 40 68 ?? ?? 00 00}
0x41414141
\x90\x90\x90\x90
```

**✅ Code Template Variables** (In Documentation):
```
{syslog_time}, {src_ip}, {user_id}
${DATABASE_URL}, ${API_KEY}
{match.rule}, {object.property}
```

**✅ Technical Identifiers**:
```
API Endpoints: /api/v1/users/{id}, /health/check
File Paths: src/components/UserList.tsx, apps/api/src/lib/entities.ts
CLI Commands: docker run --name {container}
Database Fields: user_id, created_at, is_active
```

**✅ Domain-Specific Syntax**:
```
MTG: {1}{W}{U}{B}{R}{G}, {T}: Add {C}
SQL: SELECT * FROM users WHERE id = ?
Regex: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
YARA: rule suspicious_file { condition: $hex_pattern }
```

**✅ Honest Responses for Inapplicable Sections**:
- "N/A" - Section doesn't apply to this project type
- "None" - Feature is not implemented
- "TBD" - Planned but not yet implemented (with explanation)

**❌ Actual Placeholders to Avoid**:
- [TODO: Add details]
- [REPLACE WITH ACTUAL VALUES]  
- {template_placeholder}
- [Your system name here]

## DOMAIN-APPROPRIATE SECTION REQUIREMENTS

**Security Tools**: May skip Business Logic, Frontend Architecture sections
**CLI Libraries**: May skip Authentication, External Integrations sections  
**Developer Tools**: May skip Business Logic, Performance sections
**Business Applications**: Should complete all sections
**Frameworks**: Should be comprehensive across all sections

When a section truly doesn't apply, provide a brief explanation:
"N/A - CLI tool has no user interface" or "N/A - Library provides functions, no auth needed"

---

## Section 1: Project Identity & Context

### 1.1 Basic Information
```yaml
Project Name: 
Repository URL: 
Primary Domain: [Auth / E-commerce / Analytics / MTG / etc]
Project Status: [Active / Maintenance / Deprecated]
Business Purpose: [1-2 sentences: Why does this project exist?]
Key Stakeholders: [Who depends on this? Internal team / External users / API consumers]
Monthly Active Users: [Approximate if unknown]
Critical to Business: [YES / NO / SOMEWHAT - explain]
```

### 1.2 Technology Stack Inventory
```yaml
Programming Languages:
  - Language: [Python / TypeScript / JavaScript / Go / etc]
    Version: [3.11 / ES2020 / etc]
    Percentage of Codebase: [~60% / etc]
    Primary Use: [Backend API / Frontend / Scripts / etc]

Primary Frameworks:
  Backend:
    - Name: [Django / FastAPI / Express / etc]
      Version: 
      Why Chosen: [Performance / Team familiarity / Feature set]
  
  Frontend:
    - Name: [Next.js / React / Vue / etc]
      Version:
      Router: [App Router / Pages Router / Vue Router]
      Why Chosen:

Database:
  Primary:
    - Type: [PostgreSQL / MongoDB / MySQL]
      Version:
      Size: [~1GB / ~100GB / etc]
      Schema Location: [migrations/ / schema.sql / etc]
  
  Cache:
    - Type: [Redis / Memcached / None]
      Version:
      Use Case: [Session storage / API caching / etc]

Build & Dev Tools:
  - Package Manager: [npm / yarn / pnpm / pip / poetry]
  - Build Tool: [Webpack / Vite / Rollup / etc]
  - Linter: [ESLint / Pylint / etc]
  - Formatter: [Prettier / Black / etc]
  - Testing Framework: [Jest / pytest / Cypress / etc]
  - CI/CD: [GitHub Actions / Jenkins / GitLab CI / etc]

Infrastructure:
  - Hosting: [AWS / Heroku / Vercel / Self-hosted / etc]
  - Containerization: [Docker / None]
  - Orchestration: [Kubernetes / Docker Compose / None]
  - Environment Variables: [.env file location and key variables list]
```

### 1.3 Project Structure
```
Root Directory Layout:
[Copy your actual directory tree, 2-3 levels deep]

Example:
project-root/
├── backend/
│   ├── src/
│   │   ├── models/
│   │   ├── services/
│   │   └── api/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── hooks/
│   └── package.json
└── docs/

Key Directories Explained:
- [directory name]: [what lives here and why]
```

---

## Section 2: Data Architecture [CRITICAL]

### 2.1 Data Models Inventory

**For EACH primary data model, fill this out:**

```yaml
Model Name: [e.g., User, Product, Order, Card, Combo]
Description: [1 sentence: what this represents in the domain]
Priority: [CRITICAL / IMPORTANT / NICE-TO-HAVE]
Source File: [exact file path]

Fields:
  - name: [field_name]
    type: [string / integer / boolean / foreign_key / json / etc]
    constraints: [unique / required / indexed / max_length:255]
    default: [value or "none"]
    description: [what this field represents]
    business_rules: [any validation or logic tied to this field]
  
  [Repeat for ALL fields]

Relationships:
  - related_model: [Model name]
    relationship_type: [one-to-many / many-to-many / one-to-one]
    relationship_name: [field name or through table]
    cascade_behavior: [on_delete: CASCADE / SET_NULL / PROTECT]
    description: [why this relationship exists]

Indexes:
  - fields: [field1, field2]
    type: [btree / gin / unique]
    reason: [performance / uniqueness / search optimization]

Computed Fields:
  - name: [field_name]
    computation: [how it's calculated]
    generated: [database / application_layer / on_read]
    example: [show calculation with real values]

Validation Rules:
  - rule: [e.g., "email must be valid format"]
    enforced: [database / application / both]
    error_message: [what users see when violated]

Special Behaviors:
  - behavior: [e.g., "Auto-generates slug from name"]
    implementation: [signal / save override / database trigger]
    code_location: [file path]
```

### 2.2 Critical Data Relationships Map

**Draw or describe the key relationships:**
```
[Use ASCII art or description]

Example:
User (1) ────< many >──── Post (many)
                           │
                           │
                          many
                           │
                           ▼
                        Comment (many)
                           │
                           │
                          many
                           │
                           ▼
                        User (1) [commenter]

Critical Path: User creates Posts, Posts have Comments, Comments reference Users
```

### 2.3 Database Performance Patterns

```yaml
Query Optimization Strategies:
  - strategy: [Prefetch related / Select related / Raw SQL]
    location: [file path]
    reason: [solves N+1 / handles large result sets]
    impact: [query time: 2000ms → 50ms]

Denormalization Patterns:
  - pattern: [Cached count fields / Materialized views]
    fields: [list denormalized fields]
    update_trigger: [signal / cron / on_save]
    reason: [avoid expensive joins / improve read performance]

Problematic Queries:
  - query_description: [what it does]
    performance: [slow / acceptable / fast]
    location: [file path and line number]
    notes: [any workarounds or known issues]
```

---

## Section 3: API Architecture [CRITICAL]

### 3.1 Authentication & Authorization

```yaml
Authentication Method:
  - type: [JWT / Session / OAuth / API Key / None]
    provider: [Custom / Auth0 / Discord / Cognito]
    implementation_location: [file path]
    token_lifetime: [5 minutes / 1 day / etc]
    refresh_strategy: [refresh tokens / re-login / etc]

Authorization Pattern:
  - type: [Role-based / Permission-based / Attribute-based]
    roles_list: [Admin, User, Guest, etc - list ALL]
    permissions_list: [list ALL permissions if granular]

Access Control Rules:
  - rule: [e.g., "Users can only edit own content"]
    enforcement_location: [middleware / view decorator / service layer]
    code_example: |
      [Paste actual code snippet]

External Auth Integrations:
  - provider: [Discord / Google / GitHub]
    scopes_required: [email, guilds, etc]
    special_logic: [e.g., "Must be member of specific Discord server"]
    validation_endpoint: [API URL called]
    failure_handling: [Fail closed / Fail open / Cached fallback]
```

### 3.2 API Endpoints Inventory

**For EACH endpoint (or endpoint pattern if many):**

```yaml
Endpoint: [HTTP Method] [Path]
Example: GET /api/v1/users/{id}

Authentication Required: [YES / NO / OPTIONAL]
Authorization: [Who can access: Any authenticated user / Admin only / Owner only]

Request:
  Path Parameters:
    - name: [id]
      type: [integer]
      validation: [must exist, must be positive integer]
  
  Query Parameters:
    - name: [filter]
      type: [string]
      required: [yes/no]
      default: [value]
      description: [what it does]
  
  Body Schema: [if POST/PUT/PATCH]
    ```json
    {
      "field1": "type",
      "field2": "type"
    }
    ```
  
  Headers:
    - name: [Authorization]
      value: [Bearer {token}]
      required: [yes]

Response:
  Success (200):
    ```json
    {
      "example": "response"
    }
    ```
  
  Error Cases:
    - status: [401]
      body: [{ "error": "Unauthorized" }]
      condition: [Invalid or missing token]
    
    - status: [404]
      body: [{ "error": "Not found" }]
      condition: [Resource doesn't exist]
    
    - status: [500]
      body: [{ "error": "Internal error" }]
      condition: [Database error / External API failure]

Business Logic:
  - [Describe what happens when this endpoint is called]
  - [Include any side effects: sends emails, updates cache, triggers webhooks]
  
Performance:
  - Average Response Time: [50ms / 500ms / 2s]
  - P95 Response Time: [200ms / 1s / 5s]
  - Rate Limited: [YES - 100 req/min / NO]

Dependencies:
  - External API: [Scryfall API / Stripe / etc]
    Failure Handling: [Retry / Fallback / Error response]
  
  - Database Queries: [Describe main queries]
    Optimization: [Indexed / Cached / Raw SQL]
```

### 3.3 API Patterns & Conventions

```yaml
REST Conventions:
  - URL Pattern: [/api/v1/resource/{id} or different]
  - Pagination: [cursor-based / offset-based / none]
  - Filtering: [query params / body / not supported]
  - Sorting: [query params / fixed / not supported]
  - Versioning Strategy: [URL path / header / not versioned]

Error Handling Pattern:
  - Standard Error Format: 
    ```json
    [Paste your actual error response format]
    ```
  
  - HTTP Status Code Usage:
    - 400: [Validation errors]
    - 401: [Authentication required]
    - 403: [Permission denied]
    - 404: [Resource not found]
    - 500: [Server error]
    [Add others if different]

Data Serialization:
  - Request Format: [JSON / Form data / Multipart]
  - Response Format: [JSON / XML / Both]
  - Date Format: [ISO 8601 / Unix timestamp / Other]
  - Null Handling: [null / undefined / omitted]

Rate Limiting:
  - Implemented: [YES / NO]
  - Strategy: [Token bucket / Fixed window / Sliding window]
  - Limits: [100 req/min per user / 1000 req/hour per IP]
  - Headers: [X-RateLimit-Remaining, etc]
```

---

## Section 4: Business Logic [CRITICAL]

### 4.1 Critical Algorithms

**For EACH complex algorithm or business logic:**

```yaml
Algorithm Name: [Variant Generation / Pricing Calculator / etc]
Location: [exact file path and function/class name]
Lines of Code: [approximate]
Complexity: [Simple / Medium / Complex / Very Complex]
Priority: [MUST PRESERVE / CAN REFACTOR / CAN REWRITE]

Purpose:
  [2-3 sentences: What problem does this solve?]

Inputs:
  - input_name: [type and description]
  [List ALL inputs]

Outputs:
  - output_name: [type and description]
  [List ALL outputs]

Algorithm Logic:
  [High-level description OR pseudocode OR paste actual code]
  
  Example:
  1. Load all cards matching template query
  2. For each combination of cards (up to max_cards limit):
     a. Check color identity compatibility
     b. Calculate total mana cost
     c. Validate prerequisite features
     d. Generate variant ID hash
     e. Check if variant already exists
     f. If new, create variant record
  3. Return count of generated variants

Edge Cases Handled:
  - case: [Empty input set]
    handling: [Return empty list / Raise error]
  
  - case: [Duplicate cards in combo]
    handling: [Allow if explicitly configured / Reject]
  
  - case: [Infinite loop prevention]
    handling: [Max iterations = 10000 / Timeout after 30s]

Performance Characteristics:
  - Time Complexity: [O(n²) / O(n log n) / etc]
  - Space Complexity: [O(n) / O(1) / etc]
  - Typical Runtime: [50ms / 5s / 30s]
  - Max Input Size Tested: [10,000 items / etc]

Known Issues:
  - issue: [Description of any known bugs or limitations]
    workaround: [How it's currently handled]
    priority: [Fix needed / Acceptable / etc]

Dependencies:
  - [List any external libraries or services this depends on]
  - [List any other internal functions this calls]

Test Coverage:
  - Unit Tests: [YES - 90% coverage / NO / PARTIAL]
  - Integration Tests: [YES / NO]
  - Test Location: [file path]
  
Why This Matters:
  [Explain why this can't be a simple CRUD operation]
  [What business value does this complexity provide?]
```

### 4.2 Validation Rules

```yaml
Data Validation:
  Model: [Model name]
  Rules:
    - field: [field_name]
      rule: [must be unique / must match regex / must be positive]
      error_message: [what user sees]
      enforcement: [database constraint / application validation / both]

Business Rule Validation:
  - rule_name: [Descriptive name]
    description: [What must be true]
    violated_when: [Specific conditions]
    error_response: [HTTP status and message]
    enforcement_location: [file path]
    
    example:
      valid_input: [Show example that passes]
      invalid_input: [Show example that fails]
      error_returned: [Actual error message]
```

### 4.3 Workflow & State Machines

**For each workflow (e.g., order processing, content moderation):**

```yaml
Workflow Name: [Suggestion Review Process]
Entities Involved: [User, Suggestion, Editor]

States:
  - state: [NEW]
    description: [User submitted, not yet reviewed]
    allowed_transitions: [AWAITING_DISCUSSION, REJECTED]
    permissions: [User can edit, Editor can transition]
  
  - state: [AWAITING_DISCUSSION]
    description: [Editor reviewing]
    allowed_transitions: [PENDING_APPROVAL, REJECTED]
    permissions: [Only editor can edit]
  
  [List ALL states]

Transitions:
  - from: [NEW]
    to: [AWAITING_DISCUSSION]
    trigger: [Editor clicks "Review"]
    validation: [Must have valid content]
    side_effects: [Send notification to user, Log to audit trail]
    code_location: [file path]
  
  [List ALL transitions]

Permissions by State:
  - state: [NEW]
    can_view: [Author, Editors, Admins]
    can_edit: [Author only]
    can_delete: [Author, Admins]
  
  [List for ALL states]

Terminal States:
  - [ACCEPTED]: [Cannot transition further]
  - [REJECTED]: [Cannot transition further]
```

---

## Section 5: External Integrations [IMPORTANT]

### 5.1 Third-Party APIs

**For EACH external API:**

```yaml
Service Name: [Scryfall API / Stripe / Twilio / etc]
Purpose: [Why you use this: Card data / Payments / SMS / etc]
Criticality: [CRITICAL - app won't work without / IMPORTANT / NICE-TO-HAVE]

Integration Details:
  - API Type: [REST / GraphQL / gRPC / WebSocket]
  - Base URL: [https://api.service.com]
  - Authentication: [API Key / OAuth / Bearer Token]
  - Credentials Storage: [Environment variable name]

Endpoints Used:
  - endpoint: [GET /v1/cards]
    purpose: [Fetch card data]
    frequency: [Called every 5 minutes / On demand / etc]
    rate_limit: [50 requests per second]
  
  [List ALL endpoints you call]

Data Flow:
  - direction: [INBOUND - you fetch / OUTBOUND - you send]
  - data_type: [Card metadata / Payment info / etc]
  - frequency: [Real-time / Hourly batch / etc]
  - volume: [~1000 requests/day / ~50GB/month]

Error Handling:
  - network_failure: [Retry 3 times with exponential backoff / Fail immediately]
  - rate_limit_hit: [Cache last response for 5 min / Return error to user]
  - invalid_response: [Log error and return default / Raise exception]
  - service_down: [Fail closed / Fail open / Use cached data]

Caching Strategy:
  - cached: [YES / NO]
  - cache_location: [Redis / In-memory / Database]
  - ttl: [5 minutes / 1 hour / 1 day]
  - cache_key_pattern: [api_response:{endpoint}:{params_hash}]

Dependencies:
  - data_dependency: [App cannot function without this data]
  - feature_dependency: [Only affects specific feature]

Tribal Knowledge:
  - [Any quirks about this API that aren't documented]
  - [Workarounds you've implemented]
  - [Special headers or formatting required]
  
  Example: "Must use fake User-Agent or requests get rate-limited aggressively"
```

### 5.2 Authentication Providers

```yaml
Provider: [Discord OAuth / Auth0 / Cognito / Custom]
Why Chosen: [Community requirement / Enterprise SSO / etc]

OAuth Configuration:
  - client_id: [Environment variable name]
  - client_secret: [Environment variable name]
  - scopes: [email, profile, guilds]
  - callback_url: [/auth/callback]
  - authorization_url: [Provider's auth URL]
  - token_url: [Provider's token URL]

Special Validation:
  - validation_type: [Guild membership / Email domain / etc]
  - validation_logic: [Detailed description]
  - validation_endpoint: [API URL called]
  - failure_behavior: [Deny access / Allow with restrictions]

User Data Mapping:
  - provider_field: [sub]
    maps_to: [user.external_id]
  
  - provider_field: [email]
    maps_to: [user.email]
  
  [Map ALL fields you extract]

Token Management:
  - access_token_lifetime: [5 minutes]
  - refresh_token_lifetime: [7 days]
  - storage: [HTTP-only cookie / localStorage / Database]
  - refresh_strategy: [Automatic / Manual]
```

### 5.3 Other External Services

```yaml
Service Type: [CDN / Email / SMS / Analytics / Logging / etc]
Service Name: [Cloudflare / SendGrid / etc]
Purpose: [What it does for your app]
Configuration: [Where config lives, what needs to be set]
Criticality: [CRITICAL / IMPORTANT / NICE-TO-HAVE]
Fallback: [What happens if service is unavailable]
```

---

## Section 6: Frontend Architecture [IMPORTANT - if applicable]

### 6.1 Framework & Patterns

```yaml
Framework: [Next.js / React / Vue / Svelte]
Version: 
Architecture: [App Router / Pages Router / SPA / SSR / SSG]

State Management:
  - global: [Redux / Zustand / Context / None]
  - server: [React Query / SWR / Apollo / None]
  - url: [Next.js searchParams / React Router / None]
  - local: [useState / Vue reactive / etc]

Routing Strategy:
  - type: [File-based / Programmatic]
  - authentication_guard: [YES - how implemented / NO]
  - authorization_guard: [YES - how implemented / NO]

Data Fetching:
  - pattern: [Server Components / getServerSideProps / useEffect]
  - caching: [React Query / SWR / Manual / None]
  - error_handling: [Error boundaries / try-catch / etc]
```

### 6.2 Component Architecture

```yaml
Component Organization:
  - pattern: [Feature-based / Type-based / Domain-based]
  - reusable_location: [components/ui / shared / lib]
  - page_location: [pages / app / views]

Design System:
  - library: [Custom / shadcn / MUI / Tailwind / etc]
  - theme_location: [file path]
  - component_library: [Radix UI / Headless UI / None]

Styling Approach:
  - method: [CSS Modules / Styled Components / Tailwind / SCSS]
  - organization: [Co-located / Separate / Global]
  - responsive_strategy: [Mobile-first / Desktop-first / Adaptive]
```

### 6.3 Critical Frontend Components

**For each complex or important component:**

```yaml
Component Name: [SearchResults / ComboDisplay / etc]
Location: [file path]
Purpose: [1 sentence description]
Priority: [MUST PRESERVE / CAN REFACTOR / CAN REWRITE]

Props:
  - name: [propName]
    type: [string / number / object / function]
    required: [yes / no]
    description: [what it controls]

State:
  - name: [stateName]
    type: [type]
    purpose: [what it tracks]
    derived_from: [props / API / user_input]

Side Effects:
  - effect: [Fetches data on mount]
    trigger: [useEffect dependency]
    cleanup: [Aborts request / None]

Complex Logic:
  - logic: [Description of non-obvious behavior]
    reason: [Why this complexity exists]
    location: [function/hook name]

Performance Considerations:
  - memo: [YES - because / NO]
  - callback: [useMemo / useCallback used where]
  - virtualization: [YES - for large lists / NO]
  - lazy_loading: [Images / Routes / Components]

User Interactions:
  - interaction: [Click / Hover / Form submit]
    handler: [function name]
    validation: [client-side / server-side / both]
    error_handling: [toast / inline / modal]
```

### 6.4 Client-Side Routing

```yaml
Routes:
  - path: [/search]
    component: [SearchPage]
    auth_required: [YES / NO]
    data_loading: [Server-side / Client-side / Static]
    query_params: [q, filter, sort]
    purpose: [Main search interface]
  
  [List ALL routes]

Route Guards:
  - guard_type: [Authentication / Authorization / Subscription]
    implementation: [Middleware / HOC / Component check]
    redirect_on_fail: [/login / /403 / /upgrade]

Deep Linking:
  - supported: [YES / NO]
  - state_in_url: [Search filters / Form state / etc]
  - shareable: [URLs work when shared]
```

---

## Section 7: Testing & Quality [IMPORTANT]

### 7.1 Test Coverage

```yaml
Unit Tests:
  - framework: [Jest / pytest / Vitest]
  - coverage: [~85% / Unknown / Not measured]
  - location: [tests/ / __tests__ / co-located]
  - critical_coverage: [List modules with MUST-HAVE test coverage]

Integration Tests:
  - framework: [pytest / Supertest / etc]
  - coverage: [API endpoints / User workflows]
  - location: [file path]

End-to-End Tests:
  - framework: [Cypress / Playwright / Selenium / None]
  - coverage: [Critical user flows tested]
  - location: [file path]

Test Data:
  - fixtures: [YES - where / NO]
  - factories: [YES - where / NO]
  - mocking_strategy: [Mock external APIs / Use test database / etc]

Testing Framework:
  - framework: [name]
    coverage: [Run: npm test -- --coverage and paste results]
    ⚠️ DO NOT guess coverage - run actual commands
```

### 7.2 Critical Test Cases

**For business-critical functionality:**

```yaml
Test Suite: [Variant Generation Tests]
Location: [file path]
Coverage: [90% / Unknown]

Critical Test Cases:
  - test_name: [test_generates_valid_variants]
    scenario: [Given combo with 3 cards, generates all valid combinations]
    assertion: [Variant count matches expected, IDs are deterministic]
    why_critical: [Core business logic, must not break]
  
  - test_name: [test_color_identity_validation]
    scenario: [Rejects combos with incompatible color identities]
    assertion: [Raises ValidationError with specific message]
    why_critical: [Commander format rules must be enforced]
  
  [List ALL critical test cases]

Missing Test Coverage:
  - area: [Feature X]
    risk: [Medium / High]
    reason_missing: [Complex to test / Legacy code / etc]
```

---

## Section 8: Performance Characteristics [IMPORTANT]

### 8.1 Performance Baselines

```yaml
API Performance:
  - endpoint: [GET /api/cards]
    mean_response: [150ms]
    p95_response: [350ms]
    p99_response: [800ms]
  
  - endpoint: [POST /api/variants/generate]
    mean_response: [2500ms]
    p95_response: [8000ms]
    p99_response: [15000ms]
  
  Performance Baselines:
  ⚠️ MEASURE, don't estimate
  Run: console.time('operation-name')
  Provide actual numbers, not ranges

  [Measure or estimate for ALL critical endpoints]

Page Load Performance:
  - page: [/search]
    ttfb: [200ms]
    fcp: [600ms]
    lcp: [1200ms]
  
  [Measure for key pages]

Database Performance:
  - query: [Variant search with filters]
    execution_time: [50ms]
    rows_scanned: [~10,000]
    optimization: [Indexed on colors, features]

Background Jobs:
  - job: [Daily Scryfall sync]
    runtime: [15 minutes]
    frequency: [Daily at 2am UTC]
    resource_usage: [CPU-bound / IO-bound]
```

### 8.2 Performance Bottlenecks

```yaml
Known Bottlenecks:
  - location: [Variant generation algorithm]
    symptom: [Takes 10+ seconds for large combos]
    impact: [User-facing timeout]
    workaround: [Background job processing]
    fix_priority: [High / Medium / Low]
  
  - location: [Search without filters]
    symptom: [Table scan of 50,000 rows]
    impact: [Slow response time]
    workaround: [Force at least one filter]
    fix_priority: [Medium]

Optimization Strategies Used:
  - strategy: [Database query prefetching]
    location: [Manager classes]
    improvement: [2000ms → 50ms]
  
  - strategy: [Redis caching of API responses]
    location: [Service layer]
    improvement: [500ms → 10ms for cache hits]
```

### 8.3 Scalability Characteristics

```yaml
Current Scale:
  - users: [~10,000 monthly active]
  - requests: [~1M requests/month]
  - data_size: [~5GB database]

Scaling Limits:
  - database: [Can handle ~50GB before major slowdown]
  - api: [Current server handles ~50 req/sec comfortably]
  - background_jobs: [Single worker sufficient for current load]

Horizontal Scaling:
  - supported: [YES / NO / PARTIAL]
  - stateless: [YES - can add API servers / NO - session state in memory]
  - database_strategy: [Read replicas / Sharding / Single instance only]
```

---

## Section 9: Security & Compliance [IMPORTANT]

### 9.1 Security Measures

```yaml
Authentication Security:
  - password_storage: [Bcrypt / Argon2 / Hashed / Plain - NEVER PLAIN!]
  - mfa_supported: [YES / NO]
  - session_management: [JWT / Server-side / Cookies]
  - token_rotation: [YES - every X hours / NO]

Authorization Security:
  - permission_checks: [Middleware / Decorator / Service layer]
  - admin_separation: [Separate admin interface / Integrated]
  - role_escalation_protection: [YES - how / NO]

Data Security:
  - encryption_at_rest: [YES - database level / NO]
  - encryption_in_transit: [YES - TLS 1.3 / YES - TLS 1.2 / NO]
  - sensitive_data: [Passwords, API keys, etc - list ALL]
  - pii_handling: [Email, name, etc - list ALL]

Input Validation:
  - sql_injection_protection: [Parameterized queries / ORM]
  - xss_protection: [HTML escaping / CSP headers]
  - csrf_protection: [CSRF tokens / SameSite cookies]
  - file_upload_validation: [File type / Size / Content scanning]

API Security:
  - rate_limiting: [YES - strategy / NO]
  - cors_policy: [Specific domains / Open / Not configured]
  - api_versioning: [YES / NO]
```

### 9.2 Secrets Management

```yaml
Secrets Stored:
  - secret: [Database password]
    storage: [Environment variable / Secrets manager / Config file]
    rotation: [Manual / Automatic - frequency]
  
  - secret: [API keys for external services]
    storage: [Environment variable]
    rotation: [Annual / Never / etc]
  
  [List ALL secrets]

Environment Variables Required:
  - name: [DATABASE_URL]
    description: [PostgreSQL connection string]
    example: [postgresql://user:pass@localhost/db]
    required_in: [production, staging, development]
  
  [List ALL environment variables]
```

### 9.3 Compliance Requirements

```yaml
Regulations:
  - regulation: [GDPR / CCPA / HIPAA / None]
    applies: [YES / NO / UNSURE]
    requirements: [Right to deletion / Data export / etc]
    implementation: [How you comply]

Data Retention:
  - data_type: [User accounts]
    retention_period: [Forever / 7 years / Until user deletes]
    deletion_process: [Manual / Automated / Not implemented]

Audit Logging:
  - logged_events: [User login / Data modification / Admin actions]
  - log_retention: [90 days / 1 year / Forever]
  - log_location: [Database / Log files / External service]
```

---

## Section 10: Deployment & Operations [NICE-TO-HAVE]

### 10.1 Deployment Process

```yaml
Environment Strategy:
  - environments: [development, staging, production]
  - differences: [What changes between environments]

Deployment Method:
  - type: [Manual / CI/CD / Automated script]
  - trigger: [Git push / Manual approval / Scheduled]
  - rollback_process: [Git revert + redeploy / Database restore / etc]

Build Process:
  - steps: [Install deps / Run tests / Build / Deploy]
  - duration: [~5 minutes / etc]
  - artifacts: [Docker image / Static files / etc]

Configuration Management:
  - method: [Environment variables / Config files / Both]
  - location: [.env / Kubernetes ConfigMap / etc]
  - per_environment: [What config differs]
```

### 10.2 Monitoring & Logging

```yaml
Application Monitoring:
  - tool: [New Relic / DataDog / Sentry / etc]
  - metrics_tracked: [Response time / Error rate / etc]
  - alerts_configured: [YES - for what / NO]

Logging:
  - framework: [Python logging / Winston / etc]
  - log_levels: [DEBUG / INFO / WARNING / ERROR / CRITICAL]
  - log_destination: [stdout / File / CloudWatch / etc]
  - structured_logging: [YES - JSON / NO]

Error Tracking:
  - tool: [Sentry / Rollbar / Bugsnag / None]
  - error_notifications: [Email / Slack / PagerDuty]
  - error_rate_baseline: [~10 errors/day is normal]
```

### 10.3 Backup & Disaster Recovery

```yaml
Database Backups:
  - frequency: [Daily / Hourly / Continuous]
  - retention: [30 days / 1 year / etc]
  - tested: [YES - last test date / NO]
  - restoration_time: [~1 hour / Unknown]

Code Backups:
  - location: [Git repository]
  - redundancy: [GitHub + local / etc]

Recovery Procedures:
  - documented: [YES - where / NO]
  - rto: [Recovery Time Objective - 4 hours / etc]
  - rpo: [Recovery Point Objective - 24 hours / etc]
```

---

## Section 11: Domain Knowledge & Tribal Knowledge [CRITICAL]

### 11.1 Business Domain Expertise

```yaml
Domain: [MTG Commander / E-commerce / Healthcare / etc]

Domain Concepts Encoded in Code:
  - concept: [Color Identity]
    definition: [Commander deck must match commander's color identity]
    implementation: [merge_identities() function]
    source_of_truth: [MTG official rules / Your database / etc]
  
  - concept: [Reserved List]
    definition: [Cards Wizards promised never to reprint]
    implementation: [card.reserved boolean flag]
    source_of_truth: [Scryfall API / Manual list / etc]
  
  [List ALL domain concepts your code understands]

Industry-Specific Rules:
  - rule: [Commander deck size must be exactly 100 cards]
    enforcement: [Not enforced in this project / Validated on import]
  
  [List ALL rules]

Terminology Dictionary:
  - term: [Variant]
    definition: [Specific instance of a combo with actual cards]
    used_in: [Models, API endpoints, UI]
  
  - term: [Template]
    definition: [Generic card requirement like "any creature"]
    used_in: [Combo definitions]
  
  [Define ALL domain-specific terms]
```

### 11.2 Undocumented Knowledge

```yaml
Quirks & Workarounds:
  - quirk: [Scryfall API rate limits aggressively without User-Agent]
    workaround: [Always set fake User-Agent header]
    location: [scryfall_client.py line 42]
    reason: [Discovered through production errors]
  
  - quirk: [Database constraint violation if combo uses same card twice]
    workaround: [Check for duplicates before creating combo]
    location: [combo_service.py line 156]
    reason: [Unique constraint on (combo_id, card_id)]
  
  [Document ALL quirks you remember]

Historical Context:
  - decision: [Why we use Discord OAuth instead of email/password]
    reason: [Community already active on Discord server]
    date: [~2022 or unknown]
  
  - decision: [Why variant IDs are hashes instead of sequential]
    reason: [Deterministic IDs allow deduplication across instances]
    date: [Original design]
  
  [Document WHY decisions were made]

Known Technical Debt:
  - debt: [No pagination on combo list endpoint]
    impact: [Slow for users with many combos]
    workaround: [Limit to 100 results]
    fix_estimate: [2 days]
  
  [Be honest about shortcuts taken]
```

### 11.3 User Behavior Patterns

```yaml
Common User Workflows:
  - workflow: [Search for combos with specific cards]
    frequency: [80% of user sessions]
    steps: [1. Enter card names 2. Apply color filters 3. View results]
    pain_points: [Search is slow without filters]
  
  [Document how users actually use the system]

Edge Cases Users Hit:
  - edge_case: [User submits combo with 50+ cards]
    frequency: [Rare - ~1/month]
    current_behavior: [Times out]
    expected_behavior: [Show error message]
  
  [What breaks in production?]

User Expectations:
  - expectation: [Search results match EDHREC data]
    reality: [We sync daily, so may be 24h behind]
    user_confusion: [Sometimes report "missing" combos]
```

---

## Section 12: Migration Readiness Assessment

### 12.1 Migration Priority

```yaml
Overall Priority: [CRITICAL / IMPORTANT / NICE-TO-HAVE]
Reason: [Why this matters for the monolith]

User Impact:
  - users_affected: [10,000 monthly / 5 key stakeholders / etc]
  - downtime_acceptable: [YES - X hours / NO]
  - feature_parity_required: [100% / 80% / etc]

Technical Complexity:
  - data_migration: [Simple / Medium / Complex]
  - code_migration: [Simple / Medium / Complex]
  - integration_complexity: [Simple / Medium / Complex]

Dependencies:
  - blocking_projects: [List projects that must migrate first]
  - dependent_projects: [List projects that depend on this]
```

### 12.2 Risks & Concerns

```yaml
Data Migration Risks:
  - risk: [Loss of data during migration]
    likelihood: [Low / Medium / High]
    mitigation: [Backup + validation scripts]
  
  - risk: [Downtime exceeds acceptable window]
    likelihood: [Medium]
    mitigation: [Practice migration on staging]

Technical Risks:
  - risk: [Performance regression in monolith]
    likelihood: [Medium]
    mitigation: [Load testing + performance baselines]
  
  - risk: [External API integration breaks]
    likelihood: [Low]
    mitigation: [Contract tests + staging validation]

Business Risks:
  - risk: [Users churn due to different UX]
    likelihood: [Low]
    mitigation: [Preserve UI exactly during migration]
```

### 12.3 Success Criteria

```yaml
Functional Requirements:
  - [ ] 100% feature parity
  - [ ] All data migrated without loss
  - [ ] All API endpoints work identically
  - [ ] All external integrations work
  - [ ] All tests pass

Performance Requirements:
  - [ ] API response times within ±10% of baseline
  - [ ] Page load times within ±10% of baseline
  - [ ] No new N+1 query problems
  - [ ] Database query performance maintained

Quality Requirements:
  - [ ] Test coverage >= current baseline
  - [ ] No security regressions
  - [ ] Documentation updated
  - [ ] Team trained on new codebase
```

---

## Section 13: Documentation & Resources

### 13.1 Existing Documentation

```yaml
Documentation Locations:
  - type: [README / Wiki / External docs]
    url: [Link or file path]
    completeness: [Comprehensive / Partial / Outdated]
    last_updated: [Date or "Unknown"]

Code Comments:
  - quality: [Extensive / Adequate / Minimal / None]
  - areas_well_documented: [List modules with good comments]
  - areas_poorly_documented: [List modules needing comments]

Diagrams:
  - type: [Architecture / Data model / User flow]
    location: [File path or URL]
    current: [YES / NO]
```

### 13.2 Key Contacts

```yaml
Subject Matter Experts:
  - name: [Person or "Unknown"]
    expertise: [Business domain / Technical architecture / etc]
    availability: [Available / Left company / etc]

Original Developers:
  - name: [Person or "Unknown"]
    role: [Lead / Contributor]
    contact: [Email / GitHub / Not available]

Current Maintainers:
  - name: [Person or "You"]
    responsibilities: [Feature development / Bug fixes / etc]
```

---

## Analysis Completion Checklist

**Before considering this analysis complete:**

- [ ] All sections filled out (or marked N/A)
- [ ] All CRITICAL business logic documented with code examples
- [ ] All API endpoints inventoried with examples
- [ ] All data models documented with fields and relationships
- [ ] All external integrations documented with error handling
- [ ] Performance baselines measured or estimated
- [ ] Test coverage assessed
- [ ] Migration risks identified
- [ ] Tribal knowledge captured
- [ ] Edge cases and quirks documented

**Confidence Level:** [High / Medium / Low]  
**Areas Needing More Investigation:** [List any gaps]

---

**Analysis Completed By:** [Your name]  
**Date:** [Date]  
**Time Invested:** [Hours spent on analysis]  
**Next Steps:** [What happens with this document]

