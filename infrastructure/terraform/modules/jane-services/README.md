# Jane Services Module

This Terraform module provisions infrastructure for Jane services including the UI, orchestrator, and LLM servers.

## Services Included

- **Jane UI**: Next.js 15 + React 19 frontend
- **Jane Orchestrator**: FastAPI orchestration service
- **LLM Servers**: Cyber, MTG, and Code LLM services

## Features

- Auto-scaling for all services
- Load balancing
- Health checks and monitoring
- Blue-green deployment support

## Usage

```hcl
module "jane_services" {
  source = "./modules/jane-services"

  environment           = "production"
  orchestrator_replicas = 3
  llm_server_replicas   = 2
  ui_replicas           = 3
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| environment | Environment name (dev, staging, production) | string | "dev" |
| orchestrator_replicas | Number of orchestrator replicas | number | 2 |
| llm_server_replicas | Number of LLM server replicas per service | number | 1 |
| ui_replicas | Number of UI replicas | number | 2 |

## Outputs

| Name | Description |
|------|-------------|
| jane_ui_endpoint | Jane UI endpoint |
| orchestrator_endpoint | Orchestrator service endpoint |
| llm_endpoints | LLM server endpoints (cyber, mtg, code) |

## Requirements

- Terraform >= 1.0
- AWS provider ~> 5.0
- Kubernetes cluster (from k3s-cluster module)

## Service Architecture

All services are deployed as Kubernetes workloads with:
- Horizontal Pod Autoscaling
- Service mesh integration
- Distributed tracing
- Centralized logging
