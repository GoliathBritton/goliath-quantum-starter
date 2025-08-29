"""FLYFOX AI Quantum Computing Platform - Main quantum computing interface"""

import asyncio
import logging
import numpy as np
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum
import time

# Import our components
from nqba_stack.engine import NQBAEngine, ExecutionMode
from nqba_stack.quantum_adapter import QuantumAdapter
from nqba_stack.decision_logic import DecisionLogicEngine
from .sigmaeq_engine import (
    SigmaEQEngine,
    OptimizationProblem,
    ProblemType,
    OptimizationAlgorithm,
)
from .dynex_integration import DynexAPI, DynexPoUWManager, DynexNetwork, PoUWType

logger = logging.getLogger(__name__)


class QuantumMode(Enum):
    """Quantum computing modes"""

    SIMULATOR = "simulator"
    QUANTUM_HARDWARE = "quantum_hardware"
    HYBRID = "hybrid"
    NEUROMORPHIC = "neuromorphic"
    DYNEX = "dynex"


@dataclass
class OptimizationRequest:
    """Request for quantum optimization"""

    problem_type: str
    data: np.ndarray
    algorithm: str = "hybrid"
    parameters: Optional[Dict[str, Any]] = None
    enable_pouw: bool = True
    constraints: Optional[Dict[str, Any]] = None


@dataclass
class OptimizationResponse:
    """Response from quantum optimization"""

    success: bool
    solution: Optional[np.ndarray] = None
    optimal_value: Optional[float] = None
    execution_time: float = 0.0
    metadata: Optional[Dict[str, Any]] = None
    pouw_receipt: Optional[Any] = None
    error_message: Optional[str] = None


class GoliathQuantum:
    """Main FLYFOX AI Quantum computing interface"""

    def __init__(
        self,
        use_simulator: bool = True,
        apollo_mode: bool = False,
        qdllm_params: int = 400_000_000_000,
        max_qubits: int = 64,
        enable_dynex: bool = True,
        dynex_network: DynexNetwork = DynexNetwork.TESTNET,
        dynex_api_key: Optional[str] = None,
        dynex_wallet: Optional[str] = None,
    ):

        # Configuration
        self.use_simulator = use_simulator
        self.apollo_mode = apollo_mode
        self.qdllm_params = qdllm_params
        self.max_qubits = max_qubits
        self.enable_dynex = enable_dynex

        # Determine execution mode
        if use_simulator:
            self.execution_mode = ExecutionMode.SIMULATOR
        elif apollo_mode:
            self.execution_mode = ExecutionMode.NEUROMORPHIC
        else:
            self.execution_mode = ExecutionMode.QUANTUM_HARDWARE

        # Initialize core components
        self.nqba_engine = NQBAEngine(
            mode=self.execution_mode, max_qubits=max_qubits, enable_optimization=True
        )

        self.sigmaeq_engine = SigmaEQEngine(
            max_qubits=max_qubits, enable_hybrid=True, optimization_timeout=300
        )

        # Initialize Dynex integration if enabled
        self.dynex_api = None
        self.dynex_pouw_manager = None

        if enable_dynex:
            self.dynex_api = DynexAPI(
                network=dynex_network,
                api_key=dynex_api_key,
                wallet_address=dynex_wallet,
            )
            self.dynex_pouw_manager = DynexPoUWManager(self.dynex_api)

        # Performance tracking
        self.optimization_history: List[OptimizationResponse] = []
        self.total_optimizations = 0
        self.successful_optimizations = 0

        logger.info(f"FLYFOX AI Quantum Platform initialized with {max_qubits} qubits")
        logger.info(f"Execution mode: {self.execution_mode.value}")
        logger.info(f"Apollo mode: {apollo_mode}")

    async def optimize(self, request: OptimizationRequest) -> OptimizationResponse:
        """General optimization interface"""
        start_time = time.time()

        try:
            # Validate request
            self._validate_optimization_request(request)

            # Convert to optimization problem
            problem = self._convert_to_optimization_problem(request)

            # Select best algorithm
            algorithm = self._select_algorithm(request.algorithm, problem)

            # Execute optimization
            result = await self.sigmaeq_engine.optimize(problem, algorithm)

            # Create response
            response = OptimizationResponse(
                success=result.success,
                solution=result.solution,
                optimal_value=result.optimal_value,
                execution_time=time.time() - start_time,
                metadata={
                    "algorithm": algorithm.value,
                    "problem_type": problem.problem_type.value,
                    "qubits_used": problem.qubits_used,
                    "optimization_time": result.optimization_time,
                },
            )

            # Submit as PoUW if enabled
            if request.enable_pouw and self.enable_dynex:
                try:
                    pouw_receipt = await self.dynex_pouw_manager.submit_quantum_ml_work(
                        algorithm=algorithm.value,
                        data_size=request.data.size,
                        result_quality=result.quality_score,
                    )
                    response.pouw_receipt = pouw_receipt
                except Exception as e:
                    logger.warning(f"Failed to submit PoUW: {e}")

            # Update statistics
            self._update_statistics(response)

            return response

        except Exception as e:
            logger.error(f"Optimization failed: {e}")
            return OptimizationResponse(
                success=False,
                execution_time=time.time() - start_time,
                error_message=str(e),
            )

    async def optimize_qubo(
        self, qubo_matrix: np.ndarray, algorithm: str = "qaoa", enable_pouw: bool = True
    ) -> OptimizationResponse:
        """Optimize QUBO problem"""
        request = OptimizationRequest(
            problem_type="qubo",
            data=qubo_matrix,
            algorithm=algorithm,
            enable_pouw=enable_pouw,
        )
        return await self.optimize(request)

    async def run_quantum_ml(
        self, data: np.ndarray, algorithm: str = "qsvm", enable_pouw: bool = True
    ) -> OptimizationResponse:
        """Run quantum machine learning"""
        request = OptimizationRequest(
            problem_type="ml_classification",
            data=data,
            algorithm=algorithm,
            enable_pouw=enable_pouw,
        )
        return await self.optimize(request)

    async def execute_quantum_circuit(
        self, circuit_spec: Dict[str, Any], optimization_level: int = 1
    ) -> Dict[str, Any]:
        """Execute quantum circuit directly"""
        start_time = time.time()

        try:
            # Execute via NQBA engine
            result = await self.nqba_engine.execute_quantum_circuit(
                circuit_spec, optimization_level=optimization_level
            )

            return {
                "success": True,
                "result_data": result.result_data,
                "execution_time": time.time() - start_time,
                "qubits_used": result.qubits_used,
                "backend": result.backend_used,
            }

        except Exception as e:
            logger.error(f"Circuit execution failed: {e}")
            return {
                "success": False,
                "error_message": str(e),
                "execution_time": time.time() - start_time,
            }

    async def get_dynex_balance(self) -> Optional[float]:
        """Get Dynex wallet balance"""
        if not self.enable_dynex or not self.dynex_api:
            return None

        try:
            return await self.dynex_api.get_green_credits()
        except Exception as e:
            logger.error(f"Failed to get Dynex balance: {e}")
            return None

    async def get_network_status(self) -> Dict[str, Any]:
        """Get Dynex network status"""
        if not self.enable_dynex or not self.dynex_api:
            return {"connected": False, "error": "Dynex integration disabled"}

        try:
            status = await self.dynex_api.get_network_status()
            return {
                "connected": status.get("connected", False),
                "network": status.get("network", "unknown"),
                "block_height": status.get("block_height", 0),
                "peers": status.get("peers", 0),
            }
        except Exception as e:
            logger.error(f"Failed to get network status: {e}")
            return {"connected": False, "error": str(e)}

    def get_supported_algorithms(self) -> List[str]:
        """Get list of supported optimization algorithms"""
        return [alg.value for alg in OptimizationAlgorithm]

    def get_optimization_statistics(self) -> Dict[str, Any]:
        """Get optimization performance statistics"""
        success_rate = (
            self.successful_optimizations / self.total_optimizations
            if self.total_optimizations > 0
            else 0.0
        )

        return {
            "total_optimizations": self.total_optimizations,
            "successful_optimizations": self.successful_optimizations,
            "success_rate": success_rate,
            "execution_mode": self.execution_mode.value,
            "max_qubits": self.max_qubits,
            "apollo_mode": self.apollo_mode,
            "nqba_engine": self.nqba_engine.get_execution_statistics(),
            "sigmaeq_engine": self.sigmaeq_engine.get_performance_metrics(),
        }

    def get_dynex_statistics(self) -> Dict[str, Any]:
        """Get Dynex integration statistics"""
        if not self.enable_dynex:
            return {"enabled": False}

        try:
            return {
                "enabled": True,
                "network": (
                    self.dynex_api.network.value if self.dynex_api else "unknown"
                ),
                "wallet_configured": bool(
                    self.dynex_api.wallet_address if self.dynex_api else None
                ),
                "api_key_configured": bool(
                    self.dynex_api.api_key if self.dynex_api else None
                ),
            }
        except Exception as e:
            return {"enabled": True, "error": str(e)}

    async def close(self):
        """Clean up resources"""
        try:
            if self.dynex_api:
                await self.dynex_api.disconnect()
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")

    def _validate_optimization_request(self, request: OptimizationRequest):
        """Validate optimization request"""
        if not isinstance(request.data, np.ndarray):
            raise ValueError("Data must be a numpy array")

        if request.data.size == 0:
            raise ValueError("Data cannot be empty")

        if request.data.size > self.max_qubits**2:
            raise ValueError(
                f"Data size {request.data.size} exceeds max qubits {self.max_qubits}"
            )

    def _convert_to_optimization_problem(
        self, request: OptimizationRequest
    ) -> OptimizationProblem:
        """Convert request to optimization problem"""
        problem_type = (
            ProblemType.QUBO
            if request.problem_type == "qubo"
            else ProblemType.ML_CLASSIFICATION
        )

        return OptimizationProblem(
            problem_type=problem_type,
            data=request.data,
            parameters=request.parameters or {},
            constraints=request.constraints or {},
        )

    def _select_algorithm(
        self, algorithm_name: str, problem: OptimizationProblem
    ) -> OptimizationAlgorithm:
        """Select optimization algorithm"""
        try:
            return OptimizationAlgorithm(algorithm_name)
        except ValueError:
            # Default to hybrid for unknown algorithms
            return OptimizationAlgorithm.HYBRID

    def _update_statistics(self, response: OptimizationResponse):
        """Update performance statistics"""
        self.total_optimizations += 1
        if response.success:
            self.successful_optimizations += 1

        self.optimization_history.append(response)

        # Keep only last 1000 optimizations in memory
        if len(self.optimization_history) > 1000:
            self.optimization_history = self.optimization_history[-1000:]

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
