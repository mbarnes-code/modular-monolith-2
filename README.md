# Jane Monorepo - Mental Prosthetic Platform

An NX monorepo implementing a hybrid domain-based architecture with 4 domain services, n8n workflow orchestration, Next.js 15 + React 19 UI, and specialized LLM servers for AI-first executive function support.

## Hybrid Domain-Based Architecture

**Current State**: Skeleton structure ready for migration to hybrid architecture
**Target State**: 4 domain services + n8n orchestration + specialized AI servers

```
jane-monorepo/
├── .github/                 # GitHub configuration (workflows, issue templates)
├── apps/
│   ├── n8n-workflow-service/     # Central orchestration with AI enhancement (NEW)
│   ├── security-service/         # Security domain - 13 tools (NEW)
│   ├── productivity-service/     # Productivity domain - 8 tools (NEW)
│   ├── mtg-service/             # MTG domain - 4 tools (NEW)
│   ├── infrastructure-service/  # Infrastructure domain - 12 tools (NEW)
│   ├── jane-ui/                 # Next.js 15 + React 19 unified interface
│   ├── cyber-llm-server/        # Security domain AI (Python vLLM)
│   ├── mtg-llm-server/          # MTG domain AI (Python vLLM)
│   ├── infrastructure-llm-server/ # Infrastructure domain AI (Python vLLM)
│   └── jane-orchestrator/       # LEGACY: To be removed after migration
├── docs/                    # Documentation files
│   ├── base skeleton version docs/  # Base documentation and setup guides
│   └── modular-analysis-repo-main/  # Analysis and architectural documentation
├── features/                # Feature implementations and integrations
│   ├── actual/              # Actual Budget integration
│   ├── apiscout/            # API Scout tool
│   ├── blackarch/           # BlackArch Linux tools
│   ├── Brute-Ratel-C4-Community-Kit/  # Brute Ratel C4 toolkit
│   ├── chroma-mcp/          # Chroma MCP server
│   ├── commander-spellbook-backend/    # MTG Commander Spellbook API
│   ├── commander-spellbook-site/       # MTG Commander Spellbook UI
│   ├── CyberChef/           # CyberChef data operations
│   ├── dispatch/            # Incident management
│   ├── FileScopeMCP/        # File scope MCP server
│   ├── firecrawl/           # Web scraping service
│   ├── firecrawl-mcp-server/           # Firecrawl MCP integration
│   ├── Ghostwriter/         # Penetration testing reporting
│   ├── goose/               # AI coding assistant
│   ├── HELK/                # Hunting ELK stack
│   ├── hexstrike-ai/        # AI-powered security tools
│   ├── inspector/           # Code inspection tools
│   ├── it-tools/            # IT utility tools
│   ├── KasmVNC/             # Remote desktop solution
│   ├── kong/                # API Gateway
│   ├── lscript/             # Linux scripting tools
│   ├── maltrail/            # Malware detection
│   ├── MalwareBazaar_MCP/   # Malware analysis MCP
│   ├── mcp-virustotal/      # VirusTotal MCP integration
│   ├── mealie/              # Recipe management
│   ├── meterpreter/         # Meterpreter payloads
│   ├── MISP/                # Malware Information Sharing Platform
│   ├── mtg-commander-map/   # MTG Commander mapping tools
│   ├── mtg-scripting-toolkit/          # MTG scripting utilities
│   ├── n8n/                # Workflow automation
│   ├── n8n-mcp-server/      # n8n MCP integration
│   ├── Nemesis/             # Post-exploitation framework
│   ├── onex/                # Security exploitation toolkit
│   ├── rita/                # Real Intelligence Threat Analytics
│   ├── securityonion/       # Network security monitoring
│   ├── securityonion-n8n-workflows/    # Security Onion automation
│   ├── software-forensic-kit/          # Digital forensics tools
│   └── yara-x/              # YARA rule engine
├── libs/
│   ├── shared/
│   │   ├── types/           # Shared TypeScript types
│   │   ├── utils/           # Shared utility functions
│   │   └── config/          # Configuration management
│   ├── service-adapters/    # Service integration adapters
│   │   ├── actual-budget/   # Actual Budget adapter
│   │   ├── commander-spellbook/        # Commander Spellbook adapter
│   │   ├── dispatch/        # Dispatch adapter
│   │   ├── firecrawl/       # Firecrawl adapter
│   │   ├── ghostwriter/     # Ghostwriter adapter
│   │   ├── goose/           # Goose adapter
│   │   ├── helk/            # HELK adapter
│   │   ├── kasmvnc/         # KasmVNC adapter
│   │   ├── mealie/          # Mealie adapter
│   │   ├── misp/            # MISP adapter
│   │   ├── n8n/             # n8n adapter
│   │   ├── nemesis/         # Nemesis adapter
│   │   └── scryfall/        # Scryfall MTG API adapter
│   └── ui/
│       ├── core/            # Core UI components (Button, Input, Card, Modal, Table)
│       ├── domain-security/ # Security domain UI (ThreatIndicator, SeverityBadge, IOCDisplay, IncidentCard)
│       ├── domain-mtg/      # MTG domain UI (ComboCard, ManaSymbol, ColorIdentityBadge)
│       ├── domain-finance/  # Finance domain UI (BudgetChart, TransactionList)
│       ├── domain-productivity/        # Productivity domain UI components
│       └── theme/           # Theme configuration (colors, typography, tailwind)
├── projects/
│   ├── security/            # Security project files
│   │   ├── misp/
│   │   ├── nemesis/
│   │   ├── yara-x/
│   │   ├── hexstrike-ai/
│   │   ├── dispatch/
│   │   ├── ghostwriter/
│   │   ├── helk/
│   │   ├── rita/
│   │   ├── blackarch/
│   │   ├── onex/
│   │   └── software-forensic-kit/
│   ├── mtg/                 # MTG project files
│   │   ├── commander-spellbook-backend/
│   │   ├── commander-spellbook-frontend/
│   │   └── mtg-scripting-toolkit/
│   ├── productivity/        # Productivity project files
│   │   ├── n8n/
│   │   ├── actual-budget/
│   │   ├── mealie/
│   │   └── firecrawl/
│   ├── dev-tools/           # Developer tools
│   │   ├── goose/
│   │   ├── inspector/
│   │   └── it-tools/
│   └── infrastructure/      # Infrastructure integrations
│       └── kasmvnc/
└── infrastructure/
    ├── terraform/           # Terraform IaC
    ├── kubernetes/          # Kubernetes manifests
    └── docker/              # Docker configurations

```

## Technology Stack

- **Node.js**: 20
- **Python**: 3.12
- **TypeScript**: 5.9.3
- **Next.js**: 15.5.4
- **React**: 19.2.0
- **FastAPI**: 0.119.0 
- **Django**: 5.2.7 
- **SQLAlchemy**: 2.0.44 
- **Pydantic**: 2.12.0 
- **Uvicorn**: 0.37.0 
- **vLLM**: 0.11.0 
- **NX**: 21.6.4 
- **Rust**: 1.70+ (for specific integrations)
- **Java**: 17 LTS (for specific integrations)

## Prerequisites

- Node.js 20.x
- Python 3.12.x
- npm

## Quick Start (Codespace/New Environment)

For new codespaces or fresh environments, use our automated setup scripts:

### 🚀 Full Setup (Recommended)

```bash
./setup-codespace.sh
```

This script will:

- Update and upgrade system packages
- Install UV (modern Python package installer)
- Install specify-cli for project specification management
- Install all Node.js and Python dependencies
- Verify all tools and configurations
- Set up environment files
- Test basic functionality

### ⚡ Quick Setup (Minimal)

```bash
./quick-setup.sh
```

A faster version that installs only the essentials.

### 🔧 Manual Setup

If you prefer manual installation:

1. Install Node.js dependencies:

   ```bash
   npm install
   ```

2. Install Python dependencies using the Makefile:

   ```bash
   make install
   ```

   Or manually for each service:

   ```bash
   pip install -r apps/jane-orchestrator/requirements.txt
   pip install -r apps/cyber-llm-server/requirements.txt
   pip install -r apps/mtg-llm-server/requirements.txt
   pip install -r apps/code-llm-server/requirements.txt
   ```

## Running Applications

### Hybrid Architecture Services

**Central Orchestration:**
```bash
npx nx serve n8n-workflow-service   # Port 8010 (NEW)
```

**Domain Services:**
```bash
npx nx serve security-service        # Port 8011 (NEW)
npx nx serve productivity-service    # Port 8012 (NEW)  
npx nx serve mtg-service            # Port 8013 (NEW)
npx nx serve infrastructure-service  # Port 8014 (NEW)
```

**Frontend:**
```bash
npx nx serve jane-ui                # Port 3000
```

**AI Servers:**
```bash
npx nx serve cyber-llm-server       # Port 8001 (Security AI)
npx nx serve mtg-llm-server         # Port 8002 (MTG AI)
npx nx serve infrastructure-llm-server # Port 8003 (Infrastructure AI)
```

**Legacy (Remove after migration):**
```bash
npx nx serve jane-orchestrator      # Port 8000 (DEPRECATED)
```

### Using Docker Compose

```bash
cd infrastructure/docker
docker-compose up
```

## Building

Build all applications:

```bash
npx nx run-many --target=build --all
```

Build specific application:

```bash
npx nx build jane-ui
```

## Project Structure

## Migration Status

**Current Phase**: Ready for hybrid architecture migration

### Migration Steps:
1. **✅ Planning Complete**: Hybrid domain-based architecture designed
2. **🔄 Ready to Execute**: 37 tools in `features/` directory ready for migration
3. **⏳ Pending**: Create 5 new services (n8n-workflow + 4 domains)
4. **⏳ Pending**: Migrate tools from `features/` to domain services
5. **⏳ Pending**: Implement n8n orchestration with AI enhancement
6. **⏳ Pending**: Remove legacy `jane-orchestrator`

### Success Criteria:
- ✅ **features/ directory empty** (all 37 tools migrated)
- ⏳ **5 services operational** (n8n + 4 domains)
- ⏳ **AI-first workflows** executing via n8n orchestration
- ⏳ **60/40 performance split** (AI speed prioritized over UI)

See `specs/002-mental-prosthetic-refinement/implementation-guide.md` for detailed migration commands.

## Project Structure

This monorepo follows NX best practices with hybrid domain-based architecture:

- **apps/**: Domain services + AI servers + unified UI
- **libs/**: Shared libraries and domain-specific components
- **features/**: 37 tools awaiting migration (target: empty directory)
- **infrastructure/**: Infrastructure as Code (IaC) and deployment configurations
