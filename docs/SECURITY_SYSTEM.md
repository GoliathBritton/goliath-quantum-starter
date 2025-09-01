# NQBA Security System

## Overview

The NQBA Security System provides enterprise-grade security, privacy, and compliance capabilities for the NQBA ecosystem. It implements a comprehensive security framework that addresses modern cybersecurity challenges while maintaining compliance with regulatory requirements.

## Architecture

The security system is built on a layered architecture with the following components:

```
┌─────────────────────────────────────────────────────────────┐
│                    Security API Layer                      │
├─────────────────────────────────────────────────────────────┤
│                 Security Orchestrator                      │
├─────────────────────────────────────────────────────────────┤
│  KMS  │  Encryption  │   IAM   │  Audit   │ Compliance   │
│Manager│   Manager    │ Manager │ Logger   │  Manager     │
├─────────────────────────────────────────────────────────────┤
│                 Cryptographic Layer                        │
├─────────────────────────────────────────────────────────────┤
│                 Storage & Persistence                      │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. KMS Manager (`kms_manager.py`)

**Purpose**: Centralized secrets management with automatic rotation and multi-cloud support.

**Features**:
- **Multi-cloud Support**: AWS KMS, GCP KMS, Azure Key Vault, HCP Vault
- **Automatic Rotation**: 90-day rotation with configurable policies
- **Secret Lifecycle**: Create, read, update, delete with full audit trail
- **Fallback Support**: Local encryption for development/testing

**Key Classes**:
- `KMSManager`: Main manager class
- `SecretMetadata`: Secret metadata and lifecycle information
- `RotationPolicy`: Configurable rotation policies

**Usage Example**:
```python
from src.nqba_stack.security.kms_manager import kms_manager

# Create a secret
secret_id = await kms_manager.create_secret(
    name="database_password",
    value="secure_password_123",
    description="Database connection password"
)

# Retrieve secret
password = await kms_manager.get_secret(secret_id)

# Check rotation status
status = await kms_manager.get_rotation_status()
```

### 2. Encryption Manager (`encryption_manager.py`)

**Purpose**: Multi-tenant data encryption with field-level PII protection.

**Features**:
- **Multi-tenant Isolation**: Separate encryption keys per tenant
- **Field-level Encryption**: PII-specific encryption for sensitive fields
- **Encryption Levels**: None, Basic, Enhanced, PII, Critical
- **Key Rotation**: Automatic key rotation with data preservation
- **Data Types**: Support for strings, bytes, dictionaries, and objects

**Key Classes**:
- `EncryptionManager`: Main encryption orchestrator
- `TenantEncryptionConfig`: Tenant-specific encryption settings
- `EncryptionKey`: Encryption key with metadata

**Usage Example**:
```python
from src.nqba_stack.security.encryption_manager import encryption_manager

# Create tenant
tenant_id = "acme_corp"
master_key_id = encryption_manager.create_tenant(
    tenant_id=tenant_id,
    encryption_level=EncryptionLevel.ENHANCED
)

# Add PII fields
encryption_manager.add_pii_field(tenant_id, "ssn")
encryption_manager.add_pii_field(tenant_id, "credit_card")

# Encrypt data
user_data = {
    "name": "John Doe",
    "ssn": "123-45-6789",
    "credit_card": "4111-1111-1111-1111"
}

encrypted_data = encryption_manager.encrypt_data(user_data, tenant_id)
decrypted_data = encryption_manager.decrypt_data(encrypted_data, tenant_id)
```

### 3. IAM Manager (`iam_manager.py`)

**Purpose**: Identity and access management with role-based permissions and API key management.

**Features**:
- **Organization Management**: Multi-tenant organization support
- **Role-based Access Control**: Hierarchical role system (Owner, Admin, Analyst, Viewer, Bot)
- **API Key Management**: Scoped API keys with rate limiting
- **Permission System**: Granular permission control
- **User Lifecycle**: Create, update, delete users with audit trail

**Key Classes**:
- `IAMManager`: Main IAM orchestrator
- `Organization`: Organization entity with settings
- `User`: User entity with roles and permissions
- `APIKey`: API key with scopes and rate limits

**Role Hierarchy**:
```
OWNER (Full access)
├── ADMIN (Management access)
├── ANALYST (Data access + write)
├── VIEWER (Read-only access)
└── BOT (Automated access)
```

**Usage Example**:
```python
from src.nqba_stack.security.iam_manager import iam_manager, RoleLevel

# Create organization
org_result = iam_manager.create_organization(
    name="Acme Corp",
    domain="acme.com",
    owner_email="owner@acme.com",
    owner_username="owner"
)

# Create user
user_result = iam_manager.create_user(
    org_id=org_result["org_id"],
    email="analyst@acme.com",
    username="analyst",
    role=RoleLevel.ANALYST
)

# Create API key
key_result = iam_manager.create_api_key(
    user_id=user_result["user_id"],
    name="Analytics API Key",
    rate_limit_per_minute=100
)

# Check permissions
can_read = iam_manager.check_permission(
    user_result["user_id"], 
    Permission.DATA_READ
)
```

### 4. Audit Logger (`audit_logger.py`)

**Purpose**: Comprehensive audit logging with blockchain-like integrity and IPFS export.

**Features**:
- **Append-only Logs**: Immutable audit trail
- **Hash Chain**: Cryptographic chain of events
- **Digital Signatures**: RSA-signed audit entries
- **Merkle Trees**: Efficient integrity verification
- **IPFS Export**: Decentralized audit log storage
- **Event Types**: Comprehensive event categorization
- **Search & Filtering**: Advanced audit log querying

**Key Classes**:
- `AuditLogger`: Main audit logging orchestrator
- `AuditEvent`: Individual audit event
- `AuditLogEntry`: Complete audit log entry with verification

**Event Types**:
- **Authentication**: Login, logout, user management
- **API Events**: API calls, key management
- **Data Events**: Read, write, delete, export
- **Quantum Events**: Job submission, completion, failure
- **Security Events**: Permission changes, role updates
- **Compliance Events**: Compliance checks, regulatory reports

**Usage Example**:
```python
from src.nqba_stack.security.audit_logger import audit_logger, AuditEventType, AuditSeverity

# Log security event
event_id = audit_logger.log_event(
    event_type=AuditEventType.USER_LOGIN,
    severity=AuditSeverity.LOW,
    user_id="user_123",
    org_id="org_456",
    session_id="session_789",
    ip_address="192.168.1.100",
    user_agent="Chrome/91.0",
    resource_type="authentication",
    resource_id="login_form",
    action="user_login",
    details={"method": "password", "success": True}
)

# Verify chain integrity
integrity = audit_logger.verify_chain_integrity()
assert integrity["valid"] is True

# Search audit logs
results = audit_logger.search_audit_log(
    user_id="user_123",
    event_type=AuditEventType.USER_LOGIN
)
```

### 5. Compliance Manager (`compliance_manager.py`)

**Purpose**: Regulatory compliance management for SOC 2, GDPR/CCPA, and SFG insurance.

**Features**:
- **SOC 2 Controls**: Type 1 and Type 2 control assessment
- **GDPR/CCPA**: Data flow mapping and consent management
- **SFG Insurance**: State-specific compliance requirements
- **Compliance Monitoring**: Automated compliance checking
- **Report Generation**: Comprehensive compliance reports
- **Risk Assessment**: Integrated risk management

**Key Classes**:
- `ComplianceManager`: Main compliance orchestrator
- `SOC2Control`: SOC 2 control definition and assessment
- `DataFlow`: GDPR/CCPA data flow mapping
- `ConsentRecord`: Consent management and tracking
- `SFGCompliance`: SFG insurance compliance requirements

**Usage Example**:
```python
from src.nqba_stack.security.compliance_manager import (
    compliance_manager, ComplianceFramework, DataSubjectType, DataProcessingPurpose
)

# Assess SOC 2 control
success = compliance_manager.assess_soc2_control(
    control_id="CC1.1",
    assessment_data={
        "is_implemented": True,
        "risk_level": "low"
    }
)

# Record GDPR consent
consent_id = compliance_manager.record_consent(
    data_subject_id="user_123",
    data_subject_type=DataSubjectType.INDIVIDUAL,
    purpose=DataProcessingPurpose.MARKETING,
    consent_given=True,
    consent_method="web_form",
    legal_basis="consent",
    data_categories=["contact_information"],
    third_parties=["email_service"]
)

# Generate compliance report
soc2_report = compliance_manager.generate_compliance_report(
    ComplianceFramework.SOC2_TYPE2
)
```

## Security Features

### Data Protection

- **Encryption at Rest**: AES-256 encryption for all stored data
- **Encryption in Transit**: TLS 1.3 for all communications
- **Field-level Encryption**: PII-specific encryption for sensitive data
- **Key Management**: Centralized key management with rotation

### Access Control

- **Multi-factor Authentication**: Support for MFA implementation
- **Role-based Access**: Granular permission system
- **API Key Scoping**: Limited API access based on user permissions
- **Rate Limiting**: Configurable rate limits per API key

### Audit & Compliance

- **Immutable Logs**: Append-only audit trail with cryptographic verification
- **Digital Signatures**: RSA-signed audit entries
- **Chain Integrity**: Hash chain verification for log integrity
- **IPFS Storage**: Decentralized audit log storage
- **Compliance Mapping**: SOC 2, GDPR/CCPA, SFG insurance compliance

### Threat Protection

- **Circuit Breakers**: Automatic failure detection and isolation
- **Rate Limiting**: DDoS protection through API rate limiting
- **Input Validation**: Comprehensive input sanitization and validation
- **Session Management**: Secure session handling with timeouts

## Configuration

### Environment Variables

```bash
# KMS Configuration
NQBA_MASTER_KEY=your_master_key_here
AWS_KMS_KEY_ID=your_aws_kms_key_id
GCP_PROJECT_ID=your_gcp_project_id
AZURE_KEYVAULT_URL=your_azure_keyvault_url
HCP_VAULT_URL=your_hcp_vault_url
HCP_VAULT_TOKEN=your_hcp_vault_token

# Encryption Configuration
ENCRYPTION_LEVEL=enhanced
DEFAULT_TENANT_ENCRYPTION=enhanced

# Audit Configuration
AUDIT_PRIVATE_KEY_PATH=/path/to/private/key
AUDIT_SIGNING_ENABLED=true
IPFS_EXPORT_ENABLED=true

# Compliance Configuration
SOC2_ASSESSMENT_INTERVAL_DAYS=90
GDPR_CONSENT_VERSION=1.0
SFG_REVIEW_INTERVAL_DAYS=30
```

### Security Policies

```python
# Example security policy configuration
SECURITY_POLICIES = {
    "password_policy": {
        "min_length": 12,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_numbers": True,
        "require_special": True,
        "max_age_days": 90
    },
    "session_policy": {
        "timeout_minutes": 480,
        "max_concurrent_sessions": 3,
        "require_mfa": True
    },
    "api_policy": {
        "default_rate_limit_per_minute": 100,
        "default_rate_limit_per_hour": 1000,
        "max_api_keys_per_user": 10
    }
}
```

## Integration

### API Integration

The security system integrates with the main NQBA API through middleware and decorators:

```python
from fastapi import FastAPI, Depends
from src.nqba_stack.security.iam_manager import iam_manager
from src.nqba_stack.security.audit_logger import audit_logger

app = FastAPI()

@app.middleware("http")
async def security_middleware(request, call_next):
    # API key validation
    api_key = request.headers.get("X-API-Key")
    if api_key:
        validation = iam_manager.validate_api_key(api_key)
        if validation:
            request.state.user_id = validation["user_id"]
            request.state.org_id = validation["org_id"]
    
    # Rate limiting
    if hasattr(request.state, "user_id"):
        key_id = validation["key_id"]
        if not iam_manager.check_rate_limit(key_id):
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )
    
    response = await call_next(request)
    
    # Audit logging
    if hasattr(request.state, "user_id"):
        audit_logger.log_event(
            event_type=AuditEventType.API_CALL,
            severity=AuditSeverity.LOW,
            user_id=request.state.user_id,
            org_id=request.state.org_id,
            session_id=request.headers.get("X-Session-ID"),
            ip_address=request.client.host,
            user_agent=request.headers.get("User-Agent"),
            resource_type="api",
            resource_id=request.url.path,
            action=request.method,
            details={"status_code": response.status_code}
        )
    
    return response
```

### Business Unit Integration

Security components integrate with business units for data protection:

```python
from src.nqba_stack.security.encryption_manager import encryption_manager
from src.nqba_stack.security.audit_logger import audit_logger

class FLYFOXAIBusinessUnit:
    def __init__(self, org_id: str):
        self.org_id = org_id
        self.tenant_id = f"flyfox_ai_{org_id}"
        
        # Ensure tenant exists for encryption
        if not encryption_manager.get_tenant_status(self.tenant_id):
            encryption_manager.create_tenant(
                tenant_id=self.tenant_id,
                encryption_level=EncryptionLevel.ENHANCED
            )
    
    def process_sensitive_data(self, data: dict):
        # Encrypt sensitive data
        encrypted_data = encryption_manager.encrypt_data(data, self.tenant_id)
        
        # Log data processing
        audit_logger.log_event(
            event_type=AuditEventType.DATA_WRITE,
            severity=AuditSeverity.MEDIUM,
            user_id="system",
            org_id=self.org_id,
            session_id="system_session",
            ip_address="127.0.0.1",
            user_agent="FLYFOX_AI_System",
            resource_type="business_unit",
            resource_id="flyfox_ai",
            action="data_processing",
            details={"data_type": "sensitive", "encrypted": True}
        )
        
        return encrypted_data
```

## Monitoring & Alerting

### Security Metrics

The security system provides comprehensive metrics for monitoring:

```python
# Get security system status
security_status = {
    "kms": await kms_manager.get_rotation_status(),
    "encryption": encryption_manager.get_global_status(),
    "iam": iam_manager.get_system_status(),
    "audit": audit_logger.get_audit_statistics(),
    "compliance": {
        "soc2": compliance_manager.get_soc2_status(),
        "gdpr_ccpa": compliance_manager.get_gdpr_ccpa_status(),
        "sfg": compliance_manager.get_sfg_compliance_status()
    }
}
```

### Alerting Rules

```python
# Example alerting rules
ALERTING_RULES = {
    "failed_login_attempts": {
        "threshold": 5,
        "time_window": "5 minutes",
        "severity": "high"
    },
    "api_rate_limit_exceeded": {
        "threshold": 10,
        "time_window": "1 minute",
        "severity": "medium"
    },
    "secrets_needing_rotation": {
        "threshold": 1,
        "time_window": "1 day",
        "severity": "high"
    },
    "compliance_assessments_overdue": {
        "threshold": 1,
        "time_window": "1 day",
        "severity": "high"
    }
}
```

## Deployment

### Production Deployment

```yaml
# docker-compose.security.yml
version: '3.8'
services:
  nqba-security:
    build: .
    environment:
      - NQBA_MASTER_KEY=${NQBA_MASTER_KEY}
      - AWS_KMS_KEY_ID=${AWS_KMS_KEY_ID}
      - GCP_PROJECT_ID=${GCP_PROJECT_ID}
      - AZURE_KEYVAULT_URL=${AZURE_KEYVAULT_URL}
      - HCP_VAULT_URL=${HCP_VAULT_URL}
      - HCP_VAULT_TOKEN=${HCP_VAULT_TOKEN}
    volumes:
      - ./keys:/app/keys
      - ./logs:/app/logs
    ports:
      - "8001:8000"
    depends_on:
      - redis
      - postgres
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
  
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=nqba_security
      - POSTGRES_USER=nqba_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### Security Hardening

```bash
# Security hardening script
#!/bin/bash

# Update system packages
apt-get update && apt-get upgrade -y

# Install security tools
apt-get install -y fail2ban ufw auditd

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 8000/tcp
ufw enable

# Configure fail2ban
systemctl enable fail2ban
systemctl start fail2ban

# Configure auditd
systemctl enable auditd
systemctl start auditd

# Set secure file permissions
chmod 600 /app/keys/*
chmod 644 /app/config/*
chmod 755 /app/logs
```

## Testing

### Security Testing

```bash
# Run security tests
pytest tests/test_security_system.py -v

# Run specific security component tests
pytest tests/test_security_system.py::TestKMSManager -v
pytest tests/test_security_system.py::TestEncryptionManager -v
pytest tests/test_security_system.py::TestIAMManager -v
pytest tests/test_security_system.py::TestAuditLogger -v
pytest tests/test_security_system.py::TestComplianceManager -v

# Run integration tests
pytest tests/test_security_system.py::TestSecurityIntegration -v
```

### Penetration Testing

```bash
# Run security scan
bandit -r src/nqba_stack/security/
safety check
pip-audit

# Run OWASP ZAP scan
zap-baseline.py -t http://localhost:8000

# Run dependency vulnerability scan
snyk test
```

## Compliance

### SOC 2 Type 2

The security system implements SOC 2 Type 2 controls:

- **CC1.1**: Control Environment
- **CC2.1**: Communication and Information
- **CC3.1**: Risk Assessment
- **CC4.1**: Control Activities
- **CC5.1**: Monitoring Activities

### GDPR/CCPA

- **Data Minimization**: Only collect necessary data
- **Consent Management**: Comprehensive consent tracking
- **Data Subject Rights**: Support for data subject requests
- **Data Flow Mapping**: Complete data flow documentation
- **Third-party Assessment**: Vendor compliance tracking

### SFG Insurance

- **State Licensing**: State-specific compliance requirements
- **Disclosure Requirements**: Client and regulatory disclosures
- **Data Privacy**: State data privacy law compliance
- **Risk Assessment**: Integrated risk management

## Troubleshooting

### Common Issues

1. **KMS Connection Failures**
   - Check cloud provider credentials
   - Verify network connectivity
   - Check IAM permissions

2. **Encryption Errors**
   - Verify tenant configuration
   - Check encryption key status
   - Validate data format

3. **IAM Permission Issues**
   - Check user role assignments
   - Verify permission inheritance
   - Check API key scopes

4. **Audit Log Issues**
   - Check cryptographic key status
   - Verify IPFS connectivity
   - Check disk space for logs

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable security component debugging
from src.nqba_stack.security import kms_manager, encryption_manager, iam_manager, audit_logger, compliance_manager

# Set debug mode
kms_manager.debug = True
encryption_manager.debug = True
iam_manager.debug = True
audit_logger.debug = True
compliance_manager.debug = True
```

## Future Enhancements

### Planned Features

1. **Zero-Knowledge Proofs**: Privacy-preserving authentication
2. **Homomorphic Encryption**: Encrypted data processing
3. **Quantum-Resistant Cryptography**: Post-quantum security
4. **Behavioral Analytics**: Advanced threat detection
5. **Blockchain Integration**: Decentralized identity management

### Roadmap

- **Q1 2024**: Advanced threat detection
- **Q2 2024**: Quantum-resistant cryptography
- **Q3 2024**: Zero-knowledge proofs
- **Q4 2024**: Blockchain identity management

## Support

### Documentation

- [Security API Reference](api/security.md)
- [Compliance Guidelines](compliance/guidelines.md)
- [Security Best Practices](security/best-practices.md)
- [Incident Response](security/incident-response.md)

### Contact

- **Security Team**: security@nqba.com
- **Compliance Team**: compliance@nqba.com
- **Emergency**: +1-555-SECURITY

### Reporting Security Issues

Please report security vulnerabilities to security@nqba.com. We follow responsible disclosure practices and will acknowledge receipt within 24 hours.
