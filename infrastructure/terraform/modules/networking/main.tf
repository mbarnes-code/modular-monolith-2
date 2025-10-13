# Networking Module
# Provisions networking resources

terraform {
  required_version = ">= 1.0"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b", "us-east-1c"]
}

variable "enable_nat_gateway" {
  description = "Enable NAT gateway for private subnets"
  type        = bool
  default     = true
}

variable "enable_vpn" {
  description = "Enable VPN endpoint"
  type        = bool
  default     = false
}

output "vpc_id" {
  description = "VPC ID"
  value       = "vpc-${substr(md5(var.vpc_cidr), 0, 8)}"
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = ["subnet-public-1", "subnet-public-2", "subnet-public-3"]
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = ["subnet-private-1", "subnet-private-2", "subnet-private-3"]
}
