# NQBA Platform - Production Environment Variables

# AWS Configuration
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "aws_profile" {
  description = "AWS profile to use"
  type        = string
  default     = "default"
}

# VPC Configuration
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnets" {
  description = "Private subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
}

variable "public_subnets" {
  description = "Public subnet CIDR blocks"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
}

# EKS Configuration
variable "kubernetes_version" {
  description = "Kubernetes version for EKS cluster"
  type        = string
  default     = "1.28"
}

variable "cluster_endpoint_public_access_cidrs" {
  description = "List of CIDR blocks that can access the EKS cluster endpoint"
  type        = list(string)
  default     = ["0.0.0.0/0"]  # Restrict this in production
}

# Main Node Group Configuration
variable "node_group_desired_capacity" {
  description = "Desired number of nodes in the main node group"
  type        = number
  default     = 3
}

variable "node_group_max_capacity" {
  description = "Maximum number of nodes in the main node group"
  type        = number
  default     = 10
}

variable "node_group_min_capacity" {
  description = "Minimum number of nodes in the main node group"
  type        = number
  default     = 1
}

variable "node_group_instance_types" {
  description = "Instance types for the main node group"
  type        = list(string)
  default     = ["m5.large", "m5.xlarge"]
}

# Spot Node Group Configuration
variable "spot_node_group_desired_capacity" {
  description = "Desired number of nodes in the spot node group"
  type        = number
  default     = 2
}

variable "spot_node_group_max_capacity" {
  description = "Maximum number of nodes in the spot node group"
  type        = number
  default     = 20
}

variable "spot_node_group_min_capacity" {
  description = "Minimum number of nodes in the spot node group"
  type        = number
  default     = 0
}

variable "spot_node_group_instance_types" {
  description = "Instance types for the spot node group"
  type        = list(string)
  default     = ["m5.large", "m5.xlarge", "c5.large", "c5.xlarge"]
}

# RDS Configuration
variable "postgres_version" {
  description = "PostgreSQL version"
  type        = string
  default     = "15.4"
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.r6g.large"
}

variable "db_allocated_storage" {
  description = "Initial allocated storage for RDS instance (GB)"
  type        = number
  default     = 100
}

variable "db_max_allocated_storage" {
  description = "Maximum allocated storage for RDS instance (GB)"
  type        = number
  default     = 1000
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "nqba_prod"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "nqba_admin"
}

variable "db_backup_retention_period" {
  description = "Database backup retention period (days)"
  type        = number
  default     = 30
}

variable "db_backup_window" {
  description = "Database backup window"
  type        = string
  default     = "03:00-04:00"
}

variable "db_maintenance_window" {
  description = "Database maintenance window"
  type        = string
  default     = "sun:04:00-sun:05:00"
}

# Redis Configuration
variable "redis_node_type" {
  description = "ElastiCache Redis node type"
  type        = string
  default     = "cache.r6g.large"
}

variable "redis_num_cache_nodes" {
  description = "Number of cache nodes in the Redis cluster"
  type        = number
  default     = 3
}

# Domain and SSL Configuration
variable "domain_name" {
  description = "Domain name for the application"
  type        = string
  default     = "nqba.flyfox.ai"
}

variable "create_route53_zone" {
  description = "Whether to create a Route53 hosted zone"
  type        = bool
  default     = false
}

variable "create_acm_certificate" {
  description = "Whether to create an ACM certificate"
  type        = bool
  default     = false
}

# Monitoring and Logging
variable "log_retention_days" {
  description = "CloudWatch log retention period (days)"
  type        = number
  default     = 30
}

variable "enable_container_insights" {
  description = "Enable CloudWatch Container Insights"
  type        = bool
  default     = true
}

# Security Configuration
variable "enable_irsa" {
  description = "Enable IAM Roles for Service Accounts"
  type        = bool
  default     = true
}

variable "enable_cluster_autoscaler" {
  description = "Enable cluster autoscaler"
  type        = bool
  default     = true
}

variable "enable_aws_load_balancer_controller" {
  description = "Enable AWS Load Balancer Controller"
  type        = bool
  default     = true
}

variable "enable_external_dns" {
  description = "Enable External DNS"
  type        = bool
  default     = false
}

variable "enable_cert_manager" {
  description = "Enable cert-manager"
  type        = bool
  default     = false
}

# Application Configuration
variable "app_name" {
  description = "Application name"
  type        = string
  default     = "nqba-platform"
}

variable "app_version" {
  description = "Application version"
  type        = string
  default     = "latest"
}

variable "app_replicas" {
  description = "Number of application replicas"
  type        = number
  default     = 3
}

variable "app_cpu_request" {
  description = "CPU request for application pods"
  type        = string
  default     = "500m"
}

variable "app_memory_request" {
  description = "Memory request for application pods"
  type        = string
  default     = "1Gi"
}

variable "app_cpu_limit" {
  description = "CPU limit for application pods"
  type        = string
  default     = "2000m"
}

variable "app_memory_limit" {
  description = "Memory limit for application pods"
  type        = string
  default     = "4Gi"
}

# Worker Configuration
variable "worker_replicas" {
  description = "Number of worker replicas"
  type        = number
  default     = 2
}

variable "worker_cpu_request" {
  description = "CPU request for worker pods"
  type        = string
  default     = "1000m"
}

variable "worker_memory_request" {
  description = "Memory request for worker pods"
  type        = string
  default     = "2Gi"
}

variable "worker_cpu_limit" {
  description = "CPU limit for worker pods"
  type        = string
  default     = "4000m"
}

variable "worker_memory_limit" {
  description = "Memory limit for worker pods"
  type        = string
  default     = "8Gi"
}

# Cost Optimization
variable "enable_spot_instances" {
  description = "Enable spot instances for cost optimization"
  type        = bool
  default     = true
}

variable "spot_instance_percentage" {
  description = "Percentage of spot instances in the cluster"
  type        = number
  default     = 50
}

# Backup and Disaster Recovery
variable "enable_cross_region_backup" {
  description = "Enable cross-region backup"
  type        = bool
  default     = true
}

variable "backup_region" {
  description = "Backup region for disaster recovery"
  type        = string
  default     = "us-east-1"
}

# Environment-specific tags
variable "additional_tags" {
  description = "Additional tags to apply to all resources"
  type        = map(string)
  default = {
    Environment = "production"
    Project     = "nqba-platform"
    Owner       = "flyfox-ai"
    CostCenter  = "engineering"
    Compliance  = "required"
  }
}