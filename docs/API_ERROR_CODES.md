# API Error Codes Reference

This document provides a comprehensive list of error codes that may be returned by the API, along with their descriptions and recommended troubleshooting steps.

## Error Response Format

All API errors follow a consistent JSON format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "request_id": "unique-request-identifier",
    "timestamp": "ISO-8601 timestamp"
  }
}
```

The `request_id` field can be used when contacting support for assistance with specific errors.

## System Error Codes (SYS)

| Code | Description | Troubleshooting Steps |
|------|-------------|----------------------|
| SYS-001 | Database connection error | System issue - check System Status page and try again later. |
| SYS-002 | Internal server error | Report to support with request ID from error response. |
| SYS-003 | Service unavailable | Check System Status page for maintenance notices. |
| SYS-004 | Rate limit exceeded | Reduce request frequency or implement backoff strategy. |
| SYS-005 | Invalid configuration | Verify your configuration settings and try again. |

## Authentication Error Codes (AUTH)

| Code | Description | Troubleshooting Steps |
|------|-------------|----------------------|
| AUTH-001 | Invalid credentials | Verify username/password or API key. |
| AUTH-002 | Token expired | Refresh token or re-authenticate. |
| AUTH-003 | Invalid token | Token may be malformed or tampered with. Re-authenticate. |
| AUTH-004 | Account locked | Contact support to unlock account. |
| AUTH-005 | MFA required | Complete multi-factor authentication process. |
| AUTH-006 | Insufficient permissions | Request access to the required resource. |

## Job Error Codes (JOB)

| Code | Description | Troubleshooting Steps |
|------|-------------|----------------------|
| JOB-001 | Invalid circuit format | Check circuit structure and gate parameters. |
| JOB-002 | Backend not available | Select different backend or try later. |
| JOB-003 | Execution timeout | Optimize circuit or increase timeout parameter. |
| JOB-004 | Quota exceeded | Upgrade plan or request temporary increase. |
| JOB-005 | Invalid job parameters | Check job configuration parameters. |
| JOB-006 | Job cancelled | Job was cancelled by user or system. |

## Data Error Codes (DATA)

| Code | Description | Troubleshooting Steps |
|------|-------------|----------------------|
| DATA-001 | Invalid input data | Check input data format and requirements. |
| DATA-002 | Missing required field | Ensure all required fields are provided. |
| DATA-003 | Data validation failed | Verify data meets validation requirements. |
| DATA-004 | Data processing error | Check data format and try again. |
| DATA-005 | Data not found | Verify the requested data exists. |

## Integration Error Codes (INT)

| Code | Description | Troubleshooting Steps |
|------|-------------|----------------------|
| INT-001 | Third-party service unavailable | Check third-party service status. |
| INT-002 | Integration configuration error | Verify integration settings. |
| INT-003 | Webhook delivery failed | Check webhook endpoint availability. |
| INT-004 | API version mismatch | Update client to compatible API version. |

## Best Practices for Error Handling

1. **Implement retry logic** with exponential backoff for transient errors (SYS-001, SYS-003, INT-001)
2. **Log request IDs** for all failed requests to facilitate troubleshooting
3. **Monitor error rates** to detect systemic issues
4. **Implement graceful degradation** when services are unavailable
5. **Provide clear error messages** to end-users when appropriate

## Support Resources

If you encounter persistent errors, please contact support with the following information:
- Error code and message
- Request ID
- Timestamp
- Steps to reproduce the error
- Any relevant request payloads (with sensitive data removed)