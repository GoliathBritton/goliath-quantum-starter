"""
Base Agent Class - Foundation for All NQBA Agents
Implements Q-Cortex compliance, LTC logging, and automation capabilities
"""

import asyncio
import json
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
import logging

from ..q_cortex_parser import QCortexParser
from ..ltc_logger import LTCLogger
from ..decision_logic import DecisionLogicEngine

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    """Agent operational status"""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"
    LEARNING = "learning"

class AgentCapability(Enum):
    """Agent capability types"""
    DECISION_MAKING = "decision_making"
    DATA_PROCESSING = "data_processing"
    COMMUNICATION = "communication"
    AUTOMATION = "automation"
    OPTIMIZATION = "optimization"
    MONITORING = "monitoring"

@dataclass
class AgentContext:
    """Context for agent operations"""
    business_unit: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    priority: int = 1
    constraints: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class AgentResult:
    """Standardized result from agent operations"""
    success: bool
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    ltc_reference: Optional[str] = None
    execution_time_ms: float = 0.0
    quantum_enhanced: bool = False
    compliance_status: str = "compliant"

class BaseAgent(ABC):
    """
    Base class for all NQBA agents
    Provides Q-Cortex compliance, LTC logging, and automation framework
    """
    
    def __init__(
        self,
        agent_id: str,
        agent_type: str,
        capabilities: List[AgentCapability],
        q_cortex: QCortexParser,
        ltc_logger: LTCLogger,
        decision_engine: DecisionLogicEngine
    ):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.capabilities = capabilities
        self.q_cortex = q_cortex
        self.ltc_logger = ltc_logger
        self.decision_engine = decision_engine
        
        # Operational state
        self.status = AgentStatus.IDLE
        self.context: Optional[AgentContext] = None
        self.performance_metrics = {
            'total_operations': 0,
            'successful_operations': 0,
            'average_execution_time': 0.0,
            'last_operation': None
        }
        
        # Compliance tracking
        self.compliance_checks = []
        self.policy_violations = []
        
        logger.info(f"Initialized agent {agent_id} of type {agent_type}")
    
    @abstractmethod
    async def process_request(self, request: Dict[str, Any], context: AgentContext) -> AgentResult:
        """Process incoming requests - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    async def validate_input(self, request: Dict[str, Any]) -> bool:
        """Validate input data - must be implemented by subclasses"""
        pass
    
    async def execute_with_compliance(
        self, 
        request: Dict[str, Any], 
        context: AgentContext
    ) -> AgentResult:
        """
        Execute agent operation with full Q-Cortex compliance and LTC logging
        """
        start_time = datetime.now()
        
        try:
            # Update status
            self.status = AgentStatus.BUSY
            self.context = context
            
            # Validate input
            if not await self.validate_input(request):
                return AgentResult(
                    success=False,
                    data="Input validation failed",
                    metadata={'validation_errors': self.get_validation_errors()}
                )
            
            # Check Q-Cortex compliance
            compliance_result = await self.check_compliance(request, context)
            if not compliance_result['compliant']:
                return AgentResult(
                    success=False,
                    data="Compliance check failed",
                    metadata={'compliance_errors': compliance_result['errors']}
                )
            
            # Execute core logic
            result = await self.process_request(request, context)
            
            # Log to LTC
            ltc_reference = await self.log_operation(request, context, result)
            result.ltc_reference = ltc_reference
            
            # Update metrics
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self.update_performance_metrics(result.success, execution_time)
            
            return result
            
        except Exception as e:
            logger.error(f"Agent {self.agent_id} execution error: {str(e)}")
            self.status = AgentStatus.ERROR
            
            return AgentResult(
                success=False,
                data=f"Execution error: {str(e)}",
                metadata={'error_type': type(e).__name__}
            )
        
        finally:
            self.status = AgentStatus.IDLE
            self.context = None
    
    async def check_compliance(self, request: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """Check request compliance against Q-Cortex policies"""
        try:
            # Get relevant business rules
            business_rules = self.q_cortex.get_business_rules(self.agent_type)
            
            # Validate against each rule
            compliance_errors = []
            for rule in business_rules:
                if not self.validate_rule(rule, request, context):
                    compliance_errors.append({
                        'rule_id': rule.rule_id,
                        'violation': f"Rule {rule.rule_id} validation failed"
                    })
            
            # Check compliance requirements
            compliance_reqs = self.q_cortex.get_compliance_requirements()
            for req in compliance_reqs:
                if req.enabled and not self.check_compliance_requirement(req, request):
                    compliance_errors.append({
                        'framework': req.framework,
                        'violation': f"{req.framework} requirement not met"
                    })
            
            return {
                'compliant': len(compliance_errors) == 0,
                'errors': compliance_errors
            }
            
        except Exception as e:
            logger.error(f"Compliance check error: {str(e)}")
            return {
                'compliant': False,
                'errors': [{'error': str(e)}]
            }
    
    def validate_rule(self, rule: Any, request: Dict[str, Any], context: AgentContext) -> bool:
        """Validate request against a specific business rule"""
        try:
            # Simple rule validation - can be extended
            if rule.rule_type == "condition_check":
                return self.evaluate_condition(rule.conditions, request, context)
            elif rule.rule_type == "data_validation":
                return self.validate_data_schema(rule.validation_schema, request)
            else:
                return True  # Unknown rule type, assume compliant
        except Exception:
            return False
    
    def evaluate_condition(self, conditions: Dict[str, Any], request: Dict[str, Any], context: AgentContext) -> bool:
        """Evaluate business rule conditions"""
        try:
            for field, expected in conditions.items():
                if field in request:
                    if not self.matches_condition(request[field], expected):
                        return False
                elif field in context.metadata:
                    if not self.matches_condition(context.metadata[field], expected):
                        return False
                else:
                    return False  # Required field missing
            return True
        except Exception:
            return False
    
    def matches_condition(self, actual: Any, expected: Any) -> bool:
        """Check if actual value matches expected condition"""
        if isinstance(expected, dict):
            if 'min' in expected and actual < expected['min']:
                return False
            if 'max' in expected and actual > expected['max']:
                return False
            if 'equals' in expected and actual != expected['equals']:
                return False
            if 'in' in expected and actual not in expected['in']:
                return False
        else:
            return actual == expected
        return True
    
    def validate_data_schema(self, schema: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Validate data against schema"""
        try:
            for field, field_schema in schema.items():
                if field not in data:
                    if field_schema.get('required', False):
                        return False
                    continue
                
                value = data[field]
                if 'type' in field_schema:
                    if not isinstance(value, eval(field_schema['type'])):
                        return False
                
                if 'pattern' in field_schema:
                    import re
                    if not re.match(field_schema['pattern'], str(value)):
                        return False
            
            return True
        except Exception:
            return False
    
    def check_compliance_requirement(self, req: Any, request: Dict[str, Any]) -> bool:
        """Check specific compliance requirement"""
        try:
            if req.framework == "GDPR":
                return self.check_gdpr_compliance(request)
            elif req.framework == "HIPAA":
                return self.check_hipaa_compliance(request)
            elif req.framework == "SOX":
                return self.check_sox_compliance(request)
            else:
                return True  # Unknown framework, assume compliant
        except Exception:
            return False
    
    def check_gdpr_compliance(self, request: Dict[str, Any]) -> bool:
        """Basic GDPR compliance check"""
        # Check for personal data handling
        personal_data_fields = ['email', 'phone', 'address', 'ssn', 'credit_card']
        for field in personal_data_fields:
            if field in request and request[field]:
                # Ensure consent and purpose are documented
                if 'consent_given' not in request or 'purpose' not in request:
                    return False
        return True
    
    def check_hipaa_compliance(self, request: Dict[str, Any]) -> bool:
        """Basic HIPAA compliance check"""
        # Check for health information
        health_fields = ['medical_record', 'diagnosis', 'treatment', 'medication']
        for field in health_fields:
            if field in request and request[field]:
                # Ensure authorization and minimum necessary
                if 'authorization' not in request or 'minimum_necessary' not in request:
                    return False
        return True
    
    def check_sox_compliance(self, request: Dict[str, Any]) -> bool:
        """Basic SOX compliance check"""
        # Check for financial data
        financial_fields = ['revenue', 'expenses', 'assets', 'liabilities']
        for field in financial_fields:
            if field in request and request[field]:
                # Ensure audit trail and controls
                if 'audit_trail' not in request or 'internal_controls' not in request:
                    return False
        return True
    
    async def log_operation(self, request: Dict[str, Any], context: AgentContext, result: AgentResult) -> str:
        """Log operation to LTC with full provenance"""
        try:
            operation_data = {
                'agent_id': self.agent_id,
                'agent_type': self.agent_type,
                'operation_type': 'agent_execution',
                'request': request,
                'context': {
                    'business_unit': context.business_unit,
                    'user_id': context.user_id,
                    'session_id': context.session_id,
                    'priority': context.priority
                },
                'result': {
                    'success': result.success,
                    'execution_time_ms': result.execution_time_ms,
                    'quantum_enhanced': result.quantum_enhanced
                },
                'compliance_status': result.compliance_status,
                'timestamp': datetime.now().isoformat()
            }
            
            ltc_reference = await self.ltc_logger.log_operation(
                operation_type="agent_execution",
                operation_data=operation_data,
                thread_ref=f"AGENT_{self.agent_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            return ltc_reference
            
        except Exception as e:
            logger.error(f"LTC logging error: {str(e)}")
            return f"LTC_ERROR_{hash(str(e))}"
    
    def update_performance_metrics(self, success: bool, execution_time: float):
        """Update agent performance metrics"""
        self.performance_metrics['total_operations'] += 1
        if success:
            self.performance_metrics['successful_operations'] += 1
        
        # Update average execution time
        current_avg = self.performance_metrics['average_execution_time']
        total_ops = self.performance_metrics['total_operations']
        self.performance_metrics['average_execution_time'] = (
            (current_avg * (total_ops - 1) + execution_time) / total_ops
        )
        
        self.performance_metrics['last_operation'] = datetime.now().isoformat()
    
    def get_validation_errors(self) -> List[str]:
        """Get validation errors from the agent"""
        # Can be overridden by subclasses
        return []
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get agent health and performance status"""
        return {
            'agent_id': self.agent_id,
            'agent_type': self.agent_type,
            'status': self.status.value,
            'capabilities': [cap.value for cap in self.capabilities],
            'performance_metrics': self.performance_metrics,
            'compliance_status': {
                'total_checks': len(self.compliance_checks),
                'violations': len(self.policy_violations)
            },
            'last_operation': self.performance_metrics['last_operation']
        }
    
    async def shutdown(self):
        """Graceful shutdown of the agent"""
        logger.info(f"Shutting down agent {self.agent_id}")
        self.status = AgentStatus.OFFLINE
        # Cleanup resources
        await self.cleanup()
    
    async def cleanup(self):
        """Cleanup agent resources - can be overridden"""
        pass
