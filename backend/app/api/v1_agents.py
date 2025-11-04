"""
API Routes for Quantum Agents
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from app.agents.sales.navigator import QuantumSalesNavigator
from app.core.logging import get_logger

logger = get_logger(__name__)

# Request/Response Models
class OpportunityContext(BaseModel):
    """Opportunity context for sales navigation"""
    id: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    personas: List[str] = []
    current_stage: str = "prospecting"
    objections: List[str] = []
    competitive_landscape: Optional[Dict[str, Any]] = None

class NavigationResponse(BaseModel):
    """Response from sales navigation"""
    agent: str
    strategy: str
    confidence_score: float
    next_steps: List[str]
    risk_factors: List[str]
    success_probability: float
    quantum_optimization: Optional[Dict[str, Any]] = None
    objection_reversals: Optional[List[Dict[str, Any]]] = None

class TimingOptimizationRequest(BaseModel):
    """Request for timing optimization"""
    opportunity_context: OpportunityContext

class OutcomePredictionRequest(BaseModel):
    """Request for outcome prediction"""
    opportunity_context: OpportunityContext

# Router
router = APIRouter()

# Initialize agents
navigator = QuantumSalesNavigator()

@router.post("/sales/navigator/recommend-path", response_model=NavigationResponse)
async def recommend_sales_path(context: OpportunityContext):
    """
    Get quantum-optimized sales path recommendation
    
    Uses REVERSAL REASONINGâ„¢ to turn objections into opportunities
    and provides predictive navigation for complex deal cycles.
    """
    try:
        logger.info(f"Processing navigation request for opportunity: {context.id}")
        
        # Convert Pydantic model to dict
        context_dict = context.model_dump()
        
        # Get recommendation from Quantum Sales Navigator
        recommendation = navigator.recommend_path(context_dict)
        
        # Validate response structure
        response = NavigationResponse(
            agent=recommendation.get("agent", "quantum_sales_navigator"),
            strategy=recommendation.get("strategy", "No strategy available"),
            confidence_score=recommendation.get("confidence_score", 0.0),
            next_steps=recommendation.get("next_steps", []),
            risk_factors=recommendation.get("risk_factors", []),
            success_probability=recommendation.get("success_probability", 0.0),
            quantum_optimization=recommendation.get("quantum_optimization"),
            objection_reversals=recommendation.get("objection_reversals")
        )
        
        logger.info(f"Navigation completed with {response.confidence_score}% confidence")
        return response
        
    except Exception as e:
        logger.error(f"Navigation request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Navigation failed: {str(e)}")

@router.post("/sales/navigator/optimize-timing")
async def optimize_timing(request: TimingOptimizationRequest):
    """Optimize timing for sales activities"""
    try:
        logger.info("Processing timing optimization request")
        
        timing_result = navigator.optimize_timing(request.opportunity_context.model_dump())
        
        return {
            "status": "success",
            "timing_optimization": timing_result
        }
        
    except Exception as e:
        logger.error(f"Timing optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Timing optimization failed: {str(e)}")

@router.post("/sales/navigator/predict-outcome")
async def predict_outcome(request: OutcomePredictionRequest):
    """Predict deal outcome with quantum probability modeling"""
    try:
        logger.info("Processing outcome prediction request")
        
        prediction = navigator.predict_outcome(request.opportunity_context.model_dump())
        
        return {
            "status": "success",
            "outcome_prediction": prediction
        }
        
    except Exception as e:
        logger.error(f"Outcome prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Outcome prediction failed: {str(e)}")

@router.get("/sales/navigator/health")
async def navigator_health():
    """Health check for Quantum Sales Navigator"""
    return {
        "agent": "quantum_sales_navigator",
        "status": "healthy",
        "capabilities": [
            "Predictive deal pathfinding",
            "REVERSAL REASONINGâ„¢ objection handling",
            "Quantum-optimized timing",
            "Outcome prediction modeling"
        ],
        "tier_required": "ScaleUp"
    }

@router.get("/catalog")
async def get_agent_catalog():
    """Get complete agent catalog with capabilities and tier requirements"""
    return {
        "agents": [
            {
                "id": "quantum_sales_navigator",
                "name": "Quantum Sales Navigator",
                "category": "Sales & Growth",
                "tier_required": "ScaleUp",
                "capabilities": [
                    "Predictive deal pathfinding",
                    "REVERSAL REASONINGâ„¢ objection handling", 
                    "Quantum-optimized timing",
                    "Outcome prediction modeling"
                ],
                "singularity": "Predicts deal trajectories with QUBO optimization + client psychology models",
                "roi_impact": "300% improvement in deal closure rates"
            },
            {
                "id": "quantum_lead_qualifier",
                "name": "Quantum Lead Qualifier",
                "category": "Sales & Growth",
                "tier_required": "LaunchPad",
                "capabilities": [
                    "QUBO-based lead scoring",
                    "Predictive qualification",
                    "Priority ranking"
                ],
                "singularity": "Identifies hidden patterns in lead data beyond linear scoring",
                "roi_impact": "85%+ accuracy; processes 1,000+ leads/hour"
            },
            {
                "id": "quantum_objection_handler",
                "name": "Quantum Objection Handler", 
                "category": "Sales & Growth",
                "tier_required": "ScaleUp",
                "capabilities": [
                    "Real-time objection detection",
                    "REVERSAL REASONINGâ„¢ responses",
                    "Pattern tracking"
                ],
                "singularity": "Reverse-maps objection paths into opportunities",
                "roi_impact": "Converts 40% of objections into new deals"
            }
            # Add more agents as implemented
        ],
        "total_agents": 18,
        "tiers": {
            "LaunchPad": {
                "price": "/month",
                "agents": 5,
                "target": "SMBs"
            },
            "ScaleUp": {
                "price": "/month", 
                "agents": 12,
                "target": "Mid-market"
            },
            "Enterprise": {
                "price": "+/year",
                "agents": 18,
                "target": "Global enterprises"
            }
        }
    }

@router.get("/tier/{tier_name}/agents")
async def get_tier_agents(tier_name: str):
    """Get agents available for a specific subscription tier"""
    tier_agents = {
        "LaunchPad": [
            "quantum_lead_qualifier",
            "quantum_chat_agent", 
            "quantum_voice_assistant",
            "quantum_followup_specialist",
            "lead_ingestion_engine"
        ],
        "ScaleUp": [
            "quantum_sales_navigator",
            "quantum_objection_handler",
            "quantum_demo_scheduler",
            "quantum_roi_calculator",
            "quantum_relationship_builder",
            "qsai_calling_agent"
        ],
        "Enterprise": [
            "quantum_closer",
            "quantum_pricing_negotiator",
            "digital_human",
            "quantum_industry_expert",
            "quantum_competitive_analyzer",
            "sigma_select_agent",
            "goliath_energy_agent"
        ]
    }
    
    if tier_name not in tier_agents:
        raise HTTPException(status_code=404, detail=f"Tier '{tier_name}' not found")
    
    return {
        "tier": tier_name,
        "available_agents": tier_agents[tier_name],
        "agent_count": len(tier_agents[tier_name])
    }
