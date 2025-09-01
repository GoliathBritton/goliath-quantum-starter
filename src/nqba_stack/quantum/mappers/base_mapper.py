"""
FLYFOX AI Quantum Hub - Base Problem Mapper

Defines the base protocol that all problem mappers must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import numpy as np

from ..schemas.core_models import ProblemType


class ProblemMapper(ABC):
    """Base protocol for problem mappers."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.problem_type = ProblemType.QUBO  # Default to QUBO

    @abstractmethod
    async def map_to_qubo(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map business problem to QUBO format."""
        pass

    @abstractmethod
    async def validate_input(self, problem_data: Dict[str, Any]) -> bool:
        """Validate input problem data."""
        pass

    @abstractmethod
    async def estimate_problem_size(self, problem_data: Dict[str, Any]) -> int:
        """Estimate the size of the resulting QUBO problem."""
        pass

    async def map_to_ising(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """Map business problem to Ising format (default implementation)."""
        # Convert QUBO to Ising: x_i = (1 - s_i) / 2
        qubo_result = await self.map_to_qubo(problem_data)

        # Extract QUBO matrix and linear terms
        qubo_matrix = qubo_result.get("qubo_matrix", [])
        linear_terms = qubo_result.get("linear_terms", [])

        if not qubo_matrix:
            return {"ising_matrix": [], "ising_terms": []}

        # Convert to Ising format
        n = len(qubo_matrix)
        ising_matrix = np.zeros((n, n))
        ising_terms = np.zeros(n)

        # Convert QUBO to Ising
        for i in range(n):
            for j in range(n):
                if i == j:
                    # Diagonal terms: h_i = -0.5 * (linear_terms[i] + sum of QUBO diagonal)
                    ising_terms[i] = -0.5 * (
                        linear_terms[i] if i < len(linear_terms) else 0
                    )
                    for k in range(n):
                        if k != i:
                            ising_terms[i] -= 0.5 * qubo_matrix[i][k]
                else:
                    # Off-diagonal terms: J_ij = 0.25 * QUBO[i][j]
                    ising_matrix[i][j] = 0.25 * qubo_matrix[i][j]

        return {
            "ising_matrix": ising_matrix.tolist(),
            "ising_terms": ising_terms.tolist(),
            "metadata": {
                "converted_from": "qubo",
                "mapper": self.name,
                "problem_type": "ising",
            },
        }

    async def get_mapping_info(self) -> Dict[str, Any]:
        """Get information about the mapper."""
        return {
            "name": self.name,
            "description": self.description,
            "problem_type": self.problem_type.value,
            "supported_formats": ["qubo", "ising"],
            "features": [],
        }

    def _validate_matrix(self, matrix: List[List[float]]) -> bool:
        """Validate that matrix is square and numeric."""
        if not matrix:
            return False

        n = len(matrix)
        for row in matrix:
            if len(row) != n:
                return False
            if not all(isinstance(x, (int, float)) for x in row):
                return False

        return True

    def _validate_vector(self, vector: List[float], expected_length: int) -> bool:
        """Validate that vector has correct length and numeric values."""
        if len(vector) != expected_length:
            return False
        return all(isinstance(x, (int, float)) for x in vector)
