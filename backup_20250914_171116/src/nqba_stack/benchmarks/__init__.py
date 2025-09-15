"""
NQBA Stack Benchmark Framework

This package provides comprehensive benchmarking capabilities to prove quantum advantage
over classical solvers for optimization problems.
"""

from .benchmark_runner import BenchmarkRunner, BenchmarkConfig, BenchmarkResult
from .problems import (
    PortfolioOptimization,
    TravelingSalesman,
    KnapsackProblem,
    get_all_problems,
)
from .solvers import ClassicalSolver, QuantumSolver, DynexSolver
from .reports import BenchmarkReport, PerformanceMetrics, generate_all_reports

__all__ = [
    "BenchmarkRunner",
    "BenchmarkConfig",
    "BenchmarkResult",
    "PortfolioOptimization",
    "TravelingSalesman",
    "KnapsackProblem",
    "get_all_problems",
    "ClassicalSolver",
    "QuantumSolver",
    "DynexSolver",
    "BenchmarkReport",
    "PerformanceMetrics",
    "generate_all_reports",
]
