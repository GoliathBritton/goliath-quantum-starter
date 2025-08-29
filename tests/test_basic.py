"""
Basic sanity and import tests for Goliath Quantum Starter
"""
import pytest

def test_imports():
    """Test that core modules can be imported"""
    try:
        from nqba_stack.core.dynex_adapter import DynexAdapter
        from nqba_stack.core.settings import get_settings
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import core modules: {e}")

def test_dynex_adapter_init():
    """Test DynexAdapter initialization"""
    from nqba_stack.core.dynex_adapter import DynexAdapter
    adapter = DynexAdapter()
    assert adapter.config is not None

def test_settings_load():
    """Test settings loading"""
    from nqba_stack.core.settings import get_settings
    settings = get_settings()
    assert settings is not None
    assert hasattr(settings, 'dynex_api_key')
