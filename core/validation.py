"""Comprehensive validation utilities for pipeline nodes and data processing."""

import re
from typing import Any, Dict, List, Optional, Union, Callable
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class ValidationError(Exception):
    """Custom validation error with detailed information"""
    def __init__(self, message: str, field: str = None, value: Any = None):
        self.message = message
        self.field = field
        self.value = value
        super().__init__(message)

class ValidationSeverity(Enum):
    """Validation issue severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class ValidationResult:
    """Container for validation results"""
    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.info: List[Dict[str, Any]] = []
    
    def add_issue(self, severity: ValidationSeverity, message: str, field: str = None, value: Any = None):
        """Add a validation issue"""
        issue = {
            'message': message,
            'field': field,
            'value': value,
            'severity': severity.value
        }
        
        if severity == ValidationSeverity.ERROR:
            self.errors.append(issue)
        elif severity == ValidationSeverity.WARNING:
            self.warnings.append(issue)
        else:
            self.info.append(issue)
    
    def is_valid(self) -> bool:
        """Check if validation passed (no errors)"""
        return len(self.errors) == 0
    
    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        return {
            'valid': self.is_valid(),
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'info_count': len(self.info),
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info
        }

class NodeValidator:
    """Base validator for pipeline nodes"""
    
    def __init__(self):
        self.result = ValidationResult()
    
    def validate_required_field(self, data: Dict[str, Any], field: str, field_type: type = None) -> bool:
        """Validate that a required field exists and has correct type"""
        if field not in data:
            self.result.add_issue(
                ValidationSeverity.ERROR,
                f"Required field '{field}' is missing",
                field=field
            )
            return False
        
        if field_type and not isinstance(data[field], field_type):
            self.result.add_issue(
                ValidationSeverity.ERROR,
                f"Field '{field}' must be of type {field_type.__name__}, got {type(data[field]).__name__}",
                field=field,
                value=data[field]
            )
            return False
        
        return True
    
    def validate_optional_field(self, data: Dict[str, Any], field: str, field_type: type, default: Any = None) -> Any:
        """Validate optional field and return value or default"""
        if field not in data:
            return default
        
        if not isinstance(data[field], field_type):
            self.result.add_issue(
                ValidationSeverity.WARNING,
                f"Optional field '{field}' should be of type {field_type.__name__}, got {type(data[field]).__name__}",
                field=field,
                value=data[field]
            )
            return default
        
        return data[field]
    
    def validate_range(self, value: Union[int, float], field: str, min_val: Union[int, float] = None, max_val: Union[int, float] = None) -> bool:
        """Validate that a numeric value is within range"""
        if min_val is not None and value < min_val:
            self.result.add_issue(
                ValidationSeverity.ERROR,
                f"Field '{field}' value {value} is below minimum {min_val}",
                field=field,
                value=value
            )
            return False
        
        if max_val is not None and value > max_val:
            self.result.add_issue(
                ValidationSeverity.ERROR,
                f"Field '{field}' value {value} is above maximum {max_val}",
                field=field,
                value=value
            )
            return False
        
        return True
    
    def validate_enum(self, value: str, field: str, valid_values: List[str]) -> bool:
        """Validate that a value is in allowed enum values"""
        if value not in valid_values:
            self.result.add_issue(
                ValidationSeverity.ERROR,
                f"Field '{field}' value '{value}' is not in allowed values: {valid_values}",
                field=field,
                value=value
            )
            return False
        return True
    
    def validate_string_pattern(self, value: str, field: str, pattern: str, description: str = None) -> bool:
        """Validate string against regex pattern"""
        if not re.match(pattern, value):
            desc = description or f"pattern {pattern}"
            self.result.add_issue(
                ValidationSeverity.ERROR,
                f"Field '{field}' value '{value}' does not match {desc}",
                field=field,
                value=value
            )
            return False
        return True
    
    def validate_list_length(self, value: List[Any], field: str, min_length: int = None, max_length: int = None) -> bool:
        """Validate list length"""
        length = len(value)
        
        if min_length is not None and length < min_length:
            self.result.add_issue(
                ValidationSeverity.ERROR,
                f"Field '{field}' list length {length} is below minimum {min_length}",
                field=field,
                value=length
            )
            return False
        
        if max_length is not None and length > max_length:
            self.result.add_issue(
                ValidationSeverity.ERROR,
                f"Field '{field}' list length {length} is above maximum {max_length}",
                field=field,
                value=length
            )
            return False
        
        return True

class DataSourceValidator(NodeValidator):
    """Validator for data source nodes"""
    
    def validate(self, node_data: Dict[str, Any]) -> ValidationResult:
        """Validate data source node"""
        self.result = ValidationResult()
        
        # Validate required fields
        self.validate_required_field(node_data, 'sourceType', str)
        self.validate_required_field(node_data, 'config', dict)
        
        # Validate source type
        valid_source_types = ['file', 'database', 'api', 'stream', 'manual']
        if 'sourceType' in node_data:
            self.validate_enum(node_data['sourceType'], 'sourceType', valid_source_types)
        
        # Validate config based on source type
        if 'config' in node_data and 'sourceType' in node_data:
            self._validate_source_config(node_data['sourceType'], node_data['config'])
        
        return self.result
    
    def _validate_source_config(self, source_type: str, config: Dict[str, Any]):
        """Validate source-specific configuration"""
        if source_type == 'file':
            self.validate_required_field(config, 'path', str)
            if 'path' in config:
                self.validate_string_pattern(
                    config['path'], 'config.path', 
                    r'^[^<>:"|?*]+$', 'valid file path'
                )
        
        elif source_type == 'database':
            self.validate_required_field(config, 'connection_string', str)
            self.validate_required_field(config, 'query', str)
        
        elif source_type == 'api':
            self.validate_required_field(config, 'url', str)
            if 'url' in config:
                self.validate_string_pattern(
                    config['url'], 'config.url',
                    r'^https?://.+', 'valid HTTP URL'
                )

class QuantumNodeValidator(NodeValidator):
    """Validator for quantum nodes"""
    
    def validate_quantum_gate(self, node_data: Dict[str, Any]) -> ValidationResult:
        """Validate quantum gate node"""
        self.result = ValidationResult()
        
        # Validate gate type
        valid_gate_types = ['hadamard', 'pauli_x', 'pauli_y', 'pauli_z', 'rotation_x', 'rotation_y', 'rotation_z', 'cnot', 'cz']
        gate_type = self.validate_optional_field(node_data, 'gateType', str, 'hadamard')
        if gate_type:
            self.validate_enum(gate_type, 'gateType', valid_gate_types)
        
        # Validate qubits
        qubits = self.validate_optional_field(node_data, 'qubits', int, 1)
        if qubits is not None:
            self.validate_range(qubits, 'qubits', min_val=1, max_val=50)
        
        # Validate parameters for rotation gates
        if gate_type and 'rotation' in gate_type:
            parameters = self.validate_optional_field(node_data, 'parameters', dict, {})
            if parameters and 'theta' not in parameters:
                self.result.add_issue(
                    ValidationSeverity.WARNING,
                    f"Rotation gate '{gate_type}' should have 'theta' parameter",
                    field='parameters.theta'
                )
        
        return self.result
    
    def validate_quantum_circuit(self, node_data: Dict[str, Any]) -> ValidationResult:
        """Validate quantum circuit node"""
        self.result = ValidationResult()
        
        # Validate circuit type
        valid_circuit_types = ['qaoa', 'vqe', 'qft', 'custom']
        circuit_type = self.validate_optional_field(node_data, 'circuitType', str, 'custom')
        if circuit_type:
            self.validate_enum(circuit_type, 'circuitType', valid_circuit_types)
        
        # Validate qubits
        qubits = self.validate_optional_field(node_data, 'qubits', int, 4)
        if qubits is not None:
            self.validate_range(qubits, 'qubits', min_val=1, max_val=100)
        
        # Validate depth
        depth = self.validate_optional_field(node_data, 'depth', int, 1)
        if depth is not None:
            self.validate_range(depth, 'depth', min_val=1, max_val=20)
        
        # Validate gates for custom circuits
        if circuit_type == 'custom':
            gates = self.validate_optional_field(node_data, 'gates', list, [])
            if gates is not None:
                self.validate_list_length(gates, 'gates', min_length=1)
        
        return self.result
    
    def validate_quantum_algorithm(self, node_data: Dict[str, Any]) -> ValidationResult:
        """Validate quantum algorithm node"""
        self.result = ValidationResult()
        
        # Validate algorithm type
        valid_algorithm_types = [
            'portfolio_optimization', 'energy_management', 'risk_assessment',
            'fraud_detection', 'supply_chain', 'drug_discovery'
        ]
        algorithm_type = self.validate_optional_field(node_data, 'algorithmType', str, 'portfolio_optimization')
        if algorithm_type:
            self.validate_enum(algorithm_type, 'algorithmType', valid_algorithm_types)
        
        # Validate category
        valid_categories = ['Optimization', 'Simulation', 'Machine Learning', 'Cryptography']
        category = self.validate_optional_field(node_data, 'category', str, 'Optimization')
        if category:
            self.validate_enum(category, 'category', valid_categories)
        
        # Validate parameters
        parameters = self.validate_optional_field(node_data, 'parameters', dict, {})
        if parameters:
            self._validate_algorithm_parameters(algorithm_type, parameters)
        
        return self.result
    
    def _validate_algorithm_parameters(self, algorithm_type: str, parameters: Dict[str, Any]):
        """Validate algorithm-specific parameters"""
        if algorithm_type == 'portfolio_optimization':
            if 'risk_tolerance' in parameters:
                risk_tolerance = parameters['risk_tolerance']
                if isinstance(risk_tolerance, (int, float)):
                    self.validate_range(risk_tolerance, 'parameters.risk_tolerance', min_val=0.0, max_val=1.0)
        
        elif algorithm_type == 'energy_management':
            if 'time_horizon' in parameters:
                time_horizon = parameters['time_horizon']
                if isinstance(time_horizon, int):
                    self.validate_range(time_horizon, 'parameters.time_horizon', min_val=1, max_val=168)  # 1 week max

class PipelineValidator:
    """Validator for entire pipeline structure"""
    
    def __init__(self):
        self.data_source_validator = DataSourceValidator()
        self.quantum_validator = QuantumNodeValidator()
    
    def validate_pipeline(self, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> ValidationResult:
        """Validate entire pipeline"""
        result = ValidationResult()
        
        # Basic pipeline structure validation
        if not nodes:
            result.add_issue(ValidationSeverity.ERROR, "Pipeline must contain at least one node")
            return result
        
        # Check for required node types
        node_types = [node.get('type') for node in nodes]
        if 'dataSource' not in node_types:
            result.add_issue(ValidationSeverity.ERROR, "Pipeline must have at least one data source")
        
        if 'output' not in node_types:
            result.add_issue(ValidationSeverity.ERROR, "Pipeline must have at least one output node")
        
        # Validate node connections
        node_ids = {node.get('id') for node in nodes if node.get('id')}
        connected_nodes = set()
        
        for edge in edges:
            source = edge.get('source')
            target = edge.get('target')
            
            if source not in node_ids:
                result.add_issue(
                    ValidationSeverity.ERROR,
                    f"Edge references unknown source node: {source}",
                    field='edges.source',
                    value=source
                )
            
            if target not in node_ids:
                result.add_issue(
                    ValidationSeverity.ERROR,
                    f"Edge references unknown target node: {target}",
                    field='edges.target',
                    value=target
                )
            
            connected_nodes.add(source)
            connected_nodes.add(target)
        
        # Check for disconnected nodes
        if len(nodes) > 1:
            disconnected_nodes = [node.get('id') for node in nodes if node.get('id') not in connected_nodes]
            if disconnected_nodes:
                result.add_issue(
                    ValidationSeverity.WARNING,
                    f"{len(disconnected_nodes)} node(s) are not connected to the pipeline: {disconnected_nodes}",
                    field='pipeline.connectivity'
                )
        
        # Validate individual nodes
        for node in nodes:
            node_result = self.validate_node(node)
            # Merge results
            result.errors.extend(node_result.errors)
            result.warnings.extend(node_result.warnings)
            result.info.extend(node_result.info)
        
        return result
    
    def validate_node(self, node: Dict[str, Any]) -> ValidationResult:
        """Validate individual node"""
        result = ValidationResult()
        
        # Validate basic node structure
        if 'id' not in node:
            result.add_issue(ValidationSeverity.ERROR, "Node must have an 'id' field")
        
        if 'type' not in node:
            result.add_issue(ValidationSeverity.ERROR, "Node must have a 'type' field")
            return result
        
        node_type = node['type']
        node_data = node.get('data', {})
        
        # Validate based on node type
        if node_type == 'dataSource':
            node_result = self.data_source_validator.validate(node_data)
        elif node_type == 'quantumGate':
            node_result = self.quantum_validator.validate_quantum_gate(node_data)
        elif node_type == 'quantumCircuit':
            node_result = self.quantum_validator.validate_quantum_circuit(node_data)
        elif node_type == 'quantumAlgorithm':
            node_result = self.quantum_validator.validate_quantum_algorithm(node_data)
        else:
            # For other node types, just validate basic structure
            node_result = ValidationResult()
            if not node_data:
                node_result.add_issue(
                    ValidationSeverity.WARNING,
                    f"Node of type '{node_type}' has no configuration data",
                    field='data'
                )
        
        # Add node context to validation issues
        node_id = node.get('id', 'unknown')
        for issue in node_result.errors + node_result.warnings + node_result.info:
            if issue['field']:
                issue['field'] = f"node[{node_id}].{issue['field']}"
            else:
                issue['field'] = f"node[{node_id}]"
        
        result.errors.extend(node_result.errors)
        result.warnings.extend(node_result.warnings)
        result.info.extend(node_result.info)
        
        return result

# Convenience functions
def validate_pipeline(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> ValidationResult:
    """Convenience function to validate a pipeline"""
    validator = PipelineValidator()
    return validator.validate_pipeline(nodes, edges)

def validate_node_data(node_type: str, node_data: Dict[str, Any]) -> ValidationResult:
    """Convenience function to validate node data"""
    validator = PipelineValidator()
    node = {'id': 'temp', 'type': node_type, 'data': node_data}
    return validator.validate_node(node)