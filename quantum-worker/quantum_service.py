import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json
import time
from datetime import datetime, timedelta

try:
    import dynex
except ImportError:
    dynex = None
    logging.warning("Dynex SDK not available. Quantum operations will use classical fallback.")

from .qubo_solver import QUBOSolver
from .quantum_algorithms import QuantumAlgorithms
from .result_processor import ResultProcessor
from .error_mitigation import ErrorMitigation

class QuantumBackend(Enum):
    DYNEX = "dynex"
    CLASSICAL_SIMULATION = "classical"
    HYBRID = "hybrid"

@dataclass
class QuantumJob:
    job_id: str
    problem_type: str
    backend: QuantumBackend
    parameters: Dict[str, Any]
    status: str = "pending"
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.metadata is None:
            self.metadata = {}

@dataclass
class QuantumResult:
    job_id: str
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: Optional[float] = None
    quantum_advantage: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class QuantumService:
    """
    Unified quantum computing service that abstracts different quantum backends
    and provides a consistent interface for quantum operations.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.qubo_solver = QUBOSolver(config.get('qubo', {}))
        self.algorithms = QuantumAlgorithms(config.get('algorithms', {}))
        self.result_processor = ResultProcessor(config.get('results', {}))
        self.error_mitigation = ErrorMitigation(config.get('error_mitigation', {}))
        
        # Job tracking
        self.active_jobs: Dict[str, QuantumJob] = {}
        self.completed_jobs: Dict[str, QuantumJob] = {}
        
        # Backend availability
        self.available_backends = self._check_backend_availability()
        
        self.logger.info(f"QuantumService initialized with backends: {list(self.available_backends)}")
    
    def _check_backend_availability(self) -> List[QuantumBackend]:
        """Check which quantum backends are available."""
        backends = [QuantumBackend.CLASSICAL_SIMULATION]  # Always available
        
        if dynex is not None:
            try:
                # Test Dynex connection
                backends.append(QuantumBackend.DYNEX)
                self.logger.info("Dynex backend available")
            except Exception as e:
                self.logger.warning(f"Dynex backend unavailable: {e}")
        
        backends.append(QuantumBackend.HYBRID)  # Hybrid is always available
        return backends
    
    async def submit_job(self, 
                        problem_type: str,
                        parameters: Dict[str, Any],
                        backend: Union[str, QuantumBackend] = None,
                        job_id: str = None) -> str:
        """
        Submit a quantum job for processing.
        
        Args:
            problem_type: Type of quantum problem (qubo, portfolio_optimization, etc.)
            parameters: Problem-specific parameters
            backend: Preferred quantum backend
            job_id: Optional custom job ID
        
        Returns:
            Job ID for tracking
        """
        if job_id is None:
            job_id = f"qjob_{int(time.time() * 1000)}_{len(self.active_jobs)}"
        
        if isinstance(backend, str):
            backend = QuantumBackend(backend)
        elif backend is None:
            backend = self._select_optimal_backend(problem_type, parameters)
        
        job = QuantumJob(
            job_id=job_id,
            problem_type=problem_type,
            backend=backend,
            parameters=parameters,
            metadata={
                'submitted_via': 'quantum_service',
                'backend_selected': backend.value
            }
        )
        
        self.active_jobs[job_id] = job
        
        # Start processing asynchronously
        asyncio.create_task(self._process_job(job))
        
        self.logger.info(f"Job {job_id} submitted for {problem_type} using {backend.value}")
        return job_id
    
    def _select_optimal_backend(self, problem_type: str, parameters: Dict[str, Any]) -> QuantumBackend:
        """
        Select the optimal backend based on problem characteristics.
        """
        problem_size = self._estimate_problem_size(problem_type, parameters)
        
        # For large problems, prefer Dynex if available
        if problem_size > 100 and QuantumBackend.DYNEX in self.available_backends:
            return QuantumBackend.DYNEX
        
        # For medium problems, use hybrid approach
        if problem_size > 20:
            return QuantumBackend.HYBRID
        
        # For small problems, classical simulation is fine
        return QuantumBackend.CLASSICAL_SIMULATION
    
    def _estimate_problem_size(self, problem_type: str, parameters: Dict[str, Any]) -> int:
        """
        Estimate the computational complexity of the problem.
        """
        if problem_type == "qubo":
            if "Q" in parameters:
                return len(parameters["Q"])
            elif "num_variables" in parameters:
                return parameters["num_variables"]
        
        elif problem_type == "portfolio_optimization":
            if "assets" in parameters:
                return len(parameters["assets"])
        
        elif problem_type == "tsp":
            if "cities" in parameters:
                return len(parameters["cities"])
        
        return 10  # Default small size
    
    async def _process_job(self, job: QuantumJob):
        """
        Process a quantum job using the specified backend.
        """
        try:
            job.status = "running"
            job.started_at = datetime.utcnow()
            
            start_time = time.time()
            
            # Route to appropriate solver
            if job.problem_type == "qubo":
                result = await self._solve_qubo(job)
            elif job.problem_type == "portfolio_optimization":
                result = await self._optimize_portfolio(job)
            elif job.problem_type == "tsp":
                result = await self._solve_tsp(job)
            elif job.problem_type == "max_cut":
                result = await self._solve_max_cut(job)
            else:
                raise ValueError(f"Unsupported problem type: {job.problem_type}")
            
            execution_time = time.time() - start_time
            
            # Apply error mitigation if needed
            if job.backend == QuantumBackend.DYNEX:
                result = await self.error_mitigation.apply(result, job.parameters)
            
            # Process and validate results
            processed_result = await self.result_processor.process(
                result, job.problem_type, job.parameters
            )
            
            job.result = processed_result
            job.status = "completed"
            job.completed_at = datetime.utcnow()
            job.metadata.update({
                'execution_time': execution_time,
                'backend_used': job.backend.value,
                'quantum_advantage': self._calculate_quantum_advantage(execution_time, job)
            })
            
            self.logger.info(f"Job {job.job_id} completed successfully in {execution_time:.2f}s")
            
        except Exception as e:
            job.status = "failed"
            job.error = str(e)
            job.completed_at = datetime.utcnow()
            self.logger.error(f"Job {job.job_id} failed: {e}")
        
        finally:
            # Move to completed jobs
            if job.job_id in self.active_jobs:
                del self.active_jobs[job.job_id]
            self.completed_jobs[job.job_id] = job
    
    async def _solve_qubo(self, job: QuantumJob) -> Dict[str, Any]:
        """
        Solve QUBO problem using the specified backend.
        """
        if job.backend == QuantumBackend.DYNEX:
            return await self.qubo_solver.solve_dynex(job.parameters)
        elif job.backend == QuantumBackend.HYBRID:
            return await self.qubo_solver.solve_hybrid(job.parameters)
        else:
            return await self.qubo_solver.solve_classical(job.parameters)
    
    async def _optimize_portfolio(self, job: QuantumJob) -> Dict[str, Any]:
        """
        Solve portfolio optimization problem.
        """
        return await self.algorithms.portfolio_optimization(
            job.parameters, job.backend
        )
    
    async def _solve_tsp(self, job: QuantumJob) -> Dict[str, Any]:
        """
        Solve Traveling Salesman Problem.
        """
        return await self.algorithms.traveling_salesman(
            job.parameters, job.backend
        )
    
    async def _solve_max_cut(self, job: QuantumJob) -> Dict[str, Any]:
        """
        Solve Maximum Cut problem.
        """
        return await self.algorithms.max_cut(
            job.parameters, job.backend
        )
    
    def _calculate_quantum_advantage(self, execution_time: float, job: QuantumJob) -> Dict[str, Any]:
        """
        Calculate quantum advantage metrics.
        """
        problem_size = self._estimate_problem_size(job.problem_type, job.parameters)
        
        # Estimate classical time (rough approximation)
        classical_time_estimate = problem_size ** 2 * 0.001  # Very rough estimate
        
        speedup = classical_time_estimate / execution_time if execution_time > 0 else 1
        
        return {
            'speedup_factor': speedup,
            'problem_size': problem_size,
            'execution_time': execution_time,
            'classical_estimate': classical_time_estimate,
            'backend_used': job.backend.value
        }
    
    async def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a job.
        """
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
        elif job_id in self.completed_jobs:
            job = self.completed_jobs[job_id]
        else:
            return None
        
        return {
            'job_id': job.job_id,
            'status': job.status,
            'problem_type': job.problem_type,
            'backend': job.backend.value,
            'created_at': job.created_at.isoformat(),
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'completed_at': job.completed_at.isoformat() if job.completed_at else None,
            'error': job.error,
            'metadata': job.metadata
        }
    
    async def get_job_result(self, job_id: str) -> Optional[QuantumResult]:
        """
        Get the result of a completed job.
        """
        if job_id in self.completed_jobs:
            job = self.completed_jobs[job_id]
            
            if job.status == "completed":
                return QuantumResult(
                    job_id=job.job_id,
                    success=True,
                    result=job.result,
                    execution_time=job.metadata.get('execution_time'),
                    quantum_advantage=job.metadata.get('quantum_advantage'),
                    metadata=job.metadata
                )
            else:
                return QuantumResult(
                    job_id=job.job_id,
                    success=False,
                    error=job.error,
                    metadata=job.metadata
                )
        
        return None
    
    async def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a running job.
        """
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
            job.status = "cancelled"
            job.completed_at = datetime.utcnow()
            
            # Move to completed jobs
            del self.active_jobs[job_id]
            self.completed_jobs[job_id] = job
            
            self.logger.info(f"Job {job_id} cancelled")
            return True
        
        return False
    
    async def list_jobs(self, 
                       status: Optional[str] = None,
                       limit: int = 100) -> List[Dict[str, Any]]:
        """
        List jobs with optional filtering.
        """
        all_jobs = list(self.active_jobs.values()) + list(self.completed_jobs.values())
        
        if status:
            all_jobs = [job for job in all_jobs if job.status == status]
        
        # Sort by creation time (newest first)
        all_jobs.sort(key=lambda x: x.created_at, reverse=True)
        
        # Limit results
        all_jobs = all_jobs[:limit]
        
        return [
            {
                'job_id': job.job_id,
                'status': job.status,
                'problem_type': job.problem_type,
                'backend': job.backend.value,
                'created_at': job.created_at.isoformat(),
                'completed_at': job.completed_at.isoformat() if job.completed_at else None
            }
            for job in all_jobs
        ]
    
    async def get_backend_status(self) -> Dict[str, Any]:
        """
        Get the status of available backends.
        """
        status = {
            'available_backends': [backend.value for backend in self.available_backends],
            'active_jobs': len(self.active_jobs),
            'completed_jobs': len(self.completed_jobs)
        }
        
        # Check Dynex status if available
        if QuantumBackend.DYNEX in self.available_backends:
            try:
                # Add Dynex-specific status
                status['dynex_status'] = 'available'
            except Exception as e:
                status['dynex_status'] = f'error: {e}'
        
        return status
    
    async def cleanup_old_jobs(self, max_age_hours: int = 24):
        """
        Clean up old completed jobs to free memory.
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        
        jobs_to_remove = [
            job_id for job_id, job in self.completed_jobs.items()
            if job.completed_at and job.completed_at < cutoff_time
        ]
        
        for job_id in jobs_to_remove:
            del self.completed_jobs[job_id]
        
        self.logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")
        return len(jobs_to_remove)

# Global quantum service instance
_quantum_service = None

def get_quantum_service(config: Dict[str, Any] = None) -> QuantumService:
    """
    Get or create the global quantum service instance.
    """
    global _quantum_service
    if _quantum_service is None:
        _quantum_service = QuantumService(config)
    return _quantum_service