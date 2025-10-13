# Monitoring Module
# Provisions monitoring and observability resources

terraform {
  required_version = ">= 1.0"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "dev"
}

variable "enable_prometheus" {
  description = "Enable Prometheus monitoring"
  type        = bool
  default     = true
}

variable "enable_grafana" {
  description = "Enable Grafana dashboards"
  type        = bool
  default     = true
}

variable "enable_loki" {
  description = "Enable Loki log aggregation"
  type        = bool
  default     = true
}

variable "enable_jaeger" {
  description = "Enable Jaeger distributed tracing"
  type        = bool
  default     = true
}

variable "retention_days" {
  description = "Metrics and logs retention period in days"
  type        = number
  default     = 30
}

output "prometheus_endpoint" {
  description = "Prometheus endpoint"
  value       = var.enable_prometheus ? "https://prometheus-${var.environment}.example.com" : null
}

output "grafana_endpoint" {
  description = "Grafana endpoint"
  value       = var.enable_grafana ? "https://grafana-${var.environment}.example.com" : null
}

output "loki_endpoint" {
  description = "Loki endpoint"
  value       = var.enable_loki ? "https://loki-${var.environment}.example.com" : null
}

output "jaeger_endpoint" {
  description = "Jaeger endpoint"
  value       = var.enable_jaeger ? "https://jaeger-${var.environment}.example.com" : null
}
