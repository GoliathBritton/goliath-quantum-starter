### Example: Neuromorphic/AI Automation Catalog

```python
from nqba import AUTOMATIONS

# List available automations
print(list(AUTOMATIONS.keys()))

# Run a quantum optimization
result = AUTOMATIONS["quantum_optimize"](2, [(0,0,1.0),(1,1,-1.0),(0,1,0.5)])
print(result)

# Run an OpenAI chat (if available)
if "openai_chat" in AUTOMATIONS:
	result = AUTOMATIONS["openai_chat"]("What is quantum AI?")
	print(result)
```

*Recommendation: Extend the automation catalog with more workflows—energy optimization, insurance quoting, trading, creative writing, scientific discovery, etc. Each automation can leverage Dynex, OpenAI, or NQBA pods for best-in-class results.*
### Example: Business Pods

```python
from nqba import LeadScoringPod, QuantumOptimizerPod, SalesScriptPod

# Lead scoring
pod = LeadScoringPod("lead_scoring")
result = pod.run({"lead_score": 0.8, "risk": 0.1})
print(result)

# Quantum optimization
qpod = QuantumOptimizerPod("quantum_opt")
result = qpod.run(2, [(0,0,1.0),(1,1,-1.0),(0,1,0.5)])
print(result)

# Sales script
spod = SalesScriptPod("sales_script")
result = spod.run({"name": "Alice"})
print(result)
```

*Recommendation: Extend with more pods for energy optimization, insurance quoting, trading, etc. Each pod should subclass `AgentInterface` and wire in LTC logging for audit/provenance.*
# NQBA Core

This package implements the core logic, API, and agent mesh for the Neuromorphic Quantum Business Architecture (NQBA)-first, Q-Cortex-powered intelligence economy platform.

## Usage

Import the package and run the FastAPI app:

```python
from nqba import app
```

Or use the decision and optimization utilities directly:

```python
from nqba import decide, optimize_qubo, ltc_record, AgentInterface
```


### Example: Policy-based Decision (Neuromorphic Quantum Business Architecture)

```python
features = {"lead_score": 0.8, "risk": 0.1}
result = decide("lead_score_v1", features)
print(result)
# {'decision_id': ..., 'result': {'score': ..., 'action': ...}, 'explanation': ...}
```


### Example: Quantum Optimization (QUBO)

```python
Q = [ (0, 0, 1.0), (1, 1, -1.0), (0, 1, 0.5) ]
result = optimize_qubo(2, Q)
print(result)
# {'decision_id': ..., 'assignment': [...], 'objective_value': ..., 'backend': 'dynex.sdk' or 'mock.quantum'}
```

*If the Dynex SDK is not installed, a mock backend is used for development.*

### Example: LTC Audit/Provenance Logging

```python
entry = ltc_record(
	policy_id="lead_score_v1",
	inputs={"features": {"lead_score": 0.8}},
	outputs={"score": 0.8, "action": "approve"},
	explanation="Lead approved",
	solver_backend="decision.logic"
)
print(entry["storage_ref"])
# 'ipfs://...' or 'file://...'
```

*Set the environment variable `IPFS_API_URL` to use a remote IPFS node. Otherwise, local file storage is used as fallback.*

## Next Steps
- Integrate Dynex SDK in `quantum_adapter.py`
- Connect LTC logger to persistent store (IPFS, DynexCoin, etc.)
- Implement business pods as subclasses of `AgentInterface`

## Next Steps
- Wire up Q-Cortex YAML policy loading in `decision_logic.py`
- Integrate Dynex SDK in `quantum_adapter.py`
- Connect LTC logger to persistent store (IPFS, DynexCoin, etc.)
- Implement business pods as subclasses of `AgentInterface`
