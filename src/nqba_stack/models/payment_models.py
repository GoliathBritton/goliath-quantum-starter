#!/usr/bin/env python3
"""
💳 Payment Models for NQBA Ecosystem

Defines data models for payment processing, transactions, and financial operations
across all business units in the NQBA platform.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from enum import Enum
from pydantic import BaseModel, Field, validator
from decimal import Decimal


class PaymentStatus(str, Enum):
    """Payment transaction status"""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


class PaymentMethod(str, Enum):
    """Payment method types"""

    STRIPE = "stripe"
    PAYPAL = "paypal"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"


class TransactionType(str, Enum):
    """Transaction types"""

    SUBSCRIPTION = "subscription"
    COURSE_ENROLLMENT = "course_enrollment"
    LOAN_APPLICATION_FEE = "loan_application_fee"
    LOAN_ORIGINATION_FEE = "loan_origination_fee"
    INSURANCE_PREMIUM = "insurance_premium"
    CONSULTING_FEE = "consulting_fee"
    MARKETPLACE_PURCHASE = "marketplace_purchase"
    # Energy-related transaction types
    ENERGY_QUOTE_FEE = "energy_quote_fee"
    ENERGY_CONTRACT_COMMISSION = "energy_contract_commission"
    ENERGY_CONSULTING_FEE = "energy_consulting_fee"
    ENERGY_AUDIT_FEE = "energy_audit_fee"
    ENERGY_OPTIMIZATION_FEE = "energy_optimization_fee"


class BusinessUnit(str, Enum):
    """Business unit identifiers"""

    FLYFOX_AI = "flyfox_ai"
    GOLIATH_CAPITAL = "goliath_capital"
    SIGMA_SELECT = "sigma_select"
    GOLIATH_ENERGY = "goliath_energy"
    SFG_INSURANCE = "sfg_insurance"
    EDUVERSE_AI = "eduverse_ai"


class EnergyPartner(str, Enum):
    """Energy partner identifiers"""

    DIVERSEGY_PRO = "diversegy_pro"
    OTHER_PARTNER_1 = "other_partner_1"
    OTHER_PARTNER_2 = "other_partner_2"


class EnergyServiceType(str, Enum):
    """Types of energy services"""

    ELECTRICITY = "electricity"
    NATURAL_GAS = "natural_gas"
    RENEWABLE_ENERGY = "renewable_energy"
    ENERGY_CONSULTING = "energy_consulting"
    ENERGY_AUDIT = "energy_audit"
    ENERGY_OPTIMIZATION = "energy_optimization"
    DEMAND_RESPONSE = "demand_response"
    ENERGY_STORAGE = "energy_storage"


class StripeTransaction(BaseModel):
    """Stripe-specific transaction details"""

    stripe_payment_intent_id: str
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
    stripe_invoice_id: Optional[str] = None
    stripe_refund_id: Optional[str] = None
    stripe_dispute_id: Optional[str] = None
    payment_method_type: Optional[str] = None
    card_brand: Optional[str] = None
    card_last4: Optional[str] = None
    card_exp_month: Optional[int] = None
    card_exp_year: Optional[int] = None


class PayPalTransaction(BaseModel):
    """PayPal-specific transaction details"""

    paypal_order_id: str
    paypal_payment_id: Optional[str] = None
    paypal_capture_id: Optional[str] = None
    paypal_refund_id: Optional[str] = None
    paypal_dispute_id: Optional[str] = None
    paypal_payer_id: Optional[str] = None
    paypal_payer_email: Optional[str] = None


class PaymentTransaction(BaseModel):
    """Core payment transaction model"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    business_unit: BusinessUnit
    transaction_type: TransactionType
    amount: Decimal = Field(..., decimal_places=2)
    currency: str = Field(default="USD", max_length=3)
    payment_method: PaymentMethod
    status: PaymentStatus = PaymentStatus.PENDING
    description: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Payment provider details
    stripe_details: Optional[StripeTransaction] = None
    paypal_details: Optional[PayPalTransaction] = None

    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    # Error tracking
    error_message: Optional[str] = None
    retry_count: int = Field(default=0, ge=0)

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: str}


class EnergyQuote(BaseModel):
    """Energy quote model for Goliath Energy"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    company_name: str
    contact_email: str
    contact_phone: str
    business_type: str
    annual_energy_usage_kwh: Optional[Decimal] = None
    current_energy_provider: Optional[str] = None
    current_monthly_bill: Optional[Decimal] = None
    service_type: EnergyServiceType
    energy_partner: EnergyPartner
    quote_amount: Optional[Decimal] = None
    estimated_savings: Optional[Decimal] = None
    contract_term_months: Optional[int] = None
    status: str = Field(default="pending")  # pending, quoted, accepted, rejected
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    quoted_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: str}


class EnergyContract(BaseModel):
    """Energy contract model for Goliath Energy"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    quote_id: str
    user_id: str
    energy_partner: EnergyPartner
    service_type: EnergyServiceType
    contract_number: str
    start_date: datetime
    end_date: datetime
    monthly_rate: Decimal
    contract_term_months: int
    commission_rate: Decimal  # Partner commission percentage
    commission_amount: Decimal
    status: str = Field(default="active")  # active, cancelled, expired
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: str}


class EnergyPartnerCommission(BaseModel):
    """Energy partner commission tracking"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    contract_id: str
    energy_partner: EnergyPartner
    commission_amount: Decimal
    commission_rate: Decimal
    payment_status: PaymentStatus = PaymentStatus.PENDING
    payment_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: str}


class CourseEnrollment(BaseModel):
    """Course enrollment model for Sigma Select"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    course_id: str
    course_name: str
    course_price: Decimal = Field(..., decimal_places=2)
    enrollment_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    payment_transaction_id: str
    status: str = Field(default="enrolled")  # enrolled, completed, cancelled
    completion_date: Optional[datetime] = None
    certificate_issued: bool = Field(default=False)
    certificate_id: Optional[str] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: str}


class LoanApplication(BaseModel):
    """Loan application model for Goliath Capital"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    company_name: str
    loan_amount: Decimal = Field(..., decimal_places=2)
    loan_purpose: str
    contact_email: str
    contact_phone: str
    annual_revenue: Optional[Decimal] = None
    business_type: Optional[str] = None
    years_in_business: Optional[int] = None
    credit_score: Optional[int] = None

    # Application status
    status: str = Field(
        default="submitted"
    )  # submitted, under_review, approved, denied
    submitted_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    review_date: Optional[datetime] = None
    decision_date: Optional[datetime] = None
    decision_notes: Optional[str] = None

    # External funding sources
    external_funding_source: Optional[str] = (
        None  # David Allen Capital, Lexington Capital, etc.
    )
    external_reference_id: Optional[str] = None

    # Payment details
    application_fee_paid: bool = Field(default=False)
    application_fee_transaction_id: Optional[str] = None
    origination_fee_transaction_id: Optional[str] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: str}


class SubscriptionPlan(BaseModel):
    """Subscription plan model for FLYFOX AI"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    plan_name: str
    plan_type: str  # starter, professional, enterprise
    monthly_price: Decimal = Field(..., decimal_places=2)
    annual_price: Decimal = Field(..., decimal_places=2)
    features: List[str] = Field(default_factory=list)
    max_agents: Optional[int] = None
    max_workflows: Optional[int] = None
    support_level: str = Field(default="email")  # email, chat, phone, dedicated
    is_active: bool = Field(default=True)

    class Config:
        json_encoders = {Decimal: str}


class UserSubscription(BaseModel):
    """User subscription model"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    plan_id: str
    plan_name: str
    plan_type: str
    status: str = Field(default="active")  # active, cancelled, suspended, expired
    start_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    end_date: Optional[datetime] = None
    auto_renew: bool = Field(default=True)
    payment_method: PaymentMethod
    last_payment_date: Optional[datetime] = None
    next_payment_date: Optional[datetime] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: str}


class ExternalFundingSource(BaseModel):
    """External funding source model for Goliath Capital"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    website: str
    description: str
    loan_types: List[str] = Field(default_factory=list)
    min_loan_amount: Optional[Decimal] = None
    max_loan_amount: Optional[Decimal] = None
    typical_terms: Optional[str] = None
    application_url: str
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: bool = Field(default=True)
    partnership_status: str = Field(default="active")  # active, pending, inactive

    class Config:
        json_encoders = {Decimal: str}


class EnergyPartner(BaseModel):
    """Energy partner model for Goliath Energy"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    partner_code: str  # e.g., "diversegy_pro"
    website: str
    description: str
    services_offered: List[EnergyServiceType] = Field(default_factory=list)
    commission_structure: Dict[str, Decimal] = Field(
        default_factory=dict
    )  # service_type -> commission_rate
    application_url: str
    api_endpoint: Optional[str] = None
    api_key: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    is_active: bool = Field(default=True)
    partnership_status: str = Field(default="active")  # active, pending, inactive
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat(), Decimal: str}


class PaymentWebhook(BaseModel):
    """Webhook payload model for payment providers"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    provider: PaymentMethod
    event_type: str
    payload: Dict[str, Any]
    signature: Optional[str] = None
    received_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    processed: bool = Field(default=False)
    processing_result: Optional[str] = None

    class Config:
        json_encoders = {datetime: lambda v: v.isoformat()}
