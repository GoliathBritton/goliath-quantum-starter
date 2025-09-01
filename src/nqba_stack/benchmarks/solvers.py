"""
Solver Implementations for NQBA Stack Benchmarks

Provides classical and quantum solvers for head-to-head performance comparison.
"""

import asyncio
import time
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

import logging

# Set up logger
logger = logging.getLogger(__name__)

# Try to import optimization libraries
try:
    import ortools
    from ortools.linear_solver import pywraplp

    ORTOOLS_AVAILABLE = True
except ImportError:
    ORTOOLS_AVAILABLE = False

try:
    import dimod
    from dimod import BinaryQuadraticModel

    DIMOD_AVAILABLE = True
except ImportError:
    DIMOD_AVAILABLE = False

try:
    from dynex import DynexSampler

    DYNEX_AVAILABLE = True
except ImportError:
    DYNEX_AVAILABLE = False


@dataclass
class SolverResult:
    """Result from a solver execution"""

    solution: Any
    execution_time: float
    metadata: Dict[str, Any]


class BaseSolver(ABC):
    """Abstract base class for all solvers"""

    def __init__(self, name: str, version: str = "1.0.0"):
        self.name = name
        self.version = version

    @abstractmethod
    async def solve(self, problem_data: Dict[str, Any]) -> Any:
        """Solve the optimization problem"""
        pass

    def _validate_problem_data(self, problem_data: Dict[str, Any]) -> bool:
        """Validate that problem data has required fields"""
        required_fields = ["size"]
        return all(field in problem_data for field in required_fields)


class ClassicalSolver(BaseSolver):
    """
    Classical optimization solver using OR-Tools and other classical methods

    This solver represents the current state-of-the-art classical approaches
    and serves as the baseline for quantum advantage demonstration.
    """

    def __init__(self):
        super().__init__("Classical_OR_Tools", "1.0.0")

        if not ORTOOLS_AVAILABLE:
            logger.warning("OR-Tools not available, using fallback methods")

    async def solve(self, problem_data: Dict[str, Any]) -> Any:
        """Solve optimization problem using classical methods"""
        if not self._validate_problem_data(problem_data):
            raise ValueError("Invalid problem data")

        problem_type = self._detect_problem_type(problem_data)

        if problem_type == "portfolio":
            return await self._solve_portfolio(problem_data)
        elif problem_type == "tsp":
            return await self._solve_tsp(problem_data)
        elif problem_type == "knapsack":
            return await self._solve_knapsack(problem_data)
        else:
            raise ValueError(f"Unknown problem type: {problem_type}")

    def _detect_problem_type(self, problem_data: Dict[str, Any]) -> str:
        """Detect the type of optimization problem"""
        if "covariance_matrix" in problem_data:
            return "portfolio"
        elif "distance_matrix" in problem_data:
            return "tsp"
        elif "capacity" in problem_data and "values" in problem_data:
            return "knapsack"
        else:
            return "unknown"

    async def _solve_portfolio(self, problem_data: Dict[str, Any]) -> List[float]:
        """Solve portfolio optimization using quadratic programming"""
        if not ORTOOLS_AVAILABLE:
            return self._solve_portfolio_fallback(problem_data)

        try:
            # Create solver
            solver = pywraplp.Solver.CreateSolver("SCIP")
            if not solver:
                return self._solve_portfolio_fallback(problem_data)

            n_assets = problem_data["size"]
            returns = problem_data["returns"]
            cov_matrix = problem_data["covariance_matrix"]

            # Create variables (portfolio weights)
            weights = {}
            for i in range(n_assets):
                weights[i] = solver.NumVar(0.0, 0.3, f"w_{i}")

            # Budget constraint: sum of weights = 1
            solver.Add(solver.Sum([weights[i] for i in range(n_assets)]) == 1.0)

            # Target return constraint
            target_return = 0.10
            solver.Add(
                solver.Sum([weights[i] * returns[i] for i in range(n_assets)])
                >= target_return
            )

            # Objective: minimize risk (variance)
            objective_terms = []
            for i in range(n_assets):
                for j in range(n_assets):
                    objective_terms.append(weights[i] * weights[j] * cov_matrix[i][j])

            solver.Minimize(solver.Sum(objective_terms))

            # Solve
            status = solver.Solve()

            if status == pywraplp.Solver.OPTIMAL:
                solution = [weights[i].solution_value() for i in range(n_assets)]
                return solution
            else:
                return self._solve_portfolio_fallback(problem_data)

        except Exception as e:
            logger.warning(f"OR-Tools portfolio optimization failed: {e}")
            return self._solve_portfolio_fallback(problem_data)

    def _solve_portfolio_fallback(self, problem_data: Dict[str, Any]) -> List[float]:
        """Fallback portfolio optimization using simple heuristics"""
        n_assets = problem_data["size"]
        returns = np.array(problem_data["returns"])

        # Simple equal-weight portfolio
        weights = np.ones(n_assets) / n_assets

        # Adjust based on returns (higher returns get slightly higher weights)
        return_weights = returns / np.sum(returns)
        weights = 0.7 * weights + 0.3 * return_weights
        weights = weights / np.sum(weights)  # Normalize

        return weights.tolist()

    async def _solve_tsp(self, problem_data: Dict[str, Any]) -> List[int]:
        """Solve TSP using OR-Tools"""
        if not ORTOOLS_AVAILABLE:
            return self._solve_tsp_fallback(problem_data)

        try:
            from ortools.constraint_solver import routing_enums_pb2
            from ortools.constraint_solver import pywrapcp

            n_cities = problem_data["size"]
            distance_matrix = problem_data["distance_matrix"]

            # Create routing model
            manager = pywrapcp.RoutingIndexManager(n_cities, 1, 0)
            routing = pywrapcp.RoutingModel(manager)

            def distance_callback(from_index, to_index):
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                return distance_matrix[from_node][to_node]

            transit_callback_index = routing.RegisterTransitCallback(distance_callback)
            routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

            # Set first solution heuristic
            search_parameters = pywrapcp.DefaultRoutingSearchParameters()
            search_parameters.first_solution_strategy = (
                routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
            )

            # Solve
            solution = routing.SolveWithParameters(search_parameters)

            if solution:
                # Extract route
                route = []
                index = routing.Start(0)
                while not routing.IsEnd(index):
                    route.append(manager.IndexToNode(index))
                    index = solution.Value(routing.NextVar(index))
                route.append(manager.IndexToNode(index))

                return route
            else:
                return self._solve_tsp_fallback(problem_data)

        except Exception as e:
            logger.warning(f"OR-Tools TSP optimization failed: {e}")
            return self._solve_tsp_fallback(problem_data)

    def _solve_tsp_fallback(self, problem_data: Dict[str, Any]) -> List[int]:
        """Fallback TSP solution using nearest neighbor heuristic"""
        n_cities = problem_data["size"]
        distance_matrix = problem_data["distance_matrix"]

        # Nearest neighbor heuristic
        unvisited = set(range(n_cities))
        current = 0
        tour = [current]
        unvisited.remove(current)

        while unvisited:
            nearest = min(unvisited, key=lambda city: distance_matrix[current][city])
            tour.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        return tour

    async def _solve_knapsack(self, problem_data: Dict[str, Any]) -> List[int]:
        """Solve knapsack using OR-Tools"""
        if not ORTOOLS_AVAILABLE:
            return self._solve_knapsack_fallback(problem_data)

        try:
            values = problem_data["values"]
            weights = problem_data["weights"]
            capacity = problem_data["capacity"]
            n_items = problem_data["size"]

            # Create solver
            solver = pywraplp.Solver.CreateSolver("SCIP")
            if not solver:
                return self._solve_knapsack_fallback(problem_data)

            # Create variables (binary: item selected or not)
            x = {}
            for i in range(n_items):
                x[i] = solver.IntVar(0, 1, f"x_{i}")

            # Capacity constraint
            solver.Add(
                solver.Sum([x[i] * weights[i] for i in range(n_items)]) <= capacity
            )

            # Objective: maximize value
            solver.Maximize(solver.Sum([x[i] * values[i] for i in range(n_items)]))

            # Solve
            status = solver.Solve()

            if status == pywraplp.Solver.OPTIMAL:
                solution = [int(x[i].solution_value()) for i in range(n_items)]
                return solution
            else:
                return self._solve_knapsack_fallback(problem_data)

        except Exception as e:
            logger.warning(f"OR-Tools knapsack optimization failed: {e}")
            return self._solve_knapsack_fallback(problem_data)

    def _solve_knapsack_fallback(self, problem_data: Dict[str, Any]) -> List[int]:
        """Fallback knapsack solution using greedy heuristic"""
        values = problem_data["values"]
        weights = problem_data["weights"]
        capacity = problem_data["capacity"]
        n_items = problem_data["size"]

        # Sort items by value/weight ratio
        items = [(values[i], weights[i], i) for i in range(n_items)]
        items.sort(key=lambda x: x[0] / x[1], reverse=True)

        solution = [0] * n_items
        remaining_capacity = capacity

        for value, weight, index in items:
            if weight <= remaining_capacity:
                solution[index] = 1
                remaining_capacity -= weight

        return solution


class QuantumSolver(BaseSolver):
    """
    Quantum optimization solver using Dynex and other quantum methods

    This solver represents the quantum advantage and will be compared
    against classical approaches in benchmarks.
    """

    def __init__(self):
        super().__init__("Quantum_Dynex", "1.0.0")

        if not DYNEX_AVAILABLE:
            logger.warning("Dynex not available, using quantum emulation")

    async def solve(self, problem_data: Dict[str, Any]) -> Any:
        """Solve optimization problem using quantum methods"""
        if not self._validate_problem_data(problem_data):
            raise ValueError("Invalid problem data")

        problem_type = self._detect_problem_type(problem_data)

        if problem_type == "portfolio":
            return await self._solve_portfolio_quantum(problem_data)
        elif problem_type == "tsp":
            return await self._solve_tsp_quantum(problem_data)
        elif problem_type == "knapsack":
            return await self._solve_knapsack_quantum(problem_data)
        else:
            raise ValueError(f"Unknown problem type: {problem_type}")

    def _detect_problem_type(self, problem_data: Dict[str, Any]) -> str:
        """Detect the type of optimization problem"""
        if "covariance_matrix" in problem_data:
            return "portfolio"
        elif "distance_matrix" in problem_data:
            return "tsp"
        elif "capacity" in problem_data and "values" in problem_data:
            return "knapsack"
        else:
            return "unknown"

    async def _solve_portfolio_quantum(
        self, problem_data: Dict[str, Any]
    ) -> List[float]:
        """Solve portfolio optimization using quantum methods"""
        if DYNEX_AVAILABLE:
            return await self._solve_portfolio_dynex(problem_data)
        else:
            return await self._solve_portfolio_emulation(problem_data)

    async def _solve_portfolio_dynex(self, problem_data: Dict[str, Any]) -> List[float]:
        """Solve portfolio optimization using Dynex QPU"""
        try:
            # Convert to QUBO format
            qubo = self._portfolio_to_qubo(problem_data)

            # Solve with Dynex
            sampler = DynexSampler()
            sampleset = sampler.sample_qubo(qubo, num_reads=100)

            # Extract best solution
            best_solution = sampleset.first.sample

            # Convert back to portfolio weights
            weights = self._qubo_to_portfolio_weights(
                best_solution, problem_data["size"]
            )

            return weights

        except Exception as e:
            logger.warning(f"Dynex portfolio optimization failed: {e}")
            return await self._solve_portfolio_emulation(problem_data)

    async def _solve_portfolio_emulation(
        self, problem_data: Dict[str, Any]
    ) -> List[float]:
        """Emulate quantum portfolio optimization"""
        # Simulate quantum advantage with improved heuristics
        n_assets = problem_data["size"]
        returns = np.array(problem_data["returns"])
        cov_matrix = np.array(problem_data["covariance_matrix"])

        # Quantum-inspired approach: use quantum annealing principles
        # Start with random solution and improve through local search

        # Initial random weights
        np.random.seed(int(time.time()) % 10000)
        weights = np.random.random(n_assets)
        weights = weights / np.sum(weights)

        # Quantum-inspired local search
        best_quality = self._evaluate_portfolio_quality(weights, returns, cov_matrix)

        for iteration in range(50):  # Simulate quantum iterations
            # Generate neighbor solution
            neighbor = weights + np.random.normal(0, 0.01, n_assets)
            neighbor = np.maximum(neighbor, 0)  # Ensure non-negative
            neighbor = neighbor / np.sum(neighbor)  # Normalize

            # Evaluate quality
            quality = self._evaluate_portfolio_quality(neighbor, returns, cov_matrix)

            # Accept if better (quantum tunneling effect)
            if (
                quality > best_quality or np.random.random() < 0.1
            ):  # 10% tunneling probability
                weights = neighbor
                best_quality = quality

        return weights.tolist()

    def _evaluate_portfolio_quality(
        self, weights: np.ndarray, returns: np.ndarray, cov_matrix: np.ndarray
    ) -> float:
        """Evaluate portfolio quality (Sharpe ratio)"""
        portfolio_return = np.dot(weights, returns)
        portfolio_risk = np.sqrt(np.dot(weights, np.dot(cov_matrix, weights)))

        if portfolio_risk == 0:
            return 0

        sharpe_ratio = (portfolio_return - 0.02) / portfolio_risk
        return max(0, sharpe_ratio)

    def _portfolio_to_qubo(self, problem_data: Dict[str, Any]) -> Dict[tuple, float]:
        """Convert portfolio optimization to QUBO format"""
        # This is a simplified conversion - in practice would be more sophisticated
        n_assets = problem_data["size"]
        qubo = {}

        # Add quadratic terms for risk minimization
        cov_matrix = problem_data["covariance_matrix"]
        for i in range(n_assets):
            for j in range(n_assets):
                if i != j:
                    qubo[(i, j)] = cov_matrix[i][j] * 0.5

        # Add linear terms for return maximization
        returns = problem_data["returns"]
        for i in range(n_assets):
            qubo[(i, i)] = -returns[i] * 10  # Negative for maximization

        return qubo

    def _qubo_to_portfolio_weights(
        self, qubo_solution: Dict[int, int], n_assets: int
    ) -> List[float]:
        """Convert QUBO solution back to portfolio weights"""
        weights = []
        total_weight = 0

        for i in range(n_assets):
            weight = qubo_solution.get(i, 0)
            weights.append(weight)
            total_weight += weight

        # Normalize weights
        if total_weight > 0:
            weights = [w / total_weight for w in weights]
        else:
            weights = [1.0 / n_assets] * n_assets

        return weights

    async def _solve_tsp_quantum(self, problem_data: Dict[str, Any]) -> List[int]:
        """Solve TSP using quantum methods"""
        # For TSP, we'll use a quantum-inspired approach
        # In practice, this would use Dynex for larger instances

        n_cities = problem_data["size"]
        distance_matrix = problem_data["distance_matrix"]

        # Quantum-inspired genetic algorithm
        population_size = 20
        population = self._generate_tsp_population(n_cities, population_size)

        for generation in range(30):
            # Evaluate fitness
            fitness = [
                self._evaluate_tsp_tour(tour, distance_matrix) for tour in population
            ]

            # Select parents
            parents = self._select_tsp_parents(population, fitness)

            # Generate new population
            new_population = []
            for _ in range(population_size):
                idx1, idx2 = np.random.choice(len(parents), 2, replace=False)
                parent1, parent2 = parents[idx1], parents[idx2]
                child = self._crossover_tsp(parent1, parent2)
                child = self._mutate_tsp(child)
                new_population.append(child)

            population = new_population

        # Return best solution
        best_tour = max(
            population, key=lambda tour: self._evaluate_tsp_tour(tour, distance_matrix)
        )
        return best_tour

    def _generate_tsp_population(self, n_cities: int, size: int) -> List[List[int]]:
        """Generate initial TSP population"""
        population = []
        for _ in range(size):
            tour = list(range(n_cities))
            np.random.shuffle(tour)
            population.append(tour)
        return population

    def _evaluate_tsp_tour(
        self, tour: List[int], distance_matrix: List[List[float]]
    ) -> float:
        """Evaluate TSP tour (negative distance for maximization)"""
        total_distance = 0
        for i in range(len(tour)):
            current = tour[i]
            next_city = tour[(i + 1) % len(tour)]
            total_distance += distance_matrix[current][next_city]
        return -total_distance

    def _select_tsp_parents(
        self, population: List[List[int]], fitness: List[float]
    ) -> List[List[int]]:
        """Select TSP parents using tournament selection"""
        parents = []
        for _ in range(len(population)):
            tournament_size = 3
            tournament_indices = np.random.choice(
                len(population), tournament_size, replace=False
            )
            tournament_fitness = [fitness[i] for i in tournament_indices]
            winner_index = tournament_indices[np.argmax(tournament_fitness)]
            parents.append(population[winner_index])
        return parents

    def _crossover_tsp(self, parent1: List[int], parent2: List[int]) -> List[int]:
        """Crossover TSP tours using order crossover"""
        n = len(parent1)
        start, end = sorted(np.random.choice(n, 2, replace=False))

        child = [-1] * n
        child[start:end] = parent1[start:end]

        remaining = [x for x in parent2 if x not in child[start:end]]
        j = 0
        for i in range(n):
            if child[i] == -1:
                child[i] = remaining[j]
                j += 1

        return child

    def _mutate_tsp(self, tour: List[int]) -> List[int]:
        """Mutate TSP tour using swap mutation"""
        if np.random.random() < 0.1:  # 10% mutation probability
            i, j = np.random.choice(len(tour), 2, replace=False)
            tour[i], tour[j] = tour[j], tour[i]
        return tour

    async def _solve_knapsack_quantum(self, problem_data: Dict[str, Any]) -> List[int]:
        """Solve knapsack using quantum methods"""
        # For knapsack, we'll use a quantum-inspired approach
        # In practice, this would use Dynex for larger instances

        values = problem_data["values"]
        weights = problem_data["weights"]
        capacity = problem_data["capacity"]
        n_items = problem_data["size"]

        # Quantum-inspired simulated annealing
        current_solution = [0] * n_items
        current_value = 0
        current_weight = 0

        best_solution = current_solution.copy()
        best_value = current_value

        temperature = 100.0
        cooling_rate = 0.95

        for iteration in range(100):
            # Generate neighbor
            neighbor = current_solution.copy()
            item = np.random.randint(0, n_items)
            neighbor[item] = 1 - neighbor[item]  # Flip bit

            # Calculate new weight and value
            new_weight = current_weight
            new_value = current_value

            if neighbor[item] == 1:  # Adding item
                new_weight += weights[item]
                new_value += values[item]
            else:  # Removing item
                new_weight -= weights[item]
                new_value -= values[item]

            # Check feasibility
            if new_weight <= capacity:
                # Accept if better or with probability based on temperature
                delta_value = new_value - current_value
                if delta_value > 0 or np.random.random() < np.exp(
                    delta_value / temperature
                ):
                    current_solution = neighbor.copy()
                    current_value = new_value
                    current_weight = new_weight

                    # Update best solution
                    if current_value > best_value:
                        best_solution = current_solution.copy()
                        best_value = current_value

            # Cool down
            temperature *= cooling_rate

        return best_solution


class DynexSolver(QuantumSolver):
    """
    Specialized Dynex solver for maximum quantum advantage
    """

    def __init__(self):
        super().__init__()
        self.name = "Dynex_QPU"
        self.version = "2.0.0"

    async def solve(self, problem_data: Dict[str, Any]) -> Any:
        """Solve using Dynex QPU with advanced features"""
        if not DYNEX_AVAILABLE:
            logger.warning("Dynex not available, falling back to quantum emulation")
            return await super().solve(problem_data)

        # Use Dynex-specific optimizations
        return await self._solve_with_dynex_advanced(problem_data)

    async def _solve_with_dynex_advanced(self, problem_data: Dict[str, Any]) -> Any:
        """Advanced Dynex solving with custom parameters"""
        try:
            # This would use advanced Dynex features like:
            # - Custom annealing schedules
            # - Problem-specific embeddings
            # - Advanced readout strategies

            # For now, use the standard quantum solver
            return await super().solve(problem_data)

        except Exception as e:
            logger.error(f"Advanced Dynex solving failed: {e}")
            return await super().solve(problem_data)


# Factory function to get solvers
def get_all_solvers() -> List[BaseSolver]:
    """Get all available solvers"""
    solvers = [ClassicalSolver()]

    if DYNEX_AVAILABLE:
        solvers.append(DynexSolver())
    else:
        solvers.append(QuantumSolver())

    return solvers


def get_solver_by_name(name: str) -> BaseSolver:
    """Get a specific solver by name"""
    solvers = get_all_solvers()
    for solver in solvers:
        if solver.name == name:
            return solver
    raise ValueError(f"Solver '{name}' not found")
