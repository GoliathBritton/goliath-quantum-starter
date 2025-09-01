# Phase 1: Immediate Production Deployment
# Goliath Partner System - Core Infrastructure

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Environment = var.environment
      System      = "goliath-partner-system"
      Phase       = "phase1"
      ManagedBy   = "terraform"
    }
  }
}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "goliath-partner-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["${var.aws_region}a", "${var.aws_region}b", "${var.aws_region}c"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24", "10.0.103.0/24"]
  
  enable_nat_gateway = true
  single_nat_gateway = true
  one_nat_gateway_per_az = false
  
  enable_dns_hostnames = true
  enable_dns_support   = true
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# EKS Cluster
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"
  
  cluster_name    = "goliath-partner-cluster"
  cluster_version = "1.28"
  
  cluster_endpoint_public_access = true
  
  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets
  
  eks_managed_node_groups = {
    general = {
      desired_size = 2
      min_size     = 1
      max_size     = 4
      
      instance_types = ["t3.medium"]
      capacity_type  = "ON_DEMAND"
      
      labels = {
        Environment = var.environment
        System      = "goliath-partner-system"
      }
      
      tags = {
        ExtraTag = "goliath-partner-node"
      }
    }
  }
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# RDS Database
resource "aws_db_instance" "partner_db" {
  identifier = "goliath-partner-db"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = "db.t3.micro"
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type         = "gp2"
  storage_encrypted    = true
  
  db_name  = "partner_db"
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds.id]
  db_subnet_group_name   = aws_db_subnet_group.partner_db.name
  
  backup_retention_period = 7
  backup_window          = "02:00-03:00"
  maintenance_window     = "sun:03:00-sun:04:00"
  
  multi_az               = false
  publicly_accessible    = false
  skip_final_snapshot    = false
  final_snapshot_identifier = "goliath-partner-db-final-snapshot"
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# RDS Subnet Group
resource "aws_db_subnet_group" "partner_db" {
  name       = "goliath-partner-db-subnet-group"
  subnet_ids = module.vpc.private_subnets
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# RDS Security Group
resource "aws_security_group" "rds" {
  name_prefix = "goliath-partner-db-sg"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [module.eks.cluster_security_group_id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# Redis ElastiCache
resource "aws_elasticache_subnet_group" "partner_redis" {
  name       = "goliath-partner-redis-subnet-group"
  subnet_ids = module.vpc.private_subnets
}

resource "aws_elasticache_cluster" "partner_redis" {
  cluster_id           = "goliath-partner-redis"
  engine               = "redis"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  security_group_ids   = [aws_security_group.redis.id]
  subnet_group_name    = aws_elasticache_subnet_group.partner_redis.name
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# Redis Security Group
resource "aws_security_group" "redis" {
  name_prefix = "goliath-partner-redis-sg"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [module.eks.cluster_security_group_id]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# S3 Bucket for backups
resource "aws_s3_bucket" "partner_backups" {
  bucket = "goliath-partner-backups-${random_string.bucket_suffix.result}"
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

resource "aws_s3_bucket_versioning" "partner_backups" {
  bucket = aws_s3_bucket.partner_backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "partner_backups" {
  bucket = aws_s3_bucket.partner_backups.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Application Load Balancer
resource "aws_lb" "partner_alb" {
  name               = "goliath-partner-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = module.vpc.public_subnets
  
  enable_deletion_protection = false
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# ALB Security Group
resource "aws_security_group" "alb" {
  name_prefix = "goliath-partner-alb-sg"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# ALB Target Groups
resource "aws_lb_target_group" "partner_api" {
  name     = "goliath-partner-api-tg"
  port     = 8080
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/health"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

resource "aws_lb_target_group" "partner_portal" {
  name     = "goliath-partner-portal-tg"
  port     = 3000
  protocol = "HTTP"
  vpc_id   = module.vpc.vpc_id
  
  health_check {
    enabled             = true
    healthy_threshold   = 2
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
    timeout             = 5
    unhealthy_threshold = 2
  }
  
  tags = {
    Environment = var.environment
    System      = "goliath-partner-system"
  }
}

# ALB Listeners
resource "aws_lb_listener" "partner_api" {
  load_balancer_arn = aws_lb.partner_alb.arn
  port              = "80"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.partner_api.arn
  }
}

resource "aws_lb_listener" "partner_portal" {
  load_balancer_arn = aws_lb.partner_alb.arn
  port              = "3000"
  protocol          = "HTTP"
  
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.partner_portal.arn
  }
}

# Outputs
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

output "cluster_certificate_authority_data" {
  description = "Base64 encoded certificate data required to communicate with the cluster"
  value       = module.eks.cluster_certificate_authority_data
}

output "db_endpoint" {
  description = "RDS database endpoint"
  value       = aws_db_instance.partner_db.endpoint
}

output "redis_endpoint" {
  description = "Redis ElastiCache endpoint"
  value       = aws_elasticache_cluster.partner_redis.cache_nodes.0.address
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name"
  value       = aws_lb.partner_alb.dns_name
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "private_subnets" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "public_subnets" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnets
}
