# Jane Monorepo

An NX monorepo with FastAPI orchestrator, Next.js 15 + React 19 UI, and multiple LLM servers.

## Structure

```
jane-monorepo/
├── apps/
│   ├── orchestrator/        # FastAPI orchestrator service (Python 3.12)
│   ├── ui/                  # Next.js 15.5.2 + React 19.1.0 application
│   ├── llm-server-1/        # LLM Server 1 (Python FastAPI)
│   ├── llm-server-2/        # LLM Server 2 (Python FastAPI)
│   └── llm-server-3/        # LLM Server 3 (Python FastAPI)
├── libs/
│   ├── shared/
│   │   ├── types/           # Shared TypeScript types
│   │   └── utils/           # Shared utility functions
│   ├── service-adapters/    # Service integration adapters
│   └── ui/
│       ├── core/            # Core UI components
│       ├── domain-security/ # Security domain UI components
│       ├── domain-mtg/      # MTG domain UI components
│       └── domain-productivity/ # Productivity domain UI components
├── projects/
│   ├── security/            # Security project files
│   ├── mtg/                 # MTG project files
│   └── productivity/        # Productivity project files
└── infrastructure/
    ├── terraform/           # Terraform IaC
    ├── kubernetes/          # Kubernetes manifests
    └── docker/              # Docker configurations

```

## Technology Stack

- **Node.js**: 20
- **Python**: 3.12
- **Next.js**: 15.5.2 (exact version)
- **React**: 19.1.0 (exact version)
- **FastAPI**: Latest
- **NX**: 21.6.4 (exact version)

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
   pip install -r apps/orchestrator/requirements.txt
   pip install -r apps/llm-server-1/requirements.txt
   pip install -r apps/llm-server-2/requirements.txt
   pip install -r apps/llm-server-3/requirements.txt
   ```

## Running Applications

### UI Application
```bash
npx nx serve ui
```

### Orchestrator Service
```bash
npx nx serve orchestrator
```

### LLM Servers
```bash
npx nx serve llm-server-1
npx nx serve llm-server-2
npx nx serve llm-server-3
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
npx nx build ui
```

## Project Structure

This monorepo follows NX best practices with:
- **apps/**: Application code (deployable services)
- **libs/**: Shared libraries and components
- **projects/**: Domain-specific project files
- **infrastructure/**: Infrastructure as Code (IaC) and deployment configurations