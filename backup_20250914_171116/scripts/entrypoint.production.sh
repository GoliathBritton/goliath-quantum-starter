#!/bin/bash
# Quantum Nexus Platform - Production API Entrypoint
# Handles startup sequence, migrations, and health checks

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================
APP_NAME="quantum-nexus-api"
LOG_LEVEL=${LOG_LEVEL:-INFO}
WORKERS=${WORKERS:-4}
WORKER_CLASS=${WORKER_CLASS:-uvicorn.workers.UvicornWorker}
WORKER_CONNECTIONS=${WORKER_CONNECTIONS:-1000}
MAX_REQUESTS=${MAX_REQUESTS:-1000}
MAX_REQUESTS_JITTER=${MAX_REQUESTS_JITTER:-100}
TIMEOUT=${TIMEOUT:-30}
KEEPALIVE=${KEEPALIVE:-5}
BIND=${BIND:-0.0.0.0:8000}
METRICS_PORT=${METRICS_PORT:-9090}

# =============================================================================
# Logging Functions
# =============================================================================
log() {
    echo "$(date -u +'%Y-%m-%dT%H:%M:%S.%3NZ') [${APP_NAME}] $1" >&2
}

log_info() {
    log "INFO: $1"
}

log_warn() {
    log "WARN: $1"
}

log_error() {
    log "ERROR: $1"
}

log_fatal() {
    log "FATAL: $1"
    exit 1
}

# =============================================================================
# Health Check Functions
# =============================================================================
check_database() {
    log_info "Checking database connectivity..."
    python -c "
import sys
import os
sys.path.insert(0, '/app')
try:
    from src.nqba_stack.database import get_database_health
    health = get_database_health()
    if health['status'] != 'healthy':
        print(f'Database health check failed: {health}')
        sys.exit(1)
    print('Database connectivity: OK')
except Exception as e:
    print(f'Database health check error: {e}')
    sys.exit(1)
"
}

check_redis() {
    log_info "Checking Redis connectivity..."
    python -c "
import sys
import os
sys.path.insert(0, '/app')
try:
    from src.nqba_stack.cache import get_redis_health
    health = get_redis_health()
    if health['status'] != 'healthy':
        print(f'Redis health check failed: {health}')
        sys.exit(1)
    print('Redis connectivity: OK')
except Exception as e:
    print(f'Redis health check error: {e}')
    sys.exit(1)
"
}

check_external_services() {
    log_info "Checking external service connectivity..."
    python -c "
import sys
import os
sys.path.insert(0, '/app')
try:
    from src.nqba_stack.external import check_external_services
    results = check_external_services()
    failed_services = [name for name, status in results.items() if not status['healthy']]
    if failed_services:
        print(f'External services health check failed: {failed_services}')
        # Don't exit for external services in production - log warning instead
        print('WARNING: Some external services are unavailable but continuing startup')
    else:
        print('External services connectivity: OK')
except Exception as e:
    print(f'External services health check error: {e}')
    print('WARNING: External services health check failed but continuing startup')
"
}

# =============================================================================
# Database Migration Functions
# =============================================================================
run_migrations() {
    log_info "Running database migrations..."
    python -c "
import sys
import os
sys.path.insert(0, '/app')
try:
    from src.nqba_stack.database import run_migrations
    run_migrations()
    print('Database migrations completed successfully')
except Exception as e:
    print(f'Database migration error: {e}')
    sys.exit(1)
"
}

setup_demo_data() {
    if [[ "${ENABLE_DEMO_DATA:-false}" == "true" ]]; then
        log_info "Setting up demo data..."
        python -c "
import sys
import os
sys.path.insert(0, '/app')
try:
    from src.nqba_stack.demo import setup_demo_data
    setup_demo_data()
    print('Demo data setup completed successfully')
except Exception as e:
    print(f'Demo data setup error: {e}')
    # Don't exit for demo data failures
    print('WARNING: Demo data setup failed but continuing startup')
"
    fi
}

# =============================================================================
# Prometheus Setup
# =============================================================================
setup_prometheus() {
    log_info "Setting up Prometheus metrics..."
    
    # Ensure prometheus directory exists and is writable
    mkdir -p /tmp/prometheus
    chmod 777 /tmp/prometheus
    
    # Clear any existing prometheus files
    rm -f /tmp/prometheus/*.db
    
    log_info "Prometheus metrics directory prepared"
}

# =============================================================================
# Signal Handlers
# =============================================================================
cleanup() {
    log_info "Received shutdown signal, cleaning up..."
    
    # Kill gunicorn gracefully
    if [[ -n "${GUNICORN_PID:-}" ]]; then
        log_info "Stopping Gunicorn (PID: $GUNICORN_PID)..."
        kill -TERM "$GUNICORN_PID" 2>/dev/null || true
        
        # Wait for graceful shutdown
        for i in {1..30}; do
            if ! kill -0 "$GUNICORN_PID" 2>/dev/null; then
                log_info "Gunicorn stopped gracefully"
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if kill -0 "$GUNICORN_PID" 2>/dev/null; then
            log_warn "Force killing Gunicorn..."
            kill -KILL "$GUNICORN_PID" 2>/dev/null || true
        fi
    fi
    
    # Clean up prometheus files
    rm -f /tmp/prometheus/*.db
    
    log_info "Cleanup completed"
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT SIGQUIT

# =============================================================================
# Pre-flight Checks
# =============================================================================
log_info "Starting Quantum Nexus API Server (Production)"
log_info "Environment: ${ENVIRONMENT:-production}"
log_info "Log Level: ${LOG_LEVEL}"
log_info "Workers: ${WORKERS}"
log_info "Worker Class: ${WORKER_CLASS}"
log_info "Bind Address: ${BIND}"

# Validate required environment variables
required_vars=("DATABASE_URL" "REDIS_URL" "SECRET_KEY")
for var in "${required_vars[@]}"; do
    if [[ -z "${!var:-}" ]]; then
        log_fatal "Required environment variable $var is not set"
    fi
done

# =============================================================================
# Startup Sequence
# =============================================================================

# 1. Setup Prometheus
setup_prometheus

# 2. Health checks
check_database
check_redis
check_external_services

# 3. Database migrations
run_migrations

# 4. Demo data (if enabled)
setup_demo_data

# 5. Start metrics server in background
log_info "Starting Prometheus metrics server on port ${METRICS_PORT}..."
python -c "
import sys
import os
sys.path.insert(0, '/app')
from src.nqba_stack.monitoring import start_metrics_server
start_metrics_server(${METRICS_PORT})
" &
METRICS_PID=$!

# 6. Start main application
log_info "Starting Gunicorn application server..."

# Build Gunicorn command
GUNICORN_CMD=(
    "gunicorn"
    "--bind" "${BIND}"
    "--workers" "${WORKERS}"
    "--worker-class" "${WORKER_CLASS}"
    "--worker-connections" "${WORKER_CONNECTIONS}"
    "--max-requests" "${MAX_REQUESTS}"
    "--max-requests-jitter" "${MAX_REQUESTS_JITTER}"
    "--timeout" "${TIMEOUT}"
    "--keepalive" "${KEEPALIVE}"
    "--log-level" "${LOG_LEVEL,,}"
    "--access-logfile" "-"
    "--error-logfile" "-"
    "--capture-output"
    "--enable-stdio-inheritance"
    "--preload"
    "--pid" "/tmp/gunicorn.pid"
    "main:app"
)

# Start Gunicorn
"${GUNICORN_CMD[@]}" &
GUNICORN_PID=$!

log_info "Gunicorn started with PID: $GUNICORN_PID"
log_info "Quantum Nexus API Server is ready to accept connections"

# =============================================================================
# Main Loop
# =============================================================================

# Wait for Gunicorn to finish
wait $GUNICORN_PID
GUNICORN_EXIT_CODE=$?

# Clean up
log_info "Gunicorn exited with code: $GUNICORN_EXIT_CODE"
kill $METRICS_PID 2>/dev/null || true

exit $GUNICORN_EXIT_CODE