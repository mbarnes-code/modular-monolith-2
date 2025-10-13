# Getting Started with Jane Monorepo

This guide will help you set up and start working with the Jane Monorepo.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Development Workflow](#development-workflow)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have the following installed:

### Required

- **Node.js**: Version 20.x
  ```bash
  # Check version
  node --version  # Should output v20.x.x
  ```

- **Python**: Version 3.12.x
  ```bash
  # Check version
  python --version  # Should output Python 3.12.x
  ```

- **npm**: Comes with Node.js
  ```bash
  # Check version
  npm --version
  ```

### Optional (for specific features)

- **Docker**: For containerized development
- **Docker Compose**: For multi-service orchestration
- **kubectl**: For Kubernetes deployment
- **Terraform**: For infrastructure provisioning
- **Rust**: 1.70+ (for Rust integrations)
- **Java**: 17 LTS (for Java integrations)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/jane-monorepo.git
cd jane-monorepo
```

### 2. Install Dependencies

#### Using Make (Recommended)

```bash
make install
```

#### Manual Installation

**Node.js dependencies:**
```bash
npm install
```

**Python dependencies:**
```bash
# For each Python application
pip install -r apps/jane-orchestrator/requirements.txt
pip install -r apps/cyber-llm-server/requirements.txt
pip install -r apps/mtg-llm-server/requirements.txt
pip install -r apps/code-llm-server/requirements.txt
```

### 3. Verify Installation

```bash
# Check NX is available
npx nx --version

# Check that all dependencies are installed
npm list --depth=0
```

## Running the Application

### Development Mode

#### Option 1: Using Docker Compose (Recommended for beginners)

```bash
# Start all services
make dev

# Or directly:
docker-compose -f infrastructure/docker/docker-compose.dev.yml up
```

This will start:
- Jane UI on http://localhost:3000
- Jane Orchestrator on http://localhost:8000
- Cyber LLM Server on http://localhost:8001
- MTG LLM Server on http://localhost:8002
- Code LLM Server on http://localhost:8003

#### Option 2: Running Services Individually

**Terminal 1 - UI:**
```bash
npx nx serve jane-ui
```

**Terminal 2 - Orchestrator:**
```bash
npx nx serve jane-orchestrator
```

**Terminal 3 - Cyber LLM:**
```bash
npx nx serve cyber-llm-server
```

**Terminal 4 - MTG LLM:**
```bash
npx nx serve mtg-llm-server
```

**Terminal 5 - Code LLM:**
```bash
npx nx serve code-llm-server
```

### Production Build

```bash
# Build all applications
make build

# Or using NX directly
npx nx run-many --target=build --all
```

## Development Workflow

### 1. Create a New Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

Edit files in the appropriate directory:
- `apps/` - Application code
- `libs/` - Shared libraries
- `infrastructure/` - Infrastructure configurations

### 3. Test Your Changes

```bash
# Run linter
make lint

# Run tests
make test

# Build to check for errors
make build
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat(scope): description of changes"
```

Follow [Conventional Commits](https://www.conventionalcommits.org/) format.

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub.

## Common Tasks

### Adding a New Library

```bash
# Generate a new library
npx nx generate @nx/js:library my-new-lib --directory=libs/shared
```

### Adding a New Application

```bash
# Generate a new Next.js app
npx nx generate @nx/next:application my-new-app

# Generate a new Python app (manual setup required)
mkdir -p apps/my-python-app
cd apps/my-python-app
touch requirements.txt
touch project.json
```

### Running Specific Tests

```bash
# Test a specific app
npx nx test jane-ui

# Test a specific library
npx nx test shared-types
```

### Checking Affected Projects

```bash
# See what's affected by your changes
npx nx affected:graph

# Build only affected projects
make affected-build

# Test only affected projects
make affected-test
```

### Working with NX Path Aliases

Import shared code using path aliases:

```typescript
// Good - uses path alias
import { UserType } from '@jane-monorepo/shared/types';
import { Button } from '@jane-monorepo/ui/core';

// Bad - relative path
import { UserType } from '../../libs/shared/types';
```

Path aliases are defined in `tsconfig.base.json`.

### Viewing Application Health

All applications expose health endpoints:

```bash
# Jane UI
curl http://localhost:3000/api/health

# Jane Orchestrator
curl http://localhost:8000/health
curl http://localhost:8000/ready

# LLM Servers
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
```

## Troubleshooting

### Problem: "nx: command not found"

**Solution:** Make sure you're using `npx`:
```bash
npx nx serve jane-ui
```

Or install NX globally:
```bash
npm install -g nx
```

### Problem: Port already in use

**Solution:** Check what's using the port and kill it:
```bash
# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Problem: Python module not found

**Solution:** Ensure virtual environment is activated and dependencies installed:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r apps/jane-orchestrator/requirements.txt
```

### Problem: Docker containers won't start

**Solution:** Clean up Docker resources:
```bash
docker-compose -f infrastructure/docker/docker-compose.dev.yml down
docker system prune -a
docker-compose -f infrastructure/docker/docker-compose.dev.yml up --build
```

### Problem: "ENOSPC" error on Linux

**Solution:** Increase file watch limit:
```bash
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Problem: Out of memory errors

**Solution:** Increase Node memory limit:
```bash
export NODE_OPTIONS=--max-old-space-size=4096
```

Or add to package.json scripts:
```json
{
  "scripts": {
    "build": "NODE_OPTIONS='--max-old-space-size=4096' nx build"
  }
}
```

## Next Steps

- Read the [Architecture](../ARCHITECTURE.md) document to understand system design
- Check the [API Reference](./api-reference.md) for API documentation
- Learn about [Deployment](./deployment.md) processes
- Review [Contributing Guidelines](../CONTRIBUTING.md) before making changes

## Getting Help

- Check existing [GitHub Issues](https://github.com/your-org/jane-monorepo/issues)
- Join our [Discussions](https://github.com/your-org/jane-monorepo/discussions)
- Read the [FAQ](./faq.md) (if available)
- Contact the maintainers

## Additional Resources

- [NX Documentation](https://nx.dev)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [React Documentation](https://react.dev)
