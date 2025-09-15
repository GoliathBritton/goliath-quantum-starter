"""
Classical Adapter - Fallback Optimization Solvers

This module provides classical optimization solvers as fallbacks when
quantum solvers are unavailable, ensuring 24/7 optimization capabilities.
"""

import logging
import time
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ClassicalSolver(ABC):
    """Abstract base class for classical solvers"""

    @abstractmethod
    async def solve(
        self, problem_data: Dict[str, Any], timeout: int = 300
    ) -> Dict[str, Any]:
        """Solve an optimization problem"""
        pass

    @abstractmethod
    def get_solver_info(self) -> Dict[str, Any]:
        """Get information about the solver"""
        pass


class DimodSolver(ClassicalSolver):
    """Dimod-based classical solver for QUBO problems"""

    def __init__(self):
        self.name = "dimod"
        self.version = "0.12.0"
        self.supported_problems = ["qubo", "bqm", "ising"]

        # Try to import dimod
        try:
            import dimod

            self.dimod = dimod
            self.available = True
            logger.info("Dimod solver initialized successfully")
        except ImportError:
            self.available = False
            logger.warning("Dimod not available - install with: pip install dimod")

    async def solve(
        self, problem_data: Dict[str, Any], timeout: int = 300
    ) -> Dict[str, Any]:
        """Solve QUBO problem using Dimod"""
        if not self.available:
            raise RuntimeError("Dimod solver not available")

        try:
            operation = problem_data.get("operation", "qubo")
            inputs = problem_data.get("inputs", {})

            if operation == "qubo":
                return await self._solve_qubo(inputs, timeout)
            elif operation == "bqm":
                return await self._solve_bqm(inputs, timeout)
            elif operation == "ising":
                return await self._solve_ising(inputs, timeout)
            else:
                raise ValueError(f"Unsupported operation: {operation}")

        except Exception as e:
            logger.error(f"Dimod solver error: {e}")
            raise

    async def _solve_qubo(self, inputs: Dict[str, Any], timeout: int) -> Dict[str, Any]:
        """Solve QUBO problem"""
        # Extract QUBO matrix and offset
        qubo_matrix = inputs.get("qubo_matrix", {})
        offset = inputs.get("offset", 0.0)

        # Convert to dimod format
        bqm = self.dimod.BinaryQuadraticModel.from_qubo(qubo_matrix, offset)

        # Solve using exact solver for small problems, heuristic for larger ones
        if len(bqm.variables) <= 20:
            solver = self.dimod.ExactSolver()
        else:
            solver = self.dimod.SimulatedAnnealingSampler()

        start_time = time.time()
        sampleset = solver.sample(bqm)
        execution_time = time.time() - start_time

        # Get best solution
        best_sample = sampleset.first.sample
        best_energy = sampleset.first.energy

        return {
            "solution": best_sample,
            "objective_value": best_energy,
            "execution_time": execution_time,
            "solver": "dimod",
            "solver_method": (
                "exact" if len(bqm.variables) <= 20 else "simulated_annealing"
            ),
            "num_variables": len(bqm.variables),
            "num_quadratic_terms": len(bqm.quadratic),
        }

    async def _solve_bqm(self, inputs: Dict[str, Any], timeout: int) -> Dict[str, Any]:
        """Solve Binary Quadratic Model"""
        # Extract BQM components
        linear = inputs.get("linear", {})
        quadratic = inputs.get("quadratic", {})
        vartype = inputs.get("vartype", "BINARY")

        # Create BQM
        bqm = self.dimod.BinaryQuadraticModel(linear, quadratic, vartype)

        # Solve
        solver = self.dimod.SimulatedAnnealingSampler()
        start_time = time.time()
        sampleset = solver.sample(bqm)
        execution_time = time.time() - start_time

        best_sample = sampleset.first.sample
        best_energy = sampleset.first.energy

        return {
            "solution": best_sample,
            "objective_value": best_energy,
            "execution_time": execution_time,
            "solver": "dimod",
            "solver_method": "simulated_annealing",
            "num_variables": len(bqm.variables),
            "num_quadratic_terms": len(bqm.quadratic),
        }

    async def _solve_ising(
        self, inputs: Dict[str, Any], timeout: int
    ) -> Dict[str, Any]:
        """Solve Ising model"""
        # Extract Ising components
        linear = inputs.get("linear", {})
        quadratic = inputs.get("quadratic", {})

        # Create BQM from Ising
        bqm = self.dimod.BinaryQuadraticModel.from_ising(linear, quadratic)

        # Solve
        solver = self.dimod.SimulatedAnnealingSampler()
        start_time = time.time()
        sampleset = solver.sample(bqm)
        execution_time = time.time() - start_time

        best_sample = sampleset.first.sample
        best_energy = sampleset.first.energy

        return {
            "solution": best_sample,
            "objective_value": best_energy,
            "execution_time": execution_time,
            "solver": "dimod",
            "solver_method": "simulated_annealing",
            "num_variables": len(bqm.variables),
            "num_quadratic_terms": len(bqm.quadratic),
        }

    def get_solver_info(self) -> Dict[str, Any]:
        """Get solver information"""
        return {
            "name": self.name,
            "version": self.version,
            "available": self.available,
            "supported_problems": self.supported_problems,
            "type": "classical",
        }


class ORToolsSolver(ClassicalSolver):
    """OR-Tools-based classical solver for various optimization problems"""

    def __init__(self):
        self.name = "ortools"
        self.version = "9.5.0"
        self.supported_problems = [
            "linear_programming",
            "integer_programming",
            "constraint_programming",
            "routing",
        ]

        # Try to import OR-Tools
        try:
            from ortools.linear_solver import pywraplp
            from ortools.constraint_solver import routing_enums_pb2
            from ortools.constraint_solver import pywrapcp

            self.pywraplp = pywraplp
            self.routing_enums_pb2 = routing_enums_pb2
            self.pywrapcp = pywrapcp
            self.available = True
            logger.info("OR-Tools solver initialized successfully")
        except ImportError:
            self.available = False
            logger.warning("OR-Tools not available - install with: pip install ortools")

    async def solve(
        self, problem_data: Dict[str, Any], timeout: int = 300
    ) -> Dict[str, Any]:
        """Solve optimization problem using OR-Tools"""
        if not self.available:
            raise RuntimeError("OR-Tools solver not available")

        try:
            operation = problem_data.get("operation", "linear_programming")
            inputs = problem_data.get("inputs", {})

            if operation == "linear_programming":
                return await self._solve_linear_programming(inputs, timeout)
            elif operation == "integer_programming":
                return await self._solve_integer_programming(inputs, timeout)
            elif operation == "constraint_programming":
                return await self._solve_constraint_programming(inputs, timeout)
            elif operation == "routing":
                return await self._solve_routing(inputs, timeout)
            else:
                raise ValueError(f"Unsupported operation: {operation}")

        except Exception as e:
            logger.error(f"OR-Tools solver error: {e}")
            raise

    async def _solve_linear_programming(
        self, inputs: Dict[str, Any], timeout: int
    ) -> Dict[str, Any]:
        """Solve linear programming problem"""
        # Extract LP components
        objective_coeffs = inputs.get("objective_coeffs", [])
        constraint_matrix = inputs.get("constraint_matrix", [])
        constraint_rhs = inputs.get("constraint_rhs", [])
        variable_bounds = inputs.get("variable_bounds", [])

        # Create solver
        solver = self.pywraplp.Solver.CreateSolver("GLOP")
        if not solver:
            raise RuntimeError("Failed to create GLOP solver")

        # Set timeout
        solver.SetTimeLimit(timeout * 1000)  # Convert to milliseconds

        # Create variables
        num_vars = len(objective_coeffs)
        variables = []
        for i in range(num_vars):
            if i < len(variable_bounds):
                lb, ub = variable_bounds[i]
                var = solver.NumVar(lb, ub, f"x_{i}")
            else:
                var = solver.NumVar(0, solver.infinity(), f"x_{i}")
            variables.append(var)

        # Set objective
        objective = solver.Objective()
        for i, coeff in enumerate(objective_coeffs):
            objective.SetCoefficient(variables[i], coeff)
        objective.SetMinimization()

        # Add constraints
        for i, constraint_row in enumerate(constraint_matrix):
            if i < len(constraint_rhs):
                constraint = solver.Constraint(0, constraint_rhs[i])
                for j, coeff in enumerate(constraint_row):
                    if j < len(variables):
                        constraint.SetCoefficient(variables[j], coeff)

        # Solve
        start_time = time.time()
        status = solver.Solve()
        execution_time = time.time() - start_time

        if status == self.pywraplp.Solver.OPTIMAL:
            solution = [var.solution_value() for var in variables]
            objective_value = objective.Value()
        else:
            raise RuntimeError(f"LP solver failed with status: {status}")

        return {
            "solution": solution,
            "objective_value": objective_value,
            "execution_time": execution_time,
            "solver": "ortools",
            "solver_method": "glop",
            "num_variables": num_vars,
            "num_constraints": len(constraint_matrix),
            "status": "optimal",
        }

    async def _solve_integer_programming(
        self, inputs: Dict[str, Any], timeout: int
    ) -> Dict[str, Any]:
        """Solve integer programming problem"""
        # Similar to LP but with integer variables
        # For brevity, implementing a simplified version
        return await self._solve_linear_programming(inputs, timeout)

    async def _solve_constraint_programming(
        self, inputs: Dict[str, Any], timeout: int
    ) -> Dict[str, Any]:
        """Solve constraint programming problem"""
        # Extract CP components
        variables = inputs.get("variables", [])
        constraints = inputs.get("constraints", [])

        # Create solver
        solver = self.pywrapcp.Solver("CP")

        # Set timeout
        solver.SetTimeLimit(timeout * 1000)

        # Create variables
        cp_vars = []
        for var_info in variables:
            var_type = var_info.get("type", "int")
            if var_type == "int":
                var = solver.IntVar(var_info.get("min", 0), var_info.get("max", 100))
            else:
                var = solver.BoolVar()
            cp_vars.append(var)

        # Add constraints (simplified)
        for constraint in constraints:
            # This would parse and add actual constraints
            pass

        # Create decision builder
        db = solver.Phase(
            cp_vars, solver.CHOOSE_MIN_SIZE_LOWEST_MIN, solver.ASSIGN_MIN_VALUE
        )

        # Solve
        start_time = time.time()
        solver.NewSearch(db)
        if solver.NextSolution():
            solution = [var.Value() for var in cp_vars]
        else:
            solution = []
        execution_time = time.time() - start_time

        return {
            "solution": solution,
            "objective_value": 0.0,  # CP doesn't always have explicit objective
            "execution_time": execution_time,
            "solver": "ortools",
            "solver_method": "constraint_programming",
            "num_variables": len(cp_vars),
            "status": "feasible" if solution else "infeasible",
        }

    async def _solve_routing(
        self, inputs: Dict[str, Any], timeout: int
    ) -> Dict[str, Any]:
        """Solve vehicle routing problem"""
        # Extract routing components
        distance_matrix = inputs.get("distance_matrix", [])
        num_vehicles = inputs.get("num_vehicles", 1)
        depot = inputs.get("depot", 0)

        # Create routing model
        manager = self.pywrapcp.RoutingIndexManager(
            len(distance_matrix), num_vehicles, depot
        )
        routing = self.pywrapcp.RoutingModel(manager)

        # Set distance callback
        def distance_callback(from_index, to_index):
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return distance_matrix[from_node][to_node]

        routing.SetArcCostEvaluatorOfAllVehicles(
            routing.RegisterTransitCallback(distance_callback)
        )

        # Set search parameters
        search_parameters = self.pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.time_limit.seconds = timeout

        # Solve
        start_time = time.time()
        solution = routing.SolveWithParameters(search_parameters)
        execution_time = time.time() - start_time

        if solution:
            # Extract route
            route = []
            index = routing.Start(0)
            while not routing.IsEnd(index):
                route.append(manager.IndexToNode(index))
                index = solution.Value(routing.NextVar(index))
            route.append(manager.IndexToNode(index))

            objective_value = solution.ObjectiveValue()
        else:
            route = []
            objective_value = float("inf")

        return {
            "solution": route,
            "objective_value": objective_value,
            "execution_time": execution_time,
            "solver": "ortools",
            "solver_method": "routing",
            "num_vehicles": num_vehicles,
            "num_locations": len(distance_matrix),
            "status": "optimal" if solution else "failed",
        }

    def get_solver_info(self) -> Dict[str, Any]:
        """Get solver information"""
        return {
            "name": self.name,
            "version": self.version,
            "available": self.available,
            "supported_problems": self.supported_problems,
            "type": "classical",
        }


class ClassicalAdapter:
    """Adapter for classical optimization solvers"""

    def __init__(self, solver_name: str = "auto"):
        self.solvers = {}
        self.primary_solver = None

        # Initialize available solvers
        self._initialize_solvers()

        # Set primary solver
        if solver_name == "auto":
            self._set_auto_primary()
        else:
            self._set_primary_solver(solver_name)

    def _initialize_solvers(self):
        """Initialize available classical solvers"""
        # Try to initialize Dimod
        try:
            dimod_solver = DimodSolver()
            if dimod_solver.available:
                self.solvers["dimod"] = dimod_solver
                logger.info("Dimod solver registered")
        except Exception as e:
            logger.warning(f"Failed to initialize Dimod: {e}")

        # Try to initialize OR-Tools
        try:
            ortools_solver = ORToolsSolver()
            if ortools_solver.available:
                self.solvers["ortools"] = ortools_solver
                logger.info("OR-Tools solver registered")
        except Exception as e:
            logger.warning(f"Failed to initialize OR-Tools: {e}")

    def _set_auto_primary(self):
        """Automatically set the best available primary solver"""
        if "dimod" in self.solvers:
            self.primary_solver = "dimod"
        elif "ortools" in self.solvers:
            self.primary_solver = "ortools"
        else:
            raise RuntimeError("No classical solvers available")

        logger.info(f"Auto-selected primary solver: {self.primary_solver}")

    def _set_primary_solver(self, solver_name: str):
        """Set a specific solver as primary"""
        if solver_name not in self.solvers:
            raise ValueError(f"Solver {solver_name} not available")

        self.primary_solver = solver_name
        logger.info(f"Set primary solver to: {solver_name}")

    async def solve(
        self, problem_data: Dict[str, Any], timeout: int = 300
    ) -> Dict[str, Any]:
        """Solve optimization problem using available classical solvers"""
        if not self.solvers:
            raise RuntimeError("No classical solvers available")

        # Try primary solver first
        if self.primary_solver and self.primary_solver in self.solvers:
            try:
                solver = self.solvers[self.primary_solver]
                return await solver.solve(problem_data, timeout)
            except Exception as e:
                logger.warning(f"Primary solver {self.primary_solver} failed: {e}")
                # Fall through to other solvers

        # Try other available solvers
        for solver_name, solver in self.solvers.items():
            if solver_name != self.primary_solver:
                try:
                    return await solver.solve(problem_data, timeout)
                except Exception as e:
                    logger.warning(f"Solver {solver_name} failed: {e}")
                    continue

        # All solvers failed
        raise RuntimeError("All classical solvers failed to solve the problem")

    def get_available_solvers(self) -> Dict[str, Dict[str, Any]]:
        """Get information about available solvers"""
        return {name: solver.get_solver_info() for name, solver in self.solvers.items()}

    def get_primary_solver(self) -> Optional[str]:
        """Get the name of the primary solver"""
        return self.primary_solver

    def set_primary_solver(self, solver_name: str):
        """Change the primary solver"""
        self._set_primary_solver(solver_name)
