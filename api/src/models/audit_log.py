from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class AuditLog(Base):
    """Audit Log model for compliance and security tracking."""
    
    __tablename__ = "audit_logs"
    
    # Relationships (all optional for system-level events)
    partner_id: Mapped[Optional[str]] = mapped_column(ForeignKey("partners.id"), nullable=True, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    
    # Event Information
    event_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)  # login, logout, data_access, etc.
    event_category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # security, data, system, business
    action: Mapped[str] = mapped_column(String(100), nullable=False)  # create, read, update, delete, execute
    resource_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # user, partner, lead, quantum_nexus_query
    resource_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    
    # Event Details
    description: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(String(20), default="info", nullable=False)  # debug, info, warning, error, critical
    status: Mapped[str] = mapped_column(String(20), default="success", nullable=False)  # success, failure, pending
    
    # Request Context
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True, index=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    request_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    session_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    
    # API Context
    api_endpoint: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    http_method: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    response_code: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    # Data Changes
    old_values: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    new_values: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    changed_fields: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    
    # Security Context
    authentication_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # password, oauth, api_key, 2fa
    authorization_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # admin, user, api, system
    risk_score: Mapped[Optional[int]] = mapped_column(nullable=True)  # 0-100
    
    # Compliance & Legal
    compliance_tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)  # gdpr, ccpa, hipaa, sox
    data_classification: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # public, internal, confidential, restricted
    retention_period_days: Mapped[Optional[int]] = mapped_column(nullable=True)
    
    # Business Context
    business_process: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # onboarding, billing, scoring
    cost_impact: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # none, low, medium, high
    
    # Error Information
    error_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stack_trace: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Additional Metadata
    event_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    
    # Relationships
    # partner = relationship("Partner", back_populates="audit_logs")
    # user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, event_type={self.event_type}, severity={self.severity})>"
    
    @property
    def is_security_event(self) -> bool:
        """Check if this is a security-related event."""
        return self.event_category == "security"
    
    @property
    def is_high_risk(self) -> bool:
        """Check if this is a high-risk event."""
        return (
            self.severity in ["error", "critical"] or
            (self.risk_score is not None and self.risk_score >= 70) or
            self.status == "failure"
        )
    
    @property
    def is_data_access(self) -> bool:
        """Check if this involves data access."""
        return self.action in ["read", "export", "download"]
    
    @property
    def is_data_modification(self) -> bool:
        """Check if this involves data modification."""
        return self.action in ["create", "update", "delete"]
    
    @property
    def has_sensitive_data(self) -> bool:
        """Check if event involves sensitive data."""
        return self.data_classification in ["confidential", "restricted"]
    
    def add_compliance_tag(self, tag: str) -> None:
        """Add a compliance tag."""
        if not self.compliance_tags:
            self.compliance_tags = []
        
        if tag not in self.compliance_tags:
            self.compliance_tags.append(tag)
    
    def add_tag(self, tag: str) -> None:
        """Add a general tag."""
        if not self.tags:
            self.tags = []
        
        if tag not in self.tags:
            self.tags.append(tag)
    
    def set_error(self, error_code: str, error_message: str, stack_trace: Optional[str] = None) -> None:
        """Set error information."""
        self.status = "failure"
        self.severity = "error"
        self.error_code = error_code
        self.error_message = error_message
        self.stack_trace = stack_trace
    
    @classmethod
    def create_login_event(cls,
                          user_id: str,
                          partner_id: Optional[str],
                          ip_address: str,
                          user_agent: str,
                          success: bool = True,
                          authentication_method: str = "password") -> 'AuditLog':
        """Create a login audit event."""
        return cls(
            user_id=user_id,
            partner_id=partner_id,
            event_type="user_login",
            event_category="security",
            action="authenticate",
            resource_type="user",
            resource_id=user_id,
            description=f"User login {'successful' if success else 'failed'}",
            severity="info" if success else "warning",
            status="success" if success else "failure",
            ip_address=ip_address,
            user_agent=user_agent,
            authentication_method=authentication_method,
            risk_score=10 if success else 50
        )
    
    @classmethod
    def create_data_access_event(cls,
                               user_id: Optional[str],
                               partner_id: Optional[str],
                               resource_type: str,
                               resource_id: str,
                               action: str = "read",
                               ip_address: Optional[str] = None,
                               api_endpoint: Optional[str] = None) -> 'AuditLog':
        """Create a data access audit event."""
        return cls(
            user_id=user_id,
            partner_id=partner_id,
            event_type="data_access",
            event_category="data",
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            description=f"Data {action} on {resource_type} {resource_id}",
            severity="info",
            status="success",
            ip_address=ip_address,
            api_endpoint=api_endpoint,
            data_classification="internal",
            compliance_tags=["gdpr", "ccpa"]
        )
    
    @classmethod
    def create_quantum_nexus_query_event(cls,
                                 user_id: Optional[str],
                                 partner_id: str,
                                 quantum_nexus_query_id: str,
                                 query_type: str,
                                 credits_used: int,
                                 success: bool = True) -> 'AuditLog':
        """Create an Quantum Nexus query audit event."""
        return cls(
            user_id=user_id,
            partner_id=partner_id,
            event_type="quantum_nexus_query",
            event_category="business",
            action="execute",
            resource_type="quantum_nexus_query",
            resource_id=quantum_nexus_query_id,
            description=f"Quantum Nexus query {query_type} {'completed' if success else 'failed'}",
            severity="info" if success else "error",
            status="success" if success else "failure",
            business_process="quantum_scoring",
            cost_impact="low" if credits_used <= 5 else "medium" if credits_used <= 20 else "high",
            metadata={"query_type": query_type, "credits_used": credits_used}
        )
    
    @classmethod
    def create_payment_event(cls,
                           user_id: Optional[str],
                           partner_id: str,
                           transaction_id: str,
                           amount_usd: float,
                           success: bool = True,
                           payment_method: str = "stripe") -> 'AuditLog':
        """Create a payment audit event."""
        return cls(
            user_id=user_id,
            partner_id=partner_id,
            event_type="payment",
            event_category="business",
            action="create",
            resource_type="payment",
            resource_id=transaction_id,
            description=f"Payment of ${amount_usd:.2f} {'processed' if success else 'failed'}",
            severity="info" if success else "error",
            status="success" if success else "failure",
            business_process="billing",
            cost_impact="high",
            data_classification="confidential",
            compliance_tags=["pci", "sox"],
            metadata={"amount_usd": amount_usd, "payment_method": payment_method}
        )
    
    @classmethod
    def create_system_event(cls,
                          event_type: str,
                          description: str,
                          severity: str = "info",
                          metadata: Optional[dict] = None) -> 'AuditLog':
        """Create a system-level audit event."""
        return cls(
            event_type=event_type,
            event_category="system",
            action="execute",
            description=description,
            severity=severity,
            status="success",
            metadata=metadata
        )