"""QNLP (Quantum Natural Language Processing) Module

This module provides quantum-enhanced natural language processing capabilities
within the NQBA (Neuromorphic Quantum Business Architecture) framework. 
It serves as a core intelligence component that bridges human language 
interaction with quantum-inspired reasoning engines.

As part of NQBA's foundational intelligence layer, QNLP works in conjunction
with qdLLM and QTransformers to provide comprehensive language understanding
and processing capabilities for business applications.

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

__version__ = "1.0.0"
__author__ = "NQBA Development Team"
__description__ = "Quantum Natural Language Processing for NQBA Framework"

__all__ = [
    "QNLPProcessor",
    "QuantumEmbeddings",
    "SemanticEntanglement", 
    "ContextualCoherence",
    "QuantumTokenizer",
    "QNLPUtils",
    "QuantumSemanticMetrics"
]

# NQBA Integration Functions
def analyze(text, processor=None, **kwargs):
    """Analyze text using QNLP within NQBA framework"""
    if processor is None:
        processor = QNLPProcessor()
    return processor.analyze(text, **kwargs)

def encode(text, embeddings=None, **kwargs):
    """Encode text into quantum-inspired embeddings"""
    if embeddings is None:
        embeddings = QuantumEmbeddings()
    return embeddings.encode(text, **kwargs)

def create_processor(**config):
    """Create a new QNLP processor instance for NQBA"""
    return QNLPProcessor(**config)

def get_semantic_coherence(text1, text2, **kwargs):
    """Measure semantic coherence between two texts"""
    coherence = ContextualCoherence()
    return coherence.measure(text1, text2, **kwargs)