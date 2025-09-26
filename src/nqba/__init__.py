"""Neuromorphic Quantum Business Architecture (NQBA) Framework

NQBA is a comprehensive meta-architecture that defines how quantum-inspired AI modules
interact with business processes. It serves as the unifying intelligence and operations
layer that houses reusable procedures, compliance hooks, scaling protocols, and
foundational computational intelligence modules.

Core Components:
- Intelligence Modules: qdLLM, QNLP, QTransformers
- Procedures Layer: Business workflows and algorithms
- Integration Layer: System connectors and APIs
- Governance Layer: Policies and compliance
"""

# Core Intelligence Modules (New NQBA Foundation)
try:
    from .core.intelligence import qdllm, qnlp, qtransformers
    from .core.framework import NQBAFramework
    from .core.ingestion import DataIngestor
    from .core.analysis import AdvancedAnalyzer
    from .core.presentation import SolutionPresenter
    from .core.integration import SolutionIntegrator
    from .core.outcomes import OutcomeMonitor
except ImportError:
    # Fallback for development/transition period
    qdllm = None
    qnlp = None
    qtransformers = None
    NQBAFramework = None

# NQBA Framework Layers
try:
    from .api import server as nqba_server
    from .procedures import workflows
    from .integration import connectors
    from .governance import policies
except ImportError:
    # Fallback for development/transition period
    nqba_server = None
    workflows = None
    connectors = None
    policies = None

# Legacy NQBA Components (Existing)
from .api_server import app
from .decision_logic import decide, DecisionLogicEngine
from .quantum_adapter import optimize_qubo, QuantumAdapter
from .ltc_logger import ltc_record, LTCLogger
from .agent_interface import AgentInterface
from .dynex_adapter import DynexAdapter, score_leads, OptimizationResult
from .q_cortex_parser import QCortexParser, create_q_cortex_parser
from .settings import (
    NQBASettings,
    get_settings,
    is_production,
    is_development,
    is_testing,
)

# Business pods
from .business_pods import LeadScoringPod, QuantumOptimizerPod, SalesScriptPod

# Neuromorphic/AI automation catalog
from .neuromorphic_automations import AUTOMATIONS, register_automation

# Goliath of All Trade business divisions and workflows
from .goliath_divisions import DIVISIONS

__version__ = "1.0.0"
__author__ = "NQBA Development Team"
__description__ = "Neuromorphic Quantum Business Architecture Framework"

# Main framework exports
__all__ = [
    # New NQBA Intelligence Framework
    "NQBAFramework",
    "qdllm",
    "qnlp", 
    "qtransformers",
    "nqba_server",
    "workflows",
    "connectors",
    "policies",
    # Legacy NQBA Components
    "app",
    "decide",
    "DecisionLogicEngine",
    "optimize_qubo",
    "QuantumAdapter",
    "ltc_record",
    "LTCLogger",
    "AgentInterface",
    "DynexAdapter",
    "score_leads",
    "OptimizationResult",
    "QCortexParser",
    "create_q_cortex_parser",
    "NQBASettings",
    "get_settings",
    "is_production",
    "is_development",
    "is_testing",
    "LeadScoringPod",
    "QuantumOptimizerPod",
    "SalesScriptPod",
    "AUTOMATIONS",
    "register_automation",
    "DIVISIONS",
    "DataIngestor",
    "AdvancedAnalyzer",
    "SolutionPresenter",
    "SolutionIntegrator",
    "OutcomeMonitor"
]

# Framework initialization
def create_framework(**config):
    """Create and configure an NQBA framework instance"""
    if NQBAFramework is None:
        raise ImportError("NQBA Framework not available. Please ensure all components are properly installed.")
    framework = NQBAFramework(**config)
    framework.ingestor = DataIngestor(framework)
    framework.analyzer = AdvancedAnalyzer()
    framework.presenter = SolutionPresenter()
    framework.integrator = SolutionIntegrator(
        framework.ingestor,
        framework.analyzer,
        framework.presenter
    )
    framework.monitor = OutcomeMonitor(framework)
    return framework

# Quick access functions
def process_business_request(request, framework=None):
    """Process a business request through the NQBA framework"""
    if framework is None:
        framework = create_framework()
    return framework.process_business_request(request)

def get_intelligence_modules():
    """Get references to all intelligence modules"""
    return {
        'qdllm': qdllm,
        'qnlp': qnlp,
        'qtransformers': qtransformers
    }
