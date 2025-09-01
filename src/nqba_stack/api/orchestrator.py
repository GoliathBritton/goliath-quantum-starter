"""
Cross-Agent Orchestrator API Endpoints

Provides REST API access to cross-agent workflow orchestration including:
- Workflow execution and management
- Agent registration and capability discovery
- Cross-agent communication and collaboration
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from ..auth import get_current_user, require_feature
from ..orchestrator import AgentOrchestrator, AgentType, WorkflowStatus
from ..core.ltc_logger import LTCLogger
from ..auth.entitlements import EntitlementsEngine

router = APIRouter(prefix="/orchestrator", tags=["Cross-Agent Orchestrator"])


# Pydantic models for API requests/responses
class WorkflowExecutionRequest(BaseModel):
    workflow_name: str
    input_data: Dict[str, Any]


class AgentRegistrationRequest(BaseModel):
    agent_id: str
    agent_type: AgentType
    capabilities: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    execution_timeout: int = 300
    cost_per_execution: float = 0.0


class WorkflowStatusResponse(BaseModel):
    workflow_id: str
    status: WorkflowStatus
    steps_completed: int
    total_steps: int
    current_step: Optional[str]
    error_message: Optional[str]
    created_at: str
    started_at: Optional[str]
    completed_at: Optional[str]


class AgentCapabilityResponse(BaseModel):
    agent_id: str
    agent_type: str
    capabilities: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    execution_timeout: int
    cost_per_execution: float
    availability: float


class OrchestratorMetricsResponse(BaseModel):
    total_workflows_executed: int
    successful_workflows: int
    failed_workflows: int
    success_rate: float
    average_execution_time: float
    total_cost_saved: float
    active_workflows: int
    registered_agents: int


# Dependency injection
async def get_agent_orchestrator() -> AgentOrchestrator:
    """Get the agent orchestrator instance."""
    # This would be initialized in your main app startup
    ltc_logger = LTCLogger()
    entitlements = EntitlementsEngine()
    orchestrator = AgentOrchestrator(ltc_logger, entitlements)
    await orchestrator.initialize_orchestrator()
    return orchestrator


@router.post("/workflows/execute", status_code=status.HTTP_202_ACCEPTED)
async def execute_workflow(
    request: WorkflowExecutionRequest,
    current_user: dict = Depends(get_current_user),
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Execute a cross-agent workflow."""
    try:
        workflow_id = await orchestrator.execute_workflow(
            user_id=current_user["user_id"],
            workflow_name=request.workflow_name,
            input_data=request.input_data,
        )

        return {
            "message": "Workflow execution started",
            "workflow_id": workflow_id,
            "workflow_name": request.workflow_name,
            "status": "pending",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow execution failed: {str(e)}",
        )


@router.get("/workflows/{workflow_id}/status", response_model=WorkflowStatusResponse)
async def get_workflow_status(
    workflow_id: str,
    current_user: dict = Depends(get_current_user),
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Get the current status of a workflow execution."""
    try:
        execution = await orchestrator.get_workflow_status(workflow_id)

        if not execution:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found"
            )

        # Verify user owns this workflow
        if execution.user_id != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this workflow",
            )

        return WorkflowStatusResponse(
            workflow_id=execution.workflow_id,
            status=execution.status,
            steps_completed=execution.steps_completed,
            total_steps=execution.total_steps,
            current_step=execution.current_step,
            error_message=execution.error_message,
            created_at=execution.created_at.isoformat(),
            started_at=(
                execution.started_at.isoformat() if execution.started_at else None
            ),
            completed_at=(
                execution.completed_at.isoformat() if execution.completed_at else None
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve workflow status: {str(e)}",
        )


@router.post("/workflows/{workflow_id}/cancel")
async def cancel_workflow(
    workflow_id: str,
    current_user: dict = Depends(get_current_user),
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Cancel a running workflow."""
    try:
        success = await orchestrator.cancel_workflow(
            user_id=current_user["user_id"], workflow_id=workflow_id
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to cancel workflow",
            )

        return {
            "message": "Workflow cancelled successfully",
            "workflow_id": workflow_id,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Workflow cancellation failed: {str(e)}",
        )


@router.post("/agents/register", status_code=status.HTTP_201_CREATED)
@require_feature("AGENT_REGISTRATION")
async def register_agent(
    request: AgentRegistrationRequest,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Register a new agent for orchestration."""
    try:
        success = await orchestrator.register_agent(
            agent_id=request.agent_id,
            agent_type=request.agent_type,
            capabilities=request.capabilities,
            input_schema=request.input_schema,
            output_schema=request.output_schema,
            execution_timeout=request.execution_timeout,
            cost_per_execution=request.cost_per_execution,
        )

        if not success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to register agent",
            )

        return {
            "message": "Agent registered successfully",
            "agent_id": request.agent_id,
            "agent_type": request.agent_type.value,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent registration failed: {str(e)}",
        )


@router.get("/agents/capabilities", response_model=List[AgentCapabilityResponse])
async def get_agent_capabilities(
    agent_type: Optional[AgentType] = None,
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Get available agent capabilities, optionally filtered by type."""
    try:
        capabilities = await orchestrator.get_agent_capabilities(agent_type)

        return [
            AgentCapabilityResponse(
                agent_id=cap.agent_id,
                agent_type=cap.agent_type.value,
                capabilities=cap.capabilities,
                input_schema=cap.input_schema,
                output_schema=cap.output_schema,
                execution_timeout=cap.execution_timeout,
                cost_per_execution=cap.cost_per_execution,
                availability=cap.availability,
            )
            for cap in capabilities
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve agent capabilities: {str(e)}",
        )


@router.get("/workflows/templates")
async def get_workflow_templates(
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Get available workflow templates."""
    try:
        templates = orchestrator.workflow_templates

        return [
            {
                "id": template.id,
                "name": template.name,
                "description": template.description,
                "steps": [
                    {
                        "step_id": step.step_id,
                        "agent_id": step.agent_id,
                        "step_type": step.step_type,
                        "input_mapping": step.input_mapping,
                        "config": step.config,
                    }
                    for step in template.steps
                ],
            }
            for template in templates.values()
        ]

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve workflow templates: {str(e)}",
        )


@router.get("/metrics", response_model=OrchestratorMetricsResponse)
@require_feature("ORCHESTRATOR_ADMIN")
async def get_orchestrator_metrics(
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Get orchestrator performance metrics (admin only)."""
    try:
        metrics = await orchestrator.get_orchestrator_metrics()

        return OrchestratorMetricsResponse(
            total_workflows_executed=metrics["total_workflows_executed"],
            successful_workflows=metrics["successful_workflows"],
            failed_workflows=metrics["failed_workflows"],
            success_rate=metrics["success_rate"],
            average_execution_time=metrics["average_execution_time"],
            total_cost_saved=metrics["total_cost_saved"],
            active_workflows=metrics["active_workflows"],
            registered_agents=metrics["registered_agents"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve metrics: {str(e)}",
        )


@router.get("/health")
async def orchestrator_health_check(
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Health check for the orchestrator system."""
    try:
        # Check if orchestrator is properly initialized
        if not orchestrator.workflow_templates:
            raise Exception("No workflow templates loaded")

        if not orchestrator.agent_capabilities:
            raise Exception("No agents registered")

        return {
            "status": "healthy",
            "workflow_templates": len(orchestrator.workflow_templates),
            "registered_agents": len(orchestrator.agent_capabilities),
            "active_workflows": len(orchestrator.active_workflows),
            "total_workflows_executed": orchestrator.total_workflows_executed,
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Orchestrator system unhealthy: {str(e)}",
        )


@router.get("/demo/customer-onboarding")
async def demo_customer_onboarding_workflow(
    orchestrator: AgentOrchestrator = Depends(get_agent_orchestrator),
):
    """Demo the customer onboarding workflow."""
    try:
        # This would be a demo workflow execution
        demo_input = {
            "welcome_message": "Welcome to FLYFOX AI! Let's get you started.",
            "collection_task": "collect_customer_info",
            "constraints": {"time_limit": 300, "data_quality": "high"},
        }

        # For demo purposes, return the workflow template
        template = orchestrator.workflow_templates.get("customer_onboarding")
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer onboarding workflow template not found",
            )

        return {
            "message": "Customer Onboarding Workflow Demo",
            "workflow_id": template.id,
            "description": template.description,
            "steps": [
                {
                    "step_id": step.step_id,
                    "agent_type": step.agent_id,
                    "description": f"Step {i+1}: {step.step_type} using {step.agent_id}",
                }
                for i, step in enumerate(template.steps)
            ],
            "demo_input": demo_input,
            "estimated_duration": "5-10 minutes",
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Demo failed: {str(e)}",
        )
