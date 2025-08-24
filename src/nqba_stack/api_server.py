"""
NQBA API Server - FastAPI-based REST API

This module provides a REST API interface to the NQBA platform,
exposing quantum computing, decision logic, and LTC logging capabilities.
"""

import asyncio
import logging
import time
import uuid
from datetime import datetime
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import numpy as np

# Import NQBA components
from .quantum_adapter import QuantumAdapter, OptimizationResult
from .decision_logic import DecisionLogicEngine, DecisionContext, DecisionType
from .ltc_logger import LTCLogger, LTCConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="NQBA API Server",
    description="Neuromorphic Quantum Base Architecture API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
quantum_adapter: Optional[QuantumAdapter] = None
decision_engine: Optional[DecisionLogicEngine] = None
ltc_logger: Optional[LTCLogger] = None

# Pydantic models for API requests/responses
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    components: Dict[str, str]

class OptimizationRequest(BaseModel):
    problem_type: str = Field(..., description="Type of optimization problem (e.g., 'qubo', 'ising')")
    matrix: List[List[float]] = Field(..., description="Problem matrix")
    algorithm: Optional[str] = Field("qaoa", description="Optimization algorithm to use")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Additional algorithm parameters")
    user_id: Optional[str] = Field(None, description="User ID for tracking")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")

class OptimizationResponse(BaseModel):
    success: bool
    entry_id: str
    optimal_value: Optional[float] = None
    solution_vector: Optional[List[int]] = None
    execution_time: float
    backend_used: str
    algorithm: str
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class DecisionRequest(BaseModel):
    decision_type: str = Field(..., description="Type of decision to make")
    business_context: str = Field(..., description="Business context for the decision")
    data: Optional[Dict[str, Any]] = Field(None, description="Data for decision making")
    user_id: Optional[str] = Field(None, description="User ID for tracking")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")
    priority: str = Field("normal", description="Decision priority")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Decision constraints")

class DecisionResponse(BaseModel):
    success: bool
    entry_id: str
    decision_type: str
    strategy_selected: str
    reasoning: str
    confidence_score: float
    execution_time: float
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

class CircuitRequest(BaseModel):
    qubits: int = Field(..., description="Number of qubits")
    gates: List[Dict[str, Any]] = Field(..., description="Quantum gates to apply")
    backend: Optional[str] = Field(None, description="Specific backend to use")
    user_id: Optional[str] = Field(None, description="User ID for tracking")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")

class CircuitResponse(BaseModel):
    success: bool
    entry_id: str
    result_data: Optional[Dict[str, Any]] = None
    qubits_used: int
    execution_time: float
    backend_used: str
    error_message: Optional[str] = None

class LTCSearchRequest(BaseModel):
    operation_type: Optional[str] = Field(None, description="Filter by operation type")
    component: Optional[str] = Field(None, description="Filter by component")
    user_id: Optional[str] = Field(None, description="Filter by user ID")
    session_id: Optional[str] = Field(None, description="Filter by session ID")
    limit: int = Field(100, description="Maximum number of results")

class LTCSearchResponse(BaseModel):
    success: bool
    entries: List[Dict[str, Any]]
    total_found: int
    search_criteria: Dict[str, Any]

class AgentInteractionRequest(BaseModel):
    agent_type: str = Field(..., description="Type of agent (chatbot, voice, digital_human)")
    interaction_type: str = Field(..., description="Type of interaction")
    user_input: str = Field(..., description="User input")
    user_id: Optional[str] = Field(None, description="User ID for tracking")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")

class AgentInteractionResponse(BaseModel):
    success: bool
    entry_id: str
    agent_response: str
    processing_time: float
    metadata: Optional[Dict[str, Any]] = None

# Dependency functions
async def get_quantum_adapter() -> QuantumAdapter:
    """Get quantum adapter instance"""
    if quantum_adapter is None:
        raise HTTPException(status_code=503, detail="Quantum adapter not initialized")
    return quantum_adapter

async def get_decision_engine() -> DecisionLogicEngine:
    """Get decision engine instance"""
    if decision_engine is None:
        raise HTTPException(status_code=503, detail="Decision engine not initialized")
    return decision_engine

async def get_ltc_logger() -> LTCLogger:
    """Get LTC logger instance"""
    if ltc_logger is None:
        raise HTTPException(status_code=503, detail="LTC logger not initialized")
    return ltc_logger

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize NQBA components on startup"""
    global quantum_adapter, decision_engine, ltc_logger
    
    try:
        logger.info("Initializing NQBA components...")
        
        # Initialize LTC logger
        ltc_config = LTCConfig(
            storage_path="./ltc_storage",
            async_writing=True
        )
        ltc_logger = LTCLogger(ltc_config)
        
        # Initialize quantum adapter
        quantum_adapter = QuantumAdapter(
            preferred_backend="dynex",
            max_qubits=64,
            enable_fallback=True
        )
        
        # Initialize decision engine
        decision_engine = DecisionLogicEngine(
            max_qubits=64,
            enable_optimization=True,
            rule_engine_enabled=True
        )
        
        logger.info("NQBA components initialized successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize NQBA components: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup NQBA components on shutdown"""
    global ltc_logger
    
    if ltc_logger:
        ltc_logger.shutdown()
        logger.info("LTC logger shutdown complete")

# Health check endpoints
@app.get("/healthz", response_model=HealthResponse)
async def health_check():
    """Basic health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        components={
            "quantum_adapter": "available" if quantum_adapter else "unavailable",
            "decision_engine": "available" if decision_engine else "unavailable",
            "ltc_logger": "available" if ltc_logger else "unavailable"
        }
    )

@app.get("/healthz/detailed")
async def detailed_health_check():
    """Detailed health check with component status"""
    try:
        # Get component statuses
        quantum_status = {}
        if quantum_adapter:
            quantum_status = quantum_adapter.get_backend_status()
        
        decision_status = {}
        if decision_engine:
            decision_status = {
                "business_rules": len(decision_engine.get_business_rules()),
                "optimization_strategies": len(decision_engine.get_optimization_strategies())
            }
        
        ltc_status = {}
        if ltc_logger:
            ltc_status = ltc_logger.get_statistics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "components": {
                "quantum_adapter": {
                    "status": "available" if quantum_adapter else "unavailable",
                    "details": quantum_status
                },
                "decision_engine": {
                    "status": "available" if decision_engine else "unavailable",
                    "details": decision_status
                },
                "ltc_logger": {
                    "status": "available" if ltc_logger else "unavailable",
                    "details": ltc_status
                }
            }
        }
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Quantum optimization endpoint
@app.post("/v1/optimize", response_model=OptimizationResponse)
async def optimize_problem(
    request: OptimizationRequest,
    background_tasks: BackgroundTasks,
    adapter: QuantumAdapter = Depends(get_quantum_adapter),
    ltc: LTCLogger = Depends(get_ltc_logger)
):
    """Optimize a problem using quantum computing"""
    
    start_time = time.time()
    
    try:
        # Convert matrix to numpy array
        matrix = np.array(request.matrix)
        
        # Log the optimization request
        entry_id = await ltc.log_operation(
            operation_type="optimization_request",
            component="api_server",
            user_id=request.user_id,
            session_id=request.session_id,
            input_data={
                "problem_type": request.problem_type,
                "matrix_size": matrix.shape,
                "algorithm": request.algorithm
            }
        )
        
        # Execute optimization
        result = await adapter.optimize_qubo(
            matrix=matrix,
            algorithm=request.algorithm or "qaoa",
            parameters=request.parameters
        )
        
        execution_time = time.time() - start_time
        
        # Log the optimization result
        await ltc.log_quantum_execution(
            operation="qubo_optimization",
            qubits=matrix.shape[0],
            backend=result.backend_used,
            execution_time=execution_time,
            success=result.success,
            user_id=request.user_id,
            session_id=request.session_id,
            parent_entry_id=entry_id
        )
        
        return OptimizationResponse(
            success=result.success,
            entry_id=entry_id,
            optimal_value=result.optimal_value,
            solution_vector=result.solution_vector,
            execution_time=execution_time,
            backend_used=result.backend_used,
            algorithm=result.algorithm,
            metadata=result.metadata,
            error_message=result.error_message
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Optimization failed: {e}")
        
        # Log the error
        if ltc:
            await ltc.log_operation(
                operation_type="optimization_error",
                component="api_server",
                user_id=request.user_id,
                session_id=request.session_id,
                error_data={"error": str(e)},
                performance_metrics={"execution_time": execution_time}
            )
        
        raise HTTPException(status_code=500, detail=f"Optimization failed: {str(e)}")

# Decision making endpoint
@app.post("/v1/decide", response_model=DecisionResponse)
async def make_decision(
    request: DecisionRequest,
    background_tasks: BackgroundTasks,
    engine: DecisionLogicEngine = Depends(get_decision_engine),
    ltc: LTCLogger = Depends(get_ltc_logger)
):
    """Make a decision using the decision logic engine"""
    
    start_time = time.time()
    
    try:
        # Create decision context
        context = DecisionContext(
            user_id=request.user_id or "anonymous",
            session_id=request.session_id or str(uuid.uuid4()),
            business_context=request.business_context,
            priority=request.priority,
            constraints=request.constraints
        )
        
        # Log the decision request
        entry_id = await ltc.log_operation(
            operation_type="decision_request",
            component="api_server",
            user_id=request.user_id,
            session_id=request.session_id,
            input_data={
                "decision_type": request.decision_type,
                "business_context": request.business_context,
                "data": request.data
            }
        )
        
        # Make decision
        decision_type = DecisionType(request.decision_type)
        result = await engine.make_decision(
            decision_type=decision_type,
            context=context,
            data=request.data
        )
        
        execution_time = time.time() - start_time
        
        # Log the decision result
        await ltc.log_decision_making(
            decision_type=result.decision_type,
            strategy_selected=result.strategy_selected,
            confidence_score=result.confidence_score,
            reasoning=result.reasoning,
            user_id=request.user_id,
            session_id=request.session_id,
            parent_entry_id=entry_id
        )
        
        return DecisionResponse(
            success=result.success,
            entry_id=entry_id,
            decision_type=result.decision_type,
            strategy_selected=result.strategy_selected,
            reasoning=result.reasoning,
            confidence_score=result.confidence_score,
            execution_time=execution_time,
            metadata=result.metadata,
            error_message=result.error_message
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Decision making failed: {e}")
        
        # Log the error
        if ltc:
            await ltc.log_operation(
                operation_type="decision_error",
                component="api_server",
                user_id=request.user_id,
                session_id=request.session_id,
                error_data={"error": str(e)},
                performance_metrics={"execution_time": execution_time}
            )
        
        raise HTTPException(status_code=500, detail=f"Decision making failed: {str(e)}")

# Quantum circuit execution endpoint
@app.post("/v1/circuit", response_model=CircuitResponse)
async def execute_circuit(
    request: CircuitRequest,
    background_tasks: BackgroundTasks,
    adapter: QuantumAdapter = Depends(get_quantum_adapter),
    ltc: LTCLogger = Depends(get_ltc_logger)
):
    """Execute a quantum circuit"""
    
    start_time = time.time()
    
    try:
        # Create circuit specification
        circuit_spec = {
            "qubits": request.qubits,
            "gates": request.gates
        }
        
        # Log the circuit execution request
        entry_id = await ltc.log_operation(
            operation_type="circuit_execution_request",
            component="api_server",
            user_id=request.user_id,
            session_id=request.session_id,
            input_data=circuit_spec
        )
        
        # Execute circuit
        result = await adapter.execute_circuit(
            circuit_spec=circuit_spec,
            backend=request.backend
        )
        
        execution_time = time.time() - start_time
        
        # Log the circuit execution result
        await ltc.log_quantum_execution(
            operation="circuit_execution",
            qubits=result.qubits_used,
            backend=result.backend_used,
            execution_time=execution_time,
            success=result.success,
            user_id=request.user_id,
            session_id=request.session_id,
            parent_entry_id=entry_id
        )
        
        return CircuitResponse(
            success=result.success,
            entry_id=entry_id,
            result_data=result.result_data,
            qubits_used=result.qubits_used,
            execution_time=execution_time,
            backend_used=result.backend_used,
            error_message=result.error_message
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        logger.error(f"Circuit execution failed: {e}")
        
        # Log the error
        if ltc:
            await ltc.log_operation(
                operation_type="circuit_execution_error",
                component="api_server",
                user_id=request.user_id,
                session_id=request.session_id,
                error_data={"error": str(e)},
                performance_metrics={"execution_time": execution_time}
            )
        
        raise HTTPException(status_code=500, detail=f"Circuit execution failed: {str(e)}")

# LTC search endpoint
@app.post("/v1/ltc/search", response_model=LTCSearchResponse)
async def search_ltc(
    request: LTCSearchRequest,
    ltc: LTCLogger = Depends(get_ltc_logger)
):
    """Search LTC entries"""
    
    try:
        # Search entries
        entries = await ltc.search_entries(
            operation_type=request.operation_type,
            component=request.component,
            user_id=request.user_id,
            session_id=request.session_id,
            limit=request.limit
        )
        
        # Convert entries to dictionaries
        entry_dicts = []
        for entry in entries:
            entry_dict = {
                "entry_id": entry.entry_id,
                "timestamp": entry.timestamp,
                "operation_type": entry.operation_type,
                "component": entry.component,
                "user_id": entry.user_id,
                "session_id": entry.session_id,
                "input_data": entry.input_data,
                "result_data": entry.result_data,
                "performance_metrics": entry.performance_metrics,
                "metadata": entry.metadata
            }
            entry_dicts.append(entry_dict)
        
        return LTCSearchResponse(
            success=True,
            entries=entry_dicts,
            total_found=len(entries),
            search_criteria={
                "operation_type": request.operation_type,
                "component": request.component,
                "user_id": request.user_id,
                "session_id": request.session_id,
                "limit": request.limit
            }
        )
        
    except Exception as e:
        logger.error(f"LTC search failed: {e}")
        raise HTTPException(status_code=500, detail=f"LTC search failed: {str(e)}")

# Agent interaction endpoint
@app.post("/v1/agent/interact", response_model=AgentInteractionResponse)
async def agent_interaction(
    request: AgentInteractionRequest,
    background_tasks: BackgroundTasks,
    ltc: LTCLogger = Depends(get_ltc_logger)
):
    """Log AI agent interaction"""
    
    start_time = time.time()
    
    try:
        # Simple agent response (placeholder for actual agent logic)
        if request.agent_type == "chatbot":
            response = f"Chatbot response to: {request.user_input[:50]}..."
        elif request.agent_type == "voice":
            response = f"Voice agent response to: {request.user_input[:50]}..."
        elif request.agent_type == "digital_human":
            response = f"Digital human response to: {request.user_input[:50]}..."
        else:
            response = f"Unknown agent type: {request.agent_type}"
        
        processing_time = time.time() - start_time
        
        # Log the agent interaction
        entry_id = await ltc.log_agent_interaction(
            agent_type=request.agent_type,
            interaction_type=request.interaction_type,
            user_input=request.user_input,
            agent_response=response,
            processing_time=processing_time,
            user_id=request.user_id,
            session_id=request.session_id
        )
        
        return AgentInteractionResponse(
            success=True,
            entry_id=entry_id,
            agent_response=response,
            processing_time=processing_time,
            metadata={
                "agent_type": request.agent_type,
                "interaction_type": request.interaction_type
            }
        )
        
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Agent interaction failed: {e}")
        
        # Log the error
        if ltc:
            await ltc.log_operation(
                operation_type="agent_interaction_error",
                component="api_server",
                user_id=request.user_id,
                session_id=request.session_id,
                error_data={"error": str(e)},
                performance_metrics={"processing_time": processing_time}
            )
        
        raise HTTPException(status_code=500, detail=f"Agent interaction failed: {str(e)}")

# Metrics endpoint
@app.get("/v1/metrics")
async def get_metrics(ltc: LTCLogger = Depends(get_ltc_logger)):
    """Get system metrics"""
    
    try:
        # Get LTC statistics
        ltc_stats = ltc.get_statistics()
        
        # Get component statuses
        quantum_status = {}
        if quantum_adapter:
            quantum_status = quantum_adapter.get_backend_status()
        
        decision_status = {}
        if decision_engine:
            decision_status = {
                "business_rules": len(decision_engine.get_business_rules()),
                "optimization_strategies": len(decision_engine.get_optimization_strategies())
            }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "ltc_statistics": ltc_stats,
            "quantum_adapter": quantum_status,
            "decision_engine": decision_status,
            "system": {
                "uptime": "N/A",  # Would calculate actual uptime
                "memory_usage": "N/A",  # Would get actual memory usage
                "cpu_usage": "N/A"  # Would get actual CPU usage
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to get metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "NQBA API Server",
        "version": "1.0.0",
        "description": "Neuromorphic Quantum Base Architecture API",
        "endpoints": {
            "health": "/healthz",
            "optimization": "/v1/optimize",
            "decision": "/v1/decide",
            "circuit": "/v1/circuit",
            "ltc_search": "/v1/ltc/search",
            "agent_interaction": "/v1/agent/interact",
            "metrics": "/v1/metrics"
        },
        "documentation": "/docs"
    }

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
