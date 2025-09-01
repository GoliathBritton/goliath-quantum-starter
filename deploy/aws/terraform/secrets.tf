# AWS Secrets Manager for Partner System
# Secure credential management with automatic rotation

resource "aws_secretsmanager_secret" "partner_db_credentials" {
  name        = "goliath-partner-db-credentials"
  description = "Database credentials for Partner System"
  
  tags = {
    Environment = var.environment
    System      = "partner-system"
    ManagedBy   = "terraform"
  }
}

resource "aws_secretsmanager_secret_version" "partner_db_credentials" {
  secret_id = aws_secretsmanager_secret.partner_db_credentials.id
  
  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    host     = aws_db_instance.partner_db.endpoint
    port     = 5432
    database = var.db_name
    ssl_mode = "require"
  })
}

resource "aws_secretsmanager_secret" "stripe_credentials" {
  name        = "goliath-stripe-credentials"
  description = "Stripe API keys for payment processing"
  
  tags = {
    Environment = var.environment
    System      = "partner-system"
    ManagedBy   = "terraform"
  }
}

resource "aws_secretsmanager_secret_version" "stripe_credentials" {
  secret_id = aws_secretsmanager_secret.stripe_credentials.id
  
  secret_string = jsonencode({
    publishable_key = var.stripe_publishable_key
    secret_key      = var.stripe_secret_key
    webhook_secret  = var.stripe_webhook_secret
    connect_client_id = var.stripe_connect_client_id
  })
}

resource "aws_secretsmanager_secret" "jwt_secret" {
  name        = "goliath-jwt-secret"
  description = "JWT signing secret for authentication"
  
  tags = {
    Environment = var.environment
    System      = "partner-system"
    ManagedBy   = "terraform"
  }
}

resource "aws_secretsmanager_secret_version" "jwt_secret" {
  secret_id = aws_secretsmanager_secret.jwt_secret.id
  
  secret_string = random_password.jwt_secret.result
}

# Generate secure JWT secret
resource "random_password" "jwt_secret" {
  length  = 64
  special = true
}

# IAM policy for EKS to access secrets
resource "aws_iam_policy" "eks_secrets_access" {
  name        = "goliath-eks-secrets-access"
  description = "Allow EKS to access Secrets Manager"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = [
          aws_secretsmanager_secret.partner_db_credentials.arn,
          aws_secretsmanager_secret.stripe_credentials.arn,
          aws_secretsmanager_secret.jwt_secret.arn
        ]
      }
    ]
  })
}

# Attach policy to EKS node role
resource "aws_iam_role_policy_attachment" "eks_secrets_access" {
  policy_arn = aws_iam_policy.eks_secrets_access.arn
  role       = aws_iam_role.eks_node_group.0.name
}
