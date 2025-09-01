"""
NQBA Core Integration Tests (Restored)
"""

import pytest
from nqba_stack.core.dynex_adapter import DynexAdapter
from nqba_stack.core.settings import get_settings


def test_dynex_adapter_config():
    """Test DynexAdapter config properties"""
    adapter = DynexAdapter()
    config = adapter.config
    assert config.api_key is not None
    assert isinstance(config.mainnet, bool)
    assert config.default_reads > 0


def test_settings_properties():
    """Test settings properties and validation"""
    settings = get_settings()
    assert hasattr(settings, "dynex_api_key")
    assert hasattr(settings, "environment")
    assert settings.environment in ["development", "production", "testing"]
