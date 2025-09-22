"""NQBA Integration Layer

This module provides system integration capabilities for connecting NQBA
with external systems, APIs, legacy systems, IoT devices, and other
business infrastructure components.

Key Components:
- Connectors: System-specific integration connectors
- Adapters: Protocol and format adapters
- Bridges: Legacy system bridges
- Gateways: API and service gateways
"""

# Placeholder imports - to be implemented
try:
    from .connectors import SystemConnectors, DatabaseConnector, APIConnector
    from .adapters import ProtocolAdapters, DataFormatAdapters
    from .bridges import LegacyBridges, MainframeBridge
    from .gateways import ServiceGateways, APIGateway
except ImportError:
    # Graceful fallback during development
    SystemConnectors = None
    DatabaseConnector = None
    APIConnector = None
    ProtocolAdapters = None
    DataFormatAdapters = None
    LegacyBridges = None
    MainframeBridge = None
    ServiceGateways = None
    APIGateway = None

__all__ = [
    "SystemConnectors",
    "DatabaseConnector",
    "APIConnector",
    "ProtocolAdapters",
    "DataFormatAdapters",
    "LegacyBridges",
    "MainframeBridge",
    "ServiceGateways",
    "APIGateway"
]

# Module metadata
__version__ = "1.0.0"
__description__ = "NQBA System Integration and Connectivity"

# Quick access functions
def connect_to_system(system_type, connection_params, **kwargs):
    """Connect to an external system"""
    if SystemConnectors is None:
        raise RuntimeError("System connectors not available")
    connectors = SystemConnectors()
    return connectors.connect(system_type, connection_params, **kwargs)

def create_api_connector(base_url, auth_config=None, **kwargs):
    """Create an API connector instance"""
    if APIConnector is None:
        raise RuntimeError("API connector not available")
    return APIConnector(base_url, auth_config, **kwargs)

def get_available_connectors():
    """Get list of available system connectors"""
    if SystemConnectors is None:
        return []
    return SystemConnectors.list_connectors()

# Placeholder connector definitions
connectors = {
    'database': {
        'types': ['postgresql', 'mysql', 'mongodb', 'redis'],
        'description': 'Database connectivity for NQBA data operations',
        'implemented': False
    },
    'api': {
        'types': ['rest', 'graphql', 'soap', 'grpc'],
        'description': 'API connectivity for external service integration',
        'implemented': False
    },
    'messaging': {
        'types': ['kafka', 'rabbitmq', 'azure_servicebus', 'aws_sqs'],
        'description': 'Message queue and event streaming integration',
        'implemented': False
    },
    'cloud': {
        'types': ['aws', 'azure', 'gcp', 'kubernetes'],
        'description': 'Cloud platform and container orchestration',
        'implemented': False
    },
    'iot': {
        'types': ['mqtt', 'coap', 'lorawan', 'zigbee'],
        'description': 'IoT device and sensor network connectivity',
        'implemented': False
    }
}