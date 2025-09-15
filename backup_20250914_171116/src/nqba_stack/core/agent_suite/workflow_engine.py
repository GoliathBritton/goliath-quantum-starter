"""
NQBA Workflow Engine - Quantum Process Intelligence Platform
Combines FLYFOX AI RPA, Goliath Trade workflows, and Sigma Select process mining with quantum enhancements
"""

import asyncio
import json
import yaml
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

from ..q_cortex_parser import QCortexParser
from ..ltc_logger import LTCLogger
from ..quantum_adapter import QuantumAdapter

logger = logging.getLogger(__name__)

class WorkflowStatus(Enum):
    """Workflow execution status"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PAUSED = "paused"

class WorkflowType(Enum):
    """Types of workflows supported"""
    RPA = "rpa"  # FLYFOX AI-style task automation
    PROCESS_MINING = "process_mining"  # Sigma Select-style process analysis
    API_WORKFLOW = "api_workflow"  # Goliath Trade-style API integrations
    QUANTUM_OPTIMIZATION = "quantum_optimization"  # DynexSolve enhanced
    QDA_PERSONALIZATION = "qda_personalization"  # Website agent optimization

@dataclass
class WorkflowStep:
    """Individual step in a workflow"""
    step_id: str
    step_type: str
    name: str
    description: str
    config: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    timeout_seconds: int = 300
    retry_count: int = 3
    quantum_enhanced: bool = False

@dataclass
class WorkflowDefinition:
    """Complete workflow definition"""
    workflow_id: str
    name: str
    description: str
    workflow_type: WorkflowType
    version: str = "1.0.0"
    business_unit: str = "general"
    steps: List[WorkflowStep] = field(default_factory=list)
    triggers: List[Dict[str, Any]] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    compliance_rules: List[str] = field(default_factory=list)

@dataclass
class WorkflowExecution:
    """Workflow execution instance"""
    execution_id: str
    workflow_id: str
    status: WorkflowStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    current_step: Optional[str] = None
    step_results: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)
    ltc_reference: Optional[str] = None
    quantum_enhanced: bool = False
    performance_metrics: Dict[str, Any] = field(default_factory=dict)

class QuantumWorkflowEngine:
    """
    Quantum-enhanced workflow engine combining RPA, process mining, and API workflows
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
        
        # Workflow registry
        self.workflows: Dict[str, WorkflowDefinition] = {}
        self.executions: Dict[str, WorkflowExecution] = {}
        
        # Built-in workflow templates
        self._load_builtin_workflows()
        
        logger.info("Quantum Workflow Engine initialized")
    
    def _load_builtin_workflows(self):
        """Load built-in workflow templates inspired by UiPath, n8n, and Celonis"""
        
        # UiPath-style RPA workflows
        self.workflows["invoice_processing"] = WorkflowDefinition(
            workflow_id="invoice_processing",
            name="Invoice Processing Automation",
            description="Automates invoice data extraction and processing",
            workflow_type=WorkflowType.RPA,
            business_unit="finance",
            steps=[
                WorkflowStep(
                    step_id="extract_data",
                    step_type="rpa_extraction",
                    name="Extract Invoice Data",
                    description="Use computer vision to extract invoice fields",
                    config={
                        "template": "invoice_template_v1",
                        "fields": ["invoice_number", "amount", "vendor", "date"],
                        "confidence_threshold": 0.85
                    }
                ),
                WorkflowStep(
                    step_id="validate_data",
                    step_type="data_validation",
                    name="Validate Extracted Data",
                    description="Validate extracted data against business rules",
                    config={
                        "rules": ["amount > 0", "date_format_valid", "vendor_exists"],
                        "auto_correction": True
                    }
                ),
                WorkflowStep(
                    step_id="process_approval",
                    step_type="approval_workflow",
                    name="Process Approval",
                    description="Route for approval based on amount thresholds",
                    config={
                        "thresholds": {"low": 1000, "medium": 5000, "high": 10000},
                        "approvers": {"low": "manager", "medium": "director", "high": "vp"}
                    }
                )
            ]
        )
        
        # n8n-style API workflow
        self.workflows["lead_followup"] = WorkflowDefinition(
            workflow_id="lead_followup",
            name="Lead Follow-up Automation",
            description="Automates lead nurturing and follow-up sequences",
            workflow_type=WorkflowType.API_WORKFLOW,
            business_unit="sales",
            steps=[
                WorkflowStep(
                    step_id="score_lead",
                    step_type="api_call",
                    name="Score Lead",
                    description="Call NQBA decision engine for lead scoring",
                    config={
                        "endpoint": "/v1/decide",
                        "method": "POST",
                        "data_mapping": {
                            "lead_data": "{{input.lead_data}}",
                            "context": "sigma_select"
                        }
                    }
                ),
                WorkflowStep(
                    step_id="determine_action",
                    step_type="conditional_logic",
                    name="Determine Next Action",
                    description="Route lead based on score and behavior",
                    config={
                        "conditions": [
                            {"if": "score >= 0.8", "then": "immediate_contact"},
                            {"if": "score >= 0.6", "then": "nurture_sequence"},
                            {"if": "score < 0.6", "then": "re_engagement"}
                        ]
                    }
                ),
                WorkflowStep(
                    step_id="execute_action",
                    step_type="api_call",
                    name="Execute Action",
                    description="Trigger appropriate action (email, call, etc.)",
                    config={
                        "endpoint": "/v1/trigger_action",
                        "method": "POST",
                        "data_mapping": {
                            "action": "{{step.determine_action.result}}",
                            "lead_id": "{{input.lead_id}}"
                        }
                    }
                )
            ]
        )
        
        # Celonis-style process mining
        self.workflows["process_analysis"] = WorkflowDefinition(
            workflow_id="process_analysis",
            name="Process Mining & Analysis",
            description="Analyzes business processes for optimization opportunities",
            workflow_type=WorkflowType.PROCESS_MINING,
            business_unit="operations",
            steps=[
                WorkflowStep(
                    step_id="collect_data",
                    step_type="data_collection",
                    name="Collect Process Data",
                    description="Gather data from ERP, CRM, and other systems",
                    config={
                        "sources": ["salesforce", "sap", "oracle"],
                        "time_range": "last_30_days",
                        "data_types": ["events", "transactions", "user_actions"]
                    }
                ),
                WorkflowStep(
                    step_id="create_digital_twin",
                    step_type="quantum_optimization",
                    name="Create Quantum Digital Twin",
                    description="Use DynexSolve to create optimized process model",
                    config={
                        "algorithm": "qubo_process_mapping",
                        "optimization_target": "efficiency",
                        "constraints": ["compliance", "cost", "time"]
                    },
                    quantum_enhanced=True
                ),
                WorkflowStep(
                    step_id="identify_optimizations",
                    step_type="analysis",
                    name="Identify Optimization Opportunities",
                    description="Analyze digital twin for improvement areas",
                    config={
                        "metrics": ["cycle_time", "bottlenecks", "resource_utilization"],
                        "thresholds": {"cycle_time_reduction": 0.2, "cost_savings": 0.15}
                    }
                )
            ]
        )
        
        # QDA personalization workflow
        self.workflows["qda_optimization"] = WorkflowDefinition(
            workflow_id="qda_optimization",
            name="QDA Personalization Optimization",
            description="Optimizes website agent behavior for maximum conversion",
            workflow_type=WorkflowType.QDA_PERSONALIZATION,
            business_unit="marketing",
            steps=[
                WorkflowStep(
                    step_id="analyze_behavior",
                    step_type="data_analysis",
                    name="Analyze User Behavior",
                    description="Analyze user interactions and conversion patterns",
                    config={
                        "data_sources": ["google_analytics", "hotjar", "custom_events"],
                        "metrics": ["session_duration", "page_views", "conversion_rate"]
                    }
                ),
                WorkflowStep(
                    step_id="optimize_personality",
                    step_type="quantum_optimization",
                    name="Optimize QDA Personality",
                    description="Use DynexSolve to optimize agent personality traits",
                    config={
                        "algorithm": "qubo_personality_optimization",
                        "traits": ["friendliness", "professionalism", "urgency"],
                        "target": "conversion_rate"
                    },
                    quantum_enhanced=True
                ),
                WorkflowStep(
                    step_id="deploy_changes",
                    step_type="deployment",
                    name="Deploy Optimized QDA",
                    description="Deploy optimized agent to website",
                    config={
                        "deployment_method": "blue_green",
                        "rollback_threshold": 0.05,
                        "monitoring_duration": "24_hours"
                    }
                )
            ]
        )
    
    async def create_workflow(self, workflow_def: WorkflowDefinition) -> str:
        """Create a new workflow definition"""
        try:
            # Validate workflow against Q-Cortex policies
            validation_result = await self._validate_workflow(workflow_def)
            if not validation_result['valid']:
                raise ValueError(f"Workflow validation failed: {validation_result['errors']}")
            
            # Store workflow
            self.workflows[workflow_def.workflow_id] = workflow_def
            
            # Log to LTC
            await self.ltc_logger.log_operation(
                operation_type="workflow_created",
                operation_data={
                    'workflow_id': workflow_def.workflow_id,
                    'workflow_type': workflow_def.workflow_type.value,
                    'business_unit': workflow_def.business_unit,
                    'step_count': len(workflow_def.steps)
                },
                thread_ref=f"WORKFLOW_{workflow_def.workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            logger.info(f"Created workflow: {workflow_def.workflow_id}")
            return workflow_def.workflow_id
            
        except Exception as e:
            logger.error(f"Failed to create workflow: {str(e)}")
            raise
    
    async def execute_workflow(
        self, 
        workflow_id: str, 
        input_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """Execute a workflow with quantum enhancements where applicable"""
        
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        execution_id = f"{workflow_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create execution instance
        execution = WorkflowExecution(
            execution_id=execution_id,
            workflow_id=workflow_id,
            status=WorkflowStatus.RUNNING,
            start_time=datetime.now(),
            variables=input_data.copy()
        )
        
        self.executions[execution_id] = execution
        
        try:
            # Execute workflow steps
            await self._execute_workflow_steps(workflow, execution, context)
            
            # Mark as completed
            execution.status = WorkflowStatus.COMPLETED
            execution.end_time = datetime.now()
            
            # Log completion to LTC
            execution.ltc_reference = await self.ltc_logger.log_operation(
                operation_type="workflow_completed",
                operation_data={
                    'execution_id': execution_id,
                    'workflow_id': workflow_id,
                    'duration_seconds': (execution.end_time - execution.start_time).total_seconds(),
                    'step_results': execution.step_results,
                    'quantum_enhanced': execution.quantum_enhanced
                },
                thread_ref=f"EXEC_{execution_id}"
            )
            
            logger.info(f"Workflow execution completed: {execution_id}")
            return execution_id
            
        except Exception as e:
            execution.status = WorkflowStatus.FAILED
            execution.end_time = datetime.now()
            
            logger.error(f"Workflow execution failed: {execution_id}, error: {str(e)}")
            raise
    
    async def _execute_workflow_steps(
        self, 
        workflow: WorkflowDefinition, 
        execution: WorkflowExecution,
        context: Dict[str, Any]
    ):
        """Execute individual workflow steps"""
        
        # Track dependencies and execution order
        completed_steps = set()
        step_queue = workflow.steps.copy()
        
        while step_queue:
            # Find steps ready to execute (dependencies satisfied)
            ready_steps = [
                step for step in step_queue 
                if all(dep in completed_steps for dep in step.dependencies)
            ]
            
            if not ready_steps:
                raise RuntimeError("Circular dependency detected in workflow")
            
            # Execute ready steps in parallel
            step_tasks = []
            for step in ready_steps:
                task = self._execute_step(step, execution, context)
                step_tasks.append(task)
            
            # Wait for all steps to complete
            step_results = await asyncio.gather(*step_tasks, return_exceptions=True)
            
            # Process results
            for step, result in zip(ready_steps, step_results):
                if isinstance(result, Exception):
                    raise result
                
                execution.step_results[step.step_id] = result
                completed_steps.add(step.step_id)
                step_queue.remove(step)
                
                # Update execution variables
                if isinstance(result, dict):
                    execution.variables.update(result)
    
    async def _execute_step(
        self, 
        step: WorkflowStep, 
        execution: WorkflowExecution,
        context: Dict[str, Any]
    ) -> Any:
        """Execute a single workflow step"""
        
        execution.current_step = step.step_id
        start_time = datetime.now()
        
        try:
            # Execute based on step type
            if step.step_type == "rpa_extraction":
                result = await self._execute_rpa_step(step, execution, context)
            elif step.step_type == "api_call":
                result = await self._execute_api_step(step, execution, context)
            elif step.step_type == "quantum_optimization":
                result = await self._execute_quantum_step(step, execution, context)
            elif step.step_type == "data_analysis":
                result = await self._execute_analysis_step(step, execution, context)
            elif step.step_type == "conditional_logic":
                result = await self._execute_conditional_step(step, execution, context)
            else:
                result = await self._execute_generic_step(step, execution, context)
            
            # Update performance metrics
            execution_time = (datetime.now() - start_time).total_seconds()
            execution.performance_metrics[step.step_id] = {
                'execution_time': execution_time,
                'success': True,
                'quantum_enhanced': step.quantum_enhanced
            }
            
            if step.quantum_enhanced:
                execution.quantum_enhanced = True
            
            return result
            
        except Exception as e:
            execution.performance_metrics[step.step_id] = {
                'execution_time': (datetime.now() - start_time).total_seconds(),
                'success': False,
                'error': str(e)
            }
            raise
    
    async def _execute_rpa_step(
        self, 
        step: WorkflowStep, 
        execution: WorkflowExecution,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute RPA-style automation step (UiPath-inspired)"""
        
        config = step.config
        template = config.get('template')
        fields = config.get('fields', [])
        confidence = config.get('confidence_threshold', 0.8)
        
        # Simulate RPA execution (replace with actual RPA engine)
        extracted_data = {}
        for field in fields:
            # Simulate extraction with confidence scoring
            import random
            if field == "invoice_number":
                extracted_data[field] = f"INV-{random.randint(1000, 9999)}"
            elif field == "amount":
                extracted_data[field] = round(random.uniform(100, 10000), 2)
            elif field == "vendor":
                extracted_data[field] = f"Vendor-{random.randint(1, 100)}"
            elif field == "date":
                extracted_data[field] = datetime.now().strftime("%Y-%m-%d")
        
        return {
            'extracted_data': extracted_data,
            'confidence_scores': {field: random.uniform(confidence, 1.0) for field in fields},
            'template_used': template,
            'extraction_method': 'computer_vision'
        }
    
    async def _execute_api_step(
        self, 
        step: WorkflowStep, 
        execution: WorkflowExecution,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute API call step (n8n-inspired)"""
        
        config = step.config
        endpoint = config.get('endpoint')
        method = config.get('method', 'GET')
        data_mapping = config.get('data_mapping', {})
        
        # Resolve variables in data mapping
        resolved_data = {}
        for key, value in data_mapping.items():
            if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
                # Extract variable path
                var_path = value[2:-2].strip()
                resolved_data[key] = self._resolve_variable(var_path, execution.variables)
            else:
                resolved_data[key] = value
        
        # Simulate API call (replace with actual HTTP client)
        import random
        if endpoint == "/v1/decide":
            # Simulate lead scoring
            lead_score = random.uniform(0.3, 0.95)
            return {
                'lead_score': lead_score,
                'recommendation': self._get_recommendation(lead_score),
                'confidence': random.uniform(0.8, 1.0)
            }
        elif endpoint == "/v1/trigger_action":
            # Simulate action triggering
            action = resolved_data.get('action')
            return {
                'status': 'triggered',
                'action': action,
                'timestamp': datetime.now().isoformat(),
                'delivery_method': 'email' if 'email' in action else 'phone'
            }
        else:
            return {
                'status': 'success',
                'endpoint': endpoint,
                'method': method,
                'data': resolved_data
            }
    
    async def _execute_quantum_step(
        self, 
        step: WorkflowStep, 
        execution: WorkflowExecution,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute quantum-enhanced optimization step (DynexSolve)"""
        
        config = step.config
        algorithm = config.get('algorithm')
        target = config.get('optimization_target')
        constraints = config.get('constraints', [])
        
        # Use quantum adapter for optimization
        if algorithm == "qubo_process_mapping":
            # Process mining optimization
            result = await self.quantum_adapter.optimize_process(
                target=target,
                constraints=constraints,
                data=execution.variables
            )
        elif algorithm == "qubo_personality_optimization":
            # QDA personality optimization
            result = await self.quantum_adapter.optimize_personality(
                target=target,
                constraints=constraints,
                user_data=execution.variables
            )
        else:
            # Generic quantum optimization
            result = await self.quantum_adapter.optimize(
                objective=target,
                constraints=constraints,
                data=execution.variables
            )
        
        return {
            'optimization_result': result,
            'algorithm': algorithm,
            'quantum_enhanced': True,
            'execution_time_ms': result.get('execution_time_ms', 0)
        }
    
    async def _execute_analysis_step(
        self, 
        step: WorkflowStep, 
        execution: WorkflowExecution,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute data analysis step (Celonis-inspired)"""
        
        config = step.config
        metrics = config.get('metrics', [])
        thresholds = config.get('thresholds', {})
        
        # Simulate process analysis (replace with actual analytics engine)
        import random
        
        analysis_results = {}
        for metric in metrics:
            if metric == "cycle_time":
                analysis_results[metric] = random.uniform(2.0, 8.0)
            elif metric == "bottlenecks":
                analysis_results[metric] = random.randint(1, 5)
            elif metric == "resource_utilization":
                analysis_results[metric] = random.uniform(0.6, 0.95)
        
        # Check against thresholds
        threshold_breaches = []
        for metric, threshold in thresholds.items():
            if metric in analysis_results:
                if metric == "cycle_time_reduction" and analysis_results.get("cycle_time", 0) > threshold:
                    threshold_breaches.append(f"{metric}: {analysis_results[metric]} > {threshold}")
                elif metric == "cost_savings" and analysis_results.get("cost_savings", 0) < threshold:
                    threshold_breaches.append(f"{metric}: {analysis_results.get('cost_savings', 0)} < {threshold}")
        
        return {
            'analysis_results': analysis_results,
            'threshold_breaches': threshold_breaches,
            'recommendations': self._generate_recommendations(analysis_results, thresholds)
        }
    
    async def _execute_conditional_step(
        self, 
        step: WorkflowStep, 
        execution: WorkflowExecution,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute conditional logic step"""
        
        config = step.config
        conditions = config.get('conditions', [])
        
        # Evaluate conditions
        for condition in conditions:
            if_condition = condition.get('if')
            then_action = condition.get('then')
            
            if self._evaluate_condition(if_condition, execution.variables):
                return {
                    'result': then_action,
                    'condition_met': if_condition,
                    'action_taken': then_action
                }
        
        # Default action if no conditions met
        return {
            'result': 'default_action',
            'condition_met': None,
            'action_taken': 'default_action'
        }
    
    async def _execute_generic_step(
        self, 
        step: WorkflowStep, 
        execution: WorkflowExecution,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute generic step type"""
        
        return {
            'step_id': step.step_id,
            'step_type': step.step_type,
            'status': 'completed',
            'timestamp': datetime.now().isoformat()
        }
    
    def _resolve_variable(self, var_path: str, variables: Dict[str, Any]) -> Any:
        """Resolve variable path in execution variables"""
        try:
            # Simple variable resolution (can be enhanced)
            if var_path in variables:
                return variables[var_path]
            elif '.' in var_path:
                # Handle nested paths like "step.result"
                parts = var_path.split('.')
                current = variables
                for part in parts:
                    if isinstance(current, dict) and part in current:
                        current = current[part]
                    else:
                        return None
                return current
            else:
                return None
        except Exception:
            return None
    
    def _evaluate_condition(self, condition: str, variables: Dict[str, Any]) -> bool:
        """Evaluate a condition string against variables"""
        try:
            # Simple condition evaluation (can be enhanced with proper expression parser)
            if '>=' in condition:
                var_name, value = condition.split('>=')
                var_name = var_name.strip()
                value = float(value.strip())
                return variables.get(var_name, 0) >= value
            elif '>' in condition:
                var_name, value = condition.split('>')
                var_name = var_name.strip()
                value = float(value.strip())
                return variables.get(var_name, 0) > value
            elif '<=' in condition:
                var_name, value = condition.split('<=')
                var_name = var_name.strip()
                value = float(value.strip())
                return variables.get(var_name, 0) <= value
            elif '<' in condition:
                var_name, value = condition.split('<')
                var_name = var_name.strip()
                value = float(value.strip())
                return variables.get(var_name, 0) < value
            elif '==' in condition:
                var_name, value = condition.split('==')
                var_name = var_name.strip()
                value = value.strip().strip('"\'')
                return variables.get(var_name) == value
            else:
                return False
        except Exception:
            return False
    
    def _get_recommendation(self, lead_score: float) -> str:
        """Get recommendation based on lead score"""
        if lead_score >= 0.8:
            return "immediate_contact"
        elif lead_score >= 0.6:
            return "nurture_sequence"
        else:
            return "re_engagement"
    
    def _generate_recommendations(
        self, 
        analysis_results: Dict[str, Any], 
        thresholds: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations based on analysis results"""
        recommendations = []
        
        if analysis_results.get('cycle_time', 0) > 5.0:
            recommendations.append("Optimize process flow to reduce cycle time")
        
        if analysis_results.get('bottlenecks', 0) > 2:
            recommendations.append("Identify and resolve process bottlenecks")
        
        if analysis_results.get('resource_utilization', 0) < 0.8:
            recommendations.append("Improve resource allocation and utilization")
        
        return recommendations
    
    async def _validate_workflow(self, workflow: WorkflowDefinition) -> Dict[str, Any]:
        """Validate workflow against Q-Cortex policies"""
        try:
            errors = []
            
            # Check business unit compliance
            business_rules = self.q_cortex.get_business_rules(workflow.business_unit)
            if not business_rules:
                errors.append(f"No business rules found for unit: {workflow.business_unit}")
            
            # Check compliance requirements
            compliance_reqs = self.q_cortex.get_compliance_requirements()
            for req in compliance_reqs:
                if req.enabled and workflow.business_unit in ['finance', 'healthcare']:
                    # Additional validation for regulated industries
                    if not self._check_workflow_compliance(workflow, req):
                        errors.append(f"Compliance requirement not met: {req.framework}")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Validation error: {str(e)}"]
            }
    
    def _check_workflow_compliance(self, workflow: WorkflowDefinition, req: Any) -> bool:
        """Check if workflow meets specific compliance requirements"""
        try:
            if req.framework == "SOX":
                # SOX compliance for financial workflows
                return workflow.business_unit == "finance" and "audit_trail" in workflow.compliance_rules
            elif req.framework == "GDPR":
                # GDPR compliance for data processing
                return "data_minimization" in workflow.compliance_rules
            else:
                return True
        except Exception:
            return False
    
    def get_workflow_status(self, execution_id: str) -> Optional[WorkflowExecution]:
        """Get status of a workflow execution"""
        return self.executions.get(execution_id)
    
    def get_workflow_metrics(self, workflow_id: str) -> Dict[str, Any]:
        """Get performance metrics for a workflow"""
        executions = [e for e in self.executions.values() if e.workflow_id == workflow_id]
        
        if not executions:
            return {}
        
        total_executions = len(executions)
        successful_executions = len([e for e in executions if e.status == WorkflowStatus.COMPLETED])
        failed_executions = len([e for e in executions if e.status == WorkflowStatus.FAILED])
        
        avg_execution_time = 0
        quantum_enhanced_count = 0
        
        for execution in executions:
            if execution.end_time and execution.start_time:
                execution_time = (execution.end_time - execution.start_time).total_seconds()
                avg_execution_time += execution_time
            
            if execution.quantum_enhanced:
                quantum_enhanced_count += 1
        
        if total_executions > 0:
            avg_execution_time /= total_executions
        
        return {
            'workflow_id': workflow_id,
            'total_executions': total_executions,
            'successful_executions': successful_executions,
            'failed_executions': failed_executions,
            'success_rate': successful_executions / total_executions if total_executions > 0 else 0,
            'average_execution_time': avg_execution_time,
            'quantum_enhanced_count': quantum_enhanced_count,
            'quantum_enhancement_rate': quantum_enhanced_count / total_executions if total_executions > 0 else 0
        }
    
    def list_workflows(self, workflow_type: Optional[WorkflowType] = None) -> List[WorkflowDefinition]:
        """List available workflows, optionally filtered by type"""
        if workflow_type:
            return [w for w in self.workflows.values() if w.workflow_type == workflow_type]
        else:
            return list(self.workflows.values())
    
    def export_workflow(self, workflow_id: str) -> str:
        """Export workflow definition as YAML"""
        if workflow_id not in self.workflows:
            raise ValueError(f"Workflow {workflow_id} not found")
        
        workflow = self.workflows[workflow_id]
        
        # Convert to dict for YAML export
        workflow_dict = {
            'workflow_id': workflow.workflow_id,
            'name': workflow.name,
            'description': workflow.description,
            'workflow_type': workflow.workflow_type.value,
            'version': workflow.version,
            'business_unit': workflow.business_unit,
            'steps': [
                {
                    'step_id': step.step_id,
                    'step_type': step.step_type,
                    'name': step.name,
                    'description': step.description,
                    'config': step.config,
                    'dependencies': step.dependencies,
                    'timeout_seconds': step.timeout_seconds,
                    'retry_count': step.retry_count,
                    'quantum_enhanced': step.quantum_enhanced
                }
                for step in workflow.steps
            ],
            'triggers': workflow.triggers,
            'variables': workflow.variables,
            'compliance_rules': workflow.compliance_rules
        }
        
        return yaml.dump(workflow_dict, default_flow_style=False)
    
    async def shutdown(self):
        """Graceful shutdown of the workflow engine"""
        logger.info("Shutting down Quantum Workflow Engine")
        
        # Cancel running executions
        for execution in self.executions.values():
            if execution.status == WorkflowStatus.RUNNING:
                execution.status = WorkflowStatus.PAUSED
        
        # Log shutdown to LTC
        await self.ltc_logger.log_operation(
            operation_type="workflow_engine_shutdown",
            operation_data={
                'total_workflows': len(self.workflows),
                'total_executions': len(self.executions),
                'shutdown_time': datetime.now().isoformat()
            },
            thread_ref=f"SHUTDOWN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
