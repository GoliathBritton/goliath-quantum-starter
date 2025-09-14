"""Prometheus Metrics for Quantum Nexus Engine"""

import time
import psutil
import threading
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from prometheus_client import (
    Counter, Histogram, Gauge, Summary, Info,
    CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
)
import logging

# Configure logging
logger = logging.getLogger(__name__)

class JobStatus(Enum):
    """Quantum job status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"

class MetricType(Enum):
    """Metric type enumeration"""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

@dataclass
class MetricDefinition:
    """Metric definition with metadata"""
    name: str
    description: str
    metric_type: MetricType
    labels: List[str]
    buckets: Optional[List[float]] = None

class QuantumMetricsRegistry:
    """Custom metrics registry for quantum operations"""
    
    def __init__(self):
        self.registry = CollectorRegistry()
        self.metrics: Dict[str, Any] = {}
        self._lock = threading.Lock()
        
        # Initialize core metrics
        self._initialize_quantum_metrics()
        self._initialize_api_metrics()
        self._initialize_system_metrics()
        self._initialize_error_metrics()
    
    def _initialize_quantum_metrics(self):
        """Initialize quantum-specific metrics"""
        # Quantum job metrics
        self.metrics['quantum_jobs_total'] = Counter(
            'quantum_jobs_total',
            'Total number of quantum jobs processed',
            ['job_type', 'status', 'algorithm', 'backend'],
            registry=self.registry
        )
        
        self.metrics['quantum_job_duration_seconds'] = Histogram(
            'quantum_job_duration_seconds',
            'Duration of quantum job execution',
            ['job_type', 'algorithm', 'backend'],
            buckets=[0.1, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0, 300.0, 600.0, float('inf')],
            registry=self.registry
        )
        
        self.metrics['quantum_jobs_active'] = Gauge(
            'quantum_jobs_active',
            'Number of currently active quantum jobs',
            ['job_type', 'backend'],
            registry=self.registry
        )
        
        self.metrics['quantum_circuit_depth'] = Histogram(
            'quantum_circuit_depth',
            'Depth of quantum circuits',
            ['algorithm', 'optimization_level'],
            buckets=[1, 5, 10, 20, 50, 100, 200, 500, 1000, float('inf')],
            registry=self.registry
        )
        
        self.metrics['quantum_circuit_gates'] = Histogram(
            'quantum_circuit_gates',
            'Number of gates in quantum circuits',
            ['gate_type', 'algorithm'],
            buckets=[1, 10, 50, 100, 500, 1000, 5000, 10000, float('inf')],
            registry=self.registry
        )
        
        self.metrics['quantum_fidelity'] = Gauge(
            'quantum_fidelity',
            'Quantum state fidelity measurements',
            ['job_id', 'algorithm', 'backend'],
            registry=self.registry
        )
        
        self.metrics['quantum_noise_level'] = Gauge(
            'quantum_noise_level',
            'Quantum noise level measurements',
            ['backend', 'noise_type'],
            registry=self.registry
        )
        
        self.metrics['quantum_entanglement_measure'] = Gauge(
            'quantum_entanglement_measure',
            'Quantum entanglement measurements',
            ['job_id', 'qubit_pair'],
            registry=self.registry
        )
        
        # QUBO-specific metrics
        self.metrics['qubo_problems_total'] = Counter(
            'qubo_problems_total',
            'Total number of QUBO problems solved',
            ['problem_type', 'solver', 'status'],
            registry=self.registry
        )
        
        self.metrics['qubo_solution_quality'] = Gauge(
            'qubo_solution_quality',
            'Quality of QUBO solutions (energy/cost)',
            ['problem_id', 'solver'],
            registry=self.registry
        )
        
        self.metrics['qubo_variables_count'] = Histogram(
            'qubo_variables_count',
            'Number of variables in QUBO problems',
            ['problem_type'],
            buckets=[10, 50, 100, 500, 1000, 5000, 10000, float('inf')],
            registry=self.registry
        )
    
    def _initialize_api_metrics(self):
        """Initialize API metrics"""
        self.metrics['api_requests_total'] = Counter(
            'api_requests_total',
            'Total number of API requests',
            ['method', 'endpoint', 'status_code'],
            registry=self.registry
        )
        
        self.metrics['api_request_duration_seconds'] = Histogram(
            'api_request_duration_seconds',
            'Duration of API requests',
            ['method', 'endpoint'],
            buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, float('inf')],
            registry=self.registry
        )
        
        self.metrics['api_active_connections'] = Gauge(
            'api_active_connections',
            'Number of active API connections',
            registry=self.registry
        )
        
        self.metrics['websocket_connections'] = Gauge(
            'websocket_connections_active',
            'Number of active WebSocket connections',
            ['connection_type'],
            registry=self.registry
        )
    
    def _initialize_system_metrics(self):
        """Initialize system resource metrics"""
        self.metrics['system_cpu_usage'] = Gauge(
            'system_cpu_usage_percent',
            'System CPU usage percentage',
            registry=self.registry
        )
        
        self.metrics['system_memory_usage'] = Gauge(
            'system_memory_usage_bytes',
            'System memory usage in bytes',
            ['type'],  # 'used', 'available', 'total'
            registry=self.registry
        )
        
        self.metrics['system_disk_usage'] = Gauge(
            'system_disk_usage_bytes',
            'System disk usage in bytes',
            ['device', 'type'],  # 'used', 'free', 'total'
            registry=self.registry
        )
        
        self.metrics['system_network_bytes'] = Counter(
            'system_network_bytes_total',
            'Total network bytes transferred',
            ['direction'],  # 'sent', 'received'
            registry=self.registry
        )
        
        self.metrics['redis_connections'] = Gauge(
            'redis_connections_active',
            'Number of active Redis connections',
            registry=self.registry
        )
        
        self.metrics['celery_workers'] = Gauge(
            'celery_workers_active',
            'Number of active Celery workers',
            ['queue'],
            registry=self.registry
        )
        
        self.metrics['celery_tasks'] = Counter(
            'celery_tasks_total',
            'Total number of Celery tasks',
            ['task_name', 'status'],
            registry=self.registry
        )
    
    def _initialize_error_metrics(self):
        """Initialize error and alert metrics"""
        self.metrics['errors_total'] = Counter(
            'errors_total',
            'Total number of errors',
            ['error_type', 'component', 'severity'],
            registry=self.registry
        )
        
        self.metrics['alerts_total'] = Counter(
            'alerts_total',
            'Total number of alerts triggered',
            ['alert_type', 'severity'],
            registry=self.registry
        )
        
        self.metrics['security_events_total'] = Counter(
            'security_events_total',
            'Total number of security events',
            ['event_type', 'severity'],
            registry=self.registry
        )
    
    def get_metric(self, name: str):
        """Get metric by name"""
        return self.metrics.get(name)
    
    def record_quantum_job(self, job_type: str, algorithm: str, backend: str, 
                          status: JobStatus, duration: Optional[float] = None,
                          circuit_depth: Optional[int] = None, 
                          gate_count: Optional[int] = None,
                          fidelity: Optional[float] = None):
        """Record quantum job metrics"""
        with self._lock:
            # Record job completion
            self.metrics['quantum_jobs_total'].labels(
                job_type=job_type,
                status=status.value,
                algorithm=algorithm,
                backend=backend
            ).inc()
            
            # Record duration if provided
            if duration is not None:
                self.metrics['quantum_job_duration_seconds'].labels(
                    job_type=job_type,
                    algorithm=algorithm,
                    backend=backend
                ).observe(duration)
            
            # Record circuit metrics
            if circuit_depth is not None:
                self.metrics['quantum_circuit_depth'].labels(
                    algorithm=algorithm,
                    optimization_level='default'
                ).observe(circuit_depth)
            
            if gate_count is not None:
                self.metrics['quantum_circuit_gates'].labels(
                    gate_type='mixed',
                    algorithm=algorithm
                ).observe(gate_count)
            
            # Record fidelity
            if fidelity is not None:
                self.metrics['quantum_fidelity'].labels(
                    job_id='latest',
                    algorithm=algorithm,
                    backend=backend
                ).set(fidelity)
    
    def record_api_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record API request metrics"""
        with self._lock:
            self.metrics['api_requests_total'].labels(
                method=method,
                endpoint=endpoint,
                status_code=str(status_code)
            ).inc()
            
            self.metrics['api_request_duration_seconds'].labels(
                method=method,
                endpoint=endpoint
            ).observe(duration)
    
    def record_error(self, error_type: str, component: str, severity: str = 'error'):
        """Record error metrics"""
        with self._lock:
            self.metrics['errors_total'].labels(
                error_type=error_type,
                component=component,
                severity=severity
            ).inc()
    
    def record_security_event(self, event_type: str, severity: str = 'info'):
        """Record security event metrics"""
        with self._lock:
            self.metrics['security_events_total'].labels(
                event_type=event_type,
                severity=severity
            ).inc()
    
    def update_system_metrics(self):
        """Update system resource metrics"""
        try:
            with self._lock:
                # CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.metrics['system_cpu_usage'].set(cpu_percent)
                
                # Memory usage
                memory = psutil.virtual_memory()
                self.metrics['system_memory_usage'].labels(type='used').set(memory.used)
                self.metrics['system_memory_usage'].labels(type='available').set(memory.available)
                self.metrics['system_memory_usage'].labels(type='total').set(memory.total)
                
                # Disk usage
                disk = psutil.disk_usage('/')
                self.metrics['system_disk_usage'].labels(device='root', type='used').set(disk.used)
                self.metrics['system_disk_usage'].labels(device='root', type='free').set(disk.free)
                self.metrics['system_disk_usage'].labels(device='root', type='total').set(disk.total)
                
                # Network I/O
                network = psutil.net_io_counters()
                self.metrics['system_network_bytes'].labels(direction='sent')._value._value = network.bytes_sent
                self.metrics['system_network_bytes'].labels(direction='received')._value._value = network.bytes_recv
                
        except Exception as e:
            logger.error(f"Error updating system metrics: {str(e)}")
    
    def set_active_jobs(self, job_type: str, backend: str, count: int):
        """Set number of active jobs"""
        with self._lock:
            self.metrics['quantum_jobs_active'].labels(
                job_type=job_type,
                backend=backend
            ).set(count)
    
    def set_active_connections(self, count: int):
        """Set number of active API connections"""
        with self._lock:
            self.metrics['api_active_connections'].set(count)
    
    def export_metrics(self) -> str:
        """Export metrics in Prometheus format"""
        return generate_latest(self.registry)
    
    def get_registry(self) -> CollectorRegistry:
        """Get the Prometheus registry"""
        return self.registry

# Global metrics registry
_metrics_registry = None

def get_metrics_registry() -> QuantumMetricsRegistry:
    """Get global metrics registry instance"""
    global _metrics_registry
    if _metrics_registry is None:
        _metrics_registry = QuantumMetricsRegistry()
    return _metrics_registry

# Convenience functions for common metrics
def quantum_job_counter():
    """Get quantum job counter metric"""
    return get_metrics_registry().get_metric('quantum_jobs_total')

def quantum_job_duration():
    """Get quantum job duration metric"""
    return get_metrics_registry().get_metric('quantum_job_duration_seconds')

def quantum_job_status_gauge():
    """Get quantum job status gauge"""
    return get_metrics_registry().get_metric('quantum_jobs_active')

def quantum_circuit_depth_histogram():
    """Get quantum circuit depth histogram"""
    return get_metrics_registry().get_metric('quantum_circuit_depth')

def quantum_fidelity_gauge():
    """Get quantum fidelity gauge"""
    return get_metrics_registry().get_metric('quantum_fidelity')

def api_request_counter():
    """Get API request counter"""
    return get_metrics_registry().get_metric('api_requests_total')

def api_request_duration():
    """Get API request duration histogram"""
    return get_metrics_registry().get_metric('api_request_duration_seconds')

def system_resource_gauge():
    """Get system resource gauge"""
    return get_metrics_registry().get_metric('system_cpu_usage')

def error_counter():
    """Get error counter"""
    return get_metrics_registry().get_metric('errors_total')

# Metric recording helpers
def record_quantum_job_start(job_id: str, job_type: str, algorithm: str, backend: str):
    """Record quantum job start"""
    registry = get_metrics_registry()
    registry.set_active_jobs(job_type, backend, 1)  # Simplified for demo
    logger.info(f"Quantum job started: {job_id} ({job_type}, {algorithm}, {backend})")

def record_quantum_job_completion(job_id: str, job_type: str, algorithm: str, 
                                backend: str, status: JobStatus, duration: float,
                                circuit_depth: Optional[int] = None,
                                fidelity: Optional[float] = None):
    """Record quantum job completion"""
    registry = get_metrics_registry()
    registry.record_quantum_job(
        job_type=job_type,
        algorithm=algorithm,
        backend=backend,
        status=status,
        duration=duration,
        circuit_depth=circuit_depth,
        fidelity=fidelity
    )
    registry.set_active_jobs(job_type, backend, 0)  # Simplified for demo
    logger.info(f"Quantum job completed: {job_id} ({status.value}, {duration:.2f}s)")

def record_api_call(method: str, endpoint: str, status_code: int, duration: float):
    """Record API call"""
    registry = get_metrics_registry()
    registry.record_api_request(method, endpoint, status_code, duration)

def record_system_error(error_type: str, component: str, severity: str = 'error'):
    """Record system error"""
    registry = get_metrics_registry()
    registry.record_error(error_type, component, severity)
    logger.error(f"System error recorded: {error_type} in {component} ({severity})")