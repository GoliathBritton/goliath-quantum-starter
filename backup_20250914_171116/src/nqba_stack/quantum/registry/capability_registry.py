"""
FLYFOX AI Quantum Hub - Capability Registry

Manages quantum capabilities and their mappings to providers.
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from uuid import UUID, uuid4

from ..schemas.core_models import (
    QuantumCapability,
    ProblemType,
    ResultFormat,
    ProviderInfo
)


class CapabilityRegistry:
    """Registry for quantum capabilities and their providers."""
    
    def __init__(self):
        self._capabilities: Dict[str, QuantumCapability] = {}
        self._capability_providers: Dict[str, Set[str]] = {}  # capability_name -> provider_names
        self._provider_capabilities: Dict[str, Set[str]] = {}  # provider_name -> capability_names
        self._lock = asyncio.Lock()
    
    async def register_capability(self, capability: QuantumCapability) -> bool:
        """Register a new capability."""
        async with self._lock:
            capability_id = f"{capability.provider}:{capability.name}"
            
            if capability_id in self._capabilities:
                return False  # Already registered
            
            self._capabilities[capability_id] = capability
            
            # Update provider mappings
            if capability.name not in self._capability_providers:
                self._capability_providers[capability.name] = set()
            self._capability_providers[capability.name].add(capability.provider)
            
            if capability.provider not in self._provider_capabilities:
                self._provider_capabilities[capability.provider] = set()
            self._provider_capabilities[capability.provider].add(capability.name)
            
            return True
    
    async def unregister_capability(self, provider: str, capability_name: str) -> bool:
        """Unregister a capability."""
        async with self._lock:
            capability_id = f"{provider}:{capability_name}"
            
            if capability_id not in self._capabilities:
                return False
            
            del self._capabilities[capability_id]
            
            # Update provider mappings
            if capability_name in self._capability_providers:
                self._capability_providers[capability_name].discard(provider)
                if not self._capability_providers[capability_name]:
                    del self._capability_providers[capability_name]
            
            if provider in self._provider_capabilities:
                self._provider_capabilities[provider].discard(capability_name)
                if not self._provider_capabilities[provider]:
                    del self._provider_capabilities[provider]
            
            return True
    
    async def get_capability(self, provider: str, capability_name: str) -> Optional[QuantumCapability]:
        """Get a specific capability."""
        async with self._lock:
            capability_id = f"{provider}:{capability_name}"
            return self._capabilities.get(capability_id)
    
    async def list_capabilities(
        self,
        provider: Optional[str] = None,
        problem_type: Optional[ProblemType] = None,
        result_format: Optional[ResultFormat] = None,
        available_only: bool = True
    ) -> List[QuantumCapability]:
        """List capabilities with optional filtering."""
        async with self._lock:
            capabilities = []
            
            for capability in self._capabilities.values():
                # Apply filters
                if provider and capability.provider != provider:
                    continue
                
                if problem_type and problem_type not in capability.problem_types:
                    continue
                
                if result_format and result_format not in capability.result_formats:
                    continue
                
                if available_only and not capability.is_available:
                    continue
                
                capabilities.append(capability)
            
            return capabilities
    
    async def find_best_capability(
        self,
        problem_type: ProblemType,
        result_format: ResultFormat,
        preferred_provider: Optional[str] = None,
        max_qubits: Optional[int] = None,
        max_runtime: Optional[int] = None
    ) -> Optional[QuantumCapability]:
        """Find the best capability for a given problem."""
        async with self._lock:
            candidates = []
            
            for capability in self._capabilities.values():
                if not capability.is_available:
                    continue
                
                if problem_type not in capability.problem_types:
                    continue
                
                if result_format not in capability.result_formats:
                    continue
                
                if max_qubits and capability.max_qubits and capability.max_qubits < max_qubits:
                    continue
                
                if max_runtime and capability.max_runtime and capability.max_runtime < max_runtime:
                    continue
                
                # Calculate score (lower is better)
                score = 0
                
                # Prefer preferred provider
                if preferred_provider and capability.provider == preferred_provider:
                    score -= 1000
                
                # Prefer lower cost
                if capability.cost_per_second:
                    score += capability.cost_per_second * 100
                
                # Prefer shorter typical runtime
                if capability.typical_runtime:
                    score += capability.typical_runtime
                
                candidates.append((score, capability))
            
            if not candidates:
                return None
            
            # Return the best candidate
            candidates.sort(key=lambda x: x[0])
            return candidates[0][1]
    
    async def get_capability_stats(self) -> Dict[str, Any]:
        """Get statistics about registered capabilities."""
        async with self._lock:
            stats = {
                "total_capabilities": len(self._capabilities),
                "total_providers": len(self._provider_capabilities),
                "capabilities_by_provider": {},
                "problem_types": {},
                "result_formats": {}
            }
            
            # Count capabilities by provider
            for provider, capabilities in self._provider_capabilities.items():
                stats["capabilities_by_provider"][provider] = len(capabilities)
            
            # Count problem types and result formats
            for capability in self._capabilities.values():
                for problem_type in capability.problem_types:
                    stats["problem_types"][problem_type.value] = stats["problem_types"].get(problem_type.value, 0) + 1
                
                for result_format in capability.result_formats:
                    stats["result_formats"][result_format.value] = stats["result_formats"].get(result_format.value, 0) + 1
            
            return stats
    
    async def update_capability_availability(self, provider: str, capability_name: str, is_available: bool) -> bool:
        """Update capability availability."""
        async with self._lock:
            capability = await self.get_capability(provider, capability_name)
            if not capability:
                return False
            
            capability.is_available = is_available
            return True
    
    async def cleanup_inactive_capabilities(self, max_age_hours: int = 24) -> int:
        """Clean up capabilities that haven't been updated recently."""
        async with self._lock:
            cutoff_time = datetime.utcnow().timestamp() - (max_age_hours * 3600)
            removed_count = 0
            
            capabilities_to_remove = []
            for capability_id, capability in self._capabilities.items():
                # This is a simplified check - in practice, you'd track last_updated
                # For now, we'll just check if it's marked as unavailable
                if not capability.is_available:
                    capabilities_to_remove.append(capability_id)
            
            for capability_id in capabilities_to_remove:
                provider, capability_name = capability_id.split(":", 1)
                if await self.unregister_capability(provider, capability_name):
                    removed_count += 1
            
            return removed_count


# Global registry instance
_capability_registry = CapabilityRegistry()


# Convenience functions
async def register_capability(capability: QuantumCapability) -> bool:
    """Register a capability in the global registry."""
    return await _capability_registry.register_capability(capability)


async def unregister_capability(provider: str, capability_name: str) -> bool:
    """Unregister a capability from the global registry."""
    return await _capability_registry.unregister_capability(provider, capability_name)


async def get_capability(provider: str, capability_name: str) -> Optional[QuantumCapability]:
    """Get a capability from the global registry."""
    return await _capability_registry.get_capability(provider, capability_name)


async def list_capabilities(
    provider: Optional[str] = None,
    problem_type: Optional[ProblemType] = None,
    result_format: Optional[ResultFormat] = None,
    available_only: bool = True
) -> List[QuantumCapability]:
    """List capabilities from the global registry."""
    return await _capability_registry.list_capabilities(
        provider=provider,
        problem_type=problem_type,
        result_format=result_format,
        available_only=available_only
    )


async def find_best_capability(
    problem_type: ProblemType,
    result_format: ResultFormat,
    preferred_provider: Optional[str] = None,
    max_qubits: Optional[int] = None,
    max_runtime: Optional[int] = None
) -> Optional[QuantumCapability]:
    """Find the best capability for a given problem."""
    return await _capability_registry.find_best_capability(
        problem_type=problem_type,
        result_format=result_format,
        preferred_provider=preferred_provider,
        max_qubits=max_qubits,
        max_runtime=max_runtime
    )
