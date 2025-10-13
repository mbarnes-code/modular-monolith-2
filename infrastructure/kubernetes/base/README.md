# Kubernetes Base Manifests

This directory contains the base Kubernetes manifests for the Jane monorepo services.

## Services

- **jane-ui**: Next.js 15 + React 19 frontend (port 3000)
- **jane-orchestrator**: FastAPI orchestration service (port 8000)
- **cyber-llm**: Cyber security LLM server (port 8001)
- **mtg-llm**: Magic: The Gathering LLM server (port 8002)
- **code-llm**: Code assistance LLM server (port 8003)

## Usage with Kustomize

Apply base configuration:
```bash
kubectl apply -k infrastructure/kubernetes/base/
```

## Health Checks

All services include:
- **Liveness probes**: Checks if service is running
- **Readiness probes**: Checks if service is ready to accept traffic

Endpoints:
- `/health`: Liveness check
- `/ready`: Readiness check

## Resource Limits

Each service has configured:
- Resource requests (guaranteed resources)
- Resource limits (maximum resources)

This ensures proper scheduling and prevents resource exhaustion.

## Overlays

Base manifests are extended by environment-specific overlays:
- `overlays/dev/`: Development environment
- `overlays/staging/`: Staging environment
- `overlays/production/`: Production environment
