# FLYFOX AI Platform - Vercel Deployment Script
# PowerShell script for automated deployment

Write-Host "FLYFOX AI Platform - Vercel Deployment" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green

# Check if we're in the correct directory
if (-not (Test-Path "package.json")) {
    Write-Host "Error: package.json not found. Please run this script from the web directory." -ForegroundColor Red
    exit 1
}

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Green
Write-Host "Package.json found" -ForegroundColor Green

# Step 1: Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
try {
    npm install
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to install dependencies: $_" -ForegroundColor Red
    exit 1
}

# Step 2: Build the application
Write-Host "Building application..." -ForegroundColor Yellow
try {
    npm run build
    Write-Host "Build completed successfully" -ForegroundColor Green
} catch {
    Write-Host "Build failed: $_" -ForegroundColor Red
    exit 1
}

# Step 3: Check build output
Write-Host "Checking build output..." -ForegroundColor Yellow
if (Test-Path ".next") {
    Write-Host "Build output directory (.next) created" -ForegroundColor Green
} else {
    Write-Host "Build output directory not found" -ForegroundColor Red
    exit 1
}

# Step 4: Display deployment information
Write-Host ""
Write-Host "DEPLOYMENT READY!" -ForegroundColor Green
Write-Host "====================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Go to https://vercel.com/new" -ForegroundColor White
Write-Host "2. Import repository: GoliathBritton/goliath-quantum-starter" -ForegroundColor White
Write-Host "3. Set root directory: nqba-phase2/web" -ForegroundColor White
Write-Host "4. Click Deploy" -ForegroundColor White
Write-Host ""
Write-Host "Environment Variables to Set:" -ForegroundColor Cyan
Write-Host "NEXT_PUBLIC_API_BASE=https://api.goliathomniedge.com" -ForegroundColor White
Write-Host "NEXT_PUBLIC_FLYFOX_AI_VERSION=2.0.0" -ForegroundColor White
Write-Host "NEXT_PUBLIC_ENHANCED_AGENTS=true" -ForegroundColor White
Write-Host "NEXT_PUBLIC_QUANTUM_ENHANCEMENT=true" -ForegroundColor White
Write-Host ""
Write-Host "Custom Domain: portal.goliathomniedge.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "All enhanced features are ready:" -ForegroundColor Green
Write-Host "   - Advanced Prompt Engineering System" -ForegroundColor White
Write-Host "   - Self-Learning Customer Success System" -ForegroundColor White
Write-Host "   - Agent Enhancement Integration" -ForegroundColor White
Write-Host "   - FLYFOX AI Pillars Integration" -ForegroundColor White
Write-Host ""
Write-Host "Estimated deployment time: 3 minutes" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "Deployment script completed successfully!" -ForegroundColor Green 
