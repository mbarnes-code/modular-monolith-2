# Production Overlay

This overlay customizes the base Kubernetes manifests for the production environment.

## Customizations

- **Replicas**: 3 replicas for UI and orchestrator, 2 for LLM servers
- **Horizontal Pod Autoscaling**: Auto-scaling based on CPU and memory
- **Resources**: Full resource allocation
- **Logging**: Warning level logging
- **Name Prefix**: `prod-` prefix for all resources

## Usage

Apply production configuration:
```bash
kubectl apply -k infrastructure/kubernetes/overlays/production/
```

## Environment Variables

- `ENVIRONMENT=production`
- `LOG_LEVEL=WARNING`

## Horizontal Pod Autoscaling

Services auto-scale between min and max replicas based on:
- CPU utilization (target: 70%)
- Memory utilization (target: 80%)

### HPA Targets

- **jane-ui**: 3-10 replicas
- **jane-orchestrator**: 3-10 replicas

## Purpose

The production overlay provides:
- High availability
- Auto-scaling for demand
- Optimized resource utilization
- Production-grade reliability
