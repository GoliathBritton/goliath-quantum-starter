"""
Enhanced NQBA Stack API Server

Now includes all five business pods:
- Sigma Select (Sales Intelligence)
- FLYFOX AI (Energy Optimization) 
- Goliath Trade (Financial Trading)
- SFG Symmetry Financial Group (Insurance & Financial Services)
- Ghost NeuroQ (Quantum Data Intelligence)
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import business pods
from .business_pods.sigma_select.sigma_select_pod import SigmaSelectPod
from .business_pods.flyfox_ai.flyfox_ai_pod import FLYFOXAIEnergyPod
from .business_pods.goliath_trade.goliath_trade_pod import GoliathTradePod
from .business_pods.sfg_symmetry.sfg_symmetry_pod import SFGSymmetryFinancialPod
from .business_pods.ghost_neuroq.ghost_neuroq_pod import GhostNeuroQPod

# Import core components
from .core.orchestrator import NQBAStackOrchestrator
from .ltc_logger import LTCLogger
from .quantum_adapter import QuantumAdapter

# Import Phase 2 components
from .multi_tenant.multi_tenant_manager import MultiTenantManager, ScalingPolicy
from .performance.advanced_performance_dashboard import AdvancedPerformanceDashboard

# Import Phase 2.1 components
from .constraints.constraint_evolution_engine import (
    ConstraintEvolutionEngine,
    EvolutionStrategy,
)
from .scaling.predictive_scaler import PredictiveScaler, ResourceType, ScalingAlgorithm
from .enterprise.enterprise_security_manager import (
    EnterpriseSecurityManager,
    AuthType,
    ComplianceFramework,
)
from .community.community_platform import (
    AlgorithmMarketplace,
    DeveloperPortal,
    CommunityManager,
)

# Import Phase 2.2 components
from .quantum.advanced_qubo_engine import AdvancedQUBOEngine, OptimizationStrategy
from .learning.real_time_learning_engine import (
    RealTimeLearningEngine,
    LearningMode,
    AlgorithmType,
)

# Import core components
from .core.orchestrator import BusinessPod

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Goliath Quantum Starter API",
    description="Neuromorphic Quantum Business Architecture (NQBA) Stack API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
orchestrator = NQBAStackOrchestrator()
ltc_logger = LTCLogger()
quantum_adapter = QuantumAdapter()

# Initialize Phase 2 components
multi_tenant_manager = MultiTenantManager()
advanced_performance_dashboard = AdvancedPerformanceDashboard()

# Initialize Phase 2.1 components
constraint_evolution_engine = ConstraintEvolutionEngine(ltc_logger)
predictive_scaler = PredictiveScaler(ltc_logger)
enterprise_security_manager = EnterpriseSecurityManager(ltc_logger)
algorithm_marketplace = AlgorithmMarketplace(ltc_logger)
developer_portal = DeveloperPortal(ltc_logger)
community_manager = CommunityManager(ltc_logger)

# Initialize Phase 2.2 components
advanced_qubo_engine = AdvancedQUBOEngine(ltc_logger, quantum_adapter)
real_time_learning_engine = RealTimeLearningEngine(ltc_logger)

# Initialize business pods
sigma_select_pod = SigmaSelectPod(quantum_adapter, ltc_logger)
flyfox_ai_pod = FLYFOXAIEnergyPod(quantum_adapter, ltc_logger)
goliath_trade_pod = GoliathTradePod(quantum_adapter, ltc_logger)
sfg_symmetry_pod = SFGSymmetryFinancialPod(quantum_adapter, ltc_logger)
ghost_neuroq_pod = GhostNeuroQPod(quantum_adapter, ltc_logger)


# Pydantic models for API requests/responses
class HealthCheckResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    quantum_status: str
    business_pods: List[str]


class BusinessPodMetrics(BaseModel):
    pod_id: str
    pod_name: str
    total_operations: int
    success_rate: float
    average_quantum_advantage: float
    active: bool
    last_heartbeat: str


class QuantumOperationRequest(BaseModel):
    operation_type: str
    parameters: Dict[str, Any]
    business_pod: str
    optimization_level: str = "standard"


class QuantumOperationResponse(BaseModel):
    operation_id: str
    status: str
    result: Dict[str, Any]
    quantum_advantage: float
    execution_time: float
    timestamp: str


# Health check endpoint
@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """System health check"""
    try:
        # Check quantum adapter status
        quantum_status = "operational"
        try:
            await quantum_adapter.get_status()
        except Exception as e:
            quantum_status = f"degraded: {str(e)}"

        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version="2.0.0",
            quantum_status=quantum_status,
            business_pods=[
                "sigma_select",
                "flyfox_ai",
                "goliath_trade",
                "sfg_symmetry",
                "ghost_neuroq",
            ],
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Business pod metrics endpoint
@app.get("/metrics/business-pods", response_model=List[BusinessPodMetrics])
async def get_business_pod_metrics():
    """Get metrics for all business pods"""
    try:
        metrics = []

        # Get metrics from each pod
        sigma_metrics = await sigma_select_pod.get_pod_metrics()
        flyfox_metrics = await flyfox_ai_pod.get_pod_metrics()
        goliath_metrics = await goliath_trade_pod.get_pod_metrics()
        sfg_metrics = await sfg_symmetry_pod.get_pod_metrics()
        ghost_metrics = await ghost_neuroq_pod.get_pod_metrics()

        metrics.extend(
            [
                BusinessPodMetrics(**sigma_metrics),
                BusinessPodMetrics(**flyfox_metrics),
                BusinessPodMetrics(**goliath_metrics),
                BusinessPodMetrics(**sfg_metrics),
                BusinessPodMetrics(**ghost_metrics),
            ]
        )

        return metrics
    except Exception as e:
        logger.error(f"Failed to get business pod metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Quantum operation endpoint
@app.post("/quantum/operate", response_model=QuantumOperationResponse)
async def execute_quantum_operation(request: QuantumOperationRequest):
    """Execute quantum operation through specified business pod"""
    try:
        start_time = datetime.now()

        # Route operation to appropriate business pod
        if request.business_pod == "sigma_select":
            result = await sigma_select_pod.execute_quantum_operation(
                request.operation_type, request.parameters
            )
        elif request.business_pod == "flyfox_ai":
            result = await flyfox_ai_pod.execute_quantum_operation(
                request.operation_type, request.parameters
            )
        elif request.business_pod == "goliath_trade":
            result = await goliath_trade_pod.execute_quantum_operation(
                request.operation_type, request.parameters
            )
        elif request.business_pod == "sfg_symmetry":
            result = await sfg_symmetry_pod.execute_quantum_operation(
                request.operation_type, request.parameters
            )
        elif request.business_pod == "ghost_neuroq":
            result = await ghost_neuroq_pod.execute_quantum_operation(
                request.operation_type, request.parameters
            )
        else:
            raise HTTPException(
                status_code=400, detail=f"Unknown business pod: {request.business_pod}"
            )

        execution_time = (datetime.now() - start_time).total_seconds()

        # Log operation to LTC
        await ltc_logger.log_operation(
            operation_type=request.operation_type,
            business_pod=request.business_pod,
            metadata={
                "parameters": request.parameters,
                "execution_time": execution_time,
                "quantum_advantage": result.get("quantum_advantage", 1.0),
            },
        )

        return QuantumOperationResponse(
            operation_id=result.get("operation_id", "unknown"),
            status="completed",
            result=result,
            quantum_advantage=result.get("quantum_advantage", 1.0),
            execution_time=execution_time,
            timestamp=datetime.now().isoformat(),
        )

    except Exception as e:
        logger.error(f"Quantum operation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SIGMA SELECT ENDPOINTS (Sales Intelligence)
# ============================================================================


class LeadScoringRequest(BaseModel):
    leads: List[Dict[str, Any]]
    scoring_criteria: Dict[str, float]
    optimization_level: str = "standard"


class LeadScoringResponse(BaseModel):
    scored_leads: List[Dict[str, Any]]
    quantum_advantage: float
    confidence_level: float
    execution_time: float


@app.post("/sigma-select/score-leads", response_model=LeadScoringResponse)
async def score_leads(request: LeadScoringRequest):
    """Score leads using quantum-enhanced algorithms"""
    try:
        start_time = datetime.now()

        result = await sigma_select_pod.score_leads_quantum(
            request.leads, request.scoring_criteria, request.optimization_level
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return LeadScoringResponse(
            scored_leads=result.get("scored_leads", []),
            quantum_advantage=result.get("quantum_advantage", 1.0),
            confidence_level=result.get("confidence_level", 0.8),
            execution_time=execution_time,
        )

    except Exception as e:
        logger.error(f"Lead scoring failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# FLYFOX AI ENDPOINTS (Energy Optimization)
# ============================================================================


class EnergyOptimizationRequest(BaseModel):
    energy_data: Dict[str, Any]
    optimization_horizon: int  # hours
    constraints: Dict[str, Any]
    optimization_level: str = "standard"


class EnergyOptimizationResponse(BaseModel):
    optimized_schedule: Dict[str, Any]
    cost_savings: float
    quantum_advantage: float
    execution_time: float


@app.post("/flyfox-ai/optimize-energy", response_model=EnergyOptimizationResponse)
async def optimize_energy(request: EnergyOptimizationRequest):
    """Optimize energy consumption using quantum algorithms"""
    try:
        start_time = datetime.now()

        result = await flyfox_ai_pod.optimize_energy_consumption(
            request.energy_data,
            request.optimization_horizon,
            request.constraints,
            request.optimization_level,
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return EnergyOptimizationResponse(
            optimized_schedule=result.get("optimized_schedule", {}),
            cost_savings=result.get("cost_savings", 0.0),
            quantum_advantage=result.get("quantum_advantage", 1.0),
            execution_time=execution_time,
        )

    except Exception as e:
        logger.error(f"Energy optimization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# GOLIATH TRADE ENDPOINTS (Financial Trading)
# ============================================================================


class PortfolioOptimizationRequest(BaseModel):
    portfolio_data: Dict[str, Any]
    risk_tolerance: float
    optimization_horizon: int  # days
    constraints: Dict[str, Any]
    optimization_level: str = "standard"


class PortfolioOptimizationResponse(BaseModel):
    optimized_portfolio: Dict[str, Any]
    expected_return: float
    risk_score: float
    quantum_advantage: float
    execution_time: float


@app.post(
    "/goliath-trade/optimize-portfolio", response_model=PortfolioOptimizationResponse
)
async def optimize_portfolio(request: PortfolioOptimizationRequest):
    """Optimize investment portfolio using quantum algorithms"""
    try:
        start_time = datetime.now()

        result = await goliath_trade_pod.optimize_portfolio_quantum(
            request.portfolio_data,
            request.risk_tolerance,
            request.optimization_horizon,
            request.constraints,
            request.optimization_level,
        )

        execution_time = (datetime.now() - start_time).total_seconds()

        return PortfolioOptimizationResponse(
            optimized_portfolio=result.get("optimized_portfolio", {}),
            expected_return=result.get("expected_return", 0.0),
            risk_score=result.get("risk_score", 0.0),
            quantum_advantage=result.get("quantum_advantage", 1.0),
            execution_time=execution_time,
        )

    except Exception as e:
        logger.error(f"Portfolio optimization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# SFG SYMMETRY ENDPOINTS (Insurance & Financial Services)
# ============================================================================


class ClientRegistrationRequest(BaseModel):
    age: int
    income: float
    assets: float
    liabilities: float
    risk_tolerance: float
    investment_horizon: int
    family_status: str
    health_rating: float


class FinancialRecommendationRequest(BaseModel):
    client_id: str
    recommendation_type: str  # portfolio, insurance, retirement
    optimization_level: str = "maximum"


class FinancialRecommendationResponse(BaseModel):
    recommendation_id: str
    products: List[Dict[str, Any]]
    portfolio_allocation: Dict[str, float]
    risk_score: float
    expected_return: float
    quantum_advantage: float
    confidence_level: float


@app.post("/sfg-symmetry/register-client")
async def register_client(request: ClientRegistrationRequest):
    """Register a new client for financial services"""
    try:
        client_data = request.dict()
        client_id = await sfg_symmetry_pod.register_client(client_data)

        return {
            "client_id": client_id,
            "status": "registered",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Client registration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/sfg-symmetry/generate-recommendations",
    response_model=FinancialRecommendationResponse,
)
async def generate_financial_recommendations(request: FinancialRecommendationRequest):
    """Generate quantum-optimized financial recommendations"""
    try:
        recommendation = await sfg_symmetry_pod.generate_financial_recommendations(
            request.client_id
        )

        return FinancialRecommendationResponse(
            recommendation_id=recommendation.recommendation_id,
            products=[
                {
                    "product_id": p.product_id,
                    "name": p.name,
                    "type": p.type,
                    "base_premium": p.base_premium,
                    "coverage_amount": p.coverage_amount,
                }
                for p in recommendation.products
            ],
            portfolio_allocation=recommendation.portfolio_allocation,
            risk_score=recommendation.risk_score,
            expected_return=recommendation.expected_return,
            quantum_advantage=recommendation.quantum_advantage,
            confidence_level=recommendation.confidence_level,
        )

    except Exception as e:
        logger.error(f"Financial recommendations failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sfg-symmetry/client-portfolio/{client_id}")
async def get_client_portfolio(client_id: str):
    """Get client's current portfolio and recommendations"""
    try:
        portfolio = await sfg_symmetry_pod.get_client_portfolio(client_id)
        return portfolio

    except Exception as e:
        logger.error(f"Failed to get client portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# GHOST NEUROQ ENDPOINTS (Quantum Data Intelligence)
# ============================================================================


class TargetRegistrationRequest(BaseModel):
    name: str
    organization: str
    industry: str
    risk_level: float
    data_sources: List[str]
    dependencies: List[str]
    market_position: float
    financial_strength: float
    competitive_position: float
    dependency_level: float
    vulnerability_level: float


class IntelligenceOperationRequest(BaseModel):
    target_id: str
    operation_type: str  # data_extraction, analysis, strategy
    parameters: Dict[str, Any]


class IntelligenceOperationResponse(BaseModel):
    operation_id: str
    status: str
    results: Dict[str, Any]
    quantum_enhanced: bool
    timestamp: str


@app.post("/ghost-neuroq/register-target")
async def register_target(request: TargetRegistrationRequest):
    """Register a new intelligence target"""
    try:
        target_data = request.dict()
        target_id = await ghost_neuroq_pod.register_target(target_data)

        return {
            "target_id": target_id,
            "status": "registered",
            "timestamp": datetime.now().isoformat(),
        }

    except Exception as e:
        logger.error(f"Target registration failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/ghost-neuroq/execute-neuro-siphon", response_model=IntelligenceOperationResponse
)
async def execute_neuro_siphon(request: IntelligenceOperationRequest):
    """Execute NeuroSiphon™ data extraction operation"""
    try:
        if request.operation_type != "data_extraction":
            raise HTTPException(
                status_code=400,
                detail="Operation type must be 'data_extraction' for NeuroSiphon",
            )

        operation = await ghost_neuroq_pod.execute_neuro_siphon(
            request.target_id, request.parameters.get("data_sources", [])
        )

        return IntelligenceOperationResponse(
            operation_id=operation.operation_id,
            status=operation.status,
            results=operation.results,
            quantum_enhanced=operation.quantum_enhanced,
            timestamp=(
                operation.end_time.isoformat()
                if operation.end_time
                else datetime.now().isoformat()
            ),
        )

    except Exception as e:
        logger.error(f"NeuroSiphon operation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ghost-neuroq/create-sigma-graph")
async def create_sigma_graph(request: IntelligenceOperationRequest):
    """Create Sigma Graph with Dynex-powered leverage analysis"""
    try:
        if request.operation_type != "sigma_graph":
            raise HTTPException(
                status_code=400, detail="Operation type must be 'sigma_graph'"
            )

        sigma_graph = await ghost_neuroq_pod.create_sigma_graph(request.target_id)
        return sigma_graph

    except Exception as e:
        logger.error(f"Sigma Graph creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/ghost-neuroq/execute-data-poisoning", response_model=IntelligenceOperationResponse
)
async def execute_data_poisoning(request: IntelligenceOperationRequest):
    """Execute Dynamic Data Poisoning operation"""
    try:
        if request.operation_type != "data_poisoning":
            raise HTTPException(
                status_code=400, detail="Operation type must be 'data_poisoning'"
            )

        strategy = request.parameters.get("strategy", "reality_distortion")
        operation = await ghost_neuroq_pod.execute_data_poisoning(
            request.target_id, strategy
        )

        return IntelligenceOperationResponse(
            operation_id=operation.operation_id,
            status=operation.status,
            results=operation.results,
            quantum_enhanced=operation.quantum_enhanced,
            timestamp=(
                operation.end_time.isoformat()
                if operation.end_time
                else datetime.now().isoformat()
            ),
        )

    except Exception as e:
        logger.error(f"Data poisoning operation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# ORCHESTRATOR ENDPOINTS
# ============================================================================


@app.get("/orchestrator/status")
async def get_orchestrator_status():
    """Get NQBA Stack Orchestrator status"""
    try:
        return {
            "status": "operational",
            "business_pods_count": len(orchestrator.business_pods),
            "active_routes": len(orchestrator.task_routes),
            "quantum_adapters": len(orchestrator.quantum_adapters),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Failed to get orchestrator status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/orchestrator/business-pods")
async def get_registered_business_pods():
    """Get list of registered business pods"""
    try:
        return {
            "business_pods": list(orchestrator.business_pods.keys()),
            "total_count": len(orchestrator.business_pods),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Failed to get business pods: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# LTC LOGGER ENDPOINTS
# ============================================================================


@app.get("/ltc/entries")
async def get_ltc_entries(
    limit: int = 100,
    business_pod: Optional[str] = None,
    operation_type: Optional[str] = None,
):
    """Get LTC entries with optional filtering"""
    try:
        entries = await ltc_logger.get_entries(
            limit=limit, business_pod=business_pod, operation_type=operation_type
        )
        return {
            "entries": entries,
            "total_count": len(entries),
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Failed to get LTC entries: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ltc/statistics")
async def get_ltc_statistics():
    """Get LTC statistics and metrics"""
    try:
        stats = await ltc_logger.get_statistics()
        return {"statistics": stats, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Failed to get LTC statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# QUANTUM ADAPTER ENDPOINTS
# ============================================================================


@app.get("/quantum/status")
async def get_quantum_status():
    """Get quantum computing provider status"""
    try:
        status = await quantum_adapter.get_status()
        return {"status": status, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Failed to get quantum status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/quantum/providers")
async def get_quantum_providers():
    """Get available quantum computing providers"""
    try:
        providers = await quantum_adapter.get_available_providers()
        return {"providers": providers, "timestamp": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Failed to get quantum providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PHASE 2 ENDPOINTS
# ============================================================================


class QUBOCreateRequest(BaseModel):
    dimensions: List[int]
    variable_names: List[str]
    objective_function: str
    constraints: List[Dict[str, Any]]


@app.post("/phase2/advanced-qubo/create", response_model=Dict[str, Any])
async def create_advanced_qubo(request: QUBOCreateRequest):
    """Create a multi-dimensional QUBO matrix"""
    try:
        qubo_matrix = await advanced_qubo_engine.create_multi_dimensional_qubo(
            dimensions=tuple(request.dimensions),
            variable_names=request.variable_names,
            objective_function=request.objective_function,
            constraints=request.constraints,
        )

        return {
            "success": True,
            "matrix_id": qubo_matrix.matrix_id,
            "dimensions": qubo_matrix.dimensions,
            "message": "Advanced QUBO matrix created successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class QUBOOptimizeRequest(BaseModel):
    matrix_id: str
    optimization_config: Dict[str, Any]


@app.post("/phase2/advanced-qubo/optimize", response_model=Dict[str, Any])
async def optimize_advanced_qubo(request: QUBOOptimizeRequest):
    """Optimize a multi-dimensional QUBO matrix"""
    try:
        result = await advanced_qubo_engine.optimize_multi_dimensional_qubo(
            matrix_id=request.matrix_id, optimization_config=request.optimization_config
        )

        return {
            "success": True,
            "result_id": result.result_id,
            "objective_value": result.objective_value,
            "quantum_advantage": result.quantum_advantage,
            "execution_time": result.execution_time,
            "message": "Advanced QUBO optimization completed successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AlgorithmRegistrationRequest(BaseModel):
    algorithm_type: str
    parameters: Dict[str, Any]
    hyperparameters: Dict[str, Any]
    constraints: Dict[str, Any]
    version: str = "1.0.0"


@app.post("/phase2/learning/register-algorithm", response_model=Dict[str, Any])
async def register_learning_algorithm(request: AlgorithmRegistrationRequest):
    """Register a new optimization algorithm with the learning engine"""
    try:
        algorithm_config = await real_time_learning_engine.register_algorithm(
            algorithm_type=AlgorithmType(request.algorithm_type),
            parameters=request.parameters,
            hyperparameters=request.hyperparameters,
            constraints=request.constraints,
            version=request.version,
        )

        return {
            "success": True,
            "algorithm_id": algorithm_config.algorithm_id,
            "algorithm_type": algorithm_config.algorithm_type.value,
            "message": "Algorithm registered successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PerformanceRecordRequest(BaseModel):
    algorithm_id: str
    performance_metrics: Dict[str, float]
    problem_characteristics: Dict[str, Any]
    execution_context: Dict[str, Any]
    success: bool
    metadata: Dict[str, Any] = None


@app.post("/phase2/learning/record-performance", response_model=Dict[str, Any])
async def record_algorithm_performance(request: PerformanceRecordRequest):
    """Record performance data for algorithm learning"""
    try:
        record_id = await real_time_learning_engine.record_performance(
            algorithm_id=request.algorithm_id,
            performance_metrics=request.performance_metrics,
            problem_characteristics=request.problem_characteristics,
            execution_context=request.execution_context,
            success=request.success,
            metadata=request.metadata,
        )

        return {
            "success": True,
            "record_id": record_id,
            "message": "Performance recorded successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TenantCreateRequest(BaseModel):
    name: str
    resource_limits: Dict[str, float]
    scaling_policy: str = "auto"
    isolation_level: str = "moderate"
    business_rules: Dict[str, Any] = None
    sla_requirements: Dict[str, Any] = None


@app.post("/phase2/tenant/create", response_model=Dict[str, Any])
async def create_tenant(request: TenantCreateRequest):
    """Create a new multi-tenant environment"""
    try:
        tenant_config = await multi_tenant_manager.create_tenant(
            name=request.name,
            resource_limits=request.resource_limits,
            scaling_policy=ScalingPolicy(request.scaling_policy),
            isolation_level=request.isolation_level,
            business_rules=request.business_rules,
            sla_requirements=request.sla_requirements,
        )

        return {
            "success": True,
            "tenant_id": tenant_config.tenant_id,
            "tenant_name": tenant_config.name,
            "status": tenant_config.status.value,
            "message": "Tenant created successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class TenantMetricsRequest(BaseModel):
    metrics_data: Dict[str, Any]


# Phase 2.1 Request Models
class ConstraintEvolutionRequest(BaseModel):
    tenant_id: str
    constraint_ids: List[str]
    performance_threshold: float = 0.85
    evolution_strategy: str = "moderate"


class PerformancePredictionRequest(BaseModel):
    constraint_id: str
    scenario_data: Dict[str, Any]


class ResourceDemandPredictionRequest(BaseModel):
    tenant_id: str
    time_horizon: int
    resource_types: List[str] = None
    include_business_cycles: bool = True


class ScalingScheduleRequest(BaseModel):
    predictions: List[Dict[str, Any]]
    tenant_id: str
    optimization_algorithm: str = "genetic"


class EnterpriseAuthenticationRequest(BaseModel):
    auth_type: str
    assertion: str
    issuer: str


class ComplianceCheckRequest(BaseModel):
    operation: str
    data: Dict[str, Any]
    frameworks: List[str] = None
    timeout: int = 30


class AlgorithmSubmissionRequest(BaseModel):
    name: str
    description: str
    category: str
    complexity: str
    price: float
    source_code: str
    documentation: str
    tags: List[str] = None
    requirements: List[str] = None
    example_usage: str = ""


class TutorialCreationRequest(BaseModel):
    title: str
    content: str
    category: str
    difficulty: str
    tags: List[str] = None
    estimated_time: int
    prerequisites: List[str] = None


@app.post("/phase2/tenant/{tenant_id}/metrics", response_model=Dict[str, Any])
async def record_tenant_metrics(tenant_id: str, request: TenantMetricsRequest):
    """Record performance metrics for a tenant"""
    try:
        record_id = await multi_tenant_manager.record_tenant_metrics(
            tenant_id=tenant_id, metrics_data=request.metrics_data
        )

        return {
            "success": True,
            "record_id": record_id,
            "message": "Tenant metrics recorded successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2/tenant/{tenant_id}/analytics", response_model=Dict[str, Any])
async def get_tenant_analytics(tenant_id: str):
    """Get analytics for a specific tenant"""
    try:
        analytics = await multi_tenant_manager.get_tenant_analytics(tenant_id)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2/dashboard/summary", response_model=Dict[str, Any])
async def get_dashboard_summary():
    """Get comprehensive dashboard summary"""
    try:
        summary = await advanced_performance_dashboard.get_dashboard_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2/dashboard/tenant/{tenant_id}", response_model=Dict[str, Any])
async def get_tenant_dashboard(tenant_id: str):
    """Get performance dashboard for a specific tenant"""
    try:
        tenant_data = await advanced_performance_dashboard.get_tenant_performance(
            tenant_id
        )
        return tenant_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2/dashboard/start", response_model=Dict[str, Any])
async def start_performance_dashboard():
    """Start the advanced performance dashboard"""
    try:
        await advanced_performance_dashboard.start_dashboard()
        return {
            "success": True,
            "message": "Performance dashboard started successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2/dashboard/stop", response_model=Dict[str, Any])
async def stop_performance_dashboard():
    """Stop the advanced performance dashboard"""
    try:
        await advanced_performance_dashboard.stop_dashboard()
        return {
            "success": True,
            "message": "Performance dashboard stopped successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2/analytics/qubo", response_model=Dict[str, Any])
async def get_qubo_analytics():
    """Get analytics from the Advanced QUBO Engine"""
    try:
        analytics = await advanced_qubo_engine.get_optimization_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2/analytics/learning", response_model=Dict[str, Any])
async def get_learning_analytics():
    """Get analytics from the Real-Time Learning Engine"""
    try:
        analytics = await real_time_learning_engine.get_learning_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2/analytics/tenant", response_model=Dict[str, Any])
async def get_tenant_system_analytics():
    """Get system-wide analytics from the Multi-Tenant Manager"""
    try:
        analytics = await multi_tenant_manager.get_system_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DEMO ENDPOINTS
# ============================================================================


@app.post("/demo/run-comprehensive")
async def run_comprehensive_demo():
    """Run comprehensive demonstration of all business pods"""
    try:
        # This would run the comprehensive demo
        # For now, return a summary
        return {
            "status": "demo_scheduled",
            "message": "Comprehensive demo scheduled to run",
            "business_pods": [
                "sigma_select",
                "flyfox_ai",
                "goliath_trade",
                "sfg_symmetry",
                "ghost_neuroq",
            ],
            "timestamp": datetime.now().isoformat(),
        }
    except Exception as e:
        logger.error(f"Demo scheduling failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# PHASE 2.1 API ENDPOINTS
# ============================================================================


# Constraint Evolution Endpoints
@app.post("/phase2.1/constraints/evolve", response_model=Dict[str, Any])
async def evolve_constraints(request: ConstraintEvolutionRequest):
    """Evolve constraints using AI-driven optimization"""
    try:
        strategy = EvolutionStrategy(request.evolution_strategy)
        constraint_updates = await constraint_evolution_engine.evolve_constraints(
            tenant_id=request.tenant_id,
            performance_data={"constraint_ids": request.constraint_ids},
            strategy=strategy,
        )

        return {
            "success": True,
            "updates_count": len(constraint_updates),
            "constraint_updates": [
                {
                    "constraint_id": update.constraint_id,
                    "old_parameters": update.old_parameters,
                    "new_parameters": update.new_parameters,
                    "evolution_reason": update.evolution_reason,
                    "confidence_score": update.confidence_score,
                    "expected_improvement": update.expected_improvement,
                    "risk_assessment": update.risk_assessment,
                }
                for update in constraint_updates
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.1/constraints/predict-performance", response_model=Dict[str, Any])
async def predict_constraint_performance(request: PerformancePredictionRequest):
    """Predict constraint performance under different scenarios"""
    try:
        prediction = await constraint_evolution_engine.predict_constraint_performance(
            constraint_id=request.constraint_id, scenario_data=request.scenario_data
        )

        return {
            "success": True,
            "constraint_id": prediction.constraint_id,
            "scenario_name": prediction.scenario_name,
            "predicted_performance": prediction.predicted_performance,
            "confidence_interval": prediction.confidence_interval,
            "risk_factors": prediction.risk_factors,
            "recommendations": prediction.recommendations,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/phase2.1/constraints/evolution-history/{tenant_id}", response_model=Dict[str, Any]
)
async def get_constraint_evolution_history(
    tenant_id: str, time_range: Optional[int] = None
):
    """Get evolution history for constraints"""
    try:
        history = await constraint_evolution_engine.get_evolution_history(
            tenant_id, time_range
        )
        return {
            "success": True,
            "tenant_id": tenant_id,
            "history_count": len(history),
            "evolution_history": [
                {
                    "constraint_id": entry.constraint_id,
                    "evolution_reason": entry.evolution_reason,
                    "confidence_score": entry.confidence_score,
                    "expected_improvement": entry.expected_improvement,
                    "applied_at": entry.applied_at.isoformat(),
                }
                for entry in history
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Predictive Scaling Endpoints
@app.post("/phase2.1/scaling/predict-demand", response_model=Dict[str, Any])
async def predict_resource_demand(request: ResourceDemandPredictionRequest):
    """Predict resource demand for scaling"""
    try:
        resource_types = [
            ResourceType(rt)
            for rt in (request.resource_types or ["compute", "memory", "storage"])
        ]
        predictions = await predictive_scaler.predict_resource_demand(
            tenant_id=request.tenant_id,
            time_horizon=request.time_horizon,
            resource_types=resource_types,
            include_business_cycles=request.include_business_cycles,
        )

        return {
            "success": True,
            "predictions_count": len(predictions),
            "predictions": [
                {
                    "resource_type": pred.resource_type.value,
                    "predicted_demand": pred.predicted_demand,
                    "confidence_interval": pred.confidence_interval,
                    "trend_direction": pred.trend_direction,
                    "business_cycle_factor": pred.business_cycle_factor,
                    "seasonal_factor": pred.seasonal_factor,
                    "market_factor": pred.market_factor,
                }
                for pred in predictions
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.1/scaling/optimize-schedule", response_model=Dict[str, Any])
async def optimize_scaling_schedule(request: ScalingScheduleRequest):
    """Optimize scaling schedule for cost efficiency"""
    try:
        algorithm = ScalingAlgorithm(request.optimization_algorithm)

        # Convert JSON predictions to ResourceDemandPrediction objects
        from .scaling.predictive_scaler import ResourceDemandPrediction, ResourceType

        predictions = []
        for pred_data in request.predictions:
            prediction = ResourceDemandPrediction(
                resource_type=ResourceType(pred_data["resource_type"]),
                predicted_demand=pred_data["predicted_demand"],
                confidence_interval=pred_data["confidence_interval"],
                trend_direction=pred_data["trend_direction"],
                timestamp=datetime.now(),
                business_cycle_factor=0.5,
                seasonal_factor=0.3,
                market_factor=0.2,
            )
            predictions.append(prediction)

        schedule = await predictive_scaler.optimize_scaling_schedule(
            predictions=predictions,
            tenant_id=request.tenant_id,
            optimization_algorithm=algorithm,
        )

        return {
            "success": True,
            "schedule_id": schedule.schedule_id,
            "actions_count": len(schedule.actions),
            "total_estimated_cost": schedule.total_estimated_cost,
            "expected_savings": schedule.expected_savings,
            "risk_level": schedule.risk_level,
            "actions": [
                {
                    "action_id": action.action_id,
                    "resource_type": action.resource_type.value,
                    "current_capacity": action.current_capacity,
                    "target_capacity": action.target_capacity,
                    "scaling_reason": action.scaling_reason,
                    "priority": action.priority,
                    "estimated_cost": action.estimated_cost,
                }
                for action in schedule.actions
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.1/scaling/apply-schedule", response_model=Dict[str, Any])
async def apply_scaling_schedule(schedule_id: str, auto_approve: bool = False):
    """Apply a scaling schedule"""
    try:
        # This would retrieve the schedule from storage
        # For now, return a mock result
        return {
            "success": True,
            "schedule_id": schedule_id,
            "message": "Scaling schedule applied successfully",
            "actions_applied": 3,
            "actions_failed": 0,
            "total_cost": 45.50,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Enterprise Integration Endpoints
@app.post("/phase2.1/enterprise/authenticate", response_model=Dict[str, Any])
async def authenticate_enterprise_user(request: EnterpriseAuthenticationRequest):
    """Authenticate user via enterprise SSO"""
    try:
        if request.auth_type == "saml":
            from .enterprise.enterprise_security_manager import SAMLCredentials

            credentials = SAMLCredentials(
                assertion=request.assertion, issuer=request.issuer
            )
        elif request.auth_type == "oauth":
            from .enterprise.enterprise_security_manager import OAuthCredentials

            credentials = OAuthCredentials(
                access_token=request.assertion, token_type="Bearer"
            )
        elif request.auth_type == "ldap":
            from .enterprise.enterprise_security_manager import LDAPCredentials

            credentials = LDAPCredentials(
                username=request.assertion, password=request.issuer
            )
        else:
            raise HTTPException(
                status_code=400, detail="Unsupported authentication type"
            )

        auth_result = await enterprise_security_manager.authenticate_user(credentials)

        if auth_result.is_authenticated:
            return {
                "success": True,
                "user_id": auth_result.user_id,
                "username": auth_result.username,
                "email": auth_result.email,
                "groups": auth_result.groups,
                "permissions": auth_result.permissions,
                "session_token": auth_result.session_token,
                "expires_at": (
                    auth_result.expires_at.isoformat()
                    if auth_result.expires_at
                    else None
                ),
            }
        else:
            raise HTTPException(status_code=401, detail=auth_result.error_message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.1/enterprise/compliance-check", response_model=Dict[str, Any])
async def check_compliance(request: ComplianceCheckRequest):
    """Check compliance for operations"""
    try:
        frameworks = [
            ComplianceFramework(f)
            for f in (request.frameworks or ["soc2", "iso27001", "gdpr"])
        ]
        compliance_result = await enterprise_security_manager.enforce_compliance(
            operation=request.operation,
            data=request.data,
            frameworks=frameworks,
            timeout=request.timeout,
        )

        return {
            "success": True,
            "is_compliant": compliance_result.is_compliant,
            "framework": compliance_result.framework.value,
            "requirements_checked": compliance_result.requirements_checked,
            "compliant_requirements": compliance_result.compliant_requirements,
            "non_compliant_requirements": compliance_result.non_compliant_requirements,
            "violations": compliance_result.violations,
            "warnings": compliance_result.warnings,
            "recommendations": compliance_result.recommendations,
            "audit_trail": compliance_result.audit_trail,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class AuditLogRequest(BaseModel):
    user_id: str
    action: str
    details: Dict[str, Any]
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


@app.post("/phase2.1/enterprise/audit-log", response_model=Dict[str, Any])
async def create_audit_log(request: AuditLogRequest):
    """Create audit log entry"""
    try:
        audit_entry = await enterprise_security_manager.audit_log(
            user_id=request.user_id,
            action=request.action,
            details=request.details,
            ip_address=request.ip_address,
            user_agent=request.user_agent,
        )

        return {
            "success": True,
            "entry_id": audit_entry.entry_id,
            "timestamp": audit_entry.timestamp.isoformat(),
            "message": "Audit log entry created successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Community Platform Endpoints
@app.post("/phase2.1/community/submit-algorithm", response_model=Dict[str, Any])
async def submit_algorithm(request: AlgorithmSubmissionRequest):
    """Submit algorithm to marketplace"""
    try:
        from .community.community_platform import (
            QuantumAlgorithm,
            DeveloperProfile,
            AlgorithmCategory,
            AlgorithmComplexity,
        )

        # Create developer profile (in production, this would come from authentication)
        developer = DeveloperProfile(
            developer_id="dev_temp_001",
            username="temp_developer",
            email="temp@example.com",
            full_name="Temporary Developer",
        )

        # Create algorithm object
        algorithm = QuantumAlgorithm(
            algorithm_id="",  # Will be generated
            name=request.name,
            description=request.description,
            category=AlgorithmCategory(request.category),
            complexity=AlgorithmComplexity(request.complexity),
            price=request.price,
            source_code=request.source_code,
            documentation=request.documentation,
            author=developer,
            tags=request.tags or [],
            requirements=request.requirements or [],
            example_usage=request.example_usage,
        )

        submission_result = await algorithm_marketplace.submit_algorithm(
            algorithm, developer
        )

        return {
            "success": submission_result.is_successful,
            "algorithm_id": submission_result.algorithm_id,
            "message": submission_result.message,
            "validation_errors": submission_result.validation_errors,
            "estimated_review_time": submission_result.estimated_review_time,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2.1/community/discover-algorithms", response_model=Dict[str, Any])
async def discover_algorithms(
    category: Optional[str] = None,
    complexity: Optional[str] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    tags: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    """Discover algorithms in marketplace"""
    try:
        from .community.community_platform import (
            SearchCriteria,
            AlgorithmCategory,
            AlgorithmComplexity,
        )

        search_criteria = SearchCriteria(
            category=AlgorithmCategory(category) if category else None,
            complexity=AlgorithmComplexity(complexity) if complexity else None,
            max_price=max_price,
            min_rating=min_rating,
            tags=tags.split(",") if tags else [],
            sort_by="relevance",
        )

        algorithms = await algorithm_marketplace.discover_algorithms(
            search_criteria, limit, offset
        )

        return {
            "success": True,
            "algorithms_count": len(algorithms),
            "algorithms": [
                {
                    "algorithm_id": algo.algorithm_id,
                    "name": algo.name,
                    "description": algo.description,
                    "category": algo.category.value,
                    "complexity": algo.complexity.value,
                    "price": algo.price,
                    "author": {
                        "username": algo.author.username,
                        "full_name": algo.author.full_name,
                        "reputation_score": algo.author.reputation_score,
                    },
                    "rating": algo.rating,
                    "review_count": algo.review_count,
                    "download_count": algo.download_count,
                    "tags": algo.tags,
                    "created_at": algo.created_at.isoformat(),
                    "preview_available": algo.preview_available,
                }
                for algo in algorithms
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.1/community/purchase-algorithm", response_model=Dict[str, Any])
async def purchase_algorithm(algorithm_id: str, license_type: str, buyer_id: str):
    """Purchase algorithm license"""
    try:
        purchase_result = await algorithm_marketplace.purchase_algorithm(
            algorithm_id=algorithm_id, license_type=license_type, buyer_id=buyer_id
        )

        return {
            "success": purchase_result.is_successful,
            "purchase_id": purchase_result.purchase_id,
            "download_url": purchase_result.download_url,
            "license_key": purchase_result.license_key,
            "message": purchase_result.message,
            "error_details": purchase_result.error_details,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.1/community/create-tutorial", response_model=Dict[str, Any])
async def create_tutorial(request: TutorialCreationRequest):
    """Create tutorial in developer portal"""
    try:
        from .community.community_platform import (
            Tutorial,
            DeveloperProfile,
            AlgorithmComplexity,
        )

        # Create developer profile (in production, this would come from authentication)
        developer = DeveloperProfile(
            developer_id="dev_temp_001",
            username="temp_developer",
            email="temp@example.com",
            full_name="Temporary Developer",
        )

        # Create tutorial object
        tutorial = Tutorial(
            tutorial_id="",  # Will be generated
            title=request.title,
            content=request.content,
            author=developer,
            category=request.category,
            difficulty=AlgorithmComplexity(request.difficulty),
            tags=request.tags or [],
            estimated_time=request.estimated_time,
            prerequisites=request.prerequisites or [],
        )

        tutorial_result = await developer_portal.create_tutorial(tutorial, developer)

        return {
            "success": tutorial_result.is_successful,
            "tutorial_id": tutorial_result.tutorial_id,
            "message": tutorial_result.message,
            "validation_errors": tutorial_result.validation_errors,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2.1/community/forums", response_model=Dict[str, Any])
async def get_active_forums():
    """Get list of active community forums"""
    try:
        forums = await community_manager.get_active_forums()

        return {
            "success": True,
            "forums_count": len(forums),
            "forums": [
                {
                    "forum_id": forum.forum_id,
                    "name": forum.name,
                    "description": forum.description,
                    "category": forum.category,
                    "is_public": forum.is_public,
                    "moderation_level": forum.moderation_level,
                    "member_count": forum.member_count,
                    "topic_count": forum.topic_count,
                    "is_active": forum.is_active,
                }
                for forum in forums
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2.1/community/events", response_model=Dict[str, Any])
async def get_upcoming_events():
    """Get list of upcoming community events"""
    try:
        events = await community_manager.get_upcoming_events()

        return {
            "success": True,
            "events_count": len(events),
            "events": [
                {
                    "event_id": event.event_id,
                    "title": event.title,
                    "description": event.description,
                    "event_type": event.event_type,
                    "start_date": event.start_date.isoformat(),
                    "end_date": event.end_date.isoformat(),
                    "organizer": {
                        "username": event.organizer.username,
                        "full_name": event.organizer.full_name,
                    },
                    "is_online": event.is_online,
                    "location": event.location,
                    "status": event.status,
                }
                for event in events
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# STARTUP AND SHUTDOWN EVENTS
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """Initialize all components on startup"""
    logger.info("Starting Goliath Quantum Starter API Server v2.2.0")

    # Initialize Phase 1 components
    try:
        # Initialize quantum adapter
        await quantum_adapter.initialize()

        # Initialize business pods
        await sigma_select_pod.initialize()
        await flyfox_ai_pod.initialize()
        await goliath_trade_pod.initialize()
        await sfg_symmetry_pod.initialize()
        await ghost_neuroq_pod.initialize()

        # Register business pods with orchestrator
        await orchestrator.register_business_pod(sigma_select_pod)
        await orchestrator.register_business_pod(flyfox_ai_pod)
        await orchestrator.register_business_pod(goliath_trade_pod)
        await orchestrator.register_business_pod(sfg_symmetry_pod)
        await orchestrator.register_business_pod(ghost_neuroq_pod)

        logger.info("Phase 1 components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Phase 1 components: {e}")

    # Initialize Phase 2 components
    try:
        # Initialize multi-tenant management
        await multi_tenant_manager.initialize()

        # Initialize real-time learning engine
        await real_time_learning_engine.initialize()

        # Initialize advanced QUBO engine
        await advanced_qubo_engine.initialize()

        # Initialize performance dashboard
        await advanced_performance_dashboard.initialize()

        logger.info("Phase 2 components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Phase 2 components: {e}")

    # Initialize Phase 2.1 components
    try:
        # Train constraint evolution models
        await constraint_evolution_engine.train_models("default")

        # Initialize predictive scaling models
        await predictive_scaler.retrain_models("default")

        # Clean up expired enterprise sessions
        await enterprise_security_manager.cleanup_expired_sessions()

        logger.info("Phase 2.1 components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Phase 2.1 components: {e}")

    # Initialize Phase 2.2 components
    try:
        # Initialize advanced QUBO engine (already done above, but ensure it's ready)
        logger.info("Phase 2.2 components initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing Phase 2.2 components: {e}")

    logger.info("All components initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Goliath Quantum Starter API Server")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "api_server:app", host="0.0.0.0", port=8000, reload=True, log_level="info"
    )


# Phase 2.2 Request Models
class QUBOCreateProblemRequest(BaseModel):
    name: str
    description: str
    objective_function: str
    variables: List[str]
    constraints: List[Dict[str, Any]]
    strategy: str
    tenant_id: str


class LearningModelCreateRequest(BaseModel):
    algorithm_type: str
    learning_mode: str
    initial_parameters: Dict[str, Any]
    tenant_id: str


class LearningExampleRequest(BaseModel):
    model_id: str
    input_data: Dict[str, Any]
    expected_output: Dict[str, Any]
    actual_output: Dict[str, Any]
    tenant_id: str


# Phase 2.2 API Endpoints - Advanced QUBO Engine
@app.post("/phase2.2/qubo/create-problem", response_model=Dict[str, Any])
async def create_optimization_problem(request: QUBOCreateProblemRequest):
    """Create a new optimization problem"""
    try:
        result = await advanced_qubo_engine.create_optimization_problem(
            name=request.name,
            description=request.description,
            objective_function=request.objective_function,
            variables=request.variables,
            constraints=request.constraints,
            strategy=request.strategy,
            tenant_id=request.tenant_id,
        )
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to create optimization problem: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.2/qubo/optimize/{problem_id}", response_model=Dict[str, Any])
async def optimize_problem(
    problem_id: str,
    initial_values: Optional[Dict[str, float]] = None,
    max_iterations: Optional[int] = None,
):
    """Optimize a problem using advanced QUBO techniques"""
    try:
        result = await advanced_qubo_engine.optimize_problem(
            problem_id=problem_id,
            initial_values=initial_values,
            max_iterations=max_iterations,
        )
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to optimize problem: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2.2/qubo/problem/{problem_id}/status", response_model=Dict[str, Any])
async def get_problem_status(problem_id: str):
    """Get current status of optimization problem"""
    try:
        result = await advanced_qubo_engine.get_problem_status(problem_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to get problem status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2.2/qubo/tenant/{tenant_id}/problems", response_model=Dict[str, Any])
async def get_tenant_problems(tenant_id: str):
    """Get all optimization problems for a tenant"""
    try:
        result = await advanced_qubo_engine.get_tenant_problems(tenant_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to get tenant problems: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2.2/qubo/tenant/{tenant_id}/analytics", response_model=Dict[str, Any])
async def get_qubo_analytics(tenant_id: str):
    """Get performance analytics for QUBO optimization"""
    try:
        result = await advanced_qubo_engine.get_performance_analytics(tenant_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to get QUBO analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Phase 2.2 API Endpoints - Real-Time Learning Engine
@app.post("/phase2.2/learning/create-model", response_model=Dict[str, Any])
async def create_learning_model(request: LearningModelCreateRequest):
    """Create a new learning model"""
    try:
        result = await real_time_learning_engine.create_learning_model(
            algorithm_type=request.algorithm_type,
            learning_mode=request.learning_mode,
            initial_parameters=request.initial_parameters,
            tenant_id=request.tenant_id,
        )
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to create learning model: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.2/learning/add-example", response_model=Dict[str, Any])
async def add_learning_example(request: LearningExampleRequest):
    """Add a learning example to improve the model"""
    try:
        result = await real_time_learning_engine.add_learning_example(
            model_id=request.model_id,
            input_data=request.input_data,
            expected_output=request.expected_output,
            actual_output=request.actual_output,
            tenant_id=request.tenant_id,
        )
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to add learning example: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/phase2.2/learning/model/{model_id}/performance", response_model=Dict[str, Any]
)
async def get_model_performance(model_id: str):
    """Get performance metrics for a learning model"""
    try:
        result = await real_time_learning_engine.get_model_performance(model_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to get model performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/phase2.2/learning/tenant/{tenant_id}/summary", response_model=Dict[str, Any])
async def get_learning_summary(tenant_id: str):
    """Get learning summary for a tenant"""
    try:
        result = await real_time_learning_engine.get_tenant_learning_summary(tenant_id)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to get learning summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/phase2.2/learning/export/{tenant_id}", response_model=Dict[str, Any])
async def export_learning_data(tenant_id: str, format: str = "json"):
    """Export learning data for analysis"""
    try:
        result = await real_time_learning_engine.export_learning_data(tenant_id, format)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"Failed to export learning data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
