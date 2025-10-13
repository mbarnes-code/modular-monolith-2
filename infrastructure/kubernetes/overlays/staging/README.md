# Staging Overlay

This overlay customizes the base Kubernetes manifests for the staging environment.

## Customizations

- **Replicas**: 2 replicas for UI and orchestrator, 1 for LLM servers
- **Resources**: Standard resource allocation
- **Logging**: Info level logging
- **Name Prefix**: `staging-` prefix for all resources

## Usage

Apply staging configuration:
```bash
kubectl apply -k infrastructure/kubernetes/overlays/staging/
```

## Environment Variables

- `ENVIRONMENT=staging`
- `LOG_LEVEL=INFO`

## Purpose

The staging overlay is designed for:
- Pre-production testing
- Integration testing
- Performance validation
- Production-like environment
