from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Goliath of All Trade - Diversegy Integration Models
# Energy brokerage integration with https://diversegy.com/ and https://partners.diversegypro.com/

class DiversegyPlanType(str, Enum):
    FIXED = "fixed"
    VARIABLE = "variable"
    RENEWABLE = "renewable"
    CUSTOM = "custom"

class DiversegyEnergyType(str, Enum):
    ELECTRICITY = "electricity"
    NATURAL_GAS = "natural_gas"
    RENEWABLE = "renewable"

class DiversegyCustomer(BaseModel):
    id: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: str
    city: str
    state: str
    zip_code: str
    created_at: datetime
    status: str = "active"
    partner_id: Optional[str] = None

class DiversegyPlan(BaseModel):
    id: str
    name: str
    description: str
    type: DiversegyPlanType
    energy_type: DiversegyEnergyType
    rate: float
    term_months: int
    is_renewable: bool = False
    renewable_percentage: Optional[float] = None
    available_states: List[str]
    provider: str
    features: List[str] = []
    
class DiversegyQuote(BaseModel):
    id: str
    customer_id: str
    plan_id: str
    monthly_usage_kwh: Optional[float] = None
    monthly_usage_therms: Optional[float] = None
    estimated_monthly_cost: float
    estimated_annual_cost: float
    estimated_savings: Optional[float] = None
    created_at: datetime
    expires_at: datetime
    status: str = "pending"

class DiversegyEnrollment(BaseModel):
    id: str
    customer_id: str
    plan_id: str
    quote_id: Optional[str] = None
    start_date: datetime
    end_date: datetime
    status: str = "pending"
    contract_signed: bool = False
    documents: List[str] = []
    partner_commission: Optional[float] = None

class DiversegyPartnerStats(BaseModel):
    partner_id: str
    total_customers: int
    active_enrollments: int
    pending_enrollments: int
    total_commission: float
    monthly_commission: Dict[str, float] = {}
    energy_types: Dict[str, int] = {}
    plan_types: Dict[str, int] = {}

class DiversegyAPIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    errors: Optional[List[str]] = None