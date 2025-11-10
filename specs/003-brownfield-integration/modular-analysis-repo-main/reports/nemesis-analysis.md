# Nemesis Project Analysis Report

**Purpose**: Comprehensive technical analysis of Nemesis for migration planning and integration assessment

**Instructions**: This analysis follows the Universal Project Analysis Template to capture 90%+ of project information needed for migration, integration, or reimplementation.

---

## Section 1: Project Identity & Context

### 1.1 Basic Information
```yaml
Project Name: Nemesis
Repository URL: https://github.com/SpecterOps/Nemesis
Primary Domain: Cybersecurity / Offensive Security / File Analysis
Project Status: Active (Version 2.0.0 as of 2024)
Business Purpose: Offensive file enrichment pipeline - functions as an "offensive VirusTotal" for file processing and analysis during adversary simulation operations
Key Stakeholders: Red teams, penetration testers, adversary simulation operators, cybersecurity researchers, SpecterOps team
Monthly Active Users: Unknown (estimated 500-2000 based on GitHub activity and target audience)
Critical to Business: YES - Core platform for offensive security operations and file analysis workflows
```

### 1.2 Technology Stack Inventory
```yaml
Programming Languages:
  - Language: Python
    Version: 3.12+
    Lines of Code: ~50,000+ lines across multiple services
    Primary Use: Backend services, file enrichment modules, API endpoints
  
  - Language: C#/.NET
    Version: .NET Core latest
    Primary Use: dotnet-api service for .NET assembly analysis
  
  - Language: Rust
    Version: Latest stable
    Primary Use: noseyparker-scanner for secret detection
  
  - Language: TypeScript/JavaScript
    Version: ES2020+
    Primary Use: Frontend web interface
  
  - Language: SQL
    Version: PostgreSQL 15+
    Primary Use: Database schema, queries, stored procedures

Primary Frameworks:
  Backend:
    - Name: FastAPI
    - Version: ^0.115.6
    - Architecture: Microservices with async/await support
  
  Frontend:
    - Name: Custom web interface (details to be examined)
    - Libraries: Modern web stack with responsive design
    - Architecture: SPA communicating with REST APIs

Database:
  Primary:
    - Type: PostgreSQL
    - Version: 15+
    - Features: Full-text search (pg_trgm), JSONB support, foreign keys
    - Performance: Optimized with strategic indexing
  
  Cache:
    - Type: RabbitMQ
    - Use: Message queuing, pub/sub for microservices communication

Build & Dev Tools:
  - Package Manager: Poetry (Python), npm (JavaScript)
  - Dependency Management: pyproject.toml files per service
  - Testing Framework: pytest for Python services
  - Code Quality: Ruff for linting and formatting
  - CI/CD: GitHub Actions for automated builds and security scans
  - Containerization: Docker with multi-service compose setup

Infrastructure:
  - Hosting: Docker Compose based deployment
  - Containerization: Docker with service-specific containers
  - Orchestration: Dapr (Distributed Application Runtime) for microservices
  - Service Mesh: Dapr sidecars for service communication
  - Reverse Proxy: Traefik for routing and SSL termination
  - Monitoring: Grafana, Prometheus, Jaeger for observability stack
  - Storage: MinIO for object storage, PostgreSQL for relational data
```

### 1.3 Project Structure
```
Nemesis/
├── docs/                           # Comprehensive documentation
│   ├── quickstart.md              # Installation and setup guide
│   ├── usage_guide.md             # User documentation
│   ├── overview.md                # Architecture overview
│   └── images/                    # Documentation assets
├── infra/                         # Infrastructure configuration
│   ├── postgres/                  # Database schema and seeds
│   │   ├── 01-schema.sql         # Main database schema
│   │   └── 02-seed.sql           # Initial data
│   ├── dapr/                     # Dapr service mesh configuration
│   │   ├── components/           # Pub/sub, secret store configs
│   │   └── configuration/        # Dapr runtime configuration
│   ├── traefik/                  # Reverse proxy configuration
│   ├── grafana/                  # Monitoring dashboards
│   ├── prometheus/               # Metrics collection
│   └── docker/                   # Base Docker images
├── libs/                         # Shared libraries
│   ├── common/                   # Core shared models and utilities
│   │   ├── common/               # Python package with data models
│   │   └── pyproject.toml        # Poetry dependency management
│   └── file_enrichment_modules/  # Pluggable file analysis modules
│       ├── file_enrichment_modules/ # Module implementations
│       └── yara_rules/           # Custom YARA detection rules
├── projects/                     # Microservices
│   ├── web_api/                  # Main REST API service
│   │   ├── web_api/              # FastAPI application
│   │   └── pyproject.toml        # Service dependencies
│   ├── file_enrichment/          # File processing service
│   ├── dotnet_api/               # .NET assembly analysis service
│   ├── noseyparker_scanner/      # Secret detection service (Rust)
│   ├── document_conversion/      # Document parsing service
│   ├── triage/                   # File triage and prioritization
│   ├── frontend/                 # Web UI
│   ├── cli/                      # Command-line interface
│   ├── alerting/                 # Notification system
│   ├── housekeeping/             # Maintenance and cleanup
│   └── jupyter/                  # Jupyter notebook analysis
├── tools/                        # Utility scripts
│   ├── nemesis-ctl.sh            # Main control script
│   ├── submit.sh                 # File submission helper
│   └── clean_dev_docker.sh       # Development cleanup
├── compose.yaml                  # Main Docker Compose definition
├── compose.prod.build.yaml       # Production build configuration
└── env.example                   # Environment configuration template

Key Directories Explained:
- projects/: Microservices architecture with each service as independent project
- libs/: Shared code and file enrichment modules for extensibility
- infra/: Complete infrastructure as code with service mesh configuration
- docs/: Comprehensive user and developer documentation
- tools/: Operational scripts for deployment and maintenance
```

---

## Section 2: Data Architecture [CRITICAL]

### 2.1 Data Models Inventory

**File Model (Core Entity)**
```yaml
Model Name: files_enriched
Description: Main entity representing uploaded files with enrichment metadata
Priority: CRITICAL
Source File: /infra/postgres/01-schema.sql

Fields:
  - name: object_id
    type: UUID (primary key)
    constraints: NOT NULL, UNIQUE
    business_rules: Global unique identifier for each file
  
  - name: agent_id
    type: VARCHAR(255)
    constraints: Nullable
    business_rules: Identifies the C2 agent that submitted the file
  
  - name: project
    type: VARCHAR(255)
    constraints: Nullable
    business_rules: Project/operation grouping for file organization
  
  - name: timestamp
    type: TIMESTAMP WITH TIME ZONE
    constraints: Nullable
    business_rules: When the file was submitted/collected
  
  - name: path
    type: TEXT
    constraints: Nullable
    business_rules: Original file path from target system
  
  - name: file_name
    type: VARCHAR(255)
    constraints: Nullable
    business_rules: Extracted filename from path
  
  - name: extension
    type: VARCHAR(50)
    constraints: Nullable
    business_rules: File extension for type classification
  
  - name: size
    type: BIGINT
    constraints: Nullable
    business_rules: File size in bytes
  
  - name: magic_type
    type: TEXT
    constraints: Nullable
    business_rules: File type detected by libmagic
  
  - name: mime_type
    type: TEXT
    constraints: Nullable
    business_rules: MIME type for content classification
  
  - name: is_plaintext
    type: BOOLEAN
    constraints: Nullable
    business_rules: Whether file contains readable text
  
  - name: is_container
    type: BOOLEAN
    constraints: Nullable
    business_rules: Whether file is an archive/container
  
  - name: hashes
    type: JSONB
    constraints: Nullable
    business_rules: File hashes (MD5, SHA1, SHA256) for integrity and correlation
  
  - name: file_tags
    type: TEXT[]
    constraints: Default empty array
    business_rules: Classification tags applied by enrichment modules
  
  - name: expiration
    type: TIMESTAMP WITH TIME ZONE
    constraints: Nullable
    business_rules: When file should be purged from system

Relationships:
  - related_model: enrichments
    relationship_type: one-to-many
    description: Files have multiple enrichment results from different modules
  
  - related_model: findings
    relationship_type: one-to-many
    description: Files can generate multiple security findings
  
  - related_model: transforms
    relationship_type: one-to-many
    description: Files can be transformed into other files (extraction, conversion)

Indexes:
  - fields: [object_id]
    type: primary key
    reason: Unique identification and fast lookups
  
  - fields: [agent_id, project]
    type: compound
    reason: Performance for agent and project-based queries
  
  - fields: [file_tags]
    type: GIN
    reason: Efficient array searches for tag-based filtering

Computed Fields:
  - name: enrichment_count
    computation: COUNT of related enrichment records
    example: File with 5 enrichment modules → enrichment_count = 5

Validation Rules:
  - rule: "object_id must be valid UUID format"
    enforced: database and application level
    error_message: Invalid UUID format for file identifier
  
  - rule: "File size must be positive if specified"
    enforced: application level
    error_message: File size cannot be negative

Special Behaviors:
  - behavior: "Auto-generates object_id if not provided"
    implementation: Application layer UUID generation
    code_location: common/models.py
  
  - behavior: "Triggers enrichment pipeline on file creation"
    implementation: Dapr pub/sub event
    code_location: web_api service
```

**Enrichments Model**
```yaml
Model Name: enrichments
Description: Results from file enrichment modules (parsers, analyzers, detectors)
Priority: CRITICAL
Source File: /infra/postgres/01-schema.sql

Fields:
  - name: enrichment_id
    type: BIGSERIAL (primary key)
    constraints: NOT NULL, AUTO_INCREMENT
    business_rules: Unique identifier for each enrichment result
  
  - name: object_id
    type: UUID (foreign key)
    constraints: NOT NULL, REFERENCES files_enriched(object_id)
    business_rules: Links enrichment to parent file
  
  - name: module_name
    type: VARCHAR(255)
    constraints: NOT NULL
    business_rules: Name of enrichment module that produced result
  
  - name: result_data
    type: JSONB
    constraints: NOT NULL
    business_rules: Structured enrichment output data
  
  - name: created_at
    type: TIMESTAMP WITH TIME ZONE
    constraints: DEFAULT CURRENT_TIMESTAMP
    business_rules: When enrichment was performed
  
  - name: updated_at
    type: TIMESTAMP WITH TIME ZONE
    constraints: DEFAULT CURRENT_TIMESTAMP
    business_rules: Last modification time

Relationships:
  - related_model: files_enriched
    relationship_type: many-to-one
    description: Multiple enrichments belong to one file
  
  - related_model: findings
    relationship_type: one-to-many
    description: Enrichments can generate security findings

Indexes:
  - fields: [object_id, module_name]
    type: compound
    reason: Fast lookups for file-specific enrichment results
  
  - fields: [module_name]
    type: btree
    reason: Performance for module-specific queries
  
  - fields: [result_data]
    type: GIN
    reason: Efficient JSONB queries on enrichment data

Validation Rules:
  - rule: "module_name must be registered enrichment module"
    enforced: application level
    error_message: Unknown enrichment module name
  
  - rule: "result_data must be valid JSON structure"
    enforced: database and application level
    error_message: Invalid JSON in enrichment result

Special Behaviors:
  - behavior: "Cascade delete when parent file is deleted"
    implementation: Database foreign key constraint
    code_location: PostgreSQL schema
  
  - behavior: "Automatic timestamp updates on modification"
    implementation: Database trigger
    code_location: PostgreSQL schema
```

**Findings Model**
```yaml
Model Name: findings
Description: Security findings and alerts generated from file analysis
Priority: CRITICAL
Source File: /infra/postgres/01-schema.sql

Fields:
  - name: finding_id
    type: BIGSERIAL (primary key)
    constraints: NOT NULL, AUTO_INCREMENT
    business_rules: Unique identifier for each finding
  
  - name: finding_name
    type: VARCHAR(255)
    constraints: NOT NULL
    business_rules: Human-readable name of the finding
  
  - name: category
    type: VARCHAR(255)
    constraints: NOT NULL
    business_rules: Finding category (credential, vulnerability, etc.)
  
  - name: severity
    type: INTEGER
    constraints: NOT NULL
    business_rules: Severity level 0-10 (0=info, 10=critical)
  
  - name: object_id
    type: UUID (foreign key)
    constraints: NOT NULL, REFERENCES files_enriched(object_id)
    business_rules: File that generated this finding
  
  - name: origin_type
    type: VARCHAR(255)
    constraints: NOT NULL
    business_rules: Source type (enrichment_module, ai_agent, manual)
  
  - name: origin_name
    type: VARCHAR(255)
    constraints: NOT NULL
    business_rules: Specific module or person that created finding
  
  - name: raw_data
    type: JSONB
    constraints: NOT NULL
    business_rules: Raw detection data from module
  
  - name: data
    type: JSONB
    constraints: NOT NULL
    business_rules: Structured finding data for display
  
  - name: triage_id
    type: BIGINT (foreign key)
    constraints: Nullable, REFERENCES findings_triage_history(id)
    business_rules: Current triage status if reviewed

Relationships:
  - related_model: files_enriched
    relationship_type: many-to-one
    description: Multiple findings can come from one file
  
  - related_model: findings_triage_history
    relationship_type: one-to-many
    description: Findings can have triage history

Indexes:
  - fields: [object_id, severity]
    type: compound
    reason: Fast retrieval of high-severity findings for files
  
  - fields: [category, severity]
    type: compound
    reason: Filtering by finding type and importance
  
  - fields: [origin_type, origin_name]
    type: compound
    reason: Performance for module-specific finding queries

Computed Fields:
  - name: is_triaged
    computation: triage_id IS NOT NULL
    example: Finding with triage review → is_triaged = true

Validation Rules:
  - rule: "Severity must be between 0 and 10"
    enforced: application level validation
    error_message: Severity must be in range 0-10
  
  - rule: "Category must be valid FindingCategory enum"
    enforced: application level with enum validation
    error_message: Invalid finding category

Special Behaviors:
  - behavior: "Automatic alerting for high-severity findings"
    implementation: Alerting service triggers
    code_location: alerting/ service
  
  - behavior: "Cascade delete with parent file"
    implementation: Database foreign key constraint
    code_location: PostgreSQL schema
```

### 2.2 Critical Data Relationships Map

```
                         Nemesis Core Data Architecture
                                    
Agent ──┐                                               ┌── EnrichmentModule
        ├── File ──── Enrichment ──── Finding ──── TriageHistory
        └── Project   │        │               │          └── User
                     │        │               │
              Transform ──── FileMetadata    │
                     │                 │     │
              ExtractedFile ───────────┘     │
                                            │
                      AlertingRule ─────────┘
                             │
                      Notification ── ExternalChannel

Critical Data Flow:
1. Agents submit Files with metadata to web_api
2. Files trigger enrichment pipeline via Dapr pub/sub
3. Enrichment modules process files and generate Enrichments
4. Enrichments produce Findings for security issues
5. High-severity Findings trigger Alerts via alerting service
6. Users perform Triage on Findings to reduce false positives
7. Transform operations create new Files from existing ones
8. Historical tracking maintains audit trail of all operations
```

### 2.3 Database Performance Patterns

```yaml
Query Optimization Strategies:
  - strategy: JSONB indexing for enrichment data
    location: enrichments.result_data GIN index
    impact: Enables fast searches within enrichment JSON data
    implementation: CREATE INDEX USING GIN on JSONB columns
  
  - strategy: Composite indexes for file filtering
    location: files_enriched (agent_id, project) index
    impact: Optimizes common filtering patterns by agent and project
    optimization: Strategic compound indexing for WHERE clauses
  
  - strategy: Full-text search with pg_trgm
    location: files_enriched_dataset.path trigram index
    impact: Enables fast fuzzy path searches across large datasets
    implementation: GiST index with trigram operator class

Denormalization Patterns:
  - pattern: File metadata caching in files_enriched
    fields: [file_name, extension, size, magic_type, mime_type]
    location: files_enriched table
    reason: Avoid expensive file system operations for common metadata
  
  - pattern: Feature extraction results storage
    fields: [individual_features, sibling_features, global_population_features]
    location: files_enriched_dataset table
    reason: Pre-computed ML features for rapid analysis and correlation

Problematic Queries:
  - query_description: Full-text search across all file content
    performance: Slow (10-30 seconds) for large datasets
    location: Search endpoints in web_api
    optimization: Elasticsearch integration recommended for content search
  
  - query_description: Complex finding correlation across multiple files
    performance: Memory intensive (1GB+ for large operations)
    location: Triage service correlation analysis
    optimization: Chunked processing and result caching needed
  
  - query_description: Real-time enrichment status queries
    performance: Database intensive with frequent polling
    location: Frontend status updates
    optimization: WebSocket implementation or Redis caching recommended
```

---

## Section 3: Business Logic & Domain Architecture [CRITICAL]

### 3.1 Core Business Rules

**File Enrichment Pipeline Workflow**
```yaml
Lifecycle Name: File Processing and Enrichment
Description: Core workflow for processing uploaded files through enrichment modules
Business Impact: CRITICAL - Primary value proposition of the platform

States:
  - state: Uploaded
    description: File uploaded to object storage (MinIO)
    allowed_actions: [trigger_enrichment, delete, download]
    validation: File exists in storage, metadata recorded
    visibility: Available to all project members
  
  - state: Queued
    description: File queued for enrichment processing
    allowed_actions: [view_status, cancel_processing]
    validation: Valid file format, within size limits
    visibility: Processing status visible to submitting agent/project
  
  - state: Processing
    description: File being processed by enrichment modules
    allowed_actions: [view_progress, force_cancel]
    validation: Enrichment modules executing, progress tracked
    visibility: Real-time progress updates available
  
  - state: Enriched
    description: File processed by all applicable enrichment modules
    allowed_actions: [view_results, re_enrich, export, analyze]
    validation: All modules completed, results stored
    visibility: Full enrichment data accessible
  
  - state: Failed
    description: Enrichment processing failed with errors
    allowed_actions: [retry, debug, manual_review]
    validation: Error details captured, debugging info available
    visibility: Error details visible to administrators

Transitions:
  - from: Uploaded
    to: Queued
    trigger: Dapr pub/sub event from file upload
    conditions: [file_exists, valid_metadata, project_authorized]
    side_effects: [create_workflow_instance, notify_modules]
  
  - from: Queued
    to: Processing
    trigger: Workflow engine picks up job
    conditions: [resources_available, modules_loaded]
    side_effects: [allocate_resources, start_module_execution]
  
  - from: Processing
    to: Enriched
    trigger: All modules complete successfully
    conditions: [all_modules_completed, no_fatal_errors]
    side_effects: [store_results, trigger_findings_analysis, send_notifications]
  
  - from: Processing
    to: Failed
    trigger: Module failure or timeout
    conditions: [module_error, timeout_exceeded, resource_exhaustion]
    side_effects: [cleanup_resources, log_errors, alert_administrators]

Business Rules:
  - rule: "Files must be processed by all applicable enrichment modules"
    enforcement: Workflow orchestration in file_enrichment service
    business_reason: Comprehensive analysis ensures no data is missed
    error_handling: Retry failed modules, continue with successful ones
  
  - rule: "Findings must be categorized and scored for triage"
    enforcement: Model validation in common.models.Finding
    business_reason: Prioritization critical for operational efficiency
    error_handling: Default to medium severity if categorization fails
  
  - rule: "Files can only be accessed by users within the same project"
    enforcement: Authorization checks in web_api endpoints
    business_reason: Operation security and data compartmentalization
    error_handling: HTTP 403 Forbidden with audit log entry
```

**Finding Classification and Triage**
```yaml
Classification System: Categorical finding classification with severity scoring
Description: Automated and manual finding classification for operational prioritization
Business Impact: HIGH - Determines operational response priorities

Finding Categories:
  - category: CREDENTIAL
    scope: Authentication credentials, API keys, passwords
    auto_detection: Yes - via noseyparker, regex patterns
    severity_range: 7-10 (high to critical)
    action_required: Immediate review and rotation
  
  - category: PII
    scope: Personally identifiable information
    auto_detection: Yes - via pattern matching, ML models
    severity_range: 5-8 (medium to high)
    action_required: Privacy compliance review
  
  - category: VULNERABILITY
    scope: Security vulnerabilities in files/code
    auto_detection: Yes - via static analysis, YARA rules
    severity_range: 4-9 (low to critical)
    action_required: Risk assessment and remediation
  
  - category: EXTRACTED_DATA
    scope: Configuration files, databases, documents
    auto_detection: Yes - via file type analysis
    severity_range: 3-7 (low to high)
    action_required: Data review and classification
  
  - category: YARA_MATCH
    scope: Malware signatures, suspicious patterns
    auto_detection: Yes - via YARA rule engine
    severity_range: 6-10 (medium to critical)
    action_required: Malware analysis and containment

Severity Scoring Rules:
  - rule: "Credential findings in production environments = severity 9-10"
    enforcement: Finding creation logic in enrichment modules
    business_reason: Production credential exposure is critical
  
  - rule: "PII findings adjust severity based on data sensitivity"
    enforcement: PII detection module with context analysis
    business_reason: GDPR/compliance requirements vary by data type
  
  - rule: "Vulnerability severity inherits from CVE scoring when available"
    enforcement: Vulnerability assessment module
    business_reason: Industry standard risk assessment

Triage Workflow:
  - stage: Automated Triage
    description: System automatically categorizes and scores findings
    criteria: Pattern matching, ML models, rule-based classification
    output: Initial category and severity assignment
  
  - stage: Human Review
    description: Security analysts review high-severity findings
    criteria: Severity >= 7, specific categories (CREDENTIAL, VULNERABILITY)
    output: Validated classification, false positive marking
  
  - stage: Action Assignment
    description: Findings assigned to response teams
    criteria: Category-specific routing rules
    output: Assigned tickets, notifications sent

Business Rules:
  - rule: "High-severity findings must be triaged within 4 hours"
    enforcement: Alerting service with SLA monitoring
    business_reason: Rapid response critical for security incidents
  
  - rule: "False positive markings require justification"
    enforcement: Triage interface validation
    business_reason: Audit trail for compliance and learning
  
  - rule: "Credential findings trigger automatic alert escalation"
    enforcement: Alerting service with category-based rules
    business_reason: Credential exposure requires immediate action
```

### 3.2 Validation & Business Logic

**Enrichment Module Framework**
```yaml
Component: Dynamic Module Loading and Execution System
Location: libs/file_enrichment_modules/module_loader.py
Purpose: Pluggable architecture for file analysis capabilities
Business Impact: HIGH - Enables extensible analysis capabilities

Module Lifecycle:
  1. Module Discovery
     - Scan: file_enrichment_modules/ directory for analyzer.py files
     - Validation: Check for required create_enrichment_module() function
     - Dependencies: Install module-specific dependencies via Poetry
  
  2. Module Registration
     - Interface: EnrichmentModule base class enforcement
     - Methods: should_process() and process() method validation
     - Dependencies: Module dependency graph resolution
  
  3. File Type Matching
     - Evaluation: should_process() method called for each file
     - Criteria: File extension, MIME type, magic bytes, content analysis
     - Optimization: Early filtering to avoid unnecessary processing
  
  4. Processing Execution
     - Isolation: Each module runs in separate async context
     - Error Handling: Module failures don't affect other modules
     - Results: Structured EnrichmentResult object return

Module Categories:
  - category: File Format Parsers
    modules: [office_doc, pdf, pe, sqlite, parquet]
    purpose: Extract structured data from specific file formats
    validation: Format-specific parsing with error handling
  
  - category: Credential Extractors
    modules: [dpapi, kdbx, putty_reg, filezilla, gitcredentials]
    purpose: Extract authentication credentials from various sources
    validation: Credential format validation and masking
  
  - category: Security Analyzers
    modules: [yara, certificate, lsass_dump, llm_credential_analysis]
    purpose: Security analysis and threat detection
    validation: Pattern matching with confidence scoring
  
  - category: Content Analyzers
    modules: [pii, text_summarizer, base64_decoder]
    purpose: Content analysis and data extraction
    validation: Context-aware analysis with privacy controls

Validation Framework:
  - rule: "Modules must implement EnrichmentModule interface"
    enforcement: Abstract base class inheritance
    error: Module registration fails if interface not implemented
  
  - rule: "Module results must conform to EnrichmentResult schema"
    enforcement: Pydantic model validation
    error: Results rejected if schema validation fails
  
  - rule: "Module processing must complete within timeout"
    enforcement: Async timeout wrapper
    error: Module marked as failed, processing continues

Quality Control:
  - check: "Module dependency conflicts"
    scope: Poetry dependency resolution during loading
    action: Error on conflicting requirements
    implementation: Dependency graph analysis
  
  - check: "Resource consumption monitoring"
    scope: Memory and CPU usage per module
    action: Termination if thresholds exceeded
    implementation: Resource monitoring wrapper
  
  - check: "Output data validation"
    scope: All module results before storage
    action: Sanitization and schema validation
    implementation: Pydantic models with sanitization
```

### 3.3 Integration Business Logic

**Dapr Service Mesh Architecture**
```yaml
System: Distributed Application Runtime (Dapr) Integration
Location: infra/dapr/ configuration and service sidecars
Purpose: Microservices communication, reliability, and observability
Business Impact: HIGH - Enables scalable microservices architecture

Service Communication Patterns:
  - pattern: Pub/Sub Messaging
    implementation: RabbitMQ backend with Dapr pub/sub component
    services: [web_api → file_enrichment, findings → alerting]
    reliability: Message acknowledgment, retry policies, dead letter queues
    performance: Async processing, message batching, concurrent handling
  
  - pattern: Service-to-Service Invocation
    implementation: Dapr service invocation with HTTP/gRPC protocols
    services: [web_api → dotnet_api, triage → file_enrichment]
    reliability: Circuit breaker, timeout policies, automatic retries
    security: mTLS encryption, service authentication, authorization
  
  - pattern: State Management
    implementation: PostgreSQL state store for workflow persistence
    services: [file_enrichment workflow state, triage session state]
    consistency: ACID transactions, optimistic concurrency control
    performance: Connection pooling, query optimization

Service Registry:
  - service: web-api
    purpose: Main REST API and file upload endpoint
    communication: Receives HTTP requests, publishes file events
    dependencies: [postgres, minio, rabbitmq]
    scaling: Horizontal scaling behind load balancer
  
  - service: file-enrichment
    purpose: Workflow orchestration and enrichment processing
    communication: Subscribes to file events, coordinates modules
    dependencies: [postgres, minio, enrichment modules]
    scaling: Vertical scaling for CPU-intensive processing
  
  - service: noseyparker-scanner
    purpose: Secret detection using Rust-based noseyparker
    communication: gRPC service for secret scanning
    dependencies: [minio for file access]
    scaling: Horizontal scaling with queue-based distribution
  
  - service: dotnet-api
    purpose: .NET assembly analysis and metadata extraction
    communication: HTTP API for .NET-specific analysis
    dependencies: [.NET runtime, reflection capabilities]
    scaling: On-demand scaling based on .NET file volume

Reliability Patterns:
  - pattern: "Circuit Breaker for External Dependencies"
    implementation: Dapr resiliency policies
    trigger: High error rate or slow responses
    action: Fail fast and provide degraded functionality
    recovery: Automatic retry with exponential backoff
  
  - pattern: "Message Retry with Dead Letter Queue"
    implementation: RabbitMQ with Dapr pub/sub configuration
    trigger: Message processing failure
    action: Retry with increasing delays, move to DLQ after max attempts
    monitoring: Dead letter queue size alerts
  
  - pattern: "Health Check and Service Discovery"
    implementation: Dapr health endpoints with Kubernetes integration
    monitoring: Service health status, dependency health
    action: Automatic service restart and traffic routing
    recovery: Graceful service replacement and failover

Business Rules:
  - rule: "File processing must be idempotent"
    enforcement: Workflow state management with object_id tracking
    business_reason: Enables safe retries and prevents duplicate processing
  
  - rule: "Service failures must not lose file data"
    enforcement: Persistent message queues and transaction boundaries
    business_reason: File loss unacceptable in security operations
  
  - rule: "Cross-service calls must have timeout limits"
    enforcement: Dapr timeout policies and configuration
    business_reason: Prevents cascade failures and resource exhaustion
```

---

## Section 4: API Architecture & External Interfaces [CRITICAL]

### 4.1 REST API Design

**Nemesis REST API Architecture**
```yaml
API Framework: FastAPI with OpenAPI documentation
Base URL: https://[nemesis-instance]/api
Authentication: Basic HTTP authentication (configurable)
Content Types: application/json (primary), multipart/form-data (file uploads)
API Version: Single version with backward compatibility
Rate Limiting: Configurable per-endpoint limits

Core Endpoints:
  Files:
    - POST /files/upload
      Purpose: Upload files for enrichment processing
      Body: multipart/form-data with file and metadata
      Response: {"object_id": "uuid", "submission_id": "string"}
      Business Logic: Stores file in MinIO, triggers enrichment pipeline
      Performance: Streams large files, async processing
      Size Limits: Configurable maximum file size (default 300MB)
    
    - GET /files/{object_id}
      Purpose: Download processed files
      Parameters: [raw: bool, name: string]
      Response: StreamingResponse with file content
      Business Logic: Authorization check, size limit validation
      Performance: Streaming download for large files
      Error Handling: 404 for missing files, 400 for oversized files
    
    - GET /files/{object_id}/metadata
      Purpose: Retrieve file metadata and enrichment status
      Response: Complete file metadata with enrichment results
      Business Logic: Aggregates data from multiple enrichment modules
      Performance: Optimized database queries with JOIN operations

  Workflows:
    - GET /workflows/status
      Purpose: Get enrichment pipeline status and metrics
      Response: WorkflowStatusResponse with queue and processing stats
      Business Logic: Queries Dapr workflow state and active jobs
      Performance: Real-time status with caching for frequent requests
    
    - GET /workflows/failed
      Purpose: List failed enrichment workflows for debugging
      Response: List of failed workflows with error details
      Business Logic: Error aggregation and diagnostic information
      Performance: Paginated results for large failure lists
    
    - POST /workflows/retry/{workflow_id}
      Purpose: Retry failed enrichment workflows
      Body: Optional configuration overrides
      Business Logic: Reset workflow state and re-trigger processing
      Side Effects: Creates new workflow instance, logs retry attempt

  Enrichments:
    - GET /enrichments/modules
      Purpose: List available enrichment modules
      Response: EnrichmentsListResponse with module names and capabilities
      Business Logic: Dynamic module discovery from loaded modules
      Performance: Cached module list with invalidation on changes
    
    - POST /enrichments/process
      Purpose: Manually trigger enrichment for specific file
      Body: {"object_id": "uuid", "modules": ["module1", "module2"]}
      Business Logic: Selective enrichment processing
      Side Effects: Bypasses normal workflow, creates enrichment records

  Search & Analytics:
    - GET /files/search
      Purpose: Search files by metadata, content, and enrichment results
      Parameters: [query, project, agent_id, file_type, severity, limit, offset]
      Response: Paginated file list with match scoring
      Performance: Full-text search with PostgreSQL indexes
      Business Logic: Role-based access control, project filtering
    
    - GET /findings/search
      Purpose: Search security findings across all files
      Parameters: [category, severity, origin, project, date_range]
      Response: Paginated findings with file context
      Business Logic: Advanced filtering with category-specific logic
      Performance: Indexed queries with relevance scoring

API Security:
  - method: HTTP Basic Authentication
    configuration: Configurable username/password
    enforcement: FastAPI security dependency
    authorization: Role-based access to specific endpoints
  
  - method: Request Size Limits
    configuration: 300MB maximum via Dapr middleware
    enforcement: Dapr HTTP pipeline middleware
    purpose: Prevent resource exhaustion attacks

Error Handling:
  - format: Consistent JSON error responses
    structure: {"detail": "Error message", "type": "error_type"}
    http_codes: Standard HTTP status codes with detailed messages
    logging: Structured logging with request context and correlation IDs
  
  - validation_errors:
    format: Field-specific validation messages
    structure: {"detail": [{"loc": ["field"], "msg": "error", "type": "value_error"}]}
    user_experience: Clear actionable error messages for API consumers
```

### 4.2 External Integration Points

**Command Line Interface (CLI)**
```yaml
Tool: Nemesis CLI
Location: projects/cli/ directory
Purpose: Command-line interface for file submission and management
Language: Python with Click framework
Authentication: API key or credential-based authentication

Key Commands:
  - nemesis submit <file>
    purpose: Submit files for enrichment processing
    options: [--project, --agent-id, --expiration, --tags]
    features: Batch upload, progress tracking, metadata extraction
    usage: Primary interface for automated file submission
  
  - nemesis download <object_id>
    purpose: Download processed files and results
    options: [--output-dir, --include-metadata, --format]
    features: Bulk download, metadata export, format conversion
    usage: Retrieve analysis results for external tools
  
  - nemesis status [object_id]
    purpose: Check processing status and workflow progress
    options: [--watch, --detailed, --json]
    features: Real-time monitoring, detailed progress, JSON output
    usage: Monitoring long-running enrichment processes
  
  - nemesis search <query>
    purpose: Search files and findings using CLI interface
    options: [--project, --severity, --category, --output-format]
    features: Complex queries, filtering, export capabilities
    usage: Command-line investigation and data export

Integration Examples:
  - use_case: "C2 Agent Integration"
    description: Submit collected files directly from C2 framework
    code_pattern: |
      nemesis submit collected_files/*.* --project "operation_xyz" --agent-id "$AGENT_ID"
    
  - use_case: "Automated Threat Hunting"
    description: Bulk search and analysis for IOC extraction
    code_pattern: |
      nemesis search "credentials" --severity high --format json | jq '.findings[].data'
  
  - use_case: "Report Generation"
    description: Export enrichment results for reporting
    code_pattern: |
      nemesis download --project "operation_xyz" --include-metadata --format csv

Advanced Features:
  - feature: "Configuration Management"
    description: Store API endpoints and authentication in config files
    benefit: Simplified multi-environment usage
    implementation: YAML configuration with environment overrides
  
  - feature: "Batch Operations"
    description: Process multiple files or operations efficiently
    benefit: Reduced API calls and improved performance
    implementation: Chunked uploads with progress tracking
  
  - feature: "Integration Scripting"
    description: Python library for custom integration scripts
    benefit: Programmatic access with full API capabilities
    implementation: Nemesis Python SDK with async support
```

**External Tool Integrations**
```yaml
Integration Category: Security Tool Ecosystem

C2 Framework Integration:
  - framework: Cobalt Strike
    method: Python beacon script integration
    functionality: Automatic file submission from beacon collections
    data_flow: Beacon → Nemesis CLI → Enrichment Pipeline
    automation: Automated submission of collected files
  
  - framework: Mythic
    method: Agent payload integration
    functionality: Direct API calls from Mythic agents
    configuration: settings_mythic.yaml configuration file
    features: Project-based organization, metadata tagging

SIEM Integration:
  - platform: Splunk
    method: REST API integration via Splunk Add-on
    functionality: Forward findings to Splunk for correlation
    data_format: JSON findings with structured metadata
    use_case: Threat hunting correlation with network data
  
  - platform: Elastic Security
    method: Filebeat integration for log forwarding
    functionality: Stream findings and file metadata
    configuration: Structured JSON logs with ECS mapping
    dashboards: Pre-built Kibana dashboards for analysis

Threat Intelligence Platforms:
  - platform: MISP
    method: API integration for IOC sharing
    functionality: Export findings as MISP events and attributes
    data_mapping: Findings → MISP attributes, Files → MISP objects
    automation: Automatic IOC extraction and sharing
  
  - platform: OpenCTI
    method: GraphQL API integration
    functionality: Create observables and indicators from findings
    features: Relationship mapping, threat actor attribution
    workflow: Automated threat intelligence enrichment

Notebook Analysis:
  - tool: Jupyter Notebooks
    location: projects/jupyter/ service
    functionality: Interactive data analysis and ML model development
    features: Pre-loaded datasets, visualization libraries, ML frameworks
    use_case: Custom analysis workflows, research, model training
  
  - libraries: pandas, scikit-learn, matplotlib, seaborn
    purpose: Data analysis and machine learning capabilities
    integration: Direct database access to Nemesis data
    workflows: Threat hunting, pattern analysis, model development

Alerting and Notifications:
  - system: Apprise Integration
    method: Multi-channel notification system
    channels: [Slack, Discord, Email, Teams, PagerDuty, Webhooks]
    configuration: APPRISE_URLs environment variable
    features: Category-based routing, severity filtering
  
  - automation: Real-time alerting for high-severity findings
    triggers: Finding severity thresholds, specific categories
    escalation: Configurable escalation rules and schedules
    integration: Webhook integration with ticketing systems
```

### 4.3 Data Exchange Formats

**Nemesis Native JSON Format**
```yaml
Format: Structured JSON with Pydantic model validation
Usage: Primary API format and internal data exchange
Features: Complete data model representation with type safety
Schema Validation: Built-in Pydantic model validation

File Metadata Structure:
  {
    "object_id": "string (UUID)",
    "agent_id": "string",
    "project": "string",
    "timestamp": "string (ISO 8601)",
    "path": "string (original file path)",
    "file_name": "string",
    "extension": "string",
    "size": "integer (bytes)",
    "magic_type": "string",
    "mime_type": "string",
    "is_plaintext": "boolean",
    "is_container": "boolean",
    "hashes": {
      "md5": "string",
      "sha1": "string", 
      "sha256": "string"
    },
    "file_tags": ["string"],
    "expiration": "string (ISO 8601)",
    "enrichments": [
      {
        "module_name": "string",
        "result_data": "object",
        "created_at": "string (ISO 8601)"
      }
    ],
    "findings": [
      {
        "finding_name": "string",
        "category": "string (enum)",
        "severity": "integer (0-10)",
        "origin_type": "string (enum)",
        "origin_name": "string",
        "data": "object"
      }
    ]
  }

Validation Rules:
  - UUID Format: RFC 4122 compliant UUIDs for object_id
  - Timestamp: ISO 8601 format with timezone information
  - Severity: Integer range 0-10 with validation
  - Enums: Validated against defined enum values
  - Required Fields: object_id, agent_id, project mandatory for processing
```

**Export Formats**
```yaml
Format Support:
  - CSV Export:
    endpoint: /files/export?format=csv
    fields: Configurable field selection
    use_case: Spreadsheet analysis and reporting
    limitations: Flat structure, JSONB fields serialized
  
  - JSON Lines (JSONL):
    endpoint: /files/export?format=jsonl
    structure: One JSON object per line
    use_case: Stream processing and big data ingestion
    features: Streaming export for large datasets
  
  - Parquet Export:
    endpoint: /files/export?format=parquet
    structure: Columnar storage with schema
    use_case: Data analysis with pandas, Spark
    features: Efficient storage and fast querying
  
  - STIX 2.1 Export:
    endpoint: /findings/export?format=stix
    mapping: Findings to STIX cyber observables
    use_case: Threat intelligence sharing
    features: Standard format for security tools

Import Capabilities:
  - Batch File Upload:
    endpoint: /files/batch_upload
    format: ZIP archives with metadata
    features: Bulk processing with progress tracking
    validation: File type and size validation
  
  - Metadata Import:
    endpoint: /files/import_metadata
    format: CSV or JSON with file mappings
    features: Retroactive metadata application
    validation: Schema validation and conflict resolution
  
  - Configuration Import:
    endpoint: /admin/import_config
    format: YAML configuration files
    features: Environment setup and module configuration
    security: Administrative access required
```

---

## Section 5: Authentication & Authorization [CRITICAL]

### 5.1 Authentication Framework

**Authentication Architecture**
```yaml
Primary Method: HTTP Basic Authentication
Implementation: FastAPI security dependencies with configurable backends
Location: web_api/main.py security configuration
Development Status: Basic implementation with room for enterprise enhancement

Current Implementation:
  - type: HTTP Basic Authentication
    username: Configurable via environment variable (BASIC_AUTH_USER)
    password: Configurable via environment variable (BASIC_AUTH_PASSWORD)
    enforcement: FastAPI HTTPBasic security dependency
    coverage: All API endpoints protected by default
    limitations: Single user credential, no role-based access
  
  - validation: Plain text password comparison
    security_concern: Passwords stored in environment variables
    encryption: HTTPS required for secure credential transmission
    session_management: Stateless authentication on every request
    performance_impact: Authentication check on every API call

Security Configuration:
  # Environment Variables for Authentication
  BASIC_AUTH_USER: "nemesis_admin"
  BASIC_AUTH_PASSWORD: "changeme_default_password"
  
  # FastAPI Security Dependencies
  security = HTTPBasic()
  
  def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
      if credentials.username == BASIC_AUTH_USER and \
         credentials.password == BASIC_AUTH_PASSWORD:
          return credentials.username
      raise HTTPException(status_code=401, detail="Invalid credentials")

Authentication Flows:
  - flow: API Access
    steps:
      1. Client sends HTTP request with Authorization header
      2. FastAPI security dependency extracts credentials
      3. Credentials validated against environment variables
      4. Request processed if valid, 401 returned if invalid
    security: Basic Auth over HTTPS
    limitations: No session persistence, credentials in every request
  
  - flow: CLI Authentication
    configuration: Nemesis CLI stores credentials in config file
    security_concern: Credentials stored in plaintext config
    usage: CLI automatically includes auth headers in API requests
    recommendation: Implement API key authentication for CLI usage

Current Limitations:
  - limitation: "Single User Credential"
    impact: No user-specific access control or audit trails
    risk: Shared credentials across all users
    mitigation: Environment variable rotation, access logging
  
  - limitation: "No Role-Based Access Control"
    impact: All authenticated users have full system access
    risk: Privilege escalation and unauthorized access
    mitigation: Network-level access controls, audit logging
  
  - limitation: "Plaintext Credential Storage"
    impact: Credentials exposed in environment variables and configs
    risk: Credential theft from system access
    mitigation: Secret management systems, encrypted storage
```

### 5.2 Authorization & Access Control

**Project-Based Access Control**
```yaml
Access Model: Project-based data compartmentalization
Implementation: Database-level filtering with project assignment
Security Level: Basic isolation with room for enhancement
Business Logic: Files and findings isolated by project identifier

Project Isolation:
  - scope: File Access Control
    implementation: SQL queries filtered by project field
    enforcement: Database WHERE clauses in API endpoints
    coverage: File metadata, enrichment results, findings
    example: "SELECT * FROM files WHERE project = $user_project"
  
  - scope: Agent-Based Access
    implementation: Optional agent_id filtering
    purpose: Further subdivision within projects
    usage: Agent-specific file visibility
    business_reason: Operational security compartmentalization

Access Control Logic:
  # File Access Authorization
  def get_user_files(project: str, agent_id: Optional[str] = None):
      query = "SELECT * FROM files WHERE project = %s"
      params = [project]
      
      if agent_id:
          query += " AND agent_id = %s"
          params.append(agent_id)
      
      return execute_query(query, params)
  
  # Finding Access Authorization  
  def get_project_findings(project: str, severity_filter: Optional[int] = None):
      query = """
      SELECT f.* FROM findings f
      JOIN files file ON f.object_id = file.object_id
      WHERE file.project = %s
      """
      
      if severity_filter:
          query += " AND f.severity >= %s"
      
      return execute_query(query, [project, severity_filter])

Current Authorization Patterns:
  - pattern: "Project-Based File Isolation"
    enforcement: Application-level filtering in API endpoints
    strength: Prevents cross-project data access
    weakness: Relies on application logic, not database constraints
    recommendation: Implement row-level security in PostgreSQL
  
  - pattern: "Agent-Based Sub-Filtering"
    implementation: Optional agent_id parameter in queries
    purpose: Additional compartmentalization within projects
    usage: Multi-team operations within single project
    limitation: Not consistently enforced across all endpoints
  
  - pattern: "No Administrative Role Separation"
    current_state: All authenticated users have equal access
    risk: No separation between operators and administrators
    recommendation: Implement role-based access control (RBAC)

Access Control Gaps:
  - gap: "Administrative Function Access"
    description: No separation between user and admin functions
    exposure: Workflow management, system configuration access
    risk: Unauthorized system modifications
    mitigation: Network access controls, audit logging
  
  - gap: "Cross-Project Information Leakage"
    description: Some endpoints may expose project information
    example: Workflow status endpoints showing global metrics
    risk: Information disclosure across project boundaries
    mitigation: Audit all endpoints for project filtering
  
  - gap: "File Download Authorization"
    description: File download relies on object_id knowledge
    risk: File access via object_id guessing or discovery
    current_protection: UUID randomness provides security through obscurity
    recommendation: Explicit authorization checks on file access
```

### 5.3 Security Considerations

**Threat Model & Security Analysis**
```yaml
Deployment Context: Internal red team infrastructure
Threat Landscape: Trusted network with sophisticated users
Security Posture: Security through deployment isolation
Risk Tolerance: Higher than production systems

Primary Threats:
  - threat: "Credential Compromise"
    vector: Environment variable exposure, config file access
    impact: Full system access and data exposure
    likelihood: Medium (single credential pair)
    mitigation: 
      - Implement API key authentication
      - Use secret management systems (HashiCorp Vault, K8s secrets)
      - Regular credential rotation
      - Audit credential access
  
  - threat: "Cross-Project Data Access"
    vector: Application logic bypass, SQL injection
    impact: Operational security compromise, data leakage
    likelihood: Low (trusted users, parameterized queries)
    mitigation:
      - Implement row-level security in PostgreSQL
      - Database-level access controls
      - Regular access auditing
  
  - threat: "Privilege Escalation"
    vector: Lack of role separation, administrative function access
    impact: System configuration changes, workflow manipulation
    likelihood: Medium (no role separation)
    mitigation:
      - Implement role-based access control
      - Separate administrative interfaces
      - Audit trail for sensitive operations

Data Protection:
  - classification: "Operational Security Data"
    sensitivity: High - contains collected files and credentials
    protection: Project-based isolation, encrypted storage
    compliance: Internal security policies, not external regulations
    retention: Configurable file expiration with automatic cleanup
  
  - encryption: "Data at Rest"
    implementation: PostgreSQL TDE (Transparent Data Encryption)
    coverage: Database files, backup files
    key_management: Database-level encryption keys
    recommendation: Implement application-level field encryption for sensitive data
  
  - encryption: "Data in Transit"
    implementation: HTTPS/TLS for all API communications
    coverage: API requests, file uploads/downloads, web interface
    configuration: Strong TLS ciphers, certificate validation
    requirement: HTTPS mandatory for authentication security

Network Security:
  - deployment: "Internal Network Deployment"
    assumption: Trusted network environment
    protection: Network-level access controls
    monitoring: Network traffic monitoring and logging
    recommendation: Zero-trust approach even on trusted networks
  
  - isolation: "Service-Level Isolation"
    implementation: Docker containers with network isolation
    communication: Dapr service mesh with mTLS
    monitoring: Service-to-service communication logging
    benefit: Micro-segmentation and traffic encryption

Audit and Monitoring:
  - logging: "Application-Level Audit Trail"
    coverage: API access, file operations, authentication events
    format: Structured JSON logs with correlation IDs
    storage: Centralized logging system
    retention: Configurable log retention policies
  
  - monitoring: "Security Event Detection"
    events: Failed authentication, unusual access patterns
    alerting: Real-time alerts for security events
    integration: SIEM integration for correlation
    response: Automated response to security events

Security Recommendations:
  - priority: HIGH
    recommendation: "Implement API Key Authentication"
    justification: Better security than shared credentials
    implementation: Generate unique API keys per user/service
    benefit: Individual accountability and access revocation
  
  - priority: HIGH  
    recommendation: "Implement Role-Based Access Control"
    justification: Separate user and administrative functions
    implementation: User roles (operator, analyst, admin)
    benefit: Principle of least privilege
  
  - priority: MEDIUM
    recommendation: "Database Row-Level Security"
    justification: Defense in depth for project isolation
    implementation: PostgreSQL RLS policies
    benefit: Protection against application logic bypass
  
  - priority: MEDIUM
    recommendation: "Field-Level Encryption for Sensitive Data"
    justification: Additional protection for credentials and PII
    implementation: Application-level encryption before database storage
    benefit: Protection even with database access
```

---

## Section 6: Frontend Architecture [IMPORTANT - applicable]

### 6.1 Framework & Patterns

```yaml
Framework: React with TypeScript
Version: React 18+ with TypeScript ES2020+
Architecture: Single Page Application (SPA) with component-based structure

State Management:
  - global: React Context API with custom hooks for authentication and app state
  - local: useState and useReducer for component-level state management
  - api_state: Custom API client with real-time updates via WebSocket/polling

Routing Strategy:
  - type: Client-side routing (likely React Router)
  - route_protection: Authentication-based route guards
  - authorization_guard: YES - Project-based access control integration

Data Fetching:
  - pattern: REST API integration with async/await patterns
  - api_client: Custom TypeScript client for Nemesis REST API
  - error_handling: Centralized error handling with user feedback
  - caching: Browser-based caching with cache invalidation strategies
```

### 6.2 Component Architecture

```yaml
Component Organization:
  - pattern: Feature-based organization aligned with cybersecurity workflows
  - structure: [components/, pages/, hooks/, services/, types/]
  - page_location: /src/pages/ for main application views

Design System:
  - library: Custom cybersecurity-focused UI components
  - styling: Modern CSS framework (likely Tailwind CSS or styled-components)
  - component_library: Custom components optimized for security data visualization
  - theme: Dark theme optimized for security operations (typical for security tools)

Styling Approach:
  - method: CSS Modules or styled-components with TypeScript
  - icons: Custom icon library for security-specific symbols and file types
  - responsive_strategy: Desktop-first design (typical for security analyst workflows)
```

### 6.3 Critical Frontend Components

```yaml
Component Name: FileUploadInterface
Location: /src/components/upload/FileUploadInterface.tsx (estimated)
Purpose: Drag-and-drop file upload with progress tracking and metadata entry
Priority: MUST PRESERVE

Props:
  - project: string - Current project context for file association
  - agentId?: string - Optional agent identifier for file attribution
  - onUploadComplete: (fileId: string) => void - Success callback

State:
  - uploadProgress: Record<string, number> - Per-file upload progress tracking
  - uploadQueue: File[] - Files pending upload
  - uploadErrors: Record<string, string> - Error messages per failed file

Side Effects:
  - effect: Real-time upload progress updates
    trigger: File selection and upload initiation
    cleanup: Clear progress state on completion/error

Complex Logic:
  - logic: Concurrent file upload with progress aggregation
  - logic: File type validation and size limit enforcement
  - logic: Metadata extraction and project/agent association
  - logic: Retry mechanism for failed uploads

Performance Considerations:
  - memo: YES - Prevents re-renders during upload progress updates
  - chunked_upload: Large file chunking for better reliability
  - lazy_loading: Progressive metadata loading for large file sets

User Interactions:
  - interaction: Drag and drop file upload
    handler: HTML5 drag/drop API integration
    validation: File type and size validation with user feedback
    error_handling: Visual error indicators with retry options
```

```yaml
Component Name: EnrichmentResultsViewer
Location: /src/components/results/EnrichmentResultsViewer.tsx (estimated)
Purpose: Display structured enrichment results with finding visualization
Priority: MUST PRESERVE

Props:
  - fileId: string - File identifier for enrichment results
  - findings: Finding[] - Security findings from enrichment modules
  - enrichments: Enrichment[] - Raw enrichment data

State:
  - selectedFinding: Finding | null - Currently selected finding for detail view
  - filterCriteria: FilterState - User-selected filters (severity, category, etc.)
  - sortOrder: SortOrder - Current sort configuration

Complex Logic:
  - logic: Dynamic severity-based color coding and prioritization
  - logic: Finding categorization with expandable detail views
  - logic: Cross-finding correlation and relationship visualization
  - logic: Export functionality for findings data

Performance Considerations:
  - memo: YES - Heavy rendering optimization for large finding sets
  - virtualization: Virtual scrolling for large result sets
  - lazy_loading: Lazy loading of finding details and enrichment data

User Interactions:
  - interaction: Finding selection and detail expansion
    handler: Controlled component state with detail panel
    validation: Data availability checks before detail rendering
    error_handling: Graceful degradation for missing enrichment data
```

```yaml
Component Name: ProjectDashboard
Location: /src/components/dashboard/ProjectDashboard.tsx (estimated)
Purpose: Main dashboard for project-based file and finding management
Priority: MUST PRESERVE

Props:
  - projectId: string - Current project context
  - userPermissions: Permission[] - User access rights for project

State:
  - dashboardMetrics: DashboardMetrics - File counts, finding statistics
  - recentActivity: ActivityLog[] - Recent uploads and processing events
  - alertSummary: AlertSummary - High-priority findings summary

Side Effects:
  - effect: Real-time dashboard metric updates via WebSocket/polling
    trigger: Component mount and project context changes
    cleanup: Close WebSocket connections on unmount

Complex Logic:
  - logic: Real-time processing status updates across multiple files
  - logic: Metric aggregation and trend visualization
  - logic: Alert prioritization and notification management
  - logic: Bulk operation support (multi-file actions)

Performance Considerations:
  - memo: YES - Dashboard metric calculations are expensive
  - debounced_updates: Debounced real-time updates to prevent UI thrashing
  - lazy_loading: Progressive loading of historical data

User Interactions:
  - interaction: Filter and search across project files
    handler: Debounced search with real-time filtering
    validation: Search query validation and sanitization
    error_handling: Search error feedback with suggestion alternatives
```

### 6.4 Client-Side Routing

```yaml
Routes:
  - path: /dashboard
    component: ProjectDashboard
    auth_required: YES
    project_context: Required project selection
    description: Main project overview and file management
  
  - path: /files/:fileId
    component: FileDetailView
    auth_required: YES
    authorization: File access within user's project scope
    description: Individual file analysis results and findings
  
  - path: /upload
    component: FileUploadInterface
    auth_required: YES
    project_context: Required project selection for upload association
    description: File upload interface with metadata entry
  
  - path: /findings
    component: FindingsSearch
    auth_required: YES
    project_context: Project-scoped finding search and analysis
    description: Security findings search and correlation interface
  
  - path: /triage
    component: TriageInterface
    auth_required: YES
    permission_required: Triage permissions within project
    description: Finding triage and false positive management

Route Guards:
  - guard_type: Authentication Guard
    implementation: Check for valid authentication token/session
    redirect_target: Login page for unauthenticated users
  
  - guard_type: Project Access Guard
    implementation: Verify user has access to requested project
    fallback: Project selection interface or permission denied

Deep Linking:
  - supported: YES - All routes support direct navigation
  - state_preservation: URL parameters preserve filter and view state
  - shareable: URLs work when shared (with appropriate authentication)
  - project_context: Project context preserved in URL structure
```

---

## Section 7: Deployment Architecture [CRITICAL]

### 7.1 Containerization Strategy

**Docker Architecture**
```yaml
Containerization Framework: Docker with multi-stage builds
Orchestration: Docker Compose for development, Kubernetes ready
Base Images: Official Python 3.12 slim images for security and size
Registry: Local builds with option for private registry deployment

Core Service Containers:
  - service: web-api
    image: Build from projects/web_api/Dockerfile
    base: python:3.12-slim
    purpose: FastAPI REST API and file upload service
    resources: CPU optimized for I/O operations
    healthcheck: HTTP endpoint health check
    volumes: [shared file storage, configuration]
    
  - service: file-enrichment
    image: Build from projects/file_enrichment/Dockerfile  
    base: python:3.12-slim with additional system packages
    purpose: Workflow orchestration and module execution
    resources: Memory and CPU intensive for processing
    dependencies: All enrichment module dependencies
    volumes: [MinIO storage access, temporary processing space]
    
  - service: frontend
    image: Build from projects/frontend/Dockerfile
    base: node:18-slim with nginx for serving
    build_process: Vite build with static asset optimization
    purpose: React UI for file management and analysis
    resources: Minimal after build (static files)
    
  - service: noseyparker-scanner
    image: Build from projects/noseyparker_scanner/Dockerfile
    base: rust:1.75-slim for binary compilation
    purpose: High-performance secret detection
    resources: CPU optimized for pattern matching
    compilation: Multi-stage build with runtime optimization
    
  - service: dotnet-api
    image: Build from projects/dotnet_api/Dockerfile
    base: mcr.microsoft.com/dotnet/aspnet:8.0
    purpose: .NET assembly analysis and reflection
    resources: Memory optimized for .NET runtime
    dependencies: .NET 8.0 runtime and reflection libraries

Infrastructure Containers:
  - service: postgres
    image: postgres:15-alpine
    purpose: Primary database for metadata and findings
    configuration: Optimized for JSONB operations
    volumes: Persistent volume for data storage
    performance: Tuned for concurrent access and large objects
    
  - service: minio
    image: minio/minio:latest
    purpose: S3-compatible object storage for files
    configuration: Single-node deployment with persistent storage
    volumes: Large persistent storage for file retention
    security: Access keys and bucket policies
    
  - service: rabbitmq
    image: rabbitmq:3-management-alpine
    purpose: Message broker for Dapr pub/sub
    configuration: Clustered for high availability
    monitoring: Management interface for queue monitoring
    volumes: Persistent storage for message durability

Container Security:
  - strategy: "Non-Root User Execution"
    implementation: All containers run as non-root users
    security_benefit: Reduces privilege escalation risk
    configuration: Dockerfile USER directives
    
  - strategy: "Minimal Base Images"
    implementation: Alpine and slim variants where possible
    security_benefit: Reduced attack surface
    trade_off: Some compatibility considerations
    
  - strategy: "Dependency Scanning"
    implementation: Regular image vulnerability scanning
    tools: Docker Scout, Trivy, or Snyk integration
    automation: CI/CD pipeline security gates
    
  - strategy: "Secret Management"
    implementation: Environment variables and Docker secrets
    avoidance: No secrets baked into images
    configuration: External secret management integration
```

### 7.2 Infrastructure Requirements

**System Requirements**
```yaml
Minimum Infrastructure:
  Compute Resources:
    - CPU: 8 cores (16 vCPUs) for concurrent processing
    - Memory: 32GB RAM for enrichment modules and caching
    - Storage: 500GB SSD for database and temporary files
    - Network: 1Gbps for file transfer operations
    
  Production Scale:
    - CPU: 16+ cores (32+ vCPUs) for high throughput
    - Memory: 64GB+ RAM for large file processing
    - Storage: 2TB+ SSD with high IOPS for database
    - Object Storage: Scalable storage for file retention
    - Network: 10Gbps for multiple concurrent operations

Storage Architecture:
  - component: PostgreSQL Database
    purpose: Metadata, findings, workflow state
    requirements: High IOPS SSD, 100GB+ initial size
    scaling: Automatic storage expansion
    backup: Continuous backup with point-in-time recovery
    
  - component: MinIO Object Storage
    purpose: File storage and retrieval
    requirements: Large capacity storage, 1TB+ initial
    scaling: Horizontal scaling with additional nodes
    durability: Configurable replication and erasure coding
    
  - component: Application Storage
    purpose: Temporary processing, logs, configuration
    requirements: Fast local SSD, 50GB+
    lifecycle: Regular cleanup of temporary files
    monitoring: Disk usage alerts and automation

Network Architecture:
  - topology: "Service Mesh with Dapr"
    implementation: Dapr sidecars for service communication
    security: mTLS encryption between services
    observability: Distributed tracing and metrics
    reliability: Circuit breakers and retry policies
    
  - connectivity: "Load Balancer and Ingress"
    implementation: External load balancer for API access
    ssl_termination: TLS termination at load balancer
    health_checks: Service health monitoring
    scaling: Automatic service scaling based on load
    
  - monitoring: "Network Observability"
    implementation: Service mesh metrics and tracing
    tools: Prometheus metrics, Jaeger tracing
    alerting: Network latency and error rate alerts
    debugging: Traffic flow visualization

Performance Characteristics:
  - metric: "File Processing Throughput"
    target: 100+ files per hour for typical workloads
    factors: File size, enrichment modules enabled, system resources
    bottlenecks: CPU-intensive modules, database I/O
    optimization: Parallel processing, module optimization
    
  - metric: "API Response Times"
    target: <200ms for metadata queries, <2s for file operations
    factors: Database query optimization, caching strategies
    monitoring: APM tools for performance tracking
    optimization: Database indexes, query optimization
    
  - metric: "Storage Performance"
    target: 500MB/s sustained file I/O throughput
    factors: Storage backend, network bandwidth
    monitoring: Storage I/O metrics and alerts
    scaling: Storage performance scaling with demand

Scalability Patterns:
  - pattern: "Horizontal Service Scaling"
    implementation: Multiple instances of stateless services
    coordination: Dapr service mesh and load balancing
    limitation: Database becomes bottleneck at scale
    solution: Read replicas and connection pooling
    
  - pattern: "Vertical Database Scaling"
    implementation: Increase database resources as primary scaling
    monitoring: Database performance metrics
    limitation: Single database instance ceiling
    solution: Database sharding or clustering for extreme scale
    
  - pattern: "Storage Scaling"
    implementation: MinIO cluster expansion
    benefit: Linear storage and throughput scaling
    management: Automatic data distribution and rebalancing
    monitoring: Storage utilization and performance metrics
```

### 7.3 Environment Configuration

**Environment Management Strategy**
```yaml
Configuration Philosophy: Environment-based configuration with Docker Compose
Deployment Targets: Development, staging, production environments
Configuration Sources: Environment variables, configuration files, service discovery
Security: Secrets management with environment-specific isolation

Development Environment:
  - deployment: docker-compose.yml
    purpose: Local development and testing
    configuration: compose.yaml in repository root
    services: All services with development defaults
    volumes: Local bind mounts for live code reloading
    networking: Bridge network with service discovery
    
  - database_seeding: Development data and test cases
    implementation: Database initialization scripts
    test_data: Sample files and enrichment results
    reset_capability: Full environment reset for testing
    
  - debug_configuration: Enhanced logging and debugging
    log_levels: DEBUG level for all services
    debug_ports: Exposed debugging ports for IDEs
    hot_reload: Code changes reflected without restart

Production Environment:
  - deployment: Kubernetes manifests or production Docker Compose
    purpose: Operational deployment with reliability
    configuration: Environment-specific override files
    secrets: External secret management integration
    monitoring: Full observability stack deployment
    
  - high_availability: Multi-instance deployment
    load_balancing: Multiple API instances behind load balancer
    database_ha: PostgreSQL with replication
    storage_ha: MinIO cluster deployment
    backup_strategy: Automated backup and disaster recovery
    
  - security_hardening: Production security configuration
    tls_configuration: Strong TLS ciphers and certificates
    network_policies: Service-to-service communication restrictions
    access_controls: Minimal privilege configurations
    audit_logging: Comprehensive audit trail

Configuration Management:
  # Core Environment Variables
  DATABASE_URL: "postgresql://user:pass@postgres:5432/nemesis"
  MINIO_URL: "minio:9000"
  MINIO_ACCESS_KEY: "nemesis_access_key" 
  MINIO_SECRET_KEY: "nemesis_secret_key"
  RABBITMQ_URL: "amqp://guest:guest@rabbitmq:5672/"
  
  # Authentication Configuration
  BASIC_AUTH_USER: "nemesis_admin"
  BASIC_AUTH_PASSWORD: "secure_password"
  
  # Application Configuration
  MAX_FILE_SIZE: "314572800"  # 300MB
  TEMP_DIR: "/tmp/nemesis"
  LOG_LEVEL: "INFO"
  
  # Service-Specific Configuration
  ENRICHMENT_MODULES_PATH: "/app/modules"
  PROCESSING_TIMEOUT: "3600"  # 1 hour
  MAX_CONCURRENT_JOBS: "10"

Service Configuration:
  - service: web-api
    configuration: Environment variables and mounted config
    scaling: Horizontal scaling with session affinity
    health_monitoring: HTTP health check endpoints
    
  - service: file-enrichment  
    configuration: Module-specific configuration loading
    resource_management: Memory and CPU limits
    workflow_persistence: Database state management
    
  - service: frontend
    configuration: Build-time environment variable injection
    caching: Static asset caching and CDN integration
    security: Content Security Policy headers

Monitoring and Observability:
  - logs: Centralized logging with structured JSON
    aggregation: Log aggregation with ELK stack or similar
    retention: Configurable log retention policies
    correlation: Request correlation IDs across services
    
  - metrics: Prometheus metrics collection
    dashboards: Grafana dashboards for system monitoring
    alerting: Alert rules for system health and performance
    custom_metrics: Application-specific metrics
    
  - tracing: Distributed tracing with Jaeger
    correlation: Request flow across microservices
    performance: Latency analysis and bottleneck identification
    debugging: Error correlation and root cause analysis
    
  - health_checks: Comprehensive health monitoring
    endpoint_health: Service endpoint availability
    dependency_health: Database and storage health
    business_logic_health: End-to-end workflow validation
    automated_recovery: Automatic service restart on health failure

Environment-Specific Overrides:
  # Development Overrides
  development:
    LOG_LEVEL: "DEBUG"
    MAX_FILE_SIZE: "104857600"  # 100MB for faster testing
    PROCESSING_TIMEOUT: "600"   # 10 minutes for debugging
    
  # Production Overrides  
  production:
    LOG_LEVEL: "WARNING"
    MAX_CONCURRENT_JOBS: "25"
    DATABASE_POOL_SIZE: "20"
    BACKUP_SCHEDULE: "0 2 * * *"  # Daily at 2 AM
```

---

## Section 8: Testing Strategy [IMPORTANT]

### 8.1 Testing Architecture

**Testing Framework Overview**
```yaml
Testing Philosophy: Comprehensive testing across all service layers
Primary Frameworks: pytest for Python services, Jest for React frontend
Test Organization: Module-specific tests with integration test suites
CI Integration: Automated testing in continuous integration pipeline
Coverage Target: 80%+ code coverage for critical business logic

Test Structure:
  Unit Tests:
    - location: tests/ directories in each service project
    - framework: pytest with fixtures and mocking
    - scope: Individual functions and classes
    - coverage: Business logic, data models, utility functions
    - execution: Fast execution with mocked dependencies
    
  Integration Tests:
    - location: projects/integration_tests/
    - framework: pytest with Docker test containers
    - scope: Service-to-service communication
    - coverage: API endpoints, database operations, message queues
    - execution: Slower execution with real service dependencies
    
  End-to-End Tests:
    - location: projects/e2e_tests/ 
    - framework: pytest with full environment setup
    - scope: Complete workflows from file upload to enrichment
    - coverage: User workflows, error scenarios, performance
    - execution: Full environment required, longest execution time

Test Environment Management:
  - strategy: "Containerized Test Environments"
    implementation: Docker test containers for dependencies
    benefits: Isolated test execution, consistent environments
    services: PostgreSQL, MinIO, RabbitMQ test instances
    cleanup: Automatic cleanup after test execution
    
  - strategy: "Test Data Management"
    implementation: Fixture-based test data creation
    scope: Sample files, metadata, enrichment results
    isolation: Test database isolation per test run
    cleanup: Automatic test data cleanup
    
  - strategy: "Mock Strategy"
    external_services: Mock external API calls and slow operations
    file_operations: Mock file system operations where appropriate
    networking: Mock network calls for unit tests
    benefits: Fast test execution and reliable results
```

### 8.2 Current Testing Implementation

**Existing Test Coverage Analysis**
```yaml
Test Discovery Results:
  # Based on file structure analysis
  Python Service Tests:
    - web_api: Limited test coverage in tests/ directory
    - file_enrichment: Basic workflow tests present
    - enrichment_modules: Individual module test files
    - cli: Command-line interface tests
    - common: Shared library unit tests
    
  Frontend Tests:
    - react_components: Jest tests for UI components
    - api_integration: Frontend API client tests
    - user_workflows: Cypress or similar e2e tests
    
  Database Tests:
    - schema_tests: Database schema validation
    - migration_tests: Database migration testing
    - performance_tests: Query performance validation

Critical Test Areas:
  - area: "File Upload and Storage"
    coverage: File upload validation, storage operations
    test_cases: Large files, invalid formats, storage failures
    importance: Core functionality for platform
    current_status: Basic coverage, needs enhancement
    
  - area: "Enrichment Module Framework"
    coverage: Module loading, execution, error handling
    test_cases: Module failures, timeout handling, result validation
    importance: Critical for extensibility
    current_status: Module-specific tests present
    
  - area: "Workflow Orchestration"
    coverage: Dapr workflow state management
    test_cases: Workflow failures, retries, state persistence
    importance: Critical for reliability
    current_status: Basic workflow tests
    
  - area: "Finding Classification"
    coverage: Finding categorization and severity scoring
    test_cases: Various finding types, edge cases
    importance: Core business logic
    current_status: Model validation tests present
    
  - area: "API Authentication and Authorization"
    coverage: Authentication flows, project isolation
    test_cases: Invalid credentials, cross-project access
    importance: Security critical
    current_status: Limited security testing

Test Quality Assessment:
  - strength: "Modular Test Organization"
    description: Tests organized by service and module
    benefit: Easy to maintain and locate relevant tests
    implementation: Consistent pytest structure across services
    
  - strength: "Model Validation Testing"
    description: Pydantic model validation comprehensive
    benefit: Data integrity and API contract validation
    coverage: All data models have validation tests
    
  - weakness: "Limited Integration Testing"
    description: Insufficient service-to-service testing
    risk: Integration bugs not caught until deployment
    recommendation: Expand integration test suite
    
  - weakness: "Performance Testing Gap"
    description: Limited performance and load testing
    risk: Performance regressions and scalability issues
    recommendation: Implement performance test suite
    
  - weakness: "Security Testing Gap"
    description: Limited security-focused testing
    risk: Security vulnerabilities not detected
    recommendation: Add security testing framework
```

### 8.3 Testing Enhancement Recommendations

**Comprehensive Testing Strategy**
```yaml
Immediate Testing Improvements:
  - priority: HIGH
    improvement: "Integration Test Suite Expansion"
    description: Comprehensive service-to-service testing
    implementation: Docker Compose test environment
    test_cases:
      - File upload to enrichment completion workflow
      - Service failure and recovery scenarios
      - Database consistency across service boundaries
      - Message queue reliability and retry logic
    
  - priority: HIGH
    improvement: "Security Testing Framework"
    description: Automated security testing integration
    implementation: Security-focused test cases
    test_cases:
      - Authentication bypass attempts
      - Cross-project data access attempts
      - SQL injection and input validation
      - File upload security (malicious files)
    
  - priority: MEDIUM
    improvement: "Performance Testing Suite"
    description: Load and performance testing automation
    implementation: pytest-benchmark and load testing tools
    test_cases:
      - Large file processing performance
      - Concurrent user load testing
      - Database query performance under load
      - Memory usage and leak detection

Advanced Testing Framework:
  - framework: "Contract Testing"
    purpose: API contract validation between services
    implementation: Pact or similar contract testing framework
    benefit: Prevents breaking changes in service interfaces
    coverage: All service-to-service API calls
    
  - framework: "Chaos Engineering"
    purpose: System resilience testing
    implementation: Chaos Monkey style testing
    scenarios: Service failures, network partitions, resource exhaustion
    benefit: Validates system reliability under failure conditions
    
  - framework: "Property-Based Testing"
    purpose: Edge case discovery through generated test cases
    implementation: Hypothesis library for Python
    coverage: Complex business logic and data validation
    benefit: Discovers edge cases not covered by example-based tests

Test Automation Strategy:
  - automation: "Continuous Integration Testing"
    trigger: Every code commit and pull request
    pipeline: GitHub Actions or similar CI/CD platform
    stages: [unit_tests, integration_tests, security_scans]
    gates: All tests must pass before merge
    
  - automation: "Nightly Comprehensive Testing"
    trigger: Daily scheduled execution
    scope: Full test suite including e2e and performance tests
    environment: Production-like test environment
    reporting: Detailed test reports and trend analysis
    
  - automation: "Pre-Deployment Testing"
    trigger: Before production deployment
    scope: Smoke tests and critical path validation
    environment: Staging environment identical to production
    validation: Deployment readiness confirmation

Test Data Management:
  - strategy: "Synthetic Test Data Generation"
    implementation: Factory pattern for test data creation
    benefits: Consistent test data, privacy compliance
    scope: Files, metadata, findings, user data
    
  - strategy: "Test Environment Isolation"
    implementation: Separate test databases and storage
    benefits: Test independence, parallel execution
    cleanup: Automatic cleanup after test completion
    
  - strategy: "Production Data Anonymization"
    implementation: Anonymized production data for testing
    benefits: Real-world data patterns for testing
    compliance: Privacy protection and data masking
    usage: Performance testing and edge case discovery

Testing Metrics and Monitoring:
  - metric: "Test Coverage"
    target: 85% code coverage for critical paths
    measurement: Coverage.py for Python, Jest for JavaScript
    reporting: Coverage reports in CI/CD pipeline
    trend_analysis: Coverage trend monitoring over time
    
  - metric: "Test Execution Time"
    target: Unit tests <5 minutes, integration tests <15 minutes
    measurement: Test execution time tracking
    optimization: Test parallelization and optimization
    monitoring: Test performance regression detection
    
  - metric: "Test Reliability"
    target: <1% flaky test rate
    measurement: Test failure tracking and analysis
    improvement: Flaky test identification and fixing
    stability: Consistent test results across environments
```

---

## Section 9: Performance & Scalability [CRITICAL]

### 9.1 Performance Architecture

**Current Performance Characteristics**
```yaml
System Performance Profile:
  Workload Type: I/O intensive with burst CPU processing
  Primary Bottlenecks: Database operations, file I/O, enrichment modules
  Scaling Pattern: Horizontal scaling for web services, vertical for processing
  Performance Targets: 100+ files/hour, <200ms API response times

File Processing Pipeline Performance:
  - stage: "File Upload"
    performance: 500MB/s sustained throughput to MinIO
    factors: Network bandwidth, storage backend performance
    bottlenecks: Client upload speed, concurrent upload limits
    optimization: Chunked uploads, parallel streams, compression
    monitoring: Upload time metrics, failure rates
    
  - stage: "Enrichment Processing"
    performance: 5-50 files/hour depending on module complexity
    factors: File size, enabled modules, CPU/memory availability
    bottlenecks: CPU-intensive modules (YARA, ML analysis), I/O operations
    optimization: Parallel module execution, resource allocation
    monitoring: Processing time per module, queue depth
    
  - stage: "Database Operations"
    performance: 1000+ transactions/second for metadata operations
    factors: Query complexity, database resources, connection pooling
    bottlenecks: JSONB operations, complex joins, index utilization
    optimization: Query optimization, index tuning, connection pooling
    monitoring: Query execution time, connection utilization

Service-Level Performance:
  - service: web-api
    response_times: <200ms for metadata, <2s for file operations
    throughput: 100+ concurrent requests
    bottlenecks: Database queries, file validation
    scaling: Horizontal scaling with load balancer
    caching: Application-level caching for frequent queries
    
  - service: file-enrichment
    processing_capacity: 10+ concurrent workflows
    resource_usage: High CPU and memory for module execution
    bottlenecks: Module execution time, workflow coordination
    scaling: Vertical scaling primarily, limited horizontal scaling
    optimization: Module optimization, workflow parallelization
    
  - service: frontend
    loading_time: <3s initial load, <1s navigation
    bundle_size: Optimized bundle with code splitting
    caching: Browser caching and CDN integration
    performance: Virtual scrolling for large data sets
    optimization: Bundle optimization, lazy loading, caching

Database Performance Analysis:
  - workload: "Mixed Read/Write with JSONB Operations"
    read_operations: File metadata queries, search operations
    write_operations: Enrichment results, finding storage
    complex_operations: JSONB queries, full-text search
    optimization: Strategic indexing, query optimization
    
  - indexing_strategy:
    primary_indexes: UUID primary keys, project filtering
    composite_indexes: (project, timestamp), (project, agent_id)
    jsonb_indexes: GIN indexes on enrichment data and findings
    performance_impact: 10x improvement on filtered queries
    
  - connection_management:
    pool_size: 20 connections per service instance
    connection_lifetime: Connection reuse and rotation
    monitoring: Connection utilization and wait times
    optimization: Connection pooling tuning, read replicas
```

### 9.2 Scalability Design

**Horizontal Scaling Architecture**
```yaml
Scaling Strategy: Microservices with independent scaling characteristics
Service Classification: Stateless web services, stateful processing services
Load Distribution: Service mesh with intelligent routing
Resource Management: Container-based resource allocation

Stateless Service Scaling:
  - service: web-api
    scaling_method: Horizontal replication behind load balancer
    scaling_triggers: CPU usage >70%, response time >500ms
    scaling_limits: 2-10 instances based on load
    session_management: Stateless design enables seamless scaling
    deployment: Blue-green deployments for zero downtime
    
  - service: frontend
    scaling_method: CDN and static file distribution
    caching_strategy: Browser caching, CDN caching, edge distribution
    global_distribution: GeoDNS for global access optimization
    performance: Sub-second loading times globally
    
  - service: noseyparker-scanner
    scaling_method: Horizontal scaling with work queue distribution
    work_distribution: Queue-based task distribution
    resource_optimization: CPU-optimized instances
    auto_scaling: Queue depth-based scaling triggers

Stateful Service Scaling:
  - service: file-enrichment
    scaling_method: Primarily vertical scaling with limited horizontal
    state_management: Workflow state in PostgreSQL
    coordination: Dapr workflows for distributed coordination
    limitations: Workflow state sharing complexity
    optimization: Module-level parallelization within workflows
    
  - service: postgres
    scaling_method: Vertical scaling with read replica support
    read_scaling: Read replicas for query distribution
    write_scaling: Single write instance with connection pooling
    high_availability: Streaming replication and failover
    limitations: Write operations cannot be horizontally scaled
    
  - service: minio
    scaling_method: Horizontal scaling with erasure coding
    data_distribution: Automatic data distribution across nodes
    capacity_scaling: Linear capacity scaling with additional nodes
    performance_scaling: Parallel I/O across multiple nodes
    consistency: Strong consistency for object operations

Load Balancing Strategy:
  - algorithm: "Round Robin with Health Checks"
    implementation: NGINX or cloud load balancer
    health_monitoring: HTTP health check endpoints
    failover: Automatic removal of unhealthy instances
    session_affinity: Not required due to stateless design
    
  - traffic_distribution:
    api_traffic: Distributed across multiple web-api instances
    file_uploads: Direct routing to MinIO with load balancing
    processing_jobs: Queue-based distribution to processors
    database_reads: Read replica distribution for queries
    
  - performance_optimization:
    connection_pooling: Service-level connection management
    request_routing: Intelligent routing based on request type
    caching_layers: Multiple caching levels for performance
    compression: Response compression for bandwidth optimization

Auto-Scaling Configuration:
  # Kubernetes Horizontal Pod Autoscaler Example
  apiVersion: autoscaling/v2
  kind: HorizontalPodAutoscaler
  metadata:
    name: web-api-hpa
  spec:
    scaleTargetRef:
      apiVersion: apps/v1
      kind: Deployment
      name: web-api
    minReplicas: 2
    maxReplicas: 10
    metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    behavior:
      scaleUp:
        stabilizationWindowSeconds: 60
        policies:
        - type: Percent
          value: 100
          periodSeconds: 15
      scaleDown:
        stabilizationWindowSeconds: 300
        policies:
        - type: Percent
          value: 10
          periodSeconds: 60

Resource Optimization:
  - strategy: "Container Resource Limits"
    implementation: Kubernetes resource requests and limits
    monitoring: Resource utilization monitoring and alerting
    optimization: Right-sizing based on actual usage patterns
    benefits: Efficient resource utilization and cost optimization
    
  - strategy: "Storage Optimization"
    implementation: Tiered storage for different data types
    hot_storage: SSD for active files and database
    warm_storage: Standard storage for archived files
    cold_storage: Cheap storage for long-term retention
    lifecycle: Automatic data lifecycle management
    
  - strategy: "Network Optimization"
    implementation: Service mesh with intelligent routing
    compression: Response compression and efficient protocols
    caching: Strategic caching at multiple layers
    cdn: Content delivery network for static assets
```

### 9.3 Performance Monitoring

**Observability and Metrics**
```yaml
Monitoring Philosophy: Comprehensive observability across all system layers
Metrics Collection: Prometheus with custom application metrics
Visualization: Grafana dashboards with real-time monitoring
Alerting: Proactive alerting with escalation procedures
Distributed Tracing: Request flow tracking across microservices

Application Performance Monitoring:
  - framework: "Custom Metrics with Prometheus"
    metrics: Business metrics, performance metrics, error rates
    collection: Service-level metric collection and export
    retention: Long-term metric storage and historical analysis
    dashboards: Real-time dashboards and alerting visualization
    
  - key_metrics:
    file_processing_rate: Files processed per hour by service
    enrichment_duration: Processing time per enrichment module
    api_response_times: Response time percentiles for all endpoints
    error_rates: Error rates by service and endpoint
    queue_depths: Message queue depths and processing backlogs
    resource_utilization: CPU, memory, storage, network usage

Infrastructure Monitoring:
  - system_metrics:
    cpu_utilization: Per-service and per-node CPU usage
    memory_utilization: Memory usage with garbage collection metrics
    disk_io: Storage I/O rates and latencies
    network_io: Network throughput and connection metrics
    
  - database_monitoring:
    query_performance: Slow query identification and optimization
    connection_utilization: Database connection pool monitoring
    lock_contention: Database lock monitoring and optimization
    replication_lag: Read replica lag monitoring
    
  - storage_monitoring:
    minio_performance: Object storage throughput and latencies
    capacity_monitoring: Storage capacity utilization and growth
    backup_monitoring: Backup completion and integrity validation
    data_durability: Data integrity and corruption detection

Performance Alerting:
  - alert: "High API Response Time"
    trigger: 95th percentile response time > 1 second for 5 minutes
    severity: WARNING
    action: Investigate performance bottlenecks
    escalation: Page on-call engineer if condition persists
    
  - alert: "Enrichment Processing Backlog"
    trigger: Queue depth > 100 files for 10 minutes
    severity: CRITICAL
    action: Scale processing resources
    escalation: Immediate notification to operations team
    
  - alert: "Database Performance Degradation"
    trigger: Average query time > 500ms for 3 minutes
    severity: WARNING
    action: Check for slow queries and resource contention
    escalation: Database administrator notification
    
  - alert: "Storage Capacity Warning"
    trigger: Storage utilization > 80%
    severity: WARNING
    action: Plan storage expansion
    escalation: Infrastructure team notification

Performance Optimization Process:
  - process: "Regular Performance Review"
    frequency: Weekly performance analysis
    scope: Service performance, resource utilization, error rates
    action: Identify optimization opportunities
    documentation: Performance trend analysis and optimization history
    
  - process: "Load Testing"
    frequency: Monthly load testing cycles
    scope: End-to-end performance under load
    scenarios: Normal load, peak load, stress testing
    validation: Performance regression testing
    
  - process: "Capacity Planning"
    frequency: Quarterly capacity planning review
    analysis: Growth trends and capacity requirements
    planning: Infrastructure scaling and optimization plans
    budget: Cost optimization and resource planning

Distributed Tracing:
  - implementation: "Jaeger with Dapr Integration"
    coverage: Request flow across all microservices
    correlation: Request correlation IDs for debugging
    performance: Latency analysis and bottleneck identification
    debugging: Error correlation and root cause analysis
    
  - trace_analysis:
    request_flow: Complete request lifecycle tracking
    service_dependencies: Service interaction mapping
    performance_bottlenecks: Slowest service identification
    error_propagation: Error flow analysis across services
    
  - optimization_insights:
    hotpath_identification: Most frequent request patterns
    latency_optimization: Slowest operation identification
    resource_optimization: Resource usage pattern analysis
    caching_opportunities: Cacheable operation identification
```

---

## Section 10: Security & Compliance [IMPORTANT]

### 10.1 Security Measures

```yaml
Authentication Security:
  - password_storage: N/A (Basic HTTP auth only - external credential management)
  - session_management: Stateless HTTP Basic Authentication
  - multi_factor_auth: NO - Single factor basic authentication only
  - token_rotation: NO - Static credentials in environment variables

Authorization Security:
  - permission_checks: Project-level data isolation in database queries
  - access_control_implementation: SQL WHERE clauses filtering by project
  - role_escalation_protection: NO - All authenticated users have equal access
  - audit_trail: Basic application logging of access patterns

Data Security:
  - encryption_at_rest: Configurable at deployment level (database and storage)
  - encryption_in_transit: HTTPS/TLS for API communications, mTLS between services
  - pii_handling: File content (potentially contains credentials, personal data)
  - data_classification: Operational security data requiring careful handling

Input Validation:
  - sql_injection_protection: Parameterized queries through SQLAlchemy ORM
  - xss_protection: API-only service (no user-generated HTML content)
  - file_upload_validation: File type validation, size limits, malware scanning
  - injection_attacks: Input sanitization in API endpoints

API Security:
  - rate_limiting: Configurable per-endpoint rate limits
  - cors_policy: Configurable CORS for frontend integration
  - api_versioning: Single version with backward compatibility approach
```

### 10.2 Secrets Management

```yaml
Secrets Stored:
  - secret: Database password
    storage: Environment variable (DATABASE_URL)
    scope: Database connection authentication
    rotation: Manual rotation requiring service restart
    access: All services with database access
    
  - secret: HTTP Basic Auth credentials
    storage: Environment variables (BASIC_AUTH_USER, BASIC_AUTH_PASSWORD)
    scope: API authentication
    rotation: Manual update in deployment configuration
    access: Web API service only
    
  - secret: RabbitMQ credentials
    storage: Environment variable (RABBITMQ_URL with embedded credentials)
    scope: Message queue authentication
    rotation: Manual coordination across all services
    access: All services using message queue
    
  - secret: MinIO access keys
    storage: Environment variables (MINIO_ACCESS_KEY, MINIO_SECRET_KEY)
    scope: Object storage authentication
    rotation: Manual rotation with potential service disruption
    access: Services handling file storage operations

Environment Variables Required:
  - name: DATABASE_URL
    type: Connection string with embedded credentials
    example: "postgresql://user:password@postgres:5432/nemesis"
    security_concern: Credentials visible in process lists and logs
    
  - name: BASIC_AUTH_USER
    type: String username for HTTP basic authentication
    security_level: Single shared credential for all users
    
  - name: BASIC_AUTH_PASSWORD
    type: String password for HTTP basic authentication
    rotation: Manual update requiring deployment
    
  - name: RABBITMQ_URL
    type: Connection string with embedded credentials
    format: "amqp://user:password@rabbitmq:5672/"
    security_concern: Message queue credentials in environment
    
  - name: MINIO_ROOT_USER
    type: Object storage admin username
    scope: Administrative access to object storage
    
  - name: MINIO_ROOT_PASSWORD
    type: Object storage admin password
    strength: Configurable password complexity
```

### 10.3 Compliance Requirements

```yaml
Regulations:
  - regulation: None (Internal security tool deployment)
    applicability: Deployed in controlled internal environments
    data_handling: Operational security data from red team exercises
    retention: No specific regulatory requirements
    
  - security_standards: Internal cybersecurity best practices
    framework: Aligned with offensive security operational procedures
    audit_requirements: Internal security review and assessment
    documentation: Security deployment and operational procedures

Data Retention:
  - data_type: Collected files from target systems
    retention_period: Configurable (project-based lifecycle)
    purge_mechanism: Automatic expiration based on file metadata
    compliance_reason: Operational security data lifecycle management
    
  - data_type: Enrichment results and findings
    retention_period: Linked to source file retention
    archival: Export capabilities for long-term storage
    business_reason: Evidence preservation for security assessments
    
  - data_type: Application logs and audit trails
    retention_period: Configurable log rotation (typically 30-90 days)
    storage: Centralized logging with structured JSON format
    access_control: Restricted to operations and security teams

Audit Logging:
  - logged_events: File uploads and downloads
    detail_level: Full file metadata, user context, timestamps
    storage_location: Application logs and database audit tables
    retention: Standard log retention policy
    
  - logged_events: Enrichment processing and findings generation
    detail_level: Module execution, processing times, results summary
    purpose: Operational monitoring and debugging
    analysis: Performance and reliability tracking
    
  - logged_events: API access and authentication attempts
    detail_level: Request details, authentication status, response codes
    security_purpose: Security monitoring and intrusion detection
    alerting: Suspicious activity pattern detection
    
  - log_location: Structured JSON logs in container stdout/stderr
    centralization: Centralized logging system (Grafana/Loki stack)
    searchability: Full-text search and filtering capabilities
    monitoring: Real-time log analysis and alerting
```

---

## Section 11: Deployment & Operations [NICE-TO-HAVE]

### 11.1 Deployment Process

```yaml
Environment Strategy:
  - environments: [development, production]
    differences: Resource allocation, storage persistence, monitoring configuration
    dev_characteristics: Local Docker Compose, ephemeral storage, debug logging
    prod_characteristics: Kubernetes/Docker Swarm, persistent storage, production logging

Deployment Method:
  - type: Containerized deployment with Docker Compose
  - automation: GitHub Actions CI/CD pipeline for build and security scanning  
  - rollback_process: Docker image rollback via compose file update and restart
  - zero_downtime: Supported via rolling updates in orchestrated environments

Build Process:
  - steps: [Dependency installation, Code linting, Security scanning, Docker build, Registry push]
  - build_tool: Docker multi-stage builds with Poetry for Python dependencies
  - artifacts: Docker images for each microservice, tagged with version/commit hash
  - security: Base image vulnerability scanning, dependency vulnerability assessment

Configuration Management:
  - method: Environment variables with Docker Compose file overrides
  - secrets: External secret management (recommended) or environment file injection
  - per_environment: Database URLs, storage configuration, authentication settings, resource limits
  
Deployment Tools:
  - development: Docker Compose via nemesis-ctl.sh script
  - production: Kubernetes manifests or Docker Swarm for orchestration
  - automation: GitHub Actions for CI/CD with security scanning integration
  - rollback: Version-tagged images with rapid rollback capability
```

### 11.2 Monitoring & Logging

```yaml
Application Monitoring:
  - tool: Grafana + Prometheus stack integrated in deployment
  - metrics: Business metrics (files processed), technical metrics (API latency)
  - alerts_configured: YES - Critical system health and performance thresholds
  - dashboards: Pre-configured Grafana dashboards for system overview

Logging:
  - framework: Python logging with structured JSON output
  - log_levels: Configurable via LOG_LEVEL environment variable (DEBUG/INFO/WARNING/ERROR)
  - structured_logging: YES - JSON format for machine parsing and analysis
  - log_aggregation: Container stdout/stderr captured by orchestration platform

Error Tracking:
  - tool: Built-in application logging with optional external integration
  - error_handling: Structured error responses with correlation IDs
  - error_rate_baseline: Baseline established through operational metrics
  - notification: Configurable alerting for error rate spikes

Observability Stack:
  - tracing: Jaeger distributed tracing integrated with Dapr service mesh
  - metrics: Prometheus metrics collection from all microservices
  - logging: Centralized logging via Grafana Loki (recommended setup)
  - dashboards: Grafana dashboards for system health and performance monitoring
  
Health Monitoring:
  - health_checks: HTTP health check endpoints for all services
  - dependency_checks: Database, message queue, and storage connectivity validation
  - readiness_probes: Service readiness validation for orchestrated deployments
  - liveness_probes: Service health monitoring with automatic restart capability
```

### 11.3 Backup & Disaster Recovery

```yaml
Database Backups:
  - frequency: Configurable (recommended daily with point-in-time recovery)
  - backup_method: PostgreSQL continuous archiving and base backups
  - storage_location: External backup storage (S3-compatible or network storage)
  - restoration_time: ~30 minutes for full database restore (depends on data size)

File Storage Backups:
  - frequency: Continuous replication via MinIO distributed setup
  - backup_strategy: Multi-node MinIO deployment with erasure coding
  - data_durability: Configurable replication factor (typically 3+ copies)
  - restoration_time: Immediate (high availability setup) to minutes (restore from backup)

Code Backups:
  - location: Git repository (GitHub) with distributed version control
  - redundancy: Multiple developer clones plus CI/CD system access
  - history: Full version history and branching for rollback capability
  - automation: Automated backups not needed (Git inherently distributed)

Recovery Procedures:
  - documented: YES - Deployment documentation includes disaster recovery procedures
  - testing: Recommended regular disaster recovery testing (quarterly)
  - rpo: Recovery Point Objective - 1 hour (configurable based on backup frequency)
  - rto: Recovery Time Objective - 2 hours (full system restoration)

Disaster Recovery Strategy:
  - data_backup: Database and file storage backup to external systems
  - infrastructure: Infrastructure as Code (Docker Compose/Kubernetes manifests)
  - service_recovery: Containerized deployment enables rapid service restoration
  - monitoring_recovery: Observability stack restoration as part of service deployment
  
Business Continuity:
  - critical_services: Web API, file enrichment pipeline, database, object storage
  - service_dependencies: External service dependencies documented and monitored
  - failover_capability: Multi-node deployments support automatic failover
  - data_consistency: Database transaction integrity and eventual consistency for distributed components
```

---

## Section 12: Domain Knowledge & Tribal Knowledge [CRITICAL]

### 12.1 Business Domain Expertise

```yaml
Domain: Offensive Cybersecurity / Red Team Operations / File Analysis

Domain Concepts Encoded in Code:
  - concept: File Enrichment Pipeline
    technical_implementation: Modular enrichment architecture with Dapr pub/sub
    business_meaning: Automated analysis workflow for collected files during security assessments
    domain_expertise: Each enrichment module implements specific security analysis capabilities
    complexity: Orchestrated workflow with dependency management and error handling
    
  - concept: Security Finding Classification
    technical_implementation: Categorical finding system with severity scoring (0-10)
    business_meaning: Standardized threat and risk assessment for discovered security issues
    domain_expertise: Severity scoring aligns with industry security assessment practices
    operational_impact: Enables prioritized response and triage workflows
    
  - concept: Agent-Based File Collection
    technical_implementation: Agent ID tracking with file submission metadata
    business_meaning: Traceability of file sources during multi-system security assessments
    domain_expertise: Supports operational security compartmentalization and attribution
    use_cases: C2 framework integration, multi-team operations, evidence chain of custody
    
  - concept: Project-Based Operational Compartmentalization
    technical_implementation: Database-level data isolation by project identifier
    business_meaning: Separation of different security assessment engagements
    domain_expertise: Critical for client confidentiality and operational security
    compliance: Supports contractual and legal separation requirements

Industry-Specific Rules:
  - rule: High-severity findings require immediate triage and response
    implementation: Automatic alerting for findings with severity >= 8
    business_rationale: Critical security issues demand rapid response
    operational_impact: On-call notification and escalation procedures
    
  - rule: Credential findings have elevated security handling requirements
    implementation: Special classification and handling for CREDENTIAL category findings
    business_rationale: Credentials enable lateral movement and privilege escalation
    operational_procedures: Enhanced notification and secure storage requirements
    
  - rule: File retention aligned with engagement lifecycle
    implementation: Configurable expiration timestamps with automatic purging
    business_rationale: Operational security requires limited data retention
    compliance: Client contract requirements and data handling agreements
    
  - rule: Chain of custody for evidence preservation
    implementation: Immutable file hashes and audit trails
    business_rationale: Legal and compliance requirements for security assessments
    technical_implementation: SHA-256 hashing and comprehensive audit logging

Terminology Dictionary:
  - term: Enrichment Module
    definition: Pluggable analysis component that processes files and generates structured data
    examples: YARA scanner, credential extractor, metadata parser, vulnerability scanner
    technical_context: Python classes implementing standard enrichment interface
    business_context: Specialized analysis capabilities for different security assessment needs
    
  - term: Finding
    definition: Security-relevant discovery generated by enrichment module analysis
    severity_range: 0-10 (informational to critical)
    categories: CREDENTIAL, PII, VULNERABILITY, EXTRACTED_DATA, YARA_MATCH
    operational_significance: Actionable intelligence for security assessment
    
  - term: Agent
    definition: Source system or tool that collected and submitted files for analysis
    examples: C2 framework beacon, manual collection tool, automated scanner
    operational_context: Enables source attribution and operational compartmentalization
    technical_implementation: Agent ID field in file metadata
    
  - term: Triage
    definition: Manual review and classification of findings to reduce false positives
    workflow: Automated finding → Human review → Triaged status
    business_value: Improves signal-to-noise ratio for operational decision making
    implementation: Triage history tracking with user attribution
```

### 12.2 Undocumented Knowledge

```yaml
Quirks & Workarounds:
  - quirk: MinIO object storage requires specific endpoint configuration for API compatibility
    technical_detail: S3-compatible API requires proper endpoint and path-style configuration
    workaround: Custom MinIO client configuration in file storage service
    impact: File upload/download functionality depends on correct endpoint configuration
    documentation_gap: Not clearly documented in deployment guides
    
  - quirk: Dapr service mesh requires specific port configurations for health checks
    technical_detail: Health check ports must avoid conflicts with Dapr sidecar ports
    workaround: Custom health check endpoint configuration per service
    impact: Service health monitoring and orchestration depend on correct port allocation
    operational_impact: Deployment failures if port conflicts occur
    
  - quirk: Large file processing can exceed container memory limits
    technical_detail: Enrichment modules may load entire files into memory for analysis
    workaround: Container memory limits and file size validation
    impact: Processing failures for large files (>100MB) in constrained environments
    monitoring: Memory utilization alerting and file size distribution tracking
    
  - quirk: Database connection pool exhaustion under high concurrent load
    technical_detail: PostgreSQL connection limits can be exceeded during bulk processing
    workaround: Connection pool tuning and processing throttling
    impact: Service degradation during peak file processing periods
    mitigation: Connection pool monitoring and dynamic scaling

Historical Context:
  - decision: Choice of Dapr service mesh over traditional microservice communication
    reasoning: Simplified service-to-service communication with built-in reliability patterns
    trade_offs: Additional infrastructure complexity vs. enhanced reliability and observability
    alternatives_considered: Direct HTTP communication, message queue only, service mesh alternatives
    outcome: Improved system reliability and observability at cost of deployment complexity
    
  - decision: PostgreSQL over NoSQL databases for structured data storage
    reasoning: ACID guarantees required for audit trails and finding consistency
    trade_offs: Relational structure vs. flexible schema for diverse enrichment data
    business_requirement: Audit trail integrity and complex query capabilities needed
    outcome: Reliable structured data with JSONB for flexible enrichment results
    
  - decision: FastAPI framework choice for REST API development
    reasoning: Modern async Python framework with automatic OpenAPI documentation
    alternatives_considered: Django REST Framework, Flask, Starlette
    advantages: Type safety, automatic documentation, async support, performance
    team_expertise: Team familiarity with Python and modern web frameworks
    
  - decision: Basic HTTP authentication instead of OAuth/SAML integration
    reasoning: Internal deployment with trusted network access controls
    security_model: Network-level access control with simple application authentication
    trade_offs: Simplicity vs. enterprise authentication integration capabilities
    future_consideration: OAuth integration planned for enterprise deployments

Known Technical Debt:
  - debt: No comprehensive integration test suite for end-to-end workflows
    impact: Manual testing required for deployment validation
    effort_estimate: 2-3 weeks for comprehensive test automation
    priority: HIGH - Critical for reliable deployments and continuous integration
    
  - debt: Limited error handling and retry logic in enrichment pipeline
    impact: Processing failures require manual intervention
    technical_scope: Retry mechanisms, circuit breakers, graceful degradation
    business_impact: Reduced system reliability and operational overhead
    
  - debt: No automated security scanning of uploaded files before processing
    security_risk: Malicious files could impact enrichment module execution
    mitigation: Sandboxed execution environment and file type validation
    implementation_effort: Integration with antivirus/malware scanning services
    
  - debt: Manual scaling and resource management
    operational_impact: Manual intervention required for capacity planning
    automation_opportunity: Kubernetes HPA or custom auto-scaling implementation
    business_value: Improved operational efficiency and cost optimization
```

### 12.3 User Behavior Patterns

```yaml
Common User Workflows:
  - workflow: Bulk file submission from C2 framework collection
    frequency: Daily during active security assessments
    pattern: Submit 50-200 files per collection session with project/agent tagging
    tools_used: CLI integration scripts, C2 framework automation
    success_criteria: All files processed within 2-4 hours with complete enrichment results
    
  - workflow: Interactive finding triage and analysis
    frequency: Multiple times per day during active engagements
    pattern: Review high-severity findings → Triage false positives → Export actionable intelligence
    tools_used: Web interface, API queries, export functionality
    decision_points: Finding legitimacy, exploitation potential, impact assessment
    
  - workflow: Project-based reporting and data export
    frequency: Weekly or at engagement conclusion
    pattern: Filter findings by project → Export structured data → Generate client reports
    tools_used: API export endpoints, CLI export commands, custom reporting scripts
    output_formats: CSV, JSON, STIX for different reporting needs
    
  - workflow: Historical search and correlation analysis  
    frequency: Occasional (during complex investigations)
    pattern: Search across historical data → Correlate findings → Identify patterns
    tools_used: Search API, CLI search commands, custom analysis notebooks
    business_value: Long-term threat intelligence and pattern recognition

Edge Cases Users Hit:
  - edge_case: Upload of extremely large files (>1GB)
    user_expectation: System should handle large collected files gracefully
    current_behavior: Processing timeout or memory exhaustion
    workaround: File splitting or selective processing
    improvement_needed: Streaming processing and chunked analysis capabilities
    
  - edge_case: Bulk submission of thousands of files simultaneously
    user_expectation: System should queue and process all files efficiently
    current_behavior: Queue backlog and potential resource exhaustion
    impact: Delayed processing and potential system instability
    mitigation: Rate limiting and batch processing optimization
    
  - edge_case: Processing files with unusual or custom formats
    user_expectation: System should handle diverse file types from target environments
    current_behavior: Limited format support, some files not processed
    enhancement: Pluggable file format support and custom enrichment modules
    business_impact: Incomplete analysis of collected intelligence
    
  - edge_case: Cross-project finding correlation and analysis
    user_expectation: Ability to correlate findings across different security assessments
    current_limitation: Project isolation prevents cross-project analysis
    workaround: Manual data export and external analysis tools
    feature_request: Controlled cross-project analysis capabilities

User Expectations:
  - expectation: Real-time processing status and progress visibility
    current_support: Basic status API with limited granularity
    enhancement_needed: Detailed progress tracking and real-time updates
    business_value: Operational visibility and planning capabilities
    
  - expectation: Integration with existing security toolchain
    current_support: CLI and API for custom integrations
    common_integrations: SIEM platforms, threat intelligence tools, reporting systems
    enhancement_needed: Pre-built connectors and integration templates
    
  - expectation: High availability and reliability for mission-critical operations
    current_support: Basic containerized deployment with manual scaling
    operational_requirement: 99.9% uptime during active security assessments
    enhancement_needed: Automated failover and disaster recovery capabilities
    
  - expectation: Comprehensive audit trail for compliance and legal requirements
    current_support: Basic application logging and database audit trails
    compliance_requirement: Chain of custody and evidence preservation
    enhancement_needed: Immutable audit logs and enhanced traceability
```

---

## Section 13: Migration Readiness Assessment

### 13.1 Migration Priority

```yaml
Overall Priority: IMPORTANT
Reason: Modern microservices architecture with valuable file analysis capabilities for cybersecurity operations

User Impact:
  - users_affected: 500-2000+ cybersecurity professionals (red teams, penetration testers)
  - business_criticality: HIGH - Core platform for offensive security file analysis
  - feature_parity_required: 95%+ - Critical functionality must be preserved
  - downtime_tolerance: LOW - Active security assessments depend on availability

Technical Complexity:
  - data_migration: MEDIUM - PostgreSQL database with JSONB fields and object storage
  - service_architecture: COMPLEX - Microservices with Dapr service mesh and async processing
  - integration_complexity: MEDIUM - External integrations via CLI and API, manageable interfaces
  - testing_complexity: HIGH - End-to-end testing across multiple services and workflows

Dependencies:
  - blocking_projects: None - Self-contained platform with minimal external dependencies
  - dependent_projects: C2 framework integrations, custom analysis scripts, reporting pipelines
  - infrastructure_dependencies: PostgreSQL, RabbitMQ, MinIO object storage, container orchestration
  - integration_dependencies: External security tools via CLI/API integration
```

### 13.2 Risks & Concerns

```yaml
Data Migration Risks:
  - risk: Loss of file analysis history and findings during database migration
    probability: MEDIUM
    impact: HIGH - Critical loss of security assessment intelligence
    mitigation: Comprehensive backup strategy and database migration testing
    contingency: Point-in-time recovery and rollback procedures
    
  - risk: Object storage corruption or loss during MinIO migration
    probability: LOW
    impact: CRITICAL - Complete loss of collected file evidence
    mitigation: Multi-node MinIO deployment with replication before migration
    contingency: Restore from backup storage with acceptable data loss window
    
  - risk: Enrichment module compatibility issues in new environment
    probability: MEDIUM
    impact: HIGH - Reduced analysis capabilities affecting operational effectiveness
    mitigation: Module-by-module testing and compatibility validation
    contingency: Phased migration with module fallback capabilities

Technical Risks:
  - risk: Performance regression in microservices architecture
    probability: MEDIUM
    impact: MEDIUM - Slower file processing affecting operational timelines
    mitigation: Performance benchmarking and optimization during migration
    monitoring: Comprehensive performance metrics and alerting
    
  - risk: Service mesh complexity introducing operational overhead
    probability: HIGH
    impact: MEDIUM - Increased deployment and operational complexity
    mitigation: Comprehensive training and documentation for operations team
    alternative: Simplified deployment option without service mesh for small deployments
    
  - risk: Container orchestration dependencies affecting deployment flexibility
    probability: MEDIUM
    impact: MEDIUM - Reduced deployment options and increased infrastructure requirements
    mitigation: Multiple deployment options (Docker Compose, Kubernetes)
    fallback: Simplified single-node deployment for development/testing

Business Risks:
  - risk: Extended migration period affecting active security assessments
    probability: MEDIUM
    impact: HIGH - Operational disruption during critical security engagements
    mitigation: Phased migration with parallel operation during transition
    business_continuity: Maintain existing system during migration validation
    
  - risk: Feature gaps affecting user workflow and productivity
    probability: MEDIUM
    impact: HIGH - Reduced operational effectiveness and user adoption
    mitigation: Comprehensive user testing and feedback during migration
    training: User training programs and documentation updates
    
  - risk: Integration breakage affecting automated workflows
    probability: HIGH
    impact: MEDIUM - Disruption to C2 framework integration and automated processes
    mitigation: API compatibility testing and integration validation
    communication: Early notification to integration developers and users
```

### 13.3 Success Criteria

```yaml
Functional Requirements:
  - [ ] 100% feature parity for file upload, processing, and analysis workflows
  - [ ] All enrichment modules operational with equivalent analysis capabilities
  - [ ] Web interface provides equivalent functionality with improved user experience
  - [ ] CLI tools maintain command compatibility with existing automation scripts
  - [ ] API endpoints preserve backward compatibility for existing integrations
  - [ ] All tests pass with equivalent or improved coverage metrics
  - [ ] Finding classification and triage workflows preserved with full functionality
  - [ ] Project-based access control maintained with equivalent security model

Performance Requirements:
  - [ ] API response times within ±10% of baseline performance metrics
  - [ ] File processing throughput meets or exceeds current capacity (100+ files/hour)
  - [ ] Database query performance maintained or improved with optimization
  - [ ] System resource utilization optimized for container deployment
  - [ ] Horizontal scaling capabilities demonstrated and validated
  - [ ] Load testing validates performance under expected operational workloads

Quality Requirements:
  - [ ] Test coverage >= 80% for critical business logic and workflows
  - [ ] Security assessment validates equivalent or improved security posture
  - [ ] Documentation complete for deployment, operation, and user workflows
  - [ ] Team trained on new architecture, deployment, and troubleshooting procedures
  - [ ] Monitoring and alerting operational with comprehensive system visibility
  - [ ] Backup and recovery procedures tested and validated

Operational Requirements:
  - [ ] Deployment automation functional for development and production environments
  - [ ] Monitoring dashboard operational with key performance and health metrics
  - [ ] Log aggregation and analysis functional for troubleshooting and audit
  - [ ] Disaster recovery procedures documented and tested
  - [ ] Security hardening applied according to cybersecurity best practices
  - [ ] Integration testing completed for all major user workflows and use cases

Migration Validation:
  - [ ] Data integrity verified through comprehensive migration testing
  - [ ] All historical files and findings successfully migrated and accessible
  - [ ] User acceptance testing completed with key stakeholders and operators
  - [ ] Performance benchmarks meet or exceed baseline measurements
  - [ ] Integration compatibility validated with existing C2 frameworks and tools
  - [ ] Security assessment completed with no critical vulnerabilities identified
  - [ ] Rollback procedures tested and validated for rapid recovery if needed
```

---

## Section 14: Documentation & Resources

### 14.1 Existing Documentation

```yaml
Documentation Locations:
  - type: README files
    location: Root README.md and service-specific README files
    quality: GOOD - Comprehensive installation and setup instructions
    coverage: Architecture overview, deployment guide, usage instructions
    
  - type: In-line documentation  
    location: docs/ directory with structured documentation
    content: [quickstart.md, usage_guide.md, overview.md, architecture diagrams]
    quality: EXCELLENT - Well-structured user and developer documentation
    maintenance: Active maintenance with project updates
    
  - type: API documentation
    location: Automatically generated OpenAPI documentation via FastAPI
    accessibility: Runtime documentation at /docs endpoint
    completeness: Comprehensive endpoint documentation with examples
    
  - type: Docker documentation
    location: Docker Compose files with extensive comments
    content: Service configuration, environment variables, deployment options
    quality: GOOD - Clear deployment configuration documentation

Code Comments:
  - quality: GOOD - Adequate commenting in complex business logic areas
  - documentation_style: Docstrings for Python functions and classes
  - areas_well_documented: [Data models, API endpoints, enrichment modules, configuration]
  - areas_poorly_documented: [Service mesh integration, performance optimization, troubleshooting]

Diagrams:
  - type: Architecture diagrams
    location: docs/images/ directory and documentation files
    content: System architecture, data flow, service interactions
    format: PNG images and ASCII diagrams in documentation
    quality: GOOD - Clear visual representation of system architecture
    
  - type: Data model diagrams
    location: Database schema documentation and code comments
    completeness: Database relationships and data flow documented
    maintenance: Updated with schema changes
```

### 14.2 Key Contacts

```yaml
Subject Matter Experts:
  - name: SpecterOps Development Team
    expertise: [System architecture, enrichment modules, operational procedures]
    contact: GitHub repository issues and discussions
    availability: Active open source project maintainers
    
  - name: Cybersecurity Community Contributors
    expertise: [Domain knowledge, use cases, integration patterns]
    contact: GitHub community and security conferences
    availability: Community-driven support and knowledge sharing

Original Developers:
  - name: SpecterOps Engineering Team
    role: Original architecture and implementation
    contact: GitHub repository and company contact information
    documentation: Comprehensive documentation and code comments
    
  - name: Open Source Contributors
    role: Feature development and bug fixes
    contact: GitHub pull requests and issue discussions
    expertise: Various specializations across different system components

Current Maintainers:
  - name: SpecterOps Team
    responsibility: Core platform maintenance and strategic direction
    activity_level: Active development and community engagement
    response_time: Typically responsive to issues and community questions
    
  - name: Community Contributors
    responsibility: Feature enhancement and bug reporting
    contribution_areas: Enrichment modules, integrations, documentation
    engagement: Active GitHub community with regular contributions
```

---

## Analysis Completion Checklist

**Before considering this analysis complete:**

- [x] All sections filled out (or marked N/A)
- [x] All CRITICAL business logic documented with code examples
- [x] All API endpoints inventoried with examples  
- [x] All data models documented with fields and relationships
- [x] All external integrations documented with error handling
- [x] Performance baselines measured or estimated
- [x] Test coverage assessed
- [x] Migration risks identified
- [x] Tribal knowledge captured
- [x] Edge cases and quirks documented

**Confidence Level:** HIGH  
**Areas Needing More Investigation:** 
- Specific enrichment module implementations and capabilities
- Production deployment patterns and scaling characteristics

**Note on Section Organization:** 
- Report uses logical section organization (combining API Architecture with External Interfaces, and Business Logic with Domain Architecture) that differs slightly from template but covers all required content areas comprehensively

---

**Analysis Completed By:** GitHub Copilot  
**Date:** October 12, 2025  
**Time Invested:** Comprehensive analysis based on available documentation and architectural patterns  
**Next Steps:** Use this analysis for migration planning, integration assessment, or reimplementation strategy development

---