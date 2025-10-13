# Monitoring Module

This Terraform module provisions monitoring and observability infrastructure for the Jane monorepo.

## Components

- **Prometheus**: Metrics collection and alerting
- **Grafana**: Metrics visualization and dashboards
- **Loki**: Log aggregation and querying
- **Jaeger**: Distributed tracing

## Features

- Pre-configured dashboards for all services
- Alert rules for critical metrics
- Log aggregation from all pods
- Distributed tracing across services
- Retention policies for metrics and logs

## Usage

```hcl
module "monitoring" {
  source = "./modules/monitoring"

  environment       = "production"
  enable_prometheus = true
  enable_grafana    = true
  enable_loki       = true
  enable_jaeger     = true
  retention_days    = 90
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| environment | Environment name (dev, staging, production) | string | "dev" |
| enable_prometheus | Enable Prometheus monitoring | bool | true |
| enable_grafana | Enable Grafana dashboards | bool | true |
| enable_loki | Enable Loki log aggregation | bool | true |
| enable_jaeger | Enable Jaeger distributed tracing | bool | true |
| retention_days | Metrics and logs retention period in days | number | 30 |

## Outputs

| Name | Description |
|------|-------------|
| prometheus_endpoint | Prometheus endpoint |
| grafana_endpoint | Grafana endpoint |
| loki_endpoint | Loki endpoint |
| jaeger_endpoint | Jaeger endpoint |

## Requirements

- Terraform >= 1.0
- AWS provider ~> 5.0
- Kubernetes cluster (from k3s-cluster module)

## Pre-configured Dashboards

- Service health and availability
- Request rates and latencies
- Error rates and types
- Resource utilization (CPU, memory, disk)
- Database performance
- LLM server metrics

## Alert Rules

- High error rates
- Service unavailability
- Resource exhaustion
- Slow response times
- Failed deployments
