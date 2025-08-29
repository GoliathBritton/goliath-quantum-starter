"""
Sigma Select Fixes and DynexAdapter Tests (Restored)
"""

import pytest
from nqba_stack.core.dynex_adapter import DynexAdapter, DynexConfig, OptimizationResult


def test_dynex_config_creation():
    """Test DynexConfig creation"""
    config = DynexConfig(api_key="dnx_test_key_1234567890123456")
    assert config.api_key.startswith("dnx_")
    assert config.default_reads == 1000
    assert config.timeout_seconds == 300


def test_optimization_result_creation():
    """Test OptimizationResult creation"""
    result = OptimizationResult(
        success=True, samples=[{"x": 1}], energy=0.0, execution_time=0.1
    )
    assert result.success
    assert isinstance(result.samples, list)
    assert result.energy == 0.0
    assert result.execution_time > 0


def test_dynex_adapter_initialization():
    """Test DynexAdapter initialization with dummy key"""
    adapter = DynexAdapter()
    # Accept any non-empty API key (dummy or real)
    assert isinstance(adapter.config.api_key, str)
    assert len(adapter.config.api_key) > 0
    assert adapter.config.default_reads > 0
