# src/qdllm/core/engine.py
"""
Quantum Diffusion Engine within the Neuromorphic Quantum Business Architecture (NQBA)

Main orchestration engine for the qdLLM quantum diffusion framework.
Integrates diffusion, scoring, and merging components for unified inference.
"""

import numpy as np
import time
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

from .diffusion import ForwardDiffusion, BackwardDiffusion, QuantumDiffusionOperator
from .scoring import CoherenceScorer, EnsembleScorer, QuantumCoherenceMetrics
from .merge import CoherenceMerge, AdaptiveMerger


class QuantumDiffusionEngine:
    """Main quantum diffusion engine for qdLLM inference."""
    
    def __init__(
        self,
        latent_dim: int = 128,
        vocab_size: int = 50257,
        n_candidates: int = 64,
        diffusion_steps: int = 10,
        scorer_type: str = "coherence",
        merger_type: str = "adaptive",
        enable_quantum_ops: bool = True,
        max_workers: int = 4,
        cache_size: int = 1000
    ):
        """
        Initialize the Quantum Diffusion Engine.
        
        Args:
            latent_dim: Dimensionality of latent space
            vocab_size: Size of vocabulary for token projection
            n_candidates: Number of candidates to generate per direction
            diffusion_steps: Number of diffusion evolution steps
            scorer_type: Type of scorer ('coherence', 'ensemble', 'neural')
            merger_type: Type of merger ('coherence', 'adaptive')
            enable_quantum_ops: Enable quantum-inspired operations
            max_workers: Maximum parallel workers
            cache_size: Size of inference cache
        """
        self.latent_dim = latent_dim
        self.vocab_size = vocab_size
        self.n_candidates = n_candidates
        self.diffusion_steps = diffusion_steps
        self.max_workers = max_workers
        self.enable_quantum_ops = enable_quantum_ops
        
        # Initialize components
        self._initialize_diffusion_engines()
        self._initialize_scorer(scorer_type)
        self._initialize_merger(merger_type)
        
        if enable_quantum_ops:
            self.quantum_operator = QuantumDiffusionOperator(latent_dim)
        else:
            self.quantum_operator = None
            
        # Performance tracking
        self.inference_history = []
        self.performance_metrics = {
            "total_inferences": 0,
            "average_time": 0.0,
            "cache_hits": 0,
            "cache_misses": 0
        }
        
        # Simple cache for repeated queries
        self.inference_cache = {}
        self.cache_size = cache_size
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
    def _initialize_diffusion_engines(self):
        """Initialize forward and backward diffusion engines."""
        self.forward_diffusion = ForwardDiffusion(
            latent_dim=self.latent_dim,
            noise_scale=0.1
        )
        self.backward_diffusion = BackwardDiffusion(
            latent_dim=self.latent_dim,
            noise_scale=0.1
        )
        
    def _initialize_scorer(self, scorer_type: str):
        """Initialize coherence scorer."""
        if scorer_type == "ensemble":
            self.scorer = EnsembleScorer(self.latent_dim)
        else:
            self.scorer = CoherenceScorer(self.latent_dim)
            
    def _initialize_merger(self, merger_type: str):
        """Initialize candidate merger."""
        if merger_type == "adaptive":
            self.merger = AdaptiveMerger(self.latent_dim)
        else:
            self.merger = CoherenceMerge(self.latent_dim)
            
    def infer(
        self,
        input_tokens: List[int],
        top_k: int = 5,
        temperature: float = 1.0,
        coherence_weight: float = 0.7,
        use_cache: bool = True,
        return_detailed: bool = False
    ) -> Dict[str, Any]:
        """
        Perform quantum diffusion inference.
        
        Args:
            input_tokens: Input token sequence
            top_k: Number of top tokens to return
            temperature: Sampling temperature
            coherence_weight: Weight for coherence merging
            use_cache: Whether to use inference cache
            return_detailed: Return detailed intermediate results
            
        Returns:
            Inference results dictionary
        """
        start_time = time.time()
        
        # Check cache
        cache_key = self._generate_cache_key(input_tokens, top_k, temperature, coherence_weight)
        if use_cache and cache_key in self.inference_cache:
            self.performance_metrics["cache_hits"] += 1
            cached_result = self.inference_cache[cache_key].copy()
            cached_result["from_cache"] = True
            return cached_result
            
        self.performance_metrics["cache_misses"] += 1
        
        try:
            # Generate candidates in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                forward_future = executor.submit(
                    self._generate_forward_candidates, input_tokens
                )
                backward_future = executor.submit(
                    self._generate_backward_candidates, input_tokens
                )
                
                forward_candidates = forward_future.result()
                backward_candidates = backward_future.result()
                
            # Apply quantum operations if enabled
            if self.enable_quantum_ops and self.quantum_operator:
                forward_candidates = self.quantum_operator.apply_entanglement(forward_candidates)
                backward_candidates = self.quantum_operator.apply_entanglement(backward_candidates)
                
            # Score candidates in parallel
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                forward_score_future = executor.submit(
                    self.scorer.score_candidates, forward_candidates, input_tokens, "forward"
                )
                backward_score_future = executor.submit(
                    self.scorer.score_candidates, backward_candidates, input_tokens, "backward"
                )
                
                forward_scores = forward_score_future.result()
                backward_scores = backward_score_future.result()
                
            # Select top candidates
            top_forward_idx = np.argsort(forward_scores)[-top_k:]
            top_backward_idx = np.argsort(backward_scores)[-top_k:]
            
            top_forward_candidates = forward_candidates[top_forward_idx]
            top_backward_candidates = backward_candidates[top_backward_idx]
            top_forward_scores = forward_scores[top_forward_idx]
            top_backward_scores = backward_scores[top_backward_idx]
            
            # Merge candidates
            merged_latent = self.merger.merge_candidates(
                top_forward_candidates,
                top_backward_candidates,
                top_forward_scores,
                top_backward_scores,
                coherence_weight
            )
            
            # Project to vocabulary
            vocab_logits = self._project_to_vocab(merged_latent, temperature)
            top_tokens, top_probs = self._extract_top_tokens(vocab_logits, top_k)
            
            # Calculate performance metrics
            inference_time = time.time() - start_time
            coherence_metrics = self._calculate_coherence_metrics(
                forward_candidates, backward_candidates, merged_latent
            )
            
            # Build result
            result = {
                "top_tokens": top_tokens,
                "top_probs": top_probs,
                "merged_latent": merged_latent.tolist(),
                "inference_time": inference_time,
                "coherence_metrics": coherence_metrics,
                "from_cache": False
            }
            
            if return_detailed:
                result.update({
                    "forward_scores": forward_scores.tolist(),
                    "backward_scores": backward_scores.tolist(),
                    "forward_candidates": forward_candidates.tolist(),
                    "backward_candidates": backward_candidates.tolist(),
                    "vocab_logits": vocab_logits.tolist()
                })
                
            # Update performance tracking
            self._update_performance_metrics(inference_time, result)
            
            # Cache result
            if use_cache:
                self._cache_result(cache_key, result)
                
            return result
            
        except Exception as e:
            self.logger.error(f"Inference failed: {str(e)}")
            raise
            
    def _generate_forward_candidates(self, input_tokens: List[int]) -> np.ndarray:
        """Generate forward diffusion candidates."""
        return self.forward_diffusion.generate_candidates(
            input_tokens, self.n_candidates, self.diffusion_steps
        )
        
    def _generate_backward_candidates(self, input_tokens: List[int]) -> np.ndarray:
        """Generate backward diffusion candidates."""
        return self.backward_diffusion.generate_candidates(
            input_tokens, self.n_candidates, self.diffusion_steps
        )
        
    def _project_to_vocab(self, latent: np.ndarray, temperature: float) -> np.ndarray:
        """Project latent to vocabulary space."""
        # Simple linear projection (would be learned in practice)
        projection_matrix = np.random.randn(self.latent_dim, self.vocab_size) * 0.1
        logits = np.dot(latent, projection_matrix)
        
        # Apply temperature
        logits = logits / temperature
        
        # Softmax normalization
        exp_logits = np.exp(logits - np.max(logits))
        return np.log(exp_logits / np.sum(exp_logits))
        
    def _extract_top_tokens(self, vocab_logits: np.ndarray, top_k: int) -> Tuple[List[int], List[float]]:
        """Extract top-k tokens and probabilities."""
        top_indices = np.argsort(vocab_logits)[-top_k:]
        top_tokens = top_indices.tolist()
        top_probs = np.exp(vocab_logits[top_indices])
        top_probs = (top_probs / np.sum(top_probs)).tolist()
        return top_tokens, top_probs
        
    def _calculate_coherence_metrics(
        self,
        forward_candidates: np.ndarray,
        backward_candidates: np.ndarray,
        merged_latent: np.ndarray
    ) -> Dict[str, float]:
        """Calculate quantum coherence metrics."""
        metrics = {}
        
        if self.enable_quantum_ops and self.quantum_operator:
            # Measure coherence of candidate ensembles
            forward_coherence = self.quantum_operator.measure_coherence(forward_candidates)
            backward_coherence = self.quantum_operator.measure_coherence(backward_candidates)
            
            metrics["forward_coherence"] = forward_coherence
            metrics["backward_coherence"] = backward_coherence
            
            # Measure merged state properties
            merged_entropy = QuantumCoherenceMetrics.von_neumann_entropy(merged_latent)
            metrics["merged_entropy"] = merged_entropy
            
            # Measure fidelity between directions
            if len(forward_candidates) > 0 and len(backward_candidates) > 0:
                avg_forward = np.mean(forward_candidates, axis=0)
                avg_backward = np.mean(backward_candidates, axis=0)
                fidelity = QuantumCoherenceMetrics.quantum_fidelity(avg_forward, avg_backward)
                metrics["directional_fidelity"] = fidelity
                
        return metrics
        
    def _generate_cache_key(self, input_tokens: List[int], top_k: int, temperature: float, coherence_weight: float) -> str:
        """Generate cache key for inference parameters."""
        return f"{hash(tuple(input_tokens))}_{top_k}_{temperature:.3f}_{coherence_weight:.3f}"
        
    def _cache_result(self, cache_key: str, result: Dict[str, Any]):
        """Cache inference result."""
        if len(self.inference_cache) >= self.cache_size:
            # Remove oldest entry
            oldest_key = next(iter(self.inference_cache))
            del self.inference_cache[oldest_key]
            
        self.inference_cache[cache_key] = result.copy()
        
    def _update_performance_metrics(self, inference_time: float, result: Dict[str, Any]):
        """Update performance tracking metrics."""
        self.performance_metrics["total_inferences"] += 1
        
        # Update average time
        total = self.performance_metrics["total_inferences"]
        current_avg = self.performance_metrics["average_time"]
        self.performance_metrics["average_time"] = (current_avg * (total - 1) + inference_time) / total
        
        # Store inference record
        self.inference_history.append({
            "timestamp": time.time(),
            "inference_time": inference_time,
            "coherence_metrics": result.get("coherence_metrics", {})
        })
        
        # Keep only recent history
        if len(self.inference_history) > 1000:
            self.inference_history = self.inference_history[-1000:]
            
        # Update adaptive merger if applicable
        if hasattr(self.merger, 'update_performance'):
            # Simple performance score based on coherence
            coherence_score = result.get("coherence_metrics", {}).get("forward_coherence", 0.5)
            self.merger.update_performance(coherence_score)
            
    def batch_infer(
        self,
        batch_inputs: List[Dict[str, Any]],
        max_batch_workers: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Perform batch inference on multiple inputs."""
        if max_batch_workers is None:
            max_batch_workers = min(len(batch_inputs), self.max_workers)
            
        with ThreadPoolExecutor(max_workers=max_batch_workers) as executor:
            futures = [executor.submit(self.infer, **inputs) for inputs in batch_inputs]
            results = [future.result() for future in as_completed(futures)]
            
        return results
        
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get engine performance statistics."""
        stats = self.performance_metrics.copy()
        
        if self.inference_history:
            recent_times = [record["inference_time"] for record in self.inference_history[-100:]]
            stats["recent_average_time"] = np.mean(recent_times)
            stats["time_std"] = np.std(recent_times)
            
        stats["cache_hit_rate"] = (
            self.performance_metrics["cache_hits"] / 
            max(1, self.performance_metrics["cache_hits"] + self.performance_metrics["cache_misses"])
        )
        
        if hasattr(self.merger, 'get_merge_statistics'):
            stats["merge_statistics"] = self.merger.get_merge_statistics()
            
        return stats
        
    def clear_cache(self):
        """Clear inference cache."""
        self.inference_cache.clear()
        self.performance_metrics["cache_hits"] = 0
        self.performance_metrics["cache_misses"] = 0
        
    def configure(
        self,
        n_candidates: Optional[int] = None,
        diffusion_steps: Optional[int] = None,
        latent_dim: Optional[int] = None
    ):
        """Reconfigure engine parameters."""
        if n_candidates is not None:
            self.n_candidates = n_candidates
            
        if diffusion_steps is not None:
            self.diffusion_steps = diffusion_steps
            
        if latent_dim is not None and latent_dim != self.latent_dim:
            # Reinitialize components with new latent dimension
            self.latent_dim = latent_dim
            self._initialize_diffusion_engines()
            self._initialize_scorer("coherence")  # Reset to default
            self._initialize_merger("adaptive")   # Reset to default
            
            if self.enable_quantum_ops:
                self.quantum_operator = QuantumDiffusionOperator(latent_dim)
                
        # Clear cache after reconfiguration
        self.clear_cache()