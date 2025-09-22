from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio
import logging
import uuid

# Import agent implementations
sys.path.append('../agents')
from chat_agent.quantum_chat_agent import QuantumChatAgent, ConversationMode
from calling_agent.quantum_calling_agent import QuantumCallingAgent, CallType

# Import core services
sys.path.append('../core')
from quantum_job_manager import QuantumJobManager
from qdllm_service import QdLLMService
from qhc_governance import QHCGovernance
from mcp_integration import MCPProvider

# Pydantic models for API requests/responses
class ConversationRequest(BaseModel):
    session_id: str
    text: str
    context: Optional[Dict[str, Any]] = None
    mode: str = "standard"

class ConversationResponse(BaseModel):
    session_id: str
    response: str
    confidence: float
    reasoning_trace: Dict[str, Any]
    suggested_actions: List[str]
    escalation_recommended: bool
    metadata: Dict[str, Any]

class EscalationRequest(BaseModel):
    session_id: str
    reason: str
    metadata: Optional[Dict[str, Any]] = None

class CallStartRequest(BaseModel):
    phone: str
    lead_id: Optional[str] = None
    script_id: Optional[str] = None
    call_type: str = "outbound_sales"
    metadata: Optional[Dict[str, Any]] = None

class CallHandoffRequest(BaseModel):
    session_id: str
    human_agent_id: str
    reason: Optional[str] = None

class AgentStatusResponse(BaseModel):
    agent_id: str
    status: str
    active_sessions: int
    capabilities: Dict[str, bool]
    uptime: str
    performance_metrics: Dict[str, Any]

class PodCreateRequest(BaseModel):
    agents_count: int = Field(ge=1, le=10)
    target_segment: str
    mission_parameters: Dict[str, Any]
    priority: str = "medium"

class PodMetricsResponse(BaseModel):
    pod_id: str
    agents: List[Dict[str, Any]]
    performance_metrics: Dict[str, Any]
    active_sessions: int
    total_interactions: int
    success_rate: float

# FastAPI app initialization
app = FastAPI(
    title="Quantum Agents API",
    description="FLYFOX AI Quantum Agent Platform - Chat, Calling, and Business Agents",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Global services (would be dependency injected in production)
quantum_job_manager: QuantumJobManager = None
qdllm_service: QdLLMService = None
qhc_governance: QHCGovernance = None
mcp_provider: MCPProvider = None

# Agent instances
chat_agents: Dict[str, QuantumChatAgent] = {}
calling_agents: Dict[str, QuantumCallingAgent] = {}
sales_pods: Dict[str, Dict] = {}

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Dependency functions
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate JWT token and return user info"""
    # In production, implement proper JWT validation
    # For now, return mock user
    return {
        "user_id": "user123",
        "permissions": ["agent_access", "pod_management"],
        "organization": "flyfox_ai"
    }

async def get_chat_agent(agent_id: str) -> QuantumChatAgent:
    """Get or create chat agent instance"""
    if agent_id not in chat_agents:
        agent = QuantumChatAgent(
            agent_id=agent_id,
            quantum_job_manager=quantum_job_manager,
            qdllm_service=qdllm_service,
            qhc_governance=qhc_governance,
            mcp_provider=mcp_provider
        )
        await agent.initialize()
        chat_agents[agent_id] = agent
    
    return chat_agents[agent_id]

async def get_calling_agent(agent_id: str) -> QuantumCallingAgent:
    """Get or create calling agent instance"""
    if agent_id not in calling_agents:
        # Initialize Twilio client (would be configured properly)
        from twilio.rest import Client as TwilioClient
        twilio_client = TwilioClient("account_sid", "auth_token")
        
        agent = QuantumCallingAgent(
            agent_id=agent_id,
            quantum_job_manager=quantum_job_manager,
            qdllm_service=qdllm_service,
            qhc_governance=qhc_governance,
            mcp_provider=mcp_provider,
            twilio_client=twilio_client
        )
        await agent.initialize()
        calling_agents[agent_id] = agent
    
    return calling_agents[agent_id]

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global quantum_job_manager, qdllm_service, qhc_governance, mcp_provider
    
    logger.info("Initializing Quantum Agents API...")
    
    # Initialize core services
    quantum_job_manager = QuantumJobManager()
    await quantum_job_manager.initialize()
    
    qdllm_service = QdLLMService()
    await qdllm_service.initialize()
    
    qhc_governance = QHCGovernance()
    await qhc_governance.initialize()
    
    mcp_provider = MCPProvider()
    await mcp_provider.initialize()
    
    logger.info("Quantum Agents API initialized successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Quantum Agents API...")
    
    # Close all agent connections
    for agent in chat_agents.values():
        # Implement cleanup if needed
        pass
    
    for agent in calling_agents.values():
        # Implement cleanup if needed
        pass
    
    # Close core services
    if quantum_job_manager:
        await quantum_job_manager.close()
    
    logger.info("Quantum Agents API shutdown complete")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "quantum_job_manager": "active" if quantum_job_manager else "inactive",
            "qdllm_service": "active" if qdllm_service else "inactive",
            "qhc_governance": "active" if qhc_governance else "inactive",
            "mcp_provider": "active" if mcp_provider else "inactive"
        },
        "active_agents": {
            "chat_agents": len(chat_agents),
            "calling_agents": len(calling_agents),
            "sales_pods": len(sales_pods)
        }
    }

# ============================================================================
# QUANTUM CHAT AGENT ENDPOINTS
# ============================================================================

@app.post("/api/agents/{agent_id}/converse", response_model=ConversationResponse)
async def chat_converse(
    agent_id: str,
    request: ConversationRequest,
    user: Dict = Depends(get_current_user)
):
    """Chat with quantum-enhanced agent"""
    try:
        agent = await get_chat_agent(agent_id)
        
        # Convert mode string to enum
        mode = ConversationMode(request.mode.lower())
        
        result = await agent.converse(
            session_id=request.session_id,
            text=request.text,
            context=request.context,
            mode=mode
        )
        
        return ConversationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid mode: {request.mode}")
    except Exception as e:
        logger.error(f"Chat conversation error: {e}")
        raise HTTPException(status_code=500, detail="Conversation processing failed")

@app.post("/api/agents/{agent_id}/escalate")
async def chat_escalate(
    agent_id: str,
    request: EscalationRequest,
    user: Dict = Depends(get_current_user)
):
    """Escalate chat conversation to human agent"""
    try:
        agent = await get_chat_agent(agent_id)
        
        result = await agent.escalate(
            session_id=request.session_id,
            reason=request.reason,
            metadata=request.metadata
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Chat escalation error: {e}")
        raise HTTPException(status_code=500, detail="Escalation processing failed")

@app.get("/api/agents/{agent_id}/status", response_model=AgentStatusResponse)
async def get_chat_agent_status(
    agent_id: str,
    user: Dict = Depends(get_current_user)
):
    """Get chat agent status and metrics"""
    try:
        agent = await get_chat_agent(agent_id)
        status = await agent.get_agent_status()
        
        return AgentStatusResponse(**status)
        
    except Exception as e:
        logger.error(f"Agent status error: {e}")
        raise HTTPException(status_code=500, detail="Status retrieval failed")

# ============================================================================
# QUANTUM CALLING AGENT ENDPOINTS
# ============================================================================

@app.post("/api/agents/{agent_id}/call-start")
async def start_call(
    agent_id: str,
    request: CallStartRequest,
    user: Dict = Depends(get_current_user)
):
    """Start outbound call with quantum calling agent"""
    try:
        agent = await get_calling_agent(agent_id)
        
        # Convert call type string to enum
        call_type = CallType(request.call_type.lower())
        
        result = await agent.start_call(
            phone=request.phone,
            lead_id=request.lead_id,
            script_id=request.script_id,
            call_type=call_type,
            metadata=request.metadata
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid call type: {request.call_type}")
    except Exception as e:
        logger.error(f"Call start error: {e}")
        raise HTTPException(status_code=500, detail="Call initiation failed")

@app.post("/api/agents/{agent_id}/call-handoff")
async def handoff_call(
    agent_id: str,
    request: CallHandoffRequest,
    user: Dict = Depends(get_current_user)
):
    """Hand off call to human agent"""
    try:
        agent = await get_calling_agent(agent_id)
        
        result = await agent.handoff_to_human(
            call_id=request.session_id,  # Using session_id as call_id
            human_agent_id=request.human_agent_id,
            reason=request.reason
        )
        
        return result
        
    except Exception as e:
        logger.error(f"Call handoff error: {e}")
        raise HTTPException(status_code=500, detail="Call handoff failed")

@app.post("/api/agents/{agent_id}/postcall-summary")
async def generate_postcall_summary(
    agent_id: str,
    call_id: str,
    user: Dict = Depends(get_current_user)
):
    """Generate post-call summary and analysis"""
    try:
        agent = await get_calling_agent(agent_id)
        
        result = await agent.generate_postcall_summary(call_id)
        
        return result
        
    except Exception as e:
        logger.error(f"Post-call summary error: {e}")
        raise HTTPException(status_code=500, detail="Summary generation failed")

@app.get("/api/agents/{agent_id}/call-status/{call_id}")
async def get_call_status(
    agent_id: str,
    call_id: str,
    user: Dict = Depends(get_current_user)
):
    """Get current call status"""
    try:
        agent = await get_calling_agent(agent_id)
        
        result = await agent.get_call_status(call_id)
        
        return result
        
    except Exception as e:
        logger.error(f"Call status error: {e}")
        raise HTTPException(status_code=500, detail="Status retrieval failed")

# ============================================================================
# TWILIO WEBHOOK ENDPOINTS
# ============================================================================

@app.post("/api/calling/voice/handle/{call_id}")
async def handle_voice_webhook(
    call_id: str,
    request_data: Dict[str, Any]
):
    """Handle Twilio voice webhook"""
    try:
        # Find the agent handling this call
        agent = None
        for calling_agent in calling_agents.values():
            if call_id in calling_agent.active_calls:
                agent = calling_agent
                break
        
        if not agent:
            logger.error(f"No agent found for call {call_id}")
            return "<?xml version='1.0' encoding='UTF-8'?><Response><Say>Call session not found</Say><Hangup/></Response>"
        
        twiml_response = await agent.handle_voice_webhook(call_id, request_data)
        
        return twiml_response
        
    except Exception as e:
        logger.error(f"Voice webhook error: {e}")
        return "<?xml version='1.0' encoding='UTF-8'?><Response><Say>Processing error</Say><Hangup/></Response>"

@app.post("/api/calling/voice/speech/{call_id}")
async def handle_speech_webhook(
    call_id: str,
    speech_data: Dict[str, Any]
):
    """Handle Twilio speech recognition webhook"""
    try:
        # Find the agent handling this call
        agent = None
        for calling_agent in calling_agents.values():
            if call_id in calling_agent.active_calls:
                agent = calling_agent
                break
        
        if not agent:
            logger.error(f"No agent found for call {call_id}")
            return "<?xml version='1.0' encoding='UTF-8'?><Response><Say>Call session not found</Say><Hangup/></Response>"
        
        twiml_response = await agent.handle_speech_input(call_id, speech_data)
        
        return twiml_response
        
    except Exception as e:
        logger.error(f"Speech webhook error: {e}")
        return "<?xml version='1.0' encoding='UTF-8'?><Response><Say>Speech processing error</Say><Hangup/></Response>"

@app.post("/api/calling/voice/status/{call_id}")
async def handle_status_webhook(
    call_id: str,
    status_data: Dict[str, Any]
):
    """Handle Twilio call status webhook"""
    try:
        # Update call status in relevant agent
        for calling_agent in calling_agents.values():
            if call_id in calling_agent.active_calls:
                call_session = calling_agent.active_calls[call_id]
                
                # Update status based on Twilio callback
                twilio_status = status_data.get("CallStatus")
                if twilio_status == "completed":
                    call_session.status = CallStatus.COMPLETED
                    call_session.ended_at = datetime.utcnow()
                elif twilio_status == "failed":
                    call_session.status = CallStatus.FAILED
                    call_session.ended_at = datetime.utcnow()
                elif twilio_status == "no-answer":
                    call_session.status = CallStatus.NO_ANSWER
                    call_session.ended_at = datetime.utcnow()
                elif twilio_status == "busy":
                    call_session.status = CallStatus.BUSY
                    call_session.ended_at = datetime.utcnow()
                
                logger.info(f"Call {call_id} status updated to {call_session.status.value}")
                break
        
        return {"status": "received"}
        
    except Exception as e:
        logger.error(f"Status webhook error: {e}")
        return {"status": "error", "message": str(e)}

# ============================================================================
# Q-SALES POD MANAGEMENT ENDPOINTS
# ============================================================================

@app.post("/api/pods", response_model=Dict[str, Any])
async def create_sales_pod(
    request: PodCreateRequest,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(get_current_user)
):
    """Create and deploy Q-Sales pod with multiple agents"""
    try:
        pod_id = str(uuid.uuid4())
        
        # Create pod configuration
        pod_config = {
            "pod_id": pod_id,
            "agents_count": request.agents_count,
            "target_segment": request.target_segment,
            "mission_parameters": request.mission_parameters,
            "priority": request.priority,
            "created_at": datetime.utcnow().isoformat(),
            "created_by": user["user_id"],
            "status": "initializing",
            "agents": []
        }
        
        # Create agents for the pod
        for i in range(request.agents_count):
            agent_id = f"pod-{pod_id}-agent-{i}"
            
            # Determine agent type based on mission parameters
            agent_type = request.mission_parameters.get("primary_channel", "chat")
            
            if agent_type == "calling":
                agent = await get_calling_agent(agent_id)
            else:
                agent = await get_chat_agent(agent_id)
            
            pod_config["agents"].append({
                "agent_id": agent_id,
                "type": agent_type,
                "status": "active",
                "assigned_leads": [],
                "performance_metrics": {
                    "interactions": 0,
                    "conversions": 0,
                    "avg_response_time": 0.0
                }
            })
        
        # Store pod configuration
        sales_pods[pod_id] = pod_config
        
        # Start pod optimization in background
        background_tasks.add_task(optimize_pod_allocation, pod_id)
        
        pod_config["status"] = "active"
        
        logger.info(f"Sales pod {pod_id} created with {request.agents_count} agents")
        
        return {
            "pod_id": pod_id,
            "status": "created",
            "agents_deployed": request.agents_count,
            "target_segment": request.target_segment,
            "estimated_capacity": request.agents_count * 10,  # Rough estimate
            "optimization_status": "in_progress"
        }
        
    except Exception as e:
        logger.error(f"Pod creation error: {e}")
        raise HTTPException(status_code=500, detail="Pod creation failed")

@app.get("/api/pods/{pod_id}/metrics", response_model=PodMetricsResponse)
async def get_pod_metrics(
    pod_id: str,
    user: Dict = Depends(get_current_user)
):
    """Get Q-Sales pod performance metrics"""
    try:
        pod_config = sales_pods.get(pod_id)
        if not pod_config:
            raise HTTPException(status_code=404, detail="Pod not found")
        
        # Calculate aggregate metrics
        total_interactions = sum(agent["performance_metrics"]["interactions"] for agent in pod_config["agents"])
        total_conversions = sum(agent["performance_metrics"]["conversions"] for agent in pod_config["agents"])
        avg_response_time = sum(agent["performance_metrics"]["avg_response_time"] for agent in pod_config["agents"]) / len(pod_config["agents"])
        
        success_rate = total_conversions / total_interactions if total_interactions > 0 else 0.0
        
        active_sessions = 0
        for agent_info in pod_config["agents"]:
            agent_id = agent_info["agent_id"]
            if agent_id in chat_agents:
                active_sessions += len(chat_agents[agent_id].conversations)
            elif agent_id in calling_agents:
                active_sessions += len(calling_agents[agent_id].active_calls)
        
        return PodMetricsResponse(
            pod_id=pod_id,
            agents=pod_config["agents"],
            performance_metrics={
                "total_interactions": total_interactions,
                "total_conversions": total_conversions,
                "conversion_rate": success_rate,
                "avg_response_time": avg_response_time,
                "uptime_percentage": 99.5,  # Mock value
                "customer_satisfaction": 4.2  # Mock value
            },
            active_sessions=active_sessions,
            total_interactions=total_interactions,
            success_rate=success_rate
        )
        
    except Exception as e:
        logger.error(f"Pod metrics error: {e}")
        raise HTTPException(status_code=500, detail="Metrics retrieval failed")

@app.post("/api/pods/{pod_id}/optimize")
async def optimize_pod(
    pod_id: str,
    background_tasks: BackgroundTasks,
    user: Dict = Depends(get_current_user)
):
    """Re-run QUBO optimization for pod allocation"""
    try:
        pod_config = sales_pods.get(pod_id)
        if not pod_config:
            raise HTTPException(status_code=404, detail="Pod not found")
        
        # Start optimization in background
        background_tasks.add_task(optimize_pod_allocation, pod_id)
        
        return {
            "pod_id": pod_id,
            "optimization_status": "started",
            "estimated_completion": "2-5 minutes",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Pod optimization error: {e}")
        raise HTTPException(status_code=500, detail="Optimization failed")

# ============================================================================
# BACKGROUND TASKS
# ============================================================================

async def optimize_pod_allocation(pod_id: str):
    """Background task to optimize pod agent allocation using QUBO"""
    try:
        pod_config = sales_pods.get(pod_id)
        if not pod_config:
            logger.error(f"Pod {pod_id} not found for optimization")
            return
        
        logger.info(f"Starting QUBO optimization for pod {pod_id}")
        
        # Build optimization problem
        agents = pod_config["agents"]
        mission_params = pod_config["mission_parameters"]
        
        # Create QUBO matrix for agent-lead allocation
        # This is a simplified example - real implementation would be more complex
        n_agents = len(agents)
        n_leads = mission_params.get("target_leads", 10)
        
        allocation_matrix = []
        for i in range(n_agents):
            agent_row = []
            for j in range(n_leads):
                # Cost function based on agent performance and lead characteristics
                base_cost = 1.0
                agent_performance = agents[i]["performance_metrics"].get("conversions", 0) + 1
                cost = base_cost / agent_performance  # Lower cost for better performing agents
                agent_row.append(cost)
            allocation_matrix.append(agent_row)
        
        # Submit QUBO optimization
        qubo_result = await quantum_job_manager.submit_qubo(
            problem_matrix=allocation_matrix,
            job_metadata={
                "task": "pod_optimization",
                "pod_id": pod_id,
                "agents_count": n_agents,
                "leads_count": n_leads
            }
        )
        
        # Apply optimization results
        solution = qubo_result.get("solution", {})
        
        # Update agent assignments based on solution
        for i, agent in enumerate(agents):
            assigned_leads = [j for j in range(n_leads) if solution.get(f"{i}_{j}", 0) == 1]
            agent["assigned_leads"] = assigned_leads
            
        # Update pod status
        pod_config["optimization_completed"] = datetime.utcnow().isoformat()
        pod_config["optimization_energy"] = qubo_result.get("energy")
        
        logger.info(f"Pod {pod_id} optimization completed with energy {qubo_result.get('energy')}")
        
    except Exception as e:
        logger.error(f"Pod optimization error for {pod_id}: {e}")

# ============================================================================
# QUANTUM METRICS AND MONITORING
# ============================================================================

@app.get("/api/quantum/metrics")
async def get_quantum_metrics(
    user: Dict = Depends(get_current_user)
):
    """Get quantum computing and QUBO job metrics"""
    try:
        quantum_metrics = await quantum_job_manager.get_metrics()
        
        # Add agent-specific metrics
        agent_metrics = {
            "total_chat_agents": len(chat_agents),
            "total_calling_agents": len(calling_agents),
            "total_sales_pods": len(sales_pods),
            "active_conversations": sum(len(agent.conversations) for agent in chat_agents.values()),
            "active_calls": sum(len(agent.active_calls) for agent in calling_agents.values())
        }
        
        return {
            "quantum_metrics": quantum_metrics,
            "agent_metrics": agent_metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Quantum metrics error: {e}")
        raise HTTPException(status_code=500, detail="Metrics retrieval failed")

@app.get("/api/quantum/jobs/{job_id}")
async def get_quantum_job_status(
    job_id: str,
    user: Dict = Depends(get_current_user)
):
    """Get status of specific QUBO job"""
    try:
        job_status = await quantum_job_manager.get_job_status(job_id)
        
        if not job_status:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return job_status
        
    except Exception as e:
        logger.error(f"Job status error: {e}")
        raise HTTPException(status_code=500, detail="Job status retrieval failed")

# ============================================================================
# ADMIN AND CONFIGURATION ENDPOINTS
# ============================================================================

@app.post("/api/admin/agents/{agent_id}/restart")
async def restart_agent(
    agent_id: str,
    user: Dict = Depends(get_current_user)
):
    """Restart specific agent"""
    try:
        # Check user permissions
        if "admin" not in user.get("permissions", []):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Restart chat agent
        if agent_id in chat_agents:
            del chat_agents[agent_id]
            agent = await get_chat_agent(agent_id)
            return {"status": "restarted", "type": "chat_agent", "agent_id": agent_id}
        
        # Restart calling agent
        if agent_id in calling_agents:
            del calling_agents[agent_id]
            agent = await get_calling_agent(agent_id)
            return {"status": "restarted", "type": "calling_agent", "agent_id": agent_id}
        
        raise HTTPException(status_code=404, detail="Agent not found")
        
    except Exception as e:
        logger.error(f"Agent restart error: {e}")
        raise HTTPException(status_code=500, detail="Agent restart failed")

@app.get("/api/admin/system/status")
async def get_system_status(
    user: Dict = Depends(get_current_user)
):
    """Get comprehensive system status"""
    try:
        # Check user permissions
        if "admin" not in user.get("permissions", []):
            raise HTTPException(status_code=403, detail="Admin access required")
        
        return {
            "system_status": "operational",
            "services": {
                "quantum_job_manager": "active" if quantum_job_manager else "inactive",
                "qdllm_service": "active" if qdllm_service else "inactive",
                "qhc_governance": "active" if qhc_governance else "inactive",
                "mcp_provider": "active" if mcp_provider else "inactive"
            },
            "agents": {
                "chat_agents": len(chat_agents),
                "calling_agents": len(calling_agents),
                "sales_pods": len(sales_pods)
            },
            "performance": {
                "uptime": "99.9%",  # Mock value
                "avg_response_time": "150ms",  # Mock value
                "error_rate": "0.1%"  # Mock value
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"System status error: {e}")
        raise HTTPException(status_code=500, detail="System status retrieval failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)