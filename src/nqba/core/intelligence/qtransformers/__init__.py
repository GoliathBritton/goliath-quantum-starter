"""QTransformers - Quantum-inspired transformer architecture

This module provides quantum-enhanced transformer blocks and architectures
within the NQBA (Neuromorphic Quantum Business Architecture) framework.
It serves as a core intelligence component for structured sequence processing
with quantum-inspired attention mechanisms.

As part of NQBA's foundational intelligence layer, QTransformers works in
conjunction with qdLLM and QNLP to provide advanced pattern recognition,
sequence optimization, and structured data transformation capabilities
for business applications.

Key Components:
- QTransformerBlock: Quantum-enhanced transformer block
- QuantumAttention: Quantum-inspired attention mechanism
- QuantumFeedForward: Quantum-enhanced feed-forward network
- QTransformerModel: Complete quantum transformer model
- QuantumPositionalEncoding: Quantum-inspired positional encoding
"""

from .blocks import QTransformerBlock, QuantumFeedForward
from .attention import QuantumAttention, QuantumMultiHeadAttention
from .model import QTransformerModel, QTransformerConfig
from .encoding import QuantumPositionalEncoding
from .layers import QuantumLayerNorm, QuantumDropout
from .utils import QTransformerUtils, QuantumActivations

__version__ = "1.0.0"
__author__ = "NQBA Development Team"
__description__ = "Quantum-inspired Transformers for NQBA Framework"

__all__ = [
    "QTransformerBlock",
    "QuantumAttention",
    "QuantumMultiHeadAttention",
    "QuantumFeedForward",
    "QTransformerModel",
    "QTransformerConfig",
    "QuantumPositionalEncoding",
    "QuantumLayerNorm",
    "QuantumDropout",
    "QTransformerUtils",
    "QuantumActivations"
]

# NQBA Integration Functions
def optimize(sequence, model=None, **kwargs):
    """Optimize sequence using QTransformers within NQBA framework"""
    if model is None:
        config = QTransformerConfig()
        model = QTransformerModel(config)
    return model.optimize(sequence, **kwargs)

def transform(input_data, model=None, **kwargs):
    """Transform structured data using quantum-inspired transformers"""
    if model is None:
        config = QTransformerConfig()
        model = QTransformerModel(config)
    return model.transform(input_data, **kwargs)

def create_model(config=None, **kwargs):
    """Create a new QTransformer model instance for NQBA"""
    if config is None:
        config = QTransformerConfig(**kwargs)
    return QTransformerModel(config)

def analyze_patterns(sequence, **kwargs):
    """Analyze patterns in sequence data using quantum attention"""
    attention = QuantumMultiHeadAttention()
    return attention.analyze_patterns(sequence, **kwargs)