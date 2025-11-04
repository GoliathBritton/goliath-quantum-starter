import os
from pydantic import BaseSettings, Field
from typing import List, Optional

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Quantum (Dynex primary)
    dynex_api_key: str = Field(default="", env="DYNEX_API_KEY")
    dynex_endpoint: str = Field(default="https://api.dynex.network/v1", env="DYNEX_ENDPOINT")
    
    # qdLLM / NVIDIA (optional)
    qdllm_mode: str = Field(default="hybrid", env="QDLLM_MODE")
    nvidia_api_key: Optional[str] = Field(default=None, env="NVIDIA_API_KEY")
    nvidia_triton_url: Optional[str] = Field(default=None, env="NVIDIA_TRITON_URL")
    nvidia_riva_stt_url: Optional[str] = Field(default=None, env="NVIDIA_RIVA_STT_URL")
    
    # LLM fallbacks
    openai_key: str = Field(default="", env="OPENAI_API_KEY")
    azure_endpoint: str = Field(default="", env="AZURE_OPENAI_ENDPOINT")
    azure_key: str = Field(default="", env="AZURE_OPENAI_API_KEY")
    azure_deployment: str = Field(default="gpt-4o", env="AZURE_OPENAI_DEPLOYMENT")
    azure_api_version: str = Field(default="2024-08-01-preview", env="AZURE_OPENAI_API_VERSION")
    
    # Speech
    deepgram_key: str = Field(default="", env="DEEPGRAM_API_KEY")
    
    # MCP (Model Context Protocol)
    mcp_base_url: str = Field(default="https://mcp-gateway.internal", env="MCP_BASE_URL")
    mcp_token: str = Field(default="", env="MCP_TOKEN")
    
    # GoliathCRM
    crm_base_url: str = Field(default="https://crm.goliath.local", env="GOLIATHCRM_BASE_URL")
    crm_api_key: str = Field(default="", env="GOLIATHCRM_API_KEY")
    
    # Subscriptions (Stripe)
    stripe_secret_key: str = Field(default="", env="STRIPE_SECRET_KEY")
    stripe_price_basic: str = Field(default="", env="STRIPE_PRICE_BASIC")
    stripe_price_pro: str = Field(default="", env="STRIPE_PRICE_PRO")
    stripe_price_enterprise: str = Field(default="", env="STRIPE_PRICE_ENTERPRISE")
    
    # Branding / Sigma Select
    public_brand: str = Field(default="FLYFOX AI", env="PUBLIC_BRAND")
    rev_reasoning: bool = Field(default=True, env="REVERSAL_REASONING")
    
    # Router feature flags
    ai_router_fallback: List[str] = Field(default=["openai", "azure"], env="AI_ROUTER_FALLBACK")
    ai_default_model: str = Field(default="gpt-4o-mini", env="AI_DEFAULT_MODEL")
    
    # Development
    node_env: str = Field(default="development", env="NODE_ENV")
    python_env: str = Field(default="development", env="PYTHON_ENV")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
