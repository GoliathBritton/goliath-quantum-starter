#!/bin/bash
# Quantum Nexus Platform - Health Check Script
# Comprehensive health validation for production containers

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================
HEALTH_CHECK_URL="http://localhost:8000/health"
READINESS_CHECK_URL="http://localhost:8000/ready"
METRICS_CHECK_URL="http://localhost:9090/metrics"
TIMEOUT=10
RETRIES=3
RETRY_DELAY=2

# =============================================================================
# Logging Functions
# =============================================================================
log() {
    echo "$(date -u +'%Y-%m-%dT%H:%M:%S.%3NZ') [healthcheck] $1" >&2
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

# =============================================================================
# Health Check Functions
# =============================================================================

# Check if the main application is responding
check_application_health() {
    local url="$1"
    local description="$2"
    
    log_info "Checking $description at $url"
    
    for attempt in $(seq 1 $RETRIES); do
        if curl -f -s --max-time $TIMEOUT "$url" > /dev/null 2>&1; then
            log_info "$description: OK"
            return 0
        else
            log_warn "$description check failed (attempt $attempt/$RETRIES)"
            if [[ $attempt -lt $RETRIES ]]; then
                sleep $RETRY_DELAY
            fi
        fi
    done
    
    log_error "$description: FAILED after $RETRIES attempts"
    return 1
}

# Check application health endpoint with detailed response
check_detailed_health() {
    log_info "Performing detailed health check"
    
    local response
    local http_code
    
    for attempt in $(seq 1 $RETRIES); do
        response=$(curl -s --max-time $TIMEOUT -w "HTTP_CODE:%{http_code}" "$HEALTH_CHECK_URL" 2>/dev/null || echo "CURL_FAILED")
        
        if [[ "$response" == "CURL_FAILED" ]]; then
            log_warn "Health check request failed (attempt $attempt/$RETRIES)"
            if [[ $attempt -lt $RETRIES ]]; then
                sleep $RETRY_DELAY
            fi
            continue
        fi
        
        # Extract HTTP code
        http_code=$(echo "$response" | grep -o 'HTTP_CODE:[0-9]*' | cut -d: -f2)
        response_body=$(echo "$response" | sed 's/HTTP_CODE:[0-9]*$//')
        
        if [[ "$http_code" == "200" ]]; then
            log_info "Health check: OK (HTTP $http_code)"
            
            # Parse JSON response if possible
            if command -v python3 >/dev/null 2>&1; then
                python3 -c "
import json
import sys
try:
    data = json.loads('$response_body')
    status = data.get('status', 'unknown')
    if status == 'healthy':
        print('Application status: healthy')
        sys.exit(0)
    else:
        print(f'Application status: {status}')
        sys.exit(1)
except:
    print('Health response parsing failed, but HTTP 200 received')
    sys.exit(0)
" 2>/dev/null
                return $?
            else
                # Fallback: just check for "healthy" in response
                if echo "$response_body" | grep -q "healthy"; then
                    log_info "Application status: healthy"
                    return 0
                else
                    log_warn "Application status: unknown (no JSON parser available)"
                    return 0  # Still return success for HTTP 200
                fi
            fi
        else
            log_warn "Health check returned HTTP $http_code (attempt $attempt/$RETRIES)"
            if [[ $attempt -lt $RETRIES ]]; then
                sleep $RETRY_DELAY
            fi
        fi
    done
    
    log_error "Detailed health check failed after $RETRIES attempts"
    return 1
}

# Check if metrics endpoint is responding
check_metrics() {
    log_info "Checking metrics endpoint"
    
    for attempt in $(seq 1 $RETRIES); do
        if curl -f -s --max-time $TIMEOUT "$METRICS_CHECK_URL" | head -n 5 > /dev/null 2>&1; then
            log_info "Metrics endpoint: OK"
            return 0
        else
            log_warn "Metrics check failed (attempt $attempt/$RETRIES)"
            if [[ $attempt -lt $RETRIES ]]; then
                sleep $RETRY_DELAY
            fi
        fi
    done
    
    log_warn "Metrics endpoint: FAILED (non-critical)"
    return 0  # Don't fail health check for metrics
}

# Check process health
check_process_health() {
    log_info "Checking process health"
    
    # Check if gunicorn master process is running
    if pgrep -f "gunicorn.*master" > /dev/null; then
        log_info "Gunicorn master process: OK"
    else
        log_error "Gunicorn master process: NOT FOUND"
        return 1
    fi
    
    # Check if worker processes are running
    local worker_count
    worker_count=$(pgrep -f "gunicorn.*worker" | wc -l)
    
    if [[ $worker_count -gt 0 ]]; then
        log_info "Gunicorn worker processes: $worker_count running"
    else
        log_error "Gunicorn worker processes: NONE FOUND"
        return 1
    fi
    
    return 0
}

# Check disk space
check_disk_space() {
    log_info "Checking disk space"
    
    local usage
    usage=$(df /app | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [[ $usage -lt 90 ]]; then
        log_info "Disk space: OK (${usage}% used)"
        return 0
    elif [[ $usage -lt 95 ]]; then
        log_warn "Disk space: WARNING (${usage}% used)"
        return 0  # Warning but not critical
    else
        log_error "Disk space: CRITICAL (${usage}% used)"
        return 1
    fi
}

# Check memory usage
check_memory() {
    log_info "Checking memory usage"
    
    if command -v free >/dev/null 2>&1; then
        local mem_usage
        mem_usage=$(free | awk 'NR==2{printf "%.0f", $3*100/$2}')
        
        if [[ $mem_usage -lt 90 ]]; then
            log_info "Memory usage: OK (${mem_usage}% used)"
        elif [[ $mem_usage -lt 95 ]]; then
            log_warn "Memory usage: WARNING (${mem_usage}% used)"
        else
            log_warn "Memory usage: HIGH (${mem_usage}% used)"
        fi
    else
        log_info "Memory check: SKIPPED (free command not available)"
    fi
    
    return 0  # Don't fail health check for memory
}

# =============================================================================
# Main Health Check
# =============================================================================
main() {
    log_info "Starting comprehensive health check"
    
    local exit_code=0
    
    # Critical checks (must pass)
    if ! check_process_health; then
        exit_code=1
    fi
    
    if ! check_detailed_health; then
        exit_code=1
    fi
    
    if ! check_disk_space; then
        exit_code=1
    fi
    
    # Non-critical checks (warnings only)
    check_metrics || true
    check_memory || true
    
    # Additional readiness check if available
    if curl -f -s --max-time 5 "$READINESS_CHECK_URL" > /dev/null 2>&1; then
        log_info "Readiness check: OK"
    else
        log_warn "Readiness check: FAILED (non-critical)"
    fi
    
    if [[ $exit_code -eq 0 ]]; then
        log_info "Health check: PASSED"
    else
        log_error "Health check: FAILED"
    fi
    
    return $exit_code
}

# =============================================================================
# Script Execution
# =============================================================================

# Handle script arguments
case "${1:-}" in
    "--quick")
        log_info "Running quick health check"
        check_application_health "$HEALTH_CHECK_URL" "Application health"
        ;;
    "--metrics")
        log_info "Running metrics check only"
        check_metrics
        ;;
    "--process")
        log_info "Running process check only"
        check_process_health
        ;;
    *)
        main
        ;;
esac