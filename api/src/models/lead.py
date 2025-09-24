from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, Boolean, Float, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Lead(Base):
    """Lead model for managing prospect data and quantum scoring."""
    
    __tablename__ = "leads"
    
    # Partner relationship
    partner_id: Mapped[str] = mapped_column(ForeignKey("partners.id"), nullable=False, index=True)
    
    # Basic Information
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Company Information
    company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    annual_revenue: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Contact Details
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Lead Qualification
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # website, referral, cold_call, etc.
    campaign: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_medium: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    utm_campaign: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Lead Status
    status: Mapped[str] = mapped_column(String(50), default="new", nullable=False)  # new, qualified, contacted, converted, lost
    stage: Mapped[str] = mapped_column(String(50), default="prospect", nullable=False)  # prospect, lead, opportunity, customer
    
    # Quantum Scoring
    quantum_score: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)  # 0.00 to 100.00
    quantum_confidence: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)  # 0.00 to 100.00
    last_scored_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    scoring_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Behavioral Data
    website_visits: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    email_opens: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    email_clicks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    content_downloads: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    demo_requests: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Engagement Metrics
    first_contact_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_contact_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_activity_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    contact_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Custom Fields & Metadata
    custom_fields: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    tags: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # TCPA Compliance
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    consent_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    consent_method: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # web_form, phone, email, etc.
    opt_out_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    do_not_call: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    do_not_email: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Lead Value & Conversion
    estimated_value: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    conversion_probability: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    days_to_conversion: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Assignment & Ownership
    assigned_to: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # User ID or email
    assigned_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    
    # Relationships
    # partner = relationship("Partner", back_populates="leads")
    # quantum_nexus_queries = relationship("Quantum NexusQuery", back_populates="lead")
    
    def __repr__(self) -> str:
        return f"<Lead(id={self.id}, name={self.first_name} {self.last_name}, score={self.quantum_score})>"
    
    @property
    def full_name(self) -> str:
        """Get full name of the lead."""
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def is_qualified(self) -> bool:
        """Check if lead meets qualification criteria."""
        return (
            self.quantum_score is not None and 
            self.quantum_score >= 70.0 and
            self.consent_given and
            not self.do_not_call and
            not self.do_not_email
        )
    
    @property
    def is_hot(self) -> bool:
        """Check if lead is considered hot (high priority)."""
        return (
            self.quantum_score is not None and 
            self.quantum_score >= 85.0 and
            self.quantum_confidence is not None and
            self.quantum_confidence >= 80.0
        )
    
    @property
    def days_since_last_contact(self) -> Optional[int]:
        """Calculate days since last contact."""
        if not self.last_contact_date:
            return None
        return (datetime.utcnow() - self.last_contact_date).days
    
    @property
    def engagement_score(self) -> float:
        """Calculate engagement score based on activities."""
        score = 0.0
        score += self.website_visits * 2
        score += self.email_opens * 1
        score += self.email_clicks * 3
        score += self.content_downloads * 5
        score += self.demo_requests * 10
        return min(100.0, score)
    
    def update_quantum_score(self, score: float, confidence: float, version: str = "1.0") -> None:
        """Update quantum scoring results."""
        self.quantum_score = max(0.0, min(100.0, score))
        self.quantum_confidence = max(0.0, min(100.0, confidence))
        self.last_scored_at = datetime.utcnow()
        self.scoring_version = version
    
    def add_activity(self, activity_type: str, count: int = 1) -> None:
        """Add activity tracking."""
        activity_map = {
            "website_visit": "website_visits",
            "email_open": "email_opens",
            "email_click": "email_clicks",
            "content_download": "content_downloads",
            "demo_request": "demo_requests"
        }
        
        if activity_type in activity_map:
            current_value = getattr(self, activity_map[activity_type])
            setattr(self, activity_map[activity_type], current_value + count)
            self.last_activity_date = datetime.utcnow()
    
    def record_contact(self) -> None:
        """Record a contact attempt."""
        self.contact_attempts += 1
        self.last_contact_date = datetime.utcnow()
        
        if not self.first_contact_date:
            self.first_contact_date = datetime.utcnow()
    
    def give_consent(self, method: str = "web_form") -> None:
        """Record consent for communications."""
        self.consent_given = True
        self.consent_date = datetime.utcnow()
        self.consent_method = method
        self.opt_out_date = None
    
    def opt_out(self) -> None:
        """Record opt-out from communications."""
        self.consent_given = False
        self.opt_out_date = datetime.utcnow()
        self.do_not_call = True
        self.do_not_email = True