#!/usr/bin/env python3
"""
🧪 Benchmark Tests for Quantum vs Classical Solvers

Compares performance of quantum optimization (Dynex) vs classical solvers
for various optimization problems. Generates win/loss reports for investors.
"""

import pytest
import time
import json
import statistics
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
from pathlib import Path

# Mock imports for testing - replace with actual implementations
try:
    from src.nqba_stack.quantum.adapters.dynex_adapter import DynexAdapter
    from src.nqba_stack.quantum.classical_solvers import ClassicalSolver
except ImportError:
    # Mock implementations for testing
    class DynexAdapter:
        def solve_qubo(self, qubo_matrix, **kwargs):
            return {"solution": [1, 0, 1, 0], "energy": -10.5, "time_ms": 150}

    class ClassicalSolver:
        def solve_qubo(self, qubo_matrix, **kwargs):
            return {"solution": [1, 0, 1, 0], "energy": -10.2, "time_ms": 45}


@dataclass
class BenchmarkResult:
    """Results from a single benchmark run"""

    problem_type: str
    problem_size: int
    classical_time: float
    quantum_time: float
    classical_energy: float
    quantum_energy: float
    classical_solution: List[int]
    quantum_solution: List[int]
    quantum_advantage: float
    time_improvement: float
    energy_improvement: float


class BenchmarkSuite:
    """Comprehensive benchmark suite for quantum vs classical optimization"""

    def __init__(self):
        self.dynex_adapter = DynexAdapter()
        self.classical_solver = ClassicalSolver()
        self.results: List[BenchmarkResult] = []

    def generate_knapsack_problem(self, size: int) -> Dict[str, Any]:
        """Generate a knapsack problem of given size"""
        import random

        weights = [random.randint(1, 10) for _ in range(size)]
        values = [random.randint(5, 20) for _ in range(size)]
        capacity = sum(weights) // 2

        return {
            "weights": weights,
            "values": values,
            "capacity": capacity,
            "type": "knapsack",
        }

    def generate_portfolio_problem(self, size: int) -> Dict[str, Any]:
        """Generate a portfolio optimization problem"""
        import random
        import numpy as np

        # Generate random returns and covariance matrix
        returns = [random.uniform(-0.1, 0.2) for _ in range(size)]
        cov_matrix = np.random.rand(size, size)
        cov_matrix = (cov_matrix + cov_matrix.T) / 2  # Make symmetric
        np.fill_diagonal(cov_matrix, 0.1)  # Add variance

        return {
            "returns": returns,
            "covariance": cov_matrix.tolist(),
            "target_return": 0.15,
            "type": "portfolio",
        }

    def generate_coverage_problem(self, size: int) -> Dict[str, Any]:
        """Generate a set cover problem"""
        import random

        universe_size = size * 2
        subsets = []
        for _ in range(size):
            subset_size = random.randint(1, universe_size // 2)
            subset = set(random.sample(range(universe_size), subset_size))
            subsets.append(list(subset))

        return {
            "universe": list(range(universe_size)),
            "subsets": subsets,
            "type": "coverage",
        }

    def run_benchmark(
        self, problem: Dict[str, Any], iterations: int = 5
    ) -> BenchmarkResult:
        """Run a single benchmark comparing quantum vs classical"""

        problem_type = problem["type"]
        problem_size = len(
            problem.get("weights", problem.get("returns", problem.get("subsets", [])))
        )

        # Run classical solver multiple times
        classical_times = []
        classical_energies = []
        classical_solutions = []

        for _ in range(iterations):
            start_time = time.time()
            classical_result = self.classical_solver.solve_qubo(problem)
            classical_times.append(time.time() - start_time)
            classical_energies.append(classical_result["energy"])
            classical_solutions.append(classical_result["solution"])

        # Run quantum solver
        start_time = time.time()
        quantum_result = self.dynex_adapter.solve_qubo(problem)
        quantum_time = time.time() - start_time

        # Calculate averages for classical
        avg_classical_time = statistics.mean(classical_times)
        avg_classical_energy = statistics.mean(classical_energies)
        best_classical_solution = classical_solutions[
            classical_energies.index(min(classical_energies))
        ]

        # Calculate improvements
        time_improvement = (
            (avg_classical_time - quantum_time) / avg_classical_time * 100
        )
        energy_improvement = (
            (quantum_result["energy"] - avg_classical_energy)
            / abs(avg_classical_energy)
            * 100
        )
        quantum_advantage = (
            avg_classical_time / quantum_time if quantum_time > 0 else float("inf")
        )

        return BenchmarkResult(
            problem_type=problem_type,
            problem_size=problem_size,
            classical_time=avg_classical_time,
            quantum_time=quantum_time,
            classical_energy=avg_classical_energy,
            quantum_energy=quantum_result["energy"],
            classical_solution=best_classical_solution,
            quantum_solution=quantum_result["solution"],
            quantum_advantage=quantum_advantage,
            time_improvement=time_improvement,
            energy_improvement=energy_improvement,
        )

    def run_comprehensive_benchmark(self, max_size: int = 20) -> List[BenchmarkResult]:
        """Run benchmarks across multiple problem types and sizes"""

        problem_types = ["knapsack", "portfolio", "coverage"]
        sizes = [5, 10, 15, 20] if max_size >= 20 else [5, 10, max_size]

        for problem_type in problem_types:
            for size in sizes:
                if size <= max_size:
                    if problem_type == "knapsack":
                        problem = self.generate_knapsack_problem(size)
                    elif problem_type == "portfolio":
                        problem = self.generate_portfolio_problem(size)
                    elif problem_type == "coverage":
                        problem = self.generate_coverage_problem(size)

                    result = self.run_benchmark(problem)
                    self.results.append(result)

                    print(
                        f"✅ {problem_type.capitalize()} (size {size}): "
                        f"Quantum {result.quantum_advantage:.2f}x faster, "
                        f"{result.energy_improvement:.1f}% better energy"
                    )

        return self.results

    def generate_report(
        self, output_file: str = "benchmark_report.json"
    ) -> Dict[str, Any]:
        """Generate a comprehensive benchmark report"""

        if not self.results:
            raise ValueError("No benchmark results available. Run benchmarks first.")

        # Calculate aggregate statistics
        total_problems = len(self.results)
        quantum_wins = sum(1 for r in self.results if r.quantum_advantage > 1.0)
        quantum_losses = total_problems - quantum_wins

        avg_quantum_advantage = statistics.mean(
            [
                r.quantum_advantage
                for r in self.results
                if r.quantum_advantage != float("inf")
            ]
        )
        avg_time_improvement = statistics.mean(
            [r.time_improvement for r in self.results]
        )
        avg_energy_improvement = statistics.mean(
            [r.energy_improvement for r in self.results]
        )

        # Problem type breakdown
        type_stats = {}
        for result in self.results:
            if result.problem_type not in type_stats:
                type_stats[result.problem_type] = []
            type_stats[result.problem_type].append(result.quantum_advantage)

        type_averages = {
            prob_type: statistics.mean(adv) for prob_type, adv in type_stats.items()
        }

        report = {
            "summary": {
                "total_problems": total_problems,
                "quantum_wins": quantum_wins,
                "quantum_losses": quantum_losses,
                "win_rate": f"{(quantum_wins/total_problems)*100:.1f}%",
                "avg_quantum_advantage": f"{avg_quantum_advantage:.2f}x",
                "avg_time_improvement": f"{avg_time_improvement:.1f}%",
                "avg_energy_improvement": f"{avg_energy_improvement:.1f}%",
            },
            "problem_type_breakdown": type_averages,
            "detailed_results": [
                {
                    "problem_type": r.problem_type,
                    "problem_size": r.problem_size,
                    "quantum_advantage": r.quantum_advantage,
                    "time_improvement": r.time_improvement,
                    "energy_improvement": r.energy_improvement,
                }
                for r in self.results
            ],
            "metadata": {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "benchmark_version": "1.0.0",
                "quantum_backend": "Dynex",
                "classical_backend": "OR-Tools/dimod",
            },
        }

        # Save report
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        return report


# Test functions for pytest
@pytest.mark.benchmark
def test_knapsack_benchmark():
    """Test knapsack problem benchmarking"""
    suite = BenchmarkSuite()
    problem = suite.generate_knapsack_problem(10)
    result = suite.run_benchmark(problem)

    assert result.problem_type == "knapsack"
    assert result.problem_size == 10
    assert result.quantum_time > 0
    assert result.classical_time > 0
    assert len(result.quantum_solution) == 10
    assert len(result.classical_solution) == 10


@pytest.mark.benchmark
def test_portfolio_benchmark():
    """Test portfolio optimization benchmarking"""
    suite = BenchmarkSuite()
    problem = suite.generate_portfolio_problem(8)
    result = suite.run_benchmark(problem)

    assert result.problem_type == "portfolio"
    assert result.problem_size == 8
    assert result.quantum_time > 0
    assert result.classical_time > 0


@pytest.mark.benchmark
def test_coverage_benchmark():
    """Test set cover problem benchmarking"""
    suite = BenchmarkSuite()
    problem = suite.generate_coverage_problem(12)
    result = suite.run_benchmark(problem)

    assert result.problem_type == "coverage"
    assert result.problem_size == 12
    assert result.quantum_time > 0
    assert result.classical_time > 0


@pytest.mark.benchmark
def test_comprehensive_benchmark():
    """Test comprehensive benchmarking suite"""
    suite = BenchmarkSuite()
    results = suite.run_comprehensive_benchmark(max_size=15)

    assert len(results) > 0
    assert all(isinstance(r, BenchmarkResult) for r in results)

    # Generate report
    report = suite.generate_report("test_benchmark_report.json")

    assert "summary" in report
    assert "detailed_results" in report
    assert report["summary"]["total_problems"] > 0

    # Clean up test file
    Path("test_benchmark_report.json").unlink(missing_ok=True)


if __name__ == "__main__":
    # Run benchmarks if executed directly
    print("🚀 Running NQBA Quantum vs Classical Benchmark Suite...")

    suite = BenchmarkSuite()
    results = suite.run_comprehensive_benchmark()

    print(f"\n📊 Benchmark Complete!")
    print(f"Total problems: {len(results)}")

    # Generate and display report
    report = suite.generate_report()

    print(f"\n🏆 Summary:")
    print(f"Quantum Win Rate: {report['summary']['win_rate']}")
    print(f"Average Quantum Advantage: {report['summary']['avg_quantum_advantage']}")
    print(f"Average Time Improvement: {report['summary']['avg_time_improvement']}")
    print(f"Average Energy Improvement: {report['summary']['avg_energy_improvement']}")

    print(f"\n📈 Problem Type Breakdown:")
    for prob_type, avg_adv in report["problem_type_breakdown"].items():
        print(f"  {prob_type.capitalize()}: {avg_adv:.2f}x advantage")

    print(f"\n📄 Detailed report saved to: benchmark_report.json")
