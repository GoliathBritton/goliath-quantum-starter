#!/usr/bin/env python3
"""
Monetization APIs
Usage tracking, billing, and white-label deployment system
Revenue generation for Quantum AI Calling Agents and Digital Human division
"""

import asyncio
import json
import logging
import uuid
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, validator
import uvicorn
from sqlalchemy import create_engine, Column, String, DateTime, Float, Integer, Boolean, Text, JSON, Numeric, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import redis
import stripe
import requests
from celery import Celery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import jwt
from passlib.context import CryptContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database models
Base = declarative_base()

class SubscriptionTier(Enum):
    STARTER = "starter"  # $50K/month SMB
    PROFESSIONAL = "professional"  # $100K/month Mid-market
    ENTERPRISE = "enterprise"  # $250K/month Enterprise
    ELITE_WHITE_LABEL = "elite_white_label"  # $1M+/year

class UsageType(Enum):
    VOICE_CALL_MINUTE = "voice_call_minute"  # $0.75-$1.50 per minute
    DIGITAL_HUMAN_SESSION = "digital_human_session"  # $10K/month per persona
    LEAD_PROCESSING = "lead_processing"  # $0.10 per lead
    QUANTUM_SCORING = "quantum_scoring"  # $0.25 per score
    PLAYBOOK_GENERATION = "playbook_generation"  # $5 per playbook
    API_REQUEST = "api_request"  # $0.01 per request

class BillingCycle(Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"

class Organization(Base):
    """Customer organizations"""
    __tablename__ = 'organizations'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    domain = Column(String, unique=True)
    
    # Subscription details
    subscription_tier = Column(String, nullable=False)
    billing_cycle = Column(String, default=BillingCycle.MONTHLY.value)
    
    # Contact information
    primary_contact_email = Column(String, nullable=False)
    billing_email = Column(String)
    phone = Column(String)
    
    # Address
    address_line1 = Column(String)
    address_line2 = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)
    country = Column(String, default="US")
    
    # Financial
    stripe_customer_id = Column(String, unique=True)
    tax_id = Column(String)
    
    # Limits and quotas
    monthly_call_minutes_limit = Column(Integer, default=10000)
    monthly_leads_limit = Column(Integer, default=50000)
    digital_personas_limit = Column(Integer, default=1)
    api_rate_limit = Column(Integer, default=1000)  # requests per hour
    
    # White-label settings
    is_white_label = Column(Boolean, default=False)
    white_label_domain = Column(String)
    custom_branding = Column(JSON)
    
    # Status
    is_active = Column(Boolean, default=True)
    trial_ends_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    api_keys = relationship("APIKey", back_populates="organization")
    usage_records = relationship("UsageRecord", back_populates="organization")
    invoices = relationship("Invoice", back_populates="organization")

class APIKey(Base):
    """API keys for organizations"""
    __tablename__ = 'api_keys'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey('organizations.id'), nullable=False)
    
    name = Column(String, nullable=False)  # Human-readable name
    key_hash = Column(String, nullable=False, unique=True)  # Hashed API key
    key_prefix = Column(String, nullable=False)  # First 8 chars for identification
    
    # Permissions
    scopes = Column(JSON, default=list)  # List of allowed operations
    
    # Usage limits
    rate_limit_per_hour = Column(Integer, default=1000)
    daily_usage_limit = Column(Integer)
    monthly_usage_limit = Column(Integer)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    
    # Relationships
    organization = relationship("Organization", back_populates="api_keys")

class UsageRecord(Base):
    """Usage tracking records"""
    __tablename__ = 'usage_records'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey('organizations.id'), nullable=False)
    api_key_id = Column(String, ForeignKey('api_keys.id'))
    
    # Usage details
    usage_type = Column(String, nullable=False)
    quantity = Column(Numeric(10, 4), nullable=False)  # Amount used
    unit_price = Column(Numeric(10, 4), nullable=False)  # Price per unit
    total_cost = Column(Numeric(10, 2), nullable=False)  # Total cost
    
    # Context
    resource_id = Column(String)  # ID of the resource used (call, lead, etc.)
    metadata = Column(JSON)  # Additional context
    
    # Billing
    billing_period = Column(String)  # YYYY-MM format
    is_billable = Column(Boolean, default=True)
    invoice_id = Column(String, ForeignKey('invoices.id'))
    
    # Timestamps
    usage_timestamp = Column(DateTime, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    organization = relationship("Organization", back_populates="usage_records")
    invoice = relationship("Invoice", back_populates="usage_records")

class Invoice(Base):
    """Generated invoices"""
    __tablename__ = 'invoices'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    organization_id = Column(String, ForeignKey('organizations.id'), nullable=False)
    
    # Invoice details
    invoice_number = Column(String, unique=True, nullable=False)
    billing_period_start = Column(DateTime, nullable=False)
    billing_period_end = Column(DateTime, nullable=False)
    
    # Financial
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_amount = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String, default="USD")
    
    # Payment
    stripe_invoice_id = Column(String)
    payment_status = Column(String, default="pending")  # pending, paid, failed, cancelled
    paid_at = Column(DateTime)
    
    # Status
    status = Column(String, default="draft")  # draft, sent, paid, overdue, cancelled
    due_date = Column(DateTime, nullable=False)
    
    # Content
    line_items = Column(JSON)  # Detailed breakdown
    notes = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    
    # Relationships
    organization = relationship("Organization", back_populates="invoices")
    usage_records = relationship("UsageRecord", back_populates="invoice")

class PricingRule(Base):
    """Dynamic pricing rules"""
    __tablename__ = 'pricing_rules'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Rule definition
    usage_type = Column(String, nullable=False)
    subscription_tier = Column(String)
    
    # Pricing
    base_price = Column(Numeric(10, 4), nullable=False)
    volume_tiers = Column(JSON)  # Volume-based pricing tiers
    
    # Conditions
    effective_from = Column(DateTime, default=datetime.utcnow)
    effective_until = Column(DateTime)
    
    # Metadata
    description = Column(String)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

# Pydantic models
class OrganizationCreate(BaseModel):
    name: str
    domain: str
    subscription_tier: str
    primary_contact_email: str
    billing_email: Optional[str] = None
    phone: Optional[str] = None
    billing_cycle: str = BillingCycle.MONTHLY.value
    
    @validator('subscription_tier')
    def validate_tier(cls, v):
        if v not in [tier.value for tier in SubscriptionTier]:
            raise ValueError('Invalid subscription tier')
        return v

class APIKeyCreate(BaseModel):
    name: str
    scopes: List[str] = []
    rate_limit_per_hour: int = 1000
    expires_in_days: Optional[int] = None

class APIKeyResponse(BaseModel):
    id: str
    name: str
    key: str  # Only returned on creation
    key_prefix: str
    scopes: List[str]
    created_at: datetime
    expires_at: Optional[datetime]

class UsageRecordCreate(BaseModel):
    usage_type: str
    quantity: float
    resource_id: Optional[str] = None
    metadata: Optional[Dict] = None
    usage_timestamp: Optional[datetime] = None
    
    @validator('usage_type')
    def validate_usage_type(cls, v):
        if v not in [usage.value for usage in UsageType]:
            raise ValueError('Invalid usage type')
        return v

class UsageStats(BaseModel):
    current_period: Dict[str, float]
    previous_period: Dict[str, float]
    total_cost_current: float
    total_cost_previous: float
    top_usage_types: List[Dict]

class InvoiceResponse(BaseModel):
    id: str
    invoice_number: str
    total_amount: float
    status: str
    due_date: datetime
    billing_period_start: datetime
    billing_period_end: datetime
    line_items: List[Dict]

class MonetizationEngine:
    """Core monetization and billing engine"""
    
    def __init__(self,
                 db_url: str = "postgresql://localhost/quantum_leads",
                 redis_url: str = "redis://localhost:6379",
                 stripe_api_key: str = None):
        
        # Database
        self.engine = create_engine(db_url)
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        
        # Redis for caching and rate limiting
        self.redis_client = redis.from_url(redis_url)
        
        # Stripe for payments
        if stripe_api_key:
            stripe.api_key = stripe_api_key
        
        # Password hashing
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        # JWT secret for API keys
        self.jwt_secret = "quantum-monetization-secret-key"  # Should be from env
        
        # Initialize default pricing
        asyncio.create_task(self.initialize_default_pricing())
        
        # Start background tasks
        asyncio.create_task(self.billing_cycle_processor())
        asyncio.create_task(self.usage_aggregator())
    
    def generate_api_key(self) -> Tuple[str, str, str]:
        """Generate new API key"""
        
        # Generate random key
        key = f"qai_{uuid.uuid4().hex}"
        
        # Create hash for storage
        key_hash = self.pwd_context.hash(key)
        
        # Get prefix for identification
        key_prefix = key[:12]
        
        return key, key_hash, key_prefix
    
    def verify_api_key(self, key: str, key_hash: str) -> bool:
        """Verify API key against hash"""
        return self.pwd_context.verify(key, key_hash)
    
    async def create_organization(self, org_data: OrganizationCreate) -> Organization:
        """Create new organization"""
        
        session_db = self.SessionLocal()
        
        try:
            # Create Stripe customer
            stripe_customer = None
            if stripe.api_key:
                try:
                    stripe_customer = stripe.Customer.create(
                        email=org_data.primary_contact_email,
                        name=org_data.name,
                        metadata={
                            'domain': org_data.domain,
                            'subscription_tier': org_data.subscription_tier
                        }
                    )
                except Exception as e:
                    logger.warning(f"Failed to create Stripe customer: {e}")
            
            # Set limits based on subscription tier
            tier_limits = self.get_tier_limits(org_data.subscription_tier)
            
            organization = Organization(
                name=org_data.name,
                domain=org_data.domain,
                subscription_tier=org_data.subscription_tier,
                billing_cycle=org_data.billing_cycle,
                primary_contact_email=org_data.primary_contact_email,
                billing_email=org_data.billing_email or org_data.primary_contact_email,
                phone=org_data.phone,
                stripe_customer_id=stripe_customer.id if stripe_customer else None,
                **tier_limits
            )
            
            session_db.add(organization)
            session_db.commit()
            
            # Create default API key
            await self.create_api_key(
                organization.id,
                APIKeyCreate(name="Default API Key", scopes=["*"])
            )
            
            logger.info(f"Created organization: {organization.name} ({organization.id})")
            return organization
        
        finally:
            session_db.close()
    
    def get_tier_limits(self, tier: str) -> Dict:
        """Get limits for subscription tier"""
        
        tier_configs = {
            SubscriptionTier.STARTER.value: {
                'monthly_call_minutes_limit': 5000,
                'monthly_leads_limit': 25000,
                'digital_personas_limit': 1,
                'api_rate_limit': 500
            },
            SubscriptionTier.PROFESSIONAL.value: {
                'monthly_call_minutes_limit': 15000,
                'monthly_leads_limit': 75000,
                'digital_personas_limit': 3,
                'api_rate_limit': 2000
            },
            SubscriptionTier.ENTERPRISE.value: {
                'monthly_call_minutes_limit': 50000,
                'monthly_leads_limit': 250000,
                'digital_personas_limit': 10,
                'api_rate_limit': 5000
            },
            SubscriptionTier.ELITE_WHITE_LABEL.value: {
                'monthly_call_minutes_limit': 200000,
                'monthly_leads_limit': 1000000,
                'digital_personas_limit': 50,
                'api_rate_limit': 20000,
                'is_white_label': True
            }
        }
        
        return tier_configs.get(tier, tier_configs[SubscriptionTier.STARTER.value])
    
    async def create_api_key(self, organization_id: str, key_data: APIKeyCreate) -> APIKeyResponse:
        """Create new API key for organization"""
        
        session_db = self.SessionLocal()
        
        try:
            # Generate key
            key, key_hash, key_prefix = self.generate_api_key()
            
            # Set expiration
            expires_at = None
            if key_data.expires_in_days:
                expires_at = datetime.utcnow() + timedelta(days=key_data.expires_in_days)
            
            api_key = APIKey(
                organization_id=organization_id,
                name=key_data.name,
                key_hash=key_hash,
                key_prefix=key_prefix,
                scopes=key_data.scopes,
                rate_limit_per_hour=key_data.rate_limit_per_hour,
                expires_at=expires_at
            )
            
            session_db.add(api_key)
            session_db.commit()
            
            return APIKeyResponse(
                id=api_key.id,
                name=api_key.name,
                key=key,  # Only returned on creation
                key_prefix=key_prefix,
                scopes=api_key.scopes,
                created_at=api_key.created_at,
                expires_at=api_key.expires_at
            )
        
        finally:
            session_db.close()
    
    async def authenticate_api_key(self, api_key: str) -> Optional[Tuple[Organization, APIKey]]:
        """Authenticate API key and return organization"""
        
        if not api_key or not api_key.startswith('qai_'):
            return None
        
        session_db = self.SessionLocal()
        
        try:
            # Get key prefix for lookup
            key_prefix = api_key[:12]
            
            # Find API key by prefix
            api_key_record = session_db.query(APIKey).filter(
                APIKey.key_prefix == key_prefix,
                APIKey.is_active == True
            ).first()
            
            if not api_key_record:
                return None
            
            # Verify key hash
            if not self.verify_api_key(api_key, api_key_record.key_hash):
                return None
            
            # Check expiration
            if api_key_record.expires_at and api_key_record.expires_at < datetime.utcnow():
                return None
            
            # Get organization
            organization = session_db.query(Organization).filter(
                Organization.id == api_key_record.organization_id,
                Organization.is_active == True
            ).first()
            
            if not organization:
                return None
            
            # Update last used
            api_key_record.last_used_at = datetime.utcnow()
            session_db.commit()
            
            return organization, api_key_record
        
        finally:
            session_db.close()
    
    async def check_rate_limit(self, api_key_id: str, organization_id: str) -> bool:
        """Check if request is within rate limits"""
        
        current_hour = datetime.utcnow().strftime('%Y-%m-%d-%H')
        
        # Check API key rate limit
        key_limit_key = f"rate_limit:api_key:{api_key_id}:{current_hour}"
        current_requests = self.redis_client.get(key_limit_key)
        
        if current_requests:
            current_requests = int(current_requests)
        else:
            current_requests = 0
        
        # Get API key limits
        session_db = self.SessionLocal()
        try:
            api_key = session_db.query(APIKey).filter(APIKey.id == api_key_id).first()
            if not api_key:
                return False
            
            if current_requests >= api_key.rate_limit_per_hour:
                return False
        finally:
            session_db.close()
        
        # Increment counter
        pipe = self.redis_client.pipeline()
        pipe.incr(key_limit_key)
        pipe.expire(key_limit_key, 3600)  # 1 hour
        pipe.execute()
        
        return True
    
    async def record_usage(self, organization_id: str, usage_data: UsageRecordCreate, api_key_id: str = None) -> UsageRecord:
        """Record usage for billing"""
        
        session_db = self.SessionLocal()
        
        try:
            # Get pricing for usage type
            unit_price = await self.get_usage_price(
                usage_data.usage_type,
                organization_id,
                usage_data.quantity
            )
            
            # Calculate total cost
            total_cost = Decimal(str(usage_data.quantity)) * unit_price
            total_cost = total_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Get billing period
            usage_timestamp = usage_data.usage_timestamp or datetime.utcnow()
            billing_period = usage_timestamp.strftime('%Y-%m')
            
            usage_record = UsageRecord(
                organization_id=organization_id,
                api_key_id=api_key_id,
                usage_type=usage_data.usage_type,
                quantity=Decimal(str(usage_data.quantity)),
                unit_price=unit_price,
                total_cost=total_cost,
                resource_id=usage_data.resource_id,
                metadata=usage_data.metadata or {},
                billing_period=billing_period,
                usage_timestamp=usage_timestamp
            )
            
            session_db.add(usage_record)
            session_db.commit()
            
            # Update real-time usage cache
            await self.update_usage_cache(organization_id, usage_data.usage_type, usage_data.quantity)
            
            logger.info(f"Recorded usage: {usage_data.usage_type} x {usage_data.quantity} = ${total_cost}")
            return usage_record
        
        finally:
            session_db.close()
    
    async def get_usage_price(self, usage_type: str, organization_id: str, quantity: float) -> Decimal:
        """Get price for usage type with volume discounts"""
        
        session_db = self.SessionLocal()
        
        try:
            # Get organization tier
            org = session_db.query(Organization).filter(Organization.id == organization_id).first()
            if not org:
                raise ValueError("Organization not found")
            
            # Find pricing rule
            pricing_rule = session_db.query(PricingRule).filter(
                PricingRule.usage_type == usage_type,
                PricingRule.subscription_tier == org.subscription_tier,
                PricingRule.is_active == True,
                PricingRule.effective_from <= datetime.utcnow()
            ).filter(
                (PricingRule.effective_until.is_(None)) |
                (PricingRule.effective_until > datetime.utcnow())
            ).first()
            
            if not pricing_rule:
                # Fallback to default pricing
                pricing_rule = session_db.query(PricingRule).filter(
                    PricingRule.usage_type == usage_type,
                    PricingRule.subscription_tier.is_(None),
                    PricingRule.is_active == True
                ).first()
            
            if not pricing_rule:
                # Hard-coded fallback
                default_prices = {
                    UsageType.VOICE_CALL_MINUTE.value: Decimal('1.00'),
                    UsageType.DIGITAL_HUMAN_SESSION.value: Decimal('50.00'),
                    UsageType.LEAD_PROCESSING.value: Decimal('0.10'),
                    UsageType.QUANTUM_SCORING.value: Decimal('0.25'),
                    UsageType.PLAYBOOK_GENERATION.value: Decimal('5.00'),
                    UsageType.API_REQUEST.value: Decimal('0.01')
                }
                return default_prices.get(usage_type, Decimal('1.00'))
            
            base_price = pricing_rule.base_price
            
            # Apply volume discounts
            if pricing_rule.volume_tiers:
                for tier in pricing_rule.volume_tiers:
                    if quantity >= tier.get('min_quantity', 0):
                        discount = tier.get('discount_percent', 0)
                        base_price = base_price * (1 - discount / 100)
            
            return base_price
        
        finally:
            session_db.close()
    
    async def update_usage_cache(self, organization_id: str, usage_type: str, quantity: float):
        """Update real-time usage cache"""
        
        current_month = datetime.utcnow().strftime('%Y-%m')
        
        # Update monthly usage
        monthly_key = f"usage:{organization_id}:{current_month}:{usage_type}"
        self.redis_client.incrbyfloat(monthly_key, quantity)
        self.redis_client.expire(monthly_key, 86400 * 32)  # 32 days
        
        # Update daily usage
        current_day = datetime.utcnow().strftime('%Y-%m-%d')
        daily_key = f"usage:{organization_id}:{current_day}:{usage_type}"
        self.redis_client.incrbyfloat(daily_key, quantity)
        self.redis_client.expire(daily_key, 86400 * 2)  # 2 days
    
    async def get_usage_stats(self, organization_id: str) -> UsageStats:
        """Get usage statistics for organization"""
        
        session_db = self.SessionLocal()
        
        try:
            # Current month
            current_month = datetime.utcnow().replace(day=1)
            next_month = (current_month + timedelta(days=32)).replace(day=1)
            
            current_usage = session_db.query(
                UsageRecord.usage_type,
                func.sum(UsageRecord.quantity).label('total_quantity'),
                func.sum(UsageRecord.total_cost).label('total_cost')
            ).filter(
                UsageRecord.organization_id == organization_id,
                UsageRecord.usage_timestamp >= current_month,
                UsageRecord.usage_timestamp < next_month
            ).group_by(UsageRecord.usage_type).all()
            
            # Previous month
            prev_month = (current_month - timedelta(days=1)).replace(day=1)
            
            previous_usage = session_db.query(
                UsageRecord.usage_type,
                func.sum(UsageRecord.quantity).label('total_quantity'),
                func.sum(UsageRecord.total_cost).label('total_cost')
            ).filter(
                UsageRecord.organization_id == organization_id,
                UsageRecord.usage_timestamp >= prev_month,
                UsageRecord.usage_timestamp < current_month
            ).group_by(UsageRecord.usage_type).all()
            
            # Format results
            current_period = {}
            total_cost_current = 0
            for usage in current_usage:
                current_period[usage.usage_type] = float(usage.total_quantity)
                total_cost_current += float(usage.total_cost)
            
            previous_period = {}
            total_cost_previous = 0
            for usage in previous_usage:
                previous_period[usage.usage_type] = float(usage.total_quantity)
                total_cost_previous += float(usage.total_cost)
            
            # Top usage types
            top_usage_types = [
                {
                    'usage_type': usage.usage_type,
                    'quantity': float(usage.total_quantity),
                    'cost': float(usage.total_cost)
                }
                for usage in sorted(current_usage, key=lambda x: x.total_cost, reverse=True)[:5]
            ]
            
            return UsageStats(
                current_period=current_period,
                previous_period=previous_period,
                total_cost_current=total_cost_current,
                total_cost_previous=total_cost_previous,
                top_usage_types=top_usage_types
            )
        
        finally:
            session_db.close()
    
    async def generate_invoice(self, organization_id: str, billing_period_start: datetime, billing_period_end: datetime) -> Invoice:
        """Generate invoice for billing period"""
        
        session_db = self.SessionLocal()
        
        try:
            # Get organization
            org = session_db.query(Organization).filter(Organization.id == organization_id).first()
            if not org:
                raise ValueError("Organization not found")
            
            # Get usage records for period
            usage_records = session_db.query(UsageRecord).filter(
                UsageRecord.organization_id == organization_id,
                UsageRecord.usage_timestamp >= billing_period_start,
                UsageRecord.usage_timestamp < billing_period_end,
                UsageRecord.is_billable == True,
                UsageRecord.invoice_id.is_(None)
            ).all()
            
            if not usage_records:
                logger.info(f"No billable usage for {org.name} in period")
                return None
            
            # Calculate totals
            subtotal = sum(record.total_cost for record in usage_records)
            
            # Calculate tax (simplified - should use proper tax service)
            tax_rate = Decimal('0.08')  # 8% tax
            tax_amount = subtotal * tax_rate
            total_amount = subtotal + tax_amount
            
            # Generate invoice number
            invoice_number = f"QAI-{datetime.utcnow().strftime('%Y%m')}-{org.id[:8].upper()}"
            
            # Create line items
            line_items = []
            usage_summary = {}
            
            for record in usage_records:
                if record.usage_type not in usage_summary:
                    usage_summary[record.usage_type] = {
                        'quantity': 0,
                        'total_cost': 0,
                        'unit_price': record.unit_price
                    }
                
                usage_summary[record.usage_type]['quantity'] += float(record.quantity)
                usage_summary[record.usage_type]['total_cost'] += float(record.total_cost)
            
            for usage_type, summary in usage_summary.items():
                line_items.append({
                    'description': usage_type.replace('_', ' ').title(),
                    'quantity': summary['quantity'],
                    'unit_price': float(summary['unit_price']),
                    'total': summary['total_cost']
                })
            
            # Create invoice
            invoice = Invoice(
                organization_id=organization_id,
                invoice_number=invoice_number,
                billing_period_start=billing_period_start,
                billing_period_end=billing_period_end,
                subtotal=subtotal,
                tax_amount=tax_amount,
                total_amount=total_amount,
                due_date=datetime.utcnow() + timedelta(days=30),
                line_items=line_items,
                status="draft"
            )
            
            session_db.add(invoice)
            session_db.flush()  # Get invoice ID
            
            # Link usage records to invoice
            for record in usage_records:
                record.invoice_id = invoice.id
            
            session_db.commit()
            
            # Create Stripe invoice if configured
            if stripe.api_key and org.stripe_customer_id:
                try:
                    await self.create_stripe_invoice(invoice, org)
                except Exception as e:
                    logger.error(f"Failed to create Stripe invoice: {e}")
            
            logger.info(f"Generated invoice {invoice_number} for ${total_amount}")
            return invoice
        
        finally:
            session_db.close()
    
    async def create_stripe_invoice(self, invoice: Invoice, organization: Organization):
        """Create Stripe invoice"""
        
        try:
            # Create Stripe invoice
            stripe_invoice = stripe.Invoice.create(
                customer=organization.stripe_customer_id,
                collection_method='send_invoice',
                days_until_due=30,
                metadata={
                    'internal_invoice_id': invoice.id,
                    'billing_period_start': invoice.billing_period_start.isoformat(),
                    'billing_period_end': invoice.billing_period_end.isoformat()
                }
            )
            
            # Add line items
            for item in invoice.line_items:
                stripe.InvoiceItem.create(
                    customer=organization.stripe_customer_id,
                    invoice=stripe_invoice.id,
                    description=item['description'],
                    quantity=int(item['quantity']),
                    unit_amount=int(item['unit_price'] * 100),  # Convert to cents
                    currency='usd'
                )
            
            # Finalize and send
            stripe_invoice = stripe.Invoice.finalize_invoice(stripe_invoice.id)
            stripe.Invoice.send_invoice(stripe_invoice.id)
            
            # Update our invoice
            session_db = self.SessionLocal()
            try:
                db_invoice = session_db.query(Invoice).filter(Invoice.id == invoice.id).first()
                if db_invoice:
                    db_invoice.stripe_invoice_id = stripe_invoice.id
                    db_invoice.status = "sent"
                    db_invoice.sent_at = datetime.utcnow()
                    session_db.commit()
            finally:
                session_db.close()
            
            logger.info(f"Created and sent Stripe invoice: {stripe_invoice.id}")
        
        except Exception as e:
            logger.error(f"Stripe invoice creation failed: {e}")
            raise
    
    async def billing_cycle_processor(self):
        """Background task to process billing cycles"""
        
        while True:
            try:
                # Run daily at 3 AM
                now = datetime.utcnow()
                next_run = now.replace(hour=3, minute=0, second=0, microsecond=0)
                if next_run <= now:
                    next_run += timedelta(days=1)
                
                wait_seconds = (next_run - now).total_seconds()
                await asyncio.sleep(wait_seconds)
                
                # Process monthly billing
                await self.process_monthly_billing()
                
                logger.info("Billing cycle processing completed")
                
            except Exception as e:
                logger.error(f"Error in billing cycle processor: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour on error
    
    async def process_monthly_billing(self):
        """Process monthly billing for all organizations"""
        
        session_db = self.SessionLocal()
        
        try:
            # Get organizations that need billing
            now = datetime.utcnow()
            
            # For monthly billing, check if it's the first day of the month
            if now.day != 1:
                return
            
            # Get previous month period
            current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            previous_month = (current_month - timedelta(days=1)).replace(day=1)
            
            organizations = session_db.query(Organization).filter(
                Organization.is_active == True,
                Organization.billing_cycle == BillingCycle.MONTHLY.value
            ).all()
            
            for org in organizations:
                try:
                    # Check if invoice already exists for this period
                    existing_invoice = session_db.query(Invoice).filter(
                        Invoice.organization_id == org.id,
                        Invoice.billing_period_start == previous_month,
                        Invoice.billing_period_end == current_month
                    ).first()
                    
                    if existing_invoice:
                        continue
                    
                    # Generate invoice
                    invoice = await self.generate_invoice(
                        org.id,
                        previous_month,
                        current_month
                    )
                    
                    if invoice:
                        logger.info(f"Generated monthly invoice for {org.name}")
                
                except Exception as e:
                    logger.error(f"Failed to generate invoice for {org.name}: {e}")
        
        finally:
            session_db.close()
    
    async def usage_aggregator(self):
        """Background task to aggregate usage data"""
        
        while True:
            try:
                # Run every hour
                await asyncio.sleep(3600)
                
                # Aggregate usage data for reporting
                await self.aggregate_hourly_usage()
                
            except Exception as e:
                logger.error(f"Error in usage aggregator: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error
    
    async def aggregate_hourly_usage(self):
        """Aggregate usage data for the previous hour"""
        
        session_db = self.SessionLocal()
        
        try:
            # Get previous hour
            now = datetime.utcnow()
            hour_start = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
            hour_end = hour_start + timedelta(hours=1)
            
            # Aggregate by organization and usage type
            aggregated_data = session_db.query(
                UsageRecord.organization_id,
                UsageRecord.usage_type,
                func.sum(UsageRecord.quantity).label('total_quantity'),
                func.sum(UsageRecord.total_cost).label('total_cost'),
                func.count(UsageRecord.id).label('record_count')
            ).filter(
                UsageRecord.usage_timestamp >= hour_start,
                UsageRecord.usage_timestamp < hour_end
            ).group_by(
                UsageRecord.organization_id,
                UsageRecord.usage_type
            ).all()
            
            # Store aggregated data in Redis for quick access
            hour_key = hour_start.strftime('%Y-%m-%d-%H')
            
            for data in aggregated_data:
                agg_key = f"usage_agg:{data.organization_id}:{hour_key}:{data.usage_type}"
                agg_data = {
                    'quantity': float(data.total_quantity),
                    'cost': float(data.total_cost),
                    'records': data.record_count
                }
                
                self.redis_client.setex(
                    agg_key,
                    86400 * 7,  # Keep for 7 days
                    json.dumps(agg_data)
                )
            
            logger.info(f"Aggregated usage data for hour {hour_key}")
        
        finally:
            session_db.close()
    
    async def initialize_default_pricing(self):
        """Initialize default pricing rules"""
        
        session_db = self.SessionLocal()
        
        try:
            # Check if pricing rules exist
            existing_count = session_db.query(PricingRule).count()
            if existing_count > 0:
                return
            
            # Default pricing rules
            default_pricing = [
                {
                    'usage_type': UsageType.VOICE_CALL_MINUTE.value,
                    'subscription_tier': SubscriptionTier.STARTER.value,
                    'base_price': Decimal('1.50')
                },
                {
                    'usage_type': UsageType.VOICE_CALL_MINUTE.value,
                    'subscription_tier': SubscriptionTier.PROFESSIONAL.value,
                    'base_price': Decimal('1.25')
                },
                {
                    'usage_type': UsageType.VOICE_CALL_MINUTE.value,
                    'subscription_tier': SubscriptionTier.ENTERPRISE.value,
                    'base_price': Decimal('1.00')
                },
                {
                    'usage_type': UsageType.VOICE_CALL_MINUTE.value,
                    'subscription_tier': SubscriptionTier.ELITE_WHITE_LABEL.value,
                    'base_price': Decimal('0.75')
                },
                {
                    'usage_type': UsageType.DIGITAL_HUMAN_SESSION.value,
                    'subscription_tier': None,  # Flat rate
                    'base_price': Decimal('50.00')
                },
                {
                    'usage_type': UsageType.LEAD_PROCESSING.value,
                    'subscription_tier': None,
                    'base_price': Decimal('0.10')
                },
                {
                    'usage_type': UsageType.QUANTUM_SCORING.value,
                    'subscription_tier': None,
                    'base_price': Decimal('0.25')
                },
                {
                    'usage_type': UsageType.PLAYBOOK_GENERATION.value,
                    'subscription_tier': None,
                    'base_price': Decimal('5.00')
                },
                {
                    'usage_type': UsageType.API_REQUEST.value,
                    'subscription_tier': None,
                    'base_price': Decimal('0.01')
                }
            ]
            
            for pricing_data in default_pricing:
                pricing_rule = PricingRule(
                    usage_type=pricing_data['usage_type'],
                    subscription_tier=pricing_data['subscription_tier'],
                    base_price=pricing_data['base_price'],
                    description=f"Default pricing for {pricing_data['usage_type']}"
                )
                
                session_db.add(pricing_rule)
            
            session_db.commit()
            logger.info("Initialized default pricing rules")
        
        finally:
            session_db.close()

# FastAPI application
app = FastAPI(
    title="Quantum AI Monetization APIs",
    description="Usage tracking, billing, and white-label deployment system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global monetization engine
monetization_engine = None

@app.on_event("startup")
async def startup_event():
    global monetization_engine
    
    import os
    monetization_engine = MonetizationEngine(
        stripe_api_key=os.getenv("STRIPE_SECRET_KEY")
    )
    
    logger.info("Monetization APIs started")

# Authentication dependency
async def get_current_organization(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Authenticate API key and return organization"""
    
    result = await monetization_engine.authenticate_api_key(credentials.credentials)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    organization, api_key = result
    
    # Check rate limits
    if not await monetization_engine.check_rate_limit(api_key.id, organization.id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return organization, api_key

@app.post("/organizations", response_model=dict)
async def create_organization(org_data: OrganizationCreate):
    """Create new organization"""
    try:
        organization = await monetization_engine.create_organization(org_data)
        return {
            'id': organization.id,
            'name': organization.name,
            'subscription_tier': organization.subscription_tier,
            'created_at': organization.created_at.isoformat()
        }
    except Exception as e:
        logger.error(f"Error creating organization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api-keys", response_model=APIKeyResponse)
async def create_api_key(
    key_data: APIKeyCreate,
    current_org: Tuple[Organization, APIKey] = Depends(get_current_organization)
):
    """Create new API key"""
    organization, _ = current_org
    
    try:
        api_key = await monetization_engine.create_api_key(organization.id, key_data)
        return api_key
    except Exception as e:
        logger.error(f"Error creating API key: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/usage")
async def record_usage(
    usage_data: UsageRecordCreate,
    current_org: Tuple[Organization, APIKey] = Depends(get_current_organization)
):
    """Record usage for billing"""
    organization, api_key = current_org
    
    try:
        usage_record = await monetization_engine.record_usage(
            organization.id,
            usage_data,
            api_key.id
        )
        
        return {
            'id': usage_record.id,
            'usage_type': usage_record.usage_type,
            'quantity': float(usage_record.quantity),
            'total_cost': float(usage_record.total_cost),
            'recorded_at': usage_record.recorded_at.isoformat()
        }
    except Exception as e:
        logger.error(f"Error recording usage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/usage/stats", response_model=UsageStats)
async def get_usage_stats(
    current_org: Tuple[Organization, APIKey] = Depends(get_current_organization)
):
    """Get usage statistics"""
    organization, _ = current_org
    
    try:
        stats = await monetization_engine.get_usage_stats(organization.id)
        return stats
    except Exception as e:
        logger.error(f"Error getting usage stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/invoices")
async def list_invoices(
    current_org: Tuple[Organization, APIKey] = Depends(get_current_organization)
):
    """List invoices for organization"""
    organization, _ = current_org
    
    session_db = monetization_engine.SessionLocal()
    
    try:
        invoices = session_db.query(Invoice).filter(
            Invoice.organization_id == organization.id
        ).order_by(Invoice.created_at.desc()).limit(50).all()
        
        return {
            'invoices': [{
                'id': inv.id,
                'invoice_number': inv.invoice_number,
                'total_amount': float(inv.total_amount),
                'status': inv.status,
                'due_date': inv.due_date.isoformat(),
                'billing_period_start': inv.billing_period_start.isoformat(),
                'billing_period_end': inv.billing_period_end.isoformat(),
                'created_at': inv.created_at.isoformat()
            } for inv in invoices]
        }
    
    finally:
        session_db.close()

@app.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: str,
    current_org: Tuple[Organization, APIKey] = Depends(get_current_organization)
):
    """Get specific invoice"""
    organization, _ = current_org
    
    session_db = monetization_engine.SessionLocal()
    
    try:
        invoice = session_db.query(Invoice).filter(
            Invoice.id == invoice_id,
            Invoice.organization_id == organization.id
        ).first()
        
        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")
        
        return InvoiceResponse(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            total_amount=float(invoice.total_amount),
            status=invoice.status,
            due_date=invoice.due_date,
            billing_period_start=invoice.billing_period_start,
            billing_period_end=invoice.billing_period_end,
            line_items=invoice.line_items
        )
    
    finally:
        session_db.close()

@app.post("/invoices/generate")
async def generate_invoice_manual(
    billing_period_start: datetime,
    billing_period_end: datetime,
    current_org: Tuple[Organization, APIKey] = Depends(get_current_organization)
):
    """Manually generate invoice for period"""
    organization, _ = current_org
    
    try:
        invoice = await monetization_engine.generate_invoice(
            organization.id,
            billing_period_start,
            billing_period_end
        )
        
        if not invoice:
            return {'message': 'No billable usage found for period'}
        
        return {
            'invoice_id': invoice.id,
            'invoice_number': invoice.invoice_number,
            'total_amount': float(invoice.total_amount),
            'status': invoice.status
        }
    except Exception as e:
        logger.error(f"Error generating invoice: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/organization")
async def get_organization_info(
    current_org: Tuple[Organization, APIKey] = Depends(get_current_organization)
):
    """Get organization information"""
    organization, _ = current_org
    
    return {
        'id': organization.id,
        'name': organization.name,
        'domain': organization.domain,
        'subscription_tier': organization.subscription_tier,
        'billing_cycle': organization.billing_cycle,
        'limits': {
            'monthly_call_minutes': organization.monthly_call_minutes_limit,
            'monthly_leads': organization.monthly_leads_limit,
            'digital_personas': organization.digital_personas_limit,
            'api_rate_limit': organization.api_rate_limit
        },
        'is_white_label': organization.is_white_label,
        'created_at': organization.created_at.isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }

# Webhook endpoint for Stripe
@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    """Handle Stripe webhooks"""
    
    payload = await request.body()
    sig_header = request.headers.get('stripe-signature')
    
    try:
        # Verify webhook signature
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
        )
        
        # Handle different event types
        if event['type'] == 'invoice.payment_succeeded':
            await handle_payment_succeeded(event['data']['object'])
        elif event['type'] == 'invoice.payment_failed':
            await handle_payment_failed(event['data']['object'])
        
        return {'status': 'success'}
    
    except Exception as e:
        logger.error(f"Stripe webhook error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

async def handle_payment_succeeded(stripe_invoice):
    """Handle successful payment"""
    
    session_db = monetization_engine.SessionLocal()
    
    try:
        # Find our invoice
        invoice = session_db.query(Invoice).filter(
            Invoice.stripe_invoice_id == stripe_invoice['id']
        ).first()
        
        if invoice:
            invoice.payment_status = 'paid'
            invoice.paid_at = datetime.utcnow()
            invoice.status = 'paid'
            session_db.commit()
            
            logger.info(f"Payment succeeded for invoice {invoice.invoice_number}")
    
    finally:
        session_db.close()

async def handle_payment_failed(stripe_invoice):
    """Handle failed payment"""
    
    session_db = monetization_engine.SessionLocal()
    
    try:
        # Find our invoice
        invoice = session_db.query(Invoice).filter(
            Invoice.stripe_invoice_id == stripe_invoice['id']
        ).first()
        
        if invoice:
            invoice.payment_status = 'failed'
            invoice.status = 'overdue'
            session_db.commit()
            
            logger.warning(f"Payment failed for invoice {invoice.invoice_number}")
    
    finally:
        session_db.close()

if __name__ == "__main__":
    uvicorn.run(
        "monetization_apis:app",
        host="0.0.0.0",
        port=8006,
        reload=True,
        log_level="info"
    )