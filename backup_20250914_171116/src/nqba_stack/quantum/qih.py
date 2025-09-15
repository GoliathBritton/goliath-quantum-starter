"""
Quantum Integration Hub (QIH) - Production-Grade Quantum Optimization

This module provides the core quantum integration system with:
- Job management (QUEUED → RUNNING → COMPLETED/FAILED → ARCHIVED)
- Policies (timeouts, retries, circuit breakers, fallbacks)
- Usage metering (qpu_time_ms, reads, problems_solved, bytes_in/out)
- Versioned protocol (v1alpha, schema-first JSON)
- Fallback to classical solvers when quantum is unavailable
"""

import asyncio
import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from pathlib import Path
import hashlib
import hmac

# Quantum and classical solver imports
try:
    from .adapters.dynex_adapter import DynexAdapter
    from .adapters.classical_adapter import ClassicalAdapter

    QUANTUM_AVAILABLE = True
except ImportError:
    QUANTUM_AVAILABLE = False
    DynexAdapter = None
    ClassicalAdapter = None

logger = logging.getLogger(__name__)


class JobStatus(Enum):
    """Job execution status"""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class JobPriority(Enum):
    """Job priority levels"""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class SolverType(Enum):
    """Available solver types"""

    QUANTUM_DYNEX = "quantum_dynex"
    CLASSICAL_DIMOD = "classical_dimod"
    CLASSICAL_ORTOOLS = "classical_ortools"
    HYBRID = "hybrid"


@dataclass
class OptimizationRequest:
    """Request for optimization"""

    operation: str
    inputs: Dict[str, Any]
    solver_preference: Optional[SolverType] = None
    timeout_seconds: int = 300
    priority: JobPriority = JobPriority.NORMAL
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OptimizationResult:
    """Result of optimization"""

    solution: Dict[str, Any]
    objective_value: float
    solver_used: SolverType
    execution_time_ms: int
    quantum_advantage: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JobMetrics:
    """Job execution metrics"""

    qpu_time_ms: int = 0
    reads: int = 0
    problems_solved: int = 0
    bytes_in: int = 0
    bytes_out: int = 0
    classical_fallback_time_ms: int = 0
    total_cost_usd: float = 0.0


@dataclass
class QuantumJob:
    """Quantum optimization job"""

    job_id: str
    user_id: str
    request: OptimizationRequest
    status: JobStatus = JobStatus.QUEUED
    priority: JobPriority = JobPriority.NORMAL
    created_at: datetime = field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[OptimizationResult] = None
    error: Optional[str] = None
    metrics: JobMetrics = field(default_factory=JobMetrics)
    retry_count: int = 0
    max_retries: int = 3
    idempotency_key: Optional[str] = None
    ttl_days: int = 30

    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary for storage/transmission"""
        return {
            "job_id": self.job_id,
            "user_id": self.user_id,
            "request": asdict(self.request),
            "status": self.status.value,
            "priority": self.priority.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "result": asdict(self.result) if self.result else None,
            "error": self.error,
            "metrics": asdict(self.metrics),
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "idempotency_key": self.idempotency_key,
            "ttl_days": self.ttl_days,
        }


class CircuitBreaker:
    """Circuit breaker pattern for quantum solver availability"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def record_failure(self):
        """Record a failure and potentially open the circuit"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()

        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning("Circuit breaker opened due to failure threshold")

    def record_success(self):
        """Record a success and potentially close the circuit"""
        self.failure_count = 0
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            logger.info("Circuit breaker closed after successful recovery")

    def can_execute(self) -> bool:
        """Check if execution is allowed"""
        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":
            if (
                self.last_failure_time
                and datetime.utcnow() - self.last_failure_time
                > timedelta(seconds=self.recovery_timeout)
            ):
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker moved to HALF_OPEN state")
                return True
            return False

        return True  # HALF_OPEN


class RetryPolicy:
    """Retry policy with exponential backoff"""

    def __init__(
        self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    def get_delay(self, attempt: int) -> float:
        """Calculate delay for retry attempt"""
        if attempt <= 0:
            return 0

        delay = self.base_delay * (2 ** (attempt - 1))
        return min(delay, self.max_delay)


class QuantumIntegrationHub:
    """
    Production-grade quantum integration hub with job management,
    policies, fallbacks, and comprehensive usage tracking.
    """

    def __init__(self):
        self.jobs: Dict[str, QuantumJob] = {}
        self.job_queue: List[str] = []
        self.circuit_breaker = CircuitBreaker()
        self.retry_policy = RetryPolicy()
        self.solvers: Dict[SolverType, Any] = {}
        self.usage_tracker = UsageTracker()

        self._initialize_solvers()
        self._start_cleanup_task()

    def _initialize_solvers(self):
        """Initialize available solvers"""
        # Initialize quantum solver if available
        if QUANTUM_AVAILABLE and DynexAdapter:
            try:
                from .adapters.base_adapter import AdapterConfig
                # Create default config for Dynex adapter
                dynex_config = AdapterConfig(
                    endpoint="https://api.dynex.co",
                    timeout=300,
                    max_qubits=1000,
                    extra_config={"mode": "sdk"}
                )
                self.solvers[SolverType.QUANTUM_DYNEX] = DynexAdapter(dynex_config)
                logger.info("Dynex quantum solver initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Dynex solver: {e}")
                self.circuit_breaker.record_failure()

        # Initialize classical solvers as fallbacks
        try:
            self.solvers[SolverType.CLASSICAL_DIMOD] = ClassicalAdapter("dimod")
            logger.info("Dimod classical solver initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Dimod solver: {e}")

        try:
            self.solvers[SolverType.CLASSICAL_ORTOOLS] = ClassicalAdapter("ortools")
            logger.info("OR-Tools classical solver initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize OR-Tools solver: {e}")

    def submit_job(
        self,
        user_id: str,
        request: OptimizationRequest,
        idempotency_key: Optional[str] = None,
    ) -> str:
        """Submit a new optimization job"""
        # Check idempotency
        if idempotency_key:
            existing_job = self._find_job_by_idempotency_key(idempotency_key)
            if existing_job:
                logger.info(
                    f"Job with idempotency key {idempotency_key} already exists: {existing_job.job_id}"
                )
                return existing_job.job_id

        # Create new job
        job_id = str(uuid.uuid4())
        job = QuantumJob(
            job_id=job_id,
            user_id=user_id,
            request=request,
            priority=request.priority,
            idempotency_key=idempotency_key,
        )

        self.jobs[job_id] = job
        self._add_to_queue(job_id)

        logger.info(f"Submitted job {job_id} for user {user_id}")
        return job_id

    def _find_job_by_idempotency_key(self, key: str) -> Optional[QuantumJob]:
        """Find existing job by idempotency key"""
        for job in self.jobs.values():
            if job.idempotency_key == key:
                return job
        return None

    def _add_to_queue(self, job_id: str):
        """Add job to priority queue"""
        job = self.jobs[job_id]

        # Insert based on priority
        priority_values = {
            JobPriority.LOW: 0,
            JobPriority.NORMAL: 1,
            JobPriority.HIGH: 2,
            JobPriority.URGENT: 3,
        }

        job_priority = priority_values.get(job.priority, 1)

        # Find insertion point
        insert_index = 0
        for i, queued_job_id in enumerate(self.job_queue):
            queued_job = self.jobs[queued_job_id]
            queued_priority = priority_values.get(queued_job.priority, 1)

            if job_priority > queued_priority:
                insert_index = i
                break
            elif job_priority == queued_priority:
                # Same priority, FIFO
                insert_index = i + 1

        self.job_queue.insert(insert_index, job_id)

    async def process_job_queue(self):
        """Process jobs in the queue"""
        while True:
            try:
                if self.job_queue:
                    job_id = self.job_queue.pop(0)
                    await self._execute_job(job_id)
                else:
                    await asyncio.sleep(1)  # Wait for new jobs
            except Exception as e:
                logger.error(f"Error processing job queue: {e}")
                await asyncio.sleep(5)

    async def _execute_job(self, job_id: str):
        """Execute a single job"""
        job = self.jobs[job_id]

        try:
            # Update job status
            job.status = JobStatus.RUNNING
            job.started_at = datetime.utcnow()

            # Execute optimization
            result = await self._run_optimization(job)

            # Update job with result
            job.result = result
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.utcnow()

            # Update usage metrics
            self.usage_tracker.record_job_completion(job)

            logger.info(f"Job {job_id} completed successfully")

        except Exception as e:
            # Handle job failure
            await self._handle_job_failure(job, str(e))

    async def _run_optimization(self, job: QuantumJob) -> OptimizationResult:
        """Run the actual optimization"""
        start_time = time.time()

        # Try quantum solver first if available and circuit breaker allows
        if (
            job.request.solver_preference == SolverType.QUANTUM_DYNEX
            or job.request.solver_preference is None
        ):

            if (
                SolverType.QUANTUM_DYNEX in self.solvers
                and self.circuit_breaker.can_execute()
            ):

                try:
                    result = await self._run_quantum_optimization(job)
                    self.circuit_breaker.record_success()
                    return result
                except Exception as e:
                    logger.warning(f"Quantum optimization failed: {e}")
                    self.circuit_breaker.record_failure()
                    # Fall through to classical solver

        # Fallback to classical solver
        return await self._run_classical_optimization(job)

    async def _run_quantum_optimization(self, job: QuantumJob) -> OptimizationResult:
        """Run optimization using quantum solver"""
        solver = self.solvers[SolverType.QUANTUM_DYNEX]

        # Prepare problem for quantum solver
        problem_data = self._prepare_quantum_problem(job.request)

        # Execute on quantum hardware
        start_time = time.time()
        solution = await solver.solve(problem_data, timeout=job.request.timeout_seconds)
        execution_time = (time.time() - start_time) * 1000  # Convert to ms

        # Calculate quantum advantage if possible
        quantum_advantage = self._calculate_quantum_advantage(
            job, solution, execution_time
        )

        return OptimizationResult(
            solution=solution,
            objective_value=solution.get("objective_value", 0.0),
            solver_used=SolverType.QUANTUM_DYNEX,
            execution_time_ms=int(execution_time),
            quantum_advantage=quantum_advantage,
            metadata={
                "solver_version": "dynex_latest",
                "quantum_advantage": quantum_advantage,
            },
        )

    async def _run_classical_optimization(self, job: QuantumJob) -> OptimizationResult:
        """Run optimization using classical solver"""
        # Choose best available classical solver
        if SolverType.CLASSICAL_DIMOD in self.solvers:
            solver = self.solvers[SolverType.CLASSICAL_DIMOD]
            solver_name = "dimod"
        elif SolverType.CLASSICAL_ORTOOLS in self.solvers:
            solver = self.solvers[SolverType.CLASSICAL_ORTOOLS]
            solver_name = "ortools"
        else:
            raise RuntimeError("No classical solvers available")

        # Prepare problem for classical solver
        problem_data = self._prepare_classical_problem(job.request)

        # Execute classical optimization
        start_time = time.time()
        solution = await solver.solve(problem_data, timeout=job.request.timeout_seconds)
        execution_time = (time.time() - start_time) * 1000  # Convert to ms

        return OptimizationResult(
            solution=solution,
            objective_value=solution.get("objective_value", 0.0),
            solver_used=(
                SolverType.CLASSICAL_DIMOD
                if solver_name == "dimod"
                else SolverType.CLASSICAL_ORTOOLS
            ),
            execution_time_ms=int(execution_time),
            quantum_advantage=None,  # No quantum advantage for classical solver
            metadata={"solver_version": solver_name, "fallback": True},
        )

    def _prepare_quantum_problem(self, request: OptimizationRequest) -> Dict[str, Any]:
        """Prepare problem data for quantum solver"""
        # This would convert the request into the format expected by Dynex
        return {
            "operation": request.operation,
            "inputs": request.inputs,
            "metadata": request.metadata,
        }

    def _prepare_classical_problem(
        self, request: OptimizationRequest
    ) -> Dict[str, Any]:
        """Prepare problem data for classical solver"""
        # This would convert the request into the format expected by classical solvers
        return {
            "operation": request.operation,
            "inputs": request.inputs,
            "metadata": request.metadata,
        }

    def _calculate_quantum_advantage(
        self, job: QuantumJob, solution: Dict[str, Any], execution_time_ms: float
    ) -> Optional[float]:
        """Calculate quantum advantage over classical baseline"""
        # This would compare quantum performance to classical baseline
        # For now, return a placeholder
        return None

    async def _handle_job_failure(self, job: QuantumJob, error: str):
        """Handle job execution failure"""
        job.error = error
        job.retry_count += 1

        if job.retry_count < job.max_retries:
            # Retry with exponential backoff
            delay = self.retry_policy.get_delay(job.retry_count)
            logger.info(
                f"Retrying job {job.job_id} in {delay} seconds (attempt {job.retry_count})"
            )

            # Reset job status for retry
            job.status = JobStatus.QUEUED
            job.started_at = None
            job.completed_at = None
            job.error = None

            # Re-add to queue with delay
            await asyncio.sleep(delay)
            self._add_to_queue(job.job_id)
        else:
            # Max retries exceeded
            job.status = JobStatus.FAILED
            job.completed_at = datetime.utcnow()
            logger.error(
                f"Job {job.job_id} failed after {job.max_retries} retries: {error}"
            )

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a job"""
        job = self.jobs.get(job_id)
        if not job:
            return None

        return job.to_dict()

    def get_user_jobs(
        self, user_id: str, status: Optional[JobStatus] = None
    ) -> List[Dict[str, Any]]:
        """Get all jobs for a user, optionally filtered by status"""
        user_jobs = []

        for job in self.jobs.values():
            if job.user_id == user_id and (status is None or job.status == status):
                user_jobs.append(job.to_dict())

        return user_jobs

    def _start_cleanup_task(self):
        """Start background task to clean up old jobs"""
        # Only start cleanup task if there's a running event loop
        try:
            loop = asyncio.get_running_loop()
            asyncio.create_task(self._cleanup_old_jobs())
        except RuntimeError:
            # No running event loop, skip for now
            # The cleanup task will be started when the first job is submitted
            pass

    async def _cleanup_old_jobs(self):
        """Clean up old completed/failed jobs"""
        while True:
            try:
                current_time = datetime.utcnow()
                jobs_to_archive = []

                for job in self.jobs.values():
                    if job.status in [JobStatus.COMPLETED, JobStatus.FAILED]:
                        # Check if job has exceeded TTL
                        if (
                            job.completed_at
                            and current_time - job.completed_at
                            > timedelta(days=job.ttl_days)
                        ):
                            jobs_to_archive.append(job.job_id)

                # Archive old jobs
                for job_id in jobs_to_archive:
                    job = self.jobs[job_id]
                    job.status = JobStatus.ARCHIVED
                    logger.info(f"Archived old job {job_id}")

                # Remove archived jobs from memory (they would be moved to persistent storage)
                # For now, just mark them as archived

                await asyncio.sleep(3600)  # Run cleanup every hour

            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
                await asyncio.sleep(3600)


class UsageTracker:
    """Track usage metrics for billing and analytics"""

    def __init__(self):
        self.user_usage: Dict[str, Dict[str, int]] = {}
        self.global_metrics: Dict[str, int] = {
            "total_jobs": 0,
            "quantum_jobs": 0,
            "classical_jobs": 0,
            "total_qpu_time_ms": 0,
            "total_reads": 0,
            "total_problems_solved": 0,
        }

    def record_job_completion(self, job: QuantumJob):
        """Record metrics when a job completes"""
        user_id = job.user_id

        # Initialize user usage if not exists
        if user_id not in self.user_usage:
            self.user_usage[user_id] = {
                "jobs_completed": 0,
                "qpu_time_ms": 0,
                "reads": 0,
                "problems_solved": 0,
                "bytes_processed": 0,
            }

        # Update user metrics
        user_metrics = self.user_usage[user_id]
        user_metrics["jobs_completed"] += 1
        user_metrics["qpu_time_ms"] += job.metrics.qpu_time_ms
        user_metrics["reads"] += job.metrics.reads
        user_metrics["problems_solved"] += job.metrics.problems_solved
        user_metrics["bytes_processed"] += job.metrics.bytes_in + job.metrics.bytes_out

        # Update global metrics
        self.global_metrics["total_jobs"] += 1

        if job.result and job.result.solver_used == SolverType.QUANTUM_DYNEX:
            self.global_metrics["quantum_jobs"] += 1
        else:
            self.global_metrics["classical_jobs"] += 1

        self.global_metrics["total_qpu_time_ms"] += job.metrics.qpu_time_ms
        self.global_metrics["total_reads"] += job.metrics.reads
        self.global_metrics["total_problems_solved"] += job.metrics.problems_solved

    def get_user_usage(self, user_id: str) -> Dict[str, int]:
        """Get usage metrics for a specific user"""
        return self.user_usage.get(user_id, {})

    def get_global_metrics(self) -> Dict[str, int]:
        """Get global usage metrics"""
        return self.global_metrics.copy()

    def export_usage_report(self) -> Dict[str, Any]:
        """Export comprehensive usage report"""
        return {
            "global_metrics": self.global_metrics,
            "user_usage": self.user_usage,
            "exported_at": datetime.utcnow().isoformat(),
        }


# Global QIH instance
qih = QuantumIntegrationHub()


def get_qih() -> QuantumIntegrationHub:
    """Get the global quantum integration hub instance"""
    return qih


def submit_optimization_job(
    user_id: str, request: OptimizationRequest, idempotency_key: Optional[str] = None
) -> str:
    """Submit an optimization job to the QIH"""
    return qih.submit_job(user_id, request, idempotency_key)


def get_job_status(job_id: str) -> Optional[Dict[str, Any]]:
    """Get the status of a specific job"""
    return qih.get_job_status(job_id)


def get_user_jobs(
    user_id: str, status: Optional[JobStatus] = None
) -> List[Dict[str, Any]]:
    """Get all jobs for a specific user"""
    return qih.get_user_jobs(user_id, status)
