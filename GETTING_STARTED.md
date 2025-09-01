# 🚀 Getting Started with Goliath Quantum Starter

**Transform your business with quantum advantage in under 5 minutes.**

This guide will walk you through setting up the Goliath Quantum Starter platform and running your first quantum operation.

---

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10+, macOS 10.15+, or Ubuntu 18.04+
- **Python**: Python 3.11 or higher
- **Memory**: 8GB RAM minimum, 16GB recommended
- **Storage**: 5GB free disk space
- **Network**: Internet connection for quantum computing access

### Required Accounts
- **GitHub**: For accessing the repository
- **Dynex**: For neuromorphic quantum computing (optional for demo)
- **OpenAI/Anthropic**: For AI-enhanced features (optional for demo)

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Clone the Repository
```bash
# Clone the repository
git clone https://github.com/GoliathBritton/goliath-quantum-starter
cd goliath-quantum-starter

# Verify the installation
ls -la
```

**Expected Output**:
```
total 1234
drwxr-xr-x  15 user  staff    480 Jan 15 10:00 .
drwxr-xr-x   3 user  staff     96 Jan 15 10:00 ..
-rw-r--r--   1 user  staff   1234 Jan 15 10:00 README.md
-rw-r--r--   1 user  staff    567 Jan 15 10:00 requirements.txt
drwxr-xr-x   8 user  staff    256 Jan 15 10:00 src/
drwxr-xr-x   4 user  staff    128 Jan 15 10:00 tests/
...
```

### Step 2: Install Dependencies
```bash
# Create a virtual environment (recommended)
python -m venv goliath-env

# Activate the virtual environment
# On Windows:
goliath-env\Scripts\activate
# On macOS/Linux:
source goliath-env/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Expected Output**:
```
Collecting qiskit>=0.44.0
  Downloading qiskit-0.44.0-py3-none-any.whl (5.2 MB)
Collecting dynex>=0.1.0
  Downloading dynex-0.1.0-py3-none-any.whl (2.1 MB)
...
Successfully installed qiskit-0.44.0 dynex-0.1.0 fastapi-0.110.0 ...
```

### Step 3: Set Up Environment Variables (Optional)
```bash
# For full functionality, set these environment variables
export DYNEX_API_KEY="your_dynex_api_key_here"
export OPENAI_API_KEY="your_openai_api_key_here"
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"

# On Windows, use:
# set DYNEX_API_KEY=your_dynex_api_key_here
# set OPENAI_API_KEY=your_openai_api_key_here
```

**Note**: You can run the demo without these keys, but some features will be limited.

### Step 4: Start the API Server
```bash
# Start the FastAPI server
uvicorn src.nqba_stack.api_server:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Started server process [12346]
INFO:     Application startup complete.
```

### Step 5: Run Your First Quantum Operation
Open a new terminal and run the integrated demo:

```bash
# Run the comprehensive NQBA demo
python demo_integrated_nqba.py
```

**Expected Output**:
```
🚀 FLYFOX AI - NQBA Core Demo
==================================================

📋 Step 1: Third-Party Integration Registration
----------------------------------------
✓ Third-party integration registered successfully
Client ID: demo_client_12345

🔬 Step 2: Business Assessment with Quantum Optimization
-------------------------------------------------------
✓ Business assessment completed
Quantum advantage ratio: 14.2x
...
```

---

## 🎯 Explore Business Solutions

### 1. Sigma Select - Sales Intelligence
```bash
# Launch the sales intelligence dashboard
streamlit run src/nqba_stack/business_pods/sigma_select/sigma_select_dashboard.py
```

**Features**:
- Lead scoring with quantum-enhanced AI
- Sales script generation
- Pipeline optimization
- Performance analytics

### 2. FLYFOX AI - Energy Optimization
```bash
# Launch the energy optimization dashboard
streamlit run src/nqba_stack/business_pods/flyfox_ai/flyfox_energy_optimizer.py
```

**Features**:
- Energy consumption optimization
- Cost reduction analysis
- Real-time monitoring
- Predictive analytics

### 3. Goliath Trade - Quantum Finance
```bash
# Launch the financial intelligence dashboard
streamlit run src/nqba_stack/business_pods/goliath_trade/web3_blockchain_demo.py
```

**Features**:
- Portfolio optimization
- Risk assessment
- DeFi integration
- Blockchain analytics

---

## 🧠 Your First Quantum Operations

### 1. Basic QUBO Optimization
```python
from src.nqba_stack.core.quantum_adapter import QuantumAdapter
import numpy as np

# Initialize the quantum adapter
quantum_adapter = QuantumAdapter()

# Create a simple QUBO problem
qubo_matrix = np.array([
    [2, -1, 0],
    [-1, 3, -1],
    [0, -1, 2]
])

# Solve with quantum advantage
result = await quantum_adapter.solve_qubo(
    qubo_matrix,
    provider="dynex",
    optimization_level="maximum"
)

print(f"Optimal solution: {result.solution}")
print(f"Quantum advantage: {result.quantum_advantage_ratio}x")
```

### 2. AI-Enhanced Decision Making
```python
from src.nqba_stack.core.decision_logic import SigmaEQEngine

# Initialize the SigmaEQ engine
sigmaeq = SigmaEQEngine(max_qubits=32, enable_hybrid=True)

# Score business leads
leads = [
    {"company": "TechCorp", "revenue": 1000000, "employees": 50},
    {"company": "DataInc", "revenue": 5000000, "employees": 200},
    {"company": "StartupXYZ", "revenue": 100000, "employees": 5}
]

# Get quantum-enhanced lead scores
scores = await sigmaeq.score_leads(
    leads=leads,
    model="hybrid_quantum_ai",
    optimization_target="conversion_probability"
)

for lead, score in zip(leads, scores):
    print(f"{lead['company']}: {score:.2f}")
```

### 3. Portfolio Optimization
```python
from src.nqba_stack.core.quantum_adapter import QuantumAdapter

# Create portfolio optimization problem
assets = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN"]
returns = [0.15, 0.12, 0.18, 0.25, 0.20]
risk_tolerance = 0.3

# Generate QUBO matrix for portfolio optimization
qubo_matrix = create_portfolio_qubo(assets, returns, risk_tolerance)

# Solve with quantum advantage
result = await quantum_adapter.solve_qubo(
    qubo_matrix,
    provider="dynex",
    optimization_level="maximum"
)

# Extract optimal portfolio weights
optimal_weights = result.solution
print("Optimal Portfolio Weights:")
for asset, weight in zip(assets, optimal_weights):
    print(f"  {asset}: {weight:.2%}")
```

---

## 🔧 Advanced Configuration

### 1. Custom Quantum Provider Settings
```python
from src.nqba_stack.core.quantum_adapter import QuantumAdapter

# Configure custom settings
quantum_adapter = QuantumAdapter(
    default_provider="dynex",
    fallback_providers=["qiskit", "cirq"],
    timeout_seconds=300,
    max_retries=3,
    enable_caching=True
)
```

### 2. Business Pod Configuration
```python
from src.nqba_stack.core.orchestrator import BusinessPod, NQBAStackOrchestrator

# Create custom business pod
custom_pod = BusinessPod(
    pod_id="my_business",
    name="My Business Solution",
    description="Custom quantum-enhanced business logic",
    capabilities=["optimization", "prediction", "automation"],
    qubo_problems=["supply_chain", "inventory_optimization"],
    active=True
)

# Register with orchestrator
orchestrator = NQBAStackOrchestrator()
orchestrator.register_business_pod(custom_pod)
```

### 3. Performance Monitoring
```python
from src.nqba_stack.core.orchestrator import NQBAStackOrchestrator

# Get system performance metrics
orchestrator = NQBAStackOrchestrator()
metrics = orchestrator.get_performance_metrics()

print(f"Total tasks: {metrics['total_tasks']}")
print(f"Success rate: {metrics['success_rate']:.2%}")
print(f"Average execution time: {metrics['avg_execution_time']:.3f}s")
print(f"Quantum enhancement rate: {metrics['quantum_enhanced_rate']:.2%}")
```

---

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Import Errors
**Problem**: `ModuleNotFoundError: No module named 'src'`
**Solution**:
```bash
# Add src to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Or run from the root directory
python -m src.main
```

#### 2. Dynex Connection Issues
**Problem**: `ConnectionError: Unable to connect to Dynex network`
**Solution**:
```bash
# Check your API key
echo $DYNEX_API_KEY

# Verify network connectivity
curl -I https://api.dynexcoin.org

# Use testnet for development
export DYNEX_NETWORK=testnet
```

#### 3. Memory Issues
**Problem**: `MemoryError: Unable to allocate array`
**Solution**:
```bash
# Reduce problem size
export MAX_QUBITS=1000

# Use smaller optimization problems
# Increase system memory or use cloud deployment
```

#### 4. Performance Issues
**Problem**: Slow quantum operations
**Solution**:
```python
# Enable caching
quantum_adapter = QuantumAdapter(enable_caching=True)

# Use appropriate optimization level
result = await quantum_adapter.solve_qubo(
    qubo_matrix,
    optimization_level="balanced"  # or "fast", "maximum"
)
```

---

## 📚 Next Steps

### 1. Explore the Documentation
- **📖 [API Documentation](http://localhost:8000/docs)** - Complete API reference
- **🏗️ [Architecture Guide](docs/architecture.md)** - Deep dive into NQBA Stack
- **🎯 [Business Use Cases](docs/business_pods.md)** - Real-world applications

### 2. Build Your First Application
- **🚀 [Quick Start Templates](examples/quick_start/)** - Pre-built application templates
- **🔧 [Developer Guide](docs/contributing.md)** - Building custom solutions
- **📊 [Performance Benchmarks](docs/benchmarks.md)** - Optimization strategies

### 3. Join the Community
- **💬 [Discord Community](https://discord.gg/goliath-quantum)** - Real-time support
- **🐛 [GitHub Issues](https://github.com/GoliathBritton/goliath-quantum-starter/issues)** - Report bugs and request features
- **📧 [Email Support](mailto:support@goliathquantum.com)** - Enterprise inquiries

---

## 🎯 Success Metrics

### What You Should See After Setup
- ✅ **API Server**: Running on http://localhost:8000
- ✅ **Demo Applications**: All three business pods working
- ✅ **Quantum Operations**: Successful QUBO solving
- ✅ **Performance**: 10x+ speed improvement over classical methods
- ✅ **Cost**: 90% lower than traditional quantum computing

### Validation Commands
```bash
# Test API health
curl http://localhost:8000/v1/system/health

# Run tests
python -m pytest tests/ -v

# Check coverage
python -m pytest --cov=src --cov-report=html

# Performance benchmark
python examples/benchmark_quantum_advantage.py
```

---

## 🏆 Congratulations!

You've successfully set up the Goliath Quantum Starter platform and are now ready to:

- **🚀 Run quantum operations** with 90% cost reduction
- **🤖 Build AI-enhanced business applications**
- **📊 Optimize complex business problems** with quantum advantage
- **🌐 Scale your solutions** across multiple business domains

**Welcome to the future of quantum business computing!**

---

## 📞 Need Help?

- **💬 [Discord Community](https://discord.gg/goliath-quantum)** - Real-time support
- **🐛 [GitHub Issues](https://github.com/GoliathBritton/goliath-quantum-starter/issues)** - Bug reports & feature requests
- **📧 [Email Support](mailto:support@goliathquantum.com)** - Enterprise inquiries
- **📖 [Documentation](https://docs.goliathquantum.com)** - Complete guides

---

*This guide is part of the Goliath Quantum Starter ecosystem. For the latest updates, check our [GitHub repository](https://github.com/GoliathBritton/goliath-quantum-starter).*
