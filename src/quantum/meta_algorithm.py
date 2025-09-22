#!/usr/bin/env python3
"""
Dynamic Meta-Algorithm Instituter for Goliath Quantum Starter Platform

This module implements intelligent algorithm selection and tuning based on task type,
performance metrics, and adaptive learning. Enables the platform to dynamically
choose optimal algorithms and self-improve through logged metrics.

Author: Goliath Quantum Division
Version: 1.0.0
"""

import numpy as np
import asyncio
from typing import Dict, Any, Optional, List, Tuple
import logging
import time
from enum import Enum

# Import quantum algorithms
from .reasoning import reversal_reasoning, ReversalReasoning
from .optimization import parallel_qaoa, optimize_qaoa, qaoa_engine
from .diffusion import quantum_diffusion, parallel_quantum_diffusion, diffusion_engine

logger = logging.getLogger(__name__)

class TaskType(Enum):
    """Enumeration of supported task types"""
    REASONING = "reasoning"
    OPTIMIZATION = "optimization"
    DIFFUSION = "diffusion"
    ENERGY_OPTIMIZATION = "energy_optimization"
    SCENARIO_GENERATION = "scenario_generation"
    PORTFOLIO_OPTIMIZATION = "portfolio_optimization"
    UNKNOWN = "unknown"

class AlgorithmPerformance:
    """Track algorithm performance metrics"""
    
    def __init__(self, algorithm_name: str):
        self.algorithm_name = algorithm_name
        self.execution_times = []
        self.success_rates = []
        self.quality_scores = []
        self.usage_count = 0
        self.last_used = None
        
    def record_execution(self, execution_time: float, success: bool, quality_score: float = 0.0):
        """Record algorithm execution metrics"""
        self.execution_times.append(execution_time)
        self.success_rates.append(1.0 if success else 0.0)
        self.quality_scores.append(quality_score)
        self.usage_count += 1
        self.last_used = time.time()
        
        # Keep only recent metrics (last 100 executions)
        if len(self.execution_times) > 100:
            self.execution_times = self.execution_times[-100:]
            self.success_rates = self.success_rates[-100:]
            self.quality_scores = self.quality_scores[-100:]
    
    def get_performance_score(self) -> float:
        """Calculate overall performance score"""
        if not self.execution_times:
            return 0.0
            
        # Weighted score: success rate (40%), speed (30%), quality (30%)
        avg_success = np.mean(self.success_rates)
        avg_speed = 1.0 / (np.mean(self.execution_times) + 1e-6)  # Inverse of time
        avg_quality = np.mean(self.quality_scores) if self.quality_scores else 0.5
        
        # Normalize speed (assume 1 second is baseline)
        normalized_speed = min(1.0, avg_speed)
        
        performance_score = (0.4 * avg_success + 0.3 * normalized_speed + 0.3 * avg_quality)
        return performance_score

class DynamicAlgorithmInstituter:
    """Dynamic algorithm selection and tuning system"""
    
    def __init__(self):
        self.performance_tracker = {
            'reversal_reasoning': AlgorithmPerformance('reversal_reasoning'),
            'parallel_qaoa': AlgorithmPerformance('parallel_qaoa'),
            'single_qaoa': AlgorithmPerformance('single_qaoa'),
            'quantum_diffusion': AlgorithmPerformance('quantum_diffusion'),
            'parallel_diffusion': AlgorithmPerformance('parallel_diffusion')
        }
        
        # Task-to-algorithm mapping with preferences
        self.task_algorithm_map = {
            TaskType.REASONING: ['reversal_reasoning'],
            TaskType.OPTIMIZATION: ['parallel_qaoa', 'single_qaoa'],
            TaskType.DIFFUSION: ['quantum_diffusion', 'parallel_diffusion'],
            TaskType.ENERGY_OPTIMIZATION: ['parallel_qaoa'],
            TaskType.SCENARIO_GENERATION: ['quantum_diffusion', 'parallel_diffusion'],
            TaskType.PORTFOLIO_OPTIMIZATION: ['parallel_qaoa', 'single_qaoa']
        }
        
        self.adaptation_threshold = 0.1  # Threshold for algorithm switching
        self.learning_rate = 0.05
        
    def classify_task(self, task_type: str, data: Dict[str, Any]) -> TaskType:
        """Classify task type from input parameters"""
        task_lower = task_type.lower()
        
        # Direct mapping
        if task_lower in ['reasoning', 'inference', 'logic']:
            return TaskType.REASONING
        elif task_lower in ['optimization', 'optimize']:
            # Check for specific optimization types
            if 'energy' in str(data).lower():
                return TaskType.ENERGY_OPTIMIZATION
            elif 'portfolio' in str(data).lower():
                return TaskType.PORTFOLIO_OPTIMIZATION
            return TaskType.OPTIMIZATION
        elif task_lower in ['diffusion', 'scenario', 'generation']:
            return TaskType.DIFFUSION
        elif task_lower in ['energy']:
            return TaskType.ENERGY_OPTIMIZATION
        
        # Heuristic classification based on data structure
        if 'premise' in data and 'conclusion' in data:
            return TaskType.REASONING
        elif 'matrix' in data or 'matrices' in data or 'graph' in data:
            return TaskType.OPTIMIZATION
        elif 'steps' in data and 'dim' in data:
            return TaskType.DIFFUSION
        
        return TaskType.UNKNOWN
    
    def select_algorithm(self, task_type: TaskType, data: Dict[str, Any]) -> str:
        """Select optimal algorithm for given task type"""
        available_algorithms = self.task_algorithm_map.get(task_type, [])
        
        if not available_algorithms:
            logger.warning(f"No algorithms available for task type: {task_type}")
            return 'reversal_reasoning'  # Default fallback
        
        # If only one algorithm available, use it
        if len(available_algorithms) == 1:
            return available_algorithms[0]
        
        # Select based on performance scores
        best_algorithm = available_algorithms[0]
        best_score = 0.0
        
        for algorithm in available_algorithms:
            if algorithm in self.performance_tracker:
                score = self.performance_tracker[algorithm].get_performance_score()
                
                # Add exploration bonus for less-used algorithms
                usage_penalty = min(0.1, self.performance_tracker[algorithm].usage_count / 1000)
                adjusted_score = score - usage_penalty
                
                if adjusted_score > best_score:
                    best_score = adjusted_score
                    best_algorithm = algorithm
        
        logger.info(f"Selected algorithm '{best_algorithm}' for task '{task_type}' (score: {best_score:.3f})")
        return best_algorithm
    
    async def execute_algorithm(self, algorithm_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute selected algorithm with performance tracking"""
        start_time = time.time()
        success = False
        result = {}
        quality_score = 0.0
        
        try:
            if algorithm_name == 'reversal_reasoning':
                premise = data.get('premise', '')
                conclusion = data.get('conclusion', '')
                threshold = data.get('coherence_threshold', 0.9)
                
                result = reversal_reasoning(premise, conclusion, threshold)
                quality_score = result.get('coherence_score', 0.0) if isinstance(result, dict) else 0.5
                success = True
                
            elif algorithm_name == 'parallel_qaoa':
                matrices = data.get('matrices', data.get('graph_matrices', []))
                if isinstance(matrices[0], list):  # Convert to numpy if needed
                    matrices = [np.array(m) for m in matrices]
                
                num_workers = data.get('num_workers', 4)
                problem_type = data.get('problem_type', 'portfolio')
                
                results = parallel_qaoa(matrices, num_workers, problem_type)
                result = {
                    'optimized_parameters': [r[0].tolist() for r in results],
                    'costs': [float(r[1]) for r in results]
                }
                
                # Quality based on cost improvement
                avg_cost = np.mean([r[1] for r in results])
                quality_score = max(0.0, min(1.0, 1.0 - abs(avg_cost)))
                success = True
                
            elif algorithm_name == 'single_qaoa':
                matrix = data.get('matrix', data.get('graph_matrix', []))
                if isinstance(matrix, list):
                    matrix = np.array(matrix)
                
                problem_type = data.get('problem_type', 'portfolio')
                params, cost = optimize_qaoa(matrix, problem_type)
                
                result = {
                    'optimized_parameters': params.tolist(),
                    'cost': float(cost)
                }
                
                quality_score = max(0.0, min(1.0, 1.0 - abs(cost)))
                success = True
                
            elif algorithm_name == 'quantum_diffusion':
                steps = data.get('steps', 10)
                dim = data.get('dim', 2)
                threshold = data.get('efficiency_threshold', 0.8)
                
                states = quantum_diffusion(steps, dim, threshold)
                result = {
                    'diffusion_states': [s.tolist() for s in states],
                    'num_states': len(states)
                }
                
                # Quality based on state diversity
                if states:
                    entropies = []
                    for state in states:
                        probs = np.abs(state) ** 2
                        probs = probs[probs > 1e-10]
                        if len(probs) > 0:
                            entropy = -np.sum(probs * np.log2(probs))
                            entropies.append(entropy)
                    quality_score = np.mean(entropies) / np.log2(dim) if entropies else 0.5
                else:
                    quality_score = 0.0
                    
                success = True
                
            elif algorithm_name == 'parallel_diffusion':
                scenarios = data.get('scenarios', [])
                max_workers = data.get('max_workers', 4)
                
                results = await parallel_quantum_diffusion(scenarios, max_workers)
                result = {
                    'results': [[s.tolist() for s in states] for states in results],
                    'num_scenarios': len(results)
                }
                
                quality_score = 0.8  # Default quality for parallel execution
                success = True
                
            else:
                raise ValueError(f"Unknown algorithm: {algorithm_name}")
                
        except Exception as e:
            logger.error(f"Error executing algorithm '{algorithm_name}': {e}")
            result = {'error': str(e)}
            success = False
            quality_score = 0.0
        
        # Record performance
        execution_time = time.time() - start_time
        if algorithm_name in self.performance_tracker:
            self.performance_tracker[algorithm_name].record_execution(
                execution_time, success, quality_score
            )
        
        # Add metadata to result
        result.update({
            'algorithm_used': algorithm_name,
            'execution_time': execution_time,
            'success': success,
            'quality_score': quality_score
        })
        
        return result
    
    async def dynamic_algo_instituter(self, task_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Main entry point for dynamic algorithm institution"""
        logger.info(f"Processing task: {task_type}")
        
        # Classify task
        classified_task = self.classify_task(task_type, data)
        
        # Select optimal algorithm
        selected_algorithm = self.select_algorithm(classified_task, data)
        
        # Execute algorithm
        result = await self.execute_algorithm(selected_algorithm, data)
        
        # Add meta-information
        result.update({
            'task_type': task_type,
            'classified_as': classified_task.value,
            'selected_algorithm': selected_algorithm,
            'meta_instituted': True
        })
        
        logger.info(f"Task completed: {task_type} -> {selected_algorithm} (success: {result.get('success', False)})")
        return result
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance summary for all algorithms"""
        summary = {
            'total_executions': sum(tracker.usage_count for tracker in self.performance_tracker.values()),
            'algorithms': {}
        }
        
        for name, tracker in self.performance_tracker.items():
            summary['algorithms'][name] = {
                'usage_count': tracker.usage_count,
                'performance_score': tracker.get_performance_score(),
                'avg_execution_time': np.mean(tracker.execution_times) if tracker.execution_times else 0.0,
                'success_rate': np.mean(tracker.success_rates) if tracker.success_rates else 0.0,
                'avg_quality': np.mean(tracker.quality_scores) if tracker.quality_scores else 0.0
            }
        
        return summary
    
    def adapt_algorithm_preferences(self):
        """Adapt algorithm preferences based on performance history"""
        for task_type, algorithms in self.task_algorithm_map.items():
            if len(algorithms) > 1:
                # Sort algorithms by performance score
                algorithm_scores = []
                for algo in algorithms:
                    if algo in self.performance_tracker:
                        score = self.performance_tracker[algo].get_performance_score()
                        algorithm_scores.append((algo, score))
                
                # Reorder based on performance
                algorithm_scores.sort(key=lambda x: x[1], reverse=True)
                self.task_algorithm_map[task_type] = [algo for algo, _ in algorithm_scores]
                
                logger.info(f"Adapted preferences for {task_type}: {self.task_algorithm_map[task_type]}")

# Global meta-algorithm instituter instance
meta_instituter = DynamicAlgorithmInstituter()

# Convenience function for easy integration
async def dynamic_algo_instituter(task_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function for dynamic algorithm institution.
    
    Args:
        task_type: Type of task to execute
        data: Task data and parameters
        
    Returns:
        Algorithm execution result with metadata
    """
    return await meta_instituter.dynamic_algo_instituter(task_type, data)

def get_meta_performance() -> Dict[str, Any]:
    """
    Get meta-algorithm performance summary.
    
    Returns:
        Performance summary dictionary
    """
    return meta_instituter.get_performance_summary()

def adapt_preferences():
    """
    Trigger algorithm preference adaptation.
    """
    meta_instituter.adapt_algorithm_preferences()

# Example usage and testing
if __name__ == "__main__":
    import asyncio
    
    async def test_meta_algorithm():
        print("Testing Dynamic Meta-Algorithm Instituter...")
        
        # Test 1: Reasoning task
        reasoning_data = {
            'premise': 'Strong market performance',
            'conclusion': 'Invest in growth stocks'
        }
        result1 = await dynamic_algo_instituter('reasoning', reasoning_data)
        print(f"Reasoning result: {result1.get('selected_algorithm')}")
        
        # Test 2: Optimization task
        optimization_data = {
            'matrices': [[[0, 1], [1, 0]], [[0, 2], [2, 0]]],
            'problem_type': 'portfolio'
        }
        result2 = await dynamic_algo_instituter('optimization', optimization_data)
        print(f"Optimization result: {result2.get('selected_algorithm')}")
        
        # Test 3: Diffusion task
        diffusion_data = {
            'steps': 5,
            'dim': 2
        }
        result3 = await dynamic_algo_instituter('diffusion', diffusion_data)
        print(f"Diffusion result: {result3.get('selected_algorithm')}")
        
        # Performance summary
        summary = get_meta_performance()
        print(f"Performance summary: {summary}")
        
        print("Meta-Algorithm testing completed!")
    
    asyncio.run(test_meta_algorithm())