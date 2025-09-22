# Third-Party Integration Guide

## Overview

This guide provides comprehensive instructions for integrating external systems with the Goliath Quantum Platform. It covers API integration, data exchange protocols, authentication mechanisms, and best practices for creating robust integrations.

## Integration Architecture

### High-Level Architecture

```
┌─────────────────┐      ┌───────────────────┐      ┌─────────────────┐
│                 │      │                   │      │                 │
│  Third-Party    │◄────►│  Goliath Quantum  │◄────►│  Quantum        │
│  System         │      │  Platform API     │      │  Processing     │
│                 │      │                   │      │  Infrastructure │
└─────────────────┘      └───────────────────┘      └─────────────────┘
```

The Goliath Quantum Platform provides multiple integration points:

1. **REST API**: Primary integration method for most systems
2. **Webhook Callbacks**: Event-driven integration for real-time updates
3. **Data Exchange Formats**: Standardized formats for quantum problem definition
4. **SDK Libraries**: Language-specific libraries for common programming environments

## Authentication & Security

### API Authentication

The platform uses OAuth 2.0 and API keys for authentication:

#### API Key Authentication

```http
GET /api/v1/jobs HTTP/1.1
Host: api.goliath-quantum.com
Authorization: Bearer YOUR_API_KEY
```

#### OAuth 2.0 Flow

1. Register your application in the Goliath Quantum developer portal
2. Implement the OAuth 2.0 authorization code flow
3. Exchange authorization code for access token
4. Use access token in API requests

### Security Requirements

All integrations must adhere to these security standards:

- TLS 1.2+ for all communications
- Regular rotation of API keys (90-day maximum lifetime)
- Principle of least privilege for API access
- Secure storage of credentials (no hardcoding)
- IP allowlisting for production environments

## Core API Endpoints

### Job Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/jobs` | GET | List all jobs |
| `/api/v1/jobs` | POST | Submit a new job |
| `/api/v1/jobs/{job_id}` | GET | Get job details |
| `/api/v1/jobs/{job_id}/cancel` | POST | Cancel a job |
| `/api/v1/jobs/{job_id}/results` | GET | Retrieve job results |

### User Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/users` | GET | List users (admin only) |
| `/api/v1/users/{user_id}` | GET | Get user details |
| `/api/v1/users/{user_id}` | PUT | Update user |

### System Status

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/status` | GET | Get platform status |
| `/api/v1/metrics` | GET | Get system metrics |

## Integration Patterns

### Synchronous Job Processing

For small jobs with quick execution:

1. Submit job via API
2. Wait for response with results
3. Process results in your application

```python
import requests

API_KEY = "your_api_key"
BASE_URL = "https://api.goliath-quantum.com/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Submit job with synchronous execution flag
job_data = {
    "name": "Small Optimization",
    "algorithm": "QAOA",
    "synchronous": True,
    "parameters": {
        "p": 1,
        "shots": 100
    },
    "input_data": {
        # Job-specific data
    }
}

response = requests.post(
    f"{BASE_URL}/jobs",
    headers=headers,
    json=job_data
)

# Results are included in the response
results = response.json()["results"]
print("Job results:", results)
```

### Asynchronous Job Processing

For larger jobs with longer execution times:

1. Submit job via API
2. Receive job ID
3. Poll for job status or set up webhook
4. Retrieve results when job completes

```python
import requests
import time

API_KEY = "your_api_key"
BASE_URL = "https://api.goliath-quantum.com/v1"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Submit job
job_data = {
    "name": "Large Optimization",
    "algorithm": "QAOA",
    "parameters": {
        "p": 3,
        "shots": 10000
    },
    "input_data": {
        # Job-specific data
    },
    "webhook_url": "https://your-system.com/webhooks/quantum-job"
}

response = requests.post(
    f"{BASE_URL}/jobs",
    headers=headers,
    json=job_data
)

job_id = response.json()["job_id"]
print(f"Job submitted with ID: {job_id}")

# Poll for status (alternative to webhook)
while True:
    response = requests.get(
        f"{BASE_URL}/jobs/{job_id}",
        headers=headers
    )
    
    status = response.json()["status"]
    print(f"Job status: {status}")
    
    if status in ["COMPLETED", "FAILED", "CANCELLED"]:
        break
        
    time.sleep(30)  # Check every 30 seconds

# Retrieve results
if status == "COMPLETED":
    response = requests.get(
        f"{BASE_URL}/jobs/{job_id}/results",
        headers=headers
    )
    
    results = response.json()["results"]
    print("Job results:", results)
```

### Webhook Integration

For event-driven architectures:

1. Register webhook URL in job submission
2. Implement webhook endpoint in your system
3. Receive real-time updates as job progresses

```python
# Flask example of webhook receiver
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhooks/quantum-job', methods=['POST'])
def quantum_job_webhook():
    data = request.json
    
    job_id = data["job_id"]
    status = data["status"]
    
    print(f"Received update for job {job_id}: {status}")
    
    # Process based on status
    if status == "COMPLETED":
        results = data["results"]
        # Process results
        process_job_results(job_id, results)
    elif status == "FAILED":
        error = data["error"]
        # Handle error
        handle_job_error(job_id, error)
    
    return jsonify({"status": "received"})

def process_job_results(job_id, results):
    # Your result processing logic
    pass

def handle_job_error(job_id, error):
    # Your error handling logic
    pass

if __name__ == '__main__':
    app.run(port=5000)
```

## Data Formats

### Job Submission Format

```json
{
  "name": "Sample Optimization Job",
  "description": "Optimize delivery routes",
  "algorithm": "QAOA",
  "parameters": {
    "p": 2,
    "shots": 1000,
    "optimizer": "COBYLA",
    "max_iterations": 100
  },
  "input_data": {
    "problem_type": "tsp",
    "locations": [
      {"id": "A", "lat": 40.7128, "lng": -74.0060},
      {"id": "B", "lat": 34.0522, "lng": -118.2437},
      {"id": "C", "lat": 41.8781, "lng": -87.6298}
    ],
    "constraints": {
      "max_distance": 10000
    }
  },
  "output_format": "json",
  "priority": "normal",
  "webhook_url": "https://your-system.com/webhooks/quantum-job"
}
```

### Results Format

```json
{
  "job_id": "job_12345",
  "status": "COMPLETED",
  "execution_time": 120.5,
  "results": {
    "solution": [0, 2, 1, 0],
    "solution_quality": 0.95,
    "energy": -15.7,
    "route_distance": 8500,
    "execution_details": {
      "shots": 1000,
      "backend": "quantum_simulator_v2",
      "optimizer_iterations": 87,
      "final_parameters": [0.1, 0.8, 1.2, 1.5]
    }
  },
  "timestamp": "2023-07-15T14:30:45Z"
}
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "INVALID_PARAMETER",
    "message": "Parameter 'p' must be a positive integer",
    "details": {
      "parameter": "p",
      "provided_value": -1,
      "allowed_values": "positive integers"
    },
    "request_id": "req_67890"
  }
}
```

### Common Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `AUTHENTICATION_ERROR` | Invalid API key or token | Check credentials |
| `AUTHORIZATION_ERROR` | Insufficient permissions | Request additional access |
| `INVALID_PARAMETER` | Parameter validation failed | Correct parameter values |
| `RESOURCE_NOT_FOUND` | Requested resource doesn't exist | Check resource ID |
| `QUOTA_EXCEEDED` | Usage limit reached | Upgrade plan or wait |
| `SYSTEM_ERROR` | Internal platform error | Contact support |

### Retry Strategy

For transient errors:

1. Implement exponential backoff
2. Start with 1-second delay
3. Double delay on each retry
4. Maximum 5 retries
5. Add jitter to prevent thundering herd

```python
import requests
import time
import random

def api_request_with_retry(url, headers, max_retries=5):
    retries = 0
    base_delay = 1  # 1 second
    
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code < 500:  # Don't retry 4xx errors
                return response
                
        except requests.exceptions.RequestException:
            pass
            
        retries += 1
        if retries >= max_retries:
            break
            
        # Exponential backoff with jitter
        delay = base_delay * (2 ** (retries - 1))
        jitter = random.uniform(0, 0.1 * delay)
        time.sleep(delay + jitter)
    
    # If we get here, all retries failed
    raise Exception(f"Failed after {max_retries} retries")
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- Standard tier: 100 requests per minute
- Professional tier: 500 requests per minute
- Enterprise tier: 2000 requests per minute

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1626369245
```

Implement rate limit handling in your integration:

```python
import requests
import time

def rate_limited_request(url, headers):
    response = requests.get(url, headers=headers)
    
    if response.status_code == 429:  # Too Many Requests
        # Get reset time from headers
        reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
        current_time = int(time.time())
        
        # Calculate wait time (add 1 second buffer)
        wait_time = max(0, reset_time - current_time) + 1
        
        print(f"Rate limit exceeded. Waiting {wait_time} seconds.")
        time.sleep(wait_time)
        
        # Retry the request
        return requests.get(url, headers=headers)
    
    return response
```

## SDK Libraries

Official SDK libraries are available for:

- Python: `pip install goliath-quantum-sdk`
- JavaScript: `npm install goliath-quantum-sdk`
- Java: Maven dependency
- C#: NuGet package

Example using Python SDK:

```python
from goliath_quantum import QuantumClient, QAOAJob

# Initialize client
client = QuantumClient(api_key="your_api_key")

# Create job
job = QAOAJob(
    name="SDK Example Job",
    p=2,
    shots=1000
)

# Add problem data
job.add_tsp_problem([
    {"id": "A", "lat": 40.7128, "lng": -74.0060},
    {"id": "B", "lat": 34.0522, "lng": -118.2437},
    {"id": "C", "lat": 41.8781, "lng": -87.6298}
])

# Submit job
result = client.submit_job(job)

# Get job ID
job_id = result.job_id
print(f"Job submitted with ID: {job_id}")

# Wait for completion
result = client.wait_for_job(job_id, timeout=300)

# Process results
if result.status == "COMPLETED":
    solution = result.results["solution"]
    quality = result.results["solution_quality"]
    print(f"Solution: {solution}, Quality: {quality}")
```

## Enterprise Integration

### Single Sign-On (SSO)

For enterprise customers, SSO integration is available:

- SAML 2.0 support
- OpenID Connect support
- Just-in-time user provisioning
- Role mapping from identity provider

### VPN and Private Link

For enhanced security:

- Site-to-site VPN connection
- AWS PrivateLink / Azure Private Link support
- Dedicated endpoints for enterprise customers

### Data Residency

Options for data sovereignty requirements:

- US region (default)
- EU region
- Custom region deployment (Enterprise tier)

## Testing & Validation

### Sandbox Environment

A sandbox environment is available for testing:

- Base URL: `https://sandbox-api.goliath-quantum.com/v1`
- Test API keys available in developer portal
- Simulated job execution with faster response times
- Reset daily at 00:00 UTC

### Integration Testing

Recommended testing approach:

1. Unit test your integration code
2. Use mock responses for initial testing
3. Test with sandbox environment
4. Perform end-to-end testing with small jobs
5. Validate error handling with intentional errors
6. Load test with realistic job volumes

### Validation Checklist

Before going live:

- Authentication works correctly
- Job submission and retrieval functions properly
- Error handling is robust
- Rate limiting is respected
- Webhook processing is reliable
- Data validation is thorough
- Monitoring is in place

## Monitoring & Troubleshooting

### Logging Best Practices

Implement comprehensive logging:

- Log all API requests and responses
- Include request IDs in logs
- Use structured logging format
- Implement different log levels (DEBUG, INFO, ERROR)
- Retain logs for at least 30 days

### Monitoring Metrics

Key metrics to monitor:

- API response times
- Error rates by endpoint
- Job success/failure rates
- Webhook delivery success
- Rate limit usage

### Troubleshooting Tools

Available in the developer portal:

- Request logs (last 7 days)
- Job execution history
- Webhook delivery logs
- System status dashboard
- API usage metrics

## Support Resources

### Developer Support

- Developer portal: https://developers.goliath-quantum.com
- API documentation: https://api-docs.goliath-quantum.com
- Support email: api-support@goliath-quantum.com
- Developer forum: https://community.goliath-quantum.com

### SLA Information

Support response times:

- Standard tier: 24 business hours
- Professional tier: 8 business hours
- Enterprise tier: 4 business hours, 24/7 for critical issues

## Versioning & Deprecation

### API Versioning

The API uses semantic versioning:

- Major version in URL path (`/v1/`, `/v2/`)
- Minor and patch versions transparent to clients
- Breaking changes only in major version updates

### Deprecation Policy

- 12-month deprecation period for major versions
- Deprecated endpoints marked in documentation
- Deprecation notices sent via email
- Migration guides provided for version transitions

---

*Last Updated: July 2023*  
*Document Version: 1.2*  
*Contact: integration-support@goliath-quantum.com*