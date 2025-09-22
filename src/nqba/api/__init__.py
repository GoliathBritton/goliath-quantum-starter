"""NQBA API Layer - FastAPI server for Neuromorphic Quantum Business Architecture

This module provides a comprehensive REST API for interacting with the NQBA
framework, including the intelligence modules (qdLLM, QNLP, QTransformers),
business workflows, governance, and integration capabilities.

The API serves as the primary interface for external applications to leverage
NQBA's quantum-inspired business intelligence and automation capabilities.
"""

__version__ = "1.0.0"
__author__ = "NQBA Development Team"
__description__ = "NQBA API Server and Endpoints"

# Import main API components (Legacy qdLLM API)
from .server import app, qdllm_api
from .models import *
from .routes import *
from .middleware import *
from .utils import *

# NQBA Framework API Components (New)
try:
    from .nqba_server import NQBAServer, create_nqba_server
    from .nqba_endpoints import NQBAEndpoints, IntelligenceEndpoints
    from .nqba_middleware import NQBAMiddleware, AuthenticationMiddleware
except ImportError:
    # Graceful fallback during development
    NQBAServer = None
    create_nqba_server = None
    NQBAEndpoints = None
    IntelligenceEndpoints = None
    NQBAMiddleware = None
    AuthenticationMiddleware = None

__all__ = [
    # Legacy qdLLM API
    'app',
    'qdllm_api',
    'InferenceRequest',
    'InferenceResponse',
    'QNLPRequest',
    'QNLPResponse',
    'QTransformerRequest',
    'QTransformerResponse',
    'HealthResponse',
    'ModelInfoResponse',
    # NQBA Framework API
    'NQBAServer',
    'create_nqba_server',
    'NQBAEndpoints',
    'IntelligenceEndpoints',
    'NQBAMiddleware',
    'AuthenticationMiddleware'
]

# NQBA API Integration Functions
def start_nqba_server(host="localhost", port=8000, **kwargs):
    """Start NQBA API server"""
    if create_nqba_server is None:
        raise RuntimeError("NQBA server not available")
    server = create_nqba_server(host=host, port=port, **kwargs)
    return server.start()

def create_api_server(**config):
    """Create NQBA API server instance"""
    if NQBAServer is None:
        raise RuntimeError("NQBA server not available")
    return NQBAServer(**config)

def get_available_endpoints():
    """Get list of available API endpoints"""
    if NQBAEndpoints is None:
        return []
    return NQBAEndpoints.list_endpoints()

# Server configuration
server_config = {
    'default_host': 'localhost',
    'default_port': 8000,
    'cors_enabled': True,
    'rate_limiting': True,
    'authentication_required': True,
    'api_version': 'v1',
    'documentation_enabled': True
}