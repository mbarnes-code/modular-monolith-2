.PHONY: help install build test lint clean deploy docker-build docker-up docker-down
.PHONY: serve-jane serve-security serve-productivity serve-tcg
.PHONY: docker-serve-nemesis docker-serve-helk docker-serve-misp
.PHONY: test-security test-productivity test-tcg test-python
.PHONY: lint-python lint-typescript docs-build health-check status
.PHONY: setup-dev clean-services

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
	@echo "  make docker-serve-nemesis - Start Nemesis service stack"
	@echo "  make docker-serve-helk    - Start HELK service"
	@echo "  make docker-serve-misp    - Start MISP service"
	@echo ""
	@echo "TESTING BY DOMAIN:"
	@echo "  make test-security    - Test security services"
	@echo "  make test-productivity - Test productivity services"
	@echo "  make test-tcg         - Test TCG services"
	@echo "  make test-python      - Test Python services"
	@echo ""
	@echo "LINTING BY LANGUAGE:"
	@echo "  make lint-python      - Lint Python code"
	@echo "  make lint-typescript  - Lint TypeScript code"
	@echo ""
	@echo "DEVELOPMENT:"
	@echo "  make setup-dev        - Setup complete development environment"
	@echo "  make docs-build       - Build documentation"
	@echo "  make clean-services   - Clean service-specific artifacts"
	@echo ""
	@echo "AFFECTED OPERATIONS:"
	@echo "  make affected-build   - Build affected projects"
	@echo "  make affected-test    - Test affected projects"
	@echo "  make affected-lint    - Lint affected projects"
	@echo ""

# Install dependencies
install:
	pnpm install
	@echo "Installing Python dependencies for apps..."
	pip install -r apps/core/jane-orchestrator/requirements.txt
	pip install -r apps/ai/cyber-llm-server/requirements.txt
	pip install -r apps/ai/mtg-llm-server/requirements.txt
	pip install -r apps/ai/infrastructure-llm-server/requirements.txt
	@echo "Installing additional service dependencies..."
	find apps/ -name "requirements.txt" -not -path "*/node_modules/*" -exec pip install -r {} \;
	@echo "Node.js dependencies managed by pnpm workspace"

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
	docker-compose -f infrastructure/docker/docker-compose.yml build

# Start Docker services
docker-up:
	docker-compose -f infrastructure/docker/docker-compose.yml up -d

# Stop Docker services
docker-down:
	docker-compose -f infrastructure/docker/docker-compose.yml down

# Start development environment
dev:
	docker-compose -f infrastructure/docker/docker-compose.dev.yml up

# Start staging environment
staging:
	docker-compose -f infrastructure/docker/docker-compose.staging.yml up -d

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

# Health checks
health-check:
	@echo "Checking service health..."
	curl -f http://localhost:8000/health || echo "Jane Orchestrator not responding"
	curl -f http://localhost:3000/api/health || echo "Jane UI not responding"
	curl -f http://localhost:8080/health || echo "Ghostwriter not responding"

# Service status
status:
	@echo "Service Status:"
	@echo "==============="
	pnpm nx run-many --target=status --all 2>/dev/null || echo "Status commands not available for all services"
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(jane|nemesis|helk|misp|actual|mealie)" || echo "No containerized services running"

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
	pnpm prettier --write .
	find . -name "*.py" -not -path "./node_modules/*" -not -path "./.venv/*" -exec black {} +

# Development environment setup
setup-dev:
	@echo "Setting up development environment..."
	make install
	make docker-build
	@echo "Development environment ready!"

# Clean service-specific artifacts
clean-services:
	@echo "Cleaning service artifacts..."
	find apps/ -name "dist" -type d -exec rm -rf {} + 2>/dev/null || true
	find apps/ -name "build" -type d -exec rm -rf {} + 2>/dev/null || true
	find apps/ -name ".next" -type d -exec rm -rf {} + 2>/dev/null || true
	find apps/ -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find apps/ -name "*.pyc" -delete 2>/dev/null || true
	find apps/ -name "node_modules/.cache" -type d -exec rm -rf {} + 2>/dev/null || true
