# Jane Monorepo

An NX monorepo with FastAPI orchestrator, Next.js 15 + React 19 UI, and multiple LLM servers.

## Structure

```
jane-monorepo/
├── apps/
│   ├── jane-orchestrator/   # FastAPI orchestrator service (Python 3.12)
│   ├── jane-ui/             # Next.js 15 + React 19 application
│   ├── cyber-llm-server/    # Cybersecurity LLM Server (Python vLLM)
│   ├── mtg-llm-server/      # Magic: The Gathering LLM Server (Python vLLM)
│   └── code-llm-server/     # Code generation LLM Server (Python vLLM)
├── libs/
│   ├── shared/
│   │   ├── types/           # Shared TypeScript types
│   │   ├── utils/           # Shared utility functions
│   │   └── config/          # Configuration management
│   ├── service-adapters/    # Service integration adapters
│   │   ├── commander-spellbook/
│   │   ├── misp/
│   │   ├── nemesis/
│   │   ├── dispatch/
│   │   ├── ghostwriter/
│   │   ├── n8n/
│   │   ├── scryfall/
│   │   ├── actual-budget/
│   │   ├── mealie/
│   │   ├── firecrawl/
│   │   ├── helk/
│   │   ├── goose/
│   │   └── kasmvnc/
│   └── ui/
│       ├── core/            # Core UI components (Button, Input, Card, Modal, Table)
│       ├── domain-security/ # Security domain UI (ThreatIndicator, SeverityBadge, IOCDisplay, IncidentCard)
│       ├── domain-mtg/      # MTG domain UI (ComboCard, ManaSymbol, ColorIdentityBadge)
│       ├── domain-finance/  # Finance domain UI (BudgetChart, TransactionList)
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
- **TypeScript**: 5.8.3 (exact version)
- **Next.js**: 15.5.2 (exact version)
- **React**: 19.1.0 (exact version)
- **FastAPI**: 0.115.0 (exact version)
- **Django**: 4.2.0 (exact version)
- **SQLAlchemy**: 2.0.0 (exact version)
- **Pydantic**: 2.0.0 (exact version)
- **NX**: 21.6.4 (exact version)
- **Rust**: 1.70+ (for specific integrations)
- **Java**: 17 LTS (for specific integrations)

## Prerequisites

- Node.js 20.x
- Python 3.12.x
- npm

## Setup

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Install Python dependencies for each service:
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