# Quantum Omniscient™ Quick Demo Deployment
# This script starts a development server without Docker for immediate demo

param(
    [switch]$Production = $false
)

# Colors for output
$GREEN = "`e[32m"
$BLUE = "`e[34m"
$PURPLE = "`e[35m"
$CYAN = "`e[36m"
$RESET = "`e[0m"

function Write-Status {
    param([string]$Message, [string]$Color = $BLUE)
    Write-Host "${Color}[QUANTUM] $Message${RESET}"
}

Clear-Host
Write-Host "" -ForegroundColor Purple
Write-Host "==========================================================" -ForegroundColor Purple
Write-Host "    QUANTUM OMNISCIENT QUICK DEMO DEPLOYMENT" -ForegroundColor Purple
Write-Host "    Quantum foresight for an intelligent economy" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Purple
Write-Host ""

Write-Status "Starting Quantum Omniscient development server..." $PURPLE

# Check if Python virtual environment exists
if (Test-Path ".venv") {
    Write-Status "Activating Python virtual environment..." $BLUE
    & ".venv\Scripts\Activate.ps1"
} else {
    Write-Status "Creating Python virtual environment..." $BLUE
    python -m venv .venv
    & ".venv\Scripts\Activate.ps1"
    Write-Status "Installing Python dependencies..." $BLUE
    pip install -r requirements.txt
}

# Install Node.js dependencies if package.json exists
if (Test-Path "package.json") {
    Write-Status "Installing Node.js dependencies..." $BLUE
    npm install
}

# Create .env file for development
if (!(Test-Path ".env")) {
    Write-Status "Creating development environment file..." $BLUE
    @"
APP_NAME=Quantum Omniscient
ENVIRONMENT=development
DATABASE_URL=sqlite:///./quantum_omniscient.db
REDIS_URL=redis://localhost:6379
JWT_SECRET=dev-secret-change-in-production
QUANTUM_OMNISCIENT_MODE=development
PORT=8000
FRONTEND_PORT=3000
"@ | Out-File -FilePath ".env" -Encoding UTF8
}

Write-Status "Environment configured successfully!" $GREEN
Write-Host ""
Write-Host "${CYAN}=== QUANTUM OMNISCIENT DEMO READY ===${RESET}" 
Write-Host ""
Write-Host "${GREEN}Backend API:${RESET} http://localhost:8000"
Write-Host "${GREEN}Frontend:${RESET} http://localhost:3000"
Write-Host "${GREEN}Pricing Demo:${RESET} http://localhost:3000/pricing"
Write-Host ""
Write-Host "${PURPLE}To start the servers:${RESET}"
Write-Host "  Backend: ${CYAN}uvicorn main:app --reload --port 8000${RESET}"
Write-Host "  Frontend: ${CYAN}npm run dev${RESET}"
Write-Host ""
Write-Host "${PURPLE}Press Ctrl+C to stop servers${RESET}"
Write-Host ""

# Start backend server in background if main.py exists
if (Test-Path "main.py") {
    Write-Status "Starting FastAPI backend server..." $BLUE
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '.venv\Scripts\Activate.ps1'; uvicorn main:app --reload --port 8000"
    Start-Sleep -Seconds 3
}

# Start frontend server if package.json exists
if (Test-Path "package.json") {
    Write-Status "Starting Next.js frontend server..." $BLUE
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm run dev"
    Start-Sleep -Seconds 5
}

Write-Status "Quantum Omniscient demo deployment complete!" $GREEN
Write-Host ""
Write-Host "${CYAN}Visit http://localhost:3000 to see your Quantum Omniscient platform!${RESET}"
Write-Host ""