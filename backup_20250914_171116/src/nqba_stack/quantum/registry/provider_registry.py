"""
FLYFOX AI Quantum Hub - Provider Registry

Manages quantum providers and their configurations.
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from uuid import UUID, uuid4

from ..schemas.core_models import (
    ProviderInfo,
    QuantumCapability,
    ProblemType,
    ResultFormat
)


class ProviderRegistry:
    """Registry for quantum providers and their configurations."""
    
    def __init__(self):
        self._providers: Dict[str, ProviderInfo] = {}
        self._provider_configs: Dict[str, Dict[str, Any]] = {}
        self._provider_status: Dict[str, Dict[str, Any]] = {}  # health, last_heartbeat, etc.
        self._lock = asyncio.Lock()
    
    async def register_provider(self, provider_info: ProviderInfo, config: Optional[Dict[str, Any]] = None) -> bool:
        """Register a new provider."""
        async with self._lock:
            if provider_info.name in self._providers:
                return False  # Already registered
            
            self._providers[provider_info.name] = provider_info
            self._provider_configs[provider_info.name] = config or {}
            self._provider_status[provider_info.name] = {
                "is_active": provider_info.is_active,
                "last_heartbeat": provider_info.last_heartbeat,
                "health_status": "unknown",
                "error_count": 0,
                "last_error": None
            }
            
            return True
    
    async def unregister_provider(self, provider_name: str) -> bool:
        """Unregister a provider."""
        async with self._lock:
            if provider_name not in self._providers:
                return False
            
            del self._providers[provider_name]
            del self._provider_configs[provider_name]
            del self._provider_status[provider_name]
            
            return True
    
    async def get_provider(self, provider_name: str) -> Optional[ProviderInfo]:
        """Get provider information."""
        async with self._lock:
            return self._providers.get(provider_name)
    
    async def list_providers(
        self,
        active_only: bool = True,
        problem_type: Optional[ProblemType] = None,
        result_format: Optional[ResultFormat] = None
    ) -> List[ProviderInfo]:
        """List providers with optional filtering."""
        async with self._lock:
            providers = []
            
            for provider in self._providers.values():
                # Apply filters
                if active_only and not provider.is_active:
                    continue
                
                if problem_type:
                    has_problem_type = any(
                        problem_type in capability.problem_types
                        for capability in provider.capabilities
                    )
                    if not has_problem_type:
                        continue
                
                if result_format:
                    has_result_format = any(
                        result_format in capability.result_formats
                        for capability in provider.capabilities
                    )
                    if not has_result_format:
                        continue
                
                providers.append(provider)
            
            return providers
    
    async def update_provider_status(self, provider_name: str, status_update: Dict[str, Any]) -> bool:
        """Update provider status."""
        async with self._lock:
            if provider_name not in self._provider_status:
                return False
            
            self._provider_status[provider_name].update(status_update)
            
            # Update the provider info if needed
            if provider_name in self._providers:
                if "is_active" in status_update:
                    self._providers[provider_name].is_active = status_update["is_active"]
                if "last_heartbeat" in status_update:
                    self._providers[provider_name].last_heartbeat = status_update["last_heartbeat"]
            
            return True
    
    async def get_provider_status(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """Get provider status."""
        async with self._lock:
            return self._provider_status.get(provider_name)
    
    async def get_provider_config(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """Get provider configuration."""
        async with self._lock:
            return self._provider_configs.get(provider_name)
    
    async def update_provider_config(self, provider_name: str, config_update: Dict[str, Any]) -> bool:
        """Update provider configuration."""
        async with self._lock:
            if provider_name not in self._provider_configs:
                return False
            
            self._provider_configs[provider_name].update(config_update)
            
            # Update the provider info if needed
            if provider_name in self._providers:
                self._providers[provider_name].config.update(config_update)
            
            return True
    
    async def add_provider_capability(self, provider_name: str, capability: QuantumCapability) -> bool:
        """Add a capability to a provider."""
        async with self._lock:
            if provider_name not in self._providers:
                return False
            
            # Check if capability already exists
            existing_capabilities = self._providers[provider_name].capabilities
            for existing in existing_capabilities:
                if existing.name == capability.name:
                    return False  # Already exists
            
            self._providers[provider_name].capabilities.append(capability)
            return True
    
    async def remove_provider_capability(self, provider_name: str, capability_name: str) -> bool:
        """Remove a capability from a provider."""
        async with self._lock:
            if provider_name not in self._providers:
                return False
            
            capabilities = self._providers[provider_name].capabilities
            for i, capability in enumerate(capabilities):
                if capability.name == capability_name:
                    del capabilities[i]
                    return True
            
            return False
    
    async def get_provider_capabilities(self, provider_name: str) -> List[QuantumCapability]:
        """Get all capabilities for a provider."""
        async with self._lock:
            if provider_name not in self._providers:
                return []
            
            return self._providers[provider_name].capabilities.copy()
    
    async def find_providers_for_problem(
        self,
        problem_type: ProblemType,
        result_format: ResultFormat,
        min_qubits: Optional[int] = None,
        max_cost_per_second: Optional[float] = None
    ) -> List[ProviderInfo]:
        """Find providers that can handle a specific problem."""
        async with self._lock:
            suitable_providers = []
            
            for provider in self._providers.values():
                if not provider.is_active:
                    continue
                
                # Check if provider has suitable capabilities
                has_suitable_capability = False
                for capability in provider.capabilities:
                    if problem_type not in capability.problem_types:
                        continue
                    
                    if result_format not in capability.result_formats:
                        continue
                    
                    if min_qubits and capability.max_qubits and capability.max_qubits < min_qubits:
                        continue
                    
                    if max_cost_per_second and capability.cost_per_second and capability.cost_per_second > max_cost_per_second:
                        continue
                    
                    has_suitable_capability = True
                    break
                
                if has_suitable_capability:
                    suitable_providers.append(provider)
            
            return suitable_providers
    
    async def get_provider_stats(self) -> Dict[str, Any]:
        """Get statistics about registered providers."""
        async with self._lock:
            stats = {
                "total_providers": len(self._providers),
                "active_providers": sum(1 for p in self._providers.values() if p.is_active),
                "providers_by_status": {},
                "capabilities_by_provider": {},
                "problem_types_by_provider": {}
            }
            
            # Count providers by status
            for provider_name, status in self._provider_status.items():
                health_status = status.get("health_status", "unknown")
                stats["providers_by_status"][health_status] = stats["providers_by_status"].get(health_status, 0) + 1
            
            # Count capabilities by provider
            for provider_name, provider in self._providers.items():
                stats["capabilities_by_provider"][provider_name] = len(provider.capabilities)
                
                # Count problem types by provider
                problem_types = set()
                for capability in provider.capabilities:
                    problem_types.update(capability.problem_types)
                stats["problem_types_by_provider"][provider_name] = len(problem_types)
            
            return stats
    
    async def cleanup_inactive_providers(self, max_inactive_hours: int = 24) -> int:
        """Clean up providers that have been inactive for too long."""
        async with self._lock:
            cutoff_time = datetime.utcnow().timestamp() - (max_inactive_hours * 3600)
            removed_count = 0
            
            providers_to_remove = []
            for provider_name, status in self._provider_status.items():
                last_heartbeat = status.get("last_heartbeat")
                if last_heartbeat and last_heartbeat.timestamp() < cutoff_time:
                    providers_to_remove.append(provider_name)
            
            for provider_name in providers_to_remove:
                if await self.unregister_provider(provider_name):
                    removed_count += 1
            
            return removed_count


# Global registry instance
_provider_registry = ProviderRegistry()


# Convenience functions
async def register_provider(provider_info: ProviderInfo, config: Optional[Dict[str, Any]] = None) -> bool:
    """Register a provider in the global registry."""
    return await _provider_registry.register_provider(provider_info, config)


async def unregister_provider(provider_name: str) -> bool:
    """Unregister a provider from the global registry."""
    return await _provider_registry.unregister_provider(provider_name)


async def get_provider(provider_name: str) -> Optional[ProviderInfo]:
    """Get a provider from the global registry."""
    return await _provider_registry.get_provider(provider_name)


async def list_providers(
    active_only: bool = True,
    problem_type: Optional[ProblemType] = None,
    result_format: Optional[ResultFormat] = None
) -> List[ProviderInfo]:
    """List providers from the global registry."""
    return await _provider_registry.list_providers(
        active_only=active_only,
        problem_type=problem_type,
        result_format=result_format
    )


async def get_provider_capabilities(provider_name: str) -> List[QuantumCapability]:
    """Get capabilities for a provider from the global registry."""
    return await _provider_registry.get_provider_capabilities(provider_name)


async def find_providers_for_problem(
    problem_type: ProblemType,
    result_format: ResultFormat,
    min_qubits: Optional[int] = None,
    max_cost_per_second: Optional[float] = None
) -> List[ProviderInfo]:
    """Find providers that can handle a specific problem."""
    return await _provider_registry.find_providers_for_problem(
        problem_type=problem_type,
        result_format=result_format,
        min_qubits=min_qubits,
        max_cost_per_second=max_cost_per_second
    )
