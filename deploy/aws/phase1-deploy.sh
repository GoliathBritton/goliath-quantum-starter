#!/bin/bash

# 🚀 Phase 1: Immediate Production Deployment
# Goliath Partner System - Get Live in 4 Hours!

set -e  # Exit on any error

echo "🚀 Starting Phase 1 Deployment - Goliath Partner System"
echo "========================================================"
echo "⏰ Estimated Time: 4 hours"
echo "🎯 Goal: Production-ready Partner System"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking deployment prerequisites..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI not found. Please install AWS CLI first."
        exit 1
    fi
    
    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl not found. Please install kubectl first."
        exit 1
    fi
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform not found. Please install Terraform first."
        exit 1
    fi
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker not found. Please install Docker first."
        exit 1
    fi
    
    print_success "All prerequisites are installed!"
}

# Configure AWS credentials
configure_aws() {
    print_status "Configuring AWS credentials..."
    
    # Check if AWS credentials are configured
    if ! aws sts get-caller-identity &> /dev/null; then
        print_warning "AWS credentials not configured. Please run 'aws configure' first."
        read -p "Press Enter after configuring AWS credentials..."
    fi
    
    # Get AWS account ID
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    print_success "AWS Account ID: $AWS_ACCOUNT_ID"
    
    # Set AWS region
    export AWS_REGION=${AWS_REGION:-us-east-1}
    print_success "AWS Region: $AWS_REGION"
}

# Deploy infrastructure with Terraform
deploy_infrastructure() {
    print_status "Deploying AWS infrastructure with Terraform..."
    
    cd deploy/aws/terraform/phase1
    
    # Initialize Terraform
    print_status "Initializing Terraform..."
    terraform init
    
    # Plan deployment
    print_status "Planning Terraform deployment..."
    terraform plan -out=tfplan
    
    # Apply deployment
    print_status "Applying Terraform deployment..."
    terraform apply tfplan
    
    # Get outputs
    print_status "Getting infrastructure outputs..."
    CLUSTER_ENDPOINT=$(terraform output -raw cluster_endpoint)
    DB_ENDPOINT=$(terraform output -raw db_endpoint)
    REDIS_ENDPOINT=$(terraform output -raw redis_endpoint)
    ALB_DNS=$(terraform output -raw alb_dns_name)
    
    print_success "Infrastructure deployed successfully!"
    print_status "EKS Cluster: $CLUSTER_ENDPOINT"
    print_status "RDS Database: $DB_ENDPOINT"
    print_status "Redis Cache: $REDIS_ENDPOINT"
    print_status "Load Balancer: $ALB_DNS"
    
    cd ../../../..
}

# Build and push Docker images
build_images() {
    print_status "Building and pushing Docker images..."
    
    # Get ECR login token
    aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
    
    # Build API image
    print_status "Building Partner API image..."
    docker build -t partner-api:latest ./api
    
    # Build Portal image
    print_status "Building Partner Portal image..."
    docker build -t partner-portal:latest ./ui
    
    # Tag and push images
    docker tag partner-api:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/goliath-partner-api:latest
    docker tag partner-portal:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/goliath-partner-portal:latest
    
    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/goliath-partner-api:latest
    docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/goliath-partner-portal:latest
    
    print_success "Docker images built and pushed successfully!"
}

# Deploy to Kubernetes
deploy_kubernetes() {
    print_status "Deploying to Kubernetes..."
    
    # Update kubeconfig
    aws eks update-kubeconfig --name goliath-partner-cluster --region $AWS_REGION
    
    # Create namespace
    kubectl create namespace partner-system --dry-run=client -o yaml | kubectl apply -f -
    
    # Apply Kubernetes manifests
    print_status "Applying Kubernetes manifests..."
    kubectl apply -f deploy/aws/kubernetes/phase1/
    
    # Wait for deployments
    print_status "Waiting for deployments to be ready..."
    kubectl rollout status deployment/partner-api -n partner-system
    kubectl rollout status deployment/partner-portal -n partner-system
    
    print_success "Kubernetes deployment completed!"
}

# Configure monitoring
setup_monitoring() {
    print_status "Setting up monitoring stack..."
    
    # Deploy Prometheus
    kubectl apply -f deploy/aws/kubernetes/monitoring/prometheus/
    
    # Deploy Grafana
    kubectl apply -f deploy/aws/kubernetes/monitoring/grafana/
    
    print_success "Monitoring stack deployed!"
}

# Test deployment
test_deployment() {
    print_status "Testing deployment..."
    
    # Wait for services to be ready
    sleep 30
    
    # Test API health
    if curl -f "http://$ALB_DNS:8080/health"; then
        print_success "API health check passed!"
    else
        print_error "API health check failed!"
        exit 1
    fi
    
    # Test Portal
    if curl -f "http://$ALB_DNS:3000/"; then
        print_success "Portal health check passed!"
    else
        print_error "Portal health check failed!"
        exit 1
    fi
    
    print_success "All health checks passed!"
}

# Display final status
show_final_status() {
    echo ""
    echo "🎉 PHASE 1 DEPLOYMENT COMPLETED SUCCESSFULLY! 🎉"
    echo "=================================================="
    echo ""
    echo "🌐 Your Partner System is now LIVE at:"
    echo "   Portal: http://$ALB_DNS:3000"
    echo "   API: http://$ALB_DNS:8080"
    echo ""
    echo "📊 Monitoring:"
    echo "   Grafana: http://$ALB_DNS:3000/grafana"
    echo "   Prometheus: http://$ALB_DNS:3000/prometheus"
    echo ""
    echo "🔑 Next Steps:"
    echo "   1. Configure DNS to point to: $ALB_DNS"
    echo "   2. Set up SSL certificates"
    echo "   3. Configure monitoring alerts"
    echo "   4. Test partner onboarding flow"
    echo ""
    echo "📚 Documentation:"
    echo "   - Partner Playbook: docs/PartnerPlaybook.md"
    echo "   - API Documentation: http://$ALB_DNS:8080/docs"
    echo ""
    echo "🚀 Ready for Phase 2: Enhanced Security & Monitoring"
}

# Main deployment flow
main() {
    echo "🚀 Starting Phase 1 Deployment..."
    echo ""
    
    check_prerequisites
    configure_aws
    deploy_infrastructure
    build_images
    deploy_kubernetes
    setup_monitoring
    test_deployment
    show_final_status
    
    print_success "Phase 1 deployment completed successfully!"
}

# Run main function
main "$@"
