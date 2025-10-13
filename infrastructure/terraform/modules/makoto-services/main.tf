# Makoto Services Module
# Provisions resources for Makoto domain services

terraform {
  required_version = ">= 1.0"
}

variable "environment" {
  description = "Environment name (dev, staging, production)"
  type        = string
  default     = "dev"
}

variable "enable_security_services" {
  description = "Enable security domain services (MISP, Nemesis, etc.)"
  type        = bool
  default     = true
}

variable "enable_mtg_services" {
  description = "Enable MTG domain services (Commander Spellbook, etc.)"
  type        = bool
  default     = true
}

variable "enable_productivity_services" {
  description = "Enable productivity services (n8n, Actual Budget, etc.)"
  type        = bool
  default     = true
}

output "security_services_endpoints" {
  description = "Security services endpoints"
  value = var.enable_security_services ? {
    misp       = "https://misp-${var.environment}.example.com"
    nemesis    = "https://nemesis-${var.environment}.example.com"
    dispatch   = "https://dispatch-${var.environment}.example.com"
    ghostwriter = "https://ghostwriter-${var.environment}.example.com"
  } : {}
}

output "mtg_services_endpoints" {
  description = "MTG services endpoints"
  value = var.enable_mtg_services ? {
    spellbook_backend  = "https://spellbook-api-${var.environment}.example.com"
    spellbook_frontend = "https://spellbook-${var.environment}.example.com"
  } : {}
}

output "productivity_services_endpoints" {
  description = "Productivity services endpoints"
  value = var.enable_productivity_services ? {
    n8n           = "https://n8n-${var.environment}.example.com"
    actual_budget = "https://budget-${var.environment}.example.com"
    mealie        = "https://mealie-${var.environment}.example.com"
  } : {}
}
