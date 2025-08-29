from branding import BRANDING

"""
NQBA Stack Settings
Centralized configuration management with secure credential handling
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from pydantic import ConfigDict
import logging

logger = logging.getLogger(__name__)


class NQBASettings(BaseSettings):
    """NQBA Stack Configuration Settings"""

    model_config = ConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )
    # Environment
    environment: str = Field(
        default="development", json_schema_extra={"env": "NQBA_ENVIRONMENT"}
    )
    debug: bool = Field(default=False, json_schema_extra={"env": "NQBA_DEBUG"})
    # Company Information
    company_name: str = Field(
        default=f"{BRANDING['goliath']['name']} | {BRANDING['flyfox']['name']} | {BRANDING['sigma_select']['name']}",
        json_schema_extra={"env": "NQBA_COMPANY_NAME"},
    )
    business_unit: str = Field(
        default=f"{BRANDING['goliath']['name']} / {BRANDING['flyfox']['name']} / {BRANDING['sigma_select']['name']}",
        json_schema_extra={"env": "NQBA_BUSINESS_UNIT"},
    )
    # API Credentials (SECURE - Never log or expose these)
    dynex_api_key: Optional[str] = Field(
        default=None,
        json_schema_extra={"env": "DYNEX_API_KEY", "description": "DynexSolve API key"},
    )
    dynex_api_secret: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "env": "DYNEX_API_SECRET",
            "description": "Dynex API secret",
        },
    )
    dynex_api_endpoint: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "env": "DYNEX_API_ENDPOINT",
            "description": "Dynex API endpoint",
        },
    )
    dynex_ftp_host: Optional[str] = Field(
        default=None,
        json_schema_extra={"env": "DYNEX_FTP_HOST", "description": "Dynex FTP host"},
    )
    dynex_ftp_user: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "env": "DYNEX_FTP_USER",
            "description": "Dynex FTP username",
        },
    )
    dynex_ftp_pass: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "env": "DYNEX_FTP_PASS",
            "description": "Dynex FTP password",
        },
    )
    ipfs_project_id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "env": "IPFS_PROJECT_ID",
            "description": "IPFS project identifier",
        },
    )
    ipfs_project_secret: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "env": "IPFS_PROJECT_SECRET",
            "description": "IPFS project secret",
        },
    )
    ipfs_gateway_url: Optional[str] = Field(
        default="https://gateway.pinata.cloud",
        json_schema_extra={
            "env": "IPFS_GATEWAY_URL",
            "description": "IPFS gateway URL",
        },
    )
    llm_api_key: Optional[str] = Field(
        default=None,
        json_schema_extra={"env": "LLM_API_KEY", "description": "LLM service API key"},
    )
    openai_api_key: Optional[str] = Field(
        default=None,
        json_schema_extra={"env": "OPENAI_API_KEY", "description": "OpenAI API key"},
    )
    # Web3 Configuration
    web3_provider_url: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "env": "WEB3_PROVIDER_URL",
            "description": "Web3 provider URL",
        },
    )
    # Data and Storage
    data_dir: Path = Field(
        default=Path("./data"), json_schema_extra={"env": "NQBA_DATA_DIR"}
    )
    log_dir: Path = Field(
        default=Path("./logs"), json_schema_extra={"env": "NQBA_LOG_DIR"}
    )
    cache_dir: Path = Field(
        default=Path("./cache"), json_schema_extra={"env": "NQBA_CACHE_DIR"}
    )
    # API Configuration
    api_host: str = Field(default="0.0.0.0", json_schema_extra={"env": "NQBA_API_HOST"})
    api_port: int = Field(default=8000, json_schema_extra={"env": "NQBA_API_PORT"})
    api_workers: int = Field(default=1, json_schema_extra={"env": "NQBA_API_WORKERS"})
    # Quantum Configuration
    quantum_timeout: int = Field(
        default=300, json_schema_extra={"env": "NQBA_QUANTUM_TIMEOUT"}
    )
    quantum_max_qubits: int = Field(
        default=64, json_schema_extra={"env": "NQBA_QUANTUM_MAX_QUBITS"}
    )
    quantum_backend: str = Field(
        default="dynex", json_schema_extra={"env": "NQBA_QUANTUM_BACKEND"}
    )
    # LTC Configuration
    ltc_backup_interval: int = Field(
        default=3600, json_schema_extra={"env": "NQBA_LTC_BACKUP_INTERVAL"}
    )
    ltc_max_entries: int = Field(
        default=10000, json_schema_extra={"env": "NQBA_LTC_MAX_ENTRIES"}
    )
    ltc_enable_ipfs: bool = Field(
        default=True, json_schema_extra={"env": "NQBA_LTC_ENABLE_IPFS"}
    )
    # Security Configuration
    enable_cors: bool = Field(
        default=True, json_schema_extra={"env": "NQBA_ENABLE_CORS"}
    )
    cors_origins: list = Field(
        default=["*"], json_schema_extra={"env": "NQBA_CORS_ORIGINS"}
    )
    enable_rate_limiting: bool = Field(
        default=True, json_schema_extra={"env": "NQBA_ENABLE_RATE_LIMITING"}
    )
    rate_limit_requests: int = Field(
        default=100, json_schema_extra={"env": "NQBA_RATE_LIMIT_REQUESTS"}
    )
    rate_limit_window: int = Field(
        default=60, json_schema_extra={"env": "NQBA_RATE_LIMIT_WINDOW"}
    )

    # Validation and Security
    from pydantic import field_validator

    @field_validator("dynex_api_key")
    @classmethod
    def validate_dynex_api_key(cls, v):
        """Validate Dynex API key format"""
        if v is not None:
            if not v.startswith("dnx_"):
                logger.warning("Dynex API key should start with 'dnx_'")
            if len(v) < 20:
                logger.warning("Dynex API key seems too short")
        return v

    @field_validator("ipfs_project_id")
    @classmethod
    def validate_ipfs_project_id(cls, v):
        """Validate IPFS project ID format"""
        if v is not None:
            if not v.startswith("Qm") and not v.startswith("bafy"):
                logger.warning("IPFS project ID should start with 'Qm' or 'bafy'")
        return v

    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_api_key(cls, v):
        """Validate OpenAI API key format"""
        if v is not None:
            if not v.startswith("sk-"):
                logger.warning("OpenAI API key should start with 'sk-'")
        return v

    @field_validator("llm_api_key")
    @classmethod
    def validate_llm_api_key(cls, v):
        """Validate LLM API key format"""
        if v is not None:
            if len(v) < 10:
                logger.warning("LLM API key seems too short")
        return v

    # Security methods
    def get_credential_status(self) -> Dict[str, bool]:
        """Get credential configuration status (safe to log)"""
        return {
            "dynex_configured": self.dynex_configured,
            "ipfs_configured": self.ipfs_configured,
            "web3_configured": self.web3_configured,
            "llm_configured": self.llm_configured,
            "all_credentials_configured": self.all_credentials_configured,
        }

    def validate_credentials(self) -> Dict[str, str]:
        """Validate all credentials and return status messages"""
        status = {}

        if not self.dynex_configured:
            status["dynex"] = "DYNEX_API_KEY not configured"
        else:
            status["dynex"] = "✅ Dynex configured"

        if not self.ipfs_configured:
            status["ipfs"] = "IPFS_PROJECT_ID or IPFS_PROJECT_SECRET not configured"
        else:
            status["ipfs"] = "✅ IPFS configured"

        if not self.web3_configured:
            status["web3"] = "WEB3_PROVIDER_URL not configured"
        else:
            status["web3"] = "✅ Web3 configured"

        if not self.llm_configured:
            status["llm"] = "LLM_API_KEY or OPENAI_API_KEY not configured"
        else:
            status["llm"] = "✅ LLM configured"

        return status

    # Computed properties
    @property
    def dynex_configured(self) -> bool:
        """Check if Dynex is properly configured"""
        return bool(self.dynex_api_key and len(self.dynex_api_key) > 20)

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

    @property
    def all_credentials_configured(self) -> bool:
        """Check if all critical credentials are configured"""
        return all(
            [
                self.dynex_configured,
                self.ipfs_configured,
                self.web3_configured,
                self.llm_configured,
            ]
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

    # Directory setup
    def setup_directories(self):
        """Create necessary directories"""
        for directory in [self.data_dir, self.log_dir, self.cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory ready: {directory}")

    # Security audit
    def security_audit(self) -> Dict[str, Any]:
        """Perform security audit (safe to log)"""
        return {
            "environment": self.environment,
            "debug_mode": self.debug,
            "cors_enabled": self.enable_cors,
            "rate_limiting_enabled": self.enable_rate_limiting,
            "credential_status": self.get_credential_status(),
            "directory_permissions": {
                "data_dir": str(self.data_dir),
                "log_dir": str(self.log_dir),
                "cache_dir": str(self.cache_dir),
            },
        }

    # Removed Config class for Pydantic v2 compliance


# Global settings instance
_settings: Optional[NQBASettings] = None


def get_settings() -> NQBASettings:
    """Get global settings instance"""
    global _settings
    if _settings is None:
        _settings = NQBASettings()
        _settings.setup_directories()

        # Log configuration status (without exposing credentials)
        logger.info("NQBA Settings initialized")
        logger.info(f"Environment: {_settings.environment}")
        logger.info(f"Company: {_settings.company_name}")
        logger.info(f"Business Unit: {_settings.business_unit}")

        # Log credential status safely
        cred_status = _settings.get_credential_status()
        for service, status in cred_status.items():
            logger.info(f"{service}: {status}")

        # Security audit
        audit = _settings.security_audit()
        logger.info("Security audit completed")

    return _settings


# Convenience functions
def is_production() -> bool:
    """Check if running in production"""
    return get_settings().is_production


def is_development() -> bool:
    """Check if running in development"""
    return get_settings().is_development


def is_testing() -> bool:
    """Check if running in testing"""
    return get_settings().is_testing
