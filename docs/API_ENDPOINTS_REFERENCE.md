# API Endpoints Reference

## Overview

This document provides a comprehensive reference of all API endpoints available in the Goliath Quantum Platform. It includes authentication requirements, request/response formats, error codes, and usage examples.

## Authentication

All API requests require authentication using one of the following methods:

### API Key Authentication

```http
GET /api/v1/jobs
Authorization: ApiKey YOUR_API_KEY
```

### OAuth 2.0

```http
GET /api/v1/jobs
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## Core Endpoints

### User Management

#### Create User

```
POST /api/v1/users
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "firstName": "John",
  "lastName": "Doe",
  "organization": "Acme Inc."
}
```

**Response:**
```json
{
  "userId": "usr_123456789",
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "organization": "Acme Inc.",
  "createdAt": "2023-07-01T12:00:00Z"
}
```

**Status Codes:**
- 201: User created successfully
- 400: Invalid request parameters
- 409: User already exists

#### Get User

```
GET /api/v1/users/{userId}
```

**Response:**
```json
{
  "userId": "usr_123456789",
  "email": "user@example.com",
  "firstName": "John",
  "lastName": "Doe",
  "organization": "Acme Inc.",
  "createdAt": "2023-07-01T12:00:00Z",
  "lastLoginAt": "2023-07-02T09:30:00Z"
}
```

**Status Codes:**
- 200: Success
- 404: User not found

#### Update User

```
PATCH /api/v1/users/{userId}
```

**Request Body:**
```json
{
  "firstName": "Jonathan",
  "organization": "Quantum Solutions Ltd."
}
```

**Response:**
```json
{
  "userId": "usr_123456789",
  "email": "user@example.com",
  "firstName": "Jonathan",
  "lastName": "Doe",
  "organization": "Quantum Solutions Ltd.",
  "updatedAt": "2023-07-03T15:45:00Z"
}
```

**Status Codes:**
- 200: User updated successfully
- 400: Invalid request parameters
- 404: User not found

#### Delete User

```
DELETE /api/v1/users/{userId}
```

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

**Status Codes:**
- 200: User deleted successfully
- 404: User not found

### Quantum Jobs

#### Submit Job

```
POST /api/v1/jobs
```

**Request Body:**
```json
{
  "name": "Bell State Generation",
  "description": "Creating and measuring a Bell state",
  "circuit": "OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[2];\ncreg c[2];\nh q[0];\ncx q[0],q[1];\nmeasure q -> c;",
  "backend": "simulator_statevector",
  "shots": 1024,
  "priority": "normal"
}
```

**Response:**
```json
{
  "jobId": "job_987654321",
  "name": "Bell State Generation",
  "status": "QUEUED",
  "submittedAt": "2023-07-04T10:15:00Z",
  "estimatedStartTime": "2023-07-04T10:16:00Z"
}
```

**Status Codes:**
- 201: Job submitted successfully
- 400: Invalid request parameters
- 402: Insufficient credits
- 429: Rate limit exceeded

#### Get Job Status

```
GET /api/v1/jobs/{jobId}
```

**Response:**
```json
{
  "jobId": "job_987654321",
  "name": "Bell State Generation",
  "status": "RUNNING",
  "submittedAt": "2023-07-04T10:15:00Z",
  "startedAt": "2023-07-04T10:16:30Z",
  "estimatedCompletionTime": "2023-07-04T10:17:30Z",
  "progress": 45
}
```

**Status Codes:**
- 200: Success
- 404: Job not found

#### Get Job Results

```
GET /api/v1/jobs/{jobId}/results
```

**Response:**
```json
{
  "jobId": "job_987654321",
  "status": "COMPLETED",
  "results": {
    "counts": {
      "00": 512,
      "11": 498,
      "01": 7,
      "10": 7
    },
    "executionTime": 1.25,
    "memory": ["00", "11", "00", "11", "..."]
  },
  "submittedAt": "2023-07-04T10:15:00Z",
  "completedAt": "2023-07-04T10:17:45Z"
}
```

**Status Codes:**
- 200: Success
- 404: Job not found
- 409: Results not available yet

#### Cancel Job

```
POST /api/v1/jobs/{jobId}/cancel
```

**Response:**
```json
{
  "jobId": "job_987654321",
  "status": "CANCELLED",
  "message": "Job cancelled successfully"
}
```

**Status Codes:**
- 200: Job cancelled successfully
- 404: Job not found
- 409: Job cannot be cancelled (already completed or running)

### Quantum Backends

#### List Available Backends

```
GET /api/v1/backends
```

**Response:**
```json
{
  "backends": [
    {
      "id": "simulator_statevector",
      "name": "Statevector Simulator",
      "description": "Ideal statevector simulator",
      "status": "ONLINE",
      "qubits": 32,
      "simulator": true,
      "availableGates": ["h", "x", "y", "z", "cx", "cz", "t", "s"]
    },
    {
      "id": "quantum_processor_v1",
      "name": "Quantum Processor V1",
      "description": "5-qubit superconducting quantum processor",
      "status": "ONLINE",
      "qubits": 5,
      "simulator": false,
      "availableGates": ["h", "x", "y", "z", "cx", "cz"],
      "topology": [[0,1], [1,2], [2,3], [3,4], [0,4]],
      "queueSize": 12,
      "estimatedWaitTime": 300
    }
  ]
}
```

**Status Codes:**
- 200: Success

#### Get Backend Details

```
GET /api/v1/backends/{backendId}
```

**Response:**
```json
{
  "id": "quantum_processor_v1",
  "name": "Quantum Processor V1",
  "description": "5-qubit superconducting quantum processor",
  "status": "ONLINE",
  "qubits": 5,
  "simulator": false,
  "availableGates": ["h", "x", "y", "z", "cx", "cz"],
  "topology": [[0,1], [1,2], [2,3], [3,4], [0,4]],
  "queueSize": 12,
  "estimatedWaitTime": 300,
  "calibrationData": {
    "lastCalibration": "2023-07-01T00:00:00Z",
    "gateErrors": {
      "h": [0.001, 0.0012, 0.0009, 0.0011, 0.001],
      "cx": [0.015, 0.018, 0.016, 0.017, 0.019]
    },
    "readoutErrors": [0.02, 0.018, 0.022, 0.019, 0.021],
    "t1Times": [50.5, 48.2, 52.1, 49.8, 51.3],
    "t2Times": [30.2, 28.5, 31.0, 29.7, 30.5]
  }
}
```

**Status Codes:**
- 200: Success
- 404: Backend not found

### Account Management

#### Get Account Information

```
GET /api/v1/account
```

**Response:**
```json
{
  "accountId": "acc_123456789",
  "name": "Acme Inc.",
  "plan": "ENTERPRISE",
  "credits": 5000,
  "usedCredits": 1250,
  "createdAt": "2023-01-01T00:00:00Z",
  "status": "ACTIVE"
}
```

**Status Codes:**
- 200: Success

#### Get Usage History

```
GET /api/v1/account/usage
```

**Query Parameters:**
- `startDate`: ISO date string (required)
- `endDate`: ISO date string (required)
- `granularity`: "day" | "week" | "month" (optional, default: "day")

**Response:**
```json
{
  "usage": [
    {
      "date": "2023-07-01",
      "creditsUsed": 120,
      "jobsSubmitted": 15,
      "computeTimeSeconds": 3600
    },
    {
      "date": "2023-07-02",
      "creditsUsed": 85,
      "jobsSubmitted": 10,
      "computeTimeSeconds": 2400
    }
  ],
  "totalCreditsUsed": 205,
  "totalJobsSubmitted": 25,
  "totalComputeTimeSeconds": 6000
}
```

**Status Codes:**
- 200: Success
- 400: Invalid date range

## Integration Endpoints

### Webhooks

#### Register Webhook

```
POST /api/v1/webhooks
```

**Request Body:**
```json
{
  "url": "https://example.com/webhook",
  "events": ["job.completed", "job.failed", "account.low_credits"],
  "secret": "webhookSecret123"
}
```

**Response:**
```json
{
  "webhookId": "wh_123456789",
  "url": "https://example.com/webhook",
  "events": ["job.completed", "job.failed", "account.low_credits"],
  "createdAt": "2023-07-05T14:30:00Z",
  "status": "ACTIVE"
}
```

**Status Codes:**
- 201: Webhook registered successfully
- 400: Invalid request parameters

#### List Webhooks

```
GET /api/v1/webhooks
```

**Response:**
```json
{
  "webhooks": [
    {
      "webhookId": "wh_123456789",
      "url": "https://example.com/webhook",
      "events": ["job.completed", "job.failed", "account.low_credits"],
      "createdAt": "2023-07-05T14:30:00Z",
      "status": "ACTIVE"
    }
  ]
}
```

**Status Codes:**
- 200: Success

#### Delete Webhook

```
DELETE /api/v1/webhooks/{webhookId}
```

**Response:**
```json
{
  "message": "Webhook deleted successfully"
}
```

**Status Codes:**
- 200: Webhook deleted successfully
- 404: Webhook not found

### SSO Integration

#### Configure SSO

```
POST /api/v1/account/sso
```

**Request Body:**
```json
{
  "provider": "okta",
  "entityId": "https://example.okta.com",
  "ssoUrl": "https://example.okta.com/app/example/sso/saml",
  "x509cert": "-----BEGIN CERTIFICATE-----\nMIIDpDCCAowCCQDsw5A5AjQrADANBgkq...\n-----END CERTIFICATE-----"
}
```

**Response:**
```json
{
  "status": "CONFIGURED",
  "spEntityId": "https://api.goliath-quantum.com/saml/metadata",
  "acsUrl": "https://api.goliath-quantum.com/api/v1/auth/saml/callback",
  "createdAt": "2023-07-06T09:00:00Z"
}
```

**Status Codes:**
- 200: SSO configured successfully
- 400: Invalid configuration parameters

## Data Management

### Datasets

#### Upload Dataset

```
POST /api/v1/datasets
```

**Request Body:**
Multipart form data with:
- `name`: Dataset name
- `description`: Dataset description
- `file`: Dataset file (CSV, JSON, or binary)
- `format`: File format
- `isPublic`: Boolean indicating if dataset is public

**Response:**
```json
{
  "datasetId": "ds_123456789",
  "name": "Quantum Optimization Dataset",
  "description": "Sample dataset for quantum optimization problems",
  "format": "CSV",
  "size": 1048576,
  "isPublic": false,
  "createdAt": "2023-07-07T11:20:00Z"
}
```

**Status Codes:**
- 201: Dataset uploaded successfully
- 400: Invalid request parameters
- 413: File too large

#### List Datasets

```
GET /api/v1/datasets
```

**Query Parameters:**
- `isPublic`: Boolean (optional)
- `format`: String (optional)
- `limit`: Integer (optional, default: 20)
- `offset`: Integer (optional, default: 0)

**Response:**
```json
{
  "datasets": [
    {
      "datasetId": "ds_123456789",
      "name": "Quantum Optimization Dataset",
      "description": "Sample dataset for quantum optimization problems",
      "format": "CSV",
      "size": 1048576,
      "isPublic": false,
      "createdAt": "2023-07-07T11:20:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

**Status Codes:**
- 200: Success

## Error Handling

### Error Response Format

All API errors follow this format:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "The requested resource was not found",
    "details": {
      "resourceType": "Job",
      "resourceId": "job_nonexistent"
    },
    "requestId": "req_abcdef123456"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| AUTHENTICATION_FAILED | 401 | Invalid or missing authentication credentials |
| AUTHORIZATION_FAILED | 403 | Insufficient permissions to access resource |
| RESOURCE_NOT_FOUND | 404 | The requested resource does not exist |
| VALIDATION_ERROR | 400 | Request validation failed |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests in a given time period |
| INSUFFICIENT_CREDITS | 402 | Account has insufficient credits |
| INTERNAL_SERVER_ERROR | 500 | Unexpected server error |

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Standard Plan**: 100 requests per minute
- **Professional Plan**: 500 requests per minute
- **Enterprise Plan**: 2000 requests per minute

Rate limit headers are included in all responses:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1625097600
```

## Versioning

The API uses versioning in the URL path (e.g., `/api/v1/`). When breaking changes are introduced, a new version will be released.

## SDK Libraries

Official SDK libraries are available for:

- Python: [GitHub Repository](https://github.com/goliath-quantum/python-sdk)
- JavaScript: [GitHub Repository](https://github.com/goliath-quantum/js-sdk)
- Java: [GitHub Repository](https://github.com/goliath-quantum/java-sdk)

## Appendix

### Webhook Event Types

| Event Type | Description |
|------------|-------------|
| job.created | A new job has been created |
| job.queued | A job has been queued for processing |
| job.running | A job has started running |
| job.completed | A job has completed successfully |
| job.failed | A job has failed |
| job.cancelled | A job has been cancelled |
| account.low_credits | Account credits are below threshold |
| backend.status_changed | Backend status has changed |

### Webhook Payload Format

```json
{
  "event": "job.completed",
  "timestamp": "2023-07-08T15:45:30Z",
  "data": {
    "jobId": "job_987654321",
    "status": "COMPLETED",
    "submittedAt": "2023-07-08T15:40:00Z",
    "completedAt": "2023-07-08T15:45:30Z"
  }
}
```

---

*Last Updated: July 2023*  
*API Version: v1*  
*Contact: api-support@goliath-quantum.com*