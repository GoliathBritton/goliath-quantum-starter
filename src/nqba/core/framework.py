"""NQBA Framework Core Orchestration

This module provides the main NQBAFramework class that orchestrates all
intelligence modules (qdLLM, QNLP, QTransformers) within the Neuromorphic
Quantum Business Architecture.

The framework serves as the central coordination layer that:
- Manages intelligence module interactions
- Provides unified business process interfaces
- Handles workflow orchestration
- Ensures compliance and governance
"""

import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field
import time

try:
    from .intelligence import qdllm, qnlp, qtransformers
except ImportError:
    qdllm = None
    qnlp = None
    qtransformers = None

try:
    from nqba.integration.legacy_wrapper import LegacyWrapper
except ImportError:
    LegacyWrapper = None

try:
    from nqba_stack.ltc_logger import LTCLogger
except ImportError:
    LTCLogger = None

logger = logging.getLogger(__name__)

@dataclass
class NQBAConfig:
    """Configuration for NQBA Framework"""
    enable_qdllm: bool = True
    enable_qnlp: bool = True
    enable_qtransformers: bool = True
    log_level: str = "INFO"
    max_concurrent_requests: int = 100
    timeout_seconds: int = 30
    governance_enabled: bool = True
    compliance_checks: bool = True
    performance_monitoring: bool = True
    custom_settings: Dict[str, Any] = field(default_factory=dict)

class NQBAFramework:
    """Neuromorphic Quantum Business Architecture Framework
    
    The main orchestration class that coordinates all intelligence modules
    and provides unified interfaces for business applications.
    """
    
    def __init__(self, config: Optional[NQBAConfig] = None):
        """Initialize NQBA Framework
        
        Args:
            config: Framework configuration. If None, uses default config.
        """
        self.config = config or NQBAConfig()
        self._setup_logging()
        self._initialize_modules()
        self._setup_governance()
        
        if LTCLogger is not None:
            self.ltc_logger = LTCLogger()
        else:
            self.ltc_logger = None
            logger.warning("LTCLogger not available")
        
        logger.info("NQBA Framework initialized successfully")
    
    def _setup_logging(self):
        """Setup framework logging"""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _initialize_modules(self):
        """Initialize intelligence modules"""
        self.modules = {}
        
        if self.config.enable_qdllm and qdllm is not None:
            try:
                self.modules['qdllm'] = qdllm.create_engine()
                logger.info("qdLLM module initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize qdLLM: {e}")
        
        if self.config.enable_qnlp and qnlp is not None:
            try:
                self.modules['qnlp'] = qnlp.create_processor()
                logger.info("QNLP module initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize QNLP: {e}")
        
        if self.config.enable_qtransformers and qtransformers is not None:
            try:
                self.modules['qtransformers'] = qtransformers.create_model()
                logger.info("QTransformers module initialized")
            except Exception as e:
                logger.warning(f"Failed to initialize QTransformers: {e}")
            
            if LegacyWrapper is not None:
                try:
                    self.modules['legacy_wrapper'] = LegacyWrapper()
                    logger.info("Legacy Wrapper module initialized")
                except Exception as e:
                    logger.warning(f"Failed to initialize Legacy Wrapper: {e}")
    
    def _setup_governance(self):
        """Setup governance and compliance"""
        self.governance = {
            'compliance_enabled': self.config.compliance_checks,
            'monitoring_enabled': self.config.performance_monitoring,
            'audit_trail': [],
            'policy_violations': []
        }
    
    def process_business_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a business request through the NQBA framework
        
        Args:
            request: Business request containing type, data, and parameters
            
        Returns:
            Processed response with results and metadata
        """
        request_type = request.get('type', 'general')
        data = request.get('data', '')
        params = request.get('params', {})
        
        logger.info(f"Processing business request: {request_type}")
        
        # Route request to appropriate intelligence modules
        if request_type == 'text_analysis':
            return self._process_text_analysis(data, params)
        elif request_type == 'reasoning':
            return self._process_reasoning(data, params)
        elif request_type == 'pattern_analysis':
            return self._process_pattern_analysis(data, params)
        elif request_type == 'integrated_workflow':
            return self._process_integrated_workflow(data, params)
        elif request_type == 'legacy_integration':
            return self._process_legacy_integration(data, params)
        else:
            return self._process_general_request(data, params)
    
    def _process_text_analysis(self, text: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process text analysis request using QNLP"""
        if 'qnlp' not in self.modules:
            return {'error': 'QNLP module not available'}
        
        try:
            result = qnlp.analyze(text, processor=self.modules['qnlp'], **params)
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="text_analysis",
                    component="QNLP",
                    input_data={"text": text, "params": params},
                    result_data=result
                )
            return {
                'status': 'success',
                'type': 'text_analysis',
                'result': result,
                'module': 'qnlp'
            }
        except Exception as e:
            logger.error(f"Text analysis failed: {e}")
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="text_analysis",
                    component="QNLP",
                    input_data={"text": text, "params": params},
                    error_data={"error": str(e)}
                )
            return {'error': str(e), 'status': 'failed'}
    
    def _process_reasoning(self, context: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process reasoning request using qdLLM"""
        if 'qdllm' not in self.modules:
            return {'error': 'qdLLM module not available'}
        
        try:
            direction = params.get('direction', 'bidirectional')
            result = qdllm.reason(context, direction=direction, **params)
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="reasoning",
                    component="qdLLM",
                    input_data={"context": context, "params": params},
                    result_data=result
                )
            return {
                'status': 'success',
                'type': 'reasoning',
                'result': result,
                'module': 'qdllm'
            }
        except Exception as e:
            logger.error(f"Reasoning failed: {e}")
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="reasoning",
                    component="qdLLM",
                    input_data={"context": context, "params": params},
                    error_data={"error": str(e)}
                )
            return {'error': str(e), 'status': 'failed'}
    
    def _process_pattern_analysis(self, sequence: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process pattern analysis request using QTransformers"""
        if 'qtransformers' not in self.modules:
            return {'error': 'QTransformers module not available'}
        
        try:
            result = qtransformers.analyze_patterns(sequence, **params)
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="pattern_analysis",
                    component="QTransformers",
                    input_data={"sequence": sequence, "params": params},
                    result_data=result
                )
            return {
                'status': 'success',
                'type': 'pattern_analysis',
                'result': result,
                'module': 'qtransformers'
            }
        except Exception as e:
            logger.error(f"Pattern analysis failed: {e}")
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="pattern_analysis",
                    component="QTransformers",
                    input_data={"sequence": sequence, "params": params},
                    error_data={"error": str(e)}
                )
            return {'error': str(e), 'status': 'failed'}
    
    def _process_integrated_workflow(self, data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process integrated workflow using multiple modules"""
        workflow_steps = params.get('steps', ['qnlp', 'qdllm', 'qtransformers'])
        results = {}
        
        current_data = data
        
        for step in workflow_steps:
            if step == 'qnlp' and 'qnlp' in self.modules:
                try:
                    result = qnlp.analyze(str(current_data), processor=self.modules['qnlp'])
                    results['qnlp'] = result
                    current_data = result
                except Exception as e:
                    results['qnlp'] = {'error': str(e)}
            
            elif step == 'qdllm' and 'qdllm' in self.modules:
                try:
                    result = qdllm.reason(str(current_data))
                    results['qdllm'] = result
                    current_data = result
                except Exception as e:
                    results['qdllm'] = {'error': str(e)}
            
            elif step == 'qtransformers' and 'qtransformers' in self.modules:
                try:
                    result = qtransformers.optimize(current_data, model=self.modules['qtransformers'])
                    results['qtransformers'] = result
                    current_data = result
                except Exception as e:
                    results['qtransformers'] = {'error': str(e)}
        
        if self.ltc_logger:
            self.ltc_logger.log_operation(
                operation_type="integrated_workflow",
                component="NQBAFramework",
                input_data={"data": data, "params": params},
                result_data=results
            )
        
        return {
            'status': 'success',
            'type': 'integrated_workflow',
            'results': results,
            'final_output': current_data
        }
    
    def _process_legacy_integration(self, data: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process legacy integration request using LegacyWrapper"""
        if 'legacy_wrapper' not in self.modules:
            return {'error': 'Legacy Wrapper module not available'}
        
        try:
            system_type = params.get('system_type', 'generic')
            if 'analyze' in params.get('action', 'translate'):
                result = self.modules['legacy_wrapper'].analyze_legacy_system(data, system_type)
            elif 'execute' in params.get('action', 'translate'):
                result = self.modules['legacy_wrapper'].execute_legacy_command(data, system_type)
            else:
                result = self.modules['legacy_wrapper'].translate_api_call(data, system_type)
            
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="legacy_integration",
                    component="LegacyWrapper",
                    input_data={"data": data, "params": params},
                    result_data=result
                )
            
            return {
                'status': 'success',
                'type': 'legacy_integration',
                'result': result,
                'module': 'legacy_wrapper'
            }
        except Exception as e:
            logger.error(f"Legacy integration failed: {e}")
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="legacy_integration",
                    component="LegacyWrapper",
                    input_data={"data": data, "params": params},
                    error_data={"error": str(e)}
                )
            return {'error': str(e), 'status': 'failed'}
    
    def _process_general_request(self, data: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Process general request with automatic module selection"""
        # Simple heuristic for module selection
        if isinstance(data, str) and len(data) > 0:
            # Text data - use QNLP first, then qdLLM
            qnlp_result = None
            if 'qnlp' in self.modules:
                try:
                    qnlp_result = qnlp.analyze(data, processor=self.modules['qnlp'])
                except Exception as e:
                    logger.warning(f"QNLP processing failed: {e}")
            
            qdllm_result = None
            if 'qdllm' in self.modules:
                try:
                    qdllm_result = qdllm.reason(data)
                except Exception as e:
                    logger.warning(f"qdLLM processing failed: {e}")
            
            result = {
                'status': 'success',
                'type': 'general',
                'qnlp_result': qnlp_result,
                'qdllm_result': qdllm_result
            }
            
            if self.ltc_logger:
                self.ltc_logger.log_operation(
                    operation_type="general_request",
                    component="NQBAFramework",
                    input_data={"data": data, "params": params},
                    result_data=result
                )
            
            return result
        
        return {'error': 'Unable to process request', 'status': 'failed'}
    
    def get_module_status(self) -> Dict[str, Any]:
        """Get status of all intelligence modules"""
        return {
            'qdllm': 'available' if 'qdllm' in self.modules else 'unavailable',
            'qnlp': 'available' if 'qnlp' in self.modules else 'unavailable',
            'qtransformers': 'available' if 'qtransformers' in self.modules else 'unavailable',
            'legacy_wrapper': 'available' if 'legacy_wrapper' in self.modules else 'unavailable',
            'total_modules': len(self.modules),
            'framework_status': 'operational' if self.modules else 'degraded'
        }
    
    def get_governance_report(self) -> Dict[str, Any]:
        """Get governance and compliance report"""
        return {
            'compliance_enabled': self.governance['compliance_enabled'],
            'monitoring_enabled': self.governance['monitoring_enabled'],
            'audit_entries': len(self.governance['audit_trail']),
            'policy_violations': len(self.governance['policy_violations']),
            'framework_health': 'healthy' if not self.governance['policy_violations'] else 'attention_required'
        }

# Factory function for easy framework creation
def create_nqba_framework(**config_kwargs) -> NQBAFramework:
    """Create NQBA Framework with custom configuration"""
    config = NQBAConfig(**config_kwargs)
    return NQBAFramework(config)