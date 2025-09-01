"""
Cross-Agent Orchestrator - The Interoperability Layer for FLYFOX AI Agents

This package provides seamless communication and workflow orchestration between
all types of FLYFOX AI agents, creating network effects and exponential value
for clients through agent collaboration.
"""

from .agent_orchestrator import AgentOrchestrator
from .workflow_engine import WorkflowEngine
from .agent_registry import AgentRegistry
from .communication_bus import CommunicationBus
from .workflow_templates import WorkflowTemplate, WorkflowStep
from .agent_connectors import AgentConnector, ConnectorType

__all__ = [
    "AgentOrchestrator",
    "WorkflowEngine",
    "AgentRegistry",
    "CommunicationBus",
    "WorkflowTemplate",
    "WorkflowStep",
    "AgentConnector",
    "ConnectorType",
]

__version__ = "1.0.0"
__author__ = "FLYFOX AI Team"
__description__ = "Cross-Agent Orchestrator - Agent Interoperability & Workflow Engine"
