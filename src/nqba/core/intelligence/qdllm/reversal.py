# src/qdllm/core/reversal.py
"""
Quantum Diffusion LLM - Core Reversal Orchestration

Implements bidirectional quantum-inspired diffusion for language model inference.
This module orchestrates forward/backward candidate generation, scoring, and coherence merging.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor
import time

from .diffusion import ForwardDiffusion, BackwardDiffusion
from .scoring import CoherenceScorer
from .merge import CoherenceMerge


def qdllm_infer(
    input_tokens: List[int],
    n_candidates: int = 64,
    latent_dim: int = 128,
    top_k: int = 5,
    vocab_size: int = 50257,
    diffusion_steps: int = 10,
    coherence_weight: float = 0.7,
    temperature: float = 1.0,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Main qdLLM inference function implementing quantum diffusion reversal.
    
    Args:
        input_tokens: Input token sequence
        n_candidates: Number of candidate latents to generate
        latent_dim: Dimensionality of latent space
        top_k: Number of top tokens to return
        vocab_size: Vocabulary size for token projection
        diffusion_steps: Number of diffusion evolution steps
        coherence_weight: Weight for coherence scoring (0-1)
        temperature: Sampling temperature
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary containing:
        - top_tokens: List of top-k token IDs
        - top_probs: List of corresponding probabilities
        - merged_latent: Final merged latent representation
        - forward_scores: Forward coherence scores
        - backward_scores: Backward coherence scores
        - inference_time: Total inference time in seconds
    """
    start_time = time.time()
    
    if seed is not None:
        np.random.seed(seed)
    
    # Initialize diffusion engines
    forward_diffusion = ForwardDiffusion(latent_dim=latent_dim)
    backward_diffusion = BackwardDiffusion(latent_dim=latent_dim)
    
    # Initialize scoring and merging components
    scorer = CoherenceScorer(latent_dim=latent_dim)
    merger = CoherenceMerge(latent_dim=latent_dim)
    
    # Generate initial candidate latents
    forward_candidates = forward_diffusion.generate_candidates(
        input_tokens, n_candidates, diffusion_steps
    )
    backward_candidates = backward_diffusion.generate_candidates(
        input_tokens, n_candidates, diffusion_steps
    )
    
    # Parallel scoring of candidates
    with ThreadPoolExecutor(max_workers=4) as executor:
        forward_future = executor.submit(
            scorer.score_candidates, forward_candidates, input_tokens, "forward"
        )
        backward_future = executor.submit(
            scorer.score_candidates, backward_candidates, input_tokens, "backward"
        )
        
        forward_scores = forward_future.result()
        backward_scores = backward_future.result()
    
    # Select top-k candidates from each direction
    top_forward_idx = np.argsort(forward_scores)[-top_k:]
    top_backward_idx = np.argsort(backward_scores)[-top_k:]
    
    top_forward_candidates = forward_candidates[top_forward_idx]
    top_backward_candidates = backward_candidates[top_backward_idx]
    
    # Coherence merge of top candidates
    merged_latent = merger.merge_candidates(
        top_forward_candidates,
        top_backward_candidates,
        forward_scores[top_forward_idx],
        backward_scores[top_backward_idx],
        coherence_weight
    )
    
    # Project to vocabulary space
    vocab_logits = _project_to_vocab(merged_latent, vocab_size, temperature)
    
    # Get top-k tokens and probabilities
    top_token_idx = np.argsort(vocab_logits)[-top_k:]
    top_tokens = top_token_idx.tolist()
    top_probs = np.exp(vocab_logits[top_token_idx])
    top_probs = (top_probs / np.sum(top_probs)).tolist()
    
    inference_time = time.time() - start_time
    
    return {
        "top_tokens": top_tokens,
        "top_probs": top_probs,
        "merged_latent": merged_latent,
        "forward_scores": forward_scores.tolist(),
        "backward_scores": backward_scores.tolist(),
        "inference_time": inference_time,
        "metadata": {
            "n_candidates": n_candidates,
            "latent_dim": latent_dim,
            "diffusion_steps": diffusion_steps,
            "coherence_weight": coherence_weight,
            "temperature": temperature
        }
    }


def _project_to_vocab(
    latent: np.ndarray, 
    vocab_size: int, 
    temperature: float = 1.0
) -> np.ndarray:
    """
    Project latent representation to vocabulary logits.
    
    Args:
        latent: Merged latent representation
        vocab_size: Size of vocabulary
        temperature: Sampling temperature
        
    Returns:
        Vocabulary logits array
    """
    # Simple linear projection (in practice, this would be a learned decoder)
    projection_matrix = np.random.randn(len(latent), vocab_size) * 0.1
    logits = np.dot(latent, projection_matrix)
    
    # Apply temperature scaling
    logits = logits / temperature
    
    # Apply softmax normalization
    exp_logits = np.exp(logits - np.max(logits))  # Numerical stability
    return np.log(exp_logits / np.sum(exp_logits))


def batch_qdllm_infer(
    batch_inputs: List[Dict[str, Any]],
    max_workers: int = 4
) -> List[Dict[str, Any]]:
    """
    Batch inference for multiple qdLLM requests.
    
    Args:
        batch_inputs: List of inference parameter dictionaries
        max_workers: Maximum number of parallel workers
        
    Returns:
        List of inference results
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(qdllm_infer, **inputs) for inputs in batch_inputs]
        results = [future.result() for future in futures]
    
    return results