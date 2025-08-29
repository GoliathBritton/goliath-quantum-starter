"""
NQBA Stack Core Components
The foundational kernel of the Neuromorphic Quantum Business Architecture

Components:
- Orchestrator: Central task routing and coordination
- LTC Logger: Living Technical Codex for traceability
- Dynex Adapter: Quantum optimization interface
- Settings: Configuration management
- Quantum High Council: 95%+ automated governance
- Quantum Digital Agents: Digital strategy and orchestration
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

# Quantum High Council
from .quantum_high_council import (
    QuantumHighCouncil,
    QHCDecisionType,
    QHCBusinessUnit,
    QHCMemberRole,
    QHCDecision,
    QHCMember,
    get_quantum_high_council,
    initialize_quantum_high_council
)

# Quantum Digital Agents
from .quantum_digital_agents import (
    QuantumDigitalAgentOrchestrator,
    QuantumDigitalAgentType,
    DigitalOperationType,
    DigitalOperation,
    QuantumDigitalAgent,
    get_quantum_digital_agent_orchestrator,
    initialize_quantum_digital_agent_orchestrator
)

__all__ = [
    # Core classes
    "NQBAStackOrchestrator",
    "LTCLogger",
    "DynexAdapter", 
    "NQBASettings",
    
    # Quantum High Council
    "QuantumHighCouncil",
    "QHCDecisionType",
    "QHCBusinessUnit",
    "QHCMemberRole",
    "QHCDecision",
    "QHCMember",
    
    # Quantum Digital Agents
    "QuantumDigitalAgentOrchestrator",
    "QuantumDigitalAgentType",
    "DigitalOperationType",
    "DigitalOperation",
    "QuantumDigitalAgent",
    
    # Core functions
    "get_orchestrator",
    "get_ltc_logger",
    "get_settings",
    "submit_task",
    "log_operation",
    "solve_qubo",
    "score_leads",
    "get_quantum_high_council",
    "initialize_quantum_high_council",
    "get_quantum_digital_agent_orchestrator",
    "initialize_quantum_digital_agent_orchestrator",
    
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
