"""
Q-Cortex Parser
High Council → Q-Cortex → NQBA Core → Agent Mesh → SaaS

This module parses Council Directives YAML files and converts them into
enforceable policies that NQBA Core can execute.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class CouncilDirective:
    """Represents a single council directive with its enforcement rules."""
    name: str
    category: str
    value: Any
    priority: int = 1
    enforcement_level: str = "mandatory"
    validation_rules: List[str] = field(default_factory=list)
    override_required: bool = False
    ltc_logging: bool = True


@dataclass
class BusinessRule:
    """Represents a business rule derived from council directives."""
    rule_id: str
    rule_type: str
    conditions: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int = 1
    source_directive: str = ""
    validation_schema: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceRequirement:
    """Represents a compliance requirement from council directives."""
    framework: str
    requirement: str
    enabled: bool
    validation_method: str
    audit_frequency: str
    escalation_path: str


class QCortexParser:
    """
    Q-Cortex Parser that converts Council Directives YAML into enforceable policies.
    
    This class reads the council.yaml file and converts it into:
    1. Enforceable business rules
    2. Compliance requirements
    3. Performance standards
    4. Risk management policies
    """
    
    def __init__(self, config_dir: str = "config"):
        """Initialize the Q-Cortex parser with configuration directory."""
        self.config_dir = Path(config_dir)
        self.council_directives: Dict[str, CouncilDirective] = {}
        self.business_rules: List[BusinessRule] = []
        self.compliance_requirements: List[ComplianceRequirement] = []
        self.performance_standards: Dict[str, Any] = {}
        self.risk_policies: Dict[str, Any] = {}
        
        # Load council directives
        self._load_council_directives()
        self._parse_directives()
    
    def _load_council_directives(self) -> None:
        """Load council directives from YAML files."""
        council_file = self.config_dir / "council.yaml"
        sigma_select_file = self.config_dir / "sigma_select_rules.yaml"
        
        if not council_file.exists():
            logger.warning(f"Council directives file not found: {council_file}")
            return
        
        try:
            with open(council_file, 'r', encoding='utf-8') as f:
                council_data = yaml.safe_load(f)
                self._parse_council_yaml(council_data)
        except Exception as e:
            logger.error(f"Error loading council directives: {e}")
        
        if sigma_select_file.exists():
            try:
                with open(sigma_select_file, 'r', encoding='utf-8') as f:
                    sigma_data = yaml.safe_load(f)
                    self._parse_sigma_select_yaml(sigma_data)
            except Exception as e:
                logger.error(f"Error loading Sigma Select rules: {e}")
    
    def _parse_council_yaml(self, data: Dict[str, Any]) -> None:
        """Parse the main council YAML file."""
        # Parse core principles
        if 'principles' in data:
            for i, principle in enumerate(data['principles']):
                directive = CouncilDirective(
                    name=principle,
                    category="principle",
                    value=True,
                    priority=i + 1,
                    enforcement_level="mandatory"
                )
                self.council_directives[principle] = directive
        
        # Parse compliance requirements
        if 'compliance' in data:
            for framework, requirements in data['compliance'].items():
                if isinstance(requirements, dict) and 'enabled' in requirements:
                    compliance_req = ComplianceRequirement(
                        framework=framework,
                        requirement=str(requirements),
                        enabled=requirements.get('enabled', False),
                        validation_method=requirements.get('validation_method', 'automated'),
                        audit_frequency=requirements.get('audit_frequency', 'monthly'),
                        escalation_path=requirements.get('escalation_path', 'council_review')
                    )
                    self.compliance_requirements.append(compliance_req)
        
        # Parse performance standards
        if 'performance_standards' in data:
            self.performance_standards = data['performance_standards']
        
        # Parse risk management
        if 'risk_management' in data:
            self.risk_policies = data['risk_management']
    
    def _parse_sigma_select_yaml(self, data: Dict[str, Any]) -> None:
        """Parse Sigma Select business rules YAML."""
        if 'lead_scoring' in data:
            scoring_data = data['lead_scoring']
            
            # Create lead scoring business rule
            lead_scoring_rule = BusinessRule(
                rule_id="sigma_select_lead_scoring",
                rule_type="lead_scoring",
                conditions={
                    "algorithm": scoring_data.get('algorithm', 'hybrid_quantum_classical'),
                    "scoring_range": scoring_data.get('scoring_range', [0, 100]),
                    "quantum_threshold": scoring_data.get('quantum_threshold', 75)
                },
                actions={
                    "factors": scoring_data.get('factors', {}),
                    "advanced_rules": scoring_data.get('advanced_rules', {}),
                    "classification": data.get('lead_classification', {})
                },
                priority=1,
                source_directive="sigma_select_business_rules"
            )
            self.business_rules.append(lead_scoring_rule)
            
            # Create next best action rule
            if 'next_best_action' in data:
                nba_rule = BusinessRule(
                    rule_id="sigma_select_next_best_action",
                    rule_type="next_best_action",
                    conditions={
                        "lead_classification": list(data['next_best_action'].keys())
                    },
                    actions=data['next_best_action'],
                    priority=2,
                    source_directive="sigma_select_business_rules"
                )
                self.business_rules.append(nba_rule)
    
    def _parse_directives(self) -> None:
        """Parse all directives into enforceable policies."""
        # Convert principles into business rules
        for directive in self.council_directives.values():
            if directive.category == "principle":
                rule = BusinessRule(
                    rule_id=f"principle_{directive.name}",
                    rule_type="principle",
                    conditions={"principle": directive.name},
                    actions={"enforce": directive.value},
                    priority=directive.priority,
                    source_directive="council_directives"
                )
                self.business_rules.append(rule)
    
    def get_business_rules(self, rule_type: Optional[str] = None) -> List[BusinessRule]:
        """Get business rules, optionally filtered by type."""
        if rule_type:
            return [rule for rule in self.business_rules if rule.rule_type == rule_type]
        return self.business_rules
    
    def get_compliance_requirements(self, framework: Optional[str] = None) -> List[ComplianceRequirement]:
        """Get compliance requirements, optionally filtered by framework."""
        if framework:
            return [req for req in self.compliance_requirements if req.framework == framework]
        return self.compliance_requirements
    
    def get_performance_standards(self) -> Dict[str, Any]:
        """Get performance standards from council directives."""
        return self.performance_standards
    
    def get_risk_policies(self) -> Dict[str, Any]:
        """Get risk management policies from council directives."""
        return self.risk_policies
    
    def validate_decision(self, decision_type: str, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a decision against council directives.
        
        Args:
            decision_type: Type of decision being made
            decision_data: Data associated with the decision
            
        Returns:
            Validation result with compliance status and recommendations
        """
        validation_result = {
            "compliant": True,
            "violations": [],
            "recommendations": [],
            "council_directives_applied": []
        }
        
        # Check against business rules
        applicable_rules = [rule for rule in self.business_rules if rule.rule_type == decision_type]
        
        for rule in applicable_rules:
            # Apply rule validation logic here
            # This is a simplified implementation
            validation_result["council_directives_applied"].append(rule.source_directive)
        
        # Check against compliance requirements
        for req in self.compliance_requirements:
            if req.enabled and req.framework in decision_type.lower():
                # Apply compliance validation logic here
                pass
        
        return validation_result
    
    def get_ltc_logging_requirements(self) -> Dict[str, Any]:
        """Get LTC logging requirements from council directives."""
        # This would extract LTC requirements from the council directives
        # For now, return a default structure
        return {
            "mandatory_logging": [
                "all_business_decisions",
                "all_quantum_operations",
                "all_agent_interactions",
                "all_compliance_checks",
                "all_performance_metrics"
            ],
            "log_format": "jsonl",
            "storage_backend": "postgresql",
            "backup_strategy": "ipfs_decentralized",
            "retention_policy": "permanent",
            "hash_chaining": True,
            "thread_references": True
        }
    
    def get_emergency_overrides(self) -> Dict[str, Any]:
        """Get emergency override policies from council directives."""
        # This would extract emergency override policies
        # For now, return a default structure
        return {
            "quantum_shutdown": {
                "trigger": "energy_consumption_exceeds_limit",
                "action": "immediate_fallback_to_classical",
                "notification": "immediate"
            },
            "compliance_breach": {
                "trigger": "regulatory_violation_detected",
                "action": "halt_all_operations",
                "notification": "immediate"
            }
        }


def create_q_cortex_parser(config_dir: str = "config") -> QCortexParser:
    """
    Factory function to create a Q-Cortex parser instance.
    
    Args:
        config_dir: Directory containing configuration files
        
    Returns:
        Configured QCortexParser instance
    """
    return QCortexParser(config_dir)


# Example usage and testing
if __name__ == "__main__":
    # Create parser instance
    parser = create_q_cortex_parser()
    
    # Print parsed information
    print("=== Q-Cortex Parser Test ===")
    print(f"Business Rules: {len(parser.get_business_rules())}")
    print(f"Compliance Requirements: {len(parser.get_compliance_requirements())}")
    print(f"Performance Standards: {len(parser.get_performance_standards())}")
    
    # Test validation
    test_decision = {
        "decision_type": "lead_scoring",
        "lead_score": 85,
        "company_size": "enterprise"
    }
    
    validation = parser.validate_decision("lead_scoring", test_decision)
    print(f"\nValidation Result: {validation}")
