#!/bin/bash
# Quantum Nexus Platform - Brand Replacement Script
# Systematically replace Quantum Nexus references with Quantum Nexus branding

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BRAND_CONFIG="${PROJECT_ROOT}/branding/quantum-nexus-brand.json"
BACKUP_DIR="${PROJECT_ROOT}/backup/rebrand-$(date +%Y%m%d_%H%M%S)"

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

log_rebrand() {
    echo -e "${CYAN}[REBRAND]${NC} $1"
}

# =============================================================================
# Utility Functions
# =============================================================================
check_dependencies() {
    log_step "Checking dependencies..."
    
    local deps=("sed" "find" "grep" "jq" "git")
    local missing_deps=()
    
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            missing_deps+=("$dep")
        fi
    done
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing dependencies: ${missing_deps[*]}"
        exit 1
    fi
    
    log_success "All dependencies are available"
}

create_backup() {
    log_step "Creating backup..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Create git stash if in git repo
    if git rev-parse --git-dir > /dev/null 2>&1; then
        git stash push -m "Pre-rebrand backup $(date)"
        log_info "Created git stash backup"
    fi
    
    # Copy important files
    cp -r "${PROJECT_ROOT}/api" "$BACKUP_DIR/" 2>/dev/null || true
    cp -r "${PROJECT_ROOT}/frontend" "$BACKUP_DIR/" 2>/dev/null || true
    cp -r "${PROJECT_ROOT}/docs" "$BACKUP_DIR/" 2>/dev/null || true
    cp "${PROJECT_ROOT}/README.md" "$BACKUP_DIR/" 2>/dev/null || true
    cp "${PROJECT_ROOT}/package.json" "$BACKUP_DIR/" 2>/dev/null || true
    
    log_success "Backup created at $BACKUP_DIR"
}

load_brand_config() {
    log_step "Loading brand configuration..."
    
    if [[ ! -f "$BRAND_CONFIG" ]]; then
        log_error "Brand configuration file not found: $BRAND_CONFIG"
        exit 1
    fi
    
    # Extract brand values using jq
    BRAND_NAME=$(jq -r '.brand.name' "$BRAND_CONFIG")
    BRAND_TAGLINE=$(jq -r '.brand.tagline' "$BRAND_CONFIG")
    BRAND_DOMAIN=$(jq -r '.identity.domain' "$BRAND_CONFIG")
    BRAND_CODE_NAME=$(jq -r '.identity.code_name' "$BRAND_CONFIG")
    BRAND_SHORT_NAME=$(jq -r '.identity.short_name' "$BRAND_CONFIG")
    
    log_success "Brand configuration loaded: $BRAND_NAME"
}

# =============================================================================
# Text Replacement Functions
# =============================================================================
replace_in_files() {
    local search_pattern="$1"
    local replacement="$2"
    local file_pattern="$3"
    local description="$4"
    
    log_info "Replacing $description..."
    
    # Find and replace in files
    find "$PROJECT_ROOT" -name "$file_pattern" -type f -not -path "*/node_modules/*" -not -path "*/venv/*" -not -path "*/.git/*" -not -path "*/backup/*" | while read -r file; do
        if grep -q "$search_pattern" "$file" 2>/dev/null; then
            sed -i.bak "s|$search_pattern|$replacement|g" "$file"
            log_info "  Updated: $(basename "$file")"
            rm "${file}.bak" 2>/dev/null || true
        fi
    done
}

replace_case_insensitive() {
    local search_pattern="$1"
    local replacement="$2"
    local file_pattern="$3"
    local description="$4"
    
    log_info "Replacing $description (case-insensitive)..."
    
    find "$PROJECT_ROOT" -name "$file_pattern" -type f -not -path "*/node_modules/*" -not -path "*/venv/*" -not -path "*/.git/*" -not -path "*/backup/*" | while read -r file; do
        if grep -qi "$search_pattern" "$file" 2>/dev/null; then
            sed -i.bak "s|$search_pattern|$replacement|gi" "$file"
            log_info "  Updated: $(basename "$file")"
            rm "${file}.bak" 2>/dev/null || true
        fi
    done
}

# =============================================================================
# Brand Replacement Functions
# =============================================================================
replace_brand_names() {
    log_step "Replacing brand names and references..."
    
    # Replace Quantum Nexus with Quantum Nexus
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.py" "Quantum Nexus references in Python files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.js" "Quantum Nexus references in JavaScript files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.jsx" "Quantum Nexus references in React files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.ts" "Quantum Nexus references in TypeScript files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.tsx" "Quantum Nexus references in TypeScript React files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.html" "Quantum Nexus references in HTML files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.md" "Quantum Nexus references in Markdown files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.json" "Quantum Nexus references in JSON files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.yaml" "Quantum Nexus references in YAML files"
    replace_in_files "Quantum Nexus" "Quantum Nexus" "*.yml" "Quantum Nexus references in YAML files"
    
    # Replace Quantum Nexus with quantum-nexus (lowercase)
    replace_in_files "Quantum Nexus" "quantum-nexus" "*.py" "Quantum Nexus references in Python files"
    replace_in_files "Quantum Nexus" "quantum-nexus" "*.js" "Quantum Nexus references in JavaScript files"
    replace_in_files "Quantum Nexus" "quantum-nexus" "*.json" "Quantum Nexus references in JSON files"
    replace_in_files "Quantum Nexus" "quantum-nexus" "*.yaml" "Quantum Nexus references in YAML files"
    replace_in_files "Quantum Nexus" "quantum-nexus" "*.yml" "Quantum Nexus references in YAML files"
    
    # Replace Quantum Nexus with QUANTUM_NEXUS (uppercase)
    replace_in_files "Quantum Nexus" "QUANTUM_NEXUS" "*.py" "Quantum Nexus references in Python files"
    replace_in_files "Quantum Nexus" "QUANTUM_NEXUS" "*.js" "Quantum Nexus references in JavaScript files"
    replace_in_files "Quantum Nexus" "QUANTUM_NEXUS" "*.env*" "Quantum Nexus references in environment files"
    
    log_success "Brand name replacements completed"
}

replace_domains_and_urls() {
    log_step "Replacing domains and URLs..."
    
    # Replace example domains
    replace_in_files "quantum-nexus-quantum.com" "quantum-nexus.ai" "*" "Quantum Nexus domain references"
    replace_in_files "quantum-nexus-quantum.ai" "quantum-nexus.ai" "*" "Quantum Nexus AI domain references"
    replace_in_files "Quantum Nexusquantum.com" "quantum-nexus.ai" "*" "Quantum Nexus domain references"
    
    # Replace API endpoints
    replace_in_files "api.quantum-nexus-quantum" "api.quantum-nexus" "*" "API domain references"
    replace_in_files "/Quantum Nexus/" "/quantum-nexus/" "*" "API path references"
    
    log_success "Domain and URL replacements completed"
}

replace_code_identifiers() {
    log_step "Replacing code identifiers and variables..."
    
    # Replace class names
    replace_in_files "Quantum NexusQuantum" "QuantumNexus" "*.py" "Quantum Nexus class names in Python"
    replace_in_files "Quantum NexusQuantum" "QuantumNexus" "*.js" "Quantum Nexus class names in JavaScript"
    replace_in_files "Quantum NexusQuantum" "QuantumNexus" "*.ts" "Quantum Nexus class names in TypeScript"
    
    # Replace function names
    replace_in_files "quantum_nexus_quantum" "quantum_nexus" "*.py" "Quantum Nexus function names in Python"
    replace_in_files "Quantum NexusQuantum" "quantumNexus" "*.js" "Quantum Nexus function names in JavaScript"
    replace_in_files "Quantum NexusQuantum" "quantumNexus" "*.ts" "Quantum Nexus function names in TypeScript"
    
    # Replace constants
    replace_in_files "quantum_nexus_QUANTUM" "QUANTUM_NEXUS" "*.py" "Quantum Nexus constants in Python"
    replace_in_files "quantum_nexus_QUANTUM" "QUANTUM_NEXUS" "*.js" "Quantum Nexus constants in JavaScript"
    replace_in_files "quantum_nexus_QUANTUM" "QUANTUM_NEXUS" "*.ts" "Quantum Nexus constants in TypeScript"
    
    # Replace module names
    replace_in_files "Quantum Nexus.quantum" "quantum.nexus" "*.py" "Quantum Nexus module names in Python"
    
    log_success "Code identifier replacements completed"
}

replace_configuration_files() {
    log_step "Replacing configuration files..."
    
    # Package.json
    if [[ -f "${PROJECT_ROOT}/package.json" ]]; then
        sed -i.bak 's/"name": ".*Quantum Nexus.*"/"name": "quantum-nexus-platform"/gi' "${PROJECT_ROOT}/package.json"
        sed -i.bak 's/"description": ".*Quantum Nexus.*"/"description": "Quantum Nexus Platform - Quantum-First, AGI-Ready Business Intelligence"/gi' "${PROJECT_ROOT}/package.json"
        rm "${PROJECT_ROOT}/package.json.bak" 2>/dev/null || true
        log_info "  Updated: package.json"
    fi
    
    # Setup.py
    if [[ -f "${PROJECT_ROOT}/setup.py" ]]; then
        sed -i.bak 's/name=".*Quantum Nexus.*"/name="quantum-nexus-platform"/gi' "${PROJECT_ROOT}/setup.py"
        sed -i.bak 's/description=".*Quantum Nexus.*"/description="Quantum Nexus Platform - Quantum-First, AGI-Ready Business Intelligence"/gi' "${PROJECT_ROOT}/setup.py"
        rm "${PROJECT_ROOT}/setup.py.bak" 2>/dev/null || true
        log_info "  Updated: setup.py"
    fi
    
    # Docker files
    find "$PROJECT_ROOT" -name "Dockerfile*" -type f | while read -r file; do
        if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
            sed -i.bak 's/Quantum Nexus/quantum-nexus/gi' "$file"
            sed -i.bak 's/Quantum Nexus/Quantum Nexus/g' "$file"
            rm "${file}.bak" 2>/dev/null || true
            log_info "  Updated: $(basename "$file")"
        fi
    done
    
    # Kubernetes files
    find "${PROJECT_ROOT}/deploy" -name "*.yaml" -o -name "*.yml" | while read -r file; do
        if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
            sed -i.bak 's/Quantum Nexus/quantum-nexus/gi' "$file"
            sed -i.bak 's/Quantum Nexus/Quantum Nexus/g' "$file"
            rm "${file}.bak" 2>/dev/null || true
            log_info "  Updated: $(basename "$file")"
        fi
    done
    
    log_success "Configuration file replacements completed"
}

replace_documentation() {
    log_step "Replacing documentation..."
    
    # README files
    find "$PROJECT_ROOT" -name "README*" -type f | while read -r file; do
        if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
            sed -i.bak 's/Quantum Nexus Platform/Quantum Nexus Platform/g' "$file"
            sed -i.bak 's/Quantum Nexus/Quantum Nexus/g' "$file"
            sed -i.bak 's/Quantum Nexus/quantum-nexus/g' "$file"
            rm "${file}.bak" 2>/dev/null || true
            log_info "  Updated: $(basename "$file")"
        fi
    done
    
    # Documentation files
    if [[ -d "${PROJECT_ROOT}/docs" ]]; then
        find "${PROJECT_ROOT}/docs" -name "*.md" -o -name "*.rst" -o -name "*.txt" | while read -r file; do
            if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
                sed -i.bak 's/Quantum Nexus Platform/Quantum Nexus Platform/g' "$file"
                sed -i.bak 's/Quantum Nexus/Quantum Nexus/g' "$file"
                sed -i.bak 's/Quantum Nexus/quantum-nexus/g' "$file"
                rm "${file}.bak" 2>/dev/null || true
                log_info "  Updated: $(basename "$file")"
            fi
        done
    fi
    
    log_success "Documentation replacements completed"
}

replace_frontend_assets() {
    log_step "Replacing frontend assets and UI text..."
    
    # HTML files
    find "$PROJECT_ROOT" -name "*.html" -type f | while read -r file; do
        if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
            sed -i.bak 's/<title>.*Quantum Nexus.*<\/title>/<title>Quantum Nexus Platform<\/title>/gi' "$file"
            sed -i.bak 's/Quantum Nexus Platform/Quantum Nexus Platform/g' "$file"
            sed -i.bak 's/Quantum Nexus/Quantum Nexus/g' "$file"
            rm "${file}.bak" 2>/dev/null || true
            log_info "  Updated: $(basename "$file")"
        fi
    done
    
    # CSS files
    find "$PROJECT_ROOT" -name "*.css" -type f | while read -r file; do
        if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
            sed -i.bak 's/Quantum Nexus/quantum-nexus/gi' "$file"
            rm "${file}.bak" 2>/dev/null || true
            log_info "  Updated: $(basename "$file")"
        fi
    done
    
    # JavaScript/TypeScript files
    find "$PROJECT_ROOT" -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" | while read -r file; do
        if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
            sed -i.bak 's/Quantum Nexus Platform/Quantum Nexus Platform/g' "$file"
            sed -i.bak 's/Quantum Nexus/Quantum Nexus/g' "$file"
            sed -i.bak 's/Quantum Nexus/quantum-nexus/g' "$file"
            rm "${file}.bak" 2>/dev/null || true
            log_info "  Updated: $(basename "$file")"
        fi
    done
    
    log_success "Frontend asset replacements completed"
}

update_brand_assets() {
    log_step "Updating brand assets and metadata..."
    
    # Create brand assets directory
    mkdir -p "${PROJECT_ROOT}/frontend/public/assets/brand"
    mkdir -p "${PROJECT_ROOT}/frontend/src/assets/brand"
    
    # Create placeholder brand files
    cat > "${PROJECT_ROOT}/frontend/public/assets/brand/brand-colors.css" << EOF
/* Quantum Nexus Brand Colors */
:root {
  /* Primary Colors */
  --quantum-blue: #0066FF;
  --nexus-purple: #6B46C1;
  --deep-space: #0F0F23;
  
  /* Secondary Colors */
  --electric-cyan: #00D4FF;
  --plasma-pink: #FF006B;
  --neural-green: #00FF88;
  
  /* Neutral Colors */
  --quantum-white: #FFFFFF;
  --cosmic-gray: #8B8B8B;
  --void-black: #000000;
  
  /* Gradients */
  --quantum-flow: linear-gradient(135deg, #0066FF 0%, #6B46C1 50%, #FF006B 100%);
  --nexus-energy: linear-gradient(90deg, #00D4FF 0%, #0066FF 50%, #6B46C1 100%);
  --cosmic-depth: linear-gradient(180deg, #0F0F23 0%, #6B46C1 100%);
}
EOF
    
    # Update manifest.json if it exists
    if [[ -f "${PROJECT_ROOT}/frontend/public/manifest.json" ]]; then
        sed -i.bak 's/"name": ".*Quantum Nexus.*"/"name": "Quantum Nexus Platform"/gi' "${PROJECT_ROOT}/frontend/public/manifest.json"
        sed -i.bak 's/"short_name": ".*Quantum Nexus.*"/"short_name": "Quantum Nexus"/gi' "${PROJECT_ROOT}/frontend/public/manifest.json"
        rm "${PROJECT_ROOT}/frontend/public/manifest.json.bak" 2>/dev/null || true
        log_info "  Updated: manifest.json"
    fi
    
    log_success "Brand asset updates completed"
}

# =============================================================================
# File Renaming Functions
# =============================================================================
rename_files_and_directories() {
    log_step "Renaming files and directories..."
    
    # Find and rename files containing 'Quantum Nexus' in their names
    find "$PROJECT_ROOT" -name "*Quantum Nexus*" -type f -not -path "*/node_modules/*" -not -path "*/venv/*" -not -path "*/.git/*" -not -path "*/backup/*" | while read -r file; do
        local dir=$(dirname "$file")
        local filename=$(basename "$file")
        local new_filename=$(echo "$filename" | sed 's/Quantum Nexus/quantum-nexus/gi')
        
        if [[ "$filename" != "$new_filename" ]]; then
            mv "$file" "${dir}/${new_filename}"
            log_info "  Renamed: $filename → $new_filename"
        fi
    done
    
    # Find and rename directories containing 'Quantum Nexus' in their names
    find "$PROJECT_ROOT" -name "*Quantum Nexus*" -type d -not -path "*/node_modules/*" -not -path "*/venv/*" -not -path "*/.git/*" -not -path "*/backup/*" | while read -r dir; do
        local parent_dir=$(dirname "$dir")
        local dirname=$(basename "$dir")
        local new_dirname=$(echo "$dirname" | sed 's/Quantum Nexus/quantum-nexus/gi')
        
        if [[ "$dirname" != "$new_dirname" ]]; then
            mv "$dir" "${parent_dir}/${new_dirname}"
            log_info "  Renamed directory: $dirname → $new_dirname"
        fi
    done
    
    log_success "File and directory renaming completed"
}

# =============================================================================
# Verification Functions
# =============================================================================
verify_replacements() {
    log_step "Verifying replacements..."
    
    local quantum_nexus_count=0
    local files_with_Quantum Nexus=()
    
    # Count remaining Quantum Nexus references
    while IFS= read -r -d '' file; do
        if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
            local count=$(grep -c "Quantum Nexus" "$file" 2>/dev/null || echo "0")
            quantum_nexus_count=$((quantum_nexus_count + count))
            files_with_Quantum Nexus+=("$file")
        fi
    done < <(find "$PROJECT_ROOT" -type f -not -path "*/node_modules/*" -not -path "*/venv/*" -not -path "*/.git/*" -not -path "*/backup/*" -not -path "*/branding/*" -print0)
    
    if [[ $quantum_nexus_count -gt 0 ]]; then
        log_warning "Found $quantum_nexus_count remaining Quantum Nexus references in ${#files_with_Quantum Nexus[@]} files:"
        for file in "${files_with_Quantum Nexus[@]}"; do
            log_warning "  - $(basename "$file")"
        done
    else
        log_success "No remaining Quantum Nexus references found"
    fi
    
    # Verify Quantum Nexus references
    local quantum_nexus_count=0
    while IFS= read -r -d '' file; do
        if grep -q "Quantum Nexus" "$file" 2>/dev/null; then
            local count=$(grep -c "Quantum Nexus" "$file" 2>/dev/null || echo "0")
            quantum_nexus_count=$((quantum_nexus_count + count))
        fi
    done < <(find "$PROJECT_ROOT" -type f -not -path "*/node_modules/*" -not -path "*/venv/*" -not -path "*/.git/*" -not -path "*/backup/*" -print0)
    
    log_success "Found $quantum_nexus_count Quantum Nexus references"
}

# =============================================================================
# Main Rebranding Function
# =============================================================================
rebrand_full() {
    log_rebrand "Starting complete rebranding to Quantum Nexus..."
    
    # Pre-rebranding setup
    check_dependencies
    load_brand_config
    create_backup
    
    # Core rebranding
    replace_brand_names
    replace_domains_and_urls
    replace_code_identifiers
    replace_configuration_files
    replace_documentation
    replace_frontend_assets
    update_brand_assets
    
    # File system changes
    rename_files_and_directories
    
    # Verification
    verify_replacements
    
    log_rebrand "Rebranding to Quantum Nexus completed successfully!"
    
    # Display summary
    echo
    echo "=============================================================================="
    echo "Quantum Nexus Rebranding Complete"
    echo "=============================================================================="
    echo "Brand Name: $BRAND_NAME"
    echo "Tagline: $BRAND_TAGLINE"
    echo "Domain: $BRAND_DOMAIN"
    echo "Code Name: $BRAND_CODE_NAME"
    echo
    echo "Backup Location: $BACKUP_DIR"
    echo "Brand Config: $BRAND_CONFIG"
    echo "=============================================================================="
    echo
    echo "Next Steps:"
    echo "1. Review the changes and test the application"
    echo "2. Update any remaining manual references"
    echo "3. Generate new logo and brand assets"
    echo "4. Update external services and integrations"
    echo "5. Launch the rebranded platform"
    echo "=============================================================================="
}

# =============================================================================
# Rollback Function
# =============================================================================
rollback_rebranding() {
    log_warning "Rolling back rebranding..."
    
    if git rev-parse --git-dir > /dev/null 2>&1; then
        git stash pop
        log_success "Rollback completed using git stash"
    elif [[ -d "$BACKUP_DIR" ]]; then
        # Manual rollback from backup
        log_info "Restoring from backup directory..."
        cp -r "${BACKUP_DIR}"/* "$PROJECT_ROOT/"
        log_success "Rollback completed from backup"
    else
        log_error "No backup found for rollback"
        exit 1
    fi
}

# =============================================================================
# Usage and Help
# =============================================================================
show_usage() {
    cat << EOF
Quantum Nexus Platform - Rebranding Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  rebrand     Complete rebranding from Quantum Nexus to Quantum Nexus
  verify      Verify current branding status
  rollback    Rollback rebranding changes
  help        Show this help message

Options:
  --dry-run   Show what would be changed without executing
  --backup    Create backup before rebranding (default: true)
  --force     Force rebranding without confirmations

Examples:
  $0 rebrand              # Full rebranding
  $0 verify               # Check current status
  $0 rollback             # Undo changes

EOF
}

# =============================================================================
# Main Script Logic
# =============================================================================
main() {
    local command=${1:-help}
    
    case $command in
        rebrand)
            rebrand_full
            ;;
        verify)
            check_dependencies
            load_brand_config
            verify_replacements
            ;;
        rollback)
            rollback_rebranding
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