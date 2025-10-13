# Jane Services Module
# Provisions resources for Jane services (UI, Orchestrator, LLM servers)

terraform {
  required_version = ">= 1.0"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "dev"
}

variable "orchestrator_replicas" {
  description = "Number of orchestrator replicas"
  type        = number
  default     = 2
}

variable "llm_server_replicas" {
  description = "Number of LLM server replicas per service"
  type        = number
  default     = 1
}

variable "ui_replicas" {
  description = "Number of UI replicas"
  type        = number
  default     = 2
}

output "jane_ui_endpoint" {
  description = "Jane UI endpoint"
  value       = "https://jane-ui-${var.environment}.example.com"
}

output "orchestrator_endpoint" {
  description = "Orchestrator service endpoint"
  value       = "https://orchestrator-${var.environment}.example.com"
}

output "llm_endpoints" {
  description = "LLM server endpoints"
  value = {
    cyber = "https://cyber-llm-${var.environment}.example.com"
    mtg   = "https://mtg-llm-${var.environment}.example.com"
    code  = "https://code-llm-${var.environment}.example.com"
  }
}
