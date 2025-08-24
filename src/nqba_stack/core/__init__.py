"""
NQBA Stack Core Components
The foundational kernel of the Neuromorphic Quantum Business Architecture

Components:
- Orchestrator: Central task routing and coordination
- LTC Logger: Living Technical Codex for traceability
- Dynex Adapter: Quantum optimization interface
- Settings: Configuration management
"""

from .orchestrator import (
    NQBAStackOrchestrator,
    get_orchestrator,
    submit_task,
    TaskRequest,
    TaskResult,
    BusinessPod
)

from .ltc_logger import (
    LTCLogger,
    get_ltc_logger,
    log_operation,
    LTCOperation
)

from .dynex_adapter import (
    DynexAdapter,
    DynexConfig,
    OptimizationResult,
    solve_qubo,
    score_leads
)

from .settings import (
    NQBASettings,
    get_settings,
    is_production,
    is_development,
    is_testing
)

__all__ = [
    # Core classes
    "NQBAStackOrchestrator",
    "LTCLogger",
    "DynexAdapter", 
    "NQBASettings",
    
    # Core functions
    "get_orchestrator",
    "get_ltc_logger",
    "get_settings",
    "submit_task",
    "log_operation",
    "solve_qubo",
    "score_leads",
    
    # Utility functions
    "is_production",
    "is_development",
    "is_testing",
    
    # Data classes
    "TaskRequest",
    "TaskResult", 
    "BusinessPod",
    "LTCOperation",
    "DynexConfig",
    "OptimizationResult"
]
