"""QNLP Processor - Main orchestrator for quantum-enhanced NLP

This module provides the primary interface for quantum natural language processing,
integrating quantum-inspired embeddings, semantic entanglement, and contextual coherence.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple, Union
from dataclasses import dataclass
import logging
from concurrent.futures import ThreadPoolExecutor

from .embeddings import QuantumEmbeddings, SemanticEntanglement
from .coherence import ContextualCoherence
from .tokenizer import QuantumTokenizer
from .utils import QNLPUtils, QuantumSemanticMetrics

logger = logging.getLogger(__name__)

@dataclass
class QNLPConfig:
    """Configuration for QNLP processor"""
    embedding_dim: int = 512
    max_sequence_length: int = 2048
    quantum_layers: int = 4
    entanglement_strength: float = 0.7
    coherence_threshold: float = 0.6
    parallel_workers: int = 4
    cache_embeddings: bool = True
    use_semantic_entanglement: bool = True
    enable_contextual_coherence: bool = True

@dataclass
class QNLPOutput:
    """Output structure for QNLP processing"""
    quantum_embeddings: np.ndarray
    semantic_relationships: Dict[str, Any]
    coherence_scores: Dict[str, float]
    entanglement_matrix: Optional[np.ndarray]
    contextual_features: Dict[str, Any]
    processing_metadata: Dict[str, Any]

class QNLPProcessor:
    """Main QNLP processor for quantum-enhanced natural language processing"""
    
    def __init__(self, config: Optional[QNLPConfig] = None):
        """Initialize QNLP processor with configuration
        
        Args:
            config: QNLP configuration object
        """
        self.config = config or QNLPConfig()
        
        # Initialize core components
        self.tokenizer = QuantumTokenizer(
            max_length=self.config.max_sequence_length
        )
        
        self.embeddings = QuantumEmbeddings(
            embedding_dim=self.config.embedding_dim,
            quantum_layers=self.config.quantum_layers
        )
        
        self.semantic_entanglement = SemanticEntanglement(
            embedding_dim=self.config.embedding_dim,
            entanglement_strength=self.config.entanglement_strength
        )
        
        self.contextual_coherence = ContextualCoherence(
            coherence_threshold=self.config.coherence_threshold
        )
        
        self.utils = QNLPUtils()
        self.metrics = QuantumSemanticMetrics()
        
        # Processing cache
        self._embedding_cache = {} if self.config.cache_embeddings else None
        self._processing_stats = {
            'total_processed': 0,
            'cache_hits': 0,
            'avg_processing_time': 0.0
        }
        
        logger.info(f"QNLP Processor initialized with config: {self.config}")
    
    def process_text(self, text: Union[str, List[str]], 
                    context: Optional[str] = None,
                    return_intermediate: bool = False) -> QNLPOutput:
        """Process text through quantum-enhanced NLP pipeline
        
        Args:
            text: Input text or list of texts
            context: Optional context for coherence analysis
            return_intermediate: Whether to return intermediate processing steps
            
        Returns:
            QNLPOutput with quantum embeddings and semantic analysis
        """
        import time
        start_time = time.time()
        
        # Handle single text or batch
        if isinstance(text, str):
            texts = [text]
            single_input = True
        else:
            texts = text
            single_input = False
        
        # Step 1: Tokenization with quantum properties
        tokenized_data = []
        for txt in texts:
            tokens = self.tokenizer.tokenize(txt)
            tokenized_data.append(tokens)
        
        # Step 2: Generate quantum embeddings
        quantum_embeddings = self._generate_quantum_embeddings(
            tokenized_data, return_intermediate
        )
        
        # Step 3: Semantic entanglement analysis
        semantic_relationships = {}
        entanglement_matrix = None
        
        if self.config.use_semantic_entanglement:
            semantic_relationships, entanglement_matrix = self._analyze_semantic_entanglement(
                quantum_embeddings, tokenized_data
            )
        
        # Step 4: Contextual coherence evaluation
        coherence_scores = {}
        contextual_features = {}
        
        if self.config.enable_contextual_coherence:
            coherence_scores, contextual_features = self._evaluate_contextual_coherence(
                quantum_embeddings, texts, context
            )
        
        # Step 5: Compile processing metadata
        processing_time = time.time() - start_time
        metadata = {
            'processing_time': processing_time,
            'input_length': len(texts),
            'embedding_dimension': self.config.embedding_dim,
            'quantum_layers_used': self.config.quantum_layers,
            'cache_hit': False  # Updated in _generate_quantum_embeddings
        }
        
        # Update processing statistics
        self._update_processing_stats(processing_time)
        
        # Return single embedding if single input
        if single_input:
            quantum_embeddings = quantum_embeddings[0] if len(quantum_embeddings) > 0 else quantum_embeddings
        
        return QNLPOutput(
            quantum_embeddings=quantum_embeddings,
            semantic_relationships=semantic_relationships,
            coherence_scores=coherence_scores,
            entanglement_matrix=entanglement_matrix,
            contextual_features=contextual_features,
            processing_metadata=metadata
        )
    
    def batch_process(self, texts: List[str], 
                     contexts: Optional[List[str]] = None,
                     parallel: bool = True) -> List[QNLPOutput]:
        """Process multiple texts in batch with optional parallelization
        
        Args:
            texts: List of input texts
            contexts: Optional list of contexts for each text
            parallel: Whether to use parallel processing
            
        Returns:
            List of QNLPOutput objects
        """
        if contexts is None:
            contexts = [None] * len(texts)
        
        if parallel and len(texts) > 1:
            with ThreadPoolExecutor(max_workers=self.config.parallel_workers) as executor:
                futures = [
                    executor.submit(self.process_text, text, context)
                    for text, context in zip(texts, contexts)
                ]
                results = [future.result() for future in futures]
        else:
            results = [
                self.process_text(text, context)
                for text, context in zip(texts, contexts)
            ]
        
        return results
    
    def _generate_quantum_embeddings(self, tokenized_data: List[Dict], 
                                   return_intermediate: bool = False) -> np.ndarray:
        """Generate quantum-inspired embeddings for tokenized data"""
        embeddings = []
        
        for tokens in tokenized_data:
            # Check cache first
            cache_key = self.utils.generate_cache_key(tokens) if self._embedding_cache else None
            
            if cache_key and cache_key in self._embedding_cache:
                embedding = self._embedding_cache[cache_key]
                self._processing_stats['cache_hits'] += 1
            else:
                # Generate new embedding
                embedding = self.embeddings.embed_tokens(tokens)
                
                # Cache if enabled
                if cache_key and self._embedding_cache is not None:
                    self._embedding_cache[cache_key] = embedding
            
            embeddings.append(embedding)
        
        return np.array(embeddings)
    
    def _analyze_semantic_entanglement(self, embeddings: np.ndarray, 
                                     tokenized_data: List[Dict]) -> Tuple[Dict, np.ndarray]:
        """Analyze semantic entanglement between concepts"""
        relationships = {}
        entanglement_matrix = None
        
        try:
            # Generate entanglement relationships
            entanglement_matrix = self.semantic_entanglement.create_entanglement_matrix(embeddings)
            
            # Extract semantic relationships
            relationships = self.semantic_entanglement.extract_relationships(
                embeddings, tokenized_data, entanglement_matrix
            )
            
        except Exception as e:
            logger.warning(f"Semantic entanglement analysis failed: {e}")
            relationships = {'error': str(e)}
        
        return relationships, entanglement_matrix
    
    def _evaluate_contextual_coherence(self, embeddings: np.ndarray, 
                                     texts: List[str], 
                                     context: Optional[str]) -> Tuple[Dict, Dict]:
        """Evaluate contextual coherence of embeddings"""
        coherence_scores = {}
        contextual_features = {}
        
        try:
            # Compute coherence scores
            coherence_scores = self.contextual_coherence.compute_coherence(
                embeddings, texts, context
            )
            
            # Extract contextual features
            contextual_features = self.contextual_coherence.extract_contextual_features(
                embeddings, texts, context
            )
            
        except Exception as e:
            logger.warning(f"Contextual coherence evaluation failed: {e}")
            coherence_scores = {'error': str(e)}
            contextual_features = {'error': str(e)}
        
        return coherence_scores, contextual_features
    
    def _update_processing_stats(self, processing_time: float):
        """Update internal processing statistics"""
        self._processing_stats['total_processed'] += 1
        
        # Update running average
        total = self._processing_stats['total_processed']
        current_avg = self._processing_stats['avg_processing_time']
        self._processing_stats['avg_processing_time'] = (
            (current_avg * (total - 1) + processing_time) / total
        )
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get current processing statistics"""
        stats = self._processing_stats.copy()
        if self._embedding_cache:
            stats['cache_size'] = len(self._embedding_cache)
            stats['cache_hit_rate'] = (
                stats['cache_hits'] / max(stats['total_processed'], 1)
            )
        return stats
    
    def clear_cache(self):
        """Clear embedding cache"""
        if self._embedding_cache:
            self._embedding_cache.clear()
            logger.info("QNLP embedding cache cleared")
    
    def reconfigure(self, new_config: QNLPConfig):
        """Reconfigure processor with new settings"""
        self.config = new_config
        
        # Reinitialize components if necessary
        if hasattr(self, 'embeddings'):
            self.embeddings.reconfigure(
                embedding_dim=new_config.embedding_dim,
                quantum_layers=new_config.quantum_layers
            )
        
        logger.info(f"QNLP Processor reconfigured with: {new_config}")