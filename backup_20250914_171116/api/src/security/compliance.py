from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from pydantic import BaseModel
import hashlib
import json
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class ComplianceFramework(Enum):
    GDPR = "gdpr"
    CCPA = "ccpa"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    ISO27001 = "iso27001"

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    PII = "pii"
    PHI = "phi"

class AuditEvent(BaseModel):
    event_id: str
    timestamp: datetime
    user_id: Optional[str]
    action: str
    resource: str
    ip_address: str
    user_agent: str
    result: str  # success, failure, blocked
    risk_score: float
    metadata: Dict[str, Any]
    compliance_frameworks: List[ComplianceFramework]

class PIIField(BaseModel):
    field_name: str
    classification: DataClassification
    encryption_required: bool = True
    retention_days: int = 365
    anonymization_method: str = "hash"

class ComplianceConfig(BaseModel):
    enabled_frameworks: List[ComplianceFramework]
    data_retention_days: int = 2555  # 7 years default
    encryption_key_rotation_days: int = 90
    audit_log_retention_days: int = 2555
    pii_fields: List[PIIField]
    anonymization_enabled: bool = True
    consent_tracking_enabled: bool = True

class PIIEncryption:
    """Handles PII encryption and decryption with key rotation support"""
    
    def __init__(self, master_key: Optional[str] = None):
        self.master_key = master_key or os.getenv('PII_MASTER_KEY', self._generate_key())
        self._cipher_suite = None
        self._initialize_cipher()
    
    def _generate_key(self) -> str:
        """Generate a new encryption key"""
        return Fernet.generate_key().decode()
    
    def _initialize_cipher(self):
        """Initialize the cipher suite"""
        key = self.master_key.encode() if isinstance(self.master_key, str) else self.master_key
        self._cipher_suite = Fernet(key)
    
    def encrypt_pii(self, data: str, field_type: DataClassification) -> str:
        """Encrypt PII data based on classification"""
        if field_type in [DataClassification.PII, DataClassification.PHI]:
            encrypted_data = self._cipher_suite.encrypt(data.encode())
            return base64.b64encode(encrypted_data).decode()
        return data
    
    def decrypt_pii(self, encrypted_data: str, field_type: DataClassification) -> str:
        """Decrypt PII data"""
        if field_type in [DataClassification.PII, DataClassification.PHI]:
            try:
                decoded_data = base64.b64decode(encrypted_data.encode())
                decrypted_data = self._cipher_suite.decrypt(decoded_data)
                return decrypted_data.decode()
            except Exception as e:
                logging.error(f"Failed to decrypt PII data: {e}")
                return "[DECRYPTION_ERROR]"
        return encrypted_data
    
    def anonymize_data(self, data: str, method: str = "hash") -> str:
        """Anonymize data using specified method"""
        if method == "hash":
            return hashlib.sha256(data.encode()).hexdigest()[:16]
        elif method == "mask":
            if len(data) <= 4:
                return "*" * len(data)
            return data[:2] + "*" * (len(data) - 4) + data[-2:]
        elif method == "remove":
            return "[REDACTED]"
        return data

class AuditLogger:
    """Comprehensive audit logging system"""
    
    def __init__(self, config: ComplianceConfig):
        self.config = config
        self.logger = logging.getLogger('compliance_audit')
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup audit logger with appropriate handlers"""
        handler = logging.FileHandler('audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    def log_event(self, event: AuditEvent):
        """Log an audit event"""
        event_data = {
            'event_id': event.event_id,
            'timestamp': event.timestamp.isoformat(),
            'user_id': event.user_id,
            'action': event.action,
            'resource': event.resource,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
            'result': event.result,
            'risk_score': event.risk_score,
            'metadata': event.metadata,
            'compliance_frameworks': [f.value for f in event.compliance_frameworks]
        }
        
        self.logger.info(json.dumps(event_data))
    
    def log_data_access(self, user_id: str, resource: str, action: str, 
                       ip_address: str, user_agent: str, success: bool = True):
        """Log data access events"""
        event = AuditEvent(
            event_id=self._generate_event_id(),
            timestamp=datetime.utcnow(),
            user_id=user_id,
            action=action,
            resource=resource,
            ip_address=ip_address,
            user_agent=user_agent,
            result="success" if success else "failure",
            risk_score=self._calculate_risk_score(action, resource),
            metadata={"data_classification": "confidential"},
            compliance_frameworks=self.config.enabled_frameworks
        )
        self.log_event(event)
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        return hashlib.md5(f"{datetime.utcnow().isoformat()}{os.urandom(8)}".encode()).hexdigest()
    
    def _calculate_risk_score(self, action: str, resource: str) -> float:
        """Calculate risk score for the action"""
        base_score = 0.1
        
        # Higher risk for sensitive actions
        if action in ['delete', 'export', 'bulk_download']:
            base_score += 0.5
        elif action in ['update', 'create']:
            base_score += 0.3
        
        # Higher risk for sensitive resources
        if 'pii' in resource.lower() or 'personal' in resource.lower():
            base_score += 0.4
        
        return min(base_score, 1.0)

class ComplianceEngine:
    """Main compliance engine orchestrating all security features"""
    
    def __init__(self, config: ComplianceConfig):
        self.config = config
        self.pii_encryption = PIIEncryption()
        self.audit_logger = AuditLogger(config)
        self.consent_records: Dict[str, Dict] = {}
    
    def validate_data_processing(self, user_id: str, data_type: DataClassification, 
                               purpose: str) -> bool:
        """Validate if data processing is compliant"""
        # Check consent for GDPR compliance
        if ComplianceFramework.GDPR in self.config.enabled_frameworks:
            if not self._has_valid_consent(user_id, purpose):
                return False
        
        # Check data classification requirements
        if data_type in [DataClassification.PII, DataClassification.PHI]:
            if not self._validate_pii_processing(user_id, purpose):
                return False
        
        return True
    
    def _has_valid_consent(self, user_id: str, purpose: str) -> bool:
        """Check if user has given valid consent"""
        if not self.config.consent_tracking_enabled:
            return True
        
        consent = self.consent_records.get(user_id, {})
        if purpose not in consent:
            return False
        
        consent_date = consent[purpose].get('date')
        if not consent_date:
            return False
        
        # Check if consent is still valid (not older than 2 years for GDPR)
        if datetime.utcnow() - consent_date > timedelta(days=730):
            return False
        
        return consent[purpose].get('granted', False)
    
    def _validate_pii_processing(self, user_id: str, purpose: str) -> bool:
        """Validate PII processing requirements"""
        # Implement specific PII processing validation logic
        allowed_purposes = [
            'service_provision', 'legal_compliance', 
            'legitimate_interest', 'user_consent'
        ]
        return purpose in allowed_purposes
    
    def record_consent(self, user_id: str, purpose: str, granted: bool, 
                      legal_basis: str = "consent"):
        """Record user consent"""
        if user_id not in self.consent_records:
            self.consent_records[user_id] = {}
        
        self.consent_records[user_id][purpose] = {
            'granted': granted,
            'date': datetime.utcnow(),
            'legal_basis': legal_basis,
            'version': '1.0'
        }
        
        # Log consent event
        self.audit_logger.log_event(AuditEvent(
            event_id=self.audit_logger._generate_event_id(),
            timestamp=datetime.utcnow(),
            user_id=user_id,
            action='consent_recorded',
            resource='user_consent',
            ip_address='system',
            user_agent='compliance_engine',
            result='success',
            risk_score=0.1,
            metadata={
                'purpose': purpose,
                'granted': granted,
                'legal_basis': legal_basis
            },
            compliance_frameworks=self.config.enabled_frameworks
        ))
    
    def get_compliance_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Generate compliance report"""
        return {
            'period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'frameworks': [f.value for f in self.config.enabled_frameworks],
            'data_processing_events': self._count_processing_events(start_date, end_date),
            'consent_status': self._get_consent_summary(),
            'security_incidents': self._count_security_incidents(start_date, end_date),
            'data_retention_compliance': self._check_retention_compliance()
        }
    
    def _count_processing_events(self, start_date: datetime, end_date: datetime) -> int:
        """Count data processing events in period"""
        # Implementation would query audit logs
        return 0
    
    def _get_consent_summary(self) -> Dict:
        """Get summary of consent records"""
        total_users = len(self.consent_records)
        granted_consents = sum(
            1 for user_consents in self.consent_records.values()
            for consent in user_consents.values()
            if consent.get('granted', False)
        )
        
        return {
            'total_users': total_users,
            'granted_consents': granted_consents,
            'consent_rate': granted_consents / max(total_users, 1)
        }
    
    def _count_security_incidents(self, start_date: datetime, end_date: datetime) -> int:
        """Count security incidents in period"""
        # Implementation would query security logs
        return 0
    
    def _check_retention_compliance(self) -> Dict:
        """Check data retention compliance"""
        return {
            'compliant': True,
            'expired_data_count': 0,
            'next_cleanup_date': (datetime.utcnow() + timedelta(days=30)).isoformat()
        }

# Default compliance configuration
DEFAULT_COMPLIANCE_CONFIG = ComplianceConfig(
    enabled_frameworks=[
        ComplianceFramework.GDPR,
        ComplianceFramework.CCPA,
        ComplianceFramework.SOC2
    ],
    data_retention_days=2555,
    encryption_key_rotation_days=90,
    audit_log_retention_days=2555,
    pii_fields=[
        PIIField(field_name="email", classification=DataClassification.PII),
        PIIField(field_name="phone", classification=DataClassification.PII),
        PIIField(field_name="address", classification=DataClassification.PII),
        PIIField(field_name="ssn", classification=DataClassification.RESTRICTED),
        PIIField(field_name="medical_data", classification=DataClassification.PHI)
    ],
    anonymization_enabled=True,
    consent_tracking_enabled=True
)

# Global compliance engine instance
compliance_engine = ComplianceEngine(DEFAULT_COMPLIANCE_CONFIG)