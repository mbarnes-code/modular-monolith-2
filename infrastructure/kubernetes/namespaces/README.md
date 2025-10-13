# Kubernetes Namespaces

This directory contains namespace definitions for the Jane monorepo Kubernetes cluster.

## Namespaces

- **jane-services**: Core Jane services (UI, Orchestrator, LLM servers)
- **makoto-services**: Makoto domain services (Security, MTG, Productivity)
- **monitoring**: Monitoring and observability stack (Prometheus, Grafana, Loki, Jaeger)

## Usage

Apply all namespaces:
```bash
kubectl apply -f infrastructure/kubernetes/namespaces/
```

Apply specific namespace:
```bash
kubectl apply -f infrastructure/kubernetes/namespaces/jane-services.yaml
```

## Namespace Strategy

Each namespace isolates a logical group of services with:
- Network policies for isolation
- Resource quotas
- RBAC permissions
- Service accounts
