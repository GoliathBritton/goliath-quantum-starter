# FLYFOX AI - Terraform Outputs
# Output values for infrastructure components

# VPC Outputs
output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr_block" {
  description = "CIDR block of the VPC"
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

output "database_subnets" {
  description = "List of IDs of database subnets"
  value       = module.vpc.database_subnets
}

output "nat_gateway_ids" {
  description = "List of IDs of the NAT Gateways"
  value       = module.vpc.natgw_ids
}

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
  description = "Security group ID attached to the EKS cluster"
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

output "cluster_oidc_issuer_url" {
  description = "The URL on the EKS cluster for the OpenID Connect identity provider"
  value       = module.eks.cluster_oidc_issuer_url
}

output "oidc_provider_arn" {
  description = "The ARN of the OIDC Provider if enabled"
  value       = module.eks.oidc_provider_arn
}

# EKS Node Groups
output "eks_managed_node_groups" {
  description = "Map of attribute maps for all EKS managed node groups created"
  value       = module.eks.eks_managed_node_groups
  sensitive   = true
}

output "eks_managed_node_groups_autoscaling_group_names" {
  description = "List of the autoscaling group names created by EKS managed node groups"
  value       = module.eks.eks_managed_node_groups_autoscaling_group_names
}

# RDS Outputs
output "rds_instance_id" {
  description = "RDS instance ID"
  value       = aws_db_instance.main.id
}

output "rds_instance_arn" {
  description = "RDS instance ARN"
  value       = aws_db_instance.main.arn
}

output "rds_instance_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = true
}

output "rds_instance_hosted_zone_id" {
  description = "RDS instance hosted zone ID"
  value       = aws_db_instance.main.hosted_zone_id
}

output "rds_instance_port" {
  description = "RDS instance port"
  value       = aws_db_instance.main.port
}

output "rds_instance_name" {
  description = "RDS instance name"
  value       = aws_db_instance.main.db_name
}

output "rds_instance_username" {
  description = "RDS instance root username"
  value       = aws_db_instance.main.username
  sensitive   = true
}

output "rds_subnet_group_id" {
  description = "RDS subnet group ID"
  value       = aws_db_subnet_group.main.id
}

output "rds_subnet_group_arn" {
  description = "RDS subnet group ARN"
  value       = aws_db_subnet_group.main.arn
}

# ElastiCache Outputs
output "elasticache_replication_group_id" {
  description = "ElastiCache replication group ID"
  value       = aws_elasticache_replication_group.main.id
}

output "elasticache_replication_group_arn" {
  description = "ElastiCache replication group ARN"
  value       = aws_elasticache_replication_group.main.arn
}

output "elasticache_primary_endpoint_address" {
  description = "ElastiCache primary endpoint address"
  value       = aws_elasticache_replication_group.main.primary_endpoint_address
  sensitive   = true
}

output "elasticache_reader_endpoint_address" {
  description = "ElastiCache reader endpoint address"
  value       = aws_elasticache_replication_group.main.reader_endpoint_address
  sensitive   = true
}

output "elasticache_port" {
  description = "ElastiCache port"
  value       = aws_elasticache_replication_group.main.port
}

# ECR Outputs
output "ecr_repository_urls" {
  description = "Map of ECR repository URLs"
  value = {
    for k, v in aws_ecr_repository.repositories : k => v.repository_url
  }
}

output "ecr_repository_arns" {
  description = "Map of ECR repository ARNs"
  value = {
    for k, v in aws_ecr_repository.repositories : k => v.arn
  }
}

# S3 Outputs
output "s3_bucket_artifacts_id" {
  description = "S3 artifacts bucket ID"
  value       = aws_s3_bucket.artifacts.id
}

output "s3_bucket_artifacts_arn" {
  description = "S3 artifacts bucket ARN"
  value       = aws_s3_bucket.artifacts.arn
}

output "s3_bucket_backups_id" {
  description = "S3 backups bucket ID"
  value       = aws_s3_bucket.backups.id
}

output "s3_bucket_backups_arn" {
  description = "S3 backups bucket ARN"
  value       = aws_s3_bucket.backups.arn
}

output "s3_bucket_logs_id" {
  description = "S3 logs bucket ID"
  value       = aws_s3_bucket.logs.id
}

output "s3_bucket_logs_arn" {
  description = "S3 logs bucket ARN"
  value       = aws_s3_bucket.logs.arn
}

# Security Group Outputs
output "eks_nodes_security_group_id" {
  description = "Security group ID for EKS nodes"
  value       = aws_security_group.eks_nodes.id
}

output "rds_security_group_id" {
  description = "Security group ID for RDS"
  value       = aws_security_group.rds.id
}

output "elasticache_security_group_id" {
  description = "Security group ID for ElastiCache"
  value       = aws_security_group.elasticache.id
}

# IAM Outputs
output "eks_admin_role_arn" {
  description = "ARN of the EKS admin IAM role"
  value       = aws_iam_role.eks_admin.arn
}

output "rds_monitoring_role_arn" {
  description = "ARN of the RDS monitoring IAM role"
  value       = aws_iam_role.rds_monitoring.arn
}

output "load_balancer_controller_role_arn" {
  description = "ARN of the AWS Load Balancer Controller IAM role"
  value       = module.load_balancer_controller_irsa_role.iam_role_arn
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
  description = "ARN of the ACM certificate"
  value       = var.create_route53_zone ? aws_acm_certificate.main[0].arn : null
}

output "acm_certificate_status" {
  description = "Status of the ACM certificate"
  value       = var.create_route53_zone ? aws_acm_certificate.main[0].status : null
}

# Kubernetes Configuration
output "kubectl_config" {
  description = "kubectl config as generated by the module"
  value = {
    cluster_name                     = module.eks.cluster_id
    endpoint                        = module.eks.cluster_endpoint
    certificate_authority_data      = module.eks.cluster_certificate_authority_data
    region                         = var.aws_region
  }
  sensitive = true
}

# Application Configuration
output "application_config" {
  description = "Configuration values for application deployment"
  value = {
    namespace = "flyfox"
    
    database = {
      host     = aws_db_instance.main.endpoint
      port     = aws_db_instance.main.port
      name     = aws_db_instance.main.db_name
      username = aws_db_instance.main.username
    }
    
    redis = {
      host = aws_elasticache_replication_group.main.primary_endpoint_address
      port = aws_elasticache_replication_group.main.port
    }
    
    ecr_repositories = {
      for k, v in aws_ecr_repository.repositories : k => v.repository_url
    }
    
    s3_buckets = {
      artifacts = aws_s3_bucket.artifacts.id
      backups   = aws_s3_bucket.backups.id
      logs      = aws_s3_bucket.logs.id
    }
  }
  sensitive = true
}

# Monitoring and Observability
output "monitoring_config" {
  description = "Configuration for monitoring and observability"
  value = {
    cloudwatch_log_groups = {
      cluster = "/aws/eks/${module.eks.cluster_id}/cluster"
      vpc     = module.vpc.vpc_flow_log_cloudwatch_log_group_name
    }
    
    prometheus_namespace = "monitoring"
    grafana_namespace   = "monitoring"
  }
}

# Cost Optimization
output "cost_optimization" {
  description = "Cost optimization recommendations"
  value = {
    spot_instances_enabled = var.enable_spot_instances
    autoscaling_enabled   = var.enable_cluster_autoscaler
    
    estimated_monthly_cost = {
      eks_cluster    = "$73 (cluster) + $150-500 (nodes)"
      rds_instance   = "$150-800 (depending on instance class)"
      elasticache    = "$50-200 (depending on node type)"
      nat_gateways   = "$135 (3 AZs)"
      load_balancer  = "$25-50"
      data_transfer  = "Variable based on usage"
      total_estimate = "$583-1758/month (base infrastructure)"
    }
  }
}

# Security and Compliance
output "security_config" {
  description = "Security and compliance configuration"
  value = {
    encryption_enabled = var.enable_encryption
    
    security_groups = {
      eks_nodes    = aws_security_group.eks_nodes.id
      rds          = aws_security_group.rds.id
      elasticache  = aws_security_group.elasticache.id
    }
    
    iam_roles = {
      eks_admin      = aws_iam_role.eks_admin.arn
      rds_monitoring = aws_iam_role.rds_monitoring.arn
      load_balancer  = module.load_balancer_controller_irsa_role.iam_role_arn
    }
    
    compliance_features = {
      config_enabled     = var.enable_config
      cloudtrail_enabled = var.enable_cloudtrail
      guardduty_enabled  = var.enable_guardduty
    }
  }
}

# Deployment Information
output "deployment_info" {
  description = "Information for deployment processes"
  value = {
    terraform_version = "~> 1.0"
    aws_region       = var.aws_region
    environment      = var.environment
    project_name     = var.project_name
    
    next_steps = [
      "1. Configure kubectl: aws eks update-kubeconfig --region ${var.aws_region} --name ${module.eks.cluster_id}",
      "2. Install AWS Load Balancer Controller",
      "3. Deploy application manifests from k8s/ directory",
      "4. Configure monitoring stack (Prometheus/Grafana)",
      "5. Set up CI/CD pipeline with GitHub Actions"
    ]
  }
}