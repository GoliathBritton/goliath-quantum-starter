"""
Test Suite for NQBA Core Integration

This module contains integration tests for core NQBA Framework components
including DynexAdapter, settings management, and configuration validation.

Test Coverage:
    - DynexAdapter initialization and configuration
    - Settings loading from environment variables
    - Configuration validation and defaults
    - API key management and security

Test Categories:
    - Integration Tests: Multi-component interactions
    - Configuration Tests: Settings and environment validation

Running Tests:
    Run all tests:
        $ pytest tests/test_nqba_core.py -v
    
    Run with coverage:
        $ pytest tests/test_nqba_core.py --cov=nqba_stack.core
    
    Run specific test:
        $ pytest tests/test_nqba_core.py::test_dynex_adapter_config -v

Prerequisites:
    - Environment variables configured in .env file
    - Valid Dynex API key (can use test/mock key for testing)

Related Modules:
    - nqba_stack/core/dynex_adapter.py: Dynex integration layer
    - nqba_stack/core/settings.py: Configuration management
    - .env.template: Environment variable template

See Also:
    - docs/DYNEX_QAAS_INTEGRATION.md: Dynex integration guide
    - docs/SECURITY_SYSTEM.md: Security best practices

Author: NQBA Framework Test Team
Version: 2.0.0
"""

import pytest
from nqba_stack.core.dynex_adapter import DynexAdapter
from nqba_stack.core.settings import get_settings


def test_dynex_adapter_config():
    """
    Test DynexAdapter Configuration Properties
    
    Verifies that the DynexAdapter correctly loads and validates
    configuration from environment variables including API keys,
    network selection, and default parameters.
    
    Test Steps:
        1. Initialize DynexAdapter instance
        2. Retrieve configuration object
        3. Validate API key is present
        4. Check mainnet flag is boolean
        5. Verify default_reads is positive integer
    
    Expected Behavior:
        - API key should be loaded from DYNEX_API_KEY env var
        - Mainnet flag should be True or False
        - Default reads should be > 0
    """
    adapter = DynexAdapter()
    config = adapter.config
    assert config.api_key is not None
    assert isinstance(config.mainnet, bool)
    assert config.default_reads > 0


def test_settings_properties():
    """
    Test Settings Properties and Validation
    
    Verifies that the settings module correctly loads configuration
    from environment variables and provides expected attributes with
    proper validation.
    
    Test Steps:
        1. Load settings using get_settings()
        2. Check for required attributes (dynex_api_key, environment)
        3. Validate environment value is in allowed set
    
    Expected Behavior:
        - Settings should have dynex_api_key attribute
        - Settings should have environment attribute
        - Environment should be one of: development, production, testing
    
    Related:
        - See .env.template for all available settings
        - See src/nqba_stack/core/settings.py for implementation
    """
    settings = get_settings()
    assert hasattr(settings, "dynex_api_key")
    assert hasattr(settings, "environment")
    assert settings.environment in ["development", "production", "testing"]
