# NQBA Platform - Production Environment Outputs

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

output "nat_gateway_ips" {
  description = "List of public Elastic IPs created for AWS NAT Gateway"
  value       = module.vpc.nat_public_ips
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

output "cluster_primary_security_group_id" {
  description = "The cluster primary security group ID created by the EKS cluster"
  value       = module.eks.cluster_primary_security_group_id
}

output "cluster_version" {
  description = "The Kubernetes version for the EKS cluster"
  value       = module.eks.cluster_version
}

# EKS Node Group Outputs
output "node_groups" {
  description = "EKS node groups"
  value       = module.eks.node_groups
  sensitive   = true
}

output "eks_managed_node_groups" {
  description = "Map of attribute maps for all EKS managed node groups created"
  value       = module.eks.eks_managed_node_groups
  sensitive   = true
}

# RDS Outputs
output "db_instance_endpoint" {
  description = "RDS instance endpoint"
  value       = module.rds.db_instance_endpoint
  sensitive   = true
}

output "db_instance_hosted_zone_id" {
  description = "The hosted zone ID of the DB instance"
  value       = module.rds.db_instance_hosted_zone_id
}

output "db_instance_id" {
  description = "RDS instance ID"
  value       = module.rds.db_instance_id
}

output "db_instance_resource_id" {
  description = "RDS instance resource ID"
  value       = module.rds.db_instance_resource_id
}

output "db_instance_status" {
  description = "RDS instance status"
  value       = module.rds.db_instance_status
}

output "db_instance_name" {
  description = "RDS instance name"
  value       = module.rds.db_instance_name
}

output "db_instance_username" {
  description = "RDS instance root username"
  value       = module.rds.db_instance_username
  sensitive   = true
}

output "db_instance_port" {
  description = "RDS instance port"
  value       = module.rds.db_instance_port
}

output "db_subnet_group_id" {
  description = "ID of the DB subnet group"
  value       = module.rds.db_subnet_group_id
}

output "db_subnet_group_arn" {
  description = "ARN of the DB subnet group"
  value       = module.rds.db_subnet_group_arn
}

output "db_parameter_group_id" {
  description = "ID of the DB parameter group"
  value       = module.rds.db_parameter_group_id
}

output "db_parameter_group_arn" {
  description = "ARN of the DB parameter group"
  value       = module.rds.db_parameter_group_arn
}

# Redis Outputs
output "redis_cluster_address" {
  description = "Redis cluster endpoint address"
  value       = module.redis.cluster_address
  sensitive   = true
}

output "redis_cluster_id" {
  description = "Redis cluster ID"
  value       = module.redis.cluster_id
}

output "redis_port" {
  description = "Redis port"
  value       = module.redis.port
}

output "redis_parameter_group_id" {
  description = "ID of the Redis parameter group"
  value       = module.redis.parameter_group_id
}

output "redis_subnet_group_name" {
  description = "Name of the Redis subnet group"
  value       = module.redis.subnet_group_name
}

# Security Group Outputs
output "eks_cluster_security_group_id" {
  description = "ID of the EKS cluster security group"
  value       = module.security_groups.eks_cluster_security_group_id
}

output "eks_node_security_group_id" {
  description = "ID of the EKS node security group"
  value       = module.security_groups.eks_node_security_group_id
}

output "rds_security_group_id" {
  description = "ID of the RDS security group"
  value       = module.security_groups.rds_security_group_id
}

output "redis_security_group_id" {
  description = "ID of the Redis security group"
  value       = module.security_groups.redis_security_group_id
}

output "alb_security_group_id" {
  description = "ID of the ALB security group"
  value       = module.security_groups.alb_security_group_id
}

# ALB Outputs
output "alb_id" {
  description = "ID of the Application Load Balancer"
  value       = module.alb.lb_id
}

output "alb_arn" {
  description = "ARN of the Application Load Balancer"
  value       = module.alb.lb_arn
}

output "alb_dns_name" {
  description = "DNS name of the Application Load Balancer"
  value       = module.alb.lb_dns_name
}

output "alb_hosted_zone_id" {
  description = "Hosted zone ID of the Application Load Balancer"
  value       = module.alb.lb_zone_id
}

output "alb_target_group_arns" {
  description = "ARNs of the target groups"
  value       = module.alb.target_group_arns
}

# S3 Bucket Outputs
output "alb_logs_bucket_id" {
  description = "ID of the ALB logs S3 bucket"
  value       = aws_s3_bucket.alb_logs.id
}

output "alb_logs_bucket_arn" {
  description = "ARN of the ALB logs S3 bucket"
  value       = aws_s3_bucket.alb_logs.arn
}

output "app_storage_bucket_id" {
  description = "ID of the application storage S3 bucket"
  value       = aws_s3_bucket.app_storage.id
}

output "app_storage_bucket_arn" {
  description = "ARN of the application storage S3 bucket"
  value       = aws_s3_bucket.app_storage.arn
}

# CloudWatch Outputs
output "app_logs_cloudwatch_log_group_name" {
  description = "Name of the CloudWatch log group for application logs"
  value       = aws_cloudwatch_log_group.app_logs.name
}

output "app_logs_cloudwatch_log_group_arn" {
  description = "ARN of the CloudWatch log group for application logs"
  value       = aws_cloudwatch_log_group.app_logs.arn
}

# Route53 Outputs (conditional)
output "route53_zone_id" {
  description = "Route53 hosted zone ID"
  value       = var.create_route53_zone ? aws_route53_zone.main[0].zone_id : null
}

output "route53_zone_name_servers" {
  description = "Route53 hosted zone name servers"
  value       = var.create_route53_zone ? aws_route53_zone.main[0].name_servers : null
}

# ACM Certificate Outputs (conditional)
output "acm_certificate_arn" {
  description = "ARN of the ACM certificate"
  value       = var.create_acm_certificate ? aws_acm_certificate.main[0].arn : null
}

output "acm_certificate_domain_validation_options" {
  description = "Domain validation options for ACM certificate"
  value       = var.create_acm_certificate ? aws_acm_certificate.main[0].domain_validation_options : null
  sensitive   = true
}

# IAM Outputs
output "rds_enhanced_monitoring_role_arn" {
  description = "ARN of the RDS enhanced monitoring IAM role"
  value       = aws_iam_role.rds_enhanced_monitoring.arn
}

# Utility Outputs
output "aws_caller_identity_account_id" {
  description = "AWS account ID"
  value       = data.aws_caller_identity.current.account_id
}

output "aws_caller_identity_arn" {
  description = "AWS caller identity ARN"
  value       = data.aws_caller_identity.current.arn
}

output "aws_caller_identity_user_id" {
  description = "AWS caller identity user ID"
  value       = data.aws_caller_identity.current.user_id
}

output "aws_region" {
  description = "AWS region"
  value       = var.aws_region
}

output "availability_zones" {
  description = "List of availability zones"
  value       = data.aws_availability_zones.available.names
}

# Kubernetes Configuration
output "kubectl_config" {
  description = "kubectl config as generated by the module"
  value = {
    cluster_name                     = module.eks.cluster_id
    endpoint                        = module.eks.cluster_endpoint
    ca_data                         = module.eks.cluster_certificate_authority_data
    aws_region                      = var.aws_region
    aws_profile                     = var.aws_profile
  }
  sensitive = true
}

# Connection Information
output "connection_info" {
  description = "Connection information for external services"
  value = {
    database = {
      host     = module.rds.db_instance_endpoint
      port     = module.rds.db_instance_port
      database = module.rds.db_instance_name
      username = module.rds.db_instance_username
    }
    redis = {
      host = module.redis.cluster_address
      port = module.redis.port
    }
    kubernetes = {
      cluster_name = module.eks.cluster_id
      endpoint     = module.eks.cluster_endpoint
      region       = var.aws_region
    }
    load_balancer = {
      dns_name = module.alb.lb_dns_name
      zone_id  = module.alb.lb_zone_id
    }
  }
  sensitive = true
}