"""Pydantic models for NQBA Core API

Data models corresponding to the OpenAPI specification schemas.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# Enums
class PartnerTier(str, Enum):
    bronze = "bronze"
    silver = "silver"
    gold = "gold"
    platinum = "platinum"


class PartnerStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    terminated = "terminated"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class LeadStatus(str, Enum):
    new = "new"
    qualified = "qualified"
    contacted = "contacted"
    converted = "converted"
    lost = "lost"


class TaskStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class ScoreImpact(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


class InvoiceStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    overdue = "overdue"
    cancelled = "cancelled"


class PayoutStatus(str, Enum):
    pending = "pending"
    processed = "processed"
    failed = "failed"


class TransactionStatus(str, Enum):
    pending = "pending"
    confirmed = "confirmed"
    failed = "failed"


class BlockchainNetwork(str, Enum):
    ethereum = "ethereum"
    polygon = "polygon"
    bsc = "bsc"
    solana = "solana"


# Authentication Models
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    refresh_token: Optional[str] = None


# Partner Models
class PartnerRegistrationRequest(BaseModel):
    company_name: str
    contact_email: EmailStr
    contact_name: Optional[str] = None
    tier: PartnerTier
    description: Optional[str] = None


class PartnerRegistrationResponse(BaseModel):
    partner_id: str
    api_key: str
    status: PartnerStatus


class Partner(BaseModel):
    id: str
    company_name: str
    contact_email: EmailStr
    tier: PartnerTier
    status: PartnerStatus
    created_at: datetime
    revenue_share: Optional[float] = None


class TierUpdateRequest(BaseModel):
    tier: PartnerTier
    effective_date: Optional[date] = None


# Lead Models
class Lead(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[LeadStatus] = LeadStatus.new
    source: Optional[str] = None
    created_at: Optional[datetime] = None
    custom_fields: Optional[Dict[str, Any]] = None


class Pagination(BaseModel):
    page: int
    limit: int
    total: int
    pages: int


class LeadsListResponse(BaseModel):
    leads: List[Lead]
    pagination: Pagination


# Scoring Models
class ScoreFactor(BaseModel):
    name: str
    weight: float
    value: float
    impact: ScoreImpact


class ScoreResponse(BaseModel):
    lead_id: str
    score: float = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=1)
    factors: List[ScoreFactor]
    model_version: str
    scored_at: datetime


# Billing Models
class Invoice(BaseModel):
    id: str
    partner_id: str
    amount: float
    currency: str
    status: InvoiceStatus
    due_date: date
    created_at: datetime


class Payout(BaseModel):
    id: str
    partner_id: str
    amount: float
    currency: str
    status: PayoutStatus
    processed_at: Optional[datetime] = None


# Web3 Models
class TransactionRequest(BaseModel):
    to_address: str
    amount: float
    network: BlockchainNetwork
    gas_price: Optional[float] = None
    data: Optional[str] = None


class TransactionResponse(BaseModel):
    transaction_hash: str
    status: TransactionStatus
    network: str
    gas_used: Optional[float] = None
    cost: Optional[float] = None


# Audit Models
class AuditLog(BaseModel):
    id: str
    timestamp: datetime
    user_id: str
    action: str
    resource: str
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


# Task Models
class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    created_at: datetime
    estimated_completion: Optional[datetime] = None


# Error Models
class ErrorResponse(BaseModel):
    error: str
    message: str
    code: int
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime


# Recipe Models (from OpenAPI)
class Recipe(BaseModel):
    id: str
    name: str
    description: str
    category: str
    difficulty: str
    prep_time: int
    cook_time: int
    servings: int
    ingredients: List[str]
    instructions: List[str]
    nutrition: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    created_at: datetime


class RecipeRequest(BaseModel):
    name: str
    description: str
    category: str
    difficulty: str
    prep_time: int
    cook_time: int
    servings: int
    ingredients: List[str]
    instructions: List[str]
    nutrition: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None


# Compute Models
class ComputeJob(BaseModel):
    id: str
    type: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ComputeRequest(BaseModel):
    type: str
    parameters: Dict[str, Any]
    priority: Optional[str] = "normal"


# Integration Models
class Integration(BaseModel):
    id: str
    name: str
    type: str
    status: str
    config: Dict[str, Any]
    created_at: datetime
    last_sync: Optional[datetime] = None


class IntegrationRequest(BaseModel):
    name: str
    type: str
    config: Dict[str, Any]


# Marketplace Models
class MarketplaceItem(BaseModel):
    id: str
    name: str
    description: str
    category: str
    price: float
    currency: str
    provider: str
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    created_at: datetime


class MarketplacePurchase(BaseModel):
    item_id: str
    quantity: Optional[int] = 1
    payment_method: str