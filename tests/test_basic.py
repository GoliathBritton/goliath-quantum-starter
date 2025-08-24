"""
Basic tests for Goliath Quantum
"""

import pytest
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that core modules can be imported"""
    try:
        from nqba.quantum_adapter import QuantumAdapter
        from nqba.decision_logic import DecisionLogic
        from nqba.engine import Engine
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import core modules: {e}")

def test_quantum_adapter():
    """Test QuantumAdapter initialization"""
    try:
        from nqba.quantum_adapter import QuantumAdapter
        adapter = QuantumAdapter()
        assert adapter is not None
    except Exception as e:
        pytest.fail(f"Failed to initialize QuantumAdapter: {e}")

def test_decision_logic():
    """Test DecisionLogic initialization"""
    try:
        from nqba.decision_logic import DecisionLogic
        logic = DecisionLogic()
        assert logic is not None
    except Exception as e:
        pytest.fail(f"Failed to initialize DecisionLogic: {e}")

def test_engine():
    """Test Engine initialization"""
    try:
        from nqba.engine import Engine
        engine = Engine()
        assert engine is not None
    except Exception as e:
        pytest.fail(f"Failed to initialize Engine: {e}")

def test_config():
    """Test configuration loading"""
    try:
        from utils.config import Config
        config = Config()
        assert config is not None
    except Exception as e:
        pytest.fail(f"Failed to load configuration: {e}")

def test_logger():
    """Test logger initialization"""
    try:
        from utils.logger import Logger
        logger = Logger()
        assert logger is not None
    except Exception as e:
        pytest.fail(f"Failed to initialize logger: {e}")

if __name__ == "__main__":
    pytest.main([__file__])

