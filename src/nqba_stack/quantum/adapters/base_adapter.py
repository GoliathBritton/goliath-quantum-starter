"""
FLYFOX AI Quantum Hub - Base Adapter Protocol

Defines the base protocol that all quantum provider adapters must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

from ..schemas.core_models import JobStatus, ProblemType, ResultFormat


class AdapterConfig:
    """Configuration for quantum provider adapters."""
    
    def __init__(self, **kwargs):
        self.api_key: Optional[str] = kwargs.get('api_key')
        self.endpoint: str = kwargs.get('endpoint', '')
        self.timeout: int = kwargs.get('timeout', 300)
        self.max_qubits: Optional[int] = kwargs.get('max_qubits')
        self.cost_per_second: Optional[float] = kwargs.get('cost_per_second')
        self.cost_per_qubit: Optional[float] = kwargs.get('cost_per_qubit')
        self.extra_config: Dict[str, Any] = kwargs.get('extra_config', {})


class QuantumAdapter(ABC):
    """Base protocol for quantum provider adapters."""
    
    def __init__(self, config: AdapterConfig):
        self.config = config
        self.name = self.__class__.__name__
        self.version = "1.0.0"
    
    @abstractmethod
    async def submit_qubo(self, qubo_data: Dict[str, Any]) -> str:
        """Submit a QUBO problem and return job ID."""
        pass
    
    @abstractmethod
    async def poll(self, job_id: str) -> JobStatus:
        """Poll job status."""
        pass
    
    @abstractmethod
    async def result(self, job_id: str) -> Dict[str, Any]:
        """Get job results."""
        pass
    
    @abstractmethod
    async def cancel(self, job_id: str) -> bool:
        """Cancel a job."""
        pass
    
    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get provider capabilities."""
        pass
    
    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Check provider health."""
        pass
    
    async def estimate_cost(self, problem_size: int, estimated_runtime: int) -> float:
        """Estimate cost for a problem."""
        if self.config.cost_per_second:
            return self.config.cost_per_second * estimated_runtime
        elif self.config.cost_per_qubit:
            return self.config.cost_per_qubit * problem_size
        return 0.0
    
    async def validate_problem(self, problem_type: ProblemType, problem_data: Dict[str, Any]) -> bool:
        """Validate if provider can handle the problem."""
        capabilities = await self.get_capabilities()
        supported_types = capabilities.get('problem_types', [])
        return problem_type.value in supported_types

