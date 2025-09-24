"""Quantum Job Manager

Manages QUBO job submission, orchestration, and result processing
with Dynex quantum computing platform integration.
"""

import asyncio
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

import numpy as np
from pydantic import BaseModel, Field
from src.qdllm.core.nuco_client import NucoClient

try:
    import dynex
except ImportError:
    dynex = None
    logging.warning("Dynex SDK not available. Using mock implementation.")


class JobType(Enum):
    """Types of quantum jobs"""
    LEAD_RANKING = "lead_ranking"
    ROUTE_OPTIMIZATION = "route_opt"
    CONVERSATION_PATH = "conversation_path"
    BACKTRACE = "backtrace"
    RANK_PATHS = "rank_paths"
    PORTFOLIO_OPTIMIZATION = "portfolio_opt"
    RESOURCE_ALLOCATION = "resource_allocation"


class JobStatus(Enum):
    """Job execution status"""
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class JobPriority(Enum):
    """Job priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class QuantumJob:
    """Represents a quantum computing job"""
    id: str
    job_type: JobType
    payload: Dict[str, Any]
    status: JobStatus = JobStatus.PENDING
    priority: JobPriority = JobPriority.NORMAL
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    result: Optional[Any] = None
    error: Optional[str] = None
    cost_estimate: float = 0.0
    execution_time: float = 0.0
    retry_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QUBOProblem:
    """QUBO problem representation"""
    Q: np.ndarray  # QUBO matrix
    variables: List[str]  # Variable names
    objective: str  # Objective description
    constraints: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class QuboBuilder:
    """Builds QUBO problems for different use cases"""
    
    @staticmethod
    def build_ranking_qubo(candidates: List[Dict[str, Any]], 
                          context: Dict[str, Any]) -> QUBOProblem:
        """Build QUBO for ranking conversation candidates"""
        n = len(candidates)
        if n == 0:
            raise ValueError("No candidates provided")
            
        # Create QUBO matrix
        Q = np.zeros((n, n))
        
        # Diagonal terms: individual candidate scores
        for i, candidate in enumerate(candidates):
            confidence = candidate.get("confidence", 0.5)
            risk_score = candidate.get("risk_score", 0.5)
            # Higher confidence, lower risk = more negative (better in QUBO minimization)
            Q[i, i] = -(confidence - risk_score)
            
        # Off-diagonal terms: interaction penalties
        for i in range(n):
            for j in range(i + 1, n):
                # Penalize selecting multiple candidates
                Q[i, j] = 2.0
                Q[j, i] = 2.0
                
        variables = [f"candidate_{i}" for i in range(n)]
        
        return QUBOProblem(
            Q=Q,
            variables=variables,
            objective="Minimize ranking score to select best candidate",
            constraints=["Select exactly one candidate"],
            metadata={"candidate_count": n, "context": context}
        )
        
    @staticmethod
    def build_backtrace_qubo(target_outcome: str, 
                           observed_data: Dict[str, Any]) -> QUBOProblem:
        """Build QUBO for reversal reasoning / backtrace"""
        # Simplified backtrace QUBO - in practice this would be much more sophisticated
        factors = observed_data.get("factors", [])
        n = len(factors) if factors else 3  # Default to 3 factors
        
        Q = np.random.rand(n, n) * 0.1  # Small random interactions
        np.fill_diagonal(Q, np.random.rand(n) - 0.5)  # Random factor weights
        
        variables = [f"factor_{i}" for i in range(n)]
        
        return QUBOProblem(
            Q=Q,
            variables=variables,
            objective=f"Find root causes for outcome: {target_outcome}",
            constraints=["Minimize discrepancy to observed outcome"],
            metadata={"target_outcome": target_outcome, "observed_data": observed_data}
        )
        
    @staticmethod
    def build_lead_ranking_qubo(leads: List[Dict[str, Any]]) -> QUBOProblem:
        """Build QUBO for lead scoring and ranking"""
        n = len(leads)
        Q = np.zeros((n, n))
        
        # Score leads based on various factors
        for i, lead in enumerate(leads):
            score = 0.0
            score += lead.get("engagement_score", 0.0) * 0.3
            score += lead.get("fit_score", 0.0) * 0.4
            score += lead.get("urgency_score", 0.0) * 0.3
            
            Q[i, i] = -score  # Negative for minimization
            
        variables = [f"lead_{lead.get('id', i)}" for i, lead in enumerate(leads)]
        
        return QUBOProblem(
            Q=Q,
            variables=variables,
            objective="Rank leads by conversion probability",
            metadata={"lead_count": n}
        )


class DynexClient:
    """Wrapper for Dynex SDK with error handling and retries"""
    
    def __init__(self, api_key: Optional[str] = None, testnet: bool = True):
        self.api_key = api_key
        self.testnet = testnet
        self.logger = logging.getLogger("dynex_client")
        
        if dynex is None:
            self.logger.warning("Dynex SDK not available. Using mock mode.")
            self.mock_mode = True
        else:
            self.mock_mode = False
            try:
                # Initialize Dynex client
                if api_key:
                    dynex.set_api_key(api_key)
                self.logger.info(f"Dynex client initialized (testnet={testnet})")
            except Exception as e:
                self.logger.error(f"Failed to initialize Dynex client: {e}")
                self.mock_mode = True
                
    async def submit_qubo(self, qubo: QUBOProblem, 
                         num_reads: int = 1000,
                         annealing_time: int = 10) -> Dict[str, Any]:
        """Submit QUBO problem to Dynex"""
        if self.mock_mode:
            return await self._mock_submit_qubo(qubo, num_reads, annealing_time)
            
        try:
            # Convert QUBO to Dynex format
            model = dynex.BQM()
            
            # Add quadratic terms
            for i in range(len(qubo.variables)):
                for j in range(len(qubo.variables)):
                    if qubo.Q[i, j] != 0:
                        if i == j:
                            model.add_variable(qubo.variables[i], qubo.Q[i, j])
                        else:
                            model.add_interaction(qubo.variables[i], qubo.variables[j], qubo.Q[i, j])
                            
            # Submit to Dynex
            sampler = dynex.DynexSampler()
            response = await sampler.sample(model, 
                                          num_reads=num_reads,
                                          annealing_time=annealing_time,
                                          testnet=self.testnet)
                                          
            # Process results
            best_sample = response.first
            energy = response.data_vectors['energy'][0]
            
            return {
                "solution": dict(best_sample),
                "energy": energy,
                "num_reads": num_reads,
                "timing": response.info.get("timing", {}),
                "success": True
            }
            
        except Exception as e:
            self.logger.error(f"Dynex submission failed: {e}")
            return {
                "solution": {},
                "energy": float('inf'),
                "error": str(e),
                "success": False
            }
            
    async def _mock_submit_qubo(self, qubo: QUBOProblem, 
                               num_reads: int, annealing_time: int) -> Dict[str, Any]:
        """Mock QUBO submission for testing"""
        await asyncio.sleep(0.1)  # Simulate processing time
        
        # Generate mock solution
        n = len(qubo.variables)
        solution = {}
        
        if "ranking" in qubo.objective.lower() or "candidate" in qubo.objective.lower():
            # For ranking problems, select one variable
            selected_idx = np.random.randint(0, n)
            for i, var in enumerate(qubo.variables):
                solution[var] = 1 if i == selected_idx else 0
        else:
            # For other problems, random binary assignment
            for var in qubo.variables:
                solution[var] = np.random.randint(0, 2)
                
        return {
            "solution": solution,
            "energy": np.random.uniform(-1, 1),
            "num_reads": num_reads,
            "timing": {"total_time": annealing_time * 1000},
            "success": True,
            "mock": True
        }


class QuantumJobManager:
    """Manages quantum job lifecycle and orchestration"""
    
    def __init__(self,
                 dynex_client: Optional[DynexClient] = None,
                 nuco_client: Optional[NucoClient] = None,
                 max_retries: int = 3,
                 default_timeout: int = 30,
                 max_concurrent_jobs: int = 10,
                 start_processor: bool = True):
        self.dynex = dynex_client or DynexClient()
        self.nuco = nuco_client or NucoClient(api_key="your_nuco_api_key")  # Replace with actual key handling
        self.max_retries = max_retries
        self.default_timeout = default_timeout
        self.max_concurrent_jobs = max_concurrent_jobs
        
        self.jobs: Dict[str, QuantumJob] = {}
        self.job_queue: List[str] = []
        self.running_jobs: Dict[str, asyncio.Task] = {}
        self.logger = logging.getLogger("quantum_job_manager")
        
        # Start background job processor
        if start_processor:
            self._processor_task = asyncio.create_task(self._process_jobs())
        else:
            self._processor_task = None
        
    async def submit(self, payload: Dict[str, Any], 
                    priority: JobPriority = JobPriority.NORMAL) -> QuantumJob:
        """Submit a new quantum job"""
        job_id = str(uuid.uuid4())
        job_type = JobType(payload.get("type", "conversation_path"))
        
        job = QuantumJob(
            id=job_id,
            job_type=job_type,
            payload=payload,
            priority=priority,
            metadata={"submitted_by": "quantum_agent"}
        )
        
        self.jobs[job_id] = job
        self.job_queue.append(job_id)
        
        # Sort queue by priority
        self.job_queue.sort(key=lambda jid: self.jobs[jid].priority.value, reverse=True)
        
        self.logger.info(f"Job {job_id} submitted with type {job_type.value}")
        return job
        
    async def wait(self, job_id: str, timeout: Optional[int] = None) -> Optional[Any]:
        """Wait for job completion and return result"""
        timeout = timeout or self.default_timeout
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            job = self.jobs.get(job_id)
            if not job:
                raise ValueError(f"Job {job_id} not found")
                
            if job.status == JobStatus.COMPLETED:
                return job.result
            elif job.status == JobStatus.FAILED:
                raise RuntimeError(f"Job {job_id} failed: {job.error}")
            elif job.status == JobStatus.CANCELLED:
                raise RuntimeError(f"Job {job_id} was cancelled")
                
            await asyncio.sleep(0.1)
            
        # Timeout reached
        job.status = JobStatus.TIMEOUT
        raise TimeoutError(f"Job {job_id} timed out after {timeout} seconds")
        
    async def get_status(self, job_id: str) -> Optional[QuantumJob]:
        """Get job status"""
        return self.jobs.get(job_id)
        
    async def cancel(self, job_id: str) -> bool:
        """Cancel a job"""
        job = self.jobs.get(job_id)
        if not job:
            return False
            
        if job.status in [JobStatus.COMPLETED, JobStatus.FAILED]:
            return False
            
        job.status = JobStatus.CANCELLED
        
        # Cancel running task if exists
        if job_id in self.running_jobs:
            self.running_jobs[job_id].cancel()
            del self.running_jobs[job_id]
            
        # Remove from queue
        if job_id in self.job_queue:
            self.job_queue.remove(job_id)
            
        self.logger.info(f"Job {job_id} cancelled")
        return True
        
    async def batch_submit(self, payloads: List[Dict[str, Any]], 
                          priority: JobPriority = JobPriority.NORMAL) -> List[QuantumJob]:
        """Submit multiple jobs as a batch"""
        jobs = []
        for payload in payloads:
            job = await self.submit(payload, priority)
            jobs.append(job)
            
        self.logger.info(f"Batch submitted {len(jobs)} jobs")
        return jobs
        
    async def batch_wait(self, job_ids: List[str], 
                        timeout: Optional[int] = None) -> List[Any]:
        """Wait for multiple jobs to complete"""
        tasks = [self.wait(job_id, timeout) for job_id in job_ids]
        return await asyncio.gather(*tasks, return_exceptions=True)
        
    async def _process_jobs(self):
        """Background job processor"""
        while True:
            try:
                # Process pending jobs
                while (len(self.running_jobs) < self.max_concurrent_jobs and 
                       self.job_queue):
                    job_id = self.job_queue.pop(0)
                    job = self.jobs[job_id]
                    
                    if job.status == JobStatus.PENDING:
                        task = asyncio.create_task(self._execute_job(job))
                        self.running_jobs[job_id] = task
                        
                # Clean up completed tasks
                completed_jobs = []
                for job_id, task in self.running_jobs.items():
                    if task.done():
                        completed_jobs.append(job_id)
                        
                for job_id in completed_jobs:
                    del self.running_jobs[job_id]
                    
                await asyncio.sleep(0.1)
                
            except Exception as e:
                self.logger.error(f"Job processor error: {e}")
                await asyncio.sleep(1)
                
    async def _execute_job(self, job: QuantumJob):
        """Execute a single job"""
        job.status = JobStatus.RUNNING
        job.started_at = time.time()
        
        try:
            self.logger.info(f"Executing job {job.id} of type {job.job_type.value}")
            
            # Build QUBO problem based on job type
            qubo = self._build_qubo(job)
            
            # Submit to Dynex
            result = await self.dynex.submit_qubo(qubo)
            
            if result.get("success", False):
                # Process result based on job type
                processed_result = self._process_result(job, result)
                
                job.result = processed_result
                job.status = JobStatus.COMPLETED
                job.cost_estimate = self._estimate_cost(result)
                
                self.logger.info(f"Job {job.id} completed successfully")
            else:
                raise RuntimeError(f"Quantum execution failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            self.logger.error(f"Job {job.id} failed: {e}")
            
            job.error = str(e)
            job.retry_count += 1
            
            if job.retry_count < self.max_retries:
                job.status = JobStatus.PENDING
                self.job_queue.append(job.id)
                self.logger.info(f"Job {job.id} queued for retry ({job.retry_count}/{self.max_retries})")
            else:
                job.status = JobStatus.FAILED
                self.logger.error(f"Job {job.id} failed permanently after {job.retry_count} retries")
                
        finally:
            job.completed_at = time.time()
            if job.started_at:
                job.execution_time = job.completed_at - job.started_at
                
    def _build_qubo(self, job: QuantumJob) -> QUBOProblem:
        """Build QUBO problem based on job type"""
        payload = job.payload
        
        if job.job_type == JobType.CONVERSATION_PATH or job.job_type == JobType.RANK_PATHS:
            candidates = payload.get("candidates", [])
            context = payload.get("context", {})
            return QuboBuilder.build_ranking_qubo(candidates, context)
            
        elif job.job_type == JobType.BACKTRACE:
            target_outcome = payload.get("target_outcome", "")
            observed_data = payload.get("observed_data", {})
            return QuboBuilder.build_backtrace_qubo(target_outcome, observed_data)
            
        elif job.job_type == JobType.LEAD_RANKING:
            leads = payload.get("leads", [])
            return QuboBuilder.build_lead_ranking_qubo(leads)
            
        else:
            raise ValueError(f"Unsupported job type: {job.job_type}")
            
    def _process_result(self, job: QuantumJob, raw_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw quantum result based on job type"""
        solution = raw_result.get("solution", {})
        
        if job.job_type in [JobType.CONVERSATION_PATH, JobType.RANK_PATHS]:
            # Extract ranking from solution
            candidates = job.payload.get("candidates", [])
            ranking = []
            
            # Find selected candidates (value = 1)
            for var, value in solution.items():
                if value == 1 and var.startswith("candidate_"):
                    idx = int(var.split("_")[1])
                    if idx < len(candidates):
                        ranking.append(candidates[idx].get("id", f"candidate_{idx}"))
                        
            # If no clear winner, rank by energy contribution
            if not ranking:
                candidate_scores = []
                for i, candidate in enumerate(candidates):
                    var = f"candidate_{i}"
                    score = solution.get(var, 0)
                    candidate_scores.append((candidate.get("id", f"candidate_{i}"), score))
                    
                ranking = [cid for cid, _ in sorted(candidate_scores, key=lambda x: x[1], reverse=True)]
                
            return {
                "ranking": ranking,
                "solution": solution,
                "energy": raw_result.get("energy"),
                "confidence": self._calculate_confidence(raw_result)
            }
            
        elif job.job_type == JobType.BACKTRACE:
            # Extract root causes
            factors = []
            for var, value in solution.items():
                if value == 1 and var.startswith("factor_"):
                    factors.append(var)
                    
            return {
                "root_causes": factors,
                "solution": solution,
                "energy": raw_result.get("energy"),
                "confidence": self._calculate_confidence(raw_result)
            }
            
        else:
            return {
                "solution": solution,
                "energy": raw_result.get("energy"),
                "raw_result": raw_result
            }
            
    def _calculate_confidence(self, result: Dict[str, Any]) -> float:
        """Calculate confidence score from quantum result"""
        energy = result.get("energy", 0)
        
        # Simple confidence calculation based on energy
        # Lower energy = higher confidence (for minimization problems)
        if energy == float('inf'):
            return 0.0
        elif energy < -1:
            return 0.95
        elif energy < 0:
            return 0.8
        elif energy < 1:
            return 0.6
        else:
            return 0.3
            
    def _estimate_cost(self, result: Dict[str, Any]) -> float:
        """Estimate cost of quantum computation"""
        # Mock cost calculation - in practice this would be based on
        # actual Dynex pricing and resource usage
        num_reads = result.get("num_reads", 1000)
        timing = result.get("timing", {})
        total_time = timing.get("total_time", 1000)  # milliseconds
        
        # Simple cost model: $0.001 per 1000 reads + $0.0001 per second
        read_cost = (num_reads / 1000) * 0.001
        time_cost = (total_time / 1000) * 0.0001
        
        return read_cost + time_cost
        
    async def get_stats(self) -> Dict[str, Any]:
        """Get job manager statistics"""
        total_jobs = len(self.jobs)
        completed = sum(1 for job in self.jobs.values() if job.status == JobStatus.COMPLETED)
        failed = sum(1 for job in self.jobs.values() if job.status == JobStatus.FAILED)
        running = len(self.running_jobs)
        queued = len(self.job_queue)
        
        total_cost = sum(job.cost_estimate for job in self.jobs.values() if job.cost_estimate)
        avg_execution_time = np.mean([job.execution_time for job in self.jobs.values() 
                                    if job.execution_time > 0]) if self.jobs else 0
        
        return {
            "total_jobs": total_jobs,
            "completed": completed,
            "failed": failed,
            "running": running,
            "queued": queued,
            "success_rate": completed / total_jobs if total_jobs > 0 else 0,
            "total_cost": total_cost,
            "average_execution_time": avg_execution_time,
            "jobs_per_minute": self._calculate_jobs_per_minute()
        }
        
    def _calculate_jobs_per_minute(self) -> float:
        """Calculate jobs per minute over last hour"""
        current_time = time.time()
        hour_ago = current_time - 3600
        
        recent_jobs = [job for job in self.jobs.values() 
                      if job.created_at >= hour_ago and job.status == JobStatus.COMPLETED]
        
        return len(recent_jobs) / 60 if recent_jobs else 0
        
    async def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up old completed jobs"""
        cutoff_time = time.time() - (max_age_hours * 3600)
        
        old_job_ids = []
        for job_id, job in self.jobs.items():
            if (job.status in [JobStatus.COMPLETED, JobStatus.FAILED] and 
                job.created_at < cutoff_time):
                old_job_ids.append(job_id)
                
        for job_id in old_job_ids:
            del self.jobs[job_id]
            
        self.logger.info(f"Cleaned up {len(old_job_ids)} old jobs")
        
    async def shutdown(self):
        """Shutdown job manager gracefully"""
        self.logger.info("Shutting down quantum job manager")
        
        # Cancel processor task
        if self._processor_task:
            self._processor_task.cancel()
            
        # Cancel all running jobs
        for task in self.running_jobs.values():
            task.cancel()
            
        # Wait for tasks to complete
        if self.running_jobs:
            await asyncio.gather(*self.running_jobs.values(), return_exceptions=True)
            
        self.logger.info("Quantum job manager shutdown complete")

    def submit_job(self, payload: Dict[str, Any]) -> str: 
        backend = payload.get("backend", "dynex") 
        if backend == "nuco": 
            # GPU-specific: Provision + run job 
            instance_id = self.nuco.provision_gpu(payload.get("gpu_type", "RTX 4090")) 
            # Mock job execution (replace w/ actual workload upload) 
            self.nuco.pause_reboot_instance(instance_id, "start")  # Start 
            return instance_id  # Track as job_id 
        elif backend == "dynex": 
            return self.dynex.submit_job(payload) 
        raise ValueError(f"Backend {backend} unsupported") 

    def monitor_job(self, job_id: str, backend: str) -> Dict[str, Any]: 
        if backend == "nuco": 
            # Real-time: Check status + credits 
            status = self.nuco.pause_reboot_instance(job_id, "status")  # Hypothetical status call 
            balance = self.nuco.get_credit_balance() 
            return {"status": status.get("status"), "credits_remaining": balance} 
        return self.dynex.monitor_job(job_id)  # Existing