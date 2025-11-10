# Hybrid Domain-Based Architecture: Repository Restructure Plan

**Current State**: NX monorepo skeleton with single `jane-orchestrator` and 37 features in `features/` directory
**Target State**: Hybrid domain-based architecture with 4 domain services + n8n orchestration + specialized AI servers

## Current Structure Analysis

### ✅ What's Already Good:
- **NX Monorepo**: Perfect foundation for hybrid architecture
- **AI Servers**: Already separated by domain (cyber-llm-server, mtg-llm-server, code-llm-server)
- **Service Adapters**: Good pattern in `libs/service-adapters/`
- **Domain UI Components**: Already organized by domain in `libs/ui/`
- **Features Directory**: Clear inventory of 37 tools to migrate

### ❌ What Needs to Change:
- **Monolithic jane-orchestrator**: Split into 4 domain services + n8n workflow service
- **Feature Migration**: Move 37 tools from `features/` into appropriate domain services
- **N8N Integration**: Elevate n8n from feature to central orchestration service
- **Projects Directory**: Restructure to align with domain architecture

## Proposed New Structure

```
apps/
├── n8n-workflow-service/        # NEW: Central orchestration with AI enhancement
│   ├── src/
│   │   ├── workflows/           # Existing n8n workflows
│   │   ├── ai/
│   │   │   ├── pattern-detection.py
│   │   │   ├── workflow-generator.py
│   │   │   └── workflow-optimizer.py
│   │   ├── orchestration/       # Cross-domain coordination
│   │   └── api/                # Domain service communication
│   ├── workflows/              # n8n workflow definitions
│   └── requirements.txt
├── security-service/            # NEW: 13 security tools
│   ├── src/
│   │   ├── api/                # Security domain API
│   │   ├── data/               # Security data models
│   │   ├── services/           # Security business logic
│   │   ├── ai/                 # Security-specific AI/MCP
│   │   └── domains/
│   │       ├── misp/           # MISP integration
│   │       ├── helk/           # HELK integration
│   │       ├── yara/           # YARA-X integration
│   │       ├── cyberchef/      # CyberChef integration
│   │       ├── nemesis/        # Nemesis integration
│   │       ├── ghostwriter/    # Ghostwriter integration
│   │       ├── maltrail/       # Maltrail integration
│   │       ├── securityonion/  # SecurityOnion integration
│   │       ├── rita/           # RITA integration
│   │       ├── blackarch/      # BlackArch tools
│   │       ├── onex/           # OneX toolkit
│   │       ├── brute-ratel/    # Brute Ratel C4
│   │       └── apiscout/       # API Scout
│   ├── requirements.txt
│   └── Dockerfile
├── productivity-service/        # NEW: 8 productivity tools
│   ├── src/
│   │   ├── api/
│   │   ├── data/
│   │   ├── services/
│   │   ├── ai/
│   │   └── domains/
│   │       ├── actual-budget/  # Actual Budget
│   │       ├── mealie/         # Mealie recipe management
│   │       ├── dispatch/       # Incident management
│   │       ├── firecrawl/      # Web scraping
│   │       ├── goose/          # AI coding assistant
│   │       ├── inspector/      # Code inspection
│   │       ├── it-tools/       # IT utilities
│   │       └── kong/           # API Gateway (if productivity-focused)
│   ├── requirements.txt
│   └── Dockerfile
├── mtg-service/                 # NEW: 4 MTG tools
│   ├── src/
│   │   ├── api/
│   │   ├── data/
│   │   ├── services/
│   │   ├── ai/
│   │   └── domains/
│   │       ├── commander-spellbook/     # Commander Spellbook
│   │       ├── mtg-commander-map/       # MTG Commander Map
│   │       ├── mtg-scripting-toolkit/   # MTG Scripting Toolkit
│   │       └── scryfall/               # Scryfall integration
│   ├── requirements.txt
│   └── Dockerfile
├── infrastructure-service/      # NEW: 12 infrastructure tools
│   ├── src/
│   │   ├── api/
│   │   ├── data/
│   │   ├── services/
│   │   ├── ai/
│   │   └── domains/
│   │       ├── kasmvnc/        # Remote desktop
│   │       ├── kong/           # API Gateway (if infra-focused)
│   │       ├── lscript/        # Linux scripting
│   │       ├── software-forensic-kit/
│   │       ├── mcp-servers/    # All MCP servers
│   │       │   ├── chroma-mcp/
│   │       │   ├── filescope-mcp/
│   │       │   ├── firecrawl-mcp/
│   │       │   ├── malwarebazaar-mcp/
│   │       │   ├── mcp-virustotal/
│   │       │   └── n8n-mcp/
│   │       └── meterpreter/    # If infrastructure-focused
│   ├── requirements.txt
│   └── Dockerfile
├── jane-ui/                     # KEEP: Frontend remains unified
│   └── src/
│       └── app/
│           ├── security/        # Security domain pages
│           ├── productivity/    # Productivity domain pages
│           ├── mtg/            # MTG domain pages
│           └── infrastructure/ # Infrastructure domain pages
├── cyber-llm-server/           # KEEP: Security domain AI
├── mtg-llm-server/             # KEEP: MTG domain AI
├── code-llm-server/            # RENAME: infrastructure-llm-server
└── jane-orchestrator/          # REMOVE: Split into domain services
```

## Migration Strategy: 4 Phases

### Phase 1: Create Domain Service Structure (Week 1)
```bash
# Create new domain services
npx nx generate @nx/node:application n8n-workflow-service
npx nx generate @nx/node:application security-service  
npx nx generate @nx/node:application productivity-service
npx nx generate @nx/node:application mtg-service
npx nx generate @nx/node:application infrastructure-service

# Update existing services
mv apps/code-llm-server apps/infrastructure-llm-server
```

### Phase 2: Extract n8n as Central Orchestration Service (Week 2)
```bash
# Move n8n from features/ to central service
mv features/n8n/ apps/n8n-workflow-service/src/workflows/
mv features/n8n-mcp-server/ apps/n8n-workflow-service/src/ai/

# Add AI enhancement components
mkdir -p apps/n8n-workflow-service/src/ai/
# Create pattern-detection.py, workflow-generator.py, workflow-optimizer.py
```

### Phase 3: Migrate Tools to Domain Services (Weeks 3-6)

#### Security Domain Migration (13 tools):
```bash
# High-priority security tools first
mv features/misp/ apps/security-service/src/domains/misp/
mv features/HELK/ apps/security-service/src/domains/helk/
mv features/yara-x/ apps/security-service/src/domains/yara/
mv features/CyberChef/ apps/security-service/src/domains/cyberchef/
mv features/Nemesis/ apps/security-service/src/domains/nemesis/
mv features/Ghostwriter/ apps/security-service/src/domains/ghostwriter/
mv features/maltrail/ apps/security-service/src/domains/maltrail/
mv features/securityonion/ apps/security-service/src/domains/securityonion/
mv features/rita/ apps/security-service/src/domains/rita/
mv features/blackarch/ apps/security-service/src/domains/blackarch/
mv features/onex/ apps/security-service/src/domains/onex/
mv features/Brute-Ratel-C4-Community-Kit/ apps/security-service/src/domains/brute-ratel/
mv features/apiscout/ apps/security-service/src/domains/apiscout/
```

#### Productivity Domain Migration (8 tools):
```bash
mv features/actual/ apps/productivity-service/src/domains/actual-budget/
mv features/mealie/ apps/productivity-service/src/domains/mealie/
mv features/dispatch/ apps/productivity-service/src/domains/dispatch/
mv features/firecrawl/ apps/productivity-service/src/domains/firecrawl/
mv features/goose/ apps/productivity-service/src/domains/goose/
mv features/inspector/ apps/productivity-service/src/domains/inspector/
mv features/it-tools/ apps/productivity-service/src/domains/it-tools/
# Kong placement depends on usage - could be infrastructure
```

#### MTG Domain Migration (4 tools):
```bash
mv features/commander-spellbook-backend/ apps/mtg-service/src/domains/commander-spellbook/
mv features/commander-spellbook-site/ apps/mtg-service/src/domains/commander-spellbook/ 
mv features/mtg-commander-map/ apps/mtg-service/src/domains/mtg-commander-map/
mv features/mtg-scripting-toolkit/ apps/mtg-service/src/domains/mtg-scripting-toolkit/
```

#### Infrastructure Domain Migration (12 tools):
```bash
mv features/KasmVNC/ apps/infrastructure-service/src/domains/kasmvnc/
mv features/kong/ apps/infrastructure-service/src/domains/kong/ # if infra-focused
mv features/lscript/ apps/infrastructure-service/src/domains/lscript/
mv features/software-forensic-kit/ apps/infrastructure-service/src/domains/software-forensic-kit/
mv features/meterpreter/ apps/infrastructure-service/src/domains/meterpreter/

# MCP Servers consolidation
mkdir -p apps/infrastructure-service/src/domains/mcp-servers/
mv features/chroma-mcp/ apps/infrastructure-service/src/domains/mcp-servers/chroma-mcp/
mv features/FileScopeMCP/ apps/infrastructure-service/src/domains/mcp-servers/filescope-mcp/
mv features/firecrawl-mcp-server/ apps/infrastructure-service/src/domains/mcp-servers/firecrawl-mcp/
mv features/MalwareBazaar_MCP/ apps/infrastructure-service/src/domains/mcp-servers/malwarebazaar-mcp/
mv features/mcp-virustotal/ apps/infrastructure-service/src/domains/mcp-servers/mcp-virustotal/
mv features/hexstrike-ai/ apps/infrastructure-service/src/domains/hexstrike-ai/
```

### Phase 4: Service Integration & Testing (Week 7)
```bash
# Update NX project configurations
# Configure inter-service communication
# Set up API contracts between services
# Update docker-compose.yml for 5 services
# Test cross-domain workflows
```

## Updated NX Configuration

### New project.json files needed:
- `apps/n8n-workflow-service/project.json`
- `apps/security-service/project.json`
- `apps/productivity-service/project.json`
- `apps/mtg-service/project.json`
- `apps/infrastructure-service/project.json`

### Updated docker-compose.yml:
```yaml
services:
  n8n-workflow-service:
    build: ./apps/n8n-workflow-service
    ports: ["8010:8000"]
  security-service:
    build: ./apps/security-service
    ports: ["8011:8000"]
  productivity-service:
    build: ./apps/productivity-service
    ports: ["8012:8000"]
  mtg-service:
    build: ./apps/mtg-service
    ports: ["8013:8000"]
  infrastructure-service:
    build: ./apps/infrastructure-service
    ports: ["8014:8000"]
  jane-ui:
    build: ./apps/jane-ui
    ports: ["3000:3000"]
  cyber-llm-server:
    build: ./apps/cyber-llm-server
    ports: ["8001:8000"]
  mtg-llm-server:
    build: ./apps/mtg-llm-server
    ports: ["8002:8000"]
  infrastructure-llm-server:
    build: ./apps/infrastructure-llm-server
    ports: ["8003:8000"]
```

## Service Communication Architecture

### API Communication Pattern:
```
jane-ui → n8n-workflow-service → domain-services
cyber-llm-server → n8n-workflow-service → security-service
mtg-llm-server → n8n-workflow-service → mtg-service
infrastructure-llm-server → n8n-workflow-service → infrastructure-service
```

### Inter-Service APIs:
- **n8n-workflow-service**: `:8010` - Central orchestration
- **security-service**: `:8011` - Security domain operations
- **productivity-service**: `:8012` - Productivity domain operations
- **mtg-service**: `:8013` - MTG domain operations
- **infrastructure-service**: `:8014` - Infrastructure domain operations

## Benefits of This Restructure

### ✅ Aligns with Your Requirements:
- **Parallel AI Operations**: Domain services enable parallel execution
- **n8n Central Orchestration**: Dedicated n8n service with AI enhancement
- **60/40 Performance Split**: AI-optimized service communication
- **Adaptive Workflow Creation**: AI-enhanced n8n service

### ✅ Migration Safety:
- **Domain Isolation**: Tool migration failures contained per domain
- **Incremental Deployment**: Can deploy domain by domain
- **Clear Boundaries**: Each domain has specific tool responsibility

### ✅ Future Scalability:
- **Independent Scaling**: Scale security operations without affecting MTG
- **Technology Flexibility**: Each domain can use optimal tech stack
- **Multi-Device Ready**: Services can be distributed across devices

## Validation Criteria

### Phase Completion Checkpoints:
1. **Phase 1**: All 5 services created and NX builds successfully
2. **Phase 2**: n8n service operational with AI enhancement components
3. **Phase 3**: All 37 tools moved from features/ directory (empty directory = success)
4. **Phase 4**: Cross-domain workflows executing via n8n orchestration

### Success Metrics:
- **features/ directory**: EMPTY (100% tool migration)
- **Build Success**: All 5 services + 3 AI servers + jane-ui build successfully
- **API Communication**: All inter-service APIs responding
- **Workflow Execution**: AI can trigger parallel domain operations
- **Performance**: Meeting 60/40 AI/UI performance targets

This restructure transforms your skeleton into a true hybrid domain-based architecture that supports your AI-first workflow patterns with n8n orchestration and parallel execution capabilities.