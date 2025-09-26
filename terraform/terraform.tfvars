# FLYFOX AI - Terraform Variables for Production

# General Configuration
aws_region   = "us-west-2"
environment  = "production"
project_name = "flyfox"

# VPC Configuration
vpc_cidr = "10.0.0.0/16"
private_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
public_subnets   = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
database_subnets = ["10.0.201.0/24", "10.0.202.0/24", "10.0.203.0/24"]

# EKS Configuration
cluster_name       = "flyfox-production-eks"
kubernetes_version = "1.28"

# EKS Admin Users (customize with your IAM users)
eks_admin_users = [
  {
    userarn  = "arn:aws:iam::123456789012:user/admin-user"
    username = "admin-user"
    groups   = ["system:masters"]
  }
]

# RDS Configuration
rds_instance_class        = "db.r5.large"
rds_allocated_storage     = 100
rds_max_allocated_storage = 1000
database_name             = "flyfox"
database_username         = "flyfox_admin"
database_password         = "SECURE_PASSWORD_PLACEHOLDER"  # Replace with secure password

# ElastiCache Configuration
redis_node_type        = "cache.r6g.large"
redis_num_cache_nodes  = 2
redis_auth_token       = "SECURE_REDIS_TOKEN_PLACEHOLDER"  # Replace with secure token

# Domain and SSL Configuration
domain_name         = "flyfox.ai"  # Change to your domain
create_route53_zone = false        # Set to true if you want Terraform to manage DNS

# Monitoring and Logging
enable_cloudwatch_logs = true
log_retention_days     = 30

# Security Configuration
enable_encryption    = true
allowed_cidr_blocks = ["0.0.0.0/0"]  # Restrict this in production

# Cost Optimization
enable_spot_instances      = true
enable_cluster_autoscaler  = true

# Backup Configuration
backup_retention_period = 7

# Application Configuration
app_replicas = {
  api            = 3
  worker         = 5
  quantum_worker = 2
  frontend       = 3
}

resource_limits = {
  api = {
    cpu    = "1000m"
    memory = "2Gi"
  }
  worker = {
    cpu    = "2000m"
    memory = "4Gi"
  }
  quantum_worker = {
    cpu    = "4000m"
    memory = "8Gi"
  }
  frontend = {
    cpu    = "500m"
    memory = "1Gi"
  }
}

# External Services Configuration (REQUIRED - Get from service providers)
twilio_account_sid = "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # From Twilio Console
twilio_auth_token  = "your_twilio_auth_token_here"         # From Twilio Console
openai_api_key     = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # From OpenAI
dynex_api_key      = "your_dynex_api_key_here"            # From Dynex
sentry_dsn         = "https://xxxxx@xxxxx.ingest.sentry.io/xxxxx"  # From Sentry

# Feature Flags
enable_gpu_nodes           = true
enable_monitoring_stack    = true
enable_ingress_controller  = true
enable_cert_manager        = true

# Development Configuration
enable_bastion_host = false  # Set to true for secure SSH access
enable_vpn          = false  # Set to true if you need VPN access

# Compliance and Governance
enable_config     = true
enable_cloudtrail = true
enable_guardduty  = true

# Additional Tags
additional_tags = {
  "CostCenter"    = "Engineering"
  "Owner"         = "DevOps Team"
  "BusinessUnit"  = "AI Platform"
  "Compliance"    = "SOC2"
}