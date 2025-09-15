# NQBA Platform Troubleshooting Reference

## Quick Reference Guide

This document contains specific troubleshooting scenarios encountered during development and deployment of the NQBA Platform.

## Package Installation Issues

### Issue 1: ortools Version Conflict

**Error Message**:
```
ERROR: Could not find a version that satisfies the requirement ortools==9.8.3296 (from versions: 9.12.4544, 9.13.4784, 9.14.6206)
ERROR: No matching distribution found for ortools==9.8.3296
```

**Root Cause**: The specified version `9.8.3296` is no longer available in the package repository.

**Solution**:
1. Update `requirements.txt`:
   ```diff
   - ortools==9.8.3296
   + ortools==9.14.6206
   ```
2. Reinstall dependencies

**Prevention**: Regularly check for package availability and update version pins.

### Issue 2: ipfshttpclient Version Conflict

**Error Message**:
```
ERROR: Could not find a version that satisfies the requirement ipfshttpclient==0.8.0 (from versions: 0.4.10, 0.4.11, 0.4.12, 0.4.13, 0.4.13.1, 0.4.13.2, 0.6.0, 0.6.0.post1, 0.6.1, 0.7.0a1, 0.7.0, 0.8.0a1, 0.8.0a2)
ERROR: No matching distribution found for ipfshttpclient==0.8.0
```

**Root Cause**: Version `0.8.0` is not available, only alpha versions exist.

**Solution**:
1. Update `requirements.txt`:
   ```diff
   - ipfshttpclient==0.8.0
   + ipfshttpclient==0.8.0a2
   ```
2. Reinstall dependencies

**Alternative**: Use the latest stable version `0.7.0` if alpha versions cause issues.

### Issue 3: Pandas Compilation Failure

**Error Message**:
```
ninja: build stopped: subcommand failed.
Activating VS 17.14.3
INFO: automatically activated MSVC compiler environment
error: metadata-generation-failed
```

**Root Cause**: Pandas requires compilation on Windows and may fail due to missing build tools.

**Solutions**:
1. **Immediate**: Install core dependencies without pandas:
   ```powershell
   pip install fastapi uvicorn pydantic pydantic-settings bcrypt PyJWT python-multipart requests pytest pytest-asyncio httpx python-dotenv cryptography
   ```

2. **Long-term**: Install Microsoft C++ Build Tools:
   - Download Visual Studio Build Tools
   - Install C++ build tools component
   - Retry pandas installation

3. **Alternative**: Use pre-compiled wheels:
   ```powershell
   pip install --only-binary=all pandas
   ```

## Windows-Specific Issues

### Issue 4: Make Command Not Found

**Error Message**:
```
make : The term 'make' is not recognized as the name of a cmdlet, function, script file, or operable program.
```

**Root Cause**: Make is not available on Windows PowerShell by default.

**Solutions**:
1. **Immediate**: Use PowerShell equivalents:
   ```powershell
   # Instead of: make test
   $env:PYTHONPATH="$PWD/src"; pytest --cov=src --cov-report=term-missing tests/
   
   # Instead of: make run
   uvicorn api_server:app --reload
   ```

2. **Long-term**: Install make for Windows:
   - Install via Chocolatey: `choco install make`
   - Install via Scoop: `scoop install make`
   - Use WSL (Windows Subsystem for Linux)

## Server Runtime Issues

### Issue 5: Configuration Warnings

**Warning Messages**:
```
[DYNEX] WARNING: missing configuration file dynex.ini
OpenAI API key should start with 'sk-'
```

**Root Cause**: Optional configuration files and API keys are not set up.

**Impact**: These are warnings only and don't prevent server operation.

**Solutions** (Optional):
1. Create `dynex.ini` configuration file
2. Set OpenAI API key in environment variables
3. Configure these only if using related features

### Issue 6: Test Collection Errors

**Error Pattern**:
```
ERROR tests/test_api_server_smoke.py
ERROR tests/test_auth_system.py
!!!!!!!!!!!!!!!!!!! Interrupted: 7 errors during collection !!!!!!!!!!!!!!!!!!!
```

**Root Cause**: Missing dependencies for test modules.

**Impact**: Tests fail but core functionality works.

**Solutions**:
1. **Immediate**: Skip tests and proceed with server startup
2. **Development**: Install missing test dependencies:
   ```powershell
   pip install pytest-cov pytest-mock
   ```
3. **Production**: Tests are not required for basic operation

## Performance Issues

### Issue 7: Slow Package Installation

**Symptoms**: Package installation takes very long time.

**Solutions**:
1. Use faster package index:
   ```powershell
   pip install -i https://pypi.org/simple/ <package>
   ```

2. Install from cache:
   ```powershell
   pip install --cache-dir ./pip-cache <package>
   ```

3. Use binary wheels only:
   ```powershell
   pip install --only-binary=all <package>
   ```

## Network Issues

### Issue 8: Package Download Failures

**Symptoms**: Timeout errors during package download.

**Solutions**:
1. Increase timeout:
   ```powershell
   pip install --timeout 300 <package>
   ```

2. Use different index:
   ```powershell
   pip install -i https://pypi.python.org/simple/ <package>
   ```

3. Download manually and install locally:
   ```powershell
   pip download <package>
   pip install <package-file>.whl
   ```

## Diagnostic Commands

### Environment Information
```powershell
# Python version
python --version

# Pip version
pip --version

# Installed packages
pip list

# Package information
pip show <package-name>

# Check for conflicts
pip check
```

### Server Diagnostics
```powershell
# Check port usage
netstat -an | findstr :8000

# Process information
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Server logs
# Check terminal output for error messages
```

## Recovery Procedures

### Clean Installation
1. Remove virtual environment (if used)
2. Clear pip cache: `pip cache purge`
3. Reinstall core dependencies only
4. Test basic functionality
5. Add optional dependencies incrementally

### Rollback Strategy
1. Keep backup of working `requirements.txt`
2. Document working package versions
3. Use version control for configuration changes

## Prevention Strategies

1. **Pin Dependencies**: Use exact versions in `requirements.txt`
2. **Regular Updates**: Check for package updates monthly
3. **Testing**: Test installations in clean environments
4. **Documentation**: Keep this troubleshooting guide updated
5. **Monitoring**: Watch for deprecation warnings

---

**Last Updated**: January 2025
**Maintainer**: Development Team
**Next Review**: February 2025