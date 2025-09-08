# NQBA Platform - Production Infrastructure
# AWS EKS-based deployment with high availability

terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.10"
    }
  }

  backend "s3" {
    bucket         = "nqba-terraform-state-prod"
    key            = "prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "nqba-terraform-locks"
  }
}

# Configure AWS Provider
provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = "production"
      Project     = "nqba-platform"
      ManagedBy   = "terraform"
      Owner       = "flyfox-ai"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# Local values
locals {
  cluster_name = "nqba-prod-${random_string.suffix.result}"
  
  common_tags = {
    Environment = "production"
    Project     = "nqba-platform"
    ManagedBy   = "terraform"
  }
}

# Random suffix for unique resource names
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# VPC Module
module "vpc" {
  source = "../../modules/vpc"
  
  name = "nqba-prod-vpc"
  cidr = var.vpc_cidr
  
  azs             = slice(data.aws_availability_zones.available.names, 0, 3)
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets
  
  enable_nat_gateway   = true
  enable_vpn_gateway   = false
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  # Enable flow logs
  enable_flow_log                      = true
  create_flow_log_cloudwatch_log_group = true
  create_flow_log_cloudwatch_iam_role  = true
  
  tags = local.common_tags
}

# EKS Cluster
module "eks" {
  source = "../../modules/eks"
  
  cluster_name    = local.cluster_name
  cluster_version = var.kubernetes_version
  
  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.private_subnets
  
  # Cluster endpoint configuration
  cluster_endpoint_private_access = true
  cluster_endpoint_public_access  = true
  cluster_endpoint_public_access_cidrs = var.cluster_endpoint_public_access_cidrs
  
  # Cluster logging
  cluster_enabled_log_types = ["api", "audit", "authenticator", "controllerManager", "scheduler"]
  
  # Node groups
  node_groups = {
    main = {
      desired_capacity = var.node_group_desired_capacity
      max_capacity     = var.node_group_max_capacity
      min_capacity     = var.node_group_min_capacity
      
      instance_types = var.node_group_instance_types
      capacity_type  = "ON_DEMAND"
      
      k8s_labels = {
        Environment = "production"
        NodeGroup   = "main"
      }
      
      additional_tags = {
        "kubernetes.io/cluster/${local.cluster_name}" = "owned"
      }
    }
    
    spot = {
      desired_capacity = var.spot_node_group_desired_capacity
      max_capacity     = var.spot_node_group_max_capacity
      min_capacity     = var.spot_node_group_min_capacity
      
      instance_types = var.spot_node_group_instance_types
      capacity_type  = "SPOT"
      
      k8s_labels = {
        Environment = "production"
        NodeGroup   = "spot"
        WorkloadType = "batch"
      }
      
      taints = {
        spot = {
          key    = "spot-instance"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      }
    }
  }
  
  tags = local.common_tags
}

# RDS Database
module "rds" {
  source = "../../modules/rds"
  
  identifier = "nqba-prod-db"
  
  engine         = "postgres"
  engine_version = var.postgres_version
  instance_class = var.db_instance_class
  
  allocated_storage     = var.db_allocated_storage
  max_allocated_storage = var.db_max_allocated_storage
  storage_encrypted     = true
  
  db_name  = var.db_name
  username = var.db_username
  
  vpc_security_group_ids = [module.security_groups.rds_security_group_id]
  db_subnet_group_name   = module.vpc.database_subnet_group
  
  backup_retention_period = var.db_backup_retention_period
  backup_window          = var.db_backup_window
  maintenance_window     = var.db_maintenance_window
  
  # Enable enhanced monitoring
  monitoring_interval = 60
  monitoring_role_arn = aws_iam_role.rds_enhanced_monitoring.arn
  
  # Enable performance insights
  performance_insights_enabled = true
  performance_insights_retention_period = 7
  
  # Multi-AZ deployment
  multi_az = true
  
  # Enable deletion protection
  deletion_protection = true
  
  tags = local.common_tags
}

# ElastiCache Redis
module "redis" {
  source = "../../modules/redis"
  
  cluster_id = "nqba-prod-redis"
  
  node_type               = var.redis_node_type
  num_cache_nodes         = var.redis_num_cache_nodes
  parameter_group_name    = "default.redis7"
  port                    = 6379
  
  subnet_group_name  = module.vpc.elasticache_subnet_group_name
  security_group_ids = [module.security_groups.redis_security_group_id]
  
  # Enable encryption
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  
  # Enable automatic backups
  snapshot_retention_limit = 7
  snapshot_window         = "03:00-05:00"
  
  tags = local.common_tags
}

# Security Groups
module "security_groups" {
  source = "../../modules/security-groups"
  
  name_prefix = "nqba-prod"
  vpc_id      = module.vpc.vpc_id
  
  # Allow access from EKS cluster
  eks_cluster_security_group_id = module.eks.cluster_security_group_id
  
  tags = local.common_tags
}

# Application Load Balancer
module "alb" {
  source = "../../modules/alb"
  
  name = "nqba-prod-alb"
  
  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets
  
  security_groups = [module.security_groups.alb_security_group_id]
  
  # Enable access logs
  access_logs = {
    bucket  = aws_s3_bucket.alb_logs.bucket
    enabled = true
  }
  
  tags = local.common_tags
}

# S3 Buckets
resource "aws_s3_bucket" "alb_logs" {
  bucket        = "nqba-prod-alb-logs-${random_string.suffix.result}"
  force_destroy = false
  
  tags = local.common_tags
}

resource "aws_s3_bucket" "app_storage" {
  bucket        = "nqba-prod-storage-${random_string.suffix.result}"
  force_destroy = false
  
  tags = local.common_tags
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/aws/eks/${local.cluster_name}/application"
  retention_in_days = var.log_retention_days
  
  tags = local.common_tags
}

# IAM Role for RDS Enhanced Monitoring
resource "aws_iam_role" "rds_enhanced_monitoring" {
  name = "nqba-prod-rds-enhanced-monitoring"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "monitoring.rds.amazonaws.com"
        }
      }
    ]
  })
  
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "rds_enhanced_monitoring" {
  role       = aws_iam_role.rds_enhanced_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}

# Route53 Hosted Zone (if managing DNS)
resource "aws_route53_zone" "main" {
  count = var.create_route53_zone ? 1 : 0
  
  name = var.domain_name
  
  tags = local.common_tags
}

# ACM Certificate
resource "aws_acm_certificate" "main" {
  count = var.create_acm_certificate ? 1 : 0
  
  domain_name               = var.domain_name
  subject_alternative_names = ["*.${var.domain_name}"]
  validation_method         = "DNS"
  
  lifecycle {
    create_before_destroy = true
  }
  
  tags = local.common_tags
}