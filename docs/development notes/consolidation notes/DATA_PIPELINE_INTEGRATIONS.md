# Data Pipeline Integrations Report

**Project:** Mental Prosthetic Platform (modular-monolith-2)  
**Report Date:** November 15, 2025  
**Scope:** Cross-domain event streaming and tool interoperability  
**Total Integrated Tools:** 37

---

## Executive Summary

This report documents the data pipeline integrations that enable automatic cross-tool communication and event-driven workflows across the mental prosthetic platform. These integrations allow the 37 tools to react to each other's actions through shared event streaming infrastructure.

### Key Integration Technologies

1. **Event Bus Service** - Central event routing with WebSocket support
2. **n8n Workflow Engine** - Adaptive workflow automation
3. **Dapr Workflows** - Distributed application runtime for microservices orchestration
4. **Kafka Streaming** - Real-time data pipeline for security analytics
5. **AWS SQS** - Signal consumption for security events

---

## 1. Central Event Bus (Jane Orchestrator)

**Location:** `apps/core/jane-orchestrator/src/services/event_bus_service.py`

### Architecture

The Event Bus Service provides the foundational infrastructure for cross-domain communication across all 37 integrated tools.

#### Event Types

**Data Synchronization:**
- `SYNC_STARTED` - Initiated data sync between tools
- `SYNC_COMPLETED` - Successful sync completion
- `SYNC_FAILED` - Sync failure notification
- `DATA_UPDATED` - Entity data modification
- `DATA_CREATED` - New entity creation
- `DATA_DELETED` - Entity deletion

**Domain-Specific Events:**
- `SECURITY_ALERT` - Security domain alerts
- `THREAT_DETECTED` - Threat intelligence updates
- `TASK_CREATED` - Productivity task creation
- `TASK_COMPLETED` - Task completion notification
- `WORKFLOW_TRIGGERED` - Workflow initiation
- `BUDGET_UPDATED` - Financial tracking updates

**System Events:**
- `TOOL_CONNECTED` - Tool registration
- `TOOL_DISCONNECTED` - Tool disconnection
- `DOMAIN_STATUS_CHANGED` - Domain health updates
- `PERFORMANCE_ALERT` - Performance threshold violations

**User Events:**
- `USER_ACTION` - User interaction tracking
- `PREFERENCE_UPDATED` - User preference changes
- `SESSION_STARTED/ENDED` - Session lifecycle

#### Performance Characteristics

- **Priority Levels:**
  - `CRITICAL`: <200ms delivery requirement
  - `HIGH`: <1s delivery requirement
  - `MEDIUM`: <5s delivery requirement
  - `LOW`: Best effort delivery

- **Delivery Tracking:**
  - Event IDs for correlation
  - Retry mechanism (max 3 retries)
  - TTL (Time To Live) support (default 300s)
  - Delivery confirmations for critical events

- **Real-time Metrics:**
  - Events published count
  - Events delivered count
  - Events failed count
  - Average delivery time (ms)
  - Active handlers count
  - Active WebSocket connections

### Domain-Based Routing

Events are routed based on:
- **Source Domain:** `SECURITY`, `PRODUCTIVITY`, `MTG`, `INFRASTRUCTURE`, `SYSTEM`
- **Target Tools:** Specific tool filtering
- **Target Domains:** Domain-level broadcasting
- **User Context:** User-scoped event distribution

### WebSocket Integration

Real-time bi-directional communication supporting:
- Tool-specific subscriptions
- Domain-level subscriptions
- User session tracking
- Connection lifecycle management
- <250ms latency for cross-tool sync (per NFR-006)

---

## 2. n8n Workflow Integration

**Location:** `apps/core/jane-orchestrator/src/api/n8n_integration/endpoints.py`

### Adaptive Workflow Execution

The n8n integration layer provides workflow automation capabilities that connect multiple tools through defined execution graphs.

#### Workflow Execution Capabilities

**Execution Features:**
- Trigger-based workflow activation
- Async execution with status tracking
- Workflow cancellation support
- Execution history tracking
- Performance metrics collection

**API Endpoints:**
```
POST   /api/n8n-integration/execute          - Execute workflow
GET    /api/n8n-integration/execution/{id}/status - Get execution status
POST   /api/n8n-integration/execution/{id}/cancel - Cancel execution
GET    /api/n8n-integration/workflow/{id}/history - Execution history
GET    /api/n8n-integration/connection/validate  - Connection health
POST   /api/n8n-integration/sync              - Sync workflows
GET    /api/n8n-integration/workflows/executable - List ready workflows
```

#### Integration Patterns

**Security Domain Example:**
- **Security Onion** → webhook trigger → **n8n Dispatcher Workflow**
- Parallel execution across:
  - IP Reputation Analysis
  - Domain Reputation Analysis  
  - Hash Reputation Analysis
  - CVE Information Gathering

**Cross-Domain Integration:**
- Security alerts triggering productivity tasks
- Threat intelligence updates triggering workflow automation
- Budget updates propagating to financial dashboards

---

## 3. Security Domain Data Pipelines

### 3.1 HELK Kafka Streaming Pipeline

**Location:** `apps/security/helk-service/infrastructure/docker/helk-kibana-analysis-alert-basic.yml`

#### Architecture Components

**Kafka Infrastructure:**
- **Zookeeper:** Cluster coordination
- **Kafka Broker:** Message streaming (port 9092)
- **KSQL Server:** Stream processing (port 8088)
- **Topics:** `winlogbeat`, `winevent`, `SYSMON_JOIN`, `filebeat`, `zeek`

**Data Flow:**
```
Security Events → Logstash → Kafka Topics → KSQL Processing → Elasticsearch → Kibana
```

**Integration Points:**
- **Input:** Logstash receivers (ports 5044, 8531, 3515, 5514, 8515, 8516)
- **Processing:** KSQL stream transformations
- **Output:** Elasticsearch indexing for threat hunting queries
- **Visualization:** Kibana dashboards

#### Performance Characteristics

- **Retention:** 4 hours log retention
- **Heap Allocation:** 1GB Kafka, 1GB KSQL
- **Replication Factor:** 1 (single broker)
- **Consumer Groups:** ETL pipeline tracking

### 3.2 Dispatch AWS SQS Signal Consumer

**Location:** `apps/security/dispatch-service/src/services/plugins/dispatch_aws/plugin.py`

#### Signal Processing Pipeline

**Queue Configuration:**
- Message batch size: Configurable
- Visibility timeout: 40 seconds
- Wait time: 20 seconds (long polling)
- Compression support: zlib base64 encoding

**Signal Flow:**

```text
AWS SQS Queue → Batch Receive → Decompress → Validate → 
Signal Instance Creation → Database Persistence → 
Event Bus Notification → Delete from Queue
```

**Error Handling:**
- Automatic retry on transient failures
- Message remains in queue on processing errors
- Validation error logging with skip behavior
- Duplicate detection via UUID checking

### 3.3 MISP Threat Intelligence Sharing

**Location:** `apps/security/misp-service/`

#### Integration Architecture

**Data Synchronization:**
- Automatic real-time synchronization between MISP instances
- Granular sharing levels (organization, community, connected communities, all)
- Flexible sharing groups for custom distribution
- Atomic-level attribute sharing with fine-grained control

**API Integration:**
- Extensive ReST API (OpenAPI specification)
- PyMISP library for Python integration
- restSearch API for comprehensive indicator searches
- Export support in multiple formats (STIX, JSON, XML, CSV)

**Event Processing:**
- Automatic correlation of indicators across events
- Free-text import with automatic attribute extraction
- Built-in taxonomy and tagging system
- Sighting support for indicator observations

**Feed Integration:**
- Automatic ingestion from external threat feeds
- Custom feed definitions and filtering
- Feed caching and update scheduling
- Validation and deduplication

**Workflow Automation:**
- Event publication/unpublication workflows
- Automatic attribute enrichment via modules
- Warning list checking for false positive reduction
- Proposal system for collaborative editing

**External APIs Supported:**
- VirusTotal integration
- Shodan lookups
- PassiveTotal queries
- Custom module framework for additional integrations

### 3.4 Nemesis RabbitMQ Message Queue

**Location:** `apps/security/nemesis-service/`

#### Service Communication Architecture

**Message Queue Infrastructure:**
- RabbitMQ for inter-service messaging
- Dapr pub/sub abstraction layer
- CloudEvents standard for message format
- Persistent message storage

**Service Communication Patterns:**

```text
File Upload → nemesis-web-api → RabbitMQ → file-enrichment
                                         → document-conversion
                                         → triage
                                         → alerting
```

**Queue Topics:**
- `file.uploaded` - New file submissions
- `file.enriched` - Enrichment completion
- `document.converted` - Document processing complete
- `alert.triggered` - Security alerts
- `triage.completed` - File classification done

**Message Reliability:**
- Message acknowledgment for guaranteed delivery
- Dead letter queues for failed processing
- Retry policies with exponential backoff
- Message TTL for cleanup

---

## 4. Nemesis Dapr Workflow Integration

**Location:** `apps/security/nemesis-service/`, `apps/security/nemesis-document-conversion/`

### Distributed Workflow Runtime

#### Dapr Components

**Workflow Runtime:**
- Workflow orchestration for document processing
- Activity-based decomposition
- Retry policies for fault tolerance
- Distributed state management

**Service Communication:**
- Dapr client for service-to-service calls
- Secret management via `nemesis-secret-store`
- Service invocation (e.g., Gotenberg conversion)
- Pub/sub messaging patterns

**Document Processing Pipeline:**
```
File Upload → Workflow Trigger → Document Conversion Activity →
PDF Generation (Gotenberg) → Text Extraction (Tika) → 
Enrichment → Storage (Minio) → Database Update → Event Publication
```

#### Integration Architecture

**Service Mesh:**
- **nemesis-web-api:** API gateway
- **nemesis-file-enrichment:** Processing service
- **nemesis-document-conversion:** Transformation service
- **nemesis-frontend:** User interface

**Data Flow:**
- CloudEvents for standardized messaging
- Workflow state persistence in PostgreSQL
- Object storage via MinIO
- Cross-service orchestration via Dapr sidecars

---

## 5. Productivity Domain Integrations

### 5.1 Goose Temporal Service

**Location:** `apps/productivity/goose-temporal-service/`

**Technology:** Go-based temporal workflow engine

**Capabilities:**
- Long-running process orchestration
- State persistence and recovery
- Distributed task scheduling
- Integration with main Goose service

### 5.2 n8n Trigger System

**Location:** `apps/productivity/n8n-service/src/packages/`

#### Trigger Node Architecture

**Trigger Types:**
- **Webhook Triggers:** HTTP endpoint activation
- **Polling Triggers:** Scheduled checks
- **Event Triggers:** External system notifications
- **Chat Triggers:** Conversational AI integration
- **MCP Triggers:** Model Context Protocol integration

**Integration Nodes:**
```
ManualChatTrigger    - Human-in-the-loop workflows
ChatTrigger          - Automated conversational flows
McpTrigger           - MCP protocol event handling
JiraTrigger          - Project management webhooks
AsanaTrigger         - Task management integration
SalesforceTrigger    - CRM event handling
```

**Execution Context:**
- TriggerContext class for node execution
- Event emission via `emit()` methods
- Error propagation via `emitError()`
- Trigger count tracking in database

### 5.3 Mealie API Integration

**Location:** `apps/productivity/mealie-service/`

#### External Integration Capabilities

**REST API Features:**
- Meal plan data export for external dashboards
- Recipe management via standardized endpoints
- Backup automation via API calls
- Webhook support for event notifications

**Integration Examples:**

**Home Assistant Integration:**
```yaml
# REST sensor for meal plan retrieval
rest:
  - resource: "http://mealie:9000/api/households/mealplans/today"
    method: GET
    headers:
      Authorization: Bearer <<API_TOKEN>>
    scan_interval: 3600
```

**n8n Backup Automation:**
- Scheduled backup creation via API
- Automatic retention management (keeps last 7 backups)
- Integration with notification services (ntfy, Pushover, Email)
- Failure alerting for backup monitoring

**Data Endpoints:**
- `/api/households/mealplans/today` - Current meal plans
- `/api/media/recipes/{id}/images/*` - Recipe images
- `/api/backups` - Backup management
- `/api/users/api-tokens` - API token administration

### 5.4 Goose MCP Extension System

**Location:** `apps/productivity/goose-service/`, `apps/productivity/goose-docs/docs/mcp/`

#### Model Context Protocol (MCP) Integration

The Goose AI agent uses the Model Context Protocol as its primary extension and integration mechanism, enabling it to connect with external tools and services.

**Built-in Extensions:**
- **Computer Controller:** Web scraping, file caching, automation execution
- **Auto Visualiser:** Automatic data visualization via MCP-UI
- **Developer Tools:** IDE integration, code analysis
- **Memory:** Persistent context across sessions

**Third-Party MCP Integrations:**
- **Asana:** Task management integration
- **Figma:** Design tool interaction
- **JetBrains:** IDE plugin support
- **VS Code:** Editor integration
- **Selenium:** Browser automation
- **Container Use:** Docker container management
- **Knowledge Graph:** Semantic data relationships
- **PDF:** Document processing
- **Speech:** Audio transcription and synthesis

**MCP-UI Protocol:**
- Standardized visualization rendering
- Interactive component support
- Data-driven chart generation (bar, line, scatter, sankey, treemap, etc.)
- Seamless integration with conversation flow

**Extension Management:**
- Toggle extensions via CLI (`goose session --extensions`)
- Per-session extension configuration
- Allowlist support for enterprise security
- Dynamic extension loading/unloading

---

## 6. Cross-Domain Integration Patterns

### 6.1 Security → Productivity Integration

**Scenario:** Security alert triggers task creation

```
Security Alert Event (HELK/MISP/SecurityOnion)
  ↓ Event Bus
Task Creation Workflow (Dispatch/n8n)
  ↓ 
Productivity Tool Update (Mealie/Actual/Goose)
  ↓ Event Bus
Dashboard Notification (Jane UI)
```

**Data Flow:**
1. Security tool detects threat
2. Event published to Event Bus with `SECURITY_ALERT` type
3. n8n workflow subscribed to security domain events triggers
4. Task created in Dispatch incident management
5. Notification sent to relevant productivity tools
6. User dashboard updated via WebSocket

### 6.2 Multi-Tool Synchronization

**Scenario:** Unified threat intelligence sharing

```
MISP Threat Intel Update
  ↓ Event Bus (DATA_UPDATED)
  ├→ HELK (Elasticsearch index update)
  ├→ Security Onion (Alert enrichment)
  ├→ Maltrail (IOC update)
  ├→ YARA-X (Rule compilation)
  └→ Nemesis (File scanning update)
```

**Synchronization Characteristics:**
- Eventual consistency model
- <1s propagation for high-priority events
- Retry logic with exponential backoff
- Conflict resolution via timestamp ordering

### 6.3 Workflow Orchestration

**Scenario:** Automated incident response

```
Trigger: Security Alert Detection
  ↓
n8n Dispatcher Workflow Activation
  ║
  ╠═► IP Reputation Check (VirusTotal, AbuseIPDB)
  ╠═► Domain Reputation (MalwareBazaar, URLhaus)
  ╠═► Hash Analysis (Hybrid Analysis, YARA-X)
  ╠═► CVE Lookup (NVD, GitHub Security)
  ║
  ↓ Aggregation Node
Enriched Alert → Dispatch Incident Creation
  ↓
Task Assignment + Notification
  ↓ Event Bus
Multi-Domain Dashboard Update
```

---

## 7. Integration Technologies Summary

| Technology | Purpose | Tools Integrated | Performance Target |
|------------|---------|------------------|-------------------|
| **Event Bus Service** | Real-time event routing | All 37 tools | <200ms critical events |
| **n8n Workflows** | Adaptive automation | Security + Productivity | <2s workflow trigger |
| **Kafka Streaming** | Security analytics | HELK + Security tools | <1s event processing |
| **Dapr Workflows** | Document processing | Nemesis components | <5s file enrichment |
| **AWS SQS** | Signal consumption | Dispatch security | 20s polling interval |
| **WebSockets** | Real-time UI updates | Jane UI + all tools | <250ms sync latency |
| **Temporal** | Long-running tasks | Goose AI agent | Variable by task |

---

## 8. Data Schemas and Standards

### Event Schema (Event Bus)

```python
{
  "event_id": "uuid",
  "event_type": "EventType enum",
  "source_tool": "string",
  "source_domain": "DomainType enum",
  "target_tools": ["optional tool IDs"],
  "target_domains": ["optional domain IDs"],
  "payload": {
    "entity_type": "string",
    "entity_id": "string",
    "data": {}
  },
  "metadata": {},
  "timestamp": "ISO 8601",
  "priority": "EventPriority enum",
  "ttl_seconds": 300,
  "delivery_required": false,
  "user_id": "optional",
  "session_id": "optional"
}
```

### Workflow Execution Schema (n8n Integration)

```python
{
  "workflow_id": "string",
  "execution_id": "string",
  "trigger_data": {},
  "success": boolean,
  "execution_time": float,
  "output_data": {},
  "error_message": "optional string",
  "node_executions": []
}
```

### CloudEvent Schema (Nemesis)

```python
{
  "specversion": "1.0",
  "type": "com.nemesis.file.enriched",
  "source": "nemesis-document-conversion",
  "id": "uuid",
  "time": "ISO 8601",
  "datacontenttype": "application/json",
  "data": {
    "file_id": "string",
    "enrichment_type": "string",
    "results": {}
  }
}
```

---

## 9. Monitoring and Observability

### Event Bus Metrics

**Real-time Monitoring:**
- Total events published
- Total events delivered
- Total events failed
- Average delivery time (ms)
- Active handler count
- Active WebSocket connection count
- Queue size

**Alerting Thresholds:**
- Delivery time >200ms for CRITICAL events
- Delivery time >1s for HIGH priority events
- Failed event rate >5%
- Queue depth >1000 events

### Workflow Execution Metrics

**n8n Integration:**
- Workflow execution count
- Success rate per workflow
- Average execution time
- Failed execution count
- Active workflow count

**Dapr Workflows:**
- Workflow instance count
- Activity execution time
- Retry attempt tracking
- Workflow state persistence size

### Domain Performance Validation

Per constitutional requirements (NFR-006):

| Domain | Response Time Target | Integration Latency |
|--------|---------------------|---------------------|
| Security | <1s | <200ms event delivery |
| Productivity | <2s | <500ms sync |
| MTG | <3s | <1s data fetch |
| Infrastructure | <5s | <2s orchestration |

---

## 10. Integration Points by Tool

### Security Domain (13 tools)

| Tool | Integration Type | Event Producer | Event Consumer |
|------|-----------------|----------------|----------------|
| **MISP** | Event Bus + API | ✓ Threat Intel | ✓ External feeds |
| **HELK** | Kafka + Event Bus | ✓ Security events | ✓ Log ingestion |
| **Security Onion** | Webhook + Event Bus | ✓ Alerts | ✓ Enrichment |
| **Maltrail** | Event Bus | ✓ IOC detection | ✓ IOC updates |
| **YARA-X** | Event Bus | ✓ Rule matches | ✓ Rule updates |
| **CyberChef** | API + Event Bus | ✗ | ✓ Data transformation requests |
| **Nemesis** | Dapr + Event Bus | ✓ File enrichment | ✓ File submissions |
| **Dispatch** | AWS SQS + Event Bus | ✓ Incidents | ✓ Signals |
| **Ghostwriter** | Event Bus | ✓ Reports | ✓ Findings |
| **APIScout** | Event Bus | ✓ API analysis | ✓ Binary submissions |
| **Brute Ratel** | Event Bus | ✓ C2 activity | ✗ |
| **Hexstrike** | Event Bus | ✓ CVE data | ✓ Vulnerability requests |
| **Meterpreter** | Event Bus | ✓ Session events | ✗ |

**Additional Security Integrations:**

- **Ghostwriter:** Django-based reporting platform with database migrations, static file management, and OAuth integration ready for Event Bus connection
- **Dispatch:** Full incident/case management with 50+ API endpoints, AWS SQS signal consumption, Slack websocket integration, email notifications, and plugin system
- **MISP:** Real-time threat intel sync across instances, extensive ReST API, external feed ingestion, sighting support, and automated attribute enrichment

### Productivity Domain (8 tools)

| Tool | Integration Type | Event Producer | Event Consumer |
|------|-----------------|----------------|----------------|
| **n8n** | Workflow Engine + Event Bus | ✓ Workflow results | ✓ Workflow triggers |
| **Mealie** | Event Bus | ✓ Recipe updates | ✓ Meal planning |
| **Dispatch** | (Shared with Security) | ✓ Tasks | ✓ Task creation |
| **Actual Budget** | Event Bus | ✓ Financial updates | ✓ Budget changes |
| **Firecrawl** | Event Bus | ✓ Crawl results | ✓ Crawl requests |
| **Goose** | Temporal + Event Bus | ✓ Agent actions | ✓ Task assignments |
| **IT-Tools** | Event Bus | ✗ | ✓ Utility requests |
| **Inspector** | Event Bus | ✓ Code analysis | ✓ Analysis requests |

### MTG Domain (4 tools)

| Tool | Integration Type | Event Producer | Event Consumer |
|------|-----------------|----------------|----------------|
| **Commander Spellbook** | Event Bus | ✓ Combo updates | ✓ Card searches |
| **MTG Commander Map** | Event Bus | ✓ Deck analysis | ✓ Deck requests |
| **MTG Scripts** | Event Bus | ✓ Script results | ✓ Automation triggers |
| **MTG Service** | Event Bus | ✓ Card data | ✓ Oracle updates |

### Infrastructure Domain (12 tools)

| Tool | Integration Type | Event Producer | Event Consumer |
|------|-----------------|----------------|----------------|
| **Kong Gateway** | API Gateway | ✗ | ✓ Route config |
| **KasmVNC** | Event Bus | ✓ Session events | ✓ VNC requests |
| **MCP Servers** | MCP Protocol | ✓ Tool calls | ✓ Resource requests |
| **Workflow Automation** | n8n + Event Bus | ✓ Execution results | ✓ Triggers |
| **Chroma DB** | Event Bus | ✓ Vector ops | ✓ Embedding requests |
| **vLLM** | Event Bus | ✓ Completions | ✓ Inference requests |
| **Jupyter** | Dapr | ✓ Notebook results | ✓ Analysis requests |
| **Grafana** | Event Bus | ✗ | ✓ Metrics |
| **Elasticsearch** | HELK Kafka | ✗ | ✓ Index operations |
| **PostgreSQL** | Direct DB | ✗ | ✓ State persistence |
| **Redis** | Cache/Session | ✗ | ✓ Cache operations |
| **MinIO** | Object Storage | ✗ | ✓ File operations |

---

## 11. Use Case Examples

### Use Case 1: Automated Threat Response

**Trigger:** Security Onion detects suspicious network activity

**Event Flow:**
1. Security Onion publishes `THREAT_DETECTED` event (Event Bus)
2. n8n Dispatcher workflow triggered
3. Parallel reputation checks:
   - IP reputation → VirusTotal API
   - Domain reputation → MalwareBazaar
   - Hash analysis → YARA-X
4. Results aggregated in n8n
5. Enriched alert sent to MISP for sharing
6. Incident created in Dispatch
7. Task assigned to analyst via Event Bus
8. Dashboard notification via WebSocket
9. HELK indexes event for threat hunting

**Integration Technologies:** Event Bus, n8n Workflows, HELK Kafka, WebSockets

### Use Case 2: Document Intelligence Pipeline

**Trigger:** New file submitted to Nemesis

**Event Flow:**
1. File uploaded via nemesis-web-api
2. Dapr workflow triggered for document conversion
3. Gotenberg service invoked for PDF generation
4. Tika service extracts text content
5. CloudEvent published with enrichment results
6. PostgreSQL updated with file metadata
7. MinIO stores processed documents
8. Event Bus notifies interested tools (YARA-X, CyberChef)
9. Security scanning triggered if file suspicious
10. Results indexed in Elasticsearch

**Integration Technologies:** Dapr Workflows, CloudEvents, Event Bus, Object Storage

### Use Case 3: Cross-Domain Task Automation

**Trigger:** User creates MTG deck analysis request

**Event Flow:**
1. User submits deck via Jane UI
2. `TASK_CREATED` event published to Event Bus
3. MTG Commander Map analyzes deck composition
4. Commander Spellbook identifies combos
5. Results trigger Goose AI agent
6. Goose generates optimization recommendations
7. n8n workflow creates follow-up tasks
8. Results sent back to user via WebSocket
9. Deck stored in PostgreSQL
10. Analysis cached in Redis

**Integration Technologies:** Event Bus, WebSockets, Temporal Workflows, n8n

---

## 12. Security and Reliability

### Event Bus Security

**Authentication:**
- Handler registration requires service credentials
- WebSocket connections validate user sessions
- Event user_id filtering for multi-tenant isolation

**Authorization:**
- Domain-based access control
- Tool-specific subscription filtering
- Role-based event routing

**Data Protection:**
- Event payload encryption for sensitive data
- TTL-based event expiration
- Audit logging of all event publications

### Reliability Mechanisms

**Fault Tolerance:**
- Retry logic with exponential backoff (max 3 retries)
- Dead letter queues for failed events
- Circuit breakers for failing handlers

**Scalability:**
- Async event processing
- Queue-based buffering
- Horizontal scaling via worker pools

**Monitoring:**
- Real-time metrics dashboards
- Performance alert thresholds
- Health check endpoints for all integrations

---

## 13. Future Enhancements

### Planned Improvements

1. **Enhanced Event Schemas:**
   - JSON Schema validation for all event types
   - Versioned event contracts
   - Backward compatibility guarantees

2. **Advanced Routing:**
   - Content-based routing rules
   - Geographic distribution support
   - Priority-based queue partitioning

3. **Integration Expansion:**
   - GraphQL subscription support
   - gRPC streaming for high-throughput scenarios
   - MQTT for IoT device integration

4. **Observability:**
   - Distributed tracing (OpenTelemetry)
   - Event correlation analysis
   - Performance profiling tools

5. **Resilience:**
   - Multi-region event replication
   - Automated failover mechanisms
   - Event replay capabilities

---

## 14. Developer Guide

### Subscribing to Events

**Python (Event Bus Service):**
```python
from services.event_bus_service import EventBusService, EventType, DomainType

async def my_handler(event: Event):
    print(f"Received event: {event.event_type}")
    # Process event
    
event_bus = EventBusService()
await event_bus.start()

await event_bus.subscribe_handler(
    handler_id="my_tool_handler",
    callback=my_handler,
    event_types={EventType.DATA_UPDATED, EventType.SECURITY_ALERT},
    domain_filter={DomainType.SECURITY}
)
```

### Publishing Events

**Python:**
```python
from services.event_bus_service import Event, EventType, DomainType, EventPriority

event = Event(
    event_type=EventType.THREAT_DETECTED,
    source_tool="my_security_tool",
    source_domain=DomainType.SECURITY,
    target_tools=["helk", "misp"],
    payload={
        "threat_id": "TH-12345",
        "severity": "high",
        "ioc": "192.168.1.100"
    },
    priority=EventPriority.HIGH,
    delivery_required=True
)

await event_bus.publish_event(event)
```

### Creating n8n Workflows

**Workflow Definition:**
```json
{
  "name": "Security Alert Handler",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "security-alert"
      }
    },
    {
      "name": "IP Reputation",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.virustotal.com/v3/ip_addresses/{{$json.ip}}"
      }
    }
  ]
}
```

### Dapr Workflow Activities

**Go (Temporal Service):**
```go
func ProcessDocument(ctx workflow.Context, input DocumentInput) error {
    // Define workflow activities
    var result ConversionResult
    
    err := workflow.ExecuteActivity(
        ctx,
        ConvertToPDF,
        input,
    ).Get(ctx, &result)
    
    if err != nil {
        return err
    }
    
    // Publish event on completion
    event := CloudEvent{
        Type: "document.converted",
        Data: result,
    }
    
    return publishEvent(ctx, event)
}
```

---

## 15. Appendices

### Appendix A: Event Type Reference

Complete enumeration of all Event Bus event types with descriptions and typical use cases.

### Appendix B: Integration Endpoint Catalog

Full API endpoint documentation for all integration points across the 37 tools.

### Appendix C: Performance Benchmarks

Historical performance data for each integration type under various load conditions.

### Appendix D: Troubleshooting Guide

Common integration issues and resolution steps.

---

## Document Metadata

- **Version:** 1.0.0
- **Last Updated:** November 15, 2025
- **Maintainers:** Jane Platform Team
- **Related Documents:**
  - [Architecture Overview](README.md)
  - [Performance Requirements](../specs/functional-requirements.md)
  - [Constitutional Requirements](../.github/copilot-instructions.md)
  - [Migration Tasks](../specs/003-brownfield-integration/tasks.md)

---

## Conclusion

The mental prosthetic platform leverages a sophisticated multi-layered data pipeline architecture to enable seamless communication between 37 diverse tools. The Event Bus Service provides the foundational real-time messaging infrastructure, while specialized integrations like n8n workflows, Dapr orchestration, and Kafka streaming handle domain-specific requirements.

This architecture supports the platform's executive function accommodation goals by:
- Reducing context switching through automated cross-tool synchronization
- Providing real-time feedback via WebSocket connections (<250ms latency)
- Enabling adaptive workflows that respond to user patterns
- Maintaining performance targets across all domains (<1s-5s based on criticality)

All integrations are designed with fault tolerance, observability, and scalability in mind, ensuring the platform can grow to accommodate additional tools while maintaining consistent performance characteristics.

