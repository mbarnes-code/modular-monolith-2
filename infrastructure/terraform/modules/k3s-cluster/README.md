# K3s Cluster Module

This Terraform module provisions a K3s Kubernetes cluster for the Jane monorepo.

## Features

- Lightweight Kubernetes distribution
- Optimized for edge and IoT deployments
- Fast startup times
- Low resource requirements

## Usage

```hcl
module "k3s_cluster" {
  source = "./modules/k3s-cluster"

  cluster_name  = "jane-production"
  node_count    = 3
  instance_type = "t3.medium"
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| cluster_name | Name of the K3s cluster | string | "jane-k3s-cluster" |
| node_count | Number of nodes in the cluster | number | 3 |
| instance_type | Instance type for cluster nodes | string | "t3.medium" |

## Outputs

| Name | Description |
|------|-------------|
| cluster_endpoint | K3s cluster API endpoint |
| cluster_ca_certificate | Cluster CA certificate (sensitive) |

## Requirements

- Terraform >= 1.0
- AWS provider ~> 5.0

## Notes

This module is designed to work with the Jane monorepo infrastructure and integrates with the networking and storage modules.
