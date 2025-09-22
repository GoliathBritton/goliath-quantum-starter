# Troubleshooting Guide

## Common Issues and Solutions

### Authentication Problems

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Invalid API Key | 401 Unauthorized response | Verify API key is correct and not expired. Regenerate if necessary in Account Settings → API Keys. |
| Token Expired | 401 Unauthorized with "token_expired" error code | Refresh your access token using the refresh token endpoint or re-authenticate. |
| Missing Permissions | 403 Forbidden response | Check user role and permissions in Account Settings → User Management. Request additional permissions if needed. |
| Account Locked | Unable to log in with correct credentials | Contact support at support@goliath-quantum.com with your account details. |

### Job Submission Failures

| Error Code | Description | Solution |
|------------|-------------|----------|
| INVALID_CIRCUIT | Circuit validation failed | Check circuit structure for errors. Common issues: invalid gate parameters, qubits out of range, or unsupported gates for the selected backend. |
| BACKEND_UNAVAILABLE | Selected quantum backend is offline | Choose an alternative backend or wait until the backend is back online. Check System Status page for maintenance schedules. |
| QUOTA_EXCEEDED | Monthly resource quota exceeded | Upgrade your subscription plan or wait until the next billing cycle. Temporary quota increases can be requested via Account Settings → Quota Management. |
| INVALID_SHOTS | Shot count out of allowed range | Adjust the number of shots to be within the allowed range (typically 1-10,000 depending on backend). |

### Performance Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Slow Job Execution | Jobs taking longer than expected | Check backend utilization on System Status page. Consider using a different backend or scheduling jobs during off-peak hours. |
| UI Responsiveness | Dashboard loading slowly | Clear browser cache and cookies. Ensure you're using a supported browser version. Try disabling browser extensions. |
| High Error Rates | Results show unexpected distribution | Check backend calibration data. Consider using error mitigation techniques or a backend with better qubit quality. |
| Timeout on Large Circuits | Job fails with timeout error | Break down large circuits into smaller components. Use circuit optimization techniques to reduce depth and gate count. |

### Integration Problems

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Webhook Delivery Failure | Missing job notifications | Verify webhook URL is accessible from the internet. Check webhook logs in Dashboard → Integrations → Webhook Logs. |
| SDK Compatibility | SDK methods throwing errors | Ensure you're using the latest SDK version compatible with the API version. Check release notes for breaking changes. |
| Rate Limiting | 429 Too Many Requests response | Implement exponential backoff and retry logic. Consider batching requests or optimizing your integration to reduce API calls. |
| SSO Configuration | Unable to log in with SSO | Verify IdP configuration and SAML/OIDC settings. Check logs for specific error messages and contact support with details. |

## Error Code Reference

### System Error Codes

| Code | Description | Troubleshooting Steps |
|------|-------------|----------------------|
| SYS-001 | Database connection error | System issue - check System Status page and try again later. |
| SYS-002 | Internal server error | Report to support with request ID from error response. |
| SYS-003 | Service unavailable | Check System Status page for maintenance notices. |
| SYS-004 | Rate limit exceeded | Reduce request frequency or implement backoff strategy. |

### Authentication Error Codes

| Code | Description | Troubleshooting Steps |
|------|-------------|----------------------|
| AUTH-001 | Invalid credentials | Verify username/password or API key. |
| AUTH-002 | Token expired | Refresh token or re-authenticate. |
| AUTH-003 | Invalid token | Token may be malformed or tampered with. Re-authenticate. |
| AUTH-004 | Account locked | Contact support to unlock account. |
| AUTH-005 | MFA required | Complete multi-factor authentication process. |

### Job Error Codes

| Code | Description | Troubleshooting Steps |
|------|-------------|----------------------|
| JOB-001 | Invalid circuit format | Check circuit structure and gate parameters. |
| JOB-002 | Backend not available | Select different backend or try later. |
| JOB-003 | Execution timeout | Optimize circuit or increase timeout parameter. |
| JOB-004 | Quota exceeded | Upgrade plan or request temporary increase. |
| JOB-005 | Invalid parameters | Check job submission parameters against API docs. |
| JOB-006 | Circuit too complex | Reduce circuit depth or qubit count. |
| JOB-007 | Hardware error | Backend hardware issue - try different backend. |

## Diagnostic Procedures

### API Connection Issues

1. **Verify Network Connectivity**
   ```bash
   # Test basic connectivity
   ping api.goliath-quantum.com
   
   # Test HTTPS connectivity
   curl -v https://api.goliath-quantum.com/v1/health
   ```

2. **Check API Status**
   ```bash
   # Get current API status
   curl https://status.goliath-quantum.com/api/v1/status
   ```

3. **Validate Authentication**
   ```bash
   # Test authentication with API key
   curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.goliath-quantum.com/v1/user/profile
   ```

### Job Debugging

1. **Retrieve Detailed Job Status**
   ```bash
   # Get detailed job information including error logs
   curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.goliath-quantum.com/v1/jobs/JOB_ID/details
   ```

2. **Check Backend Status**
   ```bash
   # Get backend status and calibration data
   curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.goliath-quantum.com/v1/backends/BACKEND_ID/status
   ```

3. **Validate Circuit**
   ```bash
   # Validate circuit without submitting
   curl -X POST -H "Authorization: Bearer YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"circuit": YOUR_CIRCUIT_JSON}' \
     https://api.goliath-quantum.com/v1/circuits/validate
   ```

## Common Scenarios and Solutions

### Scenario 1: Job Stuck in Queue

**Symptoms:**
- Job status remains "queued" for an extended period
- No progress updates in the dashboard

**Diagnostic Steps:**
1. Check backend status for high utilization or maintenance
2. Verify job priority setting
3. Check for system-wide delays on Status page

**Solutions:**
1. For urgent jobs, increase priority (if available on your plan)
2. Submit to an alternative backend with lower utilization
3. Break job into smaller parallel jobs if possible
4. Contact support for jobs stuck more than 24 hours

### Scenario 2: Unexpected Quantum Results

**Symptoms:**
- Results don't match theoretical expectations
- High error rates or unexpected distribution

**Diagnostic Steps:**
1. Check backend calibration data for recent changes
2. Verify circuit construction and gate parameters
3. Analyze if shot count is sufficient for statistical significance

**Solutions:**
1. Implement error mitigation techniques:
   ```python
   from goliath_quantum import ErrorMitigation
   
   # Apply readout error correction
   mitigator = ErrorMitigation.readout_correction(backend_id)
   corrected_results = mitigator.apply(raw_results)
   
   # Apply zero-noise extrapolation
   zne = ErrorMitigation.zero_noise_extrapolation()
   improved_results = zne.apply(circuit, backend_id)
   ```

2. Use a backend with better qubit quality
3. Increase shot count for better statistical sampling
4. Apply circuit optimization to reduce error accumulation

### Scenario 3: Integration Webhook Failures

**Symptoms:**
- Missing notifications for job status changes
- Webhook delivery failures in logs

**Diagnostic Steps:**
1. Check webhook endpoint accessibility
2. Verify correct URL configuration
3. Check for response timeout issues
4. Examine webhook logs for specific error messages

**Solutions:**
1. Ensure webhook server is publicly accessible
2. Implement proper response handling (return 200 OK promptly)
3. Add authentication validation if required
4. Set up webhook retry policy in Dashboard → Integrations → Webhook Settings

### Scenario 4: Account Access Issues

**Symptoms:**
- Unable to log in despite correct credentials
- SSO authentication failures
- Unexpected session timeouts

**Diagnostic Steps:**
1. Check for account status issues (suspension, expiration)
2. Verify SSO configuration if applicable
3. Check for browser compatibility issues
4. Examine for suspicious activity or security blocks

**Solutions:**
1. Reset password using the recovery process
2. Clear browser cookies and cache
3. Try an alternative supported browser
4. Contact support with specific error messages and timestamps

## Performance Optimization

### Circuit Optimization Techniques

1. **Gate Cancellation and Fusion**
   - Identify and remove redundant gates (e.g., consecutive X gates)
   - Combine adjacent gates when possible

2. **Qubit Mapping**
   - Optimize qubit layout based on backend connectivity
   - Minimize SWAP operations

3. **Noise-Aware Optimization**
   - Prioritize high-fidelity qubits and gates
   - Avoid error-prone operations when possible

### API Usage Optimization

1. **Batch Operations**
   - Combine multiple operations in single API calls
   - Use batch job submission for multiple circuits

2. **Implement Caching**
   - Cache backend information and calibration data
   - Store frequently used results locally

3. **Optimize Polling**
   - Use webhooks instead of polling when possible
   - Implement exponential backoff for status checks

## Contact Support

If you're unable to resolve an issue using this guide, contact support:

- **Email:** support@goliath-quantum.com
- **Support Portal:** https://support.goliath-quantum.com
- **Emergency Support:** +1-555-123-4567 (Premium and Enterprise plans only)

When contacting support, please provide:
- Account ID
- Job IDs (if applicable)
- Error messages and codes
- Steps to reproduce the issue
- Timestamps of when the issue occurred

---

*Last Updated: July 2023*  
*Document Version: 1.0*  
*Contact: support@goliath-quantum.com*