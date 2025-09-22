"""Contextual Coherence - Context-aware semantic understanding

This module provides quantum-inspired contextual coherence analysis for
natural language understanding and semantic consistency evaluation.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
from scipy.spatial.distance import cosine, euclidean
from scipy.stats import entropy

logger = logging.getLogger(__name__)

@dataclass
class CoherenceConfig:
    """Configuration for contextual coherence analysis"""
    coherence_threshold: float = 0.6
    context_window_size: int = 512
    semantic_depth: int = 3
    coherence_metrics: List[str] = None
    enable_quantum_coherence: bool = True
    temporal_coherence: bool = True

    def __post_init__(self):
        if self.coherence_metrics is None:
            self.coherence_metrics = [
                'semantic_consistency',
                'contextual_alignment', 
                'quantum_coherence',
                'temporal_coherence'
            ]

class ContextualCoherence:
    """Context-aware semantic coherence analyzer"""
    
    def __init__(self, coherence_threshold: float = 0.6):
        """Initialize contextual coherence analyzer
        
        Args:
            coherence_threshold: Minimum threshold for coherence acceptance
        """
        self.coherence_threshold = coherence_threshold
        self.config = CoherenceConfig(coherence_threshold=coherence_threshold)
        
        # Initialize coherence metrics
        self.metrics_registry = {
            'semantic_consistency': self._compute_semantic_consistency,
            'contextual_alignment': self._compute_contextual_alignment,
            'quantum_coherence': self._compute_quantum_coherence,
            'temporal_coherence': self._compute_temporal_coherence
        }
        
        logger.info(f"ContextualCoherence initialized with threshold: {coherence_threshold}")
    
    def compute_coherence(self, embeddings: np.ndarray, 
                         texts: List[str],
                         context: Optional[str] = None) -> Dict[str, float]:
        """Compute comprehensive coherence scores
        
        Args:
            embeddings: Quantum embeddings to analyze
            texts: Original text inputs
            context: Optional context for coherence evaluation
            
        Returns:
            Dictionary of coherence scores
        """
        coherence_scores = {}
        
        # Ensure embeddings is 2D
        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)
        
        # Compute each enabled coherence metric
        for metric_name in self.config.coherence_metrics:
            if metric_name in self.metrics_registry:
                try:
                    score = self.metrics_registry[metric_name](
                        embeddings, texts, context
                    )
                    coherence_scores[metric_name] = float(score)
                except Exception as e:
                    logger.warning(f"Failed to compute {metric_name}: {e}")
                    coherence_scores[metric_name] = 0.0
        
        # Compute overall coherence score
        if coherence_scores:
            coherence_scores['overall_coherence'] = np.mean(list(coherence_scores.values()))
        else:
            coherence_scores['overall_coherence'] = 0.0
        
        # Add coherence classification
        overall_score = coherence_scores['overall_coherence']
        coherence_scores['coherence_level'] = self._classify_coherence(overall_score)
        
        return coherence_scores
    
    def extract_contextual_features(self, embeddings: np.ndarray,
                                   texts: List[str],
                                   context: Optional[str] = None) -> Dict[str, Any]:
        """Extract contextual features from embeddings and text
        
        Args:
            embeddings: Quantum embeddings
            texts: Original text inputs
            context: Optional context
            
        Returns:
            Dictionary of contextual features
        """
        features = {}
        
        # Ensure embeddings is 2D
        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)
        
        # Basic embedding statistics
        features['embedding_stats'] = {
            'mean_magnitude': float(np.mean(np.linalg.norm(embeddings, axis=1))),
            'std_magnitude': float(np.std(np.linalg.norm(embeddings, axis=1))),
            'dimensionality': embeddings.shape[1],
            'num_embeddings': embeddings.shape[0]
        }
        
        # Semantic diversity
        features['semantic_diversity'] = self._compute_semantic_diversity(embeddings)
        
        # Context alignment features
        if context:
            features['context_features'] = self._extract_context_features(
                embeddings, texts, context
            )
        
        # Quantum coherence features
        if self.config.enable_quantum_coherence:
            features['quantum_features'] = self._extract_quantum_features(embeddings)
        
        # Temporal features
        if self.config.temporal_coherence and len(texts) > 1:
            features['temporal_features'] = self._extract_temporal_features(
                embeddings, texts
            )
        
        return features
    
    def _compute_semantic_consistency(self, embeddings: np.ndarray,
                                    texts: List[str],
                                    context: Optional[str] = None) -> float:
        """Compute semantic consistency across embeddings"""
        if embeddings.shape[0] < 2:
            return 1.0  # Single embedding is perfectly consistent
        
        # Compute pairwise cosine similarities
        similarities = []
        num_embeddings = embeddings.shape[0]
        
        for i in range(num_embeddings):
            for j in range(i + 1, num_embeddings):
                sim = 1 - cosine(embeddings[i], embeddings[j])
                similarities.append(sim)
        
        # Return mean similarity as consistency measure
        return np.mean(similarities) if similarities else 0.0
    
    def _compute_contextual_alignment(self, embeddings: np.ndarray,
                                    texts: List[str],
                                    context: Optional[str] = None) -> float:
        """Compute alignment with provided context"""
        if not context:
            return 0.5  # Neutral score when no context provided
        
        # Simple context alignment based on keyword overlap
        context_words = set(context.lower().split())
        
        alignment_scores = []
        for text in texts:
            text_words = set(text.lower().split())
            overlap = len(context_words.intersection(text_words))
            total_words = len(context_words.union(text_words))
            
            if total_words > 0:
                jaccard_similarity = overlap / total_words
                alignment_scores.append(jaccard_similarity)
        
        return np.mean(alignment_scores) if alignment_scores else 0.0
    
    def _compute_quantum_coherence(self, embeddings: np.ndarray,
                                 texts: List[str],
                                 context: Optional[str] = None) -> float:
        """Compute quantum-inspired coherence measure"""
        if embeddings.shape[0] == 0:
            return 0.0
        
        # Compute quantum coherence based on superposition principle
        # Measure how well embeddings maintain quantum-like properties
        
        # 1. Compute density matrix (simplified)
        normalized_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        density_matrix = np.dot(normalized_embeddings.T, normalized_embeddings) / embeddings.shape[0]
        
        # 2. Compute coherence as trace of off-diagonal elements
        try:
            # Remove diagonal elements
            off_diagonal = density_matrix - np.diag(np.diag(density_matrix))
            coherence = np.trace(np.abs(off_diagonal)) / (density_matrix.shape[0] - 1)
        except Exception:
            # Fallback to simpler measure
            coherence = np.mean(np.abs(density_matrix - np.eye(density_matrix.shape[0])))
        
        return float(coherence)
    
    def _compute_temporal_coherence(self, embeddings: np.ndarray,
                                  texts: List[str],
                                  context: Optional[str] = None) -> float:
        """Compute temporal coherence across sequence"""
        if embeddings.shape[0] < 2:
            return 1.0  # Single embedding has perfect temporal coherence
        
        # Compute coherence as smoothness of embedding transitions
        temporal_distances = []
        
        for i in range(embeddings.shape[0] - 1):
            distance = euclidean(embeddings[i], embeddings[i + 1])
            temporal_distances.append(distance)
        
        # Coherence is inverse of variance in distances (normalized)
        if temporal_distances:
            distance_variance = np.var(temporal_distances)
            mean_distance = np.mean(temporal_distances)
            
            # Normalize coherence score
            if mean_distance > 0:
                coherence = 1.0 / (1.0 + distance_variance / mean_distance)
            else:
                coherence = 1.0
        else:
            coherence = 1.0
        
        return float(coherence)
    
    def _compute_semantic_diversity(self, embeddings: np.ndarray) -> Dict[str, float]:
        """Compute semantic diversity metrics"""
        if embeddings.shape[0] < 2:
            return {'diversity_score': 0.0, 'entropy': 0.0}
        
        # Compute pairwise distances
        distances = []
        num_embeddings = embeddings.shape[0]
        
        for i in range(num_embeddings):
            for j in range(i + 1, num_embeddings):
                dist = euclidean(embeddings[i], embeddings[j])
                distances.append(dist)
        
        # Diversity as mean distance
        diversity_score = np.mean(distances) if distances else 0.0
        
        # Compute entropy of distance distribution
        if distances:
            # Discretize distances for entropy calculation
            hist, _ = np.histogram(distances, bins=10, density=True)
            hist = hist[hist > 0]  # Remove zero bins
            diversity_entropy = entropy(hist) if len(hist) > 1 else 0.0
        else:
            diversity_entropy = 0.0
        
        return {
            'diversity_score': float(diversity_score),
            'entropy': float(diversity_entropy)
        }
    
    def _extract_context_features(self, embeddings: np.ndarray,
                                texts: List[str],
                                context: str) -> Dict[str, Any]:
        """Extract context-specific features"""
        features = {}
        
        # Context length and complexity
        features['context_length'] = len(context.split())
        features['context_complexity'] = len(set(context.lower().split())) / len(context.split())
        
        # Text-context similarity
        similarities = []
        for text in texts:
            # Simple word overlap similarity
            text_words = set(text.lower().split())
            context_words = set(context.lower().split())
            
            if len(text_words.union(context_words)) > 0:
                similarity = len(text_words.intersection(context_words)) / len(text_words.union(context_words))
                similarities.append(similarity)
        
        features['text_context_similarity'] = {
            'mean': float(np.mean(similarities)) if similarities else 0.0,
            'std': float(np.std(similarities)) if similarities else 0.0,
            'max': float(np.max(similarities)) if similarities else 0.0
        }
        
        return features
    
    def _extract_quantum_features(self, embeddings: np.ndarray) -> Dict[str, Any]:
        """Extract quantum-inspired features"""
        features = {}
        
        # Quantum state purity
        normalized_embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        
        if embeddings.shape[0] > 1:
            # Compute density matrix
            density_matrix = np.dot(normalized_embeddings.T, normalized_embeddings) / embeddings.shape[0]
            
            # Purity = Tr(ρ²)
            try:
                purity = np.trace(np.dot(density_matrix, density_matrix))
                features['quantum_purity'] = float(purity)
            except Exception:
                features['quantum_purity'] = 0.0
            
            # Von Neumann entropy
            try:
                eigenvals = np.linalg.eigvals(density_matrix)
                eigenvals = eigenvals[eigenvals > 1e-10]  # Remove near-zero eigenvalues
                if len(eigenvals) > 0:
                    von_neumann_entropy = -np.sum(eigenvals * np.log2(eigenvals + 1e-10))
                    features['von_neumann_entropy'] = float(von_neumann_entropy)
                else:
                    features['von_neumann_entropy'] = 0.0
            except Exception:
                features['von_neumann_entropy'] = 0.0
        else:
            features['quantum_purity'] = 1.0
            features['von_neumann_entropy'] = 0.0
        
        return features
    
    def _extract_temporal_features(self, embeddings: np.ndarray,
                                 texts: List[str]) -> Dict[str, Any]:
        """Extract temporal sequence features"""
        features = {}
        
        # Temporal smoothness
        if embeddings.shape[0] > 1:
            smoothness_scores = []
            for i in range(embeddings.shape[0] - 1):
                similarity = 1 - cosine(embeddings[i], embeddings[i + 1])
                smoothness_scores.append(similarity)
            
            features['temporal_smoothness'] = {
                'mean': float(np.mean(smoothness_scores)),
                'std': float(np.std(smoothness_scores)),
                'min': float(np.min(smoothness_scores)),
                'max': float(np.max(smoothness_scores))
            }
        
        # Text length progression
        text_lengths = [len(text.split()) for text in texts]
        if len(text_lengths) > 1:
            features['length_progression'] = {
                'mean_length': float(np.mean(text_lengths)),
                'length_variance': float(np.var(text_lengths)),
                'length_trend': float(np.corrcoef(range(len(text_lengths)), text_lengths)[0, 1])
            }
        
        return features
    
    def _classify_coherence(self, coherence_score: float) -> str:
        """Classify coherence level based on score"""
        if coherence_score >= 0.8:
            return 'high'
        elif coherence_score >= 0.6:
            return 'medium'
        elif coherence_score >= 0.4:
            return 'low'
        else:
            return 'very_low'
    
    def reconfigure(self, new_config: CoherenceConfig):
        """Reconfigure coherence analyzer"""
        self.config = new_config
        self.coherence_threshold = new_config.coherence_threshold
        
        logger.info(f"ContextualCoherence reconfigured with: {new_config}")