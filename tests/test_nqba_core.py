"""
Test NQBA-Core Components

This test file verifies the basic functionality of the NQBA platform components.
"""

import pytest
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from nqba.quantum_adapter import QuantumAdapter, BackendType
from nqba.decision_logic import DecisionLogicEngine, DecisionType
from nqba.ltc_logger import LTCLogger, LTCConfig
import numpy as np

class TestNQBACore:
    """Test class for NQBA core components"""
    
    @pytest.fixture
    async def quantum_adapter(self):
        """Create quantum adapter for testing"""
        return QuantumAdapter(
            preferred_backend="dynex",
            max_qubits=32,
            enable_fallback=True
        )
    
    @pytest.fixture
    async def decision_engine(self):
        """Create decision engine for testing"""
        return DecisionLogicEngine(
            max_qubits=32,
            enable_optimization=True,
            rule_engine_enabled=True
        )
    
    @pytest.fixture
    async def ltc_logger(self):
        """Create LTC logger for testing"""
        config = LTCConfig(
            storage_path="./test_ltc_storage",
            async_writing=False  # Disable async for testing
        )
        logger = LTCLogger(config)
        yield logger
        # Cleanup
        logger.shutdown()
        import shutil
        if os.path.exists("./test_ltc_storage"):
            shutil.rmtree("./test_ltc_storage")
    
    def test_quantum_adapter_initialization(self, quantum_adapter):
        """Test quantum adapter initialization"""
        assert quantum_adapter is not None
        assert quantum_adapter.max_qubits == 32
        assert quantum_adapter.preferred_backend == BackendType.DYNEX
        assert quantum_adapter.enable_fallback is True
    
    def test_decision_engine_initialization(self, decision_engine):
        """Test decision engine initialization"""
        assert decision_engine is not None
        assert decision_engine.max_qubits == 32
        assert decision_engine.enable_optimization is True
        assert decision_engine.rule_engine_enabled is True
        
        # Check that business rules were loaded
        rules = decision_engine.get_business_rules()
        assert len(rules) > 0
        
        # Check that optimization strategies were loaded
        strategies = decision_engine.get_optimization_strategies()
        assert len(strategies) > 0
    
    def test_ltc_logger_initialization(self, ltc_logger):
        """Test LTC logger initialization"""
        assert ltc_logger is not None
        assert ltc_logger.config.storage_path == "./test_ltc_storage"
        assert ltc_logger.config.async_writing is False
    
    @pytest.mark.asyncio
    async def test_quantum_adapter_qubo_optimization(self, quantum_adapter):
        """Test QUBO optimization with quantum adapter"""
        # Create a simple 2x2 QUBO matrix
        matrix = np.array([[1.0, 0.5], [0.5, 1.0]])
        
        result = await quantum_adapter.optimize_qubo(
            matrix=matrix,
            algorithm="qaoa"
        )
        
        assert result is not None
        assert hasattr(result, 'success')
        assert hasattr(result, 'execution_time')
        assert hasattr(result, 'backend_used')
        assert result.execution_time > 0
    
    @pytest.mark.asyncio
    async def test_decision_engine_optimization_decision(self, decision_engine):
        """Test decision engine optimization strategy selection"""
        from nqba.decision_logic import DecisionContext
        
        context = DecisionContext(
            user_id="test_user",
            session_id="test_session",
            business_context="test_context",
            priority="normal"
        )
        
        result = await decision_engine.make_decision(
            decision_type=DecisionType.OPTIMIZATION,
            context=context,
            data={
                "problem_size": 10,
                "problem_type": "qubo",
                "priority": "normal"
            }
        )
        
        assert result is not None
        assert result.success is True
        assert result.decision_type == "optimization"
        assert result.strategy_selected in ["qaoa", "quantum_annealing", "heuristic", "hybrid"]
        assert result.confidence_score > 0
    
    @pytest.mark.asyncio
    async def test_ltc_logger_operation_logging(self, ltc_logger):
        """Test LTC logger operation logging"""
        entry_id = await ltc_logger.log_operation(
            operation_type="test_operation",
            component="test_component",
            user_id="test_user",
            session_id="test_session",
            input_data={"test": "data"},
            result_data={"result": "success"}
        )
        
        assert entry_id is not None
        assert len(entry_id) > 0
        
        # Get statistics
        stats = ltc_logger.get_statistics()
        assert stats['total_entries'] > 0
    
    @pytest.mark.asyncio
    async def test_quantum_adapter_circuit_execution(self, quantum_adapter):
        """Test quantum circuit execution"""
        circuit_spec = {
            "qubits": 2,
            "gates": [
                {"type": "h", "target": 0},
                {"type": "cx", "control": 0, "target": 1}
            ]
        }
        
        result = await quantum_adapter.execute_circuit(circuit_spec)
        
        assert result is not None
        assert hasattr(result, 'success')
        assert hasattr(result, 'execution_time')
        assert hasattr(result, 'backend_used')
        assert result.execution_time > 0
    
    @pytest.mark.asyncio
    async def test_decision_engine_business_rules(self, decision_engine):
        """Test business rule processing"""
        from nqba.decision_logic import DecisionContext
        
        context = DecisionContext(
            user_id="test_user",
            session_id="test_session",
            business_context="lead_scoring",
            priority="high"
        )
        
        result = await decision_engine.make_decision(
            decision_type=DecisionType.BUSINESS_RULE,
            context=context,
            data={"size": 100, "priority": "high"}
        )
        
        assert result is not None
        assert result.success is True
        assert result.decision_type == "business_rule"
    
    def test_quantum_adapter_backend_status(self, quantum_adapter):
        """Test backend status retrieval"""
        status = quantum_adapter.get_backend_status()
        
        assert status is not None
        assert isinstance(status, dict)
        assert "dynex" in status
        assert "heuristic" in status
    
    def test_decision_engine_business_rules_retrieval(self, decision_engine):
        """Test business rules retrieval"""
        rules = decision_engine.get_business_rules()
        
        assert rules is not None
        assert isinstance(rules, list)
        assert len(rules) > 0
        
        # Check first rule structure
        first_rule = rules[0]
        assert hasattr(first_rule, 'rule_id')
        assert hasattr(first_rule, 'name')
        assert hasattr(first_rule, 'description')
        assert hasattr(first_rule, 'conditions')
        assert hasattr(first_rule, 'actions')
    
    def test_decision_engine_optimization_strategies(self, decision_engine):
        """Test optimization strategies retrieval"""
        strategies = decision_engine.get_optimization_strategies()
        
        assert strategies is not None
        assert isinstance(strategies, dict)
        assert len(strategies) > 0
        
        # Check strategy structure
        for strategy_name, strategy_info in strategies.items():
            assert "name" in strategy_info
            assert "description" in strategy_info
            assert "best_for" in strategy_info
            assert "qubit_requirements" in strategy_info
    
    @pytest.mark.asyncio
    async def test_ltc_logger_search_functionality(self, ltc_logger):
        """Test LTC logger search functionality"""
        # Log a test operation
        await ltc_logger.log_operation(
            operation_type="test_search_operation",
            component="test_component",
            user_id="test_user",
            session_id="test_session"
        )
        
        # Search for the operation
        entries = await ltc_logger.search_entries(
            operation_type="test_search_operation",
            limit=10
        )
        
        assert entries is not None
        assert isinstance(entries, list)
        assert len(entries) > 0
        
        # Check entry structure
        entry = entries[0]
        assert hasattr(entry, 'entry_id')
        assert hasattr(entry, 'timestamp')
        assert hasattr(entry, 'operation_type')
        assert hasattr(entry, 'component')
    
    def test_quantum_adapter_backend_switching(self, quantum_adapter):
        """Test quantum adapter backend switching"""
        # Test switching to heuristic backend
        quantum_adapter.switch_backend("heuristic")
        assert quantum_adapter.current_backend == BackendType.HEURISTIC
        
        # Test switching back to dynex
        quantum_adapter.switch_backend("dynex")
        assert quantum_adapter.current_backend == BackendType.DYNEX
    
    def test_quantum_adapter_validation(self, quantum_adapter):
        """Test quantum adapter input validation"""
        # Test invalid matrix
        with pytest.raises(ValueError):
            quantum_adapter._validate_qubo_matrix("invalid")
        
        # Test non-square matrix
        non_square = np.array([[1, 2], [3, 4], [5, 6]])
        with pytest.raises(ValueError):
            quantum_adapter._validate_qubo_matrix(non_square)
        
        # Test matrix too large
        large_matrix = np.zeros((100, 100))  # 100 qubits > max_qubits (32)
        with pytest.raises(ValueError):
            quantum_adapter._validate_qubo_matrix(large_matrix)
    
    def test_decision_engine_context_creation(self, decision_engine):
        """Test decision context creation"""
        from nqba.decision_logic import DecisionContext
        
        context = DecisionContext(
            user_id="test_user",
            session_id="test_session",
            business_context="test_context",
            priority="high",
            constraints={"max_cost": 100}
        )
        
        assert context.user_id == "test_user"
        assert context.session_id == "test_session"
        assert context.business_context == "test_context"
        assert context.priority == "high"
        assert context.constraints == {"max_cost": 100}

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
