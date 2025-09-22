"""QNLP (Quantum Natural Language Processing) Module

This module provides quantum-enhanced natural language processing capabilities
for the qdLLM foundation stack. It bridges human language interaction with
quantum-inspired reasoning engines.

Key Components:
- QNLPProcessor: Main orchestrator for quantum-enhanced NLP
- QuantumEmbeddings: Quantum-inspired text embeddings
- SemanticEntanglement: Relationship modeling between concepts
- ContextualCoherence: Context-aware semantic understanding
- QuantumTokenizer: Enhanced tokenization with quantum properties
"""

from .processor import QNLPProcessor
from .embeddings import QuantumEmbeddings, SemanticEntanglement
from .coherence import ContextualCoherence
from .tokenizer import QuantumTokenizer
from .utils import QNLPUtils, QuantumSemanticMetrics

__version__ = "0.1.0"
__author__ = "NQBA Quantum AI Team"

__all__ = [
    "QNLPProcessor",
    "QuantumEmbeddings",
    "SemanticEntanglement", 
    "ContextualCoherence",
    "QuantumTokenizer",
    "QNLPUtils",
    "QuantumSemanticMetrics"
]