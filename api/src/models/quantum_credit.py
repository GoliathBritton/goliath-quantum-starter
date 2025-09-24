from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, Integer, Float, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class QuantumCredit(Base):
    """Quantum Credit model for tracking credit transactions and usage."""
    
    __tablename__ = "quantum_credits"
    
    # Relationships
    partner_id: Mapped[str] = mapped_column(ForeignKey("partners.id"), nullable=False, index=True)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    quantum_nexus_query_id: Mapped[Optional[str]] = mapped_column(ForeignKey("quantum_nexus_queries.id"), nullable=True, index=True)
    
    # Transaction Details
    transaction_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # purchase, usage, refund, bonus, expiry
    amount: Mapped[int] = mapped_column(Integer, nullable=False)  # Positive for credits added, negative for usage
    balance_before: Mapped[int] = mapped_column(Integer, nullable=False)
    balance_after: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Purchase Information
    purchase_order_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    stripe_payment_intent_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    unit_price_usd: Mapped[float] = mapped_column(Float(), nullable=False, default=0.01)
    total_cost_usd: Mapped[float] = mapped_column(Float(), nullable=False, default=0.00)
    discount_applied: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)  # Percentage 0.00 to 100.00
    
    # Usage Information
    usage_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # quantum_nexus_query, api_call, batch_processing
    query_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # lead_scoring, market_prediction, etc.
    processing_complexity: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # simple, medium, complex
    
    # Billing & Pricing
    billing_tier: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # starter, professional, enterprise
    discount_applied: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)  # Percentage discount
    promotion_code: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Expiry & Validity
    expires_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    is_expired: Mapped[bool] = mapped_column(default=False, nullable=False)
    
    # Refund Information
    refund_reason: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    refunded_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    refund_amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Metadata
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transaction_metadata: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    
    # Audit Trail
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Relationships
    # partner = relationship("Partner", back_populates="quantum_credits")
    # user = relationship("User", back_populates="quantum_credits")
    # quantum_nexus_query = relationship("Quantum NexusQuery", back_populates="quantum_credits")
    
    def __repr__(self) -> str:
        return f"<QuantumCredit(id={self.id}, type={self.transaction_type}, amount={self.amount})>"
    
    @property
    def is_purchase(self) -> bool:
        """Check if this is a credit purchase transaction."""
        return self.transaction_type == "purchase" and self.amount > 0
    
    @property
    def is_usage(self) -> bool:
        """Check if this is a credit usage transaction."""
        return self.transaction_type == "usage" and self.amount < 0
    
    @property
    def is_refund(self) -> bool:
        """Check if this is a refund transaction."""
        return self.transaction_type == "refund"
    
    @property
    def is_bonus(self) -> bool:
        """Check if this is a bonus credit transaction."""
        return self.transaction_type == "bonus" and self.amount > 0
    
    @property
    def credits_used(self) -> int:
        """Get number of credits used (positive value)."""
        return abs(self.amount) if self.is_usage else 0
    
    @property
    def credits_added(self) -> int:
        """Get number of credits added (positive value)."""
        return self.amount if self.amount > 0 else 0
    
    @property
    def is_valid(self) -> bool:
        """Check if credits are still valid (not expired)."""
        if self.is_expired:
            return False
        
        if self.expires_at is None:
            return True
        
        return datetime.utcnow() < self.expires_at
    
    @property
    def days_until_expiry(self) -> Optional[int]:
        """Get days until expiry."""
        if not self.expires_at:
            return None
        
        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)
    
    def mark_expired(self) -> None:
        """Mark credits as expired."""
        self.is_expired = True
    
    def process_refund(self, reason: str, amount: Optional[int] = None) -> None:
        """Process a refund for this transaction."""
        self.refund_reason = reason
        self.refunded_at = datetime.utcnow()
        self.refund_amount = amount or abs(self.amount)
    
    @classmethod
    def create_purchase(cls,
                       partner_id: str,
                       user_id: Optional[str],
                       amount: int,
                       balance_before: int,
                       unit_price_usd: float,
                       stripe_payment_intent_id: Optional[str] = None,
                       purchase_order_id: Optional[str] = None,
                       billing_tier: Optional[str] = None,
                       expires_at: Optional[datetime] = None,
                       promotion_code: Optional[str] = None,
                       discount_applied: Optional[float] = None) -> 'QuantumCredit':
        """Create a credit purchase transaction."""
        total_cost = amount * unit_price_usd
        
        if discount_applied:
            total_cost = total_cost * (1 - discount_applied / 100)
        
        return cls(
            partner_id=partner_id,
            user_id=user_id,
            transaction_type="purchase",
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_before + amount,
            unit_price_usd=unit_price_usd,
            total_cost_usd=total_cost,
            stripe_payment_intent_id=stripe_payment_intent_id,
            purchase_order_id=purchase_order_id,
            billing_tier=billing_tier,
            expires_at=expires_at,
            promotion_code=promotion_code,
            discount_applied=discount_applied,
            description=f"Purchase of {amount} quantum credits"
        )
    
    @classmethod
    def create_usage(cls,
                    partner_id: str,
                    user_id: Optional[str],
                    amount: int,
                    balance_before: int,
                    quantum_nexus_query_id: Optional[str] = None,
                    usage_type: str = "quantum_nexus_query",
                    query_type: Optional[str] = None,
                    processing_complexity: str = "simple") -> 'QuantumCredit':
        """Create a credit usage transaction."""
        return cls(
            partner_id=partner_id,
            user_id=user_id,
            quantum_nexus_query_id=quantum_nexus_query_id,
            transaction_type="usage",
            amount=-amount,  # Negative for usage
            balance_before=balance_before,
            balance_after=balance_before - amount,
            usage_type=usage_type,
            query_type=query_type,
            processing_complexity=processing_complexity,
            description=f"Used {amount} credits for {usage_type}"
        )
    
    @classmethod
    def create_bonus(cls,
                    partner_id: str,
                    user_id: Optional[str],
                    amount: int,
                    balance_before: int,
                    reason: str = "Bonus credits",
                    expires_at: Optional[datetime] = None) -> 'QuantumCredit':
        """Create a bonus credit transaction."""
        return cls(
            partner_id=partner_id,
            user_id=user_id,
            transaction_type="bonus",
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_before + amount,
            expires_at=expires_at,
            description=reason
        )
    
    @classmethod
    def create_refund(cls,
                     partner_id: str,
                     user_id: Optional[str],
                     amount: int,
                     balance_before: int,
                     reason: str,
                     original_transaction_id: Optional[str] = None) -> 'QuantumCredit':
        """Create a refund transaction."""
        return cls(
            partner_id=partner_id,
            user_id=user_id,
            transaction_type="refund",
            amount=amount,
            balance_before=balance_before,
            balance_after=balance_before + amount,
            refund_reason=reason,
            refunded_at=datetime.utcnow(),
            description=f"Refund: {reason}",
            metadata={"original_transaction_id": original_transaction_id} if original_transaction_id else None
        )
    
    @classmethod
    def create_expiry(cls,
                     partner_id: str,
                     amount: int,
                     balance_before: int,
                     expired_transaction_id: str) -> 'QuantumCredit':
        """Create an expiry transaction for expired credits."""
        return cls(
            partner_id=partner_id,
            transaction_type="expiry",
            amount=-amount,  # Negative for expired credits
            balance_before=balance_before,
            balance_after=balance_before - amount,
            is_expired=True,
            description=f"Expired {amount} credits",
            metadata={"expired_transaction_id": expired_transaction_id}
        )