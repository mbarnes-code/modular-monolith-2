# Jane Monorepo Architecture

This document describes the architecture, design decisions, data flows, and deployment topology of the Jane Monorepo.

## Table of Contents

- [System Overview](#system-overview)
- [Architecture Principles](#architecture-principles)
- [System Components](#system-components)
- [Data Flow](#data-flow)
- [Deployment Topology](#deployment-topology)
- [Infrastructure Architecture](#infrastructure-architecture)
- [Security Architecture](#security-architecture)
- [Scalability Strategy](#scalability-strategy)

## System Overview

The Jane Monorepo is a modular monolith architecture built using NX, containing multiple applications and shared libraries organized by domain. The system provides a unified interface (Jane UI) that orchestrates interactions with specialized LLM servers across different domains (cybersecurity, MTG, code assistance).

### Key Characteristics

- **Monorepo Structure**: Single repository with multiple applications and libraries
- **Domain-Driven Design**: Services and libraries organized by business domain
- **Microservices-Ready**: While monolithic in source, deployable as microservices
- **Event-Driven**: Asynchronous communication patterns where appropriate
- **Cloud-Native**: Designed for Kubernetes deployment

## Architecture Principles

### 1. Separation of Concerns

- **Apps**: Deployable services with specific responsibilities
- **Libs**: Reusable code shared across applications
- **Projects**: Domain-specific documentation and configurations

### 2. Technology Diversity

- **Frontend**: Next.js 15 + React 19 for modern web experience
- **Backend**: FastAPI (Python 3.12) for high-performance APIs
- **LLM Integration**: Specialized servers for domain-specific AI capabilities

### 3. Exact Version Pinning

All dependencies use exact versions (no ^ or ~ in package.json, == in requirements.txt) to ensure:
- Reproducible builds
- Consistent behavior across environments
- Easier debugging and troubleshooting

### 4. Path Aliases

TypeScript path aliases enable clean imports:
```typescript
import { UserType } from '@jane-monorepo/shared/types';
import { Button } from '@jane-monorepo/ui/core';
```

## System Components

### Applications (apps/)

#### 1. Jane UI (`jane-ui`)
- **Technology**: Next.js 15 + React 19
- **Port**: 3000
- **Purpose**: Primary user interface
- **Responsibilities**:
  - User authentication and authorization
  - Request routing to orchestrator
  - Result presentation and visualization
  - Real-time updates via WebSocket

#### 2. Jane Orchestrator (`jane-orchestrator`)
- **Technology**: FastAPI (Python 3.12)
- **Port**: 8000
- **Purpose**: Central coordination service
- **Responsibilities**:
  - Request validation and enrichment
  - LLM server selection and routing
  - Response aggregation
  - Caching and rate limiting
  - Health monitoring

#### 3. Cyber LLM Server (`cyber-llm-server`)
- **Technology**: Python 3.12 + vLLM
- **Port**: 8001
- **Purpose**: Cybersecurity domain LLM
- **Responsibilities**:
  - Threat analysis
  - Vulnerability assessment
  - Security recommendations
  - IOC processing

#### 4. MTG LLM Server (`mtg-llm-server`)
- **Technology**: Python 3.12 + vLLM
- **Port**: 8002
- **Purpose**: Magic: The Gathering domain LLM
- **Responsibilities**:
  - Card interactions
  - Deck building suggestions
  - Rules clarification
  - Combo analysis

#### 5. Code LLM Server (`code-llm-server`)
- **Technology**: Python 3.12 + vLLM
- **Port**: 8003
- **Purpose**: Code assistance LLM
- **Responsibilities**:
  - Code generation
  - Bug detection
  - Refactoring suggestions
  - Documentation generation

### Libraries (libs/)

#### Shared Libraries
- **shared/types**: Common TypeScript types and interfaces
- **shared/utils**: Utility functions used across apps
- **shared/config**: Configuration management

#### Service Adapters
Integration layers for external services:
- Commander Spellbook (MTG combos)
- MISP (Threat intelligence)
- Nemesis (Offensive security)
- Dispatch (Incident management)
- n8n (Workflow automation)
- Scryfall (MTG card data)
- Actual Budget (Personal finance)
- Mealie (Recipe management)
- And more...

#### UI Components
- **ui/core**: Base components (Button, Input, Card, Modal, Table)
- **ui/domain-security**: Security-specific UI components
- **ui/domain-mtg**: MTG-specific UI components
- **ui/domain-finance**: Finance-specific UI components
- **ui/theme**: Theming and design system

## Data Flow

### Request Flow

```
User → Jane UI → Jane Orchestrator → LLM Server(s) → Orchestrator → UI → User
```

### Detailed Flow

1. **User Request**
   - User submits query via Jane UI
   - Client-side validation
   - Request sent to orchestrator

2. **Orchestration**
   - Orchestrator receives request
   - Determines appropriate LLM server(s)
   - Enriches request with context
   - Checks cache for similar queries

3. **LLM Processing**
   - Request forwarded to selected LLM server(s)
   - LLM processes query using domain-specific model
   - Response generated and returned

4. **Response Aggregation**
   - Orchestrator collects responses
   - Aggregates if multiple LLMs used
   - Caches result
   - Returns to UI

5. **Presentation**
   - UI receives response
   - Formats for user display
   - Updates interface
   - Stores in local state if needed

### Data Storage

```
┌─────────────┐
│   Browser   │  (Local Storage, Session Storage)
└──────┬──────┘
       │
┌──────▼──────────────────────────────────┐
│         Jane Orchestrator               │
│  (In-memory cache, Redis for sessions)  │
└──────┬──────────────────────────────────┘
       │
┌──────▼──────┐  ┌──────────┐  ┌──────────┐
│  Cyber LLM  │  │  MTG LLM │  │ Code LLM │
│  (Model)    │  │  (Model) │  │  (Model) │
└─────────────┘  └──────────┘  └──────────┘
```

## Deployment Topology

### Development Environment

```
┌────────────────────────────────────────────────┐
│           Docker Compose (Local)               │
│                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Jane UI  │  │Orchestr. │  │ LLM Srvs │    │
│  │ (1 inst) │  │ (1 inst) │  │(3 inst)  │    │
│  └──────────┘  └──────────┘  └──────────┘    │
└────────────────────────────────────────────────┘
```

### Staging Environment

```
┌────────────────────────────────────────────────┐
│        Kubernetes Cluster (Staging)            │
│                                                │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Jane UI  │  │Orchestr. │  │ LLM Srvs │    │
│  │(2 pods)  │  │(2 pods)  │  │(3x1 pods)│    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │             │             │           │
│  ┌────▼─────────────▼─────────────▼─────┐    │
│  │      Ingress Controller               │    │
│  └───────────────────────────────────────┘    │
└────────────────────────────────────────────────┘
```

### Production Environment

```
┌────────────────────────────────────────────────────────┐
│        Kubernetes Cluster (Production)                 │
│                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Jane UI  │  │Orchestr. │  │ LLM Srvs │            │
│  │(3-10 pods│  │(3-10 pods│  │(3x2 pods)│            │
│  │ + HPA)   │  │ + HPA)   │  │          │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
│       │             │             │                   │
│  ┌────▼─────────────▼─────────────▼─────┐            │
│  │      Ingress + Load Balancer           │            │
│  └────────────────────────────────────────┘            │
│                                                        │
│  ┌────────────────────────────────────────┐            │
│  │   Monitoring Stack (Prometheus,        │            │
│  │   Grafana, Loki, Jaeger)               │            │
│  └────────────────────────────────────────┘            │
└────────────────────────────────────────────────────────┘
```

## Infrastructure Architecture

### Terraform Modules

1. **K3s Cluster**: Lightweight Kubernetes cluster provisioning
2. **Storage**: Persistent volume management
3. **Networking**: VPC, subnets, security groups
4. **Jane Services**: Core application infrastructure
5. **Makoto Services**: Domain services infrastructure
6. **Monitoring**: Observability stack

### Kubernetes Architecture

- **Namespaces**: Logical isolation (jane-services, makoto-services, monitoring)
- **Base Manifests**: Core deployment configurations
- **Overlays**: Environment-specific customizations (dev, staging, production)
- **Kustomize**: Configuration management without templating

## Security Architecture

### Authentication & Authorization

- JWT-based authentication
- Role-based access control (RBAC)
- Service-to-service authentication via mTLS

### Network Security

- Network policies for pod-to-pod communication
- Ingress with TLS termination
- Private subnets for sensitive services

### Secrets Management

- Kubernetes Secrets for sensitive data
- External secrets operator for cloud integration
- Rotation policies for credentials

### Data Security

- Encryption at rest for storage
- Encryption in transit (TLS 1.3)
- Input validation and sanitization
- Rate limiting and DDoS protection

## Scalability Strategy

### Horizontal Scaling

- **UI & Orchestrator**: Auto-scaling based on CPU/memory (HPA)
- **LLM Servers**: Manual scaling based on demand patterns
- **Load Balancing**: Kubernetes service load balancing

### Vertical Scaling

- Resource limits adjusted per environment
- LLM servers require more resources (CPU, memory)
- Database and cache instances sized appropriately

### Caching Strategy

- **Browser**: Local storage for user preferences
- **Orchestrator**: Redis for session and response caching
- **CDN**: Static assets and API responses (when applicable)

### Performance Optimization

- **Code splitting**: Next.js automatic code splitting
- **Lazy loading**: Components loaded on demand
- **Connection pooling**: Database and HTTP connections
- **Async processing**: Background jobs for non-critical tasks

## Monitoring and Observability

### Metrics (Prometheus)

- Request rates, latencies, error rates
- Resource utilization (CPU, memory, disk)
- Custom business metrics

### Logging (Loki)

- Centralized log aggregation
- Structured logging with correlation IDs
- Log levels by environment

### Tracing (Jaeger)

- Distributed tracing across services
- Request flow visualization
- Performance bottleneck identification

### Dashboards (Grafana)

- Pre-configured dashboards for each service
- Alerting rules for critical conditions
- SLO/SLI tracking

## Technology Decisions

### Why NX?

- Monorepo tooling with excellent TypeScript support
- Dependency graph and affected commands
- Caching for faster builds
- Integrated code generation

### Why FastAPI?

- High performance (async/await)
- Automatic API documentation
- Type safety with Pydantic
- Modern Python features

### Why Next.js 15?

- React 19 support with Server Components
- Optimized performance
- Built-in routing and API routes
- Excellent developer experience

### Why K3s?

- Lightweight Kubernetes distribution
- Fast startup and low resource usage
- Production-ready with full Kubernetes API
- Easy to deploy and manage

## Future Considerations

- **Service Mesh**: Istio or Linkerd for advanced traffic management
- **Event Streaming**: Kafka or NATS for event-driven architecture
- **GraphQL**: Federation for unified API layer
- **Multi-region**: Geographic distribution for lower latency
- **ML Ops**: Model versioning and A/B testing infrastructure
