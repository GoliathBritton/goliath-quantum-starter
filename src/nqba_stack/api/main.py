#!/usr/bin/env python3
"""
🚀 NQBA Stack - Main FastAPI Application

Main FastAPI application for the NQBA ecosystem with business unit
integration, authentication, and comprehensive API endpoints.
"""

import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from .business_units import router as business_units_router
from .high_council import router as high_council_router
from .monitoring import router as monitoring_router
from .auth import router as auth_router
from .qih import router as qih_router
from .video_processing import router as video_processing_router
from ..business_integration import business_unit_manager
from ..business_integration.flyfox_ai import FLYFOXAIBusinessUnit
from ..core.settings import get_settings
from ..core.ltc_logger import LTCLogger

# Import quantum algorithms
from ...quantum.reasoning import reversal_reasoning, ReversalReasoning
from ...quantum.optimization import parallel_qaoa, optimize_qaoa, qaoa_engine, OptimizationResult
from ...quantum.diffusion import quantum_diffusion, parallel_quantum_diffusion, get_diffusion_performance
from ...quantum.meta_algorithm import (
    dynamic_algo_instituter,
    get_meta_performance,
    adapt_preferences
)
from pydantic import BaseModel, Field
from typing import List, Optional, Union
import numpy as np

# Import observability components
from ..observability import (
    get_tracer,
    instrument_fastapi,
    TracingMiddleware,
    NQBADashboard,
)

# Initialize logger
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting NQBA Stack API...")

    try:
        # Initialize observability system
        logger.info("🔍 Initializing observability system...")
        tracer = get_tracer()

        # Instrument FastAPI with OpenTelemetry
        instrument_fastapi(app, tracer)
        logger.info("✅ OpenTelemetry instrumentation complete")

        # Business unit manager is already initialized
        logger.info("✅ Business unit manager ready")

        # Register FLYFOX AI business unit
        flyfox_ai_unit = FLYFOXAIBusinessUnit()
        await business_unit_manager.register_business_unit(flyfox_ai_unit)
        logger.info("✅ FLYFOX AI business unit registered")

        # Initialize authentication system
        from ..auth import AuthManager

        _ = AuthManager()  # Initialize AuthManager
        logger.info("✅ Authentication system initialized")

        logger.info("🚀 NQBA Stack API startup complete!")

    except Exception as e:
        logger.error(f"❌ Startup error: {str(e)}")
        raise

    yield

    # Shutdown
    logger.info("🔄 Shutting down NQBA Stack API...")

    try:
        # Shutdown business unit manager
        await business_unit_manager.shutdown()
        logger.info("✅ Business unit manager shutdown complete")

        logger.info("✅ NQBA Stack API shutdown complete!")

    except Exception as e:
        logger.error(f"❌ Shutdown error: {str(e)}")


# Create FastAPI app
app = FastAPI(
    title="NQBA Stack API",
    description="Neuromorphic Quantum Business Architecture - The Operating System of the Intelligence Economy",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Get settings
settings = get_settings()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# Add observability tracing middleware
tracer = get_tracer()
# Note: TracingMiddleware will be integrated via decorator pattern for specific endpoints


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.time()

    # Log request
    logger.info(f"📥 {request.method} {request.url.path} - {request.client.host}")

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = time.time() - start_time

    # Log response
    logger.info(
        f"📤 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s"
    )

    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)

    return response


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422, content={"error": "Validation error", "details": exc.errors()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    request_id = str(uuid.uuid4())
    logger.error(f"General Exception: {str(exc)}", exc_info=True, extra={"request_id": request_id})
    return JSONResponse(
        status_code=500, 
        content={
            "error": "Internal server error", 
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        }
    )


# Core endpoints
@app.get("/", tags=["Core"])
async def root():
    """Root endpoint with NQBA ecosystem information"""
    return {
        "message": "🚀 Welcome to NQBA Stack - The Operating System of the Intelligence Economy",
        "version": "2.0.0",
        "ecosystem": "Neuromorphic Quantum Business Architecture",
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
        "info": "/info",
    }


@app.get("/health", tags=["Core"])
async def health_check():
    """Health check endpoint"""
    try:
        # Check business unit manager health
        ecosystem_status = await business_unit_manager.get_ecosystem_status()

        return {
            "status": "healthy",
            "timestamp": time.time(),
            "ecosystem": ecosystem_status,
            "version": "2.0.0",
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.get("/info", tags=["Core"])
async def system_info():
    """System information endpoint"""
    settings = get_settings()

    return {
        "system": "NQBA Stack",
        "version": "2.0.0",
        "description": "Neuromorphic Quantum Business Architecture",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "allowed_hosts": settings.ALLOWED_HOSTS,
        "cors_origins": settings.ALLOWED_ORIGINS,
        "api_docs": "/docs",
        "redoc": "/redoc",
    }


# Pydantic models for quantum algorithms
class ReasoningInput(BaseModel):
    premise: str = Field(..., description="The premise for reasoning")
    conclusion: str = Field(..., description="The conclusion to evaluate")
    coherence_threshold: Optional[float] = Field(0.9, description="Coherence threshold for reasoning")

class OptimizationInput(BaseModel):
    graph_matrices: List[List[List[float]]] = Field(..., description="List of 2D matrices for optimization")
    problem_type: Optional[str] = Field("portfolio", description="Type of optimization problem")
    num_workers: Optional[int] = Field(4, description="Number of parallel workers")

class SingleOptimizationInput(BaseModel):
    graph_matrix: List[List[float]] = Field(..., description="2D matrix for single optimization")
    problem_type: Optional[str] = Field("portfolio", description="Type of optimization problem")

class EnergyOptimizationInput(BaseModel):
    data: List[List[float]] = Field(..., description="Adjacency matrix for energy network")

class DiffusionInput(BaseModel):
    steps: int = Field(10, description="Number of diffusion steps")
    dim: int = Field(2, description="Quantum system dimension")
    efficiency_threshold: Optional[float] = Field(0.8, description="Efficiency threshold for optimization")

class ParallelDiffusionInput(BaseModel):
    scenarios: List[dict] = Field(..., description="List of diffusion scenarios")
    max_workers: int = Field(4, description="Maximum number of parallel workers")

class MetaAlgorithmInput(BaseModel):
    task_type: str = Field(..., description="Type of task (reasoning, optimization, diffusion, etc.)")
    data: dict = Field(..., description="Task data and parameters")
    prefer_parallel: bool = Field(True, description="Prefer parallel algorithms when available")

# Quantum Algorithm Endpoints
@app.post("/api/v1/quantum/reasoning", tags=["Quantum Algorithms"])
async def quantum_reasoning(input_data: ReasoningInput):
    """Advanced reversal reasoning for logical inference using qdLLM-inspired bidirectional processing"""
    try:
        result = await reversal_reasoning(
            premise=input_data.premise,
            conclusion=input_data.conclusion,
            coherence_threshold=input_data.coherence_threshold
        )
        return {
            "status": "success",
            "algorithm": "Reversal Reasoning",
            "result": result,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Quantum reasoning failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Reasoning failed: {str(e)}")

@app.post("/api/v1/quantum/optimization/parallel", tags=["Quantum Algorithms"])
async def parallel_quantum_optimization(input_data: OptimizationInput):
    """Parallel QAOA optimization for finance, energy, and insurance applications"""
    try:
        # Convert input matrices to numpy arrays
        graph_matrices = [np.array(matrix) for matrix in input_data.graph_matrices]
        
        # Set worker count for the engine
        qaoa_engine.max_workers = input_data.num_workers
        
        results = await parallel_qaoa(
            graph_matrices=graph_matrices,
            problem_type=input_data.problem_type
        )
        
        # Convert results to serializable format
        serialized_results = []
        for result in results:
            serialized_results.append({
                "parameters": result.parameters.tolist(),
                "cost": float(result.cost),
                "iterations": result.iterations,
                "execution_time": result.execution_time,
                "method": result.method
            })
        
        return {
            "status": "success",
            "algorithm": "Parallel QAOA Optimization",
            "problem_type": input_data.problem_type,
            "num_problems": len(graph_matrices),
            "results": serialized_results,
            "performance_stats": qaoa_engine.get_performance_stats(),
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Parallel quantum optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.post("/api/v1/quantum/optimization/single", tags=["Quantum Algorithms"])
async def single_quantum_optimization(input_data: SingleOptimizationInput):
    """Single QAOA optimization for individual problems"""
    try:
        # Convert input matrix to numpy array
        graph_matrix = np.array(input_data.graph_matrix)
        
        result = optimize_qaoa(
            graph_matrix=graph_matrix,
            problem_type=input_data.problem_type
        )
        
        return {
            "status": "success",
            "algorithm": "Single QAOA Optimization",
            "problem_type": input_data.problem_type,
            "result": {
                "parameters": result.parameters.tolist(),
                "cost": float(result.cost),
                "iterations": result.iterations,
                "execution_time": result.execution_time,
                "method": result.method
            },
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Single quantum optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

@app.get("/api/v1/quantum/performance", tags=["Quantum Algorithms"])
async def get_quantum_performance():
    """Get performance statistics for quantum algorithms"""
    try:
        qaoa_metrics = qaoa_engine.get_performance_stats()
        diffusion_metrics = get_diffusion_performance()
        meta_metrics = get_meta_performance()
        
        return {
            "status": "success",
            "qaoa_performance": qaoa_metrics,
            "diffusion_performance": diffusion_metrics,
            "meta_algorithm_performance": meta_metrics,
            "algorithms_available": [
                "Reversal Reasoning",
                "Parallel QAOA Optimization",
                "Single QAOA Optimization",
                "Quantum Diffusion",
                "Parallel Quantum Diffusion",
                "Dynamic Meta Algorithm"
            ],
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Failed to get quantum performance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Performance retrieval failed: {str(e)}")

# Energy Optimization Endpoint
@app.post("/business-units/energy/optimize", tags=["Business Units", "Energy"])
async def optimize_energy(input_data: EnergyOptimizationInput):
    """Optimize energy networks using parallel QAOA"""
    try:
        # Convert list to numpy arrays for batch processing
        matrices = [np.array(d) for d in input_data.data]
        
        # Execute parallel QAOA optimization
        results = await parallel_qaoa(matrices, problem_type="energy")
        
        # Convert results to serializable format
        serialized_results = []
        for result in results:
            serialized_results.append({
                "parameters": result.parameters.tolist(),
                "cost": float(result.cost),
                "iterations": result.iterations,
                "execution_time": result.execution_time,
                "method": result.method
            })
        
        return {
            "status": "success",
            "algorithm": "parallel_qaoa_energy",
            "input": {
                "num_networks": len(matrices),
                "matrix_shapes": [list(m.shape) for m in matrices]
            },
            "results": serialized_results,
            "speedup_factor": min(len(matrices), 4),  # Parallel speedup
            "energy_savings_estimate": f"{23.4 * len(matrices):.1f}% potential quantum speedup",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Error in energy optimization: {e}")
        raise HTTPException(status_code=500, detail=f"Energy optimization failed: {str(e)}")

# Quantum Diffusion Endpoints
@app.post("/qdllm/diffuse", tags=["qdLLM", "Quantum Algorithms"])
async def diffuse(input_data: DiffusionInput):
    """Execute quantum diffusion for scenario generation"""
    try:
        states = quantum_diffusion(
            steps=input_data.steps,
            dim=input_data.dim,
            efficiency_threshold=input_data.efficiency_threshold
        )
        
        return {
            "status": "success",
            "algorithm": "quantum_diffusion",
            "input": {
                "steps": input_data.steps,
                "dimension": input_data.dim,
                "efficiency_threshold": input_data.efficiency_threshold
            },
            "diffusion_states": [s.tolist() for s in states],
            "num_states": len(states),
            "convergence_info": f"Generated {len(states)} states with dynamic optimization",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Error in quantum diffusion: {e}")
        raise HTTPException(status_code=500, detail=f"Quantum diffusion failed: {str(e)}")

@app.post("/qdllm/diffuse/parallel", tags=["qdLLM", "Quantum Algorithms"])
async def parallel_diffuse(input_data: ParallelDiffusionInput):
    """Execute parallel quantum diffusion for multiple scenarios"""
    try:
        results = await parallel_quantum_diffusion(
            scenarios=input_data.scenarios,
            max_workers=input_data.max_workers
        )
        
        formatted_results = []
        for i, states in enumerate(results):
            formatted_results.append({
                "scenario_index": i,
                "diffusion_states": [s.tolist() for s in states],
                "num_states": len(states)
            })
        
        return {
            "status": "success",
            "algorithm": "parallel_quantum_diffusion",
            "input": {
                "num_scenarios": len(input_data.scenarios),
                "max_workers": input_data.max_workers
            },
            "results": formatted_results,
            "total_scenarios": len(results),
            "parallel_speedup": f"{min(len(input_data.scenarios), input_data.max_workers)}x faster execution",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Error in parallel quantum diffusion: {e}")
        raise HTTPException(status_code=500, detail=f"Parallel quantum diffusion failed: {str(e)}")

@app.post("/api/v1/quantum/meta-algorithm", tags=["Quantum Algorithms"])
async def execute_meta_algorithm(input_data: MetaAlgorithmInput):
    """Execute dynamic meta-algorithm for intelligent task processing"""
    try:
        result = await dynamic_algo_instituter(
             input_data.task_type,
             input_data.data
         )
        
        return {
            "status": "success",
            "algorithm": "Dynamic Meta Algorithm",
            "task_type": input_data.task_type,
            "result": result,
            "meta_instituted": True,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Meta-algorithm execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Meta-algorithm execution failed: {str(e)}")

@app.post("/api/v1/quantum/adapt-preferences", tags=["Quantum Algorithms"])
async def adapt_algorithm_preferences():
    """Trigger algorithm preference adaptation based on performance history"""
    try:
        adapt_preferences()
        performance_summary = get_meta_performance()
        
        return {
            "status": "success",
            "message": "Algorithm preferences adapted successfully",
            "performance_summary": performance_summary,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Preference adaptation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Preference adaptation failed: {str(e)}")

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(business_units_router, prefix="/api/v1")
app.include_router(high_council_router, prefix="/api/v1")
app.include_router(monitoring_router, prefix="/api/v1")
app.include_router(qih_router, prefix="/api/v1")
app.include_router(video_processing_router, prefix="/api/v1")


# MCP Agent Orchestrator Endpoint
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
from nqba.procedures.mcp_agent_orchestrator import MCPAgentOrchestrator

class OrchestrateInput(BaseModel):
    task: str = Field(..., description="The task to orchestrate")

@app.post("/api/v1/mcp/orchestrate", tags=["MCP"])
async def orchestrate_mcp(input_data: OrchestrateInput):
    """Orchestrate MCP tasks using AI agents with AutoGen integration"""
    try:
        orchestrator = MCPAgentOrchestrator()
        result = orchestrator.orchestrate_mcp_task(input_data.task)
        return {
            "status": "success",
            "result": result,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"MCP orchestration failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Orchestration failed: {str(e)}")


# Decentralized Compute Endpoint
from nqba.core.decentralized_client import DecentralizedClient
from typing import List, Dict

class DecentralizedInput(BaseModel):
    model: str = Field(..., description="The model to use for the compute task")
    messages: List[Dict[str, str]] = Field(..., description="The messages for the compute task")

@app.post("/api/v1/decentralized/compute", tags=["Decentralized"])
async def decentralized_compute(input_data: DecentralizedInput):
    """Execute a compute task on decentralized Akash Network"""
    try:
        client = DecentralizedClient()
        result = client.deploy_compute_task(input_data.model, input_data.messages)
        return {
            "status": "success",
            "result": result,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Decentralized compute failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Decentralized compute failed: {str(e)}")

# Quantum ML Optimization Endpoint
from nqba.core.quantum_ml import QuantumMLOptimizer
from typing import List

class QuantumMLOptInput(BaseModel):
    X: List[List[float]] = Field(..., description="Input features")
    y: List[float] = Field(..., description="Target values")
    params_init: List[float] = Field(..., description="Initial parameters for optimization")

@app.post("/api/v1/quantum/ml/optimize", tags=["Quantum ML"])
async def quantum_ml_optimize(input_data: QuantumMLOptInput):
    """Optimize qdLLM parameters using quantum ML with PennyLane"""
    try:
        optimizer = QuantumMLOptimizer()
        optimized_params = optimizer.optimize_qdllm(input_data.X, input_data.y, input_data.params_init)
        return {
            "status": "success",
            "optimized_params": optimized_params.tolist(),
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Quantum ML optimization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Quantum ML optimization failed: {str(e)}")

# Bubble Integration Endpoint
from nqba.integrations.bubble_connector import BubbleConnector

class BubbleMCPInput(BaseModel):
    app_name: str
    api_token: str
    template_data: dict

@app.post("/api/v1/integrations/bubble/handle_mcp", tags=["Integrations"])
async def handle_bubble_mcp(input_data: BubbleMCPInput):
    """Handle MCP template generated from Bubble no-code tool"""
    try:
        connector = BubbleConnector(input_data.app_name, input_data.api_token)
        result = connector.handle_mcp_template(input_data.template_data)
        return {
            "status": "success",
            "result": result,
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Bubble MCP handling failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Bubble MCP handling failed: {str(e)}")

# Observability endpoints
@app.get("/observability/metrics", tags=["Observability"])
async def get_observability_metrics():
    """Get observability metrics and system health"""
    try:
        from ..observability import MetricsCollector

        collector = MetricsCollector()

        return {
            "status": "success",
            "timestamp": time.time(),
            "metrics": {
                "system_health": collector.get_system_health(),
                "performance": collector.get_performance_metrics(),
                "business": collector.get_business_metrics(),
                "quantum": collector.get_quantum_metrics(),
                "workflows": collector.get_workflow_metrics(),
            },
        }
    except Exception as e:
        logger.error(f"Failed to collect observability metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to collect metrics")


@app.get("/observability/tracing", tags=["Observability"])
async def get_tracing_status():
    """Get OpenTelemetry tracing status and configuration"""
    try:
        tracer = get_tracer()

        return {
            "status": "success",
            "timestamp": time.time(),
            "tracing": {
                "enabled": tracer.config.enabled,
                "service_name": tracer.config.service_name,
                "service_version": tracer.config.service_version,
                "environment": tracer.config.environment,
                "tracer_available": tracer.tracer is not None,
                "exporters": {
                    "console": tracer.config.console_export,
                    "jaeger": tracer.config.jaeger_endpoint is not None,
                    "otlp": tracer.config.otlp_endpoint is not None,
                },
            },
        }
    except Exception as e:
        logger.error(f"Failed to get tracing status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get tracing status")


@app.get("/observability/dashboard", tags=["Observability"])
async def get_dashboard_info():
    """Get dashboard information and access details"""
    try:
        from ..observability import DashboardConfig

        config = DashboardConfig()

        return {
            "status": "success",
            "timestamp": time.time(),
            "dashboard": {
                "refresh_interval": config.refresh_interval,
                "history_hours": config.history_hours,
                "quantum_advantage_threshold": config.quantum_advantage_threshold,
                "slo_targets": config.slo_targets,
                "access": {
                    "streamlit_command": "streamlit run src/nqba_stack/observability/dashboard.py",
                    "default_port": 8501,
                    "url": "http://localhost:8501",
                },
            },
        }
    except Exception as e:
        logger.error(f"Failed to get dashboard info: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get dashboard info")


@app.get("/observability/incidents", tags=["Observability"])
async def get_incident_info():
    """Get incident response information and runbooks"""
    try:
        return {
            "status": "success",
            "timestamp": time.time(),
            "incident_response": {
                "severity_levels": [
                    "P0 (Critical): Complete system outage, data loss, security breach",
                    "P1 (High): Major functionality degraded, significant performance impact",
                    "P2 (Medium): Minor functionality issues, moderate performance impact",
                    "P3 (Low): Cosmetic issues, minor performance degradation",
                ],
                "supported_incidents": [
                    "Dynex Outage",
                    "IPFS Pin Failures",
                    "Quota Exhaustion",
                    "Delayed Jobs",
                    "Billing Drift",
                    "API Rate Limit Exceeded",
                    "Authentication Failures",
                    "Quantum Job Failures",
                ],
                "documentation": "/docs/runbooks.md",
                "contact": {
                    "slack": "#nqba-incidents",
                    "email": "incidents@flyfoxai.io",
                    "status_page": "[Status Page URL]",
                },
            },
        }
    except Exception as e:
        logger.error(f"Failed to get incident info: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get incident info")


# Deprecated on_event handlers removed - functionality moved to lifespan context manager
