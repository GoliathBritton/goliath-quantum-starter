from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from .entitlements import SubscriptionTier

class User(BaseModel):
    id: str
    email: str
    name: Optional[str] = None
    subscription_tier: SubscriptionTier = SubscriptionTier.BASIC
    created_at: datetime
    is_active: bool = True
    quantum_jobs_used: int = 0
    storage_used_gb: float = 0.0

class Partner(BaseModel):
    id: str
    company: str
    tier: str
    monthlyRevenue: float
    commissionRate: float
    totalCustomers: int

class Lead(BaseModel):
    id: str
    company: str
    contact: str
    email: str
    status: str
    estimatedValue: float
    source: str
    assignedPartner: Optional[str] = None

class CreateLead(BaseModel):
    company: str
    contact: str
    email: str
    estimatedValue: float
    source: str
    assignedPartner: Optional[str] = None

class QNexusQuery(BaseModel):
    query: str
    context: Optional[str] = None
    priority: Optional[str] = "normal"

class QNexusPrediction(BaseModel):
    id: str
    query: str
    prediction: str
    confidence: float
    timestamp: str
    quantumCredits: int

class QuantumJob(BaseModel):
    id: str
    type: str
    status: str
    input_data: dict
    result: Optional[dict] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    quantum_credits_used: int

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None

class LeadScoreRequest(BaseModel):
    lead_ids: List[str]
    criteria: Optional[dict] = None

class LeadScore(BaseModel):
    lead_id: str
    score: float
    factors: dict
    recommendation: str

class QNexusRequest(BaseModel):
    query: str
    context: Optional[str] = None
    parameters: Optional[dict] = None

class QNexusResponse(BaseModel):
    id: str
    query: str
    prediction: str
    confidence: float
    timestamp: str
    quantum_credits_used: int

class HealthCheck(BaseModel):
    status: str
    timestamp: datetime
    version: str
    services: dict