#!/bin/bash
# Quantum Nexus Platform - UI Assets Update Script
# Generate modern branding elements, logos, gradients, and dark-mode polish

set -euo pipefail

# =============================================================================
# Configuration
# =============================================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
ASSETS_DIR="${PROJECT_ROOT}/frontend/public/assets"
SRC_ASSETS_DIR="${PROJECT_ROOT}/frontend/src/assets"
BRAND_DIR="${PROJECT_ROOT}/branding"
BRAND_CONFIG="${BRAND_DIR}/quantum-nexus-brand.json"

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

log_ui() {
    echo -e "${CYAN}[UI]${NC} $1"
}

# =============================================================================
# Setup Functions
# =============================================================================
setup_directories() {
    log_step "Setting up asset directories..."
    
    # Create directory structure
    mkdir -p "${ASSETS_DIR}/brand"
    mkdir -p "${ASSETS_DIR}/icons"
    mkdir -p "${ASSETS_DIR}/logos"
    mkdir -p "${ASSETS_DIR}/backgrounds"
    mkdir -p "${SRC_ASSETS_DIR}/brand"
    mkdir -p "${SRC_ASSETS_DIR}/icons"
    mkdir -p "${SRC_ASSETS_DIR}/styles"
    mkdir -p "${SRC_ASSETS_DIR}/components"
    
    log_success "Asset directories created"
}

load_brand_config() {
    log_step "Loading brand configuration..."
    
    if [[ ! -f "$BRAND_CONFIG" ]]; then
        log_error "Brand configuration file not found: $BRAND_CONFIG"
        exit 1
    fi
    
    log_success "Brand configuration loaded"
}

# =============================================================================
# SVG Logo Generation
# =============================================================================
generate_quantum_nexus_logo() {
    log_step "Generating Quantum Nexus logo variations..."
    
    # Main logo - Quantum Nexus with quantum circuit design
    cat > "${ASSETS_DIR}/logos/quantum-nexus-logo.svg" << 'EOF'
<svg width="300" height="80" viewBox="0 0 300 80" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="quantumGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0066FF;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#6B46C1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF006B;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="nexusGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#00D4FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0066FF;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge> 
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Quantum Circuit Background -->
  <g opacity="0.3">
    <circle cx="20" cy="25" r="2" fill="#00D4FF"/>
    <circle cx="40" cy="35" r="2" fill="#00D4FF"/>
    <circle cx="60" cy="20" r="2" fill="#00D4FF"/>
    <line x1="20" y1="25" x2="40" y2="35" stroke="#00D4FF" stroke-width="1"/>
    <line x1="40" y1="35" x2="60" y2="20" stroke="#00D4FF" stroke-width="1"/>
    
    <circle cx="240" cy="55" r="2" fill="#FF006B"/>
    <circle cx="260" cy="45" r="2" fill="#FF006B"/>
    <circle cx="280" cy="60" r="2" fill="#FF006B"/>
    <line x1="240" y1="55" x2="260" y2="45" stroke="#FF006B" stroke-width="1"/>
    <line x1="260" y1="45" x2="280" y2="60" stroke="#FF006B" stroke-width="1"/>
  </g>
  
  <!-- Main Logo Text -->
  <text x="20" y="45" font-family="Arial, sans-serif" font-size="24" font-weight="bold" fill="url(#quantumGradient)" filter="url(#glow)">QUANTUM</text>
  <text x="180" y="45" font-family="Arial, sans-serif" font-size="24" font-weight="300" fill="url(#nexusGradient)">NEXUS</text>
  
  <!-- Tagline -->
  <text x="20" y="65" font-family="Arial, sans-serif" font-size="10" fill="#8B8B8B">Quantum-First • AGI-Ready • Shockwave-Level</text>
</svg>
EOF
    
    # Icon version - Simplified for small sizes
    cat > "${ASSETS_DIR}/icons/quantum-nexus-icon.svg" << 'EOF'
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="iconGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0066FF;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#6B46C1;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF006B;stop-opacity:1" />
    </linearGradient>
    <filter id="iconGlow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge> 
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Quantum Circuit Design -->
  <g fill="url(#iconGradient)" filter="url(#iconGlow)">
    <!-- Central Nexus -->
    <circle cx="32" cy="32" r="8" fill="url(#iconGradient)" opacity="0.8"/>
    
    <!-- Quantum Nodes -->
    <circle cx="16" cy="16" r="4" fill="#00D4FF"/>
    <circle cx="48" cy="16" r="4" fill="#00D4FF"/>
    <circle cx="16" cy="48" r="4" fill="#FF006B"/>
    <circle cx="48" cy="48" r="4" fill="#FF006B"/>
    
    <!-- Connections -->
    <line x1="16" y1="16" x2="32" y2="32" stroke="#00D4FF" stroke-width="2" opacity="0.7"/>
    <line x1="48" y1="16" x2="32" y2="32" stroke="#00D4FF" stroke-width="2" opacity="0.7"/>
    <line x1="16" y1="48" x2="32" y2="32" stroke="#FF006B" stroke-width="2" opacity="0.7"/>
    <line x1="48" y1="48" x2="32" y2="32" stroke="#FF006B" stroke-width="2" opacity="0.7"/>
    
    <!-- Quantum Flow -->
    <path d="M 8 32 Q 20 20 32 32 Q 44 44 56 32" stroke="#6B46C1" stroke-width="2" fill="none" opacity="0.6"/>
  </g>
  
  <!-- Q Symbol -->
  <text x="32" y="38" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="white" text-anchor="middle">Q</text>
</svg>
EOF
    
    # Favicon version
    cat > "${ASSETS_DIR}/icons/favicon.svg" << 'EOF'
<svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="faviconGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0066FF;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#6B46C1;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Simple Q with quantum dots -->
  <circle cx="16" cy="16" r="12" fill="url(#faviconGradient)"/>
  <circle cx="16" cy="16" r="8" fill="none" stroke="white" stroke-width="2"/>
  <circle cx="20" cy="20" r="2" fill="white"/>
  <text x="16" y="20" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="white" text-anchor="middle">Q</text>
</svg>
EOF
    
    log_success "Quantum Nexus logos generated"
}

generate_background_assets() {
    log_step "Generating background assets..."
    
    # Quantum field background
    cat > "${ASSETS_DIR}/backgrounds/quantum-field.svg" << 'EOF'
<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="quantumField" cx="50%" cy="50%" r="50%">
      <stop offset="0%" style="stop-color:#0F0F23;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#1a1a3a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#000000;stop-opacity:1" />
    </radialGradient>
    <filter id="quantumGlow">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge> 
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- Base gradient -->
  <rect width="1920" height="1080" fill="url(#quantumField)"/>
  
  <!-- Quantum particles -->
  <g opacity="0.6" filter="url(#quantumGlow)">
    <circle cx="200" cy="200" r="3" fill="#00D4FF" opacity="0.8">
      <animate attributeName="opacity" values="0.3;0.8;0.3" dur="3s" repeatCount="indefinite"/>
    </circle>
    <circle cx="800" cy="300" r="2" fill="#0066FF" opacity="0.6">
      <animate attributeName="opacity" values="0.2;0.6;0.2" dur="4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1400" cy="500" r="4" fill="#6B46C1" opacity="0.7">
      <animate attributeName="opacity" values="0.4;0.7;0.4" dur="2.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="600" cy="700" r="2" fill="#FF006B" opacity="0.5">
      <animate attributeName="opacity" values="0.2;0.5;0.2" dur="3.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1200" cy="800" r="3" fill="#00FF88" opacity="0.6">
      <animate attributeName="opacity" values="0.3;0.6;0.3" dur="4.5s" repeatCount="indefinite"/>
    </circle>
  </g>
  
  <!-- Quantum connections -->
  <g opacity="0.3" stroke-width="1">
    <line x1="200" y1="200" x2="800" y2="300" stroke="#00D4FF" opacity="0.4"/>
    <line x1="800" y1="300" x2="1400" y2="500" stroke="#0066FF" opacity="0.3"/>
    <line x1="600" y1="700" x2="1200" y2="800" stroke="#FF006B" opacity="0.4"/>
  </g>
</svg>
EOF
    
    log_success "Background assets generated"
}

# =============================================================================
# CSS Generation
# =============================================================================
generate_brand_css() {
    log_step "Generating brand CSS variables and utilities..."
    
    cat > "${SRC_ASSETS_DIR}/styles/brand-variables.css" << 'EOF'
/* Quantum Nexus Brand Variables */
:root {
  /* === PRIMARY BRAND COLORS === */
  --quantum-blue: #0066FF;
  --nexus-purple: #6B46C1;
  --deep-space: #0F0F23;
  
  /* === SECONDARY COLORS === */
  --electric-cyan: #00D4FF;
  --plasma-pink: #FF006B;
  --neural-green: #00FF88;
  --quantum-gold: #FFD700;
  
  /* === NEUTRAL PALETTE === */
  --quantum-white: #FFFFFF;
  --cosmic-gray-100: #F8F9FA;
  --cosmic-gray-200: #E9ECEF;
  --cosmic-gray-300: #DEE2E6;
  --cosmic-gray-400: #CED4DA;
  --cosmic-gray-500: #8B8B8B;
  --cosmic-gray-600: #6C757D;
  --cosmic-gray-700: #495057;
  --cosmic-gray-800: #343A40;
  --cosmic-gray-900: #212529;
  --void-black: #000000;
  
  /* === DARK MODE COLORS === */
  --dark-bg-primary: #0F0F23;
  --dark-bg-secondary: #1a1a3a;
  --dark-bg-tertiary: #2d2d5a;
  --dark-text-primary: #FFFFFF;
  --dark-text-secondary: #B8BCC8;
  --dark-text-muted: #8B8B8B;
  --dark-border: #3d3d6a;
  --dark-hover: #4a4a7a;
  
  /* === LIGHT MODE COLORS === */
  --light-bg-primary: #FFFFFF;
  --light-bg-secondary: #F8F9FA;
  --light-bg-tertiary: #E9ECEF;
  --light-text-primary: #212529;
  --light-text-secondary: #495057;
  --light-text-muted: #6C757D;
  --light-border: #DEE2E6;
  --light-hover: #E9ECEF;
  
  /* === GRADIENTS === */
  --quantum-flow: linear-gradient(135deg, #0066FF 0%, #6B46C1 50%, #FF006B 100%);
  --nexus-energy: linear-gradient(90deg, #00D4FF 0%, #0066FF 50%, #6B46C1 100%);
  --cosmic-depth: linear-gradient(180deg, #0F0F23 0%, #6B46C1 100%);
  --neural-pulse: linear-gradient(45deg, #00FF88 0%, #00D4FF 100%);
  --plasma-burst: linear-gradient(135deg, #FF006B 0%, #FFD700 100%);
  --quantum-shimmer: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.2) 50%, transparent 100%);
  
  /* === SHADOWS === */
  --quantum-shadow-sm: 0 2px 4px rgba(0, 102, 255, 0.1);
  --quantum-shadow-md: 0 4px 8px rgba(0, 102, 255, 0.15);
  --quantum-shadow-lg: 0 8px 16px rgba(0, 102, 255, 0.2);
  --quantum-shadow-xl: 0 16px 32px rgba(0, 102, 255, 0.25);
  --nexus-glow: 0 0 20px rgba(107, 70, 193, 0.3);
  --plasma-glow: 0 0 30px rgba(255, 0, 107, 0.4);
  
  /* === TYPOGRAPHY === */
  --font-primary: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
  --font-display: 'Space Grotesk', 'Inter', sans-serif;
  
  /* === SPACING === */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2rem;
  --space-2xl: 3rem;
  --space-3xl: 4rem;
  
  /* === BORDER RADIUS === */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
  --radius-full: 9999px;
  
  /* === TRANSITIONS === */
  --transition-fast: 150ms ease-in-out;
  --transition-normal: 250ms ease-in-out;
  --transition-slow: 350ms ease-in-out;
  --transition-quantum: 300ms cubic-bezier(0.4, 0, 0.2, 1);
  
  /* === Z-INDEX === */
  --z-dropdown: 1000;
  --z-sticky: 1020;
  --z-fixed: 1030;
  --z-modal-backdrop: 1040;
  --z-modal: 1050;
  --z-popover: 1060;
  --z-tooltip: 1070;
  --z-toast: 1080;
}

/* === THEME SWITCHING === */
[data-theme="light"] {
  --bg-primary: var(--light-bg-primary);
  --bg-secondary: var(--light-bg-secondary);
  --bg-tertiary: var(--light-bg-tertiary);
  --text-primary: var(--light-text-primary);
  --text-secondary: var(--light-text-secondary);
  --text-muted: var(--light-text-muted);
  --border-color: var(--light-border);
  --hover-color: var(--light-hover);
}

[data-theme="dark"] {
  --bg-primary: var(--dark-bg-primary);
  --bg-secondary: var(--dark-bg-secondary);
  --bg-tertiary: var(--dark-bg-tertiary);
  --text-primary: var(--dark-text-primary);
  --text-secondary: var(--dark-text-secondary);
  --text-muted: var(--dark-text-muted);
  --border-color: var(--dark-border);
  --hover-color: var(--dark-hover);
}

/* === AUTO THEME DETECTION === */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme]) {
    --bg-primary: var(--dark-bg-primary);
    --bg-secondary: var(--dark-bg-secondary);
    --bg-tertiary: var(--dark-bg-tertiary);
    --text-primary: var(--dark-text-primary);
    --text-secondary: var(--dark-text-secondary);
    --text-muted: var(--dark-text-muted);
    --border-color: var(--dark-border);
    --hover-color: var(--dark-hover);
  }
}

@media (prefers-color-scheme: light) {
  :root:not([data-theme]) {
    --bg-primary: var(--light-bg-primary);
    --bg-secondary: var(--light-bg-secondary);
    --bg-tertiary: var(--light-bg-tertiary);
    --text-primary: var(--light-text-primary);
    --text-secondary: var(--light-text-secondary);
    --text-muted: var(--light-text-muted);
    --border-color: var(--light-border);
    --hover-color: var(--light-hover);
  }
}
EOF
    
    log_success "Brand CSS generated"
}

# =============================================================================
# Main Function
# =============================================================================
main() {
    log_ui "Starting Quantum Nexus UI assets update..."
    
    setup_directories
    load_brand_config
    
    generate_quantum_nexus_logo
    generate_background_assets
    generate_brand_css
    
    log_ui "UI assets update completed successfully!"
    
    echo
    echo "=============================================================================="
    echo "Quantum Nexus UI Assets Generated"
    echo "=============================================================================="
    echo "✓ SVG logos and icons created"
    echo "✓ Brand CSS variables and components generated"
    echo "✓ Background assets and animations ready"
    echo
    echo "Assets Location: $ASSETS_DIR"
    echo "Source Assets: $SRC_ASSETS_DIR"
    echo "=============================================================================="
    echo
    echo "Next Steps:"
    echo "1. Import the CSS files in your main application"
    echo "2. Test the branding elements"
    echo "3. Customize colors and animations as needed"
    echo "=============================================================================="
}

# Run main function
main "$@"