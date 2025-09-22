"""Quantum Transformer Blocks - Core building blocks for QTransformers

This module implements quantum-enhanced transformer blocks that combine
quantum attention mechanisms with quantum-inspired feed-forward networks
and normalization layers.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
from scipy.special import softmax

from .attention import QuantumMultiHeadAttention, AttentionConfig

logger = logging.getLogger(__name__)

@dataclass
class BlockConfig:
    """Configuration for quantum transformer blocks"""
    hidden_dim: int = 512
    num_heads: int = 8
    head_dim: int = 64
    ff_dim: int = 2048
    dropout_rate: float = 0.1
    layer_norm_eps: float = 1e-6
    quantum_enhancement: bool = True
    quantum_ff_layers: int = 2
    activation_function: str = 'gelu'
    residual_connection: bool = True
    pre_norm: bool = True
    quantum_gate_noise: float = 0.01
    entanglement_strength: float = 0.5
    coherence_preservation: float = 0.8

class QuantumLayerNorm:
    """Quantum-enhanced layer normalization"""
    
    def __init__(self, hidden_dim: int, eps: float = 1e-6, quantum_enhancement: bool = True):
        """Initialize quantum layer normalization
        
        Args:
            hidden_dim: Hidden dimension size
            eps: Small epsilon for numerical stability
            quantum_enhancement: Whether to apply quantum enhancements
        """
        self.hidden_dim = hidden_dim
        self.eps = eps
        self.quantum_enhancement = quantum_enhancement
        
        # Initialize learnable parameters (simulated)
        self.gamma = np.ones(hidden_dim)
        self.beta = np.zeros(hidden_dim)
        
        # Quantum enhancement parameters
        if quantum_enhancement:
            self.quantum_phase_shifts = np.random.uniform(0, 2*np.pi, hidden_dim)
            self.quantum_amplitude_factors = np.ones(hidden_dim)
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Apply quantum layer normalization
        
        Args:
            x: Input tensor
            
        Returns:
            Normalized tensor
        """
        # Standard layer normalization
        mean = np.mean(x, axis=-1, keepdims=True)
        variance = np.var(x, axis=-1, keepdims=True)
        normalized = (x - mean) / np.sqrt(variance + self.eps)
        
        # Apply learnable parameters
        output = self.gamma * normalized + self.beta
        
        # Apply quantum enhancement
        if self.quantum_enhancement:
            output = self._apply_quantum_normalization(output)
        
        return output
    
    def _apply_quantum_normalization(self, x: np.ndarray) -> np.ndarray:
        """Apply quantum-inspired normalization"""
        # Apply quantum phase shifts
        phase_modulated = x * np.cos(self.quantum_phase_shifts) + \
                         np.roll(x, 1, axis=-1) * np.sin(self.quantum_phase_shifts)
        
        # Apply quantum amplitude factors
        amplitude_modulated = phase_modulated * self.quantum_amplitude_factors
        
        # Preserve quantum state normalization
        norms = np.linalg.norm(amplitude_modulated, axis=-1, keepdims=True)
        quantum_normalized = amplitude_modulated / np.maximum(norms, self.eps)
        
        return quantum_normalized

class QuantumFeedForward:
    """Quantum-enhanced feed-forward network"""
    
    def __init__(self, config: BlockConfig):
        """Initialize quantum feed-forward network
        
        Args:
            config: Block configuration
        """
        self.config = config
        
        # Initialize weight matrices (simulated)
        self.w1 = self._initialize_weight_matrix(config.hidden_dim, config.ff_dim)
        self.w2 = self._initialize_weight_matrix(config.ff_dim, config.hidden_dim)
        
        # Quantum enhancement matrices
        if config.quantum_enhancement:
            self.quantum_gates = self._initialize_quantum_gates()
            self.entanglement_matrix = self._initialize_entanglement_matrix()
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass of quantum feed-forward network
        
        Args:
            x: Input tensor
            
        Returns:
            Output tensor
        """
        # Apply quantum preprocessing if enabled
        if self.config.quantum_enhancement:
            x = self._apply_quantum_preprocessing(x)
        
        # First linear transformation
        hidden = np.dot(x, self.w1)
        
        # Apply activation function
        hidden = self._apply_activation(hidden)
        
        # Apply quantum gates between layers if enabled
        if self.config.quantum_enhancement:
            hidden = self._apply_quantum_gates(hidden)
        
        # Apply dropout (simulated)
        if self.config.dropout_rate > 0:
            hidden = self._apply_dropout(hidden)
        
        # Second linear transformation
        output = np.dot(hidden, self.w2)
        
        # Apply quantum postprocessing if enabled
        if self.config.quantum_enhancement:
            output = self._apply_quantum_postprocessing(output)
        
        return output
    
    def _initialize_weight_matrix(self, input_dim: int, output_dim: int) -> np.ndarray:
        """Initialize weight matrix with Xavier initialization"""
        return np.random.randn(input_dim, output_dim) * np.sqrt(2.0 / (input_dim + output_dim))
    
    def _initialize_quantum_gates(self) -> List[np.ndarray]:
        """Initialize quantum gate matrices"""
        gates = []
        
        for layer in range(self.config.quantum_ff_layers):
            dim = self.config.ff_dim
            
            # Create rotation gate
            angles = np.random.uniform(0, 2*np.pi, dim)
            rotation_gate = np.diag(np.exp(1j * angles)).real
            
            # Add some off-diagonal elements for entanglement
            for i in range(dim - 1):
                rotation_gate[i, i+1] = self.config.entanglement_strength * np.sin(angles[i])
                rotation_gate[i+1, i] = self.config.entanglement_strength * np.cos(angles[i])
            
            gates.append(rotation_gate)
        
        return gates
    
    def _initialize_entanglement_matrix(self) -> np.ndarray:
        """Initialize entanglement matrix"""
        dim = self.config.hidden_dim
        
        # Create entanglement matrix with controlled entanglement
        entanglement = np.eye(dim)
        
        # Add nearest-neighbor entanglement
        for i in range(dim - 1):
            entanglement[i, i+1] = self.config.entanglement_strength
            entanglement[i+1, i] = self.config.entanglement_strength
        
        # Add long-range entanglement (sparse)
        for i in range(0, dim, 4):
            for j in range(i+2, min(i+6, dim)):
                entanglement[i, j] = self.config.entanglement_strength * 0.5
                entanglement[j, i] = self.config.entanglement_strength * 0.5
        
        return entanglement
    
    def _apply_quantum_preprocessing(self, x: np.ndarray) -> np.ndarray:
        """Apply quantum preprocessing to input"""
        # Apply entanglement transformation
        entangled = np.dot(x, self.entanglement_matrix)
        
        # Add quantum noise
        noise = np.random.randn(*x.shape) * self.config.quantum_gate_noise
        quantum_input = entangled + noise
        
        return quantum_input
    
    def _apply_activation(self, x: np.ndarray) -> np.ndarray:
        """Apply activation function"""
        if self.config.activation_function == 'gelu':
            # GELU activation
            return 0.5 * x * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))
        elif self.config.activation_function == 'relu':
            return np.maximum(0, x)
        elif self.config.activation_function == 'swish':
            return x * (1 / (1 + np.exp(-x)))
        else:
            # Default to GELU
            return 0.5 * x * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)))
    
    def _apply_quantum_gates(self, x: np.ndarray) -> np.ndarray:
        """Apply quantum gates to hidden representation"""
        quantum_hidden = x.copy()
        
        # Apply quantum gates sequentially
        for gate in self.quantum_gates:
            # Ensure gate dimensions match
            if gate.shape[0] == quantum_hidden.shape[-1]:
                # Apply gate to each position in sequence
                for i in range(quantum_hidden.shape[0]):
                    for j in range(quantum_hidden.shape[1]):
                        quantum_hidden[i, j] = np.dot(quantum_hidden[i, j], gate)
        
        return quantum_hidden
    
    def _apply_dropout(self, x: np.ndarray) -> np.ndarray:
        """Apply dropout (simulated)"""
        dropout_mask = np.random.binomial(1, 1 - self.config.dropout_rate, x.shape)
        return x * dropout_mask / (1 - self.config.dropout_rate)
    
    def _apply_quantum_postprocessing(self, x: np.ndarray) -> np.ndarray:
        """Apply quantum postprocessing to output"""
        # Apply coherence preservation
        norms = np.linalg.norm(x, axis=-1, keepdims=True)
        normalized = x / np.maximum(norms, 1e-8)
        
        # Mix normalized and original based on coherence preservation factor
        coherent_output = (self.config.coherence_preservation * normalized + 
                          (1 - self.config.coherence_preservation) * x)
        
        return coherent_output

class QTransformerBlock:
    """Quantum-enhanced transformer block"""
    
    def __init__(self, config: Optional[BlockConfig] = None):
        """Initialize quantum transformer block
        
        Args:
            config: Block configuration
        """
        self.config = config or BlockConfig()
        
        # Initialize attention mechanism
        attention_config = AttentionConfig(
            hidden_dim=self.config.hidden_dim,
            num_heads=self.config.num_heads,
            head_dim=self.config.head_dim,
            dropout_rate=self.config.dropout_rate,
            quantum_enhancement=self.config.quantum_enhancement,
            entanglement_strength=self.config.entanglement_strength,
            coherence_preservation=self.config.coherence_preservation
        )
        self.attention = QuantumMultiHeadAttention(attention_config)
        
        # Initialize feed-forward network
        self.feed_forward = QuantumFeedForward(self.config)
        
        # Initialize layer normalization
        self.layer_norm1 = QuantumLayerNorm(
            self.config.hidden_dim, 
            self.config.layer_norm_eps,
            self.config.quantum_enhancement
        )
        self.layer_norm2 = QuantumLayerNorm(
            self.config.hidden_dim, 
            self.config.layer_norm_eps,
            self.config.quantum_enhancement
        )
        
        logger.info(f"QTransformerBlock initialized with config: {self.config}")
    
    def forward(self, x: np.ndarray, 
               mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """Forward pass of quantum transformer block
        
        Args:
            x: Input tensor [batch_size, seq_len, hidden_dim]
            mask: Optional attention mask
            
        Returns:
            Tuple of (output_tensor, block_info)
        """
        # Store input for residual connection
        residual_input = x.copy()
        
        # Pre-normalization (if enabled)
        if self.config.pre_norm:
            x = self.layer_norm1.forward(x)
        
        # Self-attention
        attention_output, attention_info = self.attention.forward(x, x, x, mask)
        
        # Residual connection and post-normalization for attention
        if self.config.residual_connection:
            attention_output = attention_output + residual_input
        
        if not self.config.pre_norm:
            attention_output = self.layer_norm1.forward(attention_output)
        
        # Store attention output for next residual connection
        residual_attention = attention_output.copy()
        
        # Pre-normalization for feed-forward (if enabled)
        if self.config.pre_norm:
            attention_output = self.layer_norm2.forward(attention_output)
        
        # Feed-forward network
        ff_output = self.feed_forward.forward(attention_output)
        
        # Residual connection and post-normalization for feed-forward
        if self.config.residual_connection:
            ff_output = ff_output + residual_attention
        
        if not self.config.pre_norm:
            ff_output = self.layer_norm2.forward(ff_output)
        
        # Prepare block information
        block_info = {
            'attention_info': attention_info,
            'quantum_enhancement_applied': self.config.quantum_enhancement,
            'residual_connections': self.config.residual_connection,
            'pre_normalization': self.config.pre_norm,
            'block_config': self.config
        }
        
        return ff_output, block_info
    
    def reconfigure(self, new_config: BlockConfig):
        """Reconfigure the transformer block
        
        Args:
            new_config: New block configuration
        """
        self.config = new_config
        
        # Reconfigure attention
        attention_config = AttentionConfig(
            hidden_dim=new_config.hidden_dim,
            num_heads=new_config.num_heads,
            head_dim=new_config.head_dim,
            dropout_rate=new_config.dropout_rate,
            quantum_enhancement=new_config.quantum_enhancement,
            entanglement_strength=new_config.entanglement_strength,
            coherence_preservation=new_config.coherence_preservation
        )
        self.attention.reconfigure(attention_config)
        
        # Reinitialize feed-forward network
        self.feed_forward = QuantumFeedForward(new_config)
        
        # Reinitialize layer normalization
        self.layer_norm1 = QuantumLayerNorm(
            new_config.hidden_dim, 
            new_config.layer_norm_eps,
            new_config.quantum_enhancement
        )
        self.layer_norm2 = QuantumLayerNorm(
            new_config.hidden_dim, 
            new_config.layer_norm_eps,
            new_config.quantum_enhancement
        )
        
        logger.info(f"QTransformerBlock reconfigured with new config: {new_config}")

class QTransformerStack:
    """Stack of quantum transformer blocks"""
    
    def __init__(self, num_layers: int, config: Optional[BlockConfig] = None):
        """Initialize quantum transformer stack
        
        Args:
            num_layers: Number of transformer layers
            config: Block configuration
        """
        self.num_layers = num_layers
        self.config = config or BlockConfig()
        
        # Initialize transformer blocks
        self.blocks = []
        for layer_idx in range(num_layers):
            # Create layer-specific config if needed
            layer_config = self._create_layer_config(layer_idx)
            block = QTransformerBlock(layer_config)
            self.blocks.append(block)
        
        logger.info(f"QTransformerStack initialized with {num_layers} layers")
    
    def forward(self, x: np.ndarray, 
               mask: Optional[np.ndarray] = None) -> Tuple[np.ndarray, List[Dict[str, Any]]]:
        """Forward pass through transformer stack
        
        Args:
            x: Input tensor
            mask: Optional attention mask
            
        Returns:
            Tuple of (output_tensor, list_of_block_info)
        """
        current_input = x
        block_infos = []
        
        # Pass through each transformer block
        for layer_idx, block in enumerate(self.blocks):
            current_input, block_info = block.forward(current_input, mask)
            
            # Add layer index to block info
            block_info['layer_index'] = layer_idx
            block_infos.append(block_info)
        
        return current_input, block_infos
    
    def _create_layer_config(self, layer_idx: int) -> BlockConfig:
        """Create layer-specific configuration
        
        Args:
            layer_idx: Index of the layer
            
        Returns:
            Layer-specific configuration
        """
        # For now, use the same config for all layers
        # In the future, this could be customized per layer
        return self.config
    
    def reconfigure(self, new_config: BlockConfig):
        """Reconfigure all blocks in the stack
        
        Args:
            new_config: New block configuration
        """
        self.config = new_config
        
        # Reconfigure all blocks
        for block in self.blocks:
            block.reconfigure(new_config)
        
        logger.info(f"QTransformerStack reconfigured with new config: {new_config}")
    
    def get_layer_outputs(self, x: np.ndarray, 
                         mask: Optional[np.ndarray] = None) -> List[np.ndarray]:
        """Get outputs from all layers
        
        Args:
            x: Input tensor
            mask: Optional attention mask
            
        Returns:
            List of outputs from each layer
        """
        current_input = x
        layer_outputs = []
        
        # Collect output from each layer
        for block in self.blocks:
            current_input, _ = block.forward(current_input, mask)
            layer_outputs.append(current_input.copy())
        
        return layer_outputs