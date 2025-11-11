# Goose UI

The desktop user interface for Goose AI agent, built with Electron.

## Project Structure

This project was separated from the main Goose service following NX best practices.

- `src/` - Source code for the desktop application
- `desktop/` - Electron-specific configuration and main process files
- `install-link-generator/` - Tool for generating installation links

## Development

```bash
# Install dependencies
npx nx install goose-ui

# Serve in development mode
npx nx serve goose-ui

# Build for production
npx nx build goose-ui

# Package the desktop app
npx nx package goose-ui

# Run tests
npx nx test goose-ui

# Lint code
npx nx lint goose-ui
```

## Dependencies

This project depends on `goose-service` for the core AI agent functionality.
