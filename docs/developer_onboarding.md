# 🚀 Developer Onboarding Guide
# Goliath Quantum Starter Ecosystem

Welcome to the Goliath Quantum Starter! This guide will get you up and running with our quantum-AI convergence platform in minutes.

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8+ (3.9+ recommended)
- **Memory**: 8GB+ RAM
- **Storage**: 2GB+ free space
- **OS**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

### Required Software
- **Git**: Latest version
- **Python**: Official distribution or Anaconda
- **Docker**: For containerized deployment (optional)

## 🚀 Quick Start (5 minutes)

### 1. Clone & Setup
```bash
# Clone the repository
git clone https://github.com/your-org/goliath-quantum-starter.git
cd goliath-quantum-starter

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
notepad .env  # Windows
nano .env     # macOS/Linux
```

**Required Environment Variables:**
```env
# Quantum Computing
DYNEX_API_KEY=dnx_your_key_here
DYNEX_NETWORK=mainnet

# AI Services
OPENAI_API_KEY=sk-your_key_here
ANTHROPIC_API_KEY=sk-ant-your_key_here

# Optional: IPFS for data backup
IPFS_GATEWAY_URL=https://ipfs.io
```

### 3. Verify Installation
```bash
# Test quantum adapter
python -c "from src.nqba_stack.quantum_adapter import QuantumAdapter; print('✅ Quantum Adapter ready')"

# Test business pods
python -c "from src.nqba_stack.business_pods.sigma_select.sigma_select_pod import SigmaSelectPod; print('✅ Business Pods ready')"

# Run health check
python -m src.nqba_stack.api_server
```

## 🏗️ Architecture Overview

### NQBA Stack Components
```
┌─────────────────────────────────────────────────────────────┐
│                    Business Applications                    │
├─────────────────────────────────────────────────────────────┤
│  Sigma Select  │  FLYFOX AI  │  Goliath Trade  │  SFG     │
│  (Sales)       │  (Energy)   │  (Trading)      │  Symmetry│
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                NQBA Stack Orchestrator                     │
│  • Task Routing & Management                              │
│  • Resource Management                                    │
│  • Business Logic Orchestration                           │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                Living Technical Codex (LTC)                │
│  • Provenance Tracking                                    │
│  • Performance Metrics                                    │
│  • Compliance & Audit                                     │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                Quantum Computing Layer                      │
│  • Dynex (Neuromorphic)                                   │
│  • Qiskit (IBM)                                           │
│  • Cirq (Google)                                          │
│  • Classical Fallback                                     │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Configuration Guide

### Quantum Backend Selection
```python
from src.nqba_stack.quantum_adapter import QuantumAdapter

# Initialize with specific backend
adapter = QuantumAdapter(
    backend="dynex",           # dynex, qiskit, cirq, classical
    enable_fallback=True,      # Fallback to classical if quantum fails
    max_qubits=64             # Maximum qubits for operations
)
```

### Business Pod Configuration
```python
from src.nqba_stack.business_pods.sigma_select.sigma_select_pod import SigmaSelectPod

# Initialize with custom settings
pod = SigmaSelectPod(
    quantum_adapter=adapter,
    ltc_logger=ltc_logger,
    config={
        "max_leads": 1000,
        "scoring_threshold": 0.7,
        "quantum_advantage_target": 10.0
    }
)
```

### LTC Logger Setup
```python
from src.nqba_stack.ltc_logger import LTCLogger

# Initialize with blockchain anchoring
ltc_logger = LTCLogger(
    blockchain_provider="ethereum",  # ethereum, polygon, local
    enable_provenance=True,
    audit_trail=True
)
```

## 🧪 Testing & Validation

### Run Performance Benchmarks
```bash
# Comprehensive benchmark across all pods
python -m src.nqba_stack.performance.benchmark_suite

# Expected results:
# ✅ 100% Success Rate
# 🚀 400x+ Quantum Advantage
# ⏱️ Significant time savings
```

### Test Individual Business Pods
```bash
# Test Sigma Select (Sales Intelligence)
python -c "
from src.nqba_stack.business_pods.sigma_select.sigma_select_pod import SigmaSelectPod
pod = SigmaSelectPod()
result = await pod.score_leads([{'company': 'Test Corp', 'revenue': 1000000}])
print(f'Lead Score: {result}')
"

# Test FLYFOX AI (Energy Optimization)
python -c "
from src.nqba_stack.business_pods.flyfox_ai.flyfox_ai_pod import FLYFOXAIEnergyPod
pod = FLYFOXAIEnergyPod()
result = await pod.optimize_energy_consumption([100, 150, 200])
print(f'Optimization: {result}')
"
```

### API Server Testing
```bash
# Start API server
python -m src.nqba_stack.api_server

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/metrics/business-pods
```

## 🚨 Troubleshooting

### Common Issues & Solutions

#### 1. **Module Import Errors**
```bash
# Error: No module named 'src.nqba_stack'
# Solution: Run from project root directory
cd /path/to/goliath-quantum-starter
python -m src.nqba_stack.performance.benchmark_suite
```

#### 2. **API Key Issues**
```bash
# Error: Dynex API key seems too short
# Solution: Ensure API key starts with 'dnx_' and is 64+ characters
export DYNEX_API_KEY=dnx_your_actual_64_character_key_here
```

#### 3. **Quantum Resource Limits**
```bash
# Error: Matrix size 100 exceeds max qubits 64
# Solution: This is expected behavior - system falls back to classical
# Adjust max_qubits in QuantumAdapter if needed
```

#### 4. **Performance Issues**
```bash
# Slow quantum operations
# Solution: Check Dynex network status and API key validity
python -c "
from src.nqba_stack.quantum_adapter import QuantumAdapter
adapter = QuantumAdapter()
print(adapter.get_backend_status())
"
```

### Debug Mode
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
export QUANTUM_DEBUG=true

# Run with verbose output
python -m src.nqba_stack.performance.benchmark_suite --verbose
```

## 📚 Next Steps

### 1. **Explore Business Pods**
- [ ] Test Sigma Select lead scoring
- [ ] Optimize energy with FLYFOX AI
- [ ] Run portfolio optimization with Goliath Trade
- [ ] Generate financial plans with SFG Symmetry
- [ ] Execute intelligence operations with Ghost NeuroQ

### 2. **Build Custom Solutions**
- [ ] Create new business pod
- [ ] Integrate with existing systems
- [ ] Develop custom quantum algorithms
- [ ] Build performance dashboards

### 3. **Join the Community**
- [ ] Discord: [Link to be added]
- [ ] GitHub Discussions: [Link to be added]
- [ ] Documentation: [Link to be added]

## 🎯 Success Metrics

### Development Milestones
- [ ] **Setup Complete**: Environment configured and tested
- [ ] **First Quantum Operation**: Successfully run QUBO optimization
- [ ] **Business Pod Integration**: All 5 pods operational
- [ ] **Performance Validation**: 400x+ quantum advantage confirmed
- [ ] **Custom Development**: First custom solution deployed

### Performance Targets
- **Quantum Advantage**: 400x+ over classical methods
- **Success Rate**: 95%+ for all operations
- **Response Time**: <2s for standard operations
- **Scalability**: Support for 1000+ concurrent users

## 🆘 Getting Help

### Documentation Resources
- **Architecture Guide**: `docs/architecture.md`
- **API Documentation**: `docs/api_documentation.md`
- **Quick Start Templates**: `docs/quick_start_templates.md`
- **Business Case**: `BUSINESS_CASE.md`

### Support Channels
- **GitHub Issues**: For bugs and feature requests
- **Discord**: For real-time help and community
- **Email**: [Support email to be added]

---

**Welcome to the future of quantum computing! 🚀**

Your journey with the Goliath Quantum Starter begins now. Start with the quick start guide, then explore the business pods to see the power of quantum-AI convergence in action.
