# NQBA Framework - Neuromorphic Quantum Business Architecture

🚀 **Quantum-Enhanced Business Intelligence Platform** - A comprehensive meta-architecture that orchestrates quantum-inspired AI modules for enterprise business applications.

## 🌟 Overview

The NQBA (Neuromorphic Quantum Business Architecture) Framework is a cutting-edge platform that integrates:

- **Core Intelligence Layer** - qdLLM, QNLP, and QTransformers as unified intelligence modules
- **Business Procedures** - Reusable workflows, algorithms, and orchestration templates
- **Governance & Compliance** - Policy enforcement, audit trails, and regulatory frameworks
- **Integration Layer** - External system connectors and protocol adapters
- **API Layer** - Production-ready REST API with authentication and rate limiting
- **Framework Orchestration** - Central coordination and monitoring of all components

## 🏗️ NQBA Framework Architecture

```mermaid
graph TB
    subgraph "NQBA Framework - Neuromorphic Quantum Business Architecture"
        subgraph "API Layer"
            API["REST API"]
            WS["WebSocket"]
            AUTH["Authentication"]
        end
        
        subgraph "Governance Layer"
            POL["Policies"]
            COMP["Compliance"]
            AUD["Audit Trail"]
        end
        
        subgraph "Integration Layer"
            CONN["System Connectors"]
            ADAPT["Protocol Adapters"]
            BRIDGE["Legacy Bridges"]
        end
        
        subgraph "Procedures Layer"
            WF["Business Workflows"]
            ALG["Algorithms"]
            ORCH["Orchestration"]
        end
        
        subgraph "Core Intelligence Layer"
            subgraph "qdLLM Engine"
                QDIFF["Quantum Diffusion"]
                REV["Reversal Algorithms"]
                SCORE["Coherence Scoring"]
            end
            
            subgraph "QNLP Processor"
                QEMBED["Quantum Embeddings"]
                ENT["Semantic Entanglement"]
                COH["Contextual Coherence"]
            end
            
            subgraph "QTransformers"
                QATTN["Quantum Attention"]
                BLOCK["QTransformer Blocks"]
                MODEL["QTransformer Model"]
            end
        end
        
        subgraph "Framework Core"
            CORE["NQBA Orchestrator"]
            CONFIG["Configuration"]
            MONITOR["Monitoring"]
        end
    end
    
    API --> CORE
    POL --> CORE
    CONN --> CORE
    WF --> QDIFF
    WF --> QEMBED
    WF --> QATTN
    CORE --> QDIFF
    CORE --> QEMBED
    CORE --> QATTN
    QTRANS --> QATTN
    
    ENGINE --> QCOHER
    QNLP --> QCOHER
    QTRANS --> QCOHER
    
    API --> CACHE
    API --> DB
    API --> MONITOR
    API --> LOGS
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Redis (for caching)
- PostgreSQL (optional, for persistent storage)
- CUDA-compatible GPU (optional, for acceleration)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd goliath-quantum-starter/nqba-phase2/goliath-quantum-starter
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install additional NLP models:**
   ```bash
   python -m spacy download en_core_web_sm
   python -c "import nltk; nltk.download('punkt'); nltk.download('vader_lexicon')"
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Running the Demo

```bash
# Run the comprehensive demo
python demo/demo_qdllm_stack.py

# Run the test suite
python run_tests.py

# Start the FastAPI server
python -m qdllm.api.server
```

## 📚 Components

### 🧠 qdLLM Core Engine

The heart of the platform, featuring:

- **Quantum Diffusion Models** for advanced text generation
- **Bidirectional Reasoning** for multi-perspective analysis
- **Coherence Optimization** for maintaining quantum states
- **Dynamic Temperature Scaling** for controlled randomness

```python
from qdllm.core.engine import qdLLMEngine
from qdllm.api.models import InferenceRequest, ModelType

engine = qdLLMEngine()
await engine.initialize()

request = InferenceRequest(
    prompt="Explain quantum computing",
    model_type=ModelType.QDLLM,
    use_quantum_diffusion=True,
    bidirectional_reasoning=True
)

result = await engine.generate(request)
print(result.text)
```

### 🔬 QNLP Processor

Quantum-enhanced natural language processing:

- **Quantum Embeddings** for enhanced semantic representation
- **Sentiment Analysis** with quantum coherence metrics
- **Named Entity Recognition** with quantum uncertainty
- **Text Classification** using quantum feature spaces

```python
from qdllm.qnlp.processor import QNLPProcessor
from qdllm.api.models import QNLPRequest, QNLPTask

processor = QNLPProcessor()
await processor.initialize()

request = QNLPRequest(
    text="I love quantum computing!",
    task=QNLPTask.SENTIMENT,
    use_quantum_embeddings=True
)

result = await processor.process(request)
print(f"Sentiment: {result.sentiment.label} ({result.sentiment.confidence:.3f})")
```

### ⚛️ QTransformers

Quantum-inspired transformer architecture:

- **Quantum Attention Mechanisms** for enhanced focus
- **Superposition States** in hidden representations
- **Entanglement Patterns** between tokens
- **Coherence-Preserving Layers** for stable processing

```python
from qdllm.qtransformers.model import QTransformerModel
from qdllm.api.models import QTransformerRequest

model = QTransformerModel()
await model.initialize()

request = QTransformerRequest(
    input_text="The future of AI is",
    task="text_generation",
    quantum_layers=True,
    attention_type="quantum"
)

result = await model.forward(request)
print(result.output_text)
```

### 🔄 Parallel Executor

High-performance parallel processing:

- **Batch Processing** for multiple requests
- **Priority Queues** for task management
- **Resource Monitoring** for optimal performance
- **Async/Await Support** for non-blocking operations

```python
from qdllm.core.parallel_executor import ParallelExecutor, ExecutionMode

executor = ParallelExecutor()

# Process multiple tasks in parallel
tasks = [process_text(text) for text in texts]
results = await executor.execute_batch(
    tasks,
    mode=ExecutionMode.PARALLEL,
    max_workers=4
)
```

## 🌐 API Endpoints

The FastAPI server provides comprehensive REST endpoints:

### Core Inference
- `POST /api/v1/inference` - Generate text using qdLLM
- `POST /api/v1/qnlp` - Process text with QNLP
- `POST /api/v1/qtransformer` - Transform text with QTransformers
- `POST /api/v1/batch` - Batch processing requests

### System Management
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics
- `GET /api/v1/models` - Available models
- `POST /api/v1/models/load` - Load specific model

### Documentation
- `GET /docs` - Interactive API documentation
- `GET /redoc` - Alternative API documentation

## 🧪 Testing

Comprehensive test suite covering all components:

```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py --unit          # Unit tests only
python run_tests.py --integration   # Integration tests only
python run_tests.py --performance   # Performance benchmarks
python run_tests.py --coverage      # Generate coverage report

# Generate HTML report
python run_tests.py --report test_report.html
```

### Test Coverage

- **Unit Tests**: Individual component functionality
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Benchmarking and optimization
- **API Tests**: REST endpoint validation
- **Quantum Tests**: Quantum coherence and entanglement

## 📊 Performance Metrics

The platform includes comprehensive monitoring:

### Quantum Metrics
- **Coherence**: Quantum state stability (0.0 - 1.0)
- **Entanglement**: Inter-token correlations (0.0 - 1.0)
- **Fidelity**: Quantum operation accuracy (0.0 - 1.0)

### Performance Metrics
- **Inference Speed**: Tokens per second
- **Memory Usage**: RAM and GPU utilization
- **Throughput**: Requests per second
- **Latency**: Response time distribution

### Quality Metrics
- **Perplexity**: Language model quality
- **BLEU Score**: Translation quality
- **Semantic Similarity**: Embedding quality
- **Attention Entropy**: Focus distribution

## 🔧 Configuration

Environment variables for customization:

```bash
# Core Configuration
QDLLM_MODEL_PATH=/path/to/models
QDLLM_CACHE_TTL=3600
QDLLM_MAX_WORKERS=4

# Quantum Parameters
QDLLM_COHERENCE_THRESHOLD=0.8
QDLLM_DIFFUSION_STEPS=100
QDLLM_QUANTUM_NOISE=0.1

# API Configuration
QDLLM_HOST=0.0.0.0
QDLLM_PORT=8000
QDLLM_RATE_LIMIT=100

# Database
DATABASE_URL=postgresql://user:pass@localhost/qdllm
REDIS_URL=redis://localhost:6379

# Monitoring
PROMETHEUS_PORT=9090
LOG_LEVEL=INFO
```

## 🚀 Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY demo/ ./demo/
COPY tests/ ./tests/

EXPOSE 8000
CMD ["python", "-m", "qdllm.api.server"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qdllm-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: qdllm-api
  template:
    metadata:
      labels:
        app: qdllm-api
    spec:
      containers:
      - name: qdllm-api
        image: qdllm:latest
        ports:
        - containerPort: 8000
        env:
        - name: QDLLM_HOST
          value: "0.0.0.0"
        - name: REDIS_URL
          value: "redis://redis-service:6379"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run the test suite: `python run_tests.py`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run code formatting
black src/ tests/ demo/
flake8 src/ tests/ demo/

# Type checking
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Quantum computing research community
- Transformer architecture pioneers
- Open source AI/ML ecosystem
- FastAPI and Pydantic teams

## 📞 Support

For questions, issues, or contributions:

- 📧 Email: support@qdllm.ai
- 💬 Discord: [qdLLM Community](https://discord.gg/qdllm)
- 📖 Documentation: [docs.qdllm.ai](https://docs.qdllm.ai)
- 🐛 Issues: [GitHub Issues](https://github.com/qdllm/foundation-stack/issues)

---

**Built with ❤️ by the qdLLM Team**

*Advancing the frontier of quantum-enhanced artificial intelligence*