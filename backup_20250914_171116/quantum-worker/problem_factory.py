import numpy as np
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import json

try:
    import networkx as nx
except ImportError:
    nx = None
    logging.warning("NetworkX not available. Graph-based problems will use fallback implementations.")

try:
    import pandas as pd
except ImportError:
    pd = None

@dataclass
class ProblemInstance:
    problem_type: str
    qubo_matrix: Dict[Tuple[int, int], float]
    metadata: Dict[str, Any]
    num_variables: int
    description: str
    created_at: datetime
    
class ProblemFactory:
    """
    Factory class for generating various optimization problems in QUBO format.
    Supports portfolio optimization, TSP, max cut, job scheduling, and more.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("ProblemFactory initialized")
    
    def create_portfolio_optimization(self, 
                                    returns: List[float],
                                    covariance_matrix: List[List[float]],
                                    risk_aversion: float = 1.0,
                                    budget_constraint: float = 1.0,
                                    min_assets: int = 1,
                                    max_assets: Optional[int] = None) -> ProblemInstance:
        """
        Create a portfolio optimization problem in QUBO format.
        
        Args:
            returns: Expected returns for each asset
            covariance_matrix: Covariance matrix of asset returns
            risk_aversion: Risk aversion parameter (higher = more risk averse)
            budget_constraint: Total budget constraint
            min_assets: Minimum number of assets to select
            max_assets: Maximum number of assets to select
        
        Returns:
            ProblemInstance with QUBO formulation
        """
        try:
            n_assets = len(returns)
            returns = np.array(returns)
            cov_matrix = np.array(covariance_matrix)
            
            if max_assets is None:
                max_assets = n_assets
            
            # QUBO formulation: minimize risk - expected_return + constraints
            # Variables: x_i = 1 if asset i is selected, 0 otherwise
            
            qubo = {}
            
            # Objective: minimize risk (quadratic term) - maximize return (linear term)
            for i in range(n_assets):
                for j in range(n_assets):
                    if i == j:
                        # Diagonal terms: risk penalty - expected return
                        qubo[(i, i)] = risk_aversion * cov_matrix[i, i] - returns[i]
                    else:
                        # Off-diagonal terms: covariance
                        qubo[(i, j)] = risk_aversion * cov_matrix[i, j]
            
            # Budget constraint penalty
            budget_penalty = 10.0  # Penalty weight for violating budget constraint
            
            # Add budget constraint: (sum(x_i) - budget)^2
            for i in range(n_assets):
                qubo[(i, i)] += budget_penalty * (1 - 2 * budget_constraint)
                for j in range(i + 1, n_assets):
                    if (i, j) not in qubo:
                        qubo[(i, j)] = 0
                    qubo[(i, j)] += 2 * budget_penalty
            
            # Minimum assets constraint
            if min_assets > 0:
                min_penalty = 5.0
                for i in range(n_assets):
                    qubo[(i, i)] += min_penalty * (2 * min_assets - 1)
                    for j in range(i + 1, n_assets):
                        if (i, j) not in qubo:
                            qubo[(i, j)] = 0
                        qubo[(i, j)] -= 2 * min_penalty
            
            # Maximum assets constraint
            if max_assets < n_assets:
                max_penalty = 5.0
                for i in range(n_assets):
                    qubo[(i, i)] += max_penalty * (1 - 2 * max_assets)
                    for j in range(i + 1, n_assets):
                        if (i, j) not in qubo:
                            qubo[(i, j)] = 0
                        qubo[(i, j)] += 2 * max_penalty
            
            metadata = {
                'n_assets': n_assets,
                'expected_returns': returns.tolist(),
                'risk_aversion': risk_aversion,
                'budget_constraint': budget_constraint,
                'min_assets': min_assets,
                'max_assets': max_assets,
                'covariance_matrix_shape': cov_matrix.shape
            }
            
            return ProblemInstance(
                problem_type='portfolio_optimization',
                qubo_matrix=qubo,
                metadata=metadata,
                num_variables=n_assets,
                description=f"Portfolio optimization with {n_assets} assets",
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create portfolio optimization problem: {e}")
            raise
    
    def create_tsp_problem(self, 
                          distance_matrix: List[List[float]],
                          start_city: int = 0) -> ProblemInstance:
        """
        Create a Traveling Salesman Problem in QUBO format.
        
        Args:
            distance_matrix: Matrix of distances between cities
            start_city: Starting city index
        
        Returns:
            ProblemInstance with QUBO formulation
        """
        try:
            n_cities = len(distance_matrix)
            distances = np.array(distance_matrix)
            
            # Variables: x_{i,t} = 1 if city i is visited at time t
            # Total variables: n_cities * n_cities
            
            def var_index(city: int, time: int) -> int:
                return city * n_cities + time
            
            qubo = {}
            
            # Objective: minimize total distance
            for t in range(n_cities):
                for i in range(n_cities):
                    for j in range(n_cities):
                        if i != j:
                            next_t = (t + 1) % n_cities
                            var_i = var_index(i, t)
                            var_j = var_index(j, next_t)
                            
                            if (var_i, var_j) not in qubo:
                                qubo[(var_i, var_j)] = 0
                            qubo[(var_i, var_j)] += distances[i, j]
            
            # Constraint 1: Each city visited exactly once
            penalty_1 = max(np.max(distances) * n_cities, 100)
            for i in range(n_cities):
                for t1 in range(n_cities):
                    var1 = var_index(i, t1)
                    qubo[(var1, var1)] = qubo.get((var1, var1), 0) + penalty_1 * (1 - 2)
                    
                    for t2 in range(t1 + 1, n_cities):
                        var2 = var_index(i, t2)
                        if (var1, var2) not in qubo:
                            qubo[(var1, var2)] = 0
                        qubo[(var1, var2)] += 2 * penalty_1
            
            # Constraint 2: Each time slot has exactly one city
            penalty_2 = max(np.max(distances) * n_cities, 100)
            for t in range(n_cities):
                for i1 in range(n_cities):
                    var1 = var_index(i1, t)
                    qubo[(var1, var1)] = qubo.get((var1, var1), 0) + penalty_2 * (1 - 2)
                    
                    for i2 in range(i1 + 1, n_cities):
                        var2 = var_index(i2, t)
                        if (var1, var2) not in qubo:
                            qubo[(var1, var2)] = 0
                        qubo[(var1, var2)] += 2 * penalty_2
            
            # Fix starting city
            start_var = var_index(start_city, 0)
            qubo[(start_var, start_var)] = qubo.get((start_var, start_var), 0) - 1000
            
            metadata = {
                'n_cities': n_cities,
                'start_city': start_city,
                'distance_matrix_shape': distances.shape,
                'max_distance': float(np.max(distances)),
                'min_distance': float(np.min(distances[distances > 0]))
            }
            
            return ProblemInstance(
                problem_type='tsp',
                qubo_matrix=qubo,
                metadata=metadata,
                num_variables=n_cities * n_cities,
                description=f"TSP with {n_cities} cities",
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create TSP problem: {e}")
            raise
    
    def create_max_cut_problem(self, 
                              adjacency_matrix: List[List[float]],
                              edge_weights: Optional[Dict[Tuple[int, int], float]] = None) -> ProblemInstance:
        """
        Create a Maximum Cut problem in QUBO format.
        
        Args:
            adjacency_matrix: Adjacency matrix of the graph
            edge_weights: Optional edge weights (if None, uses adjacency matrix values)
        
        Returns:
            ProblemInstance with QUBO formulation
        """
        try:
            adj_matrix = np.array(adjacency_matrix)
            n_nodes = adj_matrix.shape[0]
            
            # Variables: x_i = 1 if node i is in set S, 0 if in set T
            # Objective: maximize cut size = sum of weights of edges between S and T
            
            qubo = {}
            
            # For max cut: maximize sum_{(i,j) in E} w_{ij} * (x_i + x_j - 2*x_i*x_j)
            # Convert to minimization: minimize -sum_{(i,j) in E} w_{ij} * (x_i + x_j - 2*x_i*x_j)
            
            for i in range(n_nodes):
                for j in range(i + 1, n_nodes):
                    if adj_matrix[i, j] != 0:
                        weight = edge_weights.get((i, j), adj_matrix[i, j]) if edge_weights else adj_matrix[i, j]
                        
                        # Linear terms: -w_{ij} * (x_i + x_j)
                        qubo[(i, i)] = qubo.get((i, i), 0) - weight
                        qubo[(j, j)] = qubo.get((j, j), 0) - weight
                        
                        # Quadratic term: +2*w_{ij} * x_i * x_j
                        qubo[(i, j)] = qubo.get((i, j), 0) + 2 * weight
            
            # Calculate some graph properties for metadata
            total_edges = np.count_nonzero(adj_matrix) // 2  # Undirected graph
            total_weight = np.sum(adj_matrix) / 2
            
            metadata = {
                'n_nodes': n_nodes,
                'n_edges': total_edges,
                'total_weight': float(total_weight),
                'graph_density': total_edges / (n_nodes * (n_nodes - 1) / 2) if n_nodes > 1 else 0,
                'has_edge_weights': edge_weights is not None
            }
            
            return ProblemInstance(
                problem_type='max_cut',
                qubo_matrix=qubo,
                metadata=metadata,
                num_variables=n_nodes,
                description=f"Max Cut problem with {n_nodes} nodes and {total_edges} edges",
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create Max Cut problem: {e}")
            raise
    
    def create_job_scheduling_problem(self,
                                    jobs: List[Dict[str, Any]],
                                    machines: List[Dict[str, Any]],
                                    time_horizon: int) -> ProblemInstance:
        """
        Create a job scheduling problem in QUBO format.
        
        Args:
            jobs: List of job dictionaries with 'duration', 'deadline', 'priority'
            machines: List of machine dictionaries with 'capacity', 'cost_per_hour'
            time_horizon: Maximum time horizon for scheduling
        
        Returns:
            ProblemInstance with QUBO formulation
        """
        try:
            n_jobs = len(jobs)
            n_machines = len(machines)
            
            # Variables: x_{j,m,t} = 1 if job j starts on machine m at time t
            def var_index(job: int, machine: int, time: int) -> int:
                return job * n_machines * time_horizon + machine * time_horizon + time
            
            qubo = {}
            
            # Objective: minimize cost + deadline violations + priority weights
            for j, job in enumerate(jobs):
                duration = job['duration']
                deadline = job.get('deadline', time_horizon)
                priority = job.get('priority', 1.0)
                
                for m, machine in enumerate(machines):
                    cost_per_hour = machine.get('cost_per_hour', 1.0)
                    
                    for t in range(time_horizon - duration + 1):
                        var = var_index(j, m, t)
                        
                        # Cost component
                        cost = cost_per_hour * duration
                        qubo[(var, var)] = qubo.get((var, var), 0) + cost
                        
                        # Deadline violation penalty
                        completion_time = t + duration
                        if completion_time > deadline:
                            penalty = 100 * priority * (completion_time - deadline)
                            qubo[(var, var)] = qubo.get((var, var), 0) + penalty
                        
                        # Priority bonus (negative cost for high priority jobs)
                        qubo[(var, var)] = qubo.get((var, var), 0) - priority
            
            # Constraint 1: Each job assigned to exactly one machine at one time
            penalty_1 = 1000
            for j in range(n_jobs):
                variables = []
                for m in range(n_machines):
                    for t in range(time_horizon - jobs[j]['duration'] + 1):
                        variables.append(var_index(j, m, t))
                
                # Add constraint: sum(variables) = 1
                for i, var1 in enumerate(variables):
                    qubo[(var1, var1)] = qubo.get((var1, var1), 0) + penalty_1 * (1 - 2)
                    for j_var, var2 in enumerate(variables[i + 1:], i + 1):
                        if (var1, var2) not in qubo:
                            qubo[(var1, var2)] = 0
                        qubo[(var1, var2)] += 2 * penalty_1
            
            # Constraint 2: Machine capacity constraints
            penalty_2 = 500
            for m, machine in enumerate(machines):
                capacity = machine.get('capacity', 1)
                
                for t in range(time_horizon):
                    # Find all jobs that could be running on machine m at time t
                    running_jobs = []
                    for j, job in enumerate(jobs):
                        duration = job['duration']
                        for start_t in range(max(0, t - duration + 1), min(t + 1, time_horizon - duration + 1)):
                            if start_t + duration > t:
                                running_jobs.append(var_index(j, m, start_t))
                    
                    # Add capacity constraint if more than capacity jobs could run
                    if len(running_jobs) > capacity:
                        for i, var1 in enumerate(running_jobs):
                            for j_var, var2 in enumerate(running_jobs[i + 1:], i + 1):
                                if (var1, var2) not in qubo:
                                    qubo[(var1, var2)] = 0
                                qubo[(var1, var2)] += penalty_2
            
            metadata = {
                'n_jobs': n_jobs,
                'n_machines': n_machines,
                'time_horizon': time_horizon,
                'total_job_duration': sum(job['duration'] for job in jobs),
                'avg_job_duration': sum(job['duration'] for job in jobs) / n_jobs,
                'jobs': jobs,
                'machines': machines
            }
            
            return ProblemInstance(
                problem_type='job_scheduling',
                qubo_matrix=qubo,
                metadata=metadata,
                num_variables=n_jobs * n_machines * time_horizon,
                description=f"Job scheduling with {n_jobs} jobs, {n_machines} machines, {time_horizon} time slots",
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create job scheduling problem: {e}")
            raise
    
    def create_knapsack_problem(self,
                              items: List[Dict[str, Any]],
                              capacity: float) -> ProblemInstance:
        """
        Create a 0-1 Knapsack problem in QUBO format.
        
        Args:
            items: List of item dictionaries with 'weight', 'value'
            capacity: Knapsack capacity
        
        Returns:
            ProblemInstance with QUBO formulation
        """
        try:
            n_items = len(items)
            
            # Variables: x_i = 1 if item i is selected, 0 otherwise
            qubo = {}
            
            # Objective: maximize value (minimize negative value)
            for i, item in enumerate(items):
                value = item['value']
                qubo[(i, i)] = qubo.get((i, i), 0) - value
            
            # Capacity constraint: sum(weight_i * x_i) <= capacity
            # Penalty method: add penalty * (sum(weight_i * x_i) - capacity)^2
            penalty = max(item['value'] for item in items) * 10
            
            for i, item_i in enumerate(items):
                weight_i = item_i['weight']
                
                # Linear term: -2 * penalty * capacity * weight_i
                qubo[(i, i)] = qubo.get((i, i), 0) + penalty * (weight_i**2 - 2 * capacity * weight_i)
                
                # Quadratic terms
                for j, item_j in enumerate(items[i + 1:], i + 1):
                    weight_j = item_j['weight']
                    if (i, j) not in qubo:
                        qubo[(i, j)] = 0
                    qubo[(i, j)] += 2 * penalty * weight_i * weight_j
            
            # Add constant term for capacity^2 (doesn't affect optimization but for completeness)
            constant_term = penalty * capacity**2
            
            metadata = {
                'n_items': n_items,
                'capacity': capacity,
                'total_weight': sum(item['weight'] for item in items),
                'total_value': sum(item['value'] for item in items),
                'avg_value_density': sum(item['value'] / item['weight'] for item in items) / n_items,
                'items': items,
                'constant_term': constant_term
            }
            
            return ProblemInstance(
                problem_type='knapsack',
                qubo_matrix=qubo,
                metadata=metadata,
                num_variables=n_items,
                description=f"0-1 Knapsack with {n_items} items, capacity {capacity}",
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create knapsack problem: {e}")
            raise
    
    def create_graph_coloring_problem(self,
                                     adjacency_matrix: List[List[int]],
                                     num_colors: int) -> ProblemInstance:
        """
        Create a graph coloring problem in QUBO format.
        
        Args:
            adjacency_matrix: Adjacency matrix of the graph
            num_colors: Number of colors available
        
        Returns:
            ProblemInstance with QUBO formulation
        """
        try:
            adj_matrix = np.array(adjacency_matrix)
            n_nodes = adj_matrix.shape[0]
            
            # Variables: x_{i,c} = 1 if node i has color c
            def var_index(node: int, color: int) -> int:
                return node * num_colors + color
            
            qubo = {}
            
            # Constraint 1: Each node has exactly one color
            penalty_1 = 100
            for i in range(n_nodes):
                for c1 in range(num_colors):
                    var1 = var_index(i, c1)
                    qubo[(var1, var1)] = qubo.get((var1, var1), 0) + penalty_1 * (1 - 2)
                    
                    for c2 in range(c1 + 1, num_colors):
                        var2 = var_index(i, c2)
                        if (var1, var2) not in qubo:
                            qubo[(var1, var2)] = 0
                        qubo[(var1, var2)] += 2 * penalty_1
            
            # Constraint 2: Adjacent nodes cannot have the same color
            penalty_2 = 200
            for i in range(n_nodes):
                for j in range(i + 1, n_nodes):
                    if adj_matrix[i, j] == 1:  # Adjacent nodes
                        for c in range(num_colors):
                            var_i = var_index(i, c)
                            var_j = var_index(j, c)
                            
                            if (var_i, var_j) not in qubo:
                                qubo[(var_i, var_j)] = 0
                            qubo[(var_i, var_j)] += penalty_2
            
            # Objective: minimize number of colors used (optional)
            color_penalty = 1
            for c in range(num_colors):
                for i in range(n_nodes):
                    var = var_index(i, c)
                    qubo[(var, var)] = qubo.get((var, var), 0) + color_penalty * c
            
            metadata = {
                'n_nodes': n_nodes,
                'num_colors': num_colors,
                'n_edges': np.count_nonzero(adj_matrix) // 2,
                'graph_density': np.count_nonzero(adj_matrix) / (n_nodes * (n_nodes - 1)),
                'chromatic_number_upper_bound': num_colors
            }
            
            return ProblemInstance(
                problem_type='graph_coloring',
                qubo_matrix=qubo,
                metadata=metadata,
                num_variables=n_nodes * num_colors,
                description=f"Graph coloring with {n_nodes} nodes, {num_colors} colors",
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create graph coloring problem: {e}")
            raise
    
    def create_custom_qubo(self,
                          qubo_matrix: Dict[Tuple[int, int], float],
                          problem_description: str,
                          metadata: Optional[Dict[str, Any]] = None) -> ProblemInstance:
        """
        Create a custom QUBO problem instance.
        
        Args:
            qubo_matrix: QUBO matrix in dictionary format
            problem_description: Description of the problem
            metadata: Optional metadata dictionary
        
        Returns:
            ProblemInstance with custom QUBO formulation
        """
        try:
            # Determine number of variables
            max_var = 0
            for key in qubo_matrix.keys():
                if isinstance(key, tuple):
                    max_var = max(max_var, max(key))
                else:
                    max_var = max(max_var, key)
            
            num_variables = max_var + 1
            
            if metadata is None:
                metadata = {}
            
            metadata.update({
                'custom_problem': True,
                'qubo_density': len(qubo_matrix) / (num_variables * num_variables),
                'num_nonzero_terms': len(qubo_matrix)
            })
            
            return ProblemInstance(
                problem_type='custom',
                qubo_matrix=qubo_matrix,
                metadata=metadata,
                num_variables=num_variables,
                description=problem_description,
                created_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Failed to create custom QUBO problem: {e}")
            raise
    
    def validate_problem_instance(self, problem: ProblemInstance) -> Dict[str, Any]:
        """
        Validate a problem instance for correctness and feasibility.
        
        Args:
            problem: ProblemInstance to validate
        
        Returns:
            Dictionary with validation results
        """
        try:
            validation_result = {
                'valid': True,
                'warnings': [],
                'errors': [],
                'statistics': {}
            }
            
            # Check QUBO matrix format
            if not isinstance(problem.qubo_matrix, dict):
                validation_result['errors'].append("QUBO matrix must be a dictionary")
                validation_result['valid'] = False
                return validation_result
            
            # Check variable indices
            max_var = -1
            for key in problem.qubo_matrix.keys():
                if isinstance(key, tuple) and len(key) == 2:
                    i, j = key
                    max_var = max(max_var, i, j)
                elif isinstance(key, int):
                    max_var = max(max_var, key)
                else:
                    validation_result['errors'].append(f"Invalid QUBO key format: {key}")
                    validation_result['valid'] = False
            
            if max_var + 1 != problem.num_variables:
                validation_result['warnings'].append(
                    f"Mismatch between declared num_variables ({problem.num_variables}) and actual ({max_var + 1})"
                )
            
            # Calculate statistics
            values = list(problem.qubo_matrix.values())
            if values:
                validation_result['statistics'] = {
                    'num_terms': len(values),
                    'min_coefficient': min(values),
                    'max_coefficient': max(values),
                    'mean_coefficient': sum(values) / len(values),
                    'density': len(values) / (problem.num_variables ** 2)
                }
            
            # Problem-specific validations
            if problem.problem_type == 'portfolio_optimization':
                self._validate_portfolio_problem(problem, validation_result)
            elif problem.problem_type == 'tsp':
                self._validate_tsp_problem(problem, validation_result)
            elif problem.problem_type == 'max_cut':
                self._validate_max_cut_problem(problem, validation_result)
            
            return validation_result
            
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Validation failed: {str(e)}"],
                'warnings': [],
                'statistics': {}
            }
    
    def _validate_portfolio_problem(self, problem: ProblemInstance, validation_result: Dict[str, Any]):
        """Validate portfolio optimization specific constraints."""
        metadata = problem.metadata
        
        if 'n_assets' not in metadata:
            validation_result['warnings'].append("Missing n_assets in metadata")
        
        if 'expected_returns' in metadata:
            returns = metadata['expected_returns']
            if len(returns) != metadata.get('n_assets', 0):
                validation_result['errors'].append("Mismatch between n_assets and returns length")
                validation_result['valid'] = False
    
    def _validate_tsp_problem(self, problem: ProblemInstance, validation_result: Dict[str, Any]):
        """Validate TSP specific constraints."""
        metadata = problem.metadata
        
        if 'n_cities' not in metadata:
            validation_result['warnings'].append("Missing n_cities in metadata")
        else:
            n_cities = metadata['n_cities']
            expected_vars = n_cities * n_cities
            if problem.num_variables != expected_vars:
                validation_result['errors'].append(
                    f"TSP should have {expected_vars} variables, got {problem.num_variables}"
                )
                validation_result['valid'] = False
    
    def _validate_max_cut_problem(self, problem: ProblemInstance, validation_result: Dict[str, Any]):
        """Validate Max Cut specific constraints."""
        metadata = problem.metadata
        
        if 'n_nodes' not in metadata:
            validation_result['warnings'].append("Missing n_nodes in metadata")
        else:
            n_nodes = metadata['n_nodes']
            if problem.num_variables != n_nodes:
                validation_result['errors'].append(
                    f"Max Cut should have {n_nodes} variables, got {problem.num_variables}"
                )
                validation_result['valid'] = False
    
    def export_problem(self, problem: ProblemInstance, format: str = 'json') -> str:
        """
        Export problem instance to various formats.
        
        Args:
            problem: ProblemInstance to export
            format: Export format ('json', 'qubo', 'lp')
        
        Returns:
            String representation of the problem
        """
        if format == 'json':
            return self._export_json(problem)
        elif format == 'qubo':
            return self._export_qubo_format(problem)
        elif format == 'lp':
            return self._export_lp_format(problem)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, problem: ProblemInstance) -> str:
        """Export problem as JSON."""
        data = {
            'problem_type': problem.problem_type,
            'description': problem.description,
            'num_variables': problem.num_variables,
            'qubo_matrix': {str(k): v for k, v in problem.qubo_matrix.items()},
            'metadata': problem.metadata,
            'created_at': problem.created_at.isoformat()
        }
        return json.dumps(data, indent=2)
    
    def _export_qubo_format(self, problem: ProblemInstance) -> str:
        """Export problem in QUBO format."""
        lines = [f"c {problem.description}"]
        lines.append(f"p qubo 0 {problem.num_variables} {len(problem.qubo_matrix)}")
        
        for (i, j), value in problem.qubo_matrix.items():
            lines.append(f"{i} {j} {value}")
        
        return "\n".join(lines)
    
    def _export_lp_format(self, problem: ProblemInstance) -> str:
        """Export problem in LP format."""
        lines = [f"\\ {problem.description}"]
        lines.append("Minimize")
        
        # Build objective function
        obj_terms = []
        for (i, j), coeff in problem.qubo_matrix.items():
            if i == j:
                obj_terms.append(f"{coeff} x{i}")
            else:
                obj_terms.append(f"{coeff} x{i} * x{j}")
        
        lines.append(" + ".join(obj_terms))
        lines.append("Subject To")
        lines.append("Bounds")
        
        for i in range(problem.num_variables):
            lines.append(f"x{i} = 0 or 1")
        
        lines.append("End")
        return "\n".join(lines)