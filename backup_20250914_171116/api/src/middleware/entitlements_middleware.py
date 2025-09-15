from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import time
import redis
import json
from ..entitlements import (
    EntitlementsEngine, 
    SubscriptionTier, 
    FeatureFlag,
    get_entitlements_engine
)
from ..models import User

security = HTTPBearer()

class RateLimitMiddleware:
    """Rate limiting middleware based on user subscription tier"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis_client = redis_client or redis.Redis(
            host='localhost', 
            port=6379, 
            decode_responses=True
        )
        self.entitlements = get_entitlements_engine()
    
    async def check_rate_limit(self, user_id: str, user_tier: SubscriptionTier) -> bool:
        """Check if user is within rate limits"""
        rate_limit = self.entitlements.check_api_rate_limit(user_tier)
        
        # Create rate limit key
        current_minute = int(time.time() // 60)
        rate_key = f"rate_limit:{user_id}:{current_minute}"
        
        try:
            # Get current request count
            current_count = self.redis_client.get(rate_key)
            current_count = int(current_count) if current_count else 0
            
            if current_count >= rate_limit:
                return False
            
            # Increment counter
            pipe = self.redis_client.pipeline()
            pipe.incr(rate_key)
            pipe.expire(rate_key, 60)  # Expire after 1 minute
            pipe.execute()
            
            return True
            
        except Exception:
            # If Redis is down, allow the request (fail open)
            return True
    
    async def get_rate_limit_info(self, user_id: str, user_tier: SubscriptionTier) -> Dict[str, Any]:
        """Get current rate limit status for user"""
        rate_limit = self.entitlements.check_api_rate_limit(user_tier)
        current_minute = int(time.time() // 60)
        rate_key = f"rate_limit:{user_id}:{current_minute}"
        
        try:
            current_count = self.redis_client.get(rate_key)
            current_count = int(current_count) if current_count else 0
            
            return {
                "limit": rate_limit,
                "remaining": max(0, rate_limit - current_count),
                "reset_time": (current_minute + 1) * 60,
                "current_usage": current_count
            }
        except Exception:
            return {
                "limit": rate_limit,
                "remaining": rate_limit,
                "reset_time": (current_minute + 1) * 60,
                "current_usage": 0
            }

class EntitlementsMiddleware:
    """Middleware for checking feature entitlements"""
    
    def __init__(self):
        self.entitlements = get_entitlements_engine()
        self.rate_limiter = RateLimitMiddleware()
    
    async def check_feature_access(
        self, 
        user: User, 
        required_feature: FeatureFlag,
        request: Request
    ) -> None:
        """Check if user has access to required feature"""
        # Check feature entitlement
        self.entitlements.require_feature_access(user.subscription_tier, required_feature)
        
        # Check rate limits
        if not await self.rate_limiter.check_rate_limit(user.id, user.subscription_tier):
            rate_info = await self.rate_limiter.get_rate_limit_info(user.id, user.subscription_tier)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": rate_info["limit"],
                    "reset_time": rate_info["reset_time"],
                    "upgrade_url": "/pricing"
                },
                headers={
                    "X-RateLimit-Limit": str(rate_info["limit"]),
                    "X-RateLimit-Remaining": str(rate_info["remaining"]),
                    "X-RateLimit-Reset": str(rate_info["reset_time"])
                }
            )
    
    async def add_rate_limit_headers(self, user: User, response_headers: Dict[str, str]) -> None:
        """Add rate limit headers to response"""
        rate_info = await self.rate_limiter.get_rate_limit_info(user.id, user.subscription_tier)
        
        response_headers.update({
            "X-RateLimit-Limit": str(rate_info["limit"]),
            "X-RateLimit-Remaining": str(rate_info["remaining"]),
            "X-RateLimit-Reset": str(rate_info["reset_time"])
        })

# Global middleware instances
entitlements_middleware = EntitlementsMiddleware()
rate_limit_middleware = RateLimitMiddleware()

# Dependency functions for FastAPI
def require_feature(feature: FeatureFlag):
    """Dependency factory for requiring specific features"""
    async def check_feature_dependency(
        request: Request,
        user: User = Depends(get_current_user),  # Assume this exists
        middleware: EntitlementsMiddleware = Depends(lambda: entitlements_middleware)
    ):
        await middleware.check_feature_access(user, feature, request)
        return user
    
    return check_feature_dependency

def require_digital_avatar():
    """Require Digital Avatar access"""
    return require_feature(FeatureFlag.DIGITAL_AVATAR)

def require_ai_calling_agent():
    """Require AI Calling Agent access"""
    return require_feature(FeatureFlag.AI_CALLING_AGENT)

def require_quantum_jobs_premium():
    """Require Premium Quantum Jobs access"""
    return require_feature(FeatureFlag.QUANTUM_JOBS_PREMIUM)

def require_qnexus_predictions():
    """Require Q-Nexus Predictions access"""
    return require_feature(FeatureFlag.QNEXUS_PREDICTIONS)

def require_advanced_analytics():
    """Require Advanced Analytics access"""
    return require_feature(FeatureFlag.ADVANCED_ANALYTICS)

def require_custom_algorithms():
    """Require Custom Algorithms access"""
    return require_feature(FeatureFlag.CUSTOM_ALGORITHMS)

# Placeholder for user authentication dependency
# This should be implemented based on your auth system
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user - implement based on your auth system"""
    # This is a placeholder - implement your actual user authentication logic
    # For now, return a mock user for demonstration
    return User(
        id="user_123",
        email="user@example.com",
        subscription_tier=SubscriptionTier.PREMIUM,
        is_active=True
    )