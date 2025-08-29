"""
NQBA Business Unit Integration Module

This module provides the communication layer and integration framework
for FLYFOX AI, Goliath of All Trade, and Sigma Select business units.
"""

from .core import (
    BusinessUnitManager, 
    BusinessUnitInterface, 
    BusinessUnitType, 
    BusinessUnitStatus,
    BusinessUnitConfig,
    BusinessUnitMetrics,
    business_unit_manager
)
from .flyfox_ai import FLYFOXAIBusinessUnit

__all__ = [
    "BusinessUnitManager",
    "BusinessUnitInterface",
    "BusinessUnitType", 
    "BusinessUnitStatus",
    "BusinessUnitConfig",
    "BusinessUnitMetrics",
    "business_unit_manager",
    "FLYFOXAIBusinessUnit"
]
