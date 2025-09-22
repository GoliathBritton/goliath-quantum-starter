"""API Models - Pydantic models for request/response schemas

This module defines the data models used for API requests and responses
in the qdLLM FastAPI server.
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum

class ModelType(str, Enum):
    """Supported model types"""
    QDLLM = "qdllm"
    QNLP = "qnlp"
    QTRANSFORMER = "qtransformer"

class InferenceMode(str, Enum):
    """Inference modes"""
    STANDARD = "standard"
    QUANTUM_ENHANCED = "quantum_enhanced"
    BIDIRECTIONAL = "bidirectional"
    COHERENCE_OPTIMIZED = "coherence_optimized"

class SamplingStrategy(str, Enum):
    """Text generation sampling strategies"""
    GREEDY = "greedy"
    TOP_K = "top_k"
    TOP_P = "top_p"
    TEMPERATURE = "temperature"
    QUANTUM_SAMPLING = "quantum_sampling"

# Base Models
class BaseRequest(BaseModel):
    """Base request model"""
    request_id: Optional[str] = Field(None, description="Unique request identifier")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now, description="Request timestamp")
    
class BaseResponse(BaseModel):
    """Base response model"""
    request_id: Optional[str] = Field(None, description="Request identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    processing_time: float = Field(description="Processing time in seconds")
    success: bool = Field(description="Whether the request was successful")
    error_message: Optional[str] = Field(None, description="Error message if request failed")

# qdLLM Inference Models
class InferenceRequest(BaseRequest):
    """Request model for qdLLM inference"""
    prompt: str = Field(description="Input prompt for inference")
    model_type: ModelType = Field(default=ModelType.QDLLM, description="Type of model to use")
    inference_mode: InferenceMode = Field(default=InferenceMode.QUANTUM_ENHANCED, description="Inference mode")
    
    # Generation parameters
    max_length: int = Field(default=100, ge=1, le=2048, description="Maximum generation length")
    temperature: float = Field(default=1.0, ge=0.1, le=2.0, description="Sampling temperature")
    top_k: int = Field(default=50, ge=1, le=1000, description="Top-k sampling parameter")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p sampling parameter")
    sampling_strategy: SamplingStrategy = Field(default=SamplingStrategy.TOP_P, description="Sampling strategy")
    
    # Quantum parameters
    quantum_enhancement: bool = Field(default=True, description="Enable quantum enhancements")
    entanglement_strength: float = Field(default=0.5, ge=0.0, le=1.0, description="Quantum entanglement strength")
    coherence_preservation: float = Field(default=0.8, ge=0.0, le=1.0, description="Coherence preservation factor")
    diffusion_steps: int = Field(default=10, ge=1, le=100, description="Number of diffusion steps")
    
    # Advanced options
    return_attention: bool = Field(default=False, description="Return attention weights")
    return_hidden_states: bool = Field(default=False, description="Return hidden states")
    return_quantum_info: bool = Field(default=False, description="Return quantum-specific information")
    batch_size: int = Field(default=1, ge=1, le=32, description="Batch size for processing")
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if not v or not v.strip():
            raise ValueError('Prompt cannot be empty')
        if len(v) > 10000:
            raise ValueError('Prompt too long (max 10000 characters)')
        return v.strip()

class InferenceResponse(BaseResponse):
    """Response model for qdLLM inference"""
    generated_text: str = Field(description="Generated text")
    input_prompt: str = Field(description="Original input prompt")
    
    # Generation metadata
    num_tokens_generated: int = Field(description="Number of tokens generated")
    generation_speed: float = Field(description="Tokens per second")
    
    # Model outputs
    logits: Optional[List[List[float]]] = Field(None, description="Model logits (if requested)")
    probabilities: Optional[List[List[float]]] = Field(None, description="Token probabilities (if requested)")
    attention_weights: Optional[List[List[List[float]]]] = Field(None, description="Attention weights (if requested)")
    hidden_states: Optional[List[List[List[float]]]] = Field(None, description="Hidden states (if requested)")
    
    # Quantum information
    quantum_info: Optional[Dict[str, Any]] = Field(None, description="Quantum-specific information")
    coherence_scores: Optional[List[float]] = Field(None, description="Coherence scores per layer")
    entanglement_measures: Optional[List[float]] = Field(None, description="Entanglement measures")
    
    # Performance metrics
    inference_metrics: Dict[str, float] = Field(description="Performance metrics")

# QNLP Models
class QNLPRequest(BaseRequest):
    """Request model for QNLP processing"""
    text: str = Field(description="Input text for QNLP processing")
    
    # Processing options
    include_embeddings: bool = Field(default=True, description="Include quantum embeddings")
    include_entanglement: bool = Field(default=True, description="Include semantic entanglement analysis")
    include_coherence: bool = Field(default=True, description="Include contextual coherence analysis")
    
    # Quantum parameters
    embedding_dimension: int = Field(default=256, ge=64, le=1024, description="Embedding dimension")
    quantum_enhancement: bool = Field(default=True, description="Enable quantum enhancements")
    entanglement_threshold: float = Field(default=0.5, ge=0.0, le=1.0, description="Entanglement threshold")
    
    # Analysis depth
    analysis_depth: str = Field(default="standard", regex="^(basic|standard|deep)$", description="Analysis depth")
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        if len(v) > 50000:
            raise ValueError('Text too long (max 50000 characters)')
        return v.strip()

class QNLPResponse(BaseResponse):
    """Response model for QNLP processing"""
    input_text: str = Field(description="Original input text")
    
    # Tokenization results
    tokens: List[Dict[str, Any]] = Field(description="Quantum-enhanced tokens")
    num_tokens: int = Field(description="Number of tokens")
    
    # Embeddings
    quantum_embeddings: Optional[List[List[float]]] = Field(None, description="Quantum embeddings")
    embedding_dimension: int = Field(description="Embedding dimension")
    
    # Semantic analysis
    semantic_entanglement: Optional[Dict[str, Any]] = Field(None, description="Semantic entanglement analysis")
    entanglement_graph: Optional[List[Dict[str, Any]]] = Field(None, description="Entanglement relationships")
    
    # Coherence analysis
    contextual_coherence: Optional[Dict[str, Any]] = Field(None, description="Contextual coherence analysis")
    coherence_scores: Optional[Dict[str, float]] = Field(None, description="Various coherence scores")
    
    # Quantum metrics
    quantum_metrics: Dict[str, float] = Field(description="Quantum-specific metrics")
    processing_metrics: Dict[str, float] = Field(description="Processing performance metrics")

# QTransformer Models
class QTransformerRequest(BaseRequest):
    """Request model for QTransformer processing"""
    input_text: str = Field(description="Input text for QTransformer processing")
    task_type: str = Field(default="generation", regex="^(generation|classification|embedding|analysis)$", description="Task type")
    
    # Model configuration
    model_size: str = Field(default="base", regex="^(small|base|large)$", description="Model size")
    quantum_enhancement: bool = Field(default=True, description="Enable quantum enhancements")
    
    # Generation parameters (for generation tasks)
    max_new_tokens: int = Field(default=50, ge=1, le=1000, description="Maximum new tokens to generate")
    temperature: float = Field(default=1.0, ge=0.1, le=2.0, description="Generation temperature")
    do_sample: bool = Field(default=True, description="Whether to use sampling")
    
    # Quantum parameters
    num_quantum_layers: int = Field(default=6, ge=1, le=24, description="Number of quantum transformer layers")
    quantum_attention_heads: int = Field(default=8, ge=1, le=32, description="Number of quantum attention heads")
    entanglement_strength: float = Field(default=0.5, ge=0.0, le=1.0, description="Entanglement strength")
    
    # Output options
    return_attention: bool = Field(default=False, description="Return attention patterns")
    return_layer_outputs: bool = Field(default=False, description="Return outputs from all layers")
    
    @validator('input_text')
    def validate_input_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Input text cannot be empty')
        if len(v) > 20000:
            raise ValueError('Input text too long (max 20000 characters)')
        return v.strip()

class QTransformerResponse(BaseResponse):
    """Response model for QTransformer processing"""
    input_text: str = Field(description="Original input text")
    task_type: str = Field(description="Task type that was performed")
    
    # Task-specific outputs
    generated_text: Optional[str] = Field(None, description="Generated text (for generation tasks)")
    classification_result: Optional[Dict[str, Any]] = Field(None, description="Classification result")
    embeddings: Optional[List[List[float]]] = Field(None, description="Text embeddings")
    analysis_result: Optional[Dict[str, Any]] = Field(None, description="Analysis result")
    
    # Model information
    model_info: Dict[str, Any] = Field(description="Information about the model used")
    
    # Attention and layer outputs
    attention_patterns: Optional[List[Dict[str, Any]]] = Field(None, description="Attention patterns (if requested)")
    layer_outputs: Optional[List[List[List[float]]]] = Field(None, description="Layer outputs (if requested)")
    
    # Quantum information
    quantum_metrics: Dict[str, float] = Field(description="Quantum-specific metrics")
    transformer_metrics: Dict[str, float] = Field(description="Transformer performance metrics")

# Batch Processing Models
class BatchInferenceRequest(BaseRequest):
    """Request model for batch inference"""
    prompts: List[str] = Field(description="List of prompts for batch processing")
    model_type: ModelType = Field(default=ModelType.QDLLM, description="Type of model to use")
    
    # Shared parameters for all prompts
    shared_params: Dict[str, Any] = Field(default_factory=dict, description="Shared parameters for all prompts")
    
    # Batch processing options
    parallel_processing: bool = Field(default=True, description="Enable parallel processing")
    max_batch_size: int = Field(default=8, ge=1, le=32, description="Maximum batch size")
    
    @validator('prompts')
    def validate_prompts(cls, v):
        if not v:
            raise ValueError('Prompts list cannot be empty')
        if len(v) > 100:
            raise ValueError('Too many prompts (max 100)')
        for prompt in v:
            if not prompt or not prompt.strip():
                raise ValueError('All prompts must be non-empty')
        return v

class BatchInferenceResponse(BaseResponse):
    """Response model for batch inference"""
    results: List[Union[InferenceResponse, QNLPResponse, QTransformerResponse]] = Field(description="Batch processing results")
    num_processed: int = Field(description="Number of prompts processed")
    num_successful: int = Field(description="Number of successful processes")
    num_failed: int = Field(description="Number of failed processes")
    
    # Batch metrics
    total_processing_time: float = Field(description="Total processing time")
    average_processing_time: float = Field(description="Average processing time per prompt")
    throughput: float = Field(description="Prompts processed per second")

# System Models
class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")
    version: str = Field(description="API version")
    uptime: float = Field(description="Service uptime in seconds")
    
    # Component health
    components: Dict[str, str] = Field(description="Health status of individual components")
    
    # System metrics
    system_metrics: Dict[str, float] = Field(description="System performance metrics")
    
    # Model status
    models_loaded: Dict[str, bool] = Field(description="Status of loaded models")

class ModelInfoResponse(BaseModel):
    """Model information response"""
    model_type: str = Field(description="Type of the model")
    model_name: str = Field(description="Name of the model")
    version: str = Field(description="Model version")
    
    # Model configuration
    config: Dict[str, Any] = Field(description="Model configuration")
    
    # Model statistics
    num_parameters: int = Field(description="Number of model parameters")
    model_size: str = Field(description="Estimated model size")
    
    # Capabilities
    supported_tasks: List[str] = Field(description="Supported tasks")
    quantum_enhanced: bool = Field(description="Whether the model uses quantum enhancements")
    
    # Performance info
    benchmark_results: Optional[Dict[str, float]] = Field(None, description="Benchmark results")
    
    # Metadata
    creation_time: datetime = Field(description="Model creation timestamp")
    last_updated: datetime = Field(description="Last update timestamp")

class ErrorResponse(BaseModel):
    """Error response model"""
    error_code: str = Field(description="Error code")
    error_message: str = Field(description="Human-readable error message")
    error_details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request ID that caused the error")
    
    # Debugging information
    stack_trace: Optional[str] = Field(None, description="Stack trace (in debug mode)")
    suggestions: Optional[List[str]] = Field(None, description="Suggestions to fix the error")

# Configuration Models
class APIConfig(BaseModel):
    """API configuration model"""
    # Server settings
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, ge=1, le=65535, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")
    
    # Model settings
    default_model_type: ModelType = Field(default=ModelType.QDLLM, description="Default model type")
    enable_quantum_enhancement: bool = Field(default=True, description="Enable quantum enhancements by default")
    
    # Performance settings
    max_concurrent_requests: int = Field(default=10, ge=1, le=100, description="Maximum concurrent requests")
    request_timeout: float = Field(default=300.0, ge=1.0, le=3600.0, description="Request timeout in seconds")
    
    # Security settings
    enable_cors: bool = Field(default=True, description="Enable CORS")
    api_key_required: bool = Field(default=False, description="Require API key")
    rate_limit_enabled: bool = Field(default=True, description="Enable rate limiting")
    
    # Logging settings
    log_level: str = Field(default="INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$", description="Log level")
    log_requests: bool = Field(default=True, description="Log all requests")
    
    # Cache settings
    enable_caching: bool = Field(default=True, description="Enable response caching")
    cache_ttl: int = Field(default=3600, ge=0, description="Cache TTL in seconds")

class SystemMetricsResponse(BaseModel):
    """System metrics response"""
    cpu_usage: float = Field(description="CPU usage percentage")
    memory_usage: float = Field(description="Memory usage percentage")
    disk_usage: float = Field(description="Disk usage percentage")
    uptime: float = Field(description="System uptime in seconds")
    timestamp: str = Field(description="Timestamp of metrics collection")

# Quantum Algorithm Models
class ReversalReasoningRequest(BaseModel):
    """Request for reversal reasoning algorithm"""
    premise: str = Field(description="The premise statement")
    conclusion: str = Field(description="The conclusion statement")
    coherence_threshold: float = Field(default=0.9, ge=0.0, le=1.0, description="Coherence threshold")
    max_iterations: int = Field(default=3, ge=1, le=10, description="Maximum iterations for refinement")

class ReversalReasoningResponse(BaseModel):
    """Response from reversal reasoning algorithm"""
    forward_reasoning: str = Field(description="Forward reasoning result")
    backward_reasoning: str = Field(description="Backward reasoning result")
    coherence_score: float = Field(description="Coherence score")
    confidence: float = Field(description="Confidence level")
    iterations: int = Field(description="Number of iterations performed")
    performance_stats: Dict[str, Any] = Field(description="Performance statistics")

class QAOAOptimizationRequest(BaseModel):
    """Request for QAOA optimization algorithm"""
    problem_type: str = Field(description="Type of optimization problem (portfolio, energy, insurance, general)")
    data: List[List[float]] = Field(description="Input data matrix")
    num_workers: Optional[int] = Field(default=None, description="Number of parallel workers")
    max_iterations: int = Field(default=100, ge=1, le=1000, description="Maximum optimization iterations")
    tolerance: float = Field(default=1e-6, ge=1e-10, le=1e-2, description="Convergence tolerance")

class QAOAOptimizationResponse(BaseModel):
    """Response from QAOA optimization algorithm"""
    optimal_parameters: List[float] = Field(description="Optimal QAOA parameters")
    optimal_value: float = Field(description="Optimal objective value")
    convergence_history: List[float] = Field(description="Convergence history")
    execution_time: float = Field(description="Execution time in seconds")
    num_workers_used: int = Field(description="Number of workers used")
    performance_stats: Dict[str, Any] = Field(description="Performance statistics")