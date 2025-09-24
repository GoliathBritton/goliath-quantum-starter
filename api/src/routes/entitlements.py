from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any, List
from src.models import User
from src.entitlements import (
    EntitlementsEngine, 
    SubscriptionTier, 
    FeatureFlag, 
    EntitlementConfig,
    get_entitlements_engine
)
from src.middleware.entitlements_middleware import get_current_user, rate_limit_middleware
from pydantic import BaseModel

router = APIRouter(prefix="/entitlements", tags=["entitlements"])

class FeatureAccessRequest(BaseModel):
    feature: FeatureFlag

class UpgradeQuoteRequest(BaseModel):
    target_tier: SubscriptionTier

class UsageStats(BaseModel):
    quantum_jobs_used: int
    quantum_jobs_limit: int
    storage_used_gb: float
    storage_limit_gb: int
    api_requests_today: int
    api_rate_limit: int

@router.get("/my-entitlements", response_model=EntitlementConfig)
async def get_my_entitlements(
    user: User = Depends(get_current_user),
    entitlements: EntitlementsEngine = Depends(get_entitlements_engine)
):
    """Get current user's entitlements and feature access"""
    return entitlements.get_user_entitlements(user.subscription_tier)

@router.post("/check-feature-access")
async def check_feature_access(
    request: FeatureAccessRequest,
    user: User = Depends(get_current_user),
    entitlements: EntitlementsEngine = Depends(get_entitlements_engine)
):
    """Check if user has access to a specific feature"""
    has_access = entitlements.check_feature_access(user.subscription_tier, request.feature)
    
    if not has_access:
        upgrade_info = entitlements.get_upgrade_suggestions(user.subscription_tier, request.feature)
        return {
            "has_access": False,
            "upgrade_info": upgrade_info
        }
    
    return {
        "has_access": True,
        "feature": request.feature.value
    }

@router.get("/usage-stats", response_model=UsageStats)
async def get_usage_stats(
    user: User = Depends(get_current_user),
    entitlements: EntitlementsEngine = Depends(get_entitlements_engine)
):
    """Get current usage statistics for the user"""
    user_entitlements = entitlements.get_user_entitlements(user.subscription_tier)
    rate_info = await rate_limit_middleware.get_rate_limit_info(user.id, user.subscription_tier)
    
    return UsageStats(
        quantum_jobs_used=user.quantum_jobs_used,
        quantum_jobs_limit=user_entitlements.quantum_job_limit,
        storage_used_gb=user.storage_used_gb,
        storage_limit_gb=user_entitlements.storage_limit_gb,
        api_requests_today=rate_info["current_usage"],
        api_rate_limit=user_entitlements.api_rate_limit
    )

@router.get("/available-features")
async def get_available_features(
    user: User = Depends(get_current_user),
    entitlements: EntitlementsEngine = Depends(get_entitlements_engine)
):
    """Get all available features and user's access status"""
    user_entitlements = entitlements.get_user_entitlements(user.subscription_tier)
    
    features_status = {}
    for feature in FeatureFlag:
        has_access = feature in user_entitlements.features
        features_status[feature.value] = {
            "has_access": has_access,
            "description": _get_feature_description(feature)
        }
        
        if not has_access:
            upgrade_info = entitlements.get_upgrade_suggestions(user.subscription_tier, feature)
            features_status[feature.value]["upgrade_info"] = upgrade_info
    
    return {
        "current_tier": user.subscription_tier.value,
        "features": features_status
    }

@router.post("/upgrade-quote")
async def get_upgrade_quote(
    request: UpgradeQuoteRequest,
    user: User = Depends(get_current_user),
    entitlements: EntitlementsEngine = Depends(get_entitlements_engine)
):
    """Get upgrade quote and benefits comparison"""
    if request.target_tier == user.subscription_tier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Target tier is the same as current tier"
        )
    
    current_config = entitlements.get_user_entitlements(user.subscription_tier)
    target_config = entitlements.get_user_entitlements(request.target_tier)
    
    # Calculate new features
    new_features = [f for f in target_config.features if f not in current_config.features]
    
    # Mock pricing - in real implementation, integrate with billing system
    pricing = _get_tier_pricing(request.target_tier)
    
    return {
        "current_tier": user.subscription_tier.value,
        "target_tier": request.target_tier.value,
        "pricing": pricing,
        "new_features": [f.value for f in new_features],
        "benefits_comparison": {
            "quantum_jobs": {
                "current": current_config.quantum_job_limit,
                "new": target_config.quantum_job_limit
            },
            "api_rate_limit": {
                "current": current_config.api_rate_limit,
                "new": target_config.api_rate_limit
            },
            "storage_gb": {
                "current": current_config.storage_limit_gb,
                "new": target_config.storage_limit_gb
            },
            "support_level": {
                "current": current_config.support_level,
                "new": target_config.support_level
            }
        },
        "upgrade_url": f"/billing/upgrade?tier={request.target_tier.value}"
    }

@router.get("/tier-comparison")
async def get_tier_comparison(
    entitlements: EntitlementsEngine = Depends(get_entitlements_engine)
):
    """Get comparison of all subscription tiers"""
    comparison = {}
    
    for tier in SubscriptionTier:
        config = entitlements.get_user_entitlements(tier)
        comparison[tier.value] = {
            "features": [f.value for f in config.features],
            "quantum_job_limit": config.quantum_job_limit,
            "api_rate_limit": config.api_rate_limit,
            "storage_limit_gb": config.storage_limit_gb,
            "support_level": config.support_level,
            "pricing": _get_tier_pricing(tier)
        }
    
    return comparison

def _get_feature_description(feature: FeatureFlag) -> str:
    """Get human-readable description for features"""
    descriptions = {
        FeatureFlag.DIGITAL_AVATAR: "AI-powered digital human avatars for customer interactions",
        FeatureFlag.AI_CALLING_AGENT: "Automated AI calling system for lead generation and customer outreach",
        FeatureFlag.QUANTUM_JOBS_BASIC: "Basic quantum computing jobs for optimization problems",
        FeatureFlag.QUANTUM_JOBS_PREMIUM: "Advanced quantum computing with priority processing",
        FeatureFlag.QNEXUS_PREDICTIONS: "Q-Nexus AI predictions and business intelligence insights",
        FeatureFlag.ADVANCED_ANALYTICS: "Deep analytics and performance metrics dashboard",
        FeatureFlag.CUSTOM_ALGORITHMS: "Custom quantum algorithms and business logic",
        FeatureFlag.PRIORITY_SUPPORT: "Priority customer support with dedicated assistance",
        FeatureFlag.API_ACCESS: "RESTful API access for integration and automation",
        FeatureFlag.BULK_OPERATIONS: "Bulk processing and batch operations",
        FeatureFlag.WHITE_LABEL: "White-label solutions and custom branding",
        FeatureFlag.ENTERPRISE_INTEGRATIONS: "Enterprise system integrations (SAP, Salesforce, etc.)"
    }
    return descriptions.get(feature, "Advanced feature")

def _get_tier_pricing(tier: SubscriptionTier) -> Dict[str, Any]:
    """Get pricing information for subscription tiers"""
    pricing = {
        SubscriptionTier.BASIC: {
            "monthly": 0,
            "annual": 0,
            "currency": "USD",
            "billing_cycle": "free"
        },
        SubscriptionTier.PREMIUM: {
            "monthly": 99,
            "annual": 990,
            "currency": "USD",
            "billing_cycle": "monthly",
            "savings_annual": "2 months free"
        },
        SubscriptionTier.ELITE: {
            "monthly": 299,
            "annual": 2990,
            "currency": "USD",
            "billing_cycle": "monthly",
            "savings_annual": "2 months free"
        },
        SubscriptionTier.ENTERPRISE: {
            "monthly": "Custom",
            "annual": "Custom",
            "currency": "USD",
            "billing_cycle": "custom",
            "contact_sales": True
        }
    }
    return pricing.get(tier, {})