"""
FLYFOX AI Quantum Hub - Core Schemas

This module defines the core data models for the Quantum Hub,
following MCP-style architecture for provider-agnostic quantum computing.
"""

from .core_models import (
    Problem,
    Job,
    Result,
    AuditRecord,
    QuantumCapability,
    ProviderInfo,
    JobStatus,
    ProblemType,
    ResultFormat
)

from .requests import (
    QuantumOptimizationRequest,
    QuantumLLMRequest,
    PortfolioOptimizationRequest,
    ThirdPartyRegistrationRequest,
    WebhookRegistrationRequest
)

from .responses import (
    QuantumResponse,
    JobStatusResponse,
    CapabilitiesResponse,
    ProviderListResponse,
    UsageResponse
)

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
    "UsageResponse"
]
