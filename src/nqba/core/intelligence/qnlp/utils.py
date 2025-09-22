"""QNLP Utils - Utility functions and metrics for quantum natural language processing

This module provides supporting utilities, metrics, and helper functions
for the QNLP processing pipeline.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
import hashlib
import logging
from scipy.spatial.distance import cosine, euclidean
from scipy.stats import entropy, pearsonr
from dataclasses import dataclass
import time

logger = logging.getLogger(__name__)

@dataclass
class QNLPMetrics:
    """Container for QNLP processing metrics"""
    processing_time: float
    embedding_quality: float
    semantic_coherence: float
    quantum_fidelity: float
    entanglement_strength: float
    overall_score: float

class QNLPUtils:
    """Utility functions for QNLP processing"""
    
    def __init__(self):
        """Initialize QNLP utilities"""
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'total_requests': 0
        }
        
        logger.info("QNLPUtils initialized")
    
    def generate_cache_key(self, tokens: Dict[str, Any]) -> str:
        """Generate cache key for tokenized input
        
        Args:
            tokens: Tokenized input dictionary
            
        Returns:
            Hash string for caching
        """
        # Create a string representation of key token properties
        key_data = {
            'token_ids': tokens.get('token_ids', []),
            'input_length': tokens.get('input_length', 0),
            'processed_text': tokens.get('processed_text', '')
        }
        
        # Convert to string and hash
        key_string = str(sorted(key_data.items()))
        cache_key = hashlib.md5(key_string.encode()).hexdigest()
        
        return cache_key
    
    def compute_embedding_similarity(self, emb1: np.ndarray, 
                                   emb2: np.ndarray,
                                   metric: str = 'cosine') -> float:
        """Compute similarity between embeddings
        
        Args:
            emb1: First embedding vector
            emb2: Second embedding vector
            metric: Similarity metric ('cosine', 'euclidean', 'dot')
            
        Returns:
            Similarity score
        """
        if metric == 'cosine':
            return 1 - cosine(emb1, emb2)
        elif metric == 'euclidean':
            return 1 / (1 + euclidean(emb1, emb2))
        elif metric == 'dot':
            return np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        else:
            raise ValueError(f"Unknown similarity metric: {metric}")
    
    def normalize_embeddings(self, embeddings: np.ndarray, 
                           method: str = 'l2') -> np.ndarray:
        """Normalize embeddings using specified method
        
        Args:
            embeddings: Input embeddings
            method: Normalization method ('l2', 'l1', 'max', 'unit')
            
        Returns:
            Normalized embeddings
        """
        if method == 'l2':
            norms = np.linalg.norm(embeddings, axis=-1, keepdims=True)
            return embeddings / np.maximum(norms, 1e-8)
        elif method == 'l1':
            norms = np.sum(np.abs(embeddings), axis=-1, keepdims=True)
            return embeddings / np.maximum(norms, 1e-8)
        elif method == 'max':
            max_vals = np.max(np.abs(embeddings), axis=-1, keepdims=True)
            return embeddings / np.maximum(max_vals, 1e-8)
        elif method == 'unit':
            # Scale to unit range [0, 1]
            min_vals = np.min(embeddings, axis=-1, keepdims=True)
            max_vals = np.max(embeddings, axis=-1, keepdims=True)
            return (embeddings - min_vals) / np.maximum(max_vals - min_vals, 1e-8)
        else:
            raise ValueError(f"Unknown normalization method: {method}")
    
    def compute_text_statistics(self, texts: List[str]) -> Dict[str, Any]:
        """Compute statistical properties of text inputs
        
        Args:
            texts: List of input texts
            
        Returns:
            Dictionary of text statistics
        """
        if not texts:
            return {}
        
        # Basic length statistics
        lengths = [len(text.split()) for text in texts]
        char_lengths = [len(text) for text in texts]
        
        # Vocabulary statistics
        all_words = []
        for text in texts:
            all_words.extend(text.lower().split())
        
        unique_words = set(all_words)
        word_freq = {}
        for word in all_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Compute statistics
        stats = {
            'num_texts': len(texts),
            'word_length_stats': {
                'mean': float(np.mean(lengths)),
                'std': float(np.std(lengths)),
                'min': int(np.min(lengths)),
                'max': int(np.max(lengths)),
                'median': float(np.median(lengths))
            },
            'char_length_stats': {
                'mean': float(np.mean(char_lengths)),
                'std': float(np.std(char_lengths)),
                'min': int(np.min(char_lengths)),
                'max': int(np.max(char_lengths)),
                'median': float(np.median(char_lengths))
            },
            'vocabulary_stats': {
                'total_words': len(all_words),
                'unique_words': len(unique_words),
                'vocabulary_richness': len(unique_words) / max(len(all_words), 1),
                'most_frequent_words': sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            }
        }
        
        return stats
    
    def validate_embeddings(self, embeddings: np.ndarray) -> Dict[str, Any]:
        """Validate embedding quality and properties
        
        Args:
            embeddings: Embedding vectors to validate
            
        Returns:
            Validation results
        """
        validation = {
            'is_valid': True,
            'issues': [],
            'properties': {},
            'recommendations': []
        }
        
        # Check basic properties
        if embeddings.size == 0:
            validation['is_valid'] = False
            validation['issues'].append('Empty embeddings')
            return validation
        
        # Check for NaN or infinite values
        if np.any(np.isnan(embeddings)):
            validation['is_valid'] = False
            validation['issues'].append('Contains NaN values')
        
        if np.any(np.isinf(embeddings)):
            validation['is_valid'] = False
            validation['issues'].append('Contains infinite values')
        
        # Check embedding magnitudes
        norms = np.linalg.norm(embeddings, axis=-1)
        
        if np.any(norms == 0):
            validation['issues'].append('Contains zero-magnitude embeddings')
        
        if np.any(norms > 100):
            validation['issues'].append('Contains very large magnitude embeddings')
            validation['recommendations'].append('Consider normalizing embeddings')
        
        # Compute properties
        validation['properties'] = {
            'shape': embeddings.shape,
            'dtype': str(embeddings.dtype),
            'magnitude_stats': {
                'mean': float(np.mean(norms)),
                'std': float(np.std(norms)),
                'min': float(np.min(norms)),
                'max': float(np.max(norms))
            },
            'value_range': {
                'min': float(np.min(embeddings)),
                'max': float(np.max(embeddings)),
                'mean': float(np.mean(embeddings)),
                'std': float(np.std(embeddings))
            }
        }
        
        return validation
    
    def benchmark_processing_time(self, func, *args, **kwargs) -> Tuple[Any, float]:
        """Benchmark function execution time
        
        Args:
            func: Function to benchmark
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Tuple of (function_result, execution_time)
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        return result, execution_time
    
    def update_cache_stats(self, hit: bool):
        """Update cache statistics
        
        Args:
            hit: Whether cache hit occurred
        """
        self.cache_stats['total_requests'] += 1
        if hit:
            self.cache_stats['hits'] += 1
        else:
            self.cache_stats['misses'] += 1
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics
        
        Returns:
            Cache statistics dictionary
        """
        total = self.cache_stats['total_requests']
        if total > 0:
            hit_rate = self.cache_stats['hits'] / total
            miss_rate = self.cache_stats['misses'] / total
        else:
            hit_rate = miss_rate = 0.0
        
        return {
            **self.cache_stats,
            'hit_rate': hit_rate,
            'miss_rate': miss_rate
        }

class QuantumSemanticMetrics:
    """Quantum-inspired semantic metrics for QNLP evaluation"""
    
    def __init__(self):
        """Initialize quantum semantic metrics"""
        logger.info("QuantumSemanticMetrics initialized")
    
    def compute_quantum_fidelity(self, state1: np.ndarray, 
                               state2: np.ndarray) -> float:
        """Compute quantum fidelity between two states
        
        Args:
            state1: First quantum state (embedding)
            state2: Second quantum state (embedding)
            
        Returns:
            Quantum fidelity score [0, 1]
        """
        # Normalize states
        state1_norm = state1 / np.linalg.norm(state1)
        state2_norm = state2 / np.linalg.norm(state2)
        
        # Compute fidelity as squared overlap
        fidelity = np.abs(np.dot(state1_norm, state2_norm))**2
        
        return float(fidelity)
    
    def compute_von_neumann_entropy(self, density_matrix: np.ndarray) -> float:
        """Compute von Neumann entropy of density matrix
        
        Args:
            density_matrix: Density matrix representation
            
        Returns:
            von Neumann entropy
        """
        try:
            # Compute eigenvalues
            eigenvals = np.linalg.eigvals(density_matrix)
            
            # Remove near-zero eigenvalues
            eigenvals = eigenvals[eigenvals > 1e-10]
            
            if len(eigenvals) == 0:
                return 0.0
            
            # Compute entropy
            entropy_val = -np.sum(eigenvals * np.log2(eigenvals + 1e-10))
            
            return float(entropy_val)
        
        except Exception as e:
            logger.warning(f"Failed to compute von Neumann entropy: {e}")
            return 0.0
    
    def compute_entanglement_measure(self, embeddings: np.ndarray) -> float:
        """Compute entanglement measure for embedding set
        
        Args:
            embeddings: Set of embeddings to analyze
            
        Returns:
            Entanglement measure [0, 1]
        """
        if embeddings.shape[0] < 2:
            return 0.0
        
        # Compute correlation matrix
        correlation_matrix = np.corrcoef(embeddings)
        
        # Remove diagonal (self-correlations)
        off_diagonal = correlation_matrix - np.diag(np.diag(correlation_matrix))
        
        # Entanglement as mean absolute correlation
        entanglement = np.mean(np.abs(off_diagonal))
        
        return float(entanglement)
    
    def compute_coherence_measure(self, embeddings: np.ndarray) -> float:
        """Compute quantum coherence measure
        
        Args:
            embeddings: Embeddings to analyze for coherence
            
        Returns:
            Coherence measure [0, 1]
        """
        if embeddings.shape[0] == 0:
            return 0.0
        
        # Normalize embeddings
        normalized = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        # Compute density matrix
        density_matrix = np.dot(normalized.T, normalized) / embeddings.shape[0]
        
        # Coherence as sum of off-diagonal elements
        off_diagonal_sum = np.sum(np.abs(density_matrix)) - np.sum(np.abs(np.diag(density_matrix)))
        max_possible = density_matrix.shape[0] * (density_matrix.shape[0] - 1)
        
        if max_possible > 0:
            coherence = off_diagonal_sum / max_possible
        else:
            coherence = 0.0
        
        return float(coherence)
    
    def compute_semantic_distance(self, emb1: np.ndarray, 
                                emb2: np.ndarray,
                                metric: str = 'quantum') -> float:
        """Compute semantic distance between embeddings
        
        Args:
            emb1: First embedding
            emb2: Second embedding
            metric: Distance metric ('quantum', 'cosine', 'euclidean')
            
        Returns:
            Semantic distance
        """
        if metric == 'quantum':
            # Quantum-inspired distance based on fidelity
            fidelity = self.compute_quantum_fidelity(emb1, emb2)
            distance = 1 - fidelity
        elif metric == 'cosine':
            distance = cosine(emb1, emb2)
        elif metric == 'euclidean':
            distance = euclidean(emb1, emb2)
        else:
            raise ValueError(f"Unknown distance metric: {metric}")
        
        return float(distance)
    
    def evaluate_qnlp_quality(self, embeddings: np.ndarray,
                            texts: List[str],
                            processing_time: float) -> QNLPMetrics:
        """Evaluate overall QNLP processing quality
        
        Args:
            embeddings: Generated embeddings
            texts: Original texts
            processing_time: Time taken for processing
            
        Returns:
            QNLPMetrics object with quality scores
        """
        # Embedding quality (based on magnitude and distribution)
        norms = np.linalg.norm(embeddings, axis=-1)
        embedding_quality = 1.0 / (1.0 + np.std(norms))  # Lower std = higher quality
        
        # Semantic coherence
        semantic_coherence = self.compute_coherence_measure(embeddings)
        
        # Quantum fidelity (average pairwise)
        if embeddings.shape[0] > 1:
            fidelities = []
            for i in range(embeddings.shape[0]):
                for j in range(i + 1, embeddings.shape[0]):
                    fidelity = self.compute_quantum_fidelity(embeddings[i], embeddings[j])
                    fidelities.append(fidelity)
            quantum_fidelity = np.mean(fidelities) if fidelities else 0.0
        else:
            quantum_fidelity = 1.0
        
        # Entanglement strength
        entanglement_strength = self.compute_entanglement_measure(embeddings)
        
        # Overall score (weighted combination)
        overall_score = (
            0.3 * embedding_quality +
            0.3 * semantic_coherence +
            0.2 * quantum_fidelity +
            0.2 * entanglement_strength
        )
        
        return QNLPMetrics(
            processing_time=processing_time,
            embedding_quality=float(embedding_quality),
            semantic_coherence=float(semantic_coherence),
            quantum_fidelity=float(quantum_fidelity),
            entanglement_strength=float(entanglement_strength),
            overall_score=float(overall_score)
        )
    
    def compare_embeddings(self, embeddings1: np.ndarray,
                         embeddings2: np.ndarray) -> Dict[str, float]:
        """Compare two sets of embeddings
        
        Args:
            embeddings1: First set of embeddings
            embeddings2: Second set of embeddings
            
        Returns:
            Comparison metrics
        """
        comparison = {}
        
        # Ensure same shape
        if embeddings1.shape != embeddings2.shape:
            comparison['shape_mismatch'] = True
            return comparison
        
        comparison['shape_mismatch'] = False
        
        # Compute various distance metrics
        if embeddings1.shape[0] == 1:
            # Single embeddings
            comparison['cosine_similarity'] = 1 - cosine(embeddings1[0], embeddings2[0])
            comparison['euclidean_distance'] = euclidean(embeddings1[0], embeddings2[0])
            comparison['quantum_fidelity'] = self.compute_quantum_fidelity(embeddings1[0], embeddings2[0])
        else:
            # Multiple embeddings - compute averages
            cosine_sims = []
            euclidean_dists = []
            quantum_fidelities = []
            
            for i in range(embeddings1.shape[0]):
                cosine_sims.append(1 - cosine(embeddings1[i], embeddings2[i]))
                euclidean_dists.append(euclidean(embeddings1[i], embeddings2[i]))
                quantum_fidelities.append(self.compute_quantum_fidelity(embeddings1[i], embeddings2[i]))
            
            comparison['cosine_similarity'] = float(np.mean(cosine_sims))
            comparison['euclidean_distance'] = float(np.mean(euclidean_dists))
            comparison['quantum_fidelity'] = float(np.mean(quantum_fidelities))
        
        # Coherence comparison
        coherence1 = self.compute_coherence_measure(embeddings1)
        coherence2 = self.compute_coherence_measure(embeddings2)
        comparison['coherence_difference'] = float(abs(coherence1 - coherence2))
        
        # Entanglement comparison
        entanglement1 = self.compute_entanglement_measure(embeddings1)
        entanglement2 = self.compute_entanglement_measure(embeddings2)
        comparison['entanglement_difference'] = float(abs(entanglement1 - entanglement2))
        
        return comparison