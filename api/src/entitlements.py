from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel
from fastapi import HTTPException, status

class SubscriptionTier(str, Enum):
    """User subscription tiers with different feature access levels"""
    BASIC = "basic"
    PREMIUM = "premium"
    ELITE = "elite"
    ENTERPRISE = "enterprise"

class FeatureFlag(str, Enum):
    """Available features that can be gated by subscription tier"""
    DIGITAL_AVATAR = "digital_avatar"
    AI_CALLING_AGENT = "ai_calling_agent"
    QUANTUM_JOBS_BASIC = "quantum_jobs_basic"
    QUANTUM_JOBS_PREMIUM = "quantum_jobs_premium"
    QNEXUS_PREDICTIONS = "qnexus_predictions"
    ADVANCED_ANALYTICS = "advanced_analytics"
    CUSTOM_ALGORITHMS = "custom_algorithms"
    PRIORITY_SUPPORT = "priority_support"
    API_ACCESS = "api_access"
    BULK_OPERATIONS = "bulk_operations"
    WHITE_LABEL = "white_label"
    ENTERPRISE_INTEGRATIONS = "enterprise_integrations"

class EntitlementConfig(BaseModel):
    """Configuration for feature entitlements per subscription tier"""
    tier: SubscriptionTier
    features: List[FeatureFlag]
    quantum_job_limit: int
    api_rate_limit: int  # requests per minute
    storage_limit_gb: int
    support_level: str

# Feature entitlements configuration
ENTITLEMENT_CONFIG: Dict[SubscriptionTier, EntitlementConfig] = {
    SubscriptionTier.BASIC: EntitlementConfig(
        tier=SubscriptionTier.BASIC,
        features=[
            FeatureFlag.QUANTUM_JOBS_BASIC,
            FeatureFlag.API_ACCESS
        ],
        quantum_job_limit=10,
        api_rate_limit=60,
        storage_limit_gb=1,
        support_level="community"
    ),
    SubscriptionTier.PREMIUM: EntitlementConfig(
        tier=SubscriptionTier.PREMIUM,
        features=[
            FeatureFlag.DIGITAL_AVATAR,
            FeatureFlag.AI_CALLING_AGENT,
            FeatureFlag.QUANTUM_JOBS_BASIC,
            FeatureFlag.QUANTUM_JOBS_PREMIUM,
            FeatureFlag.QNEXUS_PREDICTIONS,
            FeatureFlag.ADVANCED_ANALYTICS,
            FeatureFlag.API_ACCESS
        ],
        quantum_job_limit=100,
        api_rate_limit=300,
        storage_limit_gb=10,
        support_level="email"
    ),
    SubscriptionTier.ELITE: EntitlementConfig(
        tier=SubscriptionTier.ELITE,
        features=[
            FeatureFlag.DIGITAL_AVATAR,
            FeatureFlag.AI_CALLING_AGENT,
            FeatureFlag.QUANTUM_JOBS_BASIC,
            FeatureFlag.QUANTUM_JOBS_PREMIUM,
            FeatureFlag.QNEXUS_PREDICTIONS,
            FeatureFlag.ADVANCED_ANALYTICS,
            FeatureFlag.CUSTOM_ALGORITHMS,
            FeatureFlag.PRIORITY_SUPPORT,
            FeatureFlag.API_ACCESS,
            FeatureFlag.BULK_OPERATIONS
        ],
        quantum_job_limit=1000,
        api_rate_limit=1000,
        storage_limit_gb=100,
        support_level="priority"
    ),
    SubscriptionTier.ENTERPRISE: EntitlementConfig(
        tier=SubscriptionTier.ENTERPRISE,
        features=list(FeatureFlag),  # All features
        quantum_job_limit=-1,  # Unlimited
        api_rate_limit=5000,
        storage_limit_gb=1000,
        support_level="dedicated"
    )
}

class EntitlementsEngine:
    """Engine for checking user entitlements and feature access"""
    
    def __init__(self):
        self.config = ENTITLEMENT_CONFIG
    
    def check_feature_access(self, user_tier: SubscriptionTier, feature: FeatureFlag) -> bool:
        """Check if user has access to a specific feature"""
        if user_tier not in self.config:
            return False
        
        return feature in self.config[user_tier].features
    
    def require_feature_access(self, user_tier: SubscriptionTier, feature: FeatureFlag) -> None:
        """Raise exception if user doesn't have access to feature"""
        if not self.check_feature_access(user_tier, feature):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "Feature access denied",
                    "feature": feature.value,
                    "current_tier": user_tier.value,
                    "required_tier": self._get_minimum_tier_for_feature(feature).value,
                    "upgrade_url": "/pricing"
                }
            )
    
    def get_user_entitlements(self, user_tier: SubscriptionTier) -> EntitlementConfig:
        """Get full entitlement configuration for user tier"""
        if user_tier not in self.config:
            return self.config[SubscriptionTier.BASIC]
        
        return self.config[user_tier]
    
    def check_quantum_job_limit(self, user_tier: SubscriptionTier, current_usage: int) -> bool:
        """Check if user can submit more quantum jobs"""
        entitlements = self.get_user_entitlements(user_tier)
        
        # -1 means unlimited
        if entitlements.quantum_job_limit == -1:
            return True
        
        return current_usage < entitlements.quantum_job_limit
    
    def check_api_rate_limit(self, user_tier: SubscriptionTier) -> int:
        """Get API rate limit for user tier"""
        entitlements = self.get_user_entitlements(user_tier)
        return entitlements.api_rate_limit
    
    def check_storage_limit(self, user_tier: SubscriptionTier, current_usage_gb: float) -> bool:
        """Check if user is within storage limits"""
        entitlements = self.get_user_entitlements(user_tier)
        return current_usage_gb <= entitlements.storage_limit_gb
    
    def _get_minimum_tier_for_feature(self, feature: FeatureFlag) -> SubscriptionTier:
        """Get the minimum subscription tier required for a feature"""
        for tier in [SubscriptionTier.BASIC, SubscriptionTier.PREMIUM, 
                    SubscriptionTier.ELITE, SubscriptionTier.ENTERPRISE]:
            if feature in self.config[tier].features:
                return tier
        
        return SubscriptionTier.ENTERPRISE
    
    def get_upgrade_suggestions(self, user_tier: SubscriptionTier, requested_feature: FeatureFlag) -> Dict:
        """Get upgrade suggestions for accessing a feature"""
        if self.check_feature_access(user_tier, requested_feature):
            return {"upgrade_needed": False}
        
        minimum_tier = self._get_minimum_tier_for_feature(requested_feature)
        current_config = self.get_user_entitlements(user_tier)
        target_config = self.get_user_entitlements(minimum_tier)
        
        return {
            "upgrade_needed": True,
            "current_tier": user_tier.value,
            "recommended_tier": minimum_tier.value,
            "current_features": [f.value for f in current_config.features],
            "new_features": [f.value for f in target_config.features if f not in current_config.features],
            "benefits": {
                "quantum_jobs": f"{target_config.quantum_job_limit} vs {current_config.quantum_job_limit}",
                "api_rate_limit": f"{target_config.api_rate_limit} vs {current_config.api_rate_limit}",
                "storage": f"{target_config.storage_limit_gb}GB vs {current_config.storage_limit_gb}GB",
                "support": f"{target_config.support_level} vs {current_config.support_level}"
            }
        }

# Global entitlements engine instance
entitlements_engine = EntitlementsEngine()

# Dependency for FastAPI routes
def get_entitlements_engine() -> EntitlementsEngine:
    return entitlements_engine