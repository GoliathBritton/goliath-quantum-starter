"""
Entitlements Engine - Manages tiered access control for the NQBA ecosystem.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from enum import Enum

logger = logging.getLogger(__name__)


class Tier(Enum):
    """Available subscription tiers."""

    FREE = "FREE"
    BUSINESS = "BUSINESS"
    PREMIUM = "PREMIUM"
    LUXURY = "LUXURY"


class Feature(Enum):
    """Available features that can be gated."""

    BASIC_OPTIMIZATION = "basic_optimization"
    ADVANCED_OPTIMIZATION = "advanced_optimization"
    QUANTUM_OPTIMIZATION = "quantum_optimization"
    STANDARD_REPORTS = "standard_reports"
    ADVANCED_REPORTS = "advanced_reports"
    INTELLIGENCE_POD_ACCESS = "intelligence_pod_access"
    QUANTUM_AUDIT = "quantum_audit"
    PREMIUM_SUPPORT = "premium_support"
    API_ACCESS = "api_access"
    CUSTOM_INTEGRATIONS = "custom_integrations"


class EntitlementsEngine:
    """Manages tiered access control and feature gating."""

    def __init__(self):
        self.tier_definitions = self._initialize_tier_definitions()
        self.feature_mappings = self._initialize_feature_mappings()
        self.rate_limits = self._initialize_rate_limits()
        self.usage_tracking = {}

    def _initialize_tier_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Initialize tier definitions with features and limits."""
        return {
            Tier.FREE.value: {
                "name": "Free Tier",
                "description": "Basic access to NQBA ecosystem",
                "monthly_price": 0,
                "features": [
                    Feature.BASIC_OPTIMIZATION.value,
                    Feature.STANDARD_REPORTS.value,
                    Feature.API_ACCESS.value,
                ],
                "limits": {
                    "optimizations_per_month": 10,
                    "api_calls_per_day": 100,
                    "storage_gb": 1,
                    "support_level": "community",
                },
            },
            Tier.BUSINESS.value: {
                "name": "Business Tier",
                "description": "Professional business optimization",
                "monthly_price": 299,
                "features": [
                    Feature.BASIC_OPTIMIZATION.value,
                    Feature.ADVANCED_OPTIMIZATION.value,
                    Feature.STANDARD_REPORTS.value,
                    Feature.ADVANCED_REPORTS.value,
                    Feature.API_ACCESS.value,
                    Feature.PREMIUM_SUPPORT.value,
                ],
                "limits": {
                    "optimizations_per_month": 100,
                    "api_calls_per_day": 1000,
                    "storage_gb": 10,
                    "support_level": "email",
                },
            },
            Tier.PREMIUM.value: {
                "name": "Premium Tier",
                "description": "Advanced quantum optimization",
                "monthly_price": 999,
                "features": [
                    Feature.BASIC_OPTIMIZATION.value,
                    Feature.ADVANCED_OPTIMIZATION.value,
                    Feature.QUANTUM_OPTIMIZATION.value,
                    Feature.STANDARD_REPORTS.value,
                    Feature.ADVANCED_REPORTS.value,
                    Feature.API_ACCESS.value,
                    Feature.PREMIUM_SUPPORT.value,
                    Feature.CUSTOM_INTEGRATIONS.value,
                ],
                "limits": {
                    "optimizations_per_month": 500,
                    "api_calls_per_day": 5000,
                    "storage_gb": 50,
                    "support_level": "phone",
                },
            },
            Tier.LUXURY.value: {
                "name": "Luxury Tier",
                "description": "Full quantum advantage access",
                "monthly_price": 2999,
                "features": [
                    Feature.BASIC_OPTIMIZATION.value,
                    Feature.ADVANCED_OPTIMIZATION.value,
                    Feature.QUANTUM_OPTIMIZATION.value,
                    Feature.STANDARD_REPORTS.value,
                    Feature.ADVANCED_REPORTS.value,
                    Feature.INTELLIGENCE_POD_ACCESS.value,
                    Feature.QUANTUM_AUDIT.value,
                    Feature.API_ACCESS.value,
                    Feature.PREMIUM_SUPPORT.value,
                    Feature.CUSTOM_INTEGRATIONS.value,
                ],
                "limits": {
                    "optimizations_per_month": 1000,
                    "api_calls_per_day": 10000,
                    "storage_gb": 100,
                    "support_level": "dedicated",
                },
            },
        }

    def _initialize_feature_mappings(self) -> Dict[str, List[str]]:
        """Initialize feature to tier mappings."""
        return {
            Feature.BASIC_OPTIMIZATION.value: [
                Tier.FREE.value,
                Tier.BUSINESS.value,
                Tier.PREMIUM.value,
                Tier.LUXURY.value,
            ],
            Feature.ADVANCED_OPTIMIZATION.value: [
                Tier.BUSINESS.value,
                Tier.PREMIUM.value,
                Tier.LUXURY.value,
            ],
            Feature.QUANTUM_OPTIMIZATION.value: [Tier.PREMIUM.value, Tier.LUXURY.value],
            Feature.STANDARD_REPORTS.value: [
                Tier.FREE.value,
                Tier.BUSINESS.value,
                Tier.PREMIUM.value,
                Tier.LUXURY.value,
            ],
            Feature.ADVANCED_REPORTS.value: [
                Tier.BUSINESS.value,
                Tier.PREMIUM.value,
                Tier.LUXURY.value,
            ],
            Feature.INTELLIGENCE_POD_ACCESS.value: [Tier.LUXURY.value],
            Feature.QUANTUM_AUDIT.value: [Tier.LUXURY.value],
            Feature.PREMIUM_SUPPORT.value: [
                Tier.BUSINESS.value,
                Tier.PREMIUM.value,
                Tier.LUXURY.value,
            ],
            Feature.API_ACCESS.value: [
                Tier.FREE.value,
                Tier.BUSINESS.value,
                Tier.PREMIUM.value,
                Tier.LUXURY.value,
            ],
            Feature.CUSTOM_INTEGRATIONS.value: [Tier.PREMIUM.value, Tier.LUXURY.value],
        }

    def _initialize_rate_limits(self) -> Dict[str, Dict[str, int]]:
        """Initialize rate limits for each tier."""
        return {
            Tier.FREE.value: {
                "requests_per_minute": 10,
                "requests_per_hour": 100,
                "requests_per_day": 1000,
            },
            Tier.BUSINESS.value: {
                "requests_per_minute": 50,
                "requests_per_hour": 500,
                "requests_per_day": 5000,
            },
            Tier.PREMIUM.value: {
                "requests_per_minute": 100,
                "requests_per_hour": 1000,
                "requests_per_day": 10000,
            },
            Tier.LUXURY.value: {
                "requests_per_minute": 200,
                "requests_per_hour": 2000,
                "requests_per_day": 20000,
            },
        }

    def check_access(self, tier_key: Dict[str, Any], feature: str) -> bool:
        """Check if a tier has access to a specific feature."""
        try:
            tier = tier_key.get("tier")
            if not tier:
                logger.warning("No tier specified in tier key")
                return False

            # Check if feature exists
            if feature not in self.feature_mappings:
                logger.warning(f"Unknown feature: {feature}")
                return False

            # Check if tier has access to feature
            allowed_tiers = self.feature_mappings[feature]
            has_access = tier in allowed_tiers

            # Log access check
            logger.info(f"Access check: {tier} -> {feature} = {has_access}")

            return has_access

        except Exception as e:
            logger.error(f"Error checking access: {e}")
            return False

    def check_rate_limit(self, tier_key: Dict[str, Any], user_id: str) -> bool:
        """Check if user has exceeded rate limits for their tier."""
        try:
            tier = tier_key.get("tier")
            if not tier:
                return False

            # Get current usage
            current_time = datetime.now()
            user_key = f"{user_id}_{tier}"

            if user_key not in self.usage_tracking:
                self.usage_tracking[user_key] = {
                    "requests": [],
                    "last_reset": current_time,
                }

            usage = self.usage_tracking[user_key]

            # Reset counters if needed
            if current_time - usage["last_reset"] > timedelta(days=1):
                usage["requests"] = []
                usage["last_reset"] = current_time

            # Get rate limits for tier
            rate_limits = self.rate_limits.get(tier, {})
            requests_per_day = rate_limits.get("requests_per_day", 1000)

            # Check daily limit
            daily_requests = len(
                [r for r in usage["requests"] if current_time - r < timedelta(days=1)]
            )

            if daily_requests >= requests_per_day:
                logger.warning(f"Rate limit exceeded for user {user_id} on tier {tier}")
                return False

            # Record this request
            usage["requests"].append(current_time)

            return True

        except Exception as e:
            logger.error(f"Error checking rate limit: {e}")
            return False

    def get_tier_features(self, tier: str) -> List[str]:
        """Get all features available for a specific tier."""
        tier_def = self.tier_definitions.get(tier)
        if not tier_def:
            return []

        return tier_def.get("features", [])

    def get_tier_limits(self, tier: str) -> Dict[str, Any]:
        """Get limits for a specific tier."""
        tier_def = self.tier_definitions.get(tier)
        if not tier_def:
            return {}

        return tier_def.get("limits", {})

    def upgrade_tier(self, current_tier: str, new_tier: str) -> bool:
        """Check if tier upgrade is valid."""
        tier_order = [
            Tier.FREE.value,
            Tier.BUSINESS.value,
            Tier.PREMIUM.value,
            Tier.LUXURY.value,
        ]

        try:
            current_index = tier_order.index(current_tier)
            new_index = tier_order.index(new_tier)

            # Can only upgrade to higher tiers
            return new_index > current_index

        except ValueError:
            logger.warning(f"Invalid tier: {current_tier} or {new_tier}")
            return False

    def get_tier_comparison(self) -> Dict[str, Any]:
        """Get comparison of all tiers."""
        comparison = {}

        for tier, definition in self.tier_definitions.items():
            comparison[tier] = {
                "name": definition["name"],
                "description": definition["description"],
                "monthly_price": definition["monthly_price"],
                "feature_count": len(definition["features"]),
                "features": definition["features"],
                "limits": definition["limits"],
            }

        return comparison

    def validate_api_key(self, api_key: Dict[str, Any]) -> Dict[str, Any]:
        """Validate an API key and return tier information."""
        try:
            tier = api_key.get("tier")
            if not tier or tier not in self.tier_definitions:
                return {"valid": False, "error": "Invalid tier"}

            # Check if tier is active
            tier_def = self.tier_definitions[tier]

            return {
                "valid": True,
                "tier": tier,
                "features": tier_def["features"],
                "limits": tier_def["limits"],
                "name": tier_def["name"],
            }

        except Exception as e:
            logger.error(f"Error validating API key: {e}")
            return {"valid": False, "error": str(e)}

    def get_usage_summary(self, user_id: str, tier: str) -> Dict[str, Any]:
        """Get usage summary for a user."""
        try:
            user_key = f"{user_id}_{tier}"
            usage = self.usage_tracking.get(user_key, {"requests": []})

            current_time = datetime.now()

            # Calculate usage periods
            daily_requests = len(
                [r for r in usage["requests"] if current_time - r < timedelta(days=1)]
            )
            hourly_requests = len(
                [r for r in usage["requests"] if current_time - r < timedelta(hours=1)]
            )
            monthly_requests = len(
                [r for r in usage["requests"] if current_time - r < timedelta(days=30)]
            )

            # Get limits
            limits = self.get_tier_limits(tier)

            return {
                "user_id": user_id,
                "tier": tier,
                "usage": {
                    "daily": daily_requests,
                    "hourly": hourly_requests,
                    "monthly": monthly_requests,
                },
                "limits": limits,
                "remaining": {
                    "daily": max(
                        0, limits.get("optimizations_per_month", 0) - daily_requests
                    ),
                    "monthly": max(
                        0, limits.get("optimizations_per_month", 0) - monthly_requests
                    ),
                },
            }

        except Exception as e:
            logger.error(f"Error getting usage summary: {e}")
            return {"error": str(e)}


# Global entitlements engine instance
entitlements_engine = EntitlementsEngine()
