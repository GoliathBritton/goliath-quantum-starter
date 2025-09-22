"""qdLLM Worker Configuration

Configuration management for qdLLM worker service.
"""

import os
from typing import Dict, List, Optional

from pydantic import BaseSettings, Field


class QdLLMConfig(BaseSettings):
    """Configuration for qdLLM Worker"""
    
    # Service Configuration
    service_name: str = Field("qdllm-worker", env="QDLLM_SERVICE_NAME")
    service_version: str = Field("1.0.0", env="QDLLM_SERVICE_VERSION")
    environment: str = Field("development", env="ENVIRONMENT")
    debug: bool = Field(False, env="DEBUG")
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4", env="OPENAI_MODEL")
    openai_temperature: float = Field(0.7, env="OPENAI_TEMPERATURE")
    openai_max_tokens: int = Field(2000, env="OPENAI_MAX_TOKENS")
    openai_timeout: int = Field(30, env="OPENAI_TIMEOUT")
    
    # Quantum Job Manager Configuration
    quantum_job_manager_enabled: bool = Field(True, env="QUANTUM_JOB_MANAGER_ENABLED")
    quantum_job_manager_url: Optional[str] = Field(None, env="QUANTUM_JOB_MANAGER_URL")
    quantum_enhancement_threshold: float = Field(0.7, env="QUANTUM_ENHANCEMENT_THRESHOLD")
    
    # Dynex Configuration
    dynex_enabled: bool = Field(True, env="DYNEX_ENABLED")
    dynex_api_key: Optional[str] = Field(None, env="DYNEX_API_KEY")
    dynex_endpoint: str = Field("https://api.dynexcoin.org", env="DYNEX_ENDPOINT")
    dynex_timeout: int = Field(60, env="DYNEX_TIMEOUT")
    dynex_max_retries: int = Field(3, env="DYNEX_MAX_RETRIES")
    
    # Processing Configuration
    max_concurrent_requests: int = Field(10, env="MAX_CONCURRENT_REQUESTS")
    default_timeout: int = Field(30, env="DEFAULT_TIMEOUT")
    max_batch_size: int = Field(50, env="MAX_BATCH_SIZE")
    enable_caching: bool = Field(True, env="ENABLE_CACHING")
    cache_ttl: int = Field(3600, env="CACHE_TTL")  # 1 hour
    
    # Prompt Configuration
    prompts_directory: str = Field("prompts", env="PROMPTS_DIRECTORY")
    prompt_cache_enabled: bool = Field(True, env="PROMPT_CACHE_ENABLED")
    
    # Parallel Exploration Settings
    parallel_exploration_strategies: int = Field(6, env="PARALLEL_EXPLORATION_STRATEGIES")
    parallel_exploration_timeout: int = Field(45, env="PARALLEL_EXPLORATION_TIMEOUT")
    
    # Reversal Reasoning Settings
    reversal_reasoning_candidates: int = Field(6, env="REVERSAL_REASONING_CANDIDATES")
    reversal_reasoning_timeout: int = Field(60, env="REVERSAL_REASONING_TIMEOUT")
    
    # Quantum Ranking Settings
    quantum_ranking_candidates: int = Field(10, env="QUANTUM_RANKING_CANDIDATES")
    quantum_ranking_timeout: int = Field(30, env="QUANTUM_RANKING_TIMEOUT")
    
    # Lead Qualification Settings
    lead_qualification_timeout: int = Field(20, env="LEAD_QUALIFICATION_TIMEOUT")
    lead_qualification_threshold: float = Field(0.6, env="LEAD_QUALIFICATION_THRESHOLD")
    
    # Logging Configuration
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    enable_audit_logging: bool = Field(True, env="ENABLE_AUDIT_LOGGING")
    
    # Metrics Configuration
    enable_metrics: bool = Field(True, env="ENABLE_METRICS")
    metrics_port: int = Field(8080, env="METRICS_PORT")
    
    # Health Check Configuration
    health_check_interval: int = Field(30, env="HEALTH_CHECK_INTERVAL")
    health_check_timeout: int = Field(5, env="HEALTH_CHECK_TIMEOUT")
    
    # Security Configuration
    api_key_required: bool = Field(True, env="API_KEY_REQUIRED")
    allowed_origins: List[str] = Field(["*"], env="ALLOWED_ORIGINS")
    rate_limit_enabled: bool = Field(True, env="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(60, env="RATE_LIMIT_WINDOW")  # seconds
    
    # Error Handling Configuration
    max_retries: int = Field(3, env="MAX_RETRIES")
    retry_delay: float = Field(1.0, env="RETRY_DELAY")
    circuit_breaker_enabled: bool = Field(True, env="CIRCUIT_BREAKER_ENABLED")
    circuit_breaker_threshold: int = Field(5, env="CIRCUIT_BREAKER_THRESHOLD")
    
    # Performance Configuration
    enable_async_processing: bool = Field(True, env="ENABLE_ASYNC_PROCESSING")
    worker_pool_size: int = Field(4, env="WORKER_POOL_SIZE")
    memory_limit_mb: int = Field(1024, env="MEMORY_LIMIT_MB")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    def get_openai_config(self) -> Dict[str, any]:
        """Get OpenAI configuration dictionary"""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "temperature": self.openai_temperature,
            "max_tokens": self.openai_max_tokens,
            "timeout": self.openai_timeout
        }
    
    def get_dynex_config(self) -> Dict[str, any]:
        """Get Dynex configuration dictionary"""
        return {
            "enabled": self.dynex_enabled,
            "api_key": self.dynex_api_key,
            "endpoint": self.dynex_endpoint,
            "timeout": self.dynex_timeout,
            "max_retries": self.dynex_max_retries
        }
    
    def get_processing_config(self) -> Dict[str, any]:
        """Get processing configuration dictionary"""
        return {
            "max_concurrent_requests": self.max_concurrent_requests,
            "default_timeout": self.default_timeout,
            "max_batch_size": self.max_batch_size,
            "enable_caching": self.enable_caching,
            "cache_ttl": self.cache_ttl
        }
    
    def get_prompt_config(self) -> Dict[str, any]:
        """Get prompt configuration dictionary"""
        return {
            "prompts_directory": self.prompts_directory,
            "prompt_cache_enabled": self.prompt_cache_enabled,
            "parallel_exploration_strategies": self.parallel_exploration_strategies,
            "reversal_reasoning_candidates": self.reversal_reasoning_candidates,
            "quantum_ranking_candidates": self.quantum_ranking_candidates
        }
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of errors"""
        errors = []
        
        # Check required fields
        if not self.openai_api_key:
            errors.append("OpenAI API key is required")
        
        if self.dynex_enabled and not self.dynex_api_key:
            errors.append("Dynex API key is required when Dynex is enabled")
        
        # Check numeric ranges
        if self.openai_temperature < 0 or self.openai_temperature > 2:
            errors.append("OpenAI temperature must be between 0 and 2")
        
        if self.quantum_enhancement_threshold < 0 or self.quantum_enhancement_threshold > 1:
            errors.append("Quantum enhancement threshold must be between 0 and 1")
        
        if self.max_concurrent_requests < 1:
            errors.append("Max concurrent requests must be at least 1")
        
        if self.worker_pool_size < 1:
            errors.append("Worker pool size must be at least 1")
        
        # Check timeout values
        if self.default_timeout < 1:
            errors.append("Default timeout must be at least 1 second")
        
        if self.openai_timeout < 1:
            errors.append("OpenAI timeout must be at least 1 second")
        
        return errors


class PromptConfig(BaseSettings):
    """Configuration for prompt templates"""
    
    # Prompt file paths
    reversal_reasoning_prompt: str = Field("prompts/reversal_reasoning.txt", env="REVERSAL_REASONING_PROMPT")
    parallel_exploration_prompt: str = Field("prompts/parallel_exploration.txt", env="PARALLEL_EXPLORATION_PROMPT")
    quantum_ranking_prompt: str = Field("prompts/quantum_ranking.txt", env="QUANTUM_RANKING_PROMPT")
    lead_qualification_prompt: str = Field("prompts/lead_qualification.txt", env="LEAD_QUALIFICATION_PROMPT")
    
    # Prompt caching
    cache_prompts: bool = Field(True, env="CACHE_PROMPTS")
    prompt_cache_ttl: int = Field(3600, env="PROMPT_CACHE_TTL")  # 1 hour
    
    # Prompt validation
    validate_prompts_on_startup: bool = Field(True, env="VALIDATE_PROMPTS_ON_STARTUP")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def get_prompt_paths(self) -> Dict[str, str]:
        """Get all prompt file paths"""
        return {
            "reversal_reasoning": self.reversal_reasoning_prompt,
            "parallel_exploration": self.parallel_exploration_prompt,
            "quantum_ranking": self.quantum_ranking_prompt,
            "lead_qualification": self.lead_qualification_prompt
        }


class MetricsConfig(BaseSettings):
    """Configuration for metrics and monitoring"""
    
    # Metrics collection
    enable_prometheus: bool = Field(True, env="ENABLE_PROMETHEUS")
    prometheus_port: int = Field(8080, env="PROMETHEUS_PORT")
    
    # Custom metrics
    track_request_duration: bool = Field(True, env="TRACK_REQUEST_DURATION")
    track_quantum_enhancement_rate: bool = Field(True, env="TRACK_QUANTUM_ENHANCEMENT_RATE")
    track_error_rates: bool = Field(True, env="TRACK_ERROR_RATES")
    
    # Alerting
    enable_alerting: bool = Field(False, env="ENABLE_ALERTING")
    alert_webhook_url: Optional[str] = Field(None, env="ALERT_WEBHOOK_URL")
    error_rate_threshold: float = Field(0.05, env="ERROR_RATE_THRESHOLD")  # 5%
    response_time_threshold: float = Field(10.0, env="RESPONSE_TIME_THRESHOLD")  # 10 seconds
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global configuration instance
config = QdLLMConfig()
prompt_config = PromptConfig()
metrics_config = MetricsConfig()


def get_config() -> QdLLMConfig:
    """Get the global configuration instance"""
    return config


def get_prompt_config() -> PromptConfig:
    """Get the prompt configuration instance"""
    return prompt_config


def get_metrics_config() -> MetricsConfig:
    """Get the metrics configuration instance"""
    return metrics_config


def validate_all_configs() -> List[str]:
    """Validate all configuration instances"""
    errors = []
    
    # Validate main config
    config_errors = config.validate_config()
    errors.extend([f"Config: {error}" for error in config_errors])
    
    # Validate metrics config
    if metrics_config.enable_alerting and not metrics_config.alert_webhook_url:
        errors.append("MetricsConfig: Alert webhook URL is required when alerting is enabled")
    
    if metrics_config.error_rate_threshold < 0 or metrics_config.error_rate_threshold > 1:
        errors.append("MetricsConfig: Error rate threshold must be between 0 and 1")
    
    return errors


def load_config_from_file(config_file: str) -> QdLLMConfig:
    """Load configuration from a specific file"""
    return QdLLMConfig(_env_file=config_file)


def get_environment_info() -> Dict[str, any]:
    """Get environment information for debugging"""
    return {
        "service_name": config.service_name,
        "service_version": config.service_version,
        "environment": config.environment,
        "debug": config.debug,
        "openai_model": config.openai_model,
        "quantum_enabled": config.quantum_job_manager_enabled,
        "dynex_enabled": config.dynex_enabled,
        "max_concurrent_requests": config.max_concurrent_requests,
        "python_version": os.sys.version,
        "platform": os.name
    }