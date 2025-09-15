"""Security module for Goliath Quantum Starter

This module provides comprehensive security features including:
- Compliance management (GDPR, CCPA, HIPAA, SOC2, ISO27001)
- PII encryption and data anonymization
- Audit logging and event tracking
- Rate limiting with adaptive algorithms
- Security middleware with IP filtering and threat detection
"""

from .compliance import (
    ComplianceFramework,
    DataClassification,
    AuditEvent,
    PIIField,
    ComplianceConfig,
    PIIEncryption,
    AuditLogger,
    ComplianceEngine,
    compliance_engine,
    DEFAULT_COMPLIANCE_CONFIG
)

from .rate_limiter import (
    RateLimitType,
    RateLimit,
    RateLimitResult,
    RateLimitConfig,
    InMemoryRateLimiter,
    RedisRateLimiter,
    AdaptiveRateLimiter,
    RateLimitManager,
    RateLimitExceeded,
    rate_limit_manager
)

from .middleware import (
    SecurityMiddleware,
    security_middleware
)

__all__ = [
    # Compliance
    'ComplianceFramework',
    'DataClassification',
    'AuditEvent',
    'PIIField',
    'ComplianceConfig',
    'PIIEncryption',
    'AuditLogger',
    'ComplianceEngine',
    'compliance_engine',
    'DEFAULT_COMPLIANCE_CONFIG',
    
    # Rate Limiting
    'RateLimitType',
    'RateLimit',
    'RateLimitResult',
    'RateLimitConfig',
    'InMemoryRateLimiter',
    'RedisRateLimiter',
    'AdaptiveRateLimiter',
    'RateLimitManager',
    'RateLimitExceeded',
    'rate_limit_manager',
    
    # Middleware
    'SecurityMiddleware',
    'security_middleware'
]

# Version information
__version__ = '1.0.0'
__author__ = 'Goliath Quantum Team'
__description__ = 'Comprehensive security framework for quantum applications'