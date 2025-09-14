@echo off
REM Goliath Quantum Division - Quick Deployment Launcher
REM Windows Batch Script for Easy Deployment

echo.
echo ===============================================================
echo 🚀 GOLIATH QUANTUM DIVISION - DEPLOYMENT LAUNCHER
echo ===============================================================
echo.

REM Check if PowerShell is available
powershell -Command "Write-Host 'PowerShell is available' -ForegroundColor Green"
if %errorlevel% neq 0 (
    echo ❌ PowerShell is required but not available
    echo Please install PowerShell and try again
    pause
    exit /b 1
)

REM Set execution policy for current session
echo 🔧 Setting PowerShell execution policy...
powershell -Command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force"

REM Check for deployment mode argument
set DEPLOY_MODE=%1
if "%DEPLOY_MODE%"=="" set DEPLOY_MODE=docker

echo 📋 Deployment Configuration:
echo    Mode: %DEPLOY_MODE%
echo    Environment: production
echo    Target: 10K+ contact batch processing
echo.

REM Ask user for confirmation
set /p CONFIRM="🤔 Do you want to proceed with deployment? (y/N): "
if /i not "%CONFIRM%"=="y" (
    echo ❌ Deployment cancelled by user
    pause
    exit /b 0
)

echo.
echo 🚀 Starting deployment...
echo.

REM Run the PowerShell deployment script
powershell -ExecutionPolicy Bypass -File "deploy\deploy.ps1" -Environment production -Mode %DEPLOY_MODE%

REM Check deployment result
if %errorlevel% equ 0 (
    echo.
    echo ===============================================================
    echo ✅ DEPLOYMENT COMPLETED SUCCESSFULLY!
    echo ===============================================================
    echo.
    echo 🌐 Access URLs:
    echo    • NQBA Engine: http://localhost:8000
    echo    • Main API: http://localhost:8080
    echo    • Web Frontend: http://localhost:3000
    echo    • Grafana Dashboard: http://localhost:3001
    echo    • Prometheus Metrics: http://localhost:9090
    echo.
    echo 🎉 Goliath Quantum Division is ready for enterprise deployment!
    echo 📊 Platform can now handle 10,000+ contact batches
    echo.
) else (
    echo.
    echo ===============================================================
    echo ❌ DEPLOYMENT FAILED!
    echo ===============================================================
    echo.
    echo Please check the logs for more information:
    echo    • deployment.log
    echo    • deploy\reports\
    echo.
    echo For support, please review the deployment documentation.
    echo.
)

echo Press any key to exit...
pause >nul
exit /b %errorlevel%