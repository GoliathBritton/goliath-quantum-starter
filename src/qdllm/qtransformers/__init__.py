"""QTransformers - Quantum-inspired transformer architecture

This module provides quantum-enhanced transformer blocks and architectures
for structured sequence processing with quantum-inspired attention mechanisms.

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
from .model import QuantumPositionalEncoding
from .blocks import QuantumLayerNorm
from .utils import QTransformerUtils

__version__ = "0.1.0"
__author__ = "NQBA Quantum AI Team"

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