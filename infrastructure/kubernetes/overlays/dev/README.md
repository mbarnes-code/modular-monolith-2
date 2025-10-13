# Development Overlay

This overlay customizes the base Kubernetes manifests for the development environment.

## Customizations

- **Replicas**: Single replica for all services
- **Resources**: Reduced resource requests and limits
- **Logging**: Debug level logging enabled
- **Name Prefix**: `dev-` prefix for all resources

## Usage

Apply development configuration:
```bash
kubectl apply -k infrastructure/kubernetes/overlays/dev/
```

## Environment Variables

- `ENVIRONMENT=dev`
- `LOG_LEVEL=DEBUG`

## Purpose

The development overlay is optimized for:
- Local development
- Resource conservation
- Rapid iteration
- Enhanced debugging
