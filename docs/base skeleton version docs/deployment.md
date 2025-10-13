# Deployment Guide

This guide covers deploying the Jane Monorepo to various environments.

## Table of Contents

- [Overview](#overview)
- [Deployment Environments](#deployment-environments)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Infrastructure Provisioning](#infrastructure-provisioning)
- [CI/CD Pipeline](#cicd-pipeline)
- [Rollback Procedures](#rollback-procedures)

## Overview

The Jane Monorepo supports multiple deployment strategies:

- **Local Development**: Docker Compose
- **Staging**: Kubernetes with staging overlay
- **Production**: Kubernetes with production overlay, auto-scaling

## Deployment Environments

| Environment | Purpose | Configuration | Replicas |
|-------------|---------|--------------|----------|
| Development | Local dev, testing | docker-compose.dev.yml | 1 each |
| Staging | Pre-production testing | overlays/staging | 2 UI/Orch, 1 LLM |
| Production | Live production | overlays/production | 3-10 (HPA) |

## Docker Deployment

### Development Environment

```bash
# Start all services
make dev

# Or directly:
docker-compose -f infrastructure/docker/docker-compose.dev.yml up

# With rebuild:
docker-compose -f infrastructure/docker/docker-compose.dev.yml up --build

# Stop services:
docker-compose -f infrastructure/docker/docker-compose.dev.yml down
```

### Staging Environment

```bash
# Start staging environment
make staging

# Or directly:
docker-compose -f infrastructure/docker/docker-compose.staging.yml up -d

# View logs:
docker-compose -f infrastructure/docker/docker-compose.staging.yml logs -f

# Stop services:
docker-compose -f infrastructure/docker/docker-compose.staging.yml down
```

### Building Individual Images

```bash
# Build all images
make docker-build

# Build specific service:
docker build -t jane-ui:latest -f apps/jane-ui/Dockerfile .
docker build -t jane-orchestrator:latest -f apps/jane-orchestrator/Dockerfile .
docker build -t cyber-llm:latest -f apps/cyber-llm-server/Dockerfile .
```

## Kubernetes Deployment

### Prerequisites

1. **kubectl** installed and configured
2. **Kubernetes cluster** accessible
3. **Docker images** built and pushed to registry

### Deploy to Development

```bash
# Apply namespace
kubectl apply -f infrastructure/kubernetes/namespaces/jane-services.yaml

# Deploy with dev overlay
kubectl apply -k infrastructure/kubernetes/overlays/dev/

# Or using Make:
make k8s-apply-dev

# Check status:
kubectl get pods -n jane-services
kubectl get services -n jane-services
```

### Deploy to Staging

```bash
# Apply namespace
kubectl apply -f infrastructure/kubernetes/namespaces/jane-services.yaml

# Deploy with staging overlay
kubectl apply -k infrastructure/kubernetes/overlays/staging/

# Or using Make:
make k8s-apply-staging

# Check status:
kubectl get pods -n jane-services
kubectl describe deployment staging-jane-ui -n jane-services
```

### Deploy to Production

```bash
# Apply namespace
kubectl apply -f infrastructure/kubernetes/namespaces/jane-services.yaml

# Deploy with production overlay
kubectl apply -k infrastructure/kubernetes/overlays/production/

# Or using Make:
make k8s-apply-prod

# Check status:
kubectl get pods -n jane-services
kubectl get hpa -n jane-services
kubectl top pods -n jane-services
```

### Verify Deployment

```bash
# Check pod status
kubectl get pods -n jane-services

# Check logs
kubectl logs -f deployment/prod-jane-ui -n jane-services
kubectl logs -f deployment/prod-jane-orchestrator -n jane-services

# Check service endpoints
kubectl get services -n jane-services

# Test health endpoints
kubectl port-forward svc/prod-jane-orchestrator 8000:8000 -n jane-services
curl http://localhost:8000/health
```

### Update Deployment

```bash
# Update image tag in kustomization.yaml or deployment
kubectl set image deployment/prod-jane-ui jane-ui=jane-ui:v1.2.0 -n jane-services

# Or apply updated manifests:
kubectl apply -k infrastructure/kubernetes/overlays/production/

# Watch rollout:
kubectl rollout status deployment/prod-jane-ui -n jane-services
```

## Infrastructure Provisioning

### Terraform Setup

```bash
# Initialize Terraform
make terraform-init

# Or directly:
cd infrastructure/terraform
terraform init
```

### Plan Infrastructure Changes

```bash
# See what will be created/changed
make terraform-plan

# Or directly:
cd infrastructure/terraform
terraform plan
```

### Apply Infrastructure

```bash
# Apply changes
make terraform-apply

# Or directly:
cd infrastructure/terraform
terraform apply

# With auto-approve (use cautiously):
terraform apply -auto-approve
```

### Infrastructure Modules

The following modules are available:

1. **k3s-cluster**: Kubernetes cluster
2. **networking**: VPC, subnets, security groups
3. **storage**: Persistent volumes
4. **jane-services**: Core application infrastructure
5. **makoto-services**: Domain services
6. **monitoring**: Observability stack

Example usage in `infrastructure/terraform/main.tf`:

```hcl
module "k3s_cluster" {
  source = "./modules/k3s-cluster"
  
  cluster_name  = "jane-production"
  node_count    = 3
  instance_type = "t3.large"
}

module "networking" {
  source = "./modules/networking"
  
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  enable_nat_gateway = true
}
```

## CI/CD Pipeline

### GitHub Actions Workflows

Three main workflows are configured:

1. **CI (`.github/workflows/ci.yml`)**
   - Triggered on: Push, Pull Request
   - Actions: Lint, test, build
   - Runs on: ubuntu-latest

2. **Deploy (`.github/workflows/deploy.yml`)**
   - Triggered on: Push to main, manual dispatch
   - Actions: Build images, deploy to K8s
   - Environments: staging, production

3. **Release (`.github/workflows/release.yml`)**
   - Triggered on: Git tag push
   - Actions: Create release, publish artifacts
   - Versioning: Semantic versioning

### Manual Deployment with GitHub Actions

```bash
# Trigger deployment workflow
gh workflow run deploy.yml --ref main

# With specific environment
gh workflow run deploy.yml --ref main -f environment=production
```

### Deployment Process

1. **Build Phase**
   ```bash
   # Build all applications
   npx nx run-many --target=build --all
   
   # Build Docker images
   docker build -t registry.example.com/jane-ui:${VERSION} .
   docker build -t registry.example.com/jane-orchestrator:${VERSION} .
   # ... other images
   ```

2. **Push Phase**
   ```bash
   # Push to container registry
   docker push registry.example.com/jane-ui:${VERSION}
   docker push registry.example.com/jane-orchestrator:${VERSION}
   # ... other images
   ```

3. **Deploy Phase**
   ```bash
   # Update Kubernetes manifests
   kubectl set image deployment/prod-jane-ui \
     jane-ui=registry.example.com/jane-ui:${VERSION} \
     -n jane-services
   
   # Or apply updated kustomization
   kubectl apply -k infrastructure/kubernetes/overlays/production/
   ```

4. **Verify Phase**
   ```bash
   # Check rollout status
   kubectl rollout status deployment/prod-jane-ui -n jane-services
   
   # Run smoke tests
   curl https://jane-ui.example.com/api/health
   ```

## Rollback Procedures

### Kubernetes Rollback

```bash
# View rollout history
kubectl rollout history deployment/prod-jane-ui -n jane-services

# Rollback to previous version
kubectl rollout undo deployment/prod-jane-ui -n jane-services

# Rollback to specific revision
kubectl rollout undo deployment/prod-jane-ui --to-revision=3 -n jane-services

# Watch rollback progress
kubectl rollout status deployment/prod-jane-ui -n jane-services
```

### Docker Compose Rollback

```bash
# Stop current version
docker-compose -f infrastructure/docker/docker-compose.staging.yml down

# Pull previous image tags
docker pull registry.example.com/jane-ui:v1.1.0

# Start with previous version
docker-compose -f infrastructure/docker/docker-compose.staging.yml up -d
```

### Manual Rollback Steps

1. **Identify Issue**
   ```bash
   # Check logs
   kubectl logs -f deployment/prod-jane-ui -n jane-services
   
   # Check events
   kubectl get events -n jane-services --sort-by='.lastTimestamp'
   ```

2. **Execute Rollback**
   ```bash
   kubectl rollout undo deployment/prod-jane-ui -n jane-services
   ```

3. **Verify Rollback**
   ```bash
   # Check status
   kubectl rollout status deployment/prod-jane-ui -n jane-services
   
   # Test endpoints
   curl https://jane-ui.example.com/api/health
   ```

4. **Investigate Root Cause**
   - Review application logs
   - Check deployment changes
   - Test in staging environment
   - Fix issues before re-deploying

## Monitoring Deployment

### Health Checks

All services expose health endpoints:

- **Liveness**: `/health` - Is service running?
- **Readiness**: `/ready` - Is service ready for traffic?

### Monitoring Stack

- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **Loki**: Log aggregation
- **Jaeger**: Distributed tracing

Access monitoring:
```bash
# Port forward to Grafana
kubectl port-forward svc/grafana 3000:3000 -n monitoring

# Port forward to Prometheus
kubectl port-forward svc/prometheus 9090:9090 -n monitoring
```

### Key Metrics to Monitor

- **Request Rate**: Requests per second
- **Error Rate**: 5xx errors
- **Latency**: p50, p95, p99 response times
- **Resource Usage**: CPU, memory, disk
- **Pod Status**: Running, pending, failed

## Security Considerations

### Secrets Management

```bash
# Create secrets
kubectl create secret generic app-secrets \
  --from-literal=api-key=xyz123 \
  -n jane-services

# Use in deployment
env:
- name: API_KEY
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: api-key
```

### Network Policies

Apply network policies to restrict pod communication:

```bash
kubectl apply -f infrastructure/kubernetes/network-policies/
```

### Image Security

- Use specific image tags (not `latest`)
- Scan images for vulnerabilities
- Use minimal base images
- Run as non-root user

## Troubleshooting

### Pod Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name> -n jane-services

# Check logs
kubectl logs <pod-name> -n jane-services

# Common issues:
# - Image pull errors: Check registry credentials
# - Resource limits: Adjust limits in deployment
# - Configuration errors: Check environment variables
```

### Service Not Accessible

```bash
# Check service
kubectl get svc -n jane-services

# Check endpoints
kubectl get endpoints -n jane-services

# Check ingress
kubectl get ingress -n jane-services
kubectl describe ingress <ingress-name> -n jane-services
```

### High Resource Usage

```bash
# Check resource usage
kubectl top pods -n jane-services
kubectl top nodes

# Adjust HPA
kubectl autoscale deployment prod-jane-ui \
  --cpu-percent=70 \
  --min=3 \
  --max=15 \
  -n jane-services
```

## Best Practices

1. **Always test in staging** before production
2. **Use semantic versioning** for releases
3. **Keep rollback plan ready**
4. **Monitor deployments** actively
5. **Document all changes**
6. **Use blue-green or canary** deployments for critical updates
7. **Maintain deployment runbooks**

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)
- [Terraform Documentation](https://www.terraform.io/docs/)
- [NX Documentation](https://nx.dev/recipes/deployment)
