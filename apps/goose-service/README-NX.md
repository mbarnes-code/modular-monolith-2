# Goose Service - NX Integration

This directory contains the Goose AI agent integrated into the NX workspace as a service.

## Overview

Goose is a local, extensible, open source AI agent that automates engineering tasks. It has been migrated from `features/goose` to become a proper NX application within the modular monolith architecture.

## Project Structure

Following NX best practices, the Goose project has been organized into separate applications:

- **`goose-service`** - Core Rust CLI and libraries (this project)
  - `src/crates/` - Rust source code
  - `src/examples/` - Example configurations  
  - `src/scripts/` - Build and development scripts
  - `config/` - Configuration files
  - `tools/` - Development and build tools

- **`goose-docs`** - Docusaurus documentation site (separate project)
- **`goose-ui`** - Electron desktop application (separate project)  
- **`goose-temporal-service`** - Go temporal workflows (separate project)

## Available NX Commands

### Core Service Commands

```bash
# Build the Rust CLI
npx nx build goose-service

# Run Goose CLI in development mode
npx nx serve goose-service

# Run all tests
npx nx test goose-service

# Run unit tests only  
npx nx test goose-service --configuration=unit

# Run integration tests only
npx nx test goose-service --configuration=integration

# Run linting
npx nx lint goose-service

# Check formatting
npx nx format goose-service

# Fix formatting
npx nx format:fix goose-service

# Clean build artifacts
npx nx clean goose-service

# Build Docker image
npx nx docker:build goose-service

# Run Docker container
npx nx docker:run goose-service
```

### Related Projects

```bash
# Documentation site
npx nx serve goose-docs        # Serve docs locally
npx nx build goose-docs        # Build docs for production

# Desktop UI
npx nx serve goose-ui          # Serve UI in development
npx nx package goose-ui        # Package desktop app

# Temporal service
npx nx serve goose-temporal-service    # Run temporal workflows
npx nx build goose-temporal-service    # Build Go service
```

## Development Setup

1. **Rust Dependencies**: The project uses Cargo for Rust dependency management
2. **Documentation**: Uses Node.js/npm for the Docusaurus documentation site
3. **Desktop UI**: Electron-based desktop application
4. **Temporal Service**: Go-based workflow service

## Integration with Jane Platform

Goose integrates with the Jane platform as a productivity service, providing:

- AI-assisted coding capabilities
- Task automation
- Local development agent functionality
- Integration with other productivity tools in the platform

## Configuration

The service maintains its original configuration files:

- `Cargo.toml` - Rust workspace configuration
- `rust-toolchain.toml` - Rust toolchain specification
- `.goosehints` - Goose-specific configuration
- `recipe.yaml` - Goose recipe configuration

## Migration Notes

This service was migrated from `features/goose` as part of the modular monolith consolidation. All original functionality is preserved while gaining the benefits of NX workspace management.
