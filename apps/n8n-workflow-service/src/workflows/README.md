# n8n Workflow Engine Directory

This directory will contain the n8n workflow automation engine - the heart of the orchestration system.

## Migration Instructions

When migrating from `features/n8n/`, this becomes the central orchestration service:

### Core n8n Components
- **Workflow Engine**: Move n8n's TypeScript workflow execution engine
- **Node Definitions**: All custom and built-in node types
- **Workflow Database**: Workflow definitions and execution history
- **API Server**: n8n's REST API and WebSocket connections
- **UI Components**: Workflow editor (if keeping web interface)

### Key Files to Migrate
- `features/n8n/packages/core/` → Core workflow execution engine
- `features/n8n/packages/nodes-base/` → Standard node definitions
- `features/n8n/packages/editor-ui/` → Workflow editor interface
- `features/n8n/packages/cli/` → Command-line interface and server

### AI Enhancement Integration
- **Pattern Detection**: `../ai/pattern_detection.py` monitors user requests
- **Workflow Generation**: `../ai/workflow_generator.py` creates workflows
- **Cross-Domain Orchestration**: `../orchestration/` coordinates domain services

### Domain Service Integration
- **Security Service**: Create security-specific n8n nodes
- **Productivity Service**: Create productivity workflow nodes  
- **MTG Service**: Create MTG analysis nodes
- **Infrastructure Service**: Create infrastructure operation nodes

### Performance Requirements
- Simple workflows: <500ms execution time
- Complex workflows: <2s execution time
- 60% performance budget allocated to AI speed
- Parallel execution across domain services

## TODO: Delete this README when migration is complete

This is the most critical migration - n8n becomes the central nervous system of the hybrid architecture.