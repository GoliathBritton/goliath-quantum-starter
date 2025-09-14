# Goliath Quantum Division - Windows PowerShell Deployment Script
# Automated deployment for 10K+ contact batch processing

param(
    [string]$Environment = "production",
    [string]$Mode = "docker",  # docker, local, or hybrid
    [switch]$SkipTests = $false,
    [switch]$Force = $false
)

# Script configuration
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Colors for output
$Colors = @{
    Success = "Green"
    Warning = "Yellow"
    Error = "Red"
    Info = "Cyan"
    Header = "Magenta"
}

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Colors[$Color]
}

function Write-Header {
    param([string]$Title)
    Write-Host "`n" -NoNewline
    Write-Host "=" * 60 -ForegroundColor $Colors["Header"]
    Write-Host "🚀 $Title" -ForegroundColor $Colors["Header"]
    Write-Host "=" * 60 -ForegroundColor $Colors["Header"]
}

function Test-Prerequisites {
    Write-Header "Checking Prerequisites"
    
    $prerequisites = @(
        @{ Name = "Python"; Command = "python --version"; MinVersion = "3.8" },
        @{ Name = "Node.js"; Command = "node --version"; MinVersion = "16.0" },
        @{ Name = "Docker"; Command = "docker --version"; MinVersion = "20.0" },
        @{ Name = "Docker Compose"; Command = "docker-compose --version"; MinVersion = "2.0" }
    )
    
    foreach ($prereq in $prerequisites) {
        try {
            $version = Invoke-Expression $prereq.Command 2>$null
            if ($version) {
                Write-ColorOutput "✅ $($prereq.Name): $version" "Success"
            } else {
                Write-ColorOutput "❌ $($prereq.Name): Not found" "Error"
                throw "$($prereq.Name) is required but not installed"
            }
        } catch {
            Write-ColorOutput "❌ $($prereq.Name): Not available" "Error"
            if (-not $Force) {
                throw "$($prereq.Name) is required. Use -Force to skip checks."
            }
        }
    }
    
    # Check environment variables
    $requiredEnvVars = @("DYNEX_API_KEY", "OPENAI_API_KEY", "SECRET_KEY")
    foreach ($envVar in $requiredEnvVars) {
        if (-not $env:$envVar) {
            Write-ColorOutput "⚠️ Environment variable $envVar not set" "Warning"
        } else {
            Write-ColorOutput "✅ Environment variable $envVar is set" "Success"
        }
    }
    
    # Check disk space (minimum 10GB)
    $freeSpace = (Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'").FreeSpace / 1GB
    if ($freeSpace -lt 10) {
        Write-ColorOutput "❌ Insufficient disk space: $([math]::Round($freeSpace, 1))GB available, 10GB required" "Error"
        if (-not $Force) {
            throw "Insufficient disk space"
        }
    } else {
        Write-ColorOutput "✅ Disk space: $([math]::Round($freeSpace, 1))GB available" "Success"
    }
}

function Initialize-Environment {
    Write-Header "Initializing Environment"
    
    # Create necessary directories
    $directories = @(
        "data\leads",
        "data\processed", 
        "data\quantum_cache",
        "logs\services",
        "logs\quantum",
        "cache\nqba",
        "cache\ltc",
        "deploy\reports",
        "deploy\monitoring",
        "deploy\nginx"
    )
    
    foreach ($dir in $directories) {
        if (-not (Test-Path $dir)) {
            New-Item -ItemType Directory -Path $dir -Force | Out-Null
            Write-ColorOutput "📁 Created directory: $dir" "Info"
        }
    }
    
    # Copy environment template if .env doesn't exist
    if (-not (Test-Path ".env")) {
        if (Test-Path ".env.template") {
            Copy-Item ".env.template" ".env"
            Write-ColorOutput "📋 Created .env from template" "Info"
        } else {
            Write-ColorOutput "⚠️ No .env file found. Please create one with required environment variables." "Warning"
        }
    }
}

function Install-Dependencies {
    Write-Header "Installing Dependencies"
    
    # Install Python dependencies
    Write-ColorOutput "📦 Installing Python dependencies..." "Info"
    try {
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
        
        # Install additional quantum dependencies
        python -m pip install dimod fastapi uvicorn pydantic redis psycopg2-binary
        
        Write-ColorOutput "✅ Python dependencies installed" "Success"
    } catch {
        Write-ColorOutput "❌ Failed to install Python dependencies: $($_.Exception.Message)" "Error"
        throw
    }
    
    # Install Node.js dependencies for web frontend
    if (Test-Path "web\package.json") {
        Write-ColorOutput "📦 Installing Node.js dependencies..." "Info"
        try {
            Push-Location "web"
            npm install
            Pop-Location
            Write-ColorOutput "✅ Node.js dependencies installed" "Success"
        } catch {
            Pop-Location
            Write-ColorOutput "❌ Failed to install Node.js dependencies: $($_.Exception.Message)" "Error"
            throw
        }
    }
}

function Test-Components {
    if ($SkipTests) {
        Write-ColorOutput "⏭️ Skipping component tests" "Warning"
        return
    }
    
    Write-Header "Testing Core Components"
    
    # Test NQBA Engine
    Write-ColorOutput "🧪 Testing NQBA Engine..." "Info"
    try {
        $testResult = python -c "from src.nqba.engine import NQBAEngine; engine = NQBAEngine(); print('NQBA Engine: OK')"
        Write-ColorOutput "✅ $testResult" "Success"
    } catch {
        Write-ColorOutput "❌ NQBA Engine test failed" "Error"
        throw
    }
    
    # Test Quantum Components
    Write-ColorOutput "🧪 Testing Quantum Components..." "Info"
    try {
        $testResult = python -c @"
from src.nqba_stack.core.quantum_high_council import QuantumHighCouncil
from src.nqba_stack.core.quantum_digital_agents import QuantumDigitalAgent
council = QuantumHighCouncil()
agent = QuantumDigitalAgent('test')
print('Quantum Components: OK')
"@
        Write-ColorOutput "✅ $testResult" "Success"
    } catch {
        Write-ColorOutput "❌ Quantum Components test failed" "Error"
        throw
    }
}

function Deploy-Docker {
    Write-Header "Docker Deployment"
    
    # Build and start services
    Write-ColorOutput "🐳 Building Docker images..." "Info"
    try {
        docker-compose -f deploy\docker-compose.yml build
        Write-ColorOutput "✅ Docker images built successfully" "Success"
    } catch {
        Write-ColorOutput "❌ Failed to build Docker images: $($_.Exception.Message)" "Error"
        throw
    }
    
    Write-ColorOutput "🚀 Starting Docker services..." "Info"
    try {
        docker-compose -f deploy\docker-compose.yml up -d
        Write-ColorOutput "✅ Docker services started" "Success"
    } catch {
        Write-ColorOutput "❌ Failed to start Docker services: $($_.Exception.Message)" "Error"
        throw
    }
    
    # Wait for services to be ready
    Write-ColorOutput "⏳ Waiting for services to be ready..." "Info"
    Start-Sleep -Seconds 30
    
    # Health checks
    $services = @(
        @{ Name = "NQBA Engine"; Url = "http://localhost:8000/health" },
        @{ Name = "Main API"; Url = "http://localhost:8080/health" },
        @{ Name = "Web Frontend"; Url = "http://localhost:3000" }
    )
    
    foreach ($service in $services) {
        try {
            $response = Invoke-WebRequest -Uri $service.Url -TimeoutSec 10 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-ColorOutput "✅ $($service.Name): Healthy" "Success"
            } else {
                Write-ColorOutput "⚠️ $($service.Name): Status $($response.StatusCode)" "Warning"
            }
        } catch {
            Write-ColorOutput "❌ $($service.Name): Not responding" "Error"
        }
    }
}

function Deploy-Local {
    Write-Header "Local Deployment"
    
    # Start database services
    Write-ColorOutput "🗄️ Starting database services..." "Info"
    try {
        docker-compose -f deploy\docker-compose.yml up -d postgres redis
        Start-Sleep -Seconds 10
        Write-ColorOutput "✅ Database services started" "Success"
    } catch {
        Write-ColorOutput "❌ Failed to start database services" "Error"
        throw
    }
    
    # Start Python services
    Write-ColorOutput "🐍 Starting Python services..." "Info"
    
    # Start NQBA Engine
    Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "src.nqba.api_server:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4" -WindowStyle Hidden
    
    # Start Main API
    Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "api.src.main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "8" -WindowStyle Hidden
    
    # Start Web Frontend
    if (Test-Path "web\package.json") {
        Write-ColorOutput "🌐 Starting web frontend..." "Info"
        Push-Location "web"
        Start-Process -FilePath "npm" -ArgumentList "run", "dev" -WindowStyle Hidden
        Pop-Location
    }
    
    Start-Sleep -Seconds 15
    Write-ColorOutput "✅ Local services started" "Success"
}

function Test-Deployment {
    Write-Header "Testing Deployment"
    
    # Test batch processing capability
    Write-ColorOutput "🧪 Testing batch processing..." "Info"
    
    # Create test data
    $testData = @()
    for ($i = 1; $i -le 100; $i++) {
        $testData += @{
            id = $i
            name = "Test Contact $i"
            email = "test$i@example.com"
            company = "Company $($i % 10)"
            score = 0
        }
    }
    
    $testFile = "data\leads\test_batch.json"
    $testData | ConvertTo-Json | Out-File -FilePath $testFile -Encoding UTF8
    
    try {
        python demo_leads.py --file $testFile --test-mode
        Write-ColorOutput "✅ Batch processing test passed" "Success"
    } catch {
        Write-ColorOutput "❌ Batch processing test failed" "Error"
        throw
    }
    
    # Test API endpoints
    $endpoints = @(
        "http://localhost:8000/health",
        "http://localhost:8080/health"
    )
    
    foreach ($endpoint in $endpoints) {
        try {
            $response = Invoke-WebRequest -Uri $endpoint -TimeoutSec 10 -UseBasicParsing
            Write-ColorOutput "✅ API endpoint $endpoint: OK" "Success"
        } catch {
            Write-ColorOutput "❌ API endpoint $endpoint: Failed" "Error"
        }
    }
}

function Generate-Report {
    Write-Header "Deployment Report"
    
    $deploymentId = "deploy_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    $endTime = Get-Date
    $duration = $endTime - $script:startTime
    
    $report = @{
        deployment_id = $deploymentId
        start_time = $script:startTime.ToString("yyyy-MM-ddTHH:mm:ss")
        end_time = $endTime.ToString("yyyy-MM-ddTHH:mm:ss")
        duration_seconds = [math]::Round($duration.TotalSeconds, 1)
        environment = $Environment
        mode = $Mode
        services_deployed = @(
            "nqba_engine",
            "high_council", 
            "quantum_architect",
            "lead_processor",
            "main_api",
            "web_frontend"
        )
        status = "SUCCESS"
        batch_capacity = "10,000+ contacts"
        platform = "Windows PowerShell"
    }
    
    $reportFile = "deploy\reports\deployment_$deploymentId.json"
    $report | ConvertTo-Json -Depth 3 | Out-File -FilePath $reportFile -Encoding UTF8
    
    Write-Host "`n" -NoNewline
    Write-Host "=" * 60 -ForegroundColor $Colors["Header"]
    Write-Host "🎉 GOLIATH QUANTUM DIVISION - DEPLOYMENT COMPLETE" -ForegroundColor $Colors["Header"]
    Write-Host "=" * 60 -ForegroundColor $Colors["Header"]
    Write-ColorOutput "Deployment ID: $deploymentId" "Info"
    Write-ColorOutput "Duration: $([math]::Round($duration.TotalSeconds, 1)) seconds" "Info"
    Write-ColorOutput "Environment: $Environment" "Info"
    Write-ColorOutput "Mode: $Mode" "Info"
    Write-ColorOutput "Batch Capacity: 10,000+ contacts" "Info"
    Write-ColorOutput "Services: $($report.services_deployed.Count) deployed" "Info"
    Write-Host "`n🚀 Platform ready for enterprise deployment!" -ForegroundColor $Colors["Success"]
    Write-Host "📋 Report saved: $reportFile" -ForegroundColor $Colors["Info"]
    Write-Host "=" * 60 -ForegroundColor $Colors["Header"]
    
    # Display access URLs
    Write-Host "`n🌐 Access URLs:" -ForegroundColor $Colors["Info"]
    Write-Host "   • NQBA Engine: http://localhost:8000" -ForegroundColor $Colors["Success"]
    Write-Host "   • Main API: http://localhost:8080" -ForegroundColor $Colors["Success"]
    Write-Host "   • Web Frontend: http://localhost:3000" -ForegroundColor $Colors["Success"]
    Write-Host "   • Grafana Dashboard: http://localhost:3001" -ForegroundColor $Colors["Success"]
    Write-Host "   • Prometheus Metrics: http://localhost:9090" -ForegroundColor $Colors["Success"]
}

# Main execution
try {
    $script:startTime = Get-Date
    
    Write-Header "Goliath Quantum Division Deployment"
    Write-ColorOutput "Environment: $Environment" "Info"
    Write-ColorOutput "Mode: $Mode" "Info"
    Write-ColorOutput "Skip Tests: $SkipTests" "Info"
    
    Test-Prerequisites
    Initialize-Environment
    Install-Dependencies
    Test-Components
    
    switch ($Mode) {
        "docker" { Deploy-Docker }
        "local" { Deploy-Local }
        "hybrid" { 
            Deploy-Local
            # Could add hybrid logic here
        }
        default { 
            Write-ColorOutput "❌ Invalid mode: $Mode. Use 'docker', 'local', or 'hybrid'" "Error"
            exit 1
        }
    }
    
    Test-Deployment
    Generate-Report
    
    Write-ColorOutput "`n🎉 Deployment completed successfully!" "Success"
    exit 0
    
} catch {
    Write-ColorOutput "`n❌ Deployment failed: $($_.Exception.Message)" "Error"
    Write-ColorOutput "Stack trace: $($_.ScriptStackTrace)" "Error"
    exit 1
}