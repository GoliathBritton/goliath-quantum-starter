# NQBA Ecosystem - Observability & SRE System

## Overview

The NQBA Ecosystem Observability & SRE system provides comprehensive monitoring, tracing, and incident response capabilities. Built on OpenTelemetry standards, it delivers end-to-end visibility from frontend interactions through quantum computations to business outcomes.

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway    │    │   Quantum       │
│   (Framer)      │───▶│   (FastAPI)      │───▶│   Solvers       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   OpenTelemetry │    │   Metrics        │    │   Incident      │
│   Tracing       │    │   Collection     │    │   Response      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Jaeger/OTLP   │    │   Golden         │    │   Runbooks      │
│   Exporters     │    │   Dashboards     │    │   & Playbooks   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Components

### 1. OpenTelemetry Tracing

#### Configuration

The tracing system is configured via environment variables:

```bash
# Enable/disable tracing
NQBA_TRACING_ENABLED=true

# Service identification
NQBA_SERVICE_NAME=nqba-ecosystem
NQBA_SERVICE_VERSION=1.0.0
NQBA_ENVIRONMENT=production

# Exporters
NQBA_JAEGER_ENDPOINT=http://jaeger:14268/api/traces
NQBA_OTLP_ENDPOINT=http://collector:4317
NQBA_CONSOLE_EXPORT=true

# Sampling
NQBA_SAMPLE_RATE=1.0
```

#### Usage

```python
from src.nqba_stack.observability.tracing import get_tracer, trace_function

# Get tracer instance
tracer = get_tracer()

# Manual tracing
with tracer.span("operation_name") as span:
    tracer.set_attribute(span, "key", "value")
    # ... operation code ...

# Function decorator
@trace_function("function_name", {"attribute": "value"})
def my_function():
    return "result"
```

#### Specialized Tracers

- **QuantumJobTracer**: Tracks quantum job lifecycle
- **BusinessUnitTracer**: Monitors business unit operations
- **TracingMiddleware**: Automatic FastAPI instrumentation

### 2. Golden Dashboards

#### Dashboard Components

1. **System Health Overview**
   - Uptime, active users, quantum jobs
   - Real-time status indicators

2. **Performance Metrics**
   - API latency (P50, P95, P99)
   - Success rates by service type
   - Quantum vs classical performance

3. **Quantum Advantage Tracking**
   - Current vs target quantum advantage
   - Dynex qubit utilization
   - Job completion rates

4. **Business Metrics**
   - ARR, CAC, LTV, NPS
   - Conversion funnel analysis
   - Quantum win rate trends

5. **Workflow Performance**
   - Success rates by workflow
   - Execution time analysis
   - Volume vs performance correlation

6. **SLO Dashboard**
   - Service Level Objective tracking
   - Performance trends over time
   - Compliance status

#### Running the Dashboard

```bash
# Install dependencies
pip install -r requirements.txt

# Run dashboard
streamlit run src/nqba_stack/observability/dashboard.py

# Access at http://localhost:8501
```

#### Customization

```python
from src.nqba_stack.observability.dashboard import DashboardConfig

# Customize configuration
config = DashboardConfig()
config.refresh_interval = 60  # 1 minute refresh
config.quantum_advantage_threshold = 5.0  # Custom threshold

# Add custom metrics
class CustomMetricsCollector(MetricsCollector):
    def get_custom_metrics(self):
        return {"custom_kpi": 42}
```

### 3. Incident Response Runbooks

#### Incident Severity Levels

- **P0 (Critical)**: Complete system outage, data loss, security breach
- **P1 (High)**: Major functionality degraded, significant performance impact
- **P2 (Medium)**: Minor functionality issues, moderate performance impact
- **P3 (Low)**: Cosmetic issues, minor performance degradation

#### Supported Incidents

1. **Dynex Outage**
   - Detection: Health check failures, quantum job failures
   - Response: Circuit breaker activation, classical fallback
   - Recovery: Gradual quantum service restoration

2. **IPFS Pin Failures**
   - Detection: Pin operation failures, LTC verification issues
   - Response: Backup pinning activation, storage cleanup
   - Recovery: Failed content repinning

3. **Quota Exhaustion**
   - Detection: Rate limit exceeded, quota usage > 90%
   - Response: Rate limiting, customer notification
   - Recovery: Quota increases, usage optimization

4. **Delayed Jobs**
   - Detection: Queue depth > 100, processing delays
   - Response: Worker scaling, job prioritization
   - Recovery: Queue normalization, performance optimization

5. **Billing Drift**
   - Detection: Revenue anomalies, billing discrepancies
   - Response: Billing pause, audit initiation
   - Recovery: Charge corrections, safeguard implementation

6. **API Rate Limit Exceeded**
   - Detection: 429 errors, rate limit violations
   - Response: Throttling, abuse detection
   - Recovery: Limit increases, security review

7. **Authentication Failures**
   - Detection: High failure rates, account lockouts
   - Response: Rate limiting, security team notification
   - Recovery: Service restoration, security hardening

8. **Quantum Job Failures**
   - Detection: High failure rates, success rate < 80%
   - Response: Job pausing, solver health checks
   - Recovery: Service restoration, parameter validation

#### Incident Response Workflow

```
Incident Detection → Severity Assessment → Team Notification → 
Immediate Response → Investigation → Resolution → Recovery → 
Post-Mortem → Documentation Update
```

## Integration

### FastAPI Integration

```python
from fastapi import FastAPI
from src.nqba_stack.observability.tracing import get_tracer, instrument_fastapi

app = FastAPI()
tracer = get_tracer()

# Instrument FastAPI with OpenTelemetry
instrument_fastapi(app, tracer)

# Add tracing middleware
from src.nqba_stack.observability.tracing import TracingMiddleware
app.add_middleware(TracingMiddleware, tracer=tracer)
```

### Business Unit Integration

```python
from src.nqba_stack.observability.tracing import BusinessUnitTracer

class FLYFOXAIBusinessUnit:
    def __init__(self):
        self.tracer = BusinessUnitTracer(get_tracer())
    
    async def optimize_energy(self, user_id: str, data: dict):
        with self.tracer.trace_bu_operation("flyfox_ai", "optimize", user_id):
            # ... optimization logic ...
            pass
```

### QIH Integration

```python
from src.nqba_stack.observability.tracing import QuantumJobTracer

class QuantumIntegrationHub:
    def __init__(self):
        self.quantum_tracer = QuantumJobTracer(get_tracer())
    
    async def submit_job(self, user_id: str, request: dict):
        with self.quantum_tracer.trace_job_submission(
            "job_123", user_id, "dynex"
        ):
            # ... job submission logic ...
            pass
```

## Monitoring & Alerting

### Key Metrics

#### System Health
- `nqba.system.uptime` - System availability percentage
- `nqba.system.active_users` - Concurrent active users
- `nqba.system.quantum_jobs_running` - Active quantum jobs

#### Performance
- `nqba.api.latency.p95` - 95th percentile API response time
- `nqba.api.success_rate` - API call success rate
- `nqba.workflow.completion_rate` - Workflow success rate

#### Quantum Performance
- `nqba.quantum.advantage` - Current quantum advantage achieved
- `nqba.quantum.success_rate` - Quantum job success rate
- `nqba.quantum.fallback_rate` - Classical solver fallback rate

#### Business Metrics
- `nqba.business.arr` - Annual Recurring Revenue
- `nqba.business.conversion_rate` - Lead to customer conversion
- `nqba.business.nps` - Net Promoter Score

### Alerting Rules

```yaml
# Example Prometheus alerting rules
groups:
  - name: nqba_critical_alerts
    rules:
      - alert: SystemDown
        expr: nqba_system_uptime < 0.99
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "NQBA system is down"
          
      - alert: HighLatency
        expr: nqba_api_latency_p95 > 500
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "API latency is high"
          
      - alert: QuantumFailure
        expr: nqba_quantum_success_rate < 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Quantum job failure rate is high"
```

## Deployment

### Docker Compose

```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686"
      - "14268:14268"
    environment:
      - COLLECTOR_OTLP_ENABLED=true
      
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-storage:/var/lib/grafana
      
  nqba-app:
    build: .
    environment:
      - NQBA_TRACING_ENABLED=true
      - NQBA_JAEGER_ENDPOINT=http://jaeger:14268/api/traces
      - NQBA_OTLP_ENDPOINT=http://jaeger:4317
    depends_on:
      - jaeger
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nqba-observability
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nqba-observability
  template:
    metadata:
      labels:
        app: nqba-observability
    spec:
      containers:
      - name: nqba-app
        image: nqba-ecosystem:latest
        env:
        - name: NQBA_TRACING_ENABLED
          value: "true"
        - name: NQBA_JAEGER_ENDPOINT
          value: "http://jaeger-collector:14268/api/traces"
        - name: NQBA_OTLP_ENDPOINT
          value: "http://jaeger-collector:4317"
        ports:
        - containerPort: 8000
        - containerPort: 8501
```

## Testing

### Running Tests

```bash
# Run all observability tests
pytest tests/test_observability_system.py -v

# Run specific test categories
pytest tests/test_observability_system.py::TestTracingConfig -v
pytest tests/test_observability_system.py::TestDashboardConfig -v
pytest tests/test_observability_system.py::TestMetricsCollector -v

# Run with coverage
pytest tests/test_observability_system.py --cov=src/nqba_stack/observability --cov-report=html
```

### Test Categories

1. **Tracing Tests**: Configuration, initialization, span management
2. **Dashboard Tests**: Configuration, metrics collection, rendering
3. **Integration Tests**: End-to-end functionality, performance
4. **Error Handling Tests**: Graceful degradation, exception handling

## Troubleshooting

### Common Issues

#### Tracing Not Working
1. Check `NQBA_TRACING_ENABLED` environment variable
2. Verify OpenTelemetry dependencies are installed
3. Check exporter endpoints are accessible
4. Review tracer initialization logs

#### Dashboard Not Loading
1. Verify Streamlit dependencies are installed
2. Check metrics collector is working
3. Review dashboard logs for errors
4. Verify data sources are accessible

#### High Latency
1. Check OpenTelemetry sampling rate
2. Verify exporter performance
3. Review span processing overhead
4. Check for memory leaks

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Enable OpenTelemetry debug
import os
os.environ['OTEL_LOG_LEVEL'] = 'DEBUG'
```

## Performance Considerations

### Optimization Strategies

1. **Sampling**: Use appropriate sampling rates for production
2. **Batch Processing**: Enable batch span processors
3. **Async Export**: Use async exporters for better performance
4. **Resource Limits**: Set appropriate memory and CPU limits

### Scaling

1. **Horizontal Scaling**: Deploy multiple tracer instances
2. **Load Balancing**: Distribute tracing load across instances
3. **Caching**: Cache frequently accessed metrics
4. **Database Optimization**: Optimize metrics storage and queries

## Security

### Data Privacy

1. **PII Filtering**: Automatically filter sensitive data from traces
2. **Encryption**: Encrypt trace data in transit and at rest
3. **Access Control**: Implement role-based access to observability data
4. **Audit Logging**: Log all access to observability systems

### Compliance

1. **GDPR**: Ensure right to be forgotten for trace data
2. **SOC 2**: Implement security controls for observability
3. **Data Retention**: Implement appropriate data retention policies
4. **Access Logging**: Maintain comprehensive access logs

## Future Enhancements

### Planned Features

1. **Machine Learning Anomaly Detection**
   - Automatic anomaly detection in metrics
   - Predictive alerting
   - Root cause analysis suggestions

2. **Advanced Visualization**
   - 3D topology maps
   - Interactive quantum advantage tracking
   - Real-time business impact visualization

3. **Automated Remediation**
   - Self-healing systems
   - Automatic scaling based on metrics
   - Intelligent circuit breaker management

4. **Integration Expansion**
   - More quantum computing platforms
   - Additional business intelligence tools
   - Enhanced third-party integrations

## Support

### Documentation
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)

### Community
- [OpenTelemetry Community](https://opentelemetry.io/community/)
- [NQBA Ecosystem Discord](https://discord.gg/nqba)
- [FLYFOX AI Support](mailto:support@flyfoxai.io)

### Contributing
- [Contributing Guidelines](../CONTRIBUTING.md)
- [Code of Conduct](../CODE_OF_CONDUCT.md)
- [Development Setup](../docs/DEVELOPMENT.md)

---

## Document Version

- **Version**: 1.0
- **Last Updated**: [Current Date]
- **Next Review**: [Next Review Date]
- **Owner**: [Document Owner]
