"""Health Check System for Quantum Nexus Engine"""

import asyncio
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass, field
from fastapi import FastAPI
import aiohttp
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

# Configure logging
logger = logging.getLogger(__name__)

class HealthStatus(Enum):
    """Health check status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

class ComponentType(Enum):
    """Component types for health checks"""
    DATABASE = "database"
    REDIS = "redis"
    QUANTUM_BACKEND = "quantum_backend"
    EXTERNAL_API = "external_api"
    CELERY = "celery"
    FILE_SYSTEM = "file_system"
    NETWORK = "network"

@dataclass
class HealthCheckResult:
    """Result of a health check"""
    component: str
    component_type: ComponentType
    status: HealthStatus
    message: str
    response_time_ms: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'component': self.component,
            'component_type': self.component_type.value,
            'status': self.status.value,
            'message': self.message,
            'response_time_ms': self.response_time_ms,
            'timestamp': self.timestamp.isoformat(),
            'details': self.details
        }

@dataclass
class SystemHealthStatus:
    """Overall system health status"""
    status: HealthStatus
    components: List[HealthCheckResult]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    uptime_seconds: float = 0
    version: str = "1.0.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'status': self.status.value,
            'timestamp': self.timestamp.isoformat(),
            'uptime_seconds': self.uptime_seconds,
            'version': self.version,
            'components': [comp.to_dict() for comp in self.components]
        }

class HealthChecker:
    """Base health checker class"""
    
    def __init__(self, name: str, component_type: ComponentType, 
                 timeout_seconds: float = 5.0):
        self.name = name
        self.component_type = component_type
        self.timeout_seconds = timeout_seconds
    
    async def check(self) -> HealthCheckResult:
        """Perform health check"""
        start_time = time.time()
        
        try:
            # Perform the actual check with timeout
            result = await asyncio.wait_for(
                self._perform_check(),
                timeout=self.timeout_seconds
            )
            
            response_time = (time.time() - start_time) * 1000
            
            return HealthCheckResult(
                component=self.name,
                component_type=self.component_type,
                status=result.get('status', HealthStatus.UNKNOWN),
                message=result.get('message', 'Check completed'),
                response_time_ms=response_time,
                details=result.get('details', {})
            )
            
        except asyncio.TimeoutError:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                component=self.name,
                component_type=self.component_type,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check timed out after {self.timeout_seconds}s",
                response_time_ms=response_time
            )
            
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            return HealthCheckResult(
                component=self.name,
                component_type=self.component_type,
                status=HealthStatus.UNHEALTHY,
                message=f"Health check failed: {str(e)}",
                response_time_ms=response_time,
                details={'error': str(e), 'error_type': type(e).__name__}
            )
    
    async def _perform_check(self) -> Dict[str, Any]:
        """Override this method to implement specific health check logic"""
        raise NotImplementedError

class DatabaseHealthChecker(HealthChecker):
    """Database health checker"""
    
    def __init__(self, session_factory: Callable, name: str = "database"):
        super().__init__(name, ComponentType.DATABASE)
        self.session_factory = session_factory
    
    async def _perform_check(self) -> Dict[str, Any]:
        """Check database connectivity"""
        async with self.session_factory() as session:
            # Simple query to test connectivity
            result = await session.execute(text("SELECT 1"))
            row = result.fetchone()
            
            if row and row[0] == 1:
                return {
                    'status': HealthStatus.HEALTHY,
                    'message': 'Database connection successful',
                    'details': {'query_result': row[0]}
                }
            else:
                return {
                    'status': HealthStatus.UNHEALTHY,
                    'message': 'Database query returned unexpected result'
                }

class RedisHealthChecker(HealthChecker):
    """Redis health checker"""
    
    def __init__(self, redis_url: str, name: str = "redis"):
        super().__init__(name, ComponentType.REDIS)
        self.redis_url = redis_url
    
    async def _perform_check(self) -> Dict[str, Any]:
        """Check Redis connectivity"""
        redis_client = redis.from_url(self.redis_url)
        
        try:
            # Test basic operations
            test_key = f"health_check_{int(time.time())}"
            test_value = "test"
            
            # Set and get test value
            await redis_client.set(test_key, test_value, ex=60)
            retrieved_value = await redis_client.get(test_key)
            await redis_client.delete(test_key)
            
            # Get Redis info
            info = await redis_client.info()
            
            if retrieved_value and retrieved_value.decode() == test_value:
                return {
                    'status': HealthStatus.HEALTHY,
                    'message': 'Redis connection and operations successful',
                    'details': {
                        'redis_version': info.get('redis_version'),
                        'connected_clients': info.get('connected_clients'),
                        'used_memory_human': info.get('used_memory_human')
                    }
                }
            else:
                return {
                    'status': HealthStatus.UNHEALTHY,
                    'message': 'Redis operations failed'
                }
                
        finally:
            await redis_client.close()

class QuantumBackendHealthChecker(HealthChecker):
    """Quantum backend health checker"""
    
    def __init__(self, backend_name: str, backend_url: Optional[str] = None):
        super().__init__(f"quantum_backend_{backend_name}", ComponentType.QUANTUM_BACKEND)
        self.backend_name = backend_name
        self.backend_url = backend_url
    
    async def _perform_check(self) -> Dict[str, Any]:
        """Check quantum backend availability"""
        if self.backend_name == "dynex":
            return await self._check_dynex_backend()
        elif self.backend_name == "qiskit":
            return await self._check_qiskit_backend()
        else:
            return await self._check_generic_backend()
    
    async def _check_dynex_backend(self) -> Dict[str, Any]:
        """Check Dynex backend"""
        try:
            # This would integrate with actual Dynex SDK
            # For now, simulate the check
            import random
            
            # Simulate backend availability
            is_available = random.choice([True, True, True, False])  # 75% uptime
            
            if is_available:
                return {
                    'status': HealthStatus.HEALTHY,
                    'message': 'Dynex backend is available',
                    'details': {
                        'backend_type': 'dynex',
                        'simulated_check': True,
                        'queue_length': random.randint(0, 10)
                    }
                }
            else:
                return {
                    'status': HealthStatus.UNHEALTHY,
                    'message': 'Dynex backend is unavailable'
                }
                
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'message': f'Dynex backend check failed: {str(e)}'
            }
    
    async def _check_qiskit_backend(self) -> Dict[str, Any]:
        """Check Qiskit backend"""
        try:
            # This would integrate with actual Qiskit
            # For now, simulate the check
            return {
                'status': HealthStatus.HEALTHY,
                'message': 'Qiskit simulator is available',
                'details': {
                    'backend_type': 'qiskit_simulator',
                    'simulated_check': True
                }
            }
            
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'message': f'Qiskit backend check failed: {str(e)}'
            }
    
    async def _check_generic_backend(self) -> Dict[str, Any]:
        """Check generic quantum backend via HTTP"""
        if not self.backend_url:
            return {
                'status': HealthStatus.UNKNOWN,
                'message': 'No backend URL configured'
            }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.backend_url}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        'status': HealthStatus.HEALTHY,
                        'message': 'Backend is responding',
                        'details': data
                    }
                else:
                    return {
                        'status': HealthStatus.UNHEALTHY,
                        'message': f'Backend returned status {response.status}'
                    }

class CeleryHealthChecker(HealthChecker):
    """Celery worker health checker"""
    
    def __init__(self, broker_url: str, name: str = "celery"):
        super().__init__(name, ComponentType.CELERY)
        self.broker_url = broker_url
    
    async def _perform_check(self) -> Dict[str, Any]:
        """Check Celery workers"""
        try:
            # This would integrate with actual Celery inspection
            # For now, simulate the check
            import random
            
            active_workers = random.randint(1, 5)
            
            if active_workers > 0:
                return {
                    'status': HealthStatus.HEALTHY,
                    'message': f'{active_workers} Celery workers active',
                    'details': {
                        'active_workers': active_workers,
                        'simulated_check': True
                    }
                }
            else:
                return {
                    'status': HealthStatus.UNHEALTHY,
                    'message': 'No active Celery workers found'
                }
                
        except Exception as e:
            return {
                'status': HealthStatus.UNHEALTHY,
                'message': f'Celery check failed: {str(e)}'
            }

class ExternalAPIHealthChecker(HealthChecker):
    """External API health checker"""
    
    def __init__(self, api_name: str, api_url: str, expected_status: int = 200):
        super().__init__(f"external_api_{api_name}", ComponentType.EXTERNAL_API)
        self.api_url = api_url
        self.expected_status = expected_status
    
    async def _perform_check(self) -> Dict[str, Any]:
        """Check external API availability"""
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url) as response:
                if response.status == self.expected_status:
                    return {
                        'status': HealthStatus.HEALTHY,
                        'message': f'API responding with status {response.status}',
                        'details': {
                            'status_code': response.status,
                            'response_headers': dict(response.headers)
                        }
                    }
                else:
                    return {
                        'status': HealthStatus.DEGRADED,
                        'message': f'API returned unexpected status {response.status}',
                        'details': {'status_code': response.status}
                    }

class HealthCheckManager:
    """Manager for all health checks"""
    
    def __init__(self):
        self.checkers: List[HealthChecker] = []
        self.start_time = time.time()
        self.last_check_results: List[HealthCheckResult] = []
    
    def add_checker(self, checker: HealthChecker):
        """Add a health checker"""
        self.checkers.append(checker)
        logger.info(f"Added health checker: {checker.name}")
    
    def remove_checker(self, name: str):
        """Remove a health checker by name"""
        self.checkers = [c for c in self.checkers if c.name != name]
        logger.info(f"Removed health checker: {name}")
    
    async def check_all(self) -> SystemHealthStatus:
        """Run all health checks"""
        logger.info(f"Running {len(self.checkers)} health checks")
        
        # Run all checks concurrently
        tasks = [checker.check() for checker in self.checkers]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        check_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle exceptions from individual checks
                checker = self.checkers[i]
                check_results.append(HealthCheckResult(
                    component=checker.name,
                    component_type=checker.component_type,
                    status=HealthStatus.UNHEALTHY,
                    message=f"Health check exception: {str(result)}",
                    response_time_ms=0,
                    details={'exception': str(result)}
                ))
            else:
                check_results.append(result)
        
        self.last_check_results = check_results
        
        # Determine overall system status
        overall_status = self._calculate_overall_status(check_results)
        
        return SystemHealthStatus(
            status=overall_status,
            components=check_results,
            uptime_seconds=time.time() - self.start_time
        )
    
    def _calculate_overall_status(self, results: List[HealthCheckResult]) -> HealthStatus:
        """Calculate overall system health status"""
        if not results:
            return HealthStatus.UNKNOWN
        
        statuses = [result.status for result in results]
        
        # If any critical component is unhealthy, system is unhealthy
        critical_components = [ComponentType.DATABASE, ComponentType.REDIS]
        critical_results = [r for r in results if r.component_type in critical_components]
        
        if any(r.status == HealthStatus.UNHEALTHY for r in critical_results):
            return HealthStatus.UNHEALTHY
        
        # If any component is unhealthy, system is degraded
        if HealthStatus.UNHEALTHY in statuses:
            return HealthStatus.DEGRADED
        
        # If any component is degraded, system is degraded
        if HealthStatus.DEGRADED in statuses:
            return HealthStatus.DEGRADED
        
        # If all components are healthy, system is healthy
        if all(status == HealthStatus.HEALTHY for status in statuses):
            return HealthStatus.HEALTHY
        
        return HealthStatus.UNKNOWN
    
    async def check_component(self, component_name: str) -> Optional[HealthCheckResult]:
        """Check specific component"""
        checker = next((c for c in self.checkers if c.name == component_name), None)
        if checker:
            return await checker.check()
        return None
    
    def get_last_results(self) -> List[HealthCheckResult]:
        """Get last check results"""
        return self.last_check_results.copy()

def setup_health_checks(app: FastAPI, 
                       database_session_factory=None,
                       redis_url: str = "redis://localhost:6379",
                       celery_broker_url: str = "redis://localhost:6379") -> HealthCheckManager:
    """Setup health checks for FastAPI application"""
    
    manager = HealthCheckManager()
    
    # Add database health check if session factory provided
    if database_session_factory:
        manager.add_checker(DatabaseHealthChecker(database_session_factory))
    
    # Add Redis health check
    manager.add_checker(RedisHealthChecker(redis_url))
    
    # Add Celery health check
    manager.add_checker(CeleryHealthChecker(celery_broker_url))
    
    # Add quantum backend health checks
    manager.add_checker(QuantumBackendHealthChecker("dynex"))
    manager.add_checker(QuantumBackendHealthChecker("qiskit"))
    
    # Add external API health checks (examples)
    # manager.add_checker(ExternalAPIHealthChecker("openai", "https://api.openai.com/v1/models"))
    
    # Add health endpoints to FastAPI app
    @app.get('/health')
    async def health_check():
        """Quick health check endpoint"""
        return {
            'status': 'healthy',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'service': 'quantum-nexus-engine'
        }
    
    @app.get('/health/detailed')
    async def detailed_health_check():
        """Detailed health check endpoint"""
        system_health = await manager.check_all()
        return system_health.to_dict()
    
    @app.get('/health/component/{component_name}')
    async def component_health_check(component_name: str):
        """Check specific component health"""
        result = await manager.check_component(component_name)
        if result:
            return result.to_dict()
        else:
            return {'error': f'Component {component_name} not found'}
    
    logger.info(f"Health check system initialized with {len(manager.checkers)} checkers")
    return manager

# Global health check manager
_health_manager = None

def get_health_manager() -> Optional[HealthCheckManager]:
    """Get global health check manager"""
    return _health_manager

def set_health_manager(manager: HealthCheckManager):
    """Set global health check manager"""
    global _health_manager
    _health_manager = manager