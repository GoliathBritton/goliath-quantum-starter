"""
FLYFOX AI Quantum Hub - Registry

This module provides the capability registry for the Quantum Hub,
managing provider capabilities and problem mappings.
"""

from .capability_registry import (
    CapabilityRegistry,
    register_capability,
    get_capability,
    list_capabilities,
    unregister_capability
)

from .provider_registry import (
    ProviderRegistry,
    register_provider,
    get_provider,
    list_providers,
    unregister_provider,
    get_provider_capabilities
)

__all__ = [
    # Capability registry
    "CapabilityRegistry",
    "register_capability",
    "get_capability", 
    "list_capabilities",
    "unregister_capability",
    
    # Provider registry
    "ProviderRegistry",
    "register_provider",
    "get_provider",
    "list_providers", 
    "unregister_provider",
    "get_provider_capabilities"
]
