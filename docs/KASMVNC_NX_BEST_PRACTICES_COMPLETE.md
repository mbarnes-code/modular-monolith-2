# KasmVNC NX Best Practices Implementation

## Overview

The KasmVNC service has been reorganized to follow NX best practices, providing a more maintainable and scalable structure within the Jane Orchestrator monorepo.

## Directory Structure (NX Best Practices)

```
apps/kasmvnc-service/
├── src/                           # Source code (sourceRoot)
│   ├── main.ts                   # Main CLI entry point
│   ├── app/                      # Core application code
│   │   ├── common/               # Common VNC implementation
│   │   ├── unix/                 # Unix-specific code
│   │   ├── win/                  # Windows-specific code
│   │   └── cmake/                # CMake build system
│   ├── assets/                   # Static assets
│   ├── kasmweb/                  # Web interface (noVNC submodule)
│   ├── third_party/             # Third-party dependencies
│   ├── contrib/                  # Contributed code
│   ├── CMakeLists.txt           # Root CMake configuration
│   └── config.h.in              # Configuration template
├── infrastructure/               # Build & deployment infrastructure
│   ├── builder/                  # Docker & package build scripts
│   ├── alpine/                   # Alpine Linux packaging
│   ├── debian/                   # Debian/Ubuntu packaging
│   ├── fedora/                   # Fedora packaging
│   ├── opensuse/                 # OpenSUSE packaging
│   ├── oracle/                   # Oracle Linux packaging
│   └── release/                  # Release management
├── tests/                        # Test files
│   └── spec/                     # Functional test specifications
├── project.json                  # NX project configuration
├── package.json                  # Node.js dependencies
├── tsconfig.json                 # TypeScript base config
├── tsconfig.app.json            # Application TypeScript config
├── tsconfig.spec.json           # Test TypeScript config
├── jest.config.ts               # Jest test configuration
├── .eslintrc.json               # ESLint configuration
└── README.md                    # Original KasmVNC documentation
```

## NX Configuration Improvements

### 1. Proper sourceRoot

- **Before**: `"sourceRoot": "apps/kasmvnc-service"`
- **After**: `"sourceRoot": "apps/kasmvnc-service/src"`

### 2. Build Targets with Outputs and Caching

```json
{
  "build": {
    "executor": "@nx/js:tsc",
    "outputs": ["{options.outputPath}"],
    "options": {
      "outputPath": "dist/apps/kasmvnc-service",
      "tsConfig": "apps/kasmvnc-service/tsconfig.app.json",
      "main": "apps/kasmvnc-service/src/main.ts"
    }
  }
}
```

### 3. Target Dependencies

- Proper `dependsOn` configuration for build pipelines
- Cached outputs for faster rebuilds
- Parallel execution where possible

### 4. TypeScript Configuration

- Proper TypeScript project references
- Separate configs for app and tests
- Strict type checking enabled

### 5. Testing Integration

- Jest configuration with NX executor
- Proper test file patterns
- Coverage reporting

### 6. Linting Integration

- ESLint configuration extending workspace rules
- Proper file patterns for TypeScript

## Available Commands

### Core Development Commands

```bash
# Build TypeScript CLI
npx nx build kasmvnc-service

# Run development server
npx nx serve kasmvnc-service

# Run development with shell access
npx nx serve:dev kasmvnc-service

# Check service status
npx nx status kasmvnc-service

# Setup complete environment
npx nx setup kasmvnc-service
```

### Native Build Commands

```bash
# Build native KasmVNC server
npx nx build:native kasmvnc-service

# Build Docker image
npx nx build:docker kasmvnc-service

# Build system packages
npx nx build:deb kasmvnc-service
npx nx build:rpm kasmvnc-service
npx nx build:apk kasmvnc-service
npx nx build:tarball kasmvnc-service
```

### Web Interface Commands

```bash
# Install web dependencies
npx nx web:install kasmvnc-service

# Build web interface
npx nx web:build kasmvnc-service

# Serve web development server
npx nx web:serve kasmvnc-service
```

### Testing & Quality Commands

```bash
# Run Jest tests
npx nx test kasmvnc-service

# Run tests in watch mode
npx nx test:watch kasmvnc-service

# Run native functional tests
npx nx test:native kasmvnc-service

# Run Docker-based tests
npx nx test:docker kasmvnc-service

# Lint TypeScript code
npx nx lint kasmvnc-service
```

### Utility Commands

```bash
# Initialize submodules
npx nx init-submodules kasmvnc-service

# Clean build artifacts
npx nx clean kasmvnc-service
```

## CLI Interface

The service now provides a comprehensive CLI interface through `src/main.ts`:

```bash
# Direct CLI usage (after build)
node dist/apps/kasmvnc-service/src/main.js --help

# Available CLI commands:
kasmvnc-service setup
kasmvnc-service build [--docker|--deb|--rpm|--apk|--tarball|--web]
kasmvnc-service serve [--dev] [--web] [--port <port>]
kasmvnc-service test
kasmvnc-service clean
kasmvnc-service status
```

## Dependency Management

### Build Pipeline Dependencies

1. **init-submodules** → **web:install** → **web:build**
2. **build:native** → **build:deb/rpm/apk/tarball**
3. **build:docker** → **serve/serve:dev**

### Caching Strategy

- **Cached outputs**: TypeScript builds, web builds, package builds
- **Cache inputs**: Source files, configuration files, dependencies
- **Cache keys**: Based on file hashes and dependencies

## Performance Optimizations

### 1. Selective Builds

- TypeScript build separate from native builds
- Web interface can be built independently
- Package builds only run when native build completes

### 2. Parallel Execution

- Multiple package formats can build in parallel
- Web and native builds can run concurrently
- Test execution parallelized where possible

### 3. Incremental Builds

- NX caching prevents unnecessary rebuilds
- Only changed components rebuild
- Shared cache across team members

## Integration with Jane Orchestrator

### Tags for Dependency Graph

```json
"tags": [
  "type:application",
  "domain:infrastructure", 
  "scope:desktop",
  "technology:vnc",
  "technology:docker", 
  "technology:cpp",
  "technology:cmake",
  "technology:web",
  "technology:nodejs"
]
```

### VS Code Tasks Integration

All commands are available through VS Code tasks with proper:
- Background process handling
- Problem matchers for error detection
- Proper terminal management
- Progress indicators

## Quality Gates

### 1. Type Safety
- Strict TypeScript configuration
- No `any` types without justification
- Proper type definitions for CLI interfaces

### 2. Code Quality
- ESLint with workspace rules
- Consistent formatting
- Import/export standards

### 3. Testing
- Unit tests for CLI functionality
- Integration tests for build processes
- Functional tests for native code

### 4. Build Validation
- All targets must have proper outputs
- Dependencies correctly declared
- Caching configured for performance

## Migration Benefits

### Before (Features Structure)
- ❌ No build dependency management
- ❌ Manual command execution
- ❌ No caching or incremental builds
- ❌ Inconsistent with other services
- ❌ No type safety for tooling

### After (NX Best Practices)
- ✅ Proper build pipeline with dependencies
- ✅ CLI-driven with type safety
- ✅ Incremental builds with caching
- ✅ Consistent with monorepo standards
- ✅ Full TypeScript integration
- ✅ Comprehensive testing setup
- ✅ Quality gates and linting

## Development Workflow

### 1. Initial Setup
```bash
npx nx setup kasmvnc-service
```

### 2. Development Cycle
```bash
# Make changes to TypeScript code
npx nx build kasmvnc-service

# Test changes
npx nx test kasmvnc-service

# Build web interface
npx nx web:build kasmvnc-service

# Check status
npx nx status kasmvnc-service
```

### 3. Native Development
```bash
# Build native components
npx nx build:native kasmvnc-service

# Test native functionality
npx nx test:native kasmvnc-service

# Build packages
npx nx build:deb kasmvnc-service
```

### 4. Docker Development
```bash
# Build Docker image
npx nx build:docker kasmvnc-service

# Run development container
npx nx serve:dev kasmvnc-service
```

This NX best practices implementation provides a robust, scalable, and maintainable foundation for KasmVNC development within the Jane Orchestrator ecosystem.