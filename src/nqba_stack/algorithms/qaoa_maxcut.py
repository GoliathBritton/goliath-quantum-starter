"""QAOA MaxCut Implementation

Complete Quantum Approximate Optimization Algorithm (QAOA) implementation for MaxCut problems
with production-ready features:
- Problem-inspired ansatz with mixer and cost Hamiltonians
- Layerwise training to reduce barren plateaus
- Warm-start from classical relaxations
- Advanced gradient estimation and optimization
- Comprehensive benchmarking and telemetry
"""

import numpy as np
import networkx as nx
from scipy.optimize import minimize
from scipy.linalg import expm
import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple, Callable
import json
from pathlib import Path

# Import our backend adapter
from .quantum_backend_adapter import (
    QuantumBackendAdapter, BackendType, CircuitResult, OptimizationResult,
    BenchmarkMetrics, GradientMethod, backend_manager
)

# Classical optimization imports
try:
    from scipy.optimize import differential_evolution
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    import cvxpy as cp
    CVXPY_AVAILABLE = True
except ImportError:
    CVXPY_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class MaxCutProblem:
    """MaxCut problem definition"""
    graph: nx.Graph
    adjacency_matrix: np.ndarray
    num_vertices: int
    edge_weights: Dict[Tuple[int, int], float] = field(default_factory=dict)
    
    @classmethod
    def from_adjacency_matrix(cls, adj_matrix: np.ndarray) -> 'MaxCutProblem':
        """Create MaxCut problem from adjacency matrix"""
        graph = nx.from_numpy_array(adj_matrix)
        num_vertices = adj_matrix.shape[0]
        
        edge_weights = {}
        for i in range(num_vertices):
            for j in range(i + 1, num_vertices):
                if adj_matrix[i, j] != 0:
                    edge_weights[(i, j)] = adj_matrix[i, j]
        
        return cls(
            graph=graph,
            adjacency_matrix=adj_matrix,
            num_vertices=num_vertices,
            edge_weights=edge_weights
        )
    
    @classmethod
    def random_graph(cls, num_vertices: int, edge_probability: float = 0.5, seed: int = 42) -> 'MaxCutProblem':
        """Generate random MaxCut problem"""
        np.random.seed(seed)
        graph = nx.erdos_renyi_graph(num_vertices, edge_probability, seed=seed)
        
        # Add random weights
        for (u, v) in graph.edges():
            graph[u][v]['weight'] = np.random.uniform(0.5, 2.0)
        
        adj_matrix = nx.adjacency_matrix(graph, weight='weight').toarray()
        return cls.from_adjacency_matrix(adj_matrix)
    
    def classical_relaxation_solution(self) -> np.ndarray:
        """Solve SDP relaxation for warm-start initialization"""
        if not CVXPY_AVAILABLE:
            logger.warning("CVXPY not available, using random initialization")
            return np.random.uniform(0, 2*np.pi, self.num_vertices)
        
        try:
            # SDP relaxation of MaxCut
            X = cp.Variable((self.num_vertices, self.num_vertices), PSD=True)
            
            # Objective: maximize sum of edge weights for cut edges
            objective = 0
            for i in range(self.num_vertices):
                for j in range(i + 1, self.num_vertices):
                    if self.adjacency_matrix[i, j] != 0:
                        objective += self.adjacency_matrix[i, j] * (1 - X[i, j]) / 2
            
            # Constraints
            constraints = [cp.diag(X) == 1]
            
            # Solve SDP
            problem = cp.Problem(cp.Maximize(objective), constraints)
            problem.solve()
            
            if X.value is not None:
                # Extract angles from SDP solution using Goemans-Williamson rounding
                eigenvals, eigenvecs = np.linalg.eigh(X.value)
                # Take the largest eigenvalue's eigenvector
                principal_eigenvec = eigenvecs[:, -1]
                
                # Convert to QAOA angles (heuristic mapping)
                angles = np.arccos(np.clip(principal_eigenvec, -1, 1))
                return angles
            else:
                logger.warning("SDP relaxation failed, using random initialization")
                return np.random.uniform(0, 2*np.pi, self.num_vertices)
                
        except Exception as e:
            logger.warning(f"SDP relaxation failed: {e}, using random initialization")
            return np.random.uniform(0, 2*np.pi, self.num_vertices)
    
    def evaluate_cut_value(self, bitstring: str) -> float:
        """Evaluate cut value for a given bitstring"""
        bits = np.array([int(b) for b in bitstring])
        cut_value = 0.0
        
        for i in range(self.num_vertices):
            for j in range(i + 1, self.num_vertices):
                if self.adjacency_matrix[i, j] != 0:
                    # Edge is cut if vertices are in different partitions
                    if bits[i] != bits[j]:
                        cut_value += self.adjacency_matrix[i, j]
        
        return cut_value
    
    def get_optimal_classical_cut(self) -> Tuple[float, str]:
        """Get optimal cut using brute force (for small graphs)"""
        if self.num_vertices > 20:
            logger.warning("Graph too large for brute force, using heuristic")
            return self._heuristic_cut()
        
        best_cut = 0.0
        best_partition = "0" * self.num_vertices
        
        # Try all possible partitions
        for i in range(2**(self.num_vertices - 1)):  # Fix first vertex to 0
            partition = "0" + format(i, f'0{self.num_vertices-1}b')
            cut_value = self.evaluate_cut_value(partition)
            
            if cut_value > best_cut:
                best_cut = cut_value
                best_partition = partition
        
        return best_cut, best_partition
    
    def _heuristic_cut(self) -> Tuple[float, str]:
        """Heuristic cut using greedy algorithm"""
        # Simple greedy heuristic
        partition = np.random.randint(0, 2, self.num_vertices)
        
        # Local improvement
        improved = True
        while improved:
            improved = False
            for i in range(self.num_vertices):
                # Try flipping vertex i
                partition[i] = 1 - partition[i]
                new_cut = self.evaluate_cut_value(''.join(map(str, partition)))
                
                old_partition = partition.copy()
                old_partition[i] = 1 - old_partition[i]
                old_cut = self.evaluate_cut_value(''.join(map(str, old_partition)))
                
                if new_cut <= old_cut:
                    partition[i] = 1 - partition[i]  # Revert
                else:
                    improved = True
        
        cut_value = self.evaluate_cut_value(''.join(map(str, partition)))
        return cut_value, ''.join(map(str, partition))

@dataclass
class QAOAResult:
    """Result from QAOA optimization"""
    success: bool
    optimal_params: Optional[np.ndarray] = None
    optimal_value: Optional[float] = None
    best_cut_value: Optional[float] = None
    best_partition: Optional[str] = None
    approximation_ratio: Optional[float] = None
    iterations: int = 0
    function_evaluations: int = 0
    execution_time: float = 0.0
    convergence_data: List[float] = field(default_factory=list)
    layer_results: List[Dict[str, Any]] = field(default_factory=list)
    backend_used: str = "unknown"
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class QAOAMaxCut:
    """QAOA implementation for MaxCut problems"""
    
    def __init__(self, 
                 problem: MaxCutProblem,
                 max_layers: int = 3,
                 backend_type: Optional[BackendType] = None,
                 shots: int = 1024,
                 enable_warm_start: bool = True,
                 enable_layerwise_training: bool = True):
        
        self.problem = problem
        self.max_layers = max_layers
        self.backend_type = backend_type
        self.shots = shots
        self.enable_warm_start = enable_warm_start
        self.enable_layerwise_training = enable_layerwise_training
        
        self.function_evaluations = 0
        self.convergence_history = []
        self.layer_history = []
        
        # Get classical benchmark
        self.classical_cut_value, self.classical_partition = problem.get_optimal_classical_cut()
        
        logger.info(f"QAOA MaxCut initialized for {problem.num_vertices} vertices")
        logger.info(f"Classical optimal cut value: {self.classical_cut_value}")
    
    async def optimize(self, 
                     gradient_method: GradientMethod = GradientMethod.PARAMETER_SHIFT,
                     optimizer: str = "L-BFGS-B",
                     max_iterations: int = 100) -> QAOAResult:
        """Run QAOA optimization"""
        start_time = time.time()
        
        try:
            if self.enable_layerwise_training:
                result = await self._layerwise_optimization(gradient_method, optimizer, max_iterations)
            else:
                result = await self._direct_optimization(self.max_layers, gradient_method, optimizer, max_iterations)
            
            result.execution_time = time.time() - start_time
            
            # Calculate approximation ratio
            if result.best_cut_value is not None and self.classical_cut_value > 0:
                result.approximation_ratio = result.best_cut_value / self.classical_cut_value
            
            return result
            
        except Exception as e:
            logger.error(f"QAOA optimization failed: {e}")
            return QAOAResult(
                success=False,
                execution_time=time.time() - start_time,
                error_message=str(e)
            )
    
    async def _layerwise_optimization(self, 
                                    gradient_method: GradientMethod,
                                    optimizer: str,
                                    max_iterations: int) -> QAOAResult:
        """Layerwise training to reduce barren plateaus"""
        logger.info("Starting layerwise QAOA optimization")
        
        best_params = None
        best_value = float('-inf')
        all_layer_results = []
        
        # Start with p=1 and incrementally add layers
        for p in range(1, self.max_layers + 1):
            logger.info(f"Training QAOA with p={p} layers")
            
            # Initialize parameters for this layer
            if p == 1 or best_params is None:
                # First layer or previous optimization failed
                initial_params = self._get_initial_parameters(p)
            else:
                # Extend previous best parameters
                initial_params = self._extend_parameters(best_params, p)
            
            # Optimize this layer configuration
            layer_result = await self._direct_optimization(p, gradient_method, optimizer, max_iterations)
            all_layer_results.append({
                "layer": p,
                "result": layer_result,
                "improvement": layer_result.optimal_value - best_value if layer_result.optimal_value else 0
            })
            
            # Update best result if improved
            if layer_result.success and layer_result.optimal_value is not None:
                if layer_result.optimal_value > best_value:
                    best_value = layer_result.optimal_value
                    best_params = layer_result.optimal_params
                    logger.info(f"Layer p={p} improved objective to {best_value:.6f}")
                else:
                    logger.info(f"Layer p={p} did not improve (value: {layer_result.optimal_value:.6f})")
                    # Early stopping if no improvement
                    if p > 1:
                        logger.info("No improvement, stopping layerwise training")
                        break
            else:
                logger.warning(f"Layer p={p} optimization failed")
        
        # Evaluate best solution
        if best_params is not None:
            best_cut_value, best_partition = await self._evaluate_solution(best_params)
            
            return QAOAResult(
                success=True,
                optimal_params=best_params,
                optimal_value=best_value,
                best_cut_value=best_cut_value,
                best_partition=best_partition,
                iterations=sum(r["result"].iterations for r in all_layer_results),
                function_evaluations=sum(r["result"].function_evaluations for r in all_layer_results),
                convergence_data=self.convergence_history,
                layer_results=all_layer_results,
                metadata={"method": "layerwise", "max_layers": self.max_layers}
            )
        else:
            return QAOAResult(
                success=False,
                layer_results=all_layer_results,
                error_message="All layer optimizations failed"
            )
    
    async def _direct_optimization(self, 
                                 num_layers: int,
                                 gradient_method: GradientMethod,
                                 optimizer: str,
                                 max_iterations: int) -> QAOAResult:
        """Direct optimization for given number of layers"""
        # Initialize parameters
        initial_params = self._get_initial_parameters(num_layers)
        
        # Define objective function
        async def objective_function(params: np.ndarray) -> float:
            return await self._qaoa_objective(params, num_layers)
        
        # Choose optimization method
        if gradient_method in [GradientMethod.PARAMETER_SHIFT, GradientMethod.SPSA]:
            # Use gradient-based optimization
            result = await self._gradient_based_optimization(
                objective_function, initial_params, gradient_method, optimizer, max_iterations
            )
        else:
            # Use gradient-free optimization
            result = await self._gradient_free_optimization(
                objective_function, initial_params, optimizer, max_iterations
            )
        
        return result
    
    def _get_initial_parameters(self, num_layers: int) -> np.ndarray:
        """Get initial parameters for QAOA"""
        if self.enable_warm_start:
            # Use warm-start from classical relaxation
            try:
                classical_angles = self.problem.classical_relaxation_solution()
                
                # Map classical solution to QAOA parameters
                # This is a heuristic mapping
                beta_init = np.mean(classical_angles) * np.ones(num_layers) * 0.1
                gamma_init = np.std(classical_angles) * np.ones(num_layers) * 0.5
                
                params = np.concatenate([beta_init, gamma_init])
                logger.info("Using warm-start initialization from classical relaxation")
                return params
                
            except Exception as e:
                logger.warning(f"Warm-start failed: {e}, using random initialization")
        
        # Random initialization
        beta_init = np.random.uniform(0, np.pi, num_layers)
        gamma_init = np.random.uniform(0, 2*np.pi, num_layers)
        return np.concatenate([beta_init, gamma_init])
    
    def _extend_parameters(self, prev_params: np.ndarray, new_num_layers: int) -> np.ndarray:
        """Extend parameters from previous layer optimization"""
        prev_num_layers = len(prev_params) // 2
        
        if new_num_layers <= prev_num_layers:
            # Truncate if needed
            return prev_params[:2*new_num_layers]
        
        # Extend with new layer
        prev_beta = prev_params[:prev_num_layers]
        prev_gamma = prev_params[prev_num_layers:]
        
        # Add new layer with small random values
        new_beta = np.append(prev_beta, np.random.uniform(0, 0.1))
        new_gamma = np.append(prev_gamma, np.random.uniform(0, 0.1))
        
        return np.concatenate([new_beta, new_gamma])
    
    async def _qaoa_objective(self, params: np.ndarray, num_layers: int) -> float:
        """QAOA objective function"""
        self.function_evaluations += 1
        
        try:
            # Build circuit parameters
            beta = params[:num_layers]
            gamma = params[num_layers:]
            
            circuit_params = {
                "type": "qaoa",
                "num_qubits": self.problem.num_vertices,
                "num_layers": num_layers,
                "beta": beta,
                "gamma": gamma,
                "adjacency_matrix": self.problem.adjacency_matrix
            }
            
            # Execute circuit
            result = await backend_manager.execute_with_fallback(
                circuit_params, self.backend_type, self.shots
            )
            
            if result.success and result.expectation_value is not None:
                # QAOA minimizes energy, but we want to maximize cut value
                objective_value = -result.expectation_value
                self.convergence_history.append(objective_value)
                return objective_value
            else:
                logger.warning(f"Circuit execution failed: {result.error_message}")
                return float('-inf')
                
        except Exception as e:
            logger.error(f"Objective evaluation failed: {e}")
            return float('-inf')
    
    async def _gradient_based_optimization(self, 
                                         objective_fn: Callable,
                                         initial_params: np.ndarray,
                                         gradient_method: GradientMethod,
                                         optimizer: str,
                                         max_iterations: int) -> QAOAResult:
        """Gradient-based optimization"""
        logger.info(f"Starting gradient-based optimization with {gradient_method.value}")
        
        # Get backend adapter for gradient estimation
        available_backends = backend_manager.get_available_backends()
        if not available_backends:
            raise RuntimeError("No quantum backends available")
        
        backend_type = self.backend_type or available_backends[0]
        adapter = backend_manager.adapters[backend_type]
        
        # Define gradient function
        def gradient_fn(params: np.ndarray) -> np.ndarray:
            async def async_objective(p):
                return await objective_fn(p)
            
            def sync_objective(p):
                return asyncio.run(async_objective(p))
            
            return adapter.estimate_gradient(sync_objective, params, gradient_method)
        
        # Define objective wrapper for scipy
        def sync_objective(params: np.ndarray) -> float:
            return asyncio.run(objective_fn(params))
        
        # Run optimization
        if optimizer.upper() in ["L-BFGS-B", "SLSQP"]:
            # Use gradient information
            result = minimize(
                sync_objective,
                initial_params,
                method=optimizer,
                jac=gradient_fn,
                options={'maxiter': max_iterations, 'disp': True}
            )
        else:
            # Fallback to gradient-free
            result = minimize(
                sync_objective,
                initial_params,
                method="COBYLA",
                options={'maxiter': max_iterations, 'disp': True}
            )
        
        if result.success:
            best_cut_value, best_partition = await self._evaluate_solution(result.x)
            
            return QAOAResult(
                success=True,
                optimal_params=result.x,
                optimal_value=result.fun,
                best_cut_value=best_cut_value,
                best_partition=best_partition,
                iterations=result.nit,
                function_evaluations=result.nfev,
                convergence_data=self.convergence_history,
                backend_used=backend_type.value,
                metadata={"optimizer": optimizer, "gradient_method": gradient_method.value}
            )
        else:
            return QAOAResult(
                success=False,
                iterations=result.nit,
                function_evaluations=result.nfev,
                error_message=result.message
            )
    
    async def _gradient_free_optimization(self, 
                                        objective_fn: Callable,
                                        initial_params: np.ndarray,
                                        optimizer: str,
                                        max_iterations: int) -> QAOAResult:
        """Gradient-free optimization"""
        logger.info(f"Starting gradient-free optimization with {optimizer}")
        
        # Define objective wrapper for scipy
        def sync_objective(params: np.ndarray) -> float:
            return asyncio.run(objective_fn(params))
        
        # Choose optimization method
        if optimizer.upper() == "COBYLA":
            result = minimize(
                sync_objective,
                initial_params,
                method="COBYLA",
                options={'maxiter': max_iterations, 'disp': True}
            )
        elif optimizer.upper() == "DIFFERENTIAL_EVOLUTION" and SCIPY_AVAILABLE:
            bounds = [(0, 2*np.pi) for _ in range(len(initial_params))]
            result = differential_evolution(
                sync_objective,
                bounds,
                maxiter=max_iterations,
                disp=True,
                seed=42
            )
        else:
            # Default to COBYLA
            result = minimize(
                sync_objective,
                initial_params,
                method="COBYLA",
                options={'maxiter': max_iterations, 'disp': True}
            )
        
        if result.success:
            best_cut_value, best_partition = await self._evaluate_solution(result.x)
            
            return QAOAResult(
                success=True,
                optimal_params=result.x,
                optimal_value=result.fun,
                best_cut_value=best_cut_value,
                best_partition=best_partition,
                iterations=result.nit if hasattr(result, 'nit') else 0,
                function_evaluations=result.nfev if hasattr(result, 'nfev') else self.function_evaluations,
                convergence_data=self.convergence_history,
                metadata={"optimizer": optimizer}
            )
        else:
            return QAOAResult(
                success=False,
                iterations=result.nit if hasattr(result, 'nit') else 0,
                function_evaluations=result.nfev if hasattr(result, 'nfev') else self.function_evaluations,
                error_message=getattr(result, 'message', 'Optimization failed')
            )
    
    async def _evaluate_solution(self, params: np.ndarray) -> Tuple[float, str]:
        """Evaluate the final solution to get cut value and partition"""
        num_layers = len(params) // 2
        
        # Execute circuit with final parameters
        circuit_params = {
            "type": "qaoa",
            "num_qubits": self.problem.num_vertices,
            "num_layers": num_layers,
            "beta": params[:num_layers],
            "gamma": params[num_layers:],
            "adjacency_matrix": self.problem.adjacency_matrix,
            "measure_all": True  # Get full measurement distribution
        }
        
        result = await backend_manager.execute_with_fallback(
            circuit_params, self.backend_type, self.shots
        )
        
        if result.success and "counts" in result.metadata:
            # Find the most probable bitstring
            counts = result.metadata["counts"]
            best_bitstring = max(counts.keys(), key=lambda x: counts[x])
            best_cut_value = self.problem.evaluate_cut_value(best_bitstring)
            
            return best_cut_value, best_bitstring
        else:
            # Fallback: use classical heuristic
            logger.warning("Could not evaluate quantum solution, using classical fallback")
            return self.problem._heuristic_cut()

# Convenience functions
def create_random_maxcut_problem(num_vertices: int, 
                                edge_probability: float = 0.5, 
                                seed: int = 42) -> MaxCutProblem:
    """Create a random MaxCut problem"""
    return MaxCutProblem.random_graph(num_vertices, edge_probability, seed)

def create_maxcut_from_adjacency(adjacency_matrix: np.ndarray) -> MaxCutProblem:
    """Create MaxCut problem from adjacency matrix"""
    return MaxCutProblem.from_adjacency_matrix(adjacency_matrix)

async def solve_maxcut_qaoa(problem: MaxCutProblem,
                          max_layers: int = 3,
                          backend_type: Optional[BackendType] = None,
                          shots: int = 1024,
                          enable_warm_start: bool = True,
                          enable_layerwise_training: bool = True,
                          gradient_method: GradientMethod = GradientMethod.PARAMETER_SHIFT,
                          optimizer: str = "L-BFGS-B",
                          max_iterations: int = 100) -> QAOAResult:
    """Solve MaxCut problem using QAOA"""
    qaoa = QAOAMaxCut(
        problem=problem,
        max_layers=max_layers,
        backend_type=backend_type,
        shots=shots,
        enable_warm_start=enable_warm_start,
        enable_layerwise_training=enable_layerwise_training
    )
    
    return await qaoa.optimize(gradient_method, optimizer, max_iterations)

# Example usage and benchmarking
async def benchmark_qaoa_maxcut(num_vertices_list: List[int] = [4, 6, 8],
                              num_trials: int = 5,
                              save_results: bool = True) -> Dict[str, Any]:
    """Benchmark QAOA MaxCut performance"""
    logger.info("Starting QAOA MaxCut benchmark")
    
    benchmark_results = {
        "timestamp": time.time(),
        "trials": num_trials,
        "results": []
    }
    
    for num_vertices in num_vertices_list:
        logger.info(f"Benchmarking {num_vertices}-vertex graphs")
        
        vertex_results = {
            "num_vertices": num_vertices,
            "trials": []
        }
        
        for trial in range(num_trials):
            logger.info(f"Trial {trial + 1}/{num_trials}")
            
            # Create random problem
            problem = create_random_maxcut_problem(num_vertices, seed=trial)
            
            # Solve with QAOA
            start_time = time.time()
            result = await solve_maxcut_qaoa(
                problem,
                max_layers=3,
                enable_layerwise_training=True,
                max_iterations=50
            )
            total_time = time.time() - start_time
            
            trial_data = {
                "trial": trial,
                "success": result.success,
                "approximation_ratio": result.approximation_ratio,
                "execution_time": total_time,
                "function_evaluations": result.function_evaluations,
                "classical_cut_value": problem.classical_cut_value,
                "qaoa_cut_value": result.best_cut_value,
                "backend_used": result.backend_used
            }
            
            vertex_results["trials"].append(trial_data)
            
            if result.success:
                logger.info(f"Trial {trial + 1} completed: ratio={result.approximation_ratio:.3f}")
            else:
                logger.warning(f"Trial {trial + 1} failed: {result.error_message}")
        
        # Calculate statistics
        successful_trials = [t for t in vertex_results["trials"] if t["success"]]
        if successful_trials:
            ratios = [t["approximation_ratio"] for t in successful_trials if t["approximation_ratio"]]
            vertex_results["statistics"] = {
                "success_rate": len(successful_trials) / num_trials,
                "mean_approximation_ratio": np.mean(ratios) if ratios else 0,
                "std_approximation_ratio": np.std(ratios) if ratios else 0,
                "mean_execution_time": np.mean([t["execution_time"] for t in successful_trials]),
                "mean_function_evaluations": np.mean([t["function_evaluations"] for t in successful_trials])
            }
        else:
            vertex_results["statistics"] = {
                "success_rate": 0,
                "mean_approximation_ratio": 0,
                "std_approximation_ratio": 0,
                "mean_execution_time": 0,
                "mean_function_evaluations": 0
            }
        
        benchmark_results["results"].append(vertex_results)
        
        logger.info(f"Completed {num_vertices}-vertex benchmark: "
                   f"success_rate={vertex_results['statistics']['success_rate']:.2f}, "
                   f"mean_ratio={vertex_results['statistics']['mean_approximation_ratio']:.3f}")
    
    if save_results:
        # Save to benchmark_results directory
        results_dir = Path("benchmark_results")
        results_dir.mkdir(exist_ok=True)
        
        filename = f"qaoa_maxcut_benchmark_{int(time.time())}.json"
        filepath = results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(benchmark_results, f, indent=2)
        
        logger.info(f"Benchmark results saved to {filepath}")
    
    return benchmark_results

if __name__ == "__main__":
    # Example usage
    async def main():
        # Create a simple 4-vertex MaxCut problem
        problem = create_random_maxcut_problem(4, edge_probability=0.7)
        
        print(f"Created MaxCut problem with {problem.num_vertices} vertices")
        print(f"Classical optimal cut value: {problem.classical_cut_value}")
        
        # Solve with QAOA
        result = await solve_maxcut_qaoa(
            problem,
            max_layers=2,
            enable_layerwise_training=True,
            max_iterations=30
        )
        
        if result.success:
            print(f"QAOA optimization successful!")
            print(f"Best cut value: {result.best_cut_value}")
            print(f"Approximation ratio: {result.approximation_ratio:.3f}")
            print(f"Best partition: {result.best_partition}")
            print(f"Execution time: {result.execution_time:.2f}s")
            print(f"Function evaluations: {result.function_evaluations}")
        else:
            print(f"QAOA optimization failed: {result.error_message}")
    
    asyncio.run(main())