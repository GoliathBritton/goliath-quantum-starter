"""
FLYFOX AI Quantum Hub - Base Adapter Protocol

Defines the base protocol and abstract interface that all quantum provider
adapters must implement to ensure consistent interaction with various quantum
computing backends including Dynex, IBM Quantum, Google Quantum AI, and simulators.

Architecture:
    The adapter pattern allows the NQBA Framework to work with multiple quantum
    backends through a unified interface. Each backend implements this protocol
    while handling backend-specific details internally.

Key Features:
    - Unified QUBO problem submission across all backends
    - Consistent job lifecycle management (submit, poll, result, cancel)
    - Backend capability discovery and validation
    - Cost estimation and resource management
    - Automatic retry and error handling

Adapter Lifecycle:
    1. Initialize with AdapterConfig (API keys, endpoints, etc.)
    2. Submit QUBO problem -> receive job_id
    3. Poll job status until completion
    4. Retrieve results when ready
    5. Parse and return in standard format

Concrete Implementations:
    - DynexAdapter: Neuromorphic computing via Dynex platform
    - ClassicalAdapter: Classical QUBO solver (for development/testing)
    - SimulatorAdapter: Quantum circuit simulation
    - FlyFoxQuantumAdapter: FLYFOX proprietary quantum optimizer

Example Usage:
    >>> config = AdapterConfig(
    ...     api_key="your_key",
    ...     endpoint="https://api.quantum-provider.com",
    ...     timeout=300
    ... )
    >>> adapter = ConcreteAdapter(config)
    >>> job_id = await adapter.submit_qubo(qubo_problem)
    >>> while await adapter.poll(job_id) != JobStatus.COMPLETED:
    ...     await asyncio.sleep(1)
    >>> result = await adapter.result(job_id)

Related Modules:
    - dynex_adapter.py: Dynex implementation
    - classical_adapter.py: Classical solver implementation
    - schemas/core_models.py: Data models and enums

See Also:
    - docs/quantum-hub.md: Quantum Hub architecture
    - docs/DYNEX_QAAS_INTEGRATION.md: Dynex integration guide
    - QUANTUM_ALGORITHMS_IMPLEMENTATION.md: Algorithm implementations

Author: FLYFOX AI Quantum Team
Version: 2.0.0
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime

from ..schemas.core_models import JobStatus, ProblemType, ResultFormat


class AdapterConfig:
    """
    Configuration container for quantum provider adapters.
    
    Stores all necessary configuration parameters for connecting to and
    using quantum computing backends. Supports both common parameters
    (API keys, timeouts) and provider-specific settings via extra_config.
    
    Attributes:
        api_key: Authentication key for the quantum provider
        endpoint: API endpoint URL for the provider
        timeout: Maximum time (seconds) to wait for job completion
        max_qubits: Maximum number of qubits supported by this backend
        cost_per_second: Cost in credits per second of computation
        cost_per_qubit: Cost in credits per qubit used
        extra_config: Provider-specific configuration parameters
    
    Example:
        >>> config = AdapterConfig(
        ...     api_key="sk_test_123",
        ...     endpoint="https://api.dynex.network/v1",
        ...     timeout=600,
        ...     max_qubits=64,
        ...     extra_config={"priority": "high"}
        ... )
    """

    def __init__(self, **kwargs):
        self.api_key: Optional[str] = kwargs.get("api_key")
        self.endpoint: str = kwargs.get("endpoint", "")
        self.timeout: int = kwargs.get("timeout", 300)
        self.max_qubits: Optional[int] = kwargs.get("max_qubits")
        self.cost_per_second: Optional[float] = kwargs.get("cost_per_second")
        self.cost_per_qubit: Optional[float] = kwargs.get("cost_per_qubit")
        self.extra_config: Dict[str, Any] = kwargs.get("extra_config", {})


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

    async def validate_problem(
        self, problem_type: ProblemType, problem_data: Dict[str, Any]
    ) -> bool:
        """Validate if provider can handle the problem."""
        capabilities = await self.get_capabilities()
        supported_types = capabilities.get("problem_types", [])
        return problem_type.value in supported_types
