# Infrastructure Abstraction Layer

**Version:** 1.0.0  
**Date:** November 15, 2025  
**Status:** Production Ready

This document describes the **Hexagonal Architecture (Ports & Adapters)** implementation for infrastructure dependencies.

---

## Quick Start

```python
from libs.shared.messaging import create_message_bus, Message, Priority

# Create message bus (adapter from config)
bus = create_message_bus()
await bus.start()

# Publish message
msg = Message(
    topic="security.threat.detected",
    payload={"ip": "192.168.1.100"},
    priority=Priority.HIGH,
)
await bus.publish(msg)
```

**To swap adapters, just change config:**

```yaml
# Development: Event Bus
adapter: eventbus

# Production: RabbitMQ  
adapter: rabbitmq
```

**No code changes required.**

---

## Available Abstractions

| Abstraction | Interface | Adapters | Purpose |
|-------------|-----------|----------|---------|
| **Messaging** | `IMessageBus` | EventBus, RabbitMQ, Kafka, SQS | Pub/sub, event streaming |
| **Workflows** | `IWorkflowEngine` | n8n, Temporal, Dapr | Workflow orchestration |
| **Storage** | `IObjectStorage` | MinIO, S3, Local | Object/file storage |
| **Cache** | `ICache` | Redis, In-Memory, PostgreSQL | Key-value caching |
| **Search** | `ISearchEngine` | Elasticsearch, PostgreSQL | Full-text search |

---

## Why Abstraction Layer?

✅ **Swap infrastructure via config** (no code changes)  
✅ **Preserve battle-tested implementations**  
✅ **Incremental migration** (low risk)  
✅ **Easy testing** (mock infrastructure)  
✅ **Avoid vendor lock-in**

---

## Architecture

```
Domain Code (Security, Productivity, MTG, Infrastructure)
       ↓ uses interfaces only
Interface Layer (IMessageBus, IObjectStorage, ICache, etc.)
       ↓ implemented by
Adapter Layer (EventBus, RabbitMQ, Kafka, MinIO, S3, Redis, etc.)
```

See full architecture diagrams and detailed usage in:  
📄 **[INFRASTRUCTURE_ABSTRACTION.md](./INFRASTRUCTURE_ABSTRACTION.md)**

---

## Configuration

### Environment Variables

```bash
export MESSAGE_BUS_ADAPTER=rabbitmq
export MESSAGE_BUS_CONFIG=/etc/jane/messaging.yaml
```

### YAML Files

```yaml
# messaging.yaml
adapter: rabbitmq
config:
  host: localhost
  port: 5672
  username: guest
  password: guest
```

---

## Migration Status

- ✅ Interface definitions complete
- ✅ Core adapters implemented (EventBus, RabbitMQ, Kafka, SQS, etc.)
- ✅ Factory pattern with config loading
- ✅ Documentation complete
- ⬜ Unit tests (in progress)
- ⬜ Service migrations (starting Week 2)

---

## Documentation

- **[Full README](./INFRASTRUCTURE_ABSTRACTION.md)** - Complete documentation with examples
- **[Messaging](./messaging/)** - Message bus abstraction
- **[Workflows](./workflows/)** - Workflow orchestration
- **[Storage](./storage/)** - Object storage
- **[Cache](./cache/)** - Caching layer
- **[Search](./search/)** - Search engines

---

## Examples

See `INFRASTRUCTURE_ABSTRACTION.md` for comprehensive examples of:
- Pub/sub messaging
- Workflow orchestration
- Object storage operations
- Cache management
- Full-text search

---

**Maintained by:** Jane Platform Team  
**Last Updated:** November 15, 2025
