"""Quantum Algorithm Runner

Unified interface for running quantum algorithms in the NQBA stack.
Integrates QAOA, VQE, and other quantum algorithms with the existing demo pipeline.
"""

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union, Callable
from enum import Enum
import json
from pathlib import Path

# Import quantum algorithms
from .qaoa_maxcut import (
    QAOAMaxCut, MaxCutProblem, QAOAResult,
    create_random_maxcut_problem, solve_maxcut_qaoa
)
from .vqe_chemistry import (
    VQEChemistry, MolecularSystem, VQEResult, AnsatzType,
    create_h2_molecule, create_lih_molecule, solve_molecule_vqe
)
from .quantum_backend_adapter import (
    BackendType, GradientMethod, backend_manager
)

# Import existing NQBA components
try:
    from ..quantum_adapter import QuantumAdapter
    NQBA_QUANTUM_AVAILABLE = True
except ImportError:
    NQBA_QUANTUM_AVAILABLE = False
    logging.warning("NQBA quantum adapter not available")

try:
    from ...monitoring import PerformanceMonitor
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False
    logging.warning("Performance monitoring not available")

logger = logging.getLogger(__name__)

class AlgorithmType(Enum):
    """Available quantum algorithm types"""
    QAOA_MAXCUT = "qaoa_maxcut"
    VQE_CHEMISTRY = "vqe_chemistry"
    QUANTUM_CLASSIFIER = "quantum_classifier"
    CUSTOM = "custom"

@dataclass
class AlgorithmConfig:
    """Configuration for quantum algorithm execution"""
    algorithm_type: AlgorithmType
    backend_type: Optional[BackendType] = None
    shots: int = 1024
    max_iterations: int = 100
    gradient_method: GradientMethod = GradientMethod.PARAMETER_SHIFT
    optimizer: str = "L-BFGS-B"
    
    # Algorithm-specific parameters
    algorithm_params: Dict[str, Any] = field(default_factory=dict)
    
    # Performance and monitoring
    enable_monitoring: bool = True
    save_results: bool = True
    benchmark_mode: bool = False

@dataclass
class AlgorithmResult:
    """Unified result from quantum algorithm execution"""
    success: bool
    algorithm_type: str
    execution_time: float
    result_data: Dict[str, Any]
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

class QuantumAlgorithmRunner:
    """Unified runner for quantum algorithms"""
    
    def __init__(self, enable_monitoring: bool = True):
        self.enable_monitoring = enable_monitoring
        self.performance_monitor = None
        
        if MONITORING_AVAILABLE and enable_monitoring:
            try:
                self.performance_monitor = PerformanceMonitor()
            except Exception as e:
                logger.warning(f"Could not initialize performance monitor: {e}")
        
        # Initialize backend manager
        self._ensure_backends_available()
        
        logger.info("Quantum Algorithm Runner initialized")
    
    def _ensure_backends_available(self) -> None:
        """Ensure quantum backends are available"""
        available_backends = backend_manager.get_available_backends()
        if not available_backends:
            logger.warning("No quantum backends available, algorithms may fail")
        else:
            logger.info(f"Available backends: {[b.value for b in available_backends]}")
    
    async def run_algorithm(self, 
                          config: AlgorithmConfig,
                          problem_data: Dict[str, Any]) -> AlgorithmResult:
        """Run a quantum algorithm with the given configuration"""
        start_time = time.time()
        
        try:
            # Start performance monitoring
            if self.performance_monitor:
                await self._start_monitoring(config, problem_data)
            
            # Route to appropriate algorithm
            if config.algorithm_type == AlgorithmType.QAOA_MAXCUT:
                result = await self._run_qaoa_maxcut(config, problem_data)
            elif config.algorithm_type == AlgorithmType.VQE_CHEMISTRY:
                result = await self._run_vqe_chemistry(config, problem_data)
            elif config.algorithm_type == AlgorithmType.QUANTUM_CLASSIFIER:
                result = await self._run_quantum_classifier(config, problem_data)
            else:
                raise ValueError(f"Unsupported algorithm type: {config.algorithm_type}")
            
            execution_time = time.time() - start_time
            
            # Create unified result
            algorithm_result = AlgorithmResult(
                success=result.get("success", False),
                algorithm_type=config.algorithm_type.value,
                execution_time=execution_time,
                result_data=result,
                metadata={
                    "config": config.__dict__,
                    "problem_data_summary": self._summarize_problem_data(problem_data)
                }
            )
            
            # Add performance metrics
            if self.performance_monitor:
                algorithm_result.performance_metrics = await self._get_performance_metrics()
            
            # Save results if requested
            if config.save_results:
                await self._save_results(algorithm_result)
            
            return algorithm_result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Algorithm execution failed: {e}")
            
            return AlgorithmResult(
                success=False,
                algorithm_type=config.algorithm_type.value,
                execution_time=execution_time,
                result_data={},
                error_message=str(e)
            )
        
        finally:
            # Stop performance monitoring
            if self.performance_monitor:
                await self._stop_monitoring()
    
    async def _run_qaoa_maxcut(self, 
                             config: AlgorithmConfig, 
                             problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run QAOA MaxCut algorithm"""
        logger.info("Running QAOA MaxCut algorithm")
        
        # Extract problem parameters
        if "adjacency_matrix" in problem_data:
            import numpy as np
            adj_matrix = np.array(problem_data["adjacency_matrix"])
            problem = MaxCutProblem.from_adjacency_matrix(adj_matrix)
        elif "num_vertices" in problem_data:
            num_vertices = problem_data["num_vertices"]
            edge_prob = problem_data.get("edge_probability", 0.5)
            seed = problem_data.get("seed", 42)
            problem = create_random_maxcut_problem(num_vertices, edge_prob, seed)
        else:
            # Default small problem
            problem = create_random_maxcut_problem(4, 0.7, 42)
        
        # Extract algorithm parameters
        max_layers = config.algorithm_params.get("max_layers", 3)
        enable_warm_start = config.algorithm_params.get("enable_warm_start", True)
        enable_layerwise = config.algorithm_params.get("enable_layerwise_training", True)
        
        # Run QAOA
        result = await solve_maxcut_qaoa(
            problem=problem,
            max_layers=max_layers,
            backend_type=config.backend_type,
            shots=config.shots,
            enable_warm_start=enable_warm_start,
            enable_layerwise_training=enable_layerwise,
            gradient_method=config.gradient_method,
            optimizer=config.optimizer,
            max_iterations=config.max_iterations
        )
        
        # Convert to dictionary format
        return {
            "success": result.success,
            "optimal_params": result.optimal_params.tolist() if result.optimal_params is not None else None,
            "optimal_value": result.optimal_value,
            "best_cut_value": result.best_cut_value,
            "best_partition": result.best_partition,
            "approximation_ratio": result.approximation_ratio,
            "iterations": result.iterations,
            "function_evaluations": result.function_evaluations,
            "convergence_data": result.convergence_data,
            "backend_used": result.backend_used,
            "error_message": result.error_message,
            "classical_cut_value": problem.classical_cut_value,
            "num_vertices": problem.num_vertices
        }
    
    async def _run_vqe_chemistry(self, 
                               config: AlgorithmConfig, 
                               problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run VQE chemistry algorithm"""
        logger.info("Running VQE chemistry algorithm")
        
        # Extract molecular system
        if "molecule_name" in problem_data:
            molecule_name = problem_data["molecule_name"]
            bond_length = problem_data.get("bond_length", None)
            
            if molecule_name.upper() == "H2":
                molecule = create_h2_molecule(bond_length or 0.74)
            elif molecule_name.upper() == "LIH":
                molecule = create_lih_molecule(bond_length or 1.45)
            else:
                # Default to H2
                molecule = create_h2_molecule(0.74)
        elif "geometry" in problem_data:
            # Custom molecule from geometry
            molecule = MolecularSystem(
                name=problem_data.get("name", "custom"),
                geometry=problem_data["geometry"],
                charge=problem_data.get("charge", 0),
                spin=problem_data.get("spin", 0),
                basis=problem_data.get("basis", "sto-3g")
            )
        else:
            # Default H2 molecule
            molecule = create_h2_molecule(0.74)
        
        # Extract algorithm parameters
        ansatz_type_str = config.algorithm_params.get("ansatz_type", "hardware_efficient")
        ansatz_type = AnsatzType(ansatz_type_str)
        num_layers = config.algorithm_params.get("num_layers", 2)
        enable_adaptive = config.algorithm_params.get("enable_adaptive", False)
        
        # Run VQE
        result = await solve_molecule_vqe(
            molecular_system=molecule,
            ansatz_type=ansatz_type,
            num_layers=num_layers,
            backend_type=config.backend_type,
            shots=config.shots,
            enable_adaptive=enable_adaptive,
            gradient_method=config.gradient_method,
            optimizer=config.optimizer,
            max_iterations=config.max_iterations
        )
        
        # Convert to dictionary format
        return {
            "success": result.success,
            "optimal_params": result.optimal_params.tolist() if result.optimal_params is not None else None,
            "optimal_energy": result.optimal_energy,
            "ground_state_energy": result.ground_state_energy,
            "chemical_accuracy": result.chemical_accuracy,
            "iterations": result.iterations,
            "function_evaluations": result.function_evaluations,
            "convergence_data": result.convergence_data,
            "ansatz_type": result.ansatz_type,
            "num_parameters": result.num_parameters,
            "backend_used": result.backend_used,
            "error_message": result.error_message,
            "molecule_name": molecule.name,
            "hf_energy": molecule.hf_energy,
            "fci_energy": molecule.fci_energy
        }
    
    async def _run_quantum_classifier(self, 
                                    config: AlgorithmConfig, 
                                    problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run quantum classifier algorithm"""
        logger.info("Running quantum classifier algorithm")
        
        try:
            from .quantum_classifier import (
                QuantumClassifier, FeatureMappingType, AnsatzType,
                create_quantum_classifier, run_classification_demo
            )
            
            # Extract dataset parameters
            dataset_name = problem_data.get("dataset_name", "iris")
            num_samples = problem_data.get("num_samples", 100)
            test_size = problem_data.get("test_size", 0.3)
            random_state = problem_data.get("random_state", 42)
            
            # Extract algorithm parameters
            feature_map = config.algorithm_params.get("feature_map", "ZZFeatureMap")
            ansatz = config.algorithm_params.get("ansatz", "RealAmplitudes")
            num_layers = config.algorithm_params.get("num_layers", 2)
            
            # Convert string parameters to enums
            try:
                feature_map_type = FeatureMappingType(feature_map)
            except ValueError:
                feature_map_type = FeatureMappingType.ZZ_FEATURE_MAP
                
            try:
                ansatz_type = AnsatzType(ansatz)
            except ValueError:
                ansatz_type = AnsatzType.REAL_AMPLITUDES
            
            # Run quantum classifier demo
            result = await asyncio.to_thread(
                run_classification_demo,
                dataset_name=dataset_name,
                num_samples=num_samples,
                test_size=test_size,
                random_state=random_state,
                feature_map=feature_map_type,
                ansatz=ansatz_type,
                num_layers=num_layers,
                backend_type=config.backend_type.value if config.backend_type else "simulator",
                shots=config.shots,
                max_iterations=config.max_iterations
            )
            
            return {
                "success": result.success,
                "train_accuracy": result.train_accuracy,
                "test_accuracy": result.test_accuracy,
                "optimal_params": result.optimal_params.tolist() if result.optimal_params is not None else None,
                "iterations": result.iterations,
                "function_evaluations": result.function_evaluations,
                "feature_map_type": result.feature_map_type,
                "ansatz_type": result.ansatz_type,
                "num_qubits": result.num_qubits,
                "num_parameters": result.num_parameters,
                "backend_used": result.backend_used,
                "execution_time": result.execution_time,
                "convergence_data": result.convergence_data,
                "error_message": result.error_message,
                "dataset_info": {
                    "name": dataset_name,
                    "num_samples": num_samples,
                    "num_features": result.num_features if hasattr(result, 'num_features') else None,
                    "num_classes": result.num_classes if hasattr(result, 'num_classes') else None
                }
            }
            
        except ImportError as e:
            logger.error(f"Quantum classifier not available: {e}")
            return {
                "success": False,
                "error_message": f"Quantum classifier not available: {e}"
            }
        except Exception as e:
            logger.error(f"Quantum classifier execution failed: {e}")
            return {
                "success": False,
                "error_message": str(e)
            }
    

    
    def _summarize_problem_data(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of problem data for metadata"""
        summary = {}
        
        # Extract key information without storing large arrays
        for key, value in problem_data.items():
            if isinstance(value, (list, tuple)) and len(value) > 10:
                summary[key] = f"<{type(value).__name__} of length {len(value)}>"
            elif isinstance(value, dict) and len(value) > 5:
                summary[key] = f"<dict with {len(value)} keys>"
            elif hasattr(value, 'shape'):  # numpy arrays
                summary[key] = f"<array with shape {value.shape}>"
            else:
                summary[key] = value
        
        return summary
    
    async def _start_monitoring(self, config: AlgorithmConfig, problem_data: Dict[str, Any]) -> None:
        """Start performance monitoring"""
        if self.performance_monitor:
            try:
                await self.performance_monitor.start_monitoring(
                    task_name=f"quantum_algorithm_{config.algorithm_type.value}",
                    metadata={
                        "algorithm_type": config.algorithm_type.value,
                        "backend_type": config.backend_type.value if config.backend_type else None,
                        "shots": config.shots
                    }
                )
            except Exception as e:
                logger.warning(f"Could not start monitoring: {e}")
    
    async def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics from monitor"""
        if self.performance_monitor:
            try:
                return await self.performance_monitor.get_current_metrics()
            except Exception as e:
                logger.warning(f"Could not get performance metrics: {e}")
        return {}
    
    async def _stop_monitoring(self) -> None:
        """Stop performance monitoring"""
        if self.performance_monitor:
            try:
                await self.performance_monitor.stop_monitoring()
            except Exception as e:
                logger.warning(f"Could not stop monitoring: {e}")
    
    async def _save_results(self, result: AlgorithmResult) -> None:
        """Save algorithm results to file"""
        try:
            results_dir = Path("algorithm_results")
            results_dir.mkdir(exist_ok=True)
            
            timestamp = int(time.time())
            filename = f"{result.algorithm_type}_{timestamp}.json"
            filepath = results_dir / filename
            
            # Convert result to JSON-serializable format
            result_dict = {
                "success": result.success,
                "algorithm_type": result.algorithm_type,
                "execution_time": result.execution_time,
                "result_data": result.result_data,
                "performance_metrics": result.performance_metrics,
                "error_message": result.error_message,
                "metadata": result.metadata,
                "timestamp": timestamp
            }
            
            with open(filepath, 'w') as f:
                json.dump(result_dict, f, indent=2, default=str)
            
            logger.info(f"Results saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Could not save results: {e}")

# Convenience functions for integration with existing demos
async def run_algorithm(algorithm_type: str,
                      problem_data: Dict[str, Any],
                      backend_type: Optional[str] = None,
                      **kwargs) -> Dict[str, Any]:
    """Convenience function to run quantum algorithms"""
    
    # Convert string types to enums
    try:
        algo_type = AlgorithmType(algorithm_type)
    except ValueError:
        raise ValueError(f"Unsupported algorithm type: {algorithm_type}")
    
    backend_enum = None
    if backend_type:
        try:
            backend_enum = BackendType(backend_type)
        except ValueError:
            logger.warning(f"Unknown backend type: {backend_type}, using default")
    
    # Create configuration
    config = AlgorithmConfig(
        algorithm_type=algo_type,
        backend_type=backend_enum,
        **kwargs
    )
    
    # Run algorithm
    runner = QuantumAlgorithmRunner()
    result = await runner.run_algorithm(config, problem_data)
    
    return {
        "success": result.success,
        "execution_time": result.execution_time,
        "result_data": result.result_data,
        "error_message": result.error_message
    }

# Integration functions for existing demo scripts
def integrate_with_demo_nqba(demo_data: Dict[str, Any]) -> Dict[str, Any]:
    """Integration point for demo_integrated_nqba.py"""
    
    async def run_quantum_optimization():
        """Run quantum optimization on demo data"""
        
        # Extract optimization problem from demo data
        if "optimization_problem" in demo_data:
            problem_type = demo_data["optimization_problem"].get("type", "maxcut")
            
            if problem_type == "maxcut":
                # Run QAOA MaxCut
                problem_data = {
                    "num_vertices": demo_data["optimization_problem"].get("num_vertices", 6),
                    "edge_probability": demo_data["optimization_problem"].get("edge_probability", 0.6)
                }
                
                result = await run_algorithm(
                    algorithm_type="qaoa_maxcut",
                    problem_data=problem_data,
                    max_iterations=50,
                    algorithm_params={"max_layers": 2}
                )
                
                return {
                    "quantum_optimization_result": result,
                    "algorithm_used": "QAOA MaxCut",
                    "problem_size": problem_data["num_vertices"]
                }
        
        # Default: run small chemistry problem
        problem_data = {"molecule_name": "H2", "bond_length": 0.74}
        
        result = await run_algorithm(
            algorithm_type="vqe_chemistry",
            problem_data=problem_data,
            max_iterations=30,
            algorithm_params={"ansatz_type": "hardware_efficient", "num_layers": 2}
        )
        
        return {
            "quantum_chemistry_result": result,
            "algorithm_used": "VQE",
            "molecule": "H2"
        }
    
    # Run the quantum algorithm
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If we're already in an async context, create a task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, run_quantum_optimization())
                return future.result()
        else:
            return asyncio.run(run_quantum_optimization())
    except Exception as e:
        logger.error(f"Quantum algorithm integration failed: {e}")
        return {
            "quantum_optimization_result": {"success": False, "error": str(e)},
            "algorithm_used": "None",
            "error": str(e)
        }

def integrate_with_flyfox_demo(pod_data: Dict[str, Any]) -> Dict[str, Any]:
    """Integration point for flyfox_platform_demo.py"""
    
    async def run_pod_optimization():
        """Run quantum optimization for pod data"""
        
        # Extract relevant data from pods
        if "business_pods" in pod_data:
            pods = pod_data["business_pods"]
            
            # Create optimization problem from pod connections
            num_pods = len(pods)
            if num_pods > 1:
                # Create MaxCut problem from pod relationships
                problem_data = {
                    "num_vertices": min(num_pods, 8),  # Limit size for demo
                    "edge_probability": 0.7,
                    "seed": hash(str(pods)) % 1000  # Deterministic but varied
                }
                
                result = await run_algorithm(
                    algorithm_type="qaoa_maxcut",
                    problem_data=problem_data,
                    max_iterations=30,
                    algorithm_params={"max_layers": 2, "enable_layerwise_training": True}
                )
                
                return {
                    "pod_optimization_result": result,
                    "algorithm_used": "QAOA for Pod Clustering",
                    "num_pods_analyzed": num_pods
                }
        
        # Fallback: run quantum classifier on pod features
        problem_data = {
            "num_features": 4,
            "num_classes": 2,
            "dataset_size": pod_data.get("total_pods", 10)
        }
        
        result = await run_algorithm(
            algorithm_type="quantum_classifier",
            problem_data=problem_data
        )
        
        return {
            "pod_classification_result": result,
            "algorithm_used": "Quantum Classifier",
            "features_analyzed": problem_data["num_features"]
        }
    
    # Run the quantum algorithm
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, run_pod_optimization())
                return future.result()
        else:
            return asyncio.run(run_pod_optimization())
    except Exception as e:
        logger.error(f"Pod optimization integration failed: {e}")
        return {
            "pod_optimization_result": {"success": False, "error": str(e)},
            "algorithm_used": "None",
            "error": str(e)
        }

# Example usage and testing
if __name__ == "__main__":
    async def test_runner():
        """Test the quantum algorithm runner"""
        runner = QuantumAlgorithmRunner()
        
        # Test QAOA MaxCut
        print("Testing QAOA MaxCut...")
        qaoa_config = AlgorithmConfig(
            algorithm_type=AlgorithmType.QAOA_MAXCUT,
            max_iterations=20,
            algorithm_params={"max_layers": 2}
        )
        qaoa_problem = {"num_vertices": 4, "edge_probability": 0.7}
        
        qaoa_result = await runner.run_algorithm(qaoa_config, qaoa_problem)
        print(f"QAOA Result: {qaoa_result.success}, Time: {qaoa_result.execution_time:.2f}s")
        
        # Test VQE Chemistry
        print("\nTesting VQE Chemistry...")
        vqe_config = AlgorithmConfig(
            algorithm_type=AlgorithmType.VQE_CHEMISTRY,
            max_iterations=20,
            algorithm_params={"ansatz_type": "hardware_efficient", "num_layers": 2}
        )
        vqe_problem = {"molecule_name": "H2", "bond_length": 0.74}
        
        vqe_result = await runner.run_algorithm(vqe_config, vqe_problem)
        print(f"VQE Result: {vqe_result.success}, Time: {vqe_result.execution_time:.2f}s")
        
        # Test integration functions
        print("\nTesting demo integration...")
        demo_data = {
            "optimization_problem": {
                "type": "maxcut",
                "num_vertices": 5
            }
        }
        
        integration_result = integrate_with_demo_nqba(demo_data)
        print(f"Demo integration: {integration_result.get('algorithm_used', 'Failed')}")
    
    asyncio.run(test_runner())