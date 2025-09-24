"""
Goliath of All Trade - AIPRM Integration Package
This package provides integration with AIPRM for AI prompt management and extensions.
"""

from .client import AIPRMClient
from .models import (
    PromptTemplate, 
    AIExtension,
    PromptCategory,
    PromptCollection
)

__all__ = [
    'AIPRMClient',
    'PromptTemplate',
    'AIExtension',
    'PromptCategory',
    'PromptCollection'
]