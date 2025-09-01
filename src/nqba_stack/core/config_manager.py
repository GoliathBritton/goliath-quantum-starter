"""
Advanced Configuration Management
================================

Handles configuration validation, fallbacks, and graceful degradation
for all external services (IPFS, Dynex, LLM, etc.)
"""

import os
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
import yaml
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ServiceConfig:
    """Configuration for a specific service"""

    name: str
    enabled: bool = False
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    fallback_enabled: bool = True
    health_check_enabled: bool = True
    retry_attempts: int = 3
    timeout: int = 30
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FallbackConfig:
    """Fallback configuration for degraded operation"""

    service_name: str
    fallback_mode: str  # "local", "cache", "disabled"
    local_storage_path: Optional[str] = None
    cache_ttl: int = 3600
    degraded_features: List[str] = field(default_factory=list)


class ConfigurationManager:
    """Advanced configuration management with fallbacks and health checks"""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/quantum_automation.yaml"
        self.services: Dict[str, ServiceConfig] = {}
        self.fallbacks: Dict[str, FallbackConfig] = {}
        self.health_status: Dict[str, bool] = {}
        self._load_configuration()

    def _load_configuration(self):
        """Load configuration from file and environment"""
        # Default service configurations
        self.services = {
            "dynex": ServiceConfig(
                name="dynex",
                enabled=bool(os.getenv("DYNEX_API_KEY")),
                api_key=os.getenv("DYNEX_API_KEY"),
                endpoint="https://dynex.network",
                fallback_enabled=True,
                health_check_enabled=True,
            ),
            "ipfs": ServiceConfig(
                name="ipfs",
                enabled=bool(
                    os.getenv("IPFS_PROJECT_ID") and os.getenv("IPFS_PROJECT_SECRET")
                ),
                api_key=os.getenv("IPFS_PROJECT_SECRET"),
                endpoint=os.getenv("IPFS_GATEWAY_URL", "https://gateway.pinata.cloud"),
                fallback_enabled=True,
                health_check_enabled=True,
                metadata={
                    "project_id": os.getenv("IPFS_PROJECT_ID"),
                    "gateway_url": os.getenv(
                        "IPFS_GATEWAY_URL", "https://gateway.pinata.cloud"
                    ),
                },
            ),
            "llm": ServiceConfig(
                name="llm",
                enabled=bool(os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")),
                api_key=os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY"),
                endpoint=os.getenv("LLM_ENDPOINT", "https://api.openai.com"),
                fallback_enabled=True,
                health_check_enabled=True,
            ),
            "web3": ServiceConfig(
                name="web3",
                enabled=bool(os.getenv("WEB3_PROVIDER_URL")),
                endpoint=os.getenv("WEB3_PROVIDER_URL"),
                fallback_enabled=True,
                health_check_enabled=False,
            ),
        }

        # Configure fallbacks
        self.fallbacks = {
            "dynex": FallbackConfig(
                service_name="dynex",
                fallback_mode="local",
                local_storage_path="./data/quantum_cache",
                degraded_features=["quantum_optimization", "qubo_solving"],
            ),
            "ipfs": FallbackConfig(
                service_name="ipfs",
                fallback_mode="local",
                local_storage_path="./data/audit_backup",
                degraded_features=["audit_backup", "distributed_storage"],
            ),
            "llm": FallbackConfig(
                service_name="llm",
                fallback_mode="cache",
                cache_ttl=7200,
                degraded_features=["generative_ai", "advanced_nlp"],
            ),
        }

        # Load custom configuration if exists
        self._load_custom_config()

    def _load_custom_config(self):
        """Load custom configuration from file"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, "r") as f:
                    custom_config = yaml.safe_load(f)
                    self._apply_custom_config(custom_config)
        except Exception as e:
            logger.warning(f"Failed to load custom config: {e}")

    def _apply_custom_config(self, config: Dict[str, Any]):
        """Apply custom configuration overrides"""
        if "services" in config:
            for service_name, service_config in config["services"].items():
                if service_name in self.services:
                    for key, value in service_config.items():
                        if hasattr(self.services[service_name], key):
                            setattr(self.services[service_name], key, value)

    def get_service_config(self, service_name: str) -> Optional[ServiceConfig]:
        """Get configuration for a specific service"""
        return self.services.get(service_name)

    def is_service_enabled(self, service_name: str) -> bool:
        """Check if a service is enabled and configured"""
        service = self.services.get(service_name)
        return service is not None and service.enabled

    def get_fallback_config(self, service_name: str) -> Optional[FallbackConfig]:
        """Get fallback configuration for a service"""
        return self.fallbacks.get(service_name)

    def should_use_fallback(self, service_name: str) -> bool:
        """Determine if fallback mode should be used"""
        service = self.services.get(service_name)
        fallback = self.fallbacks.get(service_name)

        if not service or not fallback:
            return False

        # Check if service is unhealthy
        if service.health_check_enabled and not self.health_status.get(
            service_name, True
        ):
            return True

        # Check if service is disabled but fallback is available
        if not service.enabled and fallback.fallback_mode != "disabled":
            return True

        return False

    async def health_check_service(self, service_name: str) -> bool:
        """Perform health check for a service"""
        service = self.services.get(service_name)
        if not service or not service.health_check_enabled:
            return True

        try:
            # Simple health check - can be enhanced with actual API calls
            if service_name == "dynex":
                # Check if Dynex API key is valid format
                is_healthy = service.api_key and service.api_key.startswith("dnx_")
            elif service_name == "ipfs":
                # Check if IPFS credentials are present
                is_healthy = service.metadata.get("project_id") and service.api_key
            elif service_name == "llm":
                # Check if LLM API key is valid format
                is_healthy = service.api_key and len(service.api_key) > 10
            else:
                is_healthy = True

            self.health_status[service_name] = is_healthy
            return is_healthy

        except Exception as e:
            logger.warning(f"Health check failed for {service_name}: {e}")
            self.health_status[service_name] = False
            return False

    def get_degraded_features(self) -> List[str]:
        """Get list of features that are currently degraded"""
        degraded = []
        for service_name in self.services:
            if self.should_use_fallback(service_name):
                fallback = self.fallbacks.get(service_name)
                if fallback:
                    degraded.extend(fallback.degraded_features)
        return list(set(degraded))

    def get_operational_status(self) -> Dict[str, Any]:
        """Get comprehensive operational status"""
        status = {
            "services": {},
            "fallbacks": {},
            "degraded_features": self.get_degraded_features(),
            "overall_health": "healthy",
        }

        for service_name, service in self.services.items():
            is_healthy = self.health_status.get(service_name, True)
            status["services"][service_name] = {
                "enabled": service.enabled,
                "healthy": is_healthy,
                "using_fallback": self.should_use_fallback(service_name),
                "fallback_mode": (
                    self.fallbacks.get(service_name).fallback_mode
                    if self.fallbacks.get(service_name)
                    else "none"
                ),
            }

        # Determine overall health
        unhealthy_services = sum(
            1 for s in status["services"].values() if not s["healthy"]
        )
        if unhealthy_services == 0:
            status["overall_health"] = "healthy"
        elif unhealthy_services <= len(self.services) // 2:
            status["overall_health"] = "degraded"
        else:
            status["overall_health"] = "critical"

        return status

    def create_fallback_storage(self, service_name: str) -> bool:
        """Create fallback storage directories"""
        fallback = self.fallbacks.get(service_name)
        if not fallback or not fallback.local_storage_path:
            return False

        try:
            Path(fallback.local_storage_path).mkdir(parents=True, exist_ok=True)
            logger.info(
                f"Created fallback storage for {service_name}: {fallback.local_storage_path}"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to create fallback storage for {service_name}: {e}")
            return False

    def save_configuration(self, config_path: Optional[str] = None):
        """Save current configuration to file"""
        save_path = config_path or self.config_path

        try:
            # Ensure directory exists
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)

            config_data = {"services": {}, "fallbacks": {}}

            # Convert services to dict
            for name, service in self.services.items():
                config_data["services"][name] = {
                    "enabled": service.enabled,
                    "endpoint": service.endpoint,
                    "fallback_enabled": service.fallback_enabled,
                    "health_check_enabled": service.health_check_enabled,
                    "retry_attempts": service.retry_attempts,
                    "timeout": service.timeout,
                }

            # Convert fallbacks to dict
            for name, fallback in self.fallbacks.items():
                config_data["fallbacks"][name] = {
                    "fallback_mode": fallback.fallback_mode,
                    "local_storage_path": fallback.local_storage_path,
                    "cache_ttl": fallback.cache_ttl,
                    "degraded_features": fallback.degraded_features,
                }

            with open(save_path, "w") as f:
                yaml.dump(config_data, f, default_flow_style=False)

            logger.info(f"Configuration saved to {save_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            return False


# Global configuration manager instance
_config_manager = None


def get_config_manager() -> ConfigurationManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigurationManager()
    return _config_manager


def initialize_configuration(config_path: Optional[str] = None) -> ConfigurationManager:
    """Initialize global configuration manager"""
    global _config_manager
    _config_manager = ConfigurationManager(config_path)
    return _config_manager
