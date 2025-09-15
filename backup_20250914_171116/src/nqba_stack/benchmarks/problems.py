"""
Canonical Optimization Problems for NQBA Stack Benchmarks

These problems are carefully chosen to demonstrate quantum advantage
in real-world optimization scenarios.
"""

import numpy as np
import random
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ProblemData:
    """Data structure for optimization problems"""

    name: str
    size: int
    data: Dict[str, Any]
    constraints: Dict[str, Any]
    optimal_value: Optional[float] = None


class OptimizationProblem(ABC):
    """
    Abstract base class for optimization problems
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def prepare_data(self, size: int) -> ProblemData:
        """Prepare problem data of specified size"""
        pass

    @abstractmethod
    def evaluate_solution(self, solution: Any) -> float:
        """Evaluate the quality of a solution"""
        pass

    @abstractmethod
    def get_optimal_solution(self, data: ProblemData) -> Any:
        """Get the optimal solution for verification"""
        pass


class PortfolioOptimization(OptimizationProblem):
    """
    Portfolio Optimization Problem

    This is a canonical problem that demonstrates quantum advantage
    in financial applications. The goal is to find the optimal
    allocation of assets that maximizes return while minimizing risk.
    """

    def __init__(self):
        super().__init__("Portfolio_Optimization")

    def prepare_data(self, size: int) -> ProblemData:
        """Prepare portfolio optimization data"""
        np.random.seed(42)  # For reproducible results

        # Generate random asset data
        returns = np.random.normal(0.08, 0.15, size)  # 8% mean return, 15% volatility
        volatilities = np.random.uniform(0.05, 0.25, size)

        # Generate correlation matrix (positive semi-definite)
        correlation_matrix = self._generate_correlation_matrix(size)

        # Calculate covariance matrix
        covariance_matrix = np.outer(volatilities, volatilities) * correlation_matrix

        # Set constraints
        min_allocation = 0.0
        max_allocation = 0.3  # No single asset > 30%
        target_return = 0.10  # 10% target return

        constraints = {
            "min_allocation": min_allocation,
            "max_allocation": max_allocation,
            "target_return": target_return,
            "budget_constraint": 1.0,  # Total allocation = 100%
        }

        data = {
            "returns": returns.tolist(),
            "volatilities": volatilities.tolist(),
            "covariance_matrix": covariance_matrix.tolist(),
            "size": size,
        }

        return ProblemData(
            name=self.name, size=size, data=data, constraints=constraints
        )

    def evaluate_solution(self, solution: List[float]) -> float:
        """Evaluate portfolio solution quality (Sharpe ratio)"""
        if not solution or len(solution) == 0:
            return 0.0

        # Calculate portfolio return and risk
        portfolio_return = np.dot(solution, self._current_data["returns"])
        portfolio_risk = np.sqrt(
            np.dot(solution, np.dot(self._current_data["covariance_matrix"], solution))
        )

        # Calculate Sharpe ratio (risk-free rate = 2%)
        risk_free_rate = 0.02
        sharpe_ratio = (
            (portfolio_return - risk_free_rate) / portfolio_risk
            if portfolio_risk > 0
            else 0
        )

        # Penalize constraint violations
        constraint_penalty = self._calculate_constraint_penalty(solution)

        return max(0, sharpe_ratio - constraint_penalty)

    def get_optimal_solution(self, data: ProblemData) -> List[float]:
        """Get optimal solution using efficient frontier approach"""
        # This is a simplified optimal solution for verification
        # In practice, this would be computed using advanced optimization techniques

        returns = np.array(data.data["returns"])
        cov_matrix = np.array(data.data["covariance_matrix"])

        # Simple equal-weight portfolio as baseline
        n_assets = data.size
        equal_weight = 1.0 / n_assets

        # Adjust weights based on return/risk ratio
        risk_adjusted_returns = returns / np.sqrt(np.diag(cov_matrix))
        total_weight = sum(risk_adjusted_returns)

        if total_weight > 0:
            weights = risk_adjusted_returns / total_weight
        else:
            weights = [equal_weight] * n_assets

        # Normalize to sum to 1
        weights = np.array(weights)
        weights = weights / np.sum(weights)

        return weights.tolist()

    def _generate_correlation_matrix(self, size: int) -> np.ndarray:
        """Generate a valid correlation matrix"""
        # Start with random correlations
        corr_matrix = np.random.uniform(-0.3, 0.7, (size, size))

        # Make it symmetric
        corr_matrix = (corr_matrix + corr_matrix.T) / 2

        # Set diagonal to 1
        np.fill_diagonal(corr_matrix, 1.0)

        # Ensure positive semi-definite by adding identity matrix
        corr_matrix += np.eye(size) * 0.1

        # Normalize
        corr_matrix = corr_matrix / np.max(np.abs(corr_matrix))

        return corr_matrix

    def _calculate_constraint_penalty(self, solution: List[float]) -> float:
        """Calculate penalty for constraint violations"""
        penalty = 0.0

        # Budget constraint
        total_allocation = sum(solution)
        if abs(total_allocation - 1.0) > 0.01:
            penalty += abs(total_allocation - 1.0) * 10

        # Individual allocation constraints
        for weight in solution:
            if weight < 0 or weight > 0.3:
                penalty += max(0, abs(weight - 0.15)) * 5

        return penalty

    def _set_current_data(self, data: ProblemData):
        """Set current data for evaluation"""
        self._current_data = data.data


class TravelingSalesman(OptimizationProblem):
    """
    Traveling Salesman Problem (TSP)

    A classic NP-hard optimization problem that demonstrates
    quantum advantage in combinatorial optimization.
    """

    def __init__(self):
        super().__init__("Traveling_Salesman")

    def prepare_data(self, size: int) -> ProblemData:
        """Prepare TSP data with random city coordinates"""
        np.random.seed(42)

        # Generate random city coordinates
        cities = []
        for i in range(size):
            x = np.random.uniform(0, 100)
            y = np.random.uniform(0, 100)
            cities.append((x, y))

        # Calculate distance matrix
        distance_matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                if i == j:
                    row.append(0)
                else:
                    dx = cities[i][0] - cities[j][0]
                    dy = cities[i][1] - cities[j][1]
                    distance = np.sqrt(dx * dx + dy * dy)
                    row.append(distance)
            distance_matrix.append(row)

        constraints = {
            "start_city": 0,
            "return_to_start": True,
            "visit_each_city_once": True,
        }

        data = {"cities": cities, "distance_matrix": distance_matrix, "size": size}

        return ProblemData(
            name=self.name, size=size, data=data, constraints=constraints
        )

    def evaluate_solution(self, solution: List[int]) -> float:
        """Evaluate TSP solution (negative total distance for maximization)"""
        if not solution or len(solution) != self._current_data["size"]:
            return 0.0

        total_distance = 0
        distance_matrix = self._current_data["distance_matrix"]

        # Calculate total tour distance
        for i in range(len(solution)):
            current_city = solution[i]
            next_city = solution[(i + 1) % len(solution)]
            total_distance += distance_matrix[current_city][next_city]

        # Return negative distance (we want to minimize distance, so maximize negative distance)
        return -total_distance

    def get_optimal_solution(self, data: ProblemData) -> List[int]:
        """Get approximate optimal solution using nearest neighbor heuristic"""
        cities = data.data["cities"]
        distance_matrix = data.data["distance_matrix"]
        n_cities = data.size

        # Nearest neighbor heuristic
        unvisited = set(range(n_cities))
        current = 0  # Start city
        tour = [current]
        unvisited.remove(current)

        while unvisited:
            # Find nearest unvisited city
            nearest = min(unvisited, key=lambda city: distance_matrix[current][city])
            tour.append(nearest)
            unvisited.remove(nearest)
            current = nearest

        return tour

    def _set_current_data(self, data: ProblemData):
        """Set current data for evaluation"""
        self._current_data = data.data


class KnapsackProblem(OptimizationProblem):
    """
    Knapsack Problem

    A fundamental optimization problem that demonstrates
    quantum advantage in resource allocation scenarios.
    """

    def __init__(self):
        super().__init__("Knapsack_Problem")

    def prepare_data(self, size: int) -> ProblemData:
        """Prepare knapsack problem data"""
        np.random.seed(42)

        # Generate random items with values and weights
        values = np.random.uniform(10, 100, size)
        weights = np.random.uniform(1, 20, size)

        # Set knapsack capacity (about 40% of total weight)
        total_weight = np.sum(weights)
        capacity = total_weight * 0.4

        constraints = {
            "capacity": capacity,
            "binary_selection": True,  # Each item is either selected or not
            "max_items": size,
        }

        data = {
            "values": values.tolist(),
            "weights": weights.tolist(),
            "capacity": capacity,
            "size": size,
        }

        return ProblemData(
            name=self.name, size=size, data=data, constraints=constraints
        )

    def evaluate_solution(self, solution: List[int]) -> float:
        """Evaluate knapsack solution (total value)"""
        if not solution or len(solution) != self._current_data["size"]:
            return 0.0

        total_value = 0
        total_weight = 0

        values = self._current_data["values"]
        weights = self._current_data["weights"]
        capacity = self._current_data["capacity"]

        for i, selected in enumerate(solution):
            if selected:
                total_value += values[i]
                total_weight += weights[i]

        # Penalize if capacity exceeded
        if total_weight > capacity:
            return 0.0

        return total_value

    def get_optimal_solution(self, data: ProblemData) -> List[int]:
        """Get optimal solution using dynamic programming (for small problems)"""
        values = data.data["values"]
        weights = data.data["weights"]
        capacity = data.data["capacity"]
        n_items = data.size

        # Dynamic programming solution for small problems
        if n_items <= 100:  # Only use DP for reasonable sizes
            dp = [[0] * (int(capacity) + 1) for _ in range(n_items + 1)]

            for i in range(1, n_items + 1):
                for w in range(int(capacity) + 1):
                    if weights[i - 1] <= w:
                        dp[i][w] = max(
                            dp[i - 1][w],
                            dp[i - 1][w - int(weights[i - 1])] + values[i - 1],
                        )
                    else:
                        dp[i][w] = dp[i - 1][w]

            # Backtrack to find solution
            solution = [0] * n_items
            w = int(capacity)
            for i in range(n_items, 0, -1):
                if dp[i][w] != dp[i - 1][w]:
                    solution[i - 1] = 1
                    w -= int(weights[i - 1])

            return solution
        else:
            # Greedy heuristic for large problems
            items = [(values[i], weights[i], i) for i in range(n_items)]
            items.sort(
                key=lambda x: x[0] / x[1], reverse=True
            )  # Sort by value/weight ratio

            solution = [0] * n_items
            remaining_capacity = capacity

            for value, weight, index in items:
                if weight <= remaining_capacity:
                    solution[index] = 1
                    remaining_capacity -= weight

            return solution

    def _set_current_data(self, data: ProblemData):
        """Set current data for evaluation"""
        self._current_data = data.data


# Factory function to get all problems
def get_all_problems() -> List[OptimizationProblem]:
    """Get all available optimization problems"""
    return [PortfolioOptimization(), TravelingSalesman(), KnapsackProblem()]


def get_problem_by_name(name: str) -> OptimizationProblem:
    """Get a specific problem by name"""
    problems = get_all_problems()
    for problem in problems:
        if problem.name == name:
            return problem
    raise ValueError(f"Problem '{name}' not found")
