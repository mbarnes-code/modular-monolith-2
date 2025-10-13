# VS Code Configuration for Jane Monorepo

This directory contains comprehensive VS Code configuration optimized for the Jane monorepo development environment.

## Files Overview

### `settings.json`
**Enhanced workspace settings** with:
- **Editor Settings**: Format on save, rulers, trim whitespace
- **Python Configuration**: Black formatting, Pylance analysis, type checking
- **TypeScript/JavaScript**: Non-relative imports, auto-imports, path mapping
- **NX Monorepo Support**: Library imports, project viewing
- **File Associations**: Proper syntax highlighting for all file types
- **Performance**: Optimized search/file exclusions for large monorepo
- **FastAPI Integration**: REST client environment variables
- **Tailwind CSS**: Enhanced IntelliSense for UI development

### `extensions.json`
**Curated extension recommendations** including:
- **Core Development**: Prettier, ESLint, spell checker
- **Python Stack**: Python, Pylance, Black, Flake8, isort, debugpy
- **TypeScript/React**: TypeScript support, auto-rename tags, React snippets
- **NX Monorepo**: Angular Console (NX extension)
- **Infrastructure**: Docker, Kubernetes, Terraform
- **API Development**: REST Client, OpenAPI, Thunder Client
- **AI & Productivity**: GitHub Copilot, Copilot Chat
- **Git Integration**: GitLens, Pull Request management

### `launch.json`
**Comprehensive debugging configurations**:
- **Frontend Debugging**: Next.js development and build modes
- **Backend Services**: All FastAPI services with proper environment setup
- **Test Debugging**: Python pytest and TypeScript test runners
- **Docker Debugging**: Attach to containerized services
- **Compound Configurations**: 
  - 🚀 Debug All Services
  - 🌐 Debug Full Stack (UI + API)
  - 🧪 Debug Backend + Tests

### `tasks.json`
**Development workflow automation**:
- **Development Tasks**: Serve UI, orchestrator, and all services
- **Build Tasks**: Individual and bulk build operations
- **Test Tasks**: Full test suite and service-specific tests
- **Docker Tasks**: Build, start, and stop all services
- **NX Tasks**: Affected builds, dependency graph visualization
- **Maintenance**: Clean, install, format, and lint operations

### `jane-monorepo.code-snippets`
**Custom code snippets** for common patterns:
- **NX Imports**: Quick monorepo library imports
- **React Components**: TypeScript-enabled component templates
- **FastAPI**: Route definitions, Pydantic models
- **Python**: Async functions with proper typing
- **Testing**: Jest and pytest function templates
- **Configuration**: NX project.json, Docker healthchecks

### `keybindings.json`
**Optimized keyboard shortcuts**:
- `Ctrl+Shift+B`: Build project
- `Ctrl+Shift+T`: Run tests
- `Ctrl+Shift+R`: Start Jane UI
- `Ctrl+Shift+O`: Start Jane Orchestrator
- `Ctrl+Shift+G`: Show NX dependency graph
- `Ctrl+K Ctrl+F`: Format all files
- `Ctrl+K Ctrl+L`: Lint all files
- `Ctrl+K Ctrl+C`: Clean all artifacts

## Quick Start

1. **Install Recommended Extensions**:
   ```bash
   code --install-extension esbenp.prettier-vscode
   code --install-extension ms-python.python
   code --install-extension nrwl.angular-console
   ```
   *Or use the Extensions view and install all recommended extensions*

2. **Start Development**:
   - Press `Ctrl+Shift+R` to start Jane UI
   - Press `Ctrl+Shift+O` to start Jane Orchestrator
   - Or use `F5` to launch debug configurations

3. **View Dependency Graph**:
   - Press `Ctrl+Shift+G` or run "NX: Graph" task

## Features

### Monorepo-Optimized Settings
- **Path Mapping**: Automatic imports using `@jane-monorepo/*` aliases
- **Search Optimization**: Excludes node_modules, build artifacts, model files
- **File Watching**: Optimized for large monorepo performance
- **Multi-Language**: Proper formatting for Python, TypeScript, JSON, YAML

### Debugging Excellence
- **Multi-Service Debugging**: Debug all services simultaneously
- **Hot Reload Support**: FastAPI and Next.js auto-reload in debug mode
- **Container Debugging**: Attach to Docker containers with port forwarding
- **Test Integration**: Debug individual tests or entire test suites

### Development Workflow
- **One-Click Operations**: Build, test, format, lint with keyboard shortcuts
- **Background Tasks**: Services run in background with proper problem matching
- **Docker Integration**: Build and orchestrate containers from VS Code
- **Git Integration**: Enhanced with GitLens and pull request management

### Code Quality
- **Automatic Formatting**: Prettier for TS/JS, Black for Python
- **Linting Integration**: ESLint, Flake8 with auto-fix on save
- **Type Checking**: Full TypeScript and Python type analysis
- **Import Organization**: Auto-organize imports on save

## Customization

### Adding New Services
1. **Debug Configuration**: Add new service to `launch.json`
2. **Task Configuration**: Add serve task to `tasks.json`
3. **Keyboard Shortcut**: Add shortcut to `keybindings.json`

### Python Services
```json
{
  "name": "Debug New Service",
  "type": "debugpy",
  "request": "launch",
  "module": "uvicorn",
  "args": ["src.api.main:app", "--reload", "--port", "8004"],
  "cwd": "${workspaceFolder}/apps/new-service"
}
```

### TypeScript/Node Services
```json
{
  "name": "Debug New Node Service",
  "type": "node",
  "request": "launch",
  "runtimeExecutable": "npx",
  "runtimeArgs": ["nx", "serve", "new-service"]
}
```

## Troubleshooting

### Python Interpreter Issues
- Check `python.defaultInterpreterPath` in settings.json
- Ensure virtual environment is activated
- Verify PYTHONPATH in debug configurations

### Import Resolution Problems
- Check `tsconfig.base.json` path mappings
- Verify NX library exports in `index.ts` files
- Restart TypeScript server: `Ctrl+Shift+P` → "TypeScript: Restart TS Server"

### Debug Configuration Not Working
- Ensure correct `cwd` and `env` settings
- Check port conflicts (8000-8003 are reserved)
- Verify service entry points match `args` configuration

### Performance Issues
- Review `search.exclude` and `files.watcherExclude` patterns
- Consider excluding additional build artifacts
- Check VS Code workspace trust settings

## Integration Notes

### NX Monorepo
- Uses Angular Console extension for NX integration
- Supports affected builds and dependency visualization
- Configured for optimal monorepo performance

### FastAPI Services
- Debug configurations include environment variables
- Health check endpoints configured for REST client
- Proper PYTHONPATH setup for each service

### Next.js UI
- Configured for Next.js 15 with React 19
- Tailwind CSS IntelliSense enabled
- Optimized build and development modes

### Docker Integration
- Compose file integration for multi-service development
- Container debugging with port mapping
- Health check monitoring

This configuration provides a production-ready development environment optimized for the Jane monorepo's modular architecture.