import asyncio
import logging
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
import time
from scipy.optimize import minimize
from scipy.sparse import csr_matrix

try:
    import dynex
except ImportError:
    dynex = None
    logging.warning("Dynex SDK not available. Using classical fallback for QUBO solving.")

try:
    import networkx as nx
except ImportError:
    nx = None

try:
    from dimod import BinaryQuadraticModel, ExactSolver
    from dwave.system import DWaveSampler, EmbeddingComposite
except ImportError:
    BinaryQuadraticModel = None
    ExactSolver = None
    DWaveSampler = None
    EmbeddingComposite = None

@dataclass
class QUBOResult:
    solution: Dict[int, int]
    energy: float
    num_occurrences: int = 1
    chain_break_fraction: float = 0.0
    timing: Dict[str, float] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timing is None:
            self.timing = {}
        if self.metadata is None:
            self.metadata = {}

class QUBOSolver:
    """
    Unified QUBO (Quadratic Unconstrained Binary Optimization) solver
    that supports multiple backends including Dynex, classical optimization,
    and hybrid approaches.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Solver configuration
        self.max_iterations = self.config.get('max_iterations', 1000)
        self.convergence_threshold = self.config.get('convergence_threshold', 1e-6)
        self.timeout_seconds = self.config.get('timeout_seconds', 300)
        
        # Dynex configuration
        self.dynex_config = self.config.get('dynex', {
            'mainnet': True,
            'num_reads': 1000,
            'annealing_time': 20,
            'description': 'QUBO optimization via QuantumService'
        })
        
        self.logger.info("QUBOSolver initialized")
    
    async def solve_dynex(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve QUBO problem using Dynex quantum annealing.
        
        Args:
            parameters: Dictionary containing:
                - Q: QUBO matrix (dict or numpy array)
                - num_reads: Number of samples (optional)
                - annealing_time: Annealing time in microseconds (optional)
                - chain_strength: Chain strength for embedding (optional)
        
        Returns:
            Dictionary with solution, energy, and metadata
        """
        if dynex is None:
            self.logger.warning("Dynex not available, falling back to classical solver")
            return await self.solve_classical(parameters)
        
        try:
            start_time = time.time()
            
            # Extract QUBO matrix
            Q = self._extract_qubo_matrix(parameters)
            
            # Convert to Dynex format
            bqm = self._create_bqm_from_qubo(Q)
            
            # Configure Dynex sampler
            sampler_config = {
                'mainnet': self.dynex_config.get('mainnet', True),
                'num_reads': parameters.get('num_reads', self.dynex_config.get('num_reads', 1000)),
                'annealing_time': parameters.get('annealing_time', self.dynex_config.get('annealing_time', 20)),
                'description': self.dynex_config.get('description', 'QUBO optimization')
            }
            
            # Create Dynex sampler
            sampler = dynex.DynexSampler()
            
            # Sample from the BQM
            self.logger.info(f"Submitting QUBO to Dynex with {sampler_config['num_reads']} reads")
            
            sampleset = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: sampler.sample(bqm, **sampler_config)
            )
            
            # Process results
            best_sample = sampleset.first
            solution = dict(best_sample.sample)
            energy = best_sample.energy
            
            execution_time = time.time() - start_time
            
            # Calculate additional metrics
            chain_break_fraction = self._calculate_chain_breaks(sampleset)
            
            result = QUBOResult(
                solution=solution,
                energy=energy,
                num_occurrences=best_sample.num_occurrences,
                chain_break_fraction=chain_break_fraction,
                timing={
                    'total_time': execution_time,
                    'qpu_time': getattr(sampleset.info, 'timing', {}).get('qpu_access_time', 0) / 1000000,  # Convert to seconds
                },
                metadata={
                    'backend': 'dynex',
                    'num_reads': sampler_config['num_reads'],
                    'annealing_time': sampler_config['annealing_time'],
                    'num_variables': len(solution),
                    'sampleset_info': dict(sampleset.info)
                }
            )
            
            self.logger.info(f"Dynex QUBO solved in {execution_time:.2f}s with energy {energy}")
            return self._result_to_dict(result)
            
        except Exception as e:
            self.logger.error(f"Dynex QUBO solving failed: {e}")
            # Fallback to classical solver
            return await self.solve_classical(parameters)
    
    async def solve_classical(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve QUBO problem using classical optimization methods.
        
        Args:
            parameters: Dictionary containing QUBO matrix and optimization parameters
        
        Returns:
            Dictionary with solution, energy, and metadata
        """
        try:
            start_time = time.time()
            
            # Extract QUBO matrix
            Q = self._extract_qubo_matrix(parameters)
            
            # Choose classical method based on problem size
            num_vars = len(Q) if isinstance(Q, dict) else Q.shape[0]
            
            if num_vars <= 20:
                # Exact solver for small problems
                result = await self._solve_exact(Q)
            elif num_vars <= 100:
                # Simulated annealing for medium problems
                result = await self._solve_simulated_annealing(Q, parameters)
            else:
                # Tabu search for large problems
                result = await self._solve_tabu_search(Q, parameters)
            
            execution_time = time.time() - start_time
            result.timing['total_time'] = execution_time
            result.metadata['backend'] = 'classical'
            result.metadata['num_variables'] = num_vars
            
            self.logger.info(f"Classical QUBO solved in {execution_time:.2f}s with energy {result.energy}")
            return self._result_to_dict(result)
            
        except Exception as e:
            self.logger.error(f"Classical QUBO solving failed: {e}")
            raise
    
    async def solve_hybrid(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve QUBO problem using hybrid classical-quantum approach.
        
        Args:
            parameters: Dictionary containing QUBO matrix and optimization parameters
        
        Returns:
            Dictionary with solution, energy, and metadata
        """
        try:
            start_time = time.time()
            
            # Extract QUBO matrix
            Q = self._extract_qubo_matrix(parameters)
            num_vars = len(Q) if isinstance(Q, dict) else Q.shape[0]
            
            # Decompose problem into subproblems
            subproblems = self._decompose_qubo(Q, max_subproblem_size=50)
            
            # Solve subproblems
            subresults = []
            for i, subproblem in enumerate(subproblems):
                self.logger.info(f"Solving subproblem {i+1}/{len(subproblems)}")
                
                # Use quantum solver for smaller subproblems, classical for larger
                if len(subproblem['variables']) <= 30 and dynex is not None:
                    subresult = await self.solve_dynex({
                        'Q': subproblem['Q'],
                        'num_reads': parameters.get('num_reads', 500)
                    })
                else:
                    subresult = await self.solve_classical({'Q': subproblem['Q']})
                
                subresults.append({
                    'variables': subproblem['variables'],
                    'result': subresult
                })
            
            # Combine subproblem solutions
            combined_solution = self._combine_subproblem_solutions(subresults, Q)
            
            # Local optimization to improve combined solution
            optimized_solution = await self._local_optimization(combined_solution, Q)
            
            execution_time = time.time() - start_time
            
            result = QUBOResult(
                solution=optimized_solution['solution'],
                energy=optimized_solution['energy'],
                timing={'total_time': execution_time},
                metadata={
                    'backend': 'hybrid',
                    'num_variables': num_vars,
                    'num_subproblems': len(subproblems),
                    'subproblem_results': [sr['result']['metadata'] for sr in subresults]
                }
            )
            
            self.logger.info(f"Hybrid QUBO solved in {execution_time:.2f}s with energy {result.energy}")
            return self._result_to_dict(result)
            
        except Exception as e:
            self.logger.error(f"Hybrid QUBO solving failed: {e}")
            # Fallback to classical solver
            return await self.solve_classical(parameters)
    
    def _extract_qubo_matrix(self, parameters: Dict[str, Any]) -> np.ndarray:
        """
        Extract and validate QUBO matrix from parameters.
        """
        if 'Q' not in parameters:
            raise ValueError("QUBO matrix 'Q' not found in parameters")
        
        Q = parameters['Q']
        
        if isinstance(Q, dict):
            # Convert dictionary format to numpy array
            max_var = max(max(k) if isinstance(k, tuple) else k for k in Q.keys())
            Q_matrix = np.zeros((max_var + 1, max_var + 1))
            
            for key, value in Q.items():
                if isinstance(key, tuple):
                    i, j = key
                    Q_matrix[i, j] = value
                    if i != j:
                        Q_matrix[j, i] = value  # Ensure symmetry
                else:
                    Q_matrix[key, key] = value
            
            return Q_matrix
        
        elif isinstance(Q, (list, np.ndarray)):
            return np.array(Q)
        
        else:
            raise ValueError(f"Unsupported QUBO matrix format: {type(Q)}")
    
    def _create_bqm_from_qubo(self, Q: np.ndarray):
        """
        Create a Binary Quadratic Model from QUBO matrix.
        """
        if BinaryQuadraticModel is None:
            raise ImportError("dimod package required for BQM creation")
        
        # Extract linear and quadratic terms
        linear = {i: Q[i, i] for i in range(Q.shape[0])}
        quadratic = {}
        
        for i in range(Q.shape[0]):
            for j in range(i + 1, Q.shape[1]):
                if Q[i, j] != 0:
                    quadratic[(i, j)] = Q[i, j]
        
        return BinaryQuadraticModel(linear, quadratic, 'BINARY')
    
    async def _solve_exact(self, Q: np.ndarray) -> QUBOResult:
        """
        Solve QUBO exactly by enumerating all possible solutions.
        """
        n = Q.shape[0]
        best_energy = float('inf')
        best_solution = None
        
        # Enumerate all 2^n possible solutions
        for i in range(2**n):
            solution = [(i >> j) & 1 for j in range(n)]
            energy = self._calculate_qubo_energy(solution, Q)
            
            if energy < best_energy:
                best_energy = energy
                best_solution = {j: solution[j] for j in range(n)}
        
        return QUBOResult(
            solution=best_solution,
            energy=best_energy,
            metadata={'method': 'exact_enumeration'}
        )
    
    async def _solve_simulated_annealing(self, Q: np.ndarray, parameters: Dict[str, Any]) -> QUBOResult:
        """
        Solve QUBO using simulated annealing.
        """
        n = Q.shape[0]
        
        # Initialize random solution
        current_solution = np.random.randint(0, 2, n)
        current_energy = self._calculate_qubo_energy(current_solution, Q)
        
        best_solution = current_solution.copy()
        best_energy = current_energy
        
        # Simulated annealing parameters
        initial_temp = parameters.get('initial_temperature', 1.0)
        final_temp = parameters.get('final_temperature', 0.01)
        num_iterations = parameters.get('num_iterations', self.max_iterations)
        
        for iteration in range(num_iterations):
            # Temperature schedule
            temp = initial_temp * (final_temp / initial_temp) ** (iteration / num_iterations)
            
            # Propose a move (flip a random bit)
            new_solution = current_solution.copy()
            flip_index = np.random.randint(0, n)
            new_solution[flip_index] = 1 - new_solution[flip_index]
            
            new_energy = self._calculate_qubo_energy(new_solution, Q)
            
            # Accept or reject the move
            if new_energy < current_energy or np.random.random() < np.exp(-(new_energy - current_energy) / temp):
                current_solution = new_solution
                current_energy = new_energy
                
                if current_energy < best_energy:
                    best_solution = current_solution.copy()
                    best_energy = current_energy
        
        return QUBOResult(
            solution={i: int(best_solution[i]) for i in range(n)},
            energy=best_energy,
            metadata={
                'method': 'simulated_annealing',
                'iterations': num_iterations,
                'final_temperature': temp
            }
        )
    
    async def _solve_tabu_search(self, Q: np.ndarray, parameters: Dict[str, Any]) -> QUBOResult:
        """
        Solve QUBO using tabu search.
        """
        n = Q.shape[0]
        
        # Initialize random solution
        current_solution = np.random.randint(0, 2, n)
        current_energy = self._calculate_qubo_energy(current_solution, Q)
        
        best_solution = current_solution.copy()
        best_energy = current_energy
        
        # Tabu search parameters
        tabu_tenure = parameters.get('tabu_tenure', min(n, 10))
        num_iterations = parameters.get('num_iterations', self.max_iterations)
        
        tabu_list = []
        
        for iteration in range(num_iterations):
            best_move = None
            best_move_energy = float('inf')
            
            # Evaluate all possible moves
            for i in range(n):
                if i not in tabu_list:
                    # Try flipping bit i
                    new_solution = current_solution.copy()
                    new_solution[i] = 1 - new_solution[i]
                    new_energy = self._calculate_qubo_energy(new_solution, Q)
                    
                    if new_energy < best_move_energy:
                        best_move = i
                        best_move_energy = new_energy
            
            if best_move is not None:
                # Make the best move
                current_solution[best_move] = 1 - current_solution[best_move]
                current_energy = best_move_energy
                
                # Update tabu list
                tabu_list.append(best_move)
                if len(tabu_list) > tabu_tenure:
                    tabu_list.pop(0)
                
                # Update best solution
                if current_energy < best_energy:
                    best_solution = current_solution.copy()
                    best_energy = current_energy
        
        return QUBOResult(
            solution={i: int(best_solution[i]) for i in range(n)},
            energy=best_energy,
            metadata={
                'method': 'tabu_search',
                'iterations': num_iterations,
                'tabu_tenure': tabu_tenure
            }
        )
    
    def _decompose_qubo(self, Q: np.ndarray, max_subproblem_size: int = 50) -> List[Dict[str, Any]]:
        """
        Decompose QUBO problem into smaller subproblems.
        """
        n = Q.shape[0]
        
        if n <= max_subproblem_size:
            return [{
                'variables': list(range(n)),
                'Q': Q
            }]
        
        # Simple decomposition: divide variables into chunks
        subproblems = []
        chunk_size = max_subproblem_size
        
        for i in range(0, n, chunk_size):
            end_idx = min(i + chunk_size, n)
            variables = list(range(i, end_idx))
            
            # Extract subproblem QUBO matrix
            sub_Q = Q[i:end_idx, i:end_idx]
            
            subproblems.append({
                'variables': variables,
                'Q': sub_Q
            })
        
        return subproblems
    
    def _combine_subproblem_solutions(self, subresults: List[Dict[str, Any]], Q: np.ndarray) -> Dict[str, Any]:
        """
        Combine solutions from subproblems.
        """
        combined_solution = {}
        
        for subresult in subresults:
            variables = subresult['variables']
            solution = subresult['result']['solution']
            
            for var in variables:
                if var < len(variables):
                    combined_solution[var] = solution.get(var - variables[0], 0)
        
        # Calculate energy of combined solution
        solution_vector = [combined_solution.get(i, 0) for i in range(Q.shape[0])]
        energy = self._calculate_qubo_energy(solution_vector, Q)
        
        return {
            'solution': combined_solution,
            'energy': energy
        }
    
    async def _local_optimization(self, initial_solution: Dict[str, Any], Q: np.ndarray) -> Dict[str, Any]:
        """
        Perform local optimization to improve the solution.
        """
        current_solution = initial_solution['solution'].copy()
        current_energy = initial_solution['energy']
        
        improved = True
        iterations = 0
        max_local_iterations = 100
        
        while improved and iterations < max_local_iterations:
            improved = False
            iterations += 1
            
            # Try flipping each bit
            for i in range(Q.shape[0]):
                # Create new solution with bit i flipped
                new_solution = current_solution.copy()
                new_solution[i] = 1 - new_solution[i]
                
                # Calculate new energy
                solution_vector = [new_solution.get(j, 0) for j in range(Q.shape[0])]
                new_energy = self._calculate_qubo_energy(solution_vector, Q)
                
                # Accept if improvement
                if new_energy < current_energy:
                    current_solution = new_solution
                    current_energy = new_energy
                    improved = True
                    break
        
        return {
            'solution': current_solution,
            'energy': current_energy
        }
    
    def _calculate_qubo_energy(self, solution: List[int], Q: np.ndarray) -> float:
        """
        Calculate the energy of a QUBO solution.
        """
        x = np.array(solution)
        return float(x.T @ Q @ x)
    
    def _calculate_chain_breaks(self, sampleset) -> float:
        """
        Calculate the fraction of chain breaks in the solution.
        """
        try:
            if hasattr(sampleset, 'data_vectors') and 'chain_break_fraction' in sampleset.data_vectors:
                return float(np.mean(sampleset.data_vectors['chain_break_fraction']))
        except:
            pass
        return 0.0
    
    def _result_to_dict(self, result: QUBOResult) -> Dict[str, Any]:
        """
        Convert QUBOResult to dictionary format.
        """
        return {
            'solution': result.solution,
            'energy': result.energy,
            'num_occurrences': result.num_occurrences,
            'chain_break_fraction': result.chain_break_fraction,
            'timing': result.timing,
            'metadata': result.metadata
        }
    
    async def validate_qubo(self, Q: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate QUBO problem formulation.
        """
        try:
            Q_matrix = self._extract_qubo_matrix({'Q': Q})
            
            validation_result = {
                'valid': True,
                'num_variables': Q_matrix.shape[0],
                'is_symmetric': np.allclose(Q_matrix, Q_matrix.T),
                'density': np.count_nonzero(Q_matrix) / Q_matrix.size,
                'condition_number': np.linalg.cond(Q_matrix) if Q_matrix.shape[0] > 0 else 0,
                'eigenvalue_range': {
                    'min': float(np.min(np.linalg.eigvals(Q_matrix))),
                    'max': float(np.max(np.linalg.eigvals(Q_matrix)))
                } if Q_matrix.shape[0] > 0 else {'min': 0, 'max': 0}
            }
            
            # Add warnings for potential issues
            warnings = []
            if not validation_result['is_symmetric']:
                warnings.append("QUBO matrix is not symmetric")
            if validation_result['condition_number'] > 1e12:
                warnings.append("QUBO matrix is ill-conditioned")
            if validation_result['density'] < 0.1:
                warnings.append("QUBO matrix is very sparse")
            
            validation_result['warnings'] = warnings
            
            return validation_result
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }