"""
FLYFOX AI Quantum Hub - Request Models

Pydantic models for incoming API requests to the Quantum Hub.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from uuid import UUID

from pydantic import BaseModel, Field, validator

from .core_models import ProblemType, ResultFormat


class QuantumOptimizationRequest(BaseModel):
    """Request for quantum optimization operations."""
    
    # Problem definition
    problem_type: ProblemType = Field(..., description="Type of optimization problem")
    problem_data: Dict[str, Any] = Field(..., description="Problem-specific data")
    
    # Parameters
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Optimization parameters")
    constraints: Optional[Dict[str, Any]] = Field(None, description="Problem constraints")
    
    # Execution preferences
    preferred_provider: Optional[str] = Field(None, description="Preferred quantum provider")
    result_format: ResultFormat = Field(default=ResultFormat.JSON, description="Desired result format")
    
    # Resource limits
    max_runtime: Optional[int] = Field(None, description="Maximum runtime in seconds")
    cost_limit: Optional[float] = Field(None, description="Maximum cost in credits")
    
    # Metadata
    name: Optional[str] = Field(None, description="Request name for tracking")
    description: Optional[str] = Field(None, description="Request description")
    tags: List[str] = Field(default_factory=list, description="Request tags")
    
    # Client information
    client_id: str = Field(..., description="Client identifier")
    priority: Optional[str] = Field(default="normal", description="Request priority")
    
    @validator('max_runtime')
    def validate_max_runtime(cls, v):
        if v is not None and v <= 0:
            raise ValueError('max_runtime must be positive')
        return v
    
    @validator('cost_limit')
    def validate_cost_limit(cls, v):
        if v is not None and v <= 0:
            raise ValueError('cost_limit must be positive')
        return v


class QuantumLLMRequest(BaseModel):
    """Request for quantum-enhanced LLM operations."""
    
    # Input data
    prompt: str = Field(..., description="Input prompt for LLM")
    context: Optional[str] = Field(None, description="Additional context")
    
    # Model parameters
    model_name: Optional[str] = Field(None, description="Specific model to use")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
    
    # Quantum enhancement
    use_quantum_enhancement: bool = Field(default=True, description="Whether to use quantum enhancement")
    quantum_parameters: Optional[Dict[str, Any]] = Field(None, description="Quantum-specific parameters")
    
    # Output preferences
    response_format: str = Field(default="text", description="Desired response format")
    include_metadata: bool = Field(default=True, description="Whether to include metadata")
    
    # Client information
    client_id: str = Field(..., description="Client identifier")
    session_id: Optional[str] = Field(None, description="Session identifier for conversation")
    
    @validator('temperature')
    def validate_temperature(cls, v):
        if v is not None and (v < 0 or v > 2):
            raise ValueError('temperature must be between 0 and 2')
        return v
    
    @validator('max_tokens')
    def validate_max_tokens(cls, v):
        if v is not None and v <= 0:
            raise ValueError('max_tokens must be positive')
        return v


class PortfolioOptimizationRequest(BaseModel):
    """Request for portfolio optimization using quantum computing."""
    
    # Portfolio data
    assets: List[str] = Field(..., description="List of asset symbols")
    prices: List[float] = Field(..., description="Current asset prices")
    returns: Optional[List[float]] = Field(None, description="Historical returns")
    covariance_matrix: Optional[List[List[float]]] = Field(None, description="Asset covariance matrix")
    
    # Optimization parameters
    target_return: Optional[float] = Field(None, description="Target portfolio return")
    risk_tolerance: float = Field(0.5, description="Risk tolerance (0-1)")
    max_position_size: Optional[float] = Field(None, description="Maximum position size per asset")
    
    # Constraints
    budget: float = Field(..., description="Total investment budget")
    min_position_size: Optional[float] = Field(None, description="Minimum position size per asset")
    sector_constraints: Optional[Dict[str, float]] = Field(None, description="Sector allocation constraints")
    
    # Quantum parameters
    quantum_algorithm: str = Field(default="QAOA", description="Quantum algorithm to use")
    num_shots: Optional[int] = Field(None, description="Number of quantum shots")
    
    # Client information
    client_id: str = Field(..., description="Client identifier")
    portfolio_name: Optional[str] = Field(None, description="Portfolio name")
    
    @validator('risk_tolerance')
    def validate_risk_tolerance(cls, v):
        if v < 0 or v > 1:
            raise ValueError('risk_tolerance must be between 0 and 1')
        return v
    
    @validator('budget')
    def validate_budget(cls, v):
        if v <= 0:
            raise ValueError('budget must be positive')
        return v
    
    @validator('assets', 'prices')
    def validate_assets_prices_match(cls, v, values):
        if 'assets' in values and 'prices' in values:
            if len(values['assets']) != len(values['prices']):
                raise ValueError('assets and prices must have the same length')
        return v


class ThirdPartyRegistrationRequest(BaseModel):
    """Request for third-party integration registration."""
    
    # Organization information
    organization_name: str = Field(..., description="Organization name")
    organization_id: str = Field(..., description="Unique organization identifier")
    contact_email: str = Field(..., description="Primary contact email")
    
    # Integration details
    integration_name: str = Field(..., description="Integration name")
    integration_version: str = Field(..., description="Integration version")
    integration_description: str = Field(..., description="Integration description")
    
    # API access
    api_key: str = Field(..., description="API key for authentication")
    webhook_url: Optional[str] = Field(None, description="Webhook URL for notifications")
    
    # Capabilities
    supported_operations: List[str] = Field(..., description="Supported quantum operations")
    rate_limits: Optional[Dict[str, int]] = Field(None, description="Rate limits per operation")
    
    # Compliance
    data_classification: str = Field(default="public", description="Data classification level")
    jurisdictions: List[str] = Field(default_factory=list, description="Supported jurisdictions")
    
    # Metadata
    website_url: Optional[str] = Field(None, description="Organization website")
    documentation_url: Optional[str] = Field(None, description="Integration documentation")
    
    @validator('contact_email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v
    
    @validator('api_key')
    def validate_api_key(cls, v):
        if len(v) < 32:
            raise ValueError('API key must be at least 32 characters')
        return v


class WebhookRegistrationRequest(BaseModel):
    """Request for webhook registration."""
    
    # Webhook details
    url: str = Field(..., description="Webhook URL")
    events: List[str] = Field(..., description="Events to subscribe to")
    
    # Authentication
    secret: Optional[str] = Field(None, description="Webhook secret for verification")
    auth_header: Optional[str] = Field(None, description="Custom authorization header")
    
    # Configuration
    retry_count: int = Field(default=3, description="Number of retry attempts")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    
    # Client information
    client_id: str = Field(..., description="Client identifier")
    
    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v
    
    @validator('retry_count')
    def validate_retry_count(cls, v):
        if v < 0 or v > 10:
            raise ValueError('retry_count must be between 0 and 10')
        return v
    
    @validator('timeout')
    def validate_timeout(cls, v):
        if v < 1 or v > 300:
            raise ValueError('timeout must be between 1 and 300 seconds')
        return v
