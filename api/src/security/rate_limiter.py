from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import asyncio
import time
from collections import defaultdict, deque
from dataclasses import dataclass
import redis
import json
from fastapi import HTTPException, Request
from ..entitlements import SubscriptionTier

class RateLimitType(Enum):
    REQUESTS_PER_MINUTE = "requests_per_minute"
    REQUESTS_PER_HOUR = "requests_per_hour"
    REQUESTS_PER_DAY = "requests_per_day"
    QUANTUM_JOBS_PER_DAY = "quantum_jobs_per_day"
    DATA_UPLOAD_MB_PER_HOUR = "data_upload_mb_per_hour"
    API_CALLS_PER_MINUTE = "api_calls_per_minute"

@dataclass
class RateLimit:
    limit_type: RateLimitType
    max_requests: int
    window_seconds: int
    burst_allowance: int = 0  # Allow short bursts above the limit

@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int
    reset_time: datetime
    retry_after: Optional[int] = None
    current_usage: int = 0

class RateLimitConfig:
    """Rate limit configurations by subscription tier"""
    
    TIER_LIMITS = {
        SubscriptionTier.BASIC: {
            RateLimitType.REQUESTS_PER_MINUTE: RateLimit(RateLimitType.REQUESTS_PER_MINUTE, 10, 60, 2),
            RateLimitType.REQUESTS_PER_HOUR: RateLimit(RateLimitType.REQUESTS_PER_HOUR, 100, 3600, 10),
            RateLimitType.REQUESTS_PER_DAY: RateLimit(RateLimitType.REQUESTS_PER_DAY, 1000, 86400, 50),
            RateLimitType.QUANTUM_JOBS_PER_DAY: RateLimit(RateLimitType.QUANTUM_JOBS_PER_DAY, 5, 86400, 0),
            RateLimitType.DATA_UPLOAD_MB_PER_HOUR: RateLimit(RateLimitType.DATA_UPLOAD_MB_PER_HOUR, 100, 3600, 20),
            RateLimitType.API_CALLS_PER_MINUTE: RateLimit(RateLimitType.API_CALLS_PER_MINUTE, 20, 60, 5)
        },
        SubscriptionTier.PREMIUM: {
            RateLimitType.REQUESTS_PER_MINUTE: RateLimit(RateLimitType.REQUESTS_PER_MINUTE, 50, 60, 10),
            RateLimitType.REQUESTS_PER_HOUR: RateLimit(RateLimitType.REQUESTS_PER_HOUR, 1000, 3600, 100),
            RateLimitType.REQUESTS_PER_DAY: RateLimit(RateLimitType.REQUESTS_PER_DAY, 10000, 86400, 500),
            RateLimitType.QUANTUM_JOBS_PER_DAY: RateLimit(RateLimitType.QUANTUM_JOBS_PER_DAY, 50, 86400, 5),
            RateLimitType.DATA_UPLOAD_MB_PER_HOUR: RateLimit(RateLimitType.DATA_UPLOAD_MB_PER_HOUR, 1000, 3600, 200),
            RateLimitType.API_CALLS_PER_MINUTE: RateLimit(RateLimitType.API_CALLS_PER_MINUTE, 100, 60, 20)
        },
        SubscriptionTier.ENTERPRISE: {
            RateLimitType.REQUESTS_PER_MINUTE: RateLimit(RateLimitType.REQUESTS_PER_MINUTE, 200, 60, 50),
            RateLimitType.REQUESTS_PER_HOUR: RateLimit(RateLimitType.REQUESTS_PER_HOUR, 5000, 3600, 500),
            RateLimitType.REQUESTS_PER_DAY: RateLimit(RateLimitType.REQUESTS_PER_DAY, 100000, 86400, 5000),
            RateLimitType.QUANTUM_JOBS_PER_DAY: RateLimit(RateLimitType.QUANTUM_JOBS_PER_DAY, 500, 86400, 50),
            RateLimitType.DATA_UPLOAD_MB_PER_HOUR: RateLimit(RateLimitType.DATA_UPLOAD_MB_PER_HOUR, 10000, 3600, 2000),
            RateLimitType.API_CALLS_PER_MINUTE: RateLimit(RateLimitType.API_CALLS_PER_MINUTE, 500, 60, 100)
        }
    }

class InMemoryRateLimiter:
    """In-memory rate limiter using sliding window algorithm"""
    
    def __init__(self):
        self.requests: Dict[str, deque] = defaultdict(deque)
        self.lock = asyncio.Lock()
    
    async def check_rate_limit(self, key: str, rate_limit: RateLimit) -> RateLimitResult:
        """Check if request is within rate limit"""
        async with self.lock:
            now = time.time()
            window_start = now - rate_limit.window_seconds
            
            # Clean old requests outside the window
            request_times = self.requests[key]
            while request_times and request_times[0] < window_start:
                request_times.popleft()
            
            current_count = len(request_times)
            max_allowed = rate_limit.max_requests + rate_limit.burst_allowance
            
            if current_count >= max_allowed:
                # Rate limit exceeded
                oldest_request = request_times[0] if request_times else now
                reset_time = datetime.fromtimestamp(oldest_request + rate_limit.window_seconds)
                retry_after = int(oldest_request + rate_limit.window_seconds - now)
                
                return RateLimitResult(
                    allowed=False,
                    remaining=0,
                    reset_time=reset_time,
                    retry_after=max(retry_after, 1),
                    current_usage=current_count
                )
            
            # Allow request and record it
            request_times.append(now)
            remaining = max_allowed - current_count - 1
            reset_time = datetime.fromtimestamp(now + rate_limit.window_seconds)
            
            return RateLimitResult(
                allowed=True,
                remaining=remaining,
                reset_time=reset_time,
                current_usage=current_count + 1
            )

class RedisRateLimiter:
    """Redis-based rate limiter for distributed systems"""
    
    def __init__(self, redis_client: Optional[redis.Redis] = None):
        self.redis = redis_client or redis.Redis(host='localhost', port=6379, db=0)
    
    async def check_rate_limit(self, key: str, rate_limit: RateLimit) -> RateLimitResult:
        """Check rate limit using Redis sliding window"""
        now = time.time()
        window_start = now - rate_limit.window_seconds
        
        pipe = self.redis.pipeline()
        
        # Remove old entries
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count current requests
        pipe.zcard(key)
        
        # Add current request with score as timestamp
        pipe.zadd(key, {str(now): now})
        
        # Set expiration
        pipe.expire(key, rate_limit.window_seconds)
        
        results = pipe.execute()
        current_count = results[1]
        
        max_allowed = rate_limit.max_requests + rate_limit.burst_allowance
        
        if current_count > max_allowed:
            # Remove the request we just added since it's over limit
            self.redis.zrem(key, str(now))
            
            # Get the oldest request time for reset calculation
            oldest_requests = self.redis.zrange(key, 0, 0, withscores=True)
            oldest_time = oldest_requests[0][1] if oldest_requests else now
            
            reset_time = datetime.fromtimestamp(oldest_time + rate_limit.window_seconds)
            retry_after = int(oldest_time + rate_limit.window_seconds - now)
            
            return RateLimitResult(
                allowed=False,
                remaining=0,
                reset_time=reset_time,
                retry_after=max(retry_after, 1),
                current_usage=current_count
            )
        
        remaining = max_allowed - current_count
        reset_time = datetime.fromtimestamp(now + rate_limit.window_seconds)
        
        return RateLimitResult(
            allowed=True,
            remaining=remaining,
            reset_time=reset_time,
            current_usage=current_count
        )

class AdaptiveRateLimiter:
    """Adaptive rate limiter that adjusts based on system load and user behavior"""
    
    def __init__(self, base_limiter: InMemoryRateLimiter):
        self.base_limiter = base_limiter
        self.system_load_factor = 1.0
        self.user_reputation: Dict[str, float] = defaultdict(lambda: 1.0)
        self.suspicious_ips: set = set()
    
    def update_system_load(self, cpu_usage: float, memory_usage: float):
        """Update system load factor based on resource usage"""
        # Reduce rate limits when system is under high load
        if cpu_usage > 0.8 or memory_usage > 0.8:
            self.system_load_factor = 0.5
        elif cpu_usage > 0.6 or memory_usage > 0.6:
            self.system_load_factor = 0.75
        else:
            self.system_load_factor = 1.0
    
    def update_user_reputation(self, user_id: str, behavior_score: float):
        """Update user reputation based on behavior"""
        # behavior_score: 1.0 = normal, > 1.0 = good, < 1.0 = suspicious
        self.user_reputation[user_id] = max(0.1, min(2.0, behavior_score))
    
    def mark_suspicious_ip(self, ip_address: str):
        """Mark IP as suspicious for stricter rate limiting"""
        self.suspicious_ips.add(ip_address)
    
    async def check_rate_limit(self, key: str, rate_limit: RateLimit, 
                             user_id: Optional[str] = None, 
                             ip_address: Optional[str] = None) -> RateLimitResult:
        """Check rate limit with adaptive adjustments"""
        # Calculate adjustment factors
        adjustment_factor = self.system_load_factor
        
        if user_id:
            adjustment_factor *= self.user_reputation[user_id]
        
        if ip_address and ip_address in self.suspicious_ips:
            adjustment_factor *= 0.2  # Very strict for suspicious IPs
        
        # Adjust rate limit
        adjusted_limit = RateLimit(
            limit_type=rate_limit.limit_type,
            max_requests=int(rate_limit.max_requests * adjustment_factor),
            window_seconds=rate_limit.window_seconds,
            burst_allowance=int(rate_limit.burst_allowance * adjustment_factor)
        )
        
        return await self.base_limiter.check_rate_limit(key, adjusted_limit)

class RateLimitManager:
    """Main rate limit manager coordinating different limiters"""
    
    def __init__(self, use_redis: bool = False, redis_client: Optional[redis.Redis] = None):
        if use_redis:
            self.limiter = RedisRateLimiter(redis_client)
        else:
            base_limiter = InMemoryRateLimiter()
            self.limiter = AdaptiveRateLimiter(base_limiter)
        
        self.config = RateLimitConfig()
    
    async def check_limit(self, user_id: str, subscription_tier: SubscriptionTier, 
                         limit_type: RateLimitType, request: Optional[Request] = None) -> RateLimitResult:
        """Check if user is within rate limit for specific action"""
        # Get rate limit for user's subscription tier
        tier_limits = self.config.TIER_LIMITS.get(subscription_tier, self.config.TIER_LIMITS[SubscriptionTier.BASIC])
        rate_limit = tier_limits.get(limit_type)
        
        if not rate_limit:
            # No limit configured, allow request
            return RateLimitResult(
                allowed=True,
                remaining=999999,
                reset_time=datetime.utcnow() + timedelta(hours=1)
            )
        
        # Create unique key for this user and limit type
        key = f"rate_limit:{user_id}:{limit_type.value}"
        
        # Extract IP address if request is provided
        ip_address = None
        if request:
            ip_address = request.client.host if request.client else None
        
        # Check rate limit
        if isinstance(self.limiter, AdaptiveRateLimiter):
            result = await self.limiter.check_rate_limit(key, rate_limit, user_id, ip_address)
        else:
            result = await self.limiter.check_rate_limit(key, rate_limit)
        
        return result
    
    async def check_multiple_limits(self, user_id: str, subscription_tier: SubscriptionTier, 
                                  limit_types: list[RateLimitType], 
                                  request: Optional[Request] = None) -> Dict[RateLimitType, RateLimitResult]:
        """Check multiple rate limits at once"""
        results = {}
        
        for limit_type in limit_types:
            result = await self.check_limit(user_id, subscription_tier, limit_type, request)
            results[limit_type] = result
            
            # If any limit is exceeded, we can stop checking
            if not result.allowed:
                break
        
        return results
    
    def get_rate_limit_headers(self, result: RateLimitResult, limit_type: RateLimitType) -> Dict[str, str]:
        """Generate HTTP headers for rate limit information"""
        headers = {
            "X-RateLimit-Limit": str(result.current_usage + result.remaining),
            "X-RateLimit-Remaining": str(result.remaining),
            "X-RateLimit-Reset": str(int(result.reset_time.timestamp())),
            "X-RateLimit-Type": limit_type.value
        }
        
        if result.retry_after:
            headers["Retry-After"] = str(result.retry_after)
        
        return headers
    
    async def record_usage(self, user_id: str, limit_type: RateLimitType, amount: int = 1):
        """Record usage for tracking purposes (e.g., data upload amount)"""
        key = f"usage:{user_id}:{limit_type.value}:{datetime.utcnow().strftime('%Y-%m-%d-%H')}"
        
        if isinstance(self.limiter, RedisRateLimiter):
            self.limiter.redis.incrby(key, amount)
            self.limiter.redis.expire(key, 86400)  # Expire after 24 hours
        # For in-memory limiter, we could store in a separate dict if needed

# Global rate limit manager instance
rate_limit_manager = RateLimitManager(use_redis=False)

# Exception for rate limit exceeded
class RateLimitExceeded(HTTPException):
    def __init__(self, result: RateLimitResult, limit_type: RateLimitType):
        detail = {
            "error": "Rate limit exceeded",
            "limit_type": limit_type.value,
            "retry_after": result.retry_after,
            "reset_time": result.reset_time.isoformat(),
            "current_usage": result.current_usage
        }
        
        super().__init__(
            status_code=429,
            detail=detail,
            headers={
                "Retry-After": str(result.retry_after) if result.retry_after else "60"
            }
        )