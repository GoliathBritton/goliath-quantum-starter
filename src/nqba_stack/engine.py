"""Quantum Engine - Core execution layer for NQBA"""

import asyncio
import logging
import numpy as np
from typing import Dict, Any, Optional, List, Union
from dataclasses import dataclass
from enum import Enum
import time
import concurrent.futures

# Import our components
from .quantum_adapter import QuantumAdapter
from .decision_logic import DecisionLogicEngine

logger = logging.getLogger(__name__)

class ExecutionMode(Enum):
    """Execution modes for quantum operations"""
    SIMULATOR = "simulator"
    QUANTUM_HARDWARE = "quantum_hardware"
    NEUROMORPHIC = "neuromorphic"
    HYBRID = "hybrid"

class QuantumState(Enum):
    """Quantum state representations"""
    SUPERPOSITION = "superposition"
    ENTANGLED = "entangled"
    MEASURED = "measured"
    COLLAPSED = "collapsed"

@dataclass
class ExecutionResult:
    """Result from quantum execution"""
    success: bool
    result_data: Optional[Dict[str, Any]] = None
    qubits_used: int = 0
    execution_time: float = 0.0
    backend_used: str = "unknown"
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class NQBAEngine:
    """Neuromorphic Quantum Business Architecture Engine"""
    
    def __init__(self, 
                 mode: ExecutionMode = ExecutionMode.SIMULATOR,
                 max_qubits: int = 64,
                 enable_optimization: bool = True,
                 optimization_level: int = 1):
        
        self.mode = mode
        self.max_qubits = max_qubits
        self.enable_optimization = enable_optimization
        self.optimization_level = optimization_level
        
        # Initialize components
        self.quantum_adapter = QuantumAdapter(
            max_qubits=max_qubits,
            preferred_backend="qiskit" if mode == ExecutionMode.SIMULATOR else "cirq"
        )
        
        self.decision_engine = DecisionLogicEngine(
            max_qubits=max_qubits,
            enable_optimization=enable_optimization
        )
        
        # Performance tracking
        self.execution_history: List[ExecutionResult] = []
        self.total_executions = 0
        self.successful_executions = 0
        
        logger.info(f"NQBA Engine initialized with mode: {mode.value}")
        logger.info(f"Max qubits: {max_qubits}")
        logger.info(f"Optimization enabled: {enable_optimization}")
    
    async def execute_quantum_circuit(self, 
                                    circuit_spec: Dict[str, Any],
                                    optimization_level: Optional[int] = None) -> ExecutionResult:
        """Execute quantum circuit with optimization"""
        start_time = time.time()
        
        try:
            # Validate circuit specification
            self._validate_circuit_spec(circuit_spec)
            
            # Apply decision logic optimization
            if self.enable_optimization:
                optimization_level = optimization_level or self.optimization_level
                optimized_circuit = await self.decision_engine.optimize_circuit(
                    circuit_spec, 
                    optimization_level
                )
            else:
                optimized_circuit = circuit_spec
            
            # Execute via quantum adapter
            result_data = await self.quantum_adapter.execute_circuit(optimized_circuit)
            
            # Create execution result
            result = ExecutionResult(
                success=True,
                result_data=result_data,
                qubits_used=circuit_spec.get("qubits", 0),
                execution_time=time.time() - start_time,
                backend_used=self.quantum_adapter.current_backend,
                metadata={
                    "optimization_level": optimization_level,
                    "original_gates": len(circuit_spec.get("gates", [])),
                    "optimized_gates": len(optimized_circuit.get("gates", [])),
                    "execution_mode": self.mode.value
                }
            )
            
            # Update statistics
            self._update_execution_statistics(result)
            
            return result
            
        except Exception as e:
            logger.error(f"Circuit execution failed: {e}")
            return ExecutionResult(
                success=False,
                execution_time=time.time() - start_time,
                error_message=str(e),
                qubits_used=circuit_spec.get("qubits", 0)
            )
    
    async def optimize_qubo(self, 
                           qubo_matrix: np.ndarray,
                           algorithm: str = "qaoa",
                           parameters: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """Optimize QUBO problem using quantum algorithms"""
        start_time = time.time()
        
        try:
            # Validate QUBO matrix
            self._validate_qubo_matrix(qubo_matrix)
            
            # Convert QUBO to quantum circuit
            circuit_spec = self._qubo_to_circuit(qubo_matrix, algorithm, parameters)
            
            # Execute optimization
            result = await self.execute_quantum_circuit(circuit_spec, optimization_level=2)
            
            # Extract optimization results
            if result.success and result.result_data:
                result.metadata = {
                    **result.metadata,
                    "algorithm": algorithm,
                    "qubo_size": qubo_matrix.shape[0],
                    "optimal_value": self._extract_optimal_value(result.result_data),
                    "solution_vector": self._extract_solution_vector(result.result_data)
                }
            
            return result
            
        except Exception as e:
            logger.error(f"QUBO optimization failed: {e}")
            return ExecutionResult(
                success=False,
                execution_time=time.time() - start_time,
                error_message=str(e)
            )
    
    async def run_quantum_ml_pipeline(self,
                                    data: np.ndarray,
                                    algorithm: str = "qsvm",
                                    parameters: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """Run quantum machine learning pipeline"""
        start_time = time.time()
        
        try:
            # Validate data
            self._validate_ml_data(data)
            
            # Convert ML problem to quantum circuit
            circuit_spec = self._ml_to_circuit(data, algorithm, parameters)
            
            # Execute ML pipeline
            result = await self.execute_quantum_circuit(circuit_spec, optimization_level=1)
            
            # Extract ML results
            if result.success and result.result_data:
                result.metadata = {
                    **result.metadata,
                    "algorithm": algorithm,
                    "data_shape": data.shape,
                    "accuracy": self._extract_ml_accuracy(result.result_data),
                    "predictions": self._extract_ml_predictions(result.result_data)
                }
            
            return result
            
        except Exception as e:
            logger.error(f"ML pipeline failed: {e}")
            return ExecutionResult(
                success=False,
                execution_time=time.time() - start_time,
                error_message=str(e)
            )
    
    def get_execution_statistics(self) -> Dict[str, Any]:
        """Get execution performance statistics"""
        success_rate = (self.successful_executions / self.total_executions 
                       if self.total_executions > 0 else 0.0)
        
        return {
            "total_executions": self.total_executions,
            "successful_executions": self.successful_executions,
            "success_rate": success_rate,
            "execution_mode": self.mode.value,
            "max_qubits": self.max_qubits,
            "optimization_enabled": self.enable_optimization,
            "average_execution_time": self._calculate_average_execution_time()
        }
    
    def reset_state(self):
        """Reset engine state and statistics"""
        self.execution_history.clear()
        self.total_executions = 0
        self.successful_executions = 0
        logger.info("NQBA Engine state reset")
    
    def _validate_circuit_spec(self, circuit_spec: Dict[str, Any]):
        """Validate quantum circuit specification"""
        if not isinstance(circuit_spec, dict):
            raise ValueError("Circuit specification must be a dictionary")
        
        if "qubits" not in circuit_spec:
            raise ValueError("Circuit must specify number of qubits")
        
        if circuit_spec["qubits"] > self.max_qubits:
            raise ValueError(f"Circuit qubits {circuit_spec['qubits']} exceed max {self.max_qubits}")
        
        if "gates" not in circuit_spec:
            raise ValueError("Circuit must specify gates")
    
    def _validate_qubo_matrix(self, qubo_matrix: np.ndarray):
        """Validate QUBO matrix"""
        if not isinstance(qubo_matrix, np.ndarray):
            raise ValueError("QUBO matrix must be a numpy array")
        
        if qubo_matrix.ndim != 2:
            raise ValueError("QUBO matrix must be 2-dimensional")
        
        if qubo_matrix.shape[0] != qubo_matrix.shape[1]:
            raise ValueError("QUBO matrix must be square")
        
        if qubo_matrix.shape[0] > self.max_qubits:
            raise ValueError(f"QUBO size {qubo_matrix.shape[0]} exceed max qubits {self.max_qubits}")
    
    def _validate_ml_data(self, data: np.ndarray):
        """Validate machine learning data"""
        if not isinstance(data, np.ndarray):
            raise ValueError("ML data must be a numpy array")
        
        if data.size == 0:
            raise ValueError("ML data cannot be empty")
        
        if data.size > self.max_qubits ** 2:
            raise ValueError(f"ML data size {data.size} exceed max qubits {self.max_qubits}")
    
    def _qubo_to_circuit(self, 
                         qubo_matrix: np.ndarray, 
                         algorithm: str, 
                         parameters: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Convert QUBO problem to quantum circuit"""
        n = qubo_matrix.shape[0]
        
        # Basic circuit structure
        circuit = {
            "qubits": n,
            "gates": [],
            "measurements": list(range(n))
        }
        
        # Add algorithm-specific gates
        if algorithm == "qaoa":
            circuit["gates"] = self._create_qaoa_circuit(qubo_matrix, parameters)
        elif algorithm == "vqe":
            circuit["gates"] = self._create_vqe_circuit(qubo_matrix, parameters)
        else:
            # Default to simple parameterized circuit
            circuit["gates"] = self._create_parameterized_circuit(n, parameters)
        
        return circuit
    
    def _ml_to_circuit(self, 
                       data: np.ndarray, 
                       algorithm: str, 
                       parameters: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Convert ML problem to quantum circuit"""
        n_features = min(data.shape[1], self.max_qubits)
        
        circuit = {
            "qubits": n_features,
            "gates": [],
            "measurements": list(range(n_features))
        }
        
        # Add algorithm-specific gates
        if algorithm == "qsvm":
            circuit["gates"] = self._create_qsvm_circuit(n_features, parameters)
        elif algorithm == "qgan":
            circuit["gates"] = self._create_qgan_circuit(n_features, parameters)
        else:
            # Default to feature encoding circuit
            circuit["gates"] = self._create_feature_encoding_circuit(n_features, parameters)
        
        return circuit
    
    def _create_qaoa_circuit(self, qubo_matrix: np.ndarray, parameters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create QAOA circuit for QUBO optimization"""
        n = qubo_matrix.shape[0]
        p = parameters.get("p", 1) if parameters else 1
        
        gates = []
        
        # Initial Hadamard gates
        for i in range(n):
            gates.append({"type": "h", "target": i})
        
        # QAOA layers
        for layer in range(p):
            # Cost Hamiltonian
            for i in range(n):
                for j in range(i+1, n):
                    if qubo_matrix[i, j] != 0:
                        gates.append({"type": "rz", "target": i, "angle": f"gamma_{layer}"})
                        gates.append({"type": "rz", "target": j, "angle": f"gamma_{layer}"})
                        gates.append({"type": "cx", "control": i, "target": j})
                        gates.append({"type": "rz", "target": j, "angle": f"gamma_{layer}"})
                        gates.append({"type": "cx", "control": i, "target": j})
            
            # Mixing Hamiltonian
            for i in range(n):
                gates.append({"type": "rx", "target": i, "angle": f"beta_{layer}"})
        
        return gates
    
    def _create_vqe_circuit(self, qubo_matrix: np.ndarray, parameters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create VQE circuit for QUBO optimization"""
        n = qubo_matrix.shape[0]
        
        gates = []
        
        # Ansatz circuit
        for i in range(n):
            gates.append({"type": "ry", "target": i, "angle": f"theta_{i}"})
        
        # Entangling layers
        for i in range(n-1):
            gates.append({"type": "cx", "control": i, "target": i+1})
        
        return gates
    
    def _create_qsvm_circuit(self, n_features: int, parameters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create QSVM circuit for classification"""
        gates = []
        
        # Feature encoding
        for i in range(n_features):
            gates.append({"type": "ry", "target": i, "angle": f"phi_{i}"})
        
        # Kernel computation
        gates.append({"type": "h", "target": n_features})
        gates.append({"type": "cx", "control": 0, "target": n_features})
        
        return gates
    
    def _create_qgan_circuit(self, n_features: int, parameters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create QGAN circuit for generative modeling"""
        gates = []
        
        # Generator circuit
        for i in range(n_features):
            gates.append({"type": "ry", "target": i, "angle": f"theta_{i}"})
            gates.append({"type": "rz", "target": i, "angle": f"phi_{i}"})
        
        return gates
    
    def _create_parameterized_circuit(self, n_qubits: int, parameters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create generic parameterized circuit"""
        gates = []
        
        for i in range(n_qubits):
            gates.append({"type": "ry", "target": i, "angle": f"theta_{i}"})
            gates.append({"type": "rz", "target": i, "angle": f"phi_{i}"})
        
        return gates
    
    def _create_feature_encoding_circuit(self, n_features: int, parameters: Optional[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create feature encoding circuit"""
        gates = []
        
        for i in range(n_features):
            gates.append({"type": "ry", "target": i, "angle": f"phi_{i}"})
        
        return gates
    
    def _extract_optimal_value(self, result_data: Dict[str, Any]) -> Optional[float]:
        """Extract optimal value from result data"""
        return result_data.get("optimal_value")
    
    def _extract_solution_vector(self, result_data: Dict[str, Any]) -> Optional[np.ndarray]:
        """Extract solution vector from result data"""
        solution = result_data.get("solution")
        if solution is not None:
            return np.array(solution)
        return None
    
    def _extract_ml_accuracy(self, result_data: Dict[str, Any]) -> Optional[float]:
        """Extract ML accuracy from result data"""
        return result_data.get("accuracy")
    
    def _extract_ml_predictions(self, result_data: Dict[str, Any]) -> Optional[np.ndarray]:
        """Extract ML predictions from result data"""
        predictions = result_data.get("predictions")
        if predictions is not None:
            return np.array(predictions)
        return None
    
    def _update_execution_statistics(self, result: ExecutionResult):
        """Update execution statistics"""
        self.total_executions += 1
        if result.success:
            self.successful_executions += 1
        
        self.execution_history.append(result)
        
        # Keep only last 1000 executions in memory
        if len(self.execution_history) > 1000:
            self.execution_history = self.execution_history[-1000:]
    
    def _calculate_average_execution_time(self) -> float:
        """Calculate average execution time"""
        if not self.execution_history:
            return 0.0
        
        total_time = sum(result.execution_time for result in self.execution_history)
        return total_time / len(self.execution_history)
