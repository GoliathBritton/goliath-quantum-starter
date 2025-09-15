# 🚀 Goliath Quantum Starter - Quick Start Templates

**Working examples and templates for all business pods**

---

## 🎯 **Quick Start Overview**

Get up and running with **quantum-enhanced business intelligence** in under 5 minutes using these proven templates.

### **Prerequisites**
```bash
pip install requests numpy pandas
export GOLIATH_API_URL="http://localhost:8000"
```

---

## 🎯 **Sigma Select - Sales Intelligence**

### **Template 1: Lead Scoring**
```python
import requests

def score_leads_quantum():
    """Score leads with quantum enhancement"""
    response = requests.post(f"{GOLIATH_API_URL}/sigma-select/score-leads", json={
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
    return result

# Run the template
score_leads_quantum()
```

---

## ⚡ **FLYFOX AI - Energy Optimization**

### **Template 2: Energy Consumption Optimization**
```python
import requests

def optimize_energy_quantum():
    """Optimize energy consumption with quantum enhancement"""
    response = requests.post(f"{GOLIATH_API_URL}/flyfox-ai/optimize-energy", json={
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
            "maintenance_required": True
        },
        "optimization_level": "maximum"
    })
    
    result = response.json()
    print(f"Cost savings: {result['cost_savings']:.1%}")
    print(f"Quantum advantage: {result['quantum_advantage']:.1f}x")
    return result

# Run the template
optimize_energy_quantum()
```

---

## 💰 **Goliath Trade - Financial Trading**

### **Template 3: Portfolio Optimization**
```python
import requests

def optimize_portfolio_quantum():
    """Optimize investment portfolio with quantum enhancement"""
    response = requests.post(f"{GOLIATH_API_URL}/goliath-trade/optimize-portfolio", json={
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
    return result

# Run the template
optimize_portfolio_quantum()
```

---

## 🏦 **SFG Symmetry - Insurance & Financial Services**

### **Template 4: Financial Planning**
```python
import requests

def financial_planning_quantum():
    """Complete financial planning workflow with quantum enhancement"""
    
    # Step 1: Register client
    client_response = requests.post(f"{GOLIATH_API_URL}/sfg-symmetry/register-client", json={
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
    print(f"Client registered: {client_id}")
    
    # Step 2: Generate recommendations
    rec_response = requests.post(f"{GOLIATH_API_URL}/sfg-symmetry/generate-recommendations", json={
        "client_id": client_id,
        "recommendation_type": "portfolio",
        "optimization_level": "maximum"
    })
    
    recommendation = rec_response.json()
    print(f"Risk score: {recommendation['risk_score']:.2f}")
    print(f"Expected return: {recommendation['expected_return']:.1%}")
    print(f"Quantum advantage: {recommendation['quantum_advantage']:.1f}x")
    
    return {"client_id": client_id, "recommendation": recommendation}

# Run the template
financial_planning_quantum()
```

---

## 👻 **Ghost NeuroQ - Competitive Intelligence**

### **Template 5: Intelligence Gathering**
```python
import requests

def intelligence_gathering_quantum():
    """Complete intelligence gathering workflow with quantum enhancement"""
    
    # Step 1: Register target
    target_response = requests.post(f"{GOLIATH_API_URL}/ghost-neuroq/register-target", json={
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
    print(f"Target registered: {target_id}")
    
    # Step 2: Execute NeuroSiphon
    neuro_response = requests.post(f"{GOLIATH_API_URL}/ghost-neuroq/execute-neuro-siphon", json={
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
    
    return {"target_id": target_id, "neuro_result": neuro_result}

# Run the template
intelligence_gathering_quantum()
```

---

## 🎼 **NQBA Stack Orchestrator**

### **Template 6: System Status Check**
```python
import requests

def check_system_status():
    """Check complete system status"""
    
    # Health check
    health_response = requests.get(f"{GOLIATH_API_URL}/health")
    health = health_response.json()
    print(f"System Status: {health['status']}")
    print(f"Version: {health['version']}")
    print(f"Business Pods: {len(health['business_pods'])}")
    
    # Orchestrator status
    orch_response = requests.get(f"{GOLIATH_API_URL}/orchestrator/status")
    orch = orch_response.json()
    print(f"Orchestrator: {orch['status']}")
    print(f"Active Routes: {orch['active_routes']}")
    
    # Quantum status
    quantum_response = requests.get(f"{GOLIATH_API_URL}/quantum/status")
    quantum = quantum_response.json()
    print(f"Quantum Status: {quantum['status']}")
    print(f"Active Operations: {quantum['active_operations']}")
    
    return {"health": health, "orchestrator": orch, "quantum": quantum}

# Run the template
check_system_status()
```

---

## 🔄 **Advanced Workflow Templates**

### **Template 7: Multi-Pod Optimization**
```python
import requests
import asyncio

async def multi_pod_optimization():
    """Run optimization across multiple business pods"""
    
    # Portfolio optimization
    portfolio_result = requests.post(f"{GOLIATH_API_URL}/goliath-trade/optimize-portfolio", json={
        "portfolio_data": {
            "assets": [
                {"symbol": "AAPL", "current_weight": 0.3, "expected_return": 0.12, "volatility": 0.25},
                {"symbol": "GOOGL", "current_weight": 0.25, "expected_return": 0.15, "volatility": 0.30}
            ],
            "correlation_matrix": [[1.0, 0.6], [0.6, 1.0]]
        },
        "risk_tolerance": 0.6,
        "optimization_level": "maximum"
    }).json()
    
    # Energy optimization
    energy_result = requests.post(f"{GOLIATH_API_URL}/flyfox-ai/optimize-energy", json={
        "energy_data": {
            "current_consumption": {
                "peak_hours": [14, 15, 16],
                "off_peak_hours": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 17, 18, 19, 20, 21, 22, 23, 0],
                "peak_rate": 0.15,
                "off_peak_rate": 0.08
            }
        },
        "optimization_level": "maximum"
    }).json()
    
    # Lead scoring
    leads_result = requests.post(f"{GOLIATH_API_URL}/sigma-select/score-leads", json={
        "leads": [{"company": "TechCorp", "revenue": 5000000}],
        "optimization_level": "maximum"
    }).json()
    
    print(f"Portfolio Quantum Advantage: {portfolio_result['quantum_advantage']:.1f}x")
    print(f"Energy Quantum Advantage: {energy_result['quantum_advantage']:.1f}x")
    print(f"Leads Quantum Advantage: {leads_result['quantum_advantage']:.1f}x")
    
    return {
        "portfolio": portfolio_result,
        "energy": energy_result,
        "leads": leads_result
    }

# Run the template
asyncio.run(multi_pod_optimization())
```

---

## 📊 **Performance Testing Templates**

### **Template 8: Quantum Advantage Benchmark**
```python
import requests
import time

def benchmark_quantum_advantage():
    """Benchmark quantum advantage across all pods"""
    
    pods = [
        ("sigma_select", "score-leads"),
        ("flyfox-ai", "optimize-energy"),
        ("goliath-trade", "optimize-portfolio"),
        ("sfg-symmetry", "generate-recommendations"),
        ("ghost-neuroq", "execute-neuro-siphon")
    ]
    
    results = {}
    
    for pod, endpoint in pods:
        start_time = time.time()
        
        try:
            # Run basic operation for each pod
            if pod == "sigma_select":
                response = requests.post(f"{GOLIATH_API_URL}/{pod}/{endpoint}", json={
                    "leads": [{"company": "Test", "revenue": 1000000}],
                    "optimization_level": "maximum"
                })
            elif pod == "flyfox-ai":
                response = requests.post(f"{GOLIATH_API_URL}/{pod}/{endpoint}", json={
                    "energy_data": {"current_consumption": {"peak_hours": [14], "off_peak_hours": [1,2,3]}},
                    "optimization_level": "maximum"
                })
            elif pod == "goliath-trade":
                response = requests.post(f"{GOLIATH_API_URL}/{pod}/{endpoint}", json={
                    "portfolio_data": {"assets": [{"symbol": "TEST", "current_weight": 1.0}]},
                    "optimization_level": "maximum"
                })
            elif pod == "sfg-symmetry":
                # First register client
                client_response = requests.post(f"{GOLIATH_API_URL}/{pod}/register-client", json={
                    "age": 30, "income": 50000, "assets": 100000, "liabilities": 20000
                })
                client_id = client_response.json()["client_id"]
                
                response = requests.post(f"{GOLIATH_API_URL}/{pod}/{endpoint}", json={
                    "client_id": client_id,
                    "optimization_level": "maximum"
                })
            elif pod == "ghost-neuroq":
                # First register target
                target_response = requests.post(f"{GOLIATH_API_URL}/{pod}/register-target", json={
                    "name": "Test Target", "organization": "Test Org", "industry": "Test"
                })
                target_id = target_response.json()["target_id"]
                
                response = requests.post(f"{GOLIATH_API_URL}/{pod}/{endpoint}", json={
                    "target_id": target_id,
                    "operation_type": "data_extraction"
                })
            
            execution_time = time.time() - start_time
            result = response.json()
            
            results[pod] = {
                "quantum_advantage": result.get('quantum_advantage', 1.0),
                "execution_time": execution_time,
                "status": "success"
            }
            
        except Exception as e:
            results[pod] = {
                "quantum_advantage": 1.0,
                "execution_time": time.time() - start_time,
                "status": f"error: {str(e)}"
            }
    
    # Print results
    print("Quantum Advantage Benchmark Results:")
    print("-" * 50)
    for pod, result in results.items():
        print(f"{pod:20} | {result['quantum_advantage']:6.1f}x | {result['execution_time']:6.2f}s | {result['status']}")
    
    return results

# Run the benchmark
benchmark_quantum_advantage()
```

---

## 🎯 **Common Use Case Templates**

### **Template 9: Sales Pipeline Optimization**
```python
import requests

def optimize_sales_pipeline():
    """Optimize entire sales pipeline with quantum enhancement"""
    
    # 1. Score leads
    leads_result = requests.post(f"{GOLIATH_API_URL}/sigma-select/score-leads", json={
        "leads": [
            {"company": "Enterprise A", "revenue": 10000000, "industry": "Technology"},
            {"company": "Enterprise B", "revenue": 5000000, "industry": "Manufacturing"},
            {"company": "Enterprise C", "revenue": 2000000, "industry": "Healthcare"}
        ],
        "optimization_level": "maximum"
    }).json()
    
    # 2. Portfolio optimization for sales team allocation
    portfolio_result = requests.post(f"{GOLIATH_API_URL}/goliath-trade/optimize-portfolio", json={
        "portfolio_data": {
            "assets": [
                {"symbol": "Lead_A", "current_weight": 0.4, "expected_return": 0.8, "volatility": 0.3},
                {"symbol": "Lead_B", "current_weight": 0.35, "expected_return": 0.6, "volatility": 0.4},
                {"symbol": "Lead_C", "current_weight": 0.25, "expected_return": 0.4, "volatility": 0.5}
            ],
            "correlation_matrix": [[1.0, 0.2, 0.1], [0.2, 1.0, 0.3], [0.1, 0.3, 1.0]]
        },
        "risk_tolerance": 0.7,
        "optimization_level": "maximum"
    }).json()
    
    print("Sales Pipeline Optimization Results:")
    print(f"Lead Scoring Quantum Advantage: {leads_result['quantum_advantage']:.1f}x")
    print(f"Portfolio Optimization Quantum Advantage: {portfolio_result['quantum_advantage']:.1f}x")
    
    return {"leads": leads_result, "portfolio": portfolio_result}

# Run the template
optimize_sales_pipeline()
```

---

## 🚀 **Getting Started Checklist**

### **✅ Setup Complete**
- [ ] Dependencies installed (`pip install requests numpy pandas`)
- [ ] Environment variables set (`GOLIATH_API_URL`)
- [ ] API server running (`http://localhost:8000`)

### **✅ Templates Tested**
- [ ] Lead scoring template working
- [ ] Energy optimization template working
- [ ] Portfolio optimization template working
- [ ] Financial planning template working
- [ ] Intelligence gathering template working

### **✅ Performance Validated**
- [ ] Quantum advantage > 10x achieved
- [ ] Response time < 100ms achieved
- [ ] All business pods operational

---

## 📚 **Next Steps**

1. **Customize Templates** - Adapt to your specific business needs
2. **Scale Operations** - Increase data volume and complexity
3. **Integrate Systems** - Connect with existing business tools
4. **Monitor Performance** - Track quantum advantage over time

---

*These templates provide a solid foundation for quantum-enhanced business intelligence. Customize and extend based on your specific requirements.*
