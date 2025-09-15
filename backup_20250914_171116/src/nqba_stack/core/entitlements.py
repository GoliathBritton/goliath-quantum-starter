"""
NQBA Entitlements Engine - Centralized Tiering & Gating System

This module provides the core entitlements system for the NQBA ecosystem,
enabling tier-based access control across all business units and features.
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class Tier(Enum):
    """Available subscription tiers"""

    FREE = "free"
    BUSINESS = "business"
    PREMIUM = "premium"
    LUXURY = "luxury"


class Feature(Enum):
    """Available features that can be gated by tier"""

    # Core Platform Features
    BASIC_OPTIMIZATION = "basic_optimization"
    ADVANCED_OPTIMIZATION = "advanced_optimization"
    QUANTUM_OPTIMIZATION = "quantum_optimization"

    # Business Unit Access
    FLYFOX_AI_ACCESS = "flyfox_ai_access"
    GOLIATH_TRADE_ACCESS = "goliath_trade_access"
    SIGMA_SELECT_ACCESS = "sigma_select_access"

    # Marketplace Features
    MARKETPLACE_ACCESS = "marketplace_access"
    POD_INSTALLATION = "pod_installation"
    CUSTOM_PODS = "custom_pods"

    # Advanced Features
    DIGITAL_TWIN = "digital_twin"
    QUANTUM_CERTIFICATION = "quantum_certification"
    ESG_ENGINE = "esg_engine"
    M_A_ANALYTICS = "m_a_analytics"

    # API & Integration
    API_ACCESS = "api_access"
    WEBHOOKS = "webhooks"
    BULK_OPERATIONS = "bulk_operations"

    # Support & Services
    BASIC_SUPPORT = "basic_support"
    PRIORITY_SUPPORT = "priority_support"
    DEDICATED_ACCOUNT_MANAGER = "dedicated_account_manager"
    WHITE_GLOVE_SERVICE = "white_glove_service"


@dataclass
class TierLimits:
    """Limits and quotas for each tier"""

    max_optimizations_per_month: int
    max_api_calls_per_day: int
    max_storage_gb: int
    max_users: int
    max_projects: int
    support_response_hours: int
    custom_branding: bool
    sso_integration: bool
    advanced_analytics: bool
    quantum_advantage_tracking: bool


@dataclass
class UserEntitlements:
    """User's current entitlements and usage"""

    user_id: str
    tier: Tier
    features: Set[Feature] = field(default_factory=set)
    usage: Dict[str, int] = field(default_factory=dict)
    limits: TierLimits = None
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class EntitlementsEngine:
    """
    Centralized entitlements engine for the NQBA ecosystem.

    Handles tier-based access control, feature gating, and usage tracking
    across all business units and platform features.
    """

    def __init__(self):
        self._tier_configs: Dict[Tier, Dict[str, Any]] = {}
        self._feature_mappings: Dict[Feature, Set[Tier]] = {}
        self._user_entitlements: Dict[str, UserEntitlements] = {}
        self._usage_trackers: Dict[str, Any] = {}

        self._initialize_tier_configs()
        self._initialize_feature_mappings()

    def _initialize_tier_configs(self):
        """Initialize tier configurations with limits and features"""
        self._tier_configs = {
            Tier.FREE: {
                "name": "Free",
                "price": 0,
                "limits": TierLimits(
                    max_optimizations_per_month=10,
                    max_api_calls_per_day=100,
                    max_storage_gb=1,
                    max_users=1,
                    max_projects=3,
                    support_response_hours=48,
                    custom_branding=False,
                    sso_integration=False,
                    advanced_analytics=False,
                    quantum_advantage_tracking=False,
                ),
                "features": {
                    Feature.BASIC_OPTIMIZATION,
                    Feature.API_ACCESS,
                    Feature.BASIC_SUPPORT,
                },
            },
            Tier.BUSINESS: {
                "name": "Business",
                "price": 299,
                "limits": TierLimits(
                    max_optimizations_per_month=1000,
                    max_api_calls_per_day=10000,
                    max_storage_gb=100,
                    max_users=10,
                    max_projects=50,
                    support_response_hours=24,
                    custom_branding=True,
                    sso_integration=False,
                    advanced_analytics=True,
                    quantum_advantage_tracking=True,
                ),
                "features": {
                    Feature.BASIC_OPTIMIZATION,
                    Feature.ADVANCED_OPTIMIZATION,
                    Feature.FLYFOX_AI_ACCESS,
                    Feature.GOLIATH_TRADE_ACCESS,
                    Feature.SIGMA_SELECT_ACCESS,
                    Feature.API_ACCESS,
                    Feature.WEBHOOKS,
                    Feature.BASIC_SUPPORT,
                    Feature.PRIORITY_SUPPORT,
                },
            },
            Tier.PREMIUM: {
                "name": "Premium",
                "price": 999,
                "limits": TierLimits(
                    max_optimizations_per_month=10000,
                    max_api_calls_per_day=100000,
                    max_storage_gb=1000,
                    max_users=100,
                    max_projects=500,
                    support_response_hours=8,
                    custom_branding=True,
                    sso_integration=True,
                    advanced_analytics=True,
                    quantum_advantage_tracking=True,
                ),
                "features": {
                    Feature.BASIC_OPTIMIZATION,
                    Feature.ADVANCED_OPTIMIZATION,
                    Feature.QUANTUM_OPTIMIZATION,
                    Feature.FLYFOX_AI_ACCESS,
                    Feature.GOLIATH_TRADE_ACCESS,
                    Feature.SIGMA_SELECT_ACCESS,
                    Feature.MARKETPLACE_ACCESS,
                    Feature.POD_INSTALLATION,
                    Feature.DIGITAL_TWIN,
                    Feature.API_ACCESS,
                    Feature.WEBHOOKS,
                    Feature.BULK_OPERATIONS,
                    Feature.PRIORITY_SUPPORT,
                    Feature.DEDICATED_ACCOUNT_MANAGER,
                },
            },
            Tier.LUXURY: {
                "name": "Luxury",
                "price": 2999,
                "limits": TierLimits(
                    max_optimizations_per_month=100000,
                    max_api_calls_per_day=1000000,
                    max_storage_gb=10000,
                    max_users=1000,
                    max_projects=5000,
                    support_response_hours=2,
                    custom_branding=True,
                    sso_integration=True,
                    advanced_analytics=True,
                    quantum_advantage_tracking=True,
                ),
                "features": {
                    Feature.BASIC_OPTIMIZATION,
                    Feature.ADVANCED_OPTIMIZATION,
                    Feature.QUANTUM_OPTIMIZATION,
                    Feature.FLYFOX_AI_ACCESS,
                    Feature.GOLIATH_TRADE_ACCESS,
                    Feature.SIGMA_SELECT_ACCESS,
                    Feature.MARKETPLACE_ACCESS,
                    Feature.POD_INSTALLATION,
                    Feature.CUSTOM_PODS,
                    Feature.DIGITAL_TWIN,
                    Feature.QUANTUM_CERTIFICATION,
                    Feature.ESG_ENGINE,
                    Feature.M_A_ANALYTICS,
                    Feature.API_ACCESS,
                    Feature.WEBHOOKS,
                    Feature.BULK_OPERATIONS,
                    Feature.PRIORITY_SUPPORT,
                    Feature.DEDICATED_ACCOUNT_MANAGER,
                    Feature.WHITE_GLOVE_SERVICE,
                },
            },
        }

    def _initialize_feature_mappings(self):
        """Initialize which features are available at which tiers"""
        for tier, config in self._tier_configs.items():
            for feature in config["features"]:
                if feature not in self._feature_mappings:
                    self._feature_mappings[feature] = set()
                self._feature_mappings[feature].add(tier)

    def get_user_entitlements(self, user_id: str) -> Optional[UserEntitlements]:
        """Get current entitlements for a user"""
        return self._user_entitlements.get(user_id)

    def set_user_tier(
        self, user_id: str, tier: Tier, expires_at: Optional[datetime] = None
    ):
        """Set or update a user's tier"""
        if user_id not in self._user_entitlements:
            self._user_entitlements[user_id] = UserEntitlements(
                user_id=user_id, tier=tier
            )

        user_ent = self._user_entitlements[user_id]
        user_ent.tier = tier
        user_ent.features = self._tier_configs[tier]["features"].copy()
        user_ent.limits = self._tier_configs[tier]["limits"]
        user_ent.expires_at = expires_at
        user_ent.updated_at = datetime.utcnow()

        logger.info(f"Updated user {user_id} to {tier.value} tier")

    def has_feature_access(self, user_id: str, feature: Feature) -> bool:
        """Check if a user has access to a specific feature"""
        user_ent = self.get_user_entitlements(user_id)
        if not user_ent:
            return False

        # Check if feature is available at user's tier
        if feature not in user_ent.features:
            return False

        # Check if user's tier has expired
        if user_ent.expires_at and datetime.utcnow() > user_ent.expires_at:
            logger.warning(f"User {user_id} tier has expired")
            return False

        return True

    def check_usage_limit(
        self, user_id: str, limit_type: str, current_usage: int
    ) -> bool:
        """Check if a user is within their usage limits"""
        user_ent = self.get_user_entitlements(user_id)
        if not user_ent or not user_ent.limits:
            return False

        # Map limit types to TierLimits attributes
        limit_mapping = {
            "optimizations_per_month": user_ent.limits.max_optimizations_per_month,
            "api_calls_per_day": user_ent.limits.max_api_calls_per_day,
            "storage_gb": user_ent.limits.max_storage_gb,
            "users": user_ent.limits.max_users,
            "projects": user_ent.limits.max_projects,
        }

        limit = limit_mapping.get(limit_type)
        if limit is None:
            logger.warning(f"Unknown limit type: {limit_type}")
            return False

        return current_usage < limit

    def get_tier_info(self, tier: Tier) -> Dict[str, Any]:
        """Get information about a specific tier"""
        return self._tier_configs.get(tier, {})

    def get_available_tiers(self) -> List[Tier]:
        """Get list of all available tiers"""
        return list(self._tier_configs.keys())

    def get_feature_tiers(self, feature: Feature) -> Set[Tier]:
        """Get which tiers have access to a specific feature"""
        return self._feature_mappings.get(feature, set())

    def upgrade_user_tier(
        self, user_id: str, new_tier: Tier, expires_at: Optional[datetime] = None
    ):
        """Upgrade a user to a higher tier"""
        current_ent = self.get_user_entitlements(user_id)
        if not current_ent:
            raise ValueError(f"User {user_id} not found")

        current_tier_value = self._get_tier_numeric_value(current_ent.tier)
        new_tier_value = self._get_tier_numeric_value(new_tier)

        if new_tier_value <= current_tier_value:
            raise ValueError(
                f"Cannot upgrade to {new_tier.value} from {current_ent.tier.value}"
            )

        self.set_user_tier(user_id, new_tier, expires_at)
        logger.info(
            f"Upgraded user {user_id} from {current_ent.tier.value} to {new_tier.value}"
        )

    def _get_tier_numeric_value(self, tier: Tier) -> int:
        """Get numeric value for tier comparison"""
        tier_values = {Tier.FREE: 0, Tier.BUSINESS: 1, Tier.PREMIUM: 2, Tier.LUXURY: 3}
        return tier_values.get(tier, 0)

    def get_user_usage_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive usage summary for a user"""
        user_ent = self.get_user_entitlements(user_id)
        if not user_ent:
            return {}

        return {
            "user_id": user_id,
            "tier": user_ent.tier.value,
            "tier_name": self._tier_configs[user_ent.tier]["name"],
            "features": [f.value for f in user_ent.features],
            "usage": user_ent.usage,
            "limits": {
                "max_optimizations_per_month": user_ent.limits.max_optimizations_per_month,
                "max_api_calls_per_day": user_ent.limits.max_api_calls_per_day,
                "max_storage_gb": user_ent.limits.max_storage_gb,
                "max_users": user_ent.limits.max_users,
                "max_projects": user_ent.limits.max_projects,
            },
            "expires_at": (
                user_ent.expires_at.isoformat() if user_ent.expires_at else None
            ),
            "created_at": user_ent.created_at.isoformat(),
            "updated_at": user_ent.updated_at.isoformat(),
        }

    def export_entitlements_config(self) -> Dict[str, Any]:
        """Export current entitlements configuration for backup/analysis"""
        return {
            "tier_configs": {
                tier.value: {
                    "name": config["name"],
                    "price": config["price"],
                    "features": [f.value for f in config["features"]],
                }
                for tier, config in self._tier_configs.items()
            },
            "feature_mappings": {
                feature.value: [tier.value for tier in tiers]
                for feature, tiers in self._feature_mappings.items()
            },
            "user_count": len(self._user_entitlements),
            "exported_at": datetime.utcnow().isoformat(),
        }


# Global entitlements engine instance
entitlements_engine = EntitlementsEngine()


def get_entitlements_engine() -> EntitlementsEngine:
    """Get the global entitlements engine instance"""
    return entitlements_engine


def require_feature(feature: Feature):
    """
    Decorator to require a specific feature for API endpoints

    Usage:
        @require_feature(Feature.QUANTUM_OPTIMIZATION)
        async def quantum_optimization_endpoint(user_id: str):
            # Only users with quantum optimization access can reach here
            pass
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract user_id from args or kwargs
            user_id = None
            if "user_id" in kwargs:
                user_id = kwargs["user_id"]
            elif args and len(args) > 0:
                # Assume first argument might be user_id
                user_id = args[0]

            if not user_id:
                raise ValueError(
                    "user_id parameter required for feature-gated endpoints"
                )

            if not entitlements_engine.has_feature_access(user_id, feature):
                raise PermissionError(
                    f"Feature {feature.value} not available for user {user_id}"
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def check_usage_limit(user_id: str, limit_type: str, current_usage: int) -> bool:
    """Check if a user is within their usage limits"""
    return entitlements_engine.check_usage_limit(user_id, limit_type, current_usage)


def get_user_tier(user_id: str) -> Optional[Tier]:
    """Get the current tier for a user"""
    user_ent = entitlements_engine.get_user_entitlements(user_id)
    return user_ent.tier if user_ent else None
