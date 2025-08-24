"""
NQBA Stack - Neuromorphic Quantum Business Architecture
The foundational core for quantum-enhanced business operations

Core Components:
- Orchestrator: Central brain for task routing and coordination
- LTC Logger: Living Technical Codex for comprehensive traceability
- Dynex Adapter: Quantum optimization interface
- Settings: Centralized configuration management

Business Pods:
- FLYFOX AI: Industrial AI solutions and energy optimization
- Goliath Trade: Quantum finance and DeFi optimization
- Sigma Select: Sales intelligence and lead optimization
"""

from .core.orchestrator import (
    NQBAStackOrchestrator,
    get_orchestrator,
    submit_task,
    TaskRequest,
    TaskResult,
    BusinessPod
)

from .core.ltc_logger import (
    LTCLogger,
    get_ltc_logger,
    log_operation,
    LTCOperation
)

from .core.dynex_adapter import (
    DynexAdapter,
    DynexConfig,
    OptimizationResult,
    solve_qubo,
    score_leads
)

from .core.settings import (
    NQBASettings,
    get_settings,
    is_production,
    is_development,
    is_testing
)

# Version information
__version__ = "1.0.0"
__author__ = "NQBA Stack Team"
__description__ = "Neuromorphic Quantum Business Architecture Stack"

# Core exports
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

# Initialize core components on import
try:
    # Get global instances
    orchestrator = get_orchestrator()
    ltc_logger = get_ltc_logger()
    settings = get_settings()
    
    # Log successful initialization
    ltc_logger.log_operation(
        operation_type="nqba_stack_initialized",
        operation_data={
            "version": __version__,
            "components": ["orchestrator", "ltc_logger", "settings"],
            "status": "ready"
        },
        thread_ref="NQBA_STACK_INIT"
    )
    
except Exception as e:
    # Log initialization error
    print(f"Warning: NQBA Stack initialization failed: {e}")
    print("Some components may not be available")
