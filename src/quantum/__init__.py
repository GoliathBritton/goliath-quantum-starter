"""Quantum Algorithms Module for Goliath Quantum Starter Platform

This module contains advanced quantum-inspired algorithms designed to enhance
the NQBA stack with dynamic optimization and reasoning capabilities.

Modules:
- reasoning: Reversal reasoning algorithms for logical inference
- optimization: Parallel QAOA optimization for finance/energy/insurance
- utils: Utility functions for quantum algorithm operations
"""

__version__ = "1.0.0"
__author__ = "Goliath Quantum Team"

from .reasoning import reversal_reasoning
from .optimization import parallel_qaoa, optimize_qaoa
from .diffusion import quantum_diffusion, parallel_quantum_diffusion, get_diffusion_performance, diffusion_engine
from .meta_algorithm import (
    dynamic_algo_instituter,
    get_meta_performance,
    adapt_preferences,
    meta_instituter,
    DynamicAlgorithmInstituter,
    TaskType,
    AlgorithmPerformance
)

__all__ = [
    "reversal_reasoning",
    "parallel_qaoa", 
    "optimize_qaoa",
    "quantum_diffusion",
    "parallel_quantum_diffusion",
    "get_diffusion_performance",
    "diffusion_engine",
    "dynamic_algo_instituter",
    "get_meta_performance",
    "adapt_preferences",
    "meta_instituter",
    "DynamicAlgorithmInstituter",
    "TaskType",
    "AlgorithmPerformance"
]