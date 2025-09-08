# NQBA Platform Build & Deployment Guide

## Overview
This document provides comprehensive instructions for building and deploying the NQBA Quantum Computing Platform, including troubleshooting steps and procedures.

## Prerequisites
- Python 3.8+ installed
- PowerShell or Command Prompt access
- Internet connection for package downloads

## Build Process

### 1. Dependency Installation

#### Core Dependencies
The platform requires several Python packages. Install core dependencies first:

```powershell
pip install fastapi uvicorn pydantic pydantic-settings bcrypt PyJWT python-multipart requests pytest pytest-asyncio httpx python-dotenv cryptography
```

#### Known Version Compatibility Issues

**Problem**: Some packages in `requirements.txt` may have outdated versions.

**Solutions Applied**:
- Updated `ortools==9.8.3296` to `ortools==9.14.6206`
- Updated `ipfshttpclient==0.8.0` to `ipfshttpclient==0.8.0a2`

**Troubleshooting Steps**:
1. If you encounter version conflicts, check available versions:
   ```powershell
   pip index versions <package-name>
   ```
2. Update the version in `requirements.txt` to a compatible one
3. Install core dependencies separately if full requirements.txt fails

### 2. Testing

#### Running Tests
**Note**: Make is not available on Windows PowerShell by default.

**Alternative Command**:
```powershell
$env:PYTHONPATH="$PWD/src"; pytest --cov=src --cov-report=term-missing tests/
```

**Expected Issues**:
- Some tests may fail due to missing optional dependencies
- Import errors are common when not all packages are installed
- This is acceptable for basic functionality

### 3. Server Deployment

#### Starting the FastAPI Server
```powershell
uvicorn api_server:app --reload
```

**Expected Output**:
```
INFO:     Will watch for changes in these directories: ['C:\\path\\to\\project']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [PID] using WatchFiles
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Common Warnings (Safe to Ignore)**:
- `[DYNEX] WARNING: missing configuration file dynex.ini`
- `OpenAI API key should start with 'sk-'`

These warnings don't prevent the server from running.

## Verification Steps

### 1. Server Health Check
- Server should be accessible at `http://127.0.0.1:8000`
- API documentation available at `http://127.0.0.1:8000/docs`
- Server logs should show successful startup messages

### 2. Basic Functionality Test
- Check server responds to HTTP requests
- Verify no critical errors in logs
- Confirm auto-reload is working (if enabled)

## Troubleshooting Guide

### Common Issues

#### 1. Package Installation Failures
**Symptoms**: 
- `ERROR: Could not find a version that satisfies the requirement`
- Compilation errors during installation

**Solutions**:
1. Update package versions in `requirements.txt`
2. Install packages individually
3. Use pre-compiled wheels when available
4. Skip problematic optional dependencies initially

#### 2. Import Errors
**Symptoms**:
- `ModuleNotFoundError` when running tests or server
- Missing dependencies

**Solutions**:
1. Ensure `PYTHONPATH` includes the `src` directory
2. Install missing core dependencies
3. Check Python version compatibility

#### 3. Server Startup Issues
**Symptoms**:
- Server fails to start
- Port already in use errors

**Solutions**:
1. Check if port 8000 is already in use
2. Use different port: `uvicorn api_server:app --port 8001`
3. Kill existing processes using the port

### Windows-Specific Considerations

1. **Make Command**: Not available by default
   - Use PowerShell equivalents for Makefile commands
   - Translate Unix commands to Windows PowerShell

2. **Path Separators**: Use backslashes or forward slashes consistently

3. **Environment Variables**: Use `$env:VARIABLE` syntax in PowerShell

## File Structure After Build

```
project/
├── src/                    # Source code
├── tests/                  # Test files
├── docs/                   # Documentation (this file)
├── requirements.txt        # Python dependencies (updated)
├── api_server.py          # Main FastAPI application
├── Makefile               # Build commands (Unix)
└── logs/                  # Runtime logs
```

## Maintenance

### Regular Updates
1. Keep dependencies updated for security
2. Monitor for deprecated packages
3. Test compatibility with new Python versions

### Monitoring
1. Check server logs regularly
2. Monitor resource usage
3. Verify API endpoints remain functional

## Development Workflow

1. **Setup**: Follow build process above
2. **Development**: Use `--reload` flag for auto-restart
3. **Testing**: Run tests before committing changes
4. **Deployment**: Use production WSGI server for live deployment

## Production Considerations

- Use production WSGI server (e.g., Gunicorn) instead of uvicorn for production
- Configure proper logging levels
- Set up monitoring and alerting
- Use environment variables for sensitive configuration
- Implement proper security measures

---

**Last Updated**: January 2025
**Version**: 1.0
**Tested On**: Windows 11, Python 3.13