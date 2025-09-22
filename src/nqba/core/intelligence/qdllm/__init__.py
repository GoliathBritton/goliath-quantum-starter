"""qdLLM - Quantum-inspired Large Language Model Engine

This module provides the core qdLLM functionality within the NQBA framework.
qdLLM serves as the primary reasoning and inference engine for quantum-inspired
language processing tasks.

Key Components:
- Engine: Core quantum diffusion processing
- Reversal: Quantum diffusion algorithms and reversal orchestration
- Diffusion: Forward and backward diffusion processes
- Scoring: Coherence measurement and evaluation
- Merge: Coherence merging operations
"""

from .reversal import qdllm_infer
from .engine import QuantumDiffusionEngine
from .diffusion import ForwardDiffusion, BackwardDiffusion
from .scoring import CoherenceScorer
from .merge import CoherenceMerge

__all__ = [
    "qdllm_infer",
    "QuantumDiffusionEngine",
    "ForwardDiffusion",
    "BackwardDiffusion", 
    "CoherenceScorer",
    "CoherenceMerge"
]

# Module metadata
__version__ = "1.0.0"
__description__ = "Quantum-inspired Large Language Model Engine for NQBA"

# Quick access functions for NQBA integration
def process_text(text, engine=None, **kwargs):
    """Process text through qdLLM engine"""
    if engine is None:
        engine = QuantumDiffusionEngine()
    return qdllm_infer(text, engine=engine, **kwargs)

def reason(context, direction="bidirectional", **kwargs):
    """Perform quantum-inspired reasoning on given context"""
    engine = QuantumDiffusionEngine()
    return engine.reason(context, direction=direction, **kwargs)

def create_engine(**config):
    """Create a new qdLLM engine instance"""
    return QuantumDiffusionEngine(**config)