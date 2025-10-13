# Storage Module
# Provisions storage resources for the cluster

terraform {
  required_version = ">= 1.0"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "dev"
}

variable "storage_size_gb" {
  description = "Storage size in GB"
  type        = number
  default     = 100
}

variable "storage_type" {
  description = "Storage type (gp3, io1, etc.)"
  type        = string
  default     = "gp3"
}

variable "enable_encryption" {
  description = "Enable storage encryption"
  type        = bool
  default     = true
}

output "storage_id" {
  description = "Storage resource ID"
  value       = "storage-${var.environment}"
}

output "storage_endpoint" {
  description = "Storage endpoint URL"
  value       = "https://storage-${var.environment}.example.com"
}
