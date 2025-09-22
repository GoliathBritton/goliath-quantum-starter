#!/usr/bin/env pwsh
# Quantum Omniscient™ Platform Deployment Script
# One-command deployment for production-ready quantum intelligence platform

param(
    [string]$Environment = "production",
    [switch]$SkipBuild,
    [switch]$SkipMigrations,
    [switch]$DemoMode,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
🚀 Quantum Omniscient™ Deployment Script

Usage: .\deploy.ps1 [OPTIONS]

Options:
  -Environment     Target environment (production, staging, development) [default: production]
  -SkipBuild      Skip Docker image building
  -SkipMigrations Skip database migrations
  -DemoMode       Deploy with demo data and reduced security
  -Help           Show this help message

Examples:
  .\deploy.ps1                           # Full production deployment
  .\deploy.ps1 -DemoMode                 # Quick demo deployment
  .\deploy.ps1 -Environment staging      # Staging deployment
  .\deploy.ps1 -SkipBuild -SkipMigrations # Quick restart

"@
    exit 0
}

# Configuration
$PROJECT_NAME = "Quantum Omniscient"
$DOCKER_COMPOSE_FILE = "docker-compose.yml"
$ENV_FILE = ".env"
$LOG_FILE = "deployment.log"

# Colors for output
$RED = "`e[31m"
$GREEN = "`e[32m"
$YELLOW = "`e[33m"
$BLUE = "`e[34m"
$PURPLE = "`e[35m"
$CYAN = "`e[36m"
$RESET = "`e[0m"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] [$Level] $Message"
    
    switch ($Level) {
        "ERROR" { Write-Host "${RED}[ERROR] $Message${RESET}" }
        "SUCCESS" { Write-Host "${GREEN}[SUCCESS] $Message${RESET}" }
        "WARNING" { Write-Host "${YELLOW}[WARNING] $Message${RESET}" }
        "INFO" { Write-Host "${BLUE}[INFO] $Message${RESET}" }
        "QUANTUM" { Write-Host "${PURPLE}[QUANTUM] $Message${RESET}" }
        default { Write-Host "$Message" }
    }
    
    Add-Content -Path $LOG_FILE -Value $logEntry
}

function Test-Prerequisites {
    Write-Log "Checking deployment prerequisites..." "INFO"
    
    # Check Docker
    if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
        Write-Log "Docker is not installed or not in PATH" "ERROR"
        return $false
    }
    
    # Check Docker Compose
    if (!(Get-Command docker-compose -ErrorAction SilentlyContinue)) {
        Write-Log "Docker Compose is not installed or not in PATH" "ERROR"
        return $false
    }
    
    # Check if Docker is running
    try {
        docker info | Out-Null
    } catch {
        Write-Log "Docker daemon is not running" "ERROR"
        return $false
    }
    
    Write-Log "All prerequisites satisfied" "SUCCESS"
    return $true
}

function Initialize-Environment {
    Write-Log "Initializing Quantum Omniscient environment..." "QUANTUM"
    
    # Create .env file if it doesn't exist
    if (!(Test-Path $ENV_FILE)) {
        if (Test-Path ".env.example") {
            Copy-Item ".env.example" $ENV_FILE
            Write-Log "Created .env file from template" "SUCCESS"
        } else {
            Write-Log ".env.example not found. Creating minimal .env file" "WARNING"
            @"
APP_NAME=Quantum Omniscient
ENVIRONMENT=$Environment
DATABASE_URL=postgresql://quantum_user:quantum_pass@postgres:5432/quantum_omniscient_db
REDIS_URL=redis://redis:6379
JWT_SECRET=quantum-omniscient-jwt-secret-change-in-production
QUANTUM_OMNISCIENT_MODE=$Environment
"@ | Out-File -FilePath $ENV_FILE -Encoding UTF8
        }
    }
    
    # Create necessary directories
    $directories = @("logs", "data", "backups", "monitoring")
    foreach ($dir in $directories) {
        if (!(Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-Log "Created directory: $dir" "INFO"
        }
    }
    
    Write-Log "Environment initialized successfully" "SUCCESS"
}

function Build-Images {
    if ($SkipBuild) {
        Write-Log "Skipping Docker image build" "WARNING"
        return
    }
    
    Write-Log "Building Quantum Omniscient™ Docker images..." "QUANTUM"
    
    try {
        docker-compose -f $DOCKER_COMPOSE_FILE build --no-cache
        Write-Log "Docker images built successfully" "SUCCESS"
    } catch {
        Write-Log "Failed to build Docker images: $($_.Exception.Message)" "ERROR"
        exit 1
    }
}

function Start-Services {
    Write-Log "Starting Quantum Omniscient™ services..." "QUANTUM"
    
    try {
        # Start infrastructure services first
        docker-compose -f $DOCKER_COMPOSE_FILE up -d postgres redis minio
        Start-Sleep -Seconds 10
        
        # Start monitoring services
        docker-compose -f $DOCKER_COMPOSE_FILE up -d prometheus grafana
        Start-Sleep -Seconds 5
        
        # Start application services
        docker-compose -f $DOCKER_COMPOSE_FILE up -d backend frontend
        
        Write-Log "All services started successfully" "SUCCESS"
    } catch {
        Write-Log "Failed to start services: $($_.Exception.Message)" "ERROR"
        exit 1
    }
}

function Run-Migrations {
    if ($SkipMigrations) {
        Write-Log "Skipping database migrations" "WARNING"
        return
    }
    
    Write-Log "Running database migrations..." "INFO"
    
    # Wait for database to be ready
    Start-Sleep -Seconds 15
    
    try {
        docker-compose -f $DOCKER_COMPOSE_FILE exec -T backend python -m alembic upgrade head
        Write-Log "Database migrations completed" "SUCCESS"
    } catch {
        Write-Log "Database migrations failed: $($_.Exception.Message)" "WARNING"
    }
}

function Setup-DemoData {
    if (!$DemoMode) {
        return
    }
    
    Write-Log "Setting up demo data..." "QUANTUM"
    
    try {
        docker-compose -f $DOCKER_COMPOSE_FILE exec -T backend python scripts/setup_demo_data.py
        Write-Log "Demo data setup completed" "SUCCESS"
    } catch {
        Write-Log "Demo data setup failed: $($_.Exception.Message)" "WARNING"
    }
}

function Test-Deployment {
    Write-Log "Testing deployment health..." "INFO"
    
    $services = @(
        @{Name="Backend API"; URL="http://localhost:8000/health"; Port=8000},
        @{Name="Frontend"; URL="http://localhost:3000"; Port=3000},
        @{Name="Grafana"; URL="http://localhost:3001"; Port=3001},
        @{Name="MinIO"; URL="http://localhost:9001"; Port=9001}
    )
    
    Start-Sleep -Seconds 30  # Wait for services to fully start
    
    foreach ($service in $services) {
        try {
            $response = Invoke-WebRequest -Uri $service.URL -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Log "$($service.Name) is healthy" "SUCCESS"
            } else {
                Write-Log "$($service.Name) returned status $($response.StatusCode)" "WARNING"
            }
        } catch {
            Write-Log "$($service.Name) health check failed" "WARNING"
        }
    }
}

function Show-DeploymentInfo {
    Write-Log "" "INFO"
    Write-Log "🚀 Quantum Omniscient™ Platform Deployment Complete!" "QUANTUM"
    Write-Log "" "INFO"
    Write-Log "📊 Service URLs:" "INFO"
    Write-Log "   Frontend:     http://localhost:3000" "INFO"
    Write-Log "   Backend API:  http://localhost:8000" "INFO"
    Write-Log "   API Docs:     http://localhost:8000/docs" "INFO"
    Write-Log "   Grafana:      http://localhost:3001 (admin/quantum_omniscient_admin)" "INFO"
    Write-Log "   Prometheus:   http://localhost:9090" "INFO"
    Write-Log "   MinIO:        http://localhost:9001 (quantum_admin/quantum_omniscient_2024)" "INFO"
    Write-Log "" "INFO"
    Write-Log "🔮 Quantum Features:" "QUANTUM"
    Write-Log "   • NQBA Framework with Quantum Omniscient™ Engine" "INFO"
    Write-Log "   • 600% Premium Pricing Pyramid" "INFO"
    Write-Log "   • Quantum Black-Box™ Intelligence" "INFO"
    Write-Log "   • Real-time Quantum Analytics" "INFO"
    Write-Log "   • Mystique-driven Decision Engine" "INFO"
    Write-Log "" "INFO"
    Write-Log "📝 Next Steps:" "INFO"
    Write-Log "   1. Configure your Dynex API key in .env" "INFO"
    Write-Log "   2. Set up Stripe payment keys for billing" "INFO"
    Write-Log "   3. Configure SSL certificates for production" "INFO"
    Write-Log "   4. Run: docker-compose logs -f to monitor services" "INFO"
    Write-Log "" "INFO"
    
    if ($DemoMode) {
        Write-Log "🎯 Demo Mode Active - Ready for immediate showcase!" "SUCCESS"
    }
}

function Main {
    Clear-Host
    Write-Host "" -ForegroundColor Purple
    Write-Host "==========================================================" -ForegroundColor Purple
    Write-Host "    QUANTUM OMNISCIENT PLATFORM DEPLOYMENT" -ForegroundColor Purple
    Write-Host "    Quantum foresight for an intelligent economy" -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Purple
    Write-Host ""
    
    Write-Log "Starting deployment for environment: $Environment" "QUANTUM"
    
    # Clear previous log
    if (Test-Path $LOG_FILE) {
        Remove-Item $LOG_FILE -Force
    }
    
    # Deployment steps
    if (!(Test-Prerequisites)) { exit 1 }
    Initialize-Environment
    Build-Images
    Start-Services
    Run-Migrations
    Setup-DemoData
    Test-Deployment
    Show-DeploymentInfo
    
    Write-Log "Deployment completed successfully! 🚀" "SUCCESS"
}

# Execute main function
Main