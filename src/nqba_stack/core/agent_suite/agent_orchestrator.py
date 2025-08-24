"""
NQBA Agent Orchestrator - Manages and coordinates all agents
Provides unified interface for agent operations and orchestration
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

from .base_agent import BaseAgent, AgentContext, AgentResult, AgentStatus
from .automation_hub import AutomationHub
from ..q_cortex_parser import QCortexParser
from ..ltc_logger import LTCLogger
from ..quantum_adapter import QuantumAdapter

logger = logging.getLogger(__name__)

class OrchestrationMode(Enum):
    """Agent orchestration modes"""
    SEQUENTIAL = "sequential"  # Execute agents one after another
    PARALLEL = "parallel"      # Execute agents simultaneously
    PIPELINE = "pipeline"      # Chain agents in sequence
    INTELLIGENT = "intelligent"  # AI-driven orchestration

@dataclass
class OrchestrationRequest:
    """Request for agent orchestration"""
    request_id: str
    business_unit: str
    description: str
    agent_ids: List[str]
    orchestration_mode: OrchestrationMode
    input_data: Dict[str, Any] = field(default_factory=dict)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    priority: int = 1
    constraints: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class OrchestrationResult:
    """Result from agent orchestration"""
    request_id: str
    success: bool
    agent_results: Dict[str, AgentResult] = field(default_factory=dict)
    orchestration_data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0
    quantum_enhanced: bool = False
    ltc_reference: Optional[str] = None

class AgentOrchestrator:
    """
    Orchestrates multiple agents for complex business operations
    Provides intelligent routing and coordination
    """
    
    def __init__(
        self,
        q_cortex: QCortexParser,
        ltc_logger: LTCLogger,
        quantum_adapter: QuantumAdapter
    ):
        self.q_cortex = q_cortex
        self.ltc_logger = ltc_logger
        self.quantum_adapter = quantum_adapter
        
        # Core components
        self.automation_hub = AutomationHub(q_cortex, ltc_logger, quantum_adapter)
        self.agents: Dict[str, BaseAgent] = {}
        
        # Orchestration state
        self.active_orchestrations: Dict[str, OrchestrationRequest] = {}
        self.orchestration_history: List[OrchestrationResult] = []
        
        # Performance metrics
        self.metrics = {
            'total_orchestrations': 0,
            'successful_orchestrations': 0,
            'total_agent_executions': 0,
            'average_orchestration_time': 0.0,
            'business_unit_breakdown': {}
        }
        
        logger.info("NQBA Agent Orchestrator initialized")
    
    def register_agent(self, agent: BaseAgent) -> bool:
        """Register an agent with the orchestrator"""
        try:
            if agent.agent_id in self.agents:
                logger.warning(f"Agent {agent.agent_id} already registered, updating")
            
            self.agents[agent.agent_id] = agent
            logger.info(f"Registered agent: {agent.agent_id} ({agent.agent_type})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to register agent {agent.agent_id}: {str(e)}")
            return False
    
    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent from the orchestrator"""
        try:
            if agent_id in self.agents:
                del self.agents[agent_id]
                logger.info(f"Unregistered agent: {agent_id}")
                return True
            else:
                logger.warning(f"Agent {agent_id} not found for unregistration")
                return False
                
        except Exception as e:
            logger.error(f"Failed to unregister agent {agent_id}: {str(e)}")
            return False
    
    async def orchestrate_agents(
        self, 
        request: OrchestrationRequest
    ) -> OrchestrationResult:
        """Orchestrate multiple agents based on the specified mode"""
        
        start_time = datetime.now()
        
        # Validate request
        if not request.agent_ids:
            raise ValueError("Orchestration request must specify at least one agent")
        
        # Check agent availability
        unavailable_agents = [aid for aid in request.agent_ids if aid not in self.agents]
        if unavailable_agents:
            raise ValueError(f"Agents not found: {unavailable_agents}")
        
        # Store active orchestration
        self.active_orchestrations[request.request_id] = request
        
        try:
            # Execute orchestration based on mode
            if request.orchestration_mode == OrchestrationMode.SEQUENTIAL:
                result = await self._execute_sequential_orchestration(request)
            elif request.orchestration_mode == OrchestrationMode.PARALLEL:
                result = await self._execute_parallel_orchestration(request)
            elif request.orchestration_mode == OrchestrationMode.PIPELINE:
                result = await self._execute_pipeline_orchestration(request)
            elif request.orchestration_mode == OrchestrationMode.INTELLIGENT:
                result = await self._execute_intelligent_orchestration(request)
            else:
                raise ValueError(f"Unknown orchestration mode: {request.orchestration_mode}")
            
            # Update metrics
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self._update_metrics(request.business_unit, True, execution_time, result.quantum_enhanced)
            
            # Store result
            self.orchestration_history.append(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Orchestration failed: {request.request_id}, error: {str(e)}")
            
            # Create failure result
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            failure_result = OrchestrationResult(
                request_id=request.request_id,
                success=False,
                orchestration_data={'error': str(e)},
                metadata={'business_unit': request.business_unit, 'mode': request.orchestration_mode.value}
            )
            
            # Update metrics
            self._update_metrics(request.business_unit, False, execution_time, False)
            
            # Store result
            self.orchestration_history.append(failure_result)
            
            return failure_result
            
        finally:
            # Remove from active orchestrations
            if request.request_id in self.active_orchestrations:
                del self.active_orchestrations[request.request_id]
    
    async def _execute_sequential_orchestration(
        self, 
        request: OrchestrationRequest
    ) -> OrchestrationResult:
        """Execute agents sequentially, passing results between them"""
        
        agent_results = {}
        orchestration_data = {}
        current_data = request.input_data.copy()
        
        for agent_id in request.agent_ids:
            agent = self.agents[agent_id]
            
            # Create agent context
            context = AgentContext(
                business_unit=request.business_unit,
                user_id=request.user_id,
                session_id=request.session_id,
                priority=request.priority,
                constraints=request.constraints,
                metadata=request.metadata
            )
            
            # Execute agent
            result = await agent.execute_with_compliance(current_data, context)
            agent_results[agent_id] = result
            
            # Update data for next agent
            if result.success and isinstance(result.data, dict):
                current_data.update(result.data)
                orchestration_data[f"{agent_id}_output"] = result.data
            
            # Check if we should continue
            if not result.success and request.constraints.get('stop_on_failure', True):
                break
        
        return OrchestrationResult(
            request_id=request.request_id,
            success=all(r.success for r in agent_results.values()),
            agent_results=agent_results,
            orchestration_data=orchestration_data,
            metadata={
                'business_unit': request.business_unit,
                'mode': 'sequential',
                'agent_count': len(agent_results)
            },
            execution_time_ms=0,  # Will be updated by caller
            quantum_enhanced=any(r.quantum_enhanced for r in agent_results.values())
        )
    
    async def _execute_parallel_orchestration(
        self, 
        request: OrchestrationRequest
    ) -> OrchestrationResult:
        """Execute agents in parallel"""
        
        # Create tasks for all agents
        agent_tasks = {}
        for agent_id in request.agent_ids:
            agent = self.agents[agent_id]
            
            # Create agent context
            context = AgentContext(
                business_unit=request.business_unit,
                user_id=request.user_id,
                session_id=request.session_id,
                priority=request.priority,
                constraints=request.constraints,
                metadata=request.metadata
            )
            
            # Create task
            task = agent.execute_with_compliance(request.input_data, context)
            agent_tasks[agent_id] = task
        
        # Execute all agents in parallel
        agent_results = {}
        for agent_id, task in agent_tasks.items():
            try:
                result = await task
                agent_results[agent_id] = result
            except Exception as e:
                # Create error result
                agent_results[agent_id] = AgentResult(
                    success=False,
                    data=f"Execution error: {str(e)}",
                    metadata={'error_type': type(e).__name__}
                )
        
        return OrchestrationResult(
            request_id=request.request_id,
            success=all(r.success for r in agent_results.values()),
            agent_results=agent_results,
            orchestration_data={
                'parallel_execution': True,
                'agent_count': len(agent_results)
            },
            metadata={
                'business_unit': request.business_unit,
                'mode': 'parallel',
                'agent_count': len(agent_results)
            },
            execution_time_ms=0,
            quantum_enhanced=any(r.quantum_enhanced for r in agent_results.values())
        )
    
    async def _execute_pipeline_orchestration(
        self, 
        request: OrchestrationRequest
    ) -> OrchestrationResult:
        """Execute agents in a pipeline, with data flowing through each stage"""
        
        agent_results = {}
        orchestration_data = {}
        pipeline_data = request.input_data.copy()
        
        for i, agent_id in enumerate(request.agent_ids):
            agent = self.agents[agent_id]
            
            # Create agent context with pipeline stage info
            context = AgentContext(
                business_unit=request.business_unit,
                user_id=request.user_id,
                session_id=request.session_id,
                priority=request.priority,
                constraints=request.constraints,
                metadata={
                    **request.metadata,
                    'pipeline_stage': i + 1,
                    'total_stages': len(request.agent_ids),
                    'pipeline_data': pipeline_data
                }
            )
            
            # Execute agent
            result = await agent.execute_with_compliance(pipeline_data, context)
            agent_results[agent_id] = result
            
            # Update pipeline data for next stage
            if result.success and isinstance(result.data, dict):
                pipeline_data.update(result.data)
                orchestration_data[f"stage_{i+1}_{agent_id}"] = result.data
            
            # Check pipeline constraints
            if not result.success and request.constraints.get('stop_on_failure', True):
                break
        
        return OrchestrationResult(
            request_id=request.request_id,
            success=all(r.success for r in agent_results.values()),
            agent_results=agent_results,
            orchestration_data=orchestration_data,
            metadata={
                'business_unit': request.business_unit,
                'mode': 'pipeline',
                'agent_count': len(agent_results),
                'pipeline_data': pipeline_data
            },
            execution_time_ms=0,
            quantum_enhanced=any(r.quantum_enhanced for r in agent_results.values())
        )
    
    async def _execute_intelligent_orchestration(
        self, 
        request: OrchestrationRequest
    ) -> OrchestrationResult:
        """Execute agents using AI-driven intelligent orchestration"""
        
        # Use quantum adapter for intelligent routing
        orchestration_plan = await self.quantum_adapter.optimize_orchestration(
            objective="efficient_execution",
            constraints={
                'agents': request.agent_ids,
                'business_unit': request.business_unit,
                'priority': request.priority
            },
            data=request.input_data
        )
        
        # Execute based on intelligent plan
        if orchestration_plan.get('recommended_mode') == 'pipeline':
            return await self._execute_pipeline_orchestration(request)
        elif orchestration_plan.get('recommended_mode') == 'parallel':
            return await self._execute_parallel_orchestration(request)
        else:
            # Default to sequential
            return await self._execute_sequential_orchestration(request)
    
    async def execute_business_workflow(
        self, 
        business_unit: str,
        workflow_type: str,
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> OrchestrationResult:
        """Execute a predefined business workflow using multiple agents"""
        
        # Define business workflows
        business_workflows = {
            'sigma_select_lead_processing': {
                'description': 'Complete lead processing workflow for Sigma Select',
                'agents': ['lead_scoring_agent', 'followup_agent', 'crm_agent'],
                'mode': OrchestrationMode.PIPELINE,
                'automation_id': 'lead_scoring'
            },
            'goliath_trading_optimization': {
                'description': 'Portfolio optimization workflow for Goliath',
                'agents': ['market_analysis_agent', 'risk_assessment_agent', 'optimization_agent'],
                'mode': OrchestrationMode.SEQUENTIAL,
                'automation_id': 'process_optimization'
            },
            'flyfox_ai_route_optimization': {
                'description': 'Logistics route optimization for FLYFOX AI',
                'agents': ['route_analysis_agent', 'constraint_agent', 'optimization_agent'],
                'mode': OrchestrationMode.INTELLIGENT,
                'automation_id': 'process_optimization'
            }
        }
        
        if workflow_type not in business_workflows:
            raise ValueError(f"Unknown business workflow: {workflow_type}")
        
        workflow = business_workflows[workflow_type]
        
        # Create orchestration request
        request = OrchestrationRequest(
            request_id=f"{workflow_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            business_unit=business_unit,
            description=workflow['description'],
            agent_ids=workflow['agents'],
            orchestration_mode=workflow['mode'],
            input_data=input_data,
            metadata=context
        )
        
        # Execute orchestration
        result = await self.orchestrate_agents(request)
        
        # If automation ID is specified, also execute the automation
        if workflow.get('automation_id'):
            try:
                automation_result = await self.automation_hub.execute_automation(
                    automation_id=workflow['automation_id'],
                    input_data=input_data,
                    context=context
                )
                
                # Merge automation result with orchestration result
                result.orchestration_data['automation_result'] = automation_result.data
                result.quantum_enhanced = result.quantum_enhanced or automation_result.quantum_enhanced
                
            except Exception as e:
                logger.warning(f"Automation execution failed: {str(e)}")
                result.orchestration_data['automation_error'] = str(e)
        
        return result
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific agent"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        return agent.get_health_status()
    
    def get_all_agent_statuses(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all registered agents"""
        return {
            agent_id: agent.get_health_status()
            for agent_id, agent in self.agents.items()
        }
    
    def get_orchestration_metrics(self, business_unit: Optional[str] = None) -> Dict[str, Any]:
        """Get orchestration performance metrics"""
        
        if business_unit:
            return self.metrics['business_unit_breakdown'].get(business_unit, {})
        else:
            return self.metrics.copy()
    
    def get_orchestration_history(
        self, 
        limit: int = 50, 
        business_unit: Optional[str] = None
    ) -> List[OrchestrationResult]:
        """Get orchestration execution history"""
        
        history = self.orchestration_history[-limit:] if limit > 0 else self.orchestration_history
        
        if business_unit:
            return [result for result in history if result.metadata.get('business_unit') == business_unit]
        else:
            return history
    
    def get_active_orchestrations(self) -> List[Dict[str, Any]]:
        """Get currently active orchestrations"""
        return [
            {
                'request_id': req.request_id,
                'business_unit': req.business_unit,
                'description': req.description,
                'agent_count': len(req.agent_ids),
                'mode': req.orchestration_mode.value,
                'start_time': req.request_id.split('_')[-1]  # Extract timestamp
            }
            for req in self.active_orchestrations.values()
        ]
    
    def _update_metrics(
        self, 
        business_unit: str, 
        success: bool, 
        execution_time: float,
        quantum_enhanced: bool
    ):
        """Update orchestration metrics"""
        
        self.metrics['total_orchestrations'] += 1
        if success:
            self.metrics['successful_orchestrations'] += 1
        
        # Update business unit breakdown
        if business_unit not in self.metrics['business_unit_breakdown']:
            self.metrics['business_unit_breakdown'][business_unit] = {
                'total': 0,
                'successful': 0,
                'total_time': 0.0,
                'agent_executions': 0
            }
        
        bu_metrics = self.metrics['business_unit_breakdown'][business_unit]
        bu_metrics['total'] += 1
        if success:
            bu_metrics['successful'] += 1
        bu_metrics['total_time'] += execution_time
        
        # Update average execution time
        current_avg = self.metrics['average_orchestration_time']
        total_ops = self.metrics['total_orchestrations']
        self.metrics['average_orchestration_time'] = (
            (current_avg * (total_ops - 1) + execution_time) / total_ops
        )
    
    async def shutdown(self):
        """Graceful shutdown of the agent orchestrator"""
        logger.info("Shutting down NQBA Agent Orchestrator")
        
        # Shutdown automation hub
        await self.automation_hub.shutdown()
        
        # Shutdown all agents
        for agent_id, agent in self.agents.items():
            try:
                await agent.shutdown()
            except Exception as e:
                logger.error(f"Error shutting down agent {agent_id}: {str(e)}")
        
        # Log shutdown to LTC
        await self.ltc_logger.log_operation(
            operation_type="agent_orchestrator_shutdown",
            operation_data={
                'total_orchestrations': self.metrics['total_orchestrations'],
                'successful_orchestrations': self.metrics['successful_orchestrations'],
                'total_agents': len(self.agents),
                'shutdown_time': datetime.now().isoformat()
            },
            thread_ref=f"ORCHESTRATOR_SHUTDOWN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
