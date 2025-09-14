# Goliath Quantum - Terraform Outputs
# Output values for infrastructure components

# EKS Cluster Outputs
output "cluster_id" {
  description = "EKS cluster ID"
  value       = module.eks.cluster_id
}

output "cluster_arn" {
  description = "EKS cluster ARN"
  value       = module.eks.cluster_arn
}

output "cluster_endpoint" {
  description = "Endpoint for EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "cluster_security_group_id" {
  description = "Security group ids attached to the cluster control plane"
  value       = module.eks.cluster_security_group_id
}

output "cluster_iam_role_name" {
  description = "IAM role name associated with EKS cluster"
  value       = module.eks.cluster_iam_role_name
}

output "cluster_iam_role_arn" {
  description = "IAM role ARN associated with EKS cluster"
  value       = module.eks.cluster_iam_role_arn
}

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = module.eks.cluster_certificate_authority_data
}

output "cluster_primary_security_group_id" {
  description = "Cluster security group that was created by Amazon EKS for the cluster"
  value       = module.eks.cluster_primary_security_group_id
}

output "oidc_provider_arn" {
  description = "The ARN of the OIDC Provider if enabled"
  value       = module.eks.oidc_provider_arn
}

# Node Group Outputs
output "eks_managed_node_groups" {
  description = "Map of attribute maps for all EKS managed node groups created"
  value       = module.eks.eks_managed_node_groups
  sensitive   = true
}

output "eks_managed_node_groups_autoscaling_group_names" {
  description = "List of the autoscaling group names created by EKS managed node groups"
  value       = module.eks.eks_managed_node_groups_autoscaling_group_names
}

# VPC Outputs
output "vpc_id" {
  description = "ID of the VPC where the cluster and its nodes will be provisioned"
  value       = module.vpc.vpc_id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

output "private_subnets" {
  description = "List of IDs of private subnets"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "List of IDs of public subnets"
  value       = module.vpc.public_subnets
}

output "nat_gateway_ids" {
  description = "List of IDs of the NAT Gateways"
  value       = module.vpc.natgw_ids
}

output "internet_gateway_id" {
  description = "The ID of the Internet Gateway"
  value       = module.vpc.igw_id
}

# Database Outputs
output "db_instance_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "db_instance_id" {
  description = "RDS instance ID"
  value       = aws_db_instance.main.id
}

output "db_instance_port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

output "db_subnet_group_id" {
  description = "RDS subnet group ID"
  value       = aws_db_subnet_group.main.id
}

output "db_security_group_id" {
  description = "RDS security group ID"
  value       = aws_security_group.rds.id
}

# Redis Outputs
output "redis_endpoint" {
  description = "Redis cluster endpoint"
  value       = aws_elasticache_replication_group.main.primary_endpoint_address
  sensitive   = true
}

output "redis_port" {
  description = "Redis cluster port"
  value       = aws_elasticache_replication_group.main.port
}

output "redis_security_group_id" {
  description = "Redis security group ID"
  value       = aws_security_group.redis.id
}

# ECR Outputs
output "ecr_api_repository_url" {
  description = "ECR repository URL for API"
  value       = aws_ecr_repository.api.repository_url
}

output "ecr_web_repository_url" {
  description = "ECR repository URL for web frontend"
  value       = aws_ecr_repository.web.repository_url
}

output "ecr_api_repository_arn" {
  description = "ECR repository ARN for API"
  value       = aws_ecr_repository.api.arn
}

output "ecr_web_repository_arn" {
  description = "ECR repository ARN for web frontend"
  value       = aws_ecr_repository.web.arn
}

# S3 Outputs
output "s3_bucket_id" {
  description = "S3 bucket ID for application data"
  value       = aws_s3_bucket.app_data.id
}

output "s3_bucket_arn" {
  description = "S3 bucket ARN for application data"
  value       = aws_s3_bucket.app_data.arn
}

output "s3_bucket_domain_name" {
  description = "S3 bucket domain name"
  value       = aws_s3_bucket.app_data.bucket_domain_name
}

# Secrets Manager Outputs
output "db_secret_arn" {
  description = "ARN of the database credentials secret"
  value       = aws_secretsmanager_secret.db_credentials.arn
}

output "dynex_secret_arn" {
  description = "ARN of the Dynex API credentials secret"
  value       = aws_secretsmanager_secret.dynex_api.arn
}

# Route53 and SSL Outputs
output "route53_zone_id" {
  description = "Route53 hosted zone ID"
  value       = var.create_route53_zone ? aws_route53_zone.main[0].zone_id : null
}

output "route53_zone_name_servers" {
  description = "Route53 hosted zone name servers"
  value       = var.create_route53_zone ? aws_route53_zone.main[0].name_servers : null
}

output "acm_certificate_arn" {
  description = "ACM certificate ARN"
  value       = var.create_route53_zone ? aws_acm_certificate.main[0].arn : null
}

output "acm_certificate_status" {
  description = "ACM certificate status"
  value       = var.create_route53_zone ? aws_acm_certificate.main[0].status : null
}

# IAM Outputs
output "eks_admin_role_arn" {
  description = "ARN of the EKS admin role"
  value       = aws_iam_role.eks_admin.arn
}

output "rds_monitoring_role_arn" {
  description = "ARN of the RDS monitoring role"
  value       = aws_iam_role.rds_monitoring.arn
}

# Kubectl Configuration
output "kubectl_config" {
  description = "kubectl config as generated by the module"
  value = {
    cluster_name     = module.eks.cluster_id
    endpoint         = module.eks.cluster_endpoint
    ca_data          = module.eks.cluster_certificate_authority_data
    aws_region       = var.aws_region
  }
  sensitive = true
}

# Application URLs (when using ALB)
output "application_urls" {
  description = "Application URLs"
  value = {
    api_docs = var.create_route53_zone ? "https://api.${var.domain_name}/docs" : "https://<ALB_DNS_NAME>/docs"
    frontend = var.create_route53_zone ? "https://${var.domain_name}" : "https://<ALB_DNS_NAME>"
    grafana  = var.create_route53_zone ? "https://grafana.${var.domain_name}" : "https://<ALB_DNS_NAME>/grafana"
  }
}

# Cost Estimation
output "estimated_monthly_cost" {
  description = "Estimated monthly cost breakdown (USD)"
  value = {
    eks_cluster    = "73.00"  # $0.10/hour
    ec2_instances  = "150.00" # 3 x t3.large + 2 x c5.2xlarge
    rds_postgres   = "85.00"  # db.t3.medium
    elasticache    = "25.00"  # cache.t3.micro x 2
    nat_gateways   = "135.00" # 3 x $45/month
    data_transfer  = "50.00"  # Estimated
    storage        = "30.00"  # EBS + S3
    total_estimate = "548.00"
    note          = "Costs may vary based on usage patterns and data transfer"
  }
}

# Security Information
output "security_groups" {
  description = "Security group information"
  value = {
    cluster_sg = module.eks.cluster_security_group_id
    node_sg    = module.eks.node_security_group_id
    rds_sg     = aws_security_group.rds.id
    redis_sg   = aws_security_group.redis.id
  }
}

# Monitoring and Logging
output "monitoring_endpoints" {
  description = "Monitoring and logging endpoints"
  value = {
    cloudwatch_log_groups = {
      cluster = "/aws/eks/${var.cluster_name}/cluster"
      vpc_flow_logs = "/aws/vpc/flowlogs"
    }
    performance_insights = {
      rds_enabled = aws_db_instance.main.performance_insights_enabled
    }
  }
}

# Backup Information
output "backup_configuration" {
  description = "Backup configuration details"
  value = {
    rds_backup_retention = aws_db_instance.main.backup_retention_period
    rds_backup_window   = aws_db_instance.main.backup_window
    redis_snapshot_retention = aws_elasticache_replication_group.main.snapshot_retention_limit
    redis_snapshot_window = aws_elasticache_replication_group.main.snapshot_window
  }
}