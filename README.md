# Jane Monorepo - Mental Prosthetic Platform

An NX monorepo implementing a hybrid domain-based architecture with 4 domain services, n8n workflow orchestration, Next.js 15 + React 19 UI, and specialized LLM servers for AI-first executive function support.

## DDD based Hybrid Domain-Based Architecture

**Current State**: Active migration to hybrid architecture in progress
**Target State**: 4 domain services + n8n orchestration + specialized AI servers

```
modular-monolith-2/
├── .github/                 # GitHub configuration (workflows, issue templates)
├── apps/
│   ├── core/                # Core infrastructure applications
│   │   ├── jane-orchestrator/       # LEGACY: Central FastAPI backend (to be phased out)
│   │   ├── jane-ui/                 # Next.js 15 + React 19 unified interface
│   │   └── infrastructure-service/  # Infrastructure domain - 12 tools
│   ├── ai/                  # Specialized LLM servers
│   │   ├── cyber-llm-server/        # Security domain AI (Python vLLM)
│   │   ├── mtg-llm-server/          # MTG domain AI (Python vLLM)
│   │   └── infrastructure-llm-server/ # Infrastructure domain AI (Python vLLM)
│   ├── security/            # Security domain - 13 tools
│   │   ├── security-service/        # Domain aggregation service
│   │   ├── misp-service/            # Malware Information Sharing Platform
│   │   ├── nemesis-service/         # Post-exploitation framework
│   │   ├── nemesis-web-api/         # Nemesis web API
│   │   ├── nemesis-frontend/        # Nemesis UI
│   │   ├── nemesis-file-enrichment/ # Nemesis file processing
│   │   ├── nemesis-document-conversion/ # Nemesis document processing
│   │   ├── yara-x-service/          # YARA rule engine
│   │   ├── cyberchef-service/       # CyberChef data operations
│   │   ├── dispatch-service/        # Incident management
│   │   ├── ghostwriter-service/     # Penetration testing reporting
│   │   ├── helk-service/            # Hunting ELK stack
│   │   ├── kasmvnc-service/         # Remote desktop solution
│   │   ├── maltrail-service/        # Malware detection
│   │   ├── hexstrike-service/       # AI-powered security tools
│   │   ├── blackarch-service/       # BlackArch Linux tools
│   │   ├── apiscout-service/        # API Scout tool
│   │   ├── brute-ratel-service/     # Brute Ratel C4 toolkit
│   │   ├── meterpreter-service/     # Meterpreter payloads
│   │   └── software-forensic-kit-service/ # Digital forensics tools
│   ├── productivity/        # Productivity domain - 8 tools
│   │   ├── productivity-service/    # Domain aggregation service
│   │   ├── n8n-service/             # Workflow automation
│   │   ├── n8n-workflow-service/    # Central orchestration with AI enhancement
│   │   ├── actual-service/          # Actual Budget integration
│   │   ├── mealie-service/          # Recipe management
│   │   ├── firecrawl-service/       # Web scraping service
│   │   ├── goose-service/           # AI coding assistant
│   │   ├── goose-ui/                # Goose frontend
│   │   ├── goose-docs/              # Goose documentation
│   │   ├── goose-temporal-service/  # Goose workflow engine
│   │   ├── inspector-service/       # Code inspection tools
│   │   └── onex-service/            # Security exploitation toolkit
│   └── tcg/                 # Trading Card Game domain - 4 tools
│       ├── mtg-service/             # Domain aggregation service
│       ├── commander-spellbook-backend/ # MTG Commander Spellbook API
│       ├── commander-spellbook-site/    # MTG Commander Spellbook UI
│       ├── mtg-commander-map-service/   # MTG Commander mapping tools
│       └── mtg-scripts/             # MTG scripting utilities
├── libs/
│   ├── shared/              # Shared utilities and types
│   ├── ui/                  # Shared UI components and design system
│   ├── service-adapters/    # Service integration adapters for all 37 tools
│   ├── blackarch/           # BlackArch integration libraries
│   ├── dispatch-core/       # Dispatch core functionality
│   ├── dispatch-database/   # Dispatch database models
│   ├── firecrawl-core/      # Firecrawl core functionality
│   ├── firecrawl-types/     # Firecrawl TypeScript types
│   ├── firecrawl-ui/        # Firecrawl UI components
│   ├── forensic-core/       # Forensic analysis core
│   ├── intelligence/        # Intelligence gathering utilities
│   ├── mtg-scripting-toolkit/ # MTG scripting utilities
│   ├── nemesis-common/      # Nemesis shared code
│   └── nemesis-file-enrichment/ # Nemesis file processing
├── features/                # MCP servers and standalone integrations (active migration)
│   ├── chroma-mcp/          # Chroma MCP server
│   ├── FileScopeMCP/        # File scope MCP server
│   ├── firecrawl-mcp-server/ # Firecrawl MCP integration
│   ├── it-tools/            # IT utility tools
│   ├── kong/                # API Gateway
│   ├── lscript/             # Linux scripting tools
│   ├── MalwareBazaar_MCP/   # Malware analysis MCP
│   ├── mcp-virustotal/      # VirusTotal MCP integration
│   ├── n8n-mcp-server/      # n8n MCP integration
│   ├── rita/                # Real Intelligence Threat Analytics
│   ├── securityonion/       # Network security monitoring
│   ├── securityonion-n8n-workflows/ # Security Onion automation
│   └── spec-kit/            # Specification toolkit
├── projects/                # Project-specific configurations and resources
│   ├── security/            # Security project files
│   ├── mtg/                 # MTG project files
│   ├── productivity/        # Productivity project files
│   ├── dev-tools/           # Developer tools
│   └── infrastructure/      # Infrastructure integrations
├── infrastructure/
│   ├── terraform/           # Terraform IaC
│   ├── kubernetes/          # Kubernetes manifests
│   └── docker/              # Docker configurations
├── docs/                    # Documentation
├── specs/                   # Technical specifications
├── scripts/                 # Build and utility scripts
├── tests/                   # Cross-cutting integration tests
└── experimental-archive/    # Archived experimental code

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
   pnpm install
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

### Core Services

**Frontend:**

```bash
npx nx serve jane-ui                # Port 3000 - Unified Next.js 15 interface
```

**Central Orchestration:**

```bash
npx nx serve jane-orchestrator      # Port 8000 - FastAPI backend
npx nx serve n8n-workflow-service   # Port 8010 - Workflow orchestration
```

### Domain Services

**Security Domain:**

```bash
npx nx serve security-service        # Port 8011 - Security aggregation
npx nx serve misp-service           # MISP platform
npx nx serve nemesis-service        # Nemesis framework
npx nx serve cyberchef-service      # CyberChef operations
npx nx serve dispatch-service       # Incident management
npx nx serve ghostwriter-service    # Penetration testing
npx nx serve helk-service           # HELK stack
npx nx serve maltrail-service       # Malware detection
```

**Productivity Domain:**

```bash
npx nx serve productivity-service   # Port 8012 - Productivity aggregation
npx nx serve actual-service         # Actual Budget
npx nx serve mealie-service         # Recipe management
npx nx serve firecrawl-service      # Web scraping
npx nx serve goose-service          # AI coding assistant
npx nx serve inspector-service      # Code inspection
```

**TCG Domain:**

```bash
npx nx serve mtg-service            # Port 8013 - MTG aggregation
npx nx serve commander-spellbook-backend  # Commander Spellbook API
npx nx serve commander-spellbook-site     # Commander Spellbook UI
```

**Infrastructure:**

```bash
npx nx serve infrastructure-service # Port 8014 - Infrastructure aggregation
npx nx serve kasmvnc-service        # Remote desktop
```

### AI Servers

```bash
npx nx serve cyber-llm-server       # Port 8001 - Security domain AI
npx nx serve mtg-llm-server         # Port 8002 - MTG domain AI
npx nx serve infrastructure-llm-server # Port 8003 - Infrastructure AI
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

**Current Phase**: Active migration to hybrid domain-based architecture

### Migration Progress

1. **✅ Planning Complete**: Hybrid domain-based architecture designed
2. **✅ Foundation Built**: Core services and domain structure created
3. **🔄 In Progress**: Migrating tools from `features/` to domain services
4. **⏳ Pending**: Complete n8n orchestration with AI enhancement
5. **⏳ Pending**: Phase out legacy `jane-orchestrator` after full migration

### Success Criteria

- **🔄 Tool Migration**: Most tools migrated to domain services, MCP servers remain in `features/`
- **✅ Services Operational**: 4 domain services + n8n workflow service active
- **⏳ AI-First Workflows**: Implementing via n8n orchestration
- **⏳ Performance Optimization**: 60/40 performance split (AI speed prioritized over UI)

See `specs/` directory for detailed technical specifications and migration documentation.

## Architecture Overview

This monorepo follows NX best practices with a hybrid domain-based architecture:

- **apps/core/**: Core infrastructure (UI, orchestrator, infrastructure service)
- **apps/ai/**: Specialized LLM servers for domain-specific AI capabilities
- **apps/security/**: Security domain tools and services (13 tools)
- **apps/productivity/**: Productivity domain tools and services (8 tools)
- **apps/tcg/**: Trading card game domain tools and services (4 tools)
- **libs/**: Shared libraries, UI components, and service adapters
- **features/**: MCP servers and standalone integrations (active migration)
- **infrastructure/**: Infrastructure as Code and deployment configurations
