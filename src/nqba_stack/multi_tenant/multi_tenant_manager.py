"""
Multi-Tenant Manager for Phase 2
Customer isolation, dynamic resource management, and auto-scaling
"""

import asyncio
import uuid
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import logging
from enum import Enum
import json
import hashlib
import numpy as np

logger = logging.getLogger(__name__)

class TenantStatus(Enum):
    """Tenant status enumeration"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    PENDING = "pending"
    ARCHIVED = "archived"

class ResourceType(Enum):
    """Resource type enumeration"""
    COMPUTE = "compute"
    MEMORY = "memory"
    STORAGE = "storage"
    NETWORK = "network"
    QUANTUM_ACCESS = "quantum_access"

class ScalingPolicy(Enum):
    """Scaling policy enumeration"""
    MANUAL = "manual"
    AUTO = "auto"
    SCHEDULED = "scheduled"
    PREDICTIVE = "predictive"

@dataclass
class TenantConfig:
    """Configuration for a multi-tenant environment"""
    tenant_id: str
    name: str
    status: TenantStatus
    created_at: datetime
    last_updated: datetime
    
    # Resource limits
    resource_limits: Dict[str, float]
    scaling_policy: ScalingPolicy
    auto_scaling_config: Dict[str, Any]
    
    # Business rules
    business_rules: Dict[str, Any]
    sla_requirements: Dict[str, Any]
    
    # Security and isolation
    isolation_level: str  # 'strict', 'moderate', 'flexible'
    encryption_keys: Dict[str, str]
    access_controls: Dict[str, List[str]]
    
    # Performance monitoring
    performance_thresholds: Dict[str, float]
    alert_config: Dict[str, Any]
    
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ResourceAllocation:
    """Resource allocation for a tenant"""
    allocation_id: str
    tenant_id: str
    resource_type: ResourceType
    allocated_amount: float
    used_amount: float
    reserved_amount: float
    timestamp: datetime
    duration_hours: int
    cost_per_unit: float
    
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TenantMetrics:
    """Performance metrics for a tenant"""
    tenant_id: str
    timestamp: datetime
    
    # Resource utilization
    cpu_utilization: float
    memory_utilization: float
    storage_utilization: float
    network_utilization: float
    quantum_utilization: float
    
    # Performance metrics
    response_time: float
    throughput: float
    error_rate: float
    availability: float
    
    # Business metrics
    active_users: int
    operations_per_second: float
    revenue_per_hour: float
    
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ScalingDecision:
    """Scaling decision for a tenant"""
    decision_id: str
    tenant_id: str
    timestamp: datetime
    
    # Scaling details
    scaling_type: str  # 'scale_up', 'scale_down', 'maintain'
    resource_type: ResourceType
    current_allocation: float
    recommended_allocation: float
    scaling_factor: float
    
    # Decision factors
    trigger_metrics: Dict[str, float]
    business_impact: str
    cost_implications: float
    
    # Execution
    executed: bool = False
    execution_time: Optional[datetime] = None
    success: Optional[bool] = None
    
    metadata: Dict[str, Any] = field(default_factory=dict)

class MultiTenantManager:
    """Multi-tenant manager for customer isolation and scaling"""
    
    def __init__(self, max_tenants: int = 1000, max_resources_per_tenant: int = 100):
        self.max_tenants = max_tenants
        self.max_resources_per_tenant = max_resources_per_tenant
        
        # Core components
        self.tenants: Dict[str, TenantConfig] = {}
        self.resource_allocations: Dict[str, ResourceAllocation] = {}
        self.tenant_metrics: Dict[str, List[TenantMetrics]] = {}
        self.scaling_decisions: Dict[str, ScalingDecision] = {}
        
        # Resource pools
        self.available_resources: Dict[str, float] = {
            'compute': 1000.0,  # CPU cores
            'memory': 10000.0,  # GB
            'storage': 100000.0,  # GB
            'network': 1000.0,  # Mbps
            'quantum_access': 100.0  # Quantum operations per second
        }
        
        # Scaling configuration
        self.scaling_enabled = True
        self.scaling_check_interval = 300  # 5 minutes
        self.min_scaling_threshold = 0.1  # 10% change required
        
        # Performance monitoring
        self.metrics_retention_hours = 168  # 1 week
        self.alert_thresholds = {
            'cpu_utilization': 0.9,
            'memory_utilization': 0.85,
            'response_time': 2.0,  # seconds
            'error_rate': 0.05  # 5%
        }
        
        logger.info("Multi-Tenant Manager initialized")
    
    async def create_tenant(
        self,
        name: str,
        resource_limits: Dict[str, float],
        scaling_policy: ScalingPolicy = ScalingPolicy.AUTO,
        isolation_level: str = "moderate",
        business_rules: Dict[str, Any] = None,
        sla_requirements: Dict[str, Any] = None
    ) -> TenantConfig:
        """Create a new tenant with specified configuration"""
        try:
            # Check capacity
            if len(self.tenants) >= self.max_tenants:
                raise ValueError(f"Maximum tenant capacity reached: {self.max_tenants}")
            
            # Validate resource limits
            self._validate_resource_limits(resource_limits)
            
            # Check resource availability
            await self._check_resource_availability(resource_limits)
            
            # Generate tenant ID
            tenant_id = self._generate_tenant_id(name)
            
            # Create tenant configuration
            tenant_config = TenantConfig(
                tenant_id=tenant_id,
                name=name,
                status=TenantStatus.PENDING,
                created_at=datetime.now(),
                last_updated=datetime.now(),
                resource_limits=resource_limits,
                scaling_policy=scaling_policy,
                auto_scaling_config=self._get_default_scaling_config(scaling_policy),
                business_rules=business_rules or {},
                sla_requirements=sla_requirements or {},
                isolation_level=isolation_level,
                encryption_keys=self._generate_encryption_keys(),
                access_controls=self._get_default_access_controls(),
                performance_thresholds=self._get_default_performance_thresholds(),
                alert_config=self._get_default_alert_config(),
                metadata={
                    'created_by': 'system',
                    'version': '1.0.0'
                }
            )
            
            # Reserve resources
            await self._reserve_resources(tenant_id, resource_limits)
            
            # Initialize tenant metrics
            self.tenant_metrics[tenant_id] = []
            
            # Store tenant configuration
            self.tenants[tenant_id] = tenant_config
            
            # Activate tenant
            await self.activate_tenant(tenant_id)
            
            logger.info(f"Created tenant: {tenant_id} ({name})")
            return tenant_config
            
        except Exception as e:
            logger.error(f"Error creating tenant: {e}")
            raise
    
    def _validate_resource_limits(self, resource_limits: Dict[str, float]):
        """Validate resource limits against system constraints"""
        for resource_type, limit in resource_limits.items():
            if resource_type not in self.available_resources:
                raise ValueError(f"Invalid resource type: {resource_type}")
            
            if limit <= 0:
                raise ValueError(f"Resource limit must be positive: {resource_type}")
            
            if limit > self.available_resources[resource_type]:
                raise ValueError(f"Resource limit exceeds available capacity: {resource_type}")
    
    async def _check_resource_availability(self, resource_limits: Dict[str, float]) -> bool:
        """Check if requested resources are available"""
        for resource_type, requested_amount in resource_limits.items():
            available_amount = self.available_resources[resource_type]
            allocated_amount = sum(
                alloc.allocated_amount for alloc in self.resource_allocations.values()
                if alloc.resource_type.value == resource_type
            )
            
            if allocated_amount + requested_amount > available_amount:
                raise ValueError(f"Insufficient {resource_type} resources available")
        
        return True
    
    def _generate_tenant_id(self, name: str) -> str:
        """Generate a unique tenant ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
        return f"tenant_{name_hash}_{timestamp}"
    
    def _get_default_scaling_config(self, scaling_policy: ScalingPolicy) -> Dict[str, Any]:
        """Get default scaling configuration based on policy"""
        if scaling_policy == ScalingPolicy.AUTO:
            return {
                'min_scale': 0.5,
                'max_scale': 2.0,
                'scale_up_threshold': 0.8,
                'scale_down_threshold': 0.3,
                'cooldown_period': 300,  # 5 minutes
                'scaling_factor': 1.5
            }
        elif scaling_policy == ScalingPolicy.SCHEDULED:
            return {
                'schedule': {
                    'business_hours': {'start': '09:00', 'end': '17:00', 'scale_factor': 1.5},
                    'off_hours': {'start': '17:00', 'end': '09:00', 'scale_factor': 0.7}
                }
            }
        else:
            return {}
    
    def _generate_encryption_keys(self) -> Dict[str, str]:
        """Generate encryption keys for tenant isolation"""
        return {
            'data_encryption': hashlib.sha256(uuid.uuid4().bytes).hexdigest(),
            'communication_encryption': hashlib.sha256(uuid.uuid4().bytes).hexdigest(),
            'storage_encryption': hashlib.sha256(uuid.uuid4().bytes).hexdigest()
        }
    
    def _get_default_access_controls(self) -> Dict[str, List[str]]:
        """Get default access controls for new tenant"""
        return {
            'admin_users': [],
            'read_users': [],
            'write_users': [],
            'api_keys': [],
            'ip_whitelist': []
        }
    
    def _get_default_performance_thresholds(self) -> Dict[str, float]:
        """Get default performance thresholds"""
        return {
            'cpu_utilization': 0.8,
            'memory_utilization': 0.75,
            'response_time': 1.5,
            'error_rate': 0.02,
            'availability': 0.99
        }
    
    def _get_default_alert_config(self) -> Dict[str, Any]:
        """Get default alert configuration"""
        return {
            'email_alerts': True,
            'webhook_alerts': False,
            'alert_frequency': 'immediate',
            'escalation_rules': []
        }
    
    async def _reserve_resources(self, tenant_id: str, resource_limits: Dict[str, float]):
        """Reserve resources for a tenant"""
        for resource_type, amount in resource_limits.items():
            allocation = ResourceAllocation(
                allocation_id=f"alloc_{len(self.resource_allocations) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                tenant_id=tenant_id,
                resource_type=ResourceType(resource_type),
                allocated_amount=amount,
                used_amount=0.0,
                reserved_amount=amount,
                timestamp=datetime.now(),
                duration_hours=8760,  # 1 year
                cost_per_unit=self._get_resource_cost(resource_type),
                metadata={'allocation_type': 'initial'}
            )
            
            self.resource_allocations[allocation.allocation_id] = allocation
    
    def _get_resource_cost(self, resource_type: str) -> float:
        """Get cost per unit for a resource type"""
        cost_map = {
            'compute': 0.1,      # $0.10 per CPU core per hour
            'memory': 0.05,      # $0.05 per GB per hour
            'storage': 0.01,     # $0.01 per GB per hour
            'network': 0.02,     # $0.02 per Mbps per hour
            'quantum_access': 1.0  # $1.00 per quantum operation
        }
        return cost_map.get(resource_type, 0.0)
    
    async def activate_tenant(self, tenant_id: str) -> bool:
        """Activate a tenant"""
        try:
            if tenant_id not in self.tenants:
                raise ValueError(f"Tenant not found: {tenant_id}")
            
            tenant = self.tenants[tenant_id]
            tenant.status = TenantStatus.ACTIVE
            tenant.last_updated = datetime.now()
            
            logger.info(f"Activated tenant: {tenant_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error activating tenant: {e}")
            return False
    
    async def suspend_tenant(self, tenant_id: str, reason: str = "Administrative action") -> bool:
        """Suspend a tenant"""
        try:
            if tenant_id not in self.tenants:
                raise ValueError(f"Tenant not found: {tenant_id}")
            
            tenant = self.tenants[tenant_id]
            tenant.status = TenantStatus.SUSPENDED
            tenant.last_updated = datetime.now()
            tenant.metadata['suspension_reason'] = reason
            tenant.metadata['suspended_at'] = datetime.now().isoformat()
            
            # Release resources (optional - can keep reserved)
            # await self._release_resources(tenant_id)
            
            logger.info(f"Suspended tenant: {tenant_id} - {reason}")
            return True
            
        except Exception as e:
            logger.error(f"Error suspending tenant: {e}")
            return False
    
    async def record_tenant_metrics(
        self,
        tenant_id: str,
        metrics_data: Dict[str, Any]
    ) -> str:
        """Record performance metrics for a tenant"""
        try:
            if tenant_id not in self.tenants:
                raise ValueError(f"Tenant not found: {tenant_id}")
            
            # Create metrics object
            metrics = TenantMetrics(
                tenant_id=tenant_id,
                timestamp=datetime.now(),
                cpu_utilization=metrics_data.get('cpu_utilization', 0.0),
                memory_utilization=metrics_data.get('memory_utilization', 0.0),
                storage_utilization=metrics_data.get('storage_utilization', 0.0),
                network_utilization=metrics_data.get('network_utilization', 0.0),
                quantum_utilization=metrics_data.get('quantum_utilization', 0.0),
                response_time=metrics_data.get('response_time', 0.0),
                throughput=metrics_data.get('throughput', 0.0),
                error_rate=metrics_data.get('error_rate', 0.0),
                availability=metrics_data.get('availability', 1.0),
                active_users=metrics_data.get('active_users', 0),
                operations_per_second=metrics_data.get('operations_per_second', 0.0),
                revenue_per_hour=metrics_data.get('revenue_per_hour', 0.0),
                metadata=metrics_data.get('metadata', {})
            )
            
            # Store metrics
            if tenant_id not in self.tenant_metrics:
                self.tenant_metrics[tenant_id] = []
            
            self.tenant_metrics[tenant_id].append(metrics)
            
            # Check for scaling triggers
            if self.scaling_enabled and self.tenants[tenant_id].scaling_policy != ScalingPolicy.MANUAL:
                await self._check_scaling_triggers(tenant_id, metrics)
            
            # Check for SLA violations
            await self._check_sla_violations(tenant_id, metrics)
            
            # Clean up old metrics
            await self._cleanup_old_metrics(tenant_id)
            
            return f"metrics_{len(self.tenant_metrics[tenant_id])}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
        except Exception as e:
            logger.error(f"Error recording tenant metrics: {e}")
            raise
    
    async def _check_scaling_triggers(self, tenant_id: str, metrics: TenantMetrics):
        """Check if scaling is needed based on metrics"""
        try:
            tenant = self.tenants[tenant_id]
            scaling_config = tenant.auto_scaling_config
            
            if not scaling_config:
                return
            
            # Check CPU utilization scaling
            if metrics.cpu_utilization > scaling_config.get('scale_up_threshold', 0.8):
                await self._create_scaling_decision(
                    tenant_id, 'scale_up', 'compute', 
                    metrics.cpu_utilization, scaling_config.get('scaling_factor', 1.5)
                )
            elif metrics.cpu_utilization < scaling_config.get('scale_down_threshold', 0.3):
                await self._create_scaling_decision(
                    tenant_id, 'scale_down', 'compute',
                    metrics.cpu_utilization, 1.0 / scaling_config.get('scaling_factor', 1.5)
                )
            
            # Check memory utilization scaling
            if metrics.memory_utilization > scaling_config.get('scale_up_threshold', 0.8):
                await self._create_scaling_decision(
                    tenant_id, 'scale_up', 'memory',
                    metrics.memory_utilization, scaling_config.get('scaling_factor', 1.5)
                )
            
            # Check response time scaling
            if metrics.response_time > tenant.performance_thresholds.get('response_time', 1.5):
                await self._create_scaling_decision(
                    tenant_id, 'scale_up', 'compute',
                    metrics.response_time, scaling_config.get('scaling_factor', 1.5)
                )
            
        except Exception as e:
            logger.error(f"Error checking scaling triggers: {e}")
    
    async def _create_scaling_decision(
        self,
        tenant_id: str,
        scaling_type: str,
        resource_type: str,
        current_value: float,
        scaling_factor: float
    ) -> str:
        """Create a scaling decision"""
        try:
            # Get current resource allocation
            current_allocation = self._get_current_resource_allocation(tenant_id, resource_type)
            
            # Calculate recommended allocation
            recommended_allocation = current_allocation * scaling_factor
            
            # Check if scaling meets minimum threshold
            if abs(recommended_allocation - current_allocation) / current_allocation < self.min_scaling_threshold:
                return ""
            
            # Create scaling decision
            decision = ScalingDecision(
                decision_id=f"scale_{len(self.scaling_decisions) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                tenant_id=tenant_id,
                timestamp=datetime.now(),
                scaling_type=scaling_type,
                resource_type=ResourceType(resource_type),
                current_allocation=current_allocation,
                recommended_allocation=recommended_allocation,
                scaling_factor=scaling_factor,
                trigger_metrics={'current_value': current_value},
                business_impact='performance_optimization',
                cost_implications=self._calculate_scaling_cost(resource_type, current_allocation, recommended_allocation),
                metadata={'auto_generated': True}
            )
            
            self.scaling_decisions[decision.decision_id] = decision
            
            # Execute scaling if auto-execution is enabled
            if self.tenants[tenant_id].scaling_policy == ScalingPolicy.AUTO:
                await self._execute_scaling_decision(decision.decision_id)
            
            logger.info(f"Created scaling decision: {decision.decision_id} for tenant {tenant_id}")
            return decision.decision_id
            
        except Exception as e:
            logger.error(f"Error creating scaling decision: {e}")
            return ""
    
    def _get_current_resource_allocation(self, tenant_id: str, resource_type: str) -> float:
        """Get current resource allocation for a tenant"""
        for allocation in self.resource_allocations.values():
            if (allocation.tenant_id == tenant_id and 
                allocation.resource_type.value == resource_type):
                return allocation.allocated_amount
        return 0.0
    
    def _calculate_scaling_cost(self, resource_type: str, current: float, recommended: float) -> float:
        """Calculate cost implications of scaling"""
        cost_per_unit = self._get_resource_cost(resource_type)
        return (recommended - current) * cost_per_unit
    
    async def _execute_scaling_decision(self, decision_id: str) -> bool:
        """Execute a scaling decision"""
        try:
            if decision_id not in self.scaling_decisions:
                raise ValueError(f"Scaling decision not found: {decision_id}")
            
            decision = self.scaling_decisions[decision_id]
            tenant_id = decision.tenant_id
            
            # Check resource availability for scale up
            if decision.scaling_type == 'scale_up':
                resource_needed = decision.recommended_allocation - decision.current_allocation
                if not await self._check_resource_availability({decision.resource_type.value: resource_needed}):
                    logger.warning(f"Insufficient resources for scaling decision: {decision_id}")
                    return False
            
            # Update resource allocation
            await self._update_resource_allocation(
                tenant_id, 
                decision.resource_type.value, 
                decision.recommended_allocation
            )
            
            # Mark decision as executed
            decision.executed = True
            decision.execution_time = datetime.now()
            decision.success = True
            
            logger.info(f"Executed scaling decision: {decision_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error executing scaling decision: {e}")
            if decision_id in self.scaling_decisions:
                decision = self.scaling_decisions[decision_id]
                decision.executed = True
                decision.execution_time = datetime.now()
                decision.success = False
            return False
    
    async def _update_resource_allocation(
        self,
        tenant_id: str,
        resource_type: str,
        new_amount: float
    ):
        """Update resource allocation for a tenant"""
        for allocation in self.resource_allocations.values():
            if (allocation.tenant_id == tenant_id and 
                allocation.resource_type.value == resource_type):
                allocation.allocated_amount = new_amount
                allocation.last_updated = datetime.now()
                allocation.metadata['last_scaling'] = datetime.now().isoformat()
                break
    
    async def _check_sla_violations(self, tenant_id: str, metrics: TenantMetrics):
        """Check for SLA violations based on metrics"""
        try:
            tenant = self.tenants[tenant_id]
            sla_requirements = tenant.sla_requirements
            
            violations = []
            
            # Check response time SLA
            if 'response_time' in sla_requirements:
                max_response_time = sla_requirements['response_time']
                if metrics.response_time > max_response_time:
                    violations.append(f"Response time SLA violation: {metrics.response_time}s > {max_response_time}s")
            
            # Check availability SLA
            if 'availability' in sla_requirements:
                min_availability = sla_requirements['availability']
                if metrics.availability < min_availability:
                    violations.append(f"Availability SLA violation: {metrics.availability} < {min_availability}")
            
            # Check error rate SLA
            if 'error_rate' in sla_requirements:
                max_error_rate = sla_requirements['error_rate']
                if metrics.error_rate > max_error_rate:
                    violations.append(f"Error rate SLA violation: {metrics.error_rate} > {max_error_rate}")
            
            # Log violations
            if violations:
                logger.warning(f"SLA violations for tenant {tenant_id}: {violations}")
                # Could trigger alerts or notifications here
            
        except Exception as e:
            logger.error(f"Error checking SLA violations: {e}")
    
    async def _cleanup_old_metrics(self, tenant_id: str):
        """Clean up old metrics for a tenant"""
        try:
            if tenant_id not in self.tenant_metrics:
                return
            
            cutoff_time = datetime.now() - timedelta(hours=self.metrics_retention_hours)
            
            # Remove old metrics
            self.tenant_metrics[tenant_id] = [
                m for m in self.tenant_metrics[tenant_id]
                if m.timestamp >= cutoff_time
            ]
            
        except Exception as e:
            logger.error(f"Error cleaning up old metrics: {e}")
    
    async def get_tenant_analytics(self, tenant_id: str) -> Dict[str, Any]:
        """Get analytics for a specific tenant"""
        try:
            if tenant_id not in self.tenants:
                raise ValueError(f"Tenant not found: {tenant_id}")
            
            tenant = self.tenants[tenant_id]
            metrics = self.tenant_metrics.get(tenant_id, [])
            
            if not metrics:
                return {'tenant_id': tenant_id, 'no_metrics': True}
            
            # Calculate averages over last 24 hours
            recent_metrics = [m for m in metrics if m.timestamp >= datetime.now() - timedelta(hours=24)]
            
            if not recent_metrics:
                return {'tenant_id': tenant_id, 'no_recent_metrics': True}
            
            analytics = {
                'tenant_id': tenant_id,
                'tenant_name': tenant.name,
                'status': tenant.status.value,
                'last_updated': tenant.last_updated.isoformat(),
                
                'resource_utilization': {
                    'cpu': np.mean([m.cpu_utilization for m in recent_metrics]),
                    'memory': np.mean([m.memory_utilization for m in recent_metrics]),
                    'storage': np.mean([m.storage_utilization for m in recent_metrics]),
                    'network': np.mean([m.network_utilization for m in recent_metrics]),
                    'quantum': np.mean([m.quantum_utilization for m in recent_metrics])
                },
                
                'performance_metrics': {
                    'response_time': np.mean([m.response_time for m in recent_metrics]),
                    'throughput': np.mean([m.throughput for m in recent_metrics]),
                    'error_rate': np.mean([m.error_rate for m in recent_metrics]),
                    'availability': np.mean([m.availability for m in recent_metrics])
                },
                
                'business_metrics': {
                    'active_users': np.mean([m.active_users for m in recent_metrics]),
                    'operations_per_second': np.mean([m.operations_per_second for m in recent_metrics]),
                    'revenue_per_hour': np.mean([m.revenue_per_hour for m in recent_metrics])
                },
                
                'scaling_info': {
                    'scaling_policy': tenant.scaling_policy.value,
                    'recent_scaling_decisions': len([
                        d for d in self.scaling_decisions.values()
                        if d.tenant_id == tenant_id and d.timestamp >= datetime.now() - timedelta(hours=24)
                    ])
                }
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting tenant analytics: {e}")
            return {'error': str(e)}
    
    async def get_system_analytics(self) -> Dict[str, Any]:
        """Get system-wide analytics"""
        try:
            total_tenants = len(self.tenants)
            active_tenants = len([t for t in self.tenants.values() if t.status == TenantStatus.ACTIVE])
            
            # Resource utilization across all tenants
            total_allocated = {}
            total_used = {}
            
            for allocation in self.resource_allocations.values():
                resource_type = allocation.resource_type.value
                if resource_type not in total_allocated:
                    total_allocated[resource_type] = 0.0
                    total_used[resource_type] = 0.0
                
                total_allocated[resource_type] += allocation.allocated_amount
                total_used[resource_type] += allocation.used_amount
            
            # Calculate utilization percentages
            resource_utilization = {}
            for resource_type in total_allocated:
                if self.available_resources[resource_type] > 0:
                    resource_utilization[resource_type] = {
                        'allocated': total_allocated[resource_type],
                        'used': total_used[resource_type],
                        'available': self.available_resources[resource_type],
                        'utilization_percent': (total_allocated[resource_type] / self.available_resources[resource_type]) * 100
                    }
            
            # Scaling activity
            recent_scaling_decisions = len([
                d for d in self.scaling_decisions.values()
                if d.timestamp >= datetime.now() - timedelta(hours=24)
            ])
            
            # SLA compliance
            sla_violations = 0
            total_sla_checks = 0
            
            for tenant_id in self.tenants:
                metrics = self.tenant_metrics.get(tenant_id, [])
                if metrics:
                    recent_metrics = metrics[-1]  # Latest metrics
                    tenant = self.tenants[tenant_id]
                    
                    # Check response time SLA
                    if 'response_time' in tenant.sla_requirements:
                        total_sla_checks += 1
                        if recent_metrics.response_time > tenant.sla_requirements['response_time']:
                            sla_violations += 1
                    
                    # Check availability SLA
                    if 'availability' in tenant.sla_requirements:
                        total_sla_checks += 1
                        if recent_metrics.availability < tenant.sla_requirements['availability']:
                            sla_violations += 1
            
            sla_compliance_rate = (total_sla_checks - sla_violations) / max(total_sla_checks, 1) * 100
            
            return {
                'system_overview': {
                    'total_tenants': total_tenants,
                    'active_tenants': active_tenants,
                    'tenant_activation_rate': active_tenants / max(total_tenants, 1) * 100
                },
                
                'resource_management': {
                    'available_resources': self.available_resources,
                    'resource_utilization': resource_utilization,
                    'total_allocations': len(self.resource_allocations)
                },
                
                'scaling_activity': {
                    'recent_scaling_decisions': recent_scaling_decisions,
                    'scaling_enabled': self.scaling_enabled,
                    'total_scaling_decisions': len(self.scaling_decisions)
                },
                
                'sla_compliance': {
                    'sla_compliance_rate': sla_compliance_rate,
                    'total_sla_checks': total_sla_checks,
                    'sla_violations': sla_violations
                },
                
                'performance_monitoring': {
                    'metrics_retention_hours': self.metrics_retention_hours,
                    'total_metrics_records': sum(len(metrics) for metrics in self.tenant_metrics.values())
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system analytics: {e}")
            return {'error': str(e)}
    
    async def cleanup_old_data(self, max_age_hours: int = 168):
        """Clean up old data across all tenants"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            
            # Clean up old metrics
            for tenant_id in self.tenant_metrics:
                self.tenant_metrics[tenant_id] = [
                    m for m in self.tenant_metrics[tenant_id]
                    if m.timestamp >= cutoff_time
                ]
            
            # Clean up old scaling decisions
            old_decisions = [
                d_id for d_id, decision in self.scaling_decisions.items()
                if decision.timestamp < cutoff_time
            ]
            
            for decision_id in old_decisions:
                del self.scaling_decisions[decision_id]
            
            logger.info(f"Cleaned up old data: {len(old_decisions)} scaling decisions")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            raise
