"""QTransformers Utilities - Helper functions and metrics for quantum transformers

This module provides utility functions, metrics, and helper classes
for working with quantum-enhanced transformer models.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
import logging
import time
from datetime import datetime
import json

logger = logging.getLogger(__name__)

@dataclass
class QTransformerMetrics:
    """Metrics for QTransformer model performance"""
    inference_time: float = 0.0
    tokens_per_second: float = 0.0
    memory_usage: float = 0.0
    quantum_coherence_score: float = 0.0
    attention_entropy: float = 0.0
    model_perplexity: float = 0.0
    quantum_entanglement_measure: float = 0.0
    layer_wise_performance: List[float] = None
    
    def __post_init__(self):
        if self.layer_wise_performance is None:
            self.layer_wise_performance = []

class QTransformerUtils:
    """Utility functions for QTransformer models"""
    
    @staticmethod
    def compute_attention_entropy(attention_weights: np.ndarray) -> float:
        """Compute entropy of attention weights
        
        Args:
            attention_weights: Attention weight matrix
            
        Returns:
            Average attention entropy
        """
        # Add small epsilon to avoid log(0)
        epsilon = 1e-8
        attention_weights = attention_weights + epsilon
        
        # Compute entropy for each attention head and position
        entropy = -np.sum(attention_weights * np.log(attention_weights), axis=-1)
        
        # Return average entropy
        return np.mean(entropy)
    
    @staticmethod
    def compute_quantum_coherence(hidden_states: np.ndarray) -> float:
        """Compute quantum coherence measure for hidden states
        
        Args:
            hidden_states: Hidden state tensor
            
        Returns:
            Quantum coherence score
        """
        # Compute density matrix (simplified)
        batch_size, seq_len, hidden_dim = hidden_states.shape
        
        # Flatten for coherence computation
        flattened_states = hidden_states.reshape(-1, hidden_dim)
        
        # Compute covariance matrix as proxy for density matrix
        covariance = np.cov(flattened_states.T)
        
        # Compute eigenvalues
        eigenvalues = np.linalg.eigvals(covariance)
        eigenvalues = np.real(eigenvalues)  # Take real part
        eigenvalues = eigenvalues[eigenvalues > 0]  # Filter positive eigenvalues
        
        # Normalize eigenvalues
        eigenvalues = eigenvalues / np.sum(eigenvalues)
        
        # Compute von Neumann entropy as coherence measure
        coherence = -np.sum(eigenvalues * np.log(eigenvalues + 1e-8))
        
        # Normalize to [0, 1] range
        max_coherence = np.log(len(eigenvalues))
        normalized_coherence = coherence / max_coherence if max_coherence > 0 else 0.0
        
        return normalized_coherence
    
    @staticmethod
    def compute_quantum_entanglement(attention_weights: np.ndarray) -> float:
        """Compute quantum entanglement measure from attention patterns
        
        Args:
            attention_weights: Attention weight matrix
            
        Returns:
            Entanglement measure
        """
        batch_size, num_heads, seq_len, seq_len = attention_weights.shape
        
        entanglement_scores = []
        
        for batch_idx in range(batch_size):
            for head_idx in range(num_heads):
                attention_matrix = attention_weights[batch_idx, head_idx]
                
                # Compute mutual information as entanglement proxy
                # Treat attention as joint probability distribution
                joint_prob = attention_matrix / np.sum(attention_matrix)
                
                # Marginal probabilities
                marginal_i = np.sum(joint_prob, axis=1)
                marginal_j = np.sum(joint_prob, axis=0)
                
                # Compute mutual information
                mutual_info = 0.0
                for i in range(seq_len):
                    for j in range(seq_len):
                        if joint_prob[i, j] > 0 and marginal_i[i] > 0 and marginal_j[j] > 0:
                            mutual_info += joint_prob[i, j] * np.log(
                                joint_prob[i, j] / (marginal_i[i] * marginal_j[j])
                            )
                
                entanglement_scores.append(mutual_info)
        
        return np.mean(entanglement_scores)
    
    @staticmethod
    def compute_model_perplexity(logits: np.ndarray, target_ids: np.ndarray) -> float:
        """Compute model perplexity
        
        Args:
            logits: Model logits
            target_ids: Target token IDs
            
        Returns:
            Perplexity score
        """
        # Compute softmax probabilities
        exp_logits = np.exp(logits - np.max(logits, axis=-1, keepdims=True))
        probabilities = exp_logits / np.sum(exp_logits, axis=-1, keepdims=True)
        
        # Compute cross-entropy loss
        batch_size, seq_len = target_ids.shape
        total_loss = 0.0
        total_tokens = 0
        
        for batch_idx in range(batch_size):
            for seq_idx in range(seq_len):
                target_id = target_ids[batch_idx, seq_idx]
                if target_id > 0:  # Ignore padding tokens
                    prob = probabilities[batch_idx, seq_idx, target_id]
                    total_loss += -np.log(prob + 1e-8)
                    total_tokens += 1
        
        # Compute average loss and perplexity
        avg_loss = total_loss / total_tokens if total_tokens > 0 else 0.0
        perplexity = np.exp(avg_loss)
        
        return perplexity
    
    @staticmethod
    def analyze_layer_performance(block_infos: List[Dict[str, Any]]) -> List[float]:
        """Analyze performance of individual transformer layers
        
        Args:
            block_infos: Information from transformer blocks
            
        Returns:
            List of performance scores for each layer
        """
        layer_scores = []
        
        for layer_idx, block_info in enumerate(block_infos):
            # Extract attention information
            attention_info = block_info.get('attention_info', {})
            
            # Compute layer-specific metrics
            layer_score = 0.0
            
            # Attention entropy contribution
            if 'attention_weights' in attention_info:
                attention_weights = attention_info['attention_weights']
                entropy = QTransformerUtils.compute_attention_entropy(attention_weights)
                layer_score += entropy * 0.3
            
            # Quantum enhancement contribution
            if block_info.get('quantum_enhancement_applied', False):
                layer_score += 0.2
            
            # Residual connection contribution
            if block_info.get('residual_connections', False):
                layer_score += 0.1
            
            # Normalization contribution
            if block_info.get('pre_normalization', False):
                layer_score += 0.1
            
            layer_scores.append(layer_score)
        
        return layer_scores
    
    @staticmethod
    def estimate_memory_usage(model_config) -> float:
        """Estimate memory usage of the model
        
        Args:
            model_config: Model configuration
            
        Returns:
            Estimated memory usage in MB
        """
        # Estimate parameter count
        embedding_params = model_config.vocab_size * model_config.hidden_dim
        
        # Transformer parameters per layer
        attention_params = 4 * model_config.hidden_dim * model_config.hidden_dim
        ff_params = 2 * model_config.hidden_dim * model_config.ff_dim
        layer_norm_params = 4 * model_config.hidden_dim
        
        layer_params = attention_params + ff_params + layer_norm_params
        total_transformer_params = layer_params * model_config.num_layers
        
        output_head_params = model_config.hidden_dim * model_config.vocab_size
        
        total_params = embedding_params + total_transformer_params + output_head_params
        
        # Estimate memory usage (parameters + activations + gradients)
        # Assuming float32 (4 bytes per parameter)
        param_memory = total_params * 4
        
        # Estimate activation memory (rough approximation)
        batch_size = 1  # Assume single batch for estimation
        seq_length = model_config.max_seq_length
        activation_memory = (
            batch_size * seq_length * model_config.hidden_dim * 
            model_config.num_layers * 4  # 4 bytes per float
        )
        
        # Total memory in bytes, convert to MB
        total_memory_mb = (param_memory + activation_memory) / (1024 * 1024)
        
        return total_memory_mb
    
    @staticmethod
    def benchmark_inference_speed(model, test_inputs: List[str], 
                                num_runs: int = 5) -> Dict[str, float]:
        """Benchmark model inference speed
        
        Args:
            model: QTransformer model instance
            test_inputs: List of test input strings
            num_runs: Number of benchmark runs
            
        Returns:
            Dictionary with benchmark results
        """
        inference_times = []
        total_tokens = 0
        
        for run in range(num_runs):
            start_time = time.time()
            
            for test_input in test_inputs:
                # Tokenize to count tokens
                tokens = model.tokenizer.tokenize(test_input)
                total_tokens += len(tokens)
                
                # Run inference
                _ = model.forward(test_input)
            
            end_time = time.time()
            inference_times.append(end_time - start_time)
        
        # Compute statistics
        avg_inference_time = np.mean(inference_times)
        std_inference_time = np.std(inference_times)
        tokens_per_second = total_tokens / (avg_inference_time * num_runs)
        
        return {
            'avg_inference_time': avg_inference_time,
            'std_inference_time': std_inference_time,
            'tokens_per_second': tokens_per_second,
            'total_tokens_processed': total_tokens,
            'num_runs': num_runs
        }
    
    @staticmethod
    def validate_model_output(output: Dict[str, Any]) -> bool:
        """Validate model output format and content
        
        Args:
            output: Model output dictionary
            
        Returns:
            True if output is valid, False otherwise
        """
        required_keys = ['logits', 'probabilities', 'hidden_states']
        
        # Check required keys
        for key in required_keys:
            if key not in output:
                logger.error(f"Missing required key in model output: {key}")
                return False
        
        # Check tensor shapes and properties
        logits = output['logits']
        probabilities = output['probabilities']
        hidden_states = output['hidden_states']
        
        # Check if probabilities sum to 1 (approximately)
        prob_sums = np.sum(probabilities, axis=-1)
        if not np.allclose(prob_sums, 1.0, atol=1e-6):
            logger.error("Probabilities do not sum to 1")
            return False
        
        # Check for NaN or infinite values
        for key, tensor in [('logits', logits), ('probabilities', probabilities), 
                           ('hidden_states', hidden_states)]:
            if np.any(np.isnan(tensor)) or np.any(np.isinf(tensor)):
                logger.error(f"Found NaN or infinite values in {key}")
                return False
        
        # Check shape consistency
        if logits.shape[:-1] != probabilities.shape[:-1]:
            logger.error("Shape mismatch between logits and probabilities")
            return False
        
        return True
    
    @staticmethod
    def create_attention_mask(input_ids: np.ndarray, pad_token_id: int = 0) -> np.ndarray:
        """Create attention mask from input IDs
        
        Args:
            input_ids: Input token IDs
            pad_token_id: ID of padding token
            
        Returns:
            Attention mask
        """
        return (input_ids != pad_token_id).astype(np.float32)
    
    @staticmethod
    def apply_temperature_scaling(logits: np.ndarray, temperature: float) -> np.ndarray:
        """Apply temperature scaling to logits
        
        Args:
            logits: Input logits
            temperature: Temperature parameter
            
        Returns:
            Temperature-scaled logits
        """
        if temperature <= 0:
            raise ValueError("Temperature must be positive")
        
        return logits / temperature
    
    @staticmethod
    def top_k_filtering(logits: np.ndarray, k: int) -> np.ndarray:
        """Apply top-k filtering to logits
        
        Args:
            logits: Input logits
            k: Number of top tokens to keep
            
        Returns:
            Filtered logits
        """
        if k <= 0:
            return logits
        
        # Get top-k indices
        top_k_indices = np.argpartition(logits, -k, axis=-1)[..., -k:]
        
        # Create mask
        mask = np.zeros_like(logits, dtype=bool)
        np.put_along_axis(mask, top_k_indices, True, axis=-1)
        
        # Apply mask
        filtered_logits = np.where(mask, logits, -np.inf)
        
        return filtered_logits
    
    @staticmethod
    def top_p_filtering(logits: np.ndarray, p: float) -> np.ndarray:
        """Apply top-p (nucleus) filtering to logits
        
        Args:
            logits: Input logits
            p: Cumulative probability threshold
            
        Returns:
            Filtered logits
        """
        if p <= 0 or p >= 1:
            return logits
        
        # Sort logits in descending order
        sorted_indices = np.argsort(logits, axis=-1)[..., ::-1]
        sorted_logits = np.take_along_axis(logits, sorted_indices, axis=-1)
        
        # Compute probabilities
        sorted_probs = np.exp(sorted_logits - np.max(sorted_logits, axis=-1, keepdims=True))
        sorted_probs = sorted_probs / np.sum(sorted_probs, axis=-1, keepdims=True)
        
        # Compute cumulative probabilities
        cumulative_probs = np.cumsum(sorted_probs, axis=-1)
        
        # Create mask for tokens to keep
        mask = cumulative_probs <= p
        
        # Ensure at least one token is kept
        mask[..., 0] = True
        
        # Apply mask to sorted logits
        filtered_sorted_logits = np.where(mask, sorted_logits, -np.inf)
        
        # Unsort the logits
        filtered_logits = np.zeros_like(logits)
        np.put_along_axis(filtered_logits, sorted_indices, filtered_sorted_logits, axis=-1)
        
        return filtered_logits

class QTransformerProfiler:
    """Profiler for QTransformer model performance"""
    
    def __init__(self):
        """Initialize profiler"""
        self.start_time = None
        self.end_time = None
        self.metrics = QTransformerMetrics()
        self.layer_timings = []
        
    def start_profiling(self):
        """Start profiling session"""
        self.start_time = time.time()
        self.layer_timings = []
        
    def end_profiling(self):
        """End profiling session"""
        self.end_time = time.time()
        if self.start_time is not None:
            self.metrics.inference_time = self.end_time - self.start_time
    
    def profile_layer(self, layer_idx: int, layer_output: Dict[str, Any]):
        """Profile individual layer performance
        
        Args:
            layer_idx: Index of the layer
            layer_output: Output from the layer
        """
        layer_start = time.time()
        
        # Simulate layer processing time
        # In a real implementation, this would measure actual computation time
        processing_time = 0.001  # Placeholder
        
        layer_end = time.time()
        
        self.layer_timings.append({
            'layer_idx': layer_idx,
            'processing_time': processing_time,
            'timestamp': layer_end
        })
    
    def compute_comprehensive_metrics(self, model_output: Dict[str, Any], 
                                    num_tokens: int) -> QTransformerMetrics:
        """Compute comprehensive performance metrics
        
        Args:
            model_output: Output from the model
            num_tokens: Number of tokens processed
            
        Returns:
            Comprehensive metrics
        """
        # Update basic metrics
        if self.metrics.inference_time > 0:
            self.metrics.tokens_per_second = num_tokens / self.metrics.inference_time
        
        # Compute quantum-specific metrics
        if 'hidden_states' in model_output:
            self.metrics.quantum_coherence_score = QTransformerUtils.compute_quantum_coherence(
                model_output['hidden_states']
            )
        
        if 'attention_info' in model_output:
            attention_infos = model_output['attention_info']
            if attention_infos and 'attention_weights' in attention_infos[0].get('attention_info', {}):
                attention_weights = attention_infos[0]['attention_info']['attention_weights']
                self.metrics.attention_entropy = QTransformerUtils.compute_attention_entropy(
                    attention_weights
                )
                self.metrics.quantum_entanglement_measure = QTransformerUtils.compute_quantum_entanglement(
                    attention_weights
                )
        
        # Compute layer-wise performance
        if 'attention_info' in model_output:
            self.metrics.layer_wise_performance = QTransformerUtils.analyze_layer_performance(
                model_output['attention_info']
            )
        
        return self.metrics
    
    def get_profiling_report(self) -> Dict[str, Any]:
        """Get comprehensive profiling report
        
        Returns:
            Profiling report dictionary
        """
        return {
            'profiling_session': {
                'start_time': self.start_time,
                'end_time': self.end_time,
                'total_duration': self.metrics.inference_time
            },
            'performance_metrics': {
                'inference_time': self.metrics.inference_time,
                'tokens_per_second': self.metrics.tokens_per_second,
                'memory_usage': self.metrics.memory_usage,
                'model_perplexity': self.metrics.model_perplexity
            },
            'quantum_metrics': {
                'quantum_coherence_score': self.metrics.quantum_coherence_score,
                'attention_entropy': self.metrics.attention_entropy,
                'quantum_entanglement_measure': self.metrics.quantum_entanglement_measure
            },
            'layer_analysis': {
                'layer_wise_performance': self.metrics.layer_wise_performance,
                'layer_timings': self.layer_timings
            },
            'report_timestamp': datetime.now().isoformat()
        }
    
    def save_report(self, filepath: str):
        """Save profiling report to file
        
        Args:
            filepath: Path to save the report
        """
        report = self.get_profiling_report()
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            logger.info(f"Profiling report saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save profiling report: {e}")