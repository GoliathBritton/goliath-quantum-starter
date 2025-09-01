"""
FLYFOX AI Quantum Hub API
FastAPI endpoints for third-party quantum computing integrations
Provides MCP-style access to quantum computing capabilities
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import logging

from ..core.flyfox_quantum_hub import (
    flyfox_quantum_hub,
    QuantumOperation,
    QuantumProvider,
    submit_quantum_request,
    get_request_status,
    register_third_party_integration,
    get_available_providers,
    get_quantum_usage_stats
)

logger = logging.getLogger(__name__)

# Create FastAPI app for quantum hub
quantum_hub_app = FastAPI(
    title="FLYFOX AI Quantum Hub API",
    description="MCP-style quantum computing orchestration and third-party integration platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Security
security = HTTPBearer()

# Pydantic models
class QuantumOptimizationRequest(BaseModel):
    """Quantum optimization request"""
    variables: List[str] = Field(..., description="List of variables to optimize")
    constraints: List[Dict[str, Any]] = Field(default=[], description="Optimization constraints")
    objective_function: str = Field(..., description="Objective function to optimize")
    provider: str = Field(default="dynex", description="Quantum provider to use")
    priority: int = Field(default=1, description="Request priority (1-10)")
    timeout: int = Field(default=300, description="Timeout in seconds")

class QuantumLLMRequest(BaseModel):
    """Quantum LLM request"""
    prompt: str = Field(..., description="Input prompt for quantum LLM")
    max_tokens: int = Field(default=1000, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, description="Sampling temperature")
    provider: str = Field(default="dynex", description="Quantum provider to use")
    priority: int = Field(default=1, description="Request priority (1-10)")

class PortfolioOptimizationRequest(BaseModel):
    """Portfolio optimization request"""
    assets: List[str] = Field(..., description="List of assets")
    returns: List[float] = Field(..., description="Expected returns")
    risk_tolerance: float = Field(..., description="Risk tolerance (0-1)")
    constraints: Dict[str, Any] = Field(default={}, description="Portfolio constraints")
    provider: str = Field(default="dynex", description="Quantum provider to use")
    priority: int = Field(default=1, description="Request priority (1-10)")

class ThirdPartyRegistrationRequest(BaseModel):
    """Third-party integration registration request"""
    client_name: str = Field(..., description="Client company name")
    api_key: str = Field(..., description="API key for authentication")
    allowed_operations: List[str] = Field(..., description="Allowed quantum operations")
    rate_limit_per_hour: int = Field(default=100, description="Rate limit per hour")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for notifications")

class QuantumResponse(BaseModel):
    """Quantum operation response"""
    request_id: str
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

# Authentication dependency
async def authenticate_client(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Authenticate client using API key"""
    api_key = credentials.credentials
    
    # Find client by API key
    for client_id, integration in flyfox_quantum_hub.third_party_integrations.items():
        if integration.api_key == api_key and integration.is_active:
            return client_id
    
    raise HTTPException(status_code=401, detail="Invalid API key")

# API endpoints

@quantum_hub_app.post("/api/v1/quantum/optimize", response_model=QuantumResponse)
async def quantum_optimization(
    request: QuantumOptimizationRequest,
    client_id: str = Depends(authenticate_client)
):
    """Submit quantum optimization request"""
    try:
        # Convert provider string to enum
        provider_enum = QuantumProvider(request.provider)
        
        # Prepare parameters
        parameters = {
            "variables": request.variables,
            "constraints": request.constraints,
            "objective_function": request.objective_function
        }
        
        # Submit quantum request
        request_id = await submit_quantum_request(
            client_id=client_id,
            operation_type=QuantumOperation.OPTIMIZATION,
            provider=provider_enum,
            parameters=parameters,
            priority=request.priority,
            timeout=request.timeout
        )
        
        return QuantumResponse(
            request_id=request_id,
            status="submitted",
            message="Quantum optimization request submitted successfully",
            data={"request_id": request_id}
        )
        
    except Exception as e:
        logger.error(f"Quantum optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Quantum optimization failed: {str(e)}")

@quantum_hub_app.post("/api/v1/quantum/llm", response_model=QuantumResponse)
async def quantum_llm(
    request: QuantumLLMRequest,
    client_id: str = Depends(authenticate_client)
):
    """Submit quantum LLM request"""
    try:
        # Convert provider string to enum
        provider_enum = QuantumProvider(request.provider)
        
        # Prepare parameters
        parameters = {
            "prompt": request.prompt,
            "max_tokens": request.max_tokens,
            "temperature": request.temperature
        }
        
        # Submit quantum request
        request_id = await submit_quantum_request(
            client_id=client_id,
            operation_type=QuantumOperation.QUANTUM_LLM,
            provider=provider_enum,
            parameters=parameters,
            priority=request.priority
        )
        
        return QuantumResponse(
            request_id=request_id,
            status="submitted",
            message="Quantum LLM request submitted successfully",
            data={"request_id": request_id}
        )
        
    except Exception as e:
        logger.error(f"Quantum LLM request failed: {e}")
        raise HTTPException(status_code=500, detail=f"Quantum LLM request failed: {str(e)}")

@quantum_hub_app.post("/api/v1/quantum/portfolio-optimize", response_model=QuantumResponse)
async def portfolio_optimization(
    request: PortfolioOptimizationRequest,
    client_id: str = Depends(authenticate_client)
):
    """Submit portfolio optimization request"""
    try:
        # Convert provider string to enum
        provider_enum = QuantumProvider(request.provider)
        
        # Prepare parameters
        parameters = {
            "assets": request.assets,
            "returns": request.returns,
            "risk_tolerance": request.risk_tolerance,
            "constraints": request.constraints
        }
        
        # Submit quantum request
        request_id = await submit_quantum_request(
            client_id=client_id,
            operation_type=QuantumOperation.PORTFOLIO_OPTIMIZATION,
            provider=provider_enum,
            parameters=parameters,
            priority=request.priority
        )
        
        return QuantumResponse(
            request_id=request_id,
            status="submitted",
            message="Portfolio optimization request submitted successfully",
            data={"request_id": request_id}
        )
        
    except Exception as e:
        logger.error(f"Portfolio optimization failed: {e}")
        raise HTTPException(status_code=500, detail=f"Portfolio optimization failed: {str(e)}")

@quantum_hub_app.get("/api/v1/quantum/status/{request_id}")
async def get_quantum_status(
    request_id: str,
    client_id: str = Depends(authenticate_client)
):
    """Get status of quantum operation"""
    try:
        status = await get_request_status(request_id)
        
        # Verify client owns this request
        if status.get("client_id") != client_id:
            raise HTTPException(status_code=403, detail="Access denied to this request")
        
        return status
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to get quantum status: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get quantum status: {str(e)}")

@quantum_hub_app.get("/api/v1/quantum/providers")
async def get_quantum_providers():
    """Get available quantum providers"""
    try:
        providers = await get_available_providers()
        return {
            "providers": providers,
            "total_providers": len(providers)
        }
        
    except Exception as e:
        logger.error(f"Failed to get quantum providers: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get quantum providers: {str(e)}")

@quantum_hub_app.post("/api/v1/quantum/register")
async def register_third_party(
    request: ThirdPartyRegistrationRequest
):
    """Register third-party integration"""
    try:
        # Convert operation strings to enums
        allowed_operations = []
        for op_str in request.allowed_operations:
            try:
                allowed_operations.append(QuantumOperation(op_str))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid operation: {op_str}")
        
        # Register integration
        client_id = await register_third_party_integration(
            client_name=request.client_name,
            api_key=request.api_key,
            allowed_operations=allowed_operations,
            rate_limit_per_hour=request.rate_limit_per_hour,
            webhook_url=request.webhook_url
        )
        
        return {
            "client_id": client_id,
            "status": "registered",
            "message": "Third-party integration registered successfully",
            "allowed_operations": request.allowed_operations,
            "rate_limit_per_hour": request.rate_limit_per_hour
        }
        
    except Exception as e:
        logger.error(f"Third-party registration failed: {e}")
        raise HTTPException(status_code=500, detail=f"Third-party registration failed: {str(e)}")

@quantum_hub_app.get("/api/v1/quantum/usage/{client_id}")
async def get_quantum_usage(
    client_id: str,
    authenticated_client_id: str = Depends(authenticate_client)
):
    """Get quantum usage statistics"""
    try:
        # Verify client is requesting their own stats
        if client_id != authenticated_client_id:
            raise HTTPException(status_code=403, detail="Access denied to this client's stats")
        
        usage_stats = await get_quantum_usage_stats(client_id)
        return usage_stats
        
    except Exception as e:
        logger.error(f"Failed to get quantum usage: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get quantum usage: {str(e)}")

@quantum_hub_app.get("/api/v1/quantum/health")
async def quantum_hub_health():
    """Health check for quantum hub"""
    return {
        "status": "healthy",
        "service": "FLYFOX AI Quantum Hub",
        "version": "1.0.0",
        "providers_configured": len(flyfox_quantum_hub.provider_configs),
        "active_integrations": len([
            integration for integration in flyfox_quantum_hub.third_party_integrations.values()
            if integration.is_active
        ]),
        "pending_requests": len([
            req for req in flyfox_quantum_hub.quantum_requests.values()
            if req.status.value == "pending"
        ])
    }

@quantum_hub_app.get("/")
async def quantum_hub_root():
    """Root endpoint with API information"""
    return {
        "service": "FLYFOX AI Quantum Hub",
        "description": "MCP-style quantum computing orchestration and third-party integration platform",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "quantum_optimization": "POST /api/v1/quantum/optimize",
            "quantum_llm": "POST /api/v1/quantum/llm",
            "portfolio_optimization": "POST /api/v1/quantum/portfolio-optimize",
            "get_status": "GET /api/v1/quantum/status/{request_id}",
            "get_providers": "GET /api/v1/quantum/providers",
            "register": "POST /api/v1/quantum/register",
            "get_usage": "GET /api/v1/quantum/usage/{client_id}",
            "health": "GET /api/v1/quantum/health"
        },
        "supported_operations": [
            "optimization",
            "simulation", 
            "machine_learning",
            "cryptography",
            "quantum_llm",
            "portfolio_optimization",
            "risk_assessment",
            "process_optimization"
        ],
        "supported_providers": [
            "dynex",
            "ibm_q",
            "google_quantum",
            "microsoft_azure",
            "custom"
        ]
    }
