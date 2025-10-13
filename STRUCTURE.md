# Jane Monorepo Structure

## Overview
This is an NX monorepo with a modular architecture for managing FastAPI services, Next.js UI, and shared libraries.

## Directory Tree

```
jane-monorepo/
│
├── apps/                           # Application layer (deployable services)
│   ├── jane-orchestrator/          # Main orchestrator service
│   │   ├── src/
│   │   │   ├── api/               # API layer
│   │   │   │   ├── __init__.py
│   │   │   │   └── main.py        # FastAPI application
│   │   │   ├── core/              # Core business logic
│   │   │   │   └── __init__.py
│   │   │   └── db/                # Database layer
│   │   │       └── __init__.py
│   │   ├── tests/                 # Unit tests
│   │   │   └── __init__.py
│   │   ├── Dockerfile             # Container configuration
│   │   ├── pyproject.toml         # Python project configuration
│   │   ├── requirements.txt       # Python dependencies (exact versions)
│   │   └── project.json           # NX project configuration
│   │
│   ├── jane-ui/                   # Frontend application
│   │   ├── src/
│   │   │   ├── app/               # Next.js 15 app directory
│   │   │   │   ├── layout.tsx     # Root layout
│   │   │   │   └── page.tsx       # Home page
│   │   │   ├── components/        # React components
│   │   │   └── lib/               # Utility libraries
│   │   ├── public/                # Static assets
│   │   ├── next.config.js         # Next.js configuration
│   │   ├── project.json           # NX project configuration
│   │   ├── package.json           # UI-specific package.json
│   │   └── tsconfig.json          # TypeScript configuration
│   │
│   ├── cyber-llm-server/          # Cybersecurity LLM Server (port 8001)
│   │   ├── src/
│   │   │   └── server.py          # FastAPI vLLM application
│   │   ├── models/                # Model configurations
│   │   ├── Dockerfile             # Container configuration
│   │   ├── requirements.txt       # Python dependencies
│   │   ├── README.md              # Documentation
│   │   └── project.json           # NX project configuration
│   │
│   ├── mtg-llm-server/            # Magic: The Gathering LLM Server (port 8002)
│   │   └── ...                    # Same structure as cyber-llm-server
│   │
│   └── code-llm-server/           # Code generation LLM Server (port 8003)
│       └── ...                    # Same structure as cyber-llm-server
│
├── libs/                          # Shared libraries
│   ├── shared/                    # Cross-cutting shared code
│   │   ├── types/                 # TypeScript type definitions
│   │   │   ├── index.ts           # Exported types (User, ApiResponse)
│   │   │   └── project.json       # NX project configuration
│   │   │
│   │   ├── utils/                 # Utility functions
│   │   │   ├── index.ts           # Exported utilities (formatDate, generateId)
│   │   │   └── project.json       # NX project configuration
│   │   │
│   │   └── config/                # Configuration management
│   │       ├── index.ts           # Config utilities (getConfig)
│   │       └── project.json       # NX project configuration
│   │
│   ├── service-adapters/          # Service integration layer
│   │   ├── commander-spellbook/   # Commander Spellbook integration
│   │   │   ├── src/
│   │   │   │   ├── client.py     # API client
│   │   │   │   └── models.py     # Data models
│   │   │   ├── tests/            # Unit tests
│   │   │   └── README.md         # Documentation
│   │   ├── misp/                  # MISP integration
│   │   ├── nemesis/               # Nemesis integration
│   │   ├── dispatch/              # Dispatch integration
│   │   ├── ghostwriter/           # Ghostwriter integration
│   │   ├── n8n/                   # n8n integration
│   │   ├── scryfall/              # Scryfall integration
│   │   ├── actual-budget/         # Actual Budget integration
│   │   ├── mealie/                # Mealie integration
│   │   ├── firecrawl/             # Firecrawl integration
│   │   ├── helk/                  # HELK integration
│   │   ├── goose/                 # Goose integration
│   │   └── kasmvnc/               # KasmVNC integration
│   │
│   └── ui/                        # UI-specific libraries
│       ├── core/                  # Core UI components
│       │   ├── components/        # React components
│       │   │   ├── Button.tsx     # Button component
│       │   │   ├── Input.tsx      # Input component
│       │   │   ├── Card.tsx       # Card component
│       │   │   ├── Modal.tsx      # Modal component
│       │   │   └── Table.tsx      # Table component
│       │   ├── index.ts           # Exports
│       │   └── project.json       # NX project configuration
│       │
│       ├── domain-security/       # Security domain UI components
│       │   ├── components/
│       │   │   ├── ThreatIndicator.tsx
│       │   │   ├── SeverityBadge.tsx
│       │   │   ├── IOCDisplay.tsx
│       │   │   └── IncidentCard.tsx
│       │   ├── index.ts
│       │   └── project.json
│       │
│       ├── domain-mtg/            # MTG domain UI components
│       │   ├── components/
│       │   │   ├── ComboCard.tsx
│       │   │   ├── ManaSymbol.tsx
│       │   │   └── ColorIdentityBadge.tsx
│       │   ├── index.ts
│       │   └── project.json
│       │
│       ├── domain-finance/        # Finance domain UI components
│       │   ├── components/
│       │   │   ├── BudgetChart.tsx
│       │   │   └── TransactionList.tsx
│       │   ├── index.ts
│       │   └── project.json
│       │
│       ├── domain-productivity/   # Productivity domain UI components
│       │   ├── index.ts
│       │   └── project.json
│       │
│       └── theme/                 # Theme configuration
│           ├── colors.ts          # Color palette
│           ├── typography.ts      # Typography system
│           ├── tailwind.config.js # Tailwind CSS config
│           └── project.json
│
├── projects/                      # Domain-specific projects
│   ├── security/                  # Security domain
│   │   ├── misp/
│   │   │   └── README.md
│   │   ├── nemesis/
│   │   │   └── README.md
│   │   ├── yara-x/
│   │   │   └── README.md
│   │   ├── hexstrike-ai/
│   │   │   └── README.md
│   │   ├── dispatch/
│   │   │   └── README.md
│   │   ├── ghostwriter/
│   │   │   └── README.md
│   │   ├── helk/
│   │   │   └── README.md
│   │   ├── rita/
│   │   │   └── README.md
│   │   ├── blackarch/
│   │   │   └── README.md
│   │   ├── onex/
│   │   │   └── README.md
│   │   ├── software-forensic-kit/
│   │   │   └── README.md
│   │   └── README.md
│   │
│   ├── mtg/                       # MTG domain
│   │   ├── commander-spellbook-backend/
│   │   │   └── README.md
│   │   ├── commander-spellbook-frontend/
│   │   │   └── README.md
│   │   ├── mtg-scripting-toolkit/
│   │   │   └── README.md
│   │   └── README.md
│   │
│   ├── productivity/              # Productivity domain
│   │   ├── n8n/
│   │   │   └── README.md
│   │   ├── actual-budget/
│   │   │   └── README.md
│   │   ├── mealie/
│   │   │   └── README.md
│   │   ├── firecrawl/
│   │   │   └── README.md
│   │   └── README.md
│   │
│   ├── dev-tools/                 # Developer tools
│   │   ├── goose/
│   │   │   └── README.md
│   │   ├── inspector/
│   │   │   └── README.md
│   │   ├── it-tools/
│   │   │   └── README.md
│   │   └── README.md
│   │
│   └── infrastructure/            # Infrastructure integrations
│       └── kasmvnc/
│           └── README.md
│
├── infrastructure/                # Infrastructure as Code
│   ├── terraform/                 # Terraform configurations
│   │   └── main.tf                # Main Terraform file (AWS provider)
│   │
│   ├── kubernetes/                # Kubernetes manifests
│   │   └── deployment.yaml        # Deployment and service definitions
│   │
│   └── docker/                    # Docker configurations
│       ├── Dockerfile.orchestrator    # Orchestrator container
│       ├── Dockerfile.ui              # UI container
│       ├── Dockerfile.llm-server      # LLM server container template
│       └── docker-compose.yml         # Multi-service orchestration
│
├── .gitignore                     # Git ignore patterns
├── .nvmrc                         # Node version (20)
├── .python-version                # Python version (3.12)
├── .eslintrc.json                 # ESLint configuration
├── nx.json                        # NX workspace configuration
├── package.json                   # Root package.json with exact versions
├── package-lock.json              # Locked dependencies
├── tsconfig.base.json             # Base TypeScript configuration
└── README.md                      # Main documentation
```

## Technology Stack

| Technology | Version | Notes |
|------------|---------|-------|
| Node.js | 20.x | Specified in .nvmrc |
| Python | 3.12.x | Specified in .python-version |
| Next.js | 15.5.2 | Exact version (no ^ or ~) |
| React | 19.1.0 | Exact version (no ^ or ~) |
| React DOM | 19.1.0 | Exact version (no ^ or ~) |
| NX | 21.6.4 | Exact version (no ^ or ~) |
| TypeScript | 5.8.3 | Exact version (no ^ or ~) |
| FastAPI | 0.115.0 | Exact version (==) |
| Django | 4.2.0 | Exact version (==) |
| SQLAlchemy | 2.0.0 | Exact version (==) |
| Uvicorn | 0.34.2 | Exact version (==) |
| Pydantic | 2.0.0 | Exact version (==) |
| Rust | 1.70+ | For specific integrations |
| Java | 17 LTS | For specific integrations |

## Port Allocation

| Service | Port | Description |
|---------|------|-------------|
| Jane UI | 3000 | Next.js frontend application |
| Jane Orchestrator | 8000 | Main FastAPI orchestrator service |
| Cyber LLM Server | 8001 | Cybersecurity LLM server (vLLM) |
| MTG LLM Server | 8002 | Magic: The Gathering LLM server (vLLM) |
| Code LLM Server | 8003 | Code generation LLM server (vLLM) |

## NX Projects

### Applications (5)
1. **jane-ui** - Next.js 15 + React 19 frontend
2. **jane-orchestrator** - FastAPI orchestrator service
3. **cyber-llm-server** - Cybersecurity LLM server (vLLM)
4. **mtg-llm-server** - Magic: The Gathering LLM server (vLLM)
5. **code-llm-server** - Code generation LLM server (vLLM)

### Libraries (9)
1. **shared-types** - TypeScript type definitions
2. **shared-utils** - Utility functions
3. **shared-config** - Configuration management
4. **service-adapters** - Service integration adapters (13 service integrations)
5. **ui-core** - Core UI components (Button, Input, Card, Modal, Table)
6. **ui-domain-security** - Security domain UI (ThreatIndicator, SeverityBadge, IOCDisplay, IncidentCard)
7. **ui-domain-mtg** - MTG domain UI (ComboCard, ManaSymbol, ColorIdentityBadge)
8. **ui-domain-finance** - Finance domain UI (BudgetChart, TransactionList)
9. **ui-theme** - Theme configuration (colors, typography, Tailwind config)

## Key Features

- ✅ Exact version pinning (no ^ or ~ in package.json, == in requirements.txt)
- ✅ NX monorepo with proper project configuration
- ✅ TypeScript path aliases configured in tsconfig.base.json
- ✅ Docker and Docker Compose support
- ✅ Kubernetes deployment manifests
- ✅ Terraform infrastructure configuration
- ✅ Proper .gitignore for build artifacts and dependencies
- ✅ Modular architecture with clear separation of concerns

## Running the Monorepo

### Development
```bash
# UI application
npx nx serve ui

# Orchestrator service
npx nx serve orchestrator

# LLM servers
npx nx serve llm-server-1
npx nx serve llm-server-2
npx nx serve llm-server-3
```

### Production
```bash
# Build all
npx nx run-many --target=build --all

# Using Docker Compose
cd infrastructure/docker
docker-compose up
```

## Import Paths

Libraries can be imported using the configured path aliases:

```typescript
import { User, ApiResponse } from '@jane-monorepo/shared/types';
import { formatDate, generateId } from '@jane-monorepo/shared/utils';
import { OrchestratorAdapter, LLMAdapter } from '@jane-monorepo/service-adapters';
import { Button } from '@jane-monorepo/ui/core';
import { securityDomain } from '@jane-monorepo/ui/domain-security';
import { mtgDomain } from '@jane-monorepo/ui/domain-mtg';
import { productivityDomain } from '@jane-monorepo/ui/domain-productivity';
```
