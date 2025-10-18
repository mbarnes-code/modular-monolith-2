# Mental Prosthetic Platform - Developer Quickstart

**Version**: 1.0.0  
**Last Updated**: 2025-10-18  
**Prerequisites**: Node.js 20, Python 3.12, Docker (optional)

## Overview

The Mental Prosthetic Platform consolidates 37 executive function tools into a unified interface designed specifically for ADHD/autism support. This quickstart guide helps developers understand, run, and contribute to the platform.

## Architecture Summary

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Jane UI       │    │ Jane Orchestrator│    │  LLM Servers    │
│ (Next.js 15)    │◄──►│   (FastAPI)      │◄──►│  (vLLM 0.11)    │
│                 │    │                  │    │                 │
│ - Unified       │    │ - API Gateway    │    │ - Security AI   │
│   Dashboard     │    │ - Service        │    │ - MTG AI        │
│ - Tool UIs      │    │   Adapters       │    │ - Code AI       │
│ - AI Chat       │    │ - WebSocket      │    │                 │
└─────────────────┘    │   Handling       │    └─────────────────┘
                       └──────────────────┘              │
                               │                         │
                    ┌──────────▼──────────┐              │
                    │   Service Adapters  │              │
                    │                     │              │
                    │ ┌─────────────────┐ │              │
                    │ │   Security      │ │              │
                    │ │   - MISP        │ │              │
                    │ │   - Nemesis     │ │              │
                    │ │   - HELK        │ │              │
                    │ └─────────────────┘ │              │
                    │ ┌─────────────────┐ │              │
                    │ │ Productivity    │ │              │
                    │ │   - n8n         │ │              │
                    │ │   - actual      │ │              │
                    │ │   - mealie      │ │              │
                    │ └─────────────────┘ │              │
                    │ ┌─────────────────┐ │              │
                    │ │     MTG         │ │              │
                    │ │ - commander-    │ │              │
                    │ │   spellbook     │ │              │
                    │ └─────────────────┘ │              │
                    └─────────────────────┘              │
                               │                         │
                    ┌──────────▼──────────┐              │
                    │     Data Layer      │              │
                    │                     │              │
                    │ ┌─────────────────┐ │              │
                    │ │   PostgreSQL    │ │              │
                    │ │ (Transactional) │ │              │
                    │ └─────────────────┘ │              │
                    │ ┌─────────────────┐ │              │
                    │ │   Chroma DB     │ │◄─────────────┘
                    │ │  (Embeddings)   │ │
                    │ └─────────────────┘ │
                    │ ┌─────────────────┐ │
                    │ │ Synology NAS    │ │
                    │ │   (Backups)     │ │
                    │ └─────────────────┘ │
                    └─────────────────────┘
```

## Quick Start

### 1. Environment Setup

```bash
# Clone and navigate to repository
cd /workspaces/modular-monolith-2

# Install dependencies
npm install
make install

# Set up environment variables
cp .env.example .env
# Edit .env with your local configuration
```

### 2. Database Setup

```bash
# Start PostgreSQL (if using Docker)
docker run -d \
  --name mental-prosthetic-postgres \
  -e POSTGRES_DB=mental_prosthetic \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=secure_password \
  -p 5432:5432 \
  postgres:15

# Run database migrations
cd apps/jane-orchestrator
python -m alembic upgrade head
```

### 3. Start Core Services

```bash
# Terminal 1: Start Jane Orchestrator (API Backend)
npx nx serve jane-orchestrator
# Available at: http://localhost:8000

# Terminal 2: Start Jane UI (Frontend)  
npx nx serve jane-ui
# Available at: http://localhost:3000

# Terminal 3: Start LLM Servers (optional for development)
npx nx serve cyber-llm-server    # Port 8001
npx nx serve mtg-llm-server      # Port 8002  
npx nx serve code-llm-server     # Port 8003
```

### 4. Verify Installation

```bash
# Check API health
curl http://localhost:8000/health

# Check UI access
open http://localhost:3000

# Check WebSocket connections
# AI WebSocket: ws://localhost:8000/ws/ai
# Sync WebSocket: ws://localhost:8000/ws/sync
```

## Development Workflow

### Integration Status Dashboard

The platform tracks integration of all 37 projects from `features/` directory:

```bash
# Check integration status
curl http://localhost:8000/api/tools | jq '.[] | {name, domain, integrationStatus}'

# View integration progress
http://localhost:3000/dashboard/integration
```

### Working with Service Adapters

Service adapters in `libs/service-adapters/` handle integration of tools from `features/`:

```typescript
// Example: Creating a new security tool adapter
// libs/service-adapters/security/misp-adapter.ts

import { BaseAdapter } from '../base-adapter';
import { MISPConfig, ThreatIndicator } from './types';

export class MISPAdapter extends BaseAdapter {
  async initialize(config: MISPConfig): Promise<void> {
    // Initialize MISP connection using business logic from features/MISP/
  }
  
  async getThreatIndicators(): Promise<ThreatIndicator[]> {
    // Preserve original MISP functionality
  }
}
```

### AI Integration Development

```typescript
// Working with AI context for executive function support
// apps/jane-orchestrator/src/services/ai-context.ts

export class AIContextService {
  async analyzeUserState(userId: string): Promise<ExecutiveFunctionState> {
    // Analyze user patterns for ADHD/autism support
  }
  
  async generateTaskBreakdown(
    task: Task, 
    userPreferences: ADHDSettings
  ): Promise<TaskBreakdown> {
    // Generate appropriate task breakdown based on user needs
  }
}
```

### UI Component Development

```tsx
// Creating executive function-focused components
// libs/ui/core/src/executive-function/task-breakdown.tsx

export interface TaskBreakdownProps {
  task: Task;
  userSettings: ADHDSettings;
  onSubtaskComplete: (subtaskId: string) => void;
}

export const TaskBreakdown: React.FC<TaskBreakdownProps> = ({
  task,
  userSettings,
  onSubtaskComplete
}) => {
  // Component optimized for ADHD/autism users
  return (
    <div className="task-breakdown">
      {/* Clear, structured layout */}
      {/* Minimal cognitive load */}
      {/* Progress indicators */}
    </div>
  );
};
```

## Testing Strategy

### Unit Tests
```bash
# Frontend tests
npx nx test jane-ui

# Backend tests  
cd apps/jane-orchestrator
pytest tests/unit/

# Service adapter tests
npx nx test service-adapters-security
```

### Integration Tests
```bash
# API contract tests
cd apps/jane-orchestrator
pytest tests/integration/test_api_contracts.py

# WebSocket tests
pytest tests/integration/test_websocket_ai.py
pytest tests/integration/test_websocket_sync.py

# Cross-tool integration tests
pytest tests/integration/test_service_adapters.py
```

### End-to-End Tests
```bash
# Full user journey tests
npx nx e2e jane-ui-e2e

# Executive function workflow tests
npx playwright test tests/e2e/executive-function-workflows.spec.ts
```

## Configuration

### Environment Variables

```bash
# Core Services
JANE_UI_PORT=3000
JANE_ORCHESTRATOR_PORT=8000
JANE_ORCHESTRATOR_HOST=0.0.0.0

# Database
DATABASE_URL=postgresql://admin:secure_password@localhost:5432/mental_prosthetic
CHROMA_DB_PATH=./data/chroma

# LLM Servers
CYBER_LLM_SERVER_URL=http://localhost:8001
MTG_LLM_SERVER_URL=http://localhost:8002
CODE_LLM_SERVER_URL=http://localhost:8003

# Security
JWT_SECRET=your-super-secret-jwt-key
JWT_EXPIRATION=24h
CORS_ORIGINS=http://localhost:3000

# Synology NAS Integration
SYNOLOGY_HOST=your-nas-ip
SYNOLOGY_USERNAME=your-username
SYNOLOGY_PASSWORD=your-password

# Feature Integration
FEATURES_SOURCE_DIR=./features
INTEGRATION_BATCH_SIZE=5
```

### Constitution Compliance

The platform enforces strict constitution compliance:

```bash
# Check code quality
npx nx lint jane-ui
npx nx lint jane-orchestrator

# Run type checking
npx nx type-check jane-ui
cd apps/jane-orchestrator && mypy src/

# Performance testing
npx nx test:performance jane-ui
pytest tests/performance/
```

## API Usage Examples

### Authentication
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Use returned JWT token for subsequent requests
export TOKEN="your-jwt-token"
```

### Task Management
```bash
# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Organize security tools",
    "description": "Consolidate MISP and Nemesis data",
    "priority": "High",
    "sourceToolId": "uuid-of-security-adapter",
    "executiveFunctionType": "Organization"
  }'

# Get AI task breakdown
curl -X POST http://localhost:8000/api/ai/task-breakdown \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "taskId": "task-uuid",
    "complexity": "Adaptive"
  }'
```

### Tool Integration Status
```bash
# List all tools
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/tools"

# Check specific tool status
curl -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/tools/tool-uuid/status"

# Execute tool action
curl -X POST http://localhost:8000/api/adapters/security/analyze-threat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"indicators": ["malicious-ip"], "severity": "High"}'
```

## Troubleshooting

### Common Issues

**WebSocket Connection Fails**:
```bash
# Check if JWT token is properly included
# Verify CORS settings in jane-orchestrator
# Ensure WebSocket endpoint is accessible
```

**Service Adapter Not Loading**:
```bash
# Verify adapter module exists in libs/service-adapters/
# Check integration status in database
# Review adapter initialization logs
```

**AI Responses Slow**:
```bash
# Check LLM server status: curl http://localhost:8001/health
# Monitor GPU memory usage
# Review WebSocket message queue
```

**Database Connection Issues**:
```bash
# Verify PostgreSQL is running
# Check connection string in .env
# Run database migrations
```

### Monitoring and Logs

```bash
# Application logs
docker logs mental-prosthetic-app

# Database logs
docker logs mental-prosthetic-postgres

# Real-time performance monitoring
curl http://localhost:8000/api/metrics
```

## Contributing

### Integration Development Process

1. **Analyze existing tool** in `features/` directory
2. **Review analysis documentation** in `docs/modular-analysis-repo-main/`
3. **Create service adapter** in appropriate domain
4. **Implement UI components** in `libs/ui/`
5. **Add API endpoints** to jane-orchestrator
6. **Write comprehensive tests**
7. **Update integration status** tracking
8. **Verify features/ directory cleanup**

### Code Standards

- TypeScript strict mode enabled
- Python type hints required
- 80%+ test coverage
- OpenAPI specifications for all endpoints
- WCAG 2.1 AA accessibility compliance
- Response times: <200ms UI, <500ms API

### Pull Request Process

1. Ensure constitution compliance checks pass
2. Include integration tests for new adapters  
3. Update API documentation
4. Add user-facing documentation
5. Verify no business logic loss during integration

## Support

- **Documentation**: `/docs/`
- **API Reference**: `http://localhost:8000/docs` (Swagger UI)
- **Integration Status**: `http://localhost:3000/dashboard/integration`
- **Health Checks**: `http://localhost:8000/health`

## Next Steps

1. **Review existing features**: Explore the `features/` directory to understand tools being integrated
2. **Study analysis docs**: Read documentation in `docs/modular-analysis-repo-main/`
3. **Start with one adapter**: Pick a simple tool and create its service adapter
4. **Test integration**: Verify the tool works within the unified platform
5. **Add AI enhancement**: Connect the tool to AI context for executive function support