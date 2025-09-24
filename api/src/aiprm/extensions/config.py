"""
Goliath of All Trade - AIPRM Extensions Configuration
This module provides configuration for AIPRM extensions.
"""

from typing import Dict, List, Any

# Extension configuration
EXTENSION_CONFIG = {
    "quantum_prompt_enhancer": {
        "name": "Quantum Prompt Enhancer",
        "description": "Enhances prompts with quantum computing concepts",
        "version": "1.0.0",
        "author": "Goliath AI",
        "enabled_by_default": True,
        "compatibility": ["default", "quantum"],
        "settings": {
            "enhancement_level": "advanced",
            "include_quantum_examples": True,
            "auto_optimize": True
        }
    },
    "energy_domain_knowledge": {
        "name": "Energy Domain Knowledge",
        "description": "Adds energy domain knowledge to prompt responses",
        "version": "1.0.0",
        "author": "Goliath AI",
        "enabled_by_default": True,
        "compatibility": ["default", "energy"],
        "settings": {
            "include_renewable_data": True,
            "grid_optimization_focus": True,
            "energy_market_insights": True
        }
    },
    "financial_analysis_tools": {
        "name": "Financial Analysis Tools",
        "description": "Adds financial analysis capabilities to prompts",
        "version": "1.0.0",
        "author": "Goliath AI",
        "enabled_by_default": True,
        "compatibility": ["default", "finance"],
        "settings": {
            "risk_assessment_level": "comprehensive",
            "include_market_trends": True,
            "portfolio_optimization": True
        }
    },
    "diversegy_integration": {
        "name": "Diversegy Integration Extension",
        "description": "Enhances prompts with Diversegy energy partner data",
        "version": "1.0.0",
        "author": "Goliath of All Trade",
        "enabled_by_default": True,
        "compatibility": ["default", "energy", "partners"],
        "settings": {
            "include_partner_data": True,
            "energy_plan_recommendations": True,
            "commission_optimization": True
        }
    },
    "prompt_library": {
        "name": "Prompt Library",
        "description": "Access to a library of pre-built prompts for various use cases",
        "version": "1.0.0",
        "author": "Goliath AI",
        "enabled_by_default": True,
        "compatibility": ["default", "all"],
        "settings": {
            "auto_suggest_prompts": True,
            "enable_community_prompts": True,
            "enable_custom_collections": True
        }
    }
}

# Default extension settings
DEFAULT_EXTENSION_SETTINGS = {
    "auto_update": True,
    "telemetry": False,
    "usage_tracking": False
}