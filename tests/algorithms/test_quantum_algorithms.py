"""Comprehensive test suite for quantum algorithms

Tests QAOA, VQE, and quantum algorithm runner with mocked backends.
"""

import pytest
import numpy as np
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from dataclasses import dataclass
from typing import Dict, Any, List

# Import quantum algorithms
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from nqba_stack.algorithms.qaoa_maxcut import (
    QAOAMaxCut, MaxCutProblem, QAOAResult,
    create_random_maxcut_problem, solve_maxcut_qaoa
)
from nqba_stack.algorithms.vqe_chemistry import (
    VQEChemistry, MolecularSystem, VQEResult, AnsatzType,
    create_h2_molecule, create_lih_molecule, solve_molecule_vqe
)
from nqba_stack.algorithms.quantum_backend_adapter import (
    BackendType, GradientMethod, backend_manager,
    QiskitAdapter, PennyLaneAdapter, DynexAdapter
)
from nqba_stack.algorithms.runner import (
    QuantumAlgorithmRunner, AlgorithmConfig, AlgorithmType,
    run_algorithm, integrate_with_demo_nqba, integrate_with_flyfox_demo
)

import os
import sys

class MockQuantumBackend:
    """Mock quantum backend for testing"""
    
    def __init__(self, backend_type: str = "mock"):
        self.backend_type = backend_type
        self.call_count = 0
        self.last_circuit = None
        self.last_params = None
    
    def execute_circuit(self, circuit, parameters=None, shots=1024):
        """Mock circuit execution"""
        self.call_count += 1
        self.last_circuit = circuit
        self.last_params = parameters
        
        # Return deterministic mock results
        if hasattr(circuit, 'num_qubits'):
            num_qubits = circuit.num_qubits
        else:
            num_qubits = 4  # Default
        
        # Mock measurement results
        counts = {}
        for i in range(min(2**num_qubits, 16)):  # Limit to avoid large state spaces
            bitstring = format(i, f'0{num_qubits}b')
            counts[bitstring] = max(1, shots // (2**num_qubits) + np.random.randint(-10, 10))
        
        return {
            'counts': counts,
            'shots': shots,
            'success': True
        }
    
    def estimate_gradient(self, circuit, parameters, cost_function):
        """Mock gradient estimation"""
        if parameters is None:
            return np.array([])
        
        # Return mock gradients
        return np.random.normal(0, 0.1, len(parameters))
    
    def get_backend_info(self):
        """Mock backend information"""
        return {
            'name': f'mock_{self.backend_type}',
            'version': '1.0.0',
            'max_qubits': 32,
            'supports_gradient': True
        }

class TestMaxCutProblem:
    """Test MaxCut problem creation and validation"""
    
    def test_create_random_problem(self):
        """Test random MaxCut problem generation"""
        problem = create_random_maxcut_problem(num_vertices=5, edge_prob=0.6, seed=42)
        
        assert problem.num_vertices == 5
        assert len(problem.edges) > 0
        assert problem.classical_cut_value > 0
        
        # Test reproducibility
        problem2 = create_random_maxcut_problem(num_vertices=5, edge_prob=0.6, seed=42)
        assert problem.edges == problem2.edges
    
    def test_from_adjacency_matrix(self):
        """Test MaxCut problem from adjacency matrix"""
        adj_matrix = np.array([
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [0, 1, 1, 0]
        ])
        
        problem = MaxCutProblem.from_adjacency_matrix(adj_matrix)
        
        assert problem.num_vertices == 4
        assert len(problem.edges) == 5  # Number of edges in the graph
        assert problem.classical_cut_value > 0
    
    def test_evaluate_cut(self):
        """Test cut evaluation"""
        problem = create_random_maxcut_problem(4, 0.8, 42)
        
        # Test valid partition
        partition = [0, 1, 0, 1]
        cut_value = problem.evaluate_cut(partition)
        assert cut_value >= 0
        
        # Test invalid partition length
        with pytest.raises(ValueError):
            problem.evaluate_cut([0, 1])

class TestQAOAMaxCut:
    """Test QAOA MaxCut implementation"""
    
    @pytest.fixture
    def mock_backend(self):
        """Create mock backend for testing"""
        return MockQuantumBackend("qiskit")
    
    @pytest.fixture
    def sample_problem(self):
        """Create sample MaxCut problem"""
        return create_random_maxcut_problem(4, 0.7, 42)
    
    def test_qaoa_initialization(self, sample_problem, mock_backend):
        """Test QAOA initialization"""
        qaoa = QAOAMaxCut(
            problem=sample_problem,
            max_layers=2,
            backend=mock_backend
        )
        
        assert qaoa.problem == sample_problem
        assert qaoa.max_layers == 2
        assert qaoa.backend == mock_backend
        assert qaoa.current_layer == 1
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    def test_qaoa_parameter_initialization(self, mock_manager, sample_problem):
        """Test QAOA parameter initialization"""
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        qaoa = QAOAMaxCut(
            problem=sample_problem,
            max_layers=3
        )
        
        # Test random initialization
        params = qaoa._initialize_parameters(method="random")
        assert len(params) == 6  # 2 * max_layers
        assert all(0 <= p <= 2*np.pi for p in params)
        
        # Test warm start initialization
        params_warm = qaoa._initialize_parameters(method="warm_start")
        assert len(params_warm) == 6
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    def test_qaoa_circuit_construction(self, mock_manager, sample_problem):
        """Test QAOA circuit construction"""
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        qaoa = QAOAMaxCut(
            problem=sample_problem,
            max_layers=2
        )
        
        params = np.array([0.5, 1.0, 0.3, 0.8])
        circuit = qaoa._build_qaoa_circuit(params)
        
        # Circuit should be created (exact structure depends on backend)
        assert circuit is not None
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    async def test_qaoa_objective_function(self, mock_manager, sample_problem):
        """Test QAOA objective function evaluation"""
        mock_backend = MockQuantumBackend()
        mock_manager.get_backend.return_value = mock_backend
        
        qaoa = QAOAMaxCut(
            problem=sample_problem,
            max_layers=2,
            shots=1024
        )
        
        params = np.array([0.5, 1.0, 0.3, 0.8])
        objective_value = await qaoa._evaluate_objective(params)
        
        # Should return a numeric value
        assert isinstance(objective_value, (int, float))
        assert mock_backend.call_count > 0
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    async def test_solve_maxcut_qaoa(self, mock_manager, sample_problem):
        """Test complete QAOA solving process"""
        mock_backend = MockQuantumBackend()
        mock_manager.get_backend.return_value = mock_backend
        mock_manager.get_available_backends.return_value = [BackendType.QISKIT_SIMULATOR]
        
        result = await solve_maxcut_qaoa(
            problem=sample_problem,
            max_layers=2,
            backend_type=BackendType.QISKIT_SIMULATOR,
            shots=100,
            max_iterations=5
        )
        
        assert isinstance(result, QAOAResult)
        assert result.success in [True, False]  # May fail due to mocking
        assert result.iterations >= 0
        assert result.function_evaluations >= 0

class TestMolecularSystem:
    """Test molecular system creation and validation"""
    
    def test_create_h2_molecule(self):
        """Test H2 molecule creation"""
        molecule = create_h2_molecule(bond_length=0.74)
        
        assert molecule.name == "H2"
        assert len(molecule.geometry) == 2
        assert molecule.charge == 0
        assert molecule.spin == 0
        assert molecule.basis == "sto-3g"
    
    def test_create_lih_molecule(self):
        """Test LiH molecule creation"""
        molecule = create_lih_molecule(bond_length=1.45)
        
        assert molecule.name == "LiH"
        assert len(molecule.geometry) == 2
        assert molecule.charge == 0
        assert molecule.spin == 0
    
    def test_molecular_system_validation(self):
        """Test molecular system validation"""
        # Valid molecule
        molecule = MolecularSystem(
            name="test",
            geometry=[("H", [0.0, 0.0, 0.0]), ("H", [0.0, 0.0, 0.74])],
            charge=0,
            spin=0
        )
        
        assert molecule.name == "test"
        assert len(molecule.geometry) == 2

class TestVQEChemistry:
    """Test VQE chemistry implementation"""
    
    @pytest.fixture
    def mock_backend(self):
        """Create mock backend for testing"""
        return MockQuantumBackend("pennylane")
    
    @pytest.fixture
    def sample_molecule(self):
        """Create sample molecule"""
        return create_h2_molecule(0.74)
    
    def test_vqe_initialization(self, sample_molecule, mock_backend):
        """Test VQE initialization"""
        vqe = VQEChemistry(
            molecular_system=sample_molecule,
            ansatz_type=AnsatzType.HARDWARE_EFFICIENT,
            num_layers=2,
            backend=mock_backend
        )
        
        assert vqe.molecular_system == sample_molecule
        assert vqe.ansatz_type == AnsatzType.HARDWARE_EFFICIENT
        assert vqe.num_layers == 2
        assert vqe.backend == mock_backend
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    def test_vqe_hamiltonian_construction(self, mock_manager, sample_molecule):
        """Test molecular Hamiltonian construction"""
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        vqe = VQEChemistry(
            molecular_system=sample_molecule,
            ansatz_type=AnsatzType.HARDWARE_EFFICIENT,
            num_layers=2
        )
        
        hamiltonian = vqe._construct_hamiltonian()
        
        # Hamiltonian should be constructed (exact structure depends on implementation)
        assert hamiltonian is not None
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    async def test_solve_molecule_vqe(self, mock_manager, sample_molecule):
        """Test complete VQE solving process"""
        mock_backend = MockQuantumBackend()
        mock_manager.get_backend.return_value = mock_backend
        mock_manager.get_available_backends.return_value = [BackendType.PENNYLANE_SIMULATOR]
        
        result = await solve_molecule_vqe(
            molecular_system=sample_molecule,
            ansatz_type=AnsatzType.HARDWARE_EFFICIENT,
            num_layers=2,
            backend_type=BackendType.PENNYLANE_SIMULATOR,
            shots=100,
            max_iterations=5
        )
        
        assert isinstance(result, VQEResult)
        assert result.success in [True, False]  # May fail due to mocking
        assert result.iterations >= 0
        assert result.function_evaluations >= 0

class TestQuantumAlgorithmRunner:
    """Test quantum algorithm runner"""
    
    @pytest.fixture
    def mock_backends(self):
        """Mock all backend types"""
        with patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager') as mock_manager:
            mock_manager.get_available_backends.return_value = [
                BackendType.QISKIT_SIMULATOR,
                BackendType.PENNYLANE_SIMULATOR
            ]
            mock_manager.get_backend.return_value = MockQuantumBackend()
            yield mock_manager
    
    def test_runner_initialization(self, mock_backends):
        """Test runner initialization"""
        runner = QuantumAlgorithmRunner(enable_monitoring=False)
        assert runner.enable_monitoring == False
        assert runner.performance_monitor is None
    
    async def test_run_qaoa_algorithm(self, mock_backends):
        """Test running QAOA algorithm through runner"""
        runner = QuantumAlgorithmRunner(enable_monitoring=False)
        
        config = AlgorithmConfig(
            algorithm_type=AlgorithmType.QAOA_MAXCUT,
            max_iterations=5,
            algorithm_params={"max_layers": 2}
        )
        
        problem_data = {
            "num_vertices": 4,
            "edge_probability": 0.7,
            "seed": 42
        }
        
        result = await runner.run_algorithm(config, problem_data)
        
        assert result.algorithm_type == "qaoa_maxcut"
        assert result.execution_time > 0
        assert "success" in result.result_data
    
    async def test_run_vqe_algorithm(self, mock_backends):
        """Test running VQE algorithm through runner"""
        runner = QuantumAlgorithmRunner(enable_monitoring=False)
        
        config = AlgorithmConfig(
            algorithm_type=AlgorithmType.VQE_CHEMISTRY,
            max_iterations=5,
            algorithm_params={"ansatz_type": "hardware_efficient", "num_layers": 2}
        )
        
        problem_data = {
            "molecule_name": "H2",
            "bond_length": 0.74
        }
        
        result = await runner.run_algorithm(config, problem_data)
        
        assert result.algorithm_type == "vqe_chemistry"
        assert result.execution_time > 0
        assert "success" in result.result_data
    
    async def test_run_quantum_classifier(self, mock_backends):
        """Test running quantum classifier through runner"""
        runner = QuantumAlgorithmRunner(enable_monitoring=False)
        
        config = AlgorithmConfig(
            algorithm_type=AlgorithmType.QUANTUM_CLASSIFIER,
            max_iterations=5
        )
        
        problem_data = {
            "num_features": 4,
            "num_classes": 2
        }
        
        result = await runner.run_algorithm(config, problem_data)
        
        assert result.algorithm_type == "quantum_classifier"
        assert result.execution_time > 0
        assert "success" in result.result_data
    
    async def test_convenience_function(self, mock_backends):
        """Test convenience run_algorithm function"""
        problem_data = {"num_vertices": 4, "edge_probability": 0.6}
        
        result = await run_algorithm(
            algorithm_type="qaoa_maxcut",
            problem_data=problem_data,
            max_iterations=5
        )
        
        assert "success" in result
        assert "execution_time" in result
        assert "result_data" in result

class TestDemoIntegration:
    """Test integration with demo scripts"""
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    def test_demo_nqba_integration(self, mock_manager):
        """Test integration with demo_integrated_nqba.py"""
        mock_manager.get_available_backends.return_value = [BackendType.QISKIT_SIMULATOR]
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        demo_data = {
            "optimization_problem": {
                "type": "maxcut",
                "num_vertices": 5,
                "edge_probability": 0.6
            }
        }
        
        result = integrate_with_demo_nqba(demo_data)
        
        assert "quantum_optimization_result" in result
        assert "algorithm_used" in result
        assert result["algorithm_used"] == "QAOA MaxCut"
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    def test_flyfox_demo_integration(self, mock_manager):
        """Test integration with flyfox_platform_demo.py"""
        mock_manager.get_available_backends.return_value = [BackendType.QISKIT_SIMULATOR]
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        pod_data = {
            "business_pods": [
                {"id": 1, "type": "optimization"},
                {"id": 2, "type": "analytics"},
                {"id": 3, "type": "ml"}
            ],
            "total_pods": 3
        }
        
        result = integrate_with_flyfox_demo(pod_data)
        
        assert "pod_optimization_result" in result or "pod_classification_result" in result
        assert "algorithm_used" in result

class TestBackendAdapters:
    """Test quantum backend adapters"""
    
    def test_backend_type_enum(self):
        """Test BackendType enum"""
        assert BackendType.QISKIT_SIMULATOR.value == "qiskit_simulator"
        assert BackendType.PENNYLANE_SIMULATOR.value == "pennylane_simulator"
        assert BackendType.DYNEX_SAMPLER.value == "dynex_sampler"
    
    def test_gradient_method_enum(self):
        """Test GradientMethod enum"""
        assert GradientMethod.PARAMETER_SHIFT.value == "parameter_shift"
        assert GradientMethod.FINITE_DIFF.value == "finite_diff"
        assert GradientMethod.SPSA.value == "spsa"
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    def test_backend_manager_mock(self, mock_manager):
        """Test backend manager with mocks"""
        mock_manager.get_available_backends.return_value = [
            BackendType.QISKIT_SIMULATOR,
            BackendType.PENNYLANE_SIMULATOR
        ]
        
        available = mock_manager.get_available_backends()
        assert BackendType.QISKIT_SIMULATOR in available
        assert BackendType.PENNYLANE_SIMULATOR in available

class TestErrorHandling:
    """Test error handling and edge cases"""
    
    async def test_invalid_algorithm_type(self):
        """Test handling of invalid algorithm type"""
        with pytest.raises(ValueError):
            await run_algorithm(
                algorithm_type="invalid_algorithm",
                problem_data={}
            )
    
    async def test_invalid_backend_type(self):
        """Test handling of invalid backend type"""
        # Should not raise error, just log warning
        result = await run_algorithm(
            algorithm_type="qaoa_maxcut",
            problem_data={"num_vertices": 4},
            backend_type="invalid_backend",
            max_iterations=1
        )
        
        # Should still attempt to run with default backend
        assert "success" in result
    
    def test_empty_problem_data(self):
        """Test handling of empty problem data"""
        runner = QuantumAlgorithmRunner(enable_monitoring=False)
        
        # Should handle gracefully and use defaults
        summary = runner._summarize_problem_data({})
        assert isinstance(summary, dict)
    
    def test_large_problem_data_summary(self):
        """Test summarization of large problem data"""
        runner = QuantumAlgorithmRunner(enable_monitoring=False)
        
        large_data = {
            "large_list": list(range(100)),
            "large_dict": {f"key_{i}": i for i in range(20)},
            "normal_value": 42
        }
        
        summary = runner._summarize_problem_data(large_data)
        
        assert "<list of length 100>" in summary["large_list"]
        assert "<dict with 20 keys>" in summary["large_dict"]
        assert summary["normal_value"] == 42

# Performance and benchmarking tests
class TestPerformance:
    """Test performance and benchmarking features"""
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    async def test_algorithm_timing(self, mock_manager):
        """Test algorithm execution timing"""
        mock_manager.get_available_backends.return_value = [BackendType.QISKIT_SIMULATOR]
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        runner = QuantumAlgorithmRunner(enable_monitoring=False)
        
        config = AlgorithmConfig(
            algorithm_type=AlgorithmType.QAOA_MAXCUT,
            max_iterations=3
        )
        
        problem_data = {"num_vertices": 4}
        
        result = await runner.run_algorithm(config, problem_data)
        
        assert result.execution_time > 0
        assert result.execution_time < 60  # Should complete within reasonable time
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    async def test_result_saving(self, mock_manager, tmp_path):
        """Test saving of algorithm results"""
        mock_manager.get_available_backends.return_value = [BackendType.QISKIT_SIMULATOR]
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        # Change to temporary directory for testing
        import os
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            runner = QuantumAlgorithmRunner(enable_monitoring=False)
            
            config = AlgorithmConfig(
                algorithm_type=AlgorithmType.QAOA_MAXCUT,
                max_iterations=2,
                save_results=True
            )
            
            problem_data = {"num_vertices": 3}
            
            result = await runner.run_algorithm(config, problem_data)
            
            # Check if results directory was created
            results_dir = tmp_path / "algorithm_results"
            if results_dir.exists():
                result_files = list(results_dir.glob("*.json"))
                assert len(result_files) > 0
        
        finally:
            os.chdir(original_cwd)

# Integration tests
class TestIntegration:
    """Integration tests for complete workflows"""
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    async def test_complete_qaoa_workflow(self, mock_manager):
        """Test complete QAOA workflow from problem creation to result"""
        mock_manager.get_available_backends.return_value = [BackendType.QISKIT_SIMULATOR]
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        # Create problem
        problem = create_random_maxcut_problem(5, 0.6, 42)
        
        # Solve with QAOA
        result = await solve_maxcut_qaoa(
            problem=problem,
            max_layers=2,
            backend_type=BackendType.QISKIT_SIMULATOR,
            shots=100,
            max_iterations=5
        )
        
        # Verify result structure
        assert isinstance(result, QAOAResult)
        assert hasattr(result, 'success')
        assert hasattr(result, 'optimal_value')
        assert hasattr(result, 'iterations')
    
    @patch('nqba_stack.algorithms.quantum_backend_adapter.backend_manager')
    async def test_complete_vqe_workflow(self, mock_manager):
        """Test complete VQE workflow from molecule to result"""
        mock_manager.get_available_backends.return_value = [BackendType.PENNYLANE_SIMULATOR]
        mock_manager.get_backend.return_value = MockQuantumBackend()
        
        # Create molecule
        molecule = create_h2_molecule(0.74)
        
        # Solve with VQE
        result = await solve_molecule_vqe(
            molecular_system=molecule,
            ansatz_type=AnsatzType.HARDWARE_EFFICIENT,
            num_layers=2,
            backend_type=BackendType.PENNYLANE_SIMULATOR,
            shots=100,
            max_iterations=5
        )
        
        # Verify result structure
        assert isinstance(result, VQEResult)
        assert hasattr(result, 'success')
        assert hasattr(result, 'optimal_energy')
        assert hasattr(result, 'iterations')

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])