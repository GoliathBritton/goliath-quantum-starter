"""
NQBA Stack Business Pods
The three core business implementations powered by the NQBA Stack

Business Pods:
- FLYFOX AI: Industrial AI solutions and energy optimization
- Goliath Trade: Quantum finance and DeFi optimization  
- Sigma Select: Sales intelligence and lead optimization
"""

# FLYFOX AI Pod - Industrial AI Solutions
FLYFOX_AI_POD = {
    "pod_id": "flyfox_ai",
    "name": "FLYFOX AI",
    "description": "AIaaS Marketplace Pod - Industrial AI Solutions",
    "capabilities": [
        "energy_optimization",
        "quality_enhancement", 
        "production_maximization",
        "uptime_optimization",
        "asset_guardian",
        "operations_hub"
    ],
    "qubo_problems": [
        "energy_scheduling",
        "equipment_optimization",
        "quality_control",
        "production_scheduling",
        "maintenance_optimization"
    ],
    "solutions": [
        "FLYFOX Energy Optimizer",
        "FLYFOX Quality Enhancer",
        "FLYFOX Production Maximizer",
        "FLYFOX Uptime Booster",
        "FLYFOX Asset Guardian",
        "FLYFOX Operations Hub"
    ]
}

# Goliath Trade Pod - Quantum Finance & Energy Trading
GOLIATH_TRADE_POD = {
    "pod_id": "goliath_trade",
    "name": "Goliath of All Trade",
    "description": "Quantum Finance Pod - DeFi & Energy Trading",
    "capabilities": [
        "portfolio_optimization",
        "risk_assessment",
        "energy_trading",
        "defi_optimization",
        "blockchain_analytics",
        "nft_optimization"
    ],
    "qubo_problems": [
        "portfolio_allocation",
        "risk_optimization",
        "energy_scheduling",
        "defi_yield_optimization",
        "gas_optimization",
        "liquidity_optimization"
    ],
    "solutions": [
        "Goliath Trade Energy",
        "Goliath Business Funding",
        "Goliath DeFi Optimizer",
        "Goliath Portfolio Manager",
        "Goliath Risk Assessor"
    ]
}

# Sigma Select Pod - Sales Intelligence
SIGMA_SELECT_POD = {
    "pod_id": "sigma_select",
    "name": "Sigma Select",
    "description": "Sales Intelligence Pod - Lead Scoring & Optimization",
    "capabilities": [
        "lead_scoring",
        "sales_optimization",
        "customer_segmentation",
        "next_best_action",
        "sales_route_optimization",
        "customer_lifetime_value"
    ],
    "qubo_problems": [
        "lead_prioritization",
        "sales_route_optimization",
        "customer_lifetime_value",
        "sales_territory_optimization",
        "commission_optimization"
    ],
    "solutions": [
        "Sigma Select Training & Consulting",
        "Sigma Select Lead Optimizer",
        "Sigma Select Sales Intelligence",
        "Sigma Select Customer Analytics",
        "Sigma Select Performance Dashboard"
    ]
}

# All business pods
BUSINESS_PODS = {
    "flyfox_ai": FLYFOX_AI_POD,
    "goliath_trade": GOLIATH_TRADE_POD,
    "sigma_select": SIGMA_SELECT_POD
}

def get_business_pod(pod_id: str):
    """Get business pod configuration by ID"""
    return BUSINESS_PODS.get(pod_id)

def get_all_business_pods():
    """Get all business pod configurations"""
    return BUSINESS_PODS

def get_pod_capabilities(pod_id: str):
    """Get capabilities for a specific business pod"""
    pod = get_business_pod(pod_id)
    return pod.get("capabilities", []) if pod else []

def get_pod_qubo_problems(pod_id: str):
    """Get QUBO problems for a specific business pod"""
    pod = get_business_pod(pod_id)
    return pod.get("qubo_problems", []) if pod else []

def get_pod_solutions(pod_id: str):
    """Get solutions for a specific business pod"""
    pod = get_business_pod(pod_id)
    return pod.get("solutions", []) if pod else []

__all__ = [
    "FLYFOX_AI_POD",
    "GOLIATH_TRADE_POD", 
    "SIGMA_SELECT_POD",
    "BUSINESS_PODS",
    "get_business_pod",
    "get_all_business_pods",
    "get_pod_capabilities",
    "get_pod_qubo_problems",
    "get_pod_solutions"
]
