# Networking Module

This Terraform module provisions networking infrastructure for the Jane monorepo.

## Features

- VPC with public and private subnets
- NAT gateway for outbound internet access
- Security groups and network ACLs
- Optional VPN endpoint

## Usage

```hcl
module "networking" {
  source = "./modules/networking"

  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]
  enable_nat_gateway = true
  enable_vpn         = false
}
```

## Inputs

| Name | Description | Type | Default |
|------|-------------|------|---------|
| vpc_cidr | CIDR block for VPC | string | "10.0.0.0/16" |
| availability_zones | List of availability zones | list(string) | ["us-east-1a", "us-east-1b", "us-east-1c"] |
| enable_nat_gateway | Enable NAT gateway for private subnets | bool | true |
| enable_vpn | Enable VPN endpoint | bool | false |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | VPC ID |
| public_subnet_ids | List of public subnet IDs |
| private_subnet_ids | List of private subnet IDs |

## Requirements

- Terraform >= 1.0
- AWS provider ~> 5.0

## Network Architecture

The module creates:
- 1 VPC
- 3 public subnets (one per AZ)
- 3 private subnets (one per AZ)
- Internet gateway
- NAT gateway (optional)
- Route tables and associations
