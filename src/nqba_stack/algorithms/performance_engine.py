"""Performance Engine for Quantum-Enhanced Algorithms

This module provides comprehensive performance tracking, benchmarking, and dynamic
algorithm selection capabilities for the quantum-enhanced algorithm library.

Features:
- Real-time performance monitoring
- Algorithm benchmarking and comparison
- Dynamic algorithm selection based on context
- Performance prediction and optimization
- Resource usage tracking
- Quality metrics and scoring
"""

import time
import psutil
import numpy as np
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, deque
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class PerformanceMetric(Enum):
    """Types of performance metrics"""
    EXECUTION_TIME = "execution_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ACCURACY = "accuracy"
    CONFIDENCE = "confidence"
    QUANTUM_ADVANTAGE = "quantum_advantage"
    COST_EFFICIENCY = "cost_efficiency"
    SCALABILITY = "scalability"
    CONVERGENCE_RATE = "convergence_rate"
    SOLUTION_QUALITY = "solution_quality"


class AlgorithmComplexity(Enum):
    """Algorithm complexity classifications"""
    LOW = "low"          # Simple problems, < 10 variables
    MEDIUM = "medium"    # Moderate problems, 10-100 variables
    HIGH = "high"        # Complex problems, 100-1000 variables
    EXTREME = "extreme"  # Very complex problems, > 1000 variables


class ResourceType(Enum):
    """Types of computational resources"""
    CLASSICAL_CPU = "classical_cpu"
    QUANTUM_QPU = "quantum_qpu"
    HYBRID = "hybrid"
    GPU = "gpu"
    MEMORY = "memory"
    NETWORK = "network"


@dataclass
class PerformanceSnapshot:
    """Single performance measurement"""
    timestamp: datetime
    metric_type: PerformanceMetric
    value: float
    unit: str
    context: Dict[str, Any] = field(default_factory=dict)
    algorithm_id: str = ""
    problem_size: int = 0
    resource_usage: Dict[ResourceType, float] = field(default_factory=dict)


@dataclass
class AlgorithmBenchmark:
    """Comprehensive algorithm benchmark results"""
    algorithm_id: str
    algorithm_type: str
    problem_complexity: AlgorithmComplexity
    performance_metrics: Dict[PerformanceMetric, float]
    resource_efficiency: Dict[ResourceType, float]
    quality_score: float
    reliability_score: float
    scalability_factor: float
    quantum_advantage_ratio: float
    cost_per_operation: float
    benchmark_timestamp: datetime
    test_cases_passed: int
    total_test_cases: int
    error_rate: float
    convergence_iterations: int
    memory_peak_mb: float
    cpu_time_seconds: float


@dataclass
class SelectionCriteria:
    """Criteria for dynamic algorithm selection"""
    problem_size: int
    complexity: AlgorithmComplexity
    accuracy_requirement: float
    time_constraint: float  # seconds
    resource_budget: Dict[ResourceType, float]
    quality_threshold: float
    cost_limit: float
    preferred_approach: Optional[str] = None  # 'quantum', 'classical', 'hybrid'
    risk_tolerance: float = 0.5


@dataclass
class AlgorithmRecommendation:
    """Algorithm selection recommendation"""
    algorithm_id: str
    algorithm_type: str
    confidence_score: float
    expected_performance: Dict[PerformanceMetric, float]
    estimated_cost: float
    estimated_time: float
    quantum_advantage: bool
    reasoning: List[str]
    alternative_options: List[str]
    risk_assessment: Dict[str, float]


class PerformanceTracker:
    """Real-time performance tracking for algorithms"""
    
    def __init__(self, max_history: int = 10000):
        self.max_history = max_history
        self.performance_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_history))
        self.active_measurements: Dict[str, Dict] = {}
        self.baseline_metrics: Dict[str, Dict[PerformanceMetric, float]] = {}
        
    def start_measurement(self, algorithm_id: str, context: Dict[str, Any] = None) -> str:
        """Start performance measurement for an algorithm execution"""
        measurement_id = f"{algorithm_id}_{int(time.time() * 1000)}"
        
        self.active_measurements[measurement_id] = {
            'algorithm_id': algorithm_id,
            'start_time': time.time(),
            'start_memory': psutil.virtual_memory().used / 1024 / 1024,  # MB
            'start_cpu_percent': psutil.cpu_percent(),
            'context': context or {},
            'snapshots': []
        }
        
        return measurement_id
    
    def record_snapshot(self, measurement_id: str, metric_type: PerformanceMetric, 
                       value: float, unit: str, context: Dict[str, Any] = None):
        """Record a performance snapshot during execution"""
        if measurement_id not in self.active_measurements:
            logger.warning(f"Measurement ID {measurement_id} not found")
            return
            
        snapshot = PerformanceSnapshot(
            timestamp=datetime.now(),
            metric_type=metric_type,
            value=value,
            unit=unit,
            context=context or {},
            algorithm_id=self.active_measurements[measurement_id]['algorithm_id'],
            resource_usage=self._get_current_resource_usage()
        )
        
        self.active_measurements[measurement_id]['snapshots'].append(snapshot)
    
    def end_measurement(self, measurement_id: str, result_quality: float = None) -> Dict[str, Any]:
        """End performance measurement and calculate final metrics"""
        if measurement_id not in self.active_measurements:
            logger.warning(f"Measurement ID {measurement_id} not found")
            return {}
            
        measurement = self.active_measurements[measurement_id]
        end_time = time.time()
        end_memory = psutil.virtual_memory().used / 1024 / 1024
        end_cpu_percent = psutil.cpu_percent()
        
        # Calculate final metrics
        execution_time = end_time - measurement['start_time']
        memory_delta = end_memory - measurement['start_memory']
        cpu_usage = (measurement['start_cpu_percent'] + end_cpu_percent) / 2
        
        final_metrics = {
            'execution_time': execution_time,
            'memory_usage_mb': memory_delta,
            'cpu_usage_percent': cpu_usage,
            'result_quality': result_quality,
            'snapshots_count': len(measurement['snapshots']),
            'algorithm_id': measurement['algorithm_id']
        }
        
        # Store in history
        algorithm_id = measurement['algorithm_id']
        self.performance_history[algorithm_id].append({
            'timestamp': datetime.now(),
            'metrics': final_metrics,
            'context': measurement['context'],
            'snapshots': measurement['snapshots']
        })
        
        # Clean up
        del self.active_measurements[measurement_id]
        
        return final_metrics
    
    def _get_current_resource_usage(self) -> Dict[ResourceType, float]:
        """Get current system resource usage"""
        return {
            ResourceType.CLASSICAL_CPU: psutil.cpu_percent(),
            ResourceType.MEMORY: psutil.virtual_memory().percent,
            ResourceType.NETWORK: sum(psutil.net_io_counters()[:2]) / 1024 / 1024  # MB
        }
    
    def get_algorithm_statistics(self, algorithm_id: str) -> Dict[str, Any]:
        """Get statistical summary for an algorithm"""
        if algorithm_id not in self.performance_history:
            return {}
            
        history = list(self.performance_history[algorithm_id])
        if not history:
            return {}
            
        execution_times = [h['metrics']['execution_time'] for h in history]
        memory_usage = [h['metrics']['memory_usage_mb'] for h in history]
        cpu_usage = [h['metrics']['cpu_usage_percent'] for h in history]
        
        return {
            'total_executions': len(history),
            'avg_execution_time': np.mean(execution_times),
            'std_execution_time': np.std(execution_times),
            'min_execution_time': np.min(execution_times),
            'max_execution_time': np.max(execution_times),
            'avg_memory_usage': np.mean(memory_usage),
            'avg_cpu_usage': np.mean(cpu_usage),
            'last_execution': history[-1]['timestamp'],
            'success_rate': len([h for h in history if h['metrics'].get('result_quality', 0) > 0.5]) / len(history)
        }


class AlgorithmBenchmarker:
    """Comprehensive algorithm benchmarking system"""
    
    def __init__(self, performance_tracker: PerformanceTracker):
        self.performance_tracker = performance_tracker
        self.benchmark_results: Dict[str, AlgorithmBenchmark] = {}
        self.test_suites: Dict[AlgorithmComplexity, List[Dict]] = {
            AlgorithmComplexity.LOW: self._generate_low_complexity_tests(),
            AlgorithmComplexity.MEDIUM: self._generate_medium_complexity_tests(),
            AlgorithmComplexity.HIGH: self._generate_high_complexity_tests(),
            AlgorithmComplexity.EXTREME: self._generate_extreme_complexity_tests()
        }
    
    async def benchmark_algorithm(self, algorithm_instance: Any, algorithm_id: str, 
                                 complexity: AlgorithmComplexity) -> AlgorithmBenchmark:
        """Run comprehensive benchmark for an algorithm"""
        logger.info(f"Starting benchmark for {algorithm_id} at {complexity.value} complexity")
        
        test_cases = self.test_suites[complexity]
        results = []
        total_tests = len(test_cases)
        passed_tests = 0
        total_errors = 0
        
        performance_metrics = defaultdict(list)
        resource_usage = defaultdict(list)
        
        for i, test_case in enumerate(test_cases):
            try:
                logger.info(f"Running test case {i+1}/{total_tests}")
                
                # Start measurement
                measurement_id = self.performance_tracker.start_measurement(
                    algorithm_id, {'test_case': i, 'complexity': complexity.value}
                )
                
                # Execute algorithm
                start_time = time.time()
                result = await self._execute_algorithm_test(algorithm_instance, test_case)
                execution_time = time.time() - start_time
                
                # Evaluate result quality
                quality_score = self._evaluate_result_quality(result, test_case)
                
                # End measurement
                final_metrics = self.performance_tracker.end_measurement(
                    measurement_id, quality_score
                )
                
                # Record metrics
                performance_metrics[PerformanceMetric.EXECUTION_TIME].append(execution_time)
                performance_metrics[PerformanceMetric.SOLUTION_QUALITY].append(quality_score)
                performance_metrics[PerformanceMetric.MEMORY_USAGE].append(final_metrics['memory_usage_mb'])
                performance_metrics[PerformanceMetric.CPU_USAGE].append(final_metrics['cpu_usage_percent'])
                
                if quality_score > 0.7:  # Success threshold
                    passed_tests += 1
                    
                results.append({
                    'test_case': i,
                    'success': quality_score > 0.7,
                    'quality_score': quality_score,
                    'execution_time': execution_time,
                    'metrics': final_metrics
                })
                
            except Exception as e:
                logger.error(f"Test case {i+1} failed: {e}")
                total_errors += 1
                results.append({
                    'test_case': i,
                    'success': False,
                    'error': str(e),
                    'quality_score': 0.0
                })
        
        # Calculate aggregate metrics
        avg_metrics = {}
        for metric, values in performance_metrics.items():
            if values:
                avg_metrics[metric] = np.mean(values)
        
        # Calculate derived metrics
        reliability_score = passed_tests / total_tests if total_tests > 0 else 0
        error_rate = total_errors / total_tests if total_tests > 0 else 0
        
        # Estimate quantum advantage (simplified)
        quantum_advantage_ratio = self._estimate_quantum_advantage(avg_metrics, complexity)
        
        # Calculate cost efficiency
        cost_per_operation = self._calculate_cost_per_operation(avg_metrics)
        
        benchmark = AlgorithmBenchmark(
            algorithm_id=algorithm_id,
            algorithm_type=getattr(algorithm_instance, 'algorithm_type', 'unknown'),
            problem_complexity=complexity,
            performance_metrics=avg_metrics,
            resource_efficiency=self._calculate_resource_efficiency(avg_metrics),
            quality_score=np.mean([r['quality_score'] for r in results]),
            reliability_score=reliability_score,
            scalability_factor=self._calculate_scalability_factor(performance_metrics),
            quantum_advantage_ratio=quantum_advantage_ratio,
            cost_per_operation=cost_per_operation,
            benchmark_timestamp=datetime.now(),
            test_cases_passed=passed_tests,
            total_test_cases=total_tests,
            error_rate=error_rate,
            convergence_iterations=self._estimate_convergence_iterations(results),
            memory_peak_mb=max(performance_metrics[PerformanceMetric.MEMORY_USAGE]) if performance_metrics[PerformanceMetric.MEMORY_USAGE] else 0,
            cpu_time_seconds=sum(performance_metrics[PerformanceMetric.EXECUTION_TIME]) if performance_metrics[PerformanceMetric.EXECUTION_TIME] else 0
        )
        
        self.benchmark_results[algorithm_id] = benchmark
        logger.info(f"Benchmark completed for {algorithm_id}: Quality={benchmark.quality_score:.3f}, Reliability={benchmark.reliability_score:.3f}")
        
        return benchmark
    
    def _generate_low_complexity_tests(self) -> List[Dict]:
        """Generate test cases for low complexity problems"""
        return [
            {'problem_size': 5, 'variables': 5, 'constraints': 2, 'expected_quality': 0.9},
            {'problem_size': 8, 'variables': 8, 'constraints': 3, 'expected_quality': 0.85},
            {'problem_size': 10, 'variables': 10, 'constraints': 4, 'expected_quality': 0.8}
        ]
    
    def _generate_medium_complexity_tests(self) -> List[Dict]:
        """Generate test cases for medium complexity problems"""
        return [
            {'problem_size': 25, 'variables': 25, 'constraints': 8, 'expected_quality': 0.8},
            {'problem_size': 50, 'variables': 50, 'constraints': 15, 'expected_quality': 0.75},
            {'problem_size': 75, 'variables': 75, 'constraints': 20, 'expected_quality': 0.7}
        ]
    
    def _generate_high_complexity_tests(self) -> List[Dict]:
        """Generate test cases for high complexity problems"""
        return [
            {'problem_size': 150, 'variables': 150, 'constraints': 40, 'expected_quality': 0.7},
            {'problem_size': 300, 'variables': 300, 'constraints': 75, 'expected_quality': 0.65},
            {'problem_size': 500, 'variables': 500, 'constraints': 100, 'expected_quality': 0.6}
        ]
    
    def _generate_extreme_complexity_tests(self) -> List[Dict]:
        """Generate test cases for extreme complexity problems"""
        return [
            {'problem_size': 1000, 'variables': 1000, 'constraints': 200, 'expected_quality': 0.6},
            {'problem_size': 2000, 'variables': 2000, 'constraints': 400, 'expected_quality': 0.55},
            {'problem_size': 5000, 'variables': 5000, 'constraints': 800, 'expected_quality': 0.5}
        ]
    
    async def _execute_algorithm_test(self, algorithm_instance: Any, test_case: Dict) -> Any:
        """Execute algorithm with test case"""
        # Generate synthetic test data based on test case
        test_data = self._generate_test_data(test_case)
        
        # Execute algorithm (this would call the actual algorithm method)
        if hasattr(algorithm_instance, 'optimize_portfolio'):
            return algorithm_instance.optimize_portfolio(**test_data)
        elif hasattr(algorithm_instance, 'optimize_energy_schedule'):
            return algorithm_instance.optimize_energy_schedule(**test_data)
        elif hasattr(algorithm_instance, 'assess_risk'):
            return algorithm_instance.assess_risk(**test_data)
        elif hasattr(algorithm_instance, 'personalize_experience'):
            return algorithm_instance.personalize_experience(**test_data)
        else:
            # Generic execution
            return await self._generic_algorithm_execution(algorithm_instance, test_data)
    
    def _generate_test_data(self, test_case: Dict) -> Dict[str, Any]:
        """Generate synthetic test data for algorithm testing"""
        problem_size = test_case['problem_size']
        
        # Generate synthetic data based on problem size
        return {
            'assets': [{'id': f'asset_{i}', 'expected_return': np.random.uniform(0.05, 0.15), 
                       'volatility': np.random.uniform(0.1, 0.3)} for i in range(problem_size)],
            'market_data': {'volatility': 'medium', 'trend': 'neutral'},
            'constraints': {'budget': 100000, 'max_positions': problem_size // 2}
        }
    
    def _evaluate_result_quality(self, result: Any, test_case: Dict) -> float:
        """Evaluate the quality of algorithm result"""
        if not result or not hasattr(result, 'confidence_score'):
            return 0.0
            
        # Base quality on confidence score and expected quality
        base_quality = getattr(result, 'confidence_score', 0.5)
        expected_quality = test_case.get('expected_quality', 0.7)
        
        # Adjust based on execution success
        if hasattr(result, 'result_data') and result.result_data:
            quality_bonus = 0.1
        else:
            quality_bonus = 0.0
            
        return min(base_quality + quality_bonus, 1.0)
    
    def _estimate_quantum_advantage(self, metrics: Dict, complexity: AlgorithmComplexity) -> float:
        """Estimate quantum advantage ratio"""
        # Simplified quantum advantage estimation
        base_advantage = {
            AlgorithmComplexity.LOW: 1.1,
            AlgorithmComplexity.MEDIUM: 1.3,
            AlgorithmComplexity.HIGH: 1.8,
            AlgorithmComplexity.EXTREME: 2.5
        }
        
        execution_time = metrics.get(PerformanceMetric.EXECUTION_TIME, 1.0)
        quality = metrics.get(PerformanceMetric.SOLUTION_QUALITY, 0.5)
        
        # Adjust based on performance
        advantage = base_advantage[complexity]
        if execution_time < 1.0 and quality > 0.8:
            advantage *= 1.2
        elif execution_time > 10.0 or quality < 0.5:
            advantage *= 0.8
            
        return advantage
    
    def _calculate_cost_per_operation(self, metrics: Dict) -> float:
        """Calculate cost per operation"""
        execution_time = metrics.get(PerformanceMetric.EXECUTION_TIME, 1.0)
        cpu_usage = metrics.get(PerformanceMetric.CPU_USAGE, 50.0)
        memory_usage = metrics.get(PerformanceMetric.MEMORY_USAGE, 100.0)
        
        # Simplified cost calculation (in arbitrary units)
        cpu_cost = execution_time * (cpu_usage / 100.0) * 0.01  # $0.01 per CPU-second
        memory_cost = memory_usage * 0.001  # $0.001 per MB
        quantum_cost = 0.1  # Base quantum operation cost
        
        return cpu_cost + memory_cost + quantum_cost
    
    def _calculate_resource_efficiency(self, metrics: Dict) -> Dict[ResourceType, float]:
        """Calculate resource efficiency scores"""
        execution_time = metrics.get(PerformanceMetric.EXECUTION_TIME, 1.0)
        cpu_usage = metrics.get(PerformanceMetric.CPU_USAGE, 50.0)
        memory_usage = metrics.get(PerformanceMetric.MEMORY_USAGE, 100.0)
        quality = metrics.get(PerformanceMetric.SOLUTION_QUALITY, 0.5)
        
        # Efficiency = Quality / Resource_Usage
        return {
            ResourceType.CLASSICAL_CPU: quality / (cpu_usage / 100.0) if cpu_usage > 0 else 0,
            ResourceType.MEMORY: quality / (memory_usage / 1000.0) if memory_usage > 0 else 0,
            ResourceType.QUANTUM_QPU: quality / execution_time if execution_time > 0 else 0
        }
    
    def _calculate_scalability_factor(self, performance_metrics: Dict) -> float:
        """Calculate algorithm scalability factor"""
        execution_times = performance_metrics.get(PerformanceMetric.EXECUTION_TIME, [])
        if len(execution_times) < 2:
            return 1.0
            
        # Simple scalability: how execution time grows with problem size
        time_growth = execution_times[-1] / execution_times[0] if execution_times[0] > 0 else 1.0
        return 1.0 / time_growth  # Higher is better
    
    def _estimate_convergence_iterations(self, results: List[Dict]) -> int:
        """Estimate average convergence iterations"""
        # Simplified estimation based on execution time
        avg_time = np.mean([r.get('execution_time', 1.0) for r in results])
        return int(avg_time * 10)  # Assume 10 iterations per second
    
    async def _generic_algorithm_execution(self, algorithm_instance: Any, test_data: Dict) -> Any:
        """Generic algorithm execution for unknown algorithm types"""
        # Simulate algorithm execution
        await asyncio.sleep(0.1)  # Simulate processing time
        
        # Return mock result
        class MockResult:
            def __init__(self):
                self.confidence_score = np.random.uniform(0.6, 0.9)
                self.result_data = {'mock': True}
                
        return MockResult()


class DynamicAlgorithmSelector:
    """Intelligent algorithm selection system"""
    
    def __init__(self, benchmarker: AlgorithmBenchmarker):
        self.benchmarker = benchmarker
        self.selection_history: List[Dict] = []
        self.algorithm_registry: Dict[str, Dict] = {}
        
    def register_algorithm(self, algorithm_id: str, algorithm_class: type, 
                          supported_complexities: List[AlgorithmComplexity],
                          algorithm_type: str, metadata: Dict[str, Any] = None):
        """Register an algorithm for dynamic selection"""
        self.algorithm_registry[algorithm_id] = {
            'class': algorithm_class,
            'supported_complexities': supported_complexities,
            'algorithm_type': algorithm_type,
            'metadata': metadata or {},
            'registration_time': datetime.now()
        }
        
        logger.info(f"Registered algorithm: {algorithm_id} ({algorithm_type})")
    
    async def select_optimal_algorithm(self, criteria: SelectionCriteria) -> AlgorithmRecommendation:
        """Select the optimal algorithm based on selection criteria"""
        logger.info(f"Selecting optimal algorithm for {criteria.complexity.value} complexity problem")
        
        # Filter algorithms by complexity support
        candidate_algorithms = {
            alg_id: alg_info for alg_id, alg_info in self.algorithm_registry.items()
            if criteria.complexity in alg_info['supported_complexities']
        }
        
        if not candidate_algorithms:
            raise ValueError(f"No algorithms available for {criteria.complexity.value} complexity")
        
        # Score each candidate algorithm
        algorithm_scores = {}
        for alg_id, alg_info in candidate_algorithms.items():
            score = await self._score_algorithm(alg_id, alg_info, criteria)
            algorithm_scores[alg_id] = score
        
        # Select best algorithm
        best_algorithm_id = max(algorithm_scores.keys(), key=lambda x: algorithm_scores[x]['total_score'])
        best_score_info = algorithm_scores[best_algorithm_id]
        
        # Generate recommendation
        recommendation = AlgorithmRecommendation(
            algorithm_id=best_algorithm_id,
            algorithm_type=candidate_algorithms[best_algorithm_id]['algorithm_type'],
            confidence_score=best_score_info['confidence'],
            expected_performance=best_score_info['expected_performance'],
            estimated_cost=best_score_info['estimated_cost'],
            estimated_time=best_score_info['estimated_time'],
            quantum_advantage=best_score_info['quantum_advantage'],
            reasoning=best_score_info['reasoning'],
            alternative_options=sorted(
                [alg_id for alg_id in algorithm_scores.keys() if alg_id != best_algorithm_id],
                key=lambda x: algorithm_scores[x]['total_score'],
                reverse=True
            )[:3],
            risk_assessment=best_score_info['risk_assessment']
        )
        
        # Record selection
        self.selection_history.append({
            'timestamp': datetime.now(),
            'criteria': criteria,
            'recommendation': recommendation,
            'all_scores': algorithm_scores
        })
        
        logger.info(f"Selected algorithm: {best_algorithm_id} (confidence: {recommendation.confidence_score:.3f})")
        
        return recommendation
    
    async def _score_algorithm(self, algorithm_id: str, algorithm_info: Dict, 
                              criteria: SelectionCriteria) -> Dict[str, Any]:
        """Score an algorithm against selection criteria"""
        # Get benchmark results if available
        benchmark = self.benchmarker.benchmark_results.get(algorithm_id)
        
        if not benchmark:
            # Use default estimates if no benchmark available
            benchmark = self._estimate_algorithm_performance(algorithm_id, algorithm_info, criteria)
        
        # Calculate individual scores
        time_score = self._score_time_performance(benchmark, criteria)
        quality_score = self._score_quality_performance(benchmark, criteria)
        cost_score = self._score_cost_efficiency(benchmark, criteria)
        reliability_score = benchmark.reliability_score if hasattr(benchmark, 'reliability_score') else 0.7
        
        # Weight the scores based on criteria importance
        weights = {
            'time': 0.3,
            'quality': 0.4,
            'cost': 0.2,
            'reliability': 0.1
        }
        
        total_score = (
            time_score * weights['time'] +
            quality_score * weights['quality'] +
            cost_score * weights['cost'] +
            reliability_score * weights['reliability']
        )
        
        # Generate reasoning
        reasoning = []
        if time_score > 0.8:
            reasoning.append("Excellent time performance")
        if quality_score > 0.8:
            reasoning.append("High solution quality")
        if cost_score > 0.8:
            reasoning.append("Cost-efficient")
        if reliability_score > 0.9:
            reasoning.append("Highly reliable")
        
        # Assess quantum advantage
        quantum_advantage = getattr(benchmark, 'quantum_advantage_ratio', 1.0) > 1.2
        if quantum_advantage:
            reasoning.append("Significant quantum advantage")
        
        # Risk assessment
        risk_assessment = {
            'execution_risk': 1.0 - reliability_score,
            'performance_risk': max(0, criteria.time_constraint - getattr(benchmark, 'cpu_time_seconds', 1.0)) / criteria.time_constraint,
            'cost_risk': max(0, criteria.cost_limit - getattr(benchmark, 'cost_per_operation', 0.1)) / criteria.cost_limit
        }
        
        return {
            'total_score': total_score,
            'confidence': min(total_score, reliability_score),
            'expected_performance': {
                PerformanceMetric.EXECUTION_TIME: getattr(benchmark, 'cpu_time_seconds', 1.0),
                PerformanceMetric.SOLUTION_QUALITY: getattr(benchmark, 'quality_score', 0.7),
                PerformanceMetric.COST_EFFICIENCY: cost_score
            },
            'estimated_cost': getattr(benchmark, 'cost_per_operation', 0.1),
            'estimated_time': getattr(benchmark, 'cpu_time_seconds', 1.0),
            'quantum_advantage': quantum_advantage,
            'reasoning': reasoning,
            'risk_assessment': risk_assessment
        }
    
    def _score_time_performance(self, benchmark: Any, criteria: SelectionCriteria) -> float:
        """Score algorithm time performance"""
        estimated_time = getattr(benchmark, 'cpu_time_seconds', 1.0)
        time_constraint = criteria.time_constraint
        
        if estimated_time <= time_constraint * 0.5:
            return 1.0
        elif estimated_time <= time_constraint:
            return 0.8
        elif estimated_time <= time_constraint * 1.5:
            return 0.5
        else:
            return 0.2
    
    def _score_quality_performance(self, benchmark: Any, criteria: SelectionCriteria) -> float:
        """Score algorithm quality performance"""
        quality_score = getattr(benchmark, 'quality_score', 0.7)
        quality_requirement = criteria.accuracy_requirement
        
        if quality_score >= quality_requirement:
            return quality_score
        else:
            return quality_score * 0.5  # Penalty for not meeting requirement
    
    def _score_cost_efficiency(self, benchmark: Any, criteria: SelectionCriteria) -> float:
        """Score algorithm cost efficiency"""
        cost_per_operation = getattr(benchmark, 'cost_per_operation', 0.1)
        cost_limit = criteria.cost_limit
        
        if cost_per_operation <= cost_limit * 0.5:
            return 1.0
        elif cost_per_operation <= cost_limit:
            return 0.8
        elif cost_per_operation <= cost_limit * 1.5:
            return 0.5
        else:
            return 0.2
    
    def _estimate_algorithm_performance(self, algorithm_id: str, algorithm_info: Dict, 
                                       criteria: SelectionCriteria) -> Any:
        """Estimate algorithm performance when no benchmark is available"""
        # Create mock benchmark with reasonable estimates
        class MockBenchmark:
            def __init__(self):
                self.algorithm_id = algorithm_id
                self.quality_score = 0.7
                self.reliability_score = 0.8
                self.cpu_time_seconds = 2.0
                self.cost_per_operation = 0.1
                self.quantum_advantage_ratio = 1.3
        
        return MockBenchmark()
    
    def get_selection_analytics(self) -> Dict[str, Any]:
        """Get analytics on algorithm selection patterns"""
        if not self.selection_history:
            return {}
        
        # Algorithm usage frequency
        algorithm_usage = defaultdict(int)
        for selection in self.selection_history:
            algorithm_usage[selection['recommendation'].algorithm_id] += 1
        
        # Average confidence scores
        avg_confidence = np.mean([s['recommendation'].confidence_score for s in self.selection_history])
        
        # Success rate (simplified)
        success_rate = len([s for s in self.selection_history if s['recommendation'].confidence_score > 0.7]) / len(self.selection_history)
        
        return {
            'total_selections': len(self.selection_history),
            'algorithm_usage': dict(algorithm_usage),
            'average_confidence': avg_confidence,
            'success_rate': success_rate,
            'most_used_algorithm': max(algorithm_usage.keys(), key=algorithm_usage.get) if algorithm_usage else None
        }


# Global performance engine instance
performance_tracker = PerformanceTracker()
benchmarker = AlgorithmBenchmarker(performance_tracker)
algorithm_selector = DynamicAlgorithmSelector(benchmarker)


# Decorator for automatic performance tracking
def track_performance(algorithm_id: str = None):
    """Decorator to automatically track algorithm performance"""
    def decorator(func):
        async def async_wrapper(*args, **kwargs):
            alg_id = algorithm_id or func.__name__
            measurement_id = performance_tracker.start_measurement(alg_id, {'args': len(args), 'kwargs': len(kwargs)})
            
            try:
                result = await func(*args, **kwargs)
                quality = getattr(result, 'confidence_score', 0.7) if hasattr(result, 'confidence_score') else 0.7
                performance_tracker.end_measurement(measurement_id, quality)
                return result
            except Exception as e:
                performance_tracker.end_measurement(measurement_id, 0.0)
                raise e
        
        def sync_wrapper(*args, **kwargs):
            alg_id = algorithm_id or func.__name__
            measurement_id = performance_tracker.start_measurement(alg_id, {'args': len(args), 'kwargs': len(kwargs)})
            
            try:
                result = func(*args, **kwargs)
                quality = getattr(result, 'confidence_score', 0.7) if hasattr(result, 'confidence_score') else 0.7
                performance_tracker.end_measurement(measurement_id, quality)
                return result
            except Exception as e:
                performance_tracker.end_measurement(measurement_id, 0.0)
                raise e
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator


if __name__ == "__main__":
    # Example usage
    async def demo_performance_engine():
        """Demonstrate the performance engine capabilities"""
        logger.info("🚀 Performance Engine Demo")
        
        # Example algorithm registration
        from .quantum_enhanced_algorithms import QuantumPortfolioOptimizer, AlgorithmType
        
        algorithm_selector.register_algorithm(
            "quantum_portfolio_v1",
            QuantumPortfolioOptimizer,
            [AlgorithmComplexity.LOW, AlgorithmComplexity.MEDIUM],
            "portfolio_optimization"
        )
        
        # Example selection criteria
        criteria = SelectionCriteria(
            problem_size=50,
            complexity=AlgorithmComplexity.MEDIUM,
            accuracy_requirement=0.8,
            time_constraint=5.0,
            resource_budget={ResourceType.CLASSICAL_CPU: 80.0},
            quality_threshold=0.7,
            cost_limit=0.2
        )
        
        # Select optimal algorithm
        recommendation = await algorithm_selector.select_optimal_algorithm(criteria)
        logger.info(f"Recommended algorithm: {recommendation.algorithm_id}")
        logger.info(f"Confidence: {recommendation.confidence_score:.3f}")
        logger.info(f"Reasoning: {', '.join(recommendation.reasoning)}")
        
        logger.info("✅ Performance Engine Demo Completed")
    
    # Run demo
    asyncio.run(demo_performance_engine())