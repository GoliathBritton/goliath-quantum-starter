#!/bin/bash
# Quantum Nexus Platform - Kubernetes Secrets Management
# Production-ready secrets setup for secure deployment

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
NAMESPACE="quantum-nexus-prod"
ENV_FILE="${PROJECT_ROOT}/.env.production"
SECRETS_DIR="${PROJECT_ROOT}/deploy/secrets"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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

# =============================================================================
# Utility Functions
# =============================================================================
generate_random_password() {
    local length=${1:-32}
    openssl rand -base64 $length | tr -d "=+/" | cut -c1-$length
}

generate_jwt_secret() {
    openssl rand -hex 64
}

generate_api_key() {
    echo "qn_$(openssl rand -hex 16)"
}

check_dependencies() {
    local deps=("kubectl" "openssl" "base64")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log_error "Required dependency '$dep' is not installed"
            exit 1
        fi
    done
}

check_kubernetes_connection() {
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    log_success "Connected to Kubernetes cluster"
}

# =============================================================================
# Secret Generation Functions
# =============================================================================
generate_database_secrets() {
    log_info "Generating database secrets..."
    
    cat > "${SECRETS_DIR}/database-secrets.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: quantum-nexus-database
  namespace: ${NAMESPACE}
type: Opaque
data:
  POSTGRES_USER: $(echo -n "quantum_nexus" | base64 -w 0)
  POSTGRES_PASSWORD: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
  POSTGRES_DB: $(echo -n "quantum_nexus_prod" | base64 -w 0)
  DATABASE_URL: $(echo -n "postgresql://quantum_nexus:$(generate_random_password 32)@postgres:5432/quantum_nexus_prod" | base64 -w 0)
EOF
}

generate_redis_secrets() {
    log_info "Generating Redis secrets..."
    
    local redis_password=$(generate_random_password 32)
    
    cat > "${SECRETS_DIR}/redis-secrets.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: quantum-nexus-redis
  namespace: ${NAMESPACE}
type: Opaque
data:
  REDIS_PASSWORD: $(echo -n "$redis_password" | base64 -w 0)
  REDIS_URL: $(echo -n "redis://:$redis_password@redis:6379/0" | base64 -w 0)
EOF
}

generate_nats_secrets() {
    log_info "Generating NATS secrets..."
    
    cat > "${SECRETS_DIR}/nats-secrets.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: quantum-nexus-nats
  namespace: ${NAMESPACE}
type: Opaque
data:
  NATS_CLUSTER_PASSWORD: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
  NATS_API_PASSWORD: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
  NATS_WORKER_PASSWORD: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
  NATS_MONITOR_PASSWORD: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
  NATS_URL: $(echo -n "nats://quantum_api:$(generate_random_password 32)@nats:4222" | base64 -w 0)
EOF
}

generate_app_secrets() {
    log_info "Generating application secrets..."
    
    cat > "${SECRETS_DIR}/app-secrets.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: quantum-nexus-app
  namespace: ${NAMESPACE}
type: Opaque
data:
  SECRET_KEY: $(echo -n "$(generate_jwt_secret)" | base64 -w 0)
  JWT_SECRET: $(echo -n "$(generate_jwt_secret)" | base64 -w 0)
  API_KEY: $(echo -n "$(generate_api_key)" | base64 -w 0)
  ENCRYPTION_KEY: $(echo -n "$(openssl rand -base64 32)" | base64 -w 0)
  WEBHOOK_SECRET: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
EOF
}

generate_external_api_secrets() {
    log_info "Generating external API secrets..."
    
    # These should be replaced with actual values
    cat > "${SECRETS_DIR}/external-api-secrets.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: quantum-nexus-external-apis
  namespace: ${NAMESPACE}
type: Opaque
data:
  OPENAI_API_KEY: $(echo -n "sk-placeholder-openai-key" | base64 -w 0)
  ANTHROPIC_API_KEY: $(echo -n "sk-placeholder-anthropic-key" | base64 -w 0)
  DYNEX_API_KEY: $(echo -n "placeholder-dynex-key" | base64 -w 0)
  STRIPE_SECRET_KEY: $(echo -n "sk_test_placeholder" | base64 -w 0)
  STRIPE_WEBHOOK_SECRET: $(echo -n "whsec_placeholder" | base64 -w 0)
  TWILIO_ACCOUNT_SID: $(echo -n "ACplaceholder" | base64 -w 0)
  TWILIO_AUTH_TOKEN: $(echo -n "placeholder-token" | base64 -w 0)
EOF
}

generate_aws_secrets() {
    log_info "Generating AWS secrets..."
    
    cat > "${SECRETS_DIR}/aws-secrets.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: quantum-nexus-aws
  namespace: ${NAMESPACE}
type: Opaque
data:
  AWS_ACCESS_KEY_ID: $(echo -n "AKIA-placeholder" | base64 -w 0)
  AWS_SECRET_ACCESS_KEY: $(echo -n "placeholder-secret-key" | base64 -w 0)
  AWS_REGION: $(echo -n "us-west-2" | base64 -w 0)
  AWS_S3_BUCKET: $(echo -n "quantum-nexus-storage" | base64 -w 0)
EOF
}

generate_monitoring_secrets() {
    log_info "Generating monitoring secrets..."
    
    cat > "${SECRETS_DIR}/monitoring-secrets.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: quantum-nexus-monitoring
  namespace: ${NAMESPACE}
type: Opaque
data:
  PROMETHEUS_PASSWORD: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
  GRAFANA_ADMIN_PASSWORD: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
  JAEGER_PASSWORD: $(echo -n "$(generate_random_password 32)" | base64 -w 0)
  SENTRY_DSN: $(echo -n "https://placeholder@sentry.io/project" | base64 -w 0)
EOF
}

# =============================================================================
# TLS Certificate Generation
# =============================================================================
generate_tls_certificates() {
    log_info "Generating TLS certificates..."
    
    local certs_dir="${SECRETS_DIR}/certs"
    mkdir -p "$certs_dir"
    
    # Generate CA private key
    openssl genrsa -out "${certs_dir}/ca-key.pem" 4096
    
    # Generate CA certificate
    openssl req -new -x509 -days 365 -key "${certs_dir}/ca-key.pem" \
        -out "${certs_dir}/ca-cert.pem" \
        -subj "/C=US/ST=CA/L=San Francisco/O=Quantum Nexus/CN=Quantum Nexus CA"
    
    # Generate server private key
    openssl genrsa -out "${certs_dir}/server-key.pem" 4096
    
    # Generate server certificate signing request
    openssl req -new -key "${certs_dir}/server-key.pem" \
        -out "${certs_dir}/server.csr" \
        -subj "/C=US/ST=CA/L=San Francisco/O=Quantum Nexus/CN=quantum-nexus.local"
    
    # Generate server certificate
    openssl x509 -req -days 365 -in "${certs_dir}/server.csr" \
        -CA "${certs_dir}/ca-cert.pem" -CAkey "${certs_dir}/ca-key.pem" \
        -CAcreateserial -out "${certs_dir}/server-cert.pem"
    
    # Create TLS secret
    cat > "${SECRETS_DIR}/tls-secrets.yaml" << EOF
apiVersion: v1
kind: Secret
metadata:
  name: quantum-nexus-tls
  namespace: ${NAMESPACE}
type: kubernetes.io/tls
data:
  tls.crt: $(base64 -w 0 < "${certs_dir}/server-cert.pem")
  tls.key: $(base64 -w 0 < "${certs_dir}/server-key.pem")
  ca.crt: $(base64 -w 0 < "${certs_dir}/ca-cert.pem")
EOF
    
    # Clean up CSR
    rm "${certs_dir}/server.csr"
}

# =============================================================================
# ConfigMap Generation
# =============================================================================
generate_configmaps() {
    log_info "Generating ConfigMaps..."
    
    cat > "${SECRETS_DIR}/app-config.yaml" << EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: quantum-nexus-config
  namespace: ${NAMESPACE}
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  DEBUG: "false"
  WORKERS: "4"
  MAX_CONNECTIONS: "1000"
  TIMEOUT: "30"
  CORS_ORIGINS: "https://quantum-nexus.ai,https://app.quantum-nexus.ai"
  RATE_LIMIT_PER_MINUTE: "100"
  MAX_UPLOAD_SIZE: "100MB"
  SESSION_TIMEOUT: "3600"
  CACHE_TTL: "300"
  QUANTUM_TIMEOUT: "600"
  METRICS_ENABLED: "true"
  TRACING_ENABLED: "true"
  HEALTH_CHECK_INTERVAL: "30"
EOF
}

# =============================================================================
# Secret Application Functions
# =============================================================================
apply_secrets() {
    log_info "Applying secrets to Kubernetes..."
    
    # Create namespace if it doesn't exist
    kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -
    
    # Apply all secret files
    for secret_file in "${SECRETS_DIR}"/*.yaml; do
        if [[ -f "$secret_file" ]]; then
            log_info "Applying $(basename "$secret_file")..."
            kubectl apply -f "$secret_file"
        fi
    done
    
    log_success "All secrets applied successfully"
}

verify_secrets() {
    log_info "Verifying secrets..."
    
    local secrets=(
        "quantum-nexus-database"
        "quantum-nexus-redis"
        "quantum-nexus-nats"
        "quantum-nexus-app"
        "quantum-nexus-external-apis"
        "quantum-nexus-aws"
        "quantum-nexus-monitoring"
        "quantum-nexus-tls"
    )
    
    for secret in "${secrets[@]}"; do
        if kubectl get secret "$secret" -n "$NAMESPACE" &> /dev/null; then
            log_success "Secret '$secret' exists"
        else
            log_error "Secret '$secret' not found"
        fi
    done
}

# =============================================================================
# Backup and Restore Functions
# =============================================================================
backup_secrets() {
    log_info "Backing up secrets..."
    
    local backup_dir="${SECRETS_DIR}/backup/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    kubectl get secrets -n "$NAMESPACE" -o yaml > "${backup_dir}/secrets-backup.yaml"
    kubectl get configmaps -n "$NAMESPACE" -o yaml > "${backup_dir}/configmaps-backup.yaml"
    
    log_success "Secrets backed up to $backup_dir"
}

rotate_secrets() {
    log_info "Rotating secrets..."
    
    # Backup current secrets
    backup_secrets
    
    # Generate new secrets
    generate_all_secrets
    
    # Apply new secrets
    apply_secrets
    
    log_success "Secrets rotated successfully"
}

# =============================================================================
# Main Functions
# =============================================================================
generate_all_secrets() {
    log_info "Generating all secrets..."
    
    mkdir -p "$SECRETS_DIR"
    
    generate_database_secrets
    generate_redis_secrets
    generate_nats_secrets
    generate_app_secrets
    generate_external_api_secrets
    generate_aws_secrets
    generate_monitoring_secrets
    generate_tls_certificates
    generate_configmaps
    
    log_success "All secrets generated"
}

cleanup_secrets() {
    log_warning "Cleaning up secrets..."
    
    read -p "Are you sure you want to delete all secrets? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kubectl delete secrets -n "$NAMESPACE" --all
        kubectl delete configmaps -n "$NAMESPACE" --all
        log_success "Secrets cleaned up"
    else
        log_info "Cleanup cancelled"
    fi
}

show_usage() {
    cat << EOF
Quantum Nexus Platform - Secrets Management

Usage: $0 [COMMAND]

Commands:
  generate    Generate all secrets and certificates
  apply       Apply secrets to Kubernetes cluster
  verify      Verify that all secrets exist
  backup      Backup current secrets
  rotate      Rotate all secrets (backup + regenerate + apply)
  cleanup     Delete all secrets (use with caution)
  help        Show this help message

Examples:
  $0 generate    # Generate secrets locally
  $0 apply       # Apply secrets to cluster
  $0 rotate      # Rotate all secrets

Environment Variables:
  NAMESPACE      Kubernetes namespace (default: quantum-nexus-prod)
  SECRETS_DIR    Directory for secret files (default: ./deploy/secrets)

EOF
}

# =============================================================================
# Main Script Logic
# =============================================================================
main() {
    local command=${1:-help}
    
    case $command in
        generate)
            check_dependencies
            generate_all_secrets
            ;;
        apply)
            check_dependencies
            check_kubernetes_connection
            apply_secrets
            ;;
        verify)
            check_dependencies
            check_kubernetes_connection
            verify_secrets
            ;;
        backup)
            check_dependencies
            check_kubernetes_connection
            backup_secrets
            ;;
        rotate)
            check_dependencies
            check_kubernetes_connection
            rotate_secrets
            ;;
        cleanup)
            check_dependencies
            check_kubernetes_connection
            cleanup_secrets
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