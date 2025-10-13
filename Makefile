.PHONY: help install build test lint clean deploy docker-build docker-up docker-down

# Default target
help:
	@echo "Jane Monorepo - Available Commands:"
	@echo ""
	@echo "  make install          - Install all dependencies (Node.js and Python)"
	@echo "  make build            - Build all applications"
	@echo "  make test             - Run all tests"
	@echo "  make lint             - Lint all code"
	@echo "  make clean            - Clean build artifacts"
	@echo "  make deploy           - Deploy applications"
	@echo "  make docker-build     - Build all Docker images"
	@echo "  make docker-up        - Start Docker Compose services"
	@echo "  make docker-down      - Stop Docker Compose services"
	@echo "  make affected-build   - Build affected projects"
	@echo "  make affected-test    - Test affected projects"
	@echo "  make affected-lint    - Lint affected projects"
	@echo ""

# Install dependencies
install:
	npm install
	@echo "Installing Python dependencies for apps..."
	pip install -r apps/jane-orchestrator/requirements.txt
	pip install -r apps/cyber-llm-server/requirements.txt
	pip install -r apps/mtg-llm-server/requirements.txt
	pip install -r apps/code-llm-server/requirements.txt

# Build all applications
build:
	npx nx run-many --target=build --all

# Run all tests
test:
	npx nx run-many --target=test --all

# Lint all code
lint:
	npx nx run-many --target=lint --all

# Clean build artifacts
clean:
	rm -rf dist/
	rm -rf .next/
	rm -rf build/
	rm -rf node_modules/.cache/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Deploy applications
deploy:
	npx nx run-many --target=deploy --all

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
	npx nx affected --target=build

affected-test:
	npx nx affected --target=test

affected-lint:
	npx nx affected --target=lint

affected-deploy:
	npx nx affected --target=deploy

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
	npx prettier --write .
	find . -name "*.py" -not -path "./node_modules/*" -not -path "./.venv/*" -exec black {} +
