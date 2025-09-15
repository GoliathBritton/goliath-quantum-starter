#!/bin/bash
# NQBA Platform API Server Entrypoint Script
# Handles graceful startup, health checks, and shutdown

set -e

# Color codes for logging
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

# Trap signals for graceful shutdown
trap 'shutdown_handler' SIGTERM SIGINT

# Graceful shutdown handler
shutdown_handler() {
    log_info "Received shutdown signal, initiating graceful shutdown..."
    
    if [ ! -z "$API_PID" ]; then
        log_info "Stopping API server (PID: $API_PID)..."
        kill -TERM "$API_PID" 2>/dev/null || true
        
        # Wait for graceful shutdown (max 30 seconds)
        local count=0
        while kill -0 "$API_PID" 2>/dev/null && [ $count -lt 30 ]; do
            sleep 1
            count=$((count + 1))
        done
        
        # Force kill if still running
        if kill -0 "$API_PID" 2>/dev/null; then
            log_warn "Force killing API server..."
            kill -KILL "$API_PID" 2>/dev/null || true
        fi
    fi
    
    log_success "Shutdown complete"
    exit 0
}

# Health check function
health_check() {
    local max_attempts=30
    local attempt=1
    
    log_info "Waiting for API server to be ready..."
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f -s http://localhost:8000/health > /dev/null 2>&1; then
            log_success "API server is ready and healthy"
            return 0
        fi
        
        log_info "Health check attempt $attempt/$max_attempts failed, retrying in 2 seconds..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    log_error "API server failed to become healthy after $max_attempts attempts"
    return 1
}

# Database connectivity check
check_database() {
    if [ -n "$DATABASE_URL" ]; then
        log_info "Checking database connectivity..."
        
        python3 -c "
import sys
import psycopg2
from urllib.parse import urlparse
import os

try:
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print('No DATABASE_URL provided, skipping database check')
        sys.exit(0)
    
    # Parse database URL
    parsed = urlparse(db_url)
    
    # Test connection
    conn = psycopg2.connect(
        host=parsed.hostname,
        port=parsed.port or 5432,
        database=parsed.path[1:] if parsed.path else 'postgres',
        user=parsed.username,
        password=parsed.password
    )
    
    # Test query
    cur = conn.cursor()
    cur.execute('SELECT 1')
    cur.fetchone()
    cur.close()
    conn.close()
    
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')
    sys.exit(1)
" && log_success "Database connectivity check passed" || {
            log_error "Database connectivity check failed"
            exit 1
        }
    else
        log_warn "No DATABASE_URL provided, skipping database check"
    fi
}

# Redis connectivity check
check_redis() {
    if [ -n "$REDIS_URL" ]; then
        log_info "Checking Redis connectivity..."
        
        python3 -c "
import sys
import redis
from urllib.parse import urlparse
import os

try:
    redis_url = os.environ.get('REDIS_URL')
    if not redis_url:
        print('No REDIS_URL provided, skipping Redis check')
        sys.exit(0)
    
    # Create Redis client
    r = redis.from_url(redis_url)
    
    # Test connection
    r.ping()
    
    print('Redis connection successful')
except Exception as e:
    print(f'Redis connection failed: {e}')
    sys.exit(1)
" && log_success "Redis connectivity check passed" || {
            log_error "Redis connectivity check failed"
            exit 1
        }
    else
        log_warn "No REDIS_URL provided, skipping Redis check"
    fi
}

# Environment validation
validate_environment() {
    log_info "Validating environment configuration..."
    
    # Required environment variables
    local required_vars=(
        "ENVIRONMENT"
        "SECRET_KEY"
        "JWT_SECRET_KEY"
    )
    
    local missing_vars=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        log_error "Missing required environment variables: ${missing_vars[*]}"
        exit 1
    fi
    
    # Validate environment value
    if [ "$ENVIRONMENT" != "production" ] && [ "$ENVIRONMENT" != "staging" ] && [ "$ENVIRONMENT" != "development" ]; then
        log_error "Invalid ENVIRONMENT value: $ENVIRONMENT (must be production, staging, or development)"
        exit 1
    fi
    
    log_success "Environment validation passed"
}

# Database migration
run_migrations() {
    if [ "$SKIP_MIGRATIONS" = "true" ]; then
        log_info "Skipping database migrations (SKIP_MIGRATIONS=true)"
        return 0
    fi
    
    log_info "Running database migrations..."
    
    # Run Alembic migrations if available
    if [ -f "alembic.ini" ]; then
        alembic upgrade head && log_success "Database migrations completed" || {
            log_error "Database migrations failed"
            exit 1
        }
    else
        log_warn "No alembic.ini found, skipping migrations"
    fi
}

# Main execution
main() {
    log_info "Starting NQBA Platform API Server..."
    log_info "Environment: ${ENVIRONMENT:-unknown}"
    log_info "Python version: $(python3 --version)"
    log_info "Working directory: $(pwd)"
    
    # Validate environment
    validate_environment
    
    # Check external dependencies
    check_database
    check_redis
    
    # Run database migrations
    run_migrations
    
    # Determine startup command based on environment
    local cmd
    if [ "$ENVIRONMENT" = "production" ]; then
        # Production: Use Gunicorn with optimized settings
        cmd="gunicorn \
            --bind 0.0.0.0:8000 \
            --workers ${WORKERS:-4} \
            --worker-class uvicorn.workers.UvicornWorker \
            --worker-connections 1000 \
            --max-requests 1000 \
            --max-requests-jitter 100 \
            --timeout ${CONTAINER_TIMEOUT:-300} \
            --keep-alive ${CONTAINER_KEEP_ALIVE:-2} \
            --preload \
            --access-logfile - \
            --error-logfile - \
            --log-level ${LOG_LEVEL:-info} \
            --capture-output \
            --enable-stdio-inheritance \
            api_server:app"
    else
        # Development/Staging: Use Uvicorn with auto-reload
        cmd="uvicorn \
            --host 0.0.0.0 \
            --port 8000 \
            --log-level ${LOG_LEVEL:-info} \
            --access-log \
            api_server:app"
        
        if [ "$ENVIRONMENT" = "development" ]; then
            cmd="$cmd --reload"
        fi
    fi
    
    log_info "Starting server with command: $cmd"
    
    # Start the API server in background
    eval "$cmd" &
    API_PID=$!
    
    log_info "API server started with PID: $API_PID"
    
    # Wait for server to be ready
    if [ "$SKIP_HEALTH_CHECK" != "true" ]; then
        health_check || {
            log_error "Health check failed, shutting down..."
            kill "$API_PID" 2>/dev/null || true
            exit 1
        }
    fi
    
    log_success "NQBA Platform API Server is running and ready to accept requests"
    
    # Wait for the API server process
    wait "$API_PID"
}

# Execute main function
main "$@"