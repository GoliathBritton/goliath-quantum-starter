# src/qdllm/core/diffusion.py
"""
Quantum-Inspired Diffusion Engines

Implements forward and backward diffusion processes for candidate generation
in the qdLLM quantum diffusion framework.
"""

import numpy as np
from typing import List, Optional
from abc import ABC, abstractmethod


class BaseDiffusion(ABC):
    """Base class for diffusion processes."""
    
    def __init__(self, latent_dim: int, noise_scale: float = 0.1):
        self.latent_dim = latent_dim
        self.noise_scale = noise_scale
        
    @abstractmethod
    def generate_candidates(
        self, 
        input_tokens: List[int], 
        n_candidates: int, 
        steps: int
    ) -> np.ndarray:
        """Generate candidate latents through diffusion process."""
        pass
        
    def _embed_tokens(self, tokens: List[int]) -> np.ndarray:
        """Convert tokens to initial latent embedding."""
        # Simple embedding: each token contributes to latent dimensions
        embedding = np.zeros(self.latent_dim)
        for i, token in enumerate(tokens):
            # Distribute token influence across latent dimensions
            start_idx = (i * self.latent_dim // len(tokens))
            end_idx = ((i + 1) * self.latent_dim // len(tokens))
            embedding[start_idx:end_idx] = np.sin(token * 0.01) * (i + 1)
        return embedding
        
    def _apply_quantum_noise(self, latent: np.ndarray, step: int) -> np.ndarray:
        """Apply quantum-inspired noise transformation."""
        # Quantum-inspired noise with phase relationships
        phase = step * 0.1
        noise = np.random.randn(self.latent_dim) * self.noise_scale
        
        # Apply phase-shifted transformations
        cos_component = np.cos(phase) * noise
        sin_component = np.sin(phase) * np.roll(noise, 1)
        
        return latent + cos_component + sin_component
        
    def _diffuse_step(self, latent: np.ndarray, step: int, direction: str) -> np.ndarray:
        """Single diffusion step with quantum-inspired evolution."""
        # Direction-dependent evolution
        if direction == "forward":
            # Forward evolution: expand and explore
            evolution_matrix = self._get_forward_evolution_matrix(step)
        else:
            # Backward evolution: contract and refine
            evolution_matrix = self._get_backward_evolution_matrix(step)
            
        # Apply evolution transformation
        evolved = np.dot(evolution_matrix, latent)
        
        # Add quantum noise
        evolved = self._apply_quantum_noise(evolved, step)
        
        # Normalize to prevent explosion
        norm = np.linalg.norm(evolved)
        if norm > 0:
            evolved = evolved / norm * np.sqrt(self.latent_dim)
            
        return evolved
        
    def _get_forward_evolution_matrix(self, step: int) -> np.ndarray:
        """Generate forward evolution matrix."""
        # Create rotation-like matrix for forward evolution
        angle = step * 0.05
        matrix = np.eye(self.latent_dim)
        
        # Apply rotational transformations
        for i in range(0, self.latent_dim - 1, 2):
            c, s = np.cos(angle), np.sin(angle)
            matrix[i, i] = c
            matrix[i, i+1] = -s
            matrix[i+1, i] = s
            matrix[i+1, i+1] = c
            
        return matrix
        
    def _get_backward_evolution_matrix(self, step: int) -> np.ndarray:
        """Generate backward evolution matrix."""
        # Create contraction-like matrix for backward evolution
        angle = -step * 0.05  # Negative for backward
        matrix = np.eye(self.latent_dim)
        
        # Apply inverse rotational transformations
        for i in range(0, self.latent_dim - 1, 2):
            c, s = np.cos(angle), np.sin(angle)
            matrix[i, i] = c
            matrix[i, i+1] = -s
            matrix[i+1, i] = s
            matrix[i+1, i+1] = c
            
        # Add slight contraction
        matrix *= 0.98
        
        return matrix


class ForwardDiffusion(BaseDiffusion):
    """Forward diffusion process for expanding candidate space."""
    
    def generate_candidates(
        self, 
        input_tokens: List[int], 
        n_candidates: int, 
        steps: int
    ) -> np.ndarray:
        """Generate forward diffusion candidates."""
        # Start with token embedding
        base_embedding = self._embed_tokens(input_tokens)
        
        candidates = []
        for i in range(n_candidates):
            # Each candidate starts with slight variation
            candidate = base_embedding + np.random.randn(self.latent_dim) * 0.01
            
            # Evolve through diffusion steps
            for step in range(steps):
                candidate = self._diffuse_step(candidate, step, "forward")
                
            candidates.append(candidate)
            
        return np.array(candidates)


class BackwardDiffusion(BaseDiffusion):
    """Backward diffusion process for refining candidate space."""
    
    def generate_candidates(
        self, 
        input_tokens: List[int], 
        n_candidates: int, 
        steps: int
    ) -> np.ndarray:
        """Generate backward diffusion candidates."""
        # Start with token embedding
        base_embedding = self._embed_tokens(input_tokens)
        
        candidates = []
        for i in range(n_candidates):
            # Start with more dispersed initial state for backward refinement
            candidate = base_embedding + np.random.randn(self.latent_dim) * 0.1
            
            # Evolve through backward diffusion steps
            for step in range(steps):
                candidate = self._diffuse_step(candidate, step, "backward")
                
            candidates.append(candidate)
            
        return np.array(candidates)


class QuantumDiffusionOperator:
    """Advanced quantum-inspired diffusion operator."""
    
    def __init__(self, latent_dim: int, entanglement_strength: float = 0.1):
        self.latent_dim = latent_dim
        self.entanglement_strength = entanglement_strength
        
    def apply_entanglement(self, candidates: np.ndarray) -> np.ndarray:
        """Apply quantum entanglement-like correlations between candidates."""
        n_candidates = candidates.shape[0]
        
        # Create entanglement matrix
        entanglement_matrix = np.random.randn(n_candidates, n_candidates)
        entanglement_matrix = (entanglement_matrix + entanglement_matrix.T) / 2
        entanglement_matrix *= self.entanglement_strength
        
        # Apply entanglement transformation
        entangled = np.dot(entanglement_matrix, candidates)
        
        # Normalize to preserve magnitude
        for i in range(n_candidates):
            norm = np.linalg.norm(entangled[i])
            if norm > 0:
                entangled[i] = entangled[i] / norm * np.linalg.norm(candidates[i])
                
        return entangled
        
    def apply_superposition(self, candidates: np.ndarray, weights: Optional[np.ndarray] = None) -> np.ndarray:
        """Create superposition states from candidate ensemble."""
        if weights is None:
            weights = np.ones(candidates.shape[0]) / candidates.shape[0]
            
        # Create superposition by weighted combination
        superposition = np.zeros(self.latent_dim)
        for i, candidate in enumerate(candidates):
            superposition += weights[i] * candidate
            
        return superposition
        
    def measure_coherence(self, candidates: np.ndarray) -> float:
        """Measure quantum coherence of candidate ensemble."""
        # Calculate pairwise correlations
        correlations = []
        n_candidates = candidates.shape[0]
        
        for i in range(n_candidates):
            for j in range(i + 1, n_candidates):
                correlation = np.dot(candidates[i], candidates[j])
                correlation /= (np.linalg.norm(candidates[i]) * np.linalg.norm(candidates[j]))
                correlations.append(abs(correlation))
                
        return np.mean(correlations) if correlations else 0.0