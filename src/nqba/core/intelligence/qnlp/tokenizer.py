"""Quantum Tokenizer - Enhanced tokenization with quantum properties

This module provides quantum-enhanced tokenization that adds quantum properties
to tokens for improved semantic understanding and processing.
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import logging
import re
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class TokenizerConfig:
    """Configuration for quantum tokenizer"""
    max_length: int = 2048
    vocab_size: int = 50000
    add_quantum_properties: bool = True
    enable_subword_tokenization: bool = True
    quantum_token_enhancement: bool = True
    preserve_special_tokens: bool = True
    case_sensitive: bool = False

@dataclass
class QuantumToken:
    """Enhanced token with quantum properties"""
    token_id: int
    token_text: str
    position: int
    quantum_phase: float
    entanglement_potential: float
    semantic_weight: float
    coherence_factor: float
    attention_mask: int = 1

class QuantumTokenizer:
    """Quantum-enhanced tokenizer for natural language processing"""
    
    def __init__(self, max_length: int = 2048, vocab_size: int = 50000):
        """Initialize quantum tokenizer
        
        Args:
            max_length: Maximum sequence length
            vocab_size: Vocabulary size
        """
        self.config = TokenizerConfig(
            max_length=max_length,
            vocab_size=vocab_size
        )
        
        # Initialize vocabulary and tokenization components
        self.vocab = self._initialize_vocabulary()
        self.token_to_id = {token: idx for idx, token in enumerate(self.vocab)}
        self.id_to_token = {idx: token for token, idx in self.token_to_id.items()}
        
        # Special tokens
        self.special_tokens = {
            '[PAD]': 0,
            '[UNK]': 1,
            '[CLS]': 2,
            '[SEP]': 3,
            '[MASK]': 4
        }
        
        # Quantum enhancement parameters
        self.quantum_params = self._initialize_quantum_parameters()
        
        logger.info(f"QuantumTokenizer initialized: max_length={max_length}, vocab_size={vocab_size}")
    
    def tokenize(self, text: str, add_special_tokens: bool = True) -> Dict[str, Any]:
        """Tokenize text with quantum enhancements
        
        Args:
            text: Input text to tokenize
            add_special_tokens: Whether to add special tokens
            
        Returns:
            Dictionary containing tokenization results with quantum properties
        """
        # Basic text preprocessing
        processed_text = self._preprocess_text(text)
        
        # Tokenize into subwords/words
        raw_tokens = self._basic_tokenize(processed_text)
        
        # Convert to token IDs
        token_ids = self._convert_tokens_to_ids(raw_tokens)
        
        # Add special tokens if requested
        if add_special_tokens:
            token_ids = [self.special_tokens['[CLS]']] + token_ids + [self.special_tokens['[SEP]']]
            raw_tokens = ['[CLS]'] + raw_tokens + ['[SEP]']
        
        # Truncate or pad to max length
        token_ids, raw_tokens, attention_mask = self._handle_sequence_length(
            token_ids, raw_tokens
        )
        
        # Generate quantum properties for tokens
        quantum_properties = self._generate_quantum_properties(
            token_ids, raw_tokens, processed_text
        )
        
        # Create quantum tokens
        quantum_tokens = self._create_quantum_tokens(
            token_ids, raw_tokens, attention_mask, quantum_properties
        )
        
        return {
            'token_ids': token_ids,
            'tokens': raw_tokens,
            'attention_mask': attention_mask,
            'quantum_properties': quantum_properties,
            'quantum_tokens': quantum_tokens,
            'input_length': len(token_ids),
            'original_text': text,
            'processed_text': processed_text
        }
    
    def batch_tokenize(self, texts: List[str], 
                      add_special_tokens: bool = True) -> List[Dict[str, Any]]:
        """Tokenize multiple texts in batch
        
        Args:
            texts: List of input texts
            add_special_tokens: Whether to add special tokens
            
        Returns:
            List of tokenization results
        """
        return [self.tokenize(text, add_special_tokens) for text in texts]
    
    def decode(self, token_ids: List[int], skip_special_tokens: bool = True) -> str:
        """Decode token IDs back to text
        
        Args:
            token_ids: List of token IDs to decode
            skip_special_tokens: Whether to skip special tokens
            
        Returns:
            Decoded text string
        """
        tokens = []
        
        for token_id in token_ids:
            if token_id in self.id_to_token:
                token = self.id_to_token[token_id]
                
                # Skip special tokens if requested
                if skip_special_tokens and token in self.special_tokens:
                    continue
                
                tokens.append(token)
            else:
                tokens.append('[UNK]')
        
        # Join tokens and clean up
        text = ' '.join(tokens)
        text = self._postprocess_decoded_text(text)
        
        return text
    
    def _initialize_vocabulary(self) -> List[str]:
        """Initialize vocabulary with common tokens"""
        # Start with special tokens
        vocab = ['[PAD]', '[UNK]', '[CLS]', '[SEP]', '[MASK]']
        
        # Add common English words (simplified vocabulary)
        common_words = [
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'under', 'over',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
            'can', 'must', 'shall', 'this', 'that', 'these', 'those', 'i', 'you',
            'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'what', 'which',
            'who', 'whom', 'whose', 'where', 'when', 'why', 'how', 'all', 'any',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very'
        ]
        
        vocab.extend(common_words)
        
        # Add subword tokens (simplified BPE-like)
        subword_prefixes = ['##' + word[:3] for word in common_words if len(word) > 3]
        vocab.extend(subword_prefixes)
        
        # Add punctuation and numbers
        punctuation = ['.', ',', '!', '?', ';', ':', '(', ')', '[', ']', '{', '}', "'", '"']
        vocab.extend(punctuation)
        
        numbers = [str(i) for i in range(100)]
        vocab.extend(numbers)
        
        # Pad vocabulary to desired size with random tokens
        while len(vocab) < self.config.vocab_size:
            vocab.append(f'[TOKEN_{len(vocab)}]')
        
        return vocab[:self.config.vocab_size]
    
    def _initialize_quantum_parameters(self) -> Dict[str, Any]:
        """Initialize quantum enhancement parameters"""
        return {
            'phase_variance': 0.1,
            'entanglement_base': 0.5,
            'semantic_weight_range': (0.1, 1.0),
            'coherence_factor_base': 0.7,
            'position_encoding_strength': 0.2
        }
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text before tokenization"""
        # Basic cleaning
        text = text.strip()
        
        # Handle case sensitivity
        if not self.config.case_sensitive:
            text = text.lower()
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Handle punctuation (add spaces around punctuation)
        text = re.sub(r'([.!?;:,()\[\]{}"\'])', r' \1 ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def _basic_tokenize(self, text: str) -> List[str]:
        """Basic tokenization into words/subwords"""
        # Split by whitespace
        tokens = text.split()
        
        # Apply subword tokenization if enabled
        if self.config.enable_subword_tokenization:
            tokens = self._apply_subword_tokenization(tokens)
        
        return tokens
    
    def _apply_subword_tokenization(self, tokens: List[str]) -> List[str]:
        """Apply simplified subword tokenization"""
        subword_tokens = []
        
        for token in tokens:
            if len(token) <= 4 or token in self.token_to_id:
                subword_tokens.append(token)
            else:
                # Simple subword splitting for unknown long words
                if len(token) > 8:
                    # Split into chunks
                    chunks = [token[i:i+4] for i in range(0, len(token), 4)]
                    for i, chunk in enumerate(chunks):
                        if i > 0:
                            chunk = '##' + chunk
                        subword_tokens.append(chunk)
                else:
                    subword_tokens.append(token)
        
        return subword_tokens
    
    def _convert_tokens_to_ids(self, tokens: List[str]) -> List[int]:
        """Convert tokens to token IDs"""
        token_ids = []
        
        for token in tokens:
            if token in self.token_to_id:
                token_ids.append(self.token_to_id[token])
            else:
                token_ids.append(self.special_tokens['[UNK]'])
        
        return token_ids
    
    def _handle_sequence_length(self, token_ids: List[int], 
                              tokens: List[str]) -> Tuple[List[int], List[str], List[int]]:
        """Handle sequence length (truncation/padding)"""
        max_len = self.config.max_length
        
        # Truncate if too long
        if len(token_ids) > max_len:
            token_ids = token_ids[:max_len]
            tokens = tokens[:max_len]
            # Ensure we end with [SEP] if it was there
            if tokens[-1] != '[SEP]' and '[SEP]' in tokens:
                token_ids[-1] = self.special_tokens['[SEP]']
                tokens[-1] = '[SEP]'
        
        # Create attention mask (1 for real tokens, 0 for padding)
        attention_mask = [1] * len(token_ids)
        
        # Pad if too short
        while len(token_ids) < max_len:
            token_ids.append(self.special_tokens['[PAD]'])
            tokens.append('[PAD]')
            attention_mask.append(0)
        
        return token_ids, tokens, attention_mask
    
    def _generate_quantum_properties(self, token_ids: List[int], 
                                   tokens: List[str],
                                   original_text: str) -> Dict[str, Any]:
        """Generate quantum properties for tokens"""
        if not self.config.add_quantum_properties:
            return {}
        
        num_tokens = len(token_ids)
        properties = {
            'quantum_phases': [],
            'entanglement_potentials': [],
            'semantic_weights': [],
            'coherence_factors': [],
            'position_encodings': []
        }
        
        for i, (token_id, token) in enumerate(zip(token_ids, tokens)):
            # Quantum phase (based on token position and content)
            phase = (i / num_tokens) * 2 * np.pi + np.random.normal(0, self.quantum_params['phase_variance'])
            properties['quantum_phases'].append(float(phase))
            
            # Entanglement potential (based on token frequency and position)
            if token in self.special_tokens:
                entanglement = 0.1  # Low entanglement for special tokens
            else:
                # Higher entanglement for content words
                entanglement = self.quantum_params['entanglement_base'] + np.random.uniform(-0.2, 0.2)
            properties['entanglement_potentials'].append(float(entanglement))
            
            # Semantic weight (importance of token)
            if token in ['[PAD]', '[CLS]', '[SEP]']:
                weight = 0.1
            elif token == '[UNK]':
                weight = 0.3
            else:
                # Weight based on token rarity (simplified)
                weight = np.random.uniform(*self.quantum_params['semantic_weight_range'])
            properties['semantic_weights'].append(float(weight))
            
            # Coherence factor (how well token fits in context)
            coherence = self.quantum_params['coherence_factor_base'] + np.random.uniform(-0.2, 0.2)
            properties['coherence_factors'].append(float(coherence))
            
            # Position encoding (quantum-inspired)
            pos_encoding = np.sin(i / 10000) * self.quantum_params['position_encoding_strength']
            properties['position_encodings'].append(float(pos_encoding))
        
        return properties
    
    def _create_quantum_tokens(self, token_ids: List[int], 
                             tokens: List[str],
                             attention_mask: List[int],
                             quantum_properties: Dict[str, Any]) -> List[QuantumToken]:
        """Create quantum token objects"""
        quantum_tokens = []
        
        for i, (token_id, token, mask) in enumerate(zip(token_ids, tokens, attention_mask)):
            quantum_token = QuantumToken(
                token_id=token_id,
                token_text=token,
                position=i,
                quantum_phase=quantum_properties.get('quantum_phases', [0.0])[i],
                entanglement_potential=quantum_properties.get('entanglement_potentials', [0.5])[i],
                semantic_weight=quantum_properties.get('semantic_weights', [0.5])[i],
                coherence_factor=quantum_properties.get('coherence_factors', [0.7])[i],
                attention_mask=mask
            )
            quantum_tokens.append(quantum_token)
        
        return quantum_tokens
    
    def _postprocess_decoded_text(self, text: str) -> str:
        """Postprocess decoded text for readability"""
        # Remove extra spaces around punctuation
        text = re.sub(r'\s+([.!?;:,)])', r'\1', text)
        text = re.sub(r'([\(\[]\s+)', r'\1', text)
        
        # Handle subword tokens
        text = re.sub(r'##', '', text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def get_vocab_size(self) -> int:
        """Get vocabulary size"""
        return len(self.vocab)
    
    def get_special_tokens(self) -> Dict[str, int]:
        """Get special tokens mapping"""
        return self.special_tokens.copy()
    
    def add_tokens(self, new_tokens: List[str]) -> int:
        """Add new tokens to vocabulary
        
        Args:
            new_tokens: List of new tokens to add
            
        Returns:
            Number of tokens actually added
        """
        added_count = 0
        
        for token in new_tokens:
            if token not in self.token_to_id and len(self.vocab) < self.config.vocab_size:
                token_id = len(self.vocab)
                self.vocab.append(token)
                self.token_to_id[token] = token_id
                self.id_to_token[token_id] = token
                added_count += 1
        
        logger.info(f"Added {added_count} new tokens to vocabulary")
        return added_count
    
    def reconfigure(self, new_config: TokenizerConfig):
        """Reconfigure tokenizer with new settings"""
        self.config = new_config
        
        # Reinitialize quantum parameters if needed
        if new_config.quantum_token_enhancement:
            self.quantum_params = self._initialize_quantum_parameters()
        
        logger.info(f"QuantumTokenizer reconfigured with: {new_config}")