# 📚 Goliath Quantum Starter - API Documentation

**Complete API reference with working examples for all business pods**

---

## 🎯 **API Overview**

The Goliath Quantum Starter API provides **quantum-enhanced business intelligence** through five specialized business pods, each offering unique optimization capabilities powered by the NQBA Stack.

### **Base URL**
```
http://localhost:8000
```

### **API Version**
```
v2.0.0
```

### **Authentication**
Currently, the API uses **API key authentication** via Bearer token in the Authorization header.

```bash
Authorization: Bearer YOUR_API_KEY
```

---

## 🏗️ **API Architecture**

### **Business Pods**
1. **Sigma Select** - Sales Intelligence & Lead Scoring
2. **FLYFOX AI** - Energy Optimization & Consumption Management
3. **Goliath Trade** - Financial Trading & Portfolio Optimization
4. **SFG Symmetry** - Insurance & Financial Services
5. **Ghost NeuroQ** - Competitive Intelligence & Data Warfare

### **Core Components**
- **NQBA Stack Orchestrator** - Central task routing and management
- **Living Technical Codex (LTC)** - Immutable audit trail and logging
- **Quantum Adapter** - Multi-provider quantum computing interface

---

## 🔍 **Core Endpoints**

### **Health Check**
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "2.0.0",
  "quantum_status": "operational",
  "business_pods": [
    "sigma_select",
    "flyfox_ai",
    "goliath_trade",
    "sfg_symmetry",
    "ghost_neuroq"
  ]
}
```

### **Business Pod Metrics**
```http
GET /metrics/business-pods
```

**Response:**
```json
[
  {
    "pod_id": "sigma_select",
    "pod_name": "Sigma Select - Sales Intelligence",
    "total_operations": 150,
    "success_rate": 0.98,
    "average_quantum_advantage": 14.2,
    "active": true,
    "last_heartbeat": "2024-01-15T10:30:00Z"
  }
]
```

### **Quantum Operations**
```http
POST /quantum/operate
```

**Request:**
```json
{
  "operation_type": "optimization",
  "parameters": {
    "problem_type": "portfolio_optimization",
    "assets": ["AAPL", "GOOGL", "MSFT"],
    "constraints": {"risk_tolerance": 0.6}
  },
  "business_pod": "goliath_trade",
  "optimization_level": "maximum"
}
```

**Response:**
```json
{
  "operation_id": "QUANTUM_OP_001",
  "status": "completed",
  "result": {
    "optimized_portfolio": {"AAPL": 0.4, "GOOGL": 0.35, "MSFT": 0.25},
    "expected_return": 0.085,
    "risk_score": 0.42
  },
  "quantum_advantage": 14.2,
  "execution_time": 0.8,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🎯 **Sigma Select - Sales Intelligence**

### **Lead Scoring**
```http
POST /sigma-select/score-leads
```

**Request:**
```json
{
  "leads": [
    {
      "lead_id": "LEAD_001",
      "company": "TechCorp Inc.",
      "industry": "Technology",
      "revenue": 5000000,
      "employee_count": 50,
      "website_traffic": 10000,
      "social_media_followers": 5000
    }
  ],
  "scoring_criteria": {
    "revenue_weight": 0.3,
    "industry_weight": 0.2,
    "traffic_weight": 0.25,
    "social_weight": 0.25
  },
  "optimization_level": "maximum"
}
```

**Response:**
```json
{
  "scored_leads": [
    {
      "lead_id": "LEAD_001",
      "score": 0.87,
      "priority": "high",
      "recommended_actions": [
        "Schedule demo within 24 hours",
        "Prepare enterprise pricing",
        "Assign senior sales rep"
      ]
    }
  ],
  "quantum_advantage": 15.2,
  "confidence_level": 0.94,
  "execution_time": 0.8
}
```

### **Example Usage (Python)**
```python
import requests

# Score leads with quantum enhancement
response = requests.post("http://localhost:8000/sigma-select/score-leads", json={
    "leads": [
        {
            "lead_id": "LEAD_001",
            "company": "TechCorp Inc.",
            "industry": "Technology",
            "revenue": 5000000,
            "employee_count": 50,
            "website_traffic": 10000,
            "social_media_followers": 5000
        }
    ],
    "scoring_criteria": {
        "revenue_weight": 0.3,
        "industry_weight": 0.2,
        "traffic_weight": 0.25,
        "social_weight": 0.25
    },
    "optimization_level": "maximum"
})

result = response.json()
print(f"Quantum advantage: {result['quantum_advantage']:.1f}x")
print(f"Lead score: {result['scored_leads'][0]['score']:.2f}")
```

---

## ⚡ **FLYFOX AI - Energy Optimization**

### **Energy Consumption Optimization**
```http
POST /flyfox-ai/optimize-energy
```

**Request:**
```json
{
  "energy_data": {
    "current_consumption": {
      "peak_hours": [14, 15, 16, 17, 18],
      "off_peak_hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 20, 21, 22, 23, 0],
      "peak_rate": 0.15,
      "off_peak_rate": 0.08
    },
    "facility_schedule": {
      "production_hours": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
      "maintenance_hours": [6, 7, 18, 19],
      "idle_hours": [20, 21, 22, 23, 0, 1, 2, 3, 4, 5]
    }
  },
  "optimization_horizon": 24,
  "constraints": {
    "max_peak_usage": 0.4,
    "min_production_hours": 10,
    "maintenance_required": true
  },
  "optimization_level": "maximum"
}
```

**Response:**
```json
{
  "optimized_schedule": {
    "production_hours": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
    "maintenance_hours": [6, 19],
    "idle_hours": [20, 21, 22, 23, 0, 1, 2, 3, 4, 5],
    "energy_allocation": {
      "peak_hours": 0.35,
      "off_peak_hours": 0.65
    }
  },
  "cost_savings": 0.23,
  "quantum_advantage": 14.8,
  "execution_time": 0.6
}
```

### **Example Usage (Python)**
```python
import requests

# Optimize energy consumption
response = requests.post("http://localhost:8000/flyfox-ai/optimize-energy", json={
    "energy_data": {
        "current_consumption": {
            "peak_hours": [14, 15, 16, 17, 18],
            "off_peak_hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 20, 21, 22, 23, 0],
            "peak_rate": 0.15,
            "off_peak_rate": 0.08
        },
        "facility_schedule": {
            "production_hours": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17],
            "maintenance_hours": [6, 7, 18, 19],
            "idle_hours": [20, 21, 22, 23, 0, 1, 2, 3, 4, 5]
        }
    },
    "optimization_horizon": 24,
    "constraints": {
        "max_peak_usage": 0.4,
        "min_production_hours": 10,
        "maintenance_required": true
    },
    "optimization_level": "maximum"
})

result = response.json()
print(f"Cost savings: {result['cost_savings']:.1%}")
print(f"Quantum advantage: {result['quantum_advantage']:.1f}x")
```

---

## 💰 **Goliath Trade - Financial Trading**

### **Portfolio Optimization**
```http
POST /goliath-trade/optimize-portfolio
```

**Request:**
```json
{
  "portfolio_data": {
    "assets": [
      {"symbol": "AAPL", "current_weight": 0.3, "expected_return": 0.12, "volatility": 0.25},
      {"symbol": "GOOGL", "current_weight": 0.25, "expected_return": 0.15, "volatility": 0.30},
      {"symbol": "MSFT", "current_weight": 0.25, "expected_return": 0.13, "volatility": 0.28},
      {"symbol": "TSLA", "current_weight": 0.2, "expected_return": 0.20, "volatility": 0.45}
    ],
    "correlation_matrix": [
      [1.0, 0.6, 0.7, 0.4],
      [0.6, 1.0, 0.8, 0.5],
      [0.7, 0.8, 1.0, 0.6],
      [0.4, 0.5, 0.6, 1.0]
    ]
  },
  "risk_tolerance": 0.6,
  "optimization_horizon": 30,
  "constraints": {
    "min_weight": 0.05,
    "max_weight": 0.4,
    "target_return": 0.14
  },
  "optimization_level": "maximum"
}
```

**Response:**
```json
{
  "optimized_portfolio": {
    "AAPL": 0.35,
    "GOOGL": 0.30,
    "MSFT": 0.25,
    "TSLA": 0.10
  },
  "expected_return": 0.142,
  "risk_score": 0.38,
  "quantum_advantage": 14.5,
  "execution_time": 3.2
}
```

### **Example Usage (Python)**
```python
import requests

# Optimize investment portfolio
response = requests.post("http://localhost:8000/goliath-trade/optimize-portfolio", json={
    "portfolio_data": {
        "assets": [
            {"symbol": "AAPL", "current_weight": 0.3, "expected_return": 0.12, "volatility": 0.25},
            {"symbol": "GOOGL", "current_weight": 0.25, "expected_return": 0.15, "volatility": 0.30},
            {"symbol": "MSFT", "current_weight": 0.25, "expected_return": 0.13, "volatility": 0.28},
            {"symbol": "TSLA", "current_weight": 0.2, "expected_return": 0.20, "volatility": 0.45}
        ],
        "correlation_matrix": [
            [1.0, 0.6, 0.7, 0.4],
            [0.6, 1.0, 0.8, 0.5],
            [0.7, 0.8, 1.0, 0.6],
            [0.4, 0.5, 0.6, 1.0]
        ]
    },
    "risk_tolerance": 0.6,
    "optimization_horizon": 30,
    "constraints": {
        "min_weight": 0.05,
        "max_weight": 0.4,
        "target_return": 0.14
    },
    "optimization_level": "maximum"
})

result = response.json()
print(f"Expected return: {result['expected_return']:.1%}")
print(f"Risk score: {result['risk_score']:.2f}")
print(f"Quantum advantage: {result['quantum_advantage']:.1f}x")
```

---

## 🏦 **SFG Symmetry - Insurance & Financial Services**

### **Client Registration**
```http
POST /sfg-symmetry/register-client
```

**Request:**
```json
{
  "age": 42,
  "income": 120000,
  "assets": 300000,
  "liabilities": 150000,
  "risk_tolerance": 0.6,
  "investment_horizon": 25,
  "family_status": "married_with_children",
  "health_rating": 0.85
}
```

**Response:**
```json
{
  "client_id": "SFG_CLIENT_000001",
  "status": "registered",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Generate Financial Recommendations**
```http
POST /sfg-symmetry/generate-recommendations
```

**Request:**
```json
{
  "client_id": "SFG_CLIENT_000001",
  "recommendation_type": "portfolio",
  "optimization_level": "maximum"
}
```

**Response:**
```json
{
  "recommendation_id": "SFG_REC_000001",
  "products": [
    {
      "product_id": "LIFE_PREMIUM",
      "name": "Premium Life Insurance",
      "type": "life",
      "base_premium": 150.0,
      "coverage_amount": 1000000.0
    },
    {
      "product_id": "ANNUITY_FIXED",
      "name": "Fixed Rate Annuity",
      "type": "annuity",
      "base_premium": 50000.0,
      "coverage_amount": 500000.0
    }
  ],
  "portfolio_allocation": {
    "Life Insurance": 0.15,
    "Fixed Annuities": 0.20,
    "Variable Annuities": 0.10,
    "Mortgage Protection": 0.05,
    "Retirement 401(k)": 0.25,
    "Bonds": 0.15,
    "Stocks": 0.08,
    "Alternative Investments": 0.02
  },
  "risk_score": 0.42,
  "expected_return": 0.068,
  "quantum_advantage": 14.3,
  "confidence_level": 0.95
}
```

### **Get Client Portfolio**
```http
GET /sfg-symmetry/client-portfolio/{client_id}
```

**Response:**
```json
{
  "client_profile": {
    "client_id": "SFG_CLIENT_000001",
    "age": 42,
    "income": 120000,
    "assets": 300000,
    "liabilities": 150000,
    "risk_tolerance": 0.6,
    "investment_horizon": 25,
    "family_status": "married_with_children",
    "health_rating": 0.85
  },
  "current_recommendation": {
    "recommendation_id": "SFG_REC_000001",
    "products": [...],
    "portfolio_allocation": {...},
    "risk_score": 0.42,
    "expected_return": 0.068,
    "quantum_advantage": 14.3,
    "confidence_level": 0.95
  },
  "insurance_products": [...],
  "portfolio_summary": {
    "total_assets": 300000,
    "net_worth": 150000,
    "debt_to_income_ratio": 1.25
  }
}
```

### **Example Usage (Python)**
```python
import requests

# Register a new client
client_response = requests.post("http://localhost:8000/sfg-symmetry/register-client", json={
    "age": 42,
    "income": 120000,
    "assets": 300000,
    "liabilities": 150000,
    "risk_tolerance": 0.6,
    "investment_horizon": 25,
    "family_status": "married_with_children",
    "health_rating": 0.85
})

client_id = client_response.json()["client_id"]

# Generate financial recommendations
rec_response = requests.post("http://localhost:8000/sfg-symmetry/generate-recommendations", json={
    "client_id": client_id,
    "recommendation_type": "portfolio",
    "optimization_level": "maximum"
})

recommendation = rec_response.json()
print(f"Risk score: {recommendation['risk_score']:.2f}")
print(f"Expected return: {recommendation['expected_return']:.1%}")
print(f"Quantum advantage: {recommendation['quantum_advantage']:.1f}x")
```

---

## 👻 **Ghost NeuroQ - Competitive Intelligence**

### **Target Registration**
```http
POST /ghost-neuroq/register-target
```

**Request:**
```json
{
  "name": "TechCorp Industries",
  "organization": "TechCorp Inc.",
  "industry": "Technology",
  "risk_level": 0.7,
  "data_sources": ["email", "slack", "crm", "linkedin"],
  "dependencies": ["cloud_services", "supply_chain", "key_personnel"],
  "market_position": 0.8,
  "financial_strength": 0.9,
  "competitive_position": 0.7,
  "dependency_level": 0.6,
  "vulnerability_level": 0.4
}
```

**Response:**
```json
{
  "target_id": "GHOST_TARGET_000001",
  "status": "registered",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Execute NeuroSiphon™**
```http
POST /ghost-neuroq/execute-neuro-siphon
```

**Request:**
```json
{
  "target_id": "GHOST_TARGET_000001",
  "operation_type": "data_extraction",
  "parameters": {
    "data_sources": ["email", "slack"]
  }
}
```

**Response:**
```json
{
  "operation_id": "NEURO_OP_000001",
  "status": "completed",
  "results": {
    "extracted_data": [
      {
        "source": "email",
        "type": "email",
        "content": "Sample email content from TechCorp Inc.",
        "timestamp": "2024-01-15T10:30:00Z",
        "quantum_enhanced": true
      },
      {
        "source": "slack",
        "type": "slack",
        "content": "Sample Slack message from TechCorp Inc.",
        "timestamp": "2024-01-15T10:30:00Z",
        "quantum_enhanced": true
      }
    ],
    "analysis_results": {
      "analysis_score": 0.87,
      "data_patterns": ["pattern_1", "pattern_2", "pattern_3"],
      "anomalies_detected": 2,
      "confidence_level": 0.87,
      "quantum_enhanced": true
    },
    "quantum_advantage": 15.2,
    "data_volume": 2,
    "confidence_level": 0.94
  },
  "quantum_enhanced": true,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Create Sigma Graph**
```http
POST /ghost-neuroq/create-sigma-graph
```

**Request:**
```json
{
  "target_id": "GHOST_TARGET_000001",
  "operation_type": "sigma_graph"
}
```

**Response:**
```json
{
  "target_id": "GHOST_TARGET_000001",
  "organization": "TechCorp Inc.",
  "org_structure": [
    {"title": "CEO", "level": 1, "influence": 0.95},
    {"title": "CFO", "level": 2, "influence": 0.85},
    {"title": "CTO", "level": 2, "influence": 0.80}
  ],
  "leverage_scores": {
    "CEO": 0.89,
    "CFO": 0.76,
    "CTO": 0.72
  },
  "strategic_recommendations": [
    "Focus on CEO - highest leverage position",
    "Develop relationships with 2 mid-level positions",
    "Use quantum-enhanced analysis for real-time leverage updates"
  ],
  "quantum_enhanced": true,
  "generated_at": "2024-01-15T10:30:00Z"
}
```

### **Execute Data Poisoning**
```http
POST /ghost-neuroq/execute-data-poisoning
```

**Request:**
```json
{
  "target_id": "GHOST_TARGET_000001",
  "operation_type": "data_poisoning",
  "parameters": {
    "strategy": "reality_distortion"
  }
}
```

**Response:**
```json
{
  "operation_id": "POISON_OP_000001",
  "status": "completed",
  "results": {
    "strategy": "reality_distortion",
    "poisoning_results": {
      "method": "QNLP Reality Distortion",
      "target_data": "Sales numbers, market position",
      "distortion_level": "High",
      "recovery_time": "3-6 months",
      "quantum_enhanced": true
    },
    "quantum_enhanced": true,
    "success_rate": 0.87,
    "detection_probability": 0.12
  },
  "quantum_enhanced": true,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Example Usage (Python)**
```python
import requests

# Register a new target
target_response = requests.post("http://localhost:8000/ghost-neuroq/register-target", json={
    "name": "TechCorp Industries",
    "organization": "TechCorp Inc.",
    "industry": "Technology",
    "risk_level": 0.7,
    "data_sources": ["email", "slack", "crm", "linkedin"],
    "dependencies": ["cloud_services", "supply_chain", "key_personnel"],
    "market_position": 0.8,
    "financial_strength": 0.9,
    "competitive_position": 0.7,
    "dependency_level": 0.6,
    "vulnerability_level": 0.4
})

target_id = target_response.json()["target_id"]

# Execute NeuroSiphon operation
neuro_response = requests.post("http://localhost:8000/ghost-neuroq/execute-neuro-siphon", json={
    "target_id": target_id,
    "operation_type": "data_extraction",
    "parameters": {
        "data_sources": ["email", "slack"]
    }
})

neuro_result = neuro_response.json()
print(f"Quantum advantage: {neuro_result['results']['quantum_advantage']:.1f}x")
print(f"Data volume: {neuro_result['results']['data_volume']}")
print(f"Confidence level: {neuro_result['results']['confidence_level']:.1%}")
```

---

## 🎼 **NQBA Stack Orchestrator**

### **Get Orchestrator Status**
```http
GET /orchestrator/status
```

**Response:**
```json
{
  "status": "operational",
  "business_pods_count": 5,
  "active_routes": 25,
  "quantum_adapters": 3,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Get Registered Business Pods**
```http
GET /orchestrator/business-pods
```

**Response:**
```json
{
  "business_pods": [
    "sigma_select",
    "flyfox_ai",
    "goliath_trade",
    "sfg_symmetry",
    "ghost_neuroq"
  ],
  "total_count": 5,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 📚 **Living Technical Codex (LTC)**

### **Get LTC Entries**
```http
GET /ltc/entries?limit=100&business_pod=sigma_select&operation_type=lead_scoring
```

**Response:**
```json
{
  "entries": [
    {
      "entry_id": "LTC_ENTRY_000001",
      "timestamp": "2024-01-15T10:30:00Z",
      "operation_type": "lead_scoring",
      "business_pod": "sigma_select",
      "quantum_enhanced": true,
      "performance_metrics": {
        "execution_time": 0.8,
        "quantum_advantage": 15.2,
        "confidence_level": 0.94
      },
      "blockchain_hash": "0x1234...",
      "metadata": {
        "leads_count": 1,
        "scoring_criteria": {...}
      }
    }
  ],
  "total_count": 1,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Get LTC Statistics**
```http
GET /ltc/statistics
```

**Response:**
```json
{
  "statistics": {
    "total_entries": 150,
    "entries_by_pod": {
      "sigma_select": 45,
      "flyfox_ai": 32,
      "goliath_trade": 28,
      "sfg_symmetry": 25,
      "ghost_neuroq": 20
    },
    "entries_by_type": {
      "lead_scoring": 45,
      "energy_optimization": 32,
      "portfolio_optimization": 28,
      "financial_recommendation": 25,
      "data_extraction": 20
    },
    "quantum_enhanced_ratio": 0.95,
    "average_quantum_advantage": 14.8
  },
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## ⚛️ **Quantum Computing Interface**

### **Get Quantum Status**
```http
GET /quantum/status
```

**Response:**
```json
{
  "status": "operational",
  "providers": {
    "dynex": "operational",
    "qiskit": "operational",
    "cirq": "operational"
  },
  "active_operations": 12,
  "queue_length": 3,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### **Get Available Providers**
```http
GET /quantum/providers
```

**Response:**
```json
{
  "providers": [
    {
      "name": "dynex",
      "status": "operational",
      "qubits_available": 1000000,
      "cost_per_hour": 100,
      "optimization_levels": ["standard", "maximum", "extreme"]
    },
    {
      "name": "qiskit",
      "status": "operational",
      "qubits_available": 32,
      "cost_per_hour": 500,
      "optimization_levels": ["standard", "maximum"]
    },
    {
      "name": "cirq",
      "status": "operational",
      "qubits_available": 64,
      "cost_per_hour": 400,
      "optimization_levels": ["standard", "maximum"]
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🎬 **Demo & Testing**

### **Run Comprehensive Demo**
```http
POST /demo/run-comprehensive
```

**Response:**
```json
{
  "status": "demo_scheduled",
  "message": "Comprehensive demo scheduled to run",
  "business_pods": [
    "sigma_select",
    "flyfox_ai",
    "goliath_trade",
    "sfg_symmetry",
    "ghost_neuroq"
  ],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## 🔧 **Error Handling**

### **Standard Error Response**
```json
{
  "error": "Error message description",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "REQ_001",
  "details": {
    "field": "Additional error details",
    "suggestion": "How to fix the error"
  }
}
```

### **Common Error Codes**
| Code | Description | HTTP Status |
|------|-------------|-------------|
| `INVALID_REQUEST` | Request validation failed | 400 |
| `RESOURCE_NOT_FOUND` | Requested resource not found | 404 |
| `QUANTUM_ERROR` | Quantum computing operation failed | 500 |
| `RATE_LIMIT_EXCEEDED` | API rate limit exceeded | 429 |
| `INTERNAL_ERROR` | Internal server error | 500 |

---

## 📊 **Rate Limiting**

### **Rate Limits**
- **Standard Tier**: 100 requests per hour
- **Premium Tier**: 1000 requests per hour
- **Enterprise Tier**: 10000 requests per hour

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1642233600
```

---

## 🚀 **Getting Started**

### **1. Install Dependencies**
```bash
pip install requests numpy pandas
```

### **2. Set Up Environment**
```bash
export GOLIATH_API_URL="http://localhost:8000"
export GOLIATH_API_KEY="your_api_key_here"
```

### **3. Test Connection**
```python
import requests

# Test health check
response = requests.get("http://localhost:8000/health")
print(f"Status: {response.json()['status']}")
print(f"Version: {response.json()['version']}")
```

### **4. Run Your First Quantum Operation**
```python
import requests

# Run portfolio optimization
response = requests.post("http://localhost:8000/quantum/operate", json={
    "operation_type": "optimization",
    "parameters": {
        "problem_type": "portfolio_optimization",
        "assets": ["AAPL", "GOOGL", "MSFT"],
        "constraints": {"risk_tolerance": 0.6}
    },
    "business_pod": "goliath_trade",
    "optimization_level": "maximum"
})

result = response.json()
print(f"Quantum advantage: {result['quantum_advantage']:.1f}x")
print(f"Execution time: {result['execution_time']:.1f}s")
```

---

## 📚 **Additional Resources**

- **🏗️ [Architecture Guide](architecture.md)** - Deep dive into NQBA Stack
- **🎯 [Getting Started Guide](../GETTING_STARTED.md)** - Setup and configuration
- **💼 [Business Case](../BUSINESS_CASE.md)** - ROI analysis and business value
- **🚀 [Development Roadmap](../DEVELOPMENT_ROADMAP.md)** - Strategic implementation plan
- **📖 [Interactive API Docs](http://localhost:8000/docs)** - Swagger UI interface

---

## 🆘 **Support & Community**

- **📖 [Documentation](docs/)** - Comprehensive guides and tutorials
- **🐛 [Issues](https://github.com/GoliathBritton/goliath-quantum-starter/issues)** - Report bugs and request features
- **💬 [Discussions](https://github.com/GoliathBritton/goliath-quantum-starter/discussions)** - Ask questions and share ideas
- **📧 [Email](mailto:support@goliathquantum.com)** - Direct support contact
- **Discord**: [Join our community](https://discord.gg/goliath-quantum)

---

*This API documentation is updated regularly. For the latest version, visit the interactive docs at `/docs` or check the repository.*
