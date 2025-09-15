"""
Benchmark Runner for NQBA Stack

Executes comprehensive benchmarks comparing classical vs. quantum solvers
to prove quantum advantage with quantifiable metrics.
"""

import asyncio
import time
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

from .problems import OptimizationProblem
from .solvers import ClassicalSolver, QuantumSolver
from .reports import BenchmarkReport, PerformanceMetrics

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkConfig:
    """Configuration for benchmark execution"""

    problem_size: int = 100
    iterations: int = 10
    timeout_seconds: int = 300
    output_dir: str = "benchmark_results"
    save_detailed: bool = True
    compare_solutions: bool = True


@dataclass
class BenchmarkResult:
    """Results from a single benchmark run"""

    problem_name: str
    solver_name: str
    execution_time: float
    solution_quality: float
    memory_usage: float
    energy_consumption: Optional[float] = None
    cost_per_solution: Optional[float] = None
    metadata: Dict[str, Any] = None


class BenchmarkRunner:
    """
    Main benchmark runner that executes head-to-head comparisons
    between classical and quantum solvers.
    """

    def __init__(self, config: BenchmarkConfig):
        self.config = config
        self.results: List[BenchmarkResult] = []
        self.output_dir = Path(config.output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Initialize solvers
        self.classical_solver = ClassicalSolver()
        self.quantum_solver = QuantumSolver()

        logger.info(f"Benchmark runner initialized with config: {config}")

    async def run_comprehensive_benchmark(
        self, problems: List[OptimizationProblem]
    ) -> BenchmarkReport:
        """
        Run comprehensive benchmarks across all problems and solvers
        """
        logger.info(f"Starting comprehensive benchmark with {len(problems)} problems")

        start_time = time.time()

        for problem in problems:
            logger.info(f"Benchmarking problem: {problem.name}")

            # Run classical solver benchmark
            classical_result = await self._run_single_benchmark(
                problem, self.classical_solver, "Classical"
            )
            self.results.append(classical_result)

            # Run quantum solver benchmark
            quantum_result = await self._run_single_benchmark(
                problem, self.quantum_solver, "Quantum"
            )
            self.results.append(quantum_result)

            # Compare solutions if enabled
            if self.config.compare_solutions:
                comparison = self._compare_solutions(classical_result, quantum_result)
                logger.info(f"Solution comparison: {comparison}")

        total_time = time.time() - start_time
        logger.info(f"Benchmark completed in {total_time:.2f} seconds")

        # Generate comprehensive report
        report = self._generate_report()

        # Save results
        if self.config.save_detailed:
            self._save_detailed_results()

        return report

    async def _run_single_benchmark(
        self, problem: OptimizationProblem, solver: Any, solver_name: str
    ) -> BenchmarkResult:
        """
        Run a single benchmark for a problem-solver combination
        """
        logger.info(f"Running {solver_name} solver on {problem.name}")

        # Prepare problem
        problem_data = problem.prepare_data(self.config.problem_size)

        # Set current data for evaluation
        problem._set_current_data(problem_data)

        # Measure execution time
        start_time = time.time()
        start_memory = self._get_memory_usage()

        try:
            # Execute solver with timeout
            solution = await asyncio.wait_for(
                solver.solve(
                    problem_data.data
                ),  # Pass the data dict, not the ProblemData object
                timeout=self.config.timeout_seconds,
            )

            execution_time = time.time() - start_time
            end_memory = self._get_memory_usage()
            memory_usage = end_memory - start_memory

            # Calculate solution quality
            solution_quality = problem.evaluate_solution(solution)

            # Estimate energy consumption and cost
            energy_consumption = self._estimate_energy_consumption(
                execution_time, solver_name
            )
            cost_per_solution = self._estimate_cost(execution_time, solver_name)

            result = BenchmarkResult(
                problem_name=problem.name,
                solver_name=solver_name,
                execution_time=execution_time,
                solution_quality=solution_quality,
                memory_usage=memory_usage,
                energy_consumption=energy_consumption,
                cost_per_solution=cost_per_solution,
                metadata={
                    "problem_size": self.config.problem_size,
                    "solver_version": getattr(solver, "version", "unknown"),
                    "timestamp": time.time(),
                },
            )

            logger.info(
                f"{solver_name} completed in {execution_time:.3f}s, quality: {solution_quality:.3f}"
            )
            return result

        except asyncio.TimeoutError:
            logger.warning(
                f"{solver_name} solver timed out after {self.config.timeout_seconds}s"
            )
            return BenchmarkResult(
                problem_name=problem.name,
                solver_name=solver_name,
                execution_time=self.config.timeout_seconds,
                solution_quality=0.0,
                memory_usage=0.0,
                metadata={"error": "timeout"},
            )
        except Exception as e:
            logger.error(f"Error running {solver_name} solver: {e}")
            return BenchmarkResult(
                problem_name=problem.name,
                solver_name=solver_name,
                execution_time=0.0,
                solution_quality=0.0,
                memory_usage=0.0,
                metadata={"error": str(e)},
            )

    def _compare_solutions(
        self, classical: BenchmarkResult, quantum: BenchmarkResult
    ) -> Dict[str, Any]:
        """
        Compare classical vs. quantum solution performance
        """
        if classical.metadata and "error" in classical.metadata:
            return {"status": "classical_failed", "error": classical.metadata["error"]}

        if quantum.metadata and "error" in quantum.metadata:
            return {"status": "quantum_failed", "error": quantum.metadata["error"]}

        # Calculate performance deltas
        speedup = (
            classical.execution_time / quantum.execution_time
            if quantum.execution_time > 0
            else float("inf")
        )

        # Handle divide by zero for quality improvement
        if classical.solution_quality == 0:
            if quantum.solution_quality > 0:
                quality_improvement = float("inf")  # Infinite improvement from 0
            else:
                quality_improvement = 0  # Both 0, no improvement
        else:
            quality_improvement = (
                (quantum.solution_quality - classical.solution_quality)
                / classical.solution_quality
                * 100
            )

        cost_savings = 0
        if (
            classical.cost_per_solution
            and quantum.cost_per_solution
            and classical.cost_per_solution > 0
        ):
            cost_savings = (
                (classical.cost_per_solution - quantum.cost_per_solution)
                / classical.cost_per_solution
                * 100
            )

        energy_savings = 0
        if (
            classical.energy_consumption
            and quantum.energy_consumption
            and classical.energy_consumption > 0
        ):
            energy_savings = (
                (classical.energy_consumption - quantum.energy_consumption)
                / classical.energy_consumption
                * 100
            )

        return {
            "status": "success",
            "speedup": speedup,
            "quality_improvement_percent": quality_improvement,
            "cost_savings_percent": cost_savings,
            "energy_savings_percent": energy_savings,
            "quantum_advantage": {
                "speed": speedup > 1.0,
                "quality": quality_improvement > 0,
                "cost": cost_savings > 0,
                "energy": energy_savings > 0,
            },
        }

    def _generate_report(self) -> BenchmarkReport:
        """
        Generate comprehensive benchmark report
        """
        # Group results by problem
        problem_results = {}
        for result in self.results:
            if result.problem_name not in problem_results:
                problem_results[result.problem_name] = []
            problem_results[result.problem_name].append(result)

        # Calculate aggregate metrics
        total_problems = len(problem_results)
        successful_quantum_runs = sum(
            1
            for r in self.results
            if r.solver_name == "Quantum" and "error" not in (r.metadata or {})
        )
        successful_classical_runs = sum(
            1
            for r in self.results
            if r.solver_name == "Classical" and "error" not in (r.metadata or {})
        )

        # Calculate average performance metrics
        quantum_times = [
            r.execution_time
            for r in self.results
            if r.solver_name == "Quantum" and "error" not in (r.metadata or {})
        ]
        classical_times = [
            r.execution_time
            for r in self.results
            if r.solver_name == "Classical" and "error" not in (r.metadata or {})
        ]

        avg_quantum_time = (
            sum(quantum_times) / len(quantum_times) if quantum_times else 0
        )
        avg_classical_time = (
            sum(classical_times) / len(classical_times) if classical_times else 0
        )

        overall_speedup = (
            avg_classical_time / avg_quantum_time if avg_quantum_time > 0 else 0
        )

        # Calculate summary metrics
        summary = {
            "classical_success_rate": (
                successful_classical_runs
                / len([r for r in self.results if r.solver_name == "Classical"])
                if any(r.solver_name == "Classical" for r in self.results)
                else 0
            ),
            "quantum_success_rate": (
                successful_quantum_runs
                / len([r for r in self.results if r.solver_name == "Quantum"])
                if any(r.solver_name == "Quantum" for r in self.results)
                else 0
            ),
            "average_speedup": overall_speedup,
            "quality_improvement_percent": 0,  # Will be calculated from individual comparisons
            "avg_classical_time": avg_classical_time,
            "avg_quantum_time": avg_quantum_time,
            "avg_classical_quality": 0,  # Will be calculated from individual results
            "avg_quantum_quality": 0,  # Will be calculated from individual results
            "total_problems": total_problems,
        }

        report = BenchmarkReport(
            total_problems=total_problems,
            successful_quantum_runs=successful_quantum_runs,
            successful_classical_runs=successful_classical_runs,
            overall_speedup=overall_speedup,
            problem_results=problem_results,
            timestamp=time.time(),
            config=self.config,
            summary=summary,
        )

        return report

    def _save_detailed_results(self):
        """
        Save detailed benchmark results to files
        """
        # Save raw results
        results_file = self.output_dir / "benchmark_results.json"
        with open(results_file, "w") as f:
            json.dump([asdict(r) for r in self.results], f, indent=2, default=str)

        # Save summary report
        summary_file = self.output_dir / "benchmark_summary.txt"
        with open(summary_file, "w") as f:
            f.write("NQBA Stack Benchmark Summary\n")
            f.write("=" * 50 + "\n\n")

            for result in self.results:
                f.write(f"Problem: {result.problem_name}\n")
                f.write(f"Solver: {result.solver_name}\n")
                f.write(f"Time: {result.execution_time:.3f}s\n")
                f.write(f"Quality: {result.solution_quality:.3f}\n")
                f.write(f"Memory: {result.memory_usage:.2f} MB\n")
                if result.energy_consumption:
                    f.write(f"Energy: {result.energy_consumption:.2f} J\n")
                if result.cost_per_solution:
                    f.write(f"Cost: ${result.cost_per_solution:.4f}\n")
                f.write("-" * 30 + "\n")

        logger.info(f"Detailed results saved to {self.output_dir}")

    def _get_memory_usage(self) -> float:
        """
        Get current memory usage in MB
        """
        try:
            import psutil

            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            return 0.0

    def _estimate_energy_consumption(
        self, execution_time: float, solver_name: str
    ) -> float:
        """
        Estimate energy consumption based on execution time and solver type
        """
        # Rough estimates - these should be calibrated with real measurements
        if solver_name == "Quantum":
            # Quantum computers typically use more power but may be faster
            return execution_time * 1000  # 1kW for quantum system
        else:
            # Classical systems
            return execution_time * 200  # 200W for classical system

    def _estimate_cost(self, execution_time: float, solver_name: str) -> float:
        """
        Estimate cost per solution based on execution time and solver type
        """
        # Rough estimates - these should be calibrated with real pricing
        if solver_name == "Quantum":
            # Quantum cloud pricing (e.g., Dynex)
            return execution_time * 0.10  # $0.10 per second
        else:
            # Classical cloud pricing (e.g., AWS)
            return execution_time * 0.01  # $0.01 per second


async def run_quick_benchmark(problem: OptimizationProblem) -> BenchmarkReport:
    """
    Convenience function to run a quick benchmark on a single problem
    """
    config = BenchmarkConfig(
        problem_size=50, iterations=3, timeout_seconds=60, save_detailed=True
    )

    runner = BenchmarkRunner(config)
    return await runner.run_comprehensive_benchmark([problem])
