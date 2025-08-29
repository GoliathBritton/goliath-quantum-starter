"""
NQBA Dynex Adapter
Standardized interface for DynexSolve quantum optimization
Integrates with LTC logging and Q-Cortex compliance
"""
import json
import logging
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import dimod
import dynex
from dataclasses import dataclass, asdict
import os
from .settings import get_settings

logger = logging.getLogger(__name__)

@dataclass
class DynexConfig:
    """Configuration for Dynex integration"""
    api_key: str
    mainnet: bool = True
    description: str = "NQBA Quantum Optimization"
    default_reads: int = 1000
    default_annealing_time: int = 100
    timeout_seconds: int = 300

@dataclass
class OptimizationResult:
    """Result from Dynex optimization"""
    success: bool
    samples: List[Dict[str, Any]]
    energy: float
    execution_time: float
    dynex_job_id: Optional[str] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DynexAdapter:
    """Standardized Dynex adapter for NQBA"""
    
    def __init__(self, config: Optional[DynexConfig] = None):
        """Initialize Dynex adapter"""
        if config is None:
            settings = get_settings()
            # Patch: allow test/dev environments to use a dummy key
            api_key = settings.dynex_api_key
            if not api_key:
                env = os.environ.get("NQBA_ENVIRONMENT", "development").lower()
                if env != "production":
                    api_key = "dnx_test_key_1234567890123456"
                else:
                    raise ValueError("Dynex not configured. Set DYNEX_API_KEY environment variable.")
            config = DynexConfig(
                api_key=api_key,
                mainnet=getattr(settings, 'dynex_mainnet', True),
                description="NQBA Quantum Optimization",
                default_reads=getattr(settings, 'dynex_default_reads', 1000),
                default_annealing_time=getattr(settings, 'dynex_default_annealing_time', 100),
                timeout_seconds=getattr(settings, 'dynex_timeout_seconds', 300)
            )
        self.config = config
        # Removed dynex.init() call; DynexSDK uses config files and env vars
        # self._initialize_dynex()
    
    def _initialize_dynex(self):
        """Initialize Dynex with configuration (no-op, kept for compatibility)"""
        logger.info("Dynex initialization skipped: SDK uses config files and env vars.")
    
    def solve_qubo(self, 
                   bqm: dimod.BinaryQuadraticModel,
                   num_reads: Optional[int] = None,
                   annealing_time: Optional[int] = None,
                   description: Optional[str] = None) -> OptimizationResult:
        """
        Solve QUBO problem using Dynex
        
        Args:
            bqm: Binary quadratic model to solve
            num_reads: Number of reads (defaults to config)
            annealing_time: Annealing time in microseconds (defaults to config)
            description: Job description (defaults to config)
        
        Returns:
            OptimizationResult with solution details
        """
        start_time = datetime.now()
        
        try:
            # Use defaults if not specified
            num_reads = num_reads or self.config.default_reads
            annealing_time = annealing_time or self.config.default_annealing_time
            description = description or self.config.description
            
            # Initialize sampler and solve
            sampler = dynex.DynexSampler(
                mainnet=self.config.mainnet,
                description=description
            )
            
            sampleset = sampler.sample(
                bqm,
                num_reads=num_reads,
                annealing_time=annealing_time
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Extract results
            samples = []
            for sample in sampleset.samples():
                sample_dict = dict(sample)
                samples.append(sample_dict)
            
            return OptimizationResult(
                success=True,
                samples=samples,
                energy=sampleset.first.energy,
                execution_time=execution_time,
                dynex_job_id=getattr(sampleset, 'job_id', None),
                metadata={
                    'num_reads': num_reads,
                    'annealing_time': annealing_time,
                    'description': description,
                    'mainnet': self.config.mainnet
                }
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"Dynex optimization failed: {e}")
            
            return OptimizationResult(
                success=False,
                samples=[],
                energy=float('inf'),
                execution_time=execution_time,
                error_message=str(e)
            )
    
    def solve_lead_scoring_qubo(self, lead_data: List[Dict[str, Any]]) -> OptimizationResult:
        """
        Solve lead scoring QUBO problem
        
        Args:
            lead_data: List of lead dictionaries with attributes
        
        Returns:
            OptimizationResult with lead scores
        """
        # Build BQM for lead scoring
        bqm = self._build_lead_scoring_bqm(lead_data)
        
        # Solve with lead scoring specific parameters
        return self.solve_qubo(
            bqm=bqm,
            description="Sigma Select Lead Scoring",
            num_reads=2000,  # More reads for better accuracy
            annealing_time=150  # Longer annealing for complex scoring
        )
    
    def _build_lead_scoring_bqm(self, lead_data: List[Dict[str, Any]]) -> dimod.BinaryQuadraticModel:
        """Build Binary Quadratic Model for lead scoring"""
        bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)
        
        for idx, lead in enumerate(lead_data):
            lead_id = f"lead_{idx}"
            score = 0
            
            # Base scoring factors
            budget = lead.get("budget", "").lower()
            urgency = lead.get("urgency", "").lower()
            pain_points = lead.get("pain_points", "").lower()
            
            # Individual factor scoring
            if budget in ["high", "very high"]:
                score += 30
            if urgency in ["urgent", "very urgent"]:
                score += 30
            if pain_points in ["energy costs", "production delays"]:
                score += 40
            
            # Add quadratic interactions for quantum advantage
            if budget in ["high", "very high"] and urgency in ["urgent", "very urgent"]:
                bqm.add_interaction(f"budget_high_{idx}", f"urgency_urgent_{idx}", -15)
            
            if budget in ["high", "very high"] and pain_points in ["energy costs", "production delays"]:
                bqm.add_interaction(f"budget_high_{idx}", f"pain_energy_{idx}", -20)
            
            if urgency in ["urgent", "very urgent"] and pain_points in ["energy costs", "production delays"]:
                bqm.add_interaction(f"urgency_urgent_{idx}", f"pain_energy_{idx}", -25)
            
            # Add variable with negative score (minimization problem)
            bqm.add_variable(lead_id, -score)
        
        return bqm
    
    def solve_energy_optimization_qubo(self, 
                                     energy_data: Dict[str, Any]) -> OptimizationResult:
        """
        Solve energy optimization QUBO problem
        
        Args:
            energy_data: Energy consumption and cost data
        
        Returns:
            OptimizationResult with optimization results
        """
        # Build BQM for energy optimization
        bqm = self._build_energy_optimization_bqm(energy_data)
        
        return self.solve_qubo(
            bqm=bqm,
            description="FLYFOX Energy Optimizer",
            num_reads=1500,
            annealing_time=200
        )
    
    def _build_energy_optimization_bqm(self, energy_data: Dict[str, Any]) -> dimod.BinaryQuadraticModel:
        """Build Binary Quadratic Model for energy optimization"""
        bqm = dimod.BinaryQuadraticModel({}, {}, 0.0, dimod.BINARY)
        
        # Energy optimization variables
        peak_hours = energy_data.get("peak_hours", [])
        off_peak_hours = energy_data.get("off_peak_hours", [])
        equipment_schedule = energy_data.get("equipment_schedule", {})
        
        # Add variables for equipment scheduling
        for equipment, hours in equipment_schedule.items():
            for hour in range(24):
                var_name = f"{equipment}_hour_{hour}"
                cost = 1.0 if hour in peak_hours else 0.5
                bqm.add_variable(var_name, cost)
        
        # Add constraints for equipment availability
        for equipment, max_hours in equipment_schedule.items():
            constraint_vars = [f"{equipment}_hour_{hour}" for hour in range(24)]
            bqm.add_constraint(constraint_vars, max_hours, strength=100)
        
        return bqm
    
    def get_optimization_history(self) -> List[Dict[str, Any]]:
        """Get history of optimizations (placeholder for future implementation)"""
        # This would integrate with LTC logging system
        return []
    
    def validate_config(self) -> bool:
        """Validate Dynex configuration"""
        try:
            # Test connection with minimal BQM
            test_bqm = dimod.BinaryQuadraticModel({'x': 1}, {}, 0, dimod.BINARY)
            result = self.solve_qubo(test_bqm, num_reads=1, annealing_time=10)
            return result.success
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            return False

# Convenience function for quick QUBO solving
def solve_qubo(bqm: dimod.BinaryQuadraticModel, **kwargs) -> OptimizationResult:
    """Quick QUBO solving with default Dynex configuration"""
    adapter = DynexAdapter()
    return adapter.solve_qubo(bqm, **kwargs)

# Convenience function for lead scoring
def score_leads(lead_data: List[Dict[str, Any]]) -> OptimizationResult:
    """Quick lead scoring with Dynex"""
    adapter = DynexAdapter()
    return adapter.solve_lead_scoring_qubo(lead_data)
