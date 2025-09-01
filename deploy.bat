@echo off
setlocal enabledelayedexpansion

REM Q-Sales Division™ Partner Portal Deployment Script
REM This script sets up and deploys the complete portal system

echo.
echo 🚀 Q-Sales Division™ Partner Portal Deployment
echo ==============================================
echo Powered by Dynex Quantum Computing (410x Performance)
echo.

REM Check prerequisites
echo [INFO] Checking prerequisites...

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed. Please install Node.js 18+ first.
    pause
    exit /b 1
)

for /f "tokens=1,2 delims=." %%a in ('node --version') do (
    set NODE_VERSION=%%a
    set NODE_VERSION=!NODE_VERSION:~1!
)

if !NODE_VERSION! lss 18 (
    echo [ERROR] Node.js version 18+ is required. Current version: 
    node --version
    pause
    exit /b 1
)

echo [SUCCESS] Node.js 
node --version
echo ✓

REM Check npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed.
    pause
    exit /b 1
)

echo [SUCCESS] npm 
npm --version
echo ✓

REM Check if we're in the right directory
if not exist "package.json" (
    echo [ERROR] package.json not found. Please run this script from the project root.
    pause
    exit /b 1
)

echo [SUCCESS] Project structure ✓

REM Install dependencies
echo.
echo [INFO] Installing dependencies...

if exist "node_modules" (
    echo [WARNING] node_modules already exists. Removing for clean install...
    rmdir /s /q node_modules
)

npm install

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [SUCCESS] Dependencies installed successfully ✓

REM Setup environment
echo.
echo [INFO] Setting up environment...

if not exist ".env.local" (
    if exist ".env.example" (
        copy ".env.example" ".env.local" >nul
        echo [WARNING] Created .env.local from .env.example
        echo [WARNING] Please edit .env.local with your actual configuration
    ) else (
        echo [WARNING] .env.example not found. Creating basic .env.local...
        (
            echo # Q-Sales Division™ Partner Portal Environment Variables
            echo # Edit these values with your actual configuration
            echo.
            echo # Stripe Configuration
            echo NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
            echo STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
            echo STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
            echo.
            echo # NextAuth Configuration
            echo NEXTAUTH_URL=http://localhost:3000
            echo NEXTAUTH_SECRET=your_nextauth_secret_here
            echo.
            echo # NQBA MCP Integration
            echo NQBA_MCP_ENDPOINT=http://localhost:8000/mcp
            echo NQBA_API_KEY=your_nqba_api_key_here
            echo.
            echo # Goliath Business Configuration
            echo GOLIATH_PORTAL_URL=https://portal.goliath.com
            echo FLYFOX_AI_URL=https://app.flyfoxai.io
            echo SIGMA_SELECT_URL=https://sigma-select.com
        ) > .env.local
    )
) else (
    echo [WARNING] .env.local already exists. Please ensure it's configured correctly.
)

echo [SUCCESS] Environment setup complete ✓

REM Build the project
echo.
echo [INFO] Building the project...

npm run build

if %errorlevel% neq 0 (
    echo [ERROR] Build failed
    pause
    exit /b 1
)

echo [SUCCESS] Project built successfully ✓

echo.
echo [SUCCESS] Deployment completed successfully! 🎉
echo.

set /p START_SERVER="Would you like to start the development server now? (y/n): "

if /i "!START_SERVER!"=="y" (
    echo.
    echo [INFO] Starting development server...
    echo.
    echo 🚀 Q-Sales Division™ Partner Portal is starting up!
    echo.
    echo 📍 Access your portal at: http://localhost:3000
    echo 🔑 Default routes:
    echo    • Home: http://localhost:3000
    echo    • Packages: http://localhost:3000/packages
    echo    • Contacts: http://localhost:3000/contacts
    echo    • Sales Pods: http://localhost:3000/pods
    echo    • Login: http://localhost:3000/auth/login
    echo    • Register: http://localhost:3000/auth/register
    echo.
    echo ⚡ Powered by Dynex Quantum Computing (410x Performance)
    echo 🎯 Ready to deploy your autonomous sales division!
    echo.
    echo Press Ctrl+C to stop the server
    echo.
    
    npm run dev
) else (
    echo.
    echo [INFO] To start the server later, run: npm run dev
    echo.
    echo [SUCCESS] Q-Sales Division™ Partner Portal is ready for deployment! 🚀
)

pause
