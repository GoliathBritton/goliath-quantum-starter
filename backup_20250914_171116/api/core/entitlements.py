# Quantum Nexus Platform - Entitlement & Subscription Gating System
# Secure tier-based access control for safe demo deployment

from enum import Enum
from typing import Dict, List, Optional, Set, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from functools import wraps
import json
import logging
from flask import request, jsonify, g
from sqlalchemy import Column, String, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from werkzeug.exceptions import Forbidden, Unauthorized

logger = logging.getLogger(__name__)
Base = declarative_base()

# =============================================================================
# Subscription Tiers and Plans
# =============================================================================

class SubscriptionTier(Enum):
    """Quantum Nexus subscription tiers with increasing capabilities"""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    QUANTUM_UNLIMITED = "quantum_unlimited"

class FeatureType(Enum):
    """Types of features that can be gated"""
    API_CALLS = "api_calls"
    QUANTUM_JOBS = "quantum_jobs"
    AGENTS = "agents"
    WORKFLOWS = "workflows"
    STORAGE = "storage"
    USERS = "users"
    INTEGRATIONS = "integrations"
    SUPPORT = "support"
    CUSTOM_MODELS = "custom_models"
    WHITE_LABEL = "white_label"

@dataclass
class FeatureLimit:
    """Defines limits for a specific feature"""
    feature_type: FeatureType
    limit: int  # -1 for unlimited
    period: str = "monthly"  # daily, weekly, monthly, yearly
    description: str = ""
    
    def is_unlimited(self) -> bool:
        return self.limit == -1

@dataclass
class SubscriptionPlan:
    """Complete subscription plan definition"""
    tier: SubscriptionTier
    name: str
    description: str
    price_monthly: float
    price_yearly: float
    features: List[FeatureLimit] = field(default_factory=list)
    enabled_features: Set[str] = field(default_factory=set)
    trial_days: int = 0
    is_popular: bool = False
    
    def get_feature_limit(self, feature_type: FeatureType) -> Optional[FeatureLimit]:
        """Get the limit for a specific feature type"""
        for feature in self.features:
            if feature.feature_type == feature_type:
                return feature
        return None

# =============================================================================
# Predefined Subscription Plans
# =============================================================================

QUANTUM_NEXUS_PLANS = {
    SubscriptionTier.FREE: SubscriptionPlan(
        tier=SubscriptionTier.FREE,
        name="Quantum Explorer",
        description="Perfect for testing and small experiments",
        price_monthly=0.0,
        price_yearly=0.0,
        trial_days=0,
        features=[
            FeatureLimit(FeatureType.API_CALLS, 1000, "monthly", "1K API calls per month"),
            FeatureLimit(FeatureType.QUANTUM_JOBS, 10, "monthly", "10 quantum jobs per month"),
            FeatureLimit(FeatureType.AGENTS, 2, "total", "Up to 2 AI agents"),
            FeatureLimit(FeatureType.WORKFLOWS, 5, "total", "Up to 5 workflows"),
            FeatureLimit(FeatureType.STORAGE, 1, "total", "1GB storage"),
            FeatureLimit(FeatureType.USERS, 1, "total", "Single user"),
        ],
        enabled_features={
            "basic_dashboard", "community_support", "standard_templates"
        }
    ),
    
    SubscriptionTier.STARTER: SubscriptionPlan(
        tier=SubscriptionTier.STARTER,
        name="Quantum Accelerator",
        description="Ideal for growing businesses and teams",
        price_monthly=49.0,
        price_yearly=490.0,
        trial_days=14,
        features=[
            FeatureLimit(FeatureType.API_CALLS, 25000, "monthly", "25K API calls per month"),
            FeatureLimit(FeatureType.QUANTUM_JOBS, 100, "monthly", "100 quantum jobs per month"),
            FeatureLimit(FeatureType.AGENTS, 10, "total", "Up to 10 AI agents"),
            FeatureLimit(FeatureType.WORKFLOWS, 25, "total", "Up to 25 workflows"),
            FeatureLimit(FeatureType.STORAGE, 10, "total", "10GB storage"),
            FeatureLimit(FeatureType.USERS, 5, "total", "Up to 5 team members"),
            FeatureLimit(FeatureType.INTEGRATIONS, 5, "total", "5 third-party integrations"),
        ],
        enabled_features={
            "advanced_dashboard", "email_support", "premium_templates", 
            "basic_analytics", "api_access", "webhook_support"
        }
    ),
    
    SubscriptionTier.PROFESSIONAL: SubscriptionPlan(
        tier=SubscriptionTier.PROFESSIONAL,
        name="Quantum Professional",
        description="Advanced features for serious quantum computing",
        price_monthly=149.0,
        price_yearly=1490.0,
        trial_days=30,
        is_popular=True,
        features=[
            FeatureLimit(FeatureType.API_CALLS, 100000, "monthly", "100K API calls per month"),
            FeatureLimit(FeatureType.QUANTUM_JOBS, 500, "monthly", "500 quantum jobs per month"),
            FeatureLimit(FeatureType.AGENTS, 50, "total", "Up to 50 AI agents"),
            FeatureLimit(FeatureType.WORKFLOWS, 100, "total", "Up to 100 workflows"),
            FeatureLimit(FeatureType.STORAGE, 100, "total", "100GB storage"),
            FeatureLimit(FeatureType.USERS, 25, "total", "Up to 25 team members"),
            FeatureLimit(FeatureType.INTEGRATIONS, 20, "total", "20 third-party integrations"),
            FeatureLimit(FeatureType.CUSTOM_MODELS, 5, "total", "5 custom AI models"),
        ],
        enabled_features={
            "pro_dashboard", "priority_support", "advanced_templates",
            "advanced_analytics", "custom_branding", "sso_integration",
            "advanced_workflows", "quantum_optimization", "real_time_monitoring"
        }
    ),
    
    SubscriptionTier.ENTERPRISE: SubscriptionPlan(
        tier=SubscriptionTier.ENTERPRISE,
        name="Quantum Enterprise",
        description="Enterprise-grade quantum computing platform",
        price_monthly=499.0,
        price_yearly=4990.0,
        trial_days=30,
        features=[
            FeatureLimit(FeatureType.API_CALLS, 1000000, "monthly", "1M API calls per month"),
            FeatureLimit(FeatureType.QUANTUM_JOBS, 2500, "monthly", "2.5K quantum jobs per month"),
            FeatureLimit(FeatureType.AGENTS, 200, "total", "Up to 200 AI agents"),
            FeatureLimit(FeatureType.WORKFLOWS, 500, "total", "Up to 500 workflows"),
            FeatureLimit(FeatureType.STORAGE, 1000, "total", "1TB storage"),
            FeatureLimit(FeatureType.USERS, 100, "total", "Up to 100 team members"),
            FeatureLimit(FeatureType.INTEGRATIONS, -1, "total", "Unlimited integrations"),
            FeatureLimit(FeatureType.CUSTOM_MODELS, 25, "total", "25 custom AI models"),
        ],
        enabled_features={
            "enterprise_dashboard", "dedicated_support", "enterprise_templates",
            "enterprise_analytics", "full_white_label", "advanced_sso",
            "enterprise_workflows", "quantum_acceleration", "compliance_tools",
            "audit_logs", "advanced_security", "on_premise_deployment"
        }
    ),
    
    SubscriptionTier.QUANTUM_UNLIMITED: SubscriptionPlan(
        tier=SubscriptionTier.QUANTUM_UNLIMITED,
        name="Quantum Unlimited",
        description="Unlimited quantum computing power for industry leaders",
        price_monthly=1999.0,
        price_yearly=19990.0,
        trial_days=30,
        features=[
            FeatureLimit(FeatureType.API_CALLS, -1, "monthly", "Unlimited API calls"),
            FeatureLimit(FeatureType.QUANTUM_JOBS, -1, "monthly", "Unlimited quantum jobs"),
            FeatureLimit(FeatureType.AGENTS, -1, "total", "Unlimited AI agents"),
            FeatureLimit(FeatureType.WORKFLOWS, -1, "total", "Unlimited workflows"),
            FeatureLimit(FeatureType.STORAGE, -1, "total", "Unlimited storage"),
            FeatureLimit(FeatureType.USERS, -1, "total", "Unlimited team members"),
            FeatureLimit(FeatureType.INTEGRATIONS, -1, "total", "Unlimited integrations"),
            FeatureLimit(FeatureType.CUSTOM_MODELS, -1, "total", "Unlimited custom models"),
        ],
        enabled_features={
            "unlimited_dashboard", "concierge_support", "unlimited_templates",
            "unlimited_analytics", "complete_white_label", "enterprise_sso",
            "unlimited_workflows", "quantum_supremacy", "advanced_compliance",
            "real_time_audit", "military_grade_security", "private_cloud",
            "dedicated_infrastructure", "custom_development", "24_7_support"
        }
    )
}

# =============================================================================
# Database Models
# =============================================================================

class UserSubscription(Base):
    """User subscription and entitlement tracking"""
    __tablename__ = 'user_subscriptions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False, index=True)
    tier = Column(String(50), nullable=False, default=SubscriptionTier.FREE.value)
    status = Column(String(50), nullable=False, default='active')  # active, cancelled, expired, trial
    
    # Subscription dates
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime)
    trial_ends_at = Column(DateTime)
    
    # Billing
    billing_cycle = Column(String(20), default='monthly')  # monthly, yearly
    last_payment_at = Column(DateTime)
    next_payment_at = Column(DateTime)
    
    # Usage tracking
    current_usage = Column(Text)  # JSON string of current usage
    usage_reset_at = Column(DateTime)
    
    # Metadata
    metadata = Column(Text)  # JSON string for additional data
    
    def get_plan(self) -> SubscriptionPlan:
        """Get the subscription plan for this user"""
        tier = SubscriptionTier(self.tier)
        return QUANTUM_NEXUS_PLANS[tier]
    
    def get_usage(self) -> Dict[str, int]:
        """Get current usage as dictionary"""
        if not self.current_usage:
            return {}
        try:
            return json.loads(self.current_usage)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def set_usage(self, usage: Dict[str, int]):
        """Set current usage from dictionary"""
        self.current_usage = json.dumps(usage)
    
    def is_trial(self) -> bool:
        """Check if user is in trial period"""
        return (self.trial_ends_at and 
                self.trial_ends_at > datetime.utcnow() and
                self.status == 'trial')
    
    def is_active(self) -> bool:
        """Check if subscription is active"""
        if self.status not in ['active', 'trial']:
            return False
        
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
            
        return True
    
    def days_until_expiry(self) -> Optional[int]:
        """Get days until subscription expires"""
        if not self.expires_at:
            return None
        
        delta = self.expires_at - datetime.utcnow()
        return max(0, delta.days)

class FeatureUsage(Base):
    """Track feature usage for billing and limits"""
    __tablename__ = 'feature_usage'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False, index=True)
    feature_type = Column(String(50), nullable=False)
    usage_count = Column(Integer, default=0)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<FeatureUsage {self.user_id}:{self.feature_type}={self.usage_count}>"

# =============================================================================
# Entitlement Service
# =============================================================================

class EntitlementService:
    """Core service for managing user entitlements and subscription gating"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def get_user_subscription(self, user_id: str) -> UserSubscription:
        """Get or create user subscription"""
        subscription = self.db.query(UserSubscription).filter_by(user_id=user_id).first()
        
        if not subscription:
            # Create free tier subscription for new users
            subscription = UserSubscription(
                user_id=user_id,
                tier=SubscriptionTier.FREE.value,
                status='active',
                created_at=datetime.utcnow(),
                usage_reset_at=self._get_next_reset_date()
            )
            self.db.add(subscription)
            self.db.commit()
        
        return subscription
    
    def check_feature_access(self, user_id: str, feature_type: FeatureType, 
                           requested_amount: int = 1) -> Dict[str, Any]:
        """Check if user has access to a feature and sufficient quota"""
        subscription = self.get_user_subscription(user_id)
        plan = subscription.get_plan()
        
        # Check if subscription is active
        if not subscription.is_active():
            return {
                'allowed': False,
                'reason': 'subscription_expired',
                'message': 'Your subscription has expired. Please renew to continue.',
                'upgrade_required': True
            }
        
        # Get feature limit
        feature_limit = plan.get_feature_limit(feature_type)
        if not feature_limit:
            return {
                'allowed': False,
                'reason': 'feature_not_available',
                'message': f'Feature {feature_type.value} is not available in your plan.',
                'upgrade_required': True
            }
        
        # Check if unlimited
        if feature_limit.is_unlimited():
            return {
                'allowed': True,
                'unlimited': True,
                'remaining': -1
            }
        
        # Check current usage
        current_usage = self._get_current_usage(user_id, feature_type, feature_limit.period)
        remaining = feature_limit.limit - current_usage
        
        if remaining < requested_amount:
            return {
                'allowed': False,
                'reason': 'quota_exceeded',
                'message': f'You have exceeded your {feature_type.value} quota for this {feature_limit.period}.',
                'current_usage': current_usage,
                'limit': feature_limit.limit,
                'remaining': remaining,
                'upgrade_required': True
            }
        
        return {
            'allowed': True,
            'current_usage': current_usage,
            'limit': feature_limit.limit,
            'remaining': remaining - requested_amount
        }
    
    def consume_feature_quota(self, user_id: str, feature_type: FeatureType, 
                            amount: int = 1) -> bool:
        """Consume feature quota and update usage tracking"""
        access_check = self.check_feature_access(user_id, feature_type, amount)
        
        if not access_check['allowed']:
            return False
        
        # Update usage tracking
        subscription = self.get_user_subscription(user_id)
        plan = subscription.get_plan()
        feature_limit = plan.get_feature_limit(feature_type)
        
        if not feature_limit.is_unlimited():
            self._increment_usage(user_id, feature_type, feature_limit.period, amount)
        
        return True
    
    def get_usage_summary(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive usage summary for user"""
        subscription = self.get_user_subscription(user_id)
        plan = subscription.get_plan()
        
        summary = {
            'subscription': {
                'tier': subscription.tier,
                'plan_name': plan.name,
                'status': subscription.status,
                'is_trial': subscription.is_trial(),
                'expires_at': subscription.expires_at.isoformat() if subscription.expires_at else None,
                'days_until_expiry': subscription.days_until_expiry()
            },
            'features': {},
            'enabled_features': list(plan.enabled_features)
        }
        
        # Get usage for each feature
        for feature_limit in plan.features:
            feature_type = feature_limit.feature_type
            current_usage = self._get_current_usage(user_id, feature_type, feature_limit.period)
            
            summary['features'][feature_type.value] = {
                'limit': feature_limit.limit,
                'current_usage': current_usage,
                'remaining': feature_limit.limit - current_usage if not feature_limit.is_unlimited() else -1,
                'unlimited': feature_limit.is_unlimited(),
                'period': feature_limit.period,
                'description': feature_limit.description
            }
        
        return summary
    
    def upgrade_subscription(self, user_id: str, new_tier: SubscriptionTier, 
                           billing_cycle: str = 'monthly') -> UserSubscription:
        """Upgrade user subscription to new tier"""
        subscription = self.get_user_subscription(user_id)
        old_tier = subscription.tier
        
        # Update subscription
        subscription.tier = new_tier.value
        subscription.billing_cycle = billing_cycle
        subscription.status = 'active'
        subscription.updated_at = datetime.utcnow()
        
        # Set expiry based on billing cycle
        if billing_cycle == 'yearly':
            subscription.expires_at = datetime.utcnow() + timedelta(days=365)
        else:
            subscription.expires_at = datetime.utcnow() + timedelta(days=30)
        
        # Reset usage for new billing period
        subscription.usage_reset_at = self._get_next_reset_date()
        subscription.set_usage({})
        
        self.db.commit()
        
        logger.info(f"User {user_id} upgraded from {old_tier} to {new_tier.value}")
        return subscription
    
    def start_trial(self, user_id: str, tier: SubscriptionTier, trial_days: int = 14) -> UserSubscription:
        """Start trial subscription for user"""
        subscription = self.get_user_subscription(user_id)
        
        subscription.tier = tier.value
        subscription.status = 'trial'
        subscription.trial_ends_at = datetime.utcnow() + timedelta(days=trial_days)
        subscription.expires_at = subscription.trial_ends_at
        subscription.updated_at = datetime.utcnow()
        
        # Reset usage
        subscription.usage_reset_at = self._get_next_reset_date()
        subscription.set_usage({})
        
        self.db.commit()
        
        logger.info(f"User {user_id} started {trial_days}-day trial for {tier.value}")
        return subscription
    
    def _get_current_usage(self, user_id: str, feature_type: FeatureType, period: str) -> int:
        """Get current usage for a feature in the specified period"""
        period_start, period_end = self._get_period_bounds(period)
        
        usage = self.db.query(FeatureUsage).filter(
            FeatureUsage.user_id == user_id,
            FeatureUsage.feature_type == feature_type.value,
            FeatureUsage.period_start >= period_start,
            FeatureUsage.period_end <= period_end
        ).first()
        
        return usage.usage_count if usage else 0
    
    def _increment_usage(self, user_id: str, feature_type: FeatureType, 
                        period: str, amount: int):
        """Increment usage counter for a feature"""
        period_start, period_end = self._get_period_bounds(period)
        
        usage = self.db.query(FeatureUsage).filter(
            FeatureUsage.user_id == user_id,
            FeatureUsage.feature_type == feature_type.value,
            FeatureUsage.period_start == period_start,
            FeatureUsage.period_end == period_end
        ).first()
        
        if usage:
            usage.usage_count += amount
        else:
            usage = FeatureUsage(
                user_id=user_id,
                feature_type=feature_type.value,
                usage_count=amount,
                period_start=period_start,
                period_end=period_end
            )
            self.db.add(usage)
        
        self.db.commit()
    
    def _get_period_bounds(self, period: str) -> tuple:
        """Get start and end dates for a period"""
        now = datetime.utcnow()
        
        if period == 'daily':
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)
        elif period == 'weekly':
            days_since_monday = now.weekday()
            start = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(weeks=1)
        elif period == 'monthly':
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if start.month == 12:
                end = start.replace(year=start.year + 1, month=1)
            else:
                end = start.replace(month=start.month + 1)
        elif period == 'yearly':
            start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
            end = start.replace(year=start.year + 1)
        else:
            # Default to monthly
            start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if start.month == 12:
                end = start.replace(year=start.year + 1, month=1)
            else:
                end = start.replace(month=start.month + 1)
        
        return start, end
    
    def _get_next_reset_date(self) -> datetime:
        """Get next monthly reset date"""
        now = datetime.utcnow()
        if now.month == 12:
            return now.replace(year=now.year + 1, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return now.replace(month=now.month + 1, day=1, hour=0, minute=0, second=0, microsecond=0)

# =============================================================================
# Decorators for Route Protection
# =============================================================================

def require_subscription(min_tier: SubscriptionTier = SubscriptionTier.FREE):
    """Decorator to require minimum subscription tier for route access"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user_id') or not g.user_id:
                raise Unauthorized("Authentication required")
            
            from flask import current_app
            entitlement_service = EntitlementService(current_app.db.session)
            
            subscription = entitlement_service.get_user_subscription(g.user_id)
            user_tier = SubscriptionTier(subscription.tier)
            
            # Check if user tier meets minimum requirement
            tier_hierarchy = {
                SubscriptionTier.FREE: 0,
                SubscriptionTier.STARTER: 1,
                SubscriptionTier.PROFESSIONAL: 2,
                SubscriptionTier.ENTERPRISE: 3,
                SubscriptionTier.QUANTUM_UNLIMITED: 4
            }
            
            if tier_hierarchy[user_tier] < tier_hierarchy[min_tier]:
                return jsonify({
                    'error': 'subscription_required',
                    'message': f'This feature requires {min_tier.value} subscription or higher',
                    'current_tier': user_tier.value,
                    'required_tier': min_tier.value,
                    'upgrade_url': '/subscription/upgrade'
                }), 403
            
            if not subscription.is_active():
                return jsonify({
                    'error': 'subscription_expired',
                    'message': 'Your subscription has expired. Please renew to continue.',
                    'renewal_url': '/subscription/renew'
                }), 403
            
            # Add subscription info to request context
            g.subscription = subscription
            g.entitlement_service = entitlement_service
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_feature_quota(feature_type: FeatureType, amount: int = 1):
    """Decorator to check and consume feature quota"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user_id') or not g.user_id:
                raise Unauthorized("Authentication required")
            
            from flask import current_app
            entitlement_service = EntitlementService(current_app.db.session)
            
            # Check feature access
            access_check = entitlement_service.check_feature_access(
                g.user_id, feature_type, amount
            )
            
            if not access_check['allowed']:
                return jsonify({
                    'error': access_check['reason'],
                    'message': access_check['message'],
                    'upgrade_required': access_check.get('upgrade_required', False),
                    'current_usage': access_check.get('current_usage'),
                    'limit': access_check.get('limit'),
                    'upgrade_url': '/subscription/upgrade'
                }), 403
            
            # Consume quota
            if not entitlement_service.consume_feature_quota(g.user_id, feature_type, amount):
                return jsonify({
                    'error': 'quota_consumption_failed',
                    'message': 'Failed to consume feature quota'
                }), 500
            
            # Add remaining quota to response headers
            response = f(*args, **kwargs)
            if hasattr(response, 'headers') and not access_check.get('unlimited', False):
                response.headers['X-Quota-Remaining'] = str(access_check['remaining'])
                response.headers['X-Quota-Limit'] = str(access_check['limit'])
            
            return response
        return decorated_function
    return decorator

def require_feature(feature_name: str):
    """Decorator to require specific feature to be enabled in user's plan"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not hasattr(g, 'user_id') or not g.user_id:
                raise Unauthorized("Authentication required")
            
            from flask import current_app
            entitlement_service = EntitlementService(current_app.db.session)
            
            subscription = entitlement_service.get_user_subscription(g.user_id)
            plan = subscription.get_plan()
            
            if feature_name not in plan.enabled_features:
                return jsonify({
                    'error': 'feature_not_available',
                    'message': f'Feature "{feature_name}" is not available in your {plan.name} plan',
                    'current_plan': plan.name,
                    'upgrade_url': '/subscription/upgrade'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# =============================================================================
# Utility Functions
# =============================================================================

def get_all_plans() -> Dict[SubscriptionTier, SubscriptionPlan]:
    """Get all available subscription plans"""
    return QUANTUM_NEXUS_PLANS.copy()

def get_plan_comparison() -> List[Dict[str, Any]]:
    """Get plan comparison data for frontend"""
    plans = []
    
    for tier, plan in QUANTUM_NEXUS_PLANS.items():
        plan_data = {
            'tier': tier.value,
            'name': plan.name,
            'description': plan.description,
            'price_monthly': plan.price_monthly,
            'price_yearly': plan.price_yearly,
            'trial_days': plan.trial_days,
            'is_popular': plan.is_popular,
            'features': [],
            'enabled_features': list(plan.enabled_features)
        }
        
        for feature in plan.features:
            plan_data['features'].append({
                'type': feature.feature_type.value,
                'limit': feature.limit,
                'period': feature.period,
                'description': feature.description,
                'unlimited': feature.is_unlimited()
            })
        
        plans.append(plan_data)
    
    return plans

def calculate_savings(monthly_price: float, yearly_price: float) -> Dict[str, Any]:
    """Calculate savings for yearly vs monthly billing"""
    yearly_equivalent = monthly_price * 12
    savings_amount = yearly_equivalent - yearly_price
    savings_percentage = (savings_amount / yearly_equivalent) * 100 if yearly_equivalent > 0 else 0
    
    return {
        'monthly_total_yearly': yearly_equivalent,
        'yearly_price': yearly_price,
        'savings_amount': savings_amount,
        'savings_percentage': round(savings_percentage, 1)
    }