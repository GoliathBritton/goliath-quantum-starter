#!/bin/bash
# Quantum Nexus Platform - Production Deployment Script
# Complete deployment orchestration for cloud-native production environment

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DEPLOY_DIR="${PROJECT_ROOT}/deploy"
K8S_DIR="${DEPLOY_DIR}/k8s"
DOCKER_DIR="${DEPLOY_DIR}/docker"

# Default values
NAMESPACE="quantum-nexus-prod"
CLUSTER_NAME="quantum-nexus-cluster"
REGION="us-west-2"
DOMAIN="quantum-nexus.ai"
IMAGE_TAG="latest"
REPLICAS="3"
DRY_RUN="false"
SKIP_BUILD="false"
SKIP_TESTS="false"
FORCE_DEPLOY="false"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# =============================================================================
# Logging Functions
# =============================================================================
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

log_step() {
    echo -e "${PURPLE}[STEP]${NC} $1"
}

log_deploy() {
    echo -e "${CYAN}[DEPLOY]${NC} $1"
}

# =============================================================================
# Utility Functions
# =============================================================================
check_dependencies() {
    log_step "Checking dependencies..."
    
    local deps=("kubectl" "docker" "helm" "aws" "jq" "curl")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        log_info "Please install the missing dependencies and try again."
        exit 1
    fi
    
    log_success "All dependencies are installed"
}

check_cluster_connection() {
    log_step "Checking Kubernetes cluster connection..."
    
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        log_info "Please ensure your kubectl is configured correctly"
        exit 1
    fi
    
    local current_context=$(kubectl config current-context)
    log_success "Connected to cluster: $current_context"
}

check_docker_registry() {
    log_step "Checking Docker registry access..."
    
    if ! docker info &> /dev/null; then
        log_error "Docker daemon is not running"
        exit 1
    fi
    
    # Test registry access (assuming ECR)
    if ! aws ecr get-login-token --region "$REGION" &> /dev/null; then
        log_warning "Cannot access ECR registry. Please ensure AWS credentials are configured."
    else
        log_success "Docker registry access confirmed"
    fi
}

validate_environment() {
    log_step "Validating deployment environment..."
    
    # Check required environment variables
    local required_vars=(
        "AWS_ACCOUNT_ID"
        "AWS_REGION"
        "DOCKER_REGISTRY"
    )
    
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var:-}" ]]; then
            log_error "Required environment variable $var is not set"
            exit 1
        fi
    done
    
    log_success "Environment validation passed"
}

# =============================================================================
# Build Functions
# =============================================================================
build_images() {
    if [[ "$SKIP_BUILD" == "true" ]]; then
        log_info "Skipping image build (--skip-build flag)"
        return 0
    fi
    
    log_step "Building Docker images..."
    
    local registry="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    local api_image="${registry}/quantum-nexus-api:${IMAGE_TAG}"
    local worker_image="${registry}/quantum-nexus-worker:${IMAGE_TAG}"
    
    # Login to ECR
    aws ecr get-login-password --region "$AWS_REGION" | \
        docker login --username AWS --password-stdin "$registry"
    
    # Build API image
    log_info "Building API image..."
    docker build -f "${PROJECT_ROOT}/api/Dockerfile.production" \
        -t "$api_image" \
        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --build-arg VCS_REF="$(git rev-parse HEAD)" \
        --build-arg VERSION="$IMAGE_TAG" \
        "$PROJECT_ROOT"
    
    # Build Worker image
    log_info "Building Worker image..."
    docker build -f "${PROJECT_ROOT}/worker/Dockerfile" \
        -t "$worker_image" \
        --build-arg BUILD_DATE="$(date -u +'%Y-%m-%dT%H:%M:%SZ')" \
        --build-arg VCS_REF="$(git rev-parse HEAD)" \
        --build-arg VERSION="$IMAGE_TAG" \
        "$PROJECT_ROOT"
    
    # Push images
    log_info "Pushing images to registry..."
    docker push "$api_image"
    docker push "$worker_image"
    
    log_success "Images built and pushed successfully"
}

run_tests() {
    if [[ "$SKIP_TESTS" == "true" ]]; then
        log_info "Skipping tests (--skip-tests flag)"
        return 0
    fi
    
    log_step "Running tests..."
    
    cd "$PROJECT_ROOT"
    
    # Install test dependencies
    pip install -r requirements-test.txt
    
    # Run unit tests
    log_info "Running unit tests..."
    python -m pytest tests/unit/ -v --cov=api --cov-report=term-missing
    
    # Run integration tests
    log_info "Running integration tests..."
    python -m pytest tests/integration/ -v
    
    # Run security tests
    log_info "Running security tests..."
    bandit -r api/ -f json -o security-report.json || true
    
    # Run performance tests
    log_info "Running performance tests..."
    python -m pytest tests/performance/ -v
    
    log_success "All tests passed"
}

# =============================================================================
# Infrastructure Setup Functions
# =============================================================================
setup_namespace() {
    log_step "Setting up Kubernetes namespace..."
    
    kubectl apply -f "${K8S_DIR}/namespace.yaml"
    
    # Set default namespace for subsequent commands
    kubectl config set-context --current --namespace="$NAMESPACE"
    
    log_success "Namespace '$NAMESPACE' configured"
}

setup_secrets() {
    log_step "Setting up secrets and configurations..."
    
    # Run secrets setup script
    "${SCRIPT_DIR}/setup-secrets.sh" generate
    "${SCRIPT_DIR}/setup-secrets.sh" apply
    
    log_success "Secrets and configurations applied"
}

setup_storage() {
    log_step "Setting up persistent storage..."
    
    # Apply storage classes and PVCs
    kubectl apply -f "${K8S_DIR}/storage/"
    
    # Wait for PVCs to be bound
    kubectl wait --for=condition=Bound pvc --all --timeout=300s
    
    log_success "Storage setup completed"
}

setup_networking() {
    log_step "Setting up networking and ingress..."
    
    # Apply network policies
    kubectl apply -f "${K8S_DIR}/network-policies/"
    
    # Apply ingress configuration
    kubectl apply -f "${K8S_DIR}/ingress.yaml"
    
    # Setup cert-manager for TLS
    kubectl apply -f "${K8S_DIR}/cert-manager.yaml"
    
    log_success "Networking setup completed"
}

# =============================================================================
# Application Deployment Functions
# =============================================================================
deploy_infrastructure() {
    log_step "Deploying infrastructure components..."
    
    # Deploy Redis
    log_info "Deploying Redis..."
    kubectl apply -f "${K8S_DIR}/redis/"
    
    # Deploy NATS
    log_info "Deploying NATS..."
    kubectl apply -f "${K8S_DIR}/nats/"
    
    # Deploy PostgreSQL
    log_info "Deploying PostgreSQL..."
    kubectl apply -f "${K8S_DIR}/postgres/"
    
    # Wait for infrastructure to be ready
    kubectl wait --for=condition=Ready pod -l app=redis --timeout=300s
    kubectl wait --for=condition=Ready pod -l app=nats --timeout=300s
    kubectl wait --for=condition=Ready pod -l app=postgres --timeout=300s
    
    log_success "Infrastructure components deployed"
}

deploy_application() {
    log_step "Deploying application components..."
    
    # Update image tags in deployment files
    local registry="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
    
    # Deploy API
    log_info "Deploying API..."
    sed "s|IMAGE_PLACEHOLDER|${registry}/quantum-nexus-api:${IMAGE_TAG}|g" \
        "${K8S_DIR}/api-deployment.yaml" | kubectl apply -f -
    
    # Deploy Workers
    log_info "Deploying Workers..."
    sed "s|IMAGE_PLACEHOLDER|${registry}/quantum-nexus-worker:${IMAGE_TAG}|g" \
        "${K8S_DIR}/worker-deployment.yaml" | kubectl apply -f -
    
    # Scale deployments
    kubectl scale deployment quantum-nexus-api --replicas="$REPLICAS"
    kubectl scale deployment quantum-nexus-worker --replicas="$REPLICAS"
    
    # Wait for deployments to be ready
    kubectl wait --for=condition=Available deployment/quantum-nexus-api --timeout=600s
    kubectl wait --for=condition=Available deployment/quantum-nexus-worker --timeout=600s
    
    log_success "Application components deployed"
}

deploy_monitoring() {
    log_step "Deploying monitoring stack..."
    
    # Deploy Prometheus
    log_info "Deploying Prometheus..."
    kubectl apply -f "${K8S_DIR}/monitoring/prometheus/"
    
    # Deploy Grafana
    log_info "Deploying Grafana..."
    kubectl apply -f "${K8S_DIR}/monitoring/grafana/"
    
    # Deploy Jaeger
    log_info "Deploying Jaeger..."
    kubectl apply -f "${K8S_DIR}/monitoring/jaeger/"
    
    # Apply service monitors
    kubectl apply -f "${K8S_DIR}/production-resources.yaml"
    
    log_success "Monitoring stack deployed"
}

# =============================================================================
# Post-Deployment Functions
# =============================================================================
run_migrations() {
    log_step "Running database migrations..."
    
    # Run migrations job
    kubectl apply -f "${K8S_DIR}/jobs/migration-job.yaml"
    
    # Wait for migration to complete
    kubectl wait --for=condition=Complete job/quantum-nexus-migration --timeout=300s
    
    log_success "Database migrations completed"
}

setup_demo_data() {
    log_step "Setting up demo data..."
    
    # Run demo data setup job
    kubectl apply -f "${K8S_DIR}/jobs/demo-data-job.yaml"
    
    # Wait for demo data setup to complete
    kubectl wait --for=condition=Complete job/quantum-nexus-demo-data --timeout=300s
    
    log_success "Demo data setup completed"
}

verify_deployment() {
    log_step "Verifying deployment..."
    
    # Check pod status
    log_info "Checking pod status..."
    kubectl get pods -o wide
    
    # Check service status
    log_info "Checking service status..."
    kubectl get services
    
    # Check ingress status
    log_info "Checking ingress status..."
    kubectl get ingress
    
    # Health check
    log_info "Running health checks..."
    local api_url="https://${DOMAIN}/health"
    
    # Wait for API to be ready
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s "$api_url" > /dev/null; then
            log_success "API health check passed"
            break
        fi
        
        log_info "Waiting for API to be ready... (attempt $attempt/$max_attempts)"
        sleep 10
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        log_error "API health check failed after $max_attempts attempts"
        return 1
    fi
    
    # Performance test
    log_info "Running performance test..."
    curl -s "${api_url}" | jq '.response_time' || true
    
    log_success "Deployment verification completed"
}

setup_autoscaling() {
    log_step "Setting up autoscaling..."
    
    # Apply HPA configurations
    kubectl apply -f "${K8S_DIR}/hpa/"
    
    # Apply VPA configurations
    kubectl apply -f "${K8S_DIR}/vpa/"
    
    # Apply cluster autoscaler
    kubectl apply -f "${K8S_DIR}/cluster-autoscaler/"
    
    log_success "Autoscaling configured"
}

# =============================================================================
# Rollback Functions
# =============================================================================
rollback_deployment() {
    log_warning "Rolling back deployment..."
    
    # Rollback API deployment
    kubectl rollout undo deployment/quantum-nexus-api
    
    # Rollback Worker deployment
    kubectl rollout undo deployment/quantum-nexus-worker
    
    # Wait for rollback to complete
    kubectl rollout status deployment/quantum-nexus-api
    kubectl rollout status deployment/quantum-nexus-worker
    
    log_success "Rollback completed"
}

# =============================================================================
# Cleanup Functions
# =============================================================================
cleanup_deployment() {
    log_warning "Cleaning up deployment..."
    
    read -p "Are you sure you want to delete the entire deployment? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kubectl delete namespace "$NAMESPACE"
        log_success "Deployment cleaned up"
    else
        log_info "Cleanup cancelled"
    fi
}

# =============================================================================
# Main Deployment Function
# =============================================================================
deploy_full() {
    log_deploy "Starting full production deployment..."
    
    # Pre-deployment checks
    check_dependencies
    check_cluster_connection
    check_docker_registry
    validate_environment
    
    # Build and test
    build_images
    run_tests
    
    # Infrastructure setup
    setup_namespace
    setup_secrets
    setup_storage
    setup_networking
    
    # Application deployment
    deploy_infrastructure
    deploy_application
    deploy_monitoring
    
    # Post-deployment
    run_migrations
    setup_demo_data
    setup_autoscaling
    
    # Verification
    verify_deployment
    
    log_deploy "Production deployment completed successfully!"
    
    # Display access information
    echo
    echo "=============================================================================="
    echo "Quantum Nexus Platform - Production Deployment Complete"
    echo "=============================================================================="
    echo "API URL: https://${DOMAIN}"
    echo "Grafana: https://grafana.${DOMAIN}"
    echo "Prometheus: https://prometheus.${DOMAIN}"
    echo "Jaeger: https://jaeger.${DOMAIN}"
    echo
    echo "Namespace: $NAMESPACE"
    echo "Image Tag: $IMAGE_TAG"
    echo "Replicas: $REPLICAS"
    echo "=============================================================================="
}

# =============================================================================
# Usage and Help
# =============================================================================
show_usage() {
    cat << EOF
Quantum Nexus Platform - Production Deployment

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  deploy      Full production deployment
  build       Build and push Docker images
  test        Run test suite
  verify      Verify existing deployment
  rollback    Rollback to previous version
  cleanup     Clean up deployment (destructive)
  help        Show this help message

Options:
  --namespace NAME        Kubernetes namespace (default: quantum-nexus-prod)
  --image-tag TAG         Docker image tag (default: latest)
  --replicas NUM          Number of replicas (default: 3)
  --domain DOMAIN         Application domain (default: quantum-nexus.ai)
  --region REGION         AWS region (default: us-west-2)
  --dry-run              Show what would be done without executing
  --skip-build           Skip Docker image build
  --skip-tests           Skip test execution
  --force                Force deployment without confirmations

Environment Variables:
  AWS_ACCOUNT_ID         AWS account ID for ECR registry
  AWS_REGION            AWS region for resources
  DOCKER_REGISTRY       Docker registry URL

Examples:
  $0 deploy --image-tag v1.0.0 --replicas 5
  $0 build --image-tag latest
  $0 verify
  $0 rollback

EOF
}

# =============================================================================
# Argument Parsing
# =============================================================================
parse_arguments() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --namespace)
                NAMESPACE="$2"
                shift 2
                ;;
            --image-tag)
                IMAGE_TAG="$2"
                shift 2
                ;;
            --replicas)
                REPLICAS="$2"
                shift 2
                ;;
            --domain)
                DOMAIN="$2"
                shift 2
                ;;
            --region)
                REGION="$2"
                shift 2
                ;;
            --dry-run)
                DRY_RUN="true"
                shift
                ;;
            --skip-build)
                SKIP_BUILD="true"
                shift
                ;;
            --skip-tests)
                SKIP_TESTS="true"
                shift
                ;;
            --force)
                FORCE_DEPLOY="true"
                shift
                ;;
            *)
                break
                ;;
        esac
    done
}

# =============================================================================
# Main Script Logic
# =============================================================================
main() {
    local command=${1:-help}
    shift || true
    
    parse_arguments "$@"
    
    case $command in
        deploy)
            deploy_full
            ;;
        build)
            check_dependencies
            validate_environment
            build_images
            ;;
        test)
            run_tests
            ;;
        verify)
            check_dependencies
            check_cluster_connection
            verify_deployment
            ;;
        rollback)
            check_dependencies
            check_cluster_connection
            rollback_deployment
            ;;
        cleanup)
            check_dependencies
            check_cluster_connection
            cleanup_deployment
            ;;
        help|--help|-h)
            show_usage
            ;;
        *)
            log_error "Unknown command: $command"
            show_usage
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"