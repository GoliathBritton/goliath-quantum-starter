# Phase 1: Variables for Immediate Production Deployment

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "production"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "partner_admin"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}

variable "domain_name" {
  description = "Domain name for the Partner System"
  type        = string
  default     = "goliathomniedge.com"
}

variable "certificate_arn" {
  description = "SSL certificate ARN for HTTPS"
  type        = string
  default     = ""
}

# Tags
variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Environment = "production"
    System      = "goliath-partner-system"
    Phase       = "phase1"
    ManagedBy   = "terraform"
    Owner       = "goliath-team"
    Project     = "partner-system"
  }
}
