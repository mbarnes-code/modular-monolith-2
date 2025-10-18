# Jane Monorepo

An NX monorepo with FastAPI orchestrator, Next.js 15 + React 19 UI, and multiple LLM servers.

## Structure

```
jane-monorepo/
├── .github/                 # GitHub configuration (workflows, issue templates)
├── apps/
│   ├── jane-orchestrator/   # FastAPI orchestrator service (Python 3.12)
│   ├── jane-ui/             # Next.js 15 + React 19 application
│   ├── cyber-llm-server/    # Cybersecurity LLM Server (Python vLLM)
│   ├── mtg-llm-server/      # Magic: The Gathering LLM Server (Python vLLM)
│   └── code-llm-server/     # Code generation LLM Server (Python vLLM)
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
- **TypeScript**: 5.9.3 (exact version)
- **Next.js**: 15.5.4 (exact version)
- **React**: 19.2.0 (exact version)
- **FastAPI**: 0.119.0 (exact version)
- **Django**: 5.2.7 (exact version)
- **SQLAlchemy**: 2.0.44 (exact version)
- **Pydantic**: 2.12.0 (exact version)
- **Uvicorn**: 0.37.0 (exact version)
- **vLLM**: 0.11.0 (exact version)
- **NX**: 21.6.4 (exact version)
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

### UI Application

```bash
npx nx serve jane-ui
```

### Orchestrator Service

```bash
npx nx serve jane-orchestrator
```

### LLM Servers

```bash
npx nx serve cyber-llm-server   # Port 8001
npx nx serve mtg-llm-server     # Port 8002
npx nx serve code-llm-server    # Port 8003
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

This monorepo follows NX best practices with:

- **apps/**: Application code (deployable services)
- **libs/**: Shared libraries and components
- **projects/**: Domain-specific project files
- **infrastructure/**: Infrastructure as Code (IaC) and deployment configurations
