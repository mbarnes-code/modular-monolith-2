# Makoto Services Module

This Terraform module provisions infrastructure for Makoto domain services across security, MTG, and productivity domains.

## Service Domains

### Security Domain
- MISP: Threat intelligence platform
- Nemesis: Offensive security platform
- Dispatch: Incident management
- Ghostwriter: Reporting and collaboration

### MTG Domain
- Commander Spellbook Backend: Combo database API
- Commander Spellbook Frontend: Web interface

### Productivity Domain
- n8n: Workflow automation
- Actual Budget: Personal finance
- Mealie: Recipe management

## Features

- Domain-based service grouping
- Optional service enablement
- Shared authentication and authorization
- Cross-domain service communication

## Usage

```hcl
module "makoto_services" {
  source = "./modules/makoto-services"

  environment                    = "production"
  enable_security_services       = true
  enable_mtg_services            = true
  enable_productivity_services   = true
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| environment | Environment name (dev, staging, production) | string | "dev" |
| enable_security_services | Enable security domain services | bool | true |
| enable_mtg_services | Enable MTG domain services | bool | true |
| enable_productivity_services | Enable productivity services | bool | true |

## Outputs

| Name | Description |
|------|-------------|
| security_services_endpoints | Security services endpoints |
| mtg_services_endpoints | MTG services endpoints |
| productivity_services_endpoints | Productivity services endpoints |

## Requirements

- Terraform >= 1.0
- AWS provider ~> 5.0
- Kubernetes cluster (from k3s-cluster module)

## Integration

This module integrates with:
- Networking module for service discovery
- Storage module for persistent data
- Monitoring module for observability
