# Actual Budget Service

This NX application provides a clean integration layer for [Actual Budget](https://actualbudget.org/), a local-first personal finance system.

## Project Structure

```
apps/actual-service/
├── src/                          # NX service integration layer
│   ├── app/                      # Application logic
│   │   ├── actual.service.ts     # Main service class
│   │   └── actual.service.spec.ts # Service tests
│   ├── environments/             # Environment configurations
│   └── main.ts                   # Entry point
├── actual-budget/                # Actual Budget source code
│   ├── packages/                 # Actual Budget packages
│   ├── bin/                      # Build scripts
│   ├── package.json             # Actual Budget configuration
│   └── ...                      # Full Actual Budget codebase
├── project.json                 # NX project configuration
└── package.json                # NX service package configuration
```

## Architecture

This follows NX best practices by:

- **Separation of Concerns**: NX integration layer (`src/`) separate from Actual Budget codebase (`actual-budget/`)
- **Clean API**: Service class provides structured access to Actual Budget functionality
- **Environment Configuration**: Proper dev/prod environment setup
- **Multiple Build Targets**: Separate targets for service integration and Actual Budget builds

## Available Commands

### NX Service Commands (Integration Layer)
```bash
# Build the NX service integration
nx build:service actual-service

# Test the service integration
nx test actual-service

# Lint the NX service code
nx lint actual-service
```

### Actual Budget Commands (Application)
```bash
# Build Actual Budget for browser
nx build actual-service
# OR specifically
nx build:browser actual-service

# Build Actual Budget server
nx build:server actual-service

# Build Actual Budget desktop app
nx build:desktop actual-service

# Serve Actual Budget browser interface
nx serve actual-service

# Serve Actual Budget sync server
nx serve:server actual-service

# Serve Actual Budget desktop version
nx serve:desktop actual-service

# Install Actual Budget dependencies
nx install actual-service

# Test Actual Budget codebase
nx test:actual actual-service

# Lint Actual Budget code
nx lint:actual actual-service

# Run Actual Budget TypeScript checks
nx typecheck actual-service
```

## Service Integration

The `ActualService` class provides structured access to Actual Budget:

```typescript
import { ActualService } from '@actual-service/app/actual.service';

const actualService = new ActualService();

// Check if Actual Budget is available
const isInstalled = await actualService.isInstalled();

// Get configuration
const config = await actualService.getConfiguration();

// Get paths to specific parts
const lootCorePath = actualService.getPackagePath('loot-core');
const buildPath = actualService.getBuildPath();
const dataPath = actualService.getDataPath();
```

## Environment Configuration

- **Development**: Full logging, sync enabled, desktop enabled
- **Production**: Error logging only, sync enabled, desktop disabled

## Tags

- `type:app` - Application project
- `domain:productivity` - Productivity domain
- `framework:react` - React-based frontend
- `backend:node` - Node.js backend
- `scope:actual-budget` - Actual Budget integration

## Migration Status

✅ **Fully migrated** from `features/actual/` with proper NX organization following best practices.