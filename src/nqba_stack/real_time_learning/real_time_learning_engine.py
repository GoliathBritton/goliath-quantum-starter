"""
Real-Time Learning Engine for Phase 2
Adaptive algorithms with performance feedback and algorithm evolution
"""

import asyncio
import json
import numpy as np
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)

class AlgorithmType(Enum):
    """Types of optimization algorithms"""
    QAOA = "qaoa"
    VQE = "vqe"
    QSVM = "qsvm"
    QUANTUM_ANNEALING = "quantum_annealing"
    HYBRID = "hybrid"
    CLASSICAL = "classical"

class PerformanceMetric(Enum):
    """Performance metrics for algorithm evaluation"""
    EXECUTION_TIME = "execution_time"
    SOLUTION_QUALITY = "solution_quality"
    QUANTUM_ADVANTAGE = "quantum_advantage"
    CONVERGENCE_SPEED = "convergence_speed"
    RESOURCE_UTILIZATION = "resource_utilization"

@dataclass
class AlgorithmPerformance:
    """Performance data for an algorithm"""
    algorithm_id: str
    algorithm_type: AlgorithmType
    performance_metrics: Dict[str, float]
    problem_characteristics: Dict[str, Any]
    execution_context: Dict[str, Any]
    timestamp: datetime
    success: bool
    metadata: Dict[str, Any]

@dataclass
class AlgorithmConfig:
    """Configuration for an optimization algorithm"""
    algorithm_id: str
    algorithm_type: AlgorithmType
    parameters: Dict[str, Any]
    hyperparameters: Dict[str, Any]
    constraints: Dict[str, Any]
    version: str
    created_at: datetime
    last_updated: datetime
    performance_history: List[str]  # IDs of performance records

@dataclass
class LearningRule:
    """Rule for algorithm adaptation and evolution"""
    rule_id: str
    rule_type: str  # 'parameter_adjustment', 'algorithm_selection', 'constraint_evolution'
    conditions: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int
    is_active: bool
    created_at: datetime
    last_triggered: Optional[datetime] = None
    success_rate: float = 0.0

@dataclass
class KnowledgeBase:
    """Knowledge base for algorithm learning"""
    knowledge_id: str
    category: str
    content: Dict[str, Any]
    confidence: float
    source: str
    created_at: datetime
    last_updated: datetime
    usage_count: int = 0

class RealTimeLearningEngine:
    """Real-time learning engine for adaptive algorithm optimization"""
    
    def __init__(self, max_algorithms: int = 100, max_performance_records: int = 10000):
        self.max_algorithms = max_algorithms
        self.max_performance_records = max_performance_records
        
        # Core components
        self.algorithms: Dict[str, AlgorithmConfig] = {}
        self.performance_records: Dict[str, AlgorithmPerformance] = {}
        self.learning_rules: Dict[str, LearningRule] = {}
        self.knowledge_base: Dict[str, KnowledgeBase] = {}
        
        # Learning state
        self.is_learning_enabled = True
        self.learning_rate = 0.1
        self.min_performance_threshold = 0.7
        
        # Performance tracking
        self.performance_window_hours = 24
        self.min_records_for_learning = 10
        
        logger.info("Real-Time Learning Engine initialized")
    
    async def register_algorithm(
        self,
        algorithm_type: AlgorithmType,
        parameters: Dict[str, Any],
        hyperparameters: Dict[str, Any],
        constraints: Dict[str, Any],
        version: str = "1.0.0"
    ) -> AlgorithmConfig:
        """Register a new optimization algorithm"""
        try:
            algorithm_id = self._generate_algorithm_id(algorithm_type, parameters, hyperparameters)
            
            if algorithm_id in self.algorithms:
                logger.warning(f"Algorithm {algorithm_id} already exists, updating instead")
                return await self.update_algorithm(algorithm_id, parameters, hyperparameters, constraints, version)
            
            # Check capacity
            if len(self.algorithms) >= self.max_algorithms:
                await self._cleanup_old_algorithms()
            
            algorithm_config = AlgorithmConfig(
                algorithm_id=algorithm_id,
                algorithm_type=algorithm_type,
                parameters=parameters,
                hyperparameters=hyperparameters,
                constraints=constraints,
                version=version,
                created_at=datetime.now(),
                last_updated=datetime.now(),
                performance_history=[]
            )
            
            self.algorithms[algorithm_id] = algorithm_config
            logger.info(f"Registered algorithm: {algorithm_id} ({algorithm_type.value})")
            
            return algorithm_config
            
        except Exception as e:
            logger.error(f"Error registering algorithm: {e}")
            raise
    
    async def update_algorithm(
        self,
        algorithm_id: str,
        parameters: Dict[str, Any],
        hyperparameters: Dict[str, Any],
        constraints: Dict[str, Any],
        version: str = None
    ) -> AlgorithmConfig:
        """Update an existing algorithm configuration"""
        try:
            if algorithm_id not in self.algorithms:
                raise ValueError(f"Algorithm not found: {algorithm_id}")
            
            algorithm = self.algorithms[algorithm_id]
            algorithm.parameters = parameters
            algorithm.hyperparameters = hyperparameters
            algorithm.constraints = constraints
            if version:
                algorithm.version = version
            algorithm.last_updated = datetime.now()
            
            logger.info(f"Updated algorithm: {algorithm_id}")
            return algorithm
            
        except Exception as e:
            logger.error(f"Error updating algorithm: {e}")
            raise
    
    async def record_performance(
        self,
        algorithm_id: str,
        performance_metrics: Dict[str, float],
        problem_characteristics: Dict[str, Any],
        execution_context: Dict[str, Any],
        success: bool,
        metadata: Dict[str, Any] = None
    ) -> str:
        """Record performance data for an algorithm execution"""
        try:
            if algorithm_id not in self.algorithms:
                raise ValueError(f"Algorithm not found: {algorithm_id}")
            
            # Check capacity
            if len(self.performance_records) >= self.max_performance_records:
                await self._cleanup_old_performance_records()
            
            # Create performance record
            record_id = f"perf_{len(self.performance_records) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            performance_record = AlgorithmPerformance(
                algorithm_id=algorithm_id,
                algorithm_type=self.algorithms[algorithm_id].algorithm_type,
                performance_metrics=performance_metrics,
                problem_characteristics=problem_characteristics,
                execution_context=execution_context,
                timestamp=datetime.now(),
                success=success,
                metadata=metadata or {}
            )
            
            self.performance_records[record_id] = performance_record
            
            # Update algorithm performance history
            self.algorithms[algorithm_id].performance_history.append(record_id)
            
            # Trigger learning if conditions are met
            if self.is_learning_enabled:
                await self._trigger_learning(algorithm_id)
            
            logger.info(f"Recorded performance for algorithm {algorithm_id}: {record_id}")
            return record_id
            
        except Exception as e:
            logger.error(f"Error recording performance: {e}")
            raise
    
    async def _trigger_learning(self, algorithm_id: str):
        """Trigger learning process for an algorithm"""
        try:
            algorithm = self.algorithms[algorithm_id]
            
            # Check if we have enough performance data
            recent_performance = self._get_recent_performance(algorithm_id)
            if len(recent_performance) < self.min_records_for_learning:
                return
            
            # Analyze performance trends
            performance_trends = self._analyze_performance_trends(recent_performance)
            
            # Apply learning rules
            applied_rules = await self._apply_learning_rules(algorithm_id, performance_trends)
            
            if applied_rules:
                logger.info(f"Applied {len(applied_rules)} learning rules to algorithm {algorithm_id}")
                
                # Update knowledge base
                await self._update_knowledge_base(algorithm_id, performance_trends, applied_rules)
            
        except Exception as e:
            logger.error(f"Error triggering learning: {e}")
    
    def _get_recent_performance(self, algorithm_id: str, hours: int = None) -> List[AlgorithmPerformance]:
        """Get recent performance records for an algorithm"""
        if hours is None:
            hours = self.performance_window_hours
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_records = []
        for record_id in self.algorithms[algorithm_id].performance_history:
            if record_id in self.performance_records:
                record = self.performance_records[record_id]
                if record.timestamp >= cutoff_time:
                    recent_records.append(record)
        
        return recent_records
    
    def _analyze_performance_trends(self, performance_records: List[AlgorithmPerformance]) -> Dict[str, Any]:
        """Analyze performance trends from recent records"""
        if not performance_records:
            return {}
        
        trends = {}
        
        # Calculate average metrics
        for metric in PerformanceMetric:
            metric_name = metric.value
            values = [r.performance_metrics.get(metric_name, 0.0) for r in performance_records]
            if values:
                trends[f"avg_{metric_name}"] = np.mean(values)
                trends[f"std_{metric_name}"] = np.std(values)
                trends[f"trend_{metric_name}"] = self._calculate_trend(values)
        
        # Success rate
        success_count = sum(1 for r in performance_records if r.success)
        trends["success_rate"] = success_count / len(performance_records)
        
        # Performance degradation detection
        if len(performance_records) >= 2:
            recent_avg = np.mean([r.performance_metrics.get('solution_quality', 0.0) 
                                for r in performance_records[-5:]])
            older_avg = np.mean([r.performance_metrics.get('solution_quality', 0.0) 
                               for r in performance_records[:-5]])
            trends["performance_degradation"] = older_avg - recent_avg
        
        return trends
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate trend (slope) of values over time"""
        if len(values) < 2:
            return 0.0
        
        x = np.arange(len(values))
        y = np.array(values)
        
        # Simple linear regression
        slope = np.polyfit(x, y, 1)[0]
        return slope
    
    async def _apply_learning_rules(
        self,
        algorithm_id: str,
        performance_trends: Dict[str, Any]
    ) -> List[str]:
        """Apply learning rules based on performance trends"""
        applied_rules = []
        
        for rule_id, rule in self.learning_rules.items():
            if not rule.is_active:
                continue
            
            # Check if rule conditions are met
            if self._evaluate_rule_conditions(rule, performance_trends):
                # Apply rule actions
                success = await self._execute_rule_actions(rule, algorithm_id, performance_trends)
                
                if success:
                    applied_rules.append(rule_id)
                    rule.last_triggered = datetime.now()
                    
                    # Update rule success rate
                    rule.success_rate = (rule.success_rate * 0.9 + 0.1) if success else (rule.success_rate * 0.9)
        
        return applied_rules
    
    def _evaluate_rule_conditions(self, rule: LearningRule, performance_trends: Dict[str, Any]) -> bool:
        """Evaluate if rule conditions are met"""
        conditions = rule.conditions
        
        for condition_key, expected_value in conditions.items():
            if condition_key not in performance_trends:
                return False
            
            actual_value = performance_trends[condition_key]
            
            # Handle different comparison types
            if isinstance(expected_value, dict):
                comparison_type = expected_value.get('type', 'equals')
                target_value = expected_value.get('value')
                
                if comparison_type == 'equals' and actual_value != target_value:
                    return False
                elif comparison_type == 'greater_than' and actual_value <= target_value:
                    return False
                elif comparison_type == 'less_than' and actual_value >= target_value:
                    return False
                elif comparison_type == 'in_range':
                    min_val = expected_value.get('min')
                    max_val = expected_value.get('max')
                    if actual_value < min_val or actual_value > max_val:
                        return False
            else:
                if actual_value != expected_value:
                    return False
        
        return True
    
    async def _execute_rule_actions(
        self,
        rule: LearningRule,
        algorithm_id: str,
        performance_trends: Dict[str, Any]
    ) -> bool:
        """Execute the actions specified in a learning rule"""
        try:
            actions = rule.actions
            algorithm = self.algorithms[algorithm_id]
            
            for action_type, action_config in actions.items():
                if action_type == 'parameter_adjustment':
                    await self._adjust_algorithm_parameters(algorithm, action_config)
                elif action_type == 'hyperparameter_tuning':
                    await self._tune_hyperparameters(algorithm, action_config)
                elif action_type == 'constraint_evolution':
                    await self._evolve_constraints(algorithm, action_config)
                elif action_type == 'algorithm_replacement':
                    await self._replace_algorithm(algorithm, action_config)
            
            return True
            
        except Exception as e:
            logger.error(f"Error executing rule actions: {e}")
            return False
    
    async def _adjust_algorithm_parameters(
        self,
        algorithm: AlgorithmConfig,
        adjustment_config: Dict[str, Any]
    ):
        """Adjust algorithm parameters based on learning"""
        for param_name, adjustment in adjustment_config.items():
            if param_name in algorithm.parameters:
                current_value = algorithm.parameters[param_name]
                
                if adjustment.get('type') == 'percentage':
                    percentage = adjustment.get('value', 0.0)
                    new_value = current_value * (1 + percentage / 100)
                elif adjustment.get('type') == 'absolute':
                    delta = adjustment.get('value', 0.0)
                    new_value = current_value + delta
                elif adjustment.get('type') == 'multiplier':
                    multiplier = adjustment.get('value', 1.0)
                    new_value = current_value * multiplier
                else:
                    new_value = adjustment.get('value', current_value)
                
                algorithm.parameters[param_name] = new_value
                logger.info(f"Adjusted parameter {param_name}: {current_value} -> {new_value}")
    
    async def _tune_hyperparameters(
        self,
        algorithm: AlgorithmConfig,
        tuning_config: Dict[str, Any]
    ):
        """Tune algorithm hyperparameters based on learning"""
        for hyperparam_name, tuning in tuning_config.items():
            if hyperparam_name in algorithm.hyperparameters:
                current_value = algorithm.hyperparameters[hyperparam_name]
                
                # Apply tuning based on performance trends
                if tuning.get('adaptive'):
                    # Adaptive tuning based on performance
                    pass
                else:
                    # Fixed tuning
                    new_value = tuning.get('value', current_value)
                    algorithm.hyperparameters[hyperparam_name] = new_value
                    logger.info(f"Tuned hyperparameter {hyperparam_name}: {current_value} -> {new_value}")
    
    async def _evolve_constraints(
        self,
        algorithm: AlgorithmConfig,
        evolution_config: Dict[str, Any]
    ):
        """Evolve algorithm constraints based on learning"""
        for constraint_name, evolution in evolution_config.items():
            if constraint_name in algorithm.constraints:
                current_value = algorithm.constraints[constraint_name]
                
                # Apply constraint evolution
                if evolution.get('type') == 'relax':
                    # Relax constraint
                    relaxation_factor = evolution.get('factor', 0.1)
                    if isinstance(current_value, (int, float)):
                        new_value = current_value * (1 + relaxation_factor)
                    else:
                        new_value = current_value
                elif evolution.get('type') == 'tighten':
                    # Tighten constraint
                    tightening_factor = evolution.get('factor', 0.1)
                    if isinstance(current_value, (int, float)):
                        new_value = current_value * (1 - tightening_factor)
                    else:
                        new_value = current_value
                else:
                    new_value = evolution.get('value', current_value)
                
                algorithm.constraints[constraint_name] = new_value
                logger.info(f"Evolved constraint {constraint_name}: {current_value} -> {new_value}")
    
    async def _replace_algorithm(
        self,
        algorithm: AlgorithmConfig,
        replacement_config: Dict[str, Any]
    ):
        """Replace algorithm with a better performing one"""
        # This is a placeholder for algorithm replacement logic
        # In a real implementation, this would involve more sophisticated selection
        logger.info(f"Algorithm replacement triggered for {algorithm.algorithm_id}")
    
    async def add_learning_rule(
        self,
        rule_type: str,
        conditions: Dict[str, Any],
        actions: Dict[str, Any],
        priority: int = 1
    ) -> LearningRule:
        """Add a new learning rule"""
        try:
            rule_id = f"rule_{len(self.learning_rules) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            rule = LearningRule(
                rule_id=rule_id,
                rule_type=rule_type,
                conditions=conditions,
                actions=actions,
                priority=priority,
                is_active=True,
                created_at=datetime.now()
            )
            
            self.learning_rules[rule_id] = rule
            logger.info(f"Added learning rule: {rule_id}")
            
            return rule
            
        except Exception as e:
            logger.error(f"Error adding learning rule: {e}")
            raise
    
    async def _update_knowledge_base(
        self,
        algorithm_id: str,
        performance_trends: Dict[str, Any],
        applied_rules: List[str]
    ):
        """Update knowledge base with new insights"""
        try:
            # Create knowledge entry for algorithm performance
            performance_knowledge = KnowledgeBase(
                knowledge_id=f"kb_perf_{len(self.knowledge_base) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                category="algorithm_performance",
                content={
                    "algorithm_id": algorithm_id,
                    "performance_trends": performance_trends,
                    "applied_rules": applied_rules,
                    "timestamp": datetime.now().isoformat()
                },
                confidence=0.8,
                source="real_time_learning",
                created_at=datetime.now(),
                last_updated=datetime.now()
            )
            
            self.knowledge_base[performance_knowledge.knowledge_id] = performance_knowledge
            
            # Update existing knowledge based on new insights
            await self._evolve_existing_knowledge(algorithm_id, performance_trends)
            
        except Exception as e:
            logger.error(f"Error updating knowledge base: {e}")
    
    async def _evolve_existing_knowledge(
        self,
        algorithm_id: str,
        performance_trends: Dict[str, Any]
    ):
        """Evolve existing knowledge based on new performance data"""
        for kb_id, knowledge in self.knowledge_base.items():
            if (knowledge.category == "algorithm_performance" and 
                knowledge.content.get("algorithm_id") == algorithm_id):
                
                # Update confidence based on consistency
                old_trends = knowledge.content.get("performance_trends", {})
                consistency_score = self._calculate_consistency(old_trends, performance_trends)
                
                # Adjust confidence based on consistency
                if consistency_score > 0.8:
                    knowledge.confidence = min(1.0, knowledge.confidence + 0.1)
                else:
                    knowledge.confidence = max(0.1, knowledge.confidence - 0.1)
                
                knowledge.last_updated = datetime.now()
                knowledge.usage_count += 1
    
    def _calculate_consistency(self, trends1: Dict[str, Any], trends2: Dict[str, Any]) -> float:
        """Calculate consistency between two sets of performance trends"""
        if not trends1 or not trends2:
            return 0.0
        
        common_keys = set(trends1.keys()) & set(trends2.keys())
        if not common_keys:
            return 0.0
        
        consistency_scores = []
        for key in common_keys:
            val1 = trends1[key]
            val2 = trends2[key]
            
            if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
                # Calculate relative difference
                if val1 != 0:
                    relative_diff = abs(val1 - val2) / abs(val1)
                    consistency_score = max(0, 1 - relative_diff)
                    consistency_scores.append(consistency_score)
        
        return np.mean(consistency_scores) if consistency_scores else 0.0
    
    def _generate_algorithm_id(
        self,
        algorithm_type: AlgorithmType,
        parameters: Dict[str, Any],
        hyperparameters: Dict[str, Any]
    ) -> str:
        """Generate a unique algorithm ID based on configuration"""
        config_string = json.dumps({
            'type': algorithm_type.value,
            'parameters': parameters,
            'hyperparameters': hyperparameters
        }, sort_keys=True)
        
        hash_object = hashlib.md5(config_string.encode())
        return f"{algorithm_type.value}_{hash_object.hexdigest()[:8]}"
    
    async def _cleanup_old_algorithms(self):
        """Clean up old algorithms to make room for new ones"""
        # Remove algorithms with poor performance
        algorithm_scores = []
        for algorithm_id, algorithm in self.algorithms.items():
            recent_performance = self._get_recent_performance(algorithm_id, hours=1)
            if recent_performance:
                avg_quality = np.mean([p.performance_metrics.get('solution_quality', 0.0) 
                                     for p in recent_performance])
                algorithm_scores.append((algorithm_id, avg_quality))
            else:
                algorithm_scores.append((algorithm_id, 0.0))
        
        # Sort by performance score
        algorithm_scores.sort(key=lambda x: x[1])
        
        # Remove worst performing algorithms
        algorithms_to_remove = algorithm_scores[:len(algorithm_scores) // 4]  # Remove 25%
        
        for algorithm_id, _ in algorithms_to_remove:
            del self.algorithms[algorithm_id]
            logger.info(f"Removed low-performing algorithm: {algorithm_id}")
    
    async def _cleanup_old_performance_records(self):
        """Clean up old performance records"""
        cutoff_time = datetime.now() - timedelta(hours=self.performance_window_hours)
        
        records_to_remove = []
        for record_id, record in self.performance_records.items():
            if record.timestamp < cutoff_time:
                records_to_remove.append(record_id)
        
        for record_id in records_to_remove:
            del self.performance_records[record_id]
        
        logger.info(f"Cleaned up {len(records_to_remove)} old performance records")
    
    async def get_learning_analytics(self) -> Dict[str, Any]:
        """Get analytics on learning engine performance"""
        total_algorithms = len(self.algorithms)
        total_rules = len(self.learning_rules)
        total_knowledge = len(self.knowledge_base)
        total_performance_records = len(self.performance_records)
        
        # Calculate learning effectiveness
        active_rules = len([r for r in self.learning_rules.values() if r.is_active])
        successful_rules = len([r for r in self.learning_rules.values() if r.success_rate > 0.5])
        
        # Performance improvement tracking
        recent_performance = []
        for algorithm in self.algorithms.values():
            recent_records = self._get_recent_performance(algorithm.algorithm_id, hours=1)
            if recent_records:
                avg_quality = np.mean([r.performance_metrics.get('solution_quality', 0.0) 
                                     for r in recent_records])
                recent_performance.append(avg_quality)
        
        avg_recent_performance = np.mean(recent_performance) if recent_performance else 0.0
        
        return {
            'engine_metrics': {
                'total_algorithms': total_algorithms,
                'total_rules': total_rules,
                'total_knowledge': total_knowledge,
                'total_performance_records': total_performance_records
            },
            'learning_effectiveness': {
                'active_rules': active_rules,
                'successful_rules': successful_rules,
                'rule_success_rate': successful_rules / max(total_rules, 1)
            },
            'performance_tracking': {
                'average_recent_performance': avg_recent_performance,
                'learning_enabled': self.is_learning_enabled,
                'learning_rate': self.learning_rate
            }
        }
