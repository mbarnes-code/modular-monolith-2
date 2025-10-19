# Quickstart Guide: Mental Prosthetic Platform

**Feature**: Mental Prosthetic Platform (Refined)  
**Date**: 2025-10-19  
**Version**: 1.0.0  

## Overview

This guide helps you set up the Mental Prosthetic Platform development environment for consolidating 37 executive function tools into a unified modular monolith with ADHD/autism support.

## Prerequisites

### System Requirements

- **OS**: Ubuntu 20.04+ or compatible Linux distribution
- **Hardware**: Minimum 16GB RAM, 100GB available storage
- **Network**: Local network access for home server deployment
- **Docker**: Docker Engine 24.0+ and Docker Compose v2

### Required Software

```bash
# Node.js and npm
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Python 3.12
sudo apt update
sudo apt install python3.12 python3.12-pip python3.12-venv

# PostgreSQL (for development)
sudo apt install postgresql postgresql-contrib

# Redis (for caching and sessions)
sudo apt install redis-server

# Git and development tools
sudo apt install git curl wget build-essential
```

### Development Tools

```bash
# NX CLI (global installation)
npm install -g @nx/cli

# Python development tools
pip3 install poetry pytest ruff black

# Vue.js development tools
npm install -g @vue/cli @vue/cli-service-global
```

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-org/modular-monolith-2.git
cd modular-monolith-2

# Switch to feature branch
git checkout 002-mental-prosthetic-refinement
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env.local

# Edit environment variables
nano .env.local
```

**Required Environment Variables**:

```bash
# Database Configuration
DATABASE_URL="postgresql://postgres:password@localhost:5432/mental_prosthetic"
REDIS_URL="redis://localhost:6379"

# AI Integration
LLM_SERVER_URL="http://localhost:8001"
OPENAI_API_KEY="your-local-llm-key"  # If using external LLM fallback

# Security
JWT_SECRET_KEY="your-super-secret-jwt-key-change-this"
ENCRYPTION_KEY="your-32-character-encryption-key"

# Executive Function Settings
ADHD_MODE="true"
AUTISM_ACCOMMODATIONS="true"
DEFAULT_FOCUS_DURATION="25"  # Pomodoro timer in minutes
REMINDER_FREQUENCY="15"      # Minutes between reminders

# Domain Performance Tiers
SECURITY_PERFORMANCE_TIER="1000"    # <1s in milliseconds
PRODUCTIVITY_PERFORMANCE_TIER="2000" # <2s in milliseconds
MTG_PERFORMANCE_TIER="3000"         # <3s in milliseconds
INFRASTRUCTURE_PERFORMANCE_TIER="5000" # <5s in milliseconds

# Home Server Configuration
HOME_SERVER_HOST="jane-orchestrator.local"
SYNOLOGY_NAS_HOST="your-synology.local"
BACKUP_SCHEDULE="0 2 * * *"  # Daily at 2 AM

# Mobile/Remote Access
PWA_ENABLED="true"
HTTPS_ENABLED="true"
OAUTH2_CLIENT_ID="your-oauth2-client-id"
```

### 3. Database Setup

```bash
# Create PostgreSQL database
sudo -u postgres createdb mental_prosthetic
sudo -u postgres createuser --superuser $USER

# Create .pgpass for password-less access
echo "localhost:5432:mental_prosthetic:$USER:your-password" >> ~/.pgpass
chmod 600 ~/.pgpass

# Initialize database schema
cd apps/jane-orchestrator
python -m src.database.init_schema

# Run migrations
python -m src.database.migrations
```

### 4. Install Dependencies

```bash
# Install all project dependencies
make install

# Or manually:
npm install
cd apps/jane-orchestrator && pip install -r requirements.txt
cd ../jane-ui && npm install
```

### 5. Build Applications

```bash
# Build all applications
npx nx run-many --target=build --all

# Or build individually
npx nx build jane-ui
npx nx build jane-orchestrator  # If applicable
```

## Running the Platform

### Development Mode

```bash
# Start all services in development mode
make dev

# Or start services individually:

# Terminal 1: Start Jane Orchestrator (FastAPI backend)
cd apps/jane-orchestrator
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Jane UI (Vue.js frontend)
cd apps/jane-ui
npm run dev

# Terminal 3: Start Redis (if not running as service)
redis-server

# Terminal 4: Monitor logs
tail -f logs/mental-prosthetic.log
```

### Production Mode

```bash
# Build for production
make build-prod

# Start with Docker Compose
docker-compose -f infrastructure/docker/docker-compose.yml up -d

# Or start services directly
make start-prod
```

### Verify Installation

1. **Backend API**: Visit `http://localhost:8000/docs` for OpenAPI documentation
2. **Frontend UI**: Visit `http://localhost:3000` for main application
3. **Health Check**: `curl http://localhost:8000/health`

## Configuration

### Executive Function Accommodations

The platform includes specific accommodations for ADHD/autism support:

```json
// User preferences (stored in database)
{
  "adhd_preferences": {
    "reminder_frequency": 15,
    "task_breakdown_style": "detailed",
    "focus_duration": 25,
    "break_reminders": true,
    "hyperfocus_alerts": true
  },
  "autism_preferences": {
    "sensory_preferences": {
      "reduce_animations": false,
      "high_contrast": false,
      "quiet_notifications": true
    },
    "routine_support": {
      "consistent_layout": true,
      "predictable_workflows": true,
      "change_notifications": true
    }
  }
}
```

### Domain-Specific Configuration

Each domain has specific performance and behavior configurations:

```yaml
# apps/jane-orchestrator/config/domains.yml
domains:
  security:
    performance_tier: 1000ms
    tools_count: 13
    priority: critical
    features:
      - misp_integration
      - yara_analysis
      - cyberchef_processing
      - rita_monitoring
  
  productivity:
    performance_tier: 2000ms
    tools_count: 8
    priority: high
    features:
      - task_management
      - n8n_automation
      - it_tools_integration
      - ai_assistance
  
  mtg:
    performance_tier: 3000ms
    tools_count: 4
    priority: medium
    features:
      - deck_management
      - commander_spellbook
      - collection_tracking
      - card_scripting
  
  infrastructure:
    performance_tier: 5000ms
    tools_count: 12
    priority: standard
    features:
      - container_management
      - monitoring_integration
      - file_analysis
      - system_automation
```

## Development Workflow

### Adding New Tool Integration

1. **Analyze Tool**: Document tool in `features/` directory analysis
2. **Plan Integration**: Determine Category (A/B/C) and domain placement
3. **Create Migration**: Develop migration script from features/ to apps/
4. **Update Data Model**: Add necessary database tables/fields
5. **Implement API**: Add domain-specific endpoints to jane-orchestrator
6. **Create UI Components**: Add tool interface to jane-ui
7. **Add Tests**: Unit, integration, and E2E tests
8. **Update Documentation**: API contracts and user documentation

### Testing

```bash
# Run all tests
make test

# Run specific test suites
npx nx test jane-ui                    # Frontend unit tests
pytest apps/jane-orchestrator/tests   # Backend unit tests
npx nx e2e jane-ui-e2e               # End-to-end tests

# Run performance tests
npm run test:performance

# Run cross-domain integration tests
pytest apps/jane-orchestrator/tests/integration
```

### Code Quality

```bash
# Format code
make format

# Lint code
make lint

# Type checking
make typecheck

# Security scan
make security-scan
```

## Troubleshooting

### Common Issues

**Database Connection Issues**:
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Reset database
dropdb mental_prosthetic && createdb mental_prosthetic
python -m src.database.init_schema
```

**Redis Connection Issues**:
```bash
# Check Redis status
redis-cli ping

# Restart Redis
sudo systemctl restart redis-server
```

**Node.js/Python Version Issues**:
```bash
# Check versions
node --version  # Should be 20.x
python3 --version  # Should be 3.12.x

# Install correct versions using version managers
nvm install 20
pyenv install 3.12.0
```

**Build Issues**:
```bash
# Clean and rebuild
make clean
make install
make build
```

**Performance Issues**:
```bash
# Monitor resource usage
htop

# Check logs for performance warnings
grep "PERFORMANCE" logs/mental-prosthetic.log

# Run performance diagnostics
npm run diagnose:performance
```

### Executive Function Support Issues

**AI Assistant Not Responding**:
```bash
# Check LLM server status
curl http://localhost:8001/health

# Restart AI services
docker restart llm-server

# Check WebSocket connections
npx ws-client-test ws://localhost:8000/ws/sync
```

**Task Breakdown Not Working**:
```bash
# Check AI integration logs
tail -f logs/ai-integration.log

# Verify AI context data
python -m src.debug.check_ai_context
```

**Cross-Domain Data Not Syncing**:
```bash
# Check sync state
curl http://localhost:8000/api/v1/sync/status

# Force sync
curl -X POST http://localhost:8000/api/v1/sync/force

# Check WebSocket connections
grep "websocket" logs/mental-prosthetic.log
```

### Getting Help

1. **Logs**: Check `logs/` directory for detailed error information
2. **Health Checks**: Use `/api/v1/health` endpoint for system status
3. **Documentation**: Refer to `/specs/002-mental-prosthetic-refinement/`
4. **Debug Mode**: Set `DEBUG=true` in environment for verbose logging

## Next Steps

1. **Complete Tool Migration**: Move remaining tools from `features/` directory
2. **Set Up CI/CD**: Configure automated testing and deployment
3. **Configure Backup**: Set up automated backups to Synology NAS
4. **Mobile Access**: Configure PWA for remote access
5. **Monitoring**: Set up comprehensive system monitoring
6. **Documentation**: Complete user documentation for all 37 integrated tools

For detailed implementation guidance, see:
- [Data Model Documentation](./data-model.md)
- [API Contracts](./contracts/api.yaml)
- [Implementation Plan](./plan.md)