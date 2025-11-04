"""
Subscription Tier Definitions and Entitlement Resolution
"""

from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Entitlement:
    """Customer entitlement for a subscription tier"""
    tier: str
    agents: List[str]
    limits: Dict[str, Any]

# Subscription Tiers Configuration
TIERS = {
    "LaunchPad": {
        "name": "LaunchPad",
        "price": "/month",
        "agents": [
            "quantum_lead_qualifier",
            "quantum_chat_agent",
            "quantum_voice_assistant",
            "quantum_followup_specialist", 
            "lead_ingestion_engine"
        ],
        "limits": {
            "monthly_calls": 1000,
            "api_requests": 10000,
            "quantum_processing_hours": 10,
            "storage_gb": 10,
            "concurrent_users": 5
        },
        "features": [
            "Basic CRM integration",
            "Standard support",
            "Core analytics"
        ]
    },
    "ScaleUp": {
        "name": "ScaleUp",
        "price": "/month", 
        "agents": [
            "quantum_sales_navigator",
            "quantum_objection_handler",
            "quantum_demo_scheduler",
            "quantum_roi_calculator",
            "quantum_relationship_builder",
            "qsai_calling_agent"
        ],
        "limits": {
            "monthly_calls": 10000,
            "api_requests": 100000,
            "quantum_processing_hours": 100,
            "storage_gb": 100,
            "concurrent_users": 25
        },
        "features": [
            "Advanced CRM integration",
            "Priority support",
            "Advanced analytics",
            "White-label options"
        ]
    },
    "Enterprise": {
        "name": "Enterprise",
        "price": "+/year",
        "agents": [
            "quantum_closer",
            "quantum_pricing_negotiator", 
            "digital_human",
            "quantum_industry_expert",
            "quantum_competitive_analyzer",
            "sigma_select_agent",
            "goliath_energy_agent",
            "quantum_high_council"
        ],
        "limits": {
            "monthly_calls": "unlimited",
            "api_requests": "unlimited",
            "quantum_processing_hours": "unlimited", 
            "storage_gb": "unlimited",
            "concurrent_users": "unlimited"
        },
        "features": [
            "Full CRM integration",
            "24/7 dedicated support",
            "Custom quantum models",
            "Full white-label licensing",
            "SLA guarantees"
        ]
    }
}

def resolve_entitlement(tier: str) -> Entitlement:
    """
    Resolve customer entitlements based on subscription tier
    
    Args:
        tier: Subscription tier name
        
    Returns:
        Entitlement object with agents and limits
        
    Raises:
        ValueError: If tier is not valid
    """
    if tier not in TIERS:
        raise ValueError(f"Invalid tier: {tier}")
    
    tier_config = TIERS[tier]
    
    # Combine agents from current tier and all lower tiers
    all_agents = []
    
    if tier == "Enterprise":
        # Enterprise gets all agents
        all_agents = [
            # LaunchPad agents
            "quantum_lead_qualifier",
            "quantum_chat_agent", 
            "quantum_voice_assistant",
            "quantum_followup_specialist",
            "lead_ingestion_engine",
            # ScaleUp agents
            "quantum_sales_navigator",
            "quantum_objection_handler",
            "quantum_demo_scheduler", 
            "quantum_roi_calculator",
            "quantum_relationship_builder",
            "qsai_calling_agent",
            # Enterprise-only agents
            "quantum_closer",
            "quantum_pricing_negotiator",
            "digital_human",
            "quantum_industry_expert",
            "quantum_competitive_analyzer",
            "sigma_select_agent",
            "goliath_energy_agent",
            "quantum_high_council"
        ]
    elif tier == "ScaleUp":
        # ScaleUp gets LaunchPad + ScaleUp agents
        all_agents = [
            # LaunchPad agents
            "quantum_lead_qualifier",
            "quantum_chat_agent",
            "quantum_voice_assistant", 
            "quantum_followup_specialist",
            "lead_ingestion_engine",
            # ScaleUp agents
            "quantum_sales_navigator",
            "quantum_objection_handler",
            "quantum_demo_scheduler",
            "quantum_roi_calculator",
            "quantum_relationship_builder",
            "qsai_calling_agent"
        ]
    else:  # LaunchPad
        all_agents = tier_config["agents"]
    
    return Entitlement(
        tier=tier,
        agents=all_agents,
        limits=tier_config["limits"]
    )

def get_tier_by_agent(agent_id: str) -> str:
    """
    Get the minimum tier required for an agent
    
    Args:
        agent_id: Agent identifier
        
    Returns:
        Minimum tier name required for the agent
    """
    # LaunchPad agents
    launchpad_agents = [
        "quantum_lead_qualifier",
        "quantum_chat_agent",
        "quantum_voice_assistant",
        "quantum_followup_specialist",
        "lead_ingestion_engine"
    ]
    
    # ScaleUp agents
    scaleup_agents = [
        "quantum_sales_navigator",
        "quantum_objection_handler",
        "quantum_demo_scheduler",
        "quantum_roi_calculator",
        "quantum_relationship_builder",
        "qsai_calling_agent"
    ]
    
    # Enterprise agents
    enterprise_agents = [
        "quantum_closer",
        "quantum_pricing_negotiator",
        "digital_human",
        "quantum_industry_expert",
        "quantum_competitive_analyzer",
        "sigma_select_agent",
        "goliath_energy_agent",
        "quantum_high_council"
    ]
    
    if agent_id in launchpad_agents:
        return "LaunchPad"
    elif agent_id in scaleup_agents:
        return "ScaleUp"
    elif agent_id in enterprise_agents:
        return "Enterprise"
    else:
        return "Unknown"

def validate_agent_access(customer_tier: str, requested_agent: str) -> bool:
    """
    Validate if customer tier allows access to requested agent
    
    Args:
        customer_tier: Customer's subscription tier
        requested_agent: Agent being requested
        
    Returns:
        True if access is allowed, False otherwise
    """
    try:
        required_tier = get_tier_by_agent(requested_agent)
        
        # Define tier hierarchy
        tier_hierarchy = ["LaunchPad", "ScaleUp", "Enterprise"]
        
        customer_index = tier_hierarchy.index(customer_tier)
        required_index = tier_hierarchy.index(required_tier)
        
        return customer_index >= required_index
        
    except (ValueError, KeyError):
        return False

def get_upgrade_options(current_tier: str) -> List[str]:
    """
    Get available upgrade options for current tier
    
    Args:
        current_tier: Current subscription tier
        
    Returns:
        List of available upgrade tiers
    """
    upgrade_paths = {
        "LaunchPad": ["ScaleUp", "Enterprise"],
        "ScaleUp": ["Enterprise"],
        "Enterprise": []  # No upgrades available
    }
    
    return upgrade_paths.get(current_tier, [])

def calculate_tier_pricing(tier: str, billing_cycle: str = "monthly") -> Dict[str, Any]:
    """
    Calculate pricing for tier and billing cycle
    
    Args:
        tier: Subscription tier
        billing_cycle: "monthly" or "annual"
        
    Returns:
        Pricing information
    """
    base_prices = {
        "LaunchPad": {"monthly": 5000, "annual": 50000},  # 2 months free
        "ScaleUp": {"monthly": 15000, "annual": 150000},  # 2 months free
        "Enterprise": {"monthly": 83333, "annual": 1000000}  # Custom pricing
    }
    
    if tier not in base_prices:
        raise ValueError(f"Invalid tier: {tier}")
    
    monthly_price = base_prices[tier]["monthly"]
    annual_price = base_prices[tier]["annual"]
    
    if billing_cycle == "annual":
        savings = (monthly_price * 12) - annual_price
        return {
            "price": annual_price,
            "currency": "USD",
            "billing_cycle": "annual",
            "monthly_equivalent": annual_price / 12,
            "savings": savings,
            "savings_percentage": (savings / (monthly_price * 12)) * 100
        }
    else:
        return {
            "price": monthly_price,
            "currency": "USD", 
            "billing_cycle": "monthly"
        }
