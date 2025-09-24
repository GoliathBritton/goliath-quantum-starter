# qdLLM - Quantum Diffusion Large Language Model
# Core quantum-inspired inference engine for NQBA platform

__version__ = "0.1.0"
__author__ = "NQBA Team"

from .core.reversal import qdllm_infer
from .core.engine import QuantumDiffusionEngine
from .qnlp.processor import QNLPProcessor
from .qtransformers.blocks import QTransformerBlock

__all__ = [
    "qdllm_infer",
    "QuantumDiffusionEngine", 
    "QNLPProcessor",
    "QTransformerBlock"
]