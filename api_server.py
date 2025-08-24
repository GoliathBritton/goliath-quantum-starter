"""
NQBA Core API Server
FastAPI server providing the central orchestration layer for the NQBA Stack
Integrates with the NQBA Stack Orchestrator for quantum-enhanced business operations
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
import sys
from pathlib import Path

# Add src to path for NQBA imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nqba_stack.core.orchestrator import (
    submit_task, 
    get_orchestrator,
    TaskRequest,
    TaskResult
)
from nqba_stack.core.ltc_logger import get_ltc_logger
from nqba_stack.business_pods import get_all_business_pods

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="NQBA Core API",
    description="Neuromorphic Quantum Business Architecture Core Orchestration API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for API requests/responses
class LeadScoringRequest(BaseModel):
    leads: List[Dict[str, Any]]
    priority: Optional[int] = 5
    metadata: Optional[Dict[str, Any]] = None

class LeadScoringResponse(BaseModel):
    success: bool
    scored_leads: List[Dict[str, Any]]
    execution_time: float
    quantum_enhanced: bool
    ltc_reference: str
    next_actions: List[str]

class SalesScriptRequest(BaseModel):
    lead_profile: Dict[str, Any]
    sales_context: str
    target_outcome: str
    metadata: Optional[Dict[str, Any]] = None

class SalesScriptResponse(BaseModel):
    success: bool
    script: str
    sigmaeq_questions: List[str]
    execution_time: float
    ltc_reference: str

class EnergyOptimizationRequest(BaseModel):
    energy_data: Dict[str, Any]
    optimization_target: str  # "cost", "efficiency", "sustainability"
    constraints: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class EnergyOptimizationResponse(BaseModel):
    success: bool
    optimization_result: Dict[str, Any]
    cost_savings: float
    efficiency_gain: float
    execution_time: float
    quantum_enhanced: bool
    ltc_reference: str

class PortfolioOptimizationRequest(BaseModel):
    portfolio_data: Dict[str, Any]
    risk_tolerance: str  # "low", "medium", "high"
    target_return: float
    constraints: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

class PortfolioOptimizationResponse(BaseModel):
    success: bool
    portfolio_allocation: Dict[str, Any]
    risk_score: float
    expected_return: float
    execution_time: float
    quantum_enhanced: bool
    ltc_reference: str

class SystemHealthResponse(BaseModel):
    orchestrator_status: str
    business_pods: int
    active_pods: int
    task_routes: int
    metrics: Dict[str, Any]
    timestamp: str

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint with NQBA Stack information"""
    return {
        "message": "NQBA Core API - Neuromorphic Quantum Business Architecture",
        "version": "1.0.0",
        "status": "operational",
        "business_pods": list(get_all_business_pods().keys()),
        "timestamp": datetime.now().isoformat()
    }

# System health endpoint
@app.get("/v1/system/health", response_model=SystemHealthResponse)
async def get_system_health():
    """Get system health and status"""
    try:
        orchestrator = get_orchestrator()
        status = orchestrator.get_system_status()
        return SystemHealthResponse(**status)
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Sigma Select - Lead Scoring
@app.post("/v1/sales/score", response_model=LeadScoringResponse)
async def score_leads(request: LeadScoringRequest, background_tasks: BackgroundTasks):
    """Score leads using SigmaEQ methodology and quantum optimization"""
    try:
        # Submit task to orchestrator
        task_result = await submit_task(
            pod_id="sigma_select",
            task_type="lead_scoring",
            data={"leads": request.leads},
            priority=request.priority,
            metadata=request.metadata
        )
        
        if not task_result.success:
            raise HTTPException(status_code=400, detail=task_result.error_message)
        
        # Extract scored leads and generate next actions
        scored_leads = task_result.result_data.get("scored_leads", [])
        next_actions = _generate_next_actions(scored_leads)
        
        return LeadScoringResponse(
            success=True,
            scored_leads=scored_leads,
            execution_time=task_result.execution_time,
            quantum_enhanced=task_result.quantum_enhanced,
            ltc_reference=task_result.ltc_reference,
            next_actions=next_actions
        )
        
    except Exception as e:
        logger.error(f"Lead scoring failed: {e}")
        raise HTTPException(status_code=500, detail=f"Lead scoring failed: {str(e)}")

# Sigma Select - Sales Script Generation
@app.get("/v1/sales/script", response_model=SalesScriptResponse)
async def generate_sales_script(
    lead_profile: Dict[str, Any],
    sales_context: str,
    target_outcome: str,
    metadata: Optional[Dict[str, Any]] = None
):
    """Generate personalized sales scripts using SigmaEQ methodology"""
    try:
        # Log script generation request
        ltc_logger = get_ltc_logger()
        ltc_ref = ltc_logger.log_operation(
            operation_type="sales_script_generated",
            operation_data={
                "lead_profile": lead_profile,
                "sales_context": sales_context,
                "target_outcome": target_outcome,
                "metadata": metadata
            },
            thread_ref="SALES_SCRIPT"
        )
        
        # Generate script using SigmaEQ methodology
        script, sigmaeq_questions = _generate_sigmaeq_script(
            lead_profile, sales_context, target_outcome
        )
        
        return SalesScriptResponse(
            success=True,
            script=script,
            sigmaeq_questions=sigmaeq_questions,
            execution_time=0.0,  # Script generation is instant
            ltc_reference=ltc_ref
        )
        
    except Exception as e:
        logger.error(f"Script generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Script generation failed: {str(e)}")

# FLYFOX AI - Energy Optimization
@app.post("/v1/energy/optimize", response_model=EnergyOptimizationResponse)
async def optimize_energy(request: EnergyOptimizationRequest):
    """Optimize energy schedules using quantum optimization"""
    try:
        # Submit task to orchestrator
        task_result = await submit_task(
            pod_id="flyfox_ai",
            task_type="energy_optimization",
            data={
                "energy_data": request.energy_data,
                "optimization_target": request.optimization_target,
                "constraints": request.constraints
            },
            priority=8,  # High priority for energy optimization
            metadata=request.metadata
        )
        
        if not task_result.success:
            raise HTTPException(status_code=400, detail=task_result.error_message)
        
        # Extract optimization results
        optimization_result = task_result.result_data.get("optimization_result", {})
        cost_savings = optimization_result.get("cost_savings", 0.0)
        efficiency_gain = optimization_result.get("efficiency_gain", 0.0)
        
        return EnergyOptimizationResponse(
            success=True,
            optimization_result=optimization_result,
            cost_savings=cost_savings,
            efficiency_gain=efficiency_gain,
            execution_time=task_result.execution_time,
            quantum_enhanced=task_result.quantum_enhanced,
            ltc_reference=task_result.ltc_reference
        )
        
    except Exception as e:
        logger.error(f"Energy optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Energy optimization failed: {str(e)}")

# Goliath Trade - Portfolio Optimization
@app.post("/v1/energy/broker", response_model=PortfolioOptimizationResponse)
async def optimize_portfolio(request: PortfolioOptimizationRequest):
    """Optimize energy trading portfolios using quantum optimization"""
    try:
        # Submit task to orchestrator
        task_result = await submit_task(
            pod_id="goliath_trade",
            task_type="portfolio_optimization",
            data={
                "portfolio_data": request.portfolio_data,
                "risk_tolerance": request.risk_tolerance,
                "target_return": request.target_return,
                "constraints": request.constraints
            },
            priority=7,  # High priority for portfolio optimization
            metadata=request.metadata
        )
        
        if not task_result.success:
            raise HTTPException(status_code=400, detail=task_result.error_message)
        
        # Extract portfolio results
        portfolio_allocation = task_result.result_data.get("portfolio_allocation", {})
        risk_score = task_result.result_data.get("risk_score", 0.0)
        expected_return = task_result.result_data.get("expected_return", 0.0)
        
        return PortfolioOptimizationResponse(
            success=True,
            portfolio_allocation=portfolio_allocation,
            risk_score=risk_score,
            expected_return=expected_return,
            execution_time=task_result.execution_time,
            quantum_enhanced=task_result.quantum_enhanced,
            ltc_reference=task_result.ltc_reference
        )
        
    except Exception as e:
        logger.error(f"Portfolio optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Portfolio optimization failed: {str(e)}")

# LTC Query endpoint
@app.get("/v1/ltc/query")
async def query_ltc(
    operation_type: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    thread_ref: Optional[str] = None,
    limit: int = 100
):
    """Query the Living Technical Codex"""
    try:
        ltc_logger = get_ltc_logger()
        
        # Parse datetime strings
        start_dt = None
        end_dt = None
        if start_time:
            start_dt = datetime.fromisoformat(start_time)
        if end_time:
            end_dt = datetime.fromisoformat(end_time)
        
        operations = ltc_logger.query_operations(
            operation_type=operation_type,
            start_time=start_dt,
            end_time=end_dt,
            thread_ref=thread_ref,
            limit=limit
        )
        
        return {
            "success": True,
            "operations": [op.__dict__ for op in operations],
            "total_results": len(operations),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"LTC query failed: {e}")
        raise HTTPException(status_code=500, detail=f"LTC query failed: {str(e)}")

# Helper functions
def _generate_next_actions(scored_leads: List[Dict[str, Any]]) -> List[str]:
    """Generate next best actions based on lead scores"""
    actions = []
    for lead in scored_leads:
        score = lead.get("score", 0)
        if score >= 90:
            actions.append("🚀 Schedule FLYFOX Energy Optimizer Demo (Priority)")
        elif score >= 80:
            actions.append("📞 High-touch call with Quantum Calling Agent")
        elif score >= 70:
            actions.append("📚 Send SigmaEQ training module ($5K)")
        elif score >= 60:
            actions.append("📧 Nurture drip campaign with personalized content")
        else:
            actions.append("⏳ Add to nurture sequence for future engagement")
    return actions

def _generate_sigmaeq_script(
    lead_profile: Dict[str, Any], 
    sales_context: str, 
    target_outcome: str
) -> tuple[str, List[str]]:
    """Generate SigmaEQ-based sales script"""
    
    # Extract key information from lead profile
    company_size = lead_profile.get("company_size", "medium")
    industry = lead_profile.get("industry", "manufacturing")
    pain_points = lead_profile.get("pain_points", [])
    
    # Generate SigmaEQ questions
    sigmaeq_questions = [
        "What specific challenges are you facing with your current energy management?",
        "How do you measure success in your optimization efforts?",
        "What would be the impact of a 20% reduction in energy costs?",
        "Who are the key stakeholders in this decision-making process?",
        "What's your timeline for implementing a solution?"
    ]
    
    # Generate personalized script
    script = f"""
# SigmaEQ Sales Script for {lead_profile.get('company_name', 'Prospect')}

## Opening Hook
"Hi [Name], I noticed that {company_size} companies in the {industry} sector are facing similar challenges with energy optimization. 
Based on our work with companies like yours, I'd love to understand your specific situation better."

## SigmaEQ Discovery Questions
{chr(10).join([f"{i+1}. {q}" for i, q in enumerate(sigmaeq_questions)])}

## Value Proposition
"Based on what you share, I can show you exactly how our FLYFOX AI Energy Optimizer has helped similar companies achieve:
- 15-25% reduction in energy costs
- Improved operational efficiency
- Enhanced sustainability metrics

## Next Steps
"Would you be open to a 15-minute conversation where I can share some specific examples and see if there's a fit for working together?"

## Closing
"I'm confident we can help you achieve your {target_outcome} goals. When would be a good time to connect?"
"""
    
    return script.strip(), sigmaeq_questions

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize NQBA Stack components on startup"""
    try:
        # Get orchestrator to ensure it's initialized
        orchestrator = get_orchestrator()
        ltc_logger = get_ltc_logger()
        
        # Log API startup
        ltc_logger.log_operation(
            operation_type="api_server_started",
            operation_data={
                "version": "1.0.0",
                "endpoints": [
                "/v1/sales/score",
                "/v1/sales/script", 
                "/v1/energy/optimize",
                "/v1/energy/broker",
                "/v1/system/health",
                "/v1/ltc/query"
            ]},
            thread_ref="API_SERVER_STARTUP"
        )
        
        logger.info("NQBA Core API Server started successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize NQBA Stack: {e}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
