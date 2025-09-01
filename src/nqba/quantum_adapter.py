import uuid
from typing import List, Dict, Any

try:
    from dynexsdk import DynexQUBOSolver

    DYNEX_AVAILABLE = True
except ImportError:
    DYNEX_AVAILABLE = False


def optimize_qubo(
    variables: int, Q: List, constraints: List = None, objective: str = "maximize"
) -> dict:
    """
    Solve QUBO using Dynex SDK if available, else fallback to mock.
    Q: list of (i, j, value) tuples or matrix
    """
    if DYNEX_AVAILABLE:
        try:
            solver = DynexQUBOSolver(num_variables=variables)
            # QUBO matrix: convert to required format if needed
            if isinstance(Q, list) and all(
                isinstance(x, (list, tuple)) and len(x) == 3 for x in Q
            ):
                for i, j, v in Q:
                    solver.add_qubo_term(i, j, v)
            else:
                # Assume Q is a square matrix
                for i in range(variables):
                    for j in range(variables):
                        solver.add_qubo_term(i, j, Q[i][j])
            if constraints:
                for c in constraints:
                    solver.add_constraint(c)
            result = solver.solve(maximize=(objective == "maximize"))
            assignment = result.get("assignment", [0] * variables)
            obj_val = result.get("objective_value", 0.0)
            backend = "dynex.sdk"
        except Exception as e:
            assignment = [0] * variables
            obj_val = 0.0
            backend = f"dynex.error:{e}"
    else:
        assignment = [1 if i % 2 == 0 else 0 for i in range(variables)]
        obj_val = 42.0
        backend = "mock.quantum"
    return {
        "decision_id": str(uuid.uuid4()),
        "assignment": assignment,
        "objective_value": obj_val,
        "backend": backend,
    }


class QuantumAdapter:
    """NQBA Quantum Adapter for quantum computing operations."""

    def __init__(self, backend: str = "auto"):
        self.backend = backend
        self.available_backends = ["dynex", "mock", "auto"]
        self.operation_history = []

    def solve_qubo(
        self,
        variables: int,
        Q: List,
        constraints: List = None,
        objective: str = "maximize",
    ) -> dict:
        """Solve QUBO problem using quantum backend."""
        result = optimize_qubo(variables, Q, constraints, objective)
        result["adapter_backend"] = self.backend
        result["timestamp"] = str(uuid.uuid4())
        self.operation_history.append(result)
        return result

    def get_available_backends(self) -> List[str]:
        """Get list of available quantum backends."""
        return self.available_backends

    def set_backend(self, backend: str):
        """Set the quantum backend to use."""
        if backend in self.available_backends:
            self.backend = backend
        else:
            raise ValueError(
                f"Backend {backend} not available. Choose from {self.available_backends}"
            )

    def get_operation_history(self) -> List[Dict[str, Any]]:
        """Get history of quantum operations."""
        return self.operation_history

    def clear_history(self):
        """Clear operation history."""
        self.operation_history.clear()
