"""
NQBA Business Unit Core Framework

Defines the base interface and management system for all business units
in the NQBA ecosystem.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class BusinessUnitType(Enum):
    """Business unit types in the NQBA ecosystem"""

    FLYFOX_AI = "flyfox_ai"
    GOLIATH_TRADE = "goliath_trade"
    SIGMA_SELECT = "sigma_select"


class BusinessUnitStatus(Enum):
    """Business unit operational status"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"
    ERROR = "error"


@dataclass
class BusinessUnitMetrics:
    """Business unit performance metrics"""

    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    average_response_time: float = 0.0
    quantum_advantage: float = 1.0
    last_operation: Optional[datetime] = None
    uptime_percentage: float = 100.0
    revenue_impact: float = 0.0
    efficiency_score: float = 0.0


@dataclass
class BusinessUnitConfig:
    """Business unit configuration"""

    unit_id: str
    unit_type: BusinessUnitType
    name: str
    description: str
    version: str
    api_endpoint: str
    enabled: bool = True
    max_concurrent_operations: int = 100
    timeout_seconds: int = 30
    retry_attempts: int = 3
    quantum_enhancement: bool = True
    monitoring_enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class BusinessUnitInterface(ABC):
    """Abstract base class for all business units"""

    def __init__(self, config: BusinessUnitConfig):
        self.config = config
        self.status = BusinessUnitStatus.INACTIVE
        self.metrics = BusinessUnitMetrics()
        self.last_health_check = None
        self.operation_queue = asyncio.Queue(maxsize=config.max_concurrent_operations)

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the business unit"""
        pass

    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the business unit"""
        pass

    @abstractmethod
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        pass

    @abstractmethod
    async def get_capabilities(self) -> Dict[str, Any]:
        """Get business unit capabilities"""
        pass

    @abstractmethod
    async def execute_operation(
        self, operation_type: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a business operation"""
        pass

    async def update_metrics(self, operation_result: Dict[str, Any]):
        """Update business unit metrics"""
        self.metrics.total_operations += 1

        if operation_result.get("success", False):
            self.metrics.successful_operations += 1
        else:
            self.metrics.failed_operations += 1

        response_time = operation_result.get("response_time", 0.0)
        if response_time > 0:
            # Update average response time
            total_time = self.metrics.average_response_time * (
                self.metrics.total_operations - 1
            )
            self.metrics.average_response_time = (
                total_time + response_time
            ) / self.metrics.total_operations

        self.metrics.last_operation = datetime.now(timezone.utc)

        # Update quantum advantage if available
        quantum_adv = operation_result.get("quantum_advantage", 1.0)
        if quantum_adv > 1.0:
            self.metrics.quantum_advantage = quantum_adv

    async def get_status_report(self) -> Dict[str, Any]:
        """Get comprehensive status report"""
        return {
            "unit_id": self.config.unit_id,
            "unit_type": self.config.unit_type.value,
            "name": self.config.name,
            "status": self.status.value,
            "metrics": {
                "total_operations": self.metrics.total_operations,
                "successful_operations": self.metrics.successful_operations,
                "failed_operations": self.metrics.failed_operations,
                "average_response_time": self.metrics.average_response_time,
                "quantum_advantage": self.metrics.quantum_advantage,
                "last_operation": (
                    self.metrics.last_operation.isoformat()
                    if self.metrics.last_operation
                    else None
                ),
                "uptime_percentage": self.metrics.uptime_percentage,
                "revenue_impact": self.metrics.revenue_impact,
                "efficiency_score": self.metrics.efficiency_score,
            },
            "config": {
                "enabled": self.config.enabled,
                "api_endpoint": self.config.api_endpoint,
                "quantum_enhancement": self.config.quantum_enhancement,
                "max_concurrent_operations": self.config.max_concurrent_operations,
            },
            "last_health_check": (
                self.last_health_check.isoformat() if self.last_health_check else None
            ),
            "queue_size": self.operation_queue.qsize(),
        }


class BusinessUnitManager:
    """Manages all business units in the NQBA ecosystem"""

    def __init__(self):
        self.business_units: Dict[str, BusinessUnitInterface] = {}
        self.communication_layer = None
        self.monitoring_enabled = True
        self.auto_health_check = True
        self.health_check_interval = 60  # seconds

    async def register_business_unit(
        self, business_unit: BusinessUnitInterface
    ) -> bool:
        """Register a business unit with the manager"""
        try:
            unit_id = business_unit.config.unit_id

            if unit_id in self.business_units:
                logger.warning(
                    f"Business unit {unit_id} already registered, updating..."
                )

            # Initialize the business unit
            if await business_unit.initialize():
                self.business_units[unit_id] = business_unit
                business_unit.status = BusinessUnitStatus.ACTIVE
                logger.info(f"Business unit {unit_id} registered successfully")
                return True
            else:
                logger.error(f"Failed to initialize business unit {unit_id}")
                return False

        except Exception as e:
            logger.error(
                f"Error registering business unit {business_unit.config.unit_id}: {e}"
            )
            return False

    async def unregister_business_unit(self, unit_id: str) -> bool:
        """Unregister a business unit"""
        try:
            if unit_id in self.business_units:
                business_unit = self.business_units[unit_id]
                await business_unit.shutdown()
                del self.business_units[unit_id]
                logger.info(f"Business unit {unit_id} unregistered successfully")
                return True
            else:
                logger.warning(f"Business unit {unit_id} not found")
                return False

        except Exception as e:
            logger.error(f"Error unregistering business unit {unit_id}: {e}")
            return False

    async def get_business_unit(self, unit_id: str) -> Optional[BusinessUnitInterface]:
        """Get a business unit by ID"""
        return self.business_units.get(unit_id)

    async def get_all_business_units(self) -> List[BusinessUnitInterface]:
        """Get all registered business units"""
        return list(self.business_units.values())

    async def get_business_units_by_type(
        self, unit_type: BusinessUnitType
    ) -> List[BusinessUnitInterface]:
        """Get business units by type"""
        return [
            unit
            for unit in self.business_units.values()
            if unit.config.unit_type == unit_type
        ]

    async def execute_cross_unit_operation(
        self, operation_type: str, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute an operation that involves multiple business units"""
        try:
            # Identify which business units need to be involved
            involved_units = self._identify_involved_units(operation_type, parameters)

            if not involved_units:
                return {
                    "success": False,
                    "error": f"No business units found for operation: {operation_type}",
                }

            # Execute operations in parallel if possible
            results = {}
            for unit in involved_units:
                try:
                    result = await unit.execute_operation(operation_type, parameters)
                    results[unit.config.unit_id] = result
                except Exception as e:
                    results[unit.config.unit_id] = {"success": False, "error": str(e)}

            # Aggregate results
            return self._aggregate_cross_unit_results(operation_type, results)

        except Exception as e:
            logger.error(f"Error in cross-unit operation {operation_type}: {e}")
            return {"success": False, "error": str(e)}

    def _identify_involved_units(
        self, operation_type: str, parameters: Dict[str, Any]
    ) -> List[BusinessUnitInterface]:
        """Identify which business units should be involved in an operation"""
        involved_units = []

        # Simple rule-based identification - in production, this would be more sophisticated
        if (
            "energy" in operation_type.lower()
            or "consumption" in operation_type.lower()
        ):
            involved_units.extend(
                self.get_business_units_by_type(BusinessUnitType.FLYFOX_AI)
            )

        if (
            "trade" in operation_type.lower()
            or "portfolio" in operation_type.lower()
            or "financial" in operation_type.lower()
        ):
            involved_units.extend(
                self.get_business_units_by_type(BusinessUnitType.GOLIATH_TRADE)
            )

        if (
            "lead" in operation_type.lower()
            or "sales" in operation_type.lower()
            or "client" in operation_type.lower()
        ):
            involved_units.extend(
                self.get_business_units_by_type(BusinessUnitType.SIGMA_SELECT)
            )

        return involved_units

    def _aggregate_cross_unit_results(
        self, operation_type: str, results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Aggregate results from multiple business units"""
        successful_results = {
            k: v for k, v in results.items() if v.get("success", False)
        }
        failed_results = {
            k: v for k, v in results.items() if not v.get("success", False)
        }

        # Calculate overall success rate
        total_units = len(results)
        successful_units = len(successful_results)
        success_rate = successful_units / total_units if total_units > 0 else 0

        # Aggregate quantum advantages
        quantum_advantages = [
            r.get("quantum_advantage", 1.0) for r in successful_results.values()
        ]
        avg_quantum_advantage = (
            sum(quantum_advantages) / len(quantum_advantages)
            if quantum_advantages
            else 1.0
        )

        return {
            "success": success_rate > 0.5,  # Consider successful if majority succeed
            "operation_type": operation_type,
            "total_business_units": total_units,
            "successful_units": successful_units,
            "success_rate": success_rate,
            "average_quantum_advantage": avg_quantum_advantage,
            "results": results,
            "summary": {
                "successful": list(successful_results.keys()),
                "failed": list(failed_results.keys()),
                "overall_performance": (
                    "excellent"
                    if success_rate > 0.8
                    else "good" if success_rate > 0.6 else "fair"
                ),
            },
        }

    async def get_ecosystem_status(self) -> Dict[str, Any]:
        """Get overall ecosystem status"""
        try:
            all_units = await self.get_all_business_units()

            if not all_units:
                return {
                    "status": "no_business_units",
                    "message": "No business units registered",
                    "total_units": 0,
                    "active_units": 0,
                }

            active_units = [
                unit for unit in all_units if unit.status == BusinessUnitStatus.ACTIVE
            ]
            total_operations = sum(unit.metrics.total_operations for unit in all_units)
            total_quantum_advantage = sum(
                unit.metrics.quantum_advantage for unit in all_units
            )
            avg_quantum_advantage = (
                total_quantum_advantage / len(all_units) if all_units else 1.0
            )

            return {
                "status": (
                    "operational" if len(active_units) == len(all_units) else "degraded"
                ),
                "total_business_units": len(all_units),
                "active_business_units": len(active_units),
                "inactive_business_units": len(all_units) - len(active_units),
                "total_operations": total_operations,
                "average_quantum_advantage": avg_quantum_advantage,
                "ecosystem_health": (
                    "excellent" if len(active_units) == len(all_units) else "good"
                ),
                "business_units": {
                    unit.config.unit_id: await unit.get_status_report()
                    for unit in all_units
                },
            }

        except Exception as e:
            logger.error(f"Error getting ecosystem status: {e}")
            return {
                "status": "error",
                "error": str(e),
                "total_units": 0,
                "active_units": 0,
            }

    async def start_monitoring(self):
        """Start the monitoring system"""
        if not self.monitoring_enabled:
            return

        logger.info("Starting NQBA business unit monitoring...")

        while self.monitoring_enabled:
            try:
                # Perform health checks on all business units
                for unit in self.business_units.values():
                    try:
                        health_status = await unit.health_check()
                        if not health_status.get("healthy", False):
                            logger.warning(
                                f"Business unit {unit.config.unit_id} health check failed"
                            )
                            unit.status = BusinessUnitStatus.ERROR
                        else:
                            unit.status = BusinessUnitStatus.ACTIVE
                            unit.last_health_check = datetime.now(timezone.utc)
                    except Exception as e:
                        logger.error(
                            f"Health check failed for {unit.config.unit_id}: {e}"
                        )
                        unit.status = BusinessUnitStatus.ERROR

                # Wait for next health check
                await asyncio.sleep(self.health_check_interval)

            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(self.health_check_interval)

    async def stop_monitoring(self):
        """Stop the monitoring system"""
        self.monitoring_enabled = False
        logger.info("NQBA business unit monitoring stopped")


# Global business unit manager instance
business_unit_manager = BusinessUnitManager()
