#!/bin/bash

# NQBA Ecosystem Deployment Script
# Automated deployment for production environment

set -e  # Exit on any error

# Configuration
ENVIRONMENT=${1:-"production"}
AWS_REGION=${2:-"us-east-1"}
CLUSTER_NAME="nqba-cluster-${ENVIRONMENT}"
NAMESPACE="nqba-ecosystem"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if required tools are installed
    command -v terraform >/dev/null 2>&1 || { log_error "Terraform is required but not installed. Aborting."; exit 1; }
    command -v kubectl >/dev/null 2>&1 || { log_error "kubectl is required but not installed. Aborting."; exit 1; }
    command -v aws >/dev/null 2>&1 || { log_error "AWS CLI is required but not installed. Aborting."; exit 1; }
    command -v docker >/dev/null 2>&1 || { log_error "Docker is required but not installed. Aborting."; exit 1; }
    
    # Check AWS credentials
    if ! aws sts get-caller-identity >/dev/null 2>&1; then
        log_error "AWS credentials not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    log_success "Prerequisites check passed"
}

# Build and push Docker image
build_and_push_image() {
    log_info "Building and pushing Docker image..."
    
    # Build image
    docker build -t nqba-ecosystem:latest -f deploy/docker/Dockerfile .
    
    # Tag for ECR (if using ECR)
    # aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com
    # docker tag nqba-ecosystem:latest ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/nqba-ecosystem:latest
    # docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/nqba-ecosystem:latest
    
    log_success "Docker image built successfully"
}

# Deploy infrastructure with Terraform
deploy_infrastructure() {
    log_info "Deploying infrastructure with Terraform..."
    
    cd deploy/terraform
    
    # Initialize Terraform
    terraform init
    
    # Plan deployment
    terraform plan -var="environment=${ENVIRONMENT}" -var="aws_region=${AWS_REGION}" -out=tfplan
    
    # Apply deployment
    terraform apply tfplan
    
    # Get outputs
    CLUSTER_ENDPOINT=$(terraform output -raw cluster_endpoint)
    VPC_ID=$(terraform output -raw vpc_id)
    RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
    REDIS_ENDPOINT=$(terraform output -raw redis_endpoint)
    ALB_DNS_NAME=$(terraform output -raw alb_dns_name)
    
    cd ../..
    
    log_success "Infrastructure deployed successfully"
    log_info "Cluster endpoint: ${CLUSTER_ENDPOINT}"
    log_info "ALB DNS name: ${ALB_DNS_NAME}"
}

# Configure kubectl for EKS cluster
configure_kubectl() {
    log_info "Configuring kubectl for EKS cluster..."
    
    aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}
    
    # Verify connection
    if ! kubectl cluster-info >/dev/null 2>&1; then
        log_error "Failed to connect to EKS cluster"
        exit 1
    fi
    
    log_success "kubectl configured successfully"
}

# Deploy application to Kubernetes
deploy_application() {
    log_info "Deploying application to Kubernetes..."
    
    # Create namespace if it doesn't exist
    kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
    
    # Apply Kubernetes manifests
    kubectl apply -f deploy/kubernetes/nqba-deployment.yaml
    
    # Wait for deployments to be ready
    log_info "Waiting for deployments to be ready..."
    kubectl wait --for=condition=available --timeout=300s deployment/nqba-api -n ${NAMESPACE}
    kubectl wait --for=condition=available --timeout=300s deployment/nqba-business-units -n ${NAMESPACE}
    kubectl wait --for=condition=available --timeout=300s deployment/nqba-qih -n ${NAMESPACE}
    
    log_success "Application deployed successfully"
}

# Run health checks
run_health_checks() {
    log_info "Running health checks..."
    
    # Check pod status
    kubectl get pods -n ${NAMESPACE}
    
    # Check services
    kubectl get services -n ${NAMESPACE}
    
    # Check if pods are running
    RUNNING_PODS=$(kubectl get pods -n ${NAMESPACE} --field-selector=status.phase=Running --no-headers | wc -l)
    TOTAL_PODS=$(kubectl get pods -n ${NAMESPACE} --no-headers | wc -l)
    
    if [ ${RUNNING_PODS} -eq ${TOTAL_PODS} ]; then
        log_success "All pods are running"
    else
        log_warning "Some pods are not running. Check with 'kubectl get pods -n ${NAMESPACE}'"
    fi
    
    # Check application health endpoints
    log_info "Checking application health endpoints..."
    
    # Get service IPs
    API_SERVICE_IP=$(kubectl get service nqba-api-service -n ${NAMESPACE} -o jsonpath='{.spec.clusterIP}')
    
    # Test health endpoint (if accessible)
    if [ -n "${API_SERVICE_IP}" ]; then
        log_info "API service IP: ${API_SERVICE_IP}"
        # Note: Health check would require port-forwarding or external access
    fi
}

# Setup monitoring
setup_monitoring() {
    log_info "Setting up monitoring..."
    
    # Deploy Prometheus
    kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/kube-prometheus/main/manifests/setup/namespace.yaml
    kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/kube-prometheus/main/manifests/setup/
    kubectl apply -f https://raw.githubusercontent.com/prometheus-operator/kube-prometheus/main/manifests/
    
    # Deploy Grafana
    kubectl apply -f https://raw.githubusercontent.com/grafana/helm-charts/main/charts/grafana/templates/namespace.yaml
    
    log_success "Monitoring setup completed"
}

# Run integration tests
run_integration_tests() {
    log_info "Running integration tests..."
    
    # Run the integration test suite
    if python integration_test_suite.py; then
        log_success "Integration tests passed"
    else
        log_error "Integration tests failed"
        exit 1
    fi
}

# Generate deployment report
generate_deployment_report() {
    log_info "Generating deployment report..."
    
    REPORT_FILE="deployment_report_$(date +%Y%m%d_%H%M%S).md"
    
    cat > ${REPORT_FILE} << EOF
# NQBA Ecosystem Deployment Report

**Deployment Date:** $(date)
**Environment:** ${ENVIRONMENT}
**AWS Region:** ${AWS_REGION}
**Cluster Name:** ${CLUSTER_NAME}

## Infrastructure Status
- **VPC ID:** ${VPC_ID}
- **EKS Cluster:** ${CLUSTER_ENDPOINT}
- **RDS Endpoint:** ${RDS_ENDPOINT}
- **Redis Endpoint:** ${REDIS_ENDPOINT}
- **ALB DNS:** ${ALB_DNS_NAME}

## Application Status
- **Namespace:** ${NAMESPACE}
- **API Pods:** $(kubectl get pods -n ${NAMESPACE} -l app=nqba-api --no-headers | wc -l)
- **Business Units Pods:** $(kubectl get pods -n ${NAMESPACE} -l app=nqba-business-units --no-headers | wc -l)
- **QIH Pods:** $(kubectl get pods -n ${NAMESPACE} -l app=nqba-qih --no-headers | wc -l)

## Health Check Results
$(kubectl get pods -n ${NAMESPACE} -o wide)

## Next Steps
1. Configure DNS to point to ALB: ${ALB_DNS_NAME}
2. Set up SSL certificates
3. Configure monitoring dashboards
4. Run performance benchmarks
5. Set up CI/CD pipeline

## Access Information
- **Grafana:** http://localhost:3000 (port-forward required)
- **Prometheus:** http://localhost:9090 (port-forward required)
- **API Documentation:** http://${ALB_DNS_NAME}/docs

EOF
    
    log_success "Deployment report generated: ${REPORT_FILE}"
}

# Main deployment function
main() {
    log_info "Starting NQBA Ecosystem deployment..."
    log_info "Environment: ${ENVIRONMENT}"
    log_info "AWS Region: ${AWS_REGION}"
    
    # Check prerequisites
    check_prerequisites
    
    # Build and push Docker image
    build_and_push_image
    
    # Deploy infrastructure
    deploy_infrastructure
    
    # Configure kubectl
    configure_kubectl
    
    # Deploy application
    deploy_application
    
    # Setup monitoring
    setup_monitoring
    
    # Run health checks
    run_health_checks
    
    # Run integration tests
    run_integration_tests
    
    # Generate deployment report
    generate_deployment_report
    
    log_success "NQBA Ecosystem deployment completed successfully!"
    log_info "Your application is now running at: http://${ALB_DNS_NAME}"
}

# Help function
show_help() {
    echo "Usage: $0 [ENVIRONMENT] [AWS_REGION]"
    echo ""
    echo "Arguments:"
    echo "  ENVIRONMENT   Deployment environment (default: production)"
    echo "  AWS_REGION    AWS region (default: us-east-1)"
    echo ""
    echo "Examples:"
    echo "  $0                    # Deploy to production in us-east-1"
    echo "  $0 staging           # Deploy to staging in us-east-1"
    echo "  $0 production eu-west-1  # Deploy to production in eu-west-1"
}

# Parse command line arguments
case "${1}" in
    -h|--help)
        show_help
        exit 0
        ;;
    *)
        main
        ;;
esac
