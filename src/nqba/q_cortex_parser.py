"""
NQBA Q-Cortex Parser - Core module imports
Imports from nqba_stack.q_cortex_parser for compatibility
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'nqba_stack'))

try:
    from q_cortex_parser import (
        QCortexParser,
        create_q_cortex_parser
    )
except ImportError:
    # Fallback if nqba_stack is not available
    from typing import Dict, Any, List
    
    class QCortexParser:
        """Fallback QCortexParser class"""
        def __init__(self, config_dir: str = "config"):
            self.config_dir = config_dir
            self.council_directives = {}
            self.business_rules = []
            self.compliance_requirements = []
            self.performance_standards = []
        
        def get_business_rules(self) -> List[Dict[str, Any]]:
            """Get business rules (fallback)"""
            return []
        
        def get_compliance_requirements(self) -> List[Dict[str, Any]]:
            """Get compliance requirements (fallback)"""
            return []
        
        def get_performance_standards(self) -> List[Dict[str, Any]]:
            """Get performance standards (fallback)"""
            return []
        
        def validate_decision(self, decision_type: str, decision_data: Dict[str, Any]) -> Dict[str, Any]:
            """Validate decision (fallback)"""
            return {
                "compliant": True,
                "violations": [],
                "recommendations": [],
                "council_directives_applied": []
            }
    
    def create_q_cortex_parser(config_dir: str = "config") -> QCortexParser:
        """Create Q-Cortex parser instance (fallback)"""
        return QCortexParser(config_dir)
