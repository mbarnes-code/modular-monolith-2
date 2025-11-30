# Jane Monorepo Makefile
# ======================
# Cross-platform build automation for the modular monolith architecture

# Variables for cross-platform compatibility
OS := $(shell uname -s 2>/dev/null || echo "Windows")
ARCH := $(shell uname -m 2>/dev/null || echo "x64")
SHELL := /bin/bash

# Docker compose command detection (docker-compose vs docker compose)
DOCKER_COMPOSE := $(shell which docker-compose 2>/dev/null || echo "docker compose")

# Project paths
INFRA_DOCKER_PATH := infrastructure/docker
DOCKER_COMPOSE_FILE := $(INFRA_DOCKER_PATH)/docker-compose.yml
DOCKER_COMPOSE_DEV := $(INFRA_DOCKER_PATH)/docker-compose.dev.yml
DOCKER_COMPOSE_STAGING := $(INFRA_DOCKER_PATH)/docker-compose.staging.yml

# Service health endpoints
JANE_ORCHESTRATOR_URL := http://localhost:8000
JANE_UI_URL := http://localhost:3000
GHOSTWRITER_URL := http://localhost:8080

# .PHONY declarations
.PHONY: help install build test lint clean deploy docker-build docker-up docker-down
.PHONY: serve-jane serve-security serve-productivity serve-tcg
.PHONY: docker-serve-nemesis docker-serve-helk docker-serve-misp
.PHONY: test-security test-productivity test-tcg test-python test-performance test-integration
.PHONY: lint-python lint-typescript docs-build health-check status
.PHONY: setup-dev clean-services format format-check security-scan
.PHONY: docker-logs docker-ps docker-clean migrate collectstatic shell backup-db restore-db
.PHONY: coverage bench profile deps-update deps-audit validate-env setup-ci
.PHONY: dev-reset dev-logs quick-test install-dev

# Default target
help:
	@echo "Jane Monorepo - Available Commands:"
	@echo ""
	@echo "BASIC OPERATIONS:"
	@echo "  make install          - Install all dependencies (Node.js and Python)"
	@echo "  make build            - Build all applications"
	@echo "  make test             - Run all tests"
	@echo "  make lint             - Lint all code"
	@echo "  make clean            - Clean build artifacts"
	@echo "  make deploy           - Deploy applications"
	@echo ""
	@echo "SERVICE MANAGEMENT:"
	@echo "  make serve-jane       - Start Jane UI and Orchestrator"
	@echo "  make serve-security   - Start all security services"
	@echo "  make serve-productivity - Start all productivity services"
	@echo "  make serve-tcg        - Start all TCG services"
	@echo "  make status           - Show service status"
	@echo "  make health-check     - Check service health"
	@echo ""
	@echo "DOCKER OPERATIONS:"
	@echo "  make docker-build     - Build all Docker images"
	@echo "  make docker-up        - Start Docker Compose services"
	@echo "  make docker-down      - Stop Docker Compose services"
	@echo "  make docker-logs      - Show logs from all containers"
	@echo "  make docker-ps        - Show running container status"
	@echo "  make docker-clean     - Remove unused containers and images"
	@echo "  make docker-serve-nemesis - Start Nemesis service stack"
	@echo "  make docker-serve-helk    - Start HELK service"
	@echo "  make docker-serve-misp    - Start MISP service"
	@echo ""
	@echo "TESTING BY DOMAIN:"
	@echo "  make test-security    - Test security services"
	@echo "  make test-productivity - Test productivity services"
	@echo "  make test-tcg         - Test TCG services"
	@echo "  make test-python      - Test Python services"
	@echo "  make test-performance - Run performance benchmarks (<1s/2s/3s/5s by domain)"
	@echo "  make test-integration - Run integration tests across services"
	@echo "  make coverage         - Generate test coverage reports"
	@echo ""
	@echo "LINTING BY LANGUAGE:"
	@echo "  make lint-python      - Lint Python code"
	@echo "  make lint-typescript  - Lint TypeScript code"
	@echo ""
	@echo "DEVELOPMENT:"
	@echo "  make setup-dev        - Setup complete development environment"
	@echo "  make docs-build       - Build documentation"
	@echo "  make clean-services   - Clean service-specific artifacts"
	@echo "  make format           - Format all code (Prettier + Black)"
	@echo "  make format-check     - Check code formatting without changes"
	@echo "  make security-scan    - Run security vulnerability scans"
	@echo "  make deps-audit       - Audit dependencies for vulnerabilities"
	@echo ""
	@echo "LIBRARY MANAGEMENT:"
	@echo "  make analyze-dependencies - Analyze dependency overlaps across monorepo"
	@echo "  make analyze-n8n-integration - Analyze N8N monorepo integration opportunities"
	@echo "  make setup-n8n-infrastructure - Setup infrastructure for N8N integration"
	@echo "  make validate-hoisting - Validate environment for library hoisting"
	@echo "  make hoist-libraries  - Hoist Phase 1 dependencies to root"
	@echo "  make hoist-libraries-preview - Preview hoisting changes (dry run)"
	@echo ""
	@echo "DATABASE OPERATIONS:"
	@echo "  make migrate          - Run database migrations for all services"
	@echo "  make collectstatic    - Collect static files for Django services"
	@echo "  make shell            - Open interactive shell for debugging"
	@echo "  make backup-db        - Backup all service databases"
	@echo "  make restore-db       - Restore databases from backup"
	@echo ""
	@echo "AFFECTED OPERATIONS:"
	@echo "  make affected-build   - Build affected projects"
	@echo "  make affected-test    - Test affected projects"
	@echo "  make affected-lint    - Lint affected projects"
	@echo ""

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pnpm install
	@echo "Installing Python dependencies for apps..."
	pip install -r apps/core/jane-orchestrator/requirements.txt || echo "Failed to install jane-orchestrator requirements"
	pip install -r apps/ai/cyber-llm-server/requirements.txt || echo "Failed to install cyber-llm-server requirements"
	pip install -r apps/ai/mtg-llm-server/requirements.txt || echo "Failed to install mtg-llm-server requirements"
	pip install -r apps/ai/infrastructure-llm-server/requirements.txt || echo "Failed to install infrastructure-llm-server requirements"
	@echo "Installing additional service dependencies..."
	find apps/ -name "requirements.txt" -not -path "*/node_modules/*" -exec pip install -r {} \; 2>/dev/null || true
	@echo "✅ Node.js dependencies managed by pnpm workspace"
	@echo "✅ Installation complete!"

install-dev:
	@echo "📦 Installing development dependencies..."
	make install
	pip install pytest pytest-asyncio black isort flake8 mypy pip-audit || echo "Some dev dependencies failed to install"
	pnpm install -D || echo "Dev dependencies already installed"

# Build all applications
build:
	pnpm nx run-many --target=build --all

# Run all tests
test:
	pnpm nx run-many --target=test --all

# Lint all code
lint:
	pnpm nx run-many --target=lint --all

# Clean build artifacts
clean: clean-services
	rm -rf dist/
	rm -rf .next/
	rm -rf build/
	rm -rf node_modules/.cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Deploy applications
deploy:
	pnpm nx run-many --target=deploy --all

# Build Docker images
docker-build:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) build

# Start Docker services
docker-up:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) up -d

# Stop Docker services
docker-down:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) down

# Docker management
docker-logs:
	@echo "Showing logs from all containers..."
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) logs -f --tail=100

docker-ps:
	@echo "Docker container status:"
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(jane|nemesis|helk|misp|actual|mealie)" || echo "No containerized services running"
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_FILE) ps

docker-clean:
	@echo "Cleaning unused Docker resources..."
	docker system prune -f
	docker volume prune -f
	docker image prune -f

# Start development environment
dev:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_DEV) up

# Start staging environment
staging:
	$(DOCKER_COMPOSE) -f $(DOCKER_COMPOSE_STAGING) up -d

# Affected commands
affected-build:
	pnpm nx affected --target=build

affected-test:
	pnpm nx affected --target=test

affected-lint:
	pnpm nx affected --target=lint

affected-deploy:
	pnpm nx affected --target=deploy

# Service-specific commands
serve-jane:
	pnpm nx serve jane-ui & pnpm nx serve jane-orchestrator

serve-security:
	@echo "Starting security services..."
	pnpm nx serve misp-service &
	pnpm nx serve nemesis-service &
	pnpm nx serve helk-service &
	pnpm nx serve maltrail-service &
	pnpm nx serve ghostwriter-service

serve-productivity:
	@echo "Starting productivity services..."
	pnpm nx serve actual-service &
	pnpm nx serve mealie-service &
	pnpm nx serve firecrawl-service &
	pnpm nx serve goose-service &
	pnpm nx serve inspector-service

serve-tcg:
	@echo "Starting TCG services..."
	pnpm nx serve commander-spellbook-site &
	pnpm nx serve commander-spellbook-backend

# Docker service management
docker-serve-nemesis:
	docker-compose -f apps/security/nemesis-service/compose.yaml up -d

docker-serve-helk:
	pnpm nx docker:start helk-service

docker-serve-misp:
	docker-compose -f apps/security/misp-service/infrastructure/docker/docker-compose.yml up -d

# Service testing
test-security:
	pnpm nx run-many --target=test --projects=nemesis-*,helk-service,misp-service,maltrail-service,ghostwriter-service

test-productivity:
	pnpm nx run-many --target=test --projects=actual-service,mealie-service,firecrawl-service,goose-service,inspector-service

test-tcg:
	pnpm nx run-many --target=test --projects=commander-spellbook-*

test-python:
	@echo "Running Python service tests..."
	cd apps/core/jane-orchestrator && pytest tests/ -v
	find apps/ -name "pytest.ini" -o -name "pyproject.toml" -path "*/test*" -execdir python -m pytest \;

# Performance testing (from tests/performance/Makefile)
test-performance:
	@echo "🎯 Running constitutional performance testing..."
	@echo "Testing domain performance tiers..."
	@python3 tests/performance/run_performance_tests.py || echo "Performance tests require setup"
	@echo "Testing UI response times (<200ms)..."
	@curl -w "@tests/performance/curl-format.txt" -o /dev/null -s "http://localhost:8000/" || echo "UI test requires running server"

test-integration:
	@echo "Running integration tests across services..."
	pnpm nx run-many --target=test:integration --all || echo "Integration tests require running services"

# Coverage reporting
coverage:
	@echo "Generating test coverage reports..."
	cd apps/core/jane-orchestrator && python3 -m pytest --cov=src --cov-report=html --cov-report=term
	find apps/ -name "pytest.ini" -execdir python -m pytest --cov=. --cov-report=html \; 2>/dev/null || true

# Service linting
lint-python:
	@echo "Linting Python services..."
	find apps/ -name "*.py" -not -path "*/node_modules/*" -not -path "./.venv/*" -exec ruff check {} +
	find apps/ -name "*.py" -not -path "*/node_modules/*" -not -path "./.venv/*" -exec black --check {} +

lint-typescript:
	@echo "Linting TypeScript services..."
	pnpm nx run-many --target=lint --projects=jane-ui,actual-service,firecrawl-service,goose-service,inspector-service

# Documentation generation
docs-build:
	@echo "Building documentation..."
	make -C apps/security/ghostwriter-service/DOCS html
	find apps/ -name "docs" -type d -exec make -C {} html \; 2>/dev/null || true
	@echo "Building API documentation..."
	pnpm nx run-many --target=docs:build --all 2>/dev/null || true

# Database management
migrate:
	@echo "Running database migrations..."
	pnpm nx run-many --target=migrate --all 2>/dev/null || echo "Migration targets not available for all services"

อcollectstatic:
	@echo "Collecting static files..."
	pnpm nx run-many --target=collectstatic --all 2>/dev/null || echo "Collectstatic targets not available for all services"

shell:
	@echo "Opening interactive shell (first available Django service)..."
	pnpm nx shell ghostwriter-service 2>/dev/null || echo "Shell target not available"

backup-db:
	@echo "Backing up databases..."
	@echo "This is a placeholder - implement based on your database setup"

# Dependency management
deps-update:
	@echo "Updating dependencies..."
	pnpm update
	find apps/ -name "requirements.txt" -execdir pip-compile --upgrade \; 2>/dev/null || echo "pip-tools not available"

# Performance monitoring
bench:
	@echo "🏃 Running performance benchmarks..."
	make test-performance
	@echo "Running load testing..."
	@curl -w "@tests/performance/curl-format.txt" -o /dev/null -s "http://localhost:8000/" || echo "Load test requires running server"

profile:
	@echo "📈 Profiling service performance..."
	@echo "Starting profiling session (requires running services)..."
	python3 -m cProfile -o profile_output.prof -c "import requests; requests.get('http://localhost:8000/health')" 2>/dev/null || echo "Profiling requires running services"
	@echo "Profile saved to profile_output.prof"

# Quick development workflow
dev-reset:
	@echo "🔄 Resetting development environment..."
	make docker-down
	make clean
	make install
	make docker-build
	make docker-up
	@echo "Development environment reset complete!"

dev-logs:
	@echo "📋 Showing development logs..."
	make docker-logs

quick-test:
	@echo "⚡ Running quick validation tests..."
	make format-check
	make lint-typescript
	make test-python
	@echo "Quick tests complete!"

# Health checks
health-check:
	@echo "🏥 Checking service health..."
	@echo "======================="
	@echo "Core Services:"
	@curl -f -s http://localhost:8000/health && echo "✅ Jane Orchestrator: healthy" || echo "❌ Jane Orchestrator: not responding"
	@curl -f -s http://localhost:3000/api/health && echo "✅ Jane UI: healthy" || echo "❌ Jane UI: not responding"
	@echo "Security Services:"
	@curl -f -s http://localhost:8080/health && echo "✅ Ghostwriter: healthy" || echo "❌ Ghostwriter: not responding"
	@curl -f -s http://localhost:6444/misp && echo "✅ MISP: healthy" || echo "❌ MISP: not responding"
	@echo "Productivity Services:"
	@curl -f -s http://localhost:8081/api/health && echo "✅ Actual Budget: healthy" || echo "❌ Actual Budget: not responding"
	@curl -f -s http://localhost:9000/api/docs && echo "✅ Mealie: healthy" || echo "❌ Mealie: not responding"
	@echo "Database Services:"
	@nc -z localhost 5432 && echo "✅ PostgreSQL: responding" || echo "❌ PostgreSQL: not responding"
	@nc -z localhost 6379 && echo "✅ Redis: responding" || echo "❌ Redis: not responding"

# Service status
status:
	@echo "📊 Jane Monorepo Service Status"
	@echo "==============================="
	@echo "NX Workspace Status:"
	pnpm nx run-many --target=status --all 2>/dev/null || echo "Status commands not available for all services"
	@echo ""
	@echo "Docker Services:"
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(jane|nemesis|helk|misp|actual|mealie)" || echo "No containerized services running"
	@echo ""
	@echo "Process Status:"
	@pgrep -f "uvicorn" && echo "✅ Uvicorn processes running" || echo "⚠️  No Uvicorn processes"
	@pgrep -f "node.*serve" && echo "✅ Node.js dev servers running" || echo "⚠️  No Node.js dev servers"
	@echo ""
	@echo "Port Usage:"
	@netstat -tuln 2>/dev/null | grep -E ":(3000|8000|8080|8081|5432|6379|9000)" || echo "Standard ports not in use"

# Kubernetes commands
k8s-apply-dev:
	kubectl apply -k infrastructure/kubernetes/overlays/dev/

k8s-apply-staging:
	kubectl apply -k infrastructure/kubernetes/overlays/staging/

k8s-apply-prod:
	kubectl apply -k infrastructure/kubernetes/overlays/production/

# Terraform commands
terraform-init:
	cd infrastructure/terraform && terraform init

terraform-plan:
	cd infrastructure/terraform && terraform plan

terraform-apply:
	cd infrastructure/terraform && terraform apply

# Format code
format:
	@echo "Formatting TypeScript/JavaScript..."
	pnpm prettier --write .
	@echo "Formatting Python code..."
	find . -name "*.py" -not -path "./node_modules/*" -not -path "./.venv/*" -exec black {} +
	find . -name "*.py" -not -path "./node_modules/*" -not -path "./.venv/*" -exec isort {} +

format-check:
	@echo "Checking code formatting..."
	pnpm prettier --check .
	find . -name "*.py" -not -path "./node_modules/*" -not -path "./.venv/*" -exec black --check {} +
	find . -name "*.py" -not -path "./node_modules/*" -not -path "./.venv/*" -exec isort --check-only {} +

# Security scanning
security-scan:
	@echo "Running security vulnerability scans..."
	@echo "Scanning Python dependencies..."
	pip-audit || echo "pip-audit not installed, run: pip install pip-audit"
	@echo "Scanning Node.js dependencies..."
	pnpm audit || echo "Node.js audit found issues"

दeps-audit: security-scan
	@echo "Dependency audit complete"

# Development environment setup
setup-dev:
	@echo "Setting up development environment..."
	make install
	make docker-build
	@echo "Installing performance testing dependencies..."
	pip install httpx pytest pytest-asyncio pip-audit || echo "Optional dependencies not installed"
	@echo "Development environment ready!"

setup-ci:
	@echo "Setting up CI/CD environment..."
	make install
	make format-check
	make lint
	make test
	@echo "CI environment validated!"

validate-env:
	@echo "Validating development environment..."
	@command -v node >/dev/null 2>&1 || { echo "Node.js not found"; exit 1; }
	@command -v python3 >/dev/null 2>&1 || { echo "Python3 not found"; exit 1; }
	@command -v docker >/dev/null 2>&1 || { echo "Docker not found"; exit 1; }
	@command -v pnpm >/dev/null 2>&1 || { echo "pnpm not found"; exit 1; }
	@echo "✅ Environment validation complete"

# Clean service-specific artifacts
clean-services:
	@echo "Cleaning service artifacts..."
	find apps/ -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
	find apps/ -name "build" -type d -exec rm -rf {} + 2>/dev/null || true
	find apps/ -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true
	find apps/ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find apps/ -name "*.pyc" -delete 2>/dev/null || true
	find apps/ -name "node_modules/.cache" -type d -exec rm -rf {} + 2>/dev/null || true

# Library hoisting commands
.PHONY: hoist-libraries hoist-libraries-preview hoist-libraries-dry-run validate-hoisting analyze-dependencies analyze-n8n-integration
analyze-dependencies:
	@echo "🔍 Analyzing dependency overlaps..."
	npx tsx scripts/analyze-dependencies.ts

analyze-n8n-integration:
	@echo "🔍 Analyzing N8N integration opportunities..."
	npx tsx scripts/n8n-integration-analysis.ts

setup-n8n-infrastructure:
	@echo "🚀 Setting up N8N integration infrastructure..."
	npx tsx scripts/n8n-infrastructure-setup.ts

validate-hoisting:
	@echo "📋 Validating hoisting prerequisites..."
	npx tsx scripts/validate-hoisting.ts

hoist-libraries: validate-hoisting
	@echo "🚀 Starting automated library hoisting..."
	npx tsx scripts/hoist-libraries.ts --force

hoist-libraries-preview: validate-hoisting
	@echo "🔍 Previewing library hoisting changes..."
	npx tsx scripts/hoist-libraries.ts --dry-run

hoist-libraries-dry-run: hoist-libraries-preview
