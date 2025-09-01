"""
Agent Orchestrator - Cross-Agent Workflow Management & Network Effects

This module provides the core orchestration system for FLYFOX AI agents,
enabling seamless collaboration between different agent types to create
exponential value for clients through intelligent workflow automation.
"""

import asyncio
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from ..core.ltc_logger import LTCLogger
from ..auth.entitlements import EntitlementsEngine
from .workflow_engine import WorkflowEngine
from .agent_registry import AgentRegistry
from .communication_bus import CommunicationBus


class AgentType(Enum):
    """Types of FLYFOX AI agents available for orchestration."""

    DIGITAL_AGENT = "digital_agent"
    VOICE_AGENT = "voice_agent"
    CHATBOT_AGENT = "chatbot_agent"
    QUANTUM_AGENT = "quantum_agent"
    ANALYTICS_AGENT = "analytics_agent"
    WORKFLOW_AGENT = "workflow_agent"


class WorkflowStatus(Enum):
    """Status of cross-agent workflows."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentCapability:
    """Define what an agent can do and how it can be orchestrated."""

    agent_id: str
    agent_type: AgentType
    capabilities: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    execution_timeout: int  # seconds
    cost_per_execution: float
    availability: float  # 0.0 to 1.0


@dataclass
class WorkflowExecution:
    """Track the execution of a cross-agent workflow."""

    workflow_id: str
    user_id: str
    status: WorkflowStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    steps_completed: int = 0
    total_steps: int = 0
    current_step: Optional[str] = None
    error_message: Optional[str] = None
    execution_metrics: Optional[Dict[str, Any]] = None


class AgentOrchestrator:
    """
    Central orchestrator for cross-agent workflows and collaboration.

    Enables seamless communication between different FLYFOX AI agents,
    creating network effects and exponential value through intelligent
    workflow automation and agent collaboration.
    """

    def __init__(self, ltc_logger: LTCLogger, entitlements: EntitlementsEngine):
        self.ltc_logger = ltc_logger
        self.entitlements = entitlements

        # Core components
        self.workflow_engine = WorkflowEngine(ltc_logger)
        self.agent_registry = AgentRegistry(ltc_logger)
        self.communication_bus = CommunicationBus(ltc_logger)

        # Orchestration state
        self.active_workflows: Dict[str, WorkflowExecution] = {}
        self.workflow_templates: Dict[str, "WorkflowTemplate"] = {}
        self.agent_capabilities: Dict[str, AgentCapability] = {}

        # Performance metrics
        self.total_workflows_executed = 0
        self.successful_workflows = 0
        self.failed_workflows = 0
        self.average_execution_time = 0.0
        self.total_cost_saved = 0.0

    async def initialize_orchestrator(self) -> bool:
        """Initialize the orchestrator and register default agents."""
        try:
            # Initialize sub-components
            await self.workflow_engine.initialize()
            await self.agent_registry.initialize()
            await self.communication_bus.initialize()

            # Register default agent types
            await self._register_default_agents()

            # Load workflow templates
            await self._load_workflow_templates()

            # Log initialization
            await self.ltc_logger.log_operation(
                operation_type="ORCHESTRATOR_INITIALIZATION",
                operation_data={"status": "success", "components": 3},
                metadata={"orchestrator_version": "1.0.0"},
            )

            return True

        except Exception as e:
            await self.ltc_logger.log_operation(
                operation_type="ORCHESTRATOR_INITIALIZATION_ERROR",
                operation_data={"error": str(e)},
                metadata={"orchestrator_version": "1.0.0"},
            )
            return False

    async def register_agent(
        self,
        agent_id: str,
        agent_type: AgentType,
        capabilities: List[str],
        input_schema: Dict[str, Any],
        output_schema: Dict[str, Any],
        execution_timeout: int = 300,
        cost_per_execution: float = 0.0,
    ) -> bool:
        """Register a new agent for orchestration."""
        try:
            capability = AgentCapability(
                agent_id=agent_id,
                agent_type=agent_type,
                capabilities=capabilities,
                input_schema=input_schema,
                output_schema=output_schema,
                execution_timeout=execution_timeout,
                cost_per_execution=cost_per_execution,
                availability=1.0,
            )

            self.agent_capabilities[agent_id] = capability

            # Register with agent registry
            await self.agent_registry.register_agent(agent_id, agent_type, capabilities)

            # Log agent registration
            await self.ltc_logger.log_operation(
                operation_type="AGENT_REGISTRATION",
                operation_data={
                    "agent_id": agent_id,
                    "agent_type": agent_type.value,
                    "capabilities": capabilities,
                },
                metadata={"execution_timeout": execution_timeout},
            )

            return True

        except Exception as e:
            await self.ltc_logger.log_operation(
                operation_type="AGENT_REGISTRATION_ERROR",
                operation_data={"error": str(e), "agent_id": agent_id},
                metadata={"agent_type": agent_type.value},
            )
            return False

    async def execute_workflow(
        self, user_id: str, workflow_name: str, input_data: Dict[str, Any]
    ) -> str:
        """Execute a cross-agent workflow."""
        try:
            # Check entitlements
            if not self.entitlements.check_access(user_id, "WORKFLOW_EXECUTION"):
                raise ValueError("User not authorized for workflow execution")

            # Generate workflow ID
            workflow_id = f"WF_{uuid.uuid4().hex[:8]}"

            # Create workflow execution
            execution = WorkflowExecution(
                workflow_id=workflow_id,
                user_id=user_id,
                status=WorkflowStatus.PENDING,
                created_at=datetime.utcnow(),
                total_steps=0,
            )

            self.active_workflows[workflow_id] = execution

            # Start workflow execution asynchronously
            asyncio.create_task(
                self._execute_workflow_async(workflow_id, workflow_name, input_data)
            )

            # Log workflow start
            await self.ltc_logger.log_operation(
                operation_type="WORKFLOW_EXECUTION_START",
                operation_data={
                    "workflow_id": workflow_id,
                    "user_id": user_id,
                    "workflow_name": workflow_name,
                },
                metadata={"input_data_keys": list(input_data.keys())},
            )

            return workflow_id

        except Exception as e:
            await self.ltc_logger.log_operation(
                operation_type="WORKFLOW_EXECUTION_ERROR",
                operation_data={"error": str(e), "user_id": user_id},
                metadata={"workflow_name": workflow_name},
            )
            raise

    async def get_workflow_status(
        self, workflow_id: str
    ) -> Optional[WorkflowExecution]:
        """Get the current status of a workflow execution."""
        return self.active_workflows.get(workflow_id)

    async def cancel_workflow(self, user_id: str, workflow_id: str) -> bool:
        """Cancel a running workflow."""
        try:
            if workflow_id not in self.active_workflows:
                return False

            execution = self.active_workflows[workflow_id]
            if execution.user_id != user_id:
                return False

            execution.status = WorkflowStatus.CANCELLED
            execution.completed_at = datetime.utcnow()

            # Log cancellation
            await self.ltc_logger.log_operation(
                operation_type="WORKFLOW_CANCELLATION",
                operation_data={"workflow_id": workflow_id, "user_id": user_id},
                metadata={"cancellation_time": datetime.utcnow().isoformat()},
            )

            return True

        except Exception as e:
            await self.ltc_logger.log_operation(
                operation_type="WORKFLOW_CANCELLATION_ERROR",
                operation_data={"error": str(e), "workflow_id": workflow_id},
                metadata={"user_id": user_id},
            )
            return False

    async def get_agent_capabilities(
        self, agent_type: Optional[AgentType] = None
    ) -> List[AgentCapability]:
        """Get available agent capabilities, optionally filtered by type."""
        if agent_type:
            return [
                cap
                for cap in self.agent_capabilities.values()
                if cap.agent_type == agent_type
            ]
        return list(self.agent_capabilities.values())

    async def get_orchestrator_metrics(self) -> Dict[str, Any]:
        """Get orchestrator performance metrics."""
        return {
            "total_workflows_executed": self.total_workflows_executed,
            "successful_workflows": self.successful_workflows,
            "failed_workflows": self.failed_workflows,
            "success_rate": self.successful_workflows
            / max(self.total_workflows_executed, 1),
            "average_execution_time": self.average_execution_time,
            "total_cost_saved": self.total_cost_saved,
            "active_workflows": len(self.active_workflows),
            "registered_agents": len(self.agent_capabilities),
        }

    async def _execute_workflow_async(
        self, workflow_id: str, workflow_name: str, input_data: Dict[str, Any]
    ):
        """Execute a workflow asynchronously."""
        try:
            execution = self.active_workflows[workflow_id]
            execution.status = WorkflowStatus.RUNNING
            execution.started_at = datetime.utcnow()

            # Get workflow template
            if workflow_name not in self.workflow_templates:
                raise ValueError(f"Workflow template '{workflow_name}' not found")

            template = self.workflow_templates[workflow_name]
            execution.total_steps = len(template.steps)

            # Execute workflow steps
            step_results = {}
            for i, step in enumerate(template.steps):
                execution.current_step = step.step_id
                execution.steps_completed = i

                # Execute step
                step_result = await self._execute_workflow_step(
                    step, step_results, input_data
                )
                step_results[step.step_id] = step_result

                # Check for step failure
                if step_result.get("status") == "failed":
                    execution.status = WorkflowStatus.FAILED
                    execution.error_message = step_result.get(
                        "error", "Step execution failed"
                    )
                    break

            # Complete workflow
            if execution.status != WorkflowStatus.FAILED:
                execution.status = WorkflowStatus.COMPLETED
                execution.steps_completed = execution.total_steps
                self.successful_workflows += 1

            execution.completed_at = datetime.utcnow()
            execution_time = (
                execution.completed_at - execution.started_at
            ).total_seconds()

            # Update metrics
            self.total_workflows_executed += 1
            if execution.status == WorkflowStatus.COMPLETED:
                self.average_execution_time = (
                    self.average_execution_time * (self.successful_workflows - 1)
                    + execution_time
                ) / self.successful_workflows
            else:
                self.failed_workflows += 1

            # Log completion
            await self.ltc_logger.log_operation(
                operation_type="WORKFLOW_EXECUTION_COMPLETE",
                operation_data={
                    "workflow_id": workflow_id,
                    "status": execution.status.value,
                    "execution_time": execution_time,
                    "steps_completed": execution.steps_completed,
                },
                metadata={"workflow_name": workflow_name},
            )

        except Exception as e:
            execution = self.active_workflows.get(workflow_id)
            if execution:
                execution.status = WorkflowStatus.FAILED
                execution.error_message = str(e)
                execution.completed_at = datetime.utcnow()
                self.failed_workflows += 1

            await self.ltc_logger.log_operation(
                operation_type="WORKFLOW_EXECUTION_ERROR",
                operation_data={"error": str(e), "workflow_id": workflow_id},
                metadata={"workflow_name": workflow_name},
            )

    async def _execute_workflow_step(
        self,
        step: "WorkflowStep",
        step_results: Dict[str, Any],
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute a single workflow step."""
        try:
            # Get agent for this step
            agent_capability = self.agent_capabilities.get(step.agent_id)
            if not agent_capability:
                return {"status": "failed", "error": f"Agent {step.agent_id} not found"}

            # Prepare step input
            step_input = self._prepare_step_input(step, step_results, input_data)

            # Execute step via communication bus
            result = await self.communication_bus.execute_agent_step(
                step.agent_id, step.step_type, step_input
            )

            return {"status": "success", "result": result}

        except Exception as e:
            return {"status": "failed", "error": str(e)}

    def _prepare_step_input(
        self,
        step: "WorkflowStep",
        step_results: Dict[str, Any],
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Prepare input data for a workflow step."""
        step_input = {}

        # Add direct input data
        if step.input_mapping:
            for key, mapping in step.input_mapping.items():
                if mapping.startswith("input."):
                    input_key = mapping.split(".", 1)[1]
                    step_input[key] = input_data.get(input_key)
                elif mapping.startswith("step."):
                    step_key = mapping.split(".", 1)[1]
                    step_input[key] = step_results.get(step_key)

        # Add step configuration
        if step.config:
            step_input.update(step.config)

        return step_input

    async def _register_default_agents(self):
        """Register default FLYFOX AI agents for orchestration."""
        # Digital Agent
        await self.register_agent(
            agent_id="digital_agent_001",
            agent_type=AgentType.DIGITAL_AGENT,
            capabilities=["process_automation", "data_analysis", "report_generation"],
            input_schema={"task": "string", "data": "object"},
            output_schema={"result": "object", "metadata": "object"},
            execution_timeout=600,
            cost_per_execution=5.0,
        )

        # Voice Agent
        await self.register_agent(
            agent_id="voice_agent_001",
            agent_type=AgentType.VOICE_AGENT,
            capabilities=["voice_interaction", "speech_recognition", "call_handling"],
            input_schema={"audio_input": "string", "context": "object"},
            output_schema={"response": "string", "action": "string"},
            execution_timeout=300,
            cost_per_execution=2.0,
        )

        # Chatbot Agent
        await self.register_agent(
            agent_id="chatbot_agent_001",
            agent_type=AgentType.CHATBOT_AGENT,
            capabilities=["conversation", "intent_recognition", "response_generation"],
            input_schema={"message": "string", "user_context": "object"},
            output_schema={"response": "string", "confidence": "float"},
            execution_timeout=60,
            cost_per_execution=1.0,
        )

        # Quantum Agent
        await self.register_agent(
            agent_id="quantum_agent_001",
            agent_type=AgentType.QUANTUM_AGENT,
            capabilities=["quantum_optimization", "qubo_solving", "quantum_ml"],
            input_schema={"problem": "object", "constraints": "object"},
            output_schema={"solution": "object", "quantum_advantage": "float"},
            execution_timeout=1800,
            cost_per_execution=25.0,
        )

    async def _load_workflow_templates(self):
        """Load default workflow templates for common business processes."""
        # Customer Onboarding Workflow
        onboarding_workflow = WorkflowTemplate(
            id="customer_onboarding",
            name="Customer Onboarding",
            description="Automated customer onboarding using multiple agent types",
            steps=[
                WorkflowStep(
                    step_id="initial_contact",
                    agent_id="chatbot_agent_001",
                    step_type="conversation",
                    input_mapping={"message": "input.welcome_message"},
                    config={"personality": "friendly", "language": "en"},
                ),
                WorkflowStep(
                    step_id="data_collection",
                    agent_id="digital_agent_001",
                    step_type="data_processing",
                    input_mapping={
                        "task": "input.collection_task",
                        "data": "step.initial_contact.result",
                    },
                    config={"validation_rules": "standard"},
                ),
                WorkflowStep(
                    step_id="quantum_optimization",
                    agent_id="quantum_agent_001",
                    step_type="optimization",
                    input_mapping={
                        "problem": "step.data_collection.result",
                        "constraints": "input.constraints",
                    },
                    config={"algorithm": "quantum_annealing"},
                ),
                WorkflowStep(
                    step_id="confirmation_call",
                    agent_id="voice_agent_001",
                    step_type="call_handling",
                    input_mapping={"context": "step.quantum_optimization.result"},
                    config={"call_script": "onboarding_confirmation"},
                ),
            ],
        )

        # Lead Scoring Workflow
        lead_scoring_workflow = WorkflowTemplate(
            id="lead_scoring",
            name="Lead Scoring & Qualification",
            description="Automated lead scoring using AI and quantum optimization",
            steps=[
                WorkflowStep(
                    step_id="data_analysis",
                    agent_id="analytics_agent_001",
                    step_type="data_analysis",
                    input_mapping={"data": "input.lead_data"},
                    config={"analysis_type": "lead_scoring"},
                ),
                WorkflowStep(
                    step_id="quantum_scoring",
                    agent_id="quantum_agent_001",
                    step_type="quantum_ml",
                    input_mapping={"features": "step.data_analysis.result"},
                    config={"model": "quantum_svm"},
                ),
                WorkflowStep(
                    step_id="follow_up_automation",
                    agent_id="digital_agent_001",
                    step_type="automation",
                    input_mapping={
                        "task": "input.follow_up_task",
                        "priority": "step.quantum_scoring.result",
                    },
                    config={"automation_type": "email_sequence"},
                ),
            ],
        )

        # Store templates
        self.workflow_templates = {
            "customer_onboarding": onboarding_workflow,
            "lead_scoring": lead_scoring_workflow,
        }


# Placeholder classes - will be implemented in separate files
class WorkflowTemplate:
    def __init__(self, id, name, description, steps):
        self.id = id
        self.name = name
        self.description = description
        self.steps = steps


class WorkflowStep:
    def __init__(self, step_id, agent_id, step_type, input_mapping=None, config=None):
        self.step_id = step_id
        self.agent_id = agent_id
        self.step_type = step_type
        self.input_mapping = input_mapping or {}
        self.config = config or {}
