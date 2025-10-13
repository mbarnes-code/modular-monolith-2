# Jane Monorepo Structure

## Overview
This is an NX monorepo with a modular architecture for managing FastAPI services, Next.js UI, and shared libraries.

## Directory Tree

```
jane-monorepo/
│
├── apps/                           # Application layer (deployable services)
│   ├── orchestrator/               # Main orchestrator service
│   │   ├── main.py                # FastAPI application
│   │   ├── project.json           # NX project configuration
│   │   └── requirements.txt       # Python dependencies (exact versions)
│   │
│   ├── ui/                        # Frontend application
│   │   ├── app/                   # Next.js 15 app directory
│   │   │   ├── layout.tsx         # Root layout
│   │   │   └── page.tsx           # Home page
│   │   ├── public/                # Static assets
│   │   ├── next.config.js         # Next.js configuration
│   │   ├── project.json           # NX project configuration
│   │   ├── package.json           # UI-specific package.json
│   │   └── tsconfig.json          # TypeScript configuration
│   │
│   ├── llm-server-1/              # LLM Server 1 (port 8001)
│   │   ├── main.py                # FastAPI application
│   │   ├── project.json           # NX project configuration
│   │   └── requirements.txt       # Python dependencies
│   │
│   ├── llm-server-2/              # LLM Server 2 (port 8002)
│   │   └── ...                    # Same structure as llm-server-1
│   │
│   └── llm-server-3/              # LLM Server 3 (port 8003)
│       └── ...                    # Same structure as llm-server-1
│
├── libs/                          # Shared libraries
│   ├── shared/                    # Cross-cutting shared code
│   │   ├── types/                 # TypeScript type definitions
│   │   │   ├── index.ts           # Exported types (User, ApiResponse)
│   │   │   └── project.json       # NX project configuration
│   │   │
│   │   └── utils/                 # Utility functions
│   │       ├── index.ts           # Exported utilities (formatDate, generateId)
│   │       └── project.json       # NX project configuration
│   │
│   ├── service-adapters/          # Service integration layer
│   │   ├── index.ts               # Adapter classes (OrchestratorAdapter, LLMAdapter)
│   │   └── project.json           # NX project configuration
│   │
│   └── ui/                        # UI-specific libraries
│       ├── core/                  # Core UI components
│       │   ├── components/        # React components
│       │   │   └── Button.tsx     # Button component
│       │   ├── index.ts           # Exports
│       │   └── project.json       # NX project configuration
│       │
│       ├── domain-security/       # Security domain UI components
│       │   ├── index.ts
│       │   └── project.json
│       │
│       ├── domain-mtg/            # MTG domain UI components
│       │   ├── index.ts
│       │   └── project.json
│       │
│       └── domain-productivity/   # Productivity domain UI components
│           ├── index.ts
│           └── project.json
│
├── projects/                      # Domain-specific projects
│   ├── security/                  # Security domain
│   │   └── README.md
│   │
│   ├── mtg/                       # MTG domain
│   │   └── README.md
│   │
│   └── productivity/              # Productivity domain
│       └── README.md
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
| TypeScript | 5.7.3 | Exact version (no ^ or ~) |
| FastAPI | 0.115.12 | Exact version (==) |
| Uvicorn | 0.34.2 | Exact version (==) |
| Pydantic | 2.10.6 | Exact version (==) |

## Port Allocation

| Service | Port | Description |
|---------|------|-------------|
| UI | 3000 | Next.js frontend application |
| Orchestrator | 8000 | Main FastAPI orchestrator service |
| LLM Server 1 | 8001 | First LLM server instance |
| LLM Server 2 | 8002 | Second LLM server instance |
| LLM Server 3 | 8003 | Third LLM server instance |

## NX Projects

### Applications (5)
1. **ui** - Next.js 15 + React 19 frontend
2. **orchestrator** - FastAPI orchestrator service
3. **llm-server-1** - First LLM server
4. **llm-server-2** - Second LLM server
5. **llm-server-3** - Third LLM server

### Libraries (7)
1. **shared-types** - TypeScript type definitions
2. **shared-utils** - Utility functions
3. **service-adapters** - Service integration adapters
4. **ui-core** - Core UI components
5. **ui-domain-security** - Security domain UI
6. **ui-domain-mtg** - MTG domain UI
7. **ui-domain-productivity** - Productivity domain UI

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
