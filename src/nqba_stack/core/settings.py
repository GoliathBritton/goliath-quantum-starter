"""
NQBA Stack Settings Module - Centralized Configuration Management

This module provides centralized configuration management for the NQBA Framework.
All configuration values are loaded from environment variables with sensible
defaults for both development and production environments.

Key Features:
    - Environment-based configuration with .env file support
    - Type-safe settings with validation
    - Sensible defaults for rapid development
    - Production-ready security configurations
    
Usage:
    >>> from nqba_stack.core.settings import get_settings
    >>> settings = get_settings()
    >>> print(settings.dynex_api_key)
    
Environment Variables:
    See .env.template for a complete list of all available configuration options
    and their descriptions. Key variables include:
    - DYNEX_API_KEY: Required for Dynex neuromorphic computing
    - OPENAI_API_KEY: Required for AI/LLM features
    - DATABASE_URL: Database connection string
    - LOG_LEVEL: Logging verbosity (DEBUG, INFO, WARNING, ERROR)
    
Related Documentation:
    - Configuration Guide: docs/TECHNICAL_IMPLEMENTATION_GUIDE.md
    - Security Setup: docs/SECURITY_SYSTEM.md
    - Deployment Guide: docs/DEPLOYMENT_GUIDE.md
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class NQBASettings:
    """
    NQBA Stack Configuration Settings
    
    This class manages all configuration settings for the NQBA Framework,
    loading values from environment variables with fallback defaults.
    
    Attributes:
        environment: Deployment environment (development/staging/production)
        debug: Enable debug mode with verbose logging
        company_name: Organization name for branding
        dynex_api_key: API key for Dynex neuromorphic computing platform
        openai_api_key: API key for OpenAI services
        quantum_backend: Quantum computing backend selection
        
    Example:
        >>> settings = NQBASettings()
        >>> if settings.debug:
        ...     print("Running in debug mode")
    """

    def __init__(self):
        # Environment
        self.environment: str = os.getenv("NQBA_ENVIRONMENT", "development")
        self.debug: bool = os.getenv("NQBA_DEBUG", "False").lower() == "true"
        
        # Company Information
        self.company_name: str = os.getenv(
            "NQBA_COMPANY_NAME", "Goliath of All Trade | FLYFOX AI | Sigma Select"
        )
        self.business_unit: str = os.getenv(
            "NQBA_BUSINESS_UNIT", "Goliath of All Trade / FLYFOX AI / Sigma Select"
        )
        
        # API Credentials
        self.dynex_api_key: Optional[str] = os.getenv("DYNEX_API_KEY")
        self.dynex_api_secret: Optional[str] = os.getenv("DYNEX_API_SECRET")
        self.dynex_api_endpoint: Optional[str] = os.getenv("DYNEX_API_ENDPOINT")
        self.dynex_ftp_host: Optional[str] = os.getenv("DYNEX_FTP_HOST")
        self.dynex_ftp_user: Optional[str] = os.getenv("DYNEX_FTP_USER")
        self.dynex_ftp_pass: Optional[str] = os.getenv("DYNEX_FTP_PASS")
        
        # IPFS Configuration
        self.ipfs_project_id: Optional[str] = os.getenv("IPFS_PROJECT_ID")
        self.ipfs_project_secret: Optional[str] = os.getenv("IPFS_PROJECT_SECRET")
        self.ipfs_gateway_url: str = os.getenv(
            "IPFS_GATEWAY_URL", "https://gateway.pinata.cloud"
        )
        
        # LLM Configuration
        self.llm_api_key: Optional[str] = os.getenv("LLM_API_KEY")
        self.openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        
        # Security
        self.SECRET_KEY: str = os.getenv(
            "SECRET_KEY", "your-secret-key-change-this-in-production"
        )
        
        # CORS Configuration
        self.ALLOWED_ORIGINS: List[str] = [
            "http://localhost:3000",
            "http://localhost:8000", 
            "https://nqba.com"
        ]
        self.ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "nqba.com"]
        
        # Web3 Configuration
        self.web3_provider_url: Optional[str] = os.getenv("WEB3_PROVIDER_URL")
        
        # Directory Configuration
        self.data_dir: Path = Path(os.getenv("NQBA_DATA_DIR", "./data"))
        self.log_dir: Path = Path(os.getenv("NQBA_LOG_DIR", "./logs"))
        self.cache_dir: Path = Path(os.getenv("NQBA_CACHE_DIR", "./cache"))
        
        # API Configuration
        self.api_host: str = os.getenv("NQBA_API_HOST", "0.0.0.0")
        self.api_port: int = int(os.getenv("NQBA_API_PORT", "8000"))
        self.api_workers: int = int(os.getenv("NQBA_API_WORKERS", "1"))
        
        # Quantum Configuration
        self.quantum_timeout: int = int(os.getenv("NQBA_QUANTUM_TIMEOUT", "300"))
        self.quantum_max_qubits: int = int(os.getenv("NQBA_QUANTUM_MAX_QUBITS", "64"))
        self.quantum_backend: str = os.getenv("NQBA_QUANTUM_BACKEND", "dynex")
        self.ibm_quantum_api_key: Optional[str] = os.getenv("IBM_QUANTUM_API_KEY")
        
        # LTC Configuration
        self.ltc_backup_interval: int = int(os.getenv("NQBA_LTC_BACKUP_INTERVAL", "3600"))
        self.ltc_max_entries: int = int(os.getenv("NQBA_LTC_MAX_ENTRIES", "10000"))
        self.ltc_enable_ipfs: bool = os.getenv("NQBA_LTC_ENABLE_IPFS", "True").lower() == "true"
        
        # Security Configuration
        self.enable_cors: bool = os.getenv("NQBA_ENABLE_CORS", "True").lower() == "true"
        self.cors_origins: list = ["*"]
        self.enable_rate_limiting: bool = os.getenv("NQBA_ENABLE_RATE_LIMITING", "True").lower() == "true"
        self.rate_limit_requests: int = int(os.getenv("NQBA_RATE_LIMIT_REQUESTS", "100"))
        self.rate_limit_window: int = int(os.getenv("NQBA_RATE_LIMIT_WINDOW", "60"))
        
        # Setup directories
        self.setup_directories()
    
    def get_credential_status(self) -> Dict[str, bool]:
        """Get status of all credentials"""
        return {
            "dynex": self.dynex_configured,
            "ipfs": self.ipfs_configured,
            "web3": self.web3_configured,
            "llm": self.llm_configured,
        }
    
    def validate_credentials(self) -> Dict[str, str]:
        """Validate all credentials and return status"""
        issues = []
        
        if not self.dynex_configured:
            issues.append("Dynex API credentials not configured")
        
        if not self.ipfs_configured:
            issues.append("IPFS credentials not configured")
        
        if not self.llm_configured:
            issues.append("LLM API key not configured")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "credential_status": self.get_credential_status(),
        }
    
    @property
    def dynex_configured(self) -> bool:
        """Check if Dynex is properly configured"""
        return bool(self.dynex_api_key and self.dynex_api_secret)
    
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
        return bool(self.openai_api_key or self.llm_api_key)
    
    @property
    def all_credentials_configured(self) -> bool:
        """Check if all credentials are configured"""
        return (
            self.dynex_configured
            and self.ipfs_configured
            and self.web3_configured
            and self.llm_configured
        )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment.lower() == "development"
    
    @property
    def is_testing(self) -> bool:
        """Check if running in testing"""
        return self.environment.lower() == "testing"
    
    def setup_directories(self):
        """Create necessary directories"""
        for directory in [self.data_dir, self.log_dir, self.cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def security_audit(self) -> Dict[str, Any]:
        """Perform security audit"""
        return {
            "environment": self.environment,
            "debug_mode": self.debug,
            "credentials_configured": self.get_credential_status(),
            "cors_enabled": self.enable_cors,
            "rate_limiting_enabled": self.enable_rate_limiting,
            "secret_key_default": self.SECRET_KEY == "your-secret-key-change-this-in-production",
            "recommendations": [
                "Change default SECRET_KEY in production",
                "Configure all API credentials",
                "Enable rate limiting in production",
                "Review CORS origins for production",
            ],
        }


# Global settings instance
_settings: Optional[NQBASettings] = None


def get_settings() -> NQBASettings:
    """Get global settings instance"""
    global _settings
    if _settings is None:
        _settings = NQBASettings()
        logger.info("NQBA Settings initialized")
        
        # Log configuration status (without sensitive data)
        credential_status = _settings.get_credential_status()
        logger.info(f"Credential status: {credential_status}")
        
        if not _settings.all_credentials_configured:
            logger.warning(
                "Not all credentials are configured. "
                "Some features may not work properly."
            )
    
    return _settings


def is_production() -> bool:
    """Check if running in production"""
    return get_settings().is_production


def is_development() -> bool:
    """Check if running in development"""
    return get_settings().is_development


def is_testing() -> bool:
    """Check if running in testing"""
    return get_settings().is_testing
