# K3s Cluster Module
# Provisions a K3s Kubernetes cluster

terraform {
  required_version = ">= 1.0"
}

variable "cluster_name" {
  description = "Name of the K3s cluster"
  type        = string
  default     = "jane-k3s-cluster"
}

variable "node_count" {
  description = "Number of nodes in the cluster"
  type        = number
  default     = 3
}

variable "instance_type" {
  description = "Instance type for cluster nodes"
  type        = string
  default     = "t3.medium"
}

output "cluster_endpoint" {
  description = "K3s cluster API endpoint"
  value       = "https://${var.cluster_name}.example.com:6443"
}

output "cluster_ca_certificate" {
  description = "Cluster CA certificate"
  value       = "cluster-ca-cert"
  sensitive   = true
}
