"""Legacy System Analyzer using QNLP

This module provides analysis capabilities for legacy systems, including
documentation parsing, code understanding, and protocol interpretation
using Quantum Natural Language Processing (QNLP).

Key Components:
- LegacyAnalyzer: Main class for analyzing legacy artifacts
- Uses QNLPProcessor for quantum-enhanced text analysis
- Integrates with SemanticEntanglement for relationship mapping
- Employs ContextualCoherence for understanding complex contexts
"""

import logging
from typing import Dict, Any, List, Optional
import numpy as np

from nqba.core.intelligence.qnlp.processor import QNLPProcessor
from nqba.core.intelligence.qnlp.embeddings import SemanticEntanglement
from nqba.core.intelligence.qnlp.coherence import ContextualCoherence
from nqba.core.intelligence.qnlp.tokenizer import QuantumTokenizer
from nqba.core.intelligence.qnlp.utils import QuantumSemanticMetrics

logger = logging.getLogger(__name__)

class LegacyAnalyzer:
    """Analyzer for legacy systems using QNLP"""
    
    def __init__(self):
        self.processor = QNLPProcessor()
        self.entanglement = SemanticEntanglement()
        self.coherence = ContextualCoherence()
        self.tokenizer = QuantumTokenizer()
        self.metrics = QuantumSemanticMetrics()
        
        logger.info("Legacy Analyzer initialized with QNLP components")
    
    def analyze_documentation(self, doc_text: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze legacy documentation"""
        params = params or {}
        
        # Tokenize
        tokens = self.tokenizer.tokenize(doc_text)
        
        # Process with QNLP
        output = self.processor.process(tokens, **params)
        
        # Compute entanglements
        entanglements = self.entanglement.compute_entanglements(output.quantum_embeddings)
        
        # Compute coherence
        coherence = self.coherence.compute_coherence(output.quantum_embeddings)
        
        # Metrics
        metrics = self.metrics.compute_all(output.quantum_embeddings)
        
        return {
            'tokens': tokens,
            'embeddings': output.quantum_embeddings.tolist(),
            'entanglements': entanglements,
            'coherence': coherence,
            'metrics': metrics,
            'metadata': output.processing_metadata
        }
    
    def analyze_code(self, code_text: str, language: str = 'cobol', params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze legacy code (e.g., COBOL, ladder logic)"""
        params = params or {'mode': 'code_analysis', 'language': language}
        return self.analyze_documentation(code_text, params)
    
    def analyze_protocol(self, protocol_desc: str, protocol_type: str = 'opc_ua', params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Analyze industrial protocols (e.g., OPC UA, CIP, Profinet)"""
        params = params or {'mode': 'protocol_analysis', 'protocol': protocol_type}
        return self.analyze_documentation(protocol_desc, params)
    
    def compare_artifacts(self, artifact1: str, artifact2: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """Compare two legacy artifacts (docs, code, protocols)"""
        params = params or {}
        
        analysis1 = self.analyze_documentation(artifact1, params)
        analysis2 = self.analyze_documentation(artifact2, params)
        
        emb1 = np.array(analysis1['embeddings'])
        emb2 = np.array(analysis2['embeddings'])
        
        return self.metrics.compute_similarity(emb1, emb2)
    
    def extract_relationships(self, text: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Extract semantic relationships from legacy artifacts"""
        analysis = self.analyze_documentation(text, params)
        return self.entanglement.extract_relationships(analysis['entanglements'])