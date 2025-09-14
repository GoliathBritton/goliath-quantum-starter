from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, Boolean, Numeric, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Partner(Base):
    """Partner model for organizations using the Goliath Quantum platform."""
    
    __tablename__ = "partners"
    
    # Basic Information
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Contact Information
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Address
    address_line1: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    state: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    postal_code: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Business Information
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # startup, small, medium, large, enterprise
    annual_revenue: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Platform Configuration
    tier: Mapped[str] = mapped_column(String(50), default="starter", nullable=False)  # starter, professional, enterprise
    status: Mapped[str] = mapped_column(String(50), default="active", nullable=False)  # active, suspended, trial, churned
    
    # Quantum Credits & Billing
    quantum_credits_balance: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    quantum_credits_used: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    monthly_credit_limit: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Stripe Integration
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    stripe_account_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)  # For Stripe Connect
    
    # API Configuration
    api_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    api_rate_limit: Mapped[int] = mapped_column(Integer, default=1000, nullable=False)  # requests per hour
    
    # White-label Configuration
    white_label_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    custom_domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    brand_config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # Colors, logos, etc.
    
    # Integration Settings
    dynex_api_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    integration_config: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)  # UiPath, n8n, etc.
    
    # Compliance & Security
    data_retention_days: Mapped[int] = mapped_column(Integer, default=365, nullable=False)
    encryption_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    audit_logging_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Trial & Onboarding
    trial_start_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    trial_end_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    onboarding_step: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Relationships
    # users = relationship("User", back_populates="partner")
    # leads = relationship("Lead", back_populates="partner")
    # oracle_queries = relationship("OracleQuery", back_populates="partner")
    # quantum_credits = relationship("QuantumCredit", back_populates="partner")
    
    def __repr__(self) -> str:
        return f"<Partner(id={self.id}, name={self.name}, tier={self.tier})>"
    
    @property
    def is_trial(self) -> bool:
        """Check if partner is in trial period."""
        if not self.trial_end_date:
            return False
        return datetime.utcnow() <= self.trial_end_date
    
    @property
    def credits_remaining(self) -> int:
        """Calculate remaining quantum credits."""
        return max(0, self.quantum_credits_balance - self.quantum_credits_used)
    
    @property
    def usage_percentage(self) -> float:
        """Calculate usage percentage of monthly limit."""
        if not self.monthly_credit_limit or self.monthly_credit_limit == 0:
            return 0.0
        return min(100.0, (self.quantum_credits_used / self.monthly_credit_limit) * 100)
    
    def can_use_credits(self, amount: int) -> bool:
        """Check if partner can use specified amount of credits."""
        if self.credits_remaining < amount:
            return False
        
        if self.monthly_credit_limit:
            return (self.quantum_credits_used + amount) <= self.monthly_credit_limit
        
        return True
    
    def use_credits(self, amount: int) -> bool:
        """Use quantum credits if available."""
        if not self.can_use_credits(amount):
            return False
        
        self.quantum_credits_used += amount
        return True
    
    def add_credits(self, amount: int) -> None:
        """Add quantum credits to balance."""
        self.quantum_credits_balance += amount