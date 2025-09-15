"""
Quantum Integration Hub (QIH) API Endpoints

This module provides FastAPI endpoints for the QIH system, including:
- Job submission and management
- Job status queries
- Usage metrics and analytics
- Solver information and health checks
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
import logging

from ..quantum.qih import (
    get_qih,
    submit_optimization_job,
    get_job_status,
    get_user_jobs,
    OptimizationRequest,
    JobStatus,
    SolverType,
    JobPriority,
)
from ..core.entitlements import require_feature, Feature, get_user_tier
from ..auth import AuthManager, JWTHandler
from ..core.settings import get_settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/qih", tags=["Quantum Integration Hub"])
security = HTTPBearer()


# Pydantic models for API requests/responses
class OptimizationRequestModel(BaseModel):
    """API model for optimization requests"""

    operation: str = Field(..., description="Type of optimization operation")
    inputs: Dict[str, Any] = Field(..., description="Input data for optimization")
    solver_preference: Optional[str] = Field(None, description="Preferred solver type")
    timeout_seconds: int = Field(300, ge=1, le=3600, description="Timeout in seconds")
    priority: str = Field("normal", description="Job priority level")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class JobResponseModel(BaseModel):
    """API model for job responses"""

    job_id: str
    user_id: str
    status: str
    priority: str
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metrics: Dict[str, Any]
    retry_count: int
    max_retries: int


class JobStatusResponseModel(BaseModel):
    """API model for job status responses"""

    job_id: str
    status: str
    progress: Optional[float] = None
    estimated_completion: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class UsageMetricsModel(BaseModel):
    """API model for usage metrics"""

    user_id: str
    total_jobs: int
    quantum_jobs: int
    classical_jobs: int
    total_qpu_time_ms: int
    total_reads: int
    total_problems_solved: int
    bytes_processed: int


class SolverInfoModel(BaseModel):
    """API model for solver information"""

    name: str
    type: str
    version: str
    available: bool
    supported_problems: List[str]
    health_status: str


class QIHHealthModel(BaseModel):
    """API model for QIH health status"""

    status: str
    quantum_solvers: List[SolverInfoModel]
    classical_solvers: List[SolverInfoModel]
    circuit_breaker_status: str
    active_jobs: int
    queued_jobs: int
    total_jobs_processed: int


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """Extract and verify current user from JWT token"""
    try:
        # Create JWT handler instance
        jwt_handler = JWTHandler()
        payload = jwt_handler.verify_token(credentials.credentials, "access")
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication")


@router.post("/jobs", response_model=Dict[str, str])
@require_feature(Feature.API_ACCESS)
async def submit_job(
    request: OptimizationRequestModel,
    background_tasks: BackgroundTasks,
    current_user: str = Depends(get_current_user),
):
    """
    Submit a new optimization job to the QIH

    This endpoint allows users to submit optimization problems for processing.
    Jobs are queued and processed asynchronously based on priority.
    """
    try:
        # Convert API model to internal model
        solver_pref = None
        if request.solver_preference:
            try:
                solver_pref = SolverType(request.solver_preference)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid solver preference: {request.solver_preference}",
                )

        priority = JobPriority.NORMAL
        if request.priority:
            try:
                priority = JobPriority(request.priority)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail=f"Invalid priority: {request.priority}"
                )

        # Create internal optimization request
        opt_request = OptimizationRequest(
            operation=request.operation,
            inputs=request.inputs,
            solver_preference=solver_pref,
            timeout_seconds=request.timeout_seconds,
            priority=priority,
            metadata=request.metadata,
        )

        # Generate idempotency key from request content
        import hashlib

        request_hash = hashlib.sha256(
            f"{current_user}:{request.operation}:{str(request.inputs)}".encode()
        ).hexdigest()

        # Submit job
        job_id = submit_optimization_job(current_user, opt_request, request_hash)

        logger.info(f"Job submitted successfully: {job_id} for user {current_user}")

        return {
            "job_id": job_id,
            "status": "submitted",
            "message": "Job submitted successfully and queued for processing",
        }

    except Exception as e:
        logger.error(f"Error submitting job: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit job: {str(e)}")


@router.get("/jobs/{job_id}", response_model=JobStatusResponseModel)
@require_feature(Feature.API_ACCESS)
async def get_job_status_endpoint(
    job_id: str, current_user: str = Depends(get_current_user)
):
    """
    Get the current status of a specific job

    Returns detailed information about job progress, results, and any errors.
    """
    try:
        # Get job status
        job_data = get_job_status(job_id)
        if not job_data:
            raise HTTPException(status_code=404, detail="Job not found")

        # Verify user owns this job
        if job_data["user_id"] != current_user:
            raise HTTPException(status_code=403, detail="Access denied to this job")

        # Calculate progress if job is running
        progress = None
        estimated_completion = None

        if job_data["status"] == "running" and job_data["started_at"]:
            # Simple progress estimation based on time
            import datetime

            started = datetime.datetime.fromisoformat(job_data["started_at"])
            now = datetime.datetime.utcnow()
            elapsed = (now - started).total_seconds()

            # Assume average job takes 5 minutes (adjust based on historical data)
            avg_duration = 300  # 5 minutes
            progress = min(0.95, elapsed / avg_duration)

            if progress < 0.95:
                remaining = (
                    (avg_duration - elapsed) / progress
                    if progress > 0
                    else avg_duration
                )
                estimated_completion = (
                    now + datetime.timedelta(seconds=remaining)
                ).isoformat()

        return JobStatusResponseModel(
            job_id=job_id,
            status=job_data["status"],
            progress=progress,
            estimated_completion=estimated_completion,
            result=job_data.get("result"),
            error=job_data.get("error"),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get job status: {str(e)}"
        )


@router.get("/jobs", response_model=List[JobResponseModel])
@require_feature(Feature.API_ACCESS)
async def list_user_jobs(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    current_user: str = Depends(get_current_user),
):
    """
    List all jobs for the current user

    Supports filtering by status and pagination for large job histories.
    """
    try:
        # Validate status filter
        job_status = None
        if status:
            try:
                job_status = JobStatus(status)
            except ValueError:
                raise HTTPException(
                    status_code=400, detail=f"Invalid status filter: {status}"
                )

        # Validate pagination parameters
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=400, detail="Limit must be between 1 and 100"
            )
        if offset < 0:
            raise HTTPException(status_code=400, detail="Offset must be non-negative")

        # Get user jobs
        all_jobs = get_user_jobs(current_user, job_status)

        # Apply pagination
        paginated_jobs = all_jobs[offset : offset + limit]

        # Convert to response models
        response_jobs = []
        for job_data in paginated_jobs:
            response_jobs.append(JobResponseModel(**job_data))

        return response_jobs

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error listing user jobs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list jobs: {str(e)}")


@router.get("/usage", response_model=UsageMetricsModel)
@require_feature(Feature.ADVANCED_OPTIMIZATION)
async def get_user_usage(current_user: str = Depends(get_current_user)):
    """
    Get usage metrics for the current user

    Provides comprehensive usage statistics including job counts, QPU time, and data processed.
    """
    try:
        qih = get_qih()
        usage_tracker = qih.usage_tracker

        # Get user usage
        user_usage = usage_tracker.get_user_usage(current_user)

        # Get global metrics for comparison
        global_metrics = usage_tracker.get_global_metrics()

        # Calculate quantum vs classical job counts
        total_jobs = user_usage.get("jobs_completed", 0)
        quantum_jobs = 0
        classical_jobs = 0

        # This would require tracking solver type per job in the usage tracker
        # For now, estimate based on global ratios
        if global_metrics["total_jobs"] > 0:
            quantum_ratio = (
                global_metrics["quantum_jobs"] / global_metrics["total_jobs"]
            )
            quantum_jobs = int(total_jobs * quantum_ratio)
            classical_jobs = total_jobs - quantum_jobs

        return UsageMetricsModel(
            user_id=current_user,
            total_jobs=total_jobs,
            quantum_jobs=quantum_jobs,
            classical_jobs=classical_jobs,
            total_qpu_time_ms=user_usage.get("qpu_time_ms", 0),
            total_reads=user_usage.get("reads", 0),
            total_problems_solved=user_usage.get("problems_solved", 0),
            bytes_processed=user_usage.get("bytes_processed", 0),
        )

    except Exception as e:
        logger.error(f"Error getting user usage: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get usage metrics: {str(e)}"
        )


@router.get("/solvers", response_model=List[SolverInfoModel])
@require_feature(Feature.API_ACCESS)
async def get_solver_info(current_user: str = Depends(get_current_user)):
    """
    Get information about available solvers

    Returns details about quantum and classical solvers including availability and capabilities.
    """
    try:
        qih = get_qih()
        solvers_info = []

        # Get quantum solver info
        if SolverType.QUANTUM_DYNEX in qih.solvers:
            quantum_solver = qih.solvers[SolverType.QUANTUM_DYNEX]
            solvers_info.append(
                SolverInfoModel(
                    name="Dynex Quantum",
                    type="quantum",
                    version="latest",
                    available=qih.circuit_breaker.state == "CLOSED",
                    supported_problems=["qubo", "bqm", "ising"],
                    health_status=qih.circuit_breaker.state,
                )
            )

        # Get classical solver info
        for solver_type, solver in qih.solvers.items():
            if solver_type != SolverType.QUANTUM_DYNEX:
                if hasattr(solver, "get_solver_info"):
                    solver_info = solver.get_solver_info()
                    solvers_info.append(
                        SolverInfoModel(
                            name=solver_info["name"],
                            type=solver_info["type"],
                            version=solver_info["version"],
                            available=solver_info["available"],
                            supported_problems=solver_info["supported_problems"],
                            health_status=(
                                "healthy" if solver_info["available"] else "unavailable"
                            ),
                        )
                    )

        return solvers_info

    except Exception as e:
        logger.error(f"Error getting solver info: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get solver information: {str(e)}"
        )


@router.get("/health", response_model=QIHHealthModel)
async def get_qih_health():
    """
    Get overall health status of the QIH system

    Provides system health information including solver status, job queue status, and circuit breaker state.
    """
    try:
        qih = get_qih()

        # Get solver information
        quantum_solvers = []
        classical_solvers = []

        for solver_type, solver in qih.solvers.items():
            if solver_type == SolverType.QUANTUM_DYNEX:
                quantum_solvers.append(
                    SolverInfoModel(
                        name="Dynex Quantum",
                        type="quantum",
                        version="latest",
                        available=qih.circuit_breaker.state == "CLOSED",
                        supported_problems=["qubo", "bqm", "ising"],
                        health_status=qih.circuit_breaker.state,
                    )
                )
            else:
                if hasattr(solver, "get_solver_info"):
                    solver_info = solver.get_solver_info()
                    classical_solvers.append(
                        SolverInfoModel(
                            name=solver_info["name"],
                            type=solver_info["type"],
                            version=solver_info["version"],
                            available=solver_info["available"],
                            supported_problems=solver_info["supported_problems"],
                            health_status=(
                                "healthy" if solver_info["available"] else "unavailable"
                            ),
                        )
                    )

        # Get job statistics
        active_jobs = len([j for j in qih.jobs.values() if j.status.value == "running"])
        queued_jobs = len(qih.job_queue)
        total_processed = qih.usage_tracker.global_metrics["total_jobs"]

        return QIHHealthModel(
            status="healthy" if qih.circuit_breaker.state == "CLOSED" else "degraded",
            quantum_solvers=quantum_solvers,
            classical_solvers=classical_solvers,
            circuit_breaker_status=qih.circuit_breaker.state,
            active_jobs=active_jobs,
            queued_jobs=queued_jobs,
            total_jobs_processed=total_processed,
        )

    except Exception as e:
        logger.error(f"Error getting QIH health: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get health status: {str(e)}"
        )


@router.delete("/jobs/{job_id}")
@require_feature(Feature.API_ACCESS)
async def cancel_job(job_id: str, current_user: str = Depends(get_current_user)):
    """
    Cancel a running or queued job

    Allows users to cancel jobs that are still in progress or waiting in the queue.
    """
    try:
        qih = get_qih()

        # Check if job exists
        if job_id not in qih.jobs:
            raise HTTPException(status_code=404, detail="Job not found")

        job = qih.jobs[job_id]

        # Verify user owns this job
        if job.user_id != current_user:
            raise HTTPException(status_code=403, detail="Access denied to this job")

        # Check if job can be cancelled
        if job.status.value in ["completed", "failed", "archived"]:
            raise HTTPException(
                status_code=400, detail=f"Cannot cancel job in {job.status.value} state"
            )

        # Remove from queue if queued
        if job_id in qih.job_queue:
            qih.job_queue.remove(job_id)

        # Mark as cancelled
        job.status = JobStatus.FAILED
        job.error = "Cancelled by user"
        job.completed_at = qih.jobs[job_id].__class__.completed_at.__class__.utcnow()

        logger.info(f"Job {job_id} cancelled by user {current_user}")

        return {
            "job_id": job_id,
            "status": "cancelled",
            "message": "Job cancelled successfully",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling job: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to cancel job: {str(e)}")


@router.post("/jobs/{job_id}/retry")
@require_feature(Feature.API_ACCESS)
async def retry_job(job_id: str, current_user: str = Depends(get_current_user)):
    """
    Retry a failed job

    Allows users to retry jobs that have failed, potentially with different parameters.
    """
    try:
        qih = get_qih()

        # Check if job exists
        if job_id not in qih.jobs:
            raise HTTPException(status_code=404, detail="Job not found")

        job = qih.jobs[job_id]

        # Verify user owns this job
        if job.user_id != current_user:
            raise HTTPException(status_code=403, detail="Access denied to this job")

        # Check if job can be retried
        if job.status.value != "failed":
            raise HTTPException(
                status_code=400, detail=f"Cannot retry job in {job.status.value} state"
            )

        # Reset job for retry
        job.status = JobStatus.QUEUED
        job.started_at = None
        job.completed_at = None
        job.error = None
        job.retry_count = 0

        # Re-add to queue
        qih._add_to_queue(job_id)

        logger.info(f"Job {job_id} queued for retry by user {current_user}")

        return {"job_id": job_id, "status": "queued", "message": "Job queued for retry"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrying job: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retry job: {str(e)}")


@router.get("/metrics/global")
async def get_global_metrics():
    """
    Get global QIH metrics (public endpoint)

    Provides aggregate metrics about the QIH system for monitoring and analytics.
    """
    try:
        qih = get_qih()
        metrics = qih.usage_tracker.get_global_metrics()

        # Add additional system metrics
        metrics.update(
            {
                "active_jobs": len(
                    [j for j in qih.jobs.values() if j.status.value == "running"]
                ),
                "queued_jobs": len(qih.job_queue),
                "circuit_breaker_status": qih.circuit_breaker.state,
                "available_solvers": len(qih.solvers),
            }
        )

        return metrics

    except Exception as e:
        logger.error(f"Error getting global metrics: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to get global metrics: {str(e)}"
        )
