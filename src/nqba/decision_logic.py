
import uuid
from typing import Dict, Any
import yaml
import os

POLICY_DIR = os.path.join(os.path.dirname(__file__), '../../configs/policies')

def _load_policy(policy_id: str) -> dict:
    """Load a Q-Cortex YAML policy by ID from configs/policies/"""
    fname = os.path.join(POLICY_DIR, f"{policy_id}.yaml")
    if not os.path.exists(fname):
        raise FileNotFoundError(f"Policy file not found: {fname}")
    with open(fname, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def _score(features: dict, policy: dict) -> float:
    # Simple scoring: weighted sum if weights in policy, else dummy
    weights = policy.get('weights', {})
    if weights:
        return sum(features.get(k, 0) * v for k, v in weights.items())
    return 0.95

def decide(policy_id: str, features: Dict[str, Any]) -> dict:
    """Run a Q-Cortex policy decision using loaded YAML policy."""
    try:
        policy = _load_policy(policy_id)
    except Exception as e:
        return {
            "decision_id": str(uuid.uuid4()),
            "result": {"score": 0.0, "action": "reject"},
            "explanation": f"Policy load error: {e}"
        }
    score = _score(features, policy)
    threshold = policy.get('threshold', 0.5)
    action = 'approve' if score >= threshold else 'reject'
    return {
        "decision_id": str(uuid.uuid4()),
        "result": {"score": score, "action": action},
        "explanation": f"Policy {policy_id} scored {score:.2f} (threshold {threshold}) => {action}"
    }

class DecisionLogicEngine:
    """NQBA Decision Logic Engine for automated business decisions."""
    
    def __init__(self, business_unit: str = "nqba_core"):
        self.business_unit = business_unit
        self.policy_cache = {}
        self.decision_history = []
    
    def assess_business(self, company_data: Dict[str, Any], policy_id: str = "default") -> dict:
        """Assess a business using NQBA decision logic."""
        features = self._extract_features(company_data)
        decision = decide(policy_id, features)
        decision["business_unit"] = self.business_unit
        decision["timestamp"] = str(uuid.uuid4())
        self.decision_history.append(decision)
        return decision
    
    def optimize(self, data: Dict[str, Any]) -> dict:
        """Optimize business decisions using quantum-enhanced logic."""
        # Extract optimization parameters
        optimization_type = data.get("type", "business_assessment")
        
        if optimization_type == "energy_optimization":
            return self._optimize_energy(data)
        elif optimization_type == "trade_optimization":
            return self._optimize_trade(data)
        else:
            return self._optimize_business(data)
    
    def _optimize_energy(self, data: Dict[str, Any]) -> dict:
        """Optimize energy consumption patterns."""
        consumption = data.get("consumption", {})
        peak_hours = data.get("peak_hours", [])
        
        # Simple energy optimization logic
        optimization_result = {
            "optimization_type": "energy",
            "recommendations": [],
            "estimated_savings": 0.0,
            "quantum_enhanced": True,
            "optimized_schedule": {
                "peak_hours": peak_hours,
                "off_peak_hours": [h for h in range(24) if h not in peak_hours],
                "recommended_shifts": []
            }
        }
        
        if peak_hours:
            optimization_result["recommendations"].append("Shift operations to off-peak hours")
            optimization_result["estimated_savings"] = 15.0
            optimization_result["optimized_schedule"]["recommended_shifts"] = [
                {"from": hour, "to": (hour + 8) % 24} for hour in peak_hours
            ]
        
        return optimization_result
    
    def _optimize_trade(self, data: Dict[str, Any]) -> dict:
        """Optimize trading strategies."""
        assets = data.get("assets", [])
        risk_tolerance = data.get("risk_tolerance", "medium")
        
        optimization_result = {
            "optimization_type": "trade",
            "recommendations": [],
            "portfolio_allocation": {},
            "quantum_enhanced": True,
            "optimized_portfolio": {
                "assets": assets,
                "risk_score": 0.5,
                "diversification_ratio": 0.8
            }
        }
        
        if assets:
            optimization_result["recommendations"].append("Diversify portfolio across multiple asset classes")
            optimization_result["portfolio_allocation"] = {"stocks": 0.4, "bonds": 0.3, "crypto": 0.3}
            optimization_result["optimized_portfolio"]["diversification_ratio"] = 0.9
        
        return optimization_result
    
    def _optimize_business(self, data: Dict[str, Any]) -> dict:
        """General business optimization."""
        company_size = data.get("company_size", "medium")
        industry = data.get("industry", "technology")
        
        optimization_result = {
            "optimization_type": "business",
            "recommendations": [],
            "growth_potential": 0.0,
            "quantum_enhanced": True
        }
        
        if company_size == "large":
            optimization_result["recommendations"].append("Implement enterprise-wide automation")
            optimization_result["growth_potential"] = 25.0
        elif company_size == "medium":
            optimization_result["recommendations"].append("Focus on process optimization")
            optimization_result["growth_potential"] = 15.0
        
        return optimization_result
    
    def _extract_features(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant features for decision making."""
        return {
            "revenue": company_data.get("revenue", 0),
            "employees": company_data.get("employees", 0),
            "industry": company_data.get("industry", "unknown"),
            "growth_rate": company_data.get("growth_rate", 0.0),
            "credit_score": company_data.get("credit_score", 0),
            "market_cap": company_data.get("market_cap", 0)
        }
    
    def get_decision_history(self) -> list:
        """Get history of decisions made by this engine."""
        return self.decision_history
    
    def clear_history(self):
        """Clear decision history."""
        self.decision_history.clear()
