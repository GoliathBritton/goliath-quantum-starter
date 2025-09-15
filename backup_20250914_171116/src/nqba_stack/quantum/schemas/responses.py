"""
FLYFOX AI Quantum Hub - Response Models

Pydantic models for API responses from the Quantum Hub.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field

from .core_models import JobStatus, ProblemType, ResultFormat


class QuantumResponse(BaseModel):
    """Base response for quantum operations."""
    
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    
    # Operation details
    operation_id: Optional[str] = Field(None, description="Unique operation identifier")
    job_id: Optional[UUID] = Field(None, description="Associated job ID")
    
    # Timing
    request_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Request timestamp")
    processing_time_ms: Optional[float] = Field(None, description="Processing time in milliseconds")
    
    # Data
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class JobStatusResponse(BaseModel):
    """Response for job status queries."""
    
    job_id: UUID = Field(..., description="Job identifier")
    status: JobStatus = Field(..., description="Current job status")
    
    # Timing information
    submitted_at: datetime = Field(..., description="When job was submitted")
    started_at: Optional[datetime] = Field(None, description="When job started execution")
    completed_at: Optional[datetime] = Field(None, description="When job completed")
    estimated_completion: Optional[datetime] = Field(None, description="Estimated completion time")
    
    # Progress information
    progress_percentage: Optional[float] = Field(None, description="Progress percentage (0-100)")
    current_step: Optional[str] = Field(None, description="Current execution step")
    
    # Resource usage
    runtime_seconds: Optional[float] = Field(None, description="Current runtime in seconds")
    cost_credits: Optional[float] = Field(None, description="Current cost in credits")
    
    # Provider information
    provider: str = Field(..., description="Quantum provider name")
    provider_job_id: Optional[str] = Field(None, description="Provider's job identifier")
    
    # Error information
    error_message: Optional[str] = Field(None, description="Error message if failed")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    
    # Result information (if completed)
    result_id: Optional[UUID] = Field(None, description="Result identifier if completed")
    result_summary: Optional[Dict[str, Any]] = Field(None, description="Result summary")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class CapabilitiesResponse(BaseModel):
    """Response for capabilities queries."""
    
    # Provider information
    provider_name: str = Field(..., description="Provider name")
    provider_version: str = Field(..., description="Provider version")
    
    # Capabilities
    supported_problem_types: List[ProblemType] = Field(..., description="Supported problem types")
    supported_result_formats: List[ResultFormat] = Field(..., description="Supported result formats")
    
    # Performance characteristics
    max_qubits: Optional[int] = Field(None, description="Maximum qubits supported")
    max_runtime: Optional[int] = Field(None, description="Maximum runtime in seconds")
    typical_runtime: Optional[int] = Field(None, description="Typical runtime in seconds")
    
    # Cost information
    cost_per_second: Optional[float] = Field(None, description="Cost per second")
    cost_per_qubit: Optional[float] = Field(None, description="Cost per qubit")
    
    # Availability
    is_available: bool = Field(..., description="Whether provider is available")
    queue_length: Optional[int] = Field(None, description="Current queue length")
    estimated_wait_time: Optional[int] = Field(None, description="Estimated wait time in seconds")
    
    # Additional capabilities
    additional_capabilities: Dict[str, Any] = Field(default_factory=dict, description="Additional capabilities")
    
    # Metadata
    last_updated: datetime = Field(default_factory=datetime.utcnow, description="Last capability update")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ProviderListResponse(BaseModel):
    """Response for provider list queries."""
    
    providers: List[Dict[str, Any]] = Field(..., description="List of available providers")
    total_count: int = Field(..., description="Total number of providers")
    
    # Filtering information
    filters_applied: Dict[str, Any] = Field(default_factory=dict, description="Applied filters")
    
    # Pagination
    page: Optional[int] = Field(None, description="Current page number")
    page_size: Optional[int] = Field(None, description="Page size")
    total_pages: Optional[int] = Field(None, description="Total number of pages")
    
    # Metadata
    response_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UsageResponse(BaseModel):
    """Response for usage statistics queries."""
    
    # Client information
    client_id: str = Field(..., description="Client identifier")
    period_start: datetime = Field(..., description="Period start date")
    period_end: datetime = Field(..., description="Period end date")
    
    # Usage statistics
    total_jobs: int = Field(..., description="Total number of jobs")
    completed_jobs: int = Field(..., description="Number of completed jobs")
    failed_jobs: int = Field(..., description="Number of failed jobs")
    
    # Resource usage
    total_runtime_seconds: float = Field(..., description="Total runtime in seconds")
    total_cost_credits: float = Field(..., description="Total cost in credits")
    average_job_runtime: float = Field(..., description="Average job runtime in seconds")
    
    # Problem type breakdown
    jobs_by_problem_type: Dict[str, int] = Field(..., description="Jobs by problem type")
    cost_by_problem_type: Dict[str, float] = Field(..., description="Cost by problem type")
    
    # Provider breakdown
    jobs_by_provider: Dict[str, int] = Field(..., description="Jobs by provider")
    cost_by_provider: Dict[str, float] = Field(..., description="Cost by provider")
    
    # Performance metrics
    success_rate: float = Field(..., description="Job success rate (0-1)")
    average_queue_time: Optional[float] = Field(None, description="Average queue time in seconds")
    
    # Limits and quotas
    quota_used: Optional[float] = Field(None, description="Quota used")
    quota_limit: Optional[float] = Field(None, description="Quota limit")
    quota_remaining: Optional[float] = Field(None, description="Remaining quota")
    
    # Metadata
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="Report generation timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class OptimizationResultResponse(BaseModel):
    """Response for optimization operation results."""
    
    # Result identification
    job_id: UUID = Field(..., description="Job identifier")
    result_id: UUID = Field(..., description="Result identifier")
    
    # Solution data
    solution: Dict[str, Any] = Field(..., description="Optimization solution")
    solution_quality: Dict[str, float] = Field(..., description="Solution quality metrics")
    
    # Optimization metrics
    energy: Optional[float] = Field(None, description="Solution energy")
    probability: Optional[float] = Field(None, description="Solution probability")
    num_occurrences: Optional[int] = Field(None, description="Number of occurrences")
    
    # Execution information
    algorithm_used: str = Field(..., description="Algorithm used")
    num_iterations: Optional[int] = Field(None, description="Number of iterations")
    convergence_info: Optional[Dict[str, Any]] = Field(None, description="Convergence information")
    
    # Validation
    is_valid: bool = Field(..., description="Whether solution is valid")
    validation_notes: Optional[str] = Field(None, description="Validation notes")
    
    # Metadata
    created_at: datetime = Field(..., description="Result creation timestamp")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class LLMResultResponse(BaseModel):
    """Response for LLM operation results."""
    
    # Result identification
    job_id: UUID = Field(..., description="Job identifier")
    result_id: UUID = Field(..., description="Result identifier")
    
    # Generated content
    response: str = Field(..., description="Generated response")
    response_tokens: int = Field(..., description="Number of tokens in response")
    
    # Model information
    model_used: str = Field(..., description="Model used for generation")
    quantum_enhancement_used: bool = Field(..., description="Whether quantum enhancement was used")
    
    # Generation parameters
    temperature: float = Field(..., description="Temperature used")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens requested")
    
    # Quality metrics
    confidence_score: Optional[float] = Field(None, description="Confidence score")
    perplexity: Optional[float] = Field(None, description="Perplexity score")
    
    # Metadata
    created_at: datetime = Field(..., description="Result creation timestamp")
    processing_time_ms: float = Field(..., description="Processing time in milliseconds")
    
    # Additional data
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
