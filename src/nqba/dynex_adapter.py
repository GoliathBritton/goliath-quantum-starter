"""
NQBA Dynex Adapter - Core module imports
Imports from nqba_stack.core.dynex_adapter for compatibility
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "nqba_stack", "core"))

try:
    from dynex_adapter import DynexAdapter, score_leads, OptimizationResult
except ImportError:
    # Fallback if nqba_stack is not available
    from typing import Dict, Any, List
    from dataclasses import dataclass

    @dataclass
    class OptimizationResult:
        """Fallback OptimizationResult class"""

        success: bool
        samples: List[Dict[str, Any]]
        energy: float
        execution_time: float
        dynex_job_id: str = None
        error_message: str = None
        metadata: Dict[str, Any] = None

    class DynexAdapter:
        """Fallback DynexAdapter class"""

        def __init__(self, config=None):
            self.config = config or {}

        def solve_qubo(self, bqm, **kwargs):
            return OptimizationResult(
                success=False,
                samples=[],
                energy=0.0,
                execution_time=0.0,
                error_message="DynexAdapter not properly configured",
            )

    def score_leads(lead_data: List[Dict[str, Any]]) -> OptimizationResult:
        """Fallback lead scoring function"""
        return OptimizationResult(
            success=False,
            samples=[],
            energy=0.0,
            execution_time=0.0,
            error_message="Lead scoring not available",
        )
