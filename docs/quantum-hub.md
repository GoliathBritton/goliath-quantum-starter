# FLYFOX AI Quantum Hub

**Powered by NQBA**

A provider-agnostic quantum computing integration hub built as an MCP-style subsystem within NQBA Core. The Quantum Hub provides unified access to quantum computing resources with governance, compliance, and audit capabilities.

## Overview

The FLYFOX AI Quantum Hub is designed to be the central nervous system for quantum computing operations across all NQBA business pods. It provides:

- **Provider Agnostic**: Support for multiple quantum providers (Dynex, IBM Q, D-Wave, etc.)
- **MCP-Style Architecture**: Clean plugin contract for third-party integrations
- **Governance & Compliance**: Built-in policy enforcement and audit logging
- **Business Integration**: Seamless integration with NQBA business processes

## Architecture

### Core Components

```
src/nqba_stack/quantum/
├── schemas/           # Pydantic data models
│   ├── core_models.py
│   ├── requests.py
│   └── responses.py
├── registry/          # Capability and provider registries
│   ├── capability_registry.py
│   └── provider_registry.py
├── adapters/          # Provider adapters
├── mappers/           # Problem normalization
└── policy/            # Governance and compliance
```

### Data Flow

1. **Request Reception**: API endpoints receive quantum computing requests
2. **Problem Normalization**: Business problems are converted to canonical quantum forms
3. **Provider Selection**: Best provider is selected based on capabilities and constraints
4. **Execution**: Quantum computation is performed via provider adapter
5. **Result Processing**: Results are validated and formatted
6. **Audit Logging**: All operations are logged to LTC (Living Technical Codex)

## API Endpoints

### Core Quantum Operations

#### POST `/v1/quantum/optimize/qubo`
Optimize a QUBO problem using quantum computing.

**Request:**
```json
{
  "problem_type": "qubo",
  "problem_data": {
    "qubo_matrix": [[1, 2], [2, 3]],
    "linear_terms": [1, 2]
  },
  "parameters": {
    "num_reads": 1000,
    "timeout": 300
  },
  "client_id": "client123",
  "preferred_provider": "dynex"
}
```

**Response:**
```json
{
  "success": true,
  "job_id": "job-uuid",
  "message": "QUBO optimization job submitted",
  "data": {
    "estimated_runtime": 120,
    "provider": "dynex"
  }
}
```

#### POST `/v1/quantum/llm`
Generate text using quantum-enhanced language models.

**Request:**
```json
{
  "prompt": "Explain quantum computing in simple terms",
  "temperature": 0.7,
  "max_tokens": 500,
  "use_quantum_enhancement": true,
  "client_id": "client123"
}
```

#### POST `/v1/quantum/portfolio/optimize`
Optimize investment portfolio using quantum computing.

**Request:**
```json
{
  "assets": ["AAPL", "GOOGL", "MSFT"],
  "prices": [150.0, 2800.0, 300.0],
  "returns": [0.12, 0.08, 0.15],
  "budget": 100000,
  "risk_tolerance": 0.5,
  "client_id": "client123"
}
```

### Job Management

#### GET `/v1/quantum/jobs/{job_id}`
Get job status and metadata.

#### GET `/v1/quantum/jobs/{job_id}/result`
Get job results (if completed).

### Provider Management

#### GET `/v1/quantum/providers`
List available quantum providers.

#### POST `/v1/quantum/register`
Register a new third-party provider.

### Usage and Analytics

#### GET `/v1/quantum/usage/{client_id}`
Get usage statistics for a client.

#### GET `/v1/quantum/capabilities`
List available quantum capabilities.

## Provider Adapters

### Dynex Adapter (FLYFOX AI Quantum - Neuromorphic Backend)

The Dynex adapter provides access to Dynex's neuromorphic quantum computing platform.

**Configuration:**
```python
{
  "api_key": "your-dynex-api-key",
  "endpoint": "https://api.dynexcoin.org",
  "timeout": 300,
  "max_qubits": 1000
}
```

**Capabilities:**
- QUBO optimization
- Ising model solving
- Quantum machine learning
- Portfolio optimization

### Simulator Adapter

For development and testing, a quantum simulator adapter is provided.

**Configuration:**
```python
{
  "simulator_type": "qiskit_aer",
  "shots": 1000,
  "noise_model": "depolarizing"
}
```

## Problem Mappers

### Sigma Select Lead Scoring

Maps sales lead data to QUBO optimization problems.

```python
def map_lead_to_qubo(lead_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert lead scoring problem to QUBO format.
    
    Variables:
    - x_i: Whether to contact lead i
    - y_j: Whether to use channel j
    
    Objective: Maximize expected revenue - contact costs
    """
    # Implementation details...
```

### Energy Optimization

Maps energy scheduling problems to quantum optimization.

```python
def map_energy_to_qubo(energy_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert energy optimization to QUBO format.
    
    Variables:
    - x_t,s: Whether to use source s at time t
    
    Objective: Minimize total cost while meeting demand
    """
    # Implementation details...
```

### Portfolio Optimization

Maps portfolio optimization to quantum problems.

```python
def map_portfolio_to_qubo(portfolio_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert portfolio optimization to QUBO format.
    
    Variables:
    - w_i: Weight of asset i in portfolio
    
    Objective: Maximize return - risk penalty
    """
    # Implementation details...
```

## Governance and Compliance

### High Council Policy Engine

The Quantum Hub includes a policy engine that enforces:

- **Data Classification**: Ensures appropriate handling of sensitive data
- **Cost Controls**: Prevents excessive spending on quantum resources
- **Jurisdiction Compliance**: Routes requests to appropriate providers
- **Energy Budgets**: Manages quantum computing energy consumption

### Audit Logging (LTC)

All quantum operations are automatically logged to the Living Technical Codex:

```python
audit_record = AuditRecord(
    operation="quantum.optimize.qubo",
    resource_id=str(job_id),
    client_id=client_id,
    data_classification="public",
    compliance_checks=["cost_limit", "data_privacy"],
    cost_impact=estimated_cost,
    energy_impact=estimated_energy
)
```

## Integration with Business Pods

### Sigma Select Integration

```python
# Lead scoring with quantum enhancement
lead_score = await quantum_hub.score_lead(
    lead_data=lead_info,
    scoring_criteria=["engagement", "budget", "authority"],
    weights={"engagement": 0.4, "budget": 0.3, "authority": 0.3}
)
```

### FLYFOX AI Energy Integration

```python
# Energy optimization
optimal_schedule = await quantum_hub.optimize_energy(
    energy_sources=available_sources,
    demand_forecast=demand_data,
    constraints=operational_constraints
)
```

### Goliath of All Trade Integration

```python
# Portfolio optimization
optimal_portfolio = await quantum_hub.optimize_portfolio(
    assets=market_assets,
    prices=current_prices,
    budget=investment_budget,
    risk_tolerance=client_risk_profile
)
```

## Development Guide

### Adding a New Provider

1. **Create Adapter**: Implement the `QuantumAdapter` protocol
2. **Register Capabilities**: Add provider capabilities to the registry
3. **Configure Policy**: Set up appropriate governance rules
4. **Test Integration**: Verify end-to-end functionality

```python
class CustomProviderAdapter:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def submit_qubo(self, qubo_data: Dict[str, Any]) -> str:
        # Submit QUBO to custom provider
        pass
    
    async def poll(self, job_id: str) -> JobStatus:
        # Poll job status
        pass
    
    async def result(self, job_id: str) -> Dict[str, Any]:
        # Get job results
        pass
```

### Adding a New Problem Type

1. **Define Schema**: Add to `ProblemType` enum
2. **Create Mapper**: Implement problem normalization
3. **Update Registry**: Register with capability registry
4. **Add API Endpoint**: Create FastAPI endpoint

### Testing

```bash
# Run quantum hub tests
pytest tests/test_quantum_hub.py

# Test specific provider
pytest tests/test_dynex_adapter.py

# Integration tests
pytest tests/test_quantum_integration.py
```

## Configuration

### Environment Variables

```bash
# Quantum Hub Configuration
QUANTUM_HUB_ENABLED=true
QUANTUM_DEFAULT_PROVIDER=dynex
QUANTUM_MAX_CONCURRENT_JOBS=10
QUANTUM_DEFAULT_TIMEOUT=300

# Provider Configuration
DYNEX_API_KEY=your-api-key
DYNEX_ENDPOINT=https://api.dynexcoin.org

# Governance
QUANTUM_COST_LIMIT=100.0
QUANTUM_ENABLE_AUDIT_LOGGING=true
```

### Configuration File

```yaml
quantum_hub:
  enabled: true
  default_provider: dynex
  max_concurrent_jobs: 10
  default_timeout: 300
  cost_limit: 100.0
  enable_audit_logging: true
  
  providers:
    dynex:
      api_key: ${DYNEX_API_KEY}
      endpoint: https://api.dynexcoin.org
      timeout: 300
      max_qubits: 1000
    
    simulator:
      type: qiskit_aer
      shots: 1000
      noise_model: depolarizing
```

## Monitoring and Observability

### Metrics

- Job success/failure rates
- Provider response times
- Cost per operation
- Energy consumption
- Queue lengths

### Logging

```python
import logging

logger = logging.getLogger("quantum_hub")
logger.info("Quantum job submitted", extra={
    "job_id": job_id,
    "provider": provider,
    "problem_type": problem_type,
    "client_id": client_id
})
```

### Health Checks

```bash
# Check quantum hub health
curl http://localhost:8000/v1/quantum/health

# Check provider status
curl http://localhost:8000/v1/quantum/providers/status
```

## Security Considerations

### Authentication

All quantum operations require API key authentication:

```python
@router.post("/optimize/qubo")
async def optimize_qubo(
    request: QuantumOptimizationRequest,
    current_client: str = Depends(authenticate_client)
):
    # Verify client has permission for quantum operations
    pass
```

### Data Privacy

- PII is automatically detected and handled appropriately
- Data classification determines routing and storage
- Audit trails ensure compliance

### Rate Limiting

```python
# Rate limiting by client
@limiter.limit("10/minute")
async def quantum_operation(request: Request):
    pass
```

## Troubleshooting

### Common Issues

1. **Provider Unavailable**
   - Check provider status: `/v1/quantum/providers/status`
   - Verify API keys and endpoints
   - Check network connectivity

2. **Job Timeout**
   - Increase timeout in request
   - Check provider queue length
   - Consider using different provider

3. **Cost Limit Exceeded**
   - Check current usage: `/v1/quantum/usage/{client_id}`
   - Adjust cost limits in configuration
   - Use cost-optimized providers

### Debug Mode

```bash
# Enable debug logging
export QUANTUM_HUB_LOG_LEVEL=DEBUG

# Run with debug output
python -m src.nqba_stack.api_server --debug
```

## Support

For support and questions:

- **Documentation**: [https://flyfox-ai.github.io/nqba-core](https://flyfox-ai.github.io/nqba-core)
- **Issues**: [GitHub Issues](https://github.com/FLYFOX-AI/flyfoxai-nqba-core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/FLYFOX-AI/flyfoxai-nqba-core/discussions)

---

**FLYFOX AI Quantum Hub** - *Powered by NQBA*
