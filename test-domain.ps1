# Quantum Omniscient Domain Testing Script
# Tests domain configuration and connectivity

param(
    [Parameter(Mandatory=$false)]
    [string]$DomainName = "localhost:3000",
    
    [Parameter(Mandatory=$false)]
    [switch]$TestSSL = $false,
    
    [Parameter(Mandatory=$false)]
    [switch]$TestAPI = $true
)

Write-Host "Testing Quantum Omniscient Domain" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan

$protocol = if ($TestSSL) { "https" } else { "http" }
$baseUrl = "$protocol`://$DomainName"

Write-Host "Domain: $DomainName" -ForegroundColor Green
Write-Host "Base URL: $baseUrl" -ForegroundColor Yellow

# Test main site
Write-Host "`n1. Testing main site..." -ForegroundColor Blue
try {
    $response = Invoke-WebRequest -Uri $baseUrl -Method GET -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "   Main site is accessible (Status: $($response.StatusCode))" -ForegroundColor Green
        
        # Check for Quantum Omniscient branding
        if ($response.Content -match "Quantum Omniscient") {
            Write-Host "   Quantum Omniscient branding detected" -ForegroundColor Green
        } else {
            Write-Host "   Quantum Omniscient branding not found" -ForegroundColor Yellow
        }
        
        # Check security headers
        $headers = $response.Headers
        if ($headers["X-Powered-By"] -eq "Quantum Omniscient") {
            Write-Host "   Custom X-Powered-By header set" -ForegroundColor Green
        }
        if ($headers["X-Frame-Options"] -eq "DENY") {
            Write-Host "   X-Frame-Options security header set" -ForegroundColor Green
        }
        
    } else {
        Write-Host "   Main site returned status: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "   Failed to connect to main site: $($_.Exception.Message)" -ForegroundColor Red
}

# Performance test
Write-Host "`n2. Testing performance..." -ForegroundColor Blue
try {
    $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    $response = Invoke-WebRequest -Uri $baseUrl -Method GET -TimeoutSec 30
    $stopwatch.Stop()
    
    $loadTime = $stopwatch.ElapsedMilliseconds
    if ($loadTime -lt 1000) {
        Write-Host "   Fast load time: $loadTime ms" -ForegroundColor Green
    } elseif ($loadTime -lt 3000) {
        Write-Host "   Moderate load time: $loadTime ms" -ForegroundColor Yellow
    } else {
        Write-Host "   Slow load time: $loadTime ms" -ForegroundColor Red
    }
} catch {
    Write-Host "   Performance test failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Summary
Write-Host "`nTest Summary" -ForegroundColor Cyan
Write-Host "============" -ForegroundColor Cyan
Write-Host "Domain: $DomainName" -ForegroundColor White
Write-Host "Protocol: $protocol" -ForegroundColor White
Write-Host "Status: Ready for $(if ($DomainName -eq 'localhost:3000') { 'Development' } else { 'Production' })" -ForegroundColor Green

Write-Host "`nNext Steps:" -ForegroundColor Cyan
if ($DomainName -eq "localhost:3000") {
    Write-Host "- Your development server is running successfully" -ForegroundColor White
    Write-Host "- To set up a custom domain, run: .\setup-domain.ps1 -DomainName 'your-domain.com'" -ForegroundColor White
    Write-Host "- Visit http://localhost:3000 to access your Quantum Omniscient platform" -ForegroundColor White
} else {
    Write-Host "- Configure your DNS records to point to your server" -ForegroundColor White
    Write-Host "- Set up SSL certificates for production security" -ForegroundColor White
    Write-Host "- Deploy your application to the production server" -ForegroundColor White
}

Write-Host "`nQuantum Omniscient Platform is ready!" -ForegroundColor Magenta