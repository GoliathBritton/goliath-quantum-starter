# src/qdllm/core/merge.py
"""
Coherence Merge System

Implements quantum-inspired merging of forward and backward diffusion candidates
to create unified latent representations in the qdLLM framework.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from abc import ABC, abstractmethod


class BaseMerger(ABC):
    """Base class for candidate merging strategies."""
    
    def __init__(self, latent_dim: int):
        self.latent_dim = latent_dim
        
    @abstractmethod
    def merge_candidates(
        self,
        forward_candidates: np.ndarray,
        backward_candidates: np.ndarray,
        forward_scores: np.ndarray,
        backward_scores: np.ndarray,
        coherence_weight: float
    ) -> np.ndarray:
        """Merge forward and backward candidates into unified representation."""
        pass


class CoherenceMerge(BaseMerger):
    """Quantum-inspired coherence merger for candidate unification."""
    
    def __init__(self, latent_dim: int, merge_strategy: str = "quantum_superposition"):
        super().__init__(latent_dim)
        self.merge_strategy = merge_strategy
        self._initialize_merge_operators()
        
    def _initialize_merge_operators(self):
        """Initialize quantum merge operators."""
        # Unitary transformation matrices for quantum-like operations
        self.forward_unitary = self._generate_unitary_matrix()
        self.backward_unitary = self._generate_unitary_matrix()
        
        # Entanglement operator for cross-direction correlations
        self.entanglement_operator = self._generate_entanglement_operator()
        
    def _generate_unitary_matrix(self) -> np.ndarray:
        """Generate a unitary transformation matrix."""
        # Create random matrix and orthogonalize
        random_matrix = np.random.randn(self.latent_dim, self.latent_dim)
        q, r = np.linalg.qr(random_matrix)
        return q
        
    def _generate_entanglement_operator(self) -> np.ndarray:
        """Generate entanglement operator for cross-direction coupling."""
        # Create symmetric coupling matrix
        coupling = np.random.randn(self.latent_dim, self.latent_dim) * 0.1
        return (coupling + coupling.T) / 2
        
    def merge_candidates(
        self,
        forward_candidates: np.ndarray,
        backward_candidates: np.ndarray,
        forward_scores: np.ndarray,
        backward_scores: np.ndarray,
        coherence_weight: float = 0.7
    ) -> np.ndarray:
        """Merge candidates using quantum-inspired coherence principles."""
        
        if self.merge_strategy == "quantum_superposition":
            return self._quantum_superposition_merge(
                forward_candidates, backward_candidates,
                forward_scores, backward_scores, coherence_weight
            )
        elif self.merge_strategy == "entanglement_merge":
            return self._entanglement_merge(
                forward_candidates, backward_candidates,
                forward_scores, backward_scores, coherence_weight
            )
        elif self.merge_strategy == "coherent_interference":
            return self._coherent_interference_merge(
                forward_candidates, backward_candidates,
                forward_scores, backward_scores, coherence_weight
            )
        else:
            return self._weighted_average_merge(
                forward_candidates, backward_candidates,
                forward_scores, backward_scores, coherence_weight
            )
            
    def _quantum_superposition_merge(
        self,
        forward_candidates: np.ndarray,
        backward_candidates: np.ndarray,
        forward_scores: np.ndarray,
        backward_scores: np.ndarray,
        coherence_weight: float
    ) -> np.ndarray:
        """Merge using quantum superposition principles."""
        
        # Normalize scores to create probability amplitudes
        forward_amplitudes = self._scores_to_amplitudes(forward_scores)
        backward_amplitudes = self._scores_to_amplitudes(backward_scores)
        
        # Create superposition states
        forward_superposition = np.zeros(self.latent_dim)
        backward_superposition = np.zeros(self.latent_dim)
        
        for i, (candidate, amplitude) in enumerate(zip(forward_candidates, forward_amplitudes)):
            forward_superposition += amplitude * candidate
            
        for i, (candidate, amplitude) in enumerate(zip(backward_candidates, backward_amplitudes)):
            backward_superposition += amplitude * candidate
            
        # Apply unitary transformations
        forward_transformed = np.dot(self.forward_unitary, forward_superposition)
        backward_transformed = np.dot(self.backward_unitary, backward_superposition)
        
        # Coherent combination with phase relationships
        phase_factor = np.exp(1j * coherence_weight * np.pi)
        merged_complex = forward_transformed + phase_factor * backward_transformed
        
        # Extract real part and normalize
        merged = np.real(merged_complex)
        norm = np.linalg.norm(merged)
        if norm > 0:
            merged = merged / norm * np.sqrt(self.latent_dim)
            
        return merged
        
    def _entanglement_merge(
        self,
        forward_candidates: np.ndarray,
        backward_candidates: np.ndarray,
        forward_scores: np.ndarray,
        backward_scores: np.ndarray,
        coherence_weight: float
    ) -> np.ndarray:
        """Merge using quantum entanglement-inspired coupling."""
        
        # Select best candidates from each direction
        best_forward_idx = np.argmax(forward_scores)
        best_backward_idx = np.argmax(backward_scores)
        
        best_forward = forward_candidates[best_forward_idx]
        best_backward = backward_candidates[best_backward_idx]
        
        # Create entangled state
        entangled_forward = best_forward + np.dot(self.entanglement_operator, best_backward)
        entangled_backward = best_backward + np.dot(self.entanglement_operator, best_forward)
        
        # Weighted combination
        merged = coherence_weight * entangled_forward + (1 - coherence_weight) * entangled_backward
        
        # Normalize
        norm = np.linalg.norm(merged)
        if norm > 0:
            merged = merged / norm * np.sqrt(self.latent_dim)
            
        return merged
        
    def _coherent_interference_merge(
        self,
        forward_candidates: np.ndarray,
        backward_candidates: np.ndarray,
        forward_scores: np.ndarray,
        backward_scores: np.ndarray,
        coherence_weight: float
    ) -> np.ndarray:
        """Merge using coherent interference patterns."""
        
        # Create interference patterns
        forward_pattern = self._create_interference_pattern(forward_candidates, forward_scores)
        backward_pattern = self._create_interference_pattern(backward_candidates, backward_scores)
        
        # Apply phase shifts for coherent interference
        phase_shift = coherence_weight * np.pi / 2
        forward_shifted = forward_pattern * np.cos(phase_shift)
        backward_shifted = backward_pattern * np.sin(phase_shift)
        
        # Constructive interference
        merged = forward_shifted + backward_shifted
        
        # Apply interference enhancement
        interference_enhancement = self._calculate_interference_enhancement(merged)
        merged = merged * interference_enhancement
        
        # Normalize
        norm = np.linalg.norm(merged)
        if norm > 0:
            merged = merged / norm * np.sqrt(self.latent_dim)
            
        return merged
        
    def _weighted_average_merge(
        self,
        forward_candidates: np.ndarray,
        backward_candidates: np.ndarray,
        forward_scores: np.ndarray,
        backward_scores: np.ndarray,
        coherence_weight: float
    ) -> np.ndarray:
        """Simple weighted average merge (baseline)."""
        
        # Score-weighted averages
        forward_weights = forward_scores / np.sum(forward_scores)
        backward_weights = backward_scores / np.sum(backward_scores)
        
        forward_avg = np.average(forward_candidates, axis=0, weights=forward_weights)
        backward_avg = np.average(backward_candidates, axis=0, weights=backward_weights)
        
        # Weighted combination
        merged = coherence_weight * forward_avg + (1 - coherence_weight) * backward_avg
        
        return merged
        
    def _scores_to_amplitudes(self, scores: np.ndarray) -> np.ndarray:
        """Convert scores to quantum probability amplitudes."""
        # Ensure positive scores
        shifted_scores = scores - np.min(scores) + 1e-10
        
        # Convert to probabilities
        probabilities = shifted_scores / np.sum(shifted_scores)
        
        # Take square root to get amplitudes
        amplitudes = np.sqrt(probabilities)
        
        return amplitudes
        
    def _create_interference_pattern(
        self, 
        candidates: np.ndarray, 
        scores: np.ndarray
    ) -> np.ndarray:
        """Create interference pattern from candidate ensemble."""
        pattern = np.zeros(self.latent_dim)
        
        for i, (candidate, score) in enumerate(zip(candidates, scores)):
            # Create wave-like contribution
            phase = i * 2 * np.pi / len(candidates)
            amplitude = score / np.sum(scores)
            
            wave_contribution = amplitude * candidate * np.cos(phase)
            pattern += wave_contribution
            
        return pattern
        
    def _calculate_interference_enhancement(self, merged: np.ndarray) -> float:
        """Calculate interference enhancement factor."""
        # Measure constructive vs destructive interference
        positive_components = np.sum(merged[merged > 0])
        negative_components = np.sum(np.abs(merged[merged < 0]))
        
        if positive_components + negative_components == 0:
            return 1.0
            
        enhancement = positive_components / (positive_components + negative_components)
        return max(0.5, enhancement)  # Minimum enhancement of 0.5


class AdaptiveMerger(BaseMerger):
    """Adaptive merger that learns optimal merge strategies."""
    
    def __init__(self, latent_dim: int):
        super().__init__(latent_dim)
        self.merge_history = []
        self.performance_history = []
        self.current_strategy = "quantum_superposition"
        
        # Available merge strategies
        self.strategies = [
            "quantum_superposition",
            "entanglement_merge", 
            "coherent_interference",
            "weighted_average"
        ]
        
        # Strategy performance tracking
        self.strategy_performance = {strategy: [] for strategy in self.strategies}
        
    def merge_candidates(
        self,
        forward_candidates: np.ndarray,
        backward_candidates: np.ndarray,
        forward_scores: np.ndarray,
        backward_scores: np.ndarray,
        coherence_weight: float = 0.7
    ) -> np.ndarray:
        """Adaptively merge candidates using best performing strategy."""
        
        # Select strategy based on historical performance
        strategy = self._select_strategy()
        
        # Create merger with selected strategy
        merger = CoherenceMerge(self.latent_dim, strategy)
        
        # Perform merge
        merged = merger.merge_candidates(
            forward_candidates, backward_candidates,
            forward_scores, backward_scores, coherence_weight
        )
        
        # Store merge information for learning
        self.merge_history.append({
            "strategy": strategy,
            "coherence_weight": coherence_weight,
            "forward_scores": forward_scores.copy(),
            "backward_scores": backward_scores.copy(),
            "merged_result": merged.copy()
        })
        
        return merged
        
    def _select_strategy(self) -> str:
        """Select merge strategy based on performance history."""
        if not self.strategy_performance or len(self.merge_history) < 10:
            # Use default strategy initially
            return self.current_strategy
            
        # Calculate average performance for each strategy
        strategy_scores = {}
        for strategy in self.strategies:
            performances = self.strategy_performance[strategy]
            if performances:
                strategy_scores[strategy] = np.mean(performances)
            else:
                strategy_scores[strategy] = 0.0
                
        # Select best performing strategy
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        return best_strategy
        
    def update_performance(self, performance_score: float):
        """Update performance for the last merge operation."""
        if self.merge_history:
            last_merge = self.merge_history[-1]
            strategy = last_merge["strategy"]
            self.strategy_performance[strategy].append(performance_score)
            
            # Keep only recent performance history
            max_history = 100
            if len(self.strategy_performance[strategy]) > max_history:
                self.strategy_performance[strategy] = self.strategy_performance[strategy][-max_history:]
                
    def get_merge_statistics(self) -> Dict[str, Any]:
        """Get statistics about merge performance."""
        stats = {
            "total_merges": len(self.merge_history),
            "current_strategy": self.current_strategy,
            "strategy_performance": {}
        }
        
        for strategy in self.strategies:
            performances = self.strategy_performance[strategy]
            if performances:
                stats["strategy_performance"][strategy] = {
                    "count": len(performances),
                    "mean": np.mean(performances),
                    "std": np.std(performances),
                    "recent_trend": np.mean(performances[-10:]) if len(performances) >= 10 else np.mean(performances)
                }
            else:
                stats["strategy_performance"][strategy] = {
                    "count": 0,
                    "mean": 0.0,
                    "std": 0.0,
                    "recent_trend": 0.0
                }
                
        return stats