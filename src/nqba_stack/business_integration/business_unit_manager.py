"""
Business Unit Manager - Orchestrates all business units in the NQBA ecosystem.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BusinessUnit(ABC):
    """Abstract base class for all business units."""

    def __init__(self, name: str, unit_type: str):
        self.name = name
        self.unit_type = unit_type
        self.status = "initialized"
        self.created_at = datetime.now()
        self.last_activity = datetime.now()

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the business unit."""
        pass

    @abstractmethod
    async def get_status(self) -> Dict[str, Any]:
        """Get current status of the business unit."""
        pass

    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown the business unit."""
        pass


class BusinessUnitManager:
    """Manages all business units in the NQBA ecosystem."""

    def __init__(self):
        self.business_units: Dict[str, BusinessUnit] = {}
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.status = "initialized"
        self.created_at = datetime.now()

    async def initialize(self) -> bool:
        """Initialize the business unit manager."""
        try:
            logger.info("Initializing Business Unit Manager...")
            self.status = "initializing"

            # Initialize all registered business units
            for unit_name, unit in self.business_units.items():
                await unit.initialize()
                logger.info(f"Initialized business unit: {unit_name}")

            self.status = "operational"
            logger.info("Business Unit Manager initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize Business Unit Manager: {e}")
            self.status = "error"
            return False

    async def register_business_unit(self, business_unit: BusinessUnit) -> bool:
        """Register a new business unit."""
        try:
            if business_unit.name in self.business_units:
                logger.warning(f"Business unit {business_unit.name} already registered")
                return False

            self.business_units[business_unit.name] = business_unit
            logger.info(f"Registered business unit: {business_unit.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to register business unit {business_unit.name}: {e}")
            return False

    async def unregister_business_unit(self, unit_name: str) -> bool:
        """Unregister a business unit."""
        try:
            if unit_name not in self.business_units:
                logger.warning(f"Business unit {unit_name} not found")
                return False

            unit = self.business_units[unit_name]
            await unit.shutdown()
            del self.business_units[unit_name]
            logger.info(f"Unregistered business unit: {unit_name}")
            return True

        except Exception as e:
            logger.error(f"Failed to unregister business unit {unit_name}: {e}")
            return False

    async def get_business_unit(self, unit_name: str) -> Optional[BusinessUnit]:
        """Get a business unit by name."""
        return self.business_units.get(unit_name)

    async def get_all_business_units(self) -> List[BusinessUnit]:
        """Get all registered business units."""
        return list(self.business_units.values())

    async def get_ecosystem_status(self) -> Dict[str, Any]:
        """Get overall ecosystem status."""
        unit_statuses = {}
        for unit_name, unit in self.business_units.items():
            unit_statuses[unit_name] = await unit.get_status()

        return {
            "manager_status": self.status,
            "total_units": len(self.business_units),
            "unit_statuses": unit_statuses,
            "active_workflows": len(self.workflows),
            "created_at": self.created_at.isoformat(),
            "last_updated": datetime.now().isoformat(),
        }

    async def execute_workflow(
        self, workflow_id: str, workflow_steps: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute a workflow across multiple business units."""
        try:
            workflow_result = {
                "workflow_id": workflow_id,
                "status": "executing",
                "steps": [],
                "start_time": datetime.now(),
                "end_time": None,
            }

            self.workflows[workflow_id] = workflow_result

            for i, step in enumerate(workflow_steps):
                step_result = await self._execute_workflow_step(step)
                workflow_result["steps"].append(
                    {
                        "step_number": i + 1,
                        "step_name": step.get("name", f"step_{i+1}"),
                        "result": step_result,
                        "status": "completed",
                    }
                )

            workflow_result["status"] = "completed"
            workflow_result["end_time"] = datetime.now()

            logger.info(f"Workflow {workflow_id} completed successfully")
            return workflow_result

        except Exception as e:
            logger.error(f"Workflow {workflow_id} failed: {e}")
            if workflow_id in self.workflows:
                self.workflows[workflow_id]["status"] = "failed"
                self.workflows[workflow_id]["error"] = str(e)
            raise

    async def _execute_workflow_step(self, step: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow step."""
        try:
            unit_name = step.get("business_unit")
            operation = step.get("operation")
            parameters = step.get("parameters", {})

            if not unit_name or not operation:
                raise ValueError("Missing business_unit or operation in workflow step")

            unit = await self.get_business_unit(unit_name)
            if not unit:
                raise ValueError(f"Business unit {unit_name} not found")

            # Execute the operation
            if hasattr(unit, operation):
                method = getattr(unit, operation)
                if asyncio.iscoroutinefunction(method):
                    result = await method(**parameters)
                else:
                    result = method(**parameters)

                return {
                    "status": "success",
                    "result": result,
                    "execution_time_ms": 100,  # Simulated
                }
            else:
                raise ValueError(
                    f"Operation {operation} not found in business unit {unit_name}"
                )

        except Exception as e:
            logger.error(f"Workflow step execution failed: {e}")
            return {"status": "failed", "error": str(e), "execution_time_ms": 0}

    async def shutdown(self) -> bool:
        """Shutdown the business unit manager."""
        try:
            logger.info("Shutting down Business Unit Manager...")
            self.status = "shutting_down"

            # Shutdown all business units
            for unit_name, unit in self.business_units.items():
                await unit.shutdown()
                logger.info(f"Shutdown business unit: {unit_name}")

            self.status = "shutdown"
            logger.info("Business Unit Manager shutdown complete")
            return True

        except Exception as e:
            logger.error(f"Failed to shutdown Business Unit Manager: {e}")
            return False


# Global business unit manager instance
business_unit_manager = BusinessUnitManager()
