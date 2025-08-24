# NQBA Stack: Neuromorphic Quantum Business Architecture

**The core orchestration engine and Living Technical Codex (LTC)** for the next generation of intelligent enterprises. This repository is the foundational implementation of the NQBA Stack, powering the quantum-native AI capabilities of **FLYFOX AI**, **Goliath of All Trade**, and **Sigma Select**.

The NQBA Stack unifies neuromorphic quantum computing (Dynex), adaptive AI, and blockchain-based provenance into a single, coherent architecture for business automation and intelligence.

---

## 🚀 Live Demos & Business Pods
See the NQBA Stack in action:
*   **Sigma Select (Sales Intelligence):** [flyfoxai.io/sigmaeq](https://flyfoxai.io/sigmaeq) - AI-powered sales copilot and lead scoring.
*   **FLYFOX AI (Industrial AIaaS):** [flyfoxai.io/energy](https://flyfoxai.io/energy) - Quantum-optimized energy scheduling and analytics.
*   **Goliath of All Trade (Quantum Finance):** [flyfoxai.io/broker](https://flyfoxai.io/broker) - Portfolio optimization and risk analysis.

---

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/FLYFOX-AI/flyfoxai-nqba-core
cd flyfoxai-nqba-core
pip install -r requirements.txt
```

### 2. Configure Environment
Add your API keys to your environment:
```bash
# Required for Neuromorphic Quantum Compute
export DYNEX_API_KEY="your_dynex_mainnet_key"

# Required for LLM Orchestration
export OPENAI_API_KEY="your_openai_key"
# and/or
export LLM_API_KEY="your_deepseek_or_other_key"

# Required for Decentralized Storage (LTC Provenance)
export IPFS_PROJECT_ID="your_infura_project_id"
export IPFS_PROJECT_SECRET="your_infura_secret"
```

### 3. Run the Services
**Run the Core API Server (FastAPI):**
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000
```
**Run a Business Pod Dashboard (Streamlit):**
```bash
streamlit run src/nqba_stack/business_pods/sigma_select/sigma_select_dashboard.py
streamlit run src/nqba_stack/business_pods/flyfox_ai/flyfox_energy_optimizer.py
streamlit run src/nqba_stack/business_pods/goliath_trade/web3_blockchain_demo.py
```

---

## 🔌 API Endpoints (NQBA Core Orchestration)

The core API acts as the central orchestrator, routing tasks to the appropriate AI and quantum engines.

| Endpoint | Pod | Description |
| :--- | :--- | :--- |
| `POST /v1/sales/score` | Sigma Select | Score leads and prioritize pipeline using the SigmaEQ engine. |
| `GET /v1/sales/script` | Sigma Select | Generate personalized sales scripts grounded in proven SigmaEQ playbooks. |
| `POST /v1/energy/optimize` | FLYFOX AI | Optimize industrial energy schedules and consumption using quantum-derived strategies. |
| `POST /v1/energy/broker` | FLYFOX AI / Goliath | Optimize energy trading portfolios and risk exposure (QUBO-powered). |
| `GET /v1/system/health` | Core | System health and orchestrator status. |
| `GET /v1/ltc/query` | Core | Query the Living Technical Codex for audit and compliance. |

---

## 🏗️ Architecture Overview

The NQBA Stack is built in distinct layers:

```
goliath-quantum-starter/ (The NQBA Stack)
└── src/
    └── nqba_stack/              # The Core Architecture
        ├── core/                # The Kernel (Orchestrator, LTC, Quantum Adapter)
        │   ├── orchestrator.py  # Central brain for task routing
        │   ├── ltc_logger.py    # Living Technical Codex
        │   ├── dynex_adapter.py # Quantum optimization interface
        │   └── settings.py      # Configuration management
        └── business_pods/       # The Implementations
            ├── flyfox_ai/       # AIaaS Marketplace Pod
            ├── goliath_trade/   # Quantum Finance Pod
            └── sigma_select/    # Sales Intelligence Pod
```

### Core Components

1.  **Business Pods:** Specialized applications (Sigma Select, FLYFOX AI, Goliath) that consume the core's intelligence.
2.  **Orchestration & Intelligence Layer (This Repo):** The `NQBA Core` containing the orchestrator, SigmaEQ decision engine, and Living Technical Codex (LTC).
3.  **Neuromorphic Quantum Compute Layer:** Integration with the **Dynex** platform and its DynexSolve chip for quantum-powered optimization.
4.  **Provenance & Security Layer:** Blockchain-anchored logging of all decisions via IPFS and PoUW receipts for auditable trust.

---

## 🧠 The Vision: Why NQBA?

The Neuromorphic Quantum Business Architecture isn't just a platform—it's a new paradigm for business logic. It moves beyond static software to create **adaptive, self-optimizing enterprises** where every decision is enhanced by quantum-derived intelligence and recorded on an immutable ledger for perfect provenance.

### Key Differentiators

- **Quantum Advantage**: DynexSolve PoUW for complex optimization problems
- **Neuromorphic Intelligence**: Adaptive AI that learns and evolves
- **Living Technical Codex**: Immutable audit trail for all operations
- **Business Pod Architecture**: Modular, scalable business solutions
- **SigmaEQ Methodology**: Question-led sales and optimization approach

### Use Cases

- **Industrial AI**: Energy optimization, production scheduling, quality control
- **Quantum Finance**: Portfolio optimization, risk assessment, DeFi strategies
- **Sales Intelligence**: Lead scoring, next-best-action, customer analytics

---

## 🚀 Development & Testing

### Running Tests
```bash
# Test the core NQBA Stack
python -m pytest tests/ -v

# Test specific components
python -m pytest tests/test_sigma_select_fixes.py -v
```

### Development Workflow
1. **Core Development**: Work in `src/nqba_stack/core/`
2. **Business Pods**: Implement solutions in `src/nqba_stack/business_pods/`
3. **Integration**: Use the orchestrator for cross-pod communication
4. **Testing**: All operations are logged to LTC for verification

### Adding New Business Pods
```python
from nqba_stack.core.orchestrator import BusinessPod

new_pod = BusinessPod(
    pod_id="new_business",
    name="New Business",
    description="Description of capabilities",
    capabilities=["capability1", "capability2"],
    qubo_problems=["problem1", "problem2"],
    active=True,
    last_heartbeat=datetime.now()
)

orchestrator.register_business_pod(new_pod)
```

---

## 📊 Deployment & Resources

*   **GitHub Pages Documentation:** [https://flyfox-ai.github.io/nqba-core](https://flyfox-ai.github.io/nqba-core)
*   **Live Demo Dashboards:** [SigmaEQ](https://flyfoxai.io/sigmaeq) | [Energy Analytics](https://flyfoxai.io/energy) | [Broker](https://flyfoxai.io/broker)
*   **API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs) (when running locally)
*   **License:** Proprietary. See LICENSE.md for details.

---

## 🔮 Roadmap

### Phase 1: Core Foundation (Current)
- ✅ NQBA Stack Orchestrator
- ✅ Living Technical Codex (LTC)
- ✅ Dynex Quantum Integration
- ✅ Three Business Pods
- ✅ API Server

### Phase 2: Intelligence Scale-Up (Next 90 Days)
- 🚧 Advanced QUBO Models
- 🚧 Real-time Learning
- 🚧 Multi-tenant Support
- 🚧 Advanced Analytics

### Phase 3: Enterprise Features
- 🔮 Advanced Security
- 🔮 Compliance Frameworks
- 🔮 Enterprise Integrations
- 🔮 Global Deployment

---

## 🤝 Contributing

This is the foundational core of the NQBA Stack. Contributions should focus on:

1. **Core Architecture**: Orchestrator, LTC, quantum integration
2. **Business Pods**: New business solutions and capabilities
3. **Testing & Validation**: Ensuring quantum advantage and reliability
4. **Documentation**: Making the architecture accessible

---

## 📞 Support

- **Technical Issues**: Create GitHub issues
- **Business Inquiries**: Contact the NQBA Stack team
- **Partnership Opportunities**: Reach out for collaboration

---

**This core repository is the first step. Welcome to the future of business intelligence.**

---

*Built with ❤️ by the NQBA Stack Team*