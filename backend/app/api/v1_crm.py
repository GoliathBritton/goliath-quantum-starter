"""
GoliathCRM API Routes - Lead management and sales tracking
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.crm.goliathcrm_client import GoliathCRM
from app.core.logging import get_logger

logger = get_logger(__name__)

# Initialize CRM client
crm_client = GoliathCRM()

# Request/Response Models
class LeadRequest(BaseModel):
    """Lead creation request"""
    name: str
    email: str
    company: Optional[str] = None
    phone: Optional[str] = None
    source: Optional[str] = "FLYFOX-AI-Website"
    industry: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    tier_interest: Optional[str] = "LaunchPad"
    use_case: Optional[str] = None
    current_solution: Optional[str] = None

class LeadResponse(BaseModel):
    """Lead creation response"""
    id: str
    status: str
    name: str
    email: str
    quantum_assigned: bool
    created_at: str

class InteractionRequest(BaseModel):
    """Interaction logging request"""
    lead_id: str
    summary: str
    interaction_type: str = "system"

class OpportunityRequest(BaseModel):
    """Opportunity creation request"""
    name: str
    lead_id: str
    value: float
    stage: str = "prospecting"
    probability: float = 0.0
    close_date: Optional[str] = None

class ROITrackingRequest(BaseModel):
    """ROI tracking request"""
    customer_id: str
    cost_savings: float = 0.0
    revenue_increase: float = 0.0
    efficiency_gains: float = 0.0
    investment: float = 0.0

# Router
router = APIRouter()

@router.post("/leads", response_model=LeadResponse)
async def create_lead(request: LeadRequest):
    """
    Create new lead in GoliathCRM
    
    Automatically assigns to Quantum Sales Navigator for processing
    """
    try:
        logger.info(f"Creating lead: {request.name} ({request.email})")
        
        # Convert Pydantic model to dict
        lead_data = request.model_dump()
        
        # Create lead in CRM
        result = crm_client.create_lead(lead_data)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        # Prepare response
        response = LeadResponse(
            id=result["id"],
            status=result["status"],
            name=request.name,
            email=request.email,
            quantum_assigned=result.get("quantum_assigned", True),
            created_at=result["created_at"]
        )
        
        logger.info(f"Lead created successfully: {response.id}")
        return response
        
    except Exception as e:
        logger.error(f"Lead creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lead creation failed: {str(e)}")

@router.get("/leads/{lead_id}")
async def get_lead(lead_id: str):
    """Get detailed lead information"""
    try:
        logger.info(f"Getting lead details: {lead_id}")
        
        lead_data = crm_client.get_lead_details(lead_id)
        
        if "error" in lead_data:
            raise HTTPException(status_code=404, detail=lead_data["error"])
        
        return lead_data
        
    except Exception as e:
        logger.error(f"Lead retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lead retrieval failed: {str(e)}")

@router.put("/leads/{lead_id}")
async def update_lead(lead_id: str, update_data: Dict[str, Any]):
    """Update lead information"""
    try:
        logger.info(f"Updating lead: {lead_id}")
        
        result = crm_client.update_lead(lead_id, update_data)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Lead update failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lead update failed: {str(e)}")

@router.post("/interactions")
async def log_interaction(request: InteractionRequest):
    """Log interaction with lead"""
    try:
        logger.info(f"Logging interaction for lead {request.lead_id}")
        
        result = crm_client.log_interaction(
            lead_id=request.lead_id,
            summary=request.summary,
            interaction_type=request.interaction_type
        )
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Interaction logging failed: {e}")
        raise HTTPException(status_code=500, detail=f"Interaction logging failed: {str(e)}")

@router.post("/opportunities")
async def create_opportunity(request: OpportunityRequest):
    """Create sales opportunity"""
    try:
        logger.info(f"Creating opportunity: {request.name}")
        
        opportunity_data = {
            "name": request.name,
            "lead_id": request.lead_id,
            "value": request.value,
            "stage": request.stage,
            "probability": request.probability,
            "close_date": request.close_date
        }
        
        result = crm_client.create_opportunity(opportunity_data)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Opportunity creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Opportunity creation failed: {str(e)}")

@router.put("/opportunities/{opportunity_id}/stage")
async def update_opportunity_stage(opportunity_id: str, stage_data: Dict[str, str]):
    """Update opportunity stage"""
    try:
        logger.info(f"Updating opportunity {opportunity_id} stage")
        
        stage = stage_data.get("stage")
        notes = stage_data.get("notes", "")
        
        if not stage:
            raise HTTPException(status_code=400, detail="Stage is required")
        
        result = crm_client.update_opportunity_stage(opportunity_id, stage, notes)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Opportunity stage update failed: {e}")
        raise HTTPException(status_code=500, detail=f"Stage update failed: {str(e)}")

@router.post("/roi/track")
async def track_roi(request: ROITrackingRequest):
    """Track ROI metrics for customer"""
    try:
        logger.info(f"Tracking ROI for customer: {request.customer_id}")
        
        metrics = {
            "cost_savings": request.cost_savings,
            "revenue_increase": request.revenue_increase,
            "efficiency_gains": request.efficiency_gains,
            "investment": request.investment
        }
        
        result = crm_client.track_roi(request.customer_id, metrics)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"ROI tracking failed: {e}")
        raise HTTPException(status_code=500, detail=f"ROI tracking failed: {str(e)}")

@router.get("/metrics/sales")
async def get_sales_metrics(date_range: Dict[str, str]):
    """Get sales metrics and KPIs"""
    try:
        logger.info("Getting sales metrics")
        
        result = crm_client.get_sales_metrics(date_range)
        
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except Exception as e:
        logger.error(f"Sales metrics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Sales metrics failed: {str(e)}")

@router.get("/customers/{customer_id}/dashboard")
async def get_customer_dashboard(customer_id: str):
    """Get comprehensive customer dashboard"""
    try:
        logger.info(f"Getting dashboard for customer: {customer_id}")
        
        dashboard_data = crm_client.get_customer_dashboard(customer_id)
        
        if "error" in dashboard_data:
            raise HTTPException(status_code=404, detail=dashboard_data["error"])
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Customer dashboard retrieval failed: {e}")
        raise HTTPException(status_code=500, detail=f"Dashboard retrieval failed: {str(e)}")

@router.get("/leads")
async def list_leads(limit: int = 50, offset: int = 0, status: Optional[str] = None):
    """List leads with optional filtering"""
    try:
        logger.info(f"Listing leads: limit={limit}, offset={offset}, status={status}")
        
        # Mock lead listing (replace with actual CRM query)
        leads = [
            {
                "id": f"lead_{i}",
                "name": f"Lead {i}",
                "email": f"lead{i}@example.com",
                "company": f"Company {i}",
                "status": "New" if i % 3 == 0 else "Qualified",
                "created_at": "2024-10-04T09:00:00Z",
                "quantum_assigned": True
            }
            for i in range(1, min(limit + 1, 11))
        ]
        
        # Filter by status if provided
        if status:
            leads = [lead for lead in leads if lead["status"] == status]
        
        return {
            "leads": leads,
            "total_count": len(leads),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"Lead listing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lead listing failed: {str(e)}")

@router.get("/opportunities")
async def list_opportunities(limit: int = 50, offset: int = 0, stage: Optional[str] = None):
    """List opportunities with optional filtering"""
    try:
        logger.info(f"Listing opportunities: limit={limit}, offset={offset}, stage={stage}")
        
        # Mock opportunity listing
        opportunities = [
            {
                "id": f"opp_{i}",
                "name": f"Opportunity {i}",
                "lead_id": f"lead_{i}",
                "value": 10000 + (i * 5000),
                "stage": ["prospecting", "qualification", "proposal", "negotiation", "closing"][i % 5],
                "probability": 0.2 + (i * 0.1),
                "close_date": "2024-12-01",
                "created_at": "2024-10-04T09:00:00Z"
            }
            for i in range(1, min(limit + 1, 11))
        ]
        
        # Filter by stage if provided
        if stage:
            opportunities = [opp for opp in opportunities if opp["stage"] == stage]
        
        return {
            "opportunities": opportunities,
            "total_count": len(opportunities),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"Opportunity listing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Opportunity listing failed: {str(e)}")

@router.get("/health")
async def crm_health():
    """Health check for GoliathCRM integration"""
    return {
        "service": "goliathcrm",
        "status": "healthy",
        "capabilities": [
            "Lead management and tracking",
            "Opportunity pipeline management",
            "Interaction logging and history",
            "ROI tracking and reporting",
            "Sales metrics and KPIs",
            "Customer dashboard",
            "Quantum agent assignment"
        ],
        "integration": {
            "crm_system": "GoliathCRM",
            "quantum_assignment": True,
            "roi_tracking": True,
            "real_time_sync": True
        },
        "endpoints": {
            "leads": "/api/v1/crm/leads",
            "opportunities": "/api/v1/crm/opportunities", 
            "interactions": "/api/v1/crm/interactions",
            "metrics": "/api/v1/crm/metrics/sales",
            "dashboard": "/api/v1/crm/customers/{id}/dashboard"
        }
    }
