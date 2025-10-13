# Storage Module

This Terraform module provisions storage resources for the Jane monorepo infrastructure.

## Features

- Persistent volume storage
- Encryption at rest
- Automatic backups
- Scalable storage capacity

## Usage

```hcl
module "storage" {
  source = "./modules/storage"

  environment       = "production"
  storage_size_gb   = 500
  storage_type      = "gp3"
  enable_encryption = true
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| environment | Environment name (dev, staging, production) | string | "dev" |
| storage_size_gb | Storage size in GB | number | 100 |
| storage_type | Storage type (gp3, io1, etc.) | string | "gp3" |
| enable_encryption | Enable storage encryption | bool | true |

## Outputs

| Name | Description |
|------|-------------|
| storage_id | Storage resource ID |
| storage_endpoint | Storage endpoint URL |

## Requirements

- Terraform >= 1.0
- AWS provider ~> 5.0

## Notes

This module provides persistent storage for stateful services in the cluster, including databases and file storage.
