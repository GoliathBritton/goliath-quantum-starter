"""NQBA Intelligence Modules

This package contains the core computational intelligence components of NQBA:
- qdLLM: Quantum-inspired Large Language Model engine
- QNLP: Quantum Natural Language Processing
- QTransformers: Quantum-enhanced transformer architectures

These modules work together to provide the foundational AI capabilities
for the Neuromorphic Quantum Business Architecture framework.
"""

# Import intelligence modules
try:
    from . import qdllm
    from . import qnlp
    from . import qtransformers
except ImportError as e:
    # Graceful fallback during development
    import warnings
    warnings.warn(f"Some intelligence modules could not be imported: {e}")
    qdllm = None
    qnlp = None
    qtransformers = None

__all__ = [
    "qdllm",
    "qnlp",
    "qtransformers"
]

# Intelligence module registry
INTELLIGENCE_MODULES = {
    'qdllm': qdllm,
    'qnlp': qnlp,
    'qtransformers': qtransformers
}

def get_available_modules():
    """Get list of available intelligence modules"""
    return {name: module for name, module in INTELLIGENCE_MODULES.items() if module is not None}

def get_module(name):
    """Get a specific intelligence module by name"""
    if name not in INTELLIGENCE_MODULES:
        raise ValueError(f"Unknown intelligence module: {name}")
    module = INTELLIGENCE_MODULES[name]
    if module is None:
        raise ImportError(f"Intelligence module '{name}' is not available")
    return module