"""
NQBA Settings Module
Configuration management using pydantic.BaseSettings
Centralizes all environment variables and configuration
"""
import os
from typing import Optional
from pydantic import BaseSettings, Field, validator
from pathlib import Path

class NQBASettings(BaseSettings):
    """NQBA configuration settings"""
    
    # Environment
    environment: str = Field(default="development", env="NQBA_ENV")
    debug: bool = Field(default=False, env="NQBA_DEBUG")
    
    # Dynex Configuration
    dynex_api_key: Optional[str] = Field(default=None, env="DYNEX_API_KEY")
    dynex_mainnet: bool = Field(default=True, env="DYNEX_MAINNET")
    dynex_default_reads: int = Field(default=1000, env="DYNEX_DEFAULT_READS")
    dynex_default_annealing_time: int = Field(default=100, env="DYNEX_ANNEALING_TIME")
    dynex_timeout_seconds: int = Field(default=300, env="DYNEX_TIMEOUT")
    
    # IPFS Configuration
    ipfs_project_id: Optional[str] = Field(default=None, env="IPFS_PROJECT_ID")
    ipfs_project_secret: Optional[str] = Field(default=None, env="IPFS_PROJECT_SECRET")
    ipfs_gateway_url: str = Field(default="https://ipfs.infura.io:5001", env="IPFS_GATEWAY_URL")
    
    # Web3 Configuration
    web3_provider_url: Optional[str] = Field(default=None, env="WEB3_PROVIDER_URL")
    web3_private_key: Optional[str] = Field(default=None, env="WEB3_PRIVATE_KEY")
    
    # LLM Configuration
    llm_api_key: Optional[str] = Field(default=None, env="LLM_API_KEY")
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///nqba.db", env="DATABASE_URL")
    redis_url: str = Field(default="redis://localhost:6379", env="REDIS_URL")
    
    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: Optional[str] = Field(default=None, env="LOG_FILE")
    ltc_enabled: bool = Field(default=True, env="LTC_ENABLED")
    
    # API Configuration
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=1, env="API_WORKERS")
    
    # Security Configuration
    secret_key: str = Field(default="nqba-secret-key-change-in-production", env="SECRET_KEY")
    jwt_secret: str = Field(default="nqba-jwt-secret-change-in-production", env="JWT_SECRET")
    cors_origins: list = Field(default=["*"], env="CORS_ORIGINS")
    
    # Business Configuration
    company_name: str = Field(default="FLYFOX AI", env="COMPANY_NAME")
    business_unit: str = Field(default="NQBA Core", env="BUSINESS_UNIT")
    sigma_select_enabled: bool = Field(default=True, env="SIGMA_SELECT_ENABLED")
    flyfox_energy_enabled: bool = Field(default=True, env="FLYFOX_ENERGY_ENABLED")
    
    # File Paths
    base_dir: Path = Field(default=Path(__file__).parent.parent.parent)
    config_dir: Path = Field(default=Path(__file__).parent.parent.parent / "config")
    data_dir: Path = Field(default=Path(__file__).parent.parent.parent / "data")
    logs_dir: Path = Field(default=Path(__file__).parent.parent.parent / "logs")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @validator('environment')
    def validate_environment(cls, v):
        allowed = ['development', 'staging', 'production', 'testing']
        if v not in allowed:
            raise ValueError(f'Environment must be one of: {allowed}')
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        allowed = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in allowed:
            raise ValueError(f'Log level must be one of: {allowed}')
        return v.upper()
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == "development"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing"""
        return self.environment == "testing"
    
    @property
    def dynex_configured(self) -> bool:
        """Check if Dynex is properly configured"""
        return bool(self.dynex_api_key)
    
    @property
    def ipfs_configured(self) -> bool:
        """Check if IPFS is properly configured"""
        return bool(self.ipfs_project_id and self.ipfs_project_secret)
    
    @property
    def web3_configured(self) -> bool:
        """Check if Web3 is properly configured"""
        return bool(self.web3_provider_url)
    
    @property
    def llm_configured(self) -> bool:
        """Check if LLM is properly configured"""
        return bool(self.llm_api_key or self.openai_api_key)
    
    def create_directories(self):
        """Create necessary directories"""
        for directory in [self.config_dir, self.data_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_database_config(self):
        """Get database configuration"""
        return {
            "url": self.database_url,
            "echo": self.debug,
            "pool_pre_ping": True,
            "pool_recycle": 300
        }
    
    def get_redis_config(self):
        """Get Redis configuration"""
        return {
            "url": self.redis_url,
            "decode_responses": True,
            "socket_connect_timeout": 5,
            "socket_timeout": 5
        }
    
    def get_api_config(self):
        """Get API configuration"""
        return {
            "host": self.api_host,
            "port": self.api_port,
            "workers": self.api_workers,
            "debug": self.debug
        }

# Global settings instance
settings = NQBASettings()

# Convenience functions
def get_settings() -> NQBASettings:
    """Get global settings instance"""
    return settings

def is_production() -> bool:
    """Check if running in production"""
    return settings.is_production

def is_development() -> bool:
    """Check if running in development"""
    return settings.is_development

def is_testing() -> bool:
    """Check if running in testing"""
    return settings.is_testing
