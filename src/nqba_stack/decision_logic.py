"""
Decision Logic Engine - Business Rule Processing and Optimization

This module provides intelligent decision-making capabilities for the NQBA platform,
including business rule processing, optimization strategy selection, and
context-aware decision routing.
"""

import asyncio
import logging
import time
import json
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum
import numpy as np

logger = logging.getLogger(__name__)

class DecisionType(Enum):
    """Types of decisions the engine can make"""
    OPTIMIZATION = "optimization"
    ROUTING = "routing"
    RESOURCE_ALLOCATION = "resource_allocation"
    BUSINESS_RULE = "business_rule"
    QUANTUM_STRATEGY = "quantum_strategy"

class OptimizationStrategy(Enum):
    """Available optimization strategies"""
    QUANTUM_ANNEALING = "quantum_annealing"
    QAOA = "qaoa"
    VQE = "vqe"
    HEURISTIC = "heuristic"
    HYBRID = "hybrid"

@dataclass
class DecisionContext:
    """Context for decision making"""
    user_id: str
    session_id: str
    business_context: str
    priority: str = "normal"
    constraints: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class DecisionResult:
    """Result from decision logic processing"""
    success: bool
    decision_type: str
    strategy_selected: str
    reasoning: str
    execution_time: float = 0.0
    confidence_score: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

@dataclass
class BusinessRule:
    """Business rule definition"""
    rule_id: str
    name: str
    description: str
    conditions: Dict[str, Any]
    actions: List[Dict[str, Any]]
    priority: int = 1
    active: bool = True

class DecisionLogicEngine:
    """Intelligent decision-making engine for NQBA"""
    
    def __init__(self, 
                 max_qubits: int = 64,
                 enable_optimization: bool = True,
                 rule_engine_enabled: bool = True):
        """Initialize decision logic engine
        
        Args:
            max_qubits: Maximum number of qubits supported
            enable_optimization: Enable optimization strategy selection
            rule_engine_enabled: Enable business rule processing
        """
        self.max_qubits = max_qubits
        self.enable_optimization = enable_optimization
        self.rule_engine_enabled = rule_engine_enabled
        
        # Initialize components
        self.business_rules: List[BusinessRule] = []
        self.optimization_strategies: Dict[str, Dict[str, Any]] = {}
        self.decision_history: List[DecisionResult] = []
        
        # Load default rules and strategies
        self._load_default_rules()
        self._load_optimization_strategies()
        
        logger.info("Decision logic engine initialized successfully")
    
    def _load_default_rules(self):
        """Load default business rules"""
        default_rules = [
            BusinessRule(
                rule_id="rule_001",
                name="Lead Scoring Priority",
                description="Prioritize high-value leads for quantum optimization",
                conditions={
                    "context": "lead_scoring",
                    "data_size": {"operator": ">", "value": 100}
                },
                actions=[
                    {"action": "use_quantum_optimization", "parameters": {"algorithm": "qaoa"}},
                    {"action": "set_priority", "parameters": {"level": "high"}}
                ],
                priority=1
            ),
            BusinessRule(
                rule_id="rule_002",
                name="Resource Conservation",
                description="Use heuristic methods for small problems to conserve quantum resources",
                conditions={
                    "data_size": {"operator": "<=", "value": 50},
                    "priority": {"operator": "==", "value": "low"}
                },
                actions=[
                    {"action": "use_heuristic_optimization", "parameters": {"method": "simulated_annealing"}}
                ],
                priority=2
            ),
            BusinessRule(
                rule_id="rule_003",
                name="Performance Optimization",
                description="Use hybrid approaches for medium-sized problems",
                conditions={
                    "data_size": {"operator": ">", "value": 50},
                    "data_size": {"operator": "<=", "value": 200},
                    "priority": {"operator": "==", "value": "medium"}
                },
                actions=[
                    {"action": "use_hybrid_optimization", "parameters": {"quantum_ratio": 0.3}}
                ],
                priority=3
            )
        ]
        
        self.business_rules.extend(default_rules)
        logger.info(f"Loaded {len(default_rules)} default business rules")
    
    def _load_optimization_strategies(self):
        """Load available optimization strategies"""
        self.optimization_strategies = {
            OptimizationStrategy.QUANTUM_ANNEALING.value: {
                "name": "Quantum Annealing",
                "description": "Quantum annealing for discrete optimization problems",
                "best_for": ["qubo", "ising", "discrete_optimization"],
                "qubit_requirements": {"min": 2, "max": 1000},
                "execution_time": {"min": 0.1, "max": 10.0},
                "accuracy": 0.95,
                "cost_factor": 1.0
            },
            OptimizationStrategy.QAOA.value: {
                "name": "Quantum Approximate Optimization Algorithm",
                "description": "QAOA for approximate optimization",
                "best_for": ["qubo", "maxcut", "graph_optimization"],
                "qubit_requirements": {"min": 4, "max": 100},
                "execution_time": {"min": 1.0, "max": 60.0},
                "accuracy": 0.90,
                "cost_factor": 1.2
            },
            OptimizationStrategy.VQE.value: {
                "name": "Variational Quantum Eigensolver",
                "description": "VQE for eigenvalue problems",
                "best_for": ["chemistry", "eigenvalue", "ground_state"],
                "qubit_requirements": {"min": 2, "max": 50},
                "execution_time": {"min": 5.0, "max": 300.0},
                "accuracy": 0.85,
                "cost_factor": 1.5
            },
            OptimizationStrategy.HEURISTIC.value: {
                "name": "Heuristic Optimization",
                "description": "Classical heuristic methods",
                "best_for": ["general", "small_problems", "quick_results"],
                "qubit_requirements": {"min": 0, "max": 0},
                "execution_time": {"min": 0.01, "max": 1.0},
                "accuracy": 0.80,
                "cost_factor": 0.1
            },
            OptimizationStrategy.HYBRID.value: {
                "name": "Hybrid Quantum-Classical",
                "description": "Combination of quantum and classical methods",
                "best_for": ["large_problems", "balanced_approach"],
                "qubit_requirements": {"min": 2, "max": 200},
                "execution_time": {"min": 0.5, "max": 30.0},
                "accuracy": 0.88,
                "cost_factor": 0.8
            }
        }
        
        logger.info(f"Loaded {len(self.optimization_strategies)} optimization strategies")
    
    async def make_decision(self, 
                           decision_type: DecisionType,
                           context: DecisionContext,
                           data: Optional[Dict[str, Any]] = None) -> DecisionResult:
        """Make a decision based on context and data
        
        Args:
            decision_type: Type of decision to make
            context: Decision context
            data: Additional data for decision making
            
        Returns:
            DecisionResult with decision details
        """
        start_time = time.time()
        
        try:
            logger.info(f"Making {decision_type.value} decision for context: {context.business_context}")
            
            if decision_type == DecisionType.OPTIMIZATION:
                result = await self._decide_optimization_strategy(context, data)
            elif decision_type == DecisionType.ROUTING:
                result = await self._decide_routing_strategy(context, data)
            elif decision_type == DecisionType.RESOURCE_ALLOCATION:
                result = await self._decide_resource_allocation(context, data)
            elif decision_type == DecisionType.BUSINESS_RULE:
                result = await self._process_business_rules(context, data)
            elif decision_type == DecisionType.QUANTUM_STRATEGY:
                result = await self._decide_quantum_strategy(context, data)
            else:
                raise ValueError(f"Unsupported decision type: {decision_type.value}")
            
            # Store decision in history
            self.decision_history.append(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Decision making failed: {e}")
            return DecisionResult(
                success=False,
                decision_type=decision_type.value,
                strategy_selected="none",
                reasoning=f"Decision failed: {str(e)}",
                execution_time=time.time() - start_time,
                confidence_score=0.0,
                error_message=str(e)
            )
    
    async def _decide_optimization_strategy(self, 
                                          context: DecisionContext,
                                          data: Optional[Dict[str, Any]]) -> DecisionResult:
        """Decide which optimization strategy to use"""
        
        # Analyze problem characteristics
        problem_size = data.get("problem_size", 0) if data else 0
        problem_type = data.get("problem_type", "unknown") if data else "unknown"
        priority = context.priority
        
        # Apply business rules
        applicable_rules = self._get_applicable_rules(context, data)
        
        # Select strategy based on rules and problem characteristics
        if applicable_rules:
            # Use highest priority rule
            top_rule = max(applicable_rules, key=lambda r: r.priority)
            strategy = self._extract_strategy_from_rule(top_rule)
            reasoning = f"Selected by business rule: {top_rule.name}"
        else:
            # Use problem characteristics to select strategy
            strategy, reasoning = self._select_strategy_by_characteristics(problem_size, problem_type, priority)
        
        # Validate strategy selection
        if not self._is_strategy_valid(strategy, problem_size, context):
            # Fallback to heuristic
            strategy = OptimizationStrategy.HEURISTIC.value
            reasoning += " (fallback to heuristic due to constraints)"
        
        confidence = self._calculate_confidence(strategy, problem_size, problem_type)
        
        return DecisionResult(
            success=True,
            decision_type=DecisionType.OPTIMIZATION.value,
            strategy_selected=strategy,
            reasoning=reasoning,
            execution_time=time.time(),
            confidence_score=confidence,
            metadata={
                "problem_size": problem_size,
                "problem_type": problem_type,
                "priority": priority,
                "applicable_rules": len(applicable_rules)
            }
        )
    
    async def _decide_routing_strategy(self, 
                                     context: DecisionContext,
                                     data: Optional[Dict[str, Any]]) -> DecisionResult:
        """Decide routing strategy for requests"""
        
        # Simple routing based on business context
        if context.business_context == "lead_scoring":
            strategy = "quantum_optimization"
            reasoning = "Lead scoring requires quantum optimization for accuracy"
        elif context.business_context == "resource_allocation":
            strategy = "hybrid_approach"
            reasoning = "Resource allocation benefits from hybrid quantum-classical approach"
        else:
            strategy = "standard_processing"
            reasoning = "Standard processing for unknown business context"
        
        return DecisionResult(
            success=True,
            decision_type=DecisionType.ROUTING.value,
            strategy_selected=strategy,
            reasoning=reasoning,
            execution_time=time.time(),
            confidence_score=0.85,
            metadata={"business_context": context.business_context}
        )
    
    async def _decide_resource_allocation(self, 
                                        context: DecisionContext,
                                        data: Optional[Dict[str, Any]]) -> DecisionResult:
        """Decide resource allocation strategy"""
        
        # Analyze resource requirements
        qubits_needed = data.get("qubits_required", 0) if data else 0
        time_constraint = data.get("time_constraint", 60) if data else 60
        
        if qubits_needed > self.max_qubits:
            strategy = "distributed_processing"
            reasoning = f"Problem requires {qubits_needed} qubits, exceeding max {self.max_qubits}"
        elif time_constraint < 1.0:
            strategy = "heuristic_fast"
            reasoning = f"Time constraint {time_constraint}s requires fast heuristic approach"
        else:
            strategy = "optimal_allocation"
            reasoning = "Standard optimal resource allocation"
        
        return DecisionResult(
            success=True,
            decision_type=DecisionType.RESOURCE_ALLOCATION.value,
            strategy_selected=strategy,
            reasoning=reasoning,
            execution_time=time.time(),
            confidence_score=0.90,
            metadata={
                "qubits_needed": qubits_needed,
                "time_constraint": time_constraint,
                "max_qubits": self.max_qubits
            }
        )
    
    async def _process_business_rules(self, 
                                    context: DecisionContext,
                                    data: Optional[Dict[str, Any]]) -> DecisionResult:
        """Process business rules for the given context"""
        
        applicable_rules = self._get_applicable_rules(context, data)
        
        if applicable_rules:
            # Execute actions from applicable rules
            actions_executed = []
            for rule in applicable_rules:
                for action in rule.actions:
                    action_result = await self._execute_action(action, context, data)
                    actions_executed.append({
                        "rule": rule.name,
                        "action": action["action"],
                        "result": action_result
                    })
            
            strategy = "business_rules_executed"
            reasoning = f"Executed {len(actions_executed)} actions from {len(applicable_rules)} rules"
        else:
            strategy = "no_rules_applicable"
            reasoning = "No business rules applicable for this context"
            actions_executed = []
        
        return DecisionResult(
            success=True,
            decision_type=DecisionType.BUSINESS_RULE.value,
            strategy_selected=strategy,
            reasoning=reasoning,
            execution_time=time.time(),
            confidence_score=0.95 if applicable_rules else 0.70,
            metadata={
                "applicable_rules": len(applicable_rules),
                "actions_executed": actions_executed
            }
        )
    
    async def _decide_quantum_strategy(self, 
                                     context: DecisionContext,
                                     data: Optional[Dict[str, Any]]) -> DecisionResult:
        """Decide quantum computing strategy"""
        
        # Analyze quantum requirements
        problem_complexity = data.get("complexity", "low") if data else "low"
        quantum_advantage = data.get("quantum_advantage", False) if data else False
        
        if quantum_advantage and problem_complexity in ["medium", "high"]:
            strategy = "full_quantum"
            reasoning = "Problem has quantum advantage and sufficient complexity"
        elif problem_complexity == "high":
            strategy = "hybrid_quantum"
            reasoning = "High complexity problem benefits from hybrid approach"
        else:
            strategy = "classical_with_quantum_enhancement"
            reasoning = "Low complexity problem, minimal quantum enhancement"
        
        return DecisionResult(
            success=True,
            decision_type=DecisionType.QUANTUM_STRATEGY.value,
            strategy_selected=strategy,
            reasoning=reasoning,
            execution_time=time.time(),
            confidence_score=0.88,
            metadata={
                "problem_complexity": problem_complexity,
                "quantum_advantage": quantum_advantage
            }
        )
    
    def _get_applicable_rules(self, context: DecisionContext, data: Optional[Dict[str, Any]]) -> List[BusinessRule]:
        """Get business rules applicable to the current context"""
        applicable_rules = []
        
        for rule in self.business_rules:
            if not rule.active:
                continue
            
            if self._rule_matches_context(rule, context, data):
                applicable_rules.append(rule)
        
        return applicable_rules
    
    def _rule_matches_context(self, rule: BusinessRule, context: DecisionContext, data: Optional[Dict[str, Any]]) -> bool:
        """Check if a business rule matches the current context"""
        
        for condition_key, condition_value in rule.conditions.items():
            if condition_key == "context":
                if context.business_context != condition_value:
                    return False
            elif condition_key == "data_size" and data:
                data_size = data.get("size", 0)
                if not self._evaluate_condition(data_size, condition_value):
                    return False
            elif condition_key == "priority":
                if context.priority != condition_value:
                    return False
        
        return True
    
    def _evaluate_condition(self, actual_value: Any, condition: Dict[str, Any]) -> bool:
        """Evaluate a condition against an actual value"""
        operator = condition.get("operator", "==")
        expected_value = condition.get("value")
        
        if operator == "==":
            return actual_value == expected_value
        elif operator == "!=":
            return actual_value != expected_value
        elif operator == ">":
            return actual_value > expected_value
        elif operator == ">=":
            return actual_value >= expected_value
        elif operator == "<":
            return actual_value < expected_value
        elif operator == "<=":
            return actual_value <= expected_value
        else:
            logger.warning(f"Unknown operator: {operator}")
            return False
    
    def _extract_strategy_from_rule(self, rule: BusinessRule) -> str:
        """Extract optimization strategy from business rule"""
        for action in rule.actions:
            if action["action"] == "use_quantum_optimization":
                return action["parameters"].get("algorithm", "qaoa")
            elif action["action"] == "use_heuristic_optimization":
                return "heuristic"
            elif action["action"] == "use_hybrid_optimization":
                return "hybrid"
        
        return "unknown"
    
    def _select_strategy_by_characteristics(self, 
                                          problem_size: int,
                                          problem_type: str,
                                          priority: str) -> tuple[str, str]:
        """Select strategy based on problem characteristics"""
        
        if problem_size <= 50:
            strategy = OptimizationStrategy.HEURISTIC.value
            reasoning = f"Small problem size ({problem_size}), using heuristic"
        elif problem_size <= 200:
            strategy = OptimizationStrategy.HYBRID.value
            reasoning = f"Medium problem size ({problem_size}), using hybrid approach"
        else:
            strategy = OptimizationStrategy.QUANTUM_ANNEALING.value
            reasoning = f"Large problem size ({problem_size}), using quantum annealing"
        
        # Adjust based on priority
        if priority == "high":
            if strategy != OptimizationStrategy.HEURISTIC.value:
                strategy = OptimizationStrategy.QAOA.value
                reasoning += " (high priority, using QAOA for better accuracy)"
        
        return strategy, reasoning
    
    def _is_strategy_valid(self, strategy: str, problem_size: int, context: DecisionContext) -> bool:
        """Check if strategy is valid for the given problem"""
        
        if strategy not in self.optimization_strategies:
            return False
        
        strategy_info = self.optimization_strategies[strategy]
        qubit_requirements = strategy_info["qubit_requirements"]
        
        # Check qubit requirements
        if problem_size < qubit_requirements["min"] or problem_size > qubit_requirements["max"]:
            return False
        
        # Check other constraints
        if context.constraints:
            if "max_cost" in context.constraints:
                max_cost = context.constraints["max_cost"]
                if strategy_info["cost_factor"] > max_cost:
                    return False
        
        return True
    
    def _calculate_confidence(self, strategy: str, problem_size: int, problem_type: str) -> float:
        """Calculate confidence score for strategy selection"""
        
        if strategy not in self.optimization_strategies:
            return 0.0
        
        strategy_info = self.optimization_strategies[strategy]
        base_confidence = strategy_info["accuracy"]
        
        # Adjust confidence based on problem characteristics
        if problem_type in strategy_info["best_for"]:
            base_confidence += 0.1
        
        # Adjust based on problem size fit
        qubit_req = strategy_info["qubit_requirements"]
        if qubit_req["min"] <= problem_size <= qubit_req["max"]:
            base_confidence += 0.05
        
        return min(base_confidence, 1.0)
    
    async def _execute_action(self, action: Dict[str, Any], context: DecisionContext, data: Optional[Dict[str, Any]]) -> bool:
        """Execute an action from a business rule"""
        
        action_type = action["action"]
        parameters = action.get("parameters", {})
        
        try:
            if action_type == "set_priority":
                context.priority = parameters.get("level", "normal")
                logger.info(f"Set priority to {context.priority}")
                return True
            elif action_type == "use_quantum_optimization":
                logger.info(f"Configured quantum optimization with algorithm: {parameters.get('algorithm')}")
                return True
            elif action_type == "use_heuristic_optimization":
                logger.info(f"Configured heuristic optimization with method: {parameters.get('method')}")
                return True
            elif action_type == "use_hybrid_optimization":
                logger.info(f"Configured hybrid optimization with quantum ratio: {parameters.get('quantum_ratio')}")
                return True
            else:
                logger.warning(f"Unknown action type: {action_type}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to execute action {action_type}: {e}")
            return False
    
    def add_business_rule(self, rule: BusinessRule):
        """Add a new business rule"""
        self.business_rules.append(rule)
        logger.info(f"Added business rule: {rule.name}")
    
    def remove_business_rule(self, rule_id: str):
        """Remove a business rule by ID"""
        self.business_rules = [r for r in self.business_rules if r.rule_id != rule_id]
        logger.info(f"Removed business rule: {rule_id}")
    
    def get_decision_history(self, limit: int = 100) -> List[DecisionResult]:
        """Get recent decision history"""
        return self.decision_history[-limit:] if self.decision_history else []
    
    def get_optimization_strategies(self) -> Dict[str, Dict[str, Any]]:
        """Get available optimization strategies"""
        return self.optimization_strategies.copy()
    
    def get_business_rules(self) -> List[BusinessRule]:
        """Get all business rules"""
        return self.business_rules.copy()
