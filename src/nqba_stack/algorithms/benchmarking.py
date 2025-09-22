"""Quantum Algorithm Benchmarking Harness

Comprehensive benchmarking system for quantum algorithms with performance tracking,
comparison metrics, and automated reporting.
"""

import asyncio
import time
import json
import logging
import statistics
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Callable, Union
from enum import Enum
from pathlib import Path
import numpy as np
from datetime import datetime
import psutil
import tracemalloc

# Import quantum algorithms
from .qaoa_maxcut import (
    QAOAMaxCut, MaxCutProblem, QAOAResult,
    create_random_maxcut_problem, solve_maxcut_qaoa
)
from .vqe_chemistry import (
    VQEChemistry, MolecularSystem, VQEResult, AnsatzType,
    create_h2_molecule, create_lih_molecule, solve_molecule_vqe
)
from .quantum_backend_adapter import BackendType, GradientMethod
from .runner import (
    QuantumAlgorithmRunner, AlgorithmConfig, AlgorithmType, AlgorithmResult
)

logger = logging.getLogger(__name__)

class BenchmarkMetric(Enum):
    """Available benchmark metrics"""
    EXECUTION_TIME = "execution_time"
    WALL_CLOCK_TIME = "wall_clock_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    FUNCTION_EVALUATIONS = "function_evaluations"
    ITERATIONS = "iterations"
    CONVERGENCE_RATE = "convergence_rate"
    SUCCESS_RATE = "success_rate"
    APPROXIMATION_RATIO = "approximation_ratio"
    ENERGY_ERROR = "energy_error"
    SHOT_EFFICIENCY = "shot_efficiency"
    QUANTUM_COST = "quantum_cost"
    CLASSICAL_PREPROCESSING_TIME = "classical_preprocessing_time"
    GRADIENT_ESTIMATION_TIME = "gradient_estimation_time"

@dataclass
class BenchmarkConfig:
    """Configuration for benchmarking runs"""
    name: str
    description: str = ""
    num_runs: int = 5
    warmup_runs: int = 1
    timeout_seconds: float = 300.0
    
    # Metrics to collect
    metrics: List[BenchmarkMetric] = field(default_factory=lambda: [
        BenchmarkMetric.EXECUTION_TIME,
        BenchmarkMetric.MEMORY_USAGE,
        BenchmarkMetric.FUNCTION_EVALUATIONS,
        BenchmarkMetric.SUCCESS_RATE
    ])
    
    # Problem scaling parameters
    problem_sizes: List[int] = field(default_factory=lambda: [4, 6, 8])
    
    # Algorithm parameters to vary
    parameter_sweep: Dict[str, List[Any]] = field(default_factory=dict)
    
    # Output configuration
    save_individual_runs: bool = True
    save_summary: bool = True
    output_directory: str = "benchmark_results"
    
    # Comparison baselines
    include_classical_baseline: bool = True
    include_random_baseline: bool = True

@dataclass
class BenchmarkRun:
    """Results from a single benchmark run"""
    run_id: str
    algorithm_type: str
    problem_size: int
    parameters: Dict[str, Any]
    
    # Timing metrics
    start_time: float
    end_time: float
    execution_time: float
    wall_clock_time: float
    
    # Resource metrics
    peak_memory_mb: float
    avg_cpu_percent: float
    
    # Algorithm metrics
    success: bool
    iterations: int
    function_evaluations: int
    convergence_data: List[float] = field(default_factory=list)
    
    # Quality metrics
    objective_value: Optional[float] = None
    approximation_ratio: Optional[float] = None
    energy_error: Optional[float] = None
    
    # Backend metrics
    backend_used: str = ""
    shots_used: int = 0
    quantum_cost: float = 0.0
    
    # Error information
    error_message: Optional[str] = None
    
    # Additional metadata
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class BenchmarkSummary:
    """Summary statistics from multiple benchmark runs"""
    benchmark_name: str
    algorithm_type: str
    total_runs: int
    successful_runs: int
    
    # Timing statistics
    mean_execution_time: float
    std_execution_time: float
    min_execution_time: float
    max_execution_time: float
    
    # Quality statistics
    mean_objective_value: Optional[float] = None
    std_objective_value: Optional[float] = None
    best_objective_value: Optional[float] = None
    worst_objective_value: Optional[float] = None
    
    # Efficiency statistics
    mean_function_evaluations: float = 0.0
    mean_iterations: float = 0.0
    success_rate: float = 0.0
    
    # Resource statistics
    mean_memory_usage: float = 0.0
    mean_cpu_usage: float = 0.0
    
    # Scaling analysis
    scaling_coefficient: Optional[float] = None
    scaling_r_squared: Optional[float] = None
    
    # Comparison with baselines
    classical_speedup: Optional[float] = None
    quantum_advantage: Optional[float] = None
    
    # Raw data
    individual_runs: List[BenchmarkRun] = field(default_factory=list)
    
    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    environment_info: Dict[str, Any] = field(default_factory=dict)

class QuantumBenchmarkHarness:
    """Comprehensive benchmarking harness for quantum algorithms"""
    
    def __init__(self, output_dir: str = "benchmark_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.runner = QuantumAlgorithmRunner(enable_monitoring=False)
        self.current_benchmark = None
        
        # Performance monitoring
        self.memory_samples = []
        self.cpu_samples = []
        self.monitoring_active = False
        
        logger.info(f"Benchmark harness initialized, output: {self.output_dir}")
    
    async def run_benchmark(self, 
                          config: BenchmarkConfig,
                          algorithm_configs: List[AlgorithmConfig],
                          problem_generator: Callable[[int], Dict[str, Any]]) -> List[BenchmarkSummary]:
        """Run comprehensive benchmark across multiple algorithms and problem sizes"""
        
        logger.info(f"Starting benchmark: {config.name}")
        self.current_benchmark = config
        
        summaries = []
        
        for algo_config in algorithm_configs:
            logger.info(f"Benchmarking {algo_config.algorithm_type.value}")
            
            summary = await self._benchmark_algorithm(
                config, algo_config, problem_generator
            )
            summaries.append(summary)
            
            # Save individual algorithm summary
            if config.save_summary:
                await self._save_summary(summary, config)
        
        # Generate comparison report
        if len(summaries) > 1:
            await self._generate_comparison_report(summaries, config)
        
        logger.info(f"Benchmark completed: {config.name}")
        return summaries
    
    async def _benchmark_algorithm(self,
                                 benchmark_config: BenchmarkConfig,
                                 algorithm_config: AlgorithmConfig,
                                 problem_generator: Callable[[int], Dict[str, Any]]) -> BenchmarkSummary:
        """Benchmark a single algorithm across problem sizes"""
        
        all_runs = []
        
        for problem_size in benchmark_config.problem_sizes:
            logger.info(f"Testing problem size: {problem_size}")
            
            # Generate problem
            problem_data = problem_generator(problem_size)
            
            # Run multiple trials
            for run_idx in range(benchmark_config.num_runs + benchmark_config.warmup_runs):
                is_warmup = run_idx < benchmark_config.warmup_runs
                
                if is_warmup:
                    logger.debug(f"Warmup run {run_idx + 1}/{benchmark_config.warmup_runs}")
                else:
                    logger.debug(f"Run {run_idx - benchmark_config.warmup_runs + 1}/{benchmark_config.num_runs}")
                
                run_result = await self._run_single_benchmark(
                    benchmark_config,
                    algorithm_config,
                    problem_data,
                    problem_size,
                    run_idx,
                    is_warmup
                )
                
                if not is_warmup:
                    all_runs.append(run_result)
                    
                    # Save individual run if requested
                    if benchmark_config.save_individual_runs:
                        await self._save_run(run_result, benchmark_config)
        
        # Generate summary statistics
        summary = self._generate_summary(
            benchmark_config.name,
            algorithm_config.algorithm_type.value,
            all_runs
        )
        
        return summary
    
    async def _run_single_benchmark(self,
                                  benchmark_config: BenchmarkConfig,
                                  algorithm_config: AlgorithmConfig,
                                  problem_data: Dict[str, Any],
                                  problem_size: int,
                                  run_idx: int,
                                  is_warmup: bool) -> BenchmarkRun:
        """Run a single benchmark trial"""
        
        run_id = f"{algorithm_config.algorithm_type.value}_{problem_size}_{run_idx}"
        
        # Start monitoring
        await self._start_monitoring()
        
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        try:
            # Start memory tracking
            tracemalloc.start()
            
            # Run algorithm with timeout
            result = await asyncio.wait_for(
                self.runner.run_algorithm(algorithm_config, problem_data),
                timeout=benchmark_config.timeout_seconds
            )
            
            end_time = time.time()
            
            # Get memory statistics
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            # Stop monitoring
            await self._stop_monitoring()
            
            # Create benchmark run result
            run_result = BenchmarkRun(
                run_id=run_id,
                algorithm_type=algorithm_config.algorithm_type.value,
                problem_size=problem_size,
                parameters=algorithm_config.algorithm_params,
                start_time=start_time,
                end_time=end_time,
                execution_time=result.execution_time,
                wall_clock_time=end_time - start_time,
                peak_memory_mb=peak / 1024 / 1024,
                avg_cpu_percent=statistics.mean(self.cpu_samples) if self.cpu_samples else 0.0,
                success=result.success,
                iterations=result.result_data.get('iterations', 0),
                function_evaluations=result.result_data.get('function_evaluations', 0),
                convergence_data=result.result_data.get('convergence_data', []),
                objective_value=self._extract_objective_value(result),
                approximation_ratio=result.result_data.get('approximation_ratio'),
                energy_error=self._calculate_energy_error(result),
                backend_used=result.result_data.get('backend_used', ''),
                shots_used=algorithm_config.shots,
                quantum_cost=self._calculate_quantum_cost(result, algorithm_config),
                error_message=result.error_message,
                metadata={
                    'algorithm_config': asdict(algorithm_config),
                    'problem_data_summary': self._summarize_problem_data(problem_data),
                    'is_warmup': is_warmup
                }
            )
            
            return run_result
            
        except asyncio.TimeoutError:
            end_time = time.time()
            tracemalloc.stop()
            await self._stop_monitoring()
            
            logger.warning(f"Benchmark run {run_id} timed out")
            
            return BenchmarkRun(
                run_id=run_id,
                algorithm_type=algorithm_config.algorithm_type.value,
                problem_size=problem_size,
                parameters=algorithm_config.algorithm_params,
                start_time=start_time,
                end_time=end_time,
                execution_time=end_time - start_time,
                wall_clock_time=end_time - start_time,
                peak_memory_mb=0.0,
                avg_cpu_percent=0.0,
                success=False,
                iterations=0,
                function_evaluations=0,
                error_message="Timeout"
            )
            
        except Exception as e:
            end_time = time.time()
            tracemalloc.stop()
            await self._stop_monitoring()
            
            logger.error(f"Benchmark run {run_id} failed: {e}")
            
            return BenchmarkRun(
                run_id=run_id,
                algorithm_type=algorithm_config.algorithm_type.value,
                problem_size=problem_size,
                parameters=algorithm_config.algorithm_params,
                start_time=start_time,
                end_time=end_time,
                execution_time=end_time - start_time,
                wall_clock_time=end_time - start_time,
                peak_memory_mb=0.0,
                avg_cpu_percent=0.0,
                success=False,
                iterations=0,
                function_evaluations=0,
                error_message=str(e)
            )
    
    async def _start_monitoring(self):
        """Start system resource monitoring"""
        self.monitoring_active = True
        self.memory_samples = []
        self.cpu_samples = []
        
        # Start background monitoring task
        asyncio.create_task(self._monitor_resources())
    
    async def _stop_monitoring(self):
        """Stop system resource monitoring"""
        self.monitoring_active = False
    
    async def _monitor_resources(self):
        """Background task to monitor system resources"""
        while self.monitoring_active:
            try:
                # Sample memory and CPU usage
                memory_mb = self._get_memory_usage()
                cpu_percent = psutil.cpu_percent(interval=None)
                
                self.memory_samples.append(memory_mb)
                self.cpu_samples.append(cpu_percent)
                
                await asyncio.sleep(0.1)  # Sample every 100ms
                
            except Exception as e:
                logger.warning(f"Resource monitoring error: {e}")
                break
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024
        except Exception:
            return 0.0
    
    def _extract_objective_value(self, result: AlgorithmResult) -> Optional[float]:
        """Extract objective value from algorithm result"""
        if 'optimal_value' in result.result_data:
            return result.result_data['optimal_value']
        elif 'optimal_energy' in result.result_data:
            return result.result_data['optimal_energy']
        elif 'best_cut_value' in result.result_data:
            return result.result_data['best_cut_value']
        return None
    
    def _calculate_energy_error(self, result: AlgorithmResult) -> Optional[float]:
        """Calculate energy error for chemistry problems"""
        if 'optimal_energy' in result.result_data and 'fci_energy' in result.result_data:
            optimal = result.result_data['optimal_energy']
            fci = result.result_data['fci_energy']
            if optimal is not None and fci is not None:
                return abs(optimal - fci)
        return None
    
    def _calculate_quantum_cost(self, result: AlgorithmResult, config: AlgorithmConfig) -> float:
        """Calculate quantum cost (shots * circuit depth estimate)"""
        shots = config.shots
        iterations = result.result_data.get('iterations', 1)
        function_evals = result.result_data.get('function_evaluations', 1)
        
        # Rough estimate of quantum cost
        return shots * function_evals * 1.0  # Could be refined with actual circuit depth
    
    def _summarize_problem_data(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create summary of problem data"""
        summary = {}
        for key, value in problem_data.items():
            if isinstance(value, (list, tuple)) and len(value) > 10:
                summary[key] = f"<{type(value).__name__} of length {len(value)}>"
            elif isinstance(value, dict) and len(value) > 5:
                summary[key] = f"<dict with {len(value)} keys>"
            elif hasattr(value, 'shape'):
                summary[key] = f"<array with shape {value.shape}>"
            else:
                summary[key] = value
        return summary
    
    def _generate_summary(self, 
                         benchmark_name: str,
                         algorithm_type: str,
                         runs: List[BenchmarkRun]) -> BenchmarkSummary:
        """Generate summary statistics from benchmark runs"""
        
        if not runs:
            return BenchmarkSummary(
                benchmark_name=benchmark_name,
                algorithm_type=algorithm_type,
                total_runs=0,
                successful_runs=0,
                mean_execution_time=0.0,
                std_execution_time=0.0,
                min_execution_time=0.0,
                max_execution_time=0.0
            )
        
        successful_runs = [r for r in runs if r.success]
        
        # Timing statistics
        execution_times = [r.execution_time for r in runs]
        
        # Quality statistics
        objective_values = [r.objective_value for r in successful_runs if r.objective_value is not None]
        
        # Efficiency statistics
        function_evals = [r.function_evaluations for r in runs]
        iterations = [r.iterations for r in runs]
        
        # Resource statistics
        memory_usage = [r.peak_memory_mb for r in runs]
        cpu_usage = [r.avg_cpu_percent for r in runs]
        
        # Calculate scaling if multiple problem sizes
        scaling_coeff, scaling_r2 = self._analyze_scaling(runs)
        
        summary = BenchmarkSummary(
            benchmark_name=benchmark_name,
            algorithm_type=algorithm_type,
            total_runs=len(runs),
            successful_runs=len(successful_runs),
            mean_execution_time=statistics.mean(execution_times),
            std_execution_time=statistics.stdev(execution_times) if len(execution_times) > 1 else 0.0,
            min_execution_time=min(execution_times),
            max_execution_time=max(execution_times),
            mean_objective_value=statistics.mean(objective_values) if objective_values else None,
            std_objective_value=statistics.stdev(objective_values) if len(objective_values) > 1 else None,
            best_objective_value=max(objective_values) if objective_values else None,
            worst_objective_value=min(objective_values) if objective_values else None,
            mean_function_evaluations=statistics.mean(function_evals) if function_evals else 0.0,
            mean_iterations=statistics.mean(iterations) if iterations else 0.0,
            success_rate=len(successful_runs) / len(runs),
            mean_memory_usage=statistics.mean(memory_usage) if memory_usage else 0.0,
            mean_cpu_usage=statistics.mean(cpu_usage) if cpu_usage else 0.0,
            scaling_coefficient=scaling_coeff,
            scaling_r_squared=scaling_r2,
            individual_runs=runs,
            environment_info=self._get_environment_info()
        )
        
        return summary
    
    def _analyze_scaling(self, runs: List[BenchmarkRun]) -> tuple[Optional[float], Optional[float]]:
        """Analyze scaling behavior across problem sizes"""
        try:
            # Group runs by problem size
            size_times = {}
            for run in runs:
                if run.success:
                    size = run.problem_size
                    if size not in size_times:
                        size_times[size] = []
                    size_times[size].append(run.execution_time)
            
            if len(size_times) < 2:
                return None, None
            
            # Calculate mean time for each size
            sizes = []
            times = []
            for size, time_list in size_times.items():
                sizes.append(size)
                times.append(statistics.mean(time_list))
            
            # Fit polynomial (log-log for scaling analysis)
            log_sizes = np.log(sizes)
            log_times = np.log(times)
            
            # Linear regression in log space
            coeffs = np.polyfit(log_sizes, log_times, 1)
            scaling_coeff = coeffs[0]  # This is the scaling exponent
            
            # Calculate R-squared
            predicted = np.polyval(coeffs, log_sizes)
            ss_res = np.sum((log_times - predicted) ** 2)
            ss_tot = np.sum((log_times - np.mean(log_times)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
            
            return scaling_coeff, r_squared
            
        except Exception as e:
            logger.warning(f"Scaling analysis failed: {e}")
            return None, None
    
    def _get_environment_info(self) -> Dict[str, Any]:
        """Get environment information for reproducibility"""
        try:
            import platform
            return {
                'platform': platform.platform(),
                'python_version': platform.python_version(),
                'cpu_count': psutil.cpu_count(),
                'memory_gb': psutil.virtual_memory().total / 1024**3,
                'timestamp': datetime.now().isoformat()
            }
        except Exception:
            return {'timestamp': datetime.now().isoformat()}
    
    async def _save_run(self, run: BenchmarkRun, config: BenchmarkConfig):
        """Save individual benchmark run"""
        try:
            run_dir = self.output_dir / config.name / "individual_runs"
            run_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{run.run_id}.json"
            filepath = run_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(asdict(run), f, indent=2, default=str)
                
        except Exception as e:
            logger.error(f"Failed to save run {run.run_id}: {e}")
    
    async def _save_summary(self, summary: BenchmarkSummary, config: BenchmarkConfig):
        """Save benchmark summary"""
        try:
            summary_dir = self.output_dir / config.name
            summary_dir.mkdir(parents=True, exist_ok=True)
            
            filename = f"{summary.algorithm_type}_summary.json"
            filepath = summary_dir / filename
            
            with open(filepath, 'w') as f:
                json.dump(asdict(summary), f, indent=2, default=str)
                
            logger.info(f"Summary saved: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save summary: {e}")
    
    async def _generate_comparison_report(self, summaries: List[BenchmarkSummary], config: BenchmarkConfig):
        """Generate comparison report across algorithms"""
        try:
            report_dir = self.output_dir / config.name
            report_dir.mkdir(parents=True, exist_ok=True)
            
            # Create comparison data
            comparison = {
                'benchmark_name': config.name,
                'timestamp': datetime.now().isoformat(),
                'algorithms': [],
                'comparison_metrics': {}
            }
            
            for summary in summaries:
                comparison['algorithms'].append({
                    'algorithm_type': summary.algorithm_type,
                    'success_rate': summary.success_rate,
                    'mean_execution_time': summary.mean_execution_time,
                    'mean_objective_value': summary.mean_objective_value,
                    'scaling_coefficient': summary.scaling_coefficient
                })
            
            # Calculate relative performance
            if len(summaries) > 1:
                baseline = summaries[0]
                for summary in summaries[1:]:
                    speedup = baseline.mean_execution_time / summary.mean_execution_time
                    comparison['comparison_metrics'][f"{summary.algorithm_type}_vs_{baseline.algorithm_type}_speedup"] = speedup
            
            # Save comparison report
            filepath = report_dir / "comparison_report.json"
            with open(filepath, 'w') as f:
                json.dump(comparison, f, indent=2, default=str)
            
            logger.info(f"Comparison report saved: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to generate comparison report: {e}")

# Convenience functions for common benchmarks
async def benchmark_qaoa_scaling(max_vertices: int = 10, 
                               num_runs: int = 5) -> BenchmarkSummary:
    """Benchmark QAOA scaling with problem size"""
    
    def problem_generator(size: int) -> Dict[str, Any]:
        return {
            "num_vertices": size,
            "edge_probability": 0.6,
            "seed": 42
        }
    
    config = BenchmarkConfig(
        name="qaoa_scaling",
        description="QAOA scaling with MaxCut problem size",
        num_runs=num_runs,
        problem_sizes=list(range(4, max_vertices + 1, 2))
    )
    
    algorithm_config = AlgorithmConfig(
        algorithm_type=AlgorithmType.QAOA_MAXCUT,
        max_iterations=50,
        algorithm_params={"max_layers": 3}
    )
    
    harness = QuantumBenchmarkHarness()
    summaries = await harness.run_benchmark(config, [algorithm_config], problem_generator)
    
    return summaries[0]

async def benchmark_vqe_molecules(molecules: List[str] = None,
                                num_runs: int = 3) -> List[BenchmarkSummary]:
    """Benchmark VQE on different molecules"""
    
    if molecules is None:
        molecules = ["H2", "LiH"]
    
    def problem_generator(molecule_idx: int) -> Dict[str, Any]:
        molecule_name = molecules[molecule_idx % len(molecules)]
        return {
            "molecule_name": molecule_name,
            "bond_length": 0.74 if molecule_name == "H2" else 1.45
        }
    
    config = BenchmarkConfig(
        name="vqe_molecules",
        description="VQE performance on different molecules",
        num_runs=num_runs,
        problem_sizes=list(range(len(molecules)))
    )
    
    algorithm_configs = [
        AlgorithmConfig(
            algorithm_type=AlgorithmType.VQE_CHEMISTRY,
            max_iterations=30,
            algorithm_params={"ansatz_type": "hardware_efficient", "num_layers": 2}
        ),
        AlgorithmConfig(
            algorithm_type=AlgorithmType.VQE_CHEMISTRY,
            max_iterations=30,
            algorithm_params={"ansatz_type": "chemistry_inspired", "num_layers": 2}
        )
    ]
    
    harness = QuantumBenchmarkHarness()
    summaries = await harness.run_benchmark(config, algorithm_configs, problem_generator)
    
    return summaries

async def benchmark_backend_comparison(problem_size: int = 6,
                                     num_runs: int = 5) -> List[BenchmarkSummary]:
    """Compare performance across different backends"""
    
    def problem_generator(size: int) -> Dict[str, Any]:
        return {
            "num_vertices": problem_size,
            "edge_probability": 0.6,
            "seed": 42
        }
    
    config = BenchmarkConfig(
        name="backend_comparison",
        description="QAOA performance across different backends",
        num_runs=num_runs,
        problem_sizes=[problem_size]
    )
    
    algorithm_configs = [
        AlgorithmConfig(
            algorithm_type=AlgorithmType.QAOA_MAXCUT,
            backend_type=BackendType.QISKIT_SIMULATOR,
            max_iterations=30,
            algorithm_params={"max_layers": 2}
        ),
        AlgorithmConfig(
            algorithm_type=AlgorithmType.QAOA_MAXCUT,
            backend_type=BackendType.PENNYLANE_SIMULATOR,
            max_iterations=30,
            algorithm_params={"max_layers": 2}
        )
    ]
    
    harness = QuantumBenchmarkHarness()
    summaries = await harness.run_benchmark(config, algorithm_configs, problem_generator)
    
    return summaries

# Example usage
if __name__ == "__main__":
    async def run_example_benchmarks():
        """Run example benchmarks"""
        
        print("Running QAOA scaling benchmark...")
        qaoa_summary = await benchmark_qaoa_scaling(max_vertices=8, num_runs=3)
        print(f"QAOA scaling coefficient: {qaoa_summary.scaling_coefficient}")
        
        print("\nRunning VQE molecule benchmark...")
        vqe_summaries = await benchmark_vqe_molecules(num_runs=2)
        for summary in vqe_summaries:
            print(f"VQE {summary.algorithm_type}: {summary.success_rate:.2f} success rate")
        
        print("\nRunning backend comparison...")
        backend_summaries = await benchmark_backend_comparison(num_runs=3)
        for summary in backend_summaries:
            print(f"Backend comparison: {summary.mean_execution_time:.2f}s average")
    
    asyncio.run(run_example_benchmarks())