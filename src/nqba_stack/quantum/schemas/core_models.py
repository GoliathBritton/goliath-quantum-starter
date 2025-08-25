"""
FLYFOX AI Quantum Hub - Core Data Models

Core Pydantic models for the Quantum Hub, defining the fundamental
data structures for problems, jobs, results, and audit records.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator


class JobStatus(str, Enum):
    """Job execution status enumeration."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class ProblemType(str, Enum):
    """Types of quantum problems supported."""
    QUBO = "qubo"
    ISING = "ising"
    MAXCUT = "maxcut"
    SCHEDULING = "scheduling"
    ROUTING = "routing"
    KNAPSACK = "knapsack"
    PORTFOLIO_OPTIMIZATION = "portfolio_optimization"
    ENERGY_OPTIMIZATION = "energy_optimization"
    LEAD_SCORING = "lead_scoring"
    CUSTOM = "custom"


class ResultFormat(str, Enum):
    """Supported result formats."""
    JSON = "json"
    BINARY = "binary"
    TEXT = "text"
    QUANTUM_STATE = "quantum_state"
    OPTIMIZATION_RESULT = "optimization_result"


class Problem(BaseModel):
    """Core problem definition for quantum computation."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique problem identifier")
    type: ProblemType = Field(..., description="Type of quantum problem")
    name: str = Field(..., description="Human-readable problem name")
    description: Optional[str] = Field(None, description="Problem description")
    
    # Problem data
    data: Dict[str, Any] = Field(..., description="Problem-specific data")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Problem parameters")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: str = Field(..., description="Client identifier")
    tags: List[str] = Field(default_factory=list, description="Problem tags")
    
    # Constraints
    max_runtime: Optional[int] = Field(None, description="Maximum runtime in seconds")
    cost_limit: Optional[float] = Field(None, description="Maximum cost in credits")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class Job(BaseModel):
    """Job execution record."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique job identifier")
    problem_id: UUID = Field(..., description="Associated problem ID")
    provider: str = Field(..., description="Quantum provider name")
    
    # Status tracking
    status: JobStatus = Field(default=JobStatus.PENDING, description="Current job status")
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    started_at: Optional[datetime] = Field(None, description="When job started execution")
    completed_at: Optional[datetime] = Field(None, description="When job completed")
    
    # Provider-specific data
    provider_job_id: Optional[str] = Field(None, description="Provider's job identifier")
    provider_metadata: Dict[str, Any] = Field(default_factory=dict, description="Provider-specific metadata")
    
    # Execution metrics
    runtime_seconds: Optional[float] = Field(None, description="Actual runtime in seconds")
    cost_credits: Optional[float] = Field(None, description="Cost in credits")
    
    # Error handling
    error_message: Optional[str] = Field(None, description="Error message if failed")
    error_code: Optional[str] = Field(None, description="Error code if failed")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class Result(BaseModel):
    """Quantum computation result."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique result identifier")
    job_id: UUID = Field(..., description="Associated job ID")
    
    # Result data
    data: Dict[str, Any] = Field(..., description="Result data")
    format: ResultFormat = Field(default=ResultFormat.JSON, description="Result format")
    
    # Quality metrics
    energy: Optional[float] = Field(None, description="Solution energy (for optimization)")
    probability: Optional[float] = Field(None, description="Solution probability")
    num_occurrences: Optional[int] = Field(None, description="Number of occurrences")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    processing_time_ms: Optional[float] = Field(None, description="Result processing time")
    
    # Validation
    is_valid: bool = Field(default=True, description="Whether result passed validation")
    validation_notes: Optional[str] = Field(None, description="Validation notes")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class AuditRecord(BaseModel):
    """LTC audit record for quantum operations."""
    
    id: UUID = Field(default_factory=uuid4, description="Unique audit record ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Operation details
    operation: str = Field(..., description="Operation performed")
    resource_id: Optional[str] = Field(None, description="Resource identifier")
    client_id: str = Field(..., description="Client identifier")
    
    # Data classification
    data_classification: str = Field(..., description="Data classification level")
    jurisdiction: Optional[str] = Field(None, description="Jurisdiction")
    
    # Compliance
    compliance_checks: List[str] = Field(default_factory=list, description="Compliance checks performed")
    policy_violations: List[str] = Field(default_factory=list, description="Policy violations")
    
    # Metrics
    cost_impact: Optional[float] = Field(None, description="Cost impact")
    energy_impact: Optional[float] = Field(None, description="Energy impact")
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    ltc_hash: Optional[str] = Field(None, description="LTC hash for immutability")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class QuantumCapability(BaseModel):
    """Quantum provider capability definition."""
    
    name: str = Field(..., description="Capability name")
    version: str = Field(..., description="Capability version")
    description: str = Field(..., description="Capability description")
    
    # Supported operations
    problem_types: List[ProblemType] = Field(..., description="Supported problem types")
    result_formats: List[ResultFormat] = Field(..., description="Supported result formats")
    
    # Performance characteristics
    max_qubits: Optional[int] = Field(None, description="Maximum qubits supported")
    max_runtime: Optional[int] = Field(None, description="Maximum runtime in seconds")
    typical_runtime: Optional[int] = Field(None, description="Typical runtime in seconds")
    
    # Cost information
    cost_per_second: Optional[float] = Field(None, description="Cost per second")
    cost_per_qubit: Optional[float] = Field(None, description="Cost per qubit")
    
    # Availability
    is_available: bool = Field(default=True, description="Whether capability is available")
    maintenance_window: Optional[str] = Field(None, description="Maintenance window")
    
    # Metadata
    provider: str = Field(..., description="Provider name")
    tags: List[str] = Field(default_factory=list, description="Capability tags")


class ProviderInfo(BaseModel):
    """Quantum provider information."""
    
    name: str = Field(..., description="Provider name")
    version: str = Field(..., description="Provider version")
    description: str = Field(..., description="Provider description")
    
    # Contact information
    contact_email: Optional[str] = Field(None, description="Contact email")
    documentation_url: Optional[str] = Field(None, description="Documentation URL")
    support_url: Optional[str] = Field(None, description="Support URL")
    
    # Status
    is_active: bool = Field(default=True, description="Whether provider is active")
    last_heartbeat: Optional[datetime] = Field(None, description="Last heartbeat timestamp")
    
    # Capabilities
    capabilities: List[QuantumCapability] = Field(default_factory=list, description="Provider capabilities")
    
    # Configuration
    config: Dict[str, Any] = Field(default_factory=dict, description="Provider configuration")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
