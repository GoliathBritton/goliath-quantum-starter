"""
NQBA Stack - Neuromorphic Quantum Business Architecture
The foundational core for quantum-enhanced business operations

Core Components:
- Orchestrator: Central brain for task routing and coordination
- LTC Logger: Living Technical Codex for comprehensive traceability
- Dynex Adapter: Quantum optimization interface
- Settings: Centralized configuration management

Advanced Systems:
- QSAI Engine: Quantum Synthetic AI Decision Engine for autonomous decision making
- QEA-DO: Quantum-Enhanced Algorithm Development Orchestrator for automated algorithm generation

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

# Advanced Systems
from .qsai_engine import (
    QSAIEngine,
    ContextVector,
    ActionProposal,
    ActionDecision,
    AuditEntry,
    DecisionState,
    AgentType
)

from .qea_do import (
    QEA_DO,
    AlgorithmBlueprint,
    AlgorithmArtifact,
    QUBOSolution,
    VerificationReport,
    AlgorithmType,
    GenerationPhase,
    VerificationStatus
)

from .qsai_agents import (
    OfferAgent,
    TimingAgent,
    ChannelAgent,
    RiskAgent,
    AgentFactory
)

# Quantum-Enhanced Algorithms
from .algorithms.quantum_enhanced_algorithms import (
    QuantumAlgorithmFactory,
    AlgorithmType as QAlgorithmType,
    QuantumPortfolioOptimizer,
    QuantumEnergyManager,
    QuantumRiskAssessor,
    QuantumPersonalizationEngine,
    AlgorithmResult
)

# Automation Orchestrator
from .automation.quantum_automation_orchestrator import (
    QuantumAutomationOrchestrator,
    AutomationLevel,
    AutomationDomain,
    AutomationTask,
    AutomationMetrics
)

# Advanced Algorithm Templates
from .algorithms.advanced_algorithm_templates import (
    AdvancedAlgorithmFactory,
    get_algorithm_templates,
    create_algorithm_instance,
    AlgorithmCategory,
    ComplexityLevel,
    AlgorithmTemplate,
    BaseAlgorithm,
    QuantumPortfolioOptimizer as AdvancedQuantumPortfolioOptimizer,
    QuantumSupplyChainOptimizer,
    QuantumFraudDetector
)

# Advanced Automation Workflows
from .automation.advanced_automation_workflows import (
    WorkflowType,
    AutomationStage,
    WorkflowStep,
    WorkflowResult,
    AdvancedAutomationWorkflow,
    DecisionAutomationWorkflow,
    AlgorithmOptimizationWorkflow,
    DeploymentAutomationWorkflow,
    WorkflowOrchestrator,
    create_decision_automation_workflow,
    create_algorithm_optimization_workflow,
    create_deployment_automation_workflow,
    create_workflow_orchestrator
)

# Configuration Management
from .core.config_manager import (
    ConfigurationManager,
    ServiceConfig,
    FallbackConfig,
    get_config_manager,
    initialize_configuration
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
    
    # Advanced Systems
    "QSAIEngine",
    "QEA_DO",
    "OfferAgent",
    "TimingAgent",
    "ChannelAgent",
    "RiskAgent",
    "AgentFactory",
    
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
    "OptimizationResult",
    "ContextVector",
    "ActionProposal",
    "ActionDecision",
    "AuditEntry",
    "DecisionState",
    "AgentType",
    "AlgorithmBlueprint",
    "AlgorithmArtifact",
    "QUBOSolution",
    "VerificationReport",
    "AlgorithmType",
    "GenerationPhase",
    "VerificationStatus",
    
    # Quantum-Enhanced Algorithms
    "QuantumAlgorithmFactory",
    "QAlgorithmType",
    "QuantumPortfolioOptimizer",
    "QuantumEnergyManager",
    "QuantumRiskAssessor",
    "QuantumPersonalizationEngine",
    "AlgorithmResult",
    
    # Automation Orchestrator
    "QuantumAutomationOrchestrator",
    "AutomationLevel",
    "AutomationDomain",
    "AutomationTask",
    "AutomationMetrics",
    
    # Advanced Algorithm Templates
    "AdvancedAlgorithmFactory",
    "get_algorithm_templates",
    "create_algorithm_instance",
    "AlgorithmCategory",
    "ComplexityLevel",
    "AlgorithmTemplate",
    "BaseAlgorithm",
    "AdvancedQuantumPortfolioOptimizer",
    "QuantumSupplyChainOptimizer",
    "QuantumFraudDetector",
    
    # Advanced Automation Workflows
    "WorkflowType",
    "AutomationStage",
    "WorkflowStep",
    "WorkflowResult",
    "AdvancedAutomationWorkflow",
    "DecisionAutomationWorkflow",
    "AlgorithmOptimizationWorkflow",
    "DeploymentAutomationWorkflow",
    "WorkflowOrchestrator",
    "create_decision_automation_workflow",
    "create_algorithm_optimization_workflow",
    "create_deployment_automation_workflow",
    "create_workflow_orchestrator",
    
    # Configuration Management
    "ConfigurationManager",
    "ServiceConfig",
    "FallbackConfig",
    "get_config_manager",
    "initialize_configuration"
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
