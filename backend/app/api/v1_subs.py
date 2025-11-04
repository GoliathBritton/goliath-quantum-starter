"""
Subscription Management API Routes
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.crm.subs import TIERS, resolve_entitlement
from app.crm.goliathcrm_client import GoliathCRM
from app.core.logging import get_logger

logger = get_logger(__name__)

# Initialize CRM client
crm_client = GoliathCRM()

# Request/Response Models
class SubscriptionRequest(BaseModel):
    """Subscription request"""
    tier: str
    customer_id: str
    billing_email: str
    payment_method: Optional[str] = None

class SubscriptionResponse(BaseModel):
    """Subscription response"""
    subscription_id: str
    tier: str
    status: str
    agents_available: List[str]
    limits: Dict[str, Any]
    billing_cycle: str = "monthly"

class UsageMetrics(BaseModel):
    """Usage metrics for subscription"""
    agent_calls: int
    api_requests: int
    quantum_processing_time: float
    storage_used: float

class TierUpgradeRequest(BaseModel):
    """Tier upgrade request"""
    current_tier: str
    target_tier: str
    customer_id: str

# Router
router = APIRouter()

@router.get("/catalog")
async def get_subscription_catalog():
    """Get complete subscription catalog with pricing and features"""
    return {
        "tiers": {
            "LaunchPad": {
                "name": "LaunchPad",
                "price": "/month",
                "description": "Perfect for SMBs scaling sales operations",
                "agents": [
                    "Quantum Lead Qualifier",
                    "Quantum Chat Agent",
                    "Quantum Voice Assistant", 
                    "Quantum Follow-up Specialist",
                    "Lead Ingestion Engine"
                ],
                "limits": {
                    "monthly_calls": 1000,
                    "api_requests": 10000,
                    "quantum_processing_hours": 10,
                    "storage_gb": 10
                },
                "features": [
                    "Basic CRM integration",
                    "Standard support",
                    "Core analytics",
                    "5 concurrent users"
                ]
            },
            "ScaleUp": {
                "name": "ScaleUp", 
                "price": "/month",
                "description": "Ideal for mid-market firms scaling operations",
                "agents": [
                    "Quantum Sales Navigator",
                    "Quantum Objection Handler",
                    "Quantum Demo Scheduler",
                    "Quantum ROI Calculator",
                    "Quantum Relationship Builder",
                    "QSAI Calling Agent"
                ],
                "limits": {
                    "monthly_calls": 10000,
                    "api_requests": 100000,
                    "quantum_processing_hours": 100,
                    "storage_gb": 100
                },
                "features": [
                    "Advanced CRM integration",
                    "Priority support",
                    "Advanced analytics",
                    "White-label options",
                    "25 concurrent users"
                ]
            },
            "Enterprise": {
                "name": "Enterprise",
                "price": "+/year",
                "description": "Complete autonomous business ecosystem",
                "agents": "ALL_18_AGENTS",
                "limits": {
                    "monthly_calls": "unlimited",
                    "api_requests": "unlimited", 
                    "quantum_processing_hours": "unlimited",
                    "storage_gb": "unlimited"
                },
                "features": [
                    "Full CRM integration",
                    "24/7 dedicated support",
                    "Custom quantum models",
                    "Full white-label licensing",
                    "Unlimited concurrent users",
                    "Quantum High Council oversight",
                    "Custom integrations",
                    "SLA guarantees"
                ]
            }
        },
        "total_agents": 18,
        "pricing_model": "subscription",
        "billing_cycles": ["monthly", "annual"],
        "enterprise_options": {
            "custom_pricing": True,
            "volume_discounts": True,
            "pilot_programs": True,
            "roi_based_pricing": True
        }
    }

@router.post("/create", response_model=SubscriptionResponse)
async def create_subscription(request: SubscriptionRequest):
    """Create new subscription"""
    try:
        logger.info(f"Creating subscription for customer {request.customer_id}, tier: {request.tier}")
        
        # Validate tier
        if request.tier not in TIERS:
            raise HTTPException(status_code=400, detail=f"Invalid tier: {request.tier}")
        
        # Get tier details
        tier_details = TIERS[request.tier]
        
        # Create subscription in CRM
        subscription_data = {
            "customer_id": request.customer_id,
            "tier": request.tier,
            "billing_email": request.billing_email,
            "payment_method": request.payment_method,
            "status": "active",
            "agents_available": tier_details["agents"],
            "limits": tier_details["limits"]
        }
        
        # Mock subscription creation (replace with actual CRM call)
        subscription_id = f"sub_{request.customer_id}_{request.tier}_{hash(request.billing_email) % 10000}"
        
        # Log to CRM
        crm_client.log_interaction(
            lead_id=request.customer_id,
            summary=f"Subscription created: {request.tier} tier"
        )
        
        return SubscriptionResponse(
            subscription_id=subscription_id,
            tier=request.tier,
            status="active",
            agents_available=tier_details["agents"],
            limits=tier_details["limits"]
        )
        
    except Exception as e:
        logger.error(f"Subscription creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Subscription creation failed: {str(e)}")

@router.get("/{customer_id}/entitlement")
async def get_customer_entitlement(customer_id: str):
    """Get customer's subscription entitlements"""
    try:
        logger.info(f"Getting entitlements for customer: {customer_id}")
        
        # Mock customer lookup (replace with actual CRM query)
        customer_tier = "ScaleUp"  # This would come from CRM
        
        entitlement = resolve_entitlement(customer_tier)
        
        return {
            "customer_id": customer_id,
            "tier": entitlement.tier,
            "agents": entitlement.agents,
            "limits": entitlement.limits,
            "status": "active",
            "renewal_date": "2024-12-01"
        }
        
    except Exception as e:
        logger.error(f"Entitlement lookup failed: {e}")
        raise HTTPException(status_code=500, detail=f"Entitlement lookup failed: {str(e)}")

@router.post("/upgrade")
async def upgrade_subscription(request: TierUpgradeRequest):
    """Upgrade customer subscription tier"""
    try:
        logger.info(f"Upgrading customer {request.customer_id} from {request.current_tier} to {request.target_tier}")
        
        # Validate upgrade path
        valid_upgrades = {
            "LaunchPad": ["ScaleUp", "Enterprise"],
            "ScaleUp": ["Enterprise"]
        }
        
        if request.target_tier not in valid_upgrades.get(request.current_tier, []):
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot upgrade from {request.current_tier} to {request.target_tier}"
            )
        
        # Get new tier details
        new_entitlement = resolve_entitlement(request.target_tier)
        
        # Process upgrade (mock implementation)
        upgrade_result = {
            "customer_id": request.customer_id,
            "previous_tier": request.current_tier,
            "new_tier": request.target_tier,
            "effective_date": "2024-10-01",
            "new_agents": new_entitlement.agents,
            "new_limits": new_entitlement.limits,
            "prorated_amount": 5000,  # Mock prorated amount
            "status": "upgraded"
        }
        
        # Log upgrade to CRM
        crm_client.log_interaction(
            lead_id=request.customer_id,
            summary=f"Tier upgraded from {request.current_tier} to {request.target_tier}"
        )
        
        return upgrade_result
        
    except Exception as e:
        logger.error(f"Subscription upgrade failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upgrade failed: {str(e)}")

@router.get("/{customer_id}/usage")
async def get_usage_metrics(customer_id: str):
    """Get customer usage metrics"""
    try:
        logger.info(f"Getting usage metrics for customer: {customer_id}")
        
        # Mock usage data (replace with actual metrics collection)
        usage_data = {
            "customer_id": customer_id,
            "current_period": "2024-10-01 to 2024-10-31",
            "metrics": {
                "agent_calls": 2450,
                "api_requests": 18750,
                "quantum_processing_time": 12.5,  # hours
                "storage_used": 8.3  # GB
            },
            "limits": {
                "monthly_calls": 10000,
                "api_requests": 100000,
                "quantum_processing_hours": 100,
                "storage_gb": 100
            },
            "utilization": {
                "calls": "24.5%",
                "api_requests": "18.75%", 
                "quantum_processing": "12.5%",
                "storage": "8.3%"
            },
            "alerts": []  # No alerts currently
        }
        
        return usage_data
        
    except Exception as e:
        logger.error(f"Usage metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Usage metrics failed: {str(e)}")

@router.post("/{customer_id}/billing")
async def process_billing(customer_id: str, billing_data: Dict[str, Any]):
    """Process billing for customer"""
    try:
        logger.info(f"Processing billing for customer: {customer_id}")
        
        # Mock billing processing
        billing_result = {
            "customer_id": customer_id,
            "billing_period": "2024-10-01 to 2024-10-31",
            "amount": 15000,  # Mock amount
            "currency": "USD",
            "status": "paid",
            "payment_method": "credit_card",
            "transaction_id": f"txn_{customer_id}_{hash(str(billing_data)) % 100000}",
            "invoice_url": f"https://billing.goliath.local/invoices/{customer_id}_2024_10"
        }
        
        # Log billing to CRM
        crm_client.log_interaction(
            lead_id=customer_id,
            summary=f"Billing processed:  {billing_result['status']}"
        )
        
        return billing_result
        
    except Exception as e:
        logger.error(f"Billing processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Billing failed: {str(e)}")

@router.get("/health")
async def subscription_health():
    """Health check for subscription services"""
    return {
        "service": "subscription_management",
        "status": "healthy",
        "capabilities": [
            "Subscription catalog management",
            "Tier-based access control",
            "Usage tracking and billing",
            "CRM integration",
            "Upgrade/downgrade processing"
        ],
        "supported_tiers": ["LaunchPad", "ScaleUp", "Enterprise"],
        "billing_providers": ["Stripe", "Custom"],
        "crm_integration": "GoliathCRM"
    }
