# Codespace Setup Guide

This guide explains how to set up the modular-monolith-2 development environment in GitHub Codespaces or any fresh Linux environment.

## 🚀 Automated Setup Scripts

We provide two automated setup scripts to get you up and running quickly:

### Full Setup Script: `setup-codespace.sh`

**Recommended for first-time setup**

```bash
./setup-codespace.sh
```

This comprehensive script performs the following operations:

#### System Environment
- Updates and upgrades all system packages
- Installs essential build tools and dependencies
- Configures package repositories

#### Python Environment  
- Installs UV (modern Python package installer)
- Upgrades pip to the latest version
- Verifies Python 3.12.x compatibility
- Installs all Python dependencies for all services

#### Node.js Environment
- Verifies Node.js 20.x compatibility
- Installs all npm dependencies
- Configures NX workspace

#### Development Tools
- Installs specify-cli from GitHub for project specification management
- Verifies Docker and Docker Compose installation
- Sets up environment files (.env) from examples
- Tests basic build functionality

#### Verification
- Comprehensive verification of all tools and versions
- Lists all available projects and applications
- Provides ready-to-use commands and next steps

### Quick Setup Script: `quick-setup.sh`

**For minimal setup or when you know the environment is mostly ready**

```bash
./quick-setup.sh
```

This lightweight script performs:
- System package updates
- UV and specify-cli installation  
- Project dependency installation
- Pip upgrade

## 🔧 Manual Setup

If you prefer to install components manually or need to troubleshoot:

### 1. System Requirements

Ensure you have the following versions:
- **Node.js**: 20.x or higher
- **Python**: 3.12.x
- **npm**: Latest (comes with Node.js)
- **Git**: Latest

### 2. Install UV (Python Package Installer)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.cargo/bin:$PATH"
```

### 3. Install specify-cli

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
export PATH="$HOME/.local/bin:$PATH"
```

### 4. Install Project Dependencies

Using the Makefile (recommended):
```bash
make install
```

Or manually:
```bash
npm install
pip install -r apps/jane-orchestrator/requirements.txt
pip install -r apps/cyber-llm-server/requirements.txt
pip install -r apps/mtg-llm-server/requirements.txt
pip install -r apps/code-llm-server/requirements.txt
```

## 📋 Available Development Commands

After setup, you can use these commands:

### Building Applications
```bash
make build                    # Build all applications
npx nx build jane-ui         # Build specific application
npx nx run-many --target=build --all  # Build all with NX
```

### Development Servers
```bash
# Frontend
npx nx serve jane-ui                 # http://localhost:3000

# Backend Services  
npx nx serve jane-orchestrator       # http://localhost:8000
npx nx serve cyber-llm-server        # http://localhost:8001
npx nx serve mtg-llm-server          # http://localhost:8002
npx nx serve code-llm-server         # http://localhost:8003
```

### Testing
```bash
make test                    # Run all tests
npx nx test jane-orchestrator  # Run specific project tests
```

### Linting
```bash
make lint                    # Lint all projects
npx nx lint jane-ui         # Lint specific project
```

### Docker Services
```bash
cd infrastructure/docker
docker-compose up            # Start all services
docker-compose up -d         # Start in background
docker-compose down          # Stop all services
```

## 🔍 Verification

After running any setup script, verify your environment:

### Check Tool Versions
```bash
node --version        # Should be v20.x.x or higher
python --version      # Should be Python 3.12.x
npx nx --version      # Should show local NX installation
uv --version          # Should show UV version
```

### Test Project Structure
```bash
npx nx show projects  # List all available projects
npx nx show projects --type=app  # List applications only
```

### Test Build Process
```bash
npx nx build jane-ui  # Should build successfully
```

## 🐳 Dev Container Support

This repository includes a `.devcontainer/devcontainer.json` configuration that:

- Automatically runs the full setup script on container creation
- Pre-configures VS Code with relevant extensions
- Sets up port forwarding for all services
- Configures Python and Node.js environments

To use with GitHub Codespaces:
1. Create a new codespace from this repository
2. The setup will run automatically
3. Wait for the "Setup Complete" message
4. Start developing!

## 🛠️ Troubleshooting

### Common Issues

**Script Permission Denied**
```bash
chmod +x setup-codespace.sh
chmod +x quick-setup.sh
```

**UV Not in PATH**
```bash
export PATH="$HOME/.cargo/bin:$PATH"
source ~/.bashrc  # or restart terminal
```

**specify-cli Not Found**
```bash
export PATH="$HOME/.local/bin:$PATH" 
source ~/.bashrc  # or restart terminal
```

**NX Command Not Found**
```bash
npm install  # Reinstall dependencies
npx nx --version  # Use npx prefix
```

**Python Import Errors**
```bash
make install  # Reinstall all Python dependencies
python -m pip install --upgrade pip
```

### Getting Help

1. Check the setup script output for specific error messages
2. Verify all prerequisites are met
3. Try the manual setup steps individually
4. Check the project's issue tracker on GitHub

## 📁 Environment Files

The setup scripts will create `.env` files from `.env.example` templates in:
- `apps/jane-orchestrator/.env`
- `apps/jane-ui/.env` 
- `apps/cyber-llm-server/.env`
- `apps/mtg-llm-server/.env`
- `apps/code-llm-server/.env`

Review and modify these files as needed for your development environment.

## 🎯 Next Steps

After successful setup:

1. **Start the UI**: `npx nx serve jane-ui` → http://localhost:3000
2. **Start the API**: `npx nx serve jane-orchestrator` → http://localhost:8000/docs  
3. **Review Documentation**: Check individual app README files
4. **Configure Services**: Update .env files as needed
5. **Begin Development**: The modular monolith is ready!

---

For more information about the project architecture and individual services, see the main [README.md](./README.md).