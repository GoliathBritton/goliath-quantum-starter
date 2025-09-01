#!/bin/bash

# Q-Sales Division™ Partner Portal Deployment Script
# This script sets up and deploys the complete portal system

set -e

echo "🚀 Q-Sales Division™ Partner Portal Deployment"
echo "=============================================="
echo "Powered by Dynex Quantum Computing (410x Performance)"
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
    print_status "Checking prerequisites..."
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 18+ first."
        exit 1
    fi
    
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        print_error "Node.js version 18+ is required. Current version: $(node --version)"
        exit 1
    fi
    
    print_success "Node.js $(node --version) ✓"
    
    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed."
        exit 1
    fi
    
    print_success "npm $(npm --version) ✓"
    
    # Check if we're in the right directory
    if [ ! -f "package.json" ]; then
        print_error "package.json not found. Please run this script from the project root."
        exit 1
    fi
    
    print_success "Project structure ✓"
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    if [ -d "node_modules" ]; then
        print_warning "node_modules already exists. Removing for clean install..."
        rm -rf node_modules
    fi
    
    npm install
    
    if [ $? -eq 0 ]; then
        print_success "Dependencies installed successfully ✓"
    else
        print_error "Failed to install dependencies"
        exit 1
    fi
}

# Setup environment
setup_environment() {
    print_status "Setting up environment..."
    
    if [ ! -f ".env.local" ]; then
        if [ -f ".env.example" ]; then
            cp .env.example .env.local
            print_warning "Created .env.local from .env.example"
            print_warning "Please edit .env.local with your actual configuration"
        else
            print_warning ".env.example not found. Creating basic .env.local..."
            cat > .env.local << EOF
# Q-Sales Division™ Partner Portal Environment Variables
# Edit these values with your actual configuration

# Stripe Configuration
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# NextAuth Configuration
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_nextauth_secret_here

# NQBA MCP Integration
NQBA_MCP_ENDPOINT=http://localhost:8000/mcp
NQBA_API_KEY=your_nqba_api_key_here

# Goliath Business Configuration
GOLIATH_PORTAL_URL=https://portal.goliath.com
FLYFOX_AI_URL=https://app.flyfoxai.io
SIGMA_SELECT_URL=https://sigma-select.com
EOF
        fi
    else
        print_warning ".env.local already exists. Please ensure it's configured correctly."
    fi
    
    print_success "Environment setup complete ✓"
}

# Build the project
build_project() {
    print_status "Building the project..."
    
    npm run build
    
    if [ $? -eq 0 ]; then
        print_success "Project built successfully ✓"
    else
        print_error "Build failed"
        exit 1
    fi
}

# Start the development server
start_dev_server() {
    print_status "Starting development server..."
    
    print_success "🚀 Q-Sales Division™ Partner Portal is starting up!"
    echo ""
    echo "📍 Access your portal at: http://localhost:3000"
    echo "🔑 Default routes:"
    echo "   • Home: http://localhost:3000"
    echo "   • Packages: http://localhost:3000/packages"
    echo "   • Contacts: http://localhost:3000/contacts"
    echo "   • Sales Pods: http://localhost:3000/pods"
    echo "   • Login: http://localhost:3000/auth/login"
    echo "   • Register: http://localhost:3000/auth/register"
    echo ""
    echo "⚡ Powered by Dynex Quantum Computing (410x Performance)"
    echo "🎯 Ready to deploy your autonomous sales division!"
    echo ""
    echo "Press Ctrl+C to stop the server"
    echo ""
    
    npm run dev
}

# Main deployment function
main() {
    echo "🏗️  Starting deployment process..."
    echo ""
    
    check_prerequisites
    install_dependencies
    setup_environment
    build_project
    
    echo ""
    print_success "Deployment completed successfully! 🎉"
    echo ""
    
    read -p "Would you like to start the development server now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_dev_server
    else
        echo ""
        print_status "To start the server later, run: npm run dev"
        echo ""
        print_success "Q-Sales Division™ Partner Portal is ready for deployment! 🚀"
    fi
}

# Run main function
main "$@"
