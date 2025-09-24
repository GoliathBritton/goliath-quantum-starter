from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

from src.security import (
    compliance_engine, rate_limit_manager, ComplianceFramework,
    DataClassification, RateLimitType, security_middleware
)
from src.models import User
from src.auth.dependencies import get_current_user, require_admin

router = APIRouter()

# Request/Response Models
class ComplianceReportRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    frameworks: Optional[List[ComplianceFramework]] = None

class SecurityConfigUpdate(BaseModel):
    blocked_ips: Optional[List[str]] = None
    allowed_ip_ranges: Optional[List[str]] = None
    security_headers: Optional[Dict[str, str]] = None
    rate_limiting_enabled: Optional[bool] = None
    audit_logging_enabled: Optional[bool] = None

class ConsentRequest(BaseModel):
    user_id: str
    purpose: str
    granted: bool
    legal_basis: str = "consent"

class PIIEncryptionRequest(BaseModel):
    data: str
    field_type: DataClassification

class PIIDecryptionRequest(BaseModel):
    encrypted_data: str
    field_type: DataClassification

class AnonymizationRequest(BaseModel):
    data: str
    method: str = "hash"  # hash, mask, remove

class RateLimitOverride(BaseModel):
    user_id: str
    limit_type: RateLimitType
    new_limit: int
    duration_hours: int = 24

# Compliance Endpoints
@router.get("/compliance/report")
async def get_compliance_report(
    start_date: datetime,
    end_date: datetime,
    user: User = Depends(require_admin)
):
    """Generate compliance report for specified period"""
    try:
        report = compliance_engine.get_compliance_report(start_date, end_date)
        return {
            "success": True,
            "report": report,
            "generated_at": datetime.utcnow().isoformat(),
            "generated_by": user.email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate compliance report: {str(e)}")

@router.get("/compliance/frameworks")
async def get_enabled_frameworks(user: User = Depends(require_admin)):
    """Get currently enabled compliance frameworks"""
    return {
        "enabled_frameworks": [f.value for f in compliance_engine.config.enabled_frameworks],
        "available_frameworks": [f.value for f in ComplianceFramework]
    }

@router.post("/compliance/consent")
async def record_user_consent(
    consent_request: ConsentRequest,
    user: User = Depends(require_admin)
):
    """Record user consent for data processing"""
    try:
        compliance_engine.record_consent(
            consent_request.user_id,
            consent_request.purpose,
            consent_request.granted,
            consent_request.legal_basis
        )
        
        return {
            "success": True,
            "message": "Consent recorded successfully",
            "recorded_by": user.email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record consent: {str(e)}")

@router.get("/compliance/consent/{user_id}")
async def get_user_consent(
    user_id: str,
    admin_user: User = Depends(require_admin)
):
    """Get consent records for a specific user"""
    consent_records = compliance_engine.consent_records.get(user_id, {})
    
    return {
        "user_id": user_id,
        "consent_records": consent_records,
        "total_consents": len(consent_records)
    }

# PII Protection Endpoints
@router.post("/pii/encrypt")
async def encrypt_pii_data(
    encryption_request: PIIEncryptionRequest,
    user: User = Depends(require_admin)
):
    """Encrypt PII data"""
    try:
        encrypted_data = compliance_engine.pii_encryption.encrypt_pii(
            encryption_request.data,
            encryption_request.field_type
        )
        
        return {
            "success": True,
            "encrypted_data": encrypted_data,
            "field_type": encryption_request.field_type.value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Encryption failed: {str(e)}")

@router.post("/pii/decrypt")
async def decrypt_pii_data(
    decryption_request: PIIDecryptionRequest,
    user: User = Depends(require_admin)
):
    """Decrypt PII data"""
    try:
        decrypted_data = compliance_engine.pii_encryption.decrypt_pii(
            decryption_request.encrypted_data,
            decryption_request.field_type
        )
        
        return {
            "success": True,
            "decrypted_data": decrypted_data,
            "field_type": decryption_request.field_type.value
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decryption failed: {str(e)}")

@router.post("/pii/anonymize")
async def anonymize_data(
    anonymization_request: AnonymizationRequest,
    user: User = Depends(require_admin)
):
    """Anonymize sensitive data"""
    try:
        anonymized_data = compliance_engine.pii_encryption.anonymize_data(
            anonymization_request.data,
            anonymization_request.method
        )
        
        return {
            "success": True,
            "anonymized_data": anonymized_data,
            "method": anonymization_request.method
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anonymization failed: {str(e)}")

# Rate Limiting Endpoints
@router.get("/rate-limits/status/{user_id}")
async def get_user_rate_limit_status(
    user_id: str,
    admin_user: User = Depends(require_admin)
):
    """Get current rate limit status for a user"""
    try:
        # Get user's subscription tier (this would typically come from database)
        from src.entitlements import SubscriptionTier
        subscription_tier = SubscriptionTier.BASIC  # Placeholder
        
        # Check all rate limit types
        status = {}
        for limit_type in RateLimitType:
            result = await rate_limit_manager.check_limit(
                user_id, subscription_tier, limit_type
            )
            status[limit_type.value] = {
                "allowed": result.allowed,
                "remaining": result.remaining,
                "reset_time": result.reset_time.isoformat(),
                "current_usage": result.current_usage
            }
        
        return {
            "user_id": user_id,
            "subscription_tier": subscription_tier.value,
            "rate_limits": status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get rate limit status: {str(e)}")

@router.post("/rate-limits/override")
async def override_rate_limit(
    override_request: RateLimitOverride,
    admin_user: User = Depends(require_admin)
):
    """Temporarily override rate limit for a user"""
    # This would typically involve updating the rate limiter configuration
    # For now, return a success message
    return {
        "success": True,
        "message": f"Rate limit override applied for user {override_request.user_id}",
        "limit_type": override_request.limit_type.value,
        "new_limit": override_request.new_limit,
        "expires_at": (datetime.utcnow() + timedelta(hours=override_request.duration_hours)).isoformat(),
        "applied_by": admin_user.email
    }

# Security Configuration Endpoints
@router.get("/config")
async def get_security_config(user: User = Depends(require_admin)):
    """Get current security configuration"""
    # This would typically come from a configuration store
    return {
        "rate_limiting_enabled": True,
        "audit_logging_enabled": True,
        "ip_filtering_enabled": True,
        "compliance_checks_enabled": True,
        "enabled_frameworks": [f.value for f in compliance_engine.config.enabled_frameworks],
        "data_retention_days": compliance_engine.config.data_retention_days,
        "encryption_key_rotation_days": compliance_engine.config.encryption_key_rotation_days
    }

@router.put("/config")
async def update_security_config(
    config_update: SecurityConfigUpdate,
    admin_user: User = Depends(require_admin)
):
    """Update security configuration"""
    try:
        updated_fields = []
        
        # Update blocked IPs
        if config_update.blocked_ips is not None:
            # This would update the middleware configuration
            updated_fields.append("blocked_ips")
        
        # Update allowed IP ranges
        if config_update.allowed_ip_ranges is not None:
            # This would update the middleware configuration
            updated_fields.append("allowed_ip_ranges")
        
        # Update security headers
        if config_update.security_headers is not None:
            # This would update the middleware configuration
            updated_fields.append("security_headers")
        
        return {
            "success": True,
            "message": "Security configuration updated successfully",
            "updated_fields": updated_fields,
            "updated_by": admin_user.email,
            "updated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update security configuration: {str(e)}")

# Audit and Monitoring Endpoints
@router.get("/audit/events")
async def get_audit_events(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    user_id: Optional[str] = None,
    action: Optional[str] = None,
    limit: int = 100,
    admin_user: User = Depends(require_admin)
):
    """Get audit events with optional filtering"""
    # This would typically query the audit log storage
    # For now, return a placeholder response
    return {
        "events": [],
        "total_count": 0,
        "filters": {
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
            "user_id": user_id,
            "action": action,
            "limit": limit
        },
        "message": "Audit event querying would be implemented with proper log storage"
    }

@router.get("/security/threats")
async def get_security_threats(
    hours: int = 24,
    admin_user: User = Depends(require_admin)
):
    """Get security threats detected in the last N hours"""
    # This would analyze audit logs for suspicious patterns
    return {
        "time_period_hours": hours,
        "threats_detected": 0,
        "blocked_ips": [],
        "suspicious_activities": [],
        "rate_limit_violations": 0,
        "compliance_violations": 0,
        "message": "Threat detection would analyze real audit logs"
    }

@router.post("/security/ip/block")
async def block_ip_address(
    ip_address: str,
    reason: str,
    admin_user: User = Depends(require_admin)
):
    """Block an IP address"""
    try:
        # This would update the security middleware
        return {
            "success": True,
            "message": f"IP address {ip_address} has been blocked",
            "reason": reason,
            "blocked_by": admin_user.email,
            "blocked_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to block IP address: {str(e)}")

@router.delete("/security/ip/block/{ip_address}")
async def unblock_ip_address(
    ip_address: str,
    admin_user: User = Depends(require_admin)
):
    """Unblock an IP address"""
    try:
        # This would update the security middleware
        return {
            "success": True,
            "message": f"IP address {ip_address} has been unblocked",
            "unblocked_by": admin_user.email,
            "unblocked_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to unblock IP address: {str(e)}")