"""
NQBA Core API Server
FastAPI server providing the central orchestration layer for the NQBA Stack
Integrates with the NQBA Stack Orchestrator for quantum-enhanced business operations
"""

# Import GraphQL and monitoring routes (must be before app initialization)
from web3.graph_integration import graphql_router
from monitoring import app as monitoring_app
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import logging
from datetime import datetime
import sys
import os
from pathlib import Path

# Add src to path for NQBA imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nqba_stack.core.orchestrator import (
    submit_task,
    get_orchestrator,
    TaskRequest,
    TaskResult,
)
from nqba_stack.core.ltc_logger import get_ltc_logger
from nqba_stack.business_pods import get_all_business_pods

# Add import for business assessment
from nqba_stack.core.business_assessment import (
    assess_business_comprehensive,
    AuditType,
    BEMFramework,
    AssessmentResult,
)

# Add import for scheduled audits
from nqba_stack.core.scheduled_audits import (
    subscribe_company,
    get_subscription_stats,
    SubscriptionTier,
    AuditFrequency,
    scheduled_audits,
)

# Import authentication router
from auth_router import auth_router
from partners_router import partners_router
from leads_router import leads_router
from sigma_router import sigma_router
from websocket_router import router as websocket_router
from models import *

# Import entitlements system
from nqba_stack.core.entitlements import (
    get_entitlements_engine,
    require_feature,
    Feature,
    Tier,
    check_usage_limit,
    get_user_tier,
)

# Import configuration validation
from nqba_stack.core.config_validator import (
    ConfigValidator,
    ServiceStatus,
    validate_configuration,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NQBA Core API",
    description="Neuromorphic Quantum Business Architecture Core Orchestration API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount GraphQL, monitoring, and authentication endpoints
app.include_router(graphql_router)
app.include_router(auth_router, prefix="/v1")
app.include_router(partners_router, prefix="/v1")
app.include_router(leads_router, prefix="/v1")
app.include_router(sigma_router, prefix="/v1")
app.include_router(websocket_router, prefix="/v1")
app.mount("/monitoring", monitoring_app)

# --- DYNEX QUANTUM ADVANCED API ROUTES ---
from fastapi import APIRouter, UploadFile, File
from nqba_stack.quantum.adapters.dynex_adapter import DynexAdapter, AdapterConfig
from nqba_stack.core.dynex_ftp_client import DynexFTPClient
from nqba_stack.core.dynex_api_client import DynexAPIClient
import json as _json
import asyncio as _asyncio

dynex_router = APIRouter(prefix="/v1/quantum/dynex", tags=["Dynex Quantum"])


@dynex_router.post("/qubo")
async def submit_dynex_qubo(qubo: dict, mode: str = None):
    config = AdapterConfig()
    adapter = DynexAdapter(config)
    if mode:
        adapter.dynex_mode = mode
    job_id = await adapter.submit_qubo(qubo)
    return {"job_id": job_id}


@dynex_router.get("/result/{job_id}")
async def get_dynex_result(job_id: str):
    config = AdapterConfig()
    adapter = DynexAdapter(config)
    res = await adapter.result(job_id)
    return res


@dynex_router.post("/ftp/download")
async def dynex_ftp_download(remote_path: str, local_path: str):
    ftp = DynexFTPClient()
    await ftp.download(remote_path, local_path)
    return {"status": "downloaded", "remote": remote_path, "local": local_path}


@dynex_router.post("/ftp/upload")
async def dynex_ftp_upload(local_path: str, remote_path: str):
    ftp = DynexFTPClient()
    await ftp.upload(local_path, remote_path)
    return {"status": "uploaded", "local": local_path, "remote": remote_path}


@dynex_router.post("/api/post")
async def dynex_api_post(path: str, data: dict = {}):
    api = DynexAPIClient()
    res = await api.post(path, data=data)
    return res


@dynex_router.get("/api/get")
async def dynex_api_get(path: str, params: str = "{}"):
    api = DynexAPIClient()
    query = _json.loads(params)
    res = await api.get(path, params=query)
    return res


app.include_router(dynex_router)

# Import and include recipe endpoints
print("DEBUG: Importing recipe router...")
from api.recipe_endpoints import router as recipe_router
print(f"DEBUG: Recipe router imported: {recipe_router}")
print(f"DEBUG: Recipe router routes: {[route.path for route in recipe_router.routes]}")
app.include_router(recipe_router)
print("DEBUG: Recipe router included in app")
print(f"DEBUG: All app routes: {[route.path for route in app.routes]}")
print(f"DEBUG: App router count: {len(app.routes)}")

# Add a simple test route directly to the main app
@app.get("/test-main-app")
async def test_main_app():
    return {"message": "Main app is working", "status": "ok", "timestamp": "updated"}

# Add import for automated data collection
from nqba_stack.core.automated_data_collection import (
    get_audit_readiness,
    get_data_summary,
    add_custom_data_point,
    DataSource,
    DataCategory,
    automated_data_collection,
)


# Start scheduled audits scheduler and automated data collection on startup
@app.on_event("startup")
async def start_background_services():
    await scheduled_audits.start_scheduler()
    await automated_data_collection.start_collection()


# Add import for NQBA Quantum Hub


# Import GraphQL and monitoring routes (must be before app initialization)
from web3.graph_integration import graphql_router
from monitoring import app as monitoring_app

# Remove duplicate app initialization - using the one from line 53

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


from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


class SystemHealthResponse(BaseModel):
    orchestrator_status: str
    business_pods: int
    active_pods: int
    task_routes: int
    metrics: Dict[str, Any]
    timestamp: str


# Simple health endpoint for external monitoring
@app.get("/health")
def health():
    return {"status": "ok"}


# Example secure endpoint with JWT token dependency
@app.get("/secure-endpoint")
def secure_endpoint(token: str = Depends(oauth2_scheme)):
    # Add JWT validation here
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"message": "Secure data"}


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with NQBA Stack information"""
    return {
        "message": "NQBA Core API - Neuromorphic Quantum Business Architecture",
        "version": "1.0.0",
        "status": "operational",
        "business_pods": list(get_all_business_pods().keys()),
        "timestamp": datetime.now().isoformat(),
    }


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
            metadata=request.metadata,
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
            next_actions=next_actions,
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
    metadata: Optional[Dict[str, Any]] = None,
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
                "metadata": metadata,
            },
            thread_ref="SALES_SCRIPT",
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
            ltc_reference=ltc_ref,
        )

    except Exception as e:
        logger.error(f"Script generation failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Script generation failed: {str(e)}"
        )


# NQBA Energy Optimization
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
                "constraints": request.constraints,
            },
            priority=8,  # High priority for energy optimization
            metadata=request.metadata,
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
            ltc_reference=task_result.ltc_reference,
        )

    except Exception as e:
        logger.error(f"Energy optimization failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Energy optimization failed: {str(e)}"
        )


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
                "constraints": request.constraints,
            },
            priority=7,  # High priority for portfolio optimization
            metadata=request.metadata,
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
            ltc_reference=task_result.ltc_reference,
        )

    except Exception as e:
        logger.error(f"Portfolio optimization failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Portfolio optimization failed: {str(e)}"
        )


# Business Assessment endpoint
@app.post("/v1/assessment/comprehensive", response_model=AssessmentResult)
async def comprehensive_business_assessment(
    company_data: Dict[str, Any],
    audit_types: List[str] = None,
    framework: str = "baldrige",
    use_quantum: bool = True,
):
    """Perform comprehensive business assessment using IBP, BEMs, and quantum optimization"""
    try:
        # Convert string inputs to enums
        audit_type_enums = []
        if audit_types:
            for audit_type_str in audit_types:
                try:
                    audit_type_enums.append(AuditType(audit_type_str))
                except ValueError:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid audit type: {audit_type_str}"
                    )
        else:
            audit_type_enums = [
                AuditType.FINANCIAL,
                AuditType.OPERATIONAL,
                AuditType.COMPLIANCE,
            ]

        # Convert framework string to enum
        try:
            framework_enum = BEMFramework(framework)
        except ValueError:
            raise HTTPException(
                status_code=400, detail=f"Invalid framework: {framework}"
            )

        # Perform assessment
        assessment_result = await assess_business_comprehensive(
            company_data=company_data,
            audit_types=audit_type_enums,
            framework=framework_enum,
            use_quantum=use_quantum,
        )

        return assessment_result

    except Exception as e:
        logger.error(f"Business assessment failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Business assessment failed: {str(e)}"
        )


# Business Assessment frameworks endpoint
@app.get("/v1/assessment/frameworks")
async def get_assessment_frameworks():
    """Get available assessment frameworks and audit types"""
    return {
        "audit_types": [
            {
                "value": at.value,
                "name": at.name,
                "description": f"{at.name.title()} audit",
            }
            for at in AuditType
        ],
        "bem_frameworks": [
            {
                "value": bem.value,
                "name": bem.name,
                "description": f"{bem.name.title()} framework",
            }
            for bem in BEMFramework
        ],
        "ibp_components": [
            "strategic_alignment",
            "cross_functional_collaboration",
            "long_term_focus",
            "risk_resilience",
        ],
    }


# LTC Query endpoint
@app.get("/v1/ltc/query")
async def query_ltc(
    operation_type: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    thread_ref: Optional[str] = None,
    limit: int = 100,
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
            limit=limit,
        )

        return {
            "success": True,
            "operations": [op.__dict__ for op in operations],
            "total_results": len(operations),
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"LTC query failed: {e}")
        raise HTTPException(status_code=500, detail=f"LTC query failed: {str(e)}")


# Scheduled Audit Management endpoints
@app.post("/v1/subscriptions/subscribe")
async def subscribe_company_to_nqba(
    company_id: str,
    company_name: str,
    subscription_tier: str,
    custom_audit_types: List[str] = None,
    custom_framework: str = None,
):
    """Subscribe a company to NQBA scheduled audits"""
    try:
        # Convert string inputs to enums
        try:
            tier_enum = SubscriptionTier(subscription_tier)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid subscription tier: {subscription_tier}",
            )

        audit_type_enums = None
        if custom_audit_types:
            audit_type_enums = []
            for audit_type_str in custom_audit_types:
                try:
                    audit_type_enums.append(AuditType(audit_type_str))
                except ValueError:
                    raise HTTPException(
                        status_code=400, detail=f"Invalid audit type: {audit_type_str}"
                    )

        framework_enum = None
        if custom_framework:
            try:
                framework_enum = BEMFramework(custom_framework)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail=f"Invalid framework: {custom_framework}"
                )

        # Subscribe company
        result = await subscribe_company(
            company_id=company_id,
            company_name=company_name,
            subscription_tier=tier_enum,
            custom_audit_types=audit_type_enums,
            custom_framework=framework_enum,
        )

        return {
            "status": "success",
            "company_id": result,
            "message": f"Company {company_name} successfully subscribed to {subscription_tier} tier",
        }

    except Exception as e:
        logger.error(f"Company subscription failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Company subscription failed: {str(e)}"
        )


@app.get("/v1/subscriptions/stats")
async def get_nqba_subscription_statistics():
    """Get NQBA subscription statistics"""
    try:
        stats = await get_subscription_stats()
        return stats

    except Exception as e:
        logger.error(f"Failed to get subscription stats: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get subscription stats: {str(e)}"
        )


@app.get("/v1/subscriptions/tiers")
async def get_subscription_tiers():
    """Get available subscription tiers and their configurations"""
    return {
        "tiers": [
            {
                "value": "basic",
                "name": "Basic NQBA",
                "monthly_price": 5000,
                "audit_frequency": "monthly",
                "audit_types": ["financial", "operational"],
                "framework": "baldrige",
                "use_quantum": False,
                "audit_included": False,
            },
            {
                "value": "professional",
                "name": "Professional NQBA",
                "monthly_price": 15000,
                "audit_frequency": "quarterly",
                "audit_types": ["financial", "operational", "compliance"],
                "framework": "baldrige",
                "use_quantum": True,
                "audit_included": True,
            },
            {
                "value": "enterprise",
                "name": "Enterprise NQBA",
                "monthly_price": 50000,
                "audit_frequency": "monthly",
                "audit_types": [
                    "financial",
                    "operational",
                    "compliance",
                    "it_security",
                    "strategic",
                ],
                "framework": "efqm",
                "use_quantum": True,
                "audit_included": True,
            },
            {
                "value": "quantum_elite",
                "name": "Quantum Elite NQBA",
                "monthly_price": 100000,
                "audit_frequency": "continuous",
                "audit_types": [
                    "financial",
                    "operational",
                    "compliance",
                    "it_security",
                    "strategic",
                    "risk",
                    "smeta",
                    "sustainability",
                ],
                "framework": "efqm",
                "use_quantum": True,
                "audit_included": True,
            },
        ]
    }


# Automated Data Collection endpoints
@app.get("/v1/data/audit-readiness/{company_id}")
async def get_company_audit_readiness(company_id: str):
    """Get audit readiness status for a company"""
    try:
        readiness = await get_audit_readiness(company_id)
        return readiness

    except Exception as e:
        logger.error(f"Failed to get audit readiness: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get audit readiness: {str(e)}"
        )


@app.get("/v1/data/summary/{company_id}")
async def get_company_data_summary(company_id: str):
    """Get data collection summary for a company"""
    try:
        summary = await get_data_summary(company_id)
        return summary

    except Exception as e:
        logger.error(f"Failed to get data summary: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get data summary: {str(e)}"
        )


@app.post("/v1/data/custom")
async def add_custom_data_point_endpoint(
    company_id: str,
    source: str,
    category: str,
    field_name: str,
    field_value: Any,
    confidence_score: float = 1.0,
):
    """Add a custom data point"""
    try:
        # Convert string inputs to enums
        try:
            source_enum = DataSource(source)
        except ValueError:
            raise HTTPException(
                status_code=400, detail=f"Invalid data source: {source}"
            )

        try:
            category_enum = DataCategory(category)
        except ValueError:
            raise HTTPException(
                status_code=400, detail=f"Invalid data category: {category}"
            )

        # Add custom data point
        data_id = await add_custom_data_point(
            company_id=company_id,
            source=source_enum,
            category=category_enum,
            field_name=field_name,
            field_value=field_value,
            confidence_score=confidence_score,
        )

        return {
            "status": "success",
            "data_id": data_id,
            "message": f"Custom data point added successfully",
        }

    except Exception as e:
        logger.error(f"Failed to add custom data point: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to add custom data point: {str(e)}"
        )


@app.get("/v1/data/sources")
async def get_data_sources():
    """Get available data sources and categories"""
    return {
        "data_sources": [
            {"value": ds.value, "name": ds.name, "description": f"Data from {ds.value}"}
            for ds in DataSource
        ],
        "data_categories": [
            {
                "value": dc.value,
                "name": dc.name,
                "description": f"Data for {dc.value} audit",
            }
            for dc in DataCategory
        ],
    }


# Update quantum optimization endpoint to use FLYFOX AI Quantum Hub
@app.post("/v1/quantum/optimize")
async def quantum_optimization_enhanced(
    variables: List[str],
    constraints: List[Dict[str, Any]] = [],
    objective_function: str = "minimize",
    provider: str = "dynex",
    priority: int = 1,
):
    """Enhanced quantum optimization using FLYFOX AI Quantum Hub"""
    try:
        # Convert provider string to enum
        provider_enum = QuantumProvider(provider)

        # Prepare parameters
        parameters = {
            "variables": variables,
            "constraints": constraints,
            "objective_function": objective_function,
        }

        # Submit quantum request using FLYFOX AI Quantum Hub
        request_id = await submit_quantum_request(
            client_id="NQBA_INTERNAL",  # Internal NQBA client
            operation_type=QuantumOperation.OPTIMIZATION,
            provider=provider_enum,
            parameters=parameters,
            priority=priority,
        )

        return {
            "request_id": request_id,
            "status": "submitted",
            "message": "Quantum optimization request submitted to FLYFOX AI Quantum Hub",
            "provider": provider,
            "hub_endpoint": f"/quantum-hub/api/v1/quantum/status/{request_id}",
        }

    except Exception as e:
        logger.error(f"Quantum optimization failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Quantum optimization failed: {str(e)}"
        )


# Add FLYFOX AI Quantum Hub status endpoint
@app.get("/v1/quantum/status/{request_id}")
async def get_quantum_status_enhanced(request_id: str):
    """Get quantum operation status from FLYFOX AI Quantum Hub"""
    try:
        status = await get_request_status(request_id)
        return {
            **status,
            "hub_service": "FLYFOX AI Quantum Hub",
            "hub_documentation": "/quantum-hub/docs",
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get quantum status: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get quantum status: {str(e)}"
        )


# Add FLYFOX AI Quantum Hub providers endpoint
@app.get("/v1/quantum/providers")
async def get_quantum_providers_enhanced():
    """Get available quantum providers from FLYFOX AI Quantum Hub"""
    try:
        from nqba_stack.core.flyfox_quantum_hub import get_available_providers

        providers = await get_available_providers()
        return {
            "providers": providers,
            "total_providers": len(providers),
            "hub_service": "FLYFOX AI Quantum Hub",
            "hub_endpoint": "/quantum-hub/api/v1/quantum/providers",
        }

    except Exception as e:
        logger.error(f"Failed to get quantum providers: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get quantum providers: {str(e)}"
        )


# Add FLYFOX AI Quantum Hub health endpoint
@app.get("/v1/quantum/health")
async def quantum_health_enhanced():
    """Get FLYFOX AI Quantum Hub health status"""
    try:
        from nqba_stack.core.flyfox_quantum_hub import flyfox_quantum_hub

        return {
            "status": "healthy",
            "service": "FLYFOX AI Quantum Hub",
            "version": "1.0.0",
            "providers_configured": len(flyfox_quantum_hub.provider_configs),
            "active_integrations": len(
                [
                    integration
                    for integration in flyfox_quantum_hub.third_party_integrations.values()
                    if integration.is_active
                ]
            ),
            "pending_requests": len(
                [
                    req
                    for req in flyfox_quantum_hub.quantum_requests.values()
                    if req.status.value == "pending"
                ]
            ),
            "hub_endpoint": "/quantum-hub/api/v1/quantum/health",
        }

    except Exception as e:
        logger.error(f"Failed to get quantum health: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get quantum health: {str(e)}"
        )


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
    lead_profile: Dict[str, Any], sales_context: str, target_outcome: str
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
        "What's your timeline for implementing a solution?",
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


# Entitlements endpoints
@app.get("/v1/entitlements/user/{user_id}")
async def get_user_entitlements(user_id: str):
    """Get user entitlements and tier information"""
    try:
        engine = get_entitlements_engine()
        entitlements = engine.get_user_entitlements(user_id)
        tier = engine.get_user_tier(user_id)
        
        return {
            "user_id": user_id,
            "tier": tier.value,
            "entitlements": {
                "features": [f.value for f in entitlements.features],
                "limits": {
                    "api_calls_per_day": entitlements.limits.api_calls_per_day,
                    "quantum_jobs_per_day": entitlements.limits.quantum_jobs_per_day,
                    "storage_gb": entitlements.limits.storage_gb,
                    "concurrent_jobs": entitlements.limits.concurrent_jobs,
                    "max_job_duration_hours": entitlements.limits.max_job_duration_hours
                }
            },
            "usage": engine.get_usage_stats(user_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get entitlements: {str(e)}")


@app.post("/v1/entitlements/user/{user_id}/tier")
async def set_user_tier(user_id: str, tier_data: dict):
    """Set user tier"""
    try:
        tier_name = tier_data.get("tier")
        if not tier_name:
            raise HTTPException(status_code=400, detail="Tier is required")
        
        tier = Tier(tier_name)
        engine = get_entitlements_engine()
        engine.set_user_tier(user_id, tier)
        
        return {
            "user_id": user_id,
            "tier": tier.value,
            "message": f"User tier updated to {tier.value}"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid tier: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set tier: {str(e)}")


@app.get("/v1/entitlements/features")
async def get_available_features():
    """Get all available features and their descriptions"""
    return {
        "features": {
            feature.value: {
                "name": feature.value,
                "description": f"Access to {feature.value.replace('_', ' ').title()}"
            }
            for feature in Feature
        }
    }


@app.get("/v1/entitlements/tiers")
async def get_available_tiers():
    """Get all available tiers and their configurations"""
    engine = get_entitlements_engine()
    return {
        "tiers": {
            tier.value: {
                "name": tier.value,
                "features": [f.value for f in engine.tier_configs[tier].features],
                "limits": {
                    "api_calls_per_day": engine.tier_configs[tier].limits.api_calls_per_day,
                    "quantum_jobs_per_day": engine.tier_configs[tier].limits.quantum_jobs_per_day,
                    "storage_gb": engine.tier_configs[tier].limits.storage_gb,
                    "concurrent_jobs": engine.tier_configs[tier].limits.concurrent_jobs,
                    "max_job_duration_hours": engine.tier_configs[tier].limits.max_job_duration_hours
                }
            }
            for tier in Tier
        }
    }


# Health and configuration endpoints
@app.get("/v1/system/health")
async def health_check():
    """Comprehensive health check including service configuration status"""
    try:
        # Validate all service configurations
        validator = ConfigValidator()
        validations = validator.validate_all_services()
        
        # Check orchestrator health
        orchestrator_healthy = True
        try:
            orchestrator = get_orchestrator()
        except Exception as e:
            orchestrator_healthy = False
            logger.error(f"Orchestrator health check failed: {e}")
        
        # Count configured services
        configured_services = sum(1 for v in validations.values() 
                                if v.status == ServiceStatus.CONFIGURED)
        total_services = len(validations)
        
        # Determine overall health
        overall_healthy = orchestrator_healthy and configured_services >= (total_services * 0.5)
        
        return {
            "status": "healthy" if overall_healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "services": {
                "orchestrator": "healthy" if orchestrator_healthy else "unhealthy",
                "configuration": {
                    "configured_services": configured_services,
                    "total_services": total_services,
                    "configuration_score": f"{(configured_services/total_services)*100:.1f}%",
                    "services": {
                        service: {
                            "status": validation.status.value,
                            "message": validation.message,
                            "missing_vars": validation.missing_vars
                        }
                        for service, validation in validations.items()
                    }
                }
            },
            "endpoints": [
                "/v1/sales/score",
                "/v1/sales/script", 
                "/v1/energy/optimize",
                "/v1/energy/broker",
                "/v1/system/health",
                "/v1/system/config",
                "/v1/ltc/query",
                "/v1/entitlements/user/{user_id}",
                "/v1/entitlements/features",
                "/v1/entitlements/tiers"
            ]
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }


@app.get("/v1/system/config")
async def get_configuration_status():
    """Get detailed configuration status and setup guidance"""
    try:
        validator = ConfigValidator()
        validations = validator.validate_all_services()
        
        return {
            "configuration_status": {
                service: {
                    "status": validation.status.value,
                    "message": validation.message,
                    "required_vars": validation.required_vars,
                    "missing_vars": validation.missing_vars,
                    "suggestions": validation.suggestions
                }
                for service, validation in validations.items()
            },
            "setup_report": validator.generate_setup_report(),
            "next_steps": [
                "Copy .env.example to .env",
                "Update .env with your actual configuration values",
                "Restart the application",
                "Check /v1/system/health for updated status"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get configuration status: {str(e)}")


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize NQBA Stack components on startup"""
    try:
        # Validate configuration on startup
        validator = ConfigValidator()
        validations = validator.validate_all_services()
        
        # Log configuration status
        configured_count = sum(1 for v in validations.values() 
                             if v.status == ServiceStatus.CONFIGURED)
        total_count = len(validations)
        
        logger.info(f"Configuration Status: {configured_count}/{total_count} services configured")
        
        # Log missing configurations as warnings
        for service, validation in validations.items():
            if validation.status != ServiceStatus.CONFIGURED:
                logger.warning(f"{service.upper()}: {validation.message}")
                if validation.missing_vars:
                    logger.warning(f"Missing variables: {', '.join(validation.missing_vars)}")
        
        # Get orchestrator to ensure it's initialized
        orchestrator = get_orchestrator()
        ltc_logger = get_ltc_logger()

        # Log API startup
        ltc_logger.log_operation(
            operation_type="api_server_started",
            operation_data={
                "version": "1.0.0",
                "configured_services": configured_count,
                "total_services": total_count,
                "endpoints": [
                    "/v1/sales/score",
                    "/v1/sales/script",
                    "/v1/energy/optimize",
                    "/v1/energy/broker",
                    "/v1/system/health",
                    "/v1/system/config",
                    "/v1/ltc/query",
                    "/v1/entitlements/user/{user_id}",
                    "/v1/entitlements/features",
                    "/v1/entitlements/tiers"
                ],
            },
            thread_ref="API_SERVER_STARTUP",
        )

        logger.info("NQBA Core API Server started successfully")
        
        # Print configuration report if in development
        if os.getenv("ENVIRONMENT", "development") == "development":
            print(validator.generate_setup_report())

    except Exception as e:
        logger.error(f"Failed to initialize NQBA Stack: {e}")
        raise


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
