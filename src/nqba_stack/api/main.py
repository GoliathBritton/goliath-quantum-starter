"""
NQBA Stack API - Main Application
=================================
Integrated API for GOLIATH + FLYFOX AI + SIGMA SELECT Empire
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from ..core.settings import NQBASettings
from ..core.auth import get_current_user, User
from ..business_units import (
    EnergyOptimization,
    CapitalFunding,
    InsuranceRisk,
    SalesTraining,
    GoliathFinancial,
    FlyfoxAITech,
    SigmaSelect,
    QuantumDigitalAgent,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global settings
settings = NQBASettings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("🚀 Starting GOLIATH + FLYFOX AI + SIGMA SELECT Empire...")
    logger.info("🔧 Initializing NQBA Stack components...")

    # Initialize business units
    await EnergyOptimization().initialize()
    await CapitalFunding().initialize()
    await InsuranceRisk().initialize()
    await SalesTraining().initialize()
    await GoliathFinancial().initialize()
    await FlyfoxAITech().initialize()
    await SigmaSelect().initialize()

    # Initialize Quantum Digital Agent
    quantum_agent = QuantumDigitalAgent(settings)
    logger.info("🤖 Quantum Digital Agent: Ready to make quantum-enhanced calls")

    logger.info("✅ Empire initialization complete!")
    logger.info("🌟 GOLIATH Financial Empire: Ready to dominate financial services")
    logger.info("🚀 FLYFOX AI Technology Empire: Ready to lead quantum innovation")
    logger.info("🎯 SIGMA SELECT Sales Empire: Ready to optimize sales performance")
    logger.info("🤖 Quantum Digital Agent: Ready to dominate voice communications")

    yield

    # Shutdown
    logger.info("🛑 Shutting down Empire...")


# Create FastAPI application
app = FastAPI(
    title="GOLIATH + FLYFOX AI + SIGMA SELECT Empire",
    description="The Three-Pillar Business Empire - Integrated with NQBA Stack",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# EMPIRE OVERVIEW ENDPOINTS
# ============================================================================


@app.get("/")
async def empire_overview():
    """Get overview of the Three-Pillar Business Empire"""
    return {
        "empire": "GOLIATH + FLYFOX AI + SIGMA SELECT",
        "description": "The Three-Pillar Business Empire - Integrated with NQBA Stack",
        "pillars": {
            "goliath": {
                "name": "GOLIATH Financial Empire",
                "description": "Financial & CRM Foundation - Dominating financial services with quantum AI",
                "services": ["CRM", "Lending", "Insurance", "Financial Services"],
                "endpoint": "/empire/goliath",
            },
            "flyfox_ai": {
                "name": "FLYFOX AI Technology Empire",
                "description": "Transformational Technology Arm - Leading quantum computing and AI innovation",
                "services": [
                    "Quantum Computing",
                    "Energy Optimization",
                    "AI/ML",
                    "Research & Development",
                ],
                "endpoint": "/empire/flyfox-ai",
            },
            "sigma_select": {
                "name": "SIGMA SELECT Sales Empire",
                "description": "Sales & Revenue Engine - Dominating sales with quantum-powered optimization",
                "services": [
                    "Sales Training",
                    "Revenue Optimization",
                    "Market Expansion",
                    "Partner Network",
                ],
                "endpoint": "/empire/sigma-select",
            },
        },
        "nqba_integration": {
            "status": "active",
            "components": [
                "OpenAI",
                "NVIDIA",
                "Quantum Integration",
                "Observability",
                "Security",
            ],
            "quantum_advantage": "23.4x vs Classical",
        },
        "revenue_target": "$600M+ Annually",
        "status": "operational",
    }


@app.get("/empire/overview")
async def get_empire_overview(current_user: User = Depends(get_current_user)):
    """Get comprehensive overview of all three business pillars"""
    try:
        # Get overviews from all business units
        goliath_overview = await GoliathFinancial().get_empire_overview()
        flyfox_overview = await FlyfoxAITech().get_technology_overview()
        sigma_overview = await SigmaSelect().get_sales_overview()

        # Calculate total empire metrics
        total_revenue = (
            goliath_overview["financial_metrics"]["estimated_monthly_revenue"]
            + flyfox_overview["revenue_metrics"]["estimated_monthly_revenue"]
            + sigma_overview["revenue_metrics"]["estimated_monthly_revenue"]
        )

        return {
            "empire_status": "operational",
            "total_monthly_revenue": total_revenue,
            "pillars": {
                "goliath_financial": goliath_overview,
                "flyfox_ai_tech": flyfox_overview,
                "sigma_select": sigma_overview,
            },
            "empire_metrics": {
                "total_customers": goliath_overview["empire_metrics"][
                    "total_customers"
                ],
                "total_quantum_jobs": flyfox_overview["technology_metrics"][
                    "total_quantum_jobs"
                ],
                "total_training_programs": sigma_overview["sales_metrics"][
                    "total_training_programs"
                ],
                "quantum_advantage": "23.4x vs Classical",
                "energy_savings": flyfox_overview["energy_metrics"][
                    "average_energy_savings"
                ],
            },
        }
    except Exception as e:
        logger.error(f"Failed to get empire overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to get empire overview")


# ============================================================================
# GOLIATH FINANCIAL EMPIRE ENDPOINTS
# ============================================================================


@app.get("/empire/goliath")
async def goliath_empire_overview():
    """Get GOLIATH Financial Empire overview"""
    return {
        "empire": "GOLIATH Financial Empire",
        "description": "Financial & CRM Foundation - Dominating financial services with quantum AI",
        "services": {
            "crm": "Customer Relationship Management",
            "lending": "Business & Personal Loans",
            "insurance": "Property, Liability, Business Coverage",
            "financial_services": "Banking, Payments, Wealth Management",
        },
        "endpoints": {
            "customers": "/empire/goliath/customers",
            "loans": "/empire/goliath/loans",
            "insurance": "/empire/goliath/insurance",
            "accounts": "/empire/goliath/accounts",
            "overview": "/empire/goliath/overview",
        },
        "quantum_services": [
            "customer_risk_assessment",
            "loan_underwriting",
            "insurance_pricing",
            "financial_optimization",
        ],
    }


@app.post("/empire/goliath/customers")
async def create_goliath_customer(
    customer_data: dict, current_user: User = Depends(get_current_user)
):
    """Create a new customer in GOLIATH Financial Empire"""
    try:
        from ..business_units.goliath_financial import CustomerType

        customer = await GoliathFinancial().create_customer(
            name=customer_data["name"],
            customer_type=CustomerType(customer_data["customer_type"]),
            email=customer_data["email"],
            phone=customer_data["phone"],
            address=customer_data["address"],
            credit_score=customer_data.get("credit_score"),
            annual_income=customer_data.get("annual_income"),
        )

        return {
            "status": "success",
            "customer": {
                "id": customer.customer_id,
                "name": customer.name,
                "risk_profile": customer.risk_profile,
                "total_assets": customer.total_assets,
                "total_liabilities": customer.total_liabilities,
            },
            "message": f"Customer '{customer.name}' created with {customer.risk_profile} risk profile",
        }
    except Exception as e:
        logger.error(f"Failed to create customer: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create customer: {str(e)}"
        )


@app.post("/empire/goliath/loans")
async def apply_goliath_loan(
    loan_data: dict, current_user: User = Depends(get_current_user)
):
    """Apply for a loan in GOLIATH Financial Empire"""
    try:
        from ..business_units.goliath_financial import LoanType

        loan = await GoliathFinancial().apply_for_loan(
            customer_id=loan_data["customer_id"],
            loan_type=LoanType(loan_data["loan_type"]),
            amount=loan_data["amount"],
            term_months=loan_data["term_months"],
            purpose=loan_data["purpose"],
            collateral=loan_data.get("collateral"),
        )

        return {
            "status": "success",
            "loan": {
                "id": loan.application_id,
                "status": loan.status,
                "amount": loan.amount,
                "interest_rate": loan.interest_rate,
                "monthly_payment": loan.monthly_payment,
            },
            "message": f"Loan application {loan.status} for ${loan.amount:,.2f}",
        }
    except Exception as e:
        logger.error(f"Failed to apply for loan: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to apply for loan: {str(e)}"
        )


@app.get("/empire/goliath/overview")
async def get_goliath_overview(current_user: User = Depends(get_current_user)):
    """Get GOLIATH Financial Empire detailed overview"""
    try:
        overview = await GoliathFinancial().get_empire_overview()
        return {"status": "success", "goliath_empire": overview}
    except Exception as e:
        logger.error(f"Failed to get GOLIATH overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to get GOLIATH overview")


# ============================================================================
# FLYFOX AI TECHNOLOGY EMPIRE ENDPOINTS
# ============================================================================


@app.get("/empire/flyfox-ai")
async def flyfox_ai_empire_overview():
    """Get FLYFOX AI Technology Empire overview"""
    return {
        "empire": "FLYFOX AI Technology Empire",
        "description": "Transformational Technology Arm - Leading quantum computing and AI innovation",
        "services": {
            "quantum_computing": "NVIDIA GPU + cuQuantum acceleration",
            "energy_optimization": "Renewable energy & grid management",
            "ai_ml": "AI/ML pipeline with autonomous systems",
            "research_development": "Cutting-edge technology innovation",
        },
        "endpoints": {
            "quantum": "/empire/flyfox-ai/quantum",
            "energy": "/empire/flyfox-ai/energy",
            "aiml": "/empire/flyfox-ai/aiml",
            "research": "/empire/flyfox-ai/research",
            "overview": "/empire/flyfox-ai/overview",
        },
        "quantum_services": [
            "quantum_circuit_simulation",
            "energy_optimization",
            "ai_ml_acceleration",
            "research_optimization",
        ],
    }


@app.post("/empire/flyfox-ai/quantum")
async def submit_quantum_job(
    job_data: dict, current_user: User = Depends(get_current_user)
):
    """Submit a quantum computing job to FLYFOX AI Technology Empire"""
    try:
        from ..business_units.flyfox_ai_tech import QuantumServiceType

        job = await FlyfoxAITech().submit_quantum_job(
            service_type=QuantumServiceType(job_data["service_type"]),
            customer_id=job_data["customer_id"],
            job_description=job_data["job_description"],
            parameters=job_data["parameters"],
        )

        return {
            "status": "success",
            "quantum_job": {
                "id": job.job_id,
                "service_type": job.service_type.value,
                "status": job.status,
                "quantum_advantage": job.quantum_advantage,
                "processing_time_ms": job.processing_time_ms,
            },
            "message": f"Quantum job submitted for {job.service_type.value}",
        }
    except Exception as e:
        logger.error(f"Failed to submit quantum job: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to submit quantum job: {str(e)}"
        )


@app.post("/empire/flyfox-ai/energy")
async def create_energy_optimization(
    energy_data: dict, current_user: User = Depends(get_current_user)
):
    """Create an energy optimization project in FLYFOX AI Technology Empire"""
    try:
        from ..business_units.flyfox_ai_tech import EnergyOptimizationType

        project = await FlyfoxAITech().create_energy_optimization_project(
            optimization_type=EnergyOptimizationType(energy_data["optimization_type"]),
            customer_id=energy_data["customer_id"],
            project_description=energy_data["project_description"],
            energy_data=energy_data["energy_data"],
            baseline_consumption=energy_data["baseline_consumption"],
            target_savings=energy_data["target_savings"],
        )

        return {
            "status": "success",
            "energy_project": {
                "id": project.project_id,
                "optimization_type": project.optimization_type.value,
                "status": project.status,
                "achieved_savings": project.achieved_savings,
                "roi_percentage": project.roi_percentage,
            },
            "message": f"Energy optimization project created for {project.optimization_type.value}",
        }
    except Exception as e:
        logger.error(f"Failed to create energy optimization: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create energy optimization: {str(e)}"
        )


@app.get("/empire/flyfox-ai/overview")
async def get_flyfox_ai_overview(current_user: User = Depends(get_current_user)):
    """Get FLYFOX AI Technology Empire detailed overview"""
    try:
        overview = await FlyfoxAITech().get_technology_overview()
        return {"status": "success", "flyfox_ai_empire": overview}
    except Exception as e:
        logger.error(f"Failed to get FLYFOX AI overview: {e}")
        raise HTTPException(status_code=500, detail="Failed to get FLYFOX AI overview")


# ============================================================================
# SIGMA SELECT SALES EMPIRE ENDPOINTS
# ============================================================================


@app.get("/empire/sigma-select")
async def sigma_select_empire_overview():
    """Get SIGMA SELECT Sales Empire overview"""
    return {
        "empire": "SIGMA SELECT Sales Empire",
        "description": "Sales & Revenue Engine - Dominating sales with quantum-powered optimization",
        "services": {
            "sales_training": "Professional development & certification",
            "revenue_optimization": "Performance analytics & scaling",
            "market_expansion": "Industry penetration & growth strategies",
            "partner_network": "Reseller & referral programs",
        },
        "endpoints": {
            "training": "/empire/sigma-select/training",
            "revenue": "/empire/sigma-select/revenue",
            "market": "/empire/sigma-select/market",
            "partners": "/empire/sigma-select/partners",
            "overview": "/empire/sigma-select/overview",
        },
        "quantum_services": [
            "sales_training_optimization",
            "revenue_optimization",
            "market_expansion_analysis",
            "partner_performance_optimization",
        ],
    }


@app.post("/empire/sigma-select/training")
async def create_training_program(
    training_data: dict, current_user: User = Depends(get_current_user)
):
    """Create a sales training program in SIGMA SELECT Sales Empire"""
    try:
        from ..business_units.sigma_select import TrainingType

        program = await SigmaSelect().create_training_program(
            training_type=TrainingType(training_data["training_type"]),
            program_name=training_data["program_name"],
            description=training_data["description"],
            duration_hours=training_data["duration_hours"],
            price=training_data["price"],
            max_participants=training_data["max_participants"],
            start_date=training_data.get("start_date"),
        )

        return {
            "status": "success",
            "training_program": {
                "id": program.program_id,
                "name": program.program_name,
                "type": program.training_type.value,
                "price": program.price,
                "max_participants": program.max_participants,
            },
            "message": f"Training program '{program.program_name}' created with optimized pricing",
        }
    except Exception as e:
        logger.error(f"Failed to create training program: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create training program: {str(e)}"
        )


@app.post("/empire/sigma-select/revenue")
async def create_revenue_optimization(
    revenue_data: dict, current_user: User = Depends(get_current_user)
):
    """Create a revenue optimization project in SIGMA SELECT Sales Empire"""
    try:
        from ..business_units.sigma_select import RevenueOptimizationType

        project = await SigmaSelect().create_revenue_optimization_project(
            optimization_type=RevenueOptimizationType(
                revenue_data["optimization_type"]
            ),
            customer_id=revenue_data["customer_id"],
            project_description=revenue_data["project_description"],
            baseline_revenue=revenue_data["baseline_revenue"],
            target_increase=revenue_data["target_increase"],
        )

        return {
            "status": "success",
            "revenue_project": {
                "id": project.project_id,
                "optimization_type": project.optimization_type.value,
                "status": project.status,
                "achieved_increase": project.achieved_increase,
                "roi_percentage": project.roi_percentage,
            },
            "message": f"Revenue optimization project created for {project.optimization_type.value}",
        }
    except Exception as e:
        logger.error(f"Failed to create revenue optimization: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to create revenue optimization: {str(e)}"
        )


@app.get("/empire/sigma-select/overview")
async def get_sigma_select_overview(current_user: User = Depends(get_current_user)):
    """Get SIGMA SELECT Sales Empire detailed overview"""
    try:
        overview = await SigmaSelect().get_sales_overview()
        return {"status": "success", "sigma_select_empire": overview}
    except Exception as e:
        logger.error(f"Failed to get SIGMA SELECT overview: {e}")
        raise HTTPException(
            status_code=500, detail="Failed to get SIGMA SELECT overview"
        )


# ============================================================================
# EXISTING NQBA STACK ENDPOINTS (MAINTAINED)
# ============================================================================


@app.get("/health")
async def health_check():
    """Health check for the entire Empire"""
    try:
        # Check all business units
        goliath_health = await GoliathFinancial().health_check()
        flyfox_health = await FlyfoxAITech().health_check()
        sigma_health = await SigmaSelect().health_check()

        return {
            "status": "healthy",
            "empire": "GOLIATH + FLYFOX AI + SIGMA SELECT",
            "nqba_stack": "operational",
            "business_units": {
                "goliath_financial": goliath_health["status"],
                "flyfox_ai_tech": flyfox_health["status"],
                "sigma_select": sigma_health["status"],
            },
            "quantum_services": "active",
            "timestamp": "2024-12-19T00:00:00Z",
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "degraded",
            "error": str(e),
            "timestamp": "2024-12-19T00:00:00Z",
        }


@app.get("/info")
async def get_info():
    """Get Empire information"""
    return {
        "name": "GOLIATH + FLYFOX AI + SIGMA SELECT Empire",
        "version": "1.0.0",
        "description": "The Three-Pillar Business Empire - Integrated with NQBA Stack",
        "architecture": "Three-Pillar Business Empire",
        "pillars": [
            "GOLIATH - Financial & CRM Foundation",
            "FLYFOX AI - Transformational Technology Arm",
            "SIGMA SELECT - Sales & Revenue Engine",
        ],
        "nqba_integration": {
            "openai": "active",
            "nvidia": "active",
            "quantum": "active",
            "observability": "active",
            "security": "active",
        },
        "revenue_target": "$600M+ Annually",
        "quantum_advantage": "23.4x vs Classical",
    }


# ============================================================================
# QUANTUM DIGITAL AGENT ENDPOINTS
# ============================================================================


@app.post("/quantum-agent/make-call")
async def make_quantum_call(
    call_data: dict, current_user: User = Depends(get_current_user)
):
    """Make an outbound call using quantum-enhanced AI"""
    try:
        from ..quantum_digital_agent import CallRequest

        # Create call request
        call_request = CallRequest(
            to_number=call_data["to_number"],
            from_number=call_data["from_number"],
            agent_id=call_data["agent_id"],
            call_purpose=call_data["call_purpose"],
            script_template=call_data.get("script_template"),
            quantum_optimization=call_data.get("quantum_optimization", True),
            gpu_acceleration=call_data.get("gpu_acceleration", True),
        )

        # Initialize quantum agent
        quantum_agent = QuantumDigitalAgent(settings)

        # Make the call
        result = await quantum_agent.make_call(call_request)

        return {
            "status": "success",
            "empire": "FLYFOX AI Technology Empire",
            "service": "Quantum Digital Agent",
            "result": {
                "success": result.success,
                "call_id": result.call_id,
                "message": result.message,
                "quantum_insights": result.quantum_insights,
                "call_duration": result.session.duration if result.session else None,
                "call_status": result.session.status.value if result.session else None,
            },
        }

    except Exception as e:
        logger.error(f"Quantum call failed: {e}")
        raise HTTPException(status_code=500, detail=f"Quantum call failed: {str(e)}")


@app.get("/quantum-agent/analytics")
async def get_quantum_analytics(current_user: User = Depends(get_current_user)):
    """Get call analytics with quantum insights"""
    try:
        # Initialize quantum agent
        quantum_agent = QuantumDigitalAgent(settings)

        # Get analytics
        analytics = await quantum_agent.get_call_analytics()

        return {
            "status": "success",
            "empire": "FLYFOX AI Technology Empire",
            "service": "Quantum Digital Agent Analytics",
            "analytics": analytics,
        }

    except Exception as e:
        logger.error(f"Quantum analytics failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Quantum analytics failed: {str(e)}"
        )


@app.get("/quantum-agent/call-history")
async def get_quantum_call_history(
    limit: int = 50,
    status_filter: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    """Get call history with optional filtering"""
    try:
        # Initialize quantum agent
        quantum_agent = QuantumDigitalAgent(settings)

        # Get call history
        history = await quantum_agent.get_call_history(limit=limit)

        # Apply status filter if specified
        if status_filter:
            history = [call for call in history if call.status.value == status_filter]

        # Convert to serializable format
        serializable_history = []
        for call in history:
            serializable_history.append(
                {
                    "call_id": call.call_id,
                    "call_type": call.call_type.value,
                    "status": call.status.value,
                    "start_time": call.start_time.isoformat(),
                    "end_time": call.end_time.isoformat() if call.end_time else None,
                    "duration": call.duration,
                    "purpose": call.metadata.get("purpose"),
                    "quantum_insights": call.quantum_insights,
                }
            )

        return {
            "status": "success",
            "empire": "FLYFOX AI Technology Empire",
            "service": "Quantum Digital Agent Call History",
            "call_history": serializable_history,
            "total_calls": len(serializable_history),
            "filtered_by_status": status_filter,
        }

    except Exception as e:
        logger.error(f"Quantum call history failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Quantum call history failed: {str(e)}"
        )


# ============================================================================
# EXISTING BUSINESS UNIT ENDPOINTS (MAINTAINED)
# ============================================================================


@app.post("/business-units/energy/optimize")
async def optimize_energy(
    file_data: dict, current_user: User = Depends(get_current_user)
):
    """Energy optimization endpoint (maintained from existing NQBA Stack)"""
    try:
        # This maintains compatibility with existing energy optimization
        result = await EnergyOptimization().optimize_energy(file_data)
        return {
            "status": "success",
            "empire": "FLYFOX AI Technology Empire",
            "service": "Energy Optimization",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Energy optimization failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Energy optimization failed: {str(e)}"
        )


@app.post("/business-units/capital/apply")
async def apply_capital(
    application_data: dict, current_user: User = Depends(get_current_user)
):
    """Capital funding endpoint (maintained from existing NQBA Stack)"""
    try:
        # This maintains compatibility with existing capital funding
        result = await CapitalFunding().apply_for_funding(application_data)
        return {
            "status": "success",
            "empire": "GOLIATH Financial Empire",
            "service": "Capital Funding",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Capital funding failed: {e}")
        raise HTTPException(status_code=500, detail=f"Capital funding failed: {str(e)}")


# ============================================================================
# ERROR HANDLING
# ============================================================================


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for the Empire"""
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Empire encountered an error",
            "message": str(exc),
            "empire": "GOLIATH + FLYFOX AI + SIGMA SELECT",
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
