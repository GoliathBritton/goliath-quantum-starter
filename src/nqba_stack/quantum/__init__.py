"""
FLYFOX AI Quantum Hub

A provider-agnostic quantum computing integration hub built as an MCP-style
subsystem within NQBA Core. Provides unified access to quantum computing
resources with governance, compliance, and audit capabilities.

External Branding: FLYFOX AI Quantum
Internal: Provider adapters (Dynex, IBM Q, D-Wave, etc.)
"""

from .schemas import (
    Problem,
    Job,
    Result,
    AuditRecord,
    QuantumCapability,
    ProviderInfo,
    JobStatus,
    ProblemType,
    ResultFormat,
    QuantumOptimizationRequest,
    QuantumLLMRequest,
    PortfolioOptimizationRequest,
    ThirdPartyRegistrationRequest,
    WebhookRegistrationRequest,
    QuantumResponse,
    JobStatusResponse,
    CapabilitiesResponse,
    ProviderListResponse,
    UsageResponse
)

from .registry import (
    CapabilityRegistry,
    ProviderRegistry,
    register_capability,
    get_capability,
    list_capabilities,
    unregister_capability,
    register_provider,
    get_provider,
    list_providers,
    unregister_provider,
    get_provider_capabilities
)

__version__ = "1.0.0"
__author__ = "FLYFOX AI"
__description__ = "FLYFOX AI Quantum Integration Hub - Powered by NQBA"

__all__ = [
    # Core models
    "Problem",
    "Job",
    "Result", 
    "AuditRecord",
    "QuantumCapability",
    "ProviderInfo",
    "JobStatus",
    "ProblemType",
    "ResultFormat",
    
    # Request models
    "QuantumOptimizationRequest",
    "QuantumLLMRequest",
    "PortfolioOptimizationRequest", 
    "ThirdPartyRegistrationRequest",
    "WebhookRegistrationRequest",
    
    # Response models
    "QuantumResponse",
    "JobStatusResponse",
    "CapabilitiesResponse",
    "ProviderListResponse",
    "UsageResponse",
    
    # Registry components
    "CapabilityRegistry",
    "ProviderRegistry",
    "register_capability",
    "get_capability",
    "list_capabilities", 
    "unregister_capability",
    "register_provider",
    "get_provider",
    "list_providers",
    "unregister_provider",
    "get_provider_capabilities"
]
