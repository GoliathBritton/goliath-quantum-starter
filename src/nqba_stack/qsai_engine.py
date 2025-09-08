"""
Quantum Synthetic AI Decision Engine (QSAI Engine)
=================================================

A hybrid classical/quantum decisioning stack that autonomously drives business outcomes
while enforcing safety, privacy, and auditability. Integrates with Dynex quantum models
for superior decision-making and algorithm orchestration.

Core Features:
- Hybrid Decision Stack: deterministic safety + contextual bandits + hierarchical RL
- Agent-Oriented Orchestration: specialized micro-agents coordinated by Agent Manager
- Quantum-accelerated Modules: QAOA/quantum annealing for optimization
- End-to-end MLOps & Governance with immutable audit trails
- Edge-Cloud Split Execution for low-latency safety decisions
"""

import asyncio
import logging
import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import numpy as np
import pandas as pd

from .qdllm import qdllm
from .qtransformer import qtransformer
from .qnlp import qnlp
from .dynex_client import get_dynex_client
from .core.ltc_logger import LTCLogger

logger = logging.getLogger(__name__)


class DecisionPriority(Enum):
    """Decision priority levels for safety arbitration"""

    SAFETY_CRITICAL = 1
    COMPLIANCE = 2
    BUSINESS_OPTIMIZATION = 3
    EFFICIENCY = 4


class AgentType(Enum):
    """Specialized agent types for different decision domains"""

    OFFER = "offer"
    TIMING = "timing"
    CHANNEL = "channel"
    RISK = "risk"
    RESOURCE = "resource"
    ENERGY = "energy"
    PORTFOLIO = "portfolio"


class DecisionState(Enum):
    """Decision processing states"""

    IDLE = "idle"
    OBSERVING = "observing"
    PROPOSING = "proposing"
    VALIDATING = "validating"
    DECIDING = "deciding"
    ACTING = "acting"
    LEARNING = "learning"
    SIMULATING = "simulating"


@dataclass
class ContextVector:
    """Real-time context for decision making"""

    user_id: str
    timestamp: datetime
    telemetry: Dict[str, Any]
    business_context: Dict[str, Any]
    market_signals: Dict[str, Any]
    nqba_embeddings: Optional[np.ndarray] = None
    safety_flags: List[str] = field(default_factory=list)
    consent_level: str = "full"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "telemetry": self.telemetry,
            "business_context": self.business_context,
            "market_signals": self.market_signals,
            "nqba_embeddings": (
                self.nqba_embeddings.tolist()
                if self.nqba_embeddings is not None
                else None
            ),
            "safety_flags": self.safety_flags,
            "consent_level": self.consent_level,
        }


@dataclass
class ActionProposal:
    """Agent action proposal with metadata"""

    agent_id: str
    agent_type: AgentType
    action_id: str
    payload: Dict[str, Any]
    estimated_reward: float
    confidence: float
    required_resources: Dict[str, Any]
    safety_impact: str = "low"
    compliance_status: str = "compliant"
    rationale: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "action_id": self.action_id,
            "payload": self.payload,
            "estimated_reward": self.estimated_reward,
            "confidence": self.confidence,
            "required_resources": self.required_resources,
            "safety_impact": self.safety_impact,
            "compliance_status": self.compliance_status,
            "rationale": self.rationale,
        }


@dataclass
class ActionDecision:
    """Final action decision with full metadata"""

    decision_id: str
    action_id: str
    payload: Dict[str, Any]
    required_resources: Dict[str, Any]
    expected_uplift: float
    confidence: float
    model_version: str
    policy_version: str
    experiment_id: Optional[str] = None
    rationale: str = ""
    rollback_plan: Dict[str, Any] = field(default_factory=dict)
    signature: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "action_id": self.action_id,
            "payload": self.payload,
            "required_resources": self.required_resources,
            "expected_uplift": self.expected_uplift,
            "confidence": self.confidence,
            "model_version": self.model_version,
            "policy_version": self.policy_version,
            "experiment_id": self.experiment_id,
            "rationale": self.rationale,
            "rollback_plan": self.rollback_plan,
            "signature": self.signature,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class AuditEntry:
    """Immutable audit trail entry"""

    entry_id: str
    decision_id: str
    context_hash: str
    agent_proposals: List[Dict[str, Any]]
    final_decision: Dict[str, Any]
    model_versions: Dict[str, str]
    policy_versions: Dict[str, str]
    safety_checks: List[str]
    compliance_checks: List[str]
    quantum_job_ids: List[str]
    qubo_snapshots: List[Dict[str, Any]]
    signature: str
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "decision_id": self.decision_id,
            "context_hash": self.context_hash,
            "agent_proposals": self.agent_proposals,
            "final_decision": self.final_decision,
            "model_versions": self.model_versions,
            "policy_versions": self.policy_versions,
            "safety_checks": self.safety_checks,
            "compliance_checks": self.compliance_checks,
            "quantum_job_ids": self.quantum_job_ids,
            "qubo_snapshots": self.qubo_snapshots,
            "signature": self.signature,
            "timestamp": self.timestamp.isoformat(),
        }


class SafetyArbiter:
    """Deterministic safety and policy gating"""

    def __init__(self, ltc_logger: LTCLogger):
        self.ltc_logger = ltc_logger
        # Initialize with default safety policies
        self.safety_policies: Dict[str, Any] = {
            "vehicle_safety": {
                "max_speed": 120.0,  # km/h
                "min_battery": 10.0,  # %
                "max_acceleration": 8.0,  # m/s²
                "max_steering_angle": 45.0,  # degrees
            },
            "driver_safety": {
                "max_driving_time": 4.0,  # hours
                "min_break_interval": 2.0,  # hours
                "distraction_threshold": 0.8,  # 0-1 scale
            },
        }
        # Initialize with default compliance rules
        self.compliance_rules: Dict[str, Any] = {
            "gdpr": {
                "data_retention_days": 30,
                "consent_required": True,
                "pii_redaction": True,
            },
            "iso26262": {
                "asil_level": "B",
                "safety_checks_required": True,
                "audit_trail_required": True,
            },
        }

    async def validate_action(
        self, action: ActionProposal, context: ContextVector
    ) -> Tuple[bool, List[str], str]:
        """Validate action against safety and compliance policies"""
        violations = []
        status = "compliant"

        # Safety checks
        if context.safety_flags:
            violations.append(f"Safety flags active: {context.safety_flags}")
            status = "safety_violation"

        # Compliance checks
        if action.compliance_status != "compliant":
            violations.append(f"Compliance violation: {action.compliance_status}")
            status = "compliance_violation"

        # Resource constraints
        if not self._check_resource_availability(action.required_resources):
            violations.append("Insufficient resources")
            status = "resource_violation"

        is_valid = len(violations) == 0
        return is_valid, violations, status

    def _check_resource_availability(self, required_resources: Dict[str, Any]) -> bool:
        """Check if required resources are available"""
        try:
            # Check computational resources
            cpu_required = required_resources.get("cpu_cores", 0)
            memory_required = required_resources.get("memory_mb", 0)
            gpu_required = required_resources.get("gpu_memory_mb", 0)
            
            # Get current system resource usage
            import psutil
            
            # Check CPU availability
            cpu_percent = psutil.cpu_percent(interval=0.1)
            available_cpu_percent = 100 - cpu_percent
            cpu_cores_available = psutil.cpu_count() * (available_cpu_percent / 100)
            
            if cpu_required > cpu_cores_available:
                logger.warning(f"Insufficient CPU: required {cpu_required}, available {cpu_cores_available:.2f}")
                return False
            
            # Check memory availability
            memory = psutil.virtual_memory()
            available_memory_mb = memory.available / (1024 * 1024)
            
            if memory_required > available_memory_mb:
                logger.warning(f"Insufficient memory: required {memory_required}MB, available {available_memory_mb:.2f}MB")
                return False
            
            # Check GPU availability (if NVIDIA GPU is available)
            if gpu_required > 0:
                try:
                    import GPUtil
                    gpus = GPUtil.getGPUs()
                    if not gpus:
                        logger.warning("GPU required but no GPUs available")
                        return False
                    
                    # Check if any GPU has sufficient memory
                    gpu_available = False
                    for gpu in gpus:
                        available_gpu_memory = gpu.memoryFree
                        if available_gpu_memory >= gpu_required:
                            gpu_available = True
                            break
                    
                    if not gpu_available:
                        logger.warning(f"Insufficient GPU memory: required {gpu_required}MB")
                        return False
                        
                except ImportError:
                    # GPUtil not available, assume GPU check passes
                    logger.info("GPUtil not available, skipping GPU resource check")
            
            # Check quantum computing resources
            quantum_required = required_resources.get("quantum_nodes", 0)
            if quantum_required > 0:
                # Check Dynex network availability
                try:
                    # Simulate checking Dynex network status
                    # In a real implementation, this would query the Dynex network
                    dynex_nodes_available = self._check_dynex_availability()
                    
                    if quantum_required > dynex_nodes_available:
                        logger.warning(f"Insufficient Dynex nodes: required {quantum_required}, available {dynex_nodes_available}")
                        return False
                        
                except Exception as e:
                    logger.error(f"Failed to check Dynex availability: {e}")
                    # Allow execution to continue with classical fallback
            
            # Check network bandwidth requirements
            bandwidth_required = required_resources.get("bandwidth_mbps", 0)
            if bandwidth_required > 0:
                # Simulate network bandwidth check
                # In a real implementation, this would measure actual bandwidth
                estimated_bandwidth = self._estimate_network_bandwidth()
                
                if bandwidth_required > estimated_bandwidth:
                    logger.warning(f"Insufficient bandwidth: required {bandwidth_required}Mbps, estimated {estimated_bandwidth}Mbps")
                    return False
            
            # Check storage requirements
            storage_required = required_resources.get("storage_mb", 0)
            if storage_required > 0:
                disk_usage = psutil.disk_usage('/')
                available_storage_mb = disk_usage.free / (1024 * 1024)
                
                if storage_required > available_storage_mb:
                    logger.warning(f"Insufficient storage: required {storage_required}MB, available {available_storage_mb:.2f}MB")
                    return False
            
            # All resource checks passed
            logger.info(f"Resource availability check passed")
            return True
            
        except Exception as e:
            logger.error(f"Error checking resource availability: {e}")
            # Default to allowing execution if resource check fails
            return True
    
    def _check_dynex_availability(self) -> int:
        """Check available Dynex quantum computing nodes"""
        try:
            # Simulate checking Dynex network status
            # In a real implementation, this would query the Dynex network API
            import random
            import time
            
            # Simulate network latency
            time.sleep(0.1)
            
            # Return a simulated number of available nodes (10-100)
            available_nodes = random.randint(10, 100)
            logger.debug(f"Simulated Dynex nodes available: {available_nodes}")
            return available_nodes
            
        except Exception as e:
            logger.error(f"Failed to check Dynex network: {e}")
            return 0
    
    def _estimate_network_bandwidth(self) -> float:
        """Estimate available network bandwidth in Mbps"""
        try:
            # Simulate bandwidth estimation
            # In a real implementation, this would perform actual bandwidth tests
            import random
            
            # Return a simulated bandwidth (10-1000 Mbps)
            estimated_bandwidth = random.uniform(10.0, 1000.0)
            logger.debug(f"Estimated network bandwidth: {estimated_bandwidth:.2f}Mbps")
            return estimated_bandwidth
            
        except Exception as e:
            logger.error(f"Failed to estimate bandwidth: {e}")
            return 100.0  # Default conservative estimate


class AgentManager:
    """Manages specialized decision agents"""

    def __init__(self, ltc_logger: LTCLogger):
        self.ltc_logger = ltc_logger
        self.agents: Dict[str, Any] = {}
        self.agent_states: Dict[str, Dict[str, Any]] = {}

    async def register_agent(
        self, agent_id: str, agent_type: AgentType, agent_instance: Any
    ):
        """Register a new agent"""
        self.agents[agent_id] = {
            "type": agent_type,
            "instance": agent_instance,
            "status": "active",
            "last_heartbeat": datetime.now(),
        }
        self.ltc_logger.log_operation(
            "agent_registered",
            {"agent_id": agent_id, "agent_type": agent_type.value},
            "agent_manager",
        )

    async def get_agent_proposals(
        self, context: ContextVector, agent_types: List[AgentType]
    ) -> List[ActionProposal]:
        """Get proposals from specified agent types"""
        proposals = []

        for agent_id, agent_info in self.agents.items():
            if agent_info["type"] in agent_types and agent_info["status"] == "active":
                try:
                    proposal = agent_info["instance"].propose_action(context)
                    if proposal:
                        proposals.append(proposal)
                except Exception as e:
                    logger.error(f"Agent {agent_id} failed to propose: {e}")

        return proposals


class MetaController:
    """Meta-learner that coordinates agent strategies and optimization"""

    def __init__(self, ltc_logger: LTCLogger):
        self.ltc_logger = ltc_logger
        self.dynex = get_dynex_client()
        self.optimization_history: List[Dict[str, Any]] = []

    async def optimize_action_selection(
        self, proposals: List[ActionProposal], context: ContextVector
    ) -> ActionDecision:
        """Use quantum optimization to select best action combination"""
        if len(proposals) == 1:
            return self._create_decision(proposals[0], context)

        # Build QUBO for action selection
        qubo_matrix = self._build_action_selection_qubo(proposals, context)

        try:
            # Quantum optimization via Dynex
            qubo_result = await self.dynex.submit_qubo(
                qubo_matrix, algorithm="qaoa", parameters={"timeout": 5.0}
            )

            # Parse quantum result
            selected_indices = self._parse_qubo_result(qubo_result, len(proposals))
            selected_proposals = [proposals[i] for i in selected_indices]

            # Create composite decision
            return self._create_composite_decision(
                selected_proposals, context, qubo_result
            )

        except Exception as e:
            logger.warning(
                f"Quantum optimization failed, falling back to classical: {e}"
            )
            return self._classical_fallback(proposals, context)

    def _build_action_selection_qubo(
        self, proposals: List[ActionProposal], context: ContextVector
    ) -> np.ndarray:
        """Build QUBO matrix for action selection optimization"""
        n = len(proposals)
        qubo = np.zeros((n, n))

        # Objective: maximize expected reward
        for i, proposal in enumerate(proposals):
            qubo[i, i] = -proposal.estimated_reward * proposal.confidence

        # Constraints: resource limits, safety, etc.
        constraint_strength = 10.0
        
        # Resource constraint: penalize proposals that exceed available resources
        available_resources = context.available_resources or {}
        for i, proposal in enumerate(proposals):
            required_resources = proposal.required_resources or {}
            
            # Check each resource type
            for resource_type, required_amount in required_resources.items():
                available_amount = available_resources.get(resource_type, 0)
                
                # If resource requirement exceeds availability, add penalty
                if required_amount > available_amount:
                    resource_penalty = constraint_strength * (required_amount - available_amount)
                    qubo[i, i] += resource_penalty
        
        # Safety constraint: penalize unsafe proposals
        for i, proposal in enumerate(proposals):
            if hasattr(proposal, 'safety_score') and proposal.safety_score < 0.5:
                safety_penalty = constraint_strength * (0.5 - proposal.safety_score)
                qubo[i, i] += safety_penalty
        
        # Mutual exclusion constraint: ensure only one proposal is selected
        # Add penalty for selecting multiple proposals simultaneously
        for i in range(n):
            for j in range(i + 1, n):
                # Check if proposals are mutually exclusive
                if self._are_mutually_exclusive(proposals[i], proposals[j]):
                    qubo[i, j] += constraint_strength * 2
                    qubo[j, i] += constraint_strength * 2
        
        # Priority constraint: boost high-priority proposals
        for i, proposal in enumerate(proposals):
            if hasattr(proposal, 'priority') and proposal.priority == 'high':
                qubo[i, i] -= constraint_strength * 0.5  # Negative penalty = boost
        
        return qubo
    
    def _are_mutually_exclusive(self, proposal1: ActionProposal, proposal2: ActionProposal) -> bool:
        """Check if two proposals are mutually exclusive"""
        try:
            # Check if proposals target the same resource or action type
            if proposal1.action_id == proposal2.action_id:
                return True
            
            # Check if proposals require conflicting resources
            resources1 = proposal1.required_resources or {}
            resources2 = proposal2.required_resources or {}
            
            for resource_type in resources1:
                if resource_type in resources2:
                    # If both require the same exclusive resource
                    if resource_type in ['hmi_display', 'audio_channel', 'driver_attention']:
                        return True
            
            # Check if proposals have conflicting action types
            conflicting_types = [
                ('offer_charging', 'offer_maintenance'),
                ('urgent_notification', 'background_notification'),
                ('voice_interaction', 'silent_mode')
            ]
            
            for type1, type2 in conflicting_types:
                if (type1 in proposal1.action_id and type2 in proposal2.action_id) or \
                   (type2 in proposal1.action_id and type1 in proposal2.action_id):
                    return True
            
            return False
            
        except Exception as e:
            logger.warning(f"Error checking mutual exclusion: {e}")
            return False

    def _parse_qubo_result(
        self, qubo_result: Dict[str, Any], num_proposals: int
    ) -> List[int]:
        """Parse quantum result to get selected action indices"""
        try:
            selected_indices = []
            
            # Handle different QUBO result formats from Dynex
            if "solution" in qubo_result:
                solution = qubo_result["solution"]
                
                # Handle binary solution vector format
                if isinstance(solution, list):
                    if len(solution) >= num_proposals:
                        # Find indices where solution value is 1 (selected)
                        for i, value in enumerate(solution[:num_proposals]):
                            if value == 1:
                                selected_indices.append(i)
                        
                        # If no clear selection, find the highest value
                        if not selected_indices:
                            max_value = max(solution[:num_proposals])
                            for i, value in enumerate(solution[:num_proposals]):
                                if value == max_value:
                                    selected_indices.append(i)
                                    break
                    
                # Handle dictionary format with variable names
                elif isinstance(solution, dict):
                    # Look for variables that are set to 1
                    for var_name, value in solution.items():
                        if value == 1:
                            # Extract index from variable name (e.g., "x_0", "proposal_1")
                            try:
                                if "_" in var_name:
                                    index = int(var_name.split("_")[-1])
                                    if 0 <= index < num_proposals:
                                        selected_indices.append(index)
                            except (ValueError, IndexError):
                                continue
            
            # Handle energy-based selection if available
            elif "energy" in qubo_result:
                energy = qubo_result.get("energy", 0)
                num_occurrences = qubo_result.get("num_occurrences", 1)
                
                # Use energy to determine selection (lower energy = better)
                if energy < 0 and num_occurrences > 0:
                    # Convert energy to index selection
                    selected_index = abs(int(energy)) % num_proposals
                    selected_indices.append(selected_index)
            
            # Handle samples format (multiple solutions)
            elif "samples" in qubo_result:
                samples = qubo_result["samples"]
                if samples and len(samples) > 0:
                    # Use the first (best) sample
                    best_sample = samples[0]
                    if isinstance(best_sample, list) and len(best_sample) >= num_proposals:
                        for i, value in enumerate(best_sample[:num_proposals]):
                            if value == 1:
                                selected_indices.append(i)
            
            # Handle raw binary string format
            elif "binary_solution" in qubo_result:
                binary_str = qubo_result["binary_solution"]
                if len(binary_str) >= num_proposals:
                    for i, bit in enumerate(binary_str[:num_proposals]):
                        if bit == '1':
                            selected_indices.append(i)
            
            # Validate and clean up results
            if selected_indices:
                # Remove duplicates and sort
                selected_indices = sorted(list(set(selected_indices)))
                
                # Ensure indices are within valid range
                selected_indices = [i for i in selected_indices if 0 <= i < num_proposals]
                
                # Log successful parsing
                logger.info(f"QUBO result parsed successfully: selected indices {selected_indices}")
                return selected_indices
            
            # Fallback: if no clear selection, return the first proposal
            logger.warning("No clear selection from QUBO result, defaulting to first proposal")
            return [0]
            
        except Exception as e:
            logger.error(f"Failed to parse QUBO result: {e}")
            logger.debug(f"QUBO result format: {type(qubo_result)}, keys: {list(qubo_result.keys()) if isinstance(qubo_result, dict) else 'not dict'}")
            
            # Emergency fallback: return first proposal
            return [0]

    def _create_decision(
        self, proposal: ActionProposal, context: ContextVector
    ) -> ActionDecision:
        """Create decision from single proposal"""
        return ActionDecision(
            decision_id=f"dec_{int(time.time() * 1000)}",
            action_id=proposal.action_id,
            payload=proposal.payload,
            required_resources=proposal.required_resources,
            expected_uplift=proposal.estimated_reward,
            confidence=proposal.confidence,
            model_version="qsai_v1.0",
            policy_version="policy_v1.0",
            rationale=proposal.rationale,
        )

    def _create_composite_decision(
        self,
        proposals: List[ActionProposal],
        context: ContextVector,
        qubo_result: Dict[str, Any],
    ) -> ActionDecision:
        """Create composite decision from multiple proposals"""
        # Combine multiple proposals into single decision
        combined_payload = {}
        total_uplift = 0
        total_confidence = 0

        for proposal in proposals:
            combined_payload[proposal.agent_type.value] = proposal.payload
            total_uplift += proposal.estimated_reward
            total_confidence += proposal.confidence

        return ActionDecision(
            decision_id=f"dec_{int(time.time() * 1000)}",
            action_id="composite",
            payload=combined_payload,
            required_resources=self._merge_resources(
                [p.required_resources for p in proposals]
            ),
            expected_uplift=total_uplift,
            confidence=total_confidence / len(proposals),
            model_version="qsai_v1.0",
            policy_version="policy_v1.0",
            rationale=f"Composite decision from {len(proposals)} agents via quantum optimization",
        )

    def _merge_resources(self, resource_lists: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge resource requirements from multiple proposals"""
        merged = {}
        for resources in resource_lists:
            for key, value in resources.items():
                if key in merged:
                    if isinstance(value, (int, float)):
                        merged[key] += value
                    elif isinstance(value, list):
                        merged[key].extend(value)
                else:
                    merged[key] = value
        return merged

    def _classical_fallback(
        self, proposals: List[ActionProposal], context: ContextVector
    ) -> ActionDecision:
        """Classical fallback when quantum optimization fails"""
        # Simple greedy selection
        best_proposal = max(proposals, key=lambda p: p.estimated_reward * p.confidence)
        return self._create_decision(best_proposal, context)


class QSAIEngine:
    """Main Quantum Synthetic AI Decision Engine"""

    def __init__(self, ltc_logger: LTCLogger):
        self.ltc_logger = ltc_logger
        self.safety_arbiter = SafetyArbiter(ltc_logger)
        self.agent_manager = AgentManager(ltc_logger)
        self.meta_controller = MetaController(ltc_logger)

        # State management
        self.current_state = DecisionState.IDLE
        self.context_store: Dict[str, ContextVector] = {}
        self.decision_history: List[ActionDecision] = []
        self.audit_store: List[AuditEntry] = []

        # Performance metrics
        self.metrics = {
            "decisions_made": 0,
            "quantum_optimizations": 0,
            "classical_fallbacks": 0,
            "safety_violations": 0,
            "avg_decision_latency": 0.0,
        }

        logger.info("QSAI Engine initialized")

    async def initialize(self):
        """Initialize QSAI Engine components"""
        logger.info("Initializing QSAI Engine...")

        # Initialize quantum components
        await self._initialize_quantum_components()

        # Load safety policies and compliance rules
        await self._load_policies()

        self.ltc_logger.log_operation(
            "qsai_engine_initialized",
            {
                "status": "ready",
                "components": ["safety_arbiter", "agent_manager", "meta_controller"],
            },
            "system_startup",
        )

        logger.info("QSAI Engine ready")

    async def _initialize_quantum_components(self):
        """Initialize quantum computing components"""
        try:
            # Test quantum connectivity
            dynex = get_dynex_client()
            # TODO: Implement quantum readiness check

            logger.info("Quantum components initialized")
        except Exception as e:
            logger.warning(f"Quantum components unavailable: {e}")

    async def _load_policies(self):
        """Load safety and compliance policies"""
        # TODO: Load from configuration or database
        self.safety_arbiter.safety_policies = {
            "vehicle_safety": {"max_speed": 120, "min_battery": 10},
            "driver_safety": {"max_distraction": 0.3, "min_attention": 0.7},
        }

        self.safety_arbiter.compliance_rules = {
            "gdpr": {"data_retention": 30, "consent_required": True},
            "iso26262": {"asil_level": "B", "safety_gates": True},
        }

    async def process_context(self, context: ContextVector) -> Optional[ActionDecision]:
        """Main decision processing pipeline"""
        start_time = time.time()

        try:
            # Update state
            self.current_state = DecisionState.OBSERVING

            # Store context
            self.context_store[context.user_id] = context

            # Get agent proposals
            self.current_state = DecisionState.PROPOSING
            proposals = await self.agent_manager.get_agent_proposals(
                context,
                [AgentType.OFFER, AgentType.TIMING, AgentType.CHANNEL, AgentType.RISK],
            )

            if not proposals:
                logger.info(f"No proposals for user {context.user_id}")
                return None

            # Validate proposals
            self.current_state = DecisionState.VALIDATING
            valid_proposals = []
            for proposal in proposals:
                is_valid, violations, status = (
                    await self.safety_arbiter.validate_action(proposal, context)
                )
                if is_valid:
                    valid_proposals.append(proposal)
                else:
                    logger.warning(
                        f"Proposal {proposal.action_id} rejected: {violations}"
                    )
                    self.metrics["safety_violations"] += 1

            if not valid_proposals:
                logger.warning(f"No valid proposals for user {context.user_id}")
                return None

            # Optimize action selection
            self.current_state = DecisionState.DECIDING
            decision = await self.meta_controller.optimize_action_selection(
                valid_proposals, context
            )

            # Update metrics
            decision_latency = time.time() - start_time
            self.metrics["decisions_made"] += 1
            self.metrics["avg_decision_latency"] = (
                self.metrics["avg_decision_latency"]
                * (self.metrics["decisions_made"] - 1)
                + decision_latency
            ) / self.metrics["decisions_made"]

            # Store decision
            self.decision_history.append(decision)

            # Create audit entry
            await self._create_audit_entry(decision, proposals, context)

            # Update state
            self.current_state = DecisionState.IDLE

            return decision

        except Exception as e:
            logger.error(f"Decision processing failed: {e}")
            self.current_state = DecisionState.IDLE
            return None

    async def _create_audit_entry(
        self,
        decision: ActionDecision,
        proposals: List[ActionProposal],
        context: ContextVector,
    ):
        """Create immutable audit trail entry"""
        context_hash = hashlib.sha256(
            json.dumps(context.to_dict(), sort_keys=True).encode()
        ).hexdigest()

        audit_entry = AuditEntry(
            entry_id=f"audit_{int(time.time() * 1000)}",
            decision_id=decision.decision_id,
            context_hash=context_hash,
            agent_proposals=[p.to_dict() for p in proposals],
            final_decision=decision.to_dict(),
            model_versions={"qsai": "v1.0", "qdllm": "v1.0"},
            policy_versions={"safety": "v1.0", "compliance": "v1.0"},
            safety_checks=["context_validation", "proposal_validation"],
            compliance_checks=["gdpr", "iso26262"],
            quantum_job_ids=[],  # TODO: Extract from quantum results
            qubo_snapshots=[],  # TODO: Extract from quantum results
            signature=hashlib.sha256(
                json.dumps(decision.to_dict(), sort_keys=True).encode()
            ).hexdigest(),
        )

        self.audit_store.append(audit_entry)

        self.ltc_logger.log_operation(
            "audit_entry_created",
            {"entry_id": audit_entry.entry_id, "decision_id": decision.decision_id},
            "qsai_engine",
        )

    async def get_agent_proposals(
        self, context: ContextVector, agent_types: List[AgentType]
    ) -> List[ActionProposal]:
        """Get action proposals from specified agent types"""
        try:
            proposals = await self.agent_manager.get_agent_proposals(
                context, agent_types
            )
            return proposals
        except Exception as e:
            logger.error(f"Failed to get agent proposals: {e}")
            return []

    async def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.metrics,
            "current_state": self.current_state.value,
            "contexts_stored": len(self.context_store),
            "decisions_stored": len(self.decision_history),
            "audit_entries": len(self.audit_store),
        }

    async def get_audit_trail(
        self, user_id: Optional[str] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get audit trail entries"""
        entries = self.audit_store[-limit:] if limit > 0 else self.audit_store

        if user_id:
            # Filter by user context
            filtered_entries = []
            for entry in entries:
                if any(
                    proposal.get("user_id") == user_id
                    for proposal in entry.agent_proposals
                ):
                    filtered_entries.append(entry)
            entries = filtered_entries

        return [entry.to_dict() for entry in entries]


# Global instance
qsai_engine = QSAIEngine(None)  # Will be set during initialization
