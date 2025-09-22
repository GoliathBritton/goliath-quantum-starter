"""qdLLM Worker Service

Quantum-enhanced Language Model worker service for parallel exploration,
reversal reasoning, and quantum-optimized conversation generation.
"""

from .worker import QdLLMWorker
from .models import (
    QdLLMRequest,
    QdLLMResponse,
    ExplorationResult,
    ReasoningResult,
    RankingResult
)
from .config import QdLLMConfig

__version__ = "1.0.0"
__all__ = [
    "QdLLMWorker",
    "QdLLMRequest",
    "QdLLMResponse", 
    "ExplorationResult",
    "ReasoningResult",
    "RankingResult",
    "QdLLMConfig"
]